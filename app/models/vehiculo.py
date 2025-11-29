from datetime import datetime
from .base import BaseModel
from ..extensions import db


class Vehiculo(BaseModel):
    __tablename__ = "vehiculos"

    placa = db.Column(db.String(20), nullable=False, unique=True)
    capacidad_max = db.Column(db.Integer, nullable=False)
    fecha_alta = db.Column(db.Date, default=datetime.utcnow)
    modelo = db.Column(db.String(100))
    anio_fabricacion = db.Column(db.Integer)

    # Claves foráneas
    id_tipo_transporte = db.Column(
        db.Integer, db.ForeignKey("tipos_transporte.id"), nullable=False
    )
    id_operador = db.Column(db.Integer, db.ForeignKey("operadores.id"), nullable=False)

    # Relaciones
    trayectos = db.relationship("Trayecto", backref="vehiculo", lazy=True)
    incidentes = db.relationship("IncidenteTransito", backref="vehiculo", lazy=True)

    def __repr__(self):
        return f"<Vehiculo {self.placa}>"

    def to_dict(self):
        return {
            "id": self.id,
            "placa": self.placa,
            "capacidad_max": self.capacidad_max,
            "fecha_alta": self.fecha_alta.isoformat() if self.fecha_alta else None,
            "modelo": self.modelo,
            "anio_fabricacion": self.anio_fabricacion,
            "id_tipo_transporte": self.id_tipo_transporte,
            "id_operador": self.id_operador,
            "estado": self.estado,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }
