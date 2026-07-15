# Componentes

Todos os componentes principais seguem o mesmo padrao: um metodo `*_html` retorna uma string HTML e o metodo sem sufixo exibe o resultado no notebook.

## Cards e callouts

```python
CQ.card("Dataset", "Base carregada e pronta para analise.", variant="info")
CQ.callout("Atencao", "Revise valores ausentes antes do treino.", variant="warning")
```

Variantes disponiveis: `default`, `hero`, `info`, `success`, `warning` e `danger`.

## Grid

```python
CQ.grid([
    ("Entrada", "Leitura do dataset", "blue"),
    ("Treino", "Execucao dos modelos", "green"),
    ("Avaliacao", "Comparacao de metricas", "purple"),
])
```

`CQ.cards(...)` e um alias para `CQ.grid(...)`.

## Badges

```python
CQ.badges([
    ("Academico", "blue"),
    ("Reprodutivel", "green"),
    ("Em revisao", "amber"),
])
```

## Metricas

```python
CQ.metrics([
    ("Linhas", "53.940", "Registros"),
    {"label": "Acuracia", "value": "0.91", "note": "Validacao", "color": "green"},
])
```

## Checklist

```python
CQ.checklist([
    ("Dataset carregado", True),
    {"label": "Resultados interpretados", "done": False, "note": "Completar conclusao"},
])
```

## Etapas

```python
CQ.steps([
    ("Carregamento", "Obter a base.", "done"),
    ("Pre-processamento", "Preparar variaveis.", "active"),
    ("Resultados", "Comparar metricas.", "pending"),
])
```

## Comparacao

```python
CQ.compare(
    "Antes",
    "Notebook com blocos soltos.",
    "Depois",
    "Fluxo documentado com componentes visuais.",
    title="Evolucao",
)
```

## Tabelas e figuras

```python
CQ.table(df, title="Amostra", subtitle="Cinco primeiras linhas", max_rows=5)
CQ.figure(fig, title="Distribuicao", subtitle="Grafico gerado no notebook")
```

`table_html` usa `head(...).to_html(...)` quando o objeto suporta essa API. Caso contrario, renderiza `str(obj)` escapado em um bloco `pre`.

## Modulos

```python
screens = [
    CQ.screen("Resumo", CQ.card_html("Objetivo", "Explicar o fluxo.")),
    CQ.screen("Checklist", CQ.checklist_html(["Revisar dados", ("Treinar modelo", True)])),
]

CQ.module("Modulo de estudo", screens)
```

`module_html` exige ao menos uma tela e levanta `ValueError` quando recebe uma lista vazia.
