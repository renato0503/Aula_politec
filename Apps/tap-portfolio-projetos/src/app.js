/* TAP Digital · código do app (o construir.py junta com a base comum) */
"use strict";
TELAS["#/portfolio"] = async ()=> `<h1>Portfólio</h1><p class="sub">O portfólio chega no Sprint 5. Resumo da base:</p>
  ${await resumoBase(["propostas", "pendencias", "decisoes", "portfolio", "documentos"])}
  <p class="sub">Para testar, carregue os dados fictícios em <a href="#/config">Configuração</a>.</p>`;
teste("Checklist do exemplo tem 3 documentos obrigatórios", ()=> (dadosEmbutidos("seed")?.documentos || []).filter(d=>d.obrigatorio).length === 3);
teste("Exemplo sem CPF", ()=> !JSON.stringify(dadosEmbutidos("seed")).toLowerCase().includes('"cpf"'));

/* ================= Sprint 2 · TAP guiado (RN01 a RN04) ================= */
const MIN_OBJETIVO = 100, MIN_JUSTIFICATIVA = 200, LIMITE_ANEXO = 10 * 1024 * 1024;
const OBJETIVOS_ESTRATEGICOS = ["Reduzir o tempo de emissão de laudos", "Modernizar a infraestrutura das unidades", "Ampliar a capacidade dos laboratórios",
  "Fortalecer a identificação civil", "Qualificar os servidores"];
// Checklist padrão enquanto a equipe não cadastra o oficial (store documentos)
const DOCUMENTOS_PADRAO = (dadosEmbutidos("seed")?.documentos || []);
const ETAPAS_TAP = [
  {id: "ident", titulo: "Identificação", campos: ["titulo", "unidade", "responsavel", "contato"]},
  {id: "objetivo", titulo: "Objetivo e justificativa", campos: ["objetivo", "justificativa"]},
  {id: "alinhamento", titulo: "Alinhamento estratégico", campos: ["objetivo_estrategico"]},
  {id: "custo", titulo: "Custo e prazo", campos: ["valor_estimado", "prazo_meses"]},
  {id: "anexos", titulo: "Anexos", campos: []}
];
const ROT_TAP = {titulo: "Título do projeto", unidade: "Unidade demandante", responsavel: "Responsável", contato: "Contato institucional",
  objetivo: "Objetivo", justificativa: "Justificativa", objetivo_estrategico: "Objetivo estratégico", valor_estimado: "Valor estimado", prazo_meses: "Prazo (meses)"};
const AJUDA_TAP = {titulo: "Nome curto que identifica o projeto no portfólio.", contato: "E-mail ou telefone institucional.",
  objetivo: `O que o projeto entrega, em pelo menos ${MIN_OBJETIVO} caracteres.`, justificativa: `Por que é necessário agora e o que acontece se não for feito, em pelo menos ${MIN_JUSTIFICATIVA} caracteres.`,
  objetivo_estrategico: "A qual objetivo do planejamento da SESP/POLITEC o projeto atende.", valor_estimado: "Com base na pesquisa de preços anexada."};

async function documentosChecklist(){ const d = await db.list("documentos"); return d.length ? d : DOCUMENTOS_PADRAO; }

// RN01 a RN04: lista de pendências (vazia = TAP completo)
function pendenciasTap(p, anexos, docs){
  const e = [];
  for (const k of ["titulo", "unidade", "responsavel", "contato", "objetivo_estrategico"]) if (!String(p[k] || "").trim()) e.push(`${ROT_TAP[k]}: não preenchido (RN01).`);
  const lo = String(p.objetivo || "").trim().length, lj = String(p.justificativa || "").trim().length;
  if (lo < MIN_OBJETIVO) e.push(`Objetivo: ${lo} de ${MIN_OBJETIVO} caracteres (RN02).`);
  if (lj < MIN_JUSTIFICATIVA) e.push(`Justificativa: ${lj} de ${MIN_JUSTIFICATIVA} caracteres (RN02).`);
  if (!(p.valor_estimado > 0)) e.push("Valor estimado: não preenchido (RN01).");
  if (!(p.prazo_meses > 0)) e.push("Prazo: não preenchido (RN01).");
  for (const d of docs.filter(d=>d.obrigatorio)){
    const a = anexos.find(x=>x.tipo === d.tipo);
    if (!a && !String(p.ausencias?.[d.tipo] || "").trim()) e.push(`Anexo obrigatório: ${d.nome} (anexe ou justifique a ausência, RN03).`);
  }
  return e;
}
teste("RN02: justificativa curta é pendência", ()=> pendenciasTap({justificativa: "curta"}, [], []).some(x=>x.includes("Justificativa: 5 de 200")));
teste("RN03: documento ausente justificado não é pendência", ()=>
  !pendenciasTap({ausencias: {x: "Não se aplica a este projeto."}}, [], [{tipo: "x", nome: "X", obrigatorio: true}]).some(x=>x.includes("RN03")));

