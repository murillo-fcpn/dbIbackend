from datetime import datetime
from .base import BaseModel
from ..extensions import db


class Trayecto(BaseModel):
    __tablename__ = "trayectos"

    fecha_hora_salida = db.Column(db.DateTime, nullable=False)
    fecha_hora_llegada = db.Column(db.DateTime)
    estado = db.Column(
        db.String(50), default="programado"
    )  # programado, en_curso, completado, cancelado

    # Claves foráneas
    id_vehiculo = db.Column(db.Integer, db.ForeignKey("vehiculos.id"), nullable=False)
    id_conductor = db.Column(
        db.Integer, db.ForeignKey("conductores.id"), nullable=False
    )
    id_ruta = db.Column(db.Integer, db.ForeignKey("rutas.id"), nullable=False)

    def __repr__(self):
        return f"<Trayecto {self.id} - {self.fecha_hora_salida}>"

    def to_dict(self):
        return {
            "id": self.id,
            "fecha_hora_salida": (
                self.fecha_hora_salida.isoformat() if self.fecha_hora_salida else None
            ),
            "fecha_hora_llegada": (
                self.fecha_hora_llegada.isoformat() if self.fecha_hora_llegada else None
            ),
            "estado": self.estado,
            "id_vehiculo": self.id_vehiculo,
            "id_conductor": self.id_conductor,
            "id_ruta": self.id_ruta,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }
