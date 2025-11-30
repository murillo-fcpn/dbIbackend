from .base import BaseModel
from ..extensions import db


class Zona(BaseModel):
    __tablename__ = "zonas"

    nombre = db.Column(db.String(100), nullable=False)
    poligono_geojson = db.Column(db.JSON)  # Almacenamos el GeoJSON como JSON
    descripcion = db.Column(db.Text)
    tipo = db.Column(db.String(50))  # residencial, industrial, verde

    # Relaciones
    sensores = db.relationship("Sensor", backref="zona", lazy=True)

    def __repr__(self):
        return f"<Zona {self.nombre}>"

    def to_dict(self):
        return {
            "id": self.id,
            "nombre": self.nombre,
            "poligono_geojson": self.poligono_geojson,
            "descripcion": self.descripcion,
            "tipo": self.tipo,
            "estado": self.estado,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }
