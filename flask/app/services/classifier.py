"""
Arquivo com funções para classificar textos.

:created by:    Mateus Herrera
:created at:    2025-08-01

:updated by:    Mateus Herrera
:updated at:    2025-08-02
"""

from openai import OpenAI

from json               import loads
from typing             import List, Tuple
from concurrent.futures import ThreadPoolExecutor, as_completed

from app.config import Config


# Criar cliente OpenAI
openai = OpenAI(api_key=Config.OPENAI_API_KEY)

LLM_MODEL = Config.LLM_MODEL

CATEGORIES = [
    'ELOGIO',
    'CRÍTICA',
    'SUGESTÃO',
    'DÚVIDA',
    'SPAM',
]

SYSTEM_PROMPT = (
    "Você é um classificador de comentários que deve gerar tags de backlog para desenvolvimento de software. "
    "Ao receber um texto de comentário, analise-o e retorne apenas um OBJETO JSON VÁLIDO com estes campos:\n"
    "\n"
    "1. \"categoria\": uma das categorias exatas: [\"" + "\", \"".join(CATEGORIES) + "\"].\n"
    "\n"
    "2. \"tags_funcionalidades\": lista de tags no formato EXATO 'escopo_descricao' (duas palavras separadas por underscore).\n"
    "   - ESCOPOS permitidos: feat (nova funcionalidade), fix (correção), perf (performance), ui (interface), doc (documentação), test (testes), sec (segurança), api (API).\n"
    "   - DESCRIÇÃO: uma palavra que identifica o que está sendo mencionado.\n"
    "   - Exemplos válidos: feat_notificacao, fix_login, perf_carregamento, ui_layout, api_autenticacao.\n"
    "   - Se não identificar funcionalidades específicas, retorne lista vazia [].\n"
    "\n"
    "3. \"confianca\": número entre 0.0 e 1.0 refletindo sua certeza na classificação.\n"
    "\n"
    "INSTRUÇÕES IMPORTANTES:\n"
    "- Analise o comentário buscando funcionalidades, problemas ou melhorias mencionadas\n"
    "- Para cada item identificado, gere uma tag no formato escopo_descricao\n"
    "- Use escopos consistentes para facilitar agrupamento no backlog\n"
    "- Seja preciso: se o usuário fala sobre 'botão não funciona', use fix_botao\n"
    "- Se menciona 'nova funcionalidade X', use feat_x\n"
    "- Retorne APENAS o JSON, sem explicações adicionais\n"
    "Aqui vão alguns exemplos para calibrar:\n"
    "User: Texto: “O layout é lindo mas às vezes trava.”\n"
    "Bot: {\"categoria\":\"CRÍTICA\",\"tags_funcionalidades\":[\"ui_estetica\",\"performance_travamento\"],\"confianca\":0.82}\n"
    "User: Texto: “Parabéns pelo suporte rápido!”\n"
    "Bot: {\"categoria\":\"ELOGIO\",\"tags_funcionalidades\":[\"suporte_eficiente\"],\"confianca\":0.95}\n"
    "---\n"
    "Agora, classifique este comentário **sem** repetir esses exemplos:\n"
)


def classify_comment(text: str, model: str = LLM_MODEL) -> Tuple[str, List[str], float]:
    """
    Classifica um comentário de texto em uma das categorias predefinidas e gera tags de backlog.

    :param text:    Texto do comentário a ser classificado.
    :param model:   Modelo da OpenAI a ser utilizado para classificação.
    :return:        Uma tupla contendo (categoria, tags_funcionalidades, confianca).
    """

    messages = [
        { 'role': 'system', 'content': SYSTEM_PROMPT },
        { 'role': 'user',   'content': f'Texto: {text}' }
    ]

    response = openai.chat.completions.create(
        model=model,
        messages=messages,
        temperature=0.1,  # Reduzida para maior consistência
        max_tokens=200,   # Aumentado para acomodar JSON mais estruturado
        response_format={"type": "json_object"},  # Força resposta em JSON
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
