from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import text
from datetime import date
import logging

logger = logging.getLogger(__name__)

def cargar_festivos(db: Session, lista_festivos: list[date]):
    try:
        for festivo in lista_festivos:
            query = text("INSERT IGNORE INTO festivos (festivo) VALUES (:festivo)")
            db.execute(query, {"festivo": festivo})
        db.commit()
        return True
    except SQLAlchemyError as e:
        db.rollback()
        logger.error(f"Error al cargar festivos: {e}")
        raise

def get_all_festivos(db: Session):
    try:
        query = text("SELECT festivo FROM festivos ORDER BY festivo ASC")
        return db.execute(query).mappings().all()
    except SQLAlchemyError as e:
        logger.error(f"Error al obtener festivos: {e}")
        raise

def get_festivos_por_anio(db: Session, anio: int):
    try:
        query = text("""
            SELECT festivo FROM festivos
            WHERE YEAR(festivo) = :anio
            ORDER BY festivo ASC
        """)
        return db.execute(query, {"anio": anio}).mappings().all()
    except SQLAlchemyError as e:
        logger.error(f"Error al obtener festivos por año: {e}")
        raise
