from pydantic import BaseModel
from typing import List

class GrupoInstructorBase(BaseModel):
    cod_ficha: int
    id_instructor: int

class GrupoInstructorCreate(GrupoInstructorBase):
    pass

class GrupoInstructorUpdate(BaseModel):
    cod_ficha: int
    id_instructor_actual: int
    id_instructor_nuevo: int


class GrupoInstructorOut(GrupoInstructorBase):
    nombre_completo: str  
