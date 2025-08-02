"""
Arquivo para carregar extensões do Flask.

:created by:    Mateus Herrera
:created at:    2025-08-01

:updated by:    Mateus Herrera
:updated at:    2025-08-01
"""

from sqlalchemy         import MetaData
from flask_sqlalchemy   import SQLAlchemy
from flask_jwt_extended import JWTManager


metadata = MetaData(schema='flask-llm-api')

db  = SQLAlchemy(metadata=metadata)
jwt = JWTManager()
