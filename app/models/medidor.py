from .base import BaseModel
from ..extensions import db


class Medidor(BaseModel):
    __tablename__ = "medidores"

    numero_serie = db.Column(db.String(50), nullable=False, unique=True)
    tipo = db.Column(db.String(50), nullable=False)
    ubicacion = db.Column(db.Text)
    fecha_instalacion = db.Column(db.Date)

    # Claves foráneas
    id_servicio = db.Column(db.Integer, db.ForeignKey("servicios.id"), nullable=False)
    # id_ciudadano = db.Column(
    #     db.Integer, db.ForeignKey("ciudadanos.id"), nullable=True
    # )  # Asumiendo tabla ciudadanos

    # Relaciones
    lecturas = db.relationship("LecturaServicio", backref="medidor", lazy=True)

    def __repr__(self):
        return f"<Medidor {self.numero_serie}>"

    def to_dict(self):
        return {
            "id": self.id,
            "numero_serie": self.numero_serie,
            "tipo": self.tipo,
            "ubicacion": self.ubicacion,
            "fecha_instalacion": (
                self.fecha_instalacion.isoformat() if self.fecha_instalacion else None
            ),
            "id_servicio": self.id_servicio,
            # "id_ciudadano": self.id_ciudadano,
            "estado": self.estado,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }
