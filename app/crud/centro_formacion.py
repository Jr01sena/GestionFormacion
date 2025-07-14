from sqlalchemy.orm import Session
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
from app.schemas.centro_formacion import CentroCreate, CentroUpdate
import logging

logger = logging.getLogger(__name__)

def create_centro(db: Session, centro: CentroCreate):
    try:
        query = text("""
            INSERT INTO centro_formacion (
                cod_centro, nombre_centro, cod_regional
            ) VALUES (
                :cod_centro, :nombre_centro, :cod_regional
            )
        """)
        db.execute(query, centro.model_dump())
        db.commit()
        return True
    except SQLAlchemyError as e:
        db.rollback()
        logger.error(f"Error al crear centro: {e}")
        raise

def update_centro(db: Session, cod_centro: int, centro: CentroUpdate):
    try:
        fields = centro.model_dump(exclude_unset=True)
        if not fields:
            return False
        set_clause = ", ".join([f"{key} = :{key}" for key in fields])
        fields["cod_centro"] = cod_centro

        query = text(f"""
            UPDATE centro_formacion
            SET {set_clause}
            WHERE cod_centro = :cod_centro
        """)
        db.execute(query, fields)
        db.commit()
        return True
    except SQLAlchemyError as e:
        db.rollback()
        logger.error(f"Error al actualizar centro: {e}")
        raise

def get_centro_by_id(db: Session, cod_centro: int):
    try:
        query = text("""
            SELECT * FROM centro_formacion
            WHERE cod_centro = :id
        """)
        return db.execute(query, {"id": cod_centro}).mappings().first()
    except SQLAlchemyError as e:
        logger.error(f"Error al obtener centro por ID: {e}")
        raise

def get_all_centros(db: Session):
    try:
        query = text("SELECT * FROM centro_formacion")
        return db.execute(query).mappings().all()
    except SQLAlchemyError as e:
        logger.error(f"Error al obtener centros: {e}")
        raise
