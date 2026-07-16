import math
from collections.abc import Mapping, Sequence
from html import escape
from io import StringIO
from itertools import count
from typing import Any

_OUTPUT_IDS = count(1)


def render_counts_output(
    ux,
    counts: Mapping[str, int],
    *,
    title: str,
    algorithm: str = "generic",
    expected: str | None = None,
    context: str = "",
    bit_order: str = "",
) -> None:
    """Explain a counts mapping with lightweight bars and a four-step reading guide."""
    clean = {str(key): int(value) for key, value in counts.items() if int(value) >= 0}
    if not clean or sum(clean.values()) <= 0:
        raise ValueError("counts must contain at least one positive count")

    ordered = sorted(clean.items(), key=lambda item: (-item[1], item[0]))
    total = sum(clean.values())
    dominant, dominant_count = ordered[0]
    confidence = dominant_count / total
    conclusion = _counts_conclusion(algorithm, dominant, expected)
    output_id = f"quantum-counts-{next(_OUTPUT_IDS)}"
    bars = _count_bars(ordered, total)
    expected_copy = _expected_copy(expected, dominant, clean, total)
    body = f"""
    <section id="{output_id}" class="qo-root">
      <header><div><small>Saída explicada</small><h3>{escape(title)}</h3></div><span>{escape(algorithm.replace('-', ' ').title())}</span></header>
      {f'<p class="qo-context">{escape(context)}</p>' if context else ''}
      <div class="qo-metrics">
        <article><small>shots</small><b>{total:,}</b></article>
        <article><small>estado dominante</small><b>{escape(dominant)}</b></article>
        <article><small>frequência</small><b>{confidence:.1%}</b></article>
      </div>
      <div class="qo-bars">{bars}</div>
      <div class="qo-steps">
        <article><b>01</b><div><strong>Conte as execuções</strong><p>As contagens somam {total:,} shots. Cada shot termina em uma bitstring medida.</p></div></article>
        <article><b>02</b><div><strong>Localize o pico</strong><p>O resultado {escape(dominant)} apareceu {dominant_count:,} vezes e concentra {confidence:.1%} da amostra.</p></div></article>
        <article><b>03</b><div><strong>Interprete o algoritmo</strong><p>{escape(conclusion)}</p></div></article>
        <article><b>04</b><div><strong>Confira a expectativa</strong><p>{escape(expected_copy)}</p></div></article>
      </div>
      {f'<div class="qo-note"><strong>Ordem dos bits:</strong> {escape(bit_order)}</div>' if bit_order else ''}
    </section>
    """
    ux.wrap(_style(ux, output_id) + body)


def render_circuit_output(
    ux,
    circuit: Any,
    *,
    title: str,
    stage: str = "circuito",
    explanation: str = "",
    steps: Sequence[str] | None = None,
    figure: Any | None = None,
) -> None:
    """Summarize an already-built circuit without importing or executing Qiskit."""
    output_id = f"quantum-circuit-{next(_OUTPUT_IDS)}"
    num_qubits = int(getattr(circuit, "num_qubits", 0))
    num_clbits = int(getattr(circuit, "num_clbits", 0))
    depth = _call_int(circuit, "depth")
    size = _call_int(circuit, "size")
    operations = _operations(circuit)
    reading_steps = tuple(steps or (
        "Leia os fios de cima para baixo: cada linha acompanha um qubit ou bit clássico.",
        "Siga da esquerda para a direita: essa é a ordem temporal das operações.",
        "Use as barreiras como separadores visuais entre preparação, oráculo e leitura.",
        "Na medição, conecte cada qubit ao bit clássico que armazenará o resultado.",
    ))
    step_html = "".join(
        f'<article><b>{index:02d}</b><p>{escape(copy)}</p></article>'
        for index, copy in enumerate(reading_steps, 1)
    )
    operation_html = "".join(f'<span><b>{escape(name)}</b> × {amount}</span>' for name, amount in operations)
    circuit_visual = _figure_svg(figure) if figure is not None else ""
    body = f"""
    <section id="{output_id}" class="qo-root qo-circuit">
      <header><div><small>Como ler o desenho acima</small><h3>{escape(title)}</h3></div><span>{escape(stage)}</span></header>
      {f'<p class="qo-context">{escape(explanation)}</p>' if explanation else ''}
      {f'<div class="qo-circuit-visual">{circuit_visual}</div>' if circuit_visual else ''}
      <div class="qo-metrics">
        <article><small>qubits</small><b>{num_qubits}</b></article>
        <article><small>bits clássicos</small><b>{num_clbits}</b></article>
        <article><small>profundidade</small><b>{depth}</b></article>
        <article><small>operações</small><b>{size}</b></article>
      </div>
      <div class="qo-operations">{operation_html or '<span>sem operações</span>'}</div>
      <div class="qo-reading">{step_html}</div>
    </section>
    """
    ux.wrap(_style(ux, output_id) + body)


def render_statevector_output(
    ux,
    statevector: Any,
    *,
    title: str,
    explanation: str = "",
) -> None:
    """Explain the largest basis-state probabilities of an existing statevector."""
    probabilities = statevector.probabilities_dict()
    ordered = sorted(((str(key), float(value)) for key, value in probabilities.items()), key=lambda item: (-item[1], item[0]))
    nonzero = [(key, value) for key, value in ordered if value > 1e-12]
    if not nonzero:
        raise ValueError("statevector has no non-zero probabilities")
    output_id = f"quantum-state-{next(_OUTPUT_IDS)}"
    num_qubits = int(getattr(statevector, "num_qubits", round(math.log2(len(statevector)))))
    dominant, probability = nonzero[0]
    bars = "".join(
        f'<div class="qo-bar"><span>{escape(key)}</span><i><b style="height:{value * 100:.4f}%"></b></i><strong>{value:.2%}</strong></div>'
        for key, value in nonzero[:8]
    )
    body = f"""
    <section id="{output_id}" class="qo-root">
      <header><div><small>Estado quântico explicado</small><h3>{escape(title)}</h3></div><span>Statevector</span></header>
      {f'<p class="qo-context">{escape(explanation)}</p>' if explanation else ''}
      <div class="qo-metrics">
        <article><small>qubits</small><b>{num_qubits}</b></article>
        <article><small>amplitudes</small><b>{2 ** num_qubits}</b></article>
        <article><small>estados não nulos</small><b>{len(nonzero)}</b></article>
        <article><small>maior probabilidade</small><b>{probability:.1%}</b></article>
      </div>
      <div class="qo-bars">{bars}</div>
      <div class="qo-steps">
        <article><b>01</b><div><strong>Identifique a base</strong><p>Com {num_qubits} qubits existem {2 ** num_qubits} estados computacionais possíveis.</p></div></article>
        <article><b>02</b><div><strong>Observe amplitudes não nulas</strong><p>{len(nonzero)} estados possuem probabilidade maior que o limite numérico.</p></div></article>
        <article><b>03</b><div><strong>Encontre o estado dominante</strong><p>|{escape(dominant)}⟩ possui probabilidade {probability:.2%}.</p></div></article>
        <article><b>04</b><div><strong>Relacione com a medida</strong><p>A medida amostra essas probabilidades; ela não mostra diretamente amplitudes ou fases.</p></div></article>
      </div>
    </section>
    """
    ux.wrap(_style(ux, output_id) + body)


def _counts_conclusion(algorithm: str, dominant: str, expected: str | None) -> str:
    bits = dominant.replace(" ", "")
    if algorithm == "deutsch":
        return "A medida 0 classifica a função como constante." if bits == "0" else "A medida 1 classifica a função como balanceada."
    if algorithm == "deutsch-jozsa":
        return "Todos os bits são 0: a função é constante." if set(bits) <= {"0"} else "Há pelo menos um bit 1: a função é balanceada."
    if algorithm == "bernstein-vazirani":
        return f"A bitstring dominante recupera o segredo s = {bits}."
    if algorithm == "paralelismo":
        return "A bitstring registra somente um ramo por shot; a distribuição reúne muitas repetições do circuito."
    if expected is not None:
        return f"O pico observado deve ser comparado ao resultado esperado {expected}."
    return "O estado dominante é o resultado mais frequente, mas estados menores podem revelar ruído ou amostragem finita."


def _expected_copy(expected: str | None, dominant: str, counts: Mapping[str, int], total: int) -> str:
    if expected is None:
        return "Compare a conclusão com a construção do circuito e repita com mais shots se a distribuição estiver dispersa."
    expected_count = counts.get(expected, 0)
    if dominant == expected:
        return f"O pico coincide com {expected}; ele representa {expected_count / total:.1%} dos shots."
    return f"Esperávamos {expected}, mas o pico foi {dominant}. Verifique ordem dos bits, circuito, transpilações e ruído."


def _count_bars(ordered: Sequence[tuple[str, int]], total: int) -> str:
    maximum = max(value for _, value in ordered)
    return "".join(
        f'<div class="qo-bar"><span>{escape(key)}</span><i><b style="height:{value / maximum * 100:.4f}%"></b></i><strong>{value / total:.1%}</strong></div>'
        for key, value in ordered[:10]
    )


def _call_int(value: Any, method: str) -> int:
    candidate = getattr(value, method, None)
    return int(str(candidate())) if callable(candidate) else 0


def _operations(circuit: Any) -> list[tuple[str, int]]:
    method = getattr(circuit, "count_ops", None)
    if not callable(method):
        return []
    result = method()
    if not isinstance(result, Mapping):
        return []
    return sorted(((str(name), int(str(amount))) for name, amount in result.items()), key=lambda item: (-item[1], item[0]))


def _figure_svg(figure: Any) -> str:
    savefig = getattr(figure, "savefig", None)
    if not callable(savefig):
        raise TypeError("figure must provide a savefig method")
    output = StringIO()
    savefig(output, format="svg", bbox_inches="tight")
    svg = output.getvalue()
    start = svg.find("<svg")
    if start < 0 or "<script" in svg.lower():
        raise ValueError("figure did not produce a safe SVG")
    return svg[start:]


