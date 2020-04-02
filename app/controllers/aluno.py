from ..errors import UsoInvalido, ErroInterno, TipoErro
from ..dao.aluno import AlunoDAO
from ..models.aluno import Aluno, AlunoSchema
from ..logger import logger
import re


class AlunoController:

    __instance = None

    def __new__(cls, codigo: int = None):
        if AlunoController.__instance is None:
            AlunoController.__instance = object.__new__(cls)
        return AlunoController.__instance

    def __init__(self, codigo: int = None):
        self.__aluno = Aluno(codigo=codigo)
        self.__aluno_dao = AlunoDAO(self.__aluno)

    def recuperar_aluno(self) -> list or Aluno:
        try:
            resultado = self.__aluno_dao.get()
            if resultado is not None:
                logger.info("aluno(s) recuperado(s) com sucesso")
                if isinstance(resultado, list):
                    return AlunoSchema().jsonify(resultado, many=True)
                else:
                    return AlunoSchema().jsonify(resultado)
            else:
                raise UsoInvalido(
                    TipoErro.NAO_ENCONTRADO.name,
                    payload="Aluno não foi encontrado.",
                    status_code=404,
                )
        except (UsoInvalido, ErroInterno) as e:
            raise e
        except Exception as e:
            raise ErroInterno(
                TipoErro.ERRO_INTERNO.name,
                ex=e,
                payload="Ocorreu um erro ao recuperar aluno(s).",
            )

    def criar_aluno(self, aluno: dict = None) -> Aluno:
        try:
            if self.__aluno.codigo:
                raise UsoInvalido(
                    TipoErro.ALUNO_DUPLICADO.name, ex="Aluno já existe."
                )
            else:
                if aluno:
                    self.valida_aluno(aluno)
                    aluno_dao = AlunoDAO(self.__aluno)
                    result = aluno_dao.insert()
                    logger.info(
                        "aluno {} criado com sucesso".format(str(self.__aluno))
                    )
                    return AlunoSchema().jsonify(result)
                else:
                    raise UsoInvalido(
                        TipoErro.ERRO_VALIDACAO.name,
                        ex="Objeto aluno a ser inserido está nulo ou "
                        "vazio.",
                    )
        except (UsoInvalido, ErroInterno) as e:
            raise e
        except Exception as e:
            raise ErroInterno(
                TipoErro.ERRO_INTERNO.name,
                ex=e,
                payload="Ocorreu um erro ao criar aluno.",
            )

    def atualizar_aluno(self, aluno: dict = None) -> Aluno:
        try:
            self.__aluno = self.__aluno_dao.get()
            self.__aluno_dao = AlunoDAO(self.__aluno)
            if self.__aluno:
                if aluno:
                    self.valida_aluno(aluno)
                    result = self.__aluno_dao.update()
                    logger.info("aluno atualizado com sucesso")
                    return AlunoSchema().jsonify(result)
                else:
                    raise UsoInvalido(
                        TipoErro.ERRO_VALIDACAO.name,
                        payload="Objeto aluno a ser atualizado está nulo "
                        "ou vazio.",
                    )
            else:
                raise UsoInvalido(
                    TipoErro.NAO_ENCONTRADO.name,
                    payload="Aluno não existe.",
                    status_code=404,
                )
        except (UsoInvalido, ErroInterno) as e:
            raise e
        except Exception as e:
            raise ErroInterno(
                TipoErro.ERRO_INTERNO.name,
                ex=e,
                payload="Ocorreu um erro ao atualizar aluno.",
            )

    def deletar_aluno(self) -> bool:
        try:
            self.__aluno = self.__aluno_dao.get()
            self.__aluno_dao = AlunoDAO(self.__aluno)
            if self.__aluno:
                if self.__aluno_dao.delete():
                    logger.info(
                        "aluno {} deletado com sucesso".format(
                            self.__aluno.codigo
                        )
                    )
                    return True
                return False
            else:
                raise UsoInvalido(
                    TipoErro.NAO_ENCONTRADO.name,
                    payload="Aluno não existe.",
                    status_code=404,
                )
        except (UsoInvalido, ErroInterno) as e:
            raise e
        except Exception as e:
            raise ErroInterno(
                TipoErro.ERRO_INTERNO.name,
                ex=e,
                payload="Ocorreu um erro ao deletar aluno.",
            )

    def valida_aluno(self, aluno: dict) -> Aluno:
        attrs = ["nome", "email", "endereco"]
        for k, v in aluno.items():
            if k not in attrs:
                raise UsoInvalido(
                    TipoErro.ERRO_VALIDACAO.name,
                    payload="Attributo '" + k + "' não é válido.",
                )
            setattr(self.__aluno, k, v)

        regex = r"[^@]+@[^@]+\.[^@]+"
        if self.__aluno.email:
            if not re.search(regex, self.__aluno.email):
                raise UsoInvalido(
                    TipoErro.ERRO_VALIDACAO.name, payload="E-mail inválido."
                )

        return self.__aluno
