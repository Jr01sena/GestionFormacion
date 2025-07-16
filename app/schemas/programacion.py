from pydantic import BaseModel, Field, validator
from typing import Optional
from datetime import date, time


class ProgramacionBase(BaseModel):
    id_instructor: int
    cod_ficha: int
    fecha_programada: date
    horas_programadas: int = Field(..., ge=1)
    hora_inicio: time
    hora_fin: time
    cod_competencia: int
    cod_resultado: int

    @validator("hora_fin")
    def hora_fin_mayor_inicio(cls, v, values):
        if "hora_inicio" in values and v <= values["hora_inicio"]:
            raise ValueError("hora_fin debe ser mayor que hora_inicio")
        return v


class ProgramacionCreate(ProgramacionBase):
    pass


class ProgramacionUpdate(BaseModel):
    fecha_programada: Optional[date] = None
    horas_programadas: Optional[int] = Field(default=None, ge=1)
    hora_inicio: Optional[time] = None
    hora_fin: Optional[time] = None
    cod_competencia: Optional[int] = None
    cod_resultado: Optional[int] = None
    cod_ficha: Optional[int] = None

    @validator("hora_fin")
    def hora_fin_mayor_inicio(cls, v, values):
        hora_inicio = values.get("hora_inicio")
        if hora_inicio and v and v <= hora_inicio:
            raise ValueError("hora_fin debe ser mayor que hora_inicio")
        return v


class ProgramacionOut(BaseModel):
    id_programacion: int
    id_instructor: int
    nombre_instructor: str
    cod_ficha: int
    fecha_programada: date
    horas_programadas: int
    hora_inicio: time
    hora_fin: time
    cod_competencia: int
    nombre_competencia: str
    cod_resultado: int
    nombre_resultado: str
    id_user: int

    class Config:
        orm_mode = True
