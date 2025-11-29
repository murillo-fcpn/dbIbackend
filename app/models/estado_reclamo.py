from .base import BaseModel
from ..extensions import db


class EstadoReclamo(BaseModel):
    __tablename__ = "estados_reclamo"

    nombre = db.Column(db.String(50), nullable=False, unique=True)
    descripcion = db.Column(db.Text)

    # Relaciones
    reclamos = db.relationship("Reclamo", backref="estado_reclamo", lazy=True)

    def __repr__(self):
        return f"<EstadoReclamo {self.nombre}>"

    def to_dict(self):
        return {
            "id": self.id,
            "nombre": self.nombre,
            "descripcion": self.descripcion,
            "estado": self.estado,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }
