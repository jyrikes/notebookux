from __future__ import annotations

import matplotlib.pyplot as plt
import pandas as pd

from notebookux import UX as CQ

CQ.setup("blueprint", compact=True)

CQ.cover(
    title="Relatorio Academico com NotebookUX",
    subtitle="Exemplo de notebook pronto para apresentacao",
    meta=[
        ("Disciplina", "Inteligencia Artificial"),
        ("Formato", "Notebook"),
    ],
    bullets=[
        "Componentes prontos",
        "Fluxo visual consistente",
        "Sem HTML manual no notebook",
    ],
    people=[
        ("Yngrid Kalinne", "Autora"),
    ],
)

CQ.section(
    "Diagnostico inicial",
    subtitle="Resumo visual da base antes da modelagem.",
    kicker="Etapa 1",
)

CQ.badges(
    [
        ("Dataset", "blue"),
        ("Classificacao", "green"),
        ("Validacao", "amber"),
        ("Relatorio", "purple"),
    ]
)

CQ.metrics(
    [
        ("Linhas", "53.940", "Registros carregados", "blue"),
        ("Colunas", "10", "Variaveis disponiveis", "green"),
        {"label": "Classes", "value": "5", "note": "Categorias do alvo", "color": "purple"},
        {"label": "Nulos", "value": "0", "note": "Ausentes encontrados", "color": "gray"},
    ],
    title="Indicadores da base",
)

CQ.checklist(
    [
        ("Dataset carregado", True, "A fonte foi registrada no notebook."),
        ("Colunas conferidas", True),
        {"label": "Modelos executados", "done": False, "note": "Proxima etapa do experimento."},
    ],
    title="Checklist de preparacao",
)

CQ.steps(
    [
        ("Carregamento", "Obter a base e validar a estrutura.", "done"),
        ("Pre-processamento", "Preparar variaveis e separar treino/teste.", "active"),
        ("Modelagem", "Executar algoritmos com parametros comparaveis.", "pending"),
        {"title": "Resultados", "body": "Gerar tabelas, graficos e discussao.", "status": "pending"},
    ],
    title="Fluxo do notebook",
)

CQ.compare(
    "Notebook bruto",
    "Celulas longas, poucos marcadores visuais e repeticao de HTML.",
    "Notebook organizado",
    "Componentes reutilizaveis, secoes claras e relatorio mais facil de revisar.",
    title="Antes e depois",
)

df = pd.DataFrame(
    {
        "modelo": ["Arvore", "KNN", "SVM"],
        "f1_medio": [0.81, 0.78, 0.84],
        "status": ["ok", "ok", "melhor"],
    }
)

fig, ax = plt.subplots(figsize=(4, 2.4))
ax.bar(df["modelo"], df["f1_medio"], color=[CQ.color("blue"), CQ.color("green"), CQ.color("purple")])
ax.set_ylim(0, 1)
ax.set_title("F1 medio por modelo")

CQ.module(
    "Resumo final",
    [
        CQ.screen("Metricas", CQ.metrics_html([("Melhor F1", "0.84", "SVM", "purple")])),
        CQ.screen("Tabela", CQ.table_html(df, title="Comparativo de modelos")),
        CQ.screen("Grafico", CQ.figure_html(fig, title="Desempenho por modelo")),
        CQ.screen(
            "Conclusao",
            CQ.callout_html(
                "Resultado interpretavel",
                "O notebook apresenta resultados em blocos curtos, com evidencias e contexto visual.",
                variant="success",
            ),
        ),
    ],
)
