from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from core.dependencies import get_current_user
from core.database import get_db
from app.schemas.users import UserCreate, UserOut, UserUpdate
from app.crud import users as crud_users
from sqlalchemy.exc import SQLAlchemyError
from core.config import settings

router = APIRouter()

@router.post("/create", status_code=status.HTTP_201_CREATED)
def create_user(
    user: UserCreate, 
    db: Session = Depends(get_db),
    user_token: UserOut = Depends(get_current_user)
):
    if user_token.id_rol == 2:
        if user.id_rol == 1 or user.id_rol == 2:
            raise HTTPException(status_code=401, detail="Usuario no autorizado")

    if user_token.id_rol == 3:
        raise HTTPException(status_code=401, detail="Usuario no autorizado")
    try:
        user_validate = crud_users.get_user_by_email(db, user.correo)
        if user_validate:
            raise HTTPException(status_code=400, detail="Correo ya registrado")
        crud_users.create_user(db, user)
        return {"message": "Usuario creado correctamente"}
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/get-by-email", response_model=UserOut)
def get_user_by_email(email: str, db: Session = Depends(get_db)):
    try:
        user = crud_users.get_user_by_email(db, email)
        if not user:
            raise HTTPException(status_code=404, detail="Usuario no encontrado")
        return user
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router.get("/get-by-id", response_model=UserOut)
def get_user_by_id(id_usuario: int, db: Session = Depends(get_db)):
    try:
        user = crud_users.get_user_by_id(db, id_usuario)
        if not user:
            raise HTTPException(status_code=404, detail="Usuario no encontrado")
        return user
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/update/{user_id}")
def update_user(
    user_id: int, 
    user: UserUpdate, 
    db: Session = Depends(get_db),
    current_user: UserOut = Depends(get_current_user)
):
    if current_user.id_rol != 1:
        if current_user.id_usuario != user_id:
            if current_user.id_rol == 3:
                raise HTTPException(status_code=401, detail="Usuario no autorizado")
            if current_user.id_rol == 2:
                user_update = crud_users.get_user_by_id(db, user_id)
                if user_update.id_rol != 3:
                    raise HTTPException(status_code=401, detail="Usuario no autorizado")
    try:
        if user.correo is not None:
            user_validate = crud_users.get_user_by_email(db, user.correo)
            if user_validate:
                raise HTTPException(status_code=400, detail="Correo ya registrado")
            
        success = crud_users.update_user(db, user_id, user)
        if not success:
            raise HTTPException(status_code=400, detail="No se pudo actualizar el usuario")
        return {"message": "Usuario actualizado correctamente"}
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router.put("/modify-status/{user_id}")
def modify_status(
    user_id: int, 
    db: Session = Depends(get_db),
    current_user: UserOut = Depends(get_current_user)
):
    if current_user.id_rol != 1:
        if current_user.id_rol != 2:
            raise HTTPException(status_code=401, detail="Usuario no autorizado")
    try:
        user_validate = crud_users.get_user_by_id(db, user_id)
        if not user_validate:
            raise HTTPException(status_code=404, detail="Usuario no encontrado")

        crud_users.modify_status_user(db, user_id)
        
        return {"message": "Usuario actualizado correctamente"}
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router.get("/get-by-centro", response_model=List[UserOut])
def get_users_by_centro(
    cod_centro: int, 
    db: Session = Depends(get_db),
    current_user: UserOut = Depends(get_current_user)
):
    if current_user.id_rol != 1:
        if current_user.id_rol != 2:
            raise HTTPException(status_code=401, detail="Usuario no autorizado")
    
    try:
        users = crud_users.get_users_by_centro(db, cod_centro)
        if not users:
            raise HTTPException(status_code=404, detail="No se encontraron usuarios para este centro")
        return users
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=str(e))