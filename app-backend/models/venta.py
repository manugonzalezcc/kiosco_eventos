from sqlalchemy.orm import declarative_base, mapped_column, Mapped
from datetime import datetime

Base = declarative_base()

class Venta(Base):
    __tablename__ = "ventas"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    kiosco_id: Mapped[int] = mapped_column(nullable=False)  # <-- Agrega esto
    producto_id: Mapped[int] = mapped_column(nullable=False)
    cantidad: Mapped[int] = mapped_column(nullable=False)
    precio: Mapped[float] = mapped_column(nullable=False)
    fecha: Mapped[datetime] = mapped_column(nullable=False)
    responsable: Mapped[str] = mapped_column(nullable=False)