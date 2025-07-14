from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from core.database import get_db
from core.dependencies import get_current_user
from app.schemas.users import UserOut
from app.schemas.grupo_instructor import GrupoInstructorCreate, GrupoInstructorOut
from app.crud import grupo_instructor as crud_grupo_instructor
from sqlalchemy.exc import SQLAlchemyError
from typing import List

router = APIRouter()

@router.post("/asignar", status_code=status.HTTP_201_CREATED)
def asignar_instructor(
    data: GrupoInstructorCreate,
    db: Session = Depends(get_db),
    current_user: UserOut = Depends(get_current_user)
):
    if current_user.id_rol not in [1, 2]:
        raise HTTPException(status_code=401, detail="Usuario no autorizado")

    # Validar que el instructor exista y tenga rol de instructor (id_rol = 3)
    if not crud_grupo_instructor.verificar_instructor_valido(db, data.id_instructor):
        raise HTTPException(
            status_code=400, 
            detail="El usuario asignado no es un instructor válido (id_rol ≠ 3)"
        )

    try:
        crud_grupo_instructor.create_grupo_instructor(db, data)
        return {"message": "Instructor asignado correctamente"}
    except SQLAlchemyError:
        raise HTTPException(status_code=500, detail="Error al asignar instructor")


@router.delete("/eliminar")
def eliminar_asignacion(
    cod_ficha: int,
    id_instructor: int,
    db: Session = Depends(get_db),
    current_user: UserOut = Depends(get_current_user)
):
    if current_user.id_rol not in [1, 2]:
        raise HTTPException(status_code=401, detail="Usuario no autorizado")

    try:
        registros = crud_grupo_instructor.get_instructores_by_ficha(db, cod_ficha)
        existe = any(reg["id_instructor"] == id_instructor for reg in registros)

        if not existe:
            raise HTTPException(status_code=404, detail="Asignación no encontrada")

        eliminado = crud_grupo_instructor.delete_grupo_instructor(db, cod_ficha, id_instructor)
        if not eliminado:
            raise HTTPException(status_code=400, detail="No se pudo eliminar la asignación")

        return {"message": "Asignación eliminada correctamente"}

    except SQLAlchemyError:
        raise HTTPException(status_code=500, detail="Error al eliminar asignación en base de datos")

@router.get("/instructores-ficha", response_model=List[GrupoInstructorOut])
def obtener_instructores(
    cod_ficha: int,
    db: Session = Depends(get_db),
    current_user: UserOut = Depends(get_current_user)
):
    try:
        return crud_grupo_instructor.get_instructores_by_ficha(db, cod_ficha)
    except SQLAlchemyError:
        raise HTTPException(status_code=500, detail="Error al obtener instructores")
