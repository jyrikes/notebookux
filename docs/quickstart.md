# Guia rapido

Este exemplo mostra a estrutura basica de um notebook usando `notebookux`.

```python
from notebookux import UX as CQ

CQ.setup("blueprint", compact=True)

CQ.cover(
    title="Analise de Classificacao",
    subtitle="Fluxo de exploracao, treino e avaliacao",
    meta=[
        ("Disciplina", "Inteligencia Artificial"),
        ("Ambiente", "Jupyter"),
    ],
    bullets=[
        "Organizacao visual do estudo",
        "Indicadores principais",
        "Navegacao por etapas",
    ],
)
```

## Secao

```python
CQ.section(
    "Diagnostico inicial",
    subtitle="Resumo antes da modelagem.",
    kicker="Etapa 1",
)
```

## Metricas

```python
CQ.metrics(
    [
        ("Linhas", "53.940", "Registros carregados"),
        {"label": "Classes", "value": "5", "note": "Variavel alvo", "color": "purple"},
        {"label": "Acuracia", "value": "0.91", "note": "Validacao", "color": "green"},
    ],
    title="Indicadores",
)
```

## Modulo navegavel

```python
screens = [
    CQ.screen("Contexto", CQ.card_html("Objetivo", "Comparar modelos de classificacao.")),
    CQ.screen("Checklist", CQ.checklist_html([("Dataset carregado", True), ("Metricas revisadas", False)])),
]

CQ.module("Fluxo do estudo", screens)
```

Os metodos `*_html` retornam strings e podem ser combinados dentro de modulos ou celulas customizadas.
