from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from core.database import get_db
from core.dependencies import get_current_user
from app.schemas.users import UserOut
from datetime import date
from typing import List
from app.crud import festivo as crud_festivo
from app.schemas.festivo import FestivoOut
import holidays

router = APIRouter()

def authorize_admin(current_user: UserOut):
    if current_user.id_rol not in [1, 2, 3]:
        raise HTTPException(status_code=403, detail="Usuario no autorizado")

@router.post("/cargar-festivos")
def cargar_festivos_masivamente(
    db: Session = Depends(get_db),
    current_user: UserOut = Depends(get_current_user)
):
    authorize_admin(current_user)

    festivos_colombia = holidays.country_holidays("CO", years=range(date.today().year, 2031))
    fechas = sorted(list(festivos_colombia.keys()))

    crud_festivo.cargar_festivos(db, fechas)
    return {"message": f"{len(fechas)} festivos cargados correctamente hasta el 2030"}



@router.get("/get-all", response_model=List[FestivoOut])
def get_all_festivos(
    db: Session = Depends(get_db),
    current_user: UserOut = Depends(get_current_user)
):
    festivos = crud_festivo.get_all_festivos(db)
    return festivos


@router.get("/get-by-year/{anio}", response_model=List[FestivoOut])
def get_festivos_by_anio(
    anio: int,
    db: Session = Depends(get_db),
    current_user: UserOut = Depends(get_current_user)
):
    festivos = crud_festivo.get_festivos_por_anio(db, anio)
    return festivos
