from litestar import Controller, post, get
from pydantic import BaseModel
from models.producto import Producto
from database import SessionLocal
from sqlalchemy.exc import IntegrityError

class ProductoAgregar(BaseModel):
    nombre: str
    cantidad: int
    precio: float

class ProductoActualizarStock(BaseModel):
    nombre: str
    cantidad: int

class ProductoEliminar(BaseModel):
    nombre: str

class ProductoController(Controller):
    path = "/productos"

    @post("/agregar")
    async def agregar(self, data: ProductoAgregar) -> dict:
        db = SessionLocal()
        producto = Producto(
            nombre=data.nombre,
            cantidad=data.cantidad,
            precio=data.precio
        )
        db.add(producto)
        try:
            db.commit()
            return {"msg": "Producto agregado correctamente"}
        except IntegrityError as e:
            db.rollback()
            print("ERROR INTEGRITY:", e)
            return {"msg": "El producto ya existe"}
        except Exception as e:
            db.rollback()
            print("ERROR GENERAL:", e)
            return {"msg": "Error interno"}
        finally:
            db.close()

    @post("/actualizar-stock")
    async def actualizar_stock(self, data: ProductoActualizarStock) -> dict:
        db = SessionLocal()
        producto = db.query(Producto).filter_by(nombre=data.nombre).first()
        if not producto:
            db.close()
            return {"msg": "Producto no encontrado"}
        producto.cantidad += data.cantidad
        db.commit()
        db.close()
        return {"msg": "Stock actualizado correctamente"}

    @post("/eliminar")
    async def eliminar(self, data: ProductoEliminar) -> dict:
        db = SessionLocal()
        producto = db.query(Producto).filter_by(nombre=data.nombre).first()
        if not producto:
            db.close()
            return {"msg": "Producto no encontrado"}
        db.delete(producto)
        db.commit()
        db.close()
        return {"msg": "Producto eliminado correctamente"}

    @post("/eliminar-stock")
    async def eliminar_stock(self, data: ProductoActualizarStock) -> dict:
        db = SessionLocal()
        producto = db.query(Producto).filter_by(nombre=data.nombre).first()
        if not producto:
            db.close()
            return {"msg": "Producto no encontrado"}
        if producto.cantidad < data.cantidad:
            db.close()
            return {"msg": "No hay suficiente stock para eliminar"}
        producto.cantidad -= data.cantidad
        db.commit()
        db.close()
        return {"msg": f"Se eliminaron {data.cantidad} unidades de stock"}

    @get("/listar")
    async def listar(self) -> list[dict]:
        db = SessionLocal()
        productos = db.query(Producto).all()
        db.close()
        return [{"id": p.id, "nombre": p.nombre, "cantidad": p.cantidad, "precio": p.precio} for p in productos]

    async def eliminarProducto(self, nombre: str) -> dict:
        db = SessionLocal()
        producto = db.query(Producto).filter_by(nombre=nombre).first()
        if not producto:
            db.close()
            return {"msg": "Producto no encontrado"}
        producto.cantidad = 0
        db.commit()
        db.close()
        return {"msg": "Stock eliminado correctamente"}