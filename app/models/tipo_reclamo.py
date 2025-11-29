from .base import BaseModel
from ..extensions import db


class TipoReclamo(BaseModel):
    __tablename__ = "tipos_reclamo"

    nombre = db.Column(db.String(100), nullable=False)
    descripcion = db.Column(db.Text)

    # Clave foránea
    id_servicio = db.Column(db.Integer, db.ForeignKey("servicios.id"), nullable=False)

    # Relaciones
    reclamos = db.relationship("Reclamo", backref="tipo_reclamo", lazy=True)

    def __repr__(self):
        return f"<TipoReclamo {self.nombre}>"

    def to_dict(self):
        return {
            "id": self.id,
            "nombre": self.nombre,
            "descripcion": self.descripcion,
            "id_servicio": self.id_servicio,
            "estado": self.estado,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }
