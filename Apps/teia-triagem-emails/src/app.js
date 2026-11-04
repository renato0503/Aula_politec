"use strict";
/* TEIA · Triagem de E-mails
   Protótipo local do painel do triador. A extração é simulada com os dados
   fictícios: o app mostra os 9 campos, as confianças e as pendências que o
   script local produziria. Nenhum dado sai do navegador. */

const TE_CAMPOS = [
  {id: "data_cobranca", rotulo: "Data da cobrança", tipo: "date"},
  {id: "protocolo", rotulo: "Protocolo", tipo: "text"},
  {id: "tipo_crime", rotulo: "Tipo de crime", tipo: "select", opcoes: ["Crime Sexual", "Local de Crime", "Identificação Humana", "Biologia"]},
  {id: "nome_vitima", rotulo: "Nome da vítima", tipo: "text"},
  {id: "nome_investigado", rotulo: "Nome do investigado", tipo: "text"},
  {id: "reu_preso", rotulo: "Réu preso", tipo: "select", opcoes: ["Sim", "Não", "Não informado"]},
  {id: "ar_para_confronto", rotulo: "AR para confronto", tipo: "select", opcoes: ["Sim", "Não", "Não informado"]},
  {id: "regional", rotulo: "Regional", tipo: "select", opcoes: [
    "Coordenadoria de Perícias em Vivos",
    "Gerência de Perícias em Vítimas de Violência Sexual e de Gênero",
    "Coordenadoria de Perícias em Mortos",
    "Gerência de Necropsia",
    "Gerência de Antropologia",
    "Coordenadoria de Perícias Externas",
    "Coordenadoria Regional de Rondonópolis",
    "Gerência de Criminalística de Rondonópolis",
    "Gerência de Medicina Legal de Rondonópolis",
    "Gerência Regional de Primavera do Leste",
    "Gerência Regional de Alto Araguaia",
    "Coordenadoria Regional de Barra do Garças",
    "Gerência de Criminalística de Barra do Garças",
    "Gerência de Medicina Legal de Barra do Garças",
    "Gerência Regional de Água Boa",
    "Gerência Regional de Confresa",
    "Coordenadoria Regional de Cáceres",
    "Gerência de Criminalística de Cáceres",
    "Gerência de Medicina Legal de Cáceres",
    "Gerência Regional de Pontes e Lacerda",
    "Coordenadoria Regional de Sinop",
    "Gerência de Criminalística de Sinop",
    "Gerência de Medicina Legal de Sinop",
    "Gerência Regional de Alta Floresta",
    "Gerência Regional de Guarantã do Norte",
    "Gerência Regional de Sorriso",
    "Coordenadoria Regional de Tangará da Serra",
    "Gerência de Criminalística de Tangará da Serra",
    "Gerência de Medicina Legal de Tangará da Serra",
    "Gerência Regional de Juina",
    "Gerência Regional de Juara",
    "Coordenadoria Regional de Nova Mutum",
    "Gerência de Criminalística de Nova Mutum",
    "Gerência de Medicina Legal de Nova Mutum",
    "Gerência Regional de Diamantino",
    "Gerência Regional de Lucas do Rio Verde"
  ]},
  {id: "objetivo_claro", rotulo: "Objetivo claro", tipo: "textarea"}
];
const TE_STATUS = {novo: "Novo", extraido: "Extraído", pendente: "Pendente", validado: "Validado", recusado: "Recusado"};
const TE_PRIORIDADE = {normal: "Normal", alta: "Alta", urgente: "Urgente"};
const TE_ALERTA = {divergencia: "Divergência entre corpo e anexo", ocr: "PDF sem texto: leitura manual", pendencia: "Campo ausente", reiteracao: "Cobrança reiterada para o mesmo protocolo"};
const TE_REGIONAIS = TE_CAMPOS.find(c=>c.id === "regional").opcoes;
const TE_CRIMES = TE_CAMPOS.find(c=>c.id === "tipo_crime").opcoes;
const TE_REITERACAO_DIAS = 30;
const teProtocoloValido = p => /^\d{6}\/\d{4}$/.test(String(p || "").trim());
function teDataDe(valor){ const d = new Date(valor); return Number.isNaN(d.getTime()) ? null : d; }
function teMesmaCobranca(a, b){
  const da = teDataDe(a), db = teDataDe(b);
  if (!da || !db) return true;
  return Math.abs(da - db) <= TE_REITERACAO_DIAS * 86400000;
}
async function teTemReiteracao(e, c){
  const p = String(c.protocolo || "").trim();
  if (!p) return false;
  return (await db.list("emails")).some(x =>
    x.id !== e.id && x.status !== "recusado" &&
    String((x.campos || {}).protocolo || "").trim() === p &&
    teMesmaCobranca(x.recebido_em, e.recebido_em));
}
teste("TEIA: protocolo no formato 000000/0000", ()=> teProtocoloValido("001001/2026") && !teProtocoloValido("2026.1001-DNA") && !teProtocoloValido("1001/2026"));
teste("TEIA: reiteração dentro da janela", ()=> teMesmaCobranca("2026-10-23T09:00:00-04:00", "2026-11-02T10:00:00-04:00") && !teMesmaCobranca("2026-01-01T00:00:00-04:00", "2026-06-01T00:00:00-04:00"));

const teNormal = s => normalizar(s || "");
const teCampos = e => e.campos || {};
const teFaltando = c => TE_CAMPOS.filter(x=>!String(c[x.id] || "").trim()).map(x=>x.rotulo);
const teSeloStatus = s => s === "validado" ? "ok" : s === "pendente" ? "alerta" : s === "recusado" ? "erro" : s === "extraido" ? "info" : "info";
const teSeloPrioridade = p => p === "urgente" ? "erro" : p === "alta" ? "alerta" : "info";
const teData = iso => iso ? dataBR(iso) : "—";

function teAtualizarStatus(e){
  const falta = teFaltando(teCampos(e));
  if (e.status === "validado" || e.status === "recusado") return e.status;
  if (e.alerta || falta.length) return "pendente";
  return e.status === "novo" ? "novo" : "extraido";
}

async function teLog(acao, e, detalhe=""){
  await registrar(acao, {detalhe: `${e.id} · ${detalhe}`});
}

async function teExtrair(e){
  const c = {...teCampos(e)};
  if (!c.data_cobranca && e.recebido_em) c.data_cobranca = e.recebido_em.slice(0, 10);
  const falta = teFaltando(c);
  const reiterada = !falta.length && await teTemReiteracao(e, c);
  const alerta = e.alerta || (falta.length ? "pendencia" : reiterada ? "reiteracao" : "");
  const extracao = {id: e.id, email_id: e.id, campos: c, confianca: e.confianca ?? 0.9, alerta, faltando: falta, status: "extraido", criado_em: agora()};
  await db.put("extracao", extracao);
  await db.put("emails", {...e, campos: c, status: teAtualizarStatus({...e, alerta, status: "extraido"}), alerta});
  await teLog("extração executada", e, falta.length ? `falta: ${falta.join(", ")}` : `9 campos localizados${reiterada ? " · protocolo reiterado" : ""}`);
  return {extracao, falta, alerta};
}

async function teValidar(e){
  const c = teCampos(e), falta = teFaltando(c);
  if (falta.length) throw new Error(`Preencha os 9 campos antes de validar. Falta: ${falta.join(", ")}.`);
  if (!teProtocoloValido(c.protocolo)) throw new Error("Protocolo no formato 000000/0000 (seis números, barra e ano).");
  if (e.alerta) throw new Error("Trate o alerta antes de validar: " + (TE_ALERTA[e.alerta] || e.alerta) + ".");
  const atualizado = {...e, status: "validado", validado_por: estado.perfil || "triador", validado_em: agora()};
  await db.put("emails", atualizado);
  await db.put("extracao", {...(await db.get("extracao", e.id) || {id: e.id, email_id: e.id}), campos: c, status: "validado", validado_por: atualizado.validado_por, validado_em: atualizado.validado_em});
  await teLog("requisição validada", e, "9 campos conferidos e fé pública registrada");
  return atualizado;
}

async function teTratarAlerta(e){
  await db.put("emails", {...e, alerta: "", status: teAtualizarStatus({...e, alerta: ""})});
  await teLog("alerta tratado", e, e.alerta || "");
}

