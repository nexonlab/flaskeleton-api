import os
from dotenv import load_dotenv


basedir = os.path.abspath(os.getcwd())
load_dotenv(os.path.join(basedir, ".env"))


class Config(object):
    DEBUG = False
    TESTING = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JSON_AS_ASCII = False
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URI")
    APP_BINDS = {
        "development": os.environ.get("DATABASE_DEV"),
        "production": os.environ.get("DATABASE_PROD"),
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
