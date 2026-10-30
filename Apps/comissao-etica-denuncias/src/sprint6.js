/* ================= Sprint 6 · Documentos, cominação e encerramento · Sprint 7 · Relatório ================= */
const CE_COMINACOES = {
  advertência: "Advertência (servidor no exercício do cargo, art. 9º, I)",
  "censura ética": "Censura ética (servidor que já deixou o cargo, art. 9º, II)",
};
const CE_ANOS_FICHA = 5;

async function ceCominacao(id){ return (await db.porIndice("cominacoes", "denuncia_id", id)).pop(); }
async function ceDocumentos(id){ return (await db.porIndice("documentos_ce", "denuncia_id", id)).sort((a, b)=>(a.data || "").localeCompare(b.data || "")); }

/* RN: a ementa nunca leva o nome das partes (art. 11) */
function ceEmenta(d, cominacao){
  return `${d.protocolo} · ${d.categoria || "sem categoria"} · ${cominacao || "sem cominação"} · decidida pela Comissão de Ética da POLITEC/MT. (art. 11 da LC nº 112/2002-MT: divulgação sem os nomes dos interessados)`;
}
teste("art. 11: a ementa não leva nome das partes", ()=>{
  const e = ceEmenta({protocolo: "CE-2026-001", categoria: "assédio", denunciante: "Fulano", denunciado: "Beltrano"}, "advertência");
  return !/Fulano|Beltrano/.test(e) && e.includes("CE-2026-001");
});

const CE_MINUTAS = {
  comunicacao: {rotulo: "Comunicação ao denunciante", texto: d => `Ofício · Comissão de Ética da POLITEC/MT

Processo ${d.protocolo}, recebido em ${dataCurtaBR(d.data_recebimento)}.

Informamos que a denúncia foi ${d.situacao === "arquivada" ? "arquivada por falta de enquadramento no Código de Ética Funcional" : "recebida e processada pela Comissão de Ética"}.

A decisão está resumida em ementa, divulgada sem os nomes dos interessados (art. 11 da LC nº 112/2002-MT).

Atenciosamente,
Comissão de Ética · POLITEC/MT`},
  ata: {rotulo: "Ata de deliberação", texto: d => `Ata de deliberação · Comissão de Ética da POLITEC/MT

Processo ${d.protocolo}.
Comissão presente: 3 membros titulares e suplentes (art. 6º).
Deliberação: a Comissão concluiu pela ${d.situacao}.

Fundamento: Código de Ética Funcional do Servidor Público Civil do Estado de Mato Grosso (LC nº 112/2002-MT).

Cuiabá, ${dataCurtaBR(hojeISO())}.`},
  recomendacao: {rotulo: "Relatório de recomendações", texto: d => `Relatório de recomendações · Comissão de Ética da POLITEC/MT

Processo ${d.protocolo}, categoria ${d.categoria || "não informada"}.

1. Reforçar a orientação sobre o item do Código de Ética aplicável.
2. Comunicar o resultado à chefia imediata.
3. Acompanhar a reincidência por 12 meses.

A decisão será transcrita na ficha funcional por ${CE_ANOS_FICHA} anos (art. 9º, parágrafo único).

Cuiabá, ${dataCurtaBR(hojeISO())}.`},
};

TELAS["#/caso/:id/documentos"] = async ({id})=>{
  const d = await db.get("denuncias", id);
  if (!d) return `<div class="card vazio">Caso não encontrado.</div>`;
  const docs = await ceDocumentos(id), oitivas = await ceOitivas(id);
  return `<p class="sub nao-imprimir" style="margin-bottom:6px"><a href="#/caso/${encodeURIComponent(id)}">← Caso ${esc(d.protocolo)}</a></p>
    <h1>Documentos · ${esc(d.protocolo)}</h1>
    <p class="sub">Minutas geradas a partir do processo. O texto não leva o nome das partes (art. 11).</p>
    <div class="card"><h2 style="margin-top:0">Gerar minuta</h2><div class="campos">
      ${campo("ceTipoMinuta", "Minuta", {tipo: "select", opcoes: Object.entries(CE_MINUTAS).map(([k, m])=>[k, m.rotulo])})}</div>
      <div class="linha-botoes"><button class="prim" id="btnGerarMinuta">Gerar a minuta</button></div></div>
    <div class="card" id="ceMinutaAberta"></div>
    <div class="card" id="ceListaDocs"><h2 style="margin-top:0">Documentos do caso (${docs.length})</h2>
      ${docs.map(x=>`<details><summary><b>${esc(x.rotulo)}</b> · ${dataBR(x.data)}</summary>
        <pre style="white-space:pre-wrap;font-family:var(--mono);font-size:12.5px;margin-top:8px">${esc(x.texto)}</pre></details>`).join("") || '<p class="sub">Nenhum documento gerado.</p>'}
      ${oitivas.length ? `<p class="sub">${oitivas.length} oitiva(s) no processo.</p>` : ""}</div>`;
};
TELAS_DEPOIS["#/caso/:id/documentos"] = ({id})=>{
  $("#btnGerarMinuta")?.addEventListener("click", async ()=>{
    const tipo = valorDe("ceTipoMinuta"), d = await db.get("denuncias", id), m = CE_MINUTAS[tipo];
    if (!m || !d) return;
    const texto = m.texto(d);
    await db.put("documentos_ce", {id: uuid(), denuncia_id: id, tipo, rotulo: m.rotulo, texto, data: agora(), perfil: estado.perfil});
    await trilha("minuta gerada: " + m.rotulo, id);
    toast("Minuta gerada.");
    await navegar();
    const alvo = $("#ceMinutaAberta");
    if (alvo) alvo.innerHTML = `<div class="documento-a4"><div class="doc-cab">Comissão de Ética · POLITEC/MT<br>${esc(m.rotulo)}</div>
      <pre style="white-space:pre-wrap;font-family:Georgia,serif;font-size:15px;line-height:1.6">${esc(texto)}</pre></div>
      <div class="linha-botoes nao-imprimir"><button onclick="window.print()">Imprimir</button></div>`;
  });
};

TELAS["#/caso/:id/encerramento"] = async ({id})=>{
  const d = await db.get("denuncias", id);
  if (!d) return `<div class="card vazio">Caso não encontrado.</div>`;
  const [cls, admissao, oitivas, docs, cominacao] = await Promise.all([ceClassificacao(id), ceAdmissao(id), ceOitivas(id), ceDocumentos(id), ceCominacao(id)]);
  const etapas = [
    ["registro", !!d.protocolo], ["classificação", !!cls], ["admissibilidade", !!admissao],
    ["oitivas", oitivas.length > 0 || admissao?.via !== "acatada"], ["documentos", docs.length > 0],
    ["cominação", !!cominacao],
  ];
  const falta = etapas.filter(([, ok])=>!ok).map(([n])=>n);
  return `<p class="sub nao-imprimir" style="margin-bottom:6px"><a href="#/caso/${encodeURIComponent(id)}">← Caso ${esc(d.protocolo)}</a></p>
    <h1>Encerramento · ${esc(d.protocolo)}</h1>
    <div class="card"><h2 style="margin-top:0">Conferência das etapas</h2>
      <ul class="check-lista">${etapas.map(([n, ok])=>`<li class="${ok ? "feito" : "falta"}">${icone(ok ? "check" : "alerta")}<span>${esc(n)}</span></li>`).join("")}</ul>
      ${falta.length ? `<p class="erro-txt">Falta: ${falta.map(esc).join(", ")}.</p>` : '<p class="ok-txt">Todas as etapas estão preenchidas.</p>'}</div>
    ${!cominacao ? `<form class="card" id="formCominacao"><h2 style="margin-top:0">Cominação (art. 9º)</h2><div class="campos">
        ${campo("coTipo", "Cominação", {tipo: "select", opcoes: [["", "Escolha"], ...Object.entries(CE_COMINACOES)]})}
        ${campo("coParecer", "Fundamento (mínimo de 20 caracteres)", {tipo: "textarea", linhas: 3})}</div>
        <label style="display:flex;gap:8px;align-items:center;margin:8px 0"><input type="checkbox" id="coPAD" style="width:auto">
          <span>Encaminhar ao processo administrativo disciplinar (art. 10)</span></label>
        <div id="ceErrosCominacao"></div><div class="linha-botoes"><button class="prim" type="submit">Registrar a cominação</button></div></form>`
      : `<div class="card" id="cominacaoFeita"><h2 style="margin-top:0">Cominação aplicada</h2>
        <p><b>${esc(CE_COMINACOES[cominacao.tipo] || cominacao.tipo)}</b> · ${dataBR(cominacao.data)}${cominacao.pad ? " · encaminhada ao PAD (art. 10)" : ""}</p>
        <p>Transcrição na ficha funcional por <b>${CE_ANOS_FICHA} anos</b> (art. 9º, parágrafo único).</p>
        <p class="sub">Ementa (art. 11): ${esc(ceEmenta(d, cominacao.tipo))}</p></div>
      ${d.situacao === "encerrada" ? `<div class="card ok"><b>Caso encerrado.</b>
        <div class="linha-botoes"><button class="perigo" id="btnApagarCasoCe">Apagar os dados do caso (fica a contagem)</button></div></div>`
        : `<div class="card"><div class="linha-botoes"><button class="prim" id="btnEncerrarCe">Encerrar o caso</button></div></div>`}`}`;
};
TELAS_DEPOIS["#/caso/:id/encerramento"] = ({id})=>{
  $("#formCominacao")?.addEventListener("submit", async e=>{
    e.preventDefault();
    const tipo = valorDe("coTipo"), parecer = valorDe("coParecer"), pad = $("#coPAD").checked;
    const erros = [];
    if (!tipo) erros.push("Escolha a cominação.");
    if (parecer.length < 20) erros.push("Escreva o fundamento com pelo menos 20 caracteres.");
    if (!mostrarErros("#ceErrosCominacao", erros)) return;
    const d = await db.get("denuncias", id);
    await db.put("cominacoes", {id: uuid(), denuncia_id: id, tipo, parecer, pad, data: agora(), anos_ficha: CE_ANOS_FICHA, perfil: estado.perfil});
    await db.put("denuncias", {...d, etapa: "recomendações", situacao: "cominada"});
    await trilha("cominação aplicada: " + tipo, id, parecer);
    toast("Cominação registrada."); navegar();
  });
  $("#btnApagarCasoCe")?.addEventListener("click", async ()=>{
    if (!confirm("Apagar os dados pessoais e os relatos deste caso encerrado? A contagem fica guardada.")) return;
    const d = await db.get("denuncias", id);
    for (const loja of ["anexos", "classificacoes", "deliberacoes", "oitivas", "cominacoes", "documentos_ce"])
      for (const x of await db.porIndice(loja, "denuncia_id", id)) await db.del(loja, x.id);
    for (const x of (await db.list("log")).filter(l=>l.denuncia_id === id)) await db.del("log", x.id);
    await db.del("denuncias", id);
    const chave = "apagados";
    const atual = (await db.get("contagens", chave))?.valor || 0;
    await db.put("contagens", {chave, valor: atual + 1});
    await registrar("caso encerrado apagado (retenção)", {detalhe: d?.protocolo || id});
    toast("Caso apagado; a contagem ficou guardada."); location.hash = "#/painel";
  });
  $("#btnEncerrarCe")?.addEventListener("click", async ()=>{
    const d = await db.get("denuncias", id);
    await db.put("denuncias", {...d, etapa: "encerrado", situacao: "encerrada", encerrada_em: agora()});
    await trilha("caso encerrado", id); toast("Caso encerrado."); navegar();
  });
};