async function teRecusar(e, motivo){
  if (!String(motivo || "").trim()) throw new Error("Informe o motivo da recusa.");
  await db.put("emails", {...e, status: "recusado", motivo_recusa: motivo, alerta: e.alerta || ""});
  await teLog("requisição recusada", e, motivo);
}

async function teDetalhe(e, nav = {}){
  if (!e) return `<div class="card vazio te-vazio"><b>Selecione um e-mail na fila</b><p class="sub">A bancada mostra a mensagem e os 9 campos extraídos.</p></div>`;
  const c = teCampos(e), falta = teFaltando(c);
  const campos = TE_CAMPOS.map(x=>{
    const valor = c[x.id] || (x.id === "data_cobranca" && e.recebido_em ? e.recebido_em.slice(0, 10) : "");
    const extra = x.id === "data_cobranca" ? ' readonly title="Data do e-mail"' : (x.id === "protocolo" ? ' placeholder="000000/0000" inputmode="numeric"' : "");
    return `<div class="campo"><label for="te_${x.id}">${esc(x.rotulo)}${falta.includes(x.rotulo) ? ' <span class="erro-txt">falta</span>' : ""}</label>
      ${x.tipo === "select" ? `<select id="te_${x.id}">${["", ...x.opcoes].map(v=>`<option value="${esc(v)}" ${String(v) === String(valor) ? "selected" : ""}>${esc(v || "—")}</option>`).join("")}</select>`
        : x.tipo === "textarea" ? `<textarea id="te_${x.id}" rows="2">${esc(valor)}</textarea>`
        : `<input id="te_${x.id}" type="${x.tipo}" value="${esc(valor)}"${extra}>`}</div>`;
  }).join("");
  const anexos = (e.anexos || []).map(a=>`<tr><td class="mono">${esc(a.nome)}</td><td>${esc(a.tipo)}</td><td class="num">${a.paginas}</td>
    <td>${a.legivel ? '<span class="selo ok">legível</span>' : '<span class="selo erro">imagem/manuscrito</span>'}</td></tr>`).join("");
  const podeValidar = !falta.length && !e.alerta && e.status !== "validado" && e.status !== "recusado";
  const navHtml = nav.total ? `<div class="te-nav">
    <button type="button" class="sec" data-te-nav="anterior" ${nav.anterior ? `data-te-id="${esc(nav.anterior)}"` : "disabled"} aria-label="E-mail anterior" title="E-mail anterior">‹</button>
    <span class="sub">${nav.posicao} de ${nav.total}</span>
    <button type="button" class="sec" data-te-nav="proximo" ${nav.proximo ? `data-te-id="${esc(nav.proximo)}"` : "disabled"} aria-label="Próximo e-mail" title="Próximo e-mail">›</button></div>` : "";
  return `<div class="card te-detalhe" id="teDetalhe">
    <div class="te-detalhe-topo"><div class="te-detalhe-ident"><span class="sub">${esc(e.orgao)} · ${esc(e.remetente)}</span>
      <h2>${esc(e.assunto)}</h2><p class="sub">Recebido em ${teData(e.recebido_em)} · ${esc(e.id)}</p></div>
      <div class="te-detalhe-lado"><div class="te-selos"><span class="selo ${teSeloPrioridade(e.prioridade)}">${esc(TE_PRIORIDADE[e.prioridade] || e.prioridade)}</span>
        <span class="selo ${teSeloStatus(e.status)}">${esc(TE_STATUS[e.status] || e.status)}</span></div>${navHtml}</div></div>
    ${e.alerta ? `<div class="caixa-alerta"><b>Alerta:</b> ${esc(TE_ALERTA[e.alerta] || e.alerta)}.</div>` : ""}
    <div class="te-grade">
      <section class="te-mensagem"><h3>Mensagem</h3><p class="te-corpo">${esc(e.corpo)}</p>
        <h3>Anexos</h3><div class="tabela-wrap"><table><tr><th>Arquivo</th><th>Tipo</th><th class="num">Páginas</th><th>Leitura</th></tr>${anexos || '<tr><td colspan="4" class="vazio">Sem anexos.</td></tr>'}</table></div>
        <p class="sub">Confiança da extração: <b>${Math.round((e.confianca || 0) * 100)}%</b> · ${falta.length ? `${falta.length} campo(s) faltando` : "9 campos localizados"}</p>
        <details class="te-auditoria"><summary>Auditoria do e-mail</summary><div id="teAuditoria">${await teAuditoria(e.id)}</div></details>
      </section>
      <section class="te-form"><h3>9 campos essenciais</h3><div class="campos">${campos}</div>
        <div class="te-acoes"><div class="linha-botoes">
          <button type="button" id="btnTeExtrair">Extrair de novo</button>
          <button type="button" class="prim" id="btnTeSalvar">Salvar campos</button>
          <button type="button" id="btnTeValidar" ${podeValidar ? "" : "disabled"} title="${podeValidar ? "" : "Resolva os campos e os alertas"}">Validar requisição</button>
          ${e.alerta ? '<button type="button" id="btnTeAlerta">Tratar alerta</button>' : ""}
          <button type="button" class="perigo" id="btnTeRecusar">Recusar</button>
        </div></div>
        <div id="teErros"></div>
        <p class="sub">A validação é ato humano e fica registrada com perfil e data/hora. O app não envia nada para fora.</p>
      </section>
    </div></div>`;
}

