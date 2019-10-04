from ..errors import UsoInvalido, ErroInterno, TipoErro
from ..dao.aluno import AlunoDAO
from ..models.aluno import Aluno
from . import alchemy_encoder
import simplejson


class AlunoController:

    def __init__(self, cpd=None):
        self.__cpd = cpd


    def recuperar_aluno(self):
        """
        Método que recupera os alunos e trata a resposta para o formato JSON e então retorna para a View Function.

        :return: um objeto do tipo JSON pronto para ser enviado como resposta pela view function.
        """
        try:
            
            aluno_dao = AlunoDAO(Aluno(codigo=self.__cpd))
            resultado = aluno_dao.recupera_aluno()

            # transforma o resultado da consulta em JSON efetuando um dump para JSON utilizando um encoder proprio
            if resultado is not None:
                if isinstance(resultado, list):
                    resposta = simplejson.dumps([dict(aluno) for aluno in resultado], default=alchemy_encoder,
                                                ensure_ascii=False)
                else:
                    resposta = simplejson.dumps(dict(resultado), default=alchemy_encoder, ensure_ascii=False)
            else:
                return simplejson.dumps({})
            return resposta
        except UsoInvalido as e:
            raise e
        except ErroInterno as e:
            raise e
        except Exception as e:
            raise ErroInterno(TipoErro.ERRO_INTERNO.name, ex=e, payload="Ocorreu um erro ao recuperar aluno(s).")
