from datetime import datetime
from .base import BaseModel
from ..extensions import db


class IncidenteTransito(BaseModel):
    __tablename__ = "incidentes_transito"

    descripcion = db.Column(db.Text, nullable=False)
    fecha_inicio = db.Column(db.DateTime, nullable=False)
    fecha_fin = db.Column(db.DateTime)
    latitud = db.Column(db.Numeric(10, 8))
    longitud = db.Column(db.Numeric(11, 8))
    estado = db.Column(db.String(50), default="activo")  # activo, resuelto

    # Claves foráneas
    id_tipo_incidente = db.Column(
        db.Integer, db.ForeignKey("tipos_incidente.id"), nullable=False
    )
    id_ruta = db.Column(db.Integer, db.ForeignKey("rutas.id"))
    id_conductor = db.Column(db.Integer, db.ForeignKey("conductores.id"))
    id_vehiculo = db.Column(db.Integer, db.ForeignKey("vehiculos.id"))

    def __repr__(self):
        return f"<IncidenteTransito {self.id}>"

    def to_dict(self):
        return {
            "id": self.id,
            "descripcion": self.descripcion,
            "fecha_inicio": (
                self.fecha_inicio.isoformat() if self.fecha_inicio else None
            ),
            "fecha_fin": self.fecha_fin.isoformat() if self.fecha_fin else None,
            "latitud": float(self.latitud) if self.latitud else None,
            "longitud": float(self.longitud) if self.longitud else None,
            "id_tipo_incidente": self.id_tipo_incidente,
            "id_ruta": self.id_ruta,
            "id_conductor": self.id_conductor,
            "id_vehiculo": self.id_vehiculo,
            "estado": self.estado,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }
