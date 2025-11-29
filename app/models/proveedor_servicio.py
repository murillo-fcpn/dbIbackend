from .base import BaseModel
from ..extensions import db


class ProveedorServicio(BaseModel):
    __tablename__ = "proveedores_servicio"

    nombre = db.Column(db.String(200), nullable=False)
    telefono = db.Column(db.String(20))
    email = db.Column(db.String(100))
    direccion = db.Column(db.Text)

    def __repr__(self):
        return f"<ProveedorServicio {self.nombre}>"

    def to_dict(self):
        return {
            "id": self.id,
            "nombre": self.nombre,
            "telefono": self.telefono,
            "email": self.email,
            "direccion": self.direccion,
            "estado": self.estado,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }
