import simplejson
from ..errors import ErroInterno, TipoErro
from ..dao.campus import CampusDAO
from ..models.campus import Campus
from . import alchemy_encoder


class CampusController:
    __instance = None

    def __new__(cls, codigo: int = None):
        if CampusController.__instance is None:
            CampusController.__instance = object.__new__(cls)
        return CampusController.__instance

    def __init__(self, codigo: int = None):
        self.__campus_dao = CampusDAO(Campus(codigo=codigo))

    def recuperar_campus(self):
        """
        Método que recupera os alunos e trata a resposta para o formato JSON e então retorna para a View Function.

        :return: uma lista de objetos contendo informacoes dos campi.
        :exception ErroInterno
        """
        try:
            resultado = self.__campus_dao.get()

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
