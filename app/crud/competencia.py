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

def get_competencias_by_ficha(db: Session, cod_ficha: int):
    """Obtener competencias del programa de la ficha"""
    try:
        query = text("""
            SELECT c.cod_competencia, c.nombre, c.horas_programa
            FROM competencia c
            JOIN programa_competencia pc ON c.cod_competencia = pc.cod_competencia
            JOIN programa_formacion pf ON pc.cod_programa = pf.cod_programa 
                AND pc.la_version = pf.la_version
            JOIN dato_grupo dg ON pf.cod_programa = dg.cod_programa 
                AND pf.la_version = dg.la_version
            WHERE dg.cod_ficha = :cod_ficha
        """)
        return db.execute(query, {"cod_ficha": cod_ficha}).mappings().all()
    except SQLAlchemyError as e:
        logger.error(f"Error al obtener competencias por ficha: {e}")
        raise