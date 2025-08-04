"""
Arquivo para teste do endpoint de geração de insights a partir dos últimos resumos semanais.

:created by:    Mateus Herrera
:created at:    2025-08-04

:updated by:    Mateus Herrera
:updated at:    2025-08-04
"""

import pytest
from datetime import datetime, timedelta
from freezegun import freeze_time

from app.extensions import db
from app.models.resumo import ResumoSemanal


@pytest.fixture(autouse=True)
def insert_resumos(app):
    """ Insere três resumos semanais no banco antes de cada teste. """

    with app.app_context():
        # Remove quaisquer registros anteriores
        ResumoSemanal.query.delete()
        db.session.commit()

        # Data congelada em 2025-08-04 para consistência nos testes
        now = datetime.now()
        semanas = []
        for i in range(3):
            dt = now - timedelta(weeks=i)
            resumo = ResumoSemanal(
                texto=f"Resumo semana {i}",
                created_at=dt
            )
            db.session.add(resumo)
            db.session.commit()
            iso = dt.isocalendar()
            semanas.append(f"{iso[0]}-W{iso[1]:02d}")

        # Disponibiliza as semanas esperadas
        return semanas


@freeze_time("2025-08-04")
def test_insights_perguntar(monkeypatch, client, app, insert_resumos):
    """ Testa o endpoint de geração de insights a partir dos últimos resumos semanais (fakes). """

    resp_reg = client.post('/api/auth/register', json={
        'username': 'usuario_insight',
        'password': 'senha123'
    })
    assert resp_reg.status_code == 201

    resp_login = client.post('/api/auth/login', json={
        'username': 'usuario_insight',
        'password': 'senha123'
    })
    assert resp_login.status_code == 200
    access_token = resp_login.get_json()['access']

    fake_text = "Aqui está o insight gerado. [2025-W31, 2025-W30, 2025-W29]"
    class FakeChoice:
        message = type("M", (), {"content": fake_text})
    class FakeResp:
        choices = [FakeChoice()]

    monkeypatch.setattr(
        'app.services.insights.openai.chat.completions.create',
        lambda **kw: FakeResp()
    )

    response = client.post(
        '/api/insights/perguntar',
        json={'pergunta': 'Quais são as tendências recentes?'},
        headers={'Authorization': f'Bearer {access_token}'}
    )
    assert response.status_code == 200

    data = response.get_json()
    assert 'resposta' in data
    assert 'semanas' in data

    assert data['resposta'] == fake_text

    expected_semanas = insert_resumos
    assert isinstance(data['semanas'], list)
    assert set(data['semanas']) == set(expected_semanas)
