import click
from flask.cli import with_appcontext
from .extensions import db
from .models.servicio import Servicio
from .models.estado_reclamo import EstadoReclamo
from .models.proveedor_servicio import ProveedorServicio


def register_commands(app):
    """Registrar comandos CLI personalizados"""

    @app.cli.group()
    def db_seed():
        """Comandos para poblar la base de datos"""
        pass

    @db_seed.command()
    @with_appcontext
    def servicios():
        """Poblar tabla de servicios"""
        servicios_data = [
            {
                "nombre": "Agua Potable",
                "tipo": "agua",
                "descripcion": "Servicio de distribución de agua potable",
            },
            {
                "nombre": "Energía Eléctrica",
                "tipo": "luz",
                "descripcion": "Servicio de distribución de energía eléctrica",
            },
            {
                "nombre": "Gas Natural",
                "tipo": "gas",
                "descripcion": "Servicio de distribución de gas natural",
            },
        ]

        for servicio_data in servicios_data:
            if not Servicio.query.filter_by(nombre=servicio_data["nombre"]).first():
                servicio = Servicio(**servicio_data)
                db.session.add(servicio)
                click.echo(f"Servicio creado: {servicio.nombre}")

        db.session.commit()
        click.echo("✅ Servicios poblados exitosamente")

    @db_seed.command()
    @with_appcontext
    def estados_reclamo():
        """Poblar tabla de estados de reclamo"""
        estados_data = [
            {
                "nombre": "Pendiente",
                "descripcion": "Reclamo recibido, pendiente de revisión",
            },
            {"nombre": "En Proceso", "descripcion": "Reclamo en proceso de resolución"},
            {
                "nombre": "Resuelto",
                "descripcion": "Reclamo resuelto satisfactoriamente",
            },
            {"nombre": "Cerrado", "descripcion": "Reclamo cerrado"},
            {"nombre": "Rechazado", "descripcion": "Reclamo rechazado por inválido"},
        ]

        for estado_data in estados_data:
            if not EstadoReclamo.query.filter_by(nombre=estado_data["nombre"]).first():
                estado = EstadoReclamo(**estado_data)
                db.session.add(estado)
                click.echo(f"Estado de reclamo creado: {estado.nombre}")

        db.session.commit()
        click.echo("✅ Estados de reclamo poblados exitosamente")

    @db_seed.command()
    @with_appcontext
    def proveedores():
        """Poblar tabla de proveedores de servicio"""
        proveedores_data = [
            {
                "nombre": "Empresa de Agua Municipal",
                "telefono": "+1234567890",
                "email": "contacto@aguamunicipal.com",
                "direccion": "Av. Principal #123",
            },
            {
                "nombre": "Compañía Eléctrica Nacional",
                "telefono": "+0987654321",
                "email": "info@electricanacional.com",
                "direccion": "Calle Secundaria #456",
            },
            {
                "nombre": "Distribuidora de Gas Regional",
                "telefono": "+1122334455",
                "email": "servicio@gasregional.com",
                "direccion": "Plaza Central #789",
            },
        ]

        for proveedor_data in proveedores_data:
            if not ProveedorServicio.query.filter_by(
                nombre=proveedor_data["nombre"]
            ).first():
                proveedor = ProveedorServicio(**proveedor_data)
                db.session.add(proveedor)
                click.echo(f"Proveedor creado: {proveedor.nombre}")

        db.session.commit()
        click.echo("✅ Proveedores poblados exitosamente")

    @app.cli.command()
    @with_appcontext
    def init_db():
        """Inicializar base de datos con datos de prueba"""
        click.echo("🏗️  Inicializando base de datos...")

        # Crear todas las tablas
        db.create_all()
        click.echo("✅ Tablas creadas")

        # Ejecutar seeders
        servicios()
        estados_reclamo()
        proveedores()

        click.echo("🎉 Base de datos inicializada exitosamente")

    @app.cli.command()
    @with_appcontext
    def list_routes():
        """Listar todas las rutas disponibles"""
        from flask import current_app

        click.echo("🌐 Rutas disponibles:")
        for rule in current_app.url_map.iter_rules():
            methods = ",".join(sorted(rule.methods - {"OPTIONS", "HEAD"}))
            click.echo(f"{rule.endpoint:50} {methods:20} {rule.rule}")

    @app.cli.command()
    @with_appcontext
    def seed_transporte():
        """Poblar datos iniciales de transporte"""
        from .models.tipo_transporte import TipoTransporte
        from .models.tipo_incidente import TipoIncidente
        from .models.estado_reclamo import EstadoReclamo

        # Tipos de transporte
        tipos_transporte = [
            {
                "nombre": "Autobús Urbano",
                "descripcion": "Servicio de autobuses urbanos",
                "empresa_operadora": "Transporte Urbano SA",
            },
            {
                "nombre": "Microbús",
                "descripcion": "Servicio de microbuses",
                "empresa_operadora": "Micro Transporte",
            },
            {
                "nombre": "Taxi Colectivo",
                "descripcion": "Servicio de taxis colectivos",
                "empresa_operadora": "Colectivos Unidos",
            },
        ]

        for tipo_data in tipos_transporte:
            if not TipoTransporte.query.filter_by(nombre=tipo_data["nombre"]).first():
                tipo = TipoTransporte(**tipo_data)
                db.session.add(tipo)
                click.echo(f"Tipo transporte creado: {tipo.nombre}")

        # Tipos de incidente
        tipos_incidente = [
            {
                "nombre": "Accidente de tránsito",
                "categoria": "transito",
                "descripcion": "Colisión entre vehículos",
            },
            {
                "nombre": "Avería mecánica",
                "categoria": "mecanico",
                "descripcion": "Falla mecánica del vehículo",
            },
            {
                "nombre": "Problema de seguridad",
                "categoria": "seguridad",
                "descripcion": "Incidente de seguridad",
            },
            {
                "nombre": "Congestión vehicular",
                "categoria": "transito",
                "descripcion": "Tráfico congestionado",
            },
            {
                "nombre": "Cerrada de vía",
                "categoria": "transito",
                "descripcion": "Vía cerrada temporalmente",
            },
        ]

        for incidente_data in tipos_incidente:
            if not TipoIncidente.query.filter_by(
                nombre=incidente_data["nombre"]
            ).first():
                incidente = TipoIncidente(**incidente_data)
                db.session.add(incidente)
                click.echo(f"Tipo incidente creado: {incidente.nombre}")

        db.session.commit()
        click.echo("✅ Datos de transporte poblados exitosamente")
