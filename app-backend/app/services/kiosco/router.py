from litestar import Controller, post, get
from pydantic import BaseModel
from models.kiosco import Kiosco
from models.venta import Venta
from models.turno import Turno
from models.producto import Producto
from database import SessionLocal
from datetime import datetime

class KioscoInicio(BaseModel):
    nombre: str
    responsable: str
    fecha_inicio: datetime

class KioscoController(Controller):
    path = "/kioscos"

    @post("/iniciar")
    async def iniciar(self, data: KioscoInicio) -> dict:
        db = SessionLocal()
        kiosco = Kiosco(
            nombre=data.nombre,
            responsable=data.responsable,
            fecha_inicio=data.fecha_inicio
        )
        db.add(kiosco)
        db.commit()
        db.close()
        return {"msg": "Kiosco iniciado correctamente", "id": kiosco.id}

    @post("/registrar-inversion")
    async def registrar_inversion(self, data: dict) -> dict:
        db = SessionLocal()
        kiosco = db.query(Kiosco).filter_by(id=data["kiosco_id"]).first()
        if not kiosco:
            db.close()
            return {"msg": "Kiosco no encontrado"}
        kiosco.inversion = data["inversion"]
        db.commit()
        db.close()
        return {"msg": "Inversión registrada"}

    @post("/eliminar")
    async def eliminar(self, data: dict) -> dict:
        db = SessionLocal()
        kiosco = db.query(Kiosco).filter_by(id=data["id"]).first()
        if not kiosco:
            db.close()
            return {"msg": "Kiosco no encontrado"}

        # Eliminar ventas asociadas
        db.query(Venta).filter_by(kiosco_id=kiosco.id).delete()
        # Eliminar turnos asociados
        db.query(Turno).filter_by(kiosco_id=kiosco.id).delete()
        # Eliminar kiosco
        db.delete(kiosco)
        db.commit()
        db.close()
        return {"msg": "Kiosco y sus datos asociados eliminados correctamente"}

    @get("/listar")
    async def listar(self) -> list[dict]:
        db = SessionLocal()
        kioscos = db.query(Kiosco).all()
        db.close()
        return [
            {
                "id": k.id,
                "nombre": k.nombre,
                "responsable": k.responsable,
                "fecha_inicio": k.fecha_inicio.strftime("%d-%m-%y %H:%M"),
                "inversion": getattr(k, "inversion", None)
            }
            for k in kioscos
        ]

    @get("/kiosco/{kiosco_id:int}")
    async def ventas_por_kiosco(self, kiosco_id: int) -> list[dict]:
        db = SessionLocal()
        ventas = db.query(Venta).filter_by(kiosco_id=kiosco_id).all()
        db.close()
        return [
            {
                "id": v.id,
                "producto": v.producto,
                "cantidad": v.cantidad,
                "precio_total": v.precio_total,
                "fecha": v.fecha.strftime("%d-%m-%y %H:%M")
            }
            for v in ventas
        ]

    @post("/vender")
    async def vender(self, data: dict) -> dict:
        db = SessionLocal()
        # Aquí asumimos que 'producto_id' y 'kiosco_id' vienen en los datos
        producto = db.query(Producto).filter_by(id=data.producto_id).first()
        kiosco = db.query(Kiosco).filter_by(id=data.kiosco_id).first()
        if not producto or not kiosco:
            db.close()
            return {"msg": "Producto o Kiosco no encontrado"}

        venta = Venta(
            producto_id=producto.id,
            cantidad=data.cantidad,
            precio=producto.precio,
            fecha=datetime.now(),
            responsable=data.responsable
        )
        db.add(venta)
        db.commit()
        db.close()
        return {"msg": "Venta registrada correctamente"}