async function teAuditoria(id){
  const logs = (await db.list("log")).filter(l=>String(l.detalhe || "").startsWith(id)).sort((a, b)=>String(b.data_hora).localeCompare(String(a.data_hora))).slice(0, 8);
  return logs.length ? `<ul class="check-lista">${logs.map(l=>`<li class="feito"><span>${esc(l.acao)} · ${esc(l.detalhe)} · ${dataBR(l.data_hora)}</span></li>`).join("")}</ul>`
    : '<p class="sub">Sem ações registradas.</p>';
}

function teFiltro(){ return estado.teSit || ""; }

TELAS["#/painel"] = async ()=>{
  const emails = await db.list("emails");
  const f = teFiltro(), busca = normalizar(estado.teBusca || ""), urgente = !!estado.teUrgente;
  const vis = emails.filter(e=>!f || e.status === f).filter(e=>!urgente || e.prioridade === "urgente")
    .filter(e=>!busca || normalizar(`${e.assunto} ${e.remetente} ${e.orgao} ${(e.campos || {}).protocolo || ""}`).includes(busca))
    .sort((a, b)=>String(b.prioridade).localeCompare(String(a.prioridade)) || String(b.recebido_em).localeCompare(String(a.recebido_em)));
  let sel = estado.teSel ? await db.get("emails", estado.teSel) : null;
  if (!sel || !vis.some(e=>e.id === sel.id)) sel = vis[0] || null;
  if (sel) estado.teSel = sel.id;
  const conta = s => emails.filter(e=>e.status === s).length;
  const fila = emails.filter(e=>e.status === "novo" || e.status === "extraido").length;
  const urg = emails.filter(e=>e.prioridade === "urgente").length;
  const idx = sel ? vis.findIndex(e=>e.id === sel.id) : -1;
  const nav = sel ? {anterior: vis[idx - 1]?.id, proximo: vis[idx + 1]?.id, posicao: idx + 1, total: vis.length} : {};
  const ativo = k => k === "fila" ? (!f && !urgente) : (k === "urgente" ? urgente : f === k && !urgente);
  return `<h1>Bancada de triagem</h1>
    <p class="sub">Escolha um e-mail na fila. Os 9 campos ficam à direita; a extração é simulada e a validação é humana.</p>
    <div class="grade te-kpis">
      <button type="button" class="card kpi te-kpi" data-te-kpi="fila" aria-pressed="${ativo("fila")}"><span class="v">${fila}</span><span class="r">na fila</span></button>
      <button type="button" class="card kpi te-kpi" data-te-kpi="pendente" aria-pressed="${ativo("pendente")}"><span class="v">${conta("pendente")}</span><span class="r">pendentes</span></button>
      <button type="button" class="card kpi te-kpi" data-te-kpi="urgente" aria-pressed="${ativo("urgente")}"><span class="v">${urg}</span><span class="r">urgentes</span></button>
      <button type="button" class="card kpi te-kpi" data-te-kpi="validado" aria-pressed="${ativo("validado")}"><span class="v">${conta("validado")}</span><span class="r">validados</span></button></div>
    <div class="card te-filtros"><div class="campos">
      ${campo("teBusca", "Buscar por assunto, remetente, órgão ou protocolo", {valor: estado.teBusca || "", attrs: 'autocomplete="off"'})}
      <div class="campo"><label>Fila</label><div class="chips">${[["", "Todos"], ...Object.entries(TE_STATUS)].map(([v, t])=>`<button type="button" class="${f === v && !urgente ? "prim" : ""}" data-te-sit="${v}">${t} (${v ? conta(v) : emails.length})</button>`).join("")}
        ${(f || busca || urgente) ? '<button type="button" class="sec" data-te-limpar>Limpar filtros</button>' : ""}</div></div></div></div>
    <div class="te-bancada"><div class="te-fila-wrap"><div class="te-fila-topo"><b>${vis.length}</b> e-mail(s)${urgente ? " urgente(s)" : ""}<span class="sub">${vis.length ? "deslize para ver os outros" : ""}</span></div>
      <div class="te-fila">${vis.length ? vis.map(e=>`<button type="button" class="te-item ${e.id === estado.teSel ? "escolhido" : ""}" data-te-email="${esc(e.id)}" aria-current="${e.id === estado.teSel}">
      <span class="te-item-topo"><b>${esc(e.assunto)}</b><span class="selo ${teSeloPrioridade(e.prioridade)}">${esc(TE_PRIORIDADE[e.prioridade] || e.prioridade)}</span></span>
      <span class="sub">${esc(e.orgao)} · ${esc((e.campos || {}).regional || "sem regional")}</span>
      <span class="te-item-meta"><span class="selo ${teSeloStatus(e.status)}">${esc(TE_STATUS[e.status] || e.status)}</span>${e.alerta ? `<span class="selo erro">${esc(TE_ALERTA[e.alerta] || "alerta")}</span>` : ""}<small class="sub">${teData(e.recebido_em)}</small></span></button>`).join("") : '<p class="sub te-vazio-fila">Nenhum e-mail nesta fila. Limpe os filtros para ver todos.</p>'}</div></div>
      <div id="tePainel">${await teDetalhe(sel, nav)}</div></div>`;
};
TELAS_DEPOIS["#/painel"] = ()=>teLigar();

