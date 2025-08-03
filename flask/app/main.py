"""
Arquivo principal da aplicação Flask.

:created by:    Mateus Herrera
:created at:    2025-08-01

:updated by:    Mateus Herrera
:updated at:    2025-08-02
"""

from datetime import timedelta

from flask          import Flask
from flask_migrate  import Migrate

from app.config        import Config
from app.api.routes    import blueprint
from app.extensions    import (
    db,
    jwt,
    cache,
)


def create_app(config_class=Config) -> Flask:
    """
    Função para criar e configurar a aplicação Flask.

    :param config_class: Classe de configuração, acesso a variáveis de ambiente.
    """

    app = Flask(__name__)
    app.config.from_object(config_class)

    # Secret keys
    app.config['SECRET_KEY']        = Config.SECRET_KEY

    # Configuração do JWT
    app.config['JWT_SECRET_KEY']            = Config.JWT_SECRET_KEY
    app.config['JWT_ACCESS_TOKEN_EXPIRES']  = timedelta(minutes=1)
    app.config['JWT_REFRESH_TOKEN_EXPIRES'] = timedelta(days=1)

    # Inicializa as extensões
    db.init_app(app)
    if Config.PROJECT_SCHEMA:
        Migrate(app, db, version_table_schema=Config.PROJECT_SCHEMA)
    else:
        Migrate(app, db)

    jwt.init_app(app)
    cache.init_app(app)

    # Registra o blueprint
    app.register_blueprint(blueprint)
    return app


app = create_app()

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=Config.FLASK_ENV != 'production')
