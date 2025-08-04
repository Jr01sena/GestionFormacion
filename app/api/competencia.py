from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from core.database import get_db
from core.dependencies import get_current_user
from app.schemas.users import UserOut
from app.schemas.competencia import CompetenciaHorasUpdate, CompetenciaOut
from typing import List
from app.crud import competencia as crud_competencia

router = APIRouter()

@router.get("/get-by-cod-ficha/{cod_competencia}", response_model=CompetenciaOut)
def get_competencia_by_cod_ficha(cod_competencia: int, db: Session = Depends(get_db), current_user: UserOut = Depends(get_current_user)):
    if current_user.id_rol not in [1, 2, 3]:
        raise HTTPException(status_code=401, detail="No autorizado")

    competencia = crud_competencia.get_competencia_by_id(db, cod_competencia)
    if not competencia:
        raise HTTPException(status_code=404, detail="Competencia no encontrada")
    return competencia


@router.put("/update/{cod_competencia}")
def update_horas_competencia(
    cod_competencia: int,
    data: CompetenciaHorasUpdate,
    db: Session = Depends(get_db),
    current_user: UserOut = Depends(get_current_user)
):
    if current_user.id_rol not in [1, 2]:
        raise HTTPException(status_code=401, detail="No autorizado")

    try:
        success = crud_competencia.update_horas_competencia(db, cod_competencia, data)
        if not success:
            raise HTTPException(status_code=400, detail="No se pudo actualizar la competencia")
        return {"message": "Competencia actualizada correctamente"}
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail="Error en la base de datos")

@router.get("/get-by-ficha/{cod_ficha}", response_model=List[CompetenciaOut])
def get_competencias_by_ficha(
    cod_ficha: int,
    db: Session = Depends(get_db),
    current_user: UserOut = Depends(get_current_user)
):
    if current_user.id_rol not in [1, 2, 3]:
        raise HTTPException(status_code=401, detail="No autorizado")
    """Obtener competencias asociadas a una ficha específica"""
    try:
        competencias = crud_competencia.get_competencias_by_ficha(db, cod_ficha)
        return competencias
    except SQLAlchemyError:
        raise HTTPException(status_code=500, detail="Error al obtener competencias")