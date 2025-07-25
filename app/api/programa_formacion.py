from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas.programa_formacion import PaginatedProgramas, ProgramaHorasUpdate, ProgramaOut
from app.schemas.users import UserOut
from app.crud import programa_formacion as crud_programa
from core.dependencies import get_current_user
from core.database import get_db
from typing import List, Dict, Any

router = APIRouter()

@router.get("/get-by-cod-programa-la-version/{cod_programa}/{la_version}", response_model=ProgramaOut)
def get_programa_by_cod_programa_la_version(
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


@router.get("/get-by-cod-programa/{cod_programa}", response_model=List[ProgramaOut])
def get_programas_by_cod_programa(
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


@router.put("/update/{cod_programa}/{la_version}")
def update_horas_programa(
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




@router.get("/get-all", response_model=PaginatedProgramas)
def get_all_programas(
    limit: int = 10,
    offset: int = 0,
    db: Session = Depends(get_db),
    current_user: UserOut = Depends(get_current_user)
) -> Dict[str, Any]:
    if current_user.id_rol not in [1, 2, 3]:
        raise HTTPException(status_code=401, detail="No autorizado")

    programas = crud_programa.get_all_programas(db=db, limit=limit, offset=offset)
    total = crud_programa.count_programas(db)

    return PaginatedProgramas(data=programas, total=total)


@router.get("/buscar")
def buscar_programas(nombre: str, db: Session = Depends(get_db), current_user: UserOut = Depends(get_current_user)):
    if current_user.id_rol not in [1, 2, 3]:
        raise HTTPException(status_code=401, detail="No autorizado")
    return crud_programa.buscar_por_nombre(db, nombre)
