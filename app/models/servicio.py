from .base import BaseModel
from ..extensions import db


class Servicio(BaseModel):
    __tablename__ = "servicios"

    nombre = db.Column(db.String(100), nullable=False, unique=True)
    tipo = db.Column(db.String(50), nullable=False)  # agua, luz, gas
    descripcion = db.Column(db.Text)

    # Relaciones
    medidores = db.relationship("Medidor", backref="servicio", lazy=True)
    tipos_reclamo = db.relationship("TipoReclamo", backref="servicio", lazy=True)
    cortes_programados = db.relationship(
        "CorteProgramado", backref="servicio", lazy=True
    )

    def __repr__(self):
        return f"<Servicio {self.nombre}>"

    def to_dict(self):
        return {
            "id": self.id,
            "nombre": self.nombre,
            "tipo": self.tipo,
            "descripcion": self.descripcion,
            "estado": self.estado,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }
