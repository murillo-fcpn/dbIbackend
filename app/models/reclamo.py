from datetime import datetime
from .base import BaseModel
from ..extensions import db


class Reclamo(BaseModel):
    __tablename__ = "reclamos"

    descripcion = db.Column(db.Text, nullable=False)
    fecha_creacion = db.Column(db.DateTime, default=datetime.utcnow)
    imagen_url = db.Column(db.String(500))

    # Claves foráneas
    # id_ciudadano = db.Column(db.Integer, db.ForeignKey("ciudadanos.id"), nullable=True)
    id_tipo_reclamo = db.Column(
        db.Integer, db.ForeignKey("tipos_reclamo.id"), nullable=False
    )
    id_estado_reclamo = db.Column(
        db.Integer, db.ForeignKey("estados_reclamo.id"), nullable=False
    )
    id_servicio = db.Column(db.Integer, db.ForeignKey("servicios.id"), nullable=False)

    def __repr__(self):
        return f"<Reclamo {self.id}>"

    def to_dict(self):
        return {
            "id": self.id,
            "descripcion": self.descripcion,
            "fecha_creacion": (
                self.fecha_creacion.isoformat() if self.fecha_creacion else None
            ),
            "imagen_url": self.imagen_url,
            # "id_ciudadano": self.id_ciudadano,
            "id_tipo_reclamo": self.id_tipo_reclamo,
            "id_estado_reclamo": self.id_estado_reclamo,
            "id_servicio": self.id_servicio,
            "estado": self.estado,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }
