from ..models.db import db


class DAO:

    def __init__(self, obj: object):
        self.__obj = obj

    def get(self) -> list or object:
        pass

    def update(self) -> object:
        try:
            db.session.add(self.__obj)
            db.session.commit()
            return self.__obj
        except Exception as e:
            db.session.rollback()
            raise e

    def delete(self) -> bool:
        try:
            db.session.delete(self.__obj)
            db.session.commit()
            return True
        except Exception as e:
            db.session.rollback()
            raise e

    def insert(self) -> object:
        try:
            db.session.add(self.__obj)
            db.session.commit()
            return self.__obj
        except Exception as e:
            db.session.rollback()
            raise e

