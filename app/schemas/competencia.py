from pydantic import BaseModel, Field

class CompetenciaHorasUpdate(BaseModel):
    horas: int = Field(..., ge=1)


class CompetenciaOut(BaseModel):
    cod_competencia: int
    nombre: str
    horas: int
    
    class Config:
        orm_mode = True