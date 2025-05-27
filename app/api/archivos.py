# Mapeo de Columnas
column_maping = {
    "IDENTIFICACION_FICHA": "cod_ficha", # INT
    "CODIGO_CENTRO": "cod_centro", # INT
    "CODIGO_PROGRAMA": "cod_programa", # INT
    "ESTADO_CURSO": "estado_grupo", # VARCHAR
}

column_mapping_grupo = {
    "IDENTIFICADOR_FICHA": "cod_ficha",  # INT
    "CODIGO_CENTRO": "cod_centro",  # INT
    "CODIGO_PROGRAMA": "cod_programa",  # INT
    "VERSION_PROGRAMA": "la_version",  # TINYINT
    "ESTADO_CURSO": "estado_grupo",  # VARCHAR(30)
    "NIVEL_FORMACION": "nombre_nivel",  # VARCHAR(40)
    "NOMBRE_JORNADA": "jornada",  # VARCHAR(15)
    "FECHA_INICIO_FICHA": "fecha_inicio",  # DATE
    "FECHA_TERMINACION_FICHA": "fecha_fin",  # DATE
    "ETAPA_FICHA": "etapa",  # VARCHAR(20)
    "MODALIDAD_FORMACION": "modalidad",  # VARCHAR(30)
    "NOMBRE_RESPONSABLE": "responsable",  # VARCHAR(60)
    "NOMBRE_EMPRESA": "nombre_empresa",  # VARCHAR(40)
    "NOMBRE_MUNICIPIO_CURSO": "nombre_municipio",  # VARCHAR(30)
    "NOMBRE_PROGRAMA_ESPECIAL": "nombre_programa_especial",  # VARCHAR(60)
    # "hora_inicio" y "hora_fin" no están explícitos en el Excel, omitir o asignar por defecto
    # "aula_actual": no aparece en el Excel
    "IDENTIFICADOR_FICHA": "cod_ficha",  # INT
    "TOTAL_APRENDICES_MASCULINOS": "num_aprendices_masculinos",  # TINYINT
    "TOTAL_APRENDICES_FEMENINOS": "num_aprendices_femenino",  # TINYINT
    "TOTAL_APRENDICES_NOBINARIO": "num_aprendices_no_binario",  # TINYINT
    "TOTAL_APRENDICES": "num_total_aprendices",  # TINYINT
    "TOTAL_APRENDICES_ACTIVOS": "num_total_aprendices_activos",  # TINYINT
    # Otros campos como `cupo_total`, `en_transito`, etc. no están en el Excel
}
