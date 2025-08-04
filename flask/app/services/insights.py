"""
Serviço para geração de insights a partir dos três últimos resumos semanais.

:created by:    Mateus Herrera
:created at:    2025-08-04

:updated by:    Mateus Herrera
:updated at:    2025-08-04
"""

from openai     import OpenAI

from app.config         import Config
from app.models.resumo  import ResumoSemanal


# Cliente OpenAI
openai = OpenAI(api_key=Config.OPENAI_API_KEY)
LLM_MODEL = Config.LLM_MODEL


def gerar_insight(pergunta: str, num_resumos: int = 3, max_palavras: int = 150):
    """
    Gera um insight a partir dos últimos resumos semanais.

    :param pergunta:        Pergunta a ser respondida com base nos resumos.
    :param num_resumos:     Número de resumos semanais a serem considerados (padrão: 3).
    :param max_palavras:    Limite máximo de palavras na resposta (padrão: 150).
    :return:                Tupla contendo a resposta gerada e as semanas usadas como fonte.
    """

    # Buscar os resumos mais recentes
    resumos = (ResumoSemanal.query.order_by(ResumoSemanal.created_at.desc()).limit(num_resumos).all())

    # Montar contexto e extrair identificador de semana
    contextos = list()
    semanas = list()
    for r in resumos:
        year, week, _ = r.created_at.isocalendar()
        semana_str = f"{year}-W{week:02d}"
        semanas.append(semana_str)
        contextos.append(f"Semana {semana_str}:\n{r.texto}")

    # Concatenar contextos
    contexto = "\n\n".join(contextos)
    # Chamada à LLM usando contextos como mensagens de system
    system_message = (
        "Você é um assistente que responde perguntas sobre feedbacks usando resumos semanais. "
        "Considere os seguintes resumos como contexto:\n\n"
        f"{contexto}"
    )

    prompt = (
        f"Pergunta: {pergunta}\n\n"
        f"Por favor, responda em até {max_palavras} palavras e, ao final, liste as semanas usadas como fonte."
    )

    resp = openai.chat.completions.create(
        model=LLM_MODEL,
        messages=[
            {"role": "system", "content": system_message},
            {"role": "user",   "content": prompt},
        ],
    )

    # Extrair resposta e formatar
    texto = resp.choices[0].message.content.strip()
    return texto, semanas
