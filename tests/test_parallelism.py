from __future__ import annotations

from notebookux import create_theme, render_parallelism_demo


class CaptureUX:
    def __init__(self) -> None:
        self.theme = create_theme()
        self.html = ""

    def wrap(self, html: str) -> None:
        self.html = html


def test_parallelism_demo_is_self_contained_and_interactive() -> None:
    ux = CaptureUX()

    render_parallelism_demo(ux)

    assert "Paralelismo qu\u00e2ntico e seus limites" in ux.html
    assert 'id="pl-functions"' in ux.html
    assert 'id="pl-modes"' in ux.html
    assert 'id="pl-measure"' in ux.html
    assert 'let selectedFunction = "f1"' in ux.html
    assert 'let selectedInput = "superposition"' in ux.html


def test_parallelism_demo_has_no_fragile_render_dependencies() -> None:
    ux = CaptureUX()

    render_parallelism_demo(ux)

    lowered = ux.html.lower()
    assert "<table" not in lowered
    assert "<img" not in lowered
    assert "mathjax" not in lowered
    assert "\\rangle" not in ux.html
    assert "\\frac" not in ux.html
