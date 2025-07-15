from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.schemas.metas import MetaCreate, MetaUpdate, MetaOut
from app.schemas.users import UserOut
from app.crud import metas as crud_metas
from core.database import get_db
from core.dependencies import get_current_user
from typing import List

router = APIRouter()

def authorize_admin(current_user: UserOut):
    if current_user.id_rol not in [1, 2]:
        raise HTTPException(status_code=403, detail="Usuario no autorizado")

def authorize_view(current_user: UserOut):
    if current_user.id_rol not in [1, 2, 3]:
        raise HTTPException(status_code=403, detail="Usuario no autorizado")

@router.post("/create", status_code=201)
def create_meta(
    meta: MetaCreate,
    db: Session = Depends(get_db),
    current_user: UserOut = Depends(get_current_user)
):
    authorize_admin(current_user)
    crud_metas.create_meta(db, meta)
    return {"message": "Meta creada correctamente"}

@router.put("/update/{id_meta}")
def update_meta(
    id_meta: int,
    meta: MetaUpdate,
    db: Session = Depends(get_db),
    current_user: UserOut = Depends(get_current_user)
):
    authorize_admin(current_user)
    if not crud_metas.update_meta(db, id_meta, meta):
        raise HTTPException(status_code=400, detail="No se pudo actualizar la meta")
    return {"message": "Meta actualizada correctamente"}

@router.delete("/delete/{id_meta}")
def delete_meta(
    id_meta: int,
    db: Session = Depends(get_db),
    current_user: UserOut = Depends(get_current_user)
):
    authorize_admin(current_user)
    if not crud_metas.delete_meta(db, id_meta):
        raise HTTPException(status_code=404, detail="Meta no encontrada o no se pudo eliminar")
    return {"message": "Meta eliminada correctamente"}

@router.get("/get-by-id/{id_meta}", response_model=MetaOut)
def get_meta_by_id(
    id_meta: int,
    db: Session = Depends(get_db),
    current_user: UserOut = Depends(get_current_user)
):
    authorize_view(current_user)
    meta = crud_metas.get_meta_by_id(db, id_meta)
    if not meta:
        raise HTTPException(status_code=404, detail="Meta no encontrada")
    return meta

@router.get("/get-by-centro/{cod_centro}", response_model=List[MetaOut])
def get_metas_by_centro(
    cod_centro: int,
    db: Session = Depends(get_db),
    current_user: UserOut = Depends(get_current_user)
):
    authorize_view(current_user)
    return crud_metas.get_metas_by_centro(db, cod_centro)
