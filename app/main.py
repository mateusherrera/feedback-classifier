"""
Arquivo principal da aplicação Flask.

:created by:    Mateus Herrera
:created at:    2025-08-01

:updated by:    Mateus Herrera
:updated at:    2025-08-01
"""

from app.config import Config
from app        import create_app


app = create_app()

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=Config.ENV == 'dev')
