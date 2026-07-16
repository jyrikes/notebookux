from html import escape
from itertools import count

_STATUS_IDS = count(1)


def render_pipeline_guide(ux) -> None:
    """Explain Quantum-CQ execution pipelines and their three runtime targets."""
    module_id = "quantum-cq-pipeline-guide"
    screens = [
        ux.screen("O que é uma pipeline?", _overview()),
        ux.screen("Três ambientes", _targets()),
        ux.screen("Arquitetura na Quantum-CQ", _architecture()),
        ux.screen("Credencial e execução segura", _safety()),
    ]
    html = ux.module_html(
        "Quantum-CQ • Pipeline do circuito ao hardware",
        screens,
        module_id=module_id,
    )
    ux.wrap(_style(ux, module_id) + html)


def render_pipeline_status(
    ux,
    *,
    credential_ready: bool,
    credential_source: str | None,
    real_enabled: bool,
    shots: int,
    noise_source: str,
) -> None:
    """Render a token-safe execution summary for a configured pipeline."""
    status_id = f"quantum-cq-pipeline-status-{next(_STATUS_IDS)}"
    credential = escape(credential_source or "nenhum JSON localizado")
    real_state = "autorizado" if real_enabled else "bloqueado por segurança"
    credential_state = "credencial pronta" if credential_ready else "credencial ausente"
    real_class = "is-ready" if real_enabled and credential_ready else "is-locked"
    body = f"""
    <section id="{status_id}" class="qps-root" role="region" aria-label="Estado da pipeline Quantum-CQ">
      <header><div><small>execução concluída</small><h3>Quantum-CQ • Estado dos três destinos</h3></div><span>{shots:,} shots por simulador</span></header>
      <p>A mesma <strong>CircuitIR</strong> foi entregue aos dois simuladores locais. O destino físico foi configurado separadamente para impedir o envio acidental de jobs.</p>
      <div class="qps-targets">
        <article class="is-done"><i>01</i><small>referência matemática</small><b>Ideal</b><span>Aer sem modelo de ruído</span><strong>executado</strong></article>
        <article class="is-done"><i>02</i><small>ensaio de hardware</small><b>Noisy</b><span>{escape(noise_source)}</span><strong>executado</strong></article>
        <article class="{real_class}"><i>03</i><small>QPU IBM</small><b>Real</b><span>{credential_state}</span><strong>{real_state}</strong></article>
      </div>
      <div class="qps-credential">
        <div><small>origem da credencial</small><b>{credential}</b></div>
        <p>O token foi lido somente em memória e nunca é exibido nem salvo na saída do notebook.</p>
      </div>
      <div class="qps-reading"><b>Como comparar:</b><span>ideal = resposta de referência</span><span>noisy = degradação simulada</span><span>real = ruído físico e fila do provedor</span></div>
    </section>
    """
    ux.wrap(_status_style(ux, status_id) + body)


def _overview() -> str:
    return """
    <div class="qpg-hero">
      <div>
        <div class="qpg-kicker">uma sequência reproduzível</div>
        <p>Uma <strong>pipeline</strong> é o caminho completo que transforma um circuito lógico em evidência experimental. Ela mantém juntas as decisões de validação, compilação, backend, shots e coleta das contagens.</p>
        <p>Sem essa estrutura, cada célula pode transpilar ou medir de um jeito diferente, tornando a comparação entre execuções pouco confiável.</p>
      </div>
      <div class="qpg-loop"><span>IR</span><i>→</i><span>backend</span><i>→</i><span>counts</span></div>
    </div>
    <div class="qpg-flow" aria-label="Etapas de uma pipeline quântica">
      <article><small>01</small><b>Receber</b><span>CircuitIR e intenção de medição</span></article><i>→</i>
      <article><small>02</small><b>Validar</b><span>qubits, portas e registradores</span></article><i>→</i>
      <article><small>03</small><b>Transpilar</b><span>circuito compatível com o backend</span></article><i>→</i>
      <article><small>04</small><b>Executar</b><span>shots no runtime selecionado</span></article><i>→</i>
      <article><small>05</small><b>Decodificar</b><span>counts e ordem dos bits</span></article>
    </div>
    <div class="qpg-note"><strong>Ideia central:</strong> muda o ambiente de execução, mas o circuito lógico de entrada permanece o mesmo.</div>
    """


def _targets() -> str:
    return """
    <p>Os três destinos respondem perguntas diferentes. Eles não são substitutos perfeitos uns dos outros.</p>
    <div class="qpg-targets">
      <article class="ideal"><div><small>sem ruído</small><b>Ideal</b></div><p>Usa <code>AerSimulator()</code> como referência matemática. Mostra o que o circuito deveria produzir sem erros físicos.</p><span>rápido • local • reprodutível</span></article>
      <article class="noisy"><div><small>com ruído</small><b>Noisy</b></div><p>Executa no Aer com um <code>NoiseModel</code>. Neste notebook o perfil é sintético e tem seed fixa.</p><span>local • aproximado • comparável</span></article>
      <article class="real"><div><small>hardware físico</small><b>Real IBM</b></div><p>Transpila para uma QPU e usa <code>SamplerV2</code>. Há ruído físico, fila, calibração variável e possível consumo de cota.</p><span>remoto • assíncrono • opt-in</span></article>
    </div>
    <div class="qpg-warning"><b>Importante</b><p>Não existe máquina quântica física “sem ruído”. A comparação sem ruído é feita pelo simulador ideal.</p></div>
    """


def _architecture() -> str:
    return """
    <p><code>PipelineSettings</code> define como executar; <code>RuntimeSettings</code> define onde e com quais credenciais. <code>BenchmarkingPipeline</code> une as duas configurações.</p>
    <div class="qpg-architecture">
      <div class="qpg-input"><small>entrada única</small><b>CircuitIR</b><span>Deutsch-Jozsa 101</span></div>
      <div class="qpg-trunk"><span>validação</span><i>→</i><span>transpilação</span><i>→</i><span>medição</span></div>
      <div class="qpg-branches">
        <article><b>ideal</b><span>RuntimeFactory → Aer</span></article>
        <article><b>noisy</b><span>GenericBackendV2 → NoiseModel → Aer</span></article>
        <article><b>real</b><span>JSON → IBM Runtime → QPU</span></article>
      </div>
    </div>
    <pre class="qpg-code"><code>settings = PipelineSettings(modes=("ideal", "noisy"), shots=512)
runtime = RuntimeSettings(noise_source="synthetic", synthetic_seed=42)
pipeline = BenchmarkingPipeline(settings=settings, runtime_settings=runtime)
counts = pipeline.run_batch(circuito)</code></pre>
    <div class="qpg-note"><strong>Uma chamada, dois resultados locais:</strong> <code>counts["ideal"]</code> e <code>counts["noisy"]</code>.</div>
    """


def _safety() -> str:
    return """
    <div class="qpg-safety">
      <article><b>1</b><div><small>localizar</small><strong>JSON fora do notebook</strong><p>A célula procura <code>apikey.json</code> e <code>ibm-quantum-credentials.json</code> nos diretórios pais.</p></div></article>
      <article><b>2</b><div><small>normalizar</small><strong>Token em memória</strong><p>São aceitas as chaves <code>apikey</code>, <code>api_key</code> ou <code>token</code>. O valor nunca é impresso.</p></div></article>
      <article><b>3</b><div><small>preparar</small><strong>RuntimeSettings real</strong><p>Canal, instância, região e preferências são repassados para o runtime IBM.</p></div></article>
      <article><b>4</b><div><small>autorizar</small><strong>Envio explícito</strong><p>Somente <code>CQ_REAL_HARDWARE = True</code> cria a pipeline real e envia o job.</p></div></article>
    </div>
    <pre class="qpg-code"><code>if CQ_REAL_HARDWARE:
    pipeline_real = BenchmarkingPipeline(
        settings=PipelineSettings(modes=("real",), ...),
        runtime_settings=runtime_real,
    )
    counts_real = pipeline_real.run_batch(circuito)</code></pre>
    <div class="qpg-warning"><b>Execução deste notebook</b><p>Os simuladores rodam automaticamente. O hardware real permanece preparado, mas bloqueado, para evitar fila e consumo de cota sem confirmação.</p></div>
    """


def _style(ux, module_id: str) -> str:
    t = ux.theme
    root = f"#{module_id}"
    return f"""
    <style>
    {root}{{--p:{t['primary']};--a:{t['accent']};--s:{t['surface']};--s2:{t['surface_2']};--b:{t['border']};--tx:{t['text']};--m:{t['muted']};overflow:hidden}}
    {root} *{{box-sizing:border-box}} {root}_content{{min-height:0;padding:clamp(18px,2.4vw,28px)!important}} {root}_content>div:first-child{{font-size:clamp(27px,3vw,35px)!important;margin-bottom:17px!important}}
    {root} p{{font-size:clamp(16px,1.4vw,19px);line-height:1.62}} {root} code{{font-family:"IBM Plex Mono","Cascadia Code",monospace}} {root} .qpg-kicker,{root} small{{color:var(--p);font-size:10px;font-weight:950;letter-spacing:.11em;text-transform:uppercase}}
    {root} .qpg-hero{{align-items:center;display:grid;gap:24px;grid-template-columns:minmax(0,1.45fr) minmax(240px,.55fr)}} {root} .qpg-loop{{align-items:center;background:radial-gradient(circle at 30% 20%,color-mix(in srgb,var(--a) 22%,var(--s2)),var(--s2));border:1px solid var(--b);border-radius:999px;display:flex;gap:8px;justify-content:center;min-height:150px;padding:20px}} {root} .qpg-loop span{{font-size:18px;font-weight:950}} {root} .qpg-loop i{{color:var(--a);font-style:normal}}
    {root} .qpg-flow{{align-items:stretch;display:grid;gap:7px;grid-template-columns:1fr auto 1fr auto 1fr auto 1fr auto 1fr;margin:21px 0}} {root} .qpg-flow article{{background:var(--s2);border:1px solid var(--b);border-radius:10px;display:grid;gap:5px;padding:13px}} {root} .qpg-flow b{{font-size:18px}} {root} .qpg-flow span{{color:var(--m);font-size:13px;line-height:1.45}} {root} .qpg-flow>i{{align-self:center;color:var(--a);font-style:normal;font-weight:950}}
    {root} .qpg-note{{background:var(--s2);border-left:5px solid var(--a);border-radius:0 9px 9px 0;font-size:16px;line-height:1.55;padding:13px 16px}} {root} .qpg-targets{{display:grid;gap:12px;grid-template-columns:repeat(3,1fr)}} {root} .qpg-targets article{{background:var(--s2);border:1px solid var(--b);border-top:5px solid #38bdf8;border-radius:11px;display:grid;gap:9px;padding:17px}} {root} .qpg-targets .noisy{{border-top-color:#f59e0b}} {root} .qpg-targets .real{{border-top-color:#ef4444}} {root} .qpg-targets article>div{{display:flex;flex-direction:column}} {root} .qpg-targets b{{font-size:25px}} {root} .qpg-targets p{{font-size:15px;margin:0}} {root} .qpg-targets article>span{{color:var(--m);font-size:12px;font-weight:850}}
    {root} .qpg-warning{{align-items:start;background:color-mix(in srgb,#f59e0b 10%,var(--s2));border:1px solid color-mix(in srgb,#f59e0b 45%,var(--b));border-radius:10px;display:grid;gap:6px;margin-top:14px;padding:14px 16px}} {root} .qpg-warning b{{color:#fbbf24;font-size:17px}} {root} .qpg-warning p{{font-size:15px;margin:0}}
    {root} .qpg-architecture{{display:grid;gap:12px;grid-template-columns:minmax(150px,.45fr) minmax(220px,.8fr) minmax(250px,1fr);margin:18px 0}} {root} .qpg-input,{root} .qpg-trunk,{root} .qpg-branches article{{background:var(--s2);border:1px solid var(--b);border-radius:10px;padding:15px}} {root} .qpg-input{{display:flex;flex-direction:column;justify-content:center}} {root} .qpg-input b{{font-size:26px}} {root} .qpg-input span{{color:var(--m)}} {root} .qpg-trunk{{align-items:center;display:flex;flex-wrap:wrap;gap:8px;justify-content:center}} {root} .qpg-trunk span{{font-weight:850}} {root} .qpg-trunk i{{color:var(--a);font-style:normal}} {root} .qpg-branches{{display:grid;gap:7px}} {root} .qpg-branches article{{display:grid;gap:4px;padding:10px 13px}} {root} .qpg-branches article:nth-child(2){{border-left:4px solid #f59e0b}} {root} .qpg-branches article:nth-child(3){{border-left:4px solid #ef4444}} {root} .qpg-branches article:first-child{{border-left:4px solid #38bdf8}} {root} .qpg-branches span{{color:var(--m);font-size:13px}}
    {root} .qpg-code{{background:var(--s);border:1px solid var(--b);border-radius:9px;color:var(--tx);font-size:13px;line-height:1.6;margin:14px 0;overflow:auto;padding:15px;white-space:pre-wrap}} {root} .qpg-safety{{display:grid;gap:10px;grid-template-columns:1fr 1fr}} {root} .qpg-safety article{{align-items:start;background:var(--s2);border:1px solid var(--b);border-radius:10px;display:grid;gap:12px;grid-template-columns:34px 1fr;padding:14px}} {root} .qpg-safety article>b{{align-items:center;background:var(--p);border-radius:50%;color:white;display:flex;height:32px;justify-content:center}} {root} .qpg-safety strong{{display:block;font-size:18px;margin-top:4px}} {root} .qpg-safety p{{font-size:14px;margin:5px 0 0}}
    @media(max-width:820px){{{root} .qpg-hero,{root} .qpg-architecture{{grid-template-columns:1fr}} {root} .qpg-targets{{grid-template-columns:1fr}} {root} .qpg-flow{{grid-template-columns:1fr}} {root} .qpg-flow>i{{justify-self:center;transform:rotate(90deg)}}}}
    @media(max-width:620px){{{root} .qpg-safety{{grid-template-columns:1fr}} {root} .qpg-loop{{min-height:110px}}}}
    </style>
    """


def _status_style(ux, status_id: str) -> str:
    t = ux.theme
    root = f"#{status_id}"
    return f"""
    <style>
    {root}{{--p:{t['primary']};--a:{t['accent']};--s:{t['surface']};--s2:{t['surface_2']};--b:{t['border']};--tx:{t['text']};--m:{t['muted']};background:linear-gradient(145deg,var(--s),color-mix(in srgb,var(--p) 5%,var(--s2)));border:1px solid var(--b);border-radius:12px;color:var(--tx);font-family:{t['font']};margin:14px 0;overflow:hidden;padding:clamp(18px,2.4vw,28px)}}
    {root} *{{box-sizing:border-box}} {root} header{{align-items:start;display:flex;gap:16px;justify-content:space-between}} {root} header small,{root} article small,{root} .qps-credential small{{color:var(--p);font-size:10px;font-weight:950;letter-spacing:.11em;text-transform:uppercase}} {root} h3{{font-size:clamp(24px,3vw,33px);line-height:1.15;margin:5px 0}} {root} header>span{{background:var(--s2);border:1px solid var(--b);border-radius:999px;font-size:12px;font-weight:900;padding:7px 10px;white-space:nowrap}} {root}>p{{color:var(--m);font-size:16px;line-height:1.6}}
    {root} .qps-targets{{display:grid;gap:11px;grid-template-columns:repeat(3,1fr);margin:17px 0}} {root} .qps-targets article{{background:var(--s2);border:1px solid var(--b);border-top:5px solid #38bdf8;border-radius:10px;display:grid;gap:5px;padding:15px}} {root} .qps-targets article:nth-child(2){{border-top-color:#f59e0b}} {root} .qps-targets article:nth-child(3){{border-top-color:#ef4444}} {root} .qps-targets i{{align-items:center;background:var(--s);border:1px solid var(--b);border-radius:50%;display:flex;font-size:10px;font-style:normal;font-weight:950;height:28px;justify-content:center;width:28px}} {root} .qps-targets b{{font-size:23px}} {root} .qps-targets span{{color:var(--m);font-size:13px;min-height:34px}} {root} .qps-targets strong{{color:#4ade80;font-size:13px;text-transform:uppercase}} {root} .qps-targets .is-locked strong{{color:#fbbf24}}
    {root} .qps-credential{{align-items:center;background:var(--s2);border:1px solid var(--b);border-radius:10px;display:grid;gap:18px;grid-template-columns:minmax(180px,.6fr) minmax(0,1.4fr);padding:14px}} {root} .qps-credential>div{{display:grid;gap:4px}} {root} .qps-credential b{{overflow-wrap:anywhere}} {root} .qps-credential p{{color:var(--m);font-size:14px;line-height:1.5;margin:0}} {root} .qps-reading{{display:flex;flex-wrap:wrap;gap:8px;margin-top:12px}} {root} .qps-reading b,{root} .qps-reading span{{border:1px solid var(--b);border-radius:999px;font-size:12px;padding:7px 9px}} {root} .qps-reading b{{background:var(--p);border-color:var(--p);color:white}}
    @media(max-width:700px){{{root} header{{display:grid}} {root} .qps-targets,{root} .qps-credential{{grid-template-columns:1fr}}}}
    </style>
    """


__all__ = ["render_pipeline_guide", "render_pipeline_status"]
