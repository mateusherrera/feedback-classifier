"""
Arquivo para configuração de testes do Flask.

:created by:    Mateus Herrera
:created at:    2025-08-02

:updated by:  Mateus Herrera
:updated at:  2025-08-02
"""

# Configurações de ambiente para testes
import os
os.environ['FLASK_ENV']                         = 'testing'
os.environ['TESTING']                           = 'true'
os.environ['SECRET_KEY']                        = 'test-secret'
os.environ['OPENAI_API_KEY']                    = 'fake-openai-key'
os.environ['JWT_SECRET_KEY']                    = 'test-jwt-secret'
os.environ['SQLALCHEMY_DATABASE_URI']           = 'sqlite:///:memory:'
os.environ['SQLALCHEMY_TRACK_MODIFICATIONS']    = 'false'
os.environ['CACHE_TYPE']                        = 'SimpleCache'

import pytest

from app.extensions     import db
from app.main           import create_app


@pytest.fixture
def app():
    """ Função para criar uma instância do aplicativo Flask para testes. """

    app = create_app()
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()


@pytest.fixture
def client(app):
    """ Função para criar um cliente de teste do Flask. """

    return app.test_client()
