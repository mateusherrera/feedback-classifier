"""
Testes para a listagem e exportação de comentários

:created by:    Mateus Herrera
:created at:    2025-08-03

:updated by:    Mateus Herrera
:updated at:    2025-08-03
"""

from app.extensions         import db
from app.models.comentario  import Comentario
from datetime               import datetime, timedelta


def test_register_login_and_post_comment(client, app):
    """
    Função para teste de registro, login e listagem de comentários com filtros e ordenação.
    """

    agora       = datetime.now()
    ontem       = agora - timedelta(days=1)
    anteontem   = agora - timedelta(days=2)

    # Fixando dados para prever o resultado do relatório
    with app.app_context():
        comentarios = [
            Comentario(
                id='c1',
                texto='Muito bom!',
                categoria='ELOGIO',
                tags=['ui_legal'],
                confianca=0.95,
                created_at=ontem
            ),
            Comentario(
                id='c2',
                texto='Ruim demais!',
                categoria='CRÍTICA',
                tags=['performance_lenta'],
                confianca=0.55,
                created_at=anteontem
            ),
            Comentario(
                id='c3',
                texto='Como usar isso?',
                categoria='DÚVIDA',
                tags=['ux_duvida'],
                confianca=0.85,
                created_at=agora
            ),
            Comentario(
                id='c4',
                texto='Achei confuso',
                categoria='DÚVIDA',
                tags=['ux_duvida'],
                confianca=0.40,
                created_at=agora - timedelta(hours=3)
            ),
            Comentario(
                id='c5',
                texto='Gostei da interface!',
                categoria='ELOGIO',
                tags=['ui_legal', 'layout_moderno'],
                confianca=0.88,
                created_at=ontem
            ),
        ]
        db.session.bulk_save_objects(comentarios)
        db.session.commit()

    # Registro
    response = client.post('/api/auth/register', json={
        'username': 'usuario_teste',
        'password': 'senha123'
    })
    assert response.status_code == 201

    # Login
    response = client.post('/api/auth/login', json={
        'username': 'usuario_teste',
        'password': 'senha123'
    })
    assert response.status_code == 200
    access_token = response.get_json()['access']

    # Listar com filtro categoria e tag, ordenado por confiança ascendente
    response = client.get('/api/comentarios?categoria=DÚVIDA&tag=ux_duvida&ordem=asc', headers={
        'Authorization': f'Bearer {access_token}'
    })
    assert response.status_code == 200
    comentarios_filtrados = response.get_json()

    assert isinstance(comentarios_filtrados, list)
    assert len(comentarios_filtrados) == 2

    confiancas = [c['confianca'] for c in comentarios_filtrados]
    assert confiancas == sorted(confiancas), "Confianças não estão em ordem ascendente"

    # Validações adicionais
    for c in comentarios_filtrados:
        assert c['categoria'] == 'DÚVIDA'
        assert 'ux_duvida' in c['tags_funcionalidades']
