from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_restx import Api

# Inicializar extensiones
db = SQLAlchemy()
migrate = Migrate()
api = Api(
    title="API de Servicios Públicos",
    version="1.0",
    description="API para gestión de servicios públicos",
    doc="/docs/",
)