/* ================= Sprint 7 · Relatório ================= */
TELAS["#/relatorio"] = async ()=>{
  const ds = await db.list("denuncias"), oitivas = await db.list("oitivas"), coms = await db.list("cominacoes");
  const conta = campo => Object.entries(ds.reduce((a, d)=>{ const k = d[campo] || "—"; a[k] = (a[k] || 0) + 1; return a; }, {})).sort((a, b)=>b[1] - a[1]);
  const abertos = ds.filter(d=>!["encerrado", "encenrrado", "arquivada"].includes(d.etapa) && d.situacao !== "encerrada");
  const idade = d => ceDias(d.data_recebimento);
  const maisAntigos = [...abertos].sort((a, b)=>idade(b) - idade(a)).slice(0, 5);
  return `<h1>Relatório da Comissão</h1><p class="sub">Contagens e prazos, sem os nomes das partes (art. 11 da LC nº 112/2002-MT).</p>
    <div class="grade">
      <div class="card kpi"><div class="v" data-ce-ind="total">${ds.length}</div><div class="r">denúncias no recorte</div></div>
      <div class="card kpi"><div class="v" data-ce-ind="abertos">${abertos.length}</div><div class="r">em andamento</div></div>
      <div class="card kpi"><div class="v" data-ce-ind="oitivas">${oitivas.length}</div><div class="r">oitivas realizadas</div></div>
      <div class="card kpi"><div class="v" data-ce-ind="cominacoes">${coms.length}</div><div class="r">cominações aplicadas</div></div></div>
    <div class="card tabela-wrap"><h2 style="margin-top:0">Por etapa</h2><table id="tabelaEtapaCe"><tr><th>Etapa</th><th class="num">Casos</th></tr>
      ${conta("etapa").map(([k, n])=>`<tr><td>${esc(k)}</td><td class="num">${n}</td></tr>`).join("")}</table></div>
    <div class="card tabela-wrap"><h2 style="margin-top:0">Por categoria</h2><table id="tabelaCategoriaCe"><tr><th>Categoria</th><th class="num">Casos</th></tr>
      ${conta("categoria").map(([k, n])=>`<tr><td>${esc(k)}</td><td class="num">${n}</td></tr>`).join("")}</table></div>
    <div class="card tabela-wrap"><h2 style="margin-top:0">Casos há mais tempo em andamento</h2><table id="tabelaAntigosCe"><tr><th>Protocolo</th><th>Etapa</th><th class="num">Dias</th></tr>
      ${maisAntigos.map(d=>`<tr><td>${esc(d.protocolo)}</td><td>${esc(d.etapa)}</td><td class="num">${idade(d)}</td></tr>`).join("")
        || '<tr><td colspan="3" class="vazio">Nenhum caso em andamento.</td></tr>'}</table></div>
    <div class="card"><p class="sub">O relatório não mostra nome de denunciante nem de denunciado. A ementa de cada caso é divulgada sem os nomes, no próprio órgão, e remetida às demais Comissões de Ética (art. 11).</p></div>`;
};
