"""
Arquivo de roteamento da API.

:created by:    Mateus Herrera
:created at:    2025-08-01

:updated by:    Mateus Herrera
:updated at:    2025-08-02
"""

from flask_restful  import Api
from flask          import Blueprint

from app.api.resources.comentarios          import Comentarios
from app.api.resources.insights             import InsightPerguntar
from app.api.resources.relatorios           import RelatorioSemanal
from app.api.resources.comentarios_export   import ComentariosExport
from app.api.resources.auth                 import (
    Register,
    Refresh,
    Login,
)


blueprint   = Blueprint('api', __name__, url_prefix='/api')
api         = Api(blueprint)

# Registro de endpoints
# Auth
api.add_resource( Register              , '/auth/register'          )
api.add_resource( Refresh               , '/auth/refresh'           )
api.add_resource( Login                 , '/auth/login'             )

# Classificador de Comentários
api.add_resource( Comentarios           , '/comentarios'            )
api.add_resource( ComentariosExport     , '/comentarios/export'     )

# Relatórios
api.add_resource( RelatorioSemanal      , '/relatorio/semana'       )

# Insights
api.add_resource( InsightPerguntar      , '/insights/perguntar'     )
