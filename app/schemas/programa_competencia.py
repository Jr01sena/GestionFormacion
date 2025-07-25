from pydantic import BaseModel
from typing import Optional

class ProgramaCompetenciaOut(BaseModel):
    cod_prog_competencia: int
    cod_programa: int
    la_version: int
    nombre_programa: str
    cod_competencia: int
    nombre_competencia: str
    horas: int

    class Config:
        orm_mode = True
