from __future__ import annotations

import matplotlib.pyplot as plt
import pandas as pd

from notebookux import UX

UX.use_theme("blueprint")

UX.cover(
    title="NotebookUX Showcase",
    subtitle="Example notebook structure",
    meta=[
        ("Package", "notebookux"),
        ("Mode", "UI-only"),
    ],
    bullets=[
        "Cover and section pages",
        "Cards, grids and badges",
        "Tables, figures and modules",
    ],
    people=[
        ("Yngrid Kalinne", "Author"),
    ],
)

UX.page("Overview", current=1, total=2, subtitle="Reusable visual blocks for academic notebooks.")

UX.badge_row(
    [
        ("Notebook", "#2563EB"),
        ("Tables", "#15803D"),
        ("Figures", "#B45309"),
    ]
)

UX.grid(
    [
        ("HTML first", "Use *_html methods when composing larger views.", "#2563EB"),
        ("Display ready", "Use display methods directly inside notebook cells.", "#15803D"),
        ("Lightweight", "No data processing or ML pipeline logic in the core.", "#B45309"),
    ]
)

df = pd.DataFrame(
    {
        "step": ["load", "clean", "model"],
        "status": ["done", "done", "planned"],
        "notes": ["Dataset received", "Types checked", "Next notebook cell"],
    }
)

fig, ax = plt.subplots(figsize=(4, 2.4))
ax.bar(["A", "B", "C"], [3, 7, 5], color=["#2563EB", "#15803D", "#B45309"])
ax.set_title("Example figure")
ax.set_ylabel("value")

UX.module(
    "Reusable Report Block",
    [
        UX.screen(
            "Summary",
            UX.card_html(
                "Why this exists",
                "The notebook keeps data logic in normal Python cells and uses notebookux only for presentation.",
                variant="info",
            ),
        ),
        UX.screen("Table", UX.table_html(df, title="Pipeline status")),
        UX.screen("Figure", UX.figure_html(fig, title="Small chart")),
        UX.screen(
            "Code",
            UX.code_block_html(
                "from notebookux import UX\n\nUX.use_theme('blueprint')\nUX.card('Title', 'Body')",
                title="Minimal setup",
            ),
        ),
    ],
)
