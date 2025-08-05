"""
Arquivo para implementação do endpoint de geração de insights.

:created by:    Mateus Herrera
:created at:    2025-08-04

:updated by:    Mateus Herrera
:updated at:    2025-08-04
"""

from flask              import request
from flask_restful      import Resource
from flask_jwt_extended import jwt_required

from app.services.insights import gerar_insight


class InsightPerguntar(Resource):
    """ Classe para o endpoint de geração de insights a partir de resumos semanais. """

    @jwt_required()
    def post(self):
        """ Endpoint para gerar um insight a partir dos últimos resumos semanais. """

        data = request.get_json(force=True)

        # Extrair pergunta e validar
        pergunta = data.get('pergunta')
        if not pergunta:
            return { 'details': 'O campo "pergunta" é obrigatório.' }, 400

        # Gerar insight
        resposta, semanas = gerar_insight(pergunta)

        if isinstance(semanas, int):
            return { 'details': resposta }, semanas

        return {
            'resposta'  : resposta,
            'semanas'   : semanas
        }, 200
