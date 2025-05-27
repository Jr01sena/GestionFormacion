from sqlalchemy.orm import Session
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
from typing import Optional
import logging

from app.schemas.users import UserCreate, UserUpdate
from core.security import get_hashed_password

logger = logging.getLogger(__name__)

def create_user(db: Session, user: UserCreate) -> Optional[bool]:
    try:
        pass_hashed =  get_hashed_password(user.pass_hash)
        user_data = user.model_dump()
        user_data['pass_hash'] = pass_hashed
        query = text("""
            INSERT INTO usuario (
                nombre_completo, identificacion, id_rol,
                correo, pass_hash, tipo_contrato,
                telefono, estado, cod_centro
            ) VALUES (
                :nombre_completo, :identificacion, :id_rol,
                :correo, :pass_hash, :tipo_contrato,
                :telefono, :estado, :cod_centro
            )
        """)
        db.execute(query, user_data)
        db.commit()
        return True
    except SQLAlchemyError as e:
        db.rollback()
        logger.error(f"Error al crear usuario: {e}")
        raise Exception("Error de base de datos al crear el usuario")

# def get_user_by_email(db: Session, email: str):
#     try:
#         query = text("""SELECT  id_usuario, nombre_completo, identificacion, id_rol,
#                                 correo, tipo_contrato, pass_hash,
#                                 telefono, estado, cod_centro
#                      FROM usuario 
#                      WHERE correo = :email""")
#         result = db.execute(query, {"email": email}).mappings().first()
#         if not result:
#             return None
#         return result
#     except SQLAlchemyError as e:
#         logger.error(f"Error al obtener usuario por email: {e}")
#         raise Exception("Error de base de datos al obtener el usuario")

def get_user_by_email(db: Session, email: str):
    try:
        query = text("""SELECT  usuario.id_usuario, usuario.nombre_completo, usuario.identificacion,
                                usuario.id_rol, rol.nombre AS rol, usuario.correo, usuario.tipo_contrato,
                                usuario.pass_hash, usuario.telefono, usuario.estado, usuario.cod_centro
                        FROM usuario
                        JOIN rol ON usuario.id_rol = rol.id_rol
                        WHERE usuario.correo = :email""")
        result = db.execute(query, {"email": email}).mappings().first()
        if not result:
            return None
        return result
    except SQLAlchemyError as e:
        logger.error(f"Error al obtener usuario por email: {e}")
        raise Exception("Error de base de datos al obtener el usuario")

    
# def get_user_by_id(db: Session, id_user: int):
#     try:
#         query = text("""SELECT  id_usuario, nombre_completo, identificacion, id_rol,
#                                 correo, tipo_contrato,
#                                 telefono, estado, cod_centro
#                      FROM usuario 
#                      WHERE id_usuario = :id""")
#         result = db.execute(query, {"id": id_user}).mappings().first()
#         return result
#     except SQLAlchemyError as e:
#         logger.error(f"Error al obtener usuario por id: {e}")
#         raise Exception("Error de base de datos al obtener el usuario")
    
def get_user_by_id(db: Session, id_user: int):
    try:
        query = text("""SELECT  usuario.id_usuario, usuario.nombre_completo, usuario.identificacion,
                                usuario.id_rol, rol.nombre AS rol, usuario.correo, usuario.tipo_contrato,
                                usuario.telefono, usuario.estado, usuario.cod_centro
                        FROM usuario
                        JOIN rol ON usuario.id_rol = rol.id_rol
                        WHERE id_usuario = :id""")
        result = db.execute(query, {"id": id_user}).mappings().first()
        return result
    except SQLAlchemyError as e:
        logger.error(f"Error al obtener usuario por id: {e}")
        raise Exception("Error de base de datos al obtener el usuario")


def update_user(db: Session, user_id: int, user_update: UserUpdate) -> bool:
    try:
        fields = user_update.model_dump(exclude_unset=True)
        if not fields:
            return False
        set_clause = ", ".join([f"{key} = :{key}" for key in fields])
        fields["user_id"] = user_id

        query = text(f"UPDATE usuario SET {set_clause} WHERE id_usuario = :user_id")
        db.execute(query, fields)
        db.commit()
        return True
    except SQLAlchemyError as e:
        db.rollback()
        logger.error(f"Error al actualizar usuario: {e}")
        raise Exception("Error de base de datos al actualizar el usuario")

def modify_status_user(db: Session, user_id: int):
    try:
        query = text( """
                     UPDATE usuario SET estado = IF(estado, FALSE, TRUE)
                     WHERE id_usuario = :id 
                     """ )
        db.execute(query, {"id": user_id})
        db.commit()
        return True
    except SQLAlchemyError as e:
        db.rollback()
        logger.error(f"Error al modificar el estado de usuario: {e}")
        raise Exception("Error de base de datos al modificar estado del usuario")
        
# def get_users_by_centro(db: Session, cod_centro: int):
#     try:
#         query = text("""
#             SELECT id_usuario, nombre_completo, identificacion, id_rol,
#                    correo, tipo_contrato, telefono, estado, cod_centro
#             FROM usuario
#             WHERE cod_centro = :cod_centro
#         """)
#         result = db.execute(query, {"cod_centro": cod_centro}).mappings().all()
#         return result
#     except SQLAlchemyError as e:
#         logger.error(f"Error al obtener usuarios por cod_centro: {e}")
#         raise Exception("Error de base de datos al obtener los usuarios")

def get_users_by_centro(db: Session, cod_centro: int):
    try:
        query = text("""SELECT  usuario.id_usuario, usuario.nombre_completo, usuario.identificacion,
                                usuario.id_rol, rol.nombre AS rol, usuario.correo, usuario.tipo_contrato,
                                usuario.telefono, usuario.estado, usuario.cod_centro
                        FROM usuario
                        JOIN rol ON usuario.id_rol = rol.id_rol
                        WHERE cod_centro = :cod_centro""")
        result = db.execute(query, {"cod_centro": cod_centro}).mappings().all()
        return result
    except SQLAlchemyError as e:
        logger.error(f"Error al obtener usuarios por cod_centro: {e}")
        raise Exception("Error de base de datos al obtener los usuarios")