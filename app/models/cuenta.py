from .base import BaseModel
from ..extensions import db
from werkzeug.security import generate_password_hash, check_password_hash


class Cuenta(BaseModel):
    __tablename__ = "cuentas"

    usuario = db.Column(db.String(50), unique=True, nullable=False)
    contrasena = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    fecha_creacion = db.Column(db.DateTime, default=db.func.current_timestamp())

    # Claves foráneas
    rol_id = db.Column(db.Integer, db.ForeignKey("roles.id"), nullable=False)

    def set_password(self, password):
        """Hash y guardar contraseña"""
        self.contrasena = generate_password_hash(password)

    def check_password(self, password):
        """Verificar contraseña"""
        return check_password_hash(self.contrasena, password)

    def __repr__(self):
        return f"<Cuenta {self.usuario}>"

    def to_dict(self):
        return {
            "id": self.id,
            "usuario": self.usuario,
            "email": self.email,
            "rol_id": self.rol_id,
            "fecha_creacion": self.fecha_creacion.isoformat()
            if self.fecha_creacion
            else None,
            "estado": self.estado,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }
