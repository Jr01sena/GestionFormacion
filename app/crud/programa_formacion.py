from sqlalchemy.orm import Session
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
from app.schemas.programa_formacion import ProgramaHorasUpdate
import logging

logger = logging.getLogger(__name__)

def get_programa(db: Session, cod_programa: int, la_version: int):
    try:
        query = text("""
            SELECT cod_programa, la_version, nombre, horas_lectivas, horas_productivas
            FROM programa_formacion
            WHERE cod_programa = :cod_programa AND la_version = :la_version
        """)
        result = db.execute(query, {
            "cod_programa": cod_programa,
            "la_version": la_version
        }).mappings().first()
        return result
    except SQLAlchemyError as e:
        logger.error(f"Error al consultar el programa: {e}")
        raise Exception("Error al consultar el programa")

def get_programa_general(db: Session, cod_programa: int):
    try:
        query = text("""
            SELECT cod_programa, la_version, nombre, horas_lectivas, horas_productivas
            FROM programa_formacion
            WHERE cod_programa = :cod_programa
            ORDER BY la_version DESC
        """)
        results = db.execute(query, {
            "cod_programa": cod_programa
        }).mappings().all()
        return results
    except SQLAlchemyError as e:
        logger.error(f"Error al consultar las versiones del programa: {e}")
        raise Exception("Error al consultar las versiones del programa")


def update_horas_programa(db: Session, cod_programa: int, la_version: int, data: ProgramaHorasUpdate) -> bool:
    try:
        query = text("""
            UPDATE programa_formacion
            SET horas_lectivas = :horas_lectivas,
                horas_productivas = :horas_productivas
            WHERE cod_programa = :cod_programa AND la_version = :la_version
        """)
        result = db.execute(query, {
            "cod_programa": cod_programa,
            "la_version": la_version,
            "horas_lectivas": data.horas_lectivas,
            "horas_productivas": data.horas_productivas
        })
        db.commit()
        return result.rowcount > 0
    except SQLAlchemyError as e:
        db.rollback()
        logger.error(f"Error al actualizar las horas del programa: {e}")
        raise Exception("Error al actualizar las horas del programa")
