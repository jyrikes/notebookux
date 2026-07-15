# notebookux

`notebookux` e uma camada visual leve para notebooks Python. A biblioteca cria componentes HTML reutilizaveis para deixar notebooks academicos e tecnicos mais claros, sem trazer logica de limpeza de dados, machine learning ou pipeline para o pacote principal.

## Proposta

- Manter uma API simples baseada em `UX`.
- Retornar HTML testavel com metodos `*_html`.
- Exibir diretamente no notebook com metodos sem sufixo.
- Oferecer componentes prontos para capas, secoes, cards, metricas, checklists, tabelas, figuras e modulos navegaveis.
- Funcionar bem em IPython, Jupyter e ambientes compativeis.

## Instalacao

Para uso local:

```bash
pip install notebookux
```

Para desenvolvimento:

```bash
pip install -e ".[dev,docs,examples]"
```

## Primeiro uso

```python
from notebookux import UX as CQ

CQ.setup("blueprint")

CQ.cover(
    title="Analise de Dados",
    subtitle="Notebook academico com componentes visuais",
    meta=[("Curso", "IA"), ("Formato", "Notebook")],
)
```

Consulte o [guia rapido](quickstart.md) para montar um notebook completo.
