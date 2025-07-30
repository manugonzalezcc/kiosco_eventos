from models.usuario import Base as UsuarioBase
from models.kiosco import Base as KioscoBase
from models.producto import Base as ProductoBase
from models.venta import Base as VentaBase
from models.turno import Base as TurnoBase
from database import engine

UsuarioBase.metadata.create_all(bind=engine)
KioscoBase.metadata.create_all(bind=engine)
ProductoBase.metadata.create_all(bind=engine)
VentaBase.metadata.create_all(bind=engine)
TurnoBase.metadata.create_all(bind=engine)
print("Tablas creadas correctamente.")