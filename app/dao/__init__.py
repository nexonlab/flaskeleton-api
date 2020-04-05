from flask import g
from sqlalchemy.orm import sessionmaker
from ..models.db import db


class DAO:

    __instance = None
    __session = {}

    def __new__(cls, obj: object = None):
        if DAO.__instance is None:
            DAO.__instance = object.__new__(cls)
        return DAO.__instance

    def __init__(self, obj: object):
        self.__obj = obj
        if g.tenant:
            if g.tenant not in DAO.__session:
                self.__Session = sessionmaker(bind=g.tenant)
                DAO.__session[g.tenant] = self.__Session()
                self.session = DAO.__session[g.tenant]
            else:
                self.session = DAO.__session[g.tenant]
        else:
            self.session = db.session

    def get(self) -> list or object:
        pass

    def update(self) -> object:
        try:
            self.session.add(self.__obj)
            self.session.commit()
            return self.__obj
        except Exception as e:
            self.session.rollback()
            raise e

    def delete(self) -> bool:
        try:
            self.session.delete(self.__obj)
            self.session.commit()
            return True
        except Exception as e:
            self.session.rollback()
            raise e

    def insert(self) -> object:
        try:
            self.session.add(self.__obj)
            self.session.commit()
            return self.__obj
        except Exception as e:
            self.session.rollback()
            raise e
