from .base import BaseModel
from ..extensions import db


class Ciudadano(BaseModel):
    __tablename__ = "ciudadanos"

    nombre = db.Column(db.String(100), nullable=False)
    apellido = db.Column(db.String(100), nullable=False)
    ci = db.Column(db.String(20), unique=True, nullable=False)
    telefono = db.Column(db.String(20))
    email = db.Column(db.String(100))
    direccion = db.Column(db.String(200))
    latitud = db.Column(db.Float)
    longitud = db.Column(db.Float)
    fecha_nacimiento = db.Column(db.Date)

    # Relaciones
    notificaciones = db.relationship("Notificacion", backref="ciudadano", lazy=True)

    def __repr__(self):
        return f"<Ciudadano {self.nombre} {self.apellido}>"

    def to_dict(self):
        return {
            "id": self.id,
            "nombre": self.nombre,
            "apellido": self.apellido,
            "ci": self.ci,
            "telefono": self.telefono,
            "email": self.email,
            "direccion": self.direccion,
            "latitud": self.latitud,
            "longitud": self.longitud,
            "fecha_nacimiento": self.fecha_nacimiento.isoformat()
            if self.fecha_nacimiento
            else None,
            "estado": self.estado,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }
