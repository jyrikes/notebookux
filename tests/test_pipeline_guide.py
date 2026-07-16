from __future__ import annotations

from notebookux import NotebookUX, render_pipeline_guide, render_pipeline_status


class CaptureUX(NotebookUX):
    def __init__(self) -> None:
        super().__init__()
        self.html = ""

    def wrap(self, html: str) -> None:
        self.html += html


def test_pipeline_guide_explains_all_runtime_targets() -> None:
    ux = CaptureUX()
    render_pipeline_guide(ux)

    assert "O que é uma pipeline?" in ux.html
    assert "PipelineSettings" in ux.html
    assert "RuntimeSettings" in ux.html
    assert "BenchmarkingPipeline" in ux.html
    assert "Ideal" in ux.html
    assert "Noisy" in ux.html
    assert "Real IBM" in ux.html
    assert "Não existe máquina quântica física" in ux.html
    assert "Voltar" in ux.html
    assert "Avan&ccedil;ar" in ux.html
    assert "<table" not in ux.html


def test_pipeline_status_never_receives_or_renders_a_token() -> None:
    ux = CaptureUX()
    render_pipeline_status(
        ux,
        credential_ready=True,
        credential_source="apikey.json",
        real_enabled=False,
        shots=512,
        noise_source="NoiseModel sintético (seed 42)",
    )

    assert "apikey.json" in ux.html
    assert "bloqueado por segurança" in ux.html
    assert "executado" in ux.html
    assert "token foi lido somente em memória" in ux.html
    assert "<table" not in ux.html
