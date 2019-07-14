import urllib
import os


class Config(object):
    DEBUG = False
    TESTING = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_RECORD_QUERIES = True
    FLASK_SLOW_DB_QUERY_TIME = 0.2
    JSON_AS_ASCII = False
    params_conn = 'Driver={{ODBC Driver 17 for SQL Server}};' \
                  'Server={server};' \
                  'Database={database};' \
                  'APP=flaskeleton-api;' \
                  'UID=MY_USER;' \
                  'PWD=MY_PASSWORD;'
    SQLALCHEMY_DATABASE_URI = "mssql+pyodbc:///?odbc_connect=%s" % urllib.parse.quote_plus(params_conn)
    SQLALCHEMY_BINDS = {
        'development': "mssql+pyodbc:///?odbc_connect=%s" % urllib.parse.quote_plus(
            params_conn.format(server="development", database="db_development")),
        'production': "mssql+pyodbc:///?odbc_connect=%s" % urllib.parse.quote_plus(
            params_conn.format(server="production", database="db_production"))
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
