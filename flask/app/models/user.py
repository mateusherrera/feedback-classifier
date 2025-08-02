"""
Arquivo para definição do modelo de Users.

:created by:    Mateus Herrera
:created at:    2025-08-02

:updated by:    Mateus Herrera
:updated at:    2025-08-02
"""

from uuid               import uuid4
from werkzeug.security  import (
    generate_password_hash,
    check_password_hash,
)

from app.extensions import db


class User(db.Model):
    """ Modelo para tabela de Usuários. """

    __tablename__ = 'user'

    id              = db.Column( db.String, primary_key=True, default=lambda: str(uuid4())          )
    username        = db.Column( db.String(80), unique=True, nullable=False                         )
    password_hash   = db.Column( db.String(256), nullable=False                                     )
    created_at      = db.Column( db.DateTime, server_default=db.func.now()                          )
    updated_at      = db.Column( db.DateTime, server_default=db.func.now(), onupdate=db.func.now()  )

    def set_password(self, password: str):
        """ Define a senha do usuário. """

        self.password_hash = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        """ Verifica a senha do usuário. """

        return check_password_hash(self.password_hash, password)
