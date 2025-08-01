"""
Arquivo de roteamento da API.

:created by:    Mateus Herrera
:created at:    2025-08-01

:updated by:    Mateus Herrera
:updated at:    2025-08-01
"""

from flask_restful  import Api
from flask          import Blueprint

from .resources.comentarios import ComentariosList


blueprint   = Blueprint('api', __name__, url_prefix='/api')
api         = Api(blueprint)

# Registro de endpoints
api.add_resource(ComentariosList, '/comentarios')
