"""
Tasks com celery para o Flask app.

:created by:    Mateus Herrera
:created at:    2025-08-03

:updated by:    Mateus Herrera
:updated at:    2025-08-03
"""

from flask                  import Flask
from os                     import getenv
from celery                 import Celery
from celery.schedules       import crontab
from flask_mail             import Message
from datetime               import datetime

from app.config             import Config
from app.extensions         import db, mail
from app.main               import create_app
from app.models.resumo      import ResumoSemanal
from app.services.summary   import gerar_resumo_semana


CELERY_BROKER = Config.CELERY_BROKER_URL
cel = Celery(__name__, broker=CELERY_BROKER)
cel.conf.beat_schedule = {
    "resumo-semanal": {
        "task": "app.tasks.enviar_resumo_semanal",
        "schedule": crontab(day_of_week="sun", hour=0, minute=0),
    }
}

@cel.task(name="app.tasks.enviar_resumo_semanal")
def enviar_resumo_semanal():
    """ Envia o resumo semanal de feedbacks por e-mail para os stakeholders. """

    app = create_app()
    with app.app_context():
        texto = gerar_resumo_semana()

        # Salvar resumo
        resumo = ResumoSemanal(texto=texto)
        db.session.add(resumo)
        db.session.commit()

        # Envia por e-mail
        msg = Message(
            subject="Resumo Semanal de Feedbacks",
            recipients=getenv("STAKEHOLDERS_EMAILS", "").split(","),
            body=texto,
        )
        mail.send(msg)