function teLigar(){
  const irPara = async id=>{
    if (!id) return;
    estado.teSel = id; await navegar();
    if (matchMedia("(max-width:900px)").matches) $("#teDetalhe")?.scrollIntoView({behavior: "smooth", block: "start"});
  };
  $$("[data-te-email]").forEach(b=>b.addEventListener("click", ()=>irPara(b.dataset.teEmail)));
  $$("[data-te-nav]").forEach(b=>b.addEventListener("click", ()=>irPara(b.dataset.teId)));
  $$("[data-te-kpi]").forEach(b=>b.addEventListener("click", ()=>{
    const k = b.dataset.teKpi;
    if (k === "urgente"){ estado.teUrgente = !estado.teUrgente; estado.teSit = ""; }
    else { estado.teUrgente = false; estado.teSit = k === "fila" ? "" : k; }
    navegar();
  }));
  $("[data-te-limpar]")?.addEventListener("click", ()=>{ estado.teSit = ""; estado.teUrgente = false; estado.teBusca = ""; navegar(); });
  $$("[data-te-sit]").forEach(b=>b.addEventListener("click", ()=>{ estado.teSit = b.dataset.teSit; estado.teUrgente = false; navegar(); }));
  let t = null;
  $("#teBusca")?.addEventListener("input", e=>{ clearTimeout(t); const v = e.target.value; t = setTimeout(()=>{ estado.teBusca = v; navegar(); }, 350); });
  const atual = async ()=> estado.teSel ? await db.get("emails", estado.teSel) : null;
  const lerCampos = ()=> Object.fromEntries(TE_CAMPOS.map(x=>[x.id, valorDe("te_" + x.id)]));
  $("#btnTeSalvar")?.addEventListener("click", async ()=>{
    try { const e = await atual(); if (!e) return; const c = {...teCampos(e), ...lerCampos()};
      const falta = teFaltando(c); let alerta = e.alerta;
      if (alerta === "pendencia" && !falta.length) alerta = "";
      const n = {...e, campos: c, alerta}; n.status = teAtualizarStatus(n);
      await db.put("emails", n); await teLog("campos salvos", n, falta.length ? `falta: ${falta.join(", ")}` : "9 campos"); toast("Campos salvos."); navegar(); }
    catch(err){ mostrarErros("#teErros", [err.message]); }
  });
  $("#btnTeExtrair")?.addEventListener("click", async ()=>{
    try { const e = await atual(); if (!e) return; await teExtrair(e); toast("Extração executada."); navegar(); }
    catch(err){ mostrarErros("#teErros", [err.message]); }
  });
  $("#btnTeAlerta")?.addEventListener("click", async ()=>{
    try { const e = await atual(); if (!e) return; await teTratarAlerta(e); toast("Alerta tratado; confira os campos e valide."); navegar(); }
    catch(err){ mostrarErros("#teErros", [err.message]); }
  });
  $("#btnTeValidar")?.addEventListener("click", async ()=>{
    try { const e = await atual(); if (!e) return; await teValidar(e); toast("Requisição validada."); navegar(); }
    catch(err){ mostrarErros("#teErros", [err.message]); }
  });
  $("#btnTeRecusar")?.addEventListener("click", async ()=>{
    const motivo = prompt("Motivo da recusa (fictício):");
    if (motivo === null) return;
    try { const e = await atual(); if (!e) return; await teRecusar(e, motivo); toast("Requisição recusada."); navegar(); }
    catch(err){ mostrarErros("#teErros", [err.message]); }
  });
}

