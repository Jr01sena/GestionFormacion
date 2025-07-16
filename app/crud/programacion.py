from sqlalchemy.orm import Session
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
from datetime import datetime, timedelta, time

from app.schemas.programacion import ProgramacionCreate, ProgramacionUpdate
import logging

logger = logging.getLogger(__name__)


def validar_resultado_vs_competencia(db: Session, cod_competencia: int, cod_resultado: int):
    query = text("""
        SELECT 1 FROM resultado_aprendizaje
        WHERE cod_resultado = :cod_resultado AND cod_competencia = :cod_competencia
    """)
    result = db.execute(query, {"cod_resultado": cod_resultado, "cod_competencia": cod_competencia}).first()
    return result is not None


def calcular_diferencia_horas(hora_inicio, hora_fin):
    hoy = datetime.today().date()
    delta = datetime.combine(hoy, hora_fin) - datetime.combine(hoy, hora_inicio)
    return delta.total_seconds() / 3600


def convertir_a_time(result_dict):
    for key in ["hora_inicio", "hora_fin"]:
        valor = result_dict.get(key)
        if isinstance(valor, timedelta):
            segundos = int(valor.total_seconds())
            horas = segundos // 3600
            minutos = (segundos % 3600) // 60
            segundos_restantes = segundos % 60
            result_dict[key] = time(horas, minutos, segundos_restantes)
    return result_dict


def create_programacion(db: Session, data: ProgramacionCreate, id_user: int):
    if not validar_resultado_vs_competencia(db, data.cod_competencia, data.cod_resultado):
        raise ValueError("El resultado de aprendizaje no pertenece a la competencia indicada.")

    diferencia = calcular_diferencia_horas(data.hora_inicio, data.hora_fin)
    if data.horas_programadas > diferencia:
        raise ValueError("Horas programadas no pueden exceder el rango entre hora_inicio y hora_fin.")

    query = text("""
        INSERT INTO programacion (
            id_instructor, cod_ficha, fecha_programada,
            horas_programadas, hora_inicio, hora_fin,
            cod_competencia, cod_resultado, id_user
        ) VALUES (
            :id_instructor, :cod_ficha, :fecha_programada,
            :horas_programadas, :hora_inicio, :hora_fin,
            :cod_competencia, :cod_resultado, :id_user
        )
    """)
    db.execute(query, {**data.model_dump(), "id_user": id_user})
    db.commit()
    return True


def update_programacion(db: Session, id_programacion: int, data: ProgramacionUpdate, current_user):
    query_get = text("SELECT * FROM programacion WHERE id_programacion = :id")
    programacion = db.execute(query_get, {"id": id_programacion}).mappings().first()
    if not programacion:
        raise ValueError("Programación no encontrada.")

    if current_user.id_rol == 3 and (
        programacion["id_user"] != current_user.id_usuario and
        programacion["id_instructor"] != current_user.id_usuario
    ):
        raise PermissionError("No autorizado para actualizar esta programación.")

    fields = data.model_dump(exclude_unset=True)
    if not fields:
        return False

    if "hora_inicio" in fields and "hora_fin" in fields:
        if fields["hora_fin"] <= fields["hora_inicio"]:
            raise ValueError("hora_fin debe ser mayor que hora_inicio.")
        diferencia = calcular_diferencia_horas(fields["hora_inicio"], fields["hora_fin"])
        if "horas_programadas" in fields and fields["horas_programadas"] > diferencia:
            raise ValueError("Horas programadas exceden el rango permitido.")
    elif "horas_programadas" in fields and "hora_inicio" in programacion and "hora_fin" in programacion:
        diferencia = calcular_diferencia_horas(programacion["hora_inicio"], programacion["hora_fin"])
        if fields["horas_programadas"] > diferencia:
            raise ValueError("Horas programadas exceden el rango permitido.")

    if "cod_competencia" in fields or "cod_resultado" in fields:
        cod_competencia = fields.get("cod_competencia", programacion["cod_competencia"])
        cod_resultado = fields.get("cod_resultado", programacion["cod_resultado"])
        if not validar_resultado_vs_competencia(db, cod_competencia, cod_resultado):
            raise ValueError("El resultado no pertenece a la competencia.")

    set_clause = ", ".join([f"{key} = :{key}" for key in fields])
    fields["id"] = id_programacion
    query_update = text(f"UPDATE programacion SET {set_clause} WHERE id_programacion = :id")
    db.execute(query_update, fields)
    db.commit()
    return True



