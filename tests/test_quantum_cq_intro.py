from __future__ import annotations

from notebookux import NotebookUX, render_quantum_cq_intro


class CaptureUX(NotebookUX):
    def __init__(self) -> None:
        super().__init__()
        self.html = ""

    def wrap(self, html: str) -> None:
        self.html = html


def test_quantum_cq_intro_explains_four_real_dsls() -> None:
    ux = CaptureUX()
    render_quantum_cq_intro(ux)

    assert 'id="quantum-cq-intro"' in ux.html
    assert "Equação MQT" in ux.html
    assert "Matriz QC" in ux.html
    assert "Builder CQ.circuit" in ux.html
    assert "Fachada fluente de algoritmos" in ux.html
    assert "data-cqi-dsl" in ux.html
    assert "CQ.run_engine" in ux.html
    assert "CQ.emit" in ux.html
    assert "github.com/jyrikes/quantum-cq" in ux.html
    assert "<table" not in ux.html


def test_quantum_cq_intro_keeps_execution_visible() -> None:
    ux = CaptureUX()
    render_quantum_cq_intro(ux)

    assert "Nenhuma execução fica escondida" in ux.html
    assert "Voltar" in ux.html
    assert "Avan&ccedil;ar" in ux.html
    assert "<script src=" not in ux.html
