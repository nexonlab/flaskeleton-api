import pytest

from app import create_app
from app.models.db import db
from app.models.aluno import Aluno
from app.models.campus import Campus


@pytest.fixture(scope="session")
def app():
    try:
        app = create_app({
            "TESTING": True,
            "DEBUG": False,
            "SQLALCHEMY_DATABASE_URI": "sqlite:///",
            "SQLALCHEMY_TRACK_MODIFICATIONS": False,
        })

        ctx = app.app_context()
        ctx.push()

        db.create_all()
        db.session.add(Aluno(nome="Joao da Silva", email="joaosilva@email.com"))
        db.session.add(Campus(descricao="Campus Teste"))
        db.session.commit()

        yield app

        db.drop_all()
    except Exception as e:
        print(e)
        raise e


@pytest.fixture(scope="session")
def client(app):
    test_client = app.test_client()
    ctx = app.app_context()
    ctx.push()
    yield test_client
