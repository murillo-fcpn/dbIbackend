from .base import BaseModel
from ..extensions import db


class Ruta(BaseModel):
    __tablename__ = "rutas"

    nombre = db.Column(db.String(100), nullable=False, unique=True)
    distancia_km = db.Column(db.Numeric(8, 2))
    tiempo_estimado_min = db.Column(db.Integer)
    color_mapa = db.Column(db.String(7))  # Código hex color

    # Clave foránea
    id_tipo_transporte = db.Column(
        db.Integer, db.ForeignKey("tipos_transporte.id"), nullable=False
    )

    # Relaciones
    paradas = db.relationship("Parada", backref="ruta", lazy=True)
    horarios = db.relationship("Horario", backref="ruta", lazy=True)
    trayectos = db.relationship("Trayecto", backref="ruta", lazy=True)
    incidentes = db.relationship("IncidenteTransito", backref="ruta", lazy=True)

    def __repr__(self):
        return f"<Ruta {self.nombre}>"

    def to_dict(self):
        return {
            "id": self.id,
            "nombre": self.nombre,
            "distancia_km": float(self.distancia_km) if self.distancia_km else None,
            "tiempo_estimado_min": self.tiempo_estimado_min,
            "color_mapa": self.color_mapa,
            "id_tipo_transporte": self.id_tipo_transporte,
            "estado": self.estado,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }
