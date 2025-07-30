from sqlalchemy.orm import declarative_base, mapped_column, Mapped
from datetime import datetime

Base = declarative_base()

class Turno(Base):
    __tablename__ = "turnos"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    kiosco_id: Mapped[int] = mapped_column(nullable=False)
    responsable: Mapped[str] = mapped_column(nullable=False)
    hora_inicio: Mapped[datetime] = mapped_column(nullable=False)