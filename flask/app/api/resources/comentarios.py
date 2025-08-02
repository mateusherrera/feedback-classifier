"""
Arquivo para definição de métodos relacionados a comentários.

:created by:    Mateus Herrera
:created at:    2025-08-01

:updated by:    Mateus Herrera
:updated at:    2025-08-02
"""

from flask              import request
from flask_restful      import Resource
from flask_jwt_extended import jwt_required

from app.models.comentario      import Comentario
from app.extensions             import db
from app.services.classifier    import (
    classify_comment,
    classify_batch,
)


class Comentarios(Resource):
    """ Classe para manipulação de comentários. """

    # ini: constants

    # Processamento paralelo para lotes grandes
    MAX_WORKERS             = 10
    BATCH_SIZE_THRESHOLD    = 20

    # end: constants

    # ini: methods

    @jwt_required()
    def post(self):
        """ Cria um novo comentário. """

        data = request.get_json(force=True)

        try:
            # -- Em lote --
            if isinstance(data, list):
                textos = list()
                for item in data:
                    texto = item.get('texto', '').strip()

                    if not texto:
                        # 400 - Bad Request
                        return { 'details': 'Campo texto é obrigatório em todos os itens.' }, 400

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
                    comentario = Comentario(
                        texto=res['texto'],
                        categoria=res['categoria'],
                        tags=res.get('tags_funcionalidades', []),
                        confianca=res['confianca']
                    )

                    db.session.add(comentario)
                    response_list.append({
                        'id'                    : comentario.id,
                        'categoria'             : comentario.categoria,
                        'tags_funcionalidades'  : comentario.tags,
                        'confianca'             : comentario.confianca
                    })

                # 201 - Created
                db.session.commit()
                return response_list, 201

            # -- Comentário único --
            texto = data.get('texto', '').strip()
            if not texto:
                # 400 - Bad Request
                return { 'details': 'Campo texto é obrigatório.' }, 400

            categoria, tags, confianca = classify_comment(texto)
            comentario = Comentario(
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
                'categoria'             : comentario.categoria,
                'tags_funcionalidades'  : comentario.tags,
                'confianca'             : comentario.confianca
            }, 201

        except Exception as err:
            # 500 - Internal Server Error
            from traceback import format_exc
            return { 'details': 'Erro ao processar o comentário.', 'traceback': format_exc() }, 500

    # end: methods
