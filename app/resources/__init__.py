import simplejson
from flask import (jsonify, current_app, request, g, make_response)
from functools import wraps


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        response = make_response(simplejson.dumps({"message": "Not authorized."}), 401)
        response.headers['Content-Type'] = "application/json"
        if 'Authorization' in request.headers:
            if request.headers['Authorization'] != '123':
                return response
        else:
            return response
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
    current_app.logger.error(error.ex)
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response
