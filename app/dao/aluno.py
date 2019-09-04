import simplejson
from ..models.aluno import Aluno


class AlunoDAO:

    @staticmethod
    def recupera_aluno(aluno: Aluno):
        try:

            with open('./app/models/data.json') as json_file:
                dados = simplejson.load(json_file)

            if aluno.codigo is not None:
                for t in dados:
                    if t['codigo'] == aluno.codigo:
                        return t
            else:
                return dados
        except Exception as e:
            raise e
