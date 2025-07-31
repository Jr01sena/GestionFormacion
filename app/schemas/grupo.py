from pydantic import BaseModel, Field, model_validator
from typing import Optional
from datetime import time, date

class GrupoEditableUpdate(BaseModel):
    hora_inicio: time
    hora_fin: time
    id_ambiente: Optional[int] = Field(default=None)

    @model_validator(mode="after")
    def validar_horas(self):
        if self.hora_inicio >= self.hora_fin:
            raise ValueError("La hora de inicio debe ser menor que la hora de fin y no pueden ser iguales.")
        return self

class GrupoOut(BaseModel):
    cod_ficha: int
    cod_centro: int
    cod_programa: int
    la_version: int
    estado_grupo: str
    nombre_nivel: str
    jornada: str
    fecha_inicio: Optional[date]  # ← ✅ Permitir None
    fecha_fin: Optional[date]
    etapa: str
    modalidad: str
    responsable: str
    nombre_empresa: Optional[str]  # ← ✅ Permitir None
    nombre_municipio: str
    nombre_programa_especial: Optional[str]  # ← ✅ Permitir None
    hora_inicio: Optional[time]
    hora_fin: Optional[time]
    id_ambiente: Optional[int]

    class Config:
        orm_mode = True
