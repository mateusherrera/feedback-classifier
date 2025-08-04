"""
Código para avaliar o classificador de comentários.

:created by:    Mateus Herrera
:created at:    2025-08-04

:updated by:    Mateus Herrera
:updated at:    2025-08-04
"""

import os
import csv
import sys
import argparse
import unicodedata

from sklearn.metrics import (
    f1_score,
    recall_score,
    precision_score,
    classification_report,
)

from app.services.classifier import (
    CATEGORIES,
    classify_batch,
)


def slugify(text: str) -> str:
    """ Converte string para lowercase, remove acentos e caracteres não alfanuméricos. """

    # Normaliza a string
    nfkd        = unicodedata.normalize('NFKD', text)
    no_accents  = ''.join(c for c in nfkd if not unicodedata.combining(c))

    # Remove caracteres não alfanuméricos e converte para lowercase
    return ''.join(ch for ch in no_accents.lower() if ch.isalnum())


def load_dataset(path: str) -> tuple[list[str], list[str]]:
    """
    Carrega o dataset de comentários a partir de um arquivo CSV.

    :param path: Caminho para o arquivo CSV
    """

    texts, labels = list(), list()

    with open(path, encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            texts.append(row['texto'])
            labels.append(row['categoria'])

    return texts, labels


def main():
    """Função principal para executar as avaliações do classificador."""

    # Configuração do parser de argumentos
    parser = argparse.ArgumentParser(description="Evals & Métricas do classificador")

    # Caminho para o dataset CSV
    parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    data_default = os.path.join(parent_dir, 'data', 'test_comments.csv')
    parser.add_argument(
        '--data-csv',
        '-d',
        default=data_default,
        help='Arquivo CSV com colunas texto e categoria'
    )
    parser.add_argument(
        '--all',
        action='store_true',
        help='Avaliar todas as categorias'
    )

    # Flags para selecionar categorias específicas
    for cat in CATEGORIES:
        key = slugify(cat)
        parser.add_argument(
            f'--{key}',
            action='store_true',
            help=f'Avaliar somente {cat}'
        )

    # Thresholds para cada métrica e categoria
    for cat in CATEGORIES:
        key = slugify(cat)
        parser.add_argument(
            f'--{key}-min-recall',
            type=float,
            default=0.0,
            help=f'Recall mínimo para {cat}'
        )
        parser.add_argument(
            f'--{key}-max-recall',
            type=float,
            default=1.0,
            help=f'Recall máximo para {cat}'
        )
        parser.add_argument(
            f'--{key}-min-precision',
            type=float,
            default=0.0,
            help=f'Precisão mínima para {cat}'
        )
        parser.add_argument(
            f'--{key}-max-precision',
            type=float,
            default=1.0,
            help=f'Precisão máxima para {cat}'
        )
        parser.add_argument(
            f'--{key}-min-f1',
            type=float,
            default=0.0,
            help=f'F1 mínimo para {cat}'
        )
        parser.add_argument(
            f'--{key}-max-f1',
            type=float,
            default=1.0,
            help=f'F1 máximo para {cat}'
        )

    args = parser.parse_args()

    # Carregamento do dataset e classificação
    texts_full, labels_full = load_dataset(args.data_csv)

    # Classificação em lote, sem paralelismo, pois embaralhará o resultado!
    results = classify_batch(texts_full, max_workers=1)

    preds_full = [r.get('categoria') for r in results]

    # Filtra entradas sem classificação válida
    pairs = [(l, p) for l, p in zip(labels_full, preds_full) if p is not None]
    if not pairs:
        print("[✗] Nenhuma classificação válida gerada.")
        sys.exit(1)

    labels, preds = zip(*pairs)
    removed = len(labels_full) - len(preds)
    if removed:
        print(f"[!] {removed} entradas com erro e foram ignoradas na avaliação.")

    # Relatório geral
    print("\n=== Classification Report ===")
    print(
        classification_report(
            labels, preds,
            labels=CATEGORIES,
            digits=3,
            zero_division=0
        )
    )

    # Seleção de categorias a avaliar
    if args.all:
        selected = CATEGORIES
    else:
        selected = [
            cat for cat in CATEGORIES
            if getattr(args, slugify(cat))
        ]
        if not selected:
            selected = CATEGORIES

    # Avaliação por categoria
    failed = False
    for cat in selected:
        key = slugify(cat)
        rec = recall_score(labels, preds, labels=[cat], average='macro', zero_division=0)
        prec = precision_score(labels, preds, labels=[cat], average='macro', zero_division=0)
        f1 = f1_score(labels, preds, average='macro', zero_division=0)

        min_rec = getattr(args, f'{key}_min_recall')
        max_rec = getattr(args, f'{key}_max_recall')
        min_prec = getattr(args, f'{key}_min_precision')
        max_prec = getattr(args, f'{key}_max_precision')
        min_f1 = getattr(args, f'{key}_min_f1')
        max_f1 = getattr(args, f'{key}_max_f1')

        if not (min_rec <= rec <= max_rec):
            print(f"[✗] Recall {cat} {rec:.3f} não está em [{min_rec:.3f}, {max_rec:.3f}]")
            failed = True
        else:
            print(f"[✓] Recall {cat} {rec:.3f} em [{min_rec:.3f}, {max_rec:.3f}]")

        if not (min_prec <= prec <= max_prec):
            print(f"[✗] Precisão {cat} {prec:.3f} não está em [{min_prec:.3f}, {max_prec:.3f}]")
            failed = True
        else:
            print(f"[✓] Precisão {cat} {prec:.3f} em [{min_prec:.3f}, {max_prec:.3f}]")

        if not (min_f1 <= f1 <= max_f1):
            print(f"[✗] F1 {cat} {f1:.3f} não está em [{min_f1:.3f}, {max_f1:.3f}]")
            failed = True
        else:
            print(f"[✓] F1 {cat} {f1:.3f} em [{min_f1:.3f}, {max_f1:.3f}]")

    sys.exit(1 if failed else 0)


if __name__ == "__main__":
    main()
