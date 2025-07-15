from pydantic import BaseModel
from datetime import date

class FestivoBase(BaseModel):
    festivo: date

class FestivoCreate(FestivoBase):
    pass

class FestivoOut(FestivoBase):
    pass
