from pydantic import BaseModel, Field
from typing import List
from datetime import date

class GrupoInstructorBase(BaseModel):
    cod_ficha: int
    id_instructor: int

class GrupoInstructorCreate(GrupoInstructorBase):
    fecha_asignacion: date = Field(default_factory=date.today)

class GrupoInstructorUpdate(BaseModel):
    cod_ficha: int
    id_instructor_actual: int
    id_instructor_nuevo: int
    fecha_asignacion: date = Field(default_factory=date.today)

class GrupoInstructorOut(GrupoInstructorBase):
    nombre_completo: str
    fecha_asignacion: date

class FichaOut(BaseModel):
    cod_ficha: int
    
    class Config:
        orm_mode = True

class CompetenciaOut(BaseModel):
    cod_competencia: int
    nombre: str
    horas_programa: int
    
    class Config:
        orm_mode = True