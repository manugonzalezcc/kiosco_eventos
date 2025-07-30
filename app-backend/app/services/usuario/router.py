from litestar import Controller, post
from pydantic import BaseModel
from models.usuario import Usuario
from database import SessionLocal
from sqlalchemy.exc import IntegrityError

class UsuarioRegistro(BaseModel):
    username: str
    password: str

class UsuarioLogin(BaseModel):
    username: str
    password: str

class UsuarioController(Controller):
    path = "/usuarios"

    @post("/registro")
    async def registro(self, data: UsuarioRegistro) -> dict:
        db = SessionLocal()
        usuario = Usuario(username=data.username, password=data.password)
        db.add(usuario)
        try:
            db.commit()
            return {"msg": "Usuario registrado"}
        except IntegrityError as e:
            db.rollback()
            print("ERROR INTEGRITY:", e)
            return {"msg": "Usuario ya existe"}
        except Exception as e:
            db.rollback()
            print("ERROR GENERAL:", e)  # <-- Esto mostrará cualquier otro error
            return {"msg": "Error interno"}
        finally:
            db.close()

    @post("/login")
    async def login(self, data: UsuarioLogin) -> dict:
        db = SessionLocal()
        usuario = db.query(Usuario).filter_by(username=data.username, password=data.password).first()
        db.close()
        if usuario:
            return {"msg": "Inicio de sesión exitoso"}
        else:
            return {"msg": "Usuario o contraseña incorrectos"}