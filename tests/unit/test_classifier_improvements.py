"""
Test cases for improved classifier prompt and confidence handling.
"""

from app.services.classifier import classify_comment


def test_improved_prompt_structure(monkeypatch):
    """Test that the improved prompt provides more structured responses with better confidence evaluation."""
    
    # Mock OpenAI response with improved structured output
    def mock_openai_response(*args, **kwargs):
        # Extract the actual prompt from the call to verify structure
        system_content = kwargs.get('messages', [{}])[0].get('content', '')
        
        # Check that the prompt contains the new structured sections
        assert "FORMATO DE RESPOSTA:" in system_content
        assert "AVALIAÇÃO DE CONFIABILIDADE" in system_content
        assert "CRITÉRIOS PARA CONFIANÇA:" in system_content
        assert "EXEMPLOS DE CALIBRAÇÃO:" in system_content
        
        class MockChoice:
            def __init__(self):
                self.message = type('obj', (object,), {
                    'content': '{"categoria":"ELOGIO","tags_funcionalidades":["ui_design"],"confianca":0.90}'
                })
        return type('obj', (object,), {'choices': [MockChoice()]})

    monkeypatch.setattr('app.services.classifier.openai.chat.completions.create', mock_openai_response)

    categoria, tags, confianca = classify_comment('Interface muito bonita!')
    assert categoria == 'ELOGIO'
    assert tags == ['ui_design']
    assert 0 <= confianca <= 1


def test_confidence_field_separation(monkeypatch):
    """Test that confidence is properly separated and validated in the response."""
    
    def mock_openai_high_confidence(*args, **kwargs):
        class MockChoice:
            def __init__(self):
                self.message = type('obj', (object,), {
                    'content': '{"categoria":"CRÍTICA","tags_funcionalidades":["fix_login"],"confianca":0.95}'
                })
        return type('obj', (object,), {'choices': [MockChoice()]})

    monkeypatch.setattr('app.services.classifier.openai.chat.completions.create', mock_openai_high_confidence)

    categoria, tags, confianca = classify_comment('Login não funciona')
    assert categoria == 'CRÍTICA'
    assert tags == ['fix_login']
    assert confianca == 0.95  # High confidence for clear problem statement


def test_confidence_criteria_coverage(monkeypatch):
    """Test different confidence levels based on text clarity."""
    
    test_cases = [
        # High confidence - very clear text
        ('Excelente aplicativo!', 0.95),
        # Medium confidence - somewhat ambiguous
        ('Está ok, mas poderia ser melhor', 0.65),
        # Lower confidence - unclear text
        ('Não sei...', 0.35)
    ]
    
    def mock_openai_variable_confidence(*args, **kwargs):
        user_text = kwargs.get('messages', [{}])[1].get('content', '')
        
        class MockChoice:
            def __init__(self, confidence):
                self.message = type('obj', (object,), {
                    'content': f'{{"categoria":"ELOGIO","tags_funcionalidades":[],"confianca":{confidence}}}'
                })
        
        # Return different confidence based on text clarity
        if 'Excelente' in user_text:
            return type('obj', (object,), {'choices': [MockChoice(0.95)]})
        elif 'ok' in user_text:
            return type('obj', (object,), {'choices': [MockChoice(0.65)]})
        else:
            return type('obj', (object,), {'choices': [MockChoice(0.35)]})

    monkeypatch.setattr('app.services.classifier.openai.chat.completions.create', mock_openai_variable_confidence)

    for text, expected_confidence in test_cases:
        categoria, tags, confianca = classify_comment(text)
        assert confianca == expected_confidence, f"Expected {expected_confidence} for '{text}', got {confianca}"


def test_category_explanations_in_prompt(monkeypatch):
    """Test that the prompt includes clear explanations for each category."""
    
    def mock_openai_check_categories(*args, **kwargs):
        system_content = kwargs.get('messages', [{}])[0].get('content', '')
        
        # Verify category explanations are present
        assert "ELOGIO: Feedback positivo" in system_content
        assert "CRÍTICA: Problemas, falhas" in system_content
        assert "SUGESTÃO: Propostas de melhoria" in system_content
        assert "DÚVIDA: Perguntas, pedidos" in system_content
        assert "SPAM: Conteúdo irrelevante" in system_content
        
        class MockChoice:
            def __init__(self):
                self.message = type('obj', (object,), {
                    'content': '{"categoria":"DÚVIDA","tags_funcionalidades":["doc_ajuda"],"confianca":0.88}'
                })
        return type('obj', (object,), {'choices': [MockChoice()]})

    monkeypatch.setattr('app.services.classifier.openai.chat.completions.create', mock_openai_check_categories)

    categoria, tags, confianca = classify_comment('Como usar essa função?')
    assert categoria == 'DÚVIDA'


def test_enhanced_examples_in_prompt(monkeypatch):
    """Test that the prompt includes more comprehensive examples."""
    
    def mock_openai_check_examples(*args, **kwargs):
        system_content = kwargs.get('messages', [{}])[0].get('content', '')
        
        # Verify enhanced examples are present
        assert "User: Texto: \"Como faço login? Não entendi.\"" in system_content
        assert "User: Texto: \"Seria legal ter notificações push.\"" in system_content
        assert "perf_travamento" in system_content  # Performance example
        assert "feat_suporte" in system_content     # Feature example
        
        class MockChoice:
            def __init__(self):
                self.message = type('obj', (object,), {
                    'content': '{"categoria":"SUGESTÃO","tags_funcionalidades":["feat_notificacao"],"confianca":0.92}'
                })
        return type('obj', (object,), {'choices': [MockChoice()]})

    monkeypatch.setattr('app.services.classifier.openai.chat.completions.create', mock_openai_check_examples)

    categoria, tags, confianca = classify_comment('Poderiam adicionar dark mode')
    assert categoria == 'SUGESTÃO'
    assert 'feat_' in tags[0] if tags else True  # Should identify as new feature