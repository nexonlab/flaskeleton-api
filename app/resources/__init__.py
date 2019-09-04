from flask import (jsonify, current_app, request, g)
from functools import wraps
from ..errors import TipoErro, UsoInvalido


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'Authorization' in request.headers:
            if request.headers['Authorization'] != '123':
                raise UsoInvalido(TipoErro.ERRO_VALIDACAO.name, status_code=401, payload="Wrong authorization value.")
        else:
            raise UsoInvalido(TipoErro.ERRO_VALIDACAO.name, status_code=401, payload="Missing authorization header.")
        return f(*args, **kwargs)
    return decorated_function


def load_context(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'Context' in request.headers:
            g.context = request.headers['Context']
        else:
            g.context = "development"
        return f(*args, **kwargs)
    return decorated_function


def generic_handler(error):
    """
    Handler genérico de erros. Espera um objeto do tipo Exception que contenha uma 
    funcao [to_dict] e um atributo [status_code] a fim de preparar a resposta do erro no 
    formato JSON.

    :param error: objeto a ser tratado pelo handler.
    :return: um objeto JSON a ser enviado como resposta para o requisitante.
    """
    if error.ex is not None:
        current_app.logger.error(error.ex)
    else:
        if error.payload is not None:
            current_app.logger.error(error.payload)
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response
