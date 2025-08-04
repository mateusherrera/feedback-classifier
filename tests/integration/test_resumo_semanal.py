"""
Arquivo para teste de task de envio de resumo semanal.

:created by:    Mateus Herrera
:created at:    2025-08-03

:created by:    Mateus Herrera
:created at:    2025-08-03
"""

import pytest
import app.tasks as tasks_module

from datetime import datetime
from freezegun import freeze_time

from app.models.comentario  import Comentario
from app.models.resumo      import ResumoSemanal
from app.tasks              import enviar_resumo_semanal
from app.extensions         import db, mail as mail_extension


@freeze_time("2025-08-03")
def test_enviar_resumo_semanal(monkeypatch, app):
    """ Teste para a task de envio de resumo semanal. """

    # Cria um comentário de teste
    with app.app_context():
        c = Comentario(
            id="t1",
            texto="Teste de elogio",
            categoria="ELOGIO",
            tags=["tag1"],
            confianca=0.9,
            created_at=datetime.now()
        )
        db.session.add(c)
        db.session.commit()

    # Mocando o OpenAI para sempre retornar "Resumo fake"
    class FakeChoice:
        message = type("M", (), {"content": "Resumo fake"})
    class FakeResp:
        choices = [FakeChoice()]

    monkeypatch.setattr(
        "app.services.summary.openai.chat.completions.create",
        lambda **kw: FakeResp()
    )

    # Captura os envios de e-mail
    sent = []
    monkeypatch.setattr(mail_extension, "send", lambda msg: sent.append(msg))

    # Mocando create_app
    monkeypatch.setattr(tasks_module, "create_app", lambda: app)

    # Executa a task
    enviar_resumo_semanal()

    # Verifica que salvou no banco
    with app.app_context():
        resumo = ResumoSemanal.query.order_by(ResumoSemanal.created_at.desc()).first()
        assert resumo is not None
        assert resumo.texto == "Resumo fake"

    # Verifica que tentou enviar exatamente 1 e-mail
    assert len(sent) == 1
    assert "Resumo Semanal" in sent[0].subject
