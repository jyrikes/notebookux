from __future__ import annotations

import pytest

from notebookux import NotebookUX, available_algorithm_lessons, render_algorithm_lesson


class CaptureUX(NotebookUX):
    def __init__(self) -> None:
        super().__init__()
        self.html = ""

    def wrap(self, html: str) -> None:
        self.html = html


EXPECTED = {
    "parallelism-circuit", "measurement-limits", "deutsch-problem",
    "deutsch-algorithm", "deutsch-jozsa-overview", "dj-oracle-inspection",
    "dj-results", "bernstein-vazirani", "algorithm-recap",
}


def test_all_algorithm_lessons_render_as_modules() -> None:
    assert set(available_algorithm_lessons()) == EXPECTED
    for lesson_id in EXPECTED:
        ux = CaptureUX()
        render_algorithm_lesson(ux, lesson_id)
        assert f'id="algorithm-{lesson_id}"' in ux.html
        assert "Voltar" in ux.html
        assert "Avan&ccedil;ar" in ux.html
        assert "\\rangle" not in ux.html
        assert "\\frac" not in ux.html
        assert "<table" not in ux.html.lower()
        assert "data:image" not in ux.html.lower()


def test_guided_questions_and_portrait_fallbacks_are_present() -> None:
    ux = CaptureUX()
    render_algorithm_lesson(ux, "bernstein-vazirani")
    assert "Mostrar solução" in ux.html
    assert "data-lx-panel=\\\"hint\\\"" in ux.html
    assert "onerror=\\\"this.hidden=true" in ux.html
    assert "UC Berkeley EECS" in ux.html


def test_unknown_lesson_lists_available_choices() -> None:
    with pytest.raises(ValueError, match="Available lessons"):
        render_algorithm_lesson(CaptureUX(), "unknown")
