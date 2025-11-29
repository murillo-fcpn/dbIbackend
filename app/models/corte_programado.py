from datetime import datetime
from .base import BaseModel
from ..extensions import db


class CorteProgramado(BaseModel):
    __tablename__ = "cortes_programados"

    fecha_inicio = db.Column(db.DateTime, nullable=False)
    fecha_fin = db.Column(db.DateTime, nullable=False)
    motivo = db.Column(db.Text, nullable=False)
    zonas_afectadas = db.Column(db.Text, nullable=False)

    # Clave foránea
    id_servicio = db.Column(db.Integer, db.ForeignKey("servicios.id"), nullable=False)

    def __repr__(self):
        return f"<CorteProgramado {self.id}>"

    def to_dict(self):
        return {
            "id": self.id,
            "fecha_inicio": (
                self.fecha_inicio.isoformat() if self.fecha_inicio else None
            ),
            "fecha_fin": self.fecha_fin.isoformat() if self.fecha_fin else None,
            "motivo": self.motivo,
            "id_servicio": self.id_servicio,
            "zonas_afectadas": self.zonas_afectadas,
            "estado": self.estado,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }
