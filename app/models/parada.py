from .base import BaseModel
from ..extensions import db


class Parada(BaseModel):
    __tablename__ = "paradas"

    nombre = db.Column(db.String(100), nullable=False)
    latitud = db.Column(db.Numeric(10, 8), nullable=False)
    longitud = db.Column(db.Numeric(11, 8), nullable=False)
    direccion = db.Column(db.Text)
    accesible = db.Column(db.Boolean, default=False)
    techo = db.Column(db.Boolean, default=False)
    orden = db.Column(db.Integer, nullable=False)

    # Clave foránea
    id_ruta = db.Column(db.Integer, db.ForeignKey("rutas.id"), nullable=False)

    def __repr__(self):
        return f"<Parada {self.nombre}>"

    def to_dict(self):
        return {
            "id": self.id,
            "nombre": self.nombre,
            "latitud": float(self.latitud) if self.latitud else None,
            "longitud": float(self.longitud) if self.longitud else None,
            "direccion": self.direccion,
            "accesible": self.accesible,
            "techo": self.techo,
            "orden": self.orden,
            "id_ruta": self.id_ruta,
            "estado": self.estado,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }
