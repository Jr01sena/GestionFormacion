from sqlalchemy.orm import Session
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
import logging

logger = logging.getLogger(__name__)

def get_programa_competencia_by_id(db: Session, cod_prog_competencia: int):
    try:
        query = text("""
            SELECT programa_competencia.cod_prog_competencia,
                   programa_competencia.cod_programa,
                   programa_competencia.la_version,
                   programa_formacion.nombre AS nombre_programa,
                   programa_competencia.cod_competencia,
                   competencia.nombre AS nombre_competencia
            FROM programa_competencia
            JOIN programa_formacion ON programa_competencia.cod_programa = programa_formacion.cod_programa AND programa_competencia.la_version = programa_formacion.la_version
            JOIN competencia ON programa_competencia.cod_competencia = competencia.cod_competencia
            WHERE programa_competencia.cod_prog_competencia = :cod
        """)
        result = db.execute(query, {"cod": cod_prog_competencia}).mappings().first()
        return result
    except SQLAlchemyError as e:
        logger.error(f"Error al obtener programa_competencia por ID: {e}")
        raise Exception("Error de base de datos al obtener programa_competencia")


def get_programas_by_competencia(db: Session, cod_competencia: int):
    try:
        query = text("""
            SELECT programa_competencia.cod_prog_competencia,
                   programa_competencia.cod_programa,
                   programa_competencia.la_version,
                   programa_formacion.nombre AS nombre_programa,
                   programa_competencia.cod_competencia,
                   competencia.nombre AS nombre_competencia
            FROM programa_competencia
            JOIN programa_formacion ON programa_competencia.cod_programa = programa_formacion.cod_programa AND programa_competencia.la_version = programa_formacion.la_version
            JOIN competencia ON programa_competencia.cod_competencia = competencia.cod_competencia
            WHERE programa_competencia.cod_competencia = :cod_competencia
        """)
        result = db.execute(query, {"cod_competencia": cod_competencia}).mappings().all()
        return result
    except SQLAlchemyError as e:
        logger.error(f"Error al obtener programas por competencia: {e}")
        raise Exception("Error de base de datos al obtener programas por competencia")
