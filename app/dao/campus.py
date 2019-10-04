from flask import (g)
from ..models.db import db
from ..models.campus import Campus


class CampusDAO:

    def __init__(self, campus: Campus=None):
        self.__campus = campus

    def recupera_campus(self):
        """
        Método que busca todos os campi disponíveis.

        :return: uma lista com todos os campi.
        :exception Exception: Lança uma exceção genérica caso ocorra algum erro.
        """
        try:
            sql = db.select([
                db.text("CODIGO, DESCRICAO")
            ]).select_from(
                db.text("CAMPUS")
            )

            if self.__campus is not None:
                if self.__campus.codigo is not None:
                    sql = sql.where(
                        db.text(
                            """
                            CODIGO = :codigo
                            """
                        )
                    )

            resultado = db.get_engine(bind=g.context).execute(sql, codigo=self.__campus.codigo).fetchall()

            return resultado
        except Exception as e:
            raise e
