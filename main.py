from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import auth, users
from app.api import ambiente
from app.api import cargar_archivos
from app.api import centro_formacion as centro


app = FastAPI()

# Incluir en el objeto app los routers
app.include_router(users.router, prefix="/users", tags=["users"])
app.include_router(auth.router, prefix="/access", tags=["login"])
app.include_router(ambiente.router, prefix="/ambiente", tags=["Ambiente formación"])
app.include_router(cargar_archivos.router, prefix="/archivos", tags=["Cargar archivos"])
app.include_router(centro.router, prefix="/centro", tags=["Centro formación"])

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