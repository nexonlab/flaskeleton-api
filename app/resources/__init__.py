from flask import jsonify, request, g
from functools import wraps
from ..errors import TipoErro, UsoInvalido, ErroInterno
from ..logger import logger


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # implementar aqui uma funcao de autorizacao
        # abaixo um exemplo basico com o token estatico `123`
        if "Authorization" in request.headers:
            if request.headers["Authorization"] != "123":
                raise UsoInvalido(
                    TipoErro.NAO_AUTORIZADO.name,
                    status_code=401,
                    payload="Token inválido.",
                )
        else:
            raise UsoInvalido(
                TipoErro.NAO_AUTORIZADO.name,
                status_code=401,
                payload="Cabeçalho de autorização não " "encontrado.",
            )
        return f(*args, **kwargs)

    return decorated_function


def load_context(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "Context" in request.headers:
            g.context = request.headers["Context"]
        return f(*args, **kwargs)

    return decorated_function


def generic_handler(error):
    """
    Handler genérico de erros. Espera um objeto do tipo
    Exception que contenha uma funcao [to_dict] e um atributo
    [status_code] a fim de preparar a resposta do erro no
    formato JSON.

    :param error: objeto a ser tratado pelo handler.
    :return: um objeto JSON a ser enviado como resposta para o requisitante.
    """
    if isinstance(error, UsoInvalido):
        logger.info(error.payload)
    else:
        logger.error(error.payload, error.ex)

    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response
