import pytest

import os
import sys

from app.config import Config
from app.evals  import (
    main,
    slugify,
    CATEGORIES,
)


Config.OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
Config.LLM_MODEL      = os.getenv('LLM_MODEL')


MIN_VALUES_CATEGORIES = {
    'ELOGIO':   { 'min_recall': 0.60, 'min_precision': 0.60, 'min_f1': 0.60 },
    'CRÍTICA':  { 'min_recall': 0.65, 'min_precision': 0.65, 'min_f1': 0.65 },
    'SUGESTÃO': { 'min_recall': 0.50, 'min_precision': 0.60, 'min_f1': 0.70 },
    'DÚVIDA':   { 'min_recall': 0.65, 'min_precision': 0.65, 'min_f1': 0.65 },
    'SPAM':     { 'min_recall': 0.80, 'min_precision': 0.80, 'min_f1': 0.80 },
}


def run_cli_and_capture(args, capsys):
    """ Executa a CLI com os argumentos fornecidos e captura a saída."""

    old_argv = sys.argv[:]
    sys.argv = ['eval_cli'] + args

    with pytest.raises(SystemExit) as exc:
        main()

    out = capsys.readouterr().out
    sys.argv = old_argv

    return exc.value.code, out


def test_eval_cli_success_with_all_and_min_recall(capsys):
    """ Testar a CLI de avaliação com --all e definindo parametros mínimos. """

    here     = os.path.dirname(__file__)
    csv_path = os.path.abspath(os.path.join(here, '..', 'data', 'test_comments.csv'))

    args = ["--data-csv", csv_path, '--all']

    for cat in CATEGORIES:
        min_recall      = MIN_VALUES_CATEGORIES[cat]['min_recall']
        min_precision   = MIN_VALUES_CATEGORIES[cat]['min_precision']
        min_f1          = MIN_VALUES_CATEGORIES[cat]['min_f1']

        key = slugify(cat)
        args += [ f"--{key}-min-recall"     , str(min_recall)       ]
        args += [ f"--{key}-min-precision"  , str(min_precision)    ]
        args += [ f"--{key}-min-f1"         , str(min_f1)           ]

    code, out = run_cli_and_capture(args, capsys)

    # assert code == 0, f"esperava exit=0 mas foi {code!r}"
    assert "=== Classification Report ===" in out
    
    # Verificar mensagens de sucesso para cada categoria
    for cat in CATEGORIES:
        assert f"[✓] Recall {cat}" in out, f"Recall para {cat} falhou ou não encontrado"
        assert f"[✓] Precisão {cat}" in out, f"Precisão para {cat} falhou ou não encontrado"
        assert f"[✓] F1 {cat}" in out, f"F1 para {cat} falhou ou não encontrado"
