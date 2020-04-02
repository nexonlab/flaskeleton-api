from ..models.aluno import Aluno
from . import DAO


class AlunoDAO(DAO):

    __instance = None

    def __new__(cls, aluno: Aluno = None):
        if AlunoDAO.__instance is None:
            AlunoDAO.__instance = object.__new__(cls)
        return AlunoDAO.__instance

    def __init__(self, aluno: Aluno = None):
        super().__init__(aluno)
        self.__aluno = aluno

    def get(self) -> list or Aluno:
        if self.__aluno.codigo:
            self.__aluno = Aluno.query.filter_by(
                codigo=self.__aluno.codigo
            ).first()
            return self.__aluno
        else:
            return Aluno.query.all()