def _style(ux, output_id: str) -> str:
    t = ux.theme
    root = f"#{output_id}"
    return f"""
    <style>
    {root}{{--p:{t['primary']};--a:{t['accent']};--s:{t['surface']};--s2:{t['surface_2']};--b:{t['border']};--tx:{t['text']};--m:{t['muted']};background:var(--s);border:1px solid var(--b);border-radius:12px;color:var(--tx);font-family:{t['font']};margin:12px 0;overflow:hidden;padding:clamp(17px,2.4vw,25px)}}
    {root} *{{box-sizing:border-box}} {root} header{{align-items:start;display:flex;gap:15px;justify-content:space-between}} {root} header small{{color:var(--p);font-size:11px;font-weight:950;letter-spacing:.12em;text-transform:uppercase}} {root} h3{{font-size:clamp(23px,2.5vw,30px);line-height:1.15;margin:5px 0 0}} {root} header>span{{background:var(--s2);border:1px solid var(--b);border-radius:999px;color:var(--a);font-size:12px;font-weight:900;padding:7px 10px}}
    {root} .qo-context{{color:var(--m);font-size:17px;line-height:1.6;margin:15px 0}} {root} .qo-metrics{{display:grid;gap:10px;grid-template-columns:repeat(auto-fit,minmax(125px,1fr));margin:18px 0}} {root} .qo-metrics article{{background:var(--s2);border:1px solid var(--b);border-radius:9px;display:grid;gap:5px;padding:13px}} {root} .qo-metrics small{{color:var(--m);font-size:11px;font-weight:900;text-transform:uppercase}} {root} .qo-metrics b{{font-size:23px;overflow-wrap:anywhere}}
    {root} .qo-bars{{align-items:end;background:color-mix(in srgb,var(--p) 5%,var(--s2));border:1px solid var(--b);border-radius:11px;display:grid;gap:14px;grid-template-columns:repeat(auto-fit,minmax(64px,1fr));margin:20px 0;padding:18px 16px 14px}} {root} .qo-bar{{align-items:end;display:grid;gap:7px;grid-template-areas:"value" "track" "label";grid-template-rows:24px 180px minmax(22px,auto);justify-items:center;min-width:0}} {root} .qo-bar>span{{font-family:Georgia,serif;font-size:13px;font-weight:900;grid-area:label;max-width:100%;overflow-wrap:anywhere;text-align:center}} {root} .qo-bar>i{{align-items:flex-end;align-self:end;background:var(--s);border:1px solid var(--b);border-radius:8px 8px 3px 3px;display:flex;grid-area:track;height:180px;overflow:hidden;width:min(44px,100%)}} {root} .qo-bar>i>b{{background:linear-gradient(0deg,var(--p),var(--a));display:block;min-height:2px;transition:height .3s;width:100%}} {root} .qo-bar>strong{{align-self:end;font-size:13px;font-variant-numeric:tabular-nums;grid-area:value;text-align:center}}
    {root} .qo-steps,{root} .qo-reading{{display:grid;gap:10px;grid-template-columns:1fr 1fr;margin-top:19px}} {root} .qo-steps article,{root} .qo-reading article{{align-items:start;background:var(--s2);border:1px solid var(--b);border-radius:9px;display:grid;gap:11px;grid-template-columns:34px 1fr;padding:13px}} {root} .qo-steps article>b,{root} .qo-reading article>b{{align-items:center;background:var(--p);border-radius:50%;color:white;display:flex;font-size:11px;height:30px;justify-content:center}} {root} .qo-steps strong{{font-size:16px}} {root} .qo-steps p,{root} .qo-reading p{{color:var(--m);font-size:14px;line-height:1.5;margin:5px 0 0}}
    {root} .qo-note{{background:var(--s2);border-left:4px solid var(--a);border-radius:0 8px 8px 0;font-size:14px;line-height:1.5;margin-top:14px;padding:11px 13px}} {root} .qo-operations{{display:flex;flex-wrap:wrap;gap:8px;margin:14px 0}} {root} .qo-operations span{{background:var(--s2);border:1px solid var(--b);border-radius:999px;font-size:13px;padding:7px 10px}} {root} .qo-operations b{{color:var(--p)}}
    {root} .qo-circuit-visual{{background:linear-gradient(145deg,color-mix(in srgb,var(--p) 12%,var(--s2)),var(--s2));border:1px solid var(--b);border-radius:11px;margin:18px 0;overflow:auto;padding:14px}} {root} .qo-circuit-visual svg{{background:white;border-radius:7px;display:block;height:auto;margin:auto;max-width:100%;min-width:520px}}
    @media(max-width:680px){{{root} header{{display:grid}} {root} header>span{{justify-self:start}} {root} .qo-steps,{root} .qo-reading{{grid-template-columns:1fr}} {root} .qo-bars{{gap:9px;grid-template-columns:repeat(auto-fit,minmax(58px,1fr));padding-inline:10px}} {root} .qo-circuit-visual svg{{min-width:460px}}}}
    </style>
    """


__all__ = ["render_circuit_output", "render_counts_output", "render_statevector_output"]
