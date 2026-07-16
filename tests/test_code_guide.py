from __future__ import annotations

import pytest

from notebookux import NotebookUX, render_code_guide


class CaptureUX(NotebookUX):
    def __init__(self) -> None:
        super().__init__()
        self.html = ""

    def wrap(self, html: str) -> None:
        self.html = html


def test_code_guide_renders_flow_steps_and_expected_result() -> None:
    ux = CaptureUX()
    render_code_guide(
        ux,
        title="Quantum-CQ • Deutsch-Jozsa",
        library="Quantum-CQ",
        dsl="builder lógico",
        summary="Constrói uma IR neutra.",
        steps=("Prepare os qubits.", "Aplique o oráculo."),
        expected="O pico será 101.",
        concepts=("CircuitIR", "phase-kickback"),
    )

    assert "antes de executar" in ux.html
    assert "Quantum-CQ • Deutsch-Jozsa" in ux.html
    assert "builder lógico" in ux.html
    assert "O que o código fará" in ux.html
    assert "01" in ux.html and "02" in ux.html
    assert "descrição" in ux.html and "CircuitIR" in ux.html
    assert "O pico será 101." in ux.html
    assert "<table" not in ux.html


def test_code_guide_requires_steps() -> None:
    with pytest.raises(ValueError, match="steps"):
        render_code_guide(
            CaptureUX(),
            title="Sem passos",
            library="Quantum-CQ",
            dsl="MQT",
            summary="Resumo",
            steps=(),
            expected="Resultado",
        )
