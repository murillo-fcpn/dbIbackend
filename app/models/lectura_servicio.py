from datetime import datetime
from .base import BaseModel
from ..extensions import db


class LecturaServicio(BaseModel):
    __tablename__ = "lecturas_servicio"

    lectura_anterior = db.Column(db.Numeric(10, 2), nullable=False)
    lectura_actual = db.Column(db.Numeric(10, 2), nullable=False)
    consumo = db.Column(db.Numeric(10, 2), nullable=False)
    fecha_lectura = db.Column(db.DateTime, default=datetime.utcnow)
    tipo_lectura = db.Column(db.String(50), nullable=False)  # real, estimada

    # Claves foráneas
    id_medidor = db.Column(db.Integer, db.ForeignKey("medidores.id"), nullable=False)
    # id_operador = db.Column(
    #     db.Integer, db.ForeignKey("operadores.id"), nullable=True
    # )  # Asumiendo tabla operadores

    def __repr__(self):
        return f"<LecturaServicio {self.id} - Medidor {self.id_medidor}>"

    def to_dict(self):
        return {
            "id": self.id,
            "id_medidor": self.id_medidor,
            "lectura_anterior": float(self.lectura_anterior),
            "lectura_actual": float(self.lectura_actual),
            "consumo": float(self.consumo),
            "fecha_lectura": (
                self.fecha_lectura.isoformat() if self.fecha_lectura else None
            ),
            "tipo_lectura": self.tipo_lectura,
            # "id_operador": self.id_operador,
            "estado": self.estado,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }
