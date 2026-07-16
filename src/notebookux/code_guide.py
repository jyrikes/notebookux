from collections.abc import Sequence
from html import escape
from itertools import count

_GUIDE_IDS = count(1)


def render_code_guide(
    ux,
    *,
    title: str,
    library: str,
    dsl: str,
    summary: str,
    steps: Sequence[str],
    expected: str,
    flow: Sequence[str] = ("descrição", "CircuitIR", "engine", "resultado"),
    concepts: Sequence[str] = (),
) -> None:
    """Render a compact visual guide immediately before an executable cell."""
    if not steps:
        raise ValueError("steps must contain at least one item")
    guide_id = f"code-guide-{next(_GUIDE_IDS)}"
    step_html = "".join(
        f"<article><b>{index:02d}</b><p>{escape(copy)}</p></article>" for index, copy in enumerate(steps, 1)
    )
    flow_html = "".join(
        f"<span>{escape(item)}</span>{'<i>→</i>' if index < len(flow) - 1 else ''}" for index, item in enumerate(flow)
    )
    concepts_html = "".join(f"<span>{escape(item)}</span>" for item in concepts)
    body = f"""
    <section id="{guide_id}" class="cg-root" role="region" aria-label="{escape(title)}">
      <header>
        <div><small>antes de executar</small><h2>{escape(title)}</h2></div>
        <div class="cg-badges"><span>{escape(library)}</span><span>{escape(dsl)}</span></div>
      </header>
      <p class="cg-summary">{escape(summary)}</p>
      <div class="cg-flow" aria-label="Fluxo da implementação">{flow_html}</div>
      <div class="cg-section-title"><small>leitura guiada</small><strong>O que o código fará</strong></div>
      <div class="cg-steps">{step_html}</div>
      <div class="cg-bottom">
        <div class="cg-expected"><small>resultado esperado</small><strong>{escape(expected)}</strong></div>
        {f'<div class="cg-concepts"><small>conceitos-chave</small><div>{concepts_html}</div></div>' if concepts_html else ""}
      </div>
    </section>
    """
    ux.wrap(_style(ux, guide_id) + body)


def _style(ux, guide_id: str) -> str:
    t = ux.theme
    root = f"#{guide_id}"
    return f"""
    <style>
    {root}{{--p:{t["primary"]};--a:{t["accent"]};--s:{t["surface"]};--s2:{t["surface_2"]};--b:{t["border"]};--tx:{t["text"]};--m:{t["muted"]};background:linear-gradient(145deg,var(--s),color-mix(in srgb,var(--p) 5%,var(--s2)));border:1px solid var(--b);border-radius:12px;color:var(--tx);font-family:{t["font"]};margin:14px 0;overflow:hidden;padding:clamp(18px,2.5vw,28px)}}
    {root} *{{box-sizing:border-box}} {root} header{{align-items:start;display:flex;gap:18px;justify-content:space-between}} {root} header small,{root} .cg-section-title small,{root} .cg-bottom small{{color:var(--p);font-size:10px;font-weight:950;letter-spacing:.12em;text-transform:uppercase}} {root} h2{{font-size:clamp(25px,3vw,34px);line-height:1.15;margin:6px 0 0}}
    {root} .cg-badges{{display:flex;flex-wrap:wrap;gap:7px;justify-content:flex-end}} {root} .cg-badges span{{background:var(--s2);border:1px solid var(--b);border-radius:999px;color:var(--a);font-size:12px;font-weight:900;padding:7px 10px;white-space:nowrap}} {root} .cg-badges span:first-child{{background:var(--p);border-color:var(--p);color:white}}
    {root} .cg-summary{{color:var(--m);font-size:clamp(16px,1.45vw,19px);line-height:1.65;margin:17px 0}} {root} .cg-flow{{align-items:center;background:var(--s2);border:1px solid var(--b);border-radius:10px;display:flex;flex-wrap:wrap;gap:8px;margin:0 0 19px;padding:12px}} {root} .cg-flow span{{background:var(--s);border:1px solid var(--b);border-radius:7px;font-size:13px;font-weight:900;padding:7px 9px}} {root} .cg-flow i{{color:var(--a);font-style:normal;font-weight:950}}
    {root} .cg-section-title{{display:grid;gap:4px;margin-bottom:10px}} {root} .cg-section-title strong{{font-size:20px}} {root} .cg-steps{{display:grid;gap:10px;grid-template-columns:1fr 1fr}} {root} .cg-steps article{{align-items:start;background:var(--s2);border:1px solid var(--b);border-radius:9px;display:grid;gap:11px;grid-template-columns:34px 1fr;padding:13px}} {root} .cg-steps article>b{{align-items:center;background:linear-gradient(135deg,var(--p),var(--a));border-radius:50%;color:white;display:flex;font-size:11px;height:31px;justify-content:center}} {root} .cg-steps p{{font-size:15px;line-height:1.55;margin:3px 0}}
    {root} .cg-bottom{{display:grid;gap:10px;grid-template-columns:minmax(0,1.4fr) minmax(220px,.6fr);margin-top:13px}} {root} .cg-expected,{root} .cg-concepts{{background:color-mix(in srgb,var(--a) 8%,var(--s2));border:1px solid var(--b);border-left:5px solid var(--a);border-radius:9px;padding:14px}} {root} .cg-expected{{display:grid;gap:7px}} {root} .cg-expected strong{{font-size:16px;line-height:1.55}} {root} .cg-concepts>div{{display:flex;flex-wrap:wrap;gap:6px;margin-top:8px}} {root} .cg-concepts span{{background:var(--s);border:1px solid var(--b);border-radius:999px;font-size:11px;font-weight:850;padding:6px 8px}}
    @media(max-width:680px){{{root} header{{display:grid}} {root} .cg-badges{{justify-content:flex-start}} {root} .cg-steps,{root} .cg-bottom{{grid-template-columns:1fr}} {root} .cg-flow i{{transform:rotate(90deg)}}}}
    </style>
    """


__all__ = ["render_code_guide"]
