from flask import (make_response, Blueprint, request)
from ..controllers.aluno import AlunoController
from ..errors import ErroInterno, UsoInvalido, TipoErro
from . import generic_handler, login_required, load_context


bp = Blueprint('aluno', __name__, url_prefix='/aluno')
bp.register_error_handler(ErroInterno, generic_handler)
bp.register_error_handler(UsoInvalido, generic_handler)


@bp.route('/', methods=['POST'])
@load_context
@login_required
def create():
    try:
        aluno_controller = AlunoController()
        if request.is_json:
            aluno = aluno_controller.criar_aluno(request.json)

            resposta = make_response(aluno, 200)
            resposta.headers['Content-Type'] = 'application/json'

            return resposta
        else:
            raise UsoInvalido(TipoErro.ERRO_VALIDACAO.name, payload="Payload não está no formato JSON.")
    except (ErroInterno, UsoInvalido) as e:
        raise e
    except Exception as e:
        raise ErroInterno(TipoErro.ERRO_INTERNO.name, ex=e, payload="Erro ao criar aluno.")


@bp.route('/<int:codigo>', methods=['GET'])
@bp.route('/', methods=['GET'])
@load_context
def retrieve(codigo: int = None):
    try:
        aluno_controller = AlunoController(codigo=codigo)

        resposta = make_response(aluno_controller.recuperar_aluno(), 200)
        resposta.headers['Content-Type'] = 'application/json'

        return resposta
    except (UsoInvalido, ErroInterno) as e:
        raise e
    except Exception as e:
        raise ErroInterno(TipoErro.ERRO_INTERNO.name, ex=e, payload="Erro ao recuperar aluno.")


@bp.route('/<int:codigo>', methods=['PUT'])
@load_context
@login_required
def update(codigo: int = None):
    try:
        aluno_controller = AlunoController(codigo=codigo)
        if request.is_json:
            aluno = aluno_controller.atualizar_aluno(request.json)

            resposta = make_response(aluno, 200)
            resposta.headers['Content-Type'] = 'application/json'

            return resposta
        else:
            raise UsoInvalido(TipoErro.ERRO_VALIDACAO.name, payload="Payload não está no formato JSON.")
    except (UsoInvalido, ErroInterno) as e:
        raise e
    except Exception as e:
        raise ErroInterno(TipoErro.ERRO_INTERNO.name, ex=e, payload="Erro ao atualizar aluno.")


@bp.route('/<int:codigo>', methods=['DELETE'])
@load_context
@login_required
def delete(codigo: int = None):
    try:
        aluno_controller = AlunoController(codigo=codigo)
        aluno_controller.deletar_aluno()

        return make_response(204)
    except (UsoInvalido, ErroInterno) as e:
        raise e
    except Exception as e:
        raise ErroInterno(TipoErro.ERRO_INTERNO.name, ex=e, payload="Erro ao deletar aluno.")
