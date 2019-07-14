from flask import (Blueprint, current_app, render_template)
from ..errors import ErroInterno, UsoInvalido, TipoErro
from . import generic_handler


bp = Blueprint('docs', __name__, url_prefix='/apidocs')
bp.register_error_handler(ErroInterno, generic_handler)
bp.register_error_handler(UsoInvalido, generic_handler)


@bp.route('/', methods=('GET',))
def apidocs():
    """
    View function para retornar a documentacao de API.
    """
    try:
        return render_template('/apidocs/index.html')
    except UsoInvalido as e:
        raise e
    except ErroInterno as e:
        raise e
    except Exception as e:
        raise ErroInterno(TipoErro.ERRO_INTERNO.name, ex=e, payload="Erro ao renderizar documentacao.")
