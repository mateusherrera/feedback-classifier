"""
Arquivo que carrega variáveis de ambiente e configurações do aplicativo.

:created by:    Mateus Herrera
:created at:    2025-08-01

:updated by:    Mateus Herrera
:updated at:    2025-08-01
"""

from os import getenv


class Config:
    """ Classe de configuração do aplicativo. """

    # Ambiente de execução
    ENV = getenv( 'ENV', 'dev' )

    # OpenAI API Key
    OPENAI_API_KEY = getenv( 'OPENAI_API_KEY', None )

    # JWT Secret
    JWT_SECRET = getenv( 'JWT_SECRET', None )

    # SQLAlchemy - PostgreSQL
    SQLALCHEMY_DATABASE_URI         = getenv( 'SQLALCHEMY_DATABASE_URI', None )
    SQLALCHEMY_TRACK_MODIFICATIONS  = False
