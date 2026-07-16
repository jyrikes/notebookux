from __future__ import annotations

from notebookux import NotebookUX, render_parallelism_demo


class CaptureUX(NotebookUX):
    def __init__(self) -> None:
        super().__init__()
        self.html = ""

    def wrap(self, html: str) -> None:
        self.html = html


def test_parallelism_demo_is_self_contained_and_interactive() -> None:
    ux = CaptureUX()

    render_parallelism_demo(ux)

    assert "Paralelismo qu\u00e2ntico e seus limites" in ux.html
    assert "Tela ${index + 1} de ${screens.length}" in ux.html
    assert 'id="paralelismo-lite_prev"' in ux.html
    assert 'id="paralelismo-lite_next"' in ux.html
    assert "Voltar" in ux.html
    assert "Avan&ccedil;ar" in ux.html
    assert 'data-pl-function=\\"f1\\"' in ux.html
    assert 'data-pl-mode=\\"superposition\\"' in ux.html
    assert 'id=\\"pl-measure\\"' in ux.html
    assert 'let selectedFunction = "f1"' in ux.html
    assert 'let selectedInput = "superposition"' in ux.html


def test_parallelism_demo_has_no_fragile_render_dependencies() -> None:
    ux = CaptureUX()

    render_parallelism_demo(ux)

    lowered = ux.html.lower()
    assert "<table" not in lowered
    assert "<img" not in lowered
    assert "\\rangle" not in ux.html
    assert "\\frac" not in ux.html
