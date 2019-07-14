import pytest

from app import create_app
from app.config import TestConfig


@pytest.fixture
def app():

    app = create_app()
    app.config.from_object(TestConfig)

    yield app


@pytest.fixture
def client(app):
    return app.test_client()
