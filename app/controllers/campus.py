from ..errors import ErroInterno, TipoErro, UsoInvalido
from ..dao.campus import CampusDAO
from ..models.campus import Campus, CampusSchema
from ..logger import logger


class CampusController:
    __instance = None

    def __new__(cls, codigo: int = None):
        if CampusController.__instance is None:
            CampusController.__instance = object.__new__(cls)
        return CampusController.__instance

    def __init__(self, codigo: int = None):
        self.__campus = Campus(codigo=codigo)
        self.__campus_dao = CampusDAO(self.__campus)

    def recuperar_campus(self) -> list or Campus:
        try:
            resultado = self.__campus_dao.get()
            if resultado is not None:
                logger.info("campus recuperado com sucesso")
                if isinstance(resultado, list):
                    return CampusSchema().jsonify(resultado, many=True)
                else:
                    return CampusSchema().jsonify(resultado)
            else:
                raise UsoInvalido(
                    TipoErro.NAO_ENCONTRADO.name,
                    payload="Campus não foi encontrado.",
                    status_code=404,
                )
        except (ErroInterno, UsoInvalido) as e:
            raise e
        except Exception as e:
            raise ErroInterno(
                TipoErro.ERRO_INTERNO.name,
                ex=e,
                payload="Erro ao recuperar campi disponíveis.",
            )

    def criar_campus(self, campus: dict = None) -> Campus:
        try:
            if self.__campus.codigo:
                raise UsoInvalido(
                    TipoErro.ALUNO_DUPLICADO.name, ex="Campus já existe."
                )
            else:
                if campus:
                    self.valida_campus(campus)
                    campus_dao = CampusDAO(self.__campus)
                    result = campus_dao.insert()
                    logger.info(
                        "campus {} criado com sucesso".format(
                            str(self.__campus)
                        )
                    )
                    return CampusSchema().jsonify(result)
                else:
                    raise UsoInvalido(
                        TipoErro.ERRO_VALIDACAO.name,
                        ex="Objeto Campus a ser inserido está nulo ou "
                        "vazio.",
                    )
        except (UsoInvalido, ErroInterno) as e:
            raise e
        except Exception as e:
            raise ErroInterno(
                TipoErro.ERRO_INTERNO.name,
                ex=e,
                payload="Ocorreu um erro ao criar Campus.",
            )

    def atualizar_campus(self, campus: dict = None) -> Campus:
        try:
            self.__campus = self.__campus_dao.get()
            self.__campus_dao = CampusDAO(self.__campus)
            if self.__campus:
                if campus:
                    self.valida_campus(campus)
                    result = self.__campus_dao.update()
                    logger.info("campus atualizado com sucesso")
                    return CampusSchema().jsonify(result)
                else:
                    raise UsoInvalido(
                        TipoErro.ERRO_VALIDACAO.name,
                        payload="Objeto Campus a ser atualizado está nulo "
                        "ou vazio.",
                    )
            else:
                raise UsoInvalido(
                    TipoErro.NAO_ENCONTRADO.name,
                    payload="Campus não existe.",
                    status_code=404,
                )
        except (UsoInvalido, ErroInterno) as e:
            raise e
        except Exception as e:
            raise ErroInterno(
                TipoErro.ERRO_INTERNO.name,
                ex=e,
                payload="Ocorreu um erro ao atualizar Campus.",
            )

    def deletar_campus(self) -> bool:
        try:
            self.__campus = self.__campus_dao.get()
            self.__campus_dao = CampusDAO(self.__campus)
            if self.__campus:
                if self.__campus_dao.delete():
                    logger.info("campus deletado com sucesso")
                    return True
                else:
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
                payload="Ocorreu um erro ao deletar Campus.",
            )

    def valida_campus(self, campus: dict) -> Campus:
        attrs = ["descricao"]
        for k, v in campus.items():
            if k not in attrs:
                raise UsoInvalido(
                    TipoErro.ERRO_VALIDACAO.name,
                    payload="Attributo '" + k + "' não é válido.",
                )
            setattr(self.__campus, k, v)

        return self.__campus
