from pydantic import BaseModel
from typing import Optional

class ResultadoAprendizajeOut(BaseModel):
    cod_resultado: int
    nombre: str
    cod_competencia: int

    class Config:
        orm_mode = True
