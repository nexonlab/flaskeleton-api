from ..models.campus import Campus
from . import DAO


class CampusDAO(DAO):
    __instance = None

    def __new__(cls, campus: Campus = None):
        if CampusDAO.__instance is None:
            CampusDAO.__instance = object.__new__(cls)
        return CampusDAO.__instance

    def __init__(self, campus: Campus = None):
        super().__init__(campus)
        self.__campus = campus

    def get(self) -> list or Campus:
        if self.__campus.codigo:
            self.__campus = (
                self.session.query(Campus)
                .filter_by(codigo=self.__campus.codigo)
                .first()
            )
            return self.__campus
        else:
            return self.session.query(Campus).all()
