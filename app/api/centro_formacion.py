from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas.centro_formacion import CentroCreate, CentroUpdate, CentroOut
from app.schemas.users import UserOut
from app.crud import centro_formacion as crud_centro
from core.database import get_db
from core.dependencies import get_current_user
from typing import List

router = APIRouter()

def authorize_admin(current_user: UserOut):
    if current_user.id_rol not in [1, 2]:
        raise HTTPException(status_code=403, detail="Usuario no autorizado")

@router.post("/create", status_code=201)
def create_centro(
    centro: CentroCreate,
    db: Session = Depends(get_db),
    current_user: UserOut = Depends(get_current_user)
):
    authorize_admin(current_user)
    crud_centro.create_centro(db, centro)
    return {"message": "Centro creado correctamente"}

@router.put("/update/{cod_centro}")
def update_centro(
    cod_centro: int,
    centro: CentroUpdate,
    db: Session = Depends(get_db),
    current_user: UserOut = Depends(get_current_user)
):
    authorize_admin(current_user)
    if not crud_centro.update_centro(db, cod_centro, centro):
        raise HTTPException(status_code=400, detail="No se pudo actualizar el centro")
    return {"message": "Centro actualizado correctamente"}

@router.get("/get-by-id/{cod_centro}", response_model=CentroOut)
def get_centro_by_id(cod_centro: int, db: Session = Depends(get_db)):
    centro = crud_centro.get_centro_by_id(db, cod_centro)
    if not centro:
        raise HTTPException(status_code=404, detail="Centro no encontrado")
    return centro

@router.get("/get-all", response_model=List[CentroOut])
def get_all_centros(
    db: Session = Depends(get_db),
    current_user: UserOut = Depends(get_current_user)
):
    return crud_centro.get_all_centros(db)
