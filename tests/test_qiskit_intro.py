from __future__ import annotations

from notebookux import NotebookUX, render_qiskit_intro


class CaptureUX(NotebookUX):
    def __init__(self) -> None:
        super().__init__()
        self.html = ""

    def wrap(self, html: str) -> None:
        self.html = html


def test_qiskit_intro_has_video_workflow_and_official_materials() -> None:
    ux = CaptureUX()
    render_qiskit_intro(ux)

    assert 'id="qiskit-intro"' in ux.html
    assert "QcK0GK7DUh8" in ux.html
    assert 'loading=\\"lazy\\"' in ux.html
    assert "data-qi-stage" in ux.html
    assert "QuantumCircuit" in ux.html
    assert "generate_preset_pass_manager" in ux.html
    assert "quantum.cloud.ibm.com/docs/en/guides/construct-circuits" in ux.html
    assert "quantum.cloud.ibm.com/docs/en/guides/transpile" in ux.html
    assert "min-height:480px" not in ux.html


def test_qiskit_intro_keeps_execution_out_of_the_visual_component() -> None:
    ux = CaptureUX()
    render_qiskit_intro(ux)

    assert "nenhuma execução do Qiskit fica escondida" in ux.html
    assert "QiskitRuntimeService(" not in ux.html
    assert "Voltar" in ux.html
    assert "Avan&ccedil;ar" in ux.html
