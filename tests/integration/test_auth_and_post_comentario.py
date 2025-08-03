"""
Arquivos de teste para autenticação e postagem de comentários

:created by:    Mateus Herrera
:created at:    2025-08-02

:updated by:    Mateus Herrera
:updated at:    2025-08-02
"""

from app.extensions import db


def test_register_login_and_post_comment(client, app):
    """
    Função para teste de registro, login e postagem de comentário

    :param client:  Cliente de teste do Flask
    :param app:     Aplicação Flask
    """

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

    # Mock classify_comment para não chamar OpenAI real
    from unittest.mock import patch

    with patch('app.api.resources.comentarios.classify_comment') as mock_classify:
        mock_classify.return_value = ('ELOGIO', ['app_usabilidade'], 0.9)

        # Comentário
        response = client.post('/api/comentarios', json={
            'id': '1234',
            'texto': 'Gostei muito da interface!'
        }, headers={'Authorization': f'Bearer {access_token}'})

        assert response.status_code == 201
        json_data = response.get_json()
        assert json_data['categoria'] == 'ELOGIO'
        assert 'app_usabilidade' in json_data['tags_funcionalidades']
