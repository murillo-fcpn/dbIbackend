from .base import BaseModel
from ..extensions import db


class TipoIncidente(BaseModel):
    __tablename__ = "tipos_incidente"

    nombre = db.Column(db.String(100), nullable=False, unique=True)
    descripcion = db.Column(db.Text)
    categoria = db.Column(
        db.String(50), nullable=False
    )  # transito, mecanico, seguridad

    # Relaciones
    incidentes = db.relationship(
        "IncidenteTransito", backref="tipo_incidente", lazy=True
    )

    def __repr__(self):
        return f"<TipoIncidente {self.nombre}>"

    def to_dict(self):
        return {
            "id": self.id,
            "nombre": self.nombre,
            "descripcion": self.descripcion,
            "categoria": self.categoria,
            "estado": self.estado,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }
