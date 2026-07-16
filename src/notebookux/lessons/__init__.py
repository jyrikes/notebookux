from __future__ import annotations

from collections.abc import Callable
from html import escape

DAVID_IMAGE = "https://upload.wikimedia.org/wikipedia/commons/0/04/David_Deutsch.jpg"
JOZSA_IMAGE = "https://mediadepot.fra1.digitaloceanspaces.com/kingscamapps/s3fs-public/web-images/People/Fellows/richard-jozsa.jpg"
VAZIRANI_IMAGE = "https://www2.eecs.berkeley.edu/Faculty/Photos/Homepages/vazirani.jpg"


def _math(value: str) -> str:
    return f'<span class="lx-math">{value}</span>'


def _author(
    name: str,
    initials: str,
    contribution: str,
    institution: str,
    paper: str,
    year: str,
    profile_url: str,
    image_url: str = "",
    image_credit: str = "",
) -> str:
    if image_url:
        media = f"""
        <img src="{escape(image_url)}" loading="lazy" alt="Retrato de {escape(name)}"
             onerror="this.hidden=true;this.nextElementSibling.hidden=false">
        <span class="lx-avatar" hidden>{escape(initials)}</span>
        """
    else:
        media = f'<span class="lx-avatar">{escape(initials)}</span>'
    credit = f'<small>{image_credit}</small>' if image_credit else ""
    return f"""
    <article class="lx-author">
      <div class="lx-portrait">{media}</div>
      <div>
        <div class="lx-kicker">Quem criou</div>
        <h3>{escape(name)}</h3>
        <p>{contribution}</p>
        <div class="lx-meta"><span>{escape(institution)}</span><span>{escape(year)}</span></div>
        <p class="lx-paper">{paper}</p>
        <a href="{escape(profile_url)}" target="_blank" rel="noopener">Fonte e perfil ↗</a>
        {credit}
      </div>
    </article>
    """


def _question(title: str, prompt: str, hint: str, solution: str) -> str:
    return f"""
    <section class="lx-question">
      <div class="lx-kicker">Teste sua compreensão</div>
      <h3>{title}</h3>
      <p>{prompt}</p>
      <div class="lx-question-actions">
        <button type="button" data-lx-reveal="hint">Ver pista</button>
        <button type="button" data-lx-reveal="solution">Mostrar solução</button>
      </div>
      <div class="lx-reveal" data-lx-panel="hint" hidden><strong>Pista:</strong> {hint}</div>
      <div class="lx-reveal lx-solution" data-lx-panel="solution" hidden><strong>Solução:</strong> {solution}</div>
    </section>
    """


def _steps(items: list[tuple[str, str]]) -> str:
    return '<div class="lx-steps">' + "".join(
        f'<article><b>{index:02d}</b><div><h3>{title}</h3><p>{body}</p></div></article>'
        for index, (title, body) in enumerate(items, 1)
    ) + "</div>"


def _function_lab() -> str:
    cards = "".join(
        f'<button type="button" data-lx-function="{outputs}"><strong>f{index}(x)</strong><span>0 → {outputs[0]}</span><span>1 → {outputs[1]}</span></button>'
        for index, outputs in enumerate(("00", "01", "10", "11"), 1)
    )
    return f"""
    <div class="lx-function-lab">
      <div class="lx-function-grid">{cards}</div>
      <div class="lx-manual-result">
        <div class="lx-kicker">Cálculo manual</div>
        <div id="lx-function-name">f1: constante</div>
        <div class="lx-route"><span>x=0</span><i></i><strong id="lx-function-0">f(0)=0</strong></div>
        <div class="lx-route"><span>x=1</span><i></i><strong id="lx-function-1">f(1)=0</strong></div>
      </div>
    </div>
    """


def _bitstring_lab() -> str:
    bits = "".join(f'<button type="button" data-lx-dj-bit="{i}">0</button>' for i in range(4))
    return f"""
    <div class="lx-bit-lab">
      <div><div class="lx-kicker">Edite a medida</div><div class="lx-bits">{bits}</div></div>
      <div class="lx-manual-result"><strong id="lx-dj-class">0000 → função constante</strong><p>Todos os bits 0 indicam constante; qualquer 1 indica balanceada.</p></div>
    </div>
    """


def _bv_lab() -> str:
    xbits = "".join(f'<button type="button" data-lx-bv-x="{i}">0</button>' for i in range(4))
    sbits = "".join(f'<button type="button" data-lx-bv-s="{i}">{v}</button>' for i, v in enumerate("1011"))
    return f"""
    <div class="lx-bv-lab">
      <div><span>entrada x</span><div class="lx-bits">{xbits}</div></div>
      <div><span>segredo s</span><div class="lx-bits">{sbits}</div></div>
      <div class="lx-equation" id="lx-bv-result">f(x)=x·s mod 2 = 0</div>
      <p>Clique nos bits. O cálculo faz AND posição a posição e depois XOR dos resultados.</p>
    </div>
    """


def _circuit_lab(kind: str) -> str:
    circuits = {
        "deutsch": {
            "wires": (("entrada", "|0⟩", ("H", "U<sub>f</sub>", "H", "M")),
                      ("auxiliar", "|1⟩", ("H", "U<sub>f</sub>", "·", "·"))),
            "notes": (
                "Comece com o qubit de entrada em |0⟩ e o auxiliar em |1⟩.",
                "H cria os ramos x=0 e x=1; no auxiliar, prepara (|0⟩−|1⟩)/√2.",
                "U<sub>f</sub> é consultado uma vez e grava f(x) no sinal da amplitude.",
                "A última H faz as fases interferirem: 0 significa constante e 1, balanceada.",
            ),
        },
        "dj": {
            "wires": (("registro x", "|0⟩<sup>⊗n</sup>", ("H<sup>⊗n</sup>", "U<sub>f</sub>", "H<sup>⊗n</sup>", "M<sup>⊗n</sup>")),
                      ("auxiliar", "|1⟩", ("H", "U<sub>f</sub>", "·", "·"))),
            "notes": (
                "Use n qubits em |0⟩ e um auxiliar em |1⟩.",
                "A primeira camada H cria uma superposição uniforme das 2ⁿ entradas.",
                "Uma única chamada a U<sub>f</sub> associa a cada entrada a fase (−1)<sup>f(x)</sup>.",
                "A segunda H soma as fases: 0…0 indica constante; qualquer 1 indica balanceada.",
            ),
        },
        "bv": {
            "wires": (("registro x", "|0⟩<sup>⊗n</sup>", ("H<sup>⊗n</sup>", "U<sub>f(s)</sub>", "H<sup>⊗n</sup>", "M<sup>⊗n</sup>")),
                      ("auxiliar", "|1⟩", ("H", "U<sub>f(s)</sub>", "·", "·"))),
            "notes": (
                "Prepare n qubits de entrada em |0⟩ e o auxiliar em |1⟩.",
                "H distribui a amplitude igualmente entre todas as entradas x.",
                "U<sub>f(s)</sub> escreve a fase (−1)<sup>s·x</sup> sem revelar s diretamente.",
                "A última H cancela todo estado diferente de s; a medida devolve a string secreta.",
            ),
        },
    }
    config = circuits[kind]
    controls = "".join(
        f'<button type="button" data-lx-circuit-step="{index}">{index + 1}. {label}</button>'
        for index, label in enumerate(("Preparar", "Superpor", "Consultar", "Interferir e medir"))
    )
    wires = "".join(
        '<div class="lx-wire">'
        f'<span class="lx-wire-name"><b>{name}</b><small>{initial}</small></span>'
        + "".join(
            f'<span class="lx-node" data-lx-stage="{stage}"><b class="lx-gate">{gate}</b></span>'
            for stage, gate in enumerate(gates, 1)
        )
        + '<span class="lx-wire-end">saída</span></div>'
        for name, initial, gates in config["wires"]
    )
    notes = "".join(f'<span data-lx-circuit-copy="{i}">{note}</span>' for i, note in enumerate(config["notes"]))
    return f"""
    <section class="lx-circuit-lab" data-lx-circuit="{kind}">
      <div class="lx-kicker">Monte o circuito passo a passo</div>
      <div class="lx-circuit-controls">{controls}</div>
      <div class="lx-circuit-board">{wires}</div>
      <div class="lx-circuit-note" data-lx-circuit-note>{notes}</div>
    </section>
    """


def _probability_lab(kind: str) -> str:
    if kind == "deutsch":
        options = '<div class="lx-sim-options"><span>Oráculo:</span>' + "".join(
            f'<button type="button" data-lx-function="{outputs}">f{i}</button>'
            for i, outputs in enumerate(("00", "01", "10", "11"), 1)
        ) + "</div>"
    elif kind == "dj":
        options = """
        <div class="lx-sim-options"><span>Promessa:</span>
          <button type="button" data-lx-dj-case="constant">constante</button>
          <button type="button" data-lx-dj-case="balanced">balanceada</button>
        </div>
        """
    else:
        options = '<div class="lx-sim-options"><span>Segredo s:</span><div class="lx-bits">' + "".join(
            f'<button type="button" data-lx-bv-s="{i}">{v}</button>' for i, v in enumerate("1011")
        ) + "</div></div>"
    shots = "".join(f'<button type="button" data-lx-run-sim="{n}">{n} shots</button>' for n in (1, 32, 256, 1024))
    return f"""
    <section class="lx-simulator" data-lx-simulator="{kind}">
      <div class="lx-kicker">Simulador probabilístico</div>
      <p>Escolha o caso, a quantidade de shots e um ruído didático de leitura. O circuito ideal concentra 100% no resultado correto.</p>
      {options}
      <div class="lx-sim-controls">{shots}
        <label>ruído <select data-lx-noise><option value="0">0%</option><option value="0.02">2%</option><option value="0.05">5%</option><option value="0.1">10%</option></select></label>
      </div>
      <div class="lx-prob-chart" aria-live="polite">
        <div class="lx-prob-row"><span data-lx-result-label>resultado correto</span><i><b data-lx-result-bar></b></i><strong data-lx-result-count>aguardando</strong></div>
        <div class="lx-prob-row"><span>outros estados</span><i><b data-lx-other-bar></b></i><strong data-lx-other-count>aguardando</strong></div>
      </div>
      <small>O ruído acima é uma aproximação binomial para exploração visual; não substitui o modelo físico do backend IBM.</small>
    </section>
    """


def _parallelism_circuit(ux) -> list[dict[str, str]]:
    return [
        ux.screen("Da base para a superposição", _steps([
            ("Estado inicial", f'O qubit 0 começa em {_math("|0⟩")}.'),
            ("Porta Hadamard", f'H transforma a entrada em {_math("1/√2 (|0⟩ + |1⟩)")}.'),
            ("Oráculo", f'A porta {_math("U<sub>f</sub>")} avalia f(x) e aplica o resultado ao qubit 1.'),
        ])),
        ux.screen("Exemplo manual com as quatro funções", '<p>Escolha uma função e acompanhe separadamente as trajetórias de x=0 e x=1.</p>' + _function_lab()),
        ux.screen("Próxima etapa do fluxo", '<div class="lx-callout"><strong>Mapear não basta.</strong><p>Depois de construir o circuito, ele precisa ser otimizado e transpilado para as instruções e conexões disponíveis no backend escolhido.</p></div>'),
    ]


def _measurement_limits(ux) -> list[dict[str, str]]:
    q = _question(
        "Quantas execuções recuperam toda a função?",
        "Uma medida revela somente um dos ramos. Quantas vezes devemos executar o circuito para obter f(0) e f(1)? Isso supera o caso clássico?",
        "Depois de medir, anote qual x apareceu. Uma segunda execução pode repetir o mesmo x.",
        "São necessárias pelo menos duas execuções, mas duas não garantem observar os dois valores porque a medida é probabilística. No melhor caso empata com as duas consultas clássicas; por isso o computador clássico é preferível para recuperar toda a tabela dessa função.",
    )
    return [
        ux.screen("Como ler o histograma", '<p>As barras representam os estados dos dois qubits em cada shot. O Qiskit usa little endian: q0 aparece à direita e os qubits são lidos da direita para a esquerda.</p><div class="lx-equation">q1 q0 &nbsp;=&nbsp; saída entrada</div>'),
        ux.screen("Uma execução revela um ramo", '<p>A superposição permite avaliar x=0 e x=1 durante a evolução, mas a medição colapsa o estado.</p><div class="lx-shot-lab"><button type="button" data-lx-shots="1">Rodar 1 shot</button><button type="button" data-lx-shots="16">Rodar 16 shots</button><div id="lx-shot-result">Escolha a quantidade de shots.</div></div>'),
        ux.screen("Teste e solução", q + '<div class="lx-takeaway">Paralelismo quântico não é um processador paralelo clássico massivo: a leitura final continua limitada pela medição.</div>'),
    ]


def _deutsch_problem(ux) -> list[dict[str, str]]:
    author = _author(
        "David Deutsch", "DD",
        "Físico de Oxford e um dos fundadores da teoria da computação quântica. O caso n=1 introduziu a comparação entre funções constantes e balanceadas.",
        "University of Oxford", "1985",
        "Quantum theory, the Church–Turing principle and the universal quantum computer",
        "https://www.physics.ox.ac.uk/our-people/deutsch", DAVID_IMAGE,
        "Imagem: Simon Benjamin, CC BY 3.0, Wikimedia Commons.",
    )
    return [
        ux.screen("Interferência cria a vantagem", '<p>O paralelismo sozinho não basta. Deutsch combinou superposição e interferência para extrair uma propriedade global da função com uma consulta.</p><div class="lx-concept">superposição <i></i> fase <i></i> interferência <i></i> classe</div>'),
        ux.screen("O problema", '<p>Dado x∈{0,1} e f(x)∈{0,1}, determine se f é constante ou balanceada. Constante significa saídas iguais; balanceada significa saídas diferentes.</p>' + _function_lab()),
        ux.screen("Quem criou", author),
    ]


def _deutsch_algorithm(ux) -> list[dict[str, str]]:
    questions = "".join([
        _question("Qual é o estado π1?", "Aplique H a |0⟩ e H a |1⟩.", "H|0⟩ cria soma e H|1⟩ cria diferença.", "π1 = [(|0⟩−|1⟩)/√2][(|0⟩+|1⟩)/√2]."),
        _question("Qual é o estado π2?", "O que Uf muda quando f(0)=f(1) ou f(0)≠f(1)?", "Observe o sinal relativo entre os termos x=0 e x=1.", "Se f(0)=f(1), o sinal relativo permanece positivo. Se são diferentes, surge um sinal negativo no ramo x=1: esse é o phase-kickback."),
        _question("Qual é o estado π3?", "Aplique a última H ao qubit de entrada.", "H transforma soma em |0⟩ e diferença em |1⟩.", "A medida retorna 0 para função constante e 1 para função balanceada, usando apenas uma consulta ao oráculo."),
    ])
    return [
        ux.screen("Modelo de consulta", '<p>A função fica em uma caixa-preta. Não vemos sua implementação; podemos apenas consultar o oráculo Uf. O custo é medido pelo número de consultas.</p><div class="lx-oracle"><span>|x⟩</span><i></i><b>U<sub>f</sub></b><i></i><span>classe</span></div>'),
        ux.screen("Circuito passo a passo", _circuit_lab("deutsch")),
        ux.screen("Simule as medidas", _probability_lab("deutsch")),
        ux.screen("Respostas guiadas", questions),
        ux.screen("Por que uma consulta basta", '<div class="lx-takeaway"><strong>Clássico:</strong> consulta f(0) e f(1). <strong>Quântico:</strong> prepara os dois ramos, deixa as fases interferirem e mede somente a propriedade “igual ou diferente”.</div>'),
    ]


def _dj_overview(ux) -> list[dict[str, str]]:
    authors = _author("David Deutsch", "DD", "Criou o caso inicial de um bit e o modelo quântico universal.", "Oxford", "1985", "Quantum theory and the universal quantum computer", "https://www.physics.ox.ac.uk/our-people/deutsch", DAVID_IMAGE, "CC BY 3.0, Wikimedia Commons.")
    authors += _author("Richard Jozsa", "RJ", "Generalizou com Deutsch o problema para n bits, produzindo uma separação exponencial em relação ao algoritmo clássico determinístico.", "University of Cambridge", "1992", "Rapid Solution of Problems by Quantum Computation", "https://www.kings.cam.ac.uk/people/richard-jozsa", JOZSA_IMAGE, "Imagem: King's College, Cambridge.")
    return [
        ux.screen("De um bit para n bits", '<p>Deutsch–Jozsa recebe uma função de n bits para um bit, prometida constante ou balanceada. Balanceada retorna 0 para metade das entradas e 1 para a outra metade.</p><div class="lx-equation">f: {0,1}<sup>n</sup> → {0,1}</div>'),
        ux.screen("Construa o circuito", _circuit_lab("dj")),
        ux.screen("Regra da saída", '<p>Phase-kickback e interferência concentram a resposta na medida: todos os bits 0 indicam constante; pelo menos um bit 1 indica balanceada.</p>' + _bitstring_lab()),
        ux.screen("Simule as probabilidades", _probability_lab("dj")),
        ux.screen("Custo de consulta", '<div class="lx-query-compare"><article><b>Clássico determinístico</b><strong>2<sup>n−1</sup> + 1</strong><span>pior caso</span></article><article><b>Quântico</b><strong>1</strong><span>consulta</span></article></div>'),
        ux.screen("Quem criou", '<div class="lx-author-grid">' + authors + '</div>'),
    ]


def _oracle_inspection(ux) -> list[dict[str, str]]:
    return [
        ux.screen("O que observar no oráculo", '<p>O circuito gerado é garantido constante ou balanceado. Em vez de decorar portas, pergunte: a saída muda quando os bits de entrada mudam?</p>' + _steps([("Independente", "Se o último qubit recebe sempre o mesmo valor, a função é constante."),("Dependente", "Se alguma entrada controla a saída, a função pode ser balanceada."),("Confirme", "Teste pares de entradas e conte zeros e uns.")])),
        ux.screen("Classifique manualmente", '<p>Edite a saída teórica do algoritmo. A regra da medida permite classificar sem abrir a caixa-preta.</p>' + _bitstring_lab()),
        ux.screen("Por que o código é complexo", '<div class="lx-callout"><strong>O gerador do oráculo não é o algoritmo.</strong><p>Ele apenas produz uma função que satisfaz a promessa. O circuito Deutsch–Jozsa é a parte que decide a classe com uma consulta.</p></div>'),
    ]


def _dj_results(ux) -> list[dict[str, str]]:
    questions = _question("Quantas consultas clássicas garantem a resposta?", "Considere o pior caso com 2ⁿ entradas.", "Uma função balanceada pode imitar uma constante até metade das entradas.", "No pior caso são necessárias 2ⁿ/2 + 1 consultas. Só depois de ultrapassar metade com a mesma saída podemos excluir uma função balanceada.")
    questions += _question("E se bastar a resposta mais provável?", "Compare apenas duas saídas clássicas.", "Saídas diferentes provam balanceamento; saídas iguais tornam constante mais provável.", "Duas consultas já dão uma decisão probabilística. Se forem diferentes, a função é balanceada; se forem iguais, constante é mais provável, mas não há certeza.")
    return [
        ux.screen("Interprete sua bitstring", '<p>A primeira linha do resultado é a string medida. Todos os zeros significam constante; qualquer 1 significa balanceada.</p>' + _bitstring_lab()),
        ux.screen("Aceleração e limite", '<p>Deutsch–Jozsa oferece aceleração exponencial sobre algoritmos clássicos determinísticos, mas não uma vantagem significativa sobre uma estratégia clássica probabilística que aceita erro.</p><div class="lx-query-compare"><article><b>certeza clássica</b><strong>2<sup>n−1</sup>+1</strong></article><article><b>certeza quântica</b><strong>1</strong></article></div>'),
        ux.screen("Respostas guiadas", questions),
    ]


