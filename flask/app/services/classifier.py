"""
Arquivo com funções para classificar textos
    Este módulo contém funções para classificar textos usando LLM da OpenAI.

:created by:    Mateus Herrera
:created at:    2025-08-01

:updated by:    Mateus Herrera
:updated at:    2025-08-01
"""

import openai

from json               import loads
from typing             import List, Tuple
from concurrent.futures import ThreadPoolExecutor, as_completed

from app.config import Config


# Definiar OpenAI API KEY
openai.api_key = Config.OPENAI_API_KEY

CATEGORIES = [
    'ELOGIO',
    'CRÍTICA',
    'SUGESTÃO',
    'DÚVIDA',
    'SPAM',
]

SYSTEM_PROMPT = (
    "Desenvolver prompt"
)


def classify_comment(text: str, model: str = 'gpt-3.5-turbo') -> Tuple[str, List[str], float]:
    """
    Essa função classifica um comentário de texto em uma das categorias predefinidas, identifica tags de funcionalidade e  .

    :param text:    Texto do comentário a ser classificado.
    :param model:   Modelo da OpenAI a ser utilizado para classificação.
    :return:        Uma tupla contendo a categoria classificada, as categorias possíveis e a probabilidade da classificação.
    """

    messages = [
        { 'role': 'system', 'content': SYSTEM_PROMPT },
        { 'role': 'user',   'content': f'Texto: {text}' }
    ]

    response = openai.ChatComppetion.create(
        model=model,
        messages=messages,
        temperature=0.0,
        max_tokens=150,
    )

    content = response.choices[0].message.content.strip()
    data = loads(content)
    return data.get("categoria"), data.get("tags_funcionalidades", []), data.get("confianca", 0.0)


def classify_batch(texts: List[str], max_workers: int = 5) -> List[dict]:
    """
    Essa função classifica um lote de comentários de texto em suas respectivas categorias, em paralelo.

    :param texts:        Lista de textos a serem classificados.
    :param max_workers:  Número máximo de threads para processamento paralelo.
    :return:             Lista de dicionários contendo a categoria, tags de funcionalidade e confiança para cada texto.
    """

    results = list()
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = { executor.submit(classify_comment, txt): txt for txt in texts }

        for fut in as_completed(futures):
            texto = futures[fut]

            try:
                categoria, tags_funcionalidades, confianca = fut.result()
                results.append({
                    'texto': texto,
                    'categoria': categoria,
                    'tags_funcionalidades': tags_funcionalidades,
                    'confianca': confianca
                })

            except Exception as err:
                results.append({
                    'texto': texto,
                    'error': err.__str__(),
                })

    return results
