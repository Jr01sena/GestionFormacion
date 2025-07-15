from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas.programa_formacion import ProgramaHorasUpdate, ProgramaOut
from app.schemas.users import UserOut
from app.crud import programa_formacion as crud_programa
from core.dependencies import get_current_user
from core.database import get_db
from typing import List

router = APIRouter()

@router.get("/{cod_programa}/{la_version}", response_model=ProgramaOut)
def get_programa(
    cod_programa: int,
    la_version: int,
    db: Session = Depends(get_db),
    current_user: UserOut = Depends(get_current_user)
):
    if current_user.id_rol not in [1, 2, 3]:
        raise HTTPException(status_code=401, detail="No autorizado")
    
    programa = crud_programa.get_programa(db, cod_programa, la_version)
    if not programa:
        raise HTTPException(status_code=404, detail="Programa no encontrado")
    
    return programa


@router.get("/{cod_programa}", response_model=List[ProgramaOut])
def get_programa_general(
    cod_programa: int,
    db: Session = Depends(get_db),
    current_user: UserOut = Depends(get_current_user)
):
    if current_user.id_rol not in [1, 2, 3]:
        raise HTTPException(status_code=401, detail="No autorizado")
    
    programas = crud_programa.get_programa_general(db, cod_programa)
    if not programas:
        raise HTTPException(status_code=404, detail="No se encontraron versiones del programa")
    
    return programas


@router.put("/editar/{cod_programa}/{la_version}")
def editar_horas_programa(
    cod_programa: int,
    la_version: int,
    data: ProgramaHorasUpdate,
    db: Session = Depends(get_db),
    current_user: UserOut = Depends(get_current_user)
):
    if current_user.id_rol not in [1, 2]:
        raise HTTPException(status_code=401, detail="No autorizado para editar")
    
    success = crud_programa.update_horas_programa(db, cod_programa, la_version, data)
    if not success:
        raise HTTPException(status_code=400, detail="No se pudo actualizar el programa")
    
    return {"message": "Programa actualizado correctamente"}
