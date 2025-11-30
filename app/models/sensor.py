from .base import BaseModel
from ..extensions import db


class Sensor(BaseModel):
    __tablename__ = "sensores"

    codigo = db.Column(db.String(50), unique=True, nullable=False)
    tipo = db.Column(db.String(50), nullable=False)  # ruido, aire, temperatura, humedad
    ubicacion = db.Column(db.String(200))
    latitud = db.Column(db.Float)
    longitud = db.Column(db.Float)
    fecha_instalacion = db.Column(db.Date)

    # Claves foráneas
    zona_id = db.Column(db.Integer, db.ForeignKey("zonas.id"), nullable=False)

    # Relaciones
    lecturas = db.relationship("LecturaSensor", backref="sensor", lazy=True)
    alertas = db.relationship("AlertaAmbiental", backref="sensor", lazy=True)

    def __repr__(self):
        return f"<Sensor {self.codigo}>"

    def to_dict(self):
        return {
            "id": self.id,
            "codigo": self.codigo,
            "tipo": self.tipo,
            "ubicacion": self.ubicacion,
            "latitud": self.latitud,
            "longitud": self.longitud,
            "fecha_instalacion": self.fecha_instalacion.isoformat()
            if self.fecha_instalacion
            else None,
            "zona_id": self.zona_id,
            "estado": self.estado,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }
