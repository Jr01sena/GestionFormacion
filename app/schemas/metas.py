from pydantic import BaseModel, Field
from typing import Optional

class MetaBase(BaseModel):
    anio: int = Field(..., ge=2000, le=2100)
    cod_centro: int
    concepto: str = Field(..., min_length=3, max_length=100)
    valor: int = Field(..., ge=0)

class MetaCreate(MetaBase):
    pass

class MetaUpdate(BaseModel):
    anio: Optional[int] = Field(None, ge=2000, le=2100)
    cod_centro: Optional[int] = None
    concepto: Optional[str] = Field(None, min_length=3, max_length=100)
    valor: Optional[int] = Field(None, ge=0)

class MetaOut(MetaBase):
    id_meta: int
