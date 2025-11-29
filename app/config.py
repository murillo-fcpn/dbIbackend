import os
from datetime import timedelta


class Config:
    """Configuración base"""

    SECRET_KEY = os.environ.get("SECRET_KEY") or "dev-secret-key"
    DEBUG = False
    TESTING = False

    # Database
    SQLALCHEMY_DATABASE_URI = (
        os.environ.get("DATABASE_URL")
        or "postgresql://username:password@localhost/servicios_db"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ENGINE_OPTIONS = {"pool_recycle": 300, "pool_pre_ping": True}


class DevelopmentConfig(Config):
    """Configuración de desarrollo"""

    DEBUG = True
    SQLALCHEMY_ECHO = True


class ProductionConfig(Config):
    """Configuración de producción"""

    DEBUG = False
    # Usar variable de entorno en producción
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL")


class TestingConfig(Config):
    """Configuración de testing"""

    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"


config = {
    "development": DevelopmentConfig,
    "production": ProductionConfig,
    "testing": TestingConfig,
    "default": DevelopmentConfig,
}
