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

UX.page("Ambiente", current=1, total=4, subtitle="Setup, dependencias e parametros individuais.")

UX.badge_row([
    ("Qiskit", "#2563EB"),
    ("Simulador ideal", "#15803D"),
    ("Ruido", "#B45309"),
])

UX.card_grid([
    ("Deutsch-Jozsa", "Classifica uma funcao como constante ou balanceada.", "#2563EB"),
    ("Bernstein-Vazirani", "Recupera uma string secreta com uma consulta.", "#15803D"),
])
