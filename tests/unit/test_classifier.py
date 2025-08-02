"""
Arquivo com testes unitários para o classificador de comentários.

:created by:    Mateus Herrera
:created at:    2025-08-02

:updated by:    Mateus Herrera
:updated at:    2025-08-02
"""

from app.services.classifier import classify_comment


def test_classify_comment(monkeypatch):
    """  Teste unitário para a função classify_comment. """

    # Mock classify_comment para não chamar OpenAI real
    def mock_openai_response(*args, **kwargs):
        class MockChoice:
            def __init__(self):
                self.message = type('obj', (object,), {
                    'content': '{"categoria":"ELOGIO","tags_funcionalidades":["ui_legal"],"confianca":0.95}'
                })
        return type('obj', (object,), {'choices': [MockChoice()]})

    monkeypatch.setattr('app.services.classifier.openai.chat.completions.create', mock_openai_response)

    categoria, tags, confianca = classify_comment('Muito bom esse app!')
    assert categoria == 'ELOGIO'
    assert tags == ['ui_legal']
    assert 0 <= confianca <= 1
