from flask import (jsonify, current_app)


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
