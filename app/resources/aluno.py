from flask import (make_response, Blueprint, current_app)
from ..controllers.aluno import AlunoController
from ..errors import ErroInterno, UsoInvalido, TipoErro
from . import generic_handler


bp = Blueprint('aluno', __name__, url_prefix='/aluno')
bp.register_error_handler(ErroInterno, generic_handler)
bp.register_error_handler(UsoInvalido, generic_handler)


@bp.route('/<int:codigo>', methods=('GET',))
@bp.route('/', methods=('GET',))
def get_aluno(codigo: int=None):
    """
    View function para recuperar os alunos. Duas rotas são mapeadas, uma com um codigo e 
    outra sem. Caso seja passado um codigo, um aluno especifico é retornado.

    :param codigo: código do aluno.
    :return: 200 - uma lista de alunos ou aluno buscado.
             404 - erro na requisição.
             500 - erro interno.
    """
    try:
        # aqui o controller trata a resposta e manda o JSON no formato correto.
        aluno_controller = AlunoController(cpd=codigo)
        resposta = aluno_controller.recuperar_aluno()

        # criando a resposta da requisicao
        response = make_response(resposta, 200)
        response.headers['Content-Type'] = 'application/json'

        # enviando a resposta para o requisitante
        return response
    except UsoInvalido as e:
        raise e
    except ErroInterno as e:
        raise e
    except Exception as e:
        raise ErroInterno(TipoErro.ERRO_INTERNO.name, ex=e, payload="Erro ao recuperar aluno.")
