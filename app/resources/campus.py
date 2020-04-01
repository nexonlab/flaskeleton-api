from flask import (make_response, Blueprint, request)
from ..controllers.campus import CampusController
from ..errors import ErroInterno, UsoInvalido, TipoErro
from . import generic_handler, login_required, load_context


bp = Blueprint('campus', __name__, url_prefix='/campus')
bp.register_error_handler(ErroInterno, generic_handler)
bp.register_error_handler(UsoInvalido, generic_handler)


@bp.route('/', methods=['POST'])
@load_context
@login_required
def create():
    try:
        campus_controller = CampusController()
        if request.is_json:
            campus = campus_controller.criar_campus(request.json)

            resposta = make_response(campus, 200)
            resposta.headers['Content-Type'] = 'application/json'

            return resposta
        else:
            raise UsoInvalido(TipoErro.ERRO_VALIDACAO.name, payload="Payload não está no formato JSON.")
    except (ErroInterno, UsoInvalido) as e:
        raise e
    except Exception as e:
        raise ErroInterno(TipoErro.ERRO_INTERNO.name, ex=e, payload="Erro ao criar campus.")


@bp.route('/<int:codigo>', methods=['GET'])
@bp.route('/', methods=['GET'])
@load_context
@login_required
def retrieve(codigo: int = None):
    try:
        campus_controller = CampusController(codigo=codigo)

        resposta = make_response(campus_controller.recuperar_campus(), 200)
        resposta.headers['Content-Type'] = 'application/json'

        return resposta
    except (UsoInvalido, ErroInterno) as e:
        raise e
    except Exception as e:
        raise ErroInterno(TipoErro.ERRO_INTERNO.name, ex=e, payload="Erro ao recuperar campus.")


@bp.route('/<int:codigo>', methods=['PUT'])
@load_context
@login_required
def update(codigo: int = None):
    try:
        campus_controller = CampusController(codigo=codigo)
        if request.is_json:
            resposta = make_response(campus_controller.atualizar_campus(request.json), 200)
            resposta.headers['Content-Type'] = 'application/json'

            return resposta
        else:
            raise UsoInvalido(TipoErro.ERRO_VALIDACAO.name, payload="Payload não está no formato JSON.")
    except (UsoInvalido, ErroInterno) as e:
        raise e
    except Exception as e:
        raise ErroInterno(TipoErro.ERRO_INTERNO.name, ex=e, payload="Erro ao atualizar campus.")


@bp.route('/<int:codigo>', methods=['DELETE'])
@load_context
@login_required
def delete(codigo: int = None):
    try:
        campus_controller = CampusController(codigo=codigo)
        campus_controller.deletar_campus()

        return make_response()
    except (UsoInvalido, ErroInterno) as e:
        raise e
    except Exception as e:
        raise ErroInterno(TipoErro.ERRO_INTERNO.name, ex=e, payload="Erro ao deletar campus.")
