from sqlalchemy.orm import Session
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
import logging

from app.schemas.competencia import CompetenciaHorasUpdate

logger = logging.getLogger(__name__)

def get_competencia_by_id(db: Session, cod_competencia: int):
    try:
        query = text("""
            SELECT cod_competencia, nombre, horas
            FROM competencia
            WHERE cod_competencia = :id
        """)
        result = db.execute(query, {"id": cod_competencia}).mappings().first()
        return result
    except SQLAlchemyError as e:
        logger.error(f"Error al obtener competencia: {e}")
        raise Exception("Error de base de datos al obtener la competencia")

def update_horas_competencia(db: Session, cod_competencia: int, data: CompetenciaHorasUpdate):
    try:
        query = text("""
            UPDATE competencia SET horas = :horas
            WHERE cod_competencia = :id
        """)
        result = db.execute(query, {"horas": data.horas, "id": cod_competencia})
        db.commit()
        return result.rowcount > 0
    except SQLAlchemyError as e:
        db.rollback()
        logger.error(f"Error al actualizar competencia: {e}")
        raise Exception("Error de base de datos al actualizar competencia")