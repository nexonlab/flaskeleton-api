from flask import g
from sqlalchemy.orm import sessionmaker
from ..models.db import db


class DAO:
    def __init__(self, obj: object):
        self.__obj = obj
        if g.tenant:
            self.__Session = sessionmaker(bind=g.tenant)
            self.session = self.__Session()
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
