from .base import BaseModel
from ..extensions import db


class TipoTransporte(BaseModel):
    __tablename__ = "tipos_transporte"

    nombre = db.Column(db.String(100), nullable=False, unique=True)
    descripcion = db.Column(db.Text)
    empresa_operadora = db.Column(db.String(200))

    # Relaciones
    vehiculos = db.relationship("Vehiculo", backref="tipo_transporte", lazy=True)
    rutas = db.relationship("Ruta", backref="tipo_transporte", lazy=True)

    def __repr__(self):
        return f"<TipoTransporte {self.nombre}>"

    def to_dict(self):
        return {
            "id": self.id,
            "nombre": self.nombre,
            "descripcion": self.descripcion,
            "empresa_operadora": self.empresa_operadora,
            "estado": self.estado,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }
