from .base import BaseModel
from ..extensions import db


class LecturaSensor(BaseModel):
    __tablename__ = "lecturas_sensor"

    valor = db.Column(db.Float, nullable=False)
    unidad_medida = db.Column(db.String(20), nullable=False)
    fecha = db.Column(db.Date, nullable=False)
    hora = db.Column(db.Time, nullable=False)
    tipo_lectura = db.Column(db.String(50), nullable=False)

    # Claves foráneas
    sensor_id = db.Column(db.Integer, db.ForeignKey("sensores.id"), nullable=False)

    def __repr__(self):
        return f"<LecturaSensor {self.id}>"

    def to_dict(self):
        return {
            "id": self.id,
            "valor": self.valor,
            "unidad_medida": self.unidad_medida,
            "fecha": self.fecha.isoformat() if self.fecha else None,
            "hora": self.hora.isoformat() if self.hora else None,
            "tipo_lectura": self.tipo_lectura,
            "sensor_id": self.sensor_id,
            "estado": self.estado,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }
