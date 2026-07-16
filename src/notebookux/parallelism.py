from __future__ import annotations

import json
from html import escape


def render_parallelism_demo(ux) -> None:
    """Render a lightweight, self-contained quantum parallelism lesson."""
    t = ux.theme
    payload = {
        "functions": {
            "f1": {"name": "f1(x)", "outputs": [0, 0]},
            "f2": {"name": "f2(x)", "outputs": [0, 1]},
            "f3": {"name": "f3(x)", "outputs": [1, 0]},
            "f4": {"name": "f4(x)", "outputs": [1, 1]},
        },
        "labels": {
            "constant": "constante",
            "balanced": "balanceada",
            "superposition": "superposicao",
        },
    }
    data_json = json.dumps(payload, ensure_ascii=True).replace("</", "<\\/")

    title = "Paralelismo qu\u00e2ntico e seus limites"
    paragraph_1 = (
        'Parte do poder da computa\u00e7\u00e3o qu\u00e2ntica \u00e9 derivada do "paralelismo qu\u00e2ntico," que \u00e9 '
        "essencialmente a capacidade de realizar opera\u00e7\u00f5es em m\u00faltiplas entradas ao mesmo tempo, j\u00e1 que os "
        "estados de entrada do qubit podem estar em uma superposi\u00e7\u00e3o de m\u00faltiplos estados classicamente "
        "permitidos. NO ENTANTO, embora um circuito qu\u00e2ntico possa ser capaz de avaliar m\u00faltiplos estados de "
        "entrada de uma vez, extrair toda essa informa\u00e7\u00e3o de uma s\u00f3 vez \u00e9 imposs\u00edvel."
    )

    html = f"""
<style>
#paralelismo-lite {{
  --surface:{t["surface"]};
  --surface2:{t["surface_2"]};
  --border:{t["border"]};
  --text:{t["text"]};
  --muted:{t["muted"]};
  --primary:{t["primary"]};
  --accent:{t["accent"]};
  color:var(--text);
  font-family:{t["font"]};
}}
#paralelismo-lite * {{ box-sizing:border-box; }}
#paralelismo-lite .wrap {{
  background:{t["bg"]};
  border:1px solid var(--border);
  border-radius:{t["radius"]};
  box-shadow:{t["shadow"]};
  overflow:hidden;
}}
#paralelismo-lite .hero {{
  background:
    radial-gradient(circle at 88% 12%, color-mix(in srgb, var(--accent) 18%, transparent), transparent 24%),
    linear-gradient(135deg, color-mix(in srgb, var(--primary) 9%, var(--surface)), var(--surface));
  border-bottom:1px solid var(--border);
  display:grid;
  gap:26px;
  grid-template-columns:minmax(0,1.5fr) minmax(240px,.5fr);
  padding:28px;
}}
#paralelismo-lite h2 {{
  color:var(--primary);
  font-size:clamp(27px,3vw,38px);
  line-height:1.08;
  margin:6px 0 18px;
}}
#paralelismo-lite h3 {{
  color:var(--text);
  font-size:clamp(20px,2vw,26px);
  line-height:1.2;
  margin:0;
}}
#paralelismo-lite p {{
  color:var(--text);
  font-size:{t["fs_body"]};
  line-height:1.72;
  margin:0;
}}
#paralelismo-lite .lead {{ max-width:76ch; }}
#paralelismo-lite .eyebrow {{
  color:var(--primary);
  font-size:11px;
  font-weight:950;
  letter-spacing:.12em;
  text-transform:uppercase;
}}
#paralelismo-lite .limit-card {{
  align-self:stretch;
  background:color-mix(in srgb, var(--surface2) 88%, transparent);
  border:1px solid var(--border);
  border-left:4px solid var(--accent);
  border-radius:12px;
  display:flex;
  flex-direction:column;
  justify-content:center;
  min-height:160px;
  padding:20px;
}}
#paralelismo-lite .limit-symbol {{
  color:var(--accent);
  font-family:Georgia, "Times New Roman", serif;
  font-size:34px;
  font-weight:800;
  margin-bottom:12px;
}}
#paralelismo-lite .limit-card strong {{ font-size:16px; line-height:1.35; }}
#paralelismo-lite .limit-card span {{ color:var(--muted); line-height:1.55; margin-top:7px; }}
#paralelismo-lite .chapter {{ padding:30px 28px; }}
#paralelismo-lite .chapter + .chapter {{ border-top:1px solid var(--border); }}
#paralelismo-lite .chapter-head {{
  align-items:center;
  display:flex;
  gap:14px;
  margin-bottom:16px;
}}
#paralelismo-lite .step {{
  align-items:center;
  background:var(--primary);
  border-radius:999px;
  color:white;
  display:inline-flex;
  flex:0 0 38px;
  font-size:12px;
  font-weight:950;
  height:38px;
  justify-content:center;
}}
#paralelismo-lite .copy {{ max-width:88ch; }}
#paralelismo-lite .math {{
  background:var(--surface2);
  border:1px solid var(--border);
  border-radius:6px;
  display:inline-block;
  font-family:Georgia, "Times New Roman", serif;
  font-weight:700;
  line-height:1.2;
  padding:2px 6px;
  white-space:nowrap;
}}
#paralelismo-lite .function-lab {{
  display:grid;
  gap:20px;
  grid-template-columns:minmax(300px,.78fr) minmax(0,1.22fr);
  margin-top:22px;
}}
#paralelismo-lite .function-picker {{
  display:grid;
  gap:10px;
  grid-template-columns:repeat(2,minmax(0,1fr));
}}
#paralelismo-lite button {{
  appearance:none;
  background:var(--surface2);
  border:1px solid var(--border);
  border-radius:10px;
  color:var(--text);
  cursor:pointer;
  font:inherit;
}}
#paralelismo-lite button:focus-visible {{ outline:3px solid var(--accent); outline-offset:2px; }}
#paralelismo-lite .fn-card {{
  min-height:112px;
  padding:13px;
  text-align:left;
  transition:border-color .16s ease, transform .16s ease;
}}
#paralelismo-lite .fn-card:hover {{ transform:translateY(-2px); }}
#paralelismo-lite .fn-card[aria-pressed="true"] {{
  background:color-mix(in srgb, var(--primary) 14%, var(--surface2));
  border-color:var(--primary);
  box-shadow:inset 0 0 0 1px var(--primary);
}}
#paralelismo-lite .fn-name {{ color:var(--primary); display:block; font-size:16px; font-weight:950; margin-bottom:9px; }}
#paralelismo-lite .mini-route {{
  align-items:center;
  color:var(--muted);
  display:grid;
  font-size:12px;
  font-weight:850;
  gap:7px;
  grid-template-columns:24px 1fr 24px;
  margin-top:6px;
}}
#paralelismo-lite .mini-line {{ background:var(--border); height:1px; position:relative; }}
#paralelismo-lite .mini-line::after {{
  border-bottom:3px solid transparent;
  border-left:5px solid var(--primary);
  border-top:3px solid transparent;
  content:"";
  position:absolute;
  right:0;
  top:50%;
  transform:translateY(-50%);
}}
#paralelismo-lite .visual-stage {{
  background:var(--surface);
  border:1px solid var(--border);
  border-radius:12px;
  min-width:0;
  padding:18px;
}}
#paralelismo-lite .stage-top {{
  align-items:center;
  display:flex;
  flex-wrap:wrap;
  gap:10px;
  justify-content:space-between;
  margin-bottom:16px;
}}
#paralelismo-lite .stage-title {{ font-size:14px; font-weight:900; }}
#paralelismo-lite .class-pill {{
  background:var(--surface2);
  border:1px solid var(--border);
  border-radius:999px;
  color:var(--text);
  font-size:12px;
  font-weight:900;
  padding:6px 10px;
}}
#paralelismo-lite .class-pill[data-class="balanced"] {{ border-color:var(--accent); color:var(--accent); }}
#paralelismo-lite .routes {{ display:grid; gap:13px; }}
#paralelismo-lite .route {{
  align-items:center;
  display:grid;
  gap:12px;
  grid-template-columns:58px minmax(80px,1fr) 66px;
}}
#paralelismo-lite .chip {{
  background:var(--surface2);
  border:1px solid var(--border);
  border-radius:8px;
  color:var(--text);
  font-size:13px;
  font-weight:900;
  padding:8px;
  text-align:center;
}}
#paralelismo-lite .wire {{
  background:linear-gradient(90deg,var(--primary),var(--accent));
  height:2px;
  min-width:0;
  position:relative;
}}
#paralelismo-lite .wire::after {{
  border-bottom:5px solid transparent;
  border-left:8px solid var(--accent);
  border-top:5px solid transparent;
  content:"";
  position:absolute;
  right:0;
  top:50%;
  transform:translateY(-50%);
}}
#paralelismo-lite .wire::before {{
  animation:pl-flow 1.9s linear infinite;
  background:var(--accent);
  border-radius:50%;
  box-shadow:0 0 8px var(--accent);
  content:"";
  height:7px;
  left:0;
  position:absolute;
  top:50%;
  transform:translateY(-50%);
  width:7px;
}}
@keyframes pl-flow {{ from {{ left:0; }} to {{ left:calc(100% - 7px); }} }}
#paralelismo-lite .bars {{ display:grid; gap:9px; margin-top:19px; }}
#paralelismo-lite .bar-row {{
  align-items:center;
  color:var(--muted);
  display:grid;
  font-size:12px;
  font-weight:850;
  gap:9px;
  grid-template-columns:38px 1fr 18px;
}}
#paralelismo-lite .bar-track {{
  background:var(--surface2);
  border:1px solid var(--border);
  border-radius:999px;
  height:13px;
  overflow:hidden;
}}
#paralelismo-lite .bar-fill {{
  background:linear-gradient(90deg,var(--primary),var(--accent));
  height:100%;
  transition:width .2s ease;
}}
#paralelismo-lite .gate-lab {{
  display:grid;
  gap:22px;
  grid-template-columns:minmax(260px,.72fr) minmax(0,1.28fr);
  margin-top:22px;
}}
#paralelismo-lite .explain-note {{
  background:var(--surface2);
  border-left:4px solid var(--primary);
  border-radius:0 10px 10px 0;
  color:var(--muted);
  line-height:1.65;
  padding:17px;
}}
#paralelismo-lite .mode-controls {{ display:flex; flex-wrap:wrap; gap:8px; margin-bottom:20px; }}
#paralelismo-lite .mode-button {{ font-size:13px; font-weight:900; min-height:38px; padding:7px 12px; }}
#paralelismo-lite .mode-button[aria-pressed="true"] {{ background:var(--primary); border-color:var(--primary); color:white; }}
#paralelismo-lite .circuit {{
  display:grid;
  gap:18px;
  grid-template-columns:minmax(76px,auto) minmax(70px,1fr) 74px minmax(70px,1fr) minmax(96px,auto);
  overflow:hidden;
  padding:6px 0;
  position:relative;
}}
#paralelismo-lite .circuit-label {{ align-self:center; font-family:Georgia, "Times New Roman", serif; font-weight:800; white-space:nowrap; }}
#paralelismo-lite .circuit-wire {{ align-self:center; background:var(--border); height:2px; }}
#paralelismo-lite .uf-gate {{
  align-items:center;
  align-self:stretch;
  background:linear-gradient(145deg,var(--primary),color-mix(in srgb,var(--primary) 72%,var(--accent)));
  border-radius:10px;
  color:white;
  display:flex;
  font-family:Georgia, "Times New Roman", serif;
  font-size:25px;
  font-weight:900;
  grid-column:3;
  grid-row:1 / span 2;
  justify-content:center;
  min-height:108px;
}}
#paralelismo-lite .formula-card {{
  align-items:center;
  background:color-mix(in srgb,var(--primary) 8%,var(--surface2));
  border:1px solid var(--border);
  border-radius:10px;
  display:flex;
  flex-wrap:wrap;
  font-family:Georgia, "Times New Roman", serif;
  font-size:clamp(16px,2vw,21px);
  font-weight:700;
  gap:8px;
  line-height:1.65;
  margin-top:18px;
  min-height:58px;
  overflow-wrap:anywhere;
  padding:12px 15px;
}}
#paralelismo-lite .state-story {{ display:grid; gap:18px; margin-top:22px; }}
#paralelismo-lite .equation-band {{
  align-items:center;
  background:var(--surface);
  border:1px solid var(--border);
  border-radius:12px;
  display:grid;
  gap:16px;
  grid-template-columns:150px minmax(0,1fr);
  padding:18px;
}}
#paralelismo-lite .equation-caption {{ color:var(--primary); font-size:12px; font-weight:950; letter-spacing:.08em; text-transform:uppercase; }}
#paralelismo-lite .equation {{ font-family:Georgia, "Times New Roman", serif; font-size:clamp(17px,2.2vw,24px); line-height:1.6; overflow-wrap:anywhere; }}
#paralelismo-lite .measure-lab {{
  background:linear-gradient(135deg,color-mix(in srgb,var(--accent) 8%,var(--surface)),var(--surface));
  border:1px solid var(--border);
  border-radius:12px;
  display:grid;
  gap:18px;
  grid-template-columns:minmax(190px,.55fr) minmax(0,1.45fr);
  margin-top:20px;
  padding:18px;
}}
#paralelismo-lite .measure-button {{
  background:var(--primary);
  border-color:var(--primary);
  color:white;
  font-weight:950;
  min-height:48px;
  padding:10px 16px;
  width:100%;
}}
#paralelismo-lite .measure-help {{ color:var(--muted); font-size:12px; line-height:1.5; margin-top:9px; }}
#paralelismo-lite .outcome {{ align-items:center; display:flex; flex-wrap:wrap; gap:10px; min-height:62px; }}
#paralelismo-lite .outcome-empty {{ color:var(--muted); line-height:1.55; }}
#paralelismo-lite .outcome-arrow {{ color:var(--accent); font-size:22px; font-weight:950; }}
#paralelismo-lite .outcome-note {{ color:var(--muted); flex-basis:100%; font-size:12px; }}
@media (max-width:860px) {{
  #paralelismo-lite .hero,
  #paralelismo-lite .function-lab,
  #paralelismo-lite .gate-lab,
  #paralelismo-lite .measure-lab {{ grid-template-columns:1fr; }}
  #paralelismo-lite .limit-card {{ min-height:0; }}
}}
@media (max-width:560px) {{
  #paralelismo-lite .hero,
  #paralelismo-lite .chapter {{ padding:21px 17px; }}
  #paralelismo-lite .function-picker {{ grid-template-columns:1fr; }}
  #paralelismo-lite .equation-band {{ grid-template-columns:1fr; }}
  #paralelismo-lite .circuit {{ gap:7px; grid-template-columns:minmax(52px,auto) minmax(18px,1fr) 58px minmax(18px,1fr) minmax(74px,auto); }}
  #paralelismo-lite .uf-gate {{ min-height:94px; }}
  #paralelismo-lite .circuit-label {{ font-size:12px; }}
}}
@media (prefers-reduced-motion:reduce) {{
  #paralelismo-lite .wire::before {{ animation:none; left:50%; }}
  #paralelismo-lite .fn-card,
  #paralelismo-lite .bar-fill {{ transition:none; }}
}}
</style>
<div id="paralelismo-lite">
  <article class="wrap">
    <header class="hero">
      <div>
        <div class="eyebrow">Conceito fundamental</div>
        <h2>{escape(title)}</h2>
        <p class="lead">{escape(paragraph_1)}</p>
      </div>
      <aside class="limit-card" aria-label="Limite da medi\u00e7\u00e3o">
        <div class="limit-symbol">|0\u27e9 + |1\u27e9 \u2192 ?</div>
        <strong>O circuito evolui com os dois ramos.</strong>
        <span>A medi\u00e7\u00e3o, por\u00e9m, revela apenas um resultado por execu\u00e7\u00e3o.</span>
      </aside>
    </header>

    <section class="chapter">
      <div class="chapter-head"><span class="step">01</span><h3>Quatro fun\u00e7\u00f5es poss\u00edveis</h3></div>
      <p class="copy">Para ver o que quero dizer aqui, vamos dizer que temos um bit, <span class="math">x</span> e alguma fun\u00e7\u00e3o aplicada a esse bit, <span class="math">f(x)</span>. Existem quatro poss\u00edveis fun\u00e7\u00f5es bin\u00e1rias que levam um \u00fanico bit para outro \u00fanico bit:</p>
      <div class="function-lab">
        <div class="function-picker" id="pl-functions" aria-label="Selecione uma fun\u00e7\u00e3o"></div>
        <div class="visual-stage">
          <div class="stage-top">
            <span class="stage-title" id="pl-stage-title">Fluxos de f1(x)</span>
            <span class="class-pill" id="pl-class">classe: constante</span>
          </div>
          <div class="routes">
            <div class="route"><div class="chip">x = 0</div><div class="wire"></div><div class="chip" id="pl-f0">f(0) = 0</div></div>
            <div class="route"><div class="chip">x = 1</div><div class="wire"></div><div class="chip" id="pl-f1">f(1) = 0</div></div>
          </div>
          <div class="bars" aria-label="Gr\u00e1fico das sa\u00eddas da fun\u00e7\u00e3o">
            <div class="bar-row"><span>f(0)</span><div class="bar-track"><div class="bar-fill" id="pl-bar0"></div></div><span id="pl-v0">0</span></div>
            <div class="bar-row"><span>f(1)</span><div class="bar-track"><div class="bar-fill" id="pl-bar1"></div></div><span id="pl-v1">0</span></div>
          </div>
        </div>
      </div>
    </section>

    <section class="chapter">
      <div class="chapter-head"><span class="step">02</span><h3>Uma consulta ao or\u00e1culo</h3></div>
      <p class="copy">Gostar\u00edamos de descobrir qual dessas fun\u00e7\u00f5es (1-4) nossa <span class="math">f(x)</span> \u00e9. Classicamente, precisar\u00edamos executar a fun\u00e7\u00e3o duas vezes \u2014 uma vez para <span class="math">x=0</span>, uma vez para <span class="math">x=1</span>. Mas vamos ver se podemos fazer melhor com um circuito qu\u00e2ntico. Podemos aprender sobre a fun\u00e7\u00e3o com a seguinte porta:</p>
      <div class="gate-lab">
        <div class="explain-note">Alterne a entrada para observar como a mesma porta <strong>U<sub>f</sub></strong> trata um estado definido ou os dois ramos da superposi\u00e7\u00e3o.</div>
        <div class="visual-stage">
          <div class="mode-controls" id="pl-modes">
            <button class="mode-button" type="button" data-mode="0">x = 0</button>
            <button class="mode-button" type="button" data-mode="1">x = 1</button>
            <button class="mode-button" type="button" data-mode="superposition">superposi\u00e7\u00e3o</button>
          </div>
          <div class="circuit" aria-label="Diagrama da porta U f">
            <div class="circuit-label" id="pl-input-x">|x\u27e9</div><div class="circuit-wire"></div><div class="uf-gate">U<sub>f</sub></div><div class="circuit-wire"></div><div class="circuit-label">|x\u27e9</div>
            <div class="circuit-label">|y\u27e9 = |0\u27e9</div><div class="circuit-wire"></div><div class="circuit-wire"></div><div class="circuit-label" id="pl-output-y">|f(x)\u27e9</div>
          </div>
          <div class="formula-card" id="pl-formula" aria-live="polite"></div>
        </div>
      </div>
    </section>

    <section class="chapter">
      <div class="chapter-head"><span class="step">03</span><h3>O estado carrega as duas respostas</h3></div>
      <div class="state-story">
        <p class="copy">Aqui, a porta <span class="math">U<sub>f</sub></span> calcula <span class="math">f(x)</span>, onde <span class="math">x</span> \u00e9 o estado do qubit 0, e aplica isso ao qubit 1. Ent\u00e3o, o estado resultante, <span class="math">|x\u27e9|y \u2295 f(x)\u27e9</span>, simplesmente se torna <span class="math">|x\u27e9|f(x)\u27e9</span> quando <span class="math">|y\u27e9 = |0\u27e9</span>.</p>
        <div class="equation-band">
          <span class="equation-caption">A\u00e7\u00e3o da porta</span>
          <span class="equation">|x\u27e9|y \u2295 f(x)\u27e9 &nbsp;\u2192&nbsp; |x\u27e9|f(x)\u27e9</span>
        </div>
        <p class="copy">Isso cont\u00e9m toda a informa\u00e7\u00e3o que precisamos para conhecer a fun\u00e7\u00e3o <span class="math">f(x)</span>: o qubit 0 nos diz qual \u00e9 <span class="math">x</span>, e o qubit 1 nos diz qual \u00e9 <span class="math">f(x)</span>.</p>
        <div class="equation-band">
          <span class="equation-caption">Entrada em superposi\u00e7\u00e3o</span>
          <span class="equation">|x\u27e9 = 1/\u221a2 (|0\u27e9 + |1\u27e9)</span>
        </div>
        <p class="copy">Ent\u00e3o, se inicializarmos <span class="math">|x\u27e9 = 1/\u221a2 (|0\u27e9+|1\u27e9)</span>, ent\u00e3o o estado final de ambos os qubits ser\u00e1: <span class="math">|y\u27e9|x\u27e9 = 1/\u221a2 (|f(0)\u27e9|0\u27e9+|f(1)\u27e9|1\u27e9)</span>. Mas como acessamos essa informa\u00e7\u00e3o?</p>
      </div>
    </section>

    <section class="chapter">
      <div class="chapter-head"><span class="step">04</span><h3>Medir escolhe um dos ramos</h3></div>
      <p class="copy">O estado qu\u00e2ntico conserva os dois pares durante o c\u00e1lculo. Use a medi\u00e7\u00e3o abaixo para observar por que uma execu\u00e7\u00e3o n\u00e3o entrega as duas respostas ao mesmo tempo.</p>
      <div class="measure-lab">
        <div>
          <button class="measure-button" id="pl-measure" type="button">Medir uma vez</button>
          <div class="measure-help">Cada clique simula uma nova prepara\u00e7\u00e3o e medi\u00e7\u00e3o do estado.</div>
        </div>
        <div class="outcome" id="pl-outcome" aria-live="polite">
          <span class="outcome-empty">Nenhuma medi\u00e7\u00e3o realizada. Os dois ramos ainda est\u00e3o representados no estado.</span>
        </div>
      </div>
    </section>
  </article>
</div>
<script>
(() => {{
  const data = {data_json};
  const root = document.getElementById("paralelismo-lite");
  if (!root) return;

  let selectedFunction = "f1";
  let selectedInput = "superposition";
  const functionBox = root.querySelector("#pl-functions");
  const modeBox = root.querySelector("#pl-modes");
  const classElement = root.querySelector("#pl-class");
  const outcomeElement = root.querySelector("#pl-outcome");

  functionBox.innerHTML = Object.entries(data.functions).map(([key, item]) => `
    <button class="fn-card" type="button" data-fn="${{key}}" aria-pressed="false">
      <span class="fn-name">${{item.name}}</span>
      <span class="mini-route"><span>0</span><span class="mini-line"></span><span>${{item.outputs[0]}}</span></span>
      <span class="mini-route"><span>1</span><span class="mini-line"></span><span>${{item.outputs[1]}}</span></span>
    </button>
  `).join("");

  function render(resetOutcome = true) {{
    const item = data.functions[selectedFunction];
    const [y0, y1] = item.outputs;
    const isBalanced = y0 !== y1;
    const className = isBalanced ? data.labels.balanced : data.labels.constant;

    root.querySelectorAll("[data-fn]").forEach((button) => {{
      button.setAttribute("aria-pressed", button.dataset.fn === selectedFunction ? "true" : "false");
    }});
    root.querySelectorAll("[data-mode]").forEach((button) => {{
      button.setAttribute("aria-pressed", button.dataset.mode === selectedInput ? "true" : "false");
    }});

    root.querySelector("#pl-stage-title").textContent = `Fluxos de ${{item.name}}`;
    classElement.textContent = `classe: ${{className}}`;
    classElement.dataset.class = isBalanced ? "balanced" : "constant";
    root.querySelector("#pl-f0").textContent = `f(0) = ${{y0}}`;
    root.querySelector("#pl-f1").textContent = `f(1) = ${{y1}}`;
    root.querySelector("#pl-bar0").style.width = y0 ? "100%" : "0";
    root.querySelector("#pl-bar1").style.width = y1 ? "100%" : "0";
    root.querySelector("#pl-v0").textContent = String(y0);
    root.querySelector("#pl-v1").textContent = String(y1);

    const inputX = root.querySelector("#pl-input-x");
    const outputY = root.querySelector("#pl-output-y");
    const formula = root.querySelector("#pl-formula");
    if (selectedInput === "superposition") {{
      inputX.textContent = "1/\u221a2 (|0\u27e9 + |1\u27e9)";
      outputY.textContent = "dois ramos";
      formula.textContent = `1/\u221a2 (|${{y0}}\u27e9|0\u27e9 + |${{y1}}\u27e9|1\u27e9)`;
    }} else {{
      const x = Number(selectedInput);
      const y = item.outputs[x];
      inputX.textContent = `|${{x}}\u27e9`;
      outputY.textContent = `|${{y}}\u27e9`;
      formula.textContent = `|${{x}}\u27e9|0 \u2295 f(${{x}})\u27e9 = |${{x}}\u27e9|${{y}}\u27e9`;
    }}
    if (resetOutcome) {{
      outcomeElement.innerHTML = '<span class="outcome-empty">A fun\u00e7\u00e3o mudou. Me\u00e7a o novo estado para revelar um ramo.</span>';
    }}
  }}

  functionBox.addEventListener("click", (event) => {{
    const button = event.target.closest("[data-fn]");
    if (!button) return;
    selectedFunction = button.dataset.fn;
    render();
  }});
  modeBox.addEventListener("click", (event) => {{
    const button = event.target.closest("[data-mode]");
    if (!button) return;
    selectedInput = button.dataset.mode;
    render();
  }});
  root.querySelector("#pl-measure").addEventListener("click", () => {{
    const item = data.functions[selectedFunction];
    const x = Math.random() < 0.5 ? 0 : 1;
    const y = item.outputs[x];
    outcomeElement.innerHTML = `
      <span class="chip">x = ${{x}}</span>
      <span class="outcome-arrow">\u2192</span>
      <span class="chip">f(${{x}}) = ${{y}}</span>
      <span class="outcome-note">A outra sa\u00edda n\u00e3o foi revelada nesta execu\u00e7\u00e3o.</span>
    `;
  }});

  render(false);
}})();
</script>
"""
    ux.wrap(html)
