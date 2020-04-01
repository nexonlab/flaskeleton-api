import logging
from flask import Flask, request, g
from flask_cors import CORS
from .models.db import db
from .config import Config, DevelopmentConfig
from flask_migrate import Migrate
<<<<<<< HEAD
from .logger import logger
=======
import os
from gevent import monkey
>>>>>>> Adicionando gevent


__author__ = "NTI CEUMA"
__email__ = "nti@ceuma.br"
__version__ = "v0.0.1"


binds = {}


def setup_logger(app):
    gunicorn_logger = logging.getLogger("gunicorn.error")
    app.logger.handlers = gunicorn_logger.handlers
    app.logger.setLevel(gunicorn_logger.level)


def setup_engine(db):
    for k, v in Config.APP_BINDS.items():
        if v:
            binds[k] = db.create_engine(v)


def log_request():
    logger.request()


def get_tenant():
    if "Context" in request.headers:
        g.context = request.headers["Context"]
        g.tenant = binds[g.context]
    else:
        g.tenant = None


def create_app(test_config=None):

    # cria e configura a aplicacao
    app = Flask(__name__, instance_relative_config=True)

    setup_logger(app)

    # modificando prefixo da url
    app.wsgi_app = PrefixMiddleware(app.wsgi_app, prefix="/flaskeleton-api")

    if test_config is None:
        # carrega uma instancia de configuracao
        app.config.from_object(DevelopmentConfig)
    else:
        # carrega a instancia test_config passada por parametro
        app.config.from_mapping(test_config)

    # registra as blueprints de resources
    from .resources.campus import bp as bp_campus
    from .resources.aluno import bp as bp_aluno
    from .resources.docs import bp as bp_docs

    app.register_blueprint(bp_campus)
    app.register_blueprint(bp_aluno)
    app.register_blueprint(bp_docs)

    db.init_app(app)
    migrate = Migrate(app, db)  # noqa: F841
    setup_engine(db)
    CORS(app)

    app.before_request(log_request)
    app.before_request(get_tenant)

    return app


class PrefixMiddleware(object):
    def __init__(self, app, prefix=""):
        self.app = app
        self.prefix = prefix

    def __call__(self, environ, start_response):

        if environ["PATH_INFO"].startswith(self.prefix):
            environ["PATH_INFO"] = environ["PATH_INFO"][len(self.prefix) :]
            environ["SCRIPT_NAME"] = self.prefix
            return self.app(environ, start_response)
        else:
            start_response("404", [("Content-Type", "text/plain")])
            return [
                "Esta URL nao pertence a aplicacao. "
                "Por favor, insira o prefixo '/flaskeleton-api'.".encode()
            ]
