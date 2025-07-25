from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from typing import List, Optional

from app.schemas.programacion import ProgramacionCreate, ProgramacionUpdate, ProgramacionOut
from app.schemas.users import UserOut
from app.crud import programacion as crud_programacion
from core.dependencies import get_current_user
from core.database import get_db

router = APIRouter()


@router.post("/create", status_code=status.HTTP_201_CREATED)
def create_programacion(
    prog: ProgramacionCreate,
    db: Session = Depends(get_db),
    current_user: UserOut = Depends(get_current_user)
):
    try:
        if current_user.id_rol not in (1, 2, 3):
            raise HTTPException(status_code=403, detail="No autorizado")

        # Si el usuario es instructor, aseguramos que use su propio id
        if current_user.id_rol == 3:
            prog_data = prog.dict()
            prog_data["id_instructor"] = current_user.id_usuario
            prog = ProgramacionCreate(**prog_data)

        crud_programacion.create_programacion(db, prog, id_user=current_user.id_usuario)
        return {"message": "Programación creada correctamente"}

    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=str(e))



@router.put("/update/{id_programacion}", status_code=status.HTTP_200_OK)
def update_programacion(
    id_programacion: int,
    prog_update: ProgramacionUpdate,
    db: Session = Depends(get_db),
    current_user: UserOut = Depends(get_current_user)
):
    try:
        success = crud_programacion.update_programacion(db, id_programacion, prog_update, current_user)
        if not success:
            raise HTTPException(status_code=400, detail="No se pudo actualizar la programación")
        return {"message": "Programación actualizada correctamente"}
    except PermissionError as pe:
        raise HTTPException(status_code=403, detail=str(pe))
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/get-by-id/{id_programacion}", response_model=ProgramacionOut)
def get_programacion_by_id(
    id_programacion: int,
    db: Session = Depends(get_db),
    current_user: UserOut = Depends(get_current_user)
):
    try:
        result = crud_programacion.get_programacion_by_id(db, id_programacion, current_user)
        if not result:
            raise HTTPException(status_code=404, detail="Programación no encontrada")
        return result
    except PermissionError as pe:
        raise HTTPException(status_code=403, detail=str(pe))
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/get-all", response_model=List[ProgramacionOut])
def get_all_programacion(
    cod_ficha: Optional[int] = Query(None),
    id_instructor: Optional[int] = Query(None),
    cod_centro: Optional[int] = Query(None),
    fecha_programada: Optional[str] = Query(None),  # formato YYYY-MM-DD
    db: Session = Depends(get_db),
    current_user: UserOut = Depends(get_current_user)
):
    if current_user.id_rol not in (1, 2):
        raise HTTPException(status_code=403, detail="No autorizado")

    try:
        filtros = {
            "cod_ficha": cod_ficha,
            "id_instructor": id_instructor,
            "cod_centro": cod_centro,
            "fecha_programada": fecha_programada
        }
        filtros = {k: v for k, v in filtros.items() if v is not None}
        result = crud_programacion.get_all_programaciones(db, filtros)
        return result
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/get-own", response_model=List[ProgramacionOut])
def get_own_programacion(
    db: Session = Depends(get_db),
    current_user: UserOut = Depends(get_current_user)
):
    return crud_programacion.get_own_programaciones(db, current_user.id_usuario)

@router.get("/get-by-instructor/{id_instructor}", response_model=List[ProgramacionOut])
def get_by_instructor(
    id_instructor: int,
    db: Session = Depends(get_db),
    current_user: UserOut = Depends(get_current_user)
):
    # Instructores solo pueden ver su propia programación
    if current_user.id_rol == 3 and current_user.id_usuario != id_instructor:
        raise HTTPException(status_code=403, detail="No autorizado")

    try:
        return crud_programacion.get_programaciones_by_instructor(db, id_instructor)
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=str(e))

