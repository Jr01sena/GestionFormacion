from sqlalchemy.orm import Session
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
from app.schemas.grupo import GrupoEditableUpdate
from datetime import datetime, timedelta, time, date
from typing import Optional
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



def get_grupos_by_centro(db: Session, cod_centro: int, desde_fecha: Optional[date] = None):
    try:
        query = """
            SELECT cod_ficha, cod_centro, cod_programa, la_version,
                   estado_grupo, nombre_nivel, jornada, fecha_inicio, fecha_fin,
                   etapa, modalidad, responsable, nombre_empresa, nombre_municipio,
                   nombre_programa_especial, hora_inicio, hora_fin, id_ambiente
            FROM grupo
            WHERE cod_centro = :cod_centro
        """

        params = {"cod_centro": cod_centro}

        if desde_fecha:
            query += " AND fecha_inicio >= :desde_fecha"
            params["desde_fecha"] = desde_fecha

        query += " ORDER BY fecha_inicio DESC"

        raw_results = db.execute(text(query), params).mappings().all()
        
        grupos = []
        for row in raw_results:
            grupo = dict(row)
            for campo in ["hora_inicio", "hora_fin"]:
                if isinstance(grupo[campo], timedelta):
                    grupo[campo] = (datetime.min + grupo[campo]).time()
            grupos.append(grupo)

        return grupos

    except SQLAlchemyError as e:
        logger.error(f"Error al obtener grupos por centro y fecha: {e}")
        raise Exception("Error de base de datos al obtener grupos")

def estadisticas_por_modalidad_y_nivel(db: Session, cod_centro: Optional[int] = None):
    try:
        query = """
            SELECT modalidad, nombre_nivel, COUNT(*) AS cantidad
            FROM grupo
            WHERE 1=1
        """
        params = {}

        if cod_centro:
            query += " AND cod_centro = :cod_centro"
            params["cod_centro"] = cod_centro

        query += " GROUP BY modalidad, nombre_nivel"

        return db.execute(text(query), params).mappings().all()
    except SQLAlchemyError as e:
        logger.error(f"Error en estadisticas_por_modalidad_y_nivel: {e}")
        raise Exception("Error al obtener estadísticas")


def conteo_por_estado(db: Session, cod_centro: Optional[int] = None):
    try:
        query = """
            SELECT estado_grupo AS estado, COUNT(*) AS cantidad
            FROM grupo
            WHERE 1=1
        """
        params = {}

        if cod_centro:
            query += " AND cod_centro = :cod_centro"
            params["cod_centro"] = cod_centro

        query += " GROUP BY estado_grupo"

        return db.execute(text(query), params).mappings().all()
    except SQLAlchemyError as e:
        logger.error(f"Error en conteo_por_estado: {e}")
        raise Exception("Error al obtener conteo por estado")
