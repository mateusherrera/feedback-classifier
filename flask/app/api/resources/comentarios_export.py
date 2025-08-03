"""
Arquivo para definir método de expostação de comentários classificados em tipo .csv.

:created by:    Mateus Herrera
:created at:    2025-08-03

:updated by:    Mateus Herrera
:updated at:    2025-08-03
"""

from flask_restful      import Resource
from flask_jwt_extended import jwt_required
from flask              import Response, request

import csv
from io         import StringIO
from sqlalchemy import asc, desc

from app.models.comentario      import Comentario
from app.services.classifier    import CATEGORIES


class ComentariosExport(Resource):
    """ Classe para exportação de comentários classificados. """

    @jwt_required()
    def get(self):
        """ Exporta todos os comentários em formato CSV. """

        try:
            # Resquest Params
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

            # Cabeçalhos do CSV
            header = ['id', 'texto', 'categoria', 'tags', 'confianca', 'created_at', 'updated_at']

            # Cria arquivo CSV em memória
            csv_file = StringIO()
            writer = csv.writer(csv_file)
            writer.writerow(header)

            for c in comentarios:
                writer.writerow([
                    c.id,
                    c.texto,
                    c.categoria,
                    ','.join(c.tags or []),
                    round(c.confianca, 2),
                    c.created_at.isoformat(),
                    c.updated_at.isoformat()
                ])

            # Envia como arquivo para download
            return Response(
                csv_file.getvalue(),
                mimetype='text/csv',
                headers={
                    "Content-Disposition": "attachment; filename=comentarios_export.csv"
                }
            )

        except:
            # 500 - Internal Server Error
            return { 'details': 'Erro ao buscar comentários.' }, 500
