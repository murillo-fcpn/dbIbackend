from app import db
from app.models.permiso import Permiso
from app.models.rol import Rol
from app.models.cuenta import Cuenta
from app.models.ciudadano import Ciudadano
from app.models.notificacion import Notificacion
from datetime import date

print("Verifying user and citizen models...")

# Clean up
try:
    db.session.query(Notificacion).delete()
    db.session.query(Cuenta).delete()
    db.session.query(Ciudadano).delete()
    db.session.execute(db.text("DELETE FROM roles_permisos"))
    db.session.query(Rol).delete()
    db.session.query(Permiso).delete()
    db.session.commit()
except Exception as e:
    db.session.rollback()
    print(f"Cleanup failed: {e}")

try:
    # Create Permisos
    p1 = Permiso(nombre="crear_usuario", descripcion="Crear usuarios")
    p1.save()
    p2 = Permiso(nombre="editar_usuario", descripcion="Editar usuarios")
    p2.save()
    print(f"Created Permisos: {p1}, {p2}")

    # Create Rol with Permisos
    r = Rol(nombre="Administrador", descripcion="Rol de administrador")
    r.permisos = [p1, p2]
    r.save()
    print(f"Created Rol: {r} with permisos: {[p.nombre for p in r.permisos]}")

    # Create Cuenta
    c = Cuenta(usuario="admin", email="admin@test.com", rol_id=r.id)
    c.set_password("password123")
    c.save()
    print(f"Created Cuenta: {c}")

    # Create Ciudadano
    ciudadano = Ciudadano(
        nombre="Juan",
        apellido="Perez",
        ci="12345678",
        email="juan@test.com",
        fecha_nacimiento=date(1990, 1, 1)
    )
    ciudadano.save()
    print(f"Created Ciudadano: {ciudadano}")

    # Create Notificacion
    n = Notificacion(
        titulo="Bienvenido",
        mensaje="Bienvenido al sistema",
        tipo="email",
        ciudadano_id=ciudadano.id
    )
    n.save()
    print(f"Created Notificacion: {n}")

    print("Verification successful!")
except Exception as e:
    print(f"Verification failed: {e}")
    import traceback
    traceback.print_exc()
