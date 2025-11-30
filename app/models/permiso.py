from .base import BaseModel
from ..extensions import db


class Permiso(BaseModel):
    __tablename__ = "permisos"

    nombre = db.Column(db.String(50), unique=True, nullable=False)
    descripcion = db.Column(db.String(200))

    def __repr__(self):
        return f"<Permiso {self.nombre}>"

    def to_dict(self):
        return {
            "id": self.id,
            "nombre": self.nombre,
            "descripcion": self.descripcion,
            "estado": self.estado,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }
