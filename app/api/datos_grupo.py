from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.schemas.datos_grupo import DatosGrupoOut
from app.schemas.users import UserOut
from core.dependencies import get_current_user
from core.database import get_db
from app.crud import datos_grupo as crud_datos_grupo

router = APIRouter()

@router.get("/get-by-ficha/{cod_ficha}", response_model=DatosGrupoOut)
def get_datos_grupo_by_ficha(
    cod_ficha: int,
    db: Session = Depends(get_db),
    current_user: UserOut = Depends(get_current_user)
):
    if current_user.id_rol not in [1, 2, 3]:
        raise HTTPException(status_code=401, detail="Usuario no autorizado")

    try:
        result = crud_datos_grupo.get_datos_grupo(db, cod_ficha)
        if not result:
            raise HTTPException(status_code=404, detail="Datos de grupo no encontrados")
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
