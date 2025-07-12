from pydantic_settings import BaseSettings
from pydantic import model_validator
import os
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseSettings):
    PROJECT_NAME: str = "Gestión Formación"
    PROJECT_VERSION: str = "0.0.1"
    PROJECT_DESCRIPTION: str = "Aplicación para administrar la gestión de la información"

    # Configuración de la base de datos
    DB_HOST: str = os.getenv("DB_HOST", "localhost")
    DB_PORT: int = int(os.getenv("DB_PORT", "3306"))
    DB_USER: str = os.getenv("DB_USER", "root")
    DB_PASSWORD: str = os.getenv("DB_PASSWORD", "")
    DB_NAME: str = os.getenv("DB_NAME", "")

    DATABASE_URL: str = ""

    # Configuración JWT
    jwt_secret: str = os.getenv("JWT_SECRET")
    jwt_algorithm: str = os.getenv("JWT_ALGORITHM", "HS256")
    jwt_access_token_expire_minutes: int = int(os.getenv("JWT_ACCESS_TOKEN_EXPIRE_MINUTES", "30"))

    # Validaciones (con conversión correcta de string a bool)
    CREATE_USER_ADMIN_ADMIN: bool = os.getenv("CREATE_USER_ADMIN_ADMIN", "False").lower() == "true"
    CREATE_USER_ADMIN_INSTRU: bool = os.getenv("CREATE_USER_ADMIN_INSTRU", "False").lower() == "true"
    CREATE_USER_INSTRU: bool = os.getenv("CREATE_USER_INSTRU", "False").lower() == "true"

    @model_validator(mode="after")
    def validate_db(self) -> 'Settings':
        if not self.DB_NAME:
            raise ValueError("DB_NAME debe estar definido en el archivo .env")
        
        self.DATABASE_URL = (
            f"mysql+pymysql://{self.DB_USER}:{self.DB_PASSWORD}"
            f"@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
        )
        return self

    class Config:
        env_file = ".env"

settings = Settings()
