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
    "Você é um classificador especializado de comentários para desenvolvimento de software. "
    "Sua tarefa é analisar comentários e extrair informações estruturadas para geração de backlog.\n"
    "\n"
    "FORMATO DE RESPOSTA:\n"
    "Retorne APENAS um objeto JSON válido com exatamente estes 3 campos:\n"
    "\n"
    "1. \"categoria\": Classifique o sentimento/intenção principal do comentário.\n"
    "   CATEGORIAS DISPONÍVEIS: [\"" + "\", \"".join(CATEGORIES) + "\"]\n"
    "   - ELOGIO: Feedback positivo, reconhecimento, satisfação\n"
    "   - CRÍTICA: Problemas, falhas, insatisfação, reclamações\n"
    "   - SUGESTÃO: Propostas de melhoria, ideias, recomendações\n"
    "   - DÚVIDA: Perguntas, pedidos de esclarecimento, confusão\n"
    "   - SPAM: Conteúdo irrelevante, propaganda, texto sem sentido\n"
    "\n"
    "2. \"tags_funcionalidades\": Identifique componentes/funcionalidades mencionadas.\n"
    "   FORMATO OBRIGATÓRIO: 'escopo_descricao' (duas palavras separadas por underscore)\n"
    "   \n"
    "   ESCOPOS PERMITIDOS:\n"
    "   - feat: Nova funcionalidade ou recurso\n"
    "   - fix: Correção de bug ou problema\n"
    "   - perf: Performance, velocidade, otimização\n"
    "   - ui: Interface de usuário, design, layout\n"
    "   - doc: Documentação, ajuda, tutorials\n"
    "   - test: Testes, qualidade, validação\n"
    "   - sec: Segurança, privacidade, autenticação\n"
    "   - api: APIs, integração, conectividade\n"
    "   \n"
    "   EXEMPLOS VÁLIDOS: feat_notificacao, fix_login, perf_carregamento, ui_layout, api_autenticacao\n"
    "   \n"
    "   REGRAS:\n"
    "   - Se não identificar funcionalidades específicas, retorne lista vazia []\n"
    "   - Seja específico: 'botão não funciona' → fix_botao\n"
    "   - Para múltiplos problemas, crie múltiplas tags\n"
    "   - Use descrições concisas mas claras\n"
    "\n"
    "3. \"confianca\": AVALIAÇÃO DE CONFIABILIDADE DA CLASSIFICAÇÃO\n"
    "   Valor entre 0.0 e 1.0 baseado na clareza e certeza da análise.\n"
    "   \n"
    "   CRITÉRIOS PARA CONFIANÇA:\n"
    "   - 0.9-1.0: Texto muito claro, categoria óbvia, funcionalidades bem definidas\n"
    "   - 0.7-0.9: Texto claro, pequena margem de interpretação\n"
    "   - 0.5-0.7: Texto ambíguo, mas categoria identificável\n"
    "   - 0.3-0.5: Texto confuso, classificação baseada em poucas pistas\n"
    "   - 0.0-0.3: Texto muito ambíguo ou incompreensível\n"
    "\n"
    "EXEMPLOS DE CALIBRAÇÃO:\n"
    "\n"
    "User: Texto: \"O layout é lindo mas às vezes trava.\"\n"
    "Bot: {\"categoria\":\"CRÍTICA\",\"tags_funcionalidades\":[\"ui_estetica\",\"perf_travamento\"],\"confianca\":0.85}\n"
    "\n"
    "User: Texto: \"Parabéns pelo suporte rápido!\"\n"
    "Bot: {\"categoria\":\"ELOGIO\",\"tags_funcionalidades\":[\"feat_suporte\"],\"confianca\":0.95}\n"
    "\n"
    "User: Texto: \"Como faço login? Não entendi.\"\n"
    "Bot: {\"categoria\":\"DÚVIDA\",\"tags_funcionalidades\":[\"fix_login\"],\"confianca\":0.90}\n"
    "\n"
    "User: Texto: \"Seria legal ter notificações push.\"\n"
    "Bot: {\"categoria\":\"SUGESTÃO\",\"tags_funcionalidades\":[\"feat_notificacao\"],\"confianca\":0.92}\n"
    "\n"
    "IMPORTANTE: Analise cuidadosamente cada comentário e retorne APENAS o JSON, sem explicações adicionais.\n"
    "\n"
    "---\n"
    "Classifique este comentário:\n"
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