from pydantic import BaseModel
from typing import Optional

class DatosGrupoOut(BaseModel):
    cod_ficha: int
    num_aprendices_masculinos: Optional[int]
    num_aprendices_femenino: Optional[int]
    num_aprendices_no_binario: Optional[int]
    num_total_aprendices: Optional[int]
    num_total_aprendices_activos: Optional[int]
    cupo_total: Optional[int]
    en_transito: Optional[int]
    induccion: Optional[int]
    formacion: Optional[int]
    condicionado: Optional[int]
    aplazado: Optional[int]
    retiro_voluntario: Optional[int]
    cancelado: Optional[int]
    cancelamiento_vit_comp: Optional[int]
    desercion_vit_comp: Optional[int]
    por_certificar: Optional[int]
    certificados: Optional[int]
    traslados: Optional[int]
    otro: Optional[int]

    class Config:
        orm_mode = True
