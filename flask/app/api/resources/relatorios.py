"""
Arquivo com implementação de relatórios semanais.

:created by:    Mateus Herrera
:created at:    2025-08-02

:updated by:    Mateus Herrera
:updated at:    2025-08-02
"""

from flask_restful  import Resource
from datetime       import datetime, timedelta
from collections    import Counter, defaultdict

from app.extensions             import cache
from app.models.comentario      import Comentario
from app.services.classifier    import CATEGORIES


class RelatorioSemanal(Resource):
    """ Classe para geração de relatórios semanais de comentários. """

    def get(self):
        """ Endpoint para administrar cache do relatório semanal. """

        # Tenta pegar do cache
        relatorios = cache.get('relatorio_semanal')
        if relatorios is not None:
            return { 'relatorios': relatorios, 'reload': False }, 200

        # Se não tiver cache, recalcula os relatórios
        relatorios = self.gerar_relatorio()
        cache.set('relatorio_semanal', relatorios, timeout=60)
        return { 'relatorios': relatorios, 'reload': True }, 200

    def gerar_relatorio(self):
        """ Gera 5 relatórios semanais com base nos comentários classificados. """

        agora       = datetime.now()
        ha_24_horas = agora - timedelta(hours=24)
        ha_2_dias   = agora - timedelta(days=2)
        ha_7_dias   = agora - timedelta(days=7)

        # Query única para todos os dados
        comentarios = Comentario.query.filter(Comentario.created_at >= ha_7_dias).all()

        # Auxiliares
        categoria_freq = Counter()
        categoria_por_dia = defaultdict(lambda: Counter())
        confianca_categoria = defaultdict(list)
        tags_48h = Counter()
        por_hora = Counter()

        for c in comentarios:
            cat = c.categoria
            categoria_freq[cat] += 1
            dia = c.created_at.date().isoformat()
            hora = c.created_at.replace(minute=0, second=0, microsecond=0).isoformat()

            categoria_por_dia[dia][cat] += 1
            confianca_categoria[cat].append(c.confianca)

            if c.created_at >= ha_2_dias and c.tags:
                tags_48h.update(c.tags)

            if c.created_at >= ha_24_horas:
                por_hora[hora] += 1

        # Distribuição de Categorias
        total = sum(categoria_freq.values())
        distrib_categorias = {
            cat: round((categoria_freq[cat] / total) * 100, 2) if total else 0.0
            for cat in CATEGORIES
        }

        # Evolução Temporal por Categoria (últimos 7 dias)
        evolucao_temporal = []
        dias_ordenados = sorted(categoria_por_dia.keys())
        for dia in dias_ordenados:
            data = { 'data': dia }
            for cat in CATEGORIES:
                data[cat] = categoria_por_dia[dia][cat]
            evolucao_temporal.append(data)

        # Top 10 tags nas últimas 48h
        top_tags_48h = [
            {'tag': tag, 'frequencia': count}
            for tag, count in tags_48h.most_common(10)
        ]

        # Confiabilidade Média por Categoria
        confianca_media = {
            cat: round(sum(vals) / len(vals), 2) if vals else 0.0
            for cat, vals in confianca_categoria.items()
        }

        # Comentários por Hora
        comentarios_por_hora = [
            {'hora': hora, 'quantidade': por_hora[hora]}
            for hora in sorted(por_hora.keys())
        ]

        return {
            'distribuicao_categorias'           : distrib_categorias,
            'evolucao_temporal'                 : evolucao_temporal,
            'top_tags_48h'                      : top_tags_48h,
            'confianca_media_por_categoria'     : confianca_media,
            'comentarios_por_hora'              : comentarios_por_hora
        }
