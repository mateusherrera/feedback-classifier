"""
Arquivo para configuração de testes do Flask.

:created by:    Mateus Herrera
:created at:    2025-08-02

:updated by:    Mateus Herrera
:updated at:    2025-08-03
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
os.environ['MAIL_SERVER']                       = 'localhost'
os.environ['MAIL_PORT']                         = '1025'
os.environ['MAIL_USERNAME']                     = ''
os.environ['MAIL_PASSWORD']                     = ''
os.environ['MAIL_DEFAULT_SENDER']               = 'no-reply@test.local'
os.environ['STAKEHOLDERS_EMAILS']               = 'a@a.com,b@b.com'
os.environ['CELERY_BROKER_URL']                 = 'memory://'
os.environ['CELERY_TASK_ALWAYS_EAGER']          = 'True'
os.environ['CELERY_TASK_EAGER_PROPAGATES']      = 'True'

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
