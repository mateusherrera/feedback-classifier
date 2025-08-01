"""
Arquivo para carregar extensões do Flask.

:created by:    Mateus Herrera
:created at:    2025-08-01

:updated by:    Mateus Herrera
:updated at:    2025-08-01
"""

from flask_sqlalchemy   import SQLAlchemy
from flask_jwt_extended import JWTManager


db  = SQLAlchemy()
jwt = JWTManager()
