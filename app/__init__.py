import logging
from flask import Flask
from logging import Formatter
from logging.handlers import RotatingFileHandler
from flask_cors import CORS
from .models.db import db
from .config import DevelopmentConfig


__author__ = "NTI CEUMA"
__email__ = "nti@ceuma.br"
__version__ = "v0.0.1"


def create_app(test_config=None):

    # cria e configura a aplicacao
    app = Flask(__name__, instance_relative_config=True)

    # configurando log do gunicorn para escrita em arquivo
    gunicorn_logger = logging.getLogger('gunicorn.error')
    file_handler = RotatingFileHandler('logs/app.log', maxBytes=1024, backupCount=2)
    file_handler.setFormatter(Formatter(
        '%(asctime)s %(levelname)s: %(message)s '
        '[in %(pathname)s:%(lineno)d]'
    ))
    file_handler.setLevel(logging.DEBUG)
    gunicorn_logger.addHandler(file_handler)

    # adicionando logger do gunicorn a aplicacao
    app.logger.handlers = gunicorn_logger.handlers
    app.logger.setLevel(gunicorn_logger.level)

    # modificando prefixo da url
    app.wsgi_app = PrefixMiddleware(app.wsgi_app, prefix='/flaskeleton-api')

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
    CORS(app)

    return app


class PrefixMiddleware(object):

    def __init__(self, app, prefix=''):
        self.app = app
        self.prefix = prefix

    def __call__(self, environ, start_response):

        if environ['PATH_INFO'].startswith(self.prefix):
            environ['PATH_INFO'] = environ['PATH_INFO'][len(self.prefix):]
            environ['SCRIPT_NAME'] = self.prefix
            return self.app(environ, start_response)
        else:
            start_response('404', [('Content-Type', 'text/plain')])
            return ["Esta URL nao pertence a aplicacao. Por favor, insira o prefixo '/flaskeleton-api'."
                    .encode()]
