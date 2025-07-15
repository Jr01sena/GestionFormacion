from sqlalchemy.orm import Session
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
from app.schemas.metas import MetaCreate, MetaUpdate
import logging

logger = logging.getLogger(__name__)

def create_meta(db: Session, meta: MetaCreate):
    try:
        query = text("""
            INSERT INTO metas (anio, cod_centro, concepto, valor)
            VALUES (:anio, :cod_centro, :concepto, :valor)
        """)
        db.execute(query, meta.model_dump())
        db.commit()
        return True
    except SQLAlchemyError as e:
        db.rollback()
        logger.error(f"Error al crear meta: {e}")
        raise

def update_meta(db: Session, id_meta: int, meta: MetaUpdate):
    try:
        fields = meta.model_dump(exclude_unset=True)
        if not fields:
            return False
        set_clause = ", ".join([f"{key} = :{key}" for key in fields])
        fields["id_meta"] = id_meta

        query = text(f"UPDATE metas SET {set_clause} WHERE id_meta = :id_meta")
        db.execute(query, fields)
        db.commit()
        return True
    except SQLAlchemyError as e:
        db.rollback()
        logger.error(f"Error al actualizar meta: {e}")
        raise

def get_meta_by_id(db: Session, id_meta: int):
    try:
        query = text("SELECT * FROM metas WHERE id_meta = :id")
        return db.execute(query, {"id": id_meta}).mappings().first()
    except SQLAlchemyError as e:
        logger.error(f"Error al obtener meta por ID: {e}")
        raise

def get_metas_by_centro(db: Session, cod_centro: int):
    try:
        query = text("SELECT * FROM metas WHERE cod_centro = :cod_centro")
        return db.execute(query, {"cod_centro": cod_centro}).mappings().all()
    except SQLAlchemyError as e:
        logger.error(f"Error al obtener metas por centro: {e}")
        raise

def delete_meta(db: Session, id_meta: int):
    try:
        query = text("DELETE FROM metas WHERE id_meta = :id")
        db.execute(query, {"id": id_meta})
        db.commit()
        return True
    except SQLAlchemyError as e:
        db.rollback()
        logger.error(f"Error al eliminar meta: {e}")
        raise
