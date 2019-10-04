import simplejson
from ..models.aluno import Aluno


class AlunoDAO:

    def __init__(self, aluno: Aluno=None):
        self.__aluno = aluno

    def recupera_aluno(self):
        try:

            with open('./app/models/data.json') as json_file:
                dados = simplejson.load(json_file)

            if self.__aluno.codigo is not None:
                for t in dados:
                    if t['codigo'] == self.__aluno.codigo:
                        return t
            else:
                return dados
        except Exception as e:
            raise e
