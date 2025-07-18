from pydantic import BaseModel, Field

class ProgramaHorasUpdate(BaseModel):
    horas_lectivas: int = Field(..., ge=1)
    horas_productivas: int = Field(..., ge=1)

class ProgramaOut(BaseModel):
    cod_programa: int
    la_version: int
    nombre: str
    horas_lectivas: int
    horas_productivas: int
