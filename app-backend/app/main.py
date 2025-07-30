from litestar import Litestar, get
from litestar.config.cors import CORSConfig
from app.services.usuario.router import UsuarioController
from app.services.kiosco.router import KioscoController
from app.services.producto.router import ProductoController
from app.services.venta.router import VentaController
from app.services.turno.router import TurnoController

cors_config = CORSConfig(allow_origins=["*"])

@get("/")
async def home() -> dict:
    return {"msg": "API Kiosco funcionando"}

app = Litestar(
    route_handlers=[home, UsuarioController, KioscoController, ProductoController, VentaController, TurnoController],
    cors_config=cors_config
)