from sqlalchemy.orm import Session
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
from app.schemas.grupo import GrupoEditableUpdate, GrupoAmbienteUpdate
from datetime import datetime, timedelta, time
import logging

logger = logging.getLogger(__name__)


def update_campos_editables_grupo(db: Session, cod_ficha: int, grupo_data: GrupoEditableUpdate) -> bool:
    try:
        data = grupo_data.model_dump(exclude_unset=True)

        # Convertir 0 a None si aplica
        if "id_ambiente" in data and data["id_ambiente"] == 0:
            data["id_ambiente"] = None

        if not data:
            return False

        set_clause = ", ".join([f"{k} = :{k}" for k in data])
        data["cod_ficha"] = cod_ficha

        query = text(f"""
            UPDATE grupo SET {set_clause}
            WHERE cod_ficha = :cod_ficha
        """)

        result = db.execute(query, data)
        db.commit()

        return result.rowcount > 0
    except SQLAlchemyError as e:
        db.rollback()
        logger.error(f"Error al actualizar grupo {cod_ficha}: {e}")
        raise Exception("Error de base de datos al actualizar grupo")




def get_grupo_by_cod_ficha(db: Session, cod_ficha: int):
    try:
        query = text("""
            SELECT cod_ficha, cod_centro, cod_programa, la_version,
                   estado_grupo, nombre_nivel, jornada, fecha_inicio, fecha_fin,
                   etapa, modalidad, responsable, nombre_empresa, nombre_municipio,
                   nombre_programa_especial, hora_inicio, hora_fin, id_ambiente
            FROM grupo
            WHERE cod_ficha = :cod_ficha
        """)
        raw_result = db.execute(query, {"cod_ficha": cod_ficha}).mappings().first()
        if not raw_result:
            return None

        result = dict(raw_result)

        for campo in ["hora_inicio", "hora_fin"]:
            if isinstance(result[campo], timedelta):
                result[campo] = (datetime.min + result[campo]).time()

        return result
    except SQLAlchemyError as e:
        logger.error(f"Error al obtener grupo: {e}")
        raise Exception("Error de base de datos al obtener el grupo")



def asignar_ambiente_grupo(db: Session, cod_ficha: int, ambiente_data: GrupoAmbienteUpdate) -> bool:
    try:
        query = text("""
            UPDATE grupo
            SET id_ambiente = :id_ambiente
            WHERE cod_ficha = :cod_ficha
        """)
        db.execute(query, {"id_ambiente": ambiente_data.id_ambiente, "cod_ficha": cod_ficha})
        db.commit()
        return True
    except SQLAlchemyError as e:
        db.rollback()
        logger.error(f"Error al asignar ambiente: {e}")
        raise Exception("Error de base de datos al asignar ambiente al grupo")
