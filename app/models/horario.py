from .base import BaseModel
from ..extensions import db


class Horario(BaseModel):
    __tablename__ = "horarios"

    dia_semana = db.Column(db.String(20), nullable=False)  # lunes, martes, etc.
    hora_inicio = db.Column(db.Time, nullable=False)
    hora_fin = db.Column(db.Time, nullable=False)
    frecuencia_min = db.Column(db.Integer)  # Frecuencia en minutos

    # Clave foránea
    id_ruta = db.Column(db.Integer, db.ForeignKey("rutas.id"), nullable=False)

    def __repr__(self):
        return f"<Horario {self.dia_semana} {self.hora_inicio}-{self.hora_fin}>"

    def to_dict(self):
        return {
            "id": self.id,
            "dia_semana": self.dia_semana,
            "hora_inicio": self.hora_inicio.isoformat() if self.hora_inicio else None,
            "hora_fin": self.hora_fin.isoformat() if self.hora_fin else None,
            "frecuencia_min": self.frecuencia_min,
            "id_ruta": self.id_ruta,
            "estado": self.estado,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }
