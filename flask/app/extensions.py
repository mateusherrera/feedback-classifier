"""
Arquivo para carregar extensões do Flask.

:created by:    Mateus Herrera
:created at:    2025-08-01

:updated by:    Mateus Herrera
:updated at:    2025-08-03
"""

from sqlalchemy         import MetaData

from flask_mail         import Mail
from flask_caching      import Cache
from flask_sqlalchemy   import SQLAlchemy
from flask_jwt_extended import JWTManager

from app.config import Config

if Config.PROJECT_SCHEMA:
    metadata = MetaData(schema=Config.PROJECT_SCHEMA)
    db  = SQLAlchemy(metadata=metadata)
else:
    db  = SQLAlchemy()

jwt = JWTManager()

cache = Cache()

mail = Mail()
