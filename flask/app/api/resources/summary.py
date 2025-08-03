"""
Arquivo para definição de métodos relacionados ao resumo de cometários classificados semanais.

:created by:    Mateus Herrera
:created at:    2025-08-03

:updated by:    Mateus Herrera
:updated at:    2025-08-03
"""

from flask_restful      import Resource
from flask_jwt_extended import jwt_required

from app.services.summary   import gerar_resumo_semana
from app.extensions         import db

from app.models.resumo import ResumoSemanal


class ResumoSemanalResource(Resource):
    """ Classe para manipulação de resumos semanais. """

    # @jwt_required()
    def get(self):
        """ Gera e retorna o resumo semanal. """

        try:
            resumo = gerar_resumo_semana()

            # Salvar o resumo no banco de dados
            novo_resumo = ResumoSemanal(texto=resumo)
            db.session.add(novo_resumo)
            db.session.commit()

            return {"resumo": resumo}, 200
        
        except Exception as e:
            from traceback import format_exc
            return {
                "error": "Erro ao gerar o resumo semanal.",
                "details": str(e),
                "traceback": format_exc()
            }, 500
