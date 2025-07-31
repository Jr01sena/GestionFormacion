from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
import pandas as pd
import logging

logger = logging.getLogger(__name__)


def procesar_pe04(db: Session, df: pd.DataFrame):
    errores = []

    columnas_base = {
        "IDENTIFICADOR_FICHA": "cod_ficha",
        "CODIGO_CENTRO": "cod_centro",
        "CODIGO_PROGRAMA": "cod_programa",
        "VERSION_PROGRAMA": "la_version",
        "NOMBRE_PROGRAMA_FORMACION": "nombre",
        "ESTADO_CURSO": "estado_grupo",
        "NIVEL_FORMACION": "nombre_nivel",
        "NOMBRE_JORNADA": "jornada",
        "FECHA_INICIO_FICHA": "fecha_inicio",
        "FECHA_TERMINACION_FICHA": "fecha_fin",
        "ETAPA_FICHA": "etapa",
        "MODALIDAD_FORMACION": "modalidad",
        "NOMBRE_RESPONSABLE": "responsable",
        "NOMBRE_EMPRESA": "nombre_empresa",
        "NOMBRE_MUNICIPIO_CURSO": "nombre_municipio",
        "NOMBRE_PROGRAMA_ESPECIAL": "nombre_programa_especial",
        "TOTAL_APRENDICES_MASCULINOS": "num_aprendices_masculinos",
        "TOTAL_APRENDICES_FEMENINOS": "num_aprendices_femenino",
        "TOTAL_APRENDICES_NOBINARIO": "num_aprendices_no_binario",
        "TOTAL_APRENDICES": "num_total_aprendices",
        "TOTAL_APRENDICES_ACTIVOS": "num_total_aprendices_activos"
    }
    df = df.rename(columns=columnas_base)

    campos_clave = [
        "cod_ficha", "cod_centro", "cod_programa", "la_version",
        "nombre", "fecha_inicio", "fecha_fin"
    ]
    df = df.dropna(subset=campos_clave)

    # DEPURACIÓN: Verifica si la fila 3340 sigue en el DataFrame
    if 3340 in df.index:
        print("La fila 3340 sigue en el DataFrame después del dropna:")
        print(df.loc[3340])
    else:
        print("La fila 3340 fue eliminada por tener valores nulos en campos clave")

    for col in ["cod_ficha", "cod_centro", "cod_programa", "la_version"]:
        df[col] = pd.to_numeric(df[col], errors="coerce").astype("Int64")

    df["fecha_inicio"] = pd.to_datetime(df["fecha_inicio"], errors="coerce").dt.date
    df["fecha_fin"] = pd.to_datetime(df["fecha_fin"], errors="coerce").dt.date
    df["hora_inicio"] = "00:00:00"
    df["hora_fin"] = "00:00:00"

    # CONVERSIÓN IMPORTANTE
    df = df.where(pd.notnull(df), None)

    df_programas = df[["cod_programa", "la_version", "nombre"]].drop_duplicates()
    df_programas["horas_lectivas"] = 0
    df_programas["horas_productivas"] = 0

    sql_programa = text("""
        INSERT INTO programa_formacion (
            cod_programa, la_version, nombre, horas_lectivas, horas_productivas
        ) VALUES (
            :cod_programa, :la_version, :nombre, :horas_lectivas, :horas_productivas
        )
        ON DUPLICATE KEY UPDATE nombre = VALUES(nombre)
    """)

    for _, row in df_programas.iterrows():
        try:
            db.execute(sql_programa, row.to_dict())
        except SQLAlchemyError as e:
            logger.error(f"[PE04] Error programa: {e}")
            errores.append(str(e))

    df_grupo = df.drop(columns=["nombre"])
    sql_grupo = text("""
        INSERT INTO grupo (
            cod_ficha, cod_centro, cod_programa, la_version, estado_grupo,
            nombre_nivel, jornada, fecha_inicio, fecha_fin, etapa,
            modalidad, responsable, nombre_empresa, nombre_municipio,
            nombre_programa_especial, hora_inicio, hora_fin, id_ambiente
        ) VALUES (
            :cod_ficha, :cod_centro, :cod_programa, :la_version, :estado_grupo,
            :nombre_nivel, :jornada, :fecha_inicio, :fecha_fin, :etapa,
            :modalidad, :responsable, :nombre_empresa, :nombre_municipio,
            :nombre_programa_especial, :hora_inicio, :hora_fin, NULL
        )
        ON DUPLICATE KEY UPDATE estado_grupo=VALUES(estado_grupo)
    """)

    # 1. Inserta todos los grupos primero
    for _, row in df_grupo.iterrows():
        try:
            db.execute(sql_grupo, row.to_dict())
        except SQLAlchemyError as e:
            logger.error(f"[PE04] Error grupo {row['cod_ficha']}: {e}")
            errores.append(str(e))

    # 2. Inserta todos los datos_grupo después
    df_datos = df[[
        "cod_ficha", "num_aprendices_masculinos", "num_aprendices_femenino",
        "num_aprendices_no_binario", "num_total_aprendices", "num_total_aprendices_activos"
    ]]

    sql_datos = text("""
        INSERT INTO datos_grupo (
            cod_ficha, num_aprendices_masculinos, num_aprendices_femenino,
            num_aprendices_no_binario, num_total_aprendices, num_total_aprendices_activos
        ) VALUES (
            :cod_ficha, :num_aprendices_masculinos, :num_aprendices_femenino,
            :num_aprendices_no_binario, :num_total_aprendices, :num_total_aprendices_activos
        )
        ON DUPLICATE KEY UPDATE
            num_aprendices_masculinos = VALUES(num_aprendices_masculinos),
            num_aprendices_femenino = VALUES(num_aprendices_femenino),
            num_aprendices_no_binario = VALUES(num_aprendices_no_binario),
            num_total_aprendices = VALUES(num_total_aprendices),
            num_total_aprendices_activos = VALUES(num_total_aprendices_activos)
    """)

    for _, row in df_datos.iterrows():
        try:
            db.execute(sql_datos, row.to_dict())
        except SQLAlchemyError as e:
            logger.error(f"[PE04] Error datos_grupo cod_ficha={row['cod_ficha']}: {e}")
            errores.append(str(e))

    try:
        db.commit()
    except Exception as e:
        db.rollback()
        logger.critical(f"[PE04] Commit fallido: {e}")
        errores.append(str(e))

    return {"mensaje": "Carga PE-04 completada con errores" if errores else "Carga PE-04 exitosa", "errores": errores}


