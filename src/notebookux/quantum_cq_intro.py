def render_quantum_cq_intro(ux) -> None:
    """Render an interactive introduction to Quantum-CQ and its circuit DSLs."""
    module_id = "quantum-cq-intro"
    screens = [
        ux.screen("O que é Quantum-CQ?", _overview()),
        ux.screen("Da DSL até a execução", _architecture()),
        ux.screen("Quatro formas de escrever", _dsls()),
        ux.screen("Fluxo executável", _workflow()),
        ux.screen("Limites e materiais", _materials()),
    ]
    html = ux.module_html(
        "Quantum-CQ: da ideia ao circuito executável",
        screens,
        module_id=module_id,
    )
    ux.wrap(_style(ux, module_id) + html + _script(module_id))


def _overview() -> str:
    return """
    <div class="cqi-hero">
      <div>
        <div class="cqi-kicker">biblioteca educacional e experimental</div>
        <p><strong>Quantum-CQ</strong> organiza a construção de circuitos, algoritmos, métricas e execuções por uma fachada única chamada <code>CQ</code>.</p>
        <p>Em vez de prender a ideia a um único SDK, a biblioteca pode primeiro criar uma representação lógica e depois entregá-la a uma engine.</p>
      </div>
      <div class="cqi-mark" aria-label="CQ transforma descrição em circuito"><span>CQ</span><small>descrição -> IR -> engine</small></div>
    </div>
    <div class="cqi-boundaries">
      <article><b>NotebookUX</b><p>Apresenta a narrativa, os passos, os circuitos e os gráficos.</p></article>
      <article><b>Quantum-CQ</b><p>Constroi, valida, normaliza e mede a estrutura dos circuitos.</p></article>
      <article><b>Engine Qiskit</b><p>Emite o circuito nativo e executa os shots usados nesta seção.</p></article>
    </div>
    <div class="cqi-note"><strong>Regra do módulo:</strong> a DSL muda, mas cada exemplo mostra o circuito emitido, executa de verdade e exibe as contagens.</div>
    """


def _architecture() -> str:
    return """
    <p>As camadas separam a intenção do algoritmo dos detalhes do backend. Passe o cursor ou toque em cada etapa para ler sua responsabilidade.</p>
    <div class="cqi-pipeline" aria-label="Pipeline Quantum-CQ">
      <article><small>01</small><b>DSL</b><span>equação MQT, matriz QC, builder ou algoritmo</span></article>
      <i>-></i>
      <article><small>02</small><b>CircuitIR</b><span>operações, qubits, medidas e metadados neutros</span></article>
      <i>-></i>
      <article><small>03</small><b>Engine</b><span>compatibilidade, emissão e compilação nativa</span></article>
      <i>-></i>
      <article><small>04</small><b>Resultado</b><span>counts canônicos, ordem dos bits e proveniência</span></article>
    </div>
    <div class="cqi-two">
      <article><div class="cqi-kicker">por que usar IR?</div><h3>Uma lógica, mais de uma engine</h3><p>A representação intermediária permite inspecionar o circuito antes de escolher o executor e recusa recursos que a engine não suporta.</p></article>
      <article><div class="cqi-kicker">neste notebook</div><h3>Qiskit continua visível</h3><p><code>CQ.emit(..., engine="qiskit")</code> produz o desenho, e <code>CQ.run_engine(...)</code> devolve as contagens. Nenhuma execução fica escondida na camada visual.</p></article>
    </div>
    """


def _dsls() -> str:
    return """
    <p>Selecione uma DSL. As quatro descrevem circuitos reais, mas cada uma privilegia um tipo de raciocinio.</p>
    <div class="cqi-dsl" data-cqi-dsl-root>
      <div class="cqi-dsl-buttons" role="tablist" aria-label="DSLs Quantum-CQ">
        <button type="button" data-cqi-dsl="mqt">MQT textual</button>
        <button type="button" data-cqi-dsl="qc">QC matricial</button>
        <button type="button" data-cqi-dsl="builder">Builder lógico</button>
        <button type="button" data-cqi-dsl="algorithm">Algoritmo fluente</button>
      </div>
      <article class="cqi-dsl-panel">
        <div><div class="cqi-kicker" data-cqi-kind>declarativa</div><h3 data-cqi-title>Equação MQT</h3><p data-cqi-copy>Escreve a evolução do estado como composição e produto tensorial.</p></div>
        <pre><code data-cqi-code>|psi&gt; := CX[q0,q1] * (H[q0] tensor I[q1]) * |00&gt;
measure Z[q0,q1] -&gt; c[0,1]</code></pre>
        <div class="cqi-use"><b data-cqi-use-title>Use quando</b><span data-cqi-use>o foco for a álgebra do circuito e a ordem das transformações.</span></div>
      </article>
    </div>
    """


def _workflow() -> str:
    return """
    <div class="cqi-workflow">
      <article><b>1</b><div><small>descrever</small><strong>Escolha a DSL</strong><p>Declare portas, registradores, oráculo e medidas no nível adequado ao problema.</p></div></article>
      <article><b>2</b><div><small>normalizar</small><strong>Produza a IR</strong><p>Use <code>build()</code>, <code>to_ir()</code> ou a pipeline MQT para obter a estrutura lógica.</p></div></article>
      <article><b>3</b><div><small>emitir</small><strong>Inspecione o circuito</strong><p><code>CQ.emit(ir, engine="qiskit")</code> cria o circuito nativo que será desenhado.</p></div></article>
      <article><b>4</b><div><small>executar</small><strong>Colete evidencias</strong><p><code>CQ.run_engine(ir, shots=1024)</code> executa e devolve contagens canonicas.</p></div></article>
    </div>
    <pre class="cqi-run"><code>resultado = CQ.run_engine(circuito, engine="qiskit", shots=1024)
counts = dict(resultado.counts)
metricas = CQ.metrics(circuito)</code></pre>
    <div class="cqi-note"><strong>Nas células seguintes:</strong> o código de construção fica separado da célula de exibição para que desenhos e gráficos possam ser recolhidos.</div>
    """


def _materials() -> str:
    links = (
        ("Repositorio e instalacao", "README, extras opcionais e exemplos iniciais.", "https://github.com/jyrikes/quantum-cq"),
        ("Visão da API", "Fachada CQ, circuitos lógicos, engines e pipeline.", "https://github.com/jyrikes/quantum-cq/blob/main/docs/api_overview.md"),
        ("DSL MQT", "Gramática, IR semântica, lowering e limites atuais.", "https://github.com/jyrikes/quantum-cq/blob/main/docs/architecture/run_4_mqt_unified_pipeline.md"),
        ("Notas da versão 0.2.0", "Contrato multi-engine e recursos implementados.", "https://github.com/jyrikes/quantum-cq/blob/main/docs/release_0_2_0.md"),
    )
    cards = "".join(
        f'<a href="{url}" target="_blank" rel="noopener"><small>documentação</small><b>{title}</b><span>{copy}</span><i>abrir -></i></a>'
        for title, copy, url in links
    )
    return f"""
    <div class="cqi-materials">{cards}</div>
    <div class="cqi-limits">
      <div class="cqi-kicker">leitura honesta</div>
      <h3>O que a biblioteca não promete</h3>
      <p>Quantum-CQ é experimental. Ela não afirma vantagem quântica, QRAM física escalável nem suporte idêntico em todas as engines. A compatibilidade deve ser validada antes da execução.</p>
      <div><span>educação</span><span>prototipagem</span><span>IR verificável</span><span>interoperabilidade gradual</span></div>
    </div>
    """


def _style(ux, module_id: str) -> str:
    t = ux.theme
    root = f"#{module_id}"
    return f"""
    <style>
    {root} {{--p:{t['primary']};--a:{t['accent']};--s:{t['surface']};--s2:{t['surface_2']};--b:{t['border']};--tx:{t['text']};--m:{t['muted']};overflow:hidden}}
    {root} *{{box-sizing:border-box}} {root}_content{{min-height:0;padding:clamp(18px,2.4vw,28px)!important}} {root}_content>div:first-child{{font-size:clamp(27px,3vw,35px)!important;margin-bottom:17px!important}}
    {root} p,{root} li{{font-size:clamp(16px,1.45vw,19px);line-height:1.62}} {root} h3{{font-size:22px;margin:5px 0 9px}} {root} code{{font-family:"IBM Plex Mono","Cascadia Code",monospace}} {root} button{{font:inherit}}
    {root} .cqi-kicker{{color:var(--p);font-size:11px;font-weight:950;letter-spacing:.12em;text-transform:uppercase}} {root} .cqi-note{{background:var(--s2);border-left:5px solid var(--a);border-radius:0 9px 9px 0;font-size:16px;line-height:1.55;margin-top:16px;padding:13px 16px}}
    {root} .cqi-hero{{align-items:center;display:grid;gap:25px;grid-template-columns:minmax(0,1.45fr) minmax(220px,.55fr)}} {root} .cqi-hero p{{margin:10px 0}} {root} .cqi-mark{{align-items:center;aspect-ratio:1;background:radial-gradient(circle at 35% 30%,color-mix(in srgb,var(--a) 48%,var(--p)),var(--s2) 62%);border:1px solid var(--b);border-radius:50%;display:flex;flex-direction:column;justify-content:center;margin:auto;max-width:230px;text-align:center;width:100%}} {root} .cqi-mark span{{font-size:54px;font-weight:1000;letter-spacing:-.08em}} {root} .cqi-mark small{{font-size:11px;font-weight:900;max-width:140px}}
    {root} .cqi-boundaries{{display:grid;gap:11px;grid-template-columns:repeat(3,1fr);margin-top:20px}} {root} .cqi-boundaries article{{background:var(--s2);border:1px solid var(--b);border-top:4px solid var(--p);border-radius:10px;padding:15px}} {root} .cqi-boundaries article:nth-child(2){{border-top-color:var(--a)}} {root} .cqi-boundaries b{{font-size:19px}} {root} .cqi-boundaries p{{font-size:15px;margin:7px 0 0}}
    {root} .cqi-pipeline{{align-items:center;display:grid;gap:8px;grid-template-columns:1fr auto 1fr auto 1fr auto 1fr;margin:20px 0}} {root} .cqi-pipeline article{{background:var(--s2);border:1px solid var(--b);border-radius:11px;display:grid;gap:6px;min-height:142px;padding:15px}} {root} .cqi-pipeline small{{color:var(--a);font-weight:950}} {root} .cqi-pipeline b{{font-size:20px}} {root} .cqi-pipeline span{{color:var(--m);font-size:14px;line-height:1.45}} {root} .cqi-pipeline>i{{color:var(--a);font-style:normal;font-weight:950}}
    {root} .cqi-two{{display:grid;gap:12px;grid-template-columns:1fr 1fr}} {root} .cqi-two article{{background:linear-gradient(145deg,color-mix(in srgb,var(--p) 8%,var(--s2)),var(--s2));border:1px solid var(--b);border-radius:11px;padding:17px}} {root} .cqi-two p{{font-size:16px;margin-bottom:0}}
    {root} .cqi-dsl{{display:grid;gap:14px;grid-template-columns:minmax(180px,.62fr) minmax(0,1.5fr)}} {root} .cqi-dsl-buttons{{display:grid;gap:8px}} {root} .cqi-dsl-buttons button{{background:var(--s2);border:1px solid var(--b);border-radius:8px;color:var(--tx);cursor:pointer;font-weight:900;padding:12px;text-align:left}} {root} .cqi-dsl-buttons button[aria-selected=true]{{background:var(--p);border-color:var(--p);color:white}}
    {root} .cqi-dsl-panel{{background:var(--s2);border:1px solid var(--b);border-radius:11px;display:grid;gap:13px;padding:18px}} {root} .cqi-dsl-panel p{{font-size:16px;margin:0}} {root} .cqi-dsl-panel pre,{root} .cqi-run{{background:var(--s);border:1px solid var(--b);border-radius:9px;color:var(--tx);font-size:13px;line-height:1.55;margin:0;overflow:auto;padding:14px;white-space:pre-wrap}} {root} .cqi-use{{align-items:center;border-top:1px solid var(--b);display:flex;gap:9px;padding-top:12px}} {root} .cqi-use b{{color:var(--a);font-size:13px;text-transform:uppercase}} {root} .cqi-use span{{color:var(--m);font-size:14px}}
    {root} .cqi-workflow{{display:grid;gap:10px;grid-template-columns:1fr 1fr}} {root} .cqi-workflow article{{align-items:start;background:var(--s2);border:1px solid var(--b);border-radius:10px;display:grid;gap:12px;grid-template-columns:34px 1fr;padding:14px}} {root} .cqi-workflow article>b{{align-items:center;background:var(--p);border-radius:50%;color:white;display:flex;height:32px;justify-content:center}} {root} .cqi-workflow small{{color:var(--a);font-size:10px;font-weight:950;letter-spacing:.1em;text-transform:uppercase}} {root} .cqi-workflow strong{{display:block;font-size:18px;margin-top:3px}} {root} .cqi-workflow p{{font-size:15px;margin:6px 0 0}} {root} .cqi-run{{font-size:14px;margin-top:13px}}
    {root} .cqi-materials{{display:grid;gap:10px;grid-template-columns:repeat(auto-fit,minmax(210px,1fr))}} {root} .cqi-materials a{{background:var(--s2);border:1px solid var(--b);border-radius:10px;color:var(--tx);display:grid;gap:7px;padding:15px;text-decoration:none}} {root} .cqi-materials a:hover{{border-color:var(--p)}} {root} .cqi-materials small{{color:var(--p);font-size:10px;font-weight:950;letter-spacing:.1em;text-transform:uppercase}} {root} .cqi-materials b{{font-size:18px}} {root} .cqi-materials span{{color:var(--m);font-size:14px;line-height:1.45}} {root} .cqi-materials i{{color:var(--a);font-style:normal;font-weight:900}}
    {root} .cqi-limits{{background:linear-gradient(135deg,color-mix(in srgb,var(--a) 9%,var(--s2)),var(--s2));border:1px solid var(--b);border-radius:11px;margin-top:15px;padding:17px}} {root} .cqi-limits p{{font-size:16px}} {root} .cqi-limits>div:last-child{{display:flex;flex-wrap:wrap;gap:7px}} {root} .cqi-limits span{{border:1px solid var(--b);border-radius:999px;font-size:12px;font-weight:850;padding:6px 9px}}
    @media(max-width:760px){{{root} .cqi-hero,{root} .cqi-dsl,{root} .cqi-two,{root} .cqi-workflow{{grid-template-columns:1fr}} {root} .cqi-mark{{max-width:180px}} {root} .cqi-boundaries{{grid-template-columns:1fr}} {root} .cqi-pipeline{{grid-template-columns:1fr}} {root} .cqi-pipeline>i{{transform:rotate(90deg);justify-self:center}} {root} .cqi-pipeline article{{min-height:0}}}}
    </style>
    """


def _script(module_id: str) -> str:
    return f"""
    <script>(()=>{{
      const root=document.getElementById({module_id!r});if(!root)return;
      const dsls={{
        mqt:{{kind:'declarativa',title:'Equação MQT',copy:'Escreve a evolução do estado como composição e produto tensorial.',code:'|psi> := CX[q0,q1] * (H[q0] tensor I[q1]) * |00>\\nmeasure Z[q0,q1] -> c[0,1]',use:'o foco for a álgebra do circuito e a ordem das transformações.'}},
        qc:{{kind:'visual e compacta',title:'Matriz QC',copy:'Cada linha representa um qubit e cada coluna representa um instante lógico.',code:"QC('Deutsch', [\\n  [0, '-', 'H', ctrl('CX'), '-', 'H', m(0)],\\n  [0, 'X', 'H', tgt('CX'), 'X', '-', '-'],\\n], c=1)",use:'for importante enxergar simultaneamente fios, camadas e controles.'}},
        builder:{{kind:'imperativa e neutra',title:'Builder CQ.circuit',copy:'Constrói uma CircuitIR sem importar um SDK quântico dentro da lógica.',code:"c = CQ.circuit(4, 3, name='DJ')\\nc.x(3)\\nc.h(0)\\nc.cx(0, 3)\\nir = c.build()",use:'o circuito precisar ser montado passo a passo e emitido para engines diferentes.'}},
        algorithm:{{kind:'declarativa de alto nível',title:'Fachada fluente de algoritmos',copy:'Configura um algoritmo conhecido por seus parâmetros, sem repetir sua estrutura interna.',code:"modelo = (CQ.algorithm('bernstein_vazirani')\\n  .with_secret('1000')\\n  .build())",use:'o objetivo for experimentar parâmetros de um algoritmo já implementado e validado.'}}
      }};
      let active='mqt';
      const hydrate=()=>{{const panel=root.querySelector('[data-cqi-dsl-root]');if(!panel)return;const value=dsls[active];panel.querySelectorAll('[data-cqi-dsl]').forEach(button=>button.setAttribute('aria-selected',button.dataset.cqiDsl===active));panel.querySelector('[data-cqi-kind]').textContent=value.kind;panel.querySelector('[data-cqi-title]').textContent=value.title;panel.querySelector('[data-cqi-copy]').textContent=value.copy;panel.querySelector('[data-cqi-code]').textContent=value.code;panel.querySelector('[data-cqi-use]').textContent=value.use;}};
      root.addEventListener('click',event=>{{const button=event.target.closest('[data-cqi-dsl]');if(button){{active=button.dataset.cqiDsl;hydrate();}}}});
      const content=document.getElementById({(module_id + '_content')!r});if(content)new MutationObserver(hydrate).observe(content,{{childList:true}});hydrate();
    }})()</script>
    """


__all__ = ["render_quantum_cq_intro"]
