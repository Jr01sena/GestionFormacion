from sqlalchemy.orm import Session
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
import logging

logger = logging.getLogger(__name__)

def get_resultado_by_id(db: Session, cod_resultado: int):
    try:
        query = text("""
            SELECT cod_resultado, nombre, cod_competencia
            FROM resultado_aprendizaje
            WHERE cod_resultado = :cod_resultado
        """)
        result = db.execute(query, {"cod_resultado": cod_resultado}).mappings().first()
        return result
    except SQLAlchemyError as e:
        logger.error(f"Error al obtener resultado_aprendizaje por ID: {e}")
        raise Exception("Error al obtener el resultado de aprendizaje")


def get_resultados_by_competencia(db: Session, cod_competencia: int):
    try:
        query = text("""
            SELECT cod_resultado, nombre, cod_competencia
            FROM resultado_aprendizaje
            WHERE cod_competencia = :cod_competencia
        """)
        result = db.execute(query, {"cod_competencia": cod_competencia}).mappings().all()
        return result
    except SQLAlchemyError as e:
        logger.error(f"Error al obtener resultados por competencia: {e}")
        raise Exception("Error al obtener resultados de aprendizaje por competencia")
