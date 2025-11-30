from .base import BaseModel
from ..extensions import db


class Notificacion(BaseModel):
    __tablename__ = "notificaciones"

    titulo = db.Column(db.String(100), nullable=False)
    mensaje = db.Column(db.Text, nullable=False)
    fecha_hora = db.Column(db.DateTime, default=db.func.current_timestamp())
    tipo = db.Column(db.String(50))  # email, sms, push, etc.

    # Claves foráneas
    ciudadano_id = db.Column(
        db.Integer, db.ForeignKey("ciudadanos.id"), nullable=False
    )

    def __repr__(self):
        return f"<Notificacion {self.titulo}>"

    def to_dict(self):
        return {
            "id": self.id,
            "titulo": self.titulo,
            "mensaje": self.mensaje,
            "fecha_hora": self.fecha_hora.isoformat() if self.fecha_hora else None,
            "tipo": self.tipo,
            "ciudadano_id": self.ciudadano_id,
            "estado": self.estado,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }
