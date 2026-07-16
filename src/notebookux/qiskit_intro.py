VIDEO_URL = "https://www.youtube-nocookie.com/embed/QcK0GK7DUh8"


def render_qiskit_intro(ux) -> None:
    """Render a lightweight introduction to Qiskit and this notebook's workflow."""
    module_id = "qiskit-intro"
    screens = [
        ux.screen("O que é Qiskit?", _overview()),
        ux.screen("Vídeo do módulo", _video()),
        ux.screen("Do problema ao resultado", _workflow()),
        ux.screen("Conceitos que você usará", _basics()),
        ux.screen("Materiais para continuar", _materials()),
    ]
    ux.wrap(_style(ux, module_id) + ux.module_html("Qiskit: do circuito à execução", screens, module_id=module_id) + _script(module_id))


def _overview() -> str:
    return """
    <div class="qi-lead">
      <p><strong>Qiskit</strong> é o SDK usado para construir, transformar e executar circuitos quânticos com Python. Neste notebook ele contém toda a lógica quântica verificável.</p>
      <div class="qi-stack" aria-label="Camadas do fluxo Qiskit">
        <span>problema</span><i>→</i><span>QuantumCircuit</span><i>→</i><span>transpilador</span><i>→</i><span>Sampler</span><i>→</i><span>simulador ou QPU</span>
      </div>
    </div>
    <div class="qi-boundaries">
      <article><b>NotebookUX</b><p>Organiza texto, navegação, animações e explicações visuais.</p></article>
      <article><b>Qiskit</b><p>Cria portas e circuitos, transpila, executa shots e devolve resultados.</p></article>
    </div>
    <div class="qi-note"><strong>Regra deste projeto:</strong> nenhuma execução do Qiskit fica escondida dentro do componente visual.</div>
    """


def _video() -> str:
    return f"""
    <div class="qi-video-layout">
      <div class="qi-video">
        <iframe src="{VIDEO_URL}" title="Katie McCormick explica os algoritmos de Deutsch e Deutsch-Jozsa"
                loading="lazy" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share"
                referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe>
      </div>
      <aside>
        <div class="qi-kicker">Antes de programar</div>
        <h3>Observe três ideias</h3>
        <ol>
          <li>O oráculo é tratado como uma caixa-preta.</li>
          <li>A fase guarda informação sem ser medida diretamente.</li>
          <li>A interferência transforma essa fase em uma resposta observável.</li>
        </ol>
        <a href="https://youtu.be/QcK0GK7DUh8" target="_blank" rel="noopener">Abrir o vídeo no YouTube ↗</a>
      </aside>
    </div>
    """


def _workflow() -> str:
    return """
    <p>Selecione uma etapa. O exemplo mostra onde ela aparece nas células executáveis do notebook.</p>
    <div class="qi-workflow" data-qi-workflow>
      <div class="qi-stage-buttons">
        <button type="button" data-qi-stage="map">1. Mapear</button>
        <button type="button" data-qi-stage="transpile">2. Transpilar</button>
        <button type="button" data-qi-stage="run">3. Executar</button>
        <button type="button" data-qi-stage="analyze">4. Analisar</button>
      </div>
      <article class="qi-stage-panel">
        <div class="qi-kicker" data-qi-stage-kicker>Etapa 1</div>
        <h3 data-qi-stage-title>Mapear o problema</h3>
        <p data-qi-stage-copy>Converta a lógica do algoritmo em qubits, portas, oráculo e medições.</p>
        <pre><code data-qi-stage-code>qc = QuantumCircuit(2, 2)\nqc.h(0)\nqc.measure([0, 1], [0, 1])</code></pre>
      </article>
    </div>
    """


def _basics() -> str:
    return """
    <div class="qi-basics">
      <details open><summary><b>Qubit e bit clássico</b><span>|ψ⟩ → 0 ou 1</span></summary><p>O qubit evolui antes da medida. O bit clássico armazena o resultado observado.</p></details>
      <details><summary><b>Porta H</b><span>superposição</span></summary><p>A Hadamard combina os estados da base e permite que amplitudes interfiram mais tarde.</p></details>
      <details><summary><b>Portas X e CX</b><span>inversão e controle</span></summary><p>X troca |0⟩ e |1⟩. CX aplica X ao alvo quando o qubit de controle está em |1⟩.</p></details>
      <details><summary><b>Shots e contagens</b><span>amostragem</span></summary><p>Um shot é uma execução seguida de medida. Muitos shots formam um dicionário de contagens.</p></details>
      <details><summary><b>Little endian</b><span>ordem dos bits</span></summary><p>Ao interpretar bitstrings do Qiskit, confira a ordem dos registradores e leia os qubits conforme o mapeamento da medida.</p></details>
      <details><summary><b>Simulador e QPU</b><span>ideal, ruído e hardware</span></summary><p>Comece no simulador, valide o circuito com ruído e só então envie uma execução autorizada ao hardware real.</p></details>
    </div>
    """


def _materials() -> str:
    links = (
        ("Construir circuitos", "QuantumCircuit, portas, composição e medições.", "https://quantum.cloud.ibm.com/docs/en/guides/construct-circuits", "guia"),
        ("Entender transpilação", "ISA, layout, roteamento, tradução e otimização.", "https://quantum.cloud.ibm.com/docs/en/guides/transpile", "guia"),
        ("Usar primitives", "Quando usar Sampler ou Estimator.", "https://quantum.cloud.ibm.com/docs/guides/primitives-examples", "referência"),
        ("Fundamentos quânticos", "Curso oficial sobre estados, circuitos e medições.", "https://quantum.cloud.ibm.com/learning/en/courses/basics-of-quantum-information", "curso"),
        ("Executar circuitos", "Fluxo prático entre Qiskit, primitives e hardware.", "https://quantum.cloud.ibm.com/learning/en/courses/quantum-computing-in-practice/running-quantum-circuits", "aula"),
    )
    cards = "".join(
        f'<a href="{url}" target="_blank" rel="noopener"><small>{kind}</small><b>{title}</b><span>{copy}</span><i>abrir ↗</i></a>'
        for title, copy, url, kind in links
    )
    return f"""
    <p>Use esta trilha quando precisar revisar uma etapa antes de executar os algoritmos.</p>
    <div class="qi-materials">{cards}</div>
    <div class="qi-note"><strong>Ordem recomendada:</strong> circuitos → transpilação → simulador → primitives → hardware real.</div>
    """


def _style(ux, module_id: str) -> str:
    t = ux.theme
    root = f"#{module_id}"
    return f"""
    <style>
    {root} {{--p:{t['primary']};--a:{t['accent']};--s:{t['surface']};--s2:{t['surface_2']};--b:{t['border']};--tx:{t['text']};--m:{t['muted']};overflow:hidden}}
    {root} *{{box-sizing:border-box}} {root}_content{{min-height:0;padding:clamp(18px,2.4vw,28px)!important}}
    {root}_content>div:first-child{{font-size:clamp(27px,3vw,34px)!important;margin-bottom:16px!important}}
    {root} p,{root} li{{font-size:clamp(17px,1.55vw,20px);line-height:1.65}} {root} h3{{font-size:22px;margin:5px 0 10px}}
    {root} button{{font:inherit}} {root} .qi-kicker{{color:var(--p);font-size:12px;font-weight:950;letter-spacing:.12em;text-transform:uppercase}}
    {root} .qi-stack{{align-items:center;display:flex;flex-wrap:wrap;gap:9px;margin:22px 0}} {root} .qi-stack span{{background:var(--s2);border:1px solid var(--b);border-radius:8px;font-weight:900;padding:10px 12px}} {root} .qi-stack i{{color:var(--a);font-style:normal;font-weight:950}}
    {root} .qi-boundaries{{display:grid;gap:13px;grid-template-columns:1fr 1fr}} {root} .qi-boundaries article{{background:var(--s2);border:1px solid var(--b);border-top:5px solid var(--p);border-radius:11px;padding:17px}} {root} .qi-boundaries article+article{{border-top-color:var(--a)}}
    {root} .qi-boundaries b{{font-size:22px}} {root} .qi-boundaries p{{font-size:17px;margin:8px 0 0}}
    {root} .qi-note{{background:var(--s2);border-left:5px solid var(--a);border-radius:0 10px 10px 0;font-size:17px;line-height:1.55;margin-top:16px;padding:14px 17px}}
    {root} .qi-video-layout{{display:grid;gap:20px;grid-template-columns:minmax(0,1.65fr) minmax(240px,.75fr)}} {root} .qi-video{{aspect-ratio:16/9;background:#000;border:1px solid var(--b);border-radius:12px;overflow:hidden}} {root} .qi-video iframe{{border:0;height:100%;width:100%}}
    {root} .qi-video-layout aside{{background:var(--s2);border:1px solid var(--b);border-radius:12px;padding:18px}} {root} .qi-video-layout ol{{padding-left:23px}} {root} .qi-video-layout a{{color:var(--p);font-weight:900}}
    {root} .qi-workflow{{display:grid;gap:16px;grid-template-columns:minmax(170px,.65fr) minmax(0,1.5fr)}} {root} .qi-stage-buttons{{display:grid;gap:9px}}
    {root} .qi-stage-buttons button{{background:var(--s2);border:1px solid var(--b);border-radius:9px;color:var(--tx);cursor:pointer;font-weight:900;padding:13px;text-align:left}} {root} .qi-stage-buttons button[aria-pressed=true]{{background:var(--p);border-color:var(--p);color:white}}
    {root} .qi-stage-panel{{background:var(--s2);border:1px solid var(--b);border-radius:12px;padding:19px}} {root} .qi-stage-panel pre{{background:var(--s);border:1px solid var(--b);border-radius:9px;color:var(--tx);font-size:14px;line-height:1.55;margin:15px 0 0;overflow:auto;padding:14px;white-space:pre-wrap}}
    {root} .qi-basics{{display:grid;gap:10px;grid-template-columns:1fr 1fr}} {root} .qi-basics details{{background:var(--s2);border:1px solid var(--b);border-radius:10px;padding:14px}} {root} .qi-basics summary{{cursor:pointer;display:grid;gap:6px;list-style:none}} {root} .qi-basics summary span{{color:var(--a);font-size:14px;font-weight:850}} {root} .qi-basics p{{font-size:16px;margin:12px 0 0}}
    {root} .qi-materials{{display:grid;gap:11px;grid-template-columns:repeat(auto-fit,minmax(210px,1fr))}} {root} .qi-materials a{{background:var(--s2);border:1px solid var(--b);border-radius:11px;color:var(--tx);display:grid;gap:8px;padding:16px;text-decoration:none}} {root} .qi-materials a:hover{{border-color:var(--p);transform:translateY(-1px)}}
    {root} .qi-materials small{{color:var(--p);font-size:11px;font-weight:950;letter-spacing:.1em;text-transform:uppercase}} {root} .qi-materials b{{font-size:19px}} {root} .qi-materials span{{color:var(--m);font-size:15px;line-height:1.5}} {root} .qi-materials i{{color:var(--a);font-style:normal;font-weight:900}}
    @media(max-width:760px){{{root} .qi-boundaries,{root} .qi-video-layout,{root} .qi-workflow,{root} .qi-basics{{grid-template-columns:1fr}}}}
    </style>
    """


def _script(module_id: str) -> str:
    return f"""
    <script>(()=>{{
      const root=document.getElementById({module_id!r});if(!root)return;
      const stages={{
        map:['Etapa 1','Mapear o problema','Converta a lógica do algoritmo em qubits, portas, oráculo e medições.','qc = QuantumCircuit(2, 2)\\nqc.h(0)\\nqc.measure([0, 1], [0, 1])'],
        transpile:['Etapa 2','Adaptar ao backend','Reescreva o circuito para as portas e conexões permitidas pelo dispositivo escolhido.','pm = generate_preset_pass_manager(\\n    target=backend.target, optimization_level=3\\n)\\nqc_isa = pm.run(qc)'],
        run:['Etapa 3','Executar shots','Envie o circuito transpilado ao Sampler do simulador ou, quando autorizado, ao hardware.','job = sampler_sim.run([qc_isa], shots=1024)\\nresult = job.result()'],
        analyze:['Etapa 4','Interpretar contagens','Leia a distribuição medida e relacione cada bitstring à pergunta do algoritmo.','counts = result[0].data.c.get_counts()\\nplot_histogram(counts)']
      }};
      let active='map';
      const hydrate=()=>{{
        root.querySelectorAll('[data-qi-stage]').forEach(b=>b.setAttribute('aria-pressed',b.dataset.qiStage===active));
        const panel=root.querySelector('[data-qi-workflow]');if(!panel)return;const value=stages[active];
        panel.querySelector('[data-qi-stage-kicker]').textContent=value[0];panel.querySelector('[data-qi-stage-title]').textContent=value[1];panel.querySelector('[data-qi-stage-copy]').textContent=value[2];panel.querySelector('[data-qi-stage-code]').textContent=value[3];
      }};
      root.addEventListener('click',event=>{{const button=event.target.closest('[data-qi-stage]');if(button){{active=button.dataset.qiStage;hydrate()}}}});
      const content=document.getElementById({(module_id + '_content')!r});if(content)new MutationObserver(hydrate).observe(content,{{childList:true}});hydrate();
    }})()</script>
    """


__all__ = ["render_qiskit_intro"]
