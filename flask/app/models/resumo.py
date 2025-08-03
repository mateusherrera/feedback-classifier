"""
Arquivo para o modelo Resumo Semanal

:created by:    Mateus Herrera
:created at:    2025-08-03

:updated by:    Mateus Herrera
:updated at:    2025-08-03
"""

from uuid import uuid4

from app.extensions import db


class ResumoSemanal(db.Model):
    """ Modelo para tabela de Resumos Semanais. """

    __tablename__ = "resumos_semanais"

    id          = db.Column( db.String, primary_key=True, default=lambda: str(uuid4())          )
    texto       = db.Column( db.Text, nullable=False                                            )
    created_at  = db.Column( db.DateTime, server_default=db.func.now()                          )
    updated_at  = db.Column( db.DateTime, server_default=db.func.now(), onupdate=db.func.now()  )
