from litestar import Controller, post, get
from pydantic import BaseModel
from models.turno import Turno
from models.venta import Venta
from models.producto import Producto
from database import SessionLocal
from datetime import datetime

class TurnoCambio(BaseModel):
    kiosco_id: int
    responsable: str
    hora_inicio: datetime

class TurnoController(Controller):
    path = "/turnos"

    @post("/cambiar")
    async def cambiar(self, data: TurnoCambio) -> dict:
        db = SessionLocal()
        turno = Turno(
            kiosco_id=data.kiosco_id,
            responsable=data.responsable,
            hora_inicio=data.hora_inicio
        )
        db.add(turno)
        db.commit()
        db.close()
        return {"msg": "Cambio de responsable registrado"}

    @get("/listar")
    async def listar(self) -> list[dict]:
        db = SessionLocal()
        turnos = db.query(Turno).all()
        db.close()
        return [
            {
                "id": t.id,
                "nombre": t.responsable,
                "hora": t.hora_inicio.strftime("%d-%m-%y %H:%M")
            }
            for t in turnos
        ]

    @post("/venta")
    async def crear_venta(self, data: Venta) -> dict:
        db = SessionLocal()
        producto = db.query(Producto).filter(Producto.id == data.producto_id).first()
        if not producto:
            return {"msg": "Producto no encontrado"}
        venta = Venta(
            kiosco_id=data.kiosco_id,  # <-- Agrega esto
            producto_id=producto.id,
            cantidad=data.cantidad,
            precio=producto.precio,
            fecha=datetime.now(),
            responsable=data.responsable
        )
        db.add(venta)
        db.commit()
        db.close()
        return {"msg": "Venta registrada"}