def procesar_df14a(db: Session, df: pd.DataFrame):
    errores = []

    # 1. Estandarizar encabezados
    df.columns = df.columns.str.strip().str.upper()

    # 2. Renombrar columnas clave al formato de la base de datos
    df = df.rename(columns={
        "FICHA": "cod_ficha",
        "CUPO": "cupo_total",
        "CERTIFICADO": "certificados",
        "TRASLADADO": "traslados",
        "RETIRO_VOLUNTARIO": "retiro_voluntario",
        "CANCELAMIENTO_VIRT_COMP": "cancelamiento_vit_comp",
        "DESERCION_VIRT_COMP": "desercion_vit_comp"
    })

    # 3. Convertir nombres a snake_case
    df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_")

    # 4. Validar existencia de cod_ficha
    if "cod_ficha" not in df.columns:
        logger.warning(f"Columnas encontradas en DF14A: {df.columns.tolist()}")
        return {"errores": ["DF14A no contiene 'cod_ficha'"]}

    df["cod_ficha"] = pd.to_numeric(df["cod_ficha"], errors="coerce").astype("Int64")

    # 5. Lista de campos esperados en la tabla datos_grupo
    campos_necesarios = [
        "cupo_total", "en_transito", "induccion", "formacion",
        "condicionado", "aplazado", "retiro_voluntario", "cancelado",
        "cancelamiento_vit_comp", "desercion_vit_comp", "por_certificar",
        "certificados", "traslados", "otro"
    ]

    # 6. Asegurar que todos los campos están presentes y convertidos
    for campo in campos_necesarios:
        if campo not in df.columns:
            df[campo] = 0  # columna faltante → rellenar con ceros
        df[campo] = pd.to_numeric(df[campo], errors="coerce").fillna(0).astype(int)

    # 7. Preparar sentencia SQL
    sql_update = text("""
        UPDATE datos_grupo SET
            cupo_total = :cupo_total,
            en_transito = :en_transito,
            induccion = :induccion,
            formacion = :formacion,
            condicionado = :condicionado,
            aplazado = :aplazado,
            retiro_voluntario = :retiro_voluntario,
            cancelado = :cancelado,
            cancelamiento_vit_comp = :cancelamiento_vit_comp,
            desercion_vit_comp = :desercion_vit_comp,
            por_certificar = :por_certificar,
            certificados = :certificados,
            traslados = :traslados,
            otro = :otro
        WHERE cod_ficha = :cod_ficha
    """)

    # 8. Ejecutar actualización fila por fila
    for _, row in df.iterrows():
        try:
            valores = row[["cod_ficha"] + campos_necesarios].to_dict()
            db.execute(sql_update, valores)
        except SQLAlchemyError as e:
            logger.error(f"[DF14A] Error actualizando cod_ficha={row['cod_ficha']}: {e}")
            errores.append(f"cod_ficha={row['cod_ficha']}: {e}")

    # 9. Confirmar cambios
    try:
        db.commit()
    except Exception as e:
        db.rollback()
        logger.critical(f"[DF14A] Commit fallido: {e}")
        errores.append(str(e))

    return {
        "mensaje": "Carga DF-14A completada con errores" if errores else "Carga DF-14A exitosa",
        "errores": errores
    }


def procesar_juicios_evaluacion(db: Session, df: pd.DataFrame):
    errores = []

    # 1. Extraer cod_programa y la_version desde metadatos
    try:
        cod_programa = None
        la_version = None

        for i in range(min(20, len(df))):
            for j in range(min(10, df.shape[1])):
                celda = str(df.iloc[i, j]).strip().lower()
                if "código" in celda and cod_programa is None:
                    for offset in range(1, 5):
                        valor = df.iloc[i, j + offset]
                        if pd.notna(valor):
                            cod_programa = int(str(valor).strip())
                            break
                elif "versión" in celda and la_version is None:
                    for offset in range(1, 5):
                        valor = df.iloc[i, j + offset]
                        if pd.notna(valor):
                            la_version = int(str(valor).strip())
                            break

        if cod_programa is None or la_version is None:
            raise ValueError("No se encontraron cod_programa o la_version en el archivo")

        existe = db.execute(text("""
            SELECT 1 FROM programa_formacion
            WHERE cod_programa = :cod_programa AND la_version = :la_version
        """), {"cod_programa": cod_programa, "la_version": la_version}).fetchone()

        if not existe:
            errores.append(f"El programa ({cod_programa}, versión {la_version}) no existe en programa_formacion")
            return {"errores": errores}

    except Exception as e:
        errores.append("No se pudo leer cod_programa o la_version: " + str(e))
        return {"errores": errores}

    # 2. Buscar dinámicamente fila con "Tipo de Documento"
    fila_encabezado = None
    for i in range(len(df)):
        fila = df.iloc[i, :5].astype(str).str.upper().str.strip().tolist()
        if "TIPO DE DOCUMENTO" in fila:
            fila_encabezado = i
            break

    if fila_encabezado is None:
        errores.append("No se encontró fila con encabezado 'Tipo de Documento'")
        return {"errores": errores}

    # 3. Asignar encabezado real
    df.columns = df.iloc[fila_encabezado]
    df = df.iloc[fila_encabezado + 1:].reset_index(drop=True)

    # 4. Estandarizar nombres de columnas
    df.columns = (
        df.columns
        .astype(str)
        .str.replace(r"[\r\n\t]+", " ", regex=True)
        .str.strip()
        .str.lower()
        .str.replace(" +", " ", regex=True)
    )

    # 5. Buscar columnas 'competencia' y 'resultado de aprendizaje'
    col_comp = next((c for c in df.columns if "competencia" in c), None)
    col_res = next((c for c in df.columns if "resultado" in c), None)

    if not col_comp or not col_res:
        errores.append(f"No se encontraron columnas válidas. Detectadas: {df.columns.tolist()}")
        return {"errores": errores}

    df = df[[col_comp, col_res]].dropna().drop_duplicates()

    # 6. Extraer códigos y nombres
    def extraer_codigo_y_nombre(texto):
        try:
            codigo, nombre = str(texto).split(" - ", 1)
            return int(codigo.strip()), nombre.strip()
        except Exception:
            return None, None

    competencias = {}
    resultados = []

    for _, row in df.iterrows():
        cod_comp, nombre_comp = extraer_codigo_y_nombre(row[col_comp])
        cod_res, nombre_res = extraer_codigo_y_nombre(row[col_res])

        if cod_comp is None or cod_res is None:
            errores.append(f"Fila inválida: competencia={row[col_comp]} / resultado={row[col_res]}")
            continue

        if cod_comp not in competencias:
            competencias[cod_comp] = nombre_comp

        resultados.append({
            "cod_resultado": cod_res,
            "nombre": nombre_res,
            "cod_competencia": cod_comp
        })

    # 7. Insertar en competencia
    sql_comp = text("""
        INSERT INTO competencia (cod_competencia, nombre, horas)
        VALUES (:cod_competencia, :nombre, 0)
        ON DUPLICATE KEY UPDATE cod_competencia = cod_competencia
    """)
    for cod, nombre in competencias.items():
        try:
            db.execute(sql_comp, {"cod_competencia": cod, "nombre": nombre})
        except SQLAlchemyError as e:
            logger.error(f"[JUICIOS] Error insertando competencia {cod}: {e}")
            errores.append(str(e))

    # 8. Insertar en resultado_aprendizaje
    sql_res = text("""
        INSERT INTO resultado_aprendizaje (cod_resultado, nombre, cod_competencia)
        VALUES (:cod_resultado, :nombre, :cod_competencia)
        ON DUPLICATE KEY UPDATE cod_resultado = cod_resultado
    """)
    for row in resultados:
        try:
            db.execute(sql_res, row)
        except SQLAlchemyError as e:
            logger.error(f"[JUICIOS] Error resultado {row['cod_resultado']}: {e}")
            errores.append(str(e))

    # 9. Insertar en programa_competencia
    sql_prog_comp = text("""
        INSERT INTO programa_competencia (cod_programa, la_version, cod_competencia)
        VALUES (:cod_programa, :la_version, :cod_competencia)
        ON DUPLICATE KEY UPDATE cod_competencia = cod_competencia
    """)
    for cod_comp in competencias:
        try:
            db.execute(sql_prog_comp, {
                "cod_programa": cod_programa,
                "la_version": la_version,
                "cod_competencia": cod_comp
            })
        except SQLAlchemyError as e:
            logger.error(f"[JUICIOS] Error programa_competencia cod_comp={cod_comp}: {e}")
            errores.append(str(e))

    # 10. Confirmar cambios
    try:
        db.commit()
    except Exception as e:
        db.rollback()
        logger.critical(f"[JUICIOS] Commit fallido: {e}")
        errores.append(str(e))

    return {
        "mensaje": "Carga de juicios completada con errores" if errores else "Carga de juicios exitosa",
        "errores": errores
    }
