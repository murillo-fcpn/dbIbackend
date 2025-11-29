from flask import Flask
from .config import config
from .extensions import db, migrate, api


def create_app(config_name="default"):
    app = Flask(__name__)
    app.config.from_object(config[config_name])

    # Inicializar extensiones
    db.init_app(app)
    migrate.init_app(app, db)
    api.init_app(app)

    # Registrar namespaces
    from .resources.servicios import servicios_ns
    from .resources.proveedores import proveedores_ns
    from .resources.medidores import medidores_ns
    from .resources.tipos_reclamo import tipos_reclamo_ns

    from .resources.tipos_transporte import tipos_transporte_ns
    from .resources.tipos_incidente import tipos_incidente_ns
    from .resources.operadores import operadores_ns
    from .resources.conductores import conductores_ns
    from .resources.vehiculos import vehiculos_ns
    from .resources.rutas import rutas_ns

    api.add_namespace(servicios_ns, path="/api/servicios")
    api.add_namespace(proveedores_ns, path="/api/proveedores")
    api.add_namespace(medidores_ns, path="/api/medidores")
    api.add_namespace(tipos_reclamo_ns, path="/api/tipos-reclamo")

    api.add_namespace(tipos_transporte_ns, path="/api/tipos-transporte")
    api.add_namespace(tipos_incidente_ns, path="/api/tipos-incidente")
    api.add_namespace(operadores_ns, path="/api/operadores")
    api.add_namespace(conductores_ns, path="/api/conductores")
    api.add_namespace(vehiculos_ns, path="/api/vehiculos")
    api.add_namespace(rutas_ns, path="/api/rutas")

    # Registrar comandos CLI
    from .commands import register_commands

    register_commands(app)

    return app
