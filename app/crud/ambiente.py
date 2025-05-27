from sqlalchemy.orm import Session
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
from app.schemas.ambiente import AmbienteCreate, AmbienteUpdate
import logging

logger = logging.getLogger(__name__)

def create_ambiente(db: Session, ambiente: AmbienteCreate):
    try:
        query = text("""
            INSERT INTO ambiente_formacion (
                nombre_ambiente, num_max_aprendices, municipio,
                ubicacion, cod_centro, estado
            ) VALUES (
                :nombre_ambiente, :num_max_aprendices, :municipio,
                :ubicacion, :cod_centro, :estado
            )
        """)
        db.execute(query, ambiente.model_dump())
        db.commit()
        return True
    except SQLAlchemyError as e:
        db.rollback()
        logger.error(f"Error al crear ambiente: {e}")
        raise

def update_ambiente(db: Session, ambiente_id: int, ambiente: AmbienteUpdate):
    try:
        fields = ambiente.model_dump(exclude_unset=True)
        if not fields:
            return False
        set_clause = ", ".join([f"{key} = :{key}" for key in fields])
        fields["id_ambiente"] = ambiente_id

        query = text(f"UPDATE ambiente_formacion SET {set_clause} WHERE id_ambiente = :id_ambiente")
        db.execute(query, fields)
        db.commit()
        return True
    except SQLAlchemyError as e:
        db.rollback()
        logger.error(f"Error al actualizar ambiente: {e}")
        raise

def get_ambiente_by_id(db: Session, ambiente_id: int):
    try:
        query = text("SELECT * FROM ambiente_formacion WHERE id_ambiente = :id")
        return db.execute(query, {"id": ambiente_id}).mappings().first()
    except SQLAlchemyError as e:
        logger.error(f"Error al obtener ambiente por ID: {e}")
        raise

def get_ambientes_by_centro(db: Session, cod_centro: int):
    try:
        query = text("""
            SELECT * FROM ambiente_formacion
            WHERE cod_centro = :cod_centro AND estado = TRUE
        """)
        return db.execute(query, {"cod_centro": cod_centro}).mappings().all()
    except SQLAlchemyError as e:
        logger.error(f"Error al obtener ambientes por centro: {e}")
        raise

def cambiar_estado_ambiente(db: Session, ambiente_id: int):
    try:
        query = text("""
            UPDATE ambiente_formacion SET estado = IF(estado, FALSE, TRUE)
            WHERE id_ambiente = :id
        """)
        db.execute(query, {"id": ambiente_id})
        db.commit()
        return True
    except SQLAlchemyError as e:
        db.rollback()
        logger.error(f"Error al cambiar estado de ambiente: {e}")
        raise