TELAS["#/email/:id"] = async ({id})=>{
  const e = await db.get("emails", id);
  return `<h1>E-mail</h1><p class="sub"><a href="#/painel">← Bancada de triagem</a></p>${await teDetalhe(e)}`;
};
TELAS_DEPOIS["#/email/:id"] = ({id})=>{ estado.teSel = id; teLigar(); };

TELAS["#/lote"] = async ()=>{
  const [lotes, emails] = await Promise.all([db.list("lotes"), db.list("emails")]);
  return `<h1>Lotes</h1><p class="sub">Uma rodada de extração por lote. O lote não é validado automaticamente.</p>
    <div class="grade">${lotes.map(l=>{
      const doLote = emails.filter(e=>e.lote_id === l.id), novos = doLote.filter(e=>e.status === "novo").length, validados = doLote.filter(e=>e.status === "validado").length;
      return `<div class="card"><h2 style="margin-top:0">${esc(l.nome)}</h2><p class="sub">${doLote.length} e-mails · ${novos} novos · ${validados} validados</p>
        <div class="linha-botoes"><button type="button" class="prim" data-te-lote="${esc(l.id)}">Extrair o lote</button>
        <a class="botao" href="#/planilha">Ver planilha</a></div></div>`;
    }).join("") || '<div class="card vazio">Nenhum lote.</div>'}</div>`;
};
TELAS_DEPOIS["#/lote"] = ()=>{
  $$("[data-te-lote]").forEach(b=>b.addEventListener("click", async ()=>{
    const lote = b.dataset.teLote;
    const emails = (await db.list("emails")).filter(e=>e.lote_id === lote && e.status !== "validado" && e.status !== "recusado");
    for (const e of emails) await teExtrair(e);
    toast(`${emails.length} e-mail(s) do lote ${lote} processados.`); navegar();
  }));
};

