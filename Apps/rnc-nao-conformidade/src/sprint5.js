/* ================= Sprint 7 · documento oficial e prazos em dias úteis ================= */
const RNC_CAT = txt => categoriaOficial(txt);

TELAS["#/rnc/:id/documento"] = async ({id})=>{
  const r = await db.get("rncs", id);
  if (!r) return `<div class="card vazio">RNC ${esc(id)} não encontrada. <a href="#/painel">Voltar ao painel</a></div>`;
  const [es, plano, aval] = await Promise.all([db.porIndice("etapas", "rnc", id), db.get("planos", id + "-plano"), db.get("avaliacoes", id + "-aval")]);
  const setor = (await db.get("setores", r.setor_notificado))?.nome || r.setor_notificado;
  const cat = RNC_CAT(r.categoria);
  const linha = (rot, val)=> String(val || "").trim() ? `<tr><th>${esc(rot)}</th><td>${esc(val)}</td></tr>` : "";
  const extra = [["Local", r.local], ["Processo de trabalho", r.processo], ["Onde está o problema", r.onde],
    ["Requisito não atendido", r.requisito], ["Requisito ou documento", r.requisito_detalhe],
    ["Pessoas ou setores envolvidos", r.envolvidos], ["Frequência", r.frequencia],
    ["Consequências", r.consequencias], ["Medidas preventivas", r.medidas], ["Status no Trello", r.status_trello]].map(([a, b])=>linha(a, b)).join("");
  return `<div class="linha-botoes nao-imprimir"><button type="button" class="prim" id="btnImprimirDoc">${icone("imprimir")} Imprimir ou salvar em PDF</button>
      <a class="botao" href="#/rnc/${encodeURIComponent(id)}">← Voltar para a RNC</a></div>
    <article class="documento-a4 doc-rnc" id="docRnc">
      <header class="doc-rnc-cab"><div><b>POLITEC/MT</b><br>Perícia Oficial e Identificação Técnica<br>Diretoria de Laboratório Forense</div>
        <div class="dir">Registro de Não Conformidade<br><b>${esc(r.numero)}</b></div></header>
      <h1>REGISTRO DE NÃO CONFORMIDADE</h1>
      <table><tr><th>Data de abertura</th><td>${dataCurtaBR(r.aberta_em)}</td><th>Situação</th><td>${esc(r.situacao)}</td></tr>
        <tr><th>Setor relator</th><td>${esc((await db.get("setores", r.setor_relator))?.nome || r.setor_relator)}</td><th>Setor notificado</th><td>${esc(setor)}</td></tr>
        <tr><th>Categoria</th><td colspan="3">${cat ? `<b>${esc(cat.sigla)}</b> · ${esc(cat.nome)}. ${esc(cat.descricao)}` : esc(r.categoria)}</td></tr>
        <tr><th>Criticidade</th><td colspan="3">${esc(r.gravidade || "não informada")}</td></tr></table>
      <h2>1. Ocorrência</h2>
      <p class="doc-rnc-texto">${esc(r.descricao)}</p>
      ${extra ? `<table>${extra}</table>` : ""}
      ${(r.anexos || r.doc_url) ? `<p class="sub">Anexos: ${/^https?:/.test(r.anexos || "") ? `<a href="${esc(r.anexos)}">${esc(r.anexos)}</a>` : esc(r.anexos || "")} ${/^https?:/.test(r.doc_url || "") ? ` · <a href="${esc(r.doc_url)}">documento gerado</a>` : ""}</p>` : ""}
      <h2>2. Plano de ação e avaliação</h2>
      <table><tr><th>Plano (FOR 2)</th><td>${plano?.enviado_em ? `recebido em ${dataCurtaBR(plano.enviado_em)}` : "não registrado"}${plano?.acoes ? ` · ${esc(plano.acoes)}` : ""}${plano?.prorrogado_ate ? ` · prorrogado até ${dataCurtaBR(plano.prorrogado_ate)}` : ""}</td></tr>
        <tr><th>Avaliação (FOR 3)</th><td>${aval ? `${aval.eficaz ? "ações eficazes" : "ações não eficazes"} · ${dataCurtaBR(aval.avaliado_em)}${aval.observacao ? ` · ${esc(aval.observacao)}` : ""}` : "não registrada"}</td></tr></table>
      ${es.length ? `<h2>3. Etapas e prazos</h2><table><tr><th>Etapa</th><th>Início</th><th>Fim</th><th>Prazo</th></tr>
        ${es.sort((a, b)=>String(a.inicio).localeCompare(String(b.inicio))).map(e=>`<tr><td>${esc(e.etapa)}</td><td>${dataCurtaBR(e.inicio)}</td><td>${dataCurtaBR(e.fim) || "—"}</td><td>${dataCurtaBR(e.prazo)}${e.prorrogado ? " (prorrogado)" : ""}</td></tr>`).join("")}</table>` : ""}
      ${r.situacao === "encaminhada à corregedoria" ? `<p><b>Encaminhamento à corregedoria:</b> ${esc(r.motivo_corregedoria || "")}</p>` : ""}
      ${r.situacao === "anulada" ? `<p><b>Anulação:</b> ${esc(r.motivo_anulacao || "")}</p>` : ""}
      <p class="doc-rnc-data">Cuiabá, ${dataCurtaBR(hojeISO())}.</p>
      <div class="doc-rnc-ass"><div>Relator / CQUAL</div><div>Chefia da CQUAL</div></div>
      <p class="sub doc-rnc-pe">Documento gerado pelo app RNC a partir dos dados registrados. A assinatura é presencial.</p>
    </article>`;
};
TELAS_DEPOIS["#/rnc/:id/documento"] = ()=>{
  $("#btnImprimirDoc")?.addEventListener("click", ()=> window.print());
};
