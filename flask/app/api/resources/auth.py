"""
Arquivo com métodos de autenticação (JWT).

:created by:    Mateus Herrera
:created at:    2025-08-02

:updated by:    Mateus Herrera
:updated at:    2025-08-02
"""

from flask              import request
from flask_restful      import Resource
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    jwt_required,
    get_jwt_identity
)

from app.extensions     import db
from app.models.user    import User


class Register(Resource):
    """ Classe para registro de usuários. """

    def post(self):
        """ Criar novo usuário. """

        try:
            data        = request.get_json(force=True)
            username    = data.get('username', '').strip()
            password    = data.get('password', '')

            if not username or not password:
                # 400 - Bad Request
                return { 'details': 'username e password são obrigatórios.' }, 400

            if User.query.filter_by(username=username).first():
                # 400 - Bad Request
                return { 'details': 'Usuário já existe.' }, 400

            user = User(username=username)
            user.set_password(password)

            db.session.add(user)
            db.session.commit()

            # 201 - Created
            return { 'id': user.id, 'username': user.username }, 201

        except:
            # 500 - Internal Server Error
            return { 'details': 'Erro ao criar usuário' }, 500


class Login(Resource):
    """ Classe para login de usuários. """

    def post(self):
        """ Login, retorna tokens JWT (access e refresh). """

        try:
            data        = request.get_json(force=True)
            username    = data.get('username', '').strip()
            password    = data.get('password', '')

            user = User.query.filter_by(username=username).first()
            if not user or not user.check_password(password):
                # 401 - Unauthorized
                return { 'details': 'Credenciais inválidas.' }, 401

            access_token    = create_access_token(identity=user.id)
            refresh_token   = create_refresh_token(identity=user.id)

            return {
                'access'    : access_token,
                'refresh'   : refresh_token,
            }, 200
        
        except:
            # 500 - Internal Server Error
            return { 'details': 'Erro ao realizar login' }


class Refresh(Resource):
    """ Classe para gerar novo access token. """

    @jwt_required(refresh=True)
    def post(self):
        """ Gera um novo access token. """

        try:
            current_user = get_jwt_identity()
            new_access_token = create_access_token(identity=current_user)

            # 200 - Success
            return { 'access': new_access_token }, 200

        except:
            # 500 - Internal Server Error
            return { 'details': 'Erro ao atualizar access token' }
