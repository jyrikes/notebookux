from __future__ import annotations

from collections import Counter

import pytest

from notebookux import NotebookUX, render_circuit_output, render_counts_output, render_statevector_output


class CaptureUX(NotebookUX):
    def __init__(self) -> None:
        super().__init__()
        self.html = ""

    def wrap(self, html: str) -> None:
        self.html = html


class FakeCircuit:
    num_qubits = 3
    num_clbits = 2

    def depth(self) -> int:
        return 4

    def size(self) -> int:
        return 7

    def count_ops(self) -> Counter[str]:
        return Counter({"h": 3, "measure": 2, "cx": 2})


class FakeStatevector:
    num_qubits = 2

    def __len__(self) -> int:
        return 4

    def probabilities_dict(self) -> dict[str, float]:
        return {"00": 0.5, "11": 0.5, "01": 0.0, "10": 0.0}


class FakeFigure:
    def savefig(self, output, **kwargs) -> None:
        assert kwargs["format"] == "svg"
        output.write('<?xml version="1.0"?><svg viewBox="0 0 100 50"><path d="M0 0"/></svg>')


@pytest.mark.parametrize("algorithm,expected_copy", [
    ("deutsch", "função como constante"),
    ("deutsch-jozsa", "função é constante"),
    ("bernstein-vazirani", "segredo s = 0"),
    ("paralelismo", "somente um ramo"),
])
def test_counts_output_explains_algorithms(algorithm: str, expected_copy: str) -> None:
    ux = CaptureUX()
    render_counts_output(ux, {"0": 900, "1": 100}, title="Resultado", algorithm=algorithm)
    assert expected_copy in ux.html
    assert "01" in ux.html and "04" in ux.html
    assert "90.0%" in ux.html
    assert "height:100.0000%" in ux.html
    assert 'grid-template-areas:"value" "track" "label"' in ux.html
    assert "<table" not in ux.html


def test_counts_output_rejects_empty_input() -> None:
    with pytest.raises(ValueError, match="positive"):
        render_counts_output(CaptureUX(), {}, title="Vazio")


def test_circuit_output_uses_duck_typed_metrics() -> None:
    ux = CaptureUX()
    render_circuit_output(ux, FakeCircuit(), title="Circuito", figure=FakeFigure())
    assert "profundidade" in ux.html
    assert ">4<" in ux.html
    assert "measure" in ux.html
    assert "Como ler o desenho acima" in ux.html
    assert "qo-circuit-visual" in ux.html
    assert '<svg viewBox="0 0 100 50">' in ux.html


def test_statevector_output_lists_nonzero_probabilities() -> None:
    ux = CaptureUX()
    render_statevector_output(ux, FakeStatevector(), title="Estado")
    assert "estados não nulos" in ux.html
    assert "|00⟩" in ux.html
    assert ux.html.count("50.00%") >= 2