async function rascunhoAtual(){
  let id = await db.meta("rascunho_atual"), p = id ? await db.get("propostas", id) : null;
  if (!p || p.status !== "rascunho"){
    const ano = new Date().getFullYear(), seq = (await db.list("propostas")).filter(x=>x.id.startsWith(`TAP-${ano}-`)).length + 1;
    p = {id: `TAP-${ano}-${String(seq).padStart(3, "0")}`, status: "rascunho", criado_em: agora(), ausencias: {}};
    await db.put("propostas", p); await db.meta("rascunho_atual", p.id);
  }
  return p;
}

TELAS["#/tap/novo"] = async ()=>{
  const p = await rascunhoAtual(), docs = await documentosChecklist(), anexos = await db.porIndice("anexos", "proposta_id", p.id);
  const etapa = estado.etapaTap || "ident";
  const ctrl = k => {
    if (k === "objetivo" || k === "justificativa") return campo("tap-" + k, ROT_TAP[k], {tipo: "textarea", linhas: 5, valor: p[k] || "", obrigatorio: true, ajuda: AJUDA_TAP[k]}) + `<p class="sub" id="cont-${k}"></p>`;
    if (k === "objetivo_estrategico") return campo("tap-" + k, ROT_TAP[k], {tipo: "select", opcoes: [["", "Escolha"], ...OBJETIVOS_ESTRATEGICOS], valor: p[k] || "", obrigatorio: true, ajuda: AJUDA_TAP[k]});
    if (k === "valor_estimado") return campo("tap-" + k, ROT_TAP[k] + " (R$)", {valor: p[k] ? dinheiro.fmt(Math.round(p[k] * 100)).replace("R$ ", "") : "", obrigatorio: true, attrs: 'inputmode="decimal"', ajuda: AJUDA_TAP[k]});
    if (k === "prazo_meses") return campo("tap-" + k, ROT_TAP[k], {tipo: "number", valor: p[k] || "", obrigatorio: true, attrs: 'min="1" max="120"'});
    return campo("tap-" + k, ROT_TAP[k], {valor: p[k] || "", obrigatorio: true, ajuda: AJUDA_TAP[k]});
  };
  const secao = ETAPAS_TAP.find(e=>e.id === etapa);
  const corpo = etapa === "anexos" ? docs.map(d=>{
    const a = anexos.find(x=>x.tipo === d.tipo);
    return `<div class="card"><b>${esc(d.nome)}</b> ${d.obrigatorio ? '<span class="selo erro">obrigatório</span>' : '<span class="selo info">opcional</span>'}
      <p class="sub">${a ? `Anexado: ${esc(a.nome)} (${(a.tamanho / 1024).toFixed(0)} KB) <button type="button" data-tirar="${esc(a.id)}">Tirar</button>` : "Nenhum arquivo."}</p>
      <label class="botao">${a ? "Trocar arquivo" : "Anexar arquivo"}<input type="file" data-anexo="${esc(d.tipo)}" accept=".pdf,.xlsx,.xls,.csv,.jpg,.jpeg,.png" hidden></label>
      ${d.obrigatorio && !a ? campo("aus-" + d.tipo, "Ou justifique a ausência", {tipo: "textarea", linhas: 2, valor: p.ausencias?.[d.tipo] || ""}) : ""}</div>`;
  }).join("") : `<div class="campos" style="grid-template-columns:1fr">${secao.campos.map(ctrl).join("")}</div>`;
  const ip = ETAPAS_TAP.findIndex(e=>e.id === etapa);
  return `<h1>Termo de Abertura de Projeto · ${esc(p.id)}</h1><p class="sub">O rascunho é salvo a cada campo. Você pode fechar e continuar depois.</p>
    <nav class="menu" style="padding:0 0 8px" aria-label="Etapas do TAP">${ETAPAS_TAP.map((e, i)=>`<a href="javascript:void 0" data-etapa="${e.id}" ${e.id === etapa ? 'aria-current="page"' : ""}>${i + 1}. ${e.titulo}</a>`).join("")}</nav>
    <form class="card" id="formTap" onsubmit="return false"><h2 style="margin-top:0">${ip + 1}. ${esc(secao.titulo)}</h2>${corpo}
      <div class="linha-botoes">${ip > 0 ? `<button type="button" data-etapa="${ETAPAS_TAP[ip - 1].id}">Anterior</button>` : ""}
        ${ip < ETAPAS_TAP.length - 1 ? `<button type="button" class="prim" data-etapa="${ETAPAS_TAP[ip + 1].id}">Próxima</button>` : ""}</div></form>
    <div class="card" id="painelPendencias"></div>`;
};
async function atualizarPendencias(){
  const p = await rascunhoAtual(), pend = pendenciasTap(p, await db.porIndice("anexos", "proposta_id", p.id), await documentosChecklist());
  $("#painelPendencias").innerHTML = pend.length
    ? `<h2 style="margin-top:0">Pendências antes do envio (<span id="qtdPend">${pend.length}</span>)</h2><ul>${pend.map(x=>`<li>${esc(x)}</li>`).join("")}</ul>`
    : `<h2 style="margin-top:0" class="ok-txt">TAP completo (<span id="qtdPend">0</span> pendências)</h2>
       <p>O pacote para envio pelo SEI ou e-mail chega no Sprint 3.</p><button class="prim" id="btnConcluir">Concluir TAP</button>`;
  $("#btnConcluir")?.addEventListener("click", async ()=>{
    const q = await rascunhoAtual();
    if (pendenciasTap(q, await db.porIndice("anexos", "proposta_id", q.id), await documentosChecklist()).length) return toast("Ainda há pendências.");
    await db.put("propostas", {...q, status: "pronto para envio", concluido_em: agora()}); await db.meta("rascunho_atual", null);
    await registrar("TAP concluído", {proposta_id: q.id}); toast(`TAP ${q.id} concluído.`); location.hash = "#/minhas";
  });
  for (const k of ["objetivo", "justificativa"]){
    const el = $("#cont-" + k); if (!el) continue;
    const n = valorDe("tap-" + k).length, min = k === "objetivo" ? MIN_OBJETIVO : MIN_JUSTIFICATIVA;
    el.innerHTML = `<span class="${n >= min ? "ok-txt" : "erro-txt"}">${n} de ${min} caracteres</span>`;
  }
}
TELAS_DEPOIS["#/tap/novo"] = async ()=>{
  $$("[data-etapa]").forEach(b=>b.addEventListener("click", ()=>{ estado.etapaTap = b.dataset.etapa; navegar(); }));
  // salva cada campo assim que muda (rascunho)
  $$("#formTap [id^=tap-]").forEach(el=>el.addEventListener("input", async ()=>{
    const p = await rascunhoAtual(), k = el.id.slice(4);
    let v = el.value;
    if (k === "valor_estimado") v = (dinheiro.de(v) || 0) / 100;
    if (k === "prazo_meses") v = Number(v) || 0;
    await db.put("propostas", {...p, [k]: v, atualizado_em: agora()}); atualizarPendencias();
  }));
  $$("#formTap [id^=aus-]").forEach(el=>el.addEventListener("input", async ()=>{
    const p = await rascunhoAtual(); await db.put("propostas", {...p, ausencias: {...(p.ausencias || {}), [el.id.slice(4)]: el.value}}); atualizarPendencias();
  }));
  $$("[data-anexo]").forEach(inp=>inp.addEventListener("change", async e=>{
    const f = e.target.files[0]; if (!f) return;
    if (f.size > LIMITE_ANEXO) return toast(`O arquivo ${f.name} passa de 10 MB (RN04).`, 5000);
    const p = await rascunhoAtual(), tipo = e.target.dataset.anexo;
    await db.put("anexos", {id: `${p.id}-${tipo}`, proposta_id: p.id, tipo, nome: f.name, tamanho: f.size, mime: f.type, conteudo: f});
    await registrar("anexo", {proposta_id: p.id, detalhe: `${tipo}: ${f.name}`}); navegar();
  }));
  $$("[data-tirar]").forEach(b=>b.addEventListener("click", async ()=>{ await db.del("anexos", b.dataset.tirar); navegar(); }));
  await atualizarPendencias();
};