function teLinhasPlanilha(emails){ return emails.map(e=>({...e, ...teCampos(e), faltando: teFaltando(teCampos(e))})); }
function teCSV(linhas){
  const cols = ["id", "status", "prioridade", ...TE_CAMPOS.map(c=>c.id), "confianca", "alerta"];
  const cel = v => { const s = String(v ?? ""); return /[;"\n]/.test(s) ? `"${s.replace(/"/g, '""')}"` : s; };
  return "\ufeff" + [cols.join(";"), ...linhas.map(l=>cols.map(c=>cel(l[c])).join(";"))].join("\r\n");
}
TELAS["#/planilha"] = async ()=>{
  const emails = (await db.list("emails")).sort((a, b)=>String(a.id).localeCompare(String(b.id)));
  const linhas = teLinhasPlanilha(emails);
  return `<h1>Planilha consolidada</h1><p class="sub">Os 9 campos de cada e-mail, com a situação e a confiança. O CSV sai com BOM e ponto e vírgula.</p>
    <div class="linha-botoes"><button class="prim" id="btnTeCsv">Exportar CSV</button></div>
    <div class="card tabela-wrap"><table id="tabelaTeia"><thead><tr><th>E-mail</th><th>Situação</th>${TE_CAMPOS.map(c=>`<th>${esc(c.rotulo)}</th>`).join("")}<th class="num">Confiança</th></tr></thead>
      <tbody>${linhas.map(l=>`<tr><td class="mono">${esc(l.id)}</td><td><span class="selo ${teSeloStatus(l.status)}">${esc(TE_STATUS[l.status] || l.status)}</span></td>
        ${TE_CAMPOS.map(c=>`<td>${l[c.id] ? esc(l[c.id]) : '<span class="erro-txt">falta</span>'}</td>`).join("")}<td class="num">${Math.round((l.confianca || 0) * 100)}%</td></tr>`).join("")}</tbody></table></div>`;
};
TELAS_DEPOIS["#/planilha"] = ()=>{
  $("#btnTeCsv")?.addEventListener("click", async ()=>{
    const emails = await db.list("emails");
    baixar(`teia-planilha-${hojeISO()}.csv`, teCSV(teLinhasPlanilha(emails)), "text/csv;charset=utf-8");
    await registrar("planilha exportada", {detalhe: `${emails.length} e-mails`});
  });
};

async function configExtra(){
  return `<div class="card"><h2 style="margin-top:0">Dicionários da triagem</h2>
    <p class="sub">No script local, estas listas ficam em um arquivo de configuração. Aqui elas são somente leitura.</p>
    <div class="duas"><div><h3>Regionais (${TE_REGIONAIS.length})</h3><p>${TE_REGIONAIS.map(r=>`<span class="tag">${esc(r)}</span>`).join("")}</p>
      <h3>Réu preso</h3><p>${TE_CAMPOS.find(c=>c.id === "reu_preso").opcoes.map(n=>`<span class="tag">${esc(n)}</span>`).join("")}</p></div>
      <div><h3>Tipos de crime (${TE_CRIMES.length})</h3><p>${TE_CRIMES.map(c=>`<span class="tag">${esc(c)}</span>`).join("")}</p>
        <h3>Regras</h3><p class="sub">9 campos obrigatórios; divergência, PDF imagem e cobrança reiterada viram alerta; a validação é humana; nada sai da estação (LGPD).</p></div></div></div>`;
}
async function ligarConfigExtra(){}

async function iniciarApp(){
  if (!(await db.list("emails")).length){
    const seed = dadosEmbutidos("seed");
    if (seed) await db.importar({app: APP.id, dados: seed}, true);
  }
  // Deriva a situação a partir dos 9 campos e dos alertas do seed.
  for (const e of await db.list("emails")){
    const s = teAtualizarStatus(e);
    if (s !== e.status) await db.put("emails", {...e, status: s});
  }
}

teste("TEIA: 9 campos essenciais definidos", ()=> TE_CAMPOS.length === 9 && TE_CAMPOS.every(c=>c.id && c.rotulo));
teste("TEIA: campo vazio conta como falta", ()=>{
  const c = Object.fromEntries(TE_CAMPOS.map(x=>[x.id, "x"]));
  delete c.protocolo;
  const falta = teFaltando(c);
  return falta.length === 1 && falta[0] === "Protocolo";
});
teste("TEIA: validação exige os 9 campos", ()=> teFaltando({...Object.fromEntries(TE_CAMPOS.map(c=>[c.id, "x"]))}).length === 0);
teste("TEIA: divergência é alerta", ()=> !!TE_ALERTA.divergencia && !!TE_ALERTA.ocr);
teste("TEIA: status pendente quando falta campo", ()=> teAtualizarStatus({status: "extraido", campos: {protocolo: "x"}}) === "pendente");
