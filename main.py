from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import auth, users
from app.api import ambiente
from app.api import cargar_archivos
from app.api import centro_formacion as centro
from app.api import grupo_instructor
from app.api import festivo
from app.api import metas
from app.api import grupo
from app.api import competencia
from app.api import programa_formacion as programa
from app.api import datos_grupo
from app.api import resultado_aprendizaje as resultado
from app.api import programa_competencia
from app.api import programacion

app = FastAPI()

# Incluir en el objeto app los routers
app.include_router(auth.router, prefix="/access", tags=["login"])
app.include_router(users.router, prefix="/users", tags=["users"])
app.include_router(centro.router, prefix="/centro", tags=["Centro formación"])
app.include_router(ambiente.router, prefix="/ambiente", tags=["Ambiente formación"])
app.include_router(cargar_archivos.router, prefix="/archivos", tags=["Cargar archivos"])
app.include_router(festivo.router, prefix="/festivos", tags=["Festivos"])
app.include_router(programa.router, prefix="/programa", tags=["Programa formación"])
app.include_router(competencia.router, prefix="/competencia", tags=["Competencias"]) 
app.include_router(resultado.router, prefix="/resultado-aprendizaje", tags=["Resultado Aprendizaje"])
app.include_router(programa_competencia.router, prefix="/programa-competencia", tags=["Programa Competencia"])
app.include_router(grupo.router, prefix="/grupo", tags=["Grupo formación"])
app.include_router(datos_grupo.router, prefix="/datos-grupo", tags=["Datos Grupo"])
app.include_router(grupo_instructor.router, prefix="/grupo-instructor", tags=["Grupo Instructor"])
app.include_router(programacion.router, prefix="/programacion", tags=["Programación"])
app.include_router(metas.router, prefix="/metas", tags=["Metas"])
    


# Configuración de CORS para permitir todas las solicitudes desde cualquier origen
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permitir solicitudes desde cualquier origen
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],  # Permitir estos métodos HTTP
    allow_headers=["*"],  # Permitir cualquier encabezado en las solicitudes
)

@app.get("/")
def read_root():
    return {
                "message": "ok",
                "autor": "ADSO 2847248"
            }