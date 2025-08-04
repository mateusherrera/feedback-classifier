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
    LLM_MODEL      = 'gpt-3.5-turbo'

    # JWT Secret
    JWT_SECRET_KEY = getenv( 'JWT_SECRET_KEY', None )

    # SQLAlchemy - PostgreSQL
    SQLALCHEMY_DATABASE_URI         = getenv( 'SQLALCHEMY_DATABASE_URI', None )
    SQLALCHEMY_TRACK_MODIFICATIONS  = False

    PROJECT_SCHEMA = 'feedback_classifier' if FLASK_ENV != 'testing' else False

    # Redis Cache
    CACHE_TYPE              = getenv( 'CACHE_TYPE', 'RedisCache' )
    CACHE_REDIS_HOST        = getenv( 'CACHE_REDIS_HOST', 'redis' )
    CACHE_REDIS_PORT        = int( getenv('CACHE_REDIS_PORT', 6379) )
    CACHE_REDIS_DB          = int( getenv('CACHE_REDIS_DB', 0) )
    CACHE_DEFAULT_TIMEOUT   = int( getenv('CACHE_DEFAULT_TIMEOUT', 60) )

    # Email Configuration
    MAIL_SERVER         = getenv("MAIL_SERVER")
    MAIL_PORT           = int(getenv("MAIL_PORT", 587))
    MAIL_USE_TLS        = True
    MAIL_USERNAME       = getenv("MAIL_USERNAME")
    MAIL_PASSWORD       = getenv("MAIL_PASSWORD")
    MAIL_DEFAULT_SENDER = getenv("MAIL_DEFAULT_SENDER")
    CELERY_BROKER_URL   = getenv("CELERY_BROKER_URL", "redis://redis:6379/0")
