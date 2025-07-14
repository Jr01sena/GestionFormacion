from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.schemas.ambiente import AmbienteCreate, AmbienteUpdate, AmbienteOut
from app.schemas.users import UserOut
from app.crud import ambiente as crud_ambiente
from core.database import get_db
from core.dependencies import get_current_user
from typing import List

router = APIRouter()

def authorize_admin(current_user: UserOut):
    if current_user.id_rol not in [1, 2]:
        raise HTTPException(status_code=403, detail="Usuario no autorizado")

@router.post("/create", status_code=201)
def create_ambiente(
    ambiente: AmbienteCreate,
    db: Session = Depends(get_db),
    current_user: UserOut = Depends(get_current_user)
):
    authorize_admin(current_user)
    crud_ambiente.create_ambiente(db, ambiente)
    return {"message": "Ambiente creado correctamente"}

@router.put("/update/{ambiente_id}")
def update_ambiente(
    ambiente_id: int,
    ambiente: AmbienteUpdate,
    db: Session = Depends(get_db),
    current_user: UserOut = Depends(get_current_user)
):
    authorize_admin(current_user)
    if not crud_ambiente.update_ambiente(db, ambiente_id, ambiente):
        raise HTTPException(status_code=400, detail="No se pudo actualizar el ambiente")
    return {"message": "Ambiente actualizado correctamente"}

@router.get("/get-by-id/{ambiente_id}", response_model=AmbienteOut)
def get_ambiente_by_id(ambiente_id: int, db: Session = Depends(get_db)):
    ambiente = crud_ambiente.get_ambiente_by_id(db, ambiente_id)
    if not ambiente:
        raise HTTPException(status_code=404, detail="Ambiente no encontrado")
    return ambiente

@router.get("/get-by-centro/{cod_centro}", response_model=List[AmbienteOut])
def get_ambientes_by_centro(
    cod_centro: int,
    db: Session = Depends(get_db),
    current_user: UserOut = Depends(get_current_user)
):
    return crud_ambiente.get_ambientes_by_centro(db, cod_centro)

@router.put("/modify-status/{ambiente_id}")
def modify_estado_ambiente(
    ambiente_id: int,
    db: Session = Depends(get_db),
    current_user: UserOut = Depends(get_current_user)
):
    authorize_admin(current_user)
    crud_ambiente.cambiar_estado_ambiente(db, ambiente_id)
    return {"message": "Estado del ambiente modificado correctamente"}
