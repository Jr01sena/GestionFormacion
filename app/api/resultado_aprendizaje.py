from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.schemas.resultado_aprendizaje import ResultadoAprendizajeOut
from app.schemas.users import UserOut
from core.dependencies import get_current_user
from core.database import get_db
from app.crud import resultado_aprendizaje as crud_resultado

router = APIRouter()

@router.get("/get-by-cod-resultado/{cod_resultado}", response_model=ResultadoAprendizajeOut)
def get_resultado_by_cod_resultado(
    cod_resultado: int,
    db: Session = Depends(get_db),
    current_user: UserOut = Depends(get_current_user)
):
    if current_user.id_rol not in [1, 2, 3]:
        raise HTTPException(status_code=401, detail="Usuario no autorizado")

    try:
        result = crud_resultado.get_resultado_by_id(db, cod_resultado)
        if not result:
            raise HTTPException(status_code=404, detail="Resultado de aprendizaje no encontrado")
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/get-by-cod-competencia/{cod_competencia}", response_model=List[ResultadoAprendizajeOut])
def get_resultados_by_cod_competencia(
    cod_competencia: int,
    db: Session = Depends(get_db),
    current_user: UserOut = Depends(get_current_user)
):
    if current_user.id_rol not in [1, 2, 3]:
        raise HTTPException(status_code=401, detail="Usuario no autorizado")

    try:
        results = crud_resultado.get_resultados_by_competencia(db, cod_competencia)
        if not results:
            raise HTTPException(status_code=404, detail="No se encontraron resultados para esta competencia")
        return results
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
