from datetime import date
from sqlalchemy.orm import Session
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
import logging

from app.schemas.grupo_instructor import GrupoInstructorCreate

logger = logging.getLogger(__name__)

def create_grupo_instructor(db: Session, data: GrupoInstructorCreate):
    try:
        query = text("""
            INSERT INTO grupo_instructor (cod_ficha, id_instructor, fecha_asignacion)
            VALUES (:cod_ficha, :id_instructor, :fecha_asignacion)
        """)
        db.execute(query, data.model_dump())
        db.commit()
        return True
    except SQLAlchemyError as e:
        db.rollback()
        logger.error(f"Error al asignar instructor a ficha: {e}")
        raise


def update_grupo_instructor(db: Session, cod_ficha: int, id_actual: int, id_nuevo: int, fecha_asignacion: date) -> bool:
    try:
        query = text("""
            UPDATE grupo_instructor
            SET id_instructor = :id_nuevo, fecha_asignacion = :fecha_asignacion
            WHERE cod_ficha = :cod_ficha AND id_instructor = :id_actual
        """)
        result = db.execute(query, {
            "cod_ficha": cod_ficha,
            "id_actual": id_actual,
            "id_nuevo": id_nuevo,
            "fecha_asignacion": fecha_asignacion
        })
        db.commit()
        return result.rowcount > 0
    except SQLAlchemyError as e:
        db.rollback()
        logger.error(f"Error al actualizar asignación: {e}")
        raise



def delete_grupo_instructor(db: Session, cod_ficha: int, id_instructor: int):
    try:
        query = text("""
            DELETE FROM grupo_instructor
            WHERE cod_ficha = :cod_ficha AND id_instructor = :id_instructor
        """)
        result = db.execute(query, {"cod_ficha": cod_ficha, "id_instructor": id_instructor})
        db.commit()
        return result.rowcount > 0
    except SQLAlchemyError as e:
        db.rollback()
        logger.error(f"Error al eliminar asignación: {e}")
        raise

def get_instructores_by_ficha(db: Session, cod_ficha: int):
    try:
        query = text("""
            SELECT gi.cod_ficha, u.id_usuario AS id_instructor, u.nombre_completo, gi.fecha_asignacion      
            FROM grupo_instructor gi
            JOIN usuario u ON gi.id_instructor = u.id_usuario
            WHERE gi.cod_ficha = :cod_ficha
        """)
        return db.execute(query, {"cod_ficha": cod_ficha}).mappings().all()
    except SQLAlchemyError as e:
        logger.error(f"Error al obtener instructores por ficha: {e}")
        raise

def verificar_instructor_valido(db: Session, id_instructor: int) -> bool:
    try:
        query = text("""
            SELECT id_usuario FROM usuario
            WHERE id_usuario = :id AND id_rol = 3
        """)
        result = db.execute(query, {"id": id_instructor}).first()
        return result is not None
    except SQLAlchemyError as e:
        logger.error(f"Error al verificar rol de instructor: {e}")
        raise

def get_fichas_by_instructor(db: Session, id_instructor: int):
    """Obtener fichas donde el instructor está asignado"""
    try:
        query = text("""
            SELECT DISTINCT gi.cod_ficha
            FROM grupo_instructor gi
            WHERE gi.id_instructor = :id_instructor
        """)
        return db.execute(query, {"id_instructor": id_instructor}).mappings().all()
    except SQLAlchemyError as e:
        logger.error(f"Error al obtener fichas por instructor: {e}")
        raise
