from sqlalchemy.orm import Session
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
import logging

logger = logging.getLogger(__name__)

def get_programa_competencia_by_id(db: Session, cod_prog_competencia: int):
    try:
        query = text("""
            SELECT pc.cod_prog_competencia,
                   pc.cod_programa,
                   pc.la_version,
                   pf.nombre AS nombre_programa,
                   pc.cod_competencia,
                   c.nombre AS nombre_competencia
            FROM programa_competencia pc
            JOIN programa_formacion pf ON pc.cod_programa = pf.cod_programa AND pc.la_version = pf.la_version
            JOIN competencia c ON pc.cod_competencia = c.cod_competencia
            WHERE pc.cod_prog_competencia = :cod
        """)
        result = db.execute(query, {"cod": cod_prog_competencia}).mappings().first()
        return result
    except SQLAlchemyError as e:
        logger.error(f"Error al obtener programa_competencia por ID: {e}")
        raise Exception("Error de base de datos al obtener programa_competencia")


def get_programas_by_competencia(db: Session, cod_competencia: int):
    try:
        query = text("""
            SELECT pc.cod_prog_competencia,
                   pc.cod_programa,
                   pc.la_version,
                   pf.nombre AS nombre_programa,
                   pc.cod_competencia,
                   c.nombre AS nombre_competencia
            FROM programa_competencia pc
            JOIN programa_formacion pf ON pc.cod_programa = pf.cod_programa AND pc.la_version = pf.la_version
            JOIN competencia c ON pc.cod_competencia = c.cod_competencia
            WHERE pc.cod_competencia = :cod_competencia
        """)
        result = db.execute(query, {"cod_competencia": cod_competencia}).mappings().all()
        return result
    except SQLAlchemyError as e:
        logger.error(f"Error al obtener programas por competencia: {e}")
        raise Exception("Error de base de datos al obtener programas por competencia")
