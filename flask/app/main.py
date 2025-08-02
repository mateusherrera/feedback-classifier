"""
Arquivo principal da aplicação Flask.

:created by:    Mateus Herrera
:created at:    2025-08-01

:updated by:    Mateus Herrera
:updated at:    2025-08-01
"""

from flask          import Flask
from flask_migrate  import Migrate

from app.config        import Config
from app.api.routes    import blueprint
from app.extensions    import (
    db,
    jwt,
)


def create_app(config_class=Config) -> Flask:
    """
    Função para criar e configurar a aplicação Flask.

    :param config_class: Classe de configuração, acesso a variáveis de ambiente.
    """

    app = Flask(__name__)
    app.config.from_object(config_class)

    # Inicializa as extensões
    db.init_app(app)
    Migrate(app, db)

    jwt.init_app(app)

    # Registra o blueprint
    app.register_blueprint(blueprint)
    return app


app = create_app()

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=Config.FLASK_ENV != 'production')
