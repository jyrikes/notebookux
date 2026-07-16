from __future__ import annotations

import pytest

from notebookux import UX, NotebookUX, __version__, create_theme


def test_public_imports() -> None:
    assert isinstance(UX, NotebookUX)
    assert __version__ == "0.2.1"
    assert create_theme()["primary"] == "#1a73e8"


def test_theme_merge_and_overrides() -> None:
    ux = NotebookUX()

    theme = ux.use_theme("blueprint", primary="#123456", fs_body="18px")

    assert theme["accent"] == "#c9a227"
    assert theme["primary"] == "#123456"
    assert theme["fs_body"] == "18px"


def test_mapping_theme_starts_from_base_theme() -> None:
    ux = NotebookUX()

    theme = ux.use_theme({"primary": "#111111"})

    assert theme["primary"] == "#111111"
    assert theme["surface"] == "#ffffff"


def test_setup_applies_theme_compact_typography_language_and_overrides() -> None:
    ux = NotebookUX()

    theme = ux.setup("blueprint", compact=True, language="pt", primary="#123456")

    assert ux.language == "pt"
    assert theme["accent"] == "#c9a227"
    assert theme["fs_body"] == "15px"
    assert theme["page_padding"] == "18px"
    assert theme["primary"] == "#123456"


def test_color_supports_names_hex_theme_keys_and_fallback() -> None:
    ux = NotebookUX()
    ux.use_theme("blueprint")

    assert ux.color("blue") == "#2563EB"
    assert ux.color("#abcdef") == "#abcdef"
    assert ux.color("primary") == "#1f4e8c"
    assert ux.color("unknown", fallback="gray") == "#57534E"


def test_card_html_escapes_text_and_supports_variants() -> None:
    ux = NotebookUX()

    html = ux.card_html("<Title>", "a < b\nc", variant="info")

    assert "&lt;Title&gt;" in html
    assert "a &lt; b<br>c" in html
    assert "#e8f0fe" in html


def test_callout_html_reuses_card_variants_and_escapes_text() -> None:
    ux = NotebookUX()

    html = ux.callout_html("<Aviso>", "valor < limite", variant="warning")

    assert "&lt;Aviso&gt;" in html
    assert "valor &lt; limite" in html
    assert "#fef7e0" in html


def test_code_block_html_escapes_code() -> None:
    ux = NotebookUX()

    html = ux.code_block_html("print('<x>')", title="<Code>")

    assert "&lt;Code&gt;" in html
    assert "print(&#x27;&lt;x&gt;&#x27;)" in html


def test_grid_html_accepts_tuples_and_mappings() -> None:
    ux = NotebookUX()

    html = ux.grid_html(
        [
            ("Tuple", "Body", "#123456"),
            {"title": "Mapping", "body": "Text", "color": "#654321"},
        ]
    )

    assert "Tuple" in html
    assert "Mapping" in html
    assert "#123456" in html
    assert "#654321" in html


def test_badges_and_cards_aliases_render_named_colors() -> None:
    ux = NotebookUX()

    badges = ux.badges_html([("Dataset", "blue")])
    cards = ux.cards_html([("Modelo", "Arvore", "green")])

    assert "#2563EB" in badges
    assert "#15803D" in cards
    assert "Modelo" in cards


def test_metrics_html_accepts_tuples_and_mappings() -> None:
    ux = NotebookUX()

    html = ux.metrics_html(
        [
            ("Linhas", "53.940", "Registros", "blue"),
            {"label": "Classes", "value": "5", "note": "Alvo", "color": "purple"},
        ],
        title="<Indicadores>",
    )

    assert "&lt;Indicadores&gt;" in html
    assert "Linhas" in html
    assert "53.940" in html
    assert "Classes" in html
    assert "#7C3AED" in html


def test_checklist_html_accepts_strings_tuples_and_mappings() -> None:
    ux = NotebookUX()

    html = ux.checklist_html(
        [
            "Item simples",
            ("Feito", True),
            {"label": "Pendente", "done": False, "note": "<revisar>"},
        ],
        title="Checklist",
    )

    assert "Item simples" in html
    assert "Feito" in html
    assert "Pendente" in html
    assert "&lt;revisar&gt;" in html
    assert "&#10003;" in html
    assert "&#9675;" in html


def test_steps_html_accepts_strings_tuples_and_mappings() -> None:
    ux = NotebookUX()

    html = ux.steps_html(
        [
            "Carregar dataset",
            ("Preparar", "Normalizar variaveis", "active"),
            {"title": "Treino", "body": "Executar modelos", "status": "done"},
        ],
        title="Fluxo",
    )

    assert "Carregar dataset" in html
    assert "Normalizar variaveis" in html
    assert "Treino" in html
    assert "#15803D" in html


def test_compare_key_values_and_section_escape_text() -> None:
    ux = NotebookUX()

    compare = ux.compare_html("<Antes>", "a < b", "Depois", "ok", title="Comparacao")
    key_values = ux.key_values_html({"Disciplina": "<IA>"}, title="Meta")
    section = ux.section_html("<Titulo>", subtitle="sub < texto", kicker="Etapa")

    assert "&lt;Antes&gt;" in compare
    assert "a &lt; b" in compare
    assert "&lt;IA&gt;" in key_values
    assert "&lt;Titulo&gt;" in section
    assert "sub &lt; texto" in section


class FakeTable:
    def __init__(self) -> None:
        self.head_arg: int | None = None

    def head(self, rows: int) -> FakeTable:
        self.head_arg = rows
        return self

    def to_html(self, index: bool = True, border: int = 0) -> str:
        assert index is True
        assert border == 0
        return "<table><thead><tr><th>name</th></tr></thead><tbody><tr><td>Alice</td></tr></tbody></table>"


def test_table_html_uses_head_and_styles_table() -> None:
    ux = NotebookUX()
    table = FakeTable()

    html = ux.table_html(table, title="<People>", subtitle="First rows", max_rows=2)

    assert table.head_arg == 2
    assert "&lt;People&gt;" in html
    assert "First rows" in html
    assert "border-collapse:separate" in html
    assert "Alice" in html


def test_table_html_fallback_escapes_plain_objects() -> None:
    ux = NotebookUX()

    html = ux.table_html("<not a table>")

    assert "<pre>&lt;not a table&gt;</pre>" in html


class FakeFigure:
    def __init__(self) -> None:
        self.kwargs: dict[str, object] = {}

    def savefig(self, buffer, **kwargs: object) -> None:
        self.kwargs = kwargs
        buffer.write(b"fake-png")


def test_figure_html_embeds_png_data() -> None:
    ux = NotebookUX()
    fig = FakeFigure()

    html = ux.figure_html(fig, title="Chart", dpi=90)

    assert fig.kwargs["format"] == "png"
    assert fig.kwargs["bbox_inches"] == "tight"
    assert fig.kwargs["dpi"] == 90
    assert "data:image/png;base64,ZmFrZS1wbmc=" in html


def test_screen_returns_title_and_html_strings() -> None:
    ux = NotebookUX()

    screen = ux.screen("Intro", ux.card_html("A", "B"))

    assert screen["title"] == "Intro"
    assert "A" in screen["html"]


def test_markdown_html_renders_tables_details_math_and_media() -> None:
    ux = NotebookUX()

    html = ux.markdown_html(
        "## Titulo\n\n| a | b |\n|---|---|\n| 1 | 2 |\n\n<details><summary>Resposta</summary>$|0\\rangle$</details>",
        image_url="https://example.com/photo.png?x=1&y=2",
        image_caption="Foto <historica>",
    )

    assert "<table>" in html
    assert "<details>" in html
    assert "$|0\\rangle$" in html
    assert "https://example.com/photo.png?x=1&amp;y=2" in html
    assert "Foto &lt;historica&gt;" in html
    assert "nbux-markdown-layout has-media" in html


def test_markdown_screen_returns_rendered_screen() -> None:
    ux = NotebookUX()

    screen = ux.markdown_screen("Historia", "**Texto original**")

    assert screen["title"] == "Historia"
    assert "<strong>Texto original</strong>" in screen["html"]


def test_module_html_renders_one_screen_and_sanitizes_id() -> None:
    ux = NotebookUX()

    html = ux.module_html("My Module", [ux.screen("Intro", "<p>Body</p>")], module_id="my module")

    assert 'id="my-module"' in html
    assert "Intro" in html
    assert "<p>Body</p>" in html
    assert "Tela ${index + 1} de ${screens.length}" in html


def test_module_html_renders_multiple_screens() -> None:
    ux = NotebookUX()

    html = ux.module_html(
        "Flow",
        [
            ux.screen("First", "<p>1</p>"),
            ux.screen("Second", "<p>2</p>"),
        ],
    )

    assert "First" in html
    assert "Second" in html
    assert "Avan&ccedil;ar" in html
    assert "typesetPromise" in html


def test_module_html_rejects_empty_screens() -> None:
    ux = NotebookUX()

    with pytest.raises(ValueError, match="at least one screen"):
        ux.module_html("Empty", [])
