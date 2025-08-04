"""
Testes para a função de EVALs

:created by:    Mateus Herrera
:created at:    2025-08-04

:updated by:    Mateus Herrera
:updated at:    2025-08-04
"""

import pytest
import time
from app.services.classifier import classify_batch


def test_classify_batch_all_texts(monkeypatch):
    """ Testa se todos os textos são processados corretamente e se as categorias correspondem. """

    # Testa se todos os textos são processados
    texts = [f'text_{i}' for i in range(5)]
    labels = [f'label_{i}' for i in range(5)]

    # Mock classify_comment retornando índice do texto
    def mock_classify(text, model=None):
        idx = int(text.split('_')[1])
        return labels[idx], [], 1.0

    monkeypatch.setattr('app.services.classifier.classify_comment', mock_classify)

    results = classify_batch(texts, max_workers=1)

    # Verifica processamento completo e correspondência de categoria
    assert len(results) == len(texts)
    for i, r in enumerate(results):
        assert r['texto'] == texts[i]
        assert r['categoria'] == labels[i]
