from datetime import datetime
from ..extensions import db


class BaseModel(db.Model):
    """Modelo base con campos comunes"""

    __abstract__ = True

    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )
    estado = db.Column(db.String(20), default="activo", nullable=False)

    def save(self):
        """Guardar objeto en la base de datos"""
        db.session.add(self)
        db.session.commit()

    def delete(self):
        """Eliminar objeto de la base de datos"""
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def get_all(cls):
        """Obtener todos los objetos activos"""
        return cls.query.filter_by(estado="activo").all()

    @classmethod
    def get_by_id(cls, id):
        """Obtener objeto por ID"""
        return cls.query.filter_by(id=id, estado="activo").first()
