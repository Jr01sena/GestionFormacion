from fastapi import APIRouter, UploadFile, File, Depends
from sqlalchemy.orm import Session
from io import BytesIO
import pandas as pd

from app.crud.cargar_archivos import procesar_pe04, procesar_df14a, procesar_juicios_evaluacion
from core.database import get_db

router = APIRouter()


@router.post("/upload-excel-pe04/")
async def upload_pe04(file: UploadFile = File(...), db: Session = Depends(get_db)):
    contents = await file.read()
    df = pd.read_excel(BytesIO(contents), engine="openpyxl", skiprows=4)
    return procesar_pe04(db, df)

@router.post("/upload-excel-df14a/")
async def upload_df14a(file: UploadFile = File(...), db: Session = Depends(get_db)):
    contents = await file.read()
    df = pd.read_excel(BytesIO(contents), engine="openpyxl", skiprows=4)
    return procesar_df14a(db, df)


@router.post("/upload-excel-juicios-evaluacion/")
async def upload_juicios_evaluacion(file: UploadFile = File(...), db: Session = Depends(get_db)):
    contents = await file.read()
    df = pd.read_excel(BytesIO(contents), engine="openpyxl")
    return procesar_juicios_evaluacion(db, df)