def _bernstein_vazirani(ux) -> list[dict[str, str]]:
    authors = _author("Ethan Bernstein", "EB", "Coautor da formulação de complexidade quântica e do problema de recuperar uma string oculta.", "Teoria da computação", "1997", "Quantum Complexity Theory", "https://epubs.siam.org/doi/abs/10.1137/S0097539796300921")
    authors += _author("Umesh Vazirani", "UV", "Professor de Berkeley, com pesquisa em algoritmos, complexidade e computação quântica.", "UC Berkeley", "1997", "Quantum Complexity Theory", "https://www2.eecs.berkeley.edu/Faculty/Homepages/vazirani.html", VAZIRANI_IMAGE, "Imagem: UC Berkeley EECS.")
    questions = _question("Verifique o caso n=1", "Mostre que a interferência deixa o estado |s⟩.", "Teste separadamente s=0 e s=1 nos quatro termos da soma.", "Para s=0, os termos de |0⟩ somam e os de |1⟩ cancelam. Para s=1 ocorre o contrário. Em ambos os casos o registrador termina em |s⟩.")
    questions += _question("Por que o mesmo circuito resolve DJ e BV?", "Analise f(x)=s·x quando s é zero e quando contém algum 1.", "s=00…0 produz sempre zero.", "Se s=00…0, a função é constante. Para qualquer outro s, o produto binário é balanceado. Assim o circuito retorna a própria string e, ao mesmo tempo, sua classe DJ.")
    return [
        ux.screen("O problema da string secreta", '<p>A função recebe x e devolve o produto escalar binário com uma string desconhecida s: f(x)=s·x mod 2. O objetivo é descobrir todos os bits de s.</p>' + _bv_lab()),
        ux.screen("Cálculo quântico em quatro passos", _circuit_lab("bv")),
        ux.screen("Simule a recuperação de s", _probability_lab("bv")),
        ux.screen("Quem criou", '<div class="lx-author-grid">' + authors + '</div>'),
        ux.screen("Respostas guiadas", questions),
        ux.screen("Vantagem de consulta", '<div class="lx-query-compare"><article><b>Clássico</b><strong>n</strong><span>consultas</span></article><article><b>Quântico</b><strong>1</strong><span>consulta</span></article></div>'),
    ]


def _algorithm_recap(ux) -> list[dict[str, str]]:
    return [
        ux.screen("Três perguntas, uma mesma arquitetura", '<div class="lx-recap"><article><b>Deutsch</b><span>As duas saídas são iguais?</span><strong>1 consulta</strong></article><article><b>Deutsch–Jozsa</b><span>A função n-bit é constante ou balanceada?</span><strong>1 consulta</strong></article><article><b>Bernstein–Vazirani</b><span>Qual é a string secreta s?</span><strong>1 consulta</strong></article></div>'),
        ux.screen("O mecanismo comum", '<div class="lx-concept">superposição <i></i> oráculo <i></i> phase-kickback <i></i> interferência</div><p>O ganho não vem de ler todas as respostas, mas de fazer amplitudes se cancelarem ou se reforçarem até que a propriedade desejada fique mensurável.</p>'),
        ux.screen("Linha histórica", _steps([("1985 — Deutsch", "Computador quântico universal e primeiro problema de consulta."),("1992 — Deutsch e Jozsa", "Generalização e separação exponencial determinística."),("1997 — Bernstein e Vazirani", "Complexidade quântica e recuperação da string oculta."),("Depois", "Amostragem de Fourier recursiva e algoritmos como o de Shor ampliaram a vantagem quântica.")])),
        ux.screen("Conclusão", '<div class="lx-takeaway">Superposição cria possibilidades; o oráculo escreve informação em fases; interferência seleciona a propriedade útil; a medição entrega a resposta final.</div>'),
    ]


_BUILDERS: dict[str, Callable] = {
    "parallelism-circuit": _parallelism_circuit,
    "measurement-limits": _measurement_limits,
    "deutsch-problem": _deutsch_problem,
    "deutsch-algorithm": _deutsch_algorithm,
    "deutsch-jozsa-overview": _dj_overview,
    "dj-oracle-inspection": _oracle_inspection,
    "dj-results": _dj_results,
    "bernstein-vazirani": _bernstein_vazirani,
    "algorithm-recap": _algorithm_recap,
}

_TITLES = {
    "parallelism-circuit": "Paralelismo: do estado ao circuito",
    "measurement-limits": "Medição e limites do paralelismo",
    "deutsch-problem": "O problema de Deutsch",
    "deutsch-algorithm": "O algoritmo de Deutsch",
    "deutsch-jozsa-overview": "O algoritmo de Deutsch–Jozsa",
    "dj-oracle-inspection": "Como interpretar o oráculo",
    "dj-results": "Como interpretar os resultados",
    "bernstein-vazirani": "O problema de Bernstein–Vazirani",
    "algorithm-recap": "Síntese dos algoritmos",
}


def available_algorithm_lessons() -> tuple[str, ...]:
    return tuple(_BUILDERS)


def render_algorithm_lesson(ux, lesson_id: str) -> None:
    """Render one self-contained algorithm lesson using the NotebookUX module pattern."""
    if lesson_id not in _BUILDERS:
        choices = ", ".join(_BUILDERS)
        raise ValueError(f"Unknown lesson_id {lesson_id!r}. Available lessons: {choices}")
    module_id = f"algorithm-{lesson_id}"
    title = _TITLES[lesson_id]
    screens = _BUILDERS[lesson_id](ux)
    ux.wrap(_style(ux, module_id) + ux.module_html(title, screens, module_id=module_id) + _script(module_id))


def _style(ux, module_id: str) -> str:
    t = ux.theme
    root = f"#{module_id}"
    return f"""
    <style>
    {root} {{--p:{t['primary']};--a:{t['accent']};--s:{t['surface']};--s2:{t['surface_2']};--b:{t['border']};--tx:{t['text']};--m:{t['muted']};overflow:hidden}}
    {root} *{{box-sizing:border-box}} {root}_content{{min-height:0;padding:clamp(18px,2.4vw,28px)!important}}
    {root}_content>div:first-child{{font-size:clamp(27px,3vw,34px)!important;margin-bottom:16px!important}}
    {root} p{{font-size:clamp(18px,1.6vw,21px);line-height:1.72;margin:0 0 16px}} {root} h3{{font-size:21px;margin:4px 0 10px}}
    {root} button{{font:inherit}} {root} .lx-kicker{{color:var(--p);font-size:12px;font-weight:950;letter-spacing:.12em;text-transform:uppercase}}
    {root} .lx-math,{root} .lx-equation{{background:var(--s2);border:1px solid var(--b);border-radius:8px;font-family:Georgia,serif;font-weight:750;padding:3px 8px}}
    {root} .lx-equation{{font-size:clamp(22px,3vw,32px);padding:18px;text-align:center}}
    {root} .lx-steps{{display:grid;gap:12px}} {root} .lx-steps article{{align-items:start;background:var(--s2);border:1px solid var(--b);border-radius:11px;display:grid;gap:14px;grid-template-columns:44px 1fr;padding:16px}}
    {root} .lx-steps article>b{{align-items:center;background:var(--p);border-radius:50%;color:white;display:flex;height:40px;justify-content:center}}
    {root} .lx-steps p{{font-size:17px;margin:0}} {root} .lx-function-lab{{display:grid;gap:18px;grid-template-columns:1fr 1fr}}
    {root} .lx-function-grid{{display:grid;gap:10px;grid-template-columns:1fr 1fr}} {root} .lx-function-grid button{{background:var(--s2);border:1px solid var(--b);border-radius:10px;color:var(--tx);cursor:pointer;display:grid;gap:6px;padding:14px;text-align:left}}
    {root} .lx-function-grid button[aria-pressed=true]{{border:2px solid var(--p)}} {root} .lx-function-grid strong{{color:var(--p);font-size:18px}}
    {root} .lx-manual-result,{root} .lx-callout,{root} .lx-takeaway,{root} .lx-bv-lab{{background:var(--s2);border:1px solid var(--b);border-left:5px solid var(--a);border-radius:10px;padding:18px}}
    {root} .lx-route{{align-items:center;display:grid;gap:10px;grid-template-columns:55px 1fr 80px;margin-top:15px}} {root} .lx-route i{{background:linear-gradient(90deg,var(--p),var(--a));height:3px}}
    {root} .lx-question{{background:var(--s2);border:1px solid var(--b);border-radius:12px;margin-bottom:16px;padding:18px}} {root} .lx-question-actions{{display:flex;flex-wrap:wrap;gap:9px}}
    {root} .lx-question button,{root} .lx-shot-lab button{{background:var(--s);border:1px solid var(--p);border-radius:999px;color:var(--tx);cursor:pointer;font-weight:850;padding:9px 14px}}
    {root} .lx-reveal{{border-left:4px solid var(--p);font-size:17px;line-height:1.65;margin-top:14px;padding:12px 14px}} {root} .lx-solution{{border-left-color:var(--a)}}
    {root} .lx-author{{align-items:center;background:var(--s2);border:1px solid var(--b);border-radius:12px;display:grid;gap:20px;grid-template-columns:180px 1fr;padding:20px}}
    {root} .lx-portrait img,{root} .lx-avatar{{border-radius:12px;display:block;height:210px;object-fit:cover;width:100%}} {root} .lx-avatar{{align-items:center;background:linear-gradient(145deg,var(--p),var(--a));color:white;display:flex;font-size:48px;font-weight:950;justify-content:center}}
    {root} .lx-author p{{font-size:17px}} {root} .lx-author a{{color:var(--p);font-weight:850}} {root} .lx-author small{{color:var(--m);display:block;margin-top:7px}}
    {root} .lx-meta{{display:flex;flex-wrap:wrap;gap:8px}} {root} .lx-meta span{{background:var(--s);border:1px solid var(--b);border-radius:999px;padding:5px 9px}}
    {root} .lx-author-grid{{display:grid;gap:14px}} {root} .lx-concept{{align-items:center;display:flex;flex-wrap:wrap;font-size:18px;font-weight:900;gap:10px;margin:20px 0}} {root} .lx-concept i{{background:var(--a);height:3px;min-width:35px}}
    {root} .lx-oracle{{align-items:center;display:grid;gap:12px;grid-template-columns:auto 1fr 85px 1fr auto;margin:30px 0}} {root} .lx-oracle i{{background:var(--b);height:3px}} {root} .lx-oracle b{{background:var(--p);border-radius:9px;color:white;font-size:28px;padding:25px;text-align:center}}
    {root} .lx-bits{{display:flex;gap:8px;margin:9px 0}} {root} .lx-bits button{{background:var(--s2);border:1px solid var(--b);border-radius:8px;color:var(--tx);cursor:pointer;font-size:21px;font-weight:950;height:46px;width:46px}}
    {root} .lx-bits button[data-on=true]{{background:var(--p);color:white}} {root} .lx-bit-lab,{root} .lx-measure-lab{{display:grid;gap:18px;grid-template-columns:1fr 1fr}}
    {root} .lx-query-compare,{root} .lx-recap{{display:grid;gap:14px;grid-template-columns:repeat(auto-fit,minmax(190px,1fr))}} {root} .lx-query-compare article,{root} .lx-recap article{{background:var(--s2);border:1px solid var(--b);border-radius:11px;display:grid;gap:10px;padding:20px}}
    {root} .lx-query-compare strong,{root} .lx-recap strong{{color:var(--a);font-size:30px}} {root} .lx-shot-lab{{display:flex;flex-wrap:wrap;gap:10px}} {root} #lx-shot-result{{flex-basis:100%;font-size:20px;margin-top:12px}}
    {root} .lx-circuit-lab,{root} .lx-simulator{{background:var(--s2);border:1px solid var(--b);border-radius:14px;padding:clamp(15px,2.2vw,24px)}}
    {root} .lx-circuit-controls,{root} .lx-sim-controls,{root} .lx-sim-options{{align-items:center;display:flex;flex-wrap:wrap;gap:9px;margin:14px 0}}
    {root} .lx-circuit-controls button,{root} .lx-sim-controls button,{root} .lx-sim-options button{{background:var(--s);border:1px solid var(--b);border-radius:8px;color:var(--tx);cursor:pointer;font-weight:850;padding:9px 12px}}
    {root} .lx-circuit-controls button[aria-pressed=true],{root} .lx-sim-options button[aria-pressed=true]{{background:var(--p);border-color:var(--p);color:white}}
    {root} .lx-circuit-board{{background:var(--s);border:1px solid var(--b);border-radius:11px;padding:13px}}
    {root} .lx-wire{{align-items:stretch;display:grid;grid-template-columns:minmax(72px,1.2fr) repeat(4,minmax(48px,1fr)) minmax(38px,.7fr);min-width:0}}
    {root} .lx-wire-name,{root} .lx-wire-end{{align-items:center;display:flex;flex-direction:column;justify-content:center;min-width:0;padding:6px;text-align:center}}
    {root} .lx-wire-name small{{color:var(--m);font-family:Georgia,serif}} {root} .lx-wire-end{{color:var(--m);font-size:12px}}
    {root} .lx-node{{align-items:center;display:flex;justify-content:center;min-height:70px;opacity:.22;position:relative;transition:opacity .25s ease,transform .25s ease}}
    {root} .lx-node:before{{background:var(--b);content:"";height:2px;left:0;position:absolute;right:0;top:50%}}
    {root} .lx-node[data-on=true]{{opacity:1;transform:translateY(-1px)}}
    {root} .lx-gate{{align-items:center;background:var(--p);border:2px solid color-mix(in srgb,var(--p),white 22%);border-radius:8px;color:white;display:flex;font-size:clamp(12px,1.5vw,17px);justify-content:center;min-height:44px;min-width:42px;padding:5px;position:relative;text-align:center;z-index:1}}
    {root} .lx-gate:has(>sub){{background:var(--a)}} {root} .lx-circuit-note{{border-left:4px solid var(--a);font-size:18px;line-height:1.55;margin-top:14px;padding:10px 13px}}
    {root} .lx-circuit-note span{{display:none}} {root} .lx-circuit-note span[data-on=true]{{display:inline}}
    {root} .lx-sim-options>span{{font-weight:900}} {root} .lx-sim-controls label{{align-items:center;display:flex;font-weight:850;gap:7px;margin-left:auto}}
    {root} .lx-sim-controls select{{background:var(--s);border:1px solid var(--b);border-radius:8px;color:var(--tx);padding:8px}}
    {root} .lx-prob-chart{{display:grid;gap:13px;margin:22px 0 12px}} {root} .lx-prob-row{{align-items:center;display:grid;gap:11px;grid-template-columns:minmax(105px,1fr) minmax(130px,3fr) minmax(76px,.8fr)}}
    {root} .lx-prob-row>span{{font-weight:850}} {root} .lx-prob-row>i{{background:var(--s);border:1px solid var(--b);border-radius:999px;height:22px;overflow:hidden}}
    {root} .lx-prob-row>i>b{{background:linear-gradient(90deg,var(--p),var(--a));display:block;height:100%;transition:width .35s ease;width:0}}
    {root} .lx-prob-row:nth-child(2)>i>b{{background:color-mix(in srgb,var(--m),transparent 35%)}} {root} .lx-prob-row>strong{{font-variant-numeric:tabular-nums;text-align:right}}
    {root} .lx-simulator>small{{color:var(--m);display:block;line-height:1.5}}
    @media(max-width:760px){{{root} .lx-function-lab,{root} .lx-bit-lab,{root} .lx-author{{grid-template-columns:1fr}} {root} .lx-portrait{{max-width:240px}} {root} .lx-function-grid{{grid-template-columns:1fr}} {root} .lx-wire{{grid-template-columns:minmax(58px,1fr) repeat(4,minmax(38px,1fr)) 30px}} {root} .lx-wire-name b{{font-size:11px}} {root} .lx-gate{{font-size:11px;min-width:34px;padding:3px}} {root} .lx-prob-row{{grid-template-columns:1fr}} {root} .lx-prob-row>strong{{text-align:left}} {root} .lx-sim-controls label{{margin-left:0}}}}
    </style>
    """


def _script(module_id: str) -> str:
    return f"""
    <script>(()=>{{
      const root=document.getElementById({module_id!r}); if(!root)return;
      const state={{fn:'00',dj:[0,0,0,0],djCase:'constant',x:[0,0,0,0],s:[1,0,1,1],circuitStep:0}};
      const resultLabel=sim=>{{
        if(sim.dataset.lxSimulator==='deutsch')return `${{state.fn[0]===state.fn[1]?'0 · constante':'1 · balanceada'}}`;
        if(sim.dataset.lxSimulator==='dj')return state.djCase==='constant'?'0000 · constante':'1010 · balanceada';
        return `${{state.s.join('')}} · segredo s`;
      }};
      const resetSimulator=()=>root.querySelectorAll('[data-lx-simulator]').forEach(sim=>{{
        sim.querySelector('[data-lx-result-label]').textContent=resultLabel(sim);
        for(const k of ['result','other']){{sim.querySelector(`[data-lx-${{k}}-bar]`).style.width='0';sim.querySelector(`[data-lx-${{k}}-count]`).textContent='aguardando';}}
      }});
      const hydrate=()=>{{
        root.querySelectorAll('[data-lx-function]').forEach(b=>b.setAttribute('aria-pressed',b.dataset.lxFunction===state.fn));
        root.querySelectorAll('[data-lx-dj-case]').forEach(b=>b.setAttribute('aria-pressed',b.dataset.lxDjCase===state.djCase));
        const name=root.querySelector('#lx-function-name'); if(name){{const i=['00','01','10','11'].indexOf(state.fn)+1;name.textContent=`f${{i}}: ${{state.fn[0]===state.fn[1]?'constante':'balanceada'}}`;root.querySelector('#lx-function-0').textContent=`f(0)=${{state.fn[0]}}`;root.querySelector('#lx-function-1').textContent=`f(1)=${{state.fn[1]}}`;}}
        root.querySelectorAll('[data-lx-dj-bit]').forEach(b=>{{const v=state.dj[+b.dataset.lxDjBit];b.textContent=v;b.dataset.on=v===1}}); const dc=root.querySelector('#lx-dj-class');if(dc){{const bits=state.dj.join('');dc.textContent=`${{bits}} → função ${{bits.includes('1')?'balanceada':'constante'}}`;}}
        for(const kind of ['x','s'])root.querySelectorAll(`[data-lx-bv-${{kind}}]`).forEach(b=>{{const v=state[kind][+b.dataset[`lxBv${{kind.toUpperCase()}}`]];b.textContent=v;b.dataset.on=v===1}});
        const bv=root.querySelector('#lx-bv-result');if(bv){{const products=state.x.map((v,i)=>v*state.s[i]);bv.textContent=`f(x)= ${{products.join(' ⊕ ')}} = ${{products.reduce((a,v)=>a^v,0)}}`;}}
        root.querySelectorAll('[data-lx-circuit-step]').forEach(b=>b.setAttribute('aria-pressed',+b.dataset.lxCircuitStep===state.circuitStep));
        root.querySelectorAll('[data-lx-stage]').forEach(n=>n.dataset.on=+n.dataset.lxStage<=state.circuitStep+1);
        root.querySelectorAll('[data-lx-circuit-copy]').forEach(n=>n.dataset.on=+n.dataset.lxCircuitCopy===state.circuitStep);
        root.querySelectorAll('[data-lx-simulator]').forEach(sim=>sim.querySelector('[data-lx-result-label]').textContent=resultLabel(sim));
      }};
      root.addEventListener('click',e=>{{
        const r=e.target.closest('[data-lx-reveal]');if(r){{const q=r.closest('.lx-question');q.querySelector(`[data-lx-panel=${{r.dataset.lxReveal}}]`).hidden=false;return}}
        let changed=false;
        const f=e.target.closest('[data-lx-function]');if(f){{state.fn=f.dataset.lxFunction;changed=true}}
        const dc=e.target.closest('[data-lx-dj-case]');if(dc){{state.djCase=dc.dataset.lxDjCase;changed=true}}
        const d=e.target.closest('[data-lx-dj-bit]');if(d)state.dj[+d.dataset.lxDjBit]^=1;
        for(const k of ['x','s']){{const b=e.target.closest(`[data-lx-bv-${{k}}]`);if(b){{state[k][+b.dataset[`lxBv${{k.toUpperCase()}}`]]^=1;if(k==='s')changed=true}}}}
        const step=e.target.closest('[data-lx-circuit-step]');if(step)state.circuitStep=+step.dataset.lxCircuitStep;
        const sh=e.target.closest('[data-lx-shots]');if(sh){{const n=+sh.dataset.lxShots;let z=0;for(let i=0;i<n;i++)z+=Math.random()<.5;root.querySelector('#lx-shot-result').textContent=`${{n}} shot(s): ramo x=0 apareceu ${{z}} vez(es), x=1 apareceu ${{n-z}} vez(es).`;}}
        const run=e.target.closest('[data-lx-run-sim]');if(run){{
          const sim=run.closest('[data-lx-simulator]'),n=+run.dataset.lxRunSim,noise=+sim.querySelector('[data-lx-noise]').value;
          let correct=0;for(let i=0;i<n;i++)if(Math.random()>=noise)correct++;const other=n-correct,pct=100*correct/n;
          sim.querySelector('[data-lx-result-label]').textContent=resultLabel(sim);sim.querySelector('[data-lx-result-bar]').style.width=`${{pct}}%`;sim.querySelector('[data-lx-other-bar]').style.width=`${{100-pct}}%`;
          sim.querySelector('[data-lx-result-count]').textContent=`${{correct}} · ${{pct.toFixed(1)}}%`;sim.querySelector('[data-lx-other-count]').textContent=`${{other}} · ${{(100-pct).toFixed(1)}}%`;
        }}
        hydrate();if(changed)resetSimulator();
      }});
      const c=document.getElementById({(module_id + '_content')!r});if(c)new MutationObserver(hydrate).observe(c,{{childList:true}});hydrate();
    }})()</script>
    """


__all__ = ["available_algorithm_lessons", "render_algorithm_lesson"]
