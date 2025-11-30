from .base import BaseModel
from ..extensions import db


class AlertaAmbiental(BaseModel):
    __tablename__ = "alertas_ambientales"

    fecha = db.Column(db.Date, nullable=False)
    hora = db.Column(db.Time, nullable=False)
    tipo_alerta = db.Column(db.String(50), nullable=False)
    descripcion = db.Column(db.Text)

    # Claves foráneas
    sensor_id = db.Column(db.Integer, db.ForeignKey("sensores.id"), nullable=False)

    def __repr__(self):
        return f"<AlertaAmbiental {self.id}>"

    def to_dict(self):
        return {
            "id": self.id,
            "fecha": self.fecha.isoformat() if self.fecha else None,
            "hora": self.hora.isoformat() if self.hora else None,
            "tipo_alerta": self.tipo_alerta,
            "descripcion": self.descripcion,
            "sensor_id": self.sensor_id,
            "estado": self.estado,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }
