from datetime import datetime
from .base import BaseModel
from ..extensions import db


class Operador(BaseModel):
    __tablename__ = "operadores"

    nombre = db.Column(db.String(200), nullable=False)
    telefono = db.Column(db.String(20))
    email = db.Column(db.String(100))
    certificado_vigente = db.Column(db.Boolean, default=True)
    fecha_vencimiento_certificado = db.Column(db.Date)

    # Relaciones
    vehiculos = db.relationship("Vehiculo", backref="operador", lazy=True)

    def __repr__(self):
        return f"<Operador {self.nombre}>"

    def to_dict(self):
        return {
            "id": self.id,
            "nombre": self.nombre,
            "telefono": self.telefono,
            "email": self.email,
            "certificado_vigente": self.certificado_vigente,
            "fecha_vencimiento_certificado": (
                self.fecha_vencimiento_certificado.isoformat()
                if self.fecha_vencimiento_certificado
                else None
            ),
            "estado": self.estado,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }
