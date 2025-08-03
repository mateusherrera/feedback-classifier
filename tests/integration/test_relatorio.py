"""
Arquivos de teste para autenticação e postagem de comentários

:created by:    Mateus Herrera
:created at:    2025-08-03

:updated by:    Mateus Herrera
:updated at:    2025-08-03
"""

from app.extensions         import db
from app.models.comentario  import Comentario
from datetime               import datetime, timedelta


def test_relatorio_semanal(client, app):
    """ Testa geração de relatório semanal com base em dados inseridos """

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
        ]
        db.session.bulk_save_objects(comentarios)
        db.session.commit()

    # Requisição
    response = client.get('/api/relatorio/semana')
    assert response.status_code == 200

    data = response.get_json()
    assert 'relatorios' in data
    relatorios = data['relatorios']

    # Checar estrutura esperada
    assert 'distribuicao_categorias' in relatorios
    assert 'evolucao_temporal' in relatorios
    assert 'top_tags_48h' in relatorios
    assert 'confianca_media_por_categoria' in relatorios
    assert 'comentarios_por_hora' in relatorios

    # Validação de conteúdo básico
    dist = relatorios['distribuicao_categorias']
    assert dist['ELOGIO'] > 0
    assert dist['CRÍTICA'] > 0
    assert dist['DÚVIDA'] > 0

    confianca = relatorios['confianca_media_por_categoria']
    assert round(confianca['ELOGIO'], 2) == 0.95
    assert round(confianca['CRÍTICA'], 2) == 0.55
