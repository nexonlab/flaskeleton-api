class Config(object):
    DEBUG = False
    TESTING = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JSON_AS_ASCII = False
    params_conn = (
        "Driver={{ODBC Driver 17 for SQL Server}};"
        "Server={server};"
        "Database={database};"
        "APP=flaskeleton-api;"
        "UID=MY_USER;"
        "PWD=MY_PASSWORD;"
    )
    SQLALCHEMY_DATABASE_URI = (
        "sqlite:///../flaskeleton.db"  # default sqlalchemy uri
    )
    SQLALCHEMY_BINDS = {
        "development": "sqlite:///../flaskeleton.db",
        "production": "sqlite:///../flaskeleton.db",
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
