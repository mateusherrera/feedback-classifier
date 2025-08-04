"""
Arquivo para o serviço de resumo semanal.

:created by:    Mateus Herrera
:created at:    2025-08-03

:updated by:    Mateus Herrera
:updated at:    2025-08-03
"""

from openai import OpenAI

from app.models.comentario  import Comentario
from datetime               import datetime, timedelta

from app.config import Config


# Criar cliente OpenAI
openai = OpenAI(api_key=Config.OPENAI_API_KEY)

LLM_MODEL = Config.LLM_MODEL


def gerar_resumo_semana() -> str:
    agora = datetime.now()
    comeco_semana = agora - timedelta(days=7)

    comentarios = Comentario.query.filter(
        Comentario.created_at >= comeco_semana
    ).all()

    # Prepare um contexto básico (você pode enriquecer com estatísticas)
    textos = "\n".join(f"- {c.texto}" for c in comentarios)
    prompt = (
        "Você é um assistente que gera um resumo semanal destacando as principais tendências "
        "nos comentários listados abaixo:\n\n"
        f"{textos}\n\n"
        "Gere um texto conciso de até 200 palavras, apontando categorias em alta, críticas recorrentes e sugestões relevantes."
        "Seria interessante pontuar explicitamente pontos de melhorias em forma de novas features ou melhorias de UX.\n"
        "Formato de e-mail, assine como 'Feedbacks por IA', inicie com 'Olá'.\n\n"
    )

    resp = openai.chat.completions.create(
        model=LLM_MODEL,
        messages=[
            {"role": "system", "content": "Você é um gerador de relatórios de feedback."},
            {"role": "user", "content": prompt},
        ],
    )

    return resp.choices[0].message.content.strip()
