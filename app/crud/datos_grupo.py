from sqlalchemy.orm import Session
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
import logging

logger = logging.getLogger(__name__)

def get_datos_grupo(db: Session, cod_ficha: int):
    try:
        query = text("""
            SELECT *
            FROM datos_grupo
            WHERE cod_ficha = :cod_ficha
        """)
        result = db.execute(query, {"cod_ficha": cod_ficha}).mappings().first()
        return result
    except SQLAlchemyError as e:
        logger.error(f"Error al obtener datos del grupo: {e}")
        raise Exception("Error de base de datos al obtener los datos del grupo")
