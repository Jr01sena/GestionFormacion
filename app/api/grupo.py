from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

from core.database import get_db
from core.dependencies import get_current_user
from app.schemas.users import UserOut
from app.schemas.grupo import GrupoEditableUpdate, GrupoOut, GrupoAmbienteUpdate
from app.crud import grupo as crud_grupo

router = APIRouter()


@router.get("/get-by-cod-ficha/{cod_ficha}", response_model=GrupoOut)
def get_grupo_by_cod_ficha(
    cod_ficha: int,
    db: Session = Depends(get_db),
    current_user: UserOut = Depends(get_current_user)
):
    if current_user.id_rol not in [1, 2]:
        raise HTTPException(status_code=401, detail="No autorizado")

    grupo = crud_grupo.get_grupo_by_cod_ficha(db, cod_ficha)
    if not grupo:
        raise HTTPException(status_code=404, detail="Grupo no encontrado")
    
    return grupo


@router.put("/update/{cod_ficha}")
def update_campos_editables_grupo(
    cod_ficha: int,
    grupo_data: GrupoEditableUpdate,
    db: Session = Depends(get_db),
    current_user: UserOut = Depends(get_current_user)
):
    if current_user.id_rol not in [1, 2]:
        raise HTTPException(status_code=401, detail="No autorizado")
    
    try:
        success = crud_grupo.update_campos_editables_grupo(db, cod_ficha, grupo_data)
        if not success:
            raise HTTPException(status_code=404, detail="Grupo no encontrado o no modificado")
        
        return {"message": "Grupo actualizado correctamente"}
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail="Error al actualizar el grupo en base de datos")


@router.put("/update-ambiente/{cod_ficha}")
def update_ambiente_grupo(
    cod_ficha: int,
    ambiente_data: GrupoAmbienteUpdate,
    db: Session = Depends(get_db),
    current_user: UserOut = Depends(get_current_user)
):
    if current_user.id_rol not in [1, 2]:
        raise HTTPException(status_code=401, detail="No autorizado para asignar ambientes")

    try:
        success = crud_grupo.asignar_ambiente_grupo(db, cod_ficha, ambiente_data)
        if not success:
            raise HTTPException(status_code=400, detail="No se pudo actualizar el ambiente del grupo")

        return {"message": "Ambiente asignado correctamente"}
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail="Error interno en la base de datos")
