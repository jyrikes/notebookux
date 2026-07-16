from __future__ import annotations

import json
from html import escape


def render_parallelism_demo(ux) -> None:
    """Render quantum parallelism as a lightweight, interactive UX module."""
    t = ux.theme
    payload = {
        "functions": {
            "f1": {"name": "f1(x)", "outputs": [0, 0]},
            "f2": {"name": "f2(x)", "outputs": [0, 1]},
            "f3": {"name": "f3(x)", "outputs": [1, 0]},
            "f4": {"name": "f4(x)", "outputs": [1, 1]},
        },
        "labels": {"constant": "constante", "balanced": "balanceada"},
    }
    data_json = json.dumps(payload, ensure_ascii=True).replace("</", "<\\/")

    paragraph_1 = (
        'Parte do poder da computa\u00e7\u00e3o qu\u00e2ntica \u00e9 derivada do "paralelismo qu\u00e2ntico," que \u00e9 '
        "essencialmente a capacidade de realizar opera\u00e7\u00f5es em m\u00faltiplas entradas ao mesmo tempo, j\u00e1 que os "
        "estados de entrada do qubit podem estar em uma superposi\u00e7\u00e3o de m\u00faltiplos estados classicamente "
        "permitidos. NO ENTANTO, embora um circuito qu\u00e2ntico possa ser capaz de avaliar m\u00faltiplos estados de "
        "entrada de uma vez, extrair toda essa informa\u00e7\u00e3o de uma s\u00f3 vez \u00e9 imposs\u00edvel."
    )

    function_cards = "".join(
        f"""
        <button class="pl-fn-card" type="button" data-pl-function="{key}" aria-pressed="false">
          <span class="pl-fn-name">{item['name']}</span>
          <span class="pl-mini-route"><span>0</span><span class="pl-mini-line"></span><span>{item['outputs'][0]}</span></span>
          <span class="pl-mini-route"><span>1</span><span class="pl-mini-line"></span><span>{item['outputs'][1]}</span></span>
        </button>
        """
        for key, item in payload["functions"].items()
    )

    screens = [
        ux.screen(
            "Ideia central",
            f"""
            <div class="pl-intro-grid">
              <p class="pl-lead">{escape(paragraph_1)}</p>
              <aside class="pl-limit-card" aria-label="Limite da medi\u00e7\u00e3o">
                <div class="pl-limit-symbol">|0\u27e9 + |1\u27e9 \u2192 ?</div>
                <strong>O circuito evolui com os dois ramos.</strong>
                <span>A medi\u00e7\u00e3o, por\u00e9m, revela apenas um resultado por execu\u00e7\u00e3o.</span>
              </aside>
            </div>
            <div class="pl-concept-flow" aria-label="Fluxo conceitual do paralelismo">
              <span>superposi\u00e7\u00e3o</span><i></i><span>U<sub>f</sub></span><i></i><span>medi\u00e7\u00e3o</span>
            </div>
            """,
        ),
        ux.screen(
            "Quatro fun\u00e7\u00f5es poss\u00edveis",
            f"""
            <p>Para ver o que quero dizer aqui, vamos dizer que temos um bit, <span class="pl-math">x</span> e alguma fun\u00e7\u00e3o aplicada a esse bit, <span class="pl-math">f(x)</span>. Existem quatro poss\u00edveis fun\u00e7\u00f5es bin\u00e1rias que levam um \u00fanico bit para outro \u00fanico bit:</p>
            <div class="pl-function-lab">
              <div class="pl-function-picker" aria-label="Selecione uma fun\u00e7\u00e3o">{function_cards}</div>
              <div class="pl-stage">
                <div class="pl-stage-top">
                  <strong id="pl-stage-title">Fluxos de f1(x)</strong>
                  <span class="pl-class-pill" id="pl-class">classe: constante</span>
                </div>
                <div class="pl-routes">
                  <div class="pl-route"><span class="pl-chip">x = 0</span><i class="pl-wire"></i><span class="pl-chip" id="pl-f0">f(0) = 0</span></div>
                  <div class="pl-route"><span class="pl-chip">x = 1</span><i class="pl-wire"></i><span class="pl-chip" id="pl-f1">f(1) = 0</span></div>
                </div>
                <div class="pl-bars" aria-label="Gr\u00e1fico das sa\u00eddas">
                  <div class="pl-bar-row"><span>f(0)</span><i><b id="pl-bar0"></b></i><span id="pl-v0">0</span></div>
                  <div class="pl-bar-row"><span>f(1)</span><i><b id="pl-bar1"></b></i><span id="pl-v1">0</span></div>
                </div>
              </div>
            </div>
            """,
        ),
        ux.screen(
            "Uma consulta ao or\u00e1culo",
            """
            <p>Gostar\u00edamos de descobrir qual dessas fun\u00e7\u00f5es (1-4) nossa <span class="pl-math">f(x)</span> \u00e9. Classicamente, precisar\u00edamos executar a fun\u00e7\u00e3o duas vezes &mdash; uma vez para <span class="pl-math">x=0</span>, uma vez para <span class="pl-math">x=1</span>. Mas vamos ver se podemos fazer melhor com um circuito qu\u00e2ntico. Podemos aprender sobre a fun\u00e7\u00e3o com a seguinte porta:</p>
            <div class="pl-gate-lab">
              <div class="pl-note">Alterne a entrada para observar como a mesma porta <strong>U<sub>f</sub></strong> trata um estado definido ou os dois ramos da superposi\u00e7\u00e3o.</div>
              <div class="pl-stage">
                <div class="pl-mode-controls">
                  <button type="button" data-pl-mode="0">x = 0</button>
                  <button type="button" data-pl-mode="1">x = 1</button>
                  <button type="button" data-pl-mode="superposition">superposi\u00e7\u00e3o</button>
                </div>
                <div class="pl-circuit" aria-label="Diagrama da porta U f">
                  <strong id="pl-input-x">|x\u27e9</strong><i></i><b>U<sub>f</sub></b><i></i><strong>|x\u27e9</strong>
                  <strong>|y\u27e9 = |0\u27e9</strong><i></i><i></i><strong id="pl-output-y">|f(x)\u27e9</strong>
                </div>
                <div class="pl-formula" id="pl-formula" aria-live="polite"></div>
              </div>
            </div>
            """,
        ),
        ux.screen(
            "O estado carrega as duas respostas",
            """
            <div class="pl-state-story">
              <p>Aqui, a porta <span class="pl-math">U<sub>f</sub></span> calcula <span class="pl-math">f(x)</span>, onde <span class="pl-math">x</span> \u00e9 o estado do qubit 0, e aplica isso ao qubit 1. Ent\u00e3o, o estado resultante, <span class="pl-math">|x\u27e9|y \u2295 f(x)\u27e9</span>, simplesmente se torna <span class="pl-math">|x\u27e9|f(x)\u27e9</span> quando <span class="pl-math">|y\u27e9 = |0\u27e9</span>.</p>
              <div class="pl-equation-band"><span>A\u00e7\u00e3o da porta</span><strong>|x\u27e9|y \u2295 f(x)\u27e9 &nbsp;\u2192&nbsp; |x\u27e9|f(x)\u27e9</strong></div>
              <p>Isso cont\u00e9m toda a informa\u00e7\u00e3o que precisamos para conhecer a fun\u00e7\u00e3o <span class="pl-math">f(x)</span>: o qubit 0 nos diz qual \u00e9 <span class="pl-math">x</span>, e o qubit 1 nos diz qual \u00e9 <span class="pl-math">f(x)</span>.</p>
              <div class="pl-equation-band"><span>Entrada em superposi\u00e7\u00e3o</span><strong>|x\u27e9 = 1/\u221a2 (|0\u27e9 + |1\u27e9)</strong></div>
              <p>Ent\u00e3o, se inicializarmos <span class="pl-math">|x\u27e9 = 1/\u221a2 (|0\u27e9+|1\u27e9)</span>, ent\u00e3o o estado final de ambos os qubits ser\u00e1: <span class="pl-math">|y\u27e9|x\u27e9 = 1/\u221a2 (|f(0)\u27e9|0\u27e9+|f(1)\u27e9|1\u27e9)</span>. Mas como acessamos essa informa\u00e7\u00e3o?</p>
            </div>
            """,
        ),
        ux.screen(
            "O limite aparece na medi\u00e7\u00e3o",
            """
            <div class="pl-measure-intro">
              <div class="pl-measure-icon">|\u03c8\u27e9 \u2192 |x, f(x)\u27e9</div>
              <p>O estado qu\u00e2ntico conserva os dois pares durante o c\u00e1lculo. Use a medi\u00e7\u00e3o abaixo para observar por que uma execu\u00e7\u00e3o n\u00e3o entrega as duas respostas ao mesmo tempo.</p>
            </div>
            <div class="pl-measure-lab">
              <div>
                <button id="pl-measure" type="button">Medir uma vez</button>
                <small>Cada clique simula uma nova prepara\u00e7\u00e3o e medi\u00e7\u00e3o do estado.</small>
              </div>
              <div class="pl-outcome" id="pl-outcome" aria-live="polite">
                <span>Nenhuma medi\u00e7\u00e3o realizada. Os dois ramos ainda est\u00e3o representados no estado.</span>
              </div>
            </div>
            <div class="pl-takeaway"><strong>Limite:</strong> o paralelismo est\u00e1 na evolu\u00e7\u00e3o do estado, n\u00e3o na leitura simult\u00e2nea de todas as sa\u00eddas.</div>
            """,
        ),
    ]

    module_html = ux.module_html(
        "Paralelismo qu\u00e2ntico e seus limites",
        screens,
        module_id="paralelismo-lite",
    )

    css = f"""
    <style>
    #paralelismo-lite {{
      --pl-surface:{t['surface']};
      --pl-surface2:{t['surface_2']};
      --pl-border:{t['border']};
      --pl-text:{t['text']};
      --pl-muted:{t['muted']};
      --pl-primary:{t['primary']};
      --pl-accent:{t['accent']};
      overflow:hidden;
    }}
    #paralelismo-lite * {{ box-sizing:border-box; }}
    #paralelismo-lite > div:nth-child(2) {{ font-size:clamp(32px,4vw,44px) !important; }}
    #paralelismo-lite_content {{ min-height:0; padding:clamp(18px,2.4vw,28px) !important; }}
    #paralelismo-lite_content > div:first-child {{ font-size:clamp(27px,3vw,34px) !important; margin-bottom:22px !important; }}
    #paralelismo-lite_content p {{ color:var(--pl-text); font-size:clamp(18px,1.65vw,21px); line-height:1.76; margin:0; }}
    #paralelismo-lite_prev,
    #paralelismo-lite_next {{ font-size:17px !important; min-height:46px; padding:11px 22px !important; }}
    #paralelismo-lite button:focus-visible {{ outline:3px solid var(--pl-accent); outline-offset:2px; }}
    #paralelismo-lite .pl-intro-grid {{ display:grid; gap:26px; grid-template-columns:minmax(0,1.35fr) minmax(250px,.65fr); }}
    #paralelismo-lite .pl-limit-card {{
      background:linear-gradient(145deg,var(--pl-surface2),color-mix(in srgb,var(--pl-accent) 7%,var(--pl-surface2)));
      border:1px solid var(--pl-border);
      border-left:5px solid var(--pl-accent);
      border-radius:12px;
      display:flex;
      flex-direction:column;
      justify-content:center;
      min-height:220px;
      padding:24px;
    }}
    #paralelismo-lite .pl-limit-symbol {{ color:var(--pl-accent); font-family:Georgia,serif; font-size:36px; font-weight:800; margin-bottom:17px; }}
    #paralelismo-lite .pl-limit-card strong {{ font-size:19px; line-height:1.4; }}
    #paralelismo-lite .pl-limit-card span {{ color:var(--pl-muted); font-size:17px; line-height:1.6; margin-top:9px; }}
    #paralelismo-lite .pl-concept-flow {{ align-items:center; display:grid; gap:12px; grid-template-columns:auto 1fr auto 1fr auto; margin-top:28px; }}
    #paralelismo-lite .pl-concept-flow span {{ background:var(--pl-surface2); border:1px solid var(--pl-border); border-radius:999px; font-size:16px; font-weight:900; padding:10px 15px; text-align:center; }}
    #paralelismo-lite .pl-concept-flow i {{ background:linear-gradient(90deg,var(--pl-primary),var(--pl-accent)); height:3px; }}
    #paralelismo-lite .pl-math {{ background:var(--pl-surface2); border:1px solid var(--pl-border); border-radius:6px; display:inline-block; font-family:Georgia,serif; font-size:1.05em; font-weight:700; line-height:1.2; padding:2px 7px; white-space:nowrap; }}
    #paralelismo-lite .pl-function-lab {{ display:grid; gap:22px; grid-template-columns:minmax(310px,.78fr) minmax(0,1.22fr); margin-top:25px; }}
    #paralelismo-lite .pl-function-picker {{ display:grid; gap:11px; grid-template-columns:repeat(2,minmax(0,1fr)); }}
    #paralelismo-lite .pl-fn-card {{ background:var(--pl-surface2); border:1px solid var(--pl-border); border-radius:11px; color:var(--pl-text); cursor:pointer; min-height:126px; padding:15px; text-align:left; }}
    #paralelismo-lite .pl-fn-card[aria-pressed="true"] {{ border:2px solid var(--pl-primary); background:color-mix(in srgb,var(--pl-primary) 13%,var(--pl-surface2)); }}
    #paralelismo-lite .pl-fn-name {{ color:var(--pl-primary); display:block; font-size:19px; font-weight:950; margin-bottom:10px; }}
    #paralelismo-lite .pl-mini-route {{ align-items:center; color:var(--pl-muted); display:grid; font-size:15px; font-weight:850; gap:8px; grid-template-columns:25px 1fr 25px; margin-top:7px; }}
    #paralelismo-lite .pl-mini-line {{ background:var(--pl-border); height:1px; position:relative; }}
    #paralelismo-lite .pl-mini-line::after {{ border:4px solid transparent; border-left-color:var(--pl-primary); content:""; position:absolute; right:-4px; top:-4px; }}
    #paralelismo-lite .pl-stage {{ background:var(--pl-surface); border:1px solid var(--pl-border); border-radius:12px; min-width:0; padding:20px; }}
    #paralelismo-lite .pl-stage-top {{ align-items:center; display:flex; flex-wrap:wrap; gap:12px; justify-content:space-between; margin-bottom:19px; }}
    #paralelismo-lite .pl-stage-top strong {{ font-size:18px; }}
    #paralelismo-lite .pl-class-pill {{ background:var(--pl-surface2); border:1px solid var(--pl-border); border-radius:999px; font-size:14px; font-weight:900; padding:7px 11px; }}
    #paralelismo-lite .pl-class-pill[data-class="balanced"] {{ border-color:var(--pl-accent); color:var(--pl-accent); }}
    #paralelismo-lite .pl-routes {{ display:grid; gap:14px; }}
    #paralelismo-lite .pl-route {{ align-items:center; display:grid; gap:12px; grid-template-columns:72px minmax(70px,1fr) 92px; }}
    #paralelismo-lite .pl-chip {{ background:var(--pl-surface2); border:1px solid var(--pl-border); border-radius:8px; font-size:15px; font-weight:900; padding:9px; text-align:center; }}
    #paralelismo-lite .pl-wire {{ background:linear-gradient(90deg,var(--pl-primary),var(--pl-accent)); height:3px; position:relative; }}
    #paralelismo-lite .pl-wire::before {{ animation:pl-flow 1.8s linear infinite; background:var(--pl-accent); border-radius:50%; box-shadow:0 0 8px var(--pl-accent); content:""; height:8px; left:0; position:absolute; top:-3px; width:8px; }}
    #paralelismo-lite .pl-wire::after {{ border:6px solid transparent; border-left-color:var(--pl-accent); content:""; position:absolute; right:-6px; top:-5px; }}
    @keyframes pl-flow {{ from {{ left:0; }} to {{ left:calc(100% - 8px); }} }}
    #paralelismo-lite .pl-bars {{ display:grid; gap:10px; margin-top:20px; }}
    #paralelismo-lite .pl-bar-row {{ align-items:center; color:var(--pl-muted); display:grid; font-size:14px; font-weight:850; gap:9px; grid-template-columns:42px 1fr 20px; }}
    #paralelismo-lite .pl-bar-row > i {{ background:var(--pl-surface2); border:1px solid var(--pl-border); border-radius:999px; height:15px; overflow:hidden; }}
    #paralelismo-lite .pl-bar-row b {{ background:linear-gradient(90deg,var(--pl-primary),var(--pl-accent)); display:block; height:100%; transition:width .2s; }}
    #paralelismo-lite .pl-gate-lab {{ display:grid; gap:22px; grid-template-columns:minmax(250px,.62fr) minmax(0,1.38fr); margin-top:26px; }}
    #paralelismo-lite .pl-note {{ background:var(--pl-surface2); border-left:5px solid var(--pl-primary); border-radius:0 10px 10px 0; color:var(--pl-muted); font-size:18px; line-height:1.7; padding:20px; }}
    #paralelismo-lite .pl-mode-controls {{ display:flex; flex-wrap:wrap; gap:9px; margin-bottom:22px; }}
    #paralelismo-lite .pl-mode-controls button {{ background:var(--pl-surface2); border:1px solid var(--pl-border); border-radius:9px; color:var(--pl-text); cursor:pointer; font-size:16px; font-weight:900; min-height:42px; padding:8px 13px; }}
    #paralelismo-lite .pl-mode-controls button[aria-pressed="true"] {{ background:var(--pl-primary); border-color:var(--pl-primary); color:white; }}
    #paralelismo-lite .pl-circuit {{ display:grid; gap:17px; grid-template-columns:minmax(86px,auto) minmax(35px,1fr) 78px minmax(35px,1fr) minmax(96px,auto); overflow:hidden; padding:5px 0; }}
    #paralelismo-lite .pl-circuit strong {{ align-self:center; font-family:Georgia,serif; font-size:17px; white-space:nowrap; }}
    #paralelismo-lite .pl-circuit > i {{ align-self:center; background:var(--pl-border); height:2px; }}
    #paralelismo-lite .pl-circuit > b {{ align-items:center; background:linear-gradient(145deg,var(--pl-primary),var(--pl-accent)); border-radius:10px; color:white; display:flex; font-family:Georgia,serif; font-size:27px; grid-column:3; grid-row:1 / span 2; justify-content:center; min-height:112px; }}
    #paralelismo-lite .pl-formula {{ background:color-mix(in srgb,var(--pl-primary) 8%,var(--pl-surface2)); border:1px solid var(--pl-border); border-radius:10px; font-family:Georgia,serif; font-size:clamp(20px,2.3vw,27px); font-weight:700; line-height:1.6; margin-top:20px; overflow-wrap:anywhere; padding:14px 17px; }}
    #paralelismo-lite .pl-state-story {{ display:grid; gap:21px; }}
    #paralelismo-lite .pl-equation-band {{ align-items:center; background:var(--pl-surface2); border:1px solid var(--pl-border); border-radius:11px; display:grid; gap:18px; grid-template-columns:170px minmax(0,1fr); padding:20px; }}
    #paralelismo-lite .pl-equation-band span {{ color:var(--pl-primary); font-size:14px; font-weight:950; letter-spacing:.08em; text-transform:uppercase; }}
    #paralelismo-lite .pl-equation-band strong {{ font-family:Georgia,serif; font-size:clamp(21px,2.5vw,29px); line-height:1.55; overflow-wrap:anywhere; }}
    #paralelismo-lite .pl-measure-intro {{ align-items:center; display:grid; gap:22px; grid-template-columns:minmax(210px,.45fr) minmax(0,1.55fr); }}
    #paralelismo-lite .pl-measure-icon {{ background:var(--pl-surface2); border:1px solid var(--pl-border); border-left:5px solid var(--pl-accent); border-radius:11px; color:var(--pl-accent); font-family:Georgia,serif; font-size:27px; font-weight:800; padding:24px; text-align:center; }}
    #paralelismo-lite .pl-measure-lab {{ background:var(--pl-surface); border:1px solid var(--pl-border); border-radius:12px; display:grid; gap:20px; grid-template-columns:minmax(210px,.55fr) minmax(0,1.45fr); margin-top:26px; padding:22px; }}
    #paralelismo-lite #pl-measure {{ background:var(--pl-primary); border:1px solid var(--pl-primary); border-radius:9px; color:white; cursor:pointer; font-size:18px; font-weight:950; min-height:50px; padding:10px 16px; width:100%; }}
    #paralelismo-lite .pl-measure-lab small {{ color:var(--pl-muted); display:block; font-size:14px; line-height:1.55; margin-top:10px; }}
    #paralelismo-lite .pl-outcome {{ align-content:center; align-items:center; display:flex; flex-wrap:wrap; font-size:18px; gap:11px; min-height:76px; }}
    #paralelismo-lite .pl-outcome small {{ flex-basis:100%; margin:0; }}
    #paralelismo-lite .pl-takeaway {{ background:color-mix(in srgb,var(--pl-accent) 9%,var(--pl-surface2)); border:1px solid var(--pl-border); border-radius:11px; font-size:18px; line-height:1.65; margin-top:22px; padding:17px 20px; }}
    @media (max-width:860px) {{
      #paralelismo-lite .pl-intro-grid,
      #paralelismo-lite .pl-function-lab,
      #paralelismo-lite .pl-gate-lab,
      #paralelismo-lite .pl-measure-intro,
      #paralelismo-lite .pl-measure-lab {{ grid-template-columns:1fr; }}
      #paralelismo-lite_content {{ min-height:0; }}
    }}
    @media (max-width:560px) {{
      #paralelismo-lite .pl-function-picker {{ grid-template-columns:1fr; }}
      #paralelismo-lite .pl-concept-flow {{ grid-template-columns:1fr; }}
      #paralelismo-lite .pl-concept-flow i {{ height:22px; justify-self:center; width:3px; }}
      #paralelismo-lite .pl-equation-band {{ grid-template-columns:1fr; }}
      #paralelismo-lite .pl-circuit {{ gap:6px; grid-template-columns:minmax(55px,auto) minmax(15px,1fr) 58px minmax(15px,1fr) minmax(70px,auto); }}
      #paralelismo-lite .pl-circuit strong {{ font-size:12px; }}
      #paralelismo-lite .pl-circuit > b {{ min-height:94px; }}
    }}
    @media (prefers-reduced-motion:reduce) {{ #paralelismo-lite .pl-wire::before {{ animation:none; left:50%; }} }}
    </style>
    """

    script = f"""
    <script>
    (() => {{
      const data = {data_json};
      const root = document.getElementById("paralelismo-lite");
      const content = document.getElementById("paralelismo-lite_content");
      if (!root || !content) return;
      let selectedFunction = "f1";
      let selectedInput = "superposition";

      function renderFunction() {{
        const item = data.functions[selectedFunction];
        const [y0, y1] = item.outputs;
        const balanced = y0 !== y1;
        root.querySelectorAll("[data-pl-function]").forEach((button) => {{
          button.setAttribute("aria-pressed", button.dataset.plFunction === selectedFunction ? "true" : "false");
        }});
        const title = root.querySelector("#pl-stage-title");
        if (!title) return;
        title.textContent = `Fluxos de ${{item.name}}`;
        const classElement = root.querySelector("#pl-class");
        classElement.textContent = `classe: ${{balanced ? data.labels.balanced : data.labels.constant}}`;
        classElement.dataset.class = balanced ? "balanced" : "constant";
        root.querySelector("#pl-f0").textContent = `f(0) = ${{y0}}`;
        root.querySelector("#pl-f1").textContent = `f(1) = ${{y1}}`;
        root.querySelector("#pl-bar0").style.width = y0 ? "100%" : "0";
        root.querySelector("#pl-bar1").style.width = y1 ? "100%" : "0";
        root.querySelector("#pl-v0").textContent = String(y0);
        root.querySelector("#pl-v1").textContent = String(y1);
      }}

      function renderGate() {{
        const formula = root.querySelector("#pl-formula");
        if (!formula) return;
        const item = data.functions[selectedFunction];
        const [y0, y1] = item.outputs;
        root.querySelectorAll("[data-pl-mode]").forEach((button) => {{
          button.setAttribute("aria-pressed", button.dataset.plMode === selectedInput ? "true" : "false");
        }});
        const input = root.querySelector("#pl-input-x");
        const output = root.querySelector("#pl-output-y");
        if (selectedInput === "superposition") {{
          input.textContent = "1/\u221a2 (|0\u27e9 + |1\u27e9)";
          output.textContent = "dois ramos";
          formula.textContent = `1/\u221a2 (|${{y0}}\u27e9|0\u27e9 + |${{y1}}\u27e9|1\u27e9)`;
        }} else {{
          const x = Number(selectedInput);
          const y = item.outputs[x];
          input.textContent = `|${{x}}\u27e9`;
          output.textContent = `|${{y}}\u27e9`;
          formula.textContent = `|${{x}}\u27e9|0 \u2295 f(${{x}})\u27e9 = |${{x}}\u27e9|${{y}}\u27e9`;
        }}
      }}

      function hydrate() {{
        renderFunction();
        renderGate();
      }}

      root.addEventListener("click", (event) => {{
        const functionButton = event.target.closest("[data-pl-function]");
        if (functionButton) {{
          selectedFunction = functionButton.dataset.plFunction;
          renderFunction();
          return;
        }}
        const modeButton = event.target.closest("[data-pl-mode]");
        if (modeButton) {{
          selectedInput = modeButton.dataset.plMode;
          renderGate();
          return;
        }}
        if (event.target.closest("#pl-measure")) {{
          const item = data.functions[selectedFunction];
          const x = Math.random() < 0.5 ? 0 : 1;
          const y = item.outputs[x];
          root.querySelector("#pl-outcome").innerHTML = `
            <span class="pl-chip">x = ${{x}}</span><strong>\u2192</strong><span class="pl-chip">f(${{x}}) = ${{y}}</span>
            <small>A outra sa\u00edda n\u00e3o foi revelada nesta execu\u00e7\u00e3o.</small>
          `;
        }}
      }});

      new MutationObserver(hydrate).observe(content, {{childList:true}});
      hydrate();
    }})();
    </script>
    """
    ux.wrap(css + module_html + script)
