from datetime import datetime
from .base import BaseModel
from ..extensions import db


class Conductor(BaseModel):
    __tablename__ = "conductores"

    nombre = db.Column(db.String(100), nullable=False)
    apellido = db.Column(db.String(100), nullable=False)
    ci = db.Column(db.String(20), nullable=False, unique=True)
    licencia = db.Column(db.String(50), nullable=False)
    vencimiento_licencia = db.Column(db.Date, nullable=False)
    telefono = db.Column(db.String(20))

    # Relaciones
    trayectos = db.relationship("Trayecto", backref="conductor", lazy=True)
    incidentes = db.relationship("IncidenteTransito", backref="conductor", lazy=True)

    def __repr__(self):
        return f"<Conductor {self.nombre} {self.apellido}>"

    def to_dict(self):
        return {
            "id": self.id,
            "nombre": self.nombre,
            "apellido": self.apellido,
            "ci": self.ci,
            "licencia": self.licencia,
            "vencimiento_licencia": (
                self.vencimiento_licencia.isoformat()
                if self.vencimiento_licencia
                else None
            ),
            "telefono": self.telefono,
            "estado": self.estado,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }
