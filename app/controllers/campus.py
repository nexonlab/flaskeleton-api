import simplejson
from ..errors import ErroInterno, TipoErro
from ..dao.campus import CampusDAO
from . import alchemy_encoder


class CampusController:

    @staticmethod
    def recuperar_campus():
        """
        Método que recupera os alunos e trata a resposta para o formato JSON e então retorna para a View Function.

        :return: uma lista de objetos contendo informacoes dos campi.
        :exception ErroInterno
        """
        try:
            resultado = CampusDAO.recupera_campus()

            # transforma o resultado da consulta em JSON efetuando um dump para JSON utilizando um encoder proprio
            if isinstance(resultado, list):
                resposta = simplejson.dumps([dict(aluno) for aluno in resultado], default=alchemy_encoder,
                                            ensure_ascii=False)
            else:
                resposta = simplejson.dumps(dict(resultado), default=alchemy_encoder, ensure_ascii=False)

            return resposta
        except ErroInterno as e:
            raise e
        except Exception as e:
            raise ErroInterno(TipoErro.ERRO_INTERNO.name, ex=e, status_code=501,
                              payload="Erro ao recuperar campi disponíveis.")
