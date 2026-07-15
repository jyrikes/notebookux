# notebookux

[![CI](https://github.com/jyrikes/notebookux/actions/workflows/ci.yml/badge.svg)](https://github.com/jyrikes/notebookux/actions/workflows/ci.yml)
[![Docs](https://github.com/jyrikes/notebookux/actions/workflows/docs.yml/badge.svg)](https://github.com/jyrikes/notebookux/actions/workflows/docs.yml)
[![PyPI](https://img.shields.io/pypi/v/notebookux.svg)](https://pypi.org/project/notebookux/)

`notebookux` is a small visual layer for Python notebooks.

It provides reusable presentation helpers for academic and technical notebooks:

- themes
- cover and section pages
- badges, cards, grids and code panels
- styled tables and figures
- simple multi-screen modules with previous/next navigation

The package is UI-only. It does not depend on Colab and does not implement data
processing, machine learning pipelines or project-specific logic.

## Docs

Documentation is published with MkDocs Material:

- GitHub Pages: <https://jyrikes.github.io/notebookux/>
- API reference: <https://jyrikes.github.io/notebookux/api/>

## Install for development

```powershell
cd "C:\Users\Yngrid Kalinne\Documents\cq-novo\notebookux"
python -m pip install -e ".[dev,docs,examples]"
```

## Basic use

```python
from notebookux import UX

UX.use_theme("blueprint")

UX.cover(
    title="Resolucao de Computacao Quantica",
    subtitle="Deutsch-Jozsa e Bernstein-Vazirani",
    meta=[
        ("Disciplina", "Computacao Quantica"),
        ("Formato", "Notebook"),
    ],
    bullets=[
        "Execucoes com evidencias",
        "Tabelas de contagens",
        "Comparacao entre simuladores",
    ],
)
```

## Uso rapido

Para notebooks academicos, voce pode importar com um nome curto e usar os
componentes prontos sem escrever HTML manualmente.

```python
from notebookux import UX as CQ

CQ.setup("blueprint", compact=True)

CQ.section(
    "Diagnostico inicial",
    subtitle="Resumo visual da base antes da modelagem.",
    kicker="Etapa 1",
)

CQ.badges([
    ("Dataset", "blue"),
    ("Classificacao", "green"),
    ("Reprodutivel", "amber"),
])

CQ.metrics([
    ("Linhas", "53.940", "Registros carregados"),
    {"label": "Classes", "value": "5", "note": "Variavel alvo", "color": "purple"},
])

CQ.checklist([
    ("Dataset carregado", True),
    {"label": "Modelos configurados", "done": False, "note": "Executar na proxima celula"},
])

CQ.steps([
    ("Carregamento", "Obter a base e conferir as colunas.", "done"),
    ("Pre-processamento", "Preparar dados para os modelos.", "active"),
    ("Resultados", "Comparar metricas e discutir.", "pending"),
])

CQ.compare(
    "Antes",
    "Dados brutos e sem organizacao visual.",
    "Depois",
    "Notebook com secoes, metricas e fluxo documentado.",
    title="Comparacao do notebook",
)
```

## HTML-first API

Every main visual component has a method that returns HTML and a matching method
that displays it in a notebook.

```python
card = UX.card_html("Dataset", "Resumo da base carregada.", variant="info")
table = UX.table_html(df.head(), title="Amostra")

UX.module(
    "Diagnostico",
    [
        UX.screen("Contexto", card),
        UX.screen("Tabela", table),
    ],
)
```

Use `from notebookux import UX as CQ` when migrating notebooks that already use a
short `CQ` helper name.

## Checks

```powershell
python -m ruff check .
python -m pyright
python -m pytest --cov=notebookux --cov-report=term-missing
python -m build
python -m mkdocs build --strict
```

## Release

Releases are published by GitHub Actions when a `v*` tag is pushed. The PyPI
project must be configured with Trusted Publishing for repository
`jyrikes/notebookux`, workflow `release.yml` and environment `pypi`.