def get_programacion_by_id(db: Session, id_programacion: int, current_user):
    query = text("""
        SELECT progamacion.*, 
               usuario.nombre_completo AS nombre_instructor,
               competencia.nombre AS nombre_competencia,
               resultado_aprendizaje.nombre AS nombre_resultado
        FROM programacion
        JOIN usuario ON progamacion.id_instructor = usuario.id_usuario
        JOIN competencia ON progamacion.cod_competencia = competencia.cod_competencia
        JOIN resultado_aprendizaje ON progamacion.cod_resultado = resultado_aprendizaje.cod_resultado
        WHERE progamacion.id_programacion = :id
    """)
    result = db.execute(query, {"id": id_programacion}).mappings().first()
    if not result:
        return None
    if current_user.id_rol == 3 and result["id_user"] != current_user.id_usuario:
        raise PermissionError("No autorizado para consultar esta programación.")
    return convertir_a_time(dict(result))


def get_all_programaciones(db: Session, filtros: dict):
    condiciones = []
    params = {}

    if "cod_ficha" in filtros:
        condiciones.append("programacion.cod_ficha = :cod_ficha")
        params["cod_ficha"] = filtros["cod_ficha"]

    if "id_instructor" in filtros:
        condiciones.append("programacion.id_instructor = :id_instructor")
        params["id_instructor"] = filtros["id_instructor"]

    if "cod_centro" in filtros:
        condiciones.append("usuario.cod_centro = :cod_centro")
        params["cod_centro"] = filtros["cod_centro"]

    if "fecha_programada" in filtros:
        condiciones.append("programacion.fecha_programada = :fecha_programada")
        params["fecha_programada"] = filtros["fecha_programada"]

    where_clause = " AND ".join(condiciones)
    where_clause = f"WHERE {where_clause}" if where_clause else ""

    query = text(f"""
        SELECT programacion.*, 
               usuario.nombre_completo AS nombre_instructor,
               competencia.nombre AS nombre_competencia,
               resultado_aprendizaje.nombre AS nombre_resultado
        FROM programacion
        JOIN usuario ON programacion.id_instructor = usuario.id_usuario
        JOIN competencia ON programacion.cod_competencia = competencia.cod_competencia
        JOIN resultado_aprendizaje ON programacion.cod_resultado = resultado_aprendizaje.cod_resultado
        {where_clause}
        ORDER BY programacion.fecha_programada DESC
    """)
    resultados = db.execute(query, params).mappings().all()
    return [convertir_a_time(dict(r)) for r in resultados]


def get_own_programaciones(db: Session, id_usuario: int):
    query = text("""
        SELECT programacion.*,
               usuario.nombre_completo AS nombre_instructor,
               competencia.nombre AS nombre_competencia,
               resultado_aprendizaje.nombre AS nombre_resultado
        FROM programacion
        LEFT JOIN usuario ON programacion.id_instructor = usuario.id_usuario
        LEFT JOIN competencia ON programacion.cod_competencia = competencia.cod_competencia
        LEFT JOIN resultado_aprendizaje ON programacion.cod_resultado = resultado_aprendizaje.cod_resultado
        WHERE programacion.id_user = :id_usuario OR programacion.id_instructor = :id_usuario
        ORDER BY programacion.fecha_programada DESC
    """)
    resultados = db.execute(query, {"id_usuario": id_usuario}).mappings().all()

    # Si usas hora_inicio y hora_fin como timedelta, convertir a time
    from datetime import timedelta, time
    def convertir_a_time(row: dict) -> dict:
        for campo in ["hora_inicio", "hora_fin"]:
            if isinstance(row.get(campo), timedelta):
                td = row[campo]
                row[campo] = time(td.seconds // 3600, (td.seconds // 60) % 60)
        return row

    return [convertir_a_time(dict(r)) for r in resultados]
