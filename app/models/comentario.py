"""
Arquivo para definição do modelo de Comntário.

:created by:    Mateus Herrera
:created at:    2025-08-01

:updated by:    Mateus Herrera
:updated at:    2025-08-01
"""

from uuid import uuid4

from extensions import db


class Comentario(db.Model):
    """ Modelo para tabela de Comentários. """

    __tablename__ = 'comentario'

    id          = db.Column( db.String, primary_key=True, default=lambda: str(uuid4())          )
    texto       = db.Column( db.Text, nullable=False                                            )
    categoria   = db.Column( db.String(50), nullable=False                                      )
    tags        = db.Column( db.ARRAY(db.String), nullable=True                                 )
    confianca   = db.Column( db.Float, nullable=False                                           )
    created_at  = db.Column( db.DateTime, server_default=db.func.now()                          )
    updated_at  = db.Column( db.DateTime, server_default=db.func.now(), onupdate=db.func.now()  )
