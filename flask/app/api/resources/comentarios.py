"""
Arquivo para definição de métodos relacionados a comentários.

:created by:    Mateus Herrera
:created at:    2025-08-01

:updated by:    Mateus Herrera
:updated at:    2025-08-03
"""

from flask              import request
from flask_restful      import Resource
from flask_jwt_extended import jwt_required

from sqlalchemy import asc, desc

from app.models.comentario      import Comentario
from app.extensions             import db
from app.services.classifier    import (
    classify_comment,
    classify_batch,
    CATEGORIES
)


class Comentarios(Resource):
    """ Classe para manipulação de comentários. """

    # ini: constants

    # Processamento paralelo para lotes grandes
    MAX_WORKERS             = 10
    BATCH_SIZE_THRESHOLD    = 5

    # end: constants

    # ini: methods

    @jwt_required()
    def get(self):
        """ Retorna comentários com filtros opcionais. """

        try:
            # Request Params
            categoria   = request.args.get('categoria')
            tag         = request.args.get('tag')
            ordem       = request.args.get('ordem').lower() if request.args.get('ordem') else None

            query = Comentario.query

            if categoria in CATEGORIES:
                query = query.filter(Comentario.categoria == categoria)

            if tag:
                query = query.filter(Comentario.tags.contains([tag]))

            if ordem in ['asc', 'desc']:
                comentarios = query.order_by(
                    asc(Comentario.confianca) if ordem == 'asc' else desc(Comentario.confianca)
                ).all()
            else:
                comentarios = query.order_by(Comentario.created_at.desc()).all()

            return [
                {
                    'id': c.id,
                    'texto': c.texto,
                    'categoria': c.categoria,
                    'tags_funcionalidades': c.tags,
                    'confianca': round(c.confianca, 2),
                    'created_at': c.created_at.isoformat(),
                    'updated_at': c.updated_at.isoformat()
                }
                for c in comentarios
            ], 200

        except:
            # 500 - Internal Server Error
            from traceback import format_exc
            return { 'details': 'Erro ao buscar comentários.', 'trace': format_exc() }, 500

    @jwt_required()
    def post(self):
        """ Cria um novo comentário. """

        data = request.get_json(force=True)

        try:
            # -- Em lote --
            if isinstance(data, list):
                items_data = {}
                textos = list()

                for item in data:
                    uuid_comentario = item.get('id', '')
                    texto = item.get('texto', '').strip()

                    if not uuid_comentario or not texto:
                        # 400 - Bad Request
                        return { 'details': 'Campo id e texto são obrigatórios em todos os itens.' }, 400

                    items_data[texto] = uuid_comentario
                    textos.append(texto)

                # Definindo quantidade de workers para processamento em lote
                num_comments = len(textos)
                if num_comments >= self.BATCH_SIZE_THRESHOLD:
                    workers = min(self.MAX_WORKERS, num_comments)
                else:
                    workers = 1

                # Classifica em lote
                results = classify_batch(textos, max_workers=workers)

                # Salvando classificações no banco de dados
                response_list = list()
                for res in results:
                    uuid_comentario = items_data[res['texto']]
                    comentario = Comentario(
                        id=uuid_comentario,
                        texto=res['texto'],
                        categoria=res['categoria'],
                        tags=res.get('tags_funcionalidades', []),
                        confianca=res['confianca']
                    )

                    db.session.add(comentario)
                    response_list.append({
                        'id'                    : comentario.id,
                        'texto'                 : comentario.texto,
                        'categoria'             : comentario.categoria,
                        'tags_funcionalidades'  : comentario.tags,
                        'confianca'             : comentario.confianca
                    })

                # 201 - Created
                db.session.commit()
                return response_list, 201

            # -- Comentário único --
            uuid_comentario = data.get('id', '')
            texto = data.get('texto', '').strip()
            if not uuid_comentario or not texto:
                # 400 - Bad Request
                return { 'details': 'Campo id e texto são obrigatórios.' }, 400

            categoria, tags, confianca = classify_comment(texto)
            comentario = Comentario(
                id=uuid_comentario,
                texto=texto,
                categoria=categoria,
                tags=tags,
                confianca=confianca
            )
            db.session.add(comentario)

            # 201 - Created
            db.session.commit()
            return {
                'id'                    : comentario.id,
                'texto'                 : comentario.texto,
                'categoria'             : comentario.categoria,
                'tags_funcionalidades'  : comentario.tags,
                'confianca'             : comentario.confianca
            }, 201

        except Exception as err:
            # 500 - Internal Server Error
            return { 'details': 'Erro ao processar o comentário.' }, 500

    # end: methods
