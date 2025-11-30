from .base import BaseModel
from ..extensions import db

# Tabla de asociación para la relación Many-to-Many entre Roles y Permisos
roles_permisos = db.Table(
    "roles_permisos",
    db.Column("rol_id", db.Integer, db.ForeignKey("roles.id"), primary_key=True),
    db.Column(
        "permiso_id", db.Integer, db.ForeignKey("permisos.id"), primary_key=True
    ),
)


class Rol(BaseModel):
    __tablename__ = "roles"

    nombre = db.Column(db.String(50), unique=True, nullable=False)
    descripcion = db.Column(db.String(200))

    # Relaciones
    permisos = db.relationship(
        "Permiso",
        secondary=roles_permisos,
        lazy="subquery",
        backref=db.backref("roles", lazy=True),
    )
    cuentas = db.relationship("Cuenta", backref="rol", lazy=True)

    def __repr__(self):
        return f"<Rol {self.nombre}>"

    def to_dict(self):
        return {
            "id": self.id,
            "nombre": self.nombre,
            "descripcion": self.descripcion,
            "permisos": [p.nombre for p in self.permisos],
            "estado": self.estado,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }
