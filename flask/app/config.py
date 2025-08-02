"""
Arquivo que carrega variáveis de ambiente e configurações do aplicativo.

:created by:    Mateus Herrera
:created at:    2025-08-01

:updated by:    Mateus Herrera
:updated at:    2025-08-02
"""

from os import getenv


class Config:
    """ Classe de configuração do aplicativo. """

    # Ambiente de execução
    FLASK_ENV   = getenv( 'FLASK_ENV', 'development' )
    SECRET_KEY  = getenv( 'SECRET_KEY', None )

    # OpenAI API Key
    OPENAI_API_KEY = getenv( 'OPENAI_API_KEY', None )

    # JWT Secret
    JWT_SECRET_KEY = getenv( 'JWT_SECRET_KEY', None )

    # SQLAlchemy - PostgreSQL
    SQLALCHEMY_DATABASE_URI         = getenv( 'SQLALCHEMY_DATABASE_URI', None )
    SQLALCHEMY_TRACK_MODIFICATIONS  = False

    PROJECT_SCHEMA = 'feedback_classifier' if FLASK_ENV != 'testing' else False
