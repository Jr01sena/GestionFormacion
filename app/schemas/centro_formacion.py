from pydantic import BaseModel, Field
from typing import Optional

class CentroBase(BaseModel):
    cod_centro: int  
    nombre_centro: str = Field(min_length=3, max_length=80)
    cod_regional: int

class CentroCreate(CentroBase):
    pass

class CentroUpdate(BaseModel):
    nombre_centro: Optional[str] = None
    cod_regional: Optional[int] = None

class CentroOut(CentroBase):
    pass
