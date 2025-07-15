from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.schemas.programa_competencia import ProgramaCompetenciaOut
from app.schemas.users import UserOut
from core.dependencies import get_current_user
from core.database import get_db
from app.crud import programa_competencia as crud_pc

router = APIRouter(prefix="/programa-competencia", tags=["Programa Competencia"])

@router.get("/get-by-id/{cod_prog_competencia}", response_model=ProgramaCompetenciaOut)
def get_pc_by_id(
    cod_prog_competencia: int,
    db: Session = Depends(get_db),
    current_user: UserOut = Depends(get_current_user)
):
    if current_user.id_rol not in [1, 2, 3]:
        raise HTTPException(status_code=401, detail="Usuario no autorizado")

    try:
        result = crud_pc.get_programa_competencia_by_id(db, cod_prog_competencia)
        if not result:
            raise HTTPException(status_code=404, detail="Programa-competencia no encontrado")
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/get-by-competencia/{cod_competencia}", response_model=List[ProgramaCompetenciaOut])
def get_pcs_by_competencia(
    cod_competencia: int,
    db: Session = Depends(get_db),
    current_user: UserOut = Depends(get_current_user)
):
    if current_user.id_rol not in [1, 2, 3]:
        raise HTTPException(status_code=401, detail="Usuario no autorizado")

    try:
        results = crud_pc.get_programas_by_competencia(db, cod_competencia)
        if not results:
            raise HTTPException(status_code=404, detail="No se encontraron programas para esta competencia")
        return results
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
