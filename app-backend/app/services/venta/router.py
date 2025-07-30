from litestar import Controller, post, get
from pydantic import BaseModel
from models.venta import Venta
from models.turno import Turno
from models.producto import Producto
from database import SessionLocal
from datetime import datetime

class VentaRegistrar(BaseModel):
    nombre: str
    cantidad: int
    responsable: str
    kiosco_id: int  # <-- Agrega esto

class VentaEliminar(BaseModel):
    id: int

class VentaController(Controller):
    path = "/ventas"

    @post("/registrar")
    async def registrar(self, data: VentaRegistrar) -> dict:
        db = SessionLocal()
        producto = db.query(Producto).filter_by(nombre=data.nombre).first()
        if not producto:
            db.close()
            return {"msg": "Producto no encontrado"}
        if producto.cantidad < data.cantidad:
            db.close()
            return {"msg": "Stock insuficiente"}
        producto.cantidad -= data.cantidad
        venta = Venta(
            producto_id=producto.id,
            cantidad=data.cantidad,
            precio=producto.precio,
            fecha=datetime.now(),
            responsable=data.responsable,  # <-- Guarda el responsable
            kiosco_id=data.kiosco_id  # <-- Guarda el kiosco_id
        )
        db.add(venta)
        db.commit()
        db.close()
        return {"msg": "Venta registrada correctamente"}

    @get("/listar")
    async def listar(self) -> list[dict]:
        db = SessionLocal()
        ventas = db.query(Venta).all()
        productos = {p.id: p.nombre for p in db.query(Producto).all()}
        db.close()
        return [
            {
                "id": v.id,
                "producto": productos.get(v.producto_id, "Desconocido"),
                "cantidad": v.cantidad,
                "precio": v.precio,
                "responsable": v.responsable
            }
            for v in ventas
        ]

    @post("/eliminar")
    async def eliminar(self, data: VentaEliminar) -> dict:
        db = SessionLocal()
        venta = db.query(Venta).filter_by(id=data.id).first()
        if not venta:
            db.close()
            return {"msg": "Venta no encontrada"}
        db.delete(venta)
        db.commit()
        db.close()
        return {"msg": "Venta eliminada correctamente"}

    @get("/kiosco/{kiosco_id:int}")
    async def ventas_por_kiosco(self, kiosco_id: int) -> list[dict]:
        db = SessionLocal()
        ventas = db.query(Venta).filter_by(kiosco_id=kiosco_id).all()
        productos = {p.id: p.nombre for p in db.query(Producto).all()}
        db.close()
        return [
            {
                "id": v.id,
                "producto": productos.get(v.producto_id, "Desconocido"),
                "cantidad": v.cantidad,
                "precio": v.precio,
                "responsable": v.responsable,
                "fecha": v.fecha.strftime("%d-%m-%y %H:%M")
            }
            for v in ventas
        ]