from sqlalchemy.orm import declarative_base, mapped_column, Mapped
from datetime import datetime

Base = declarative_base()

class Kiosco(Base):
    __tablename__ = "kioscos"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    nombre: Mapped[str] = mapped_column(nullable=False)
    responsable: Mapped[str] = mapped_column(nullable=False)
    fecha_inicio: Mapped[datetime] = mapped_column(nullable=False)
    inversion: Mapped[float] = mapped_column(nullable=True)