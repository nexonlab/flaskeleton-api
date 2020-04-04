import os


class Config(object):
    DEBUG = False
    TESTING = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JSON_AS_ASCII = False
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URI")
    APP_BINDS = {
        "development": os.getenv("DATABASE_DEV"),
        "production": os.getenv("DATABASE_PROD"),
    }


class DevelopmentConfig(Config):
    DEBUG = True
    CONTEXT = "Development"


class TestConfig(Config):
    DEBUG = True
    TESTING = True
    CONTEXT = "Test"


class ProductionConfig(Config):
    DEBUG = False
    CONTEXT = "Production"
