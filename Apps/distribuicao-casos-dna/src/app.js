/* Distribuição de Casos de DNA · código do app (Sprints 1 e 2) */
"use strict";
const DD_PROCESSADO = ["processado", "distribuido", "laudo"];
const ddDias = (a, b = hojeISO())=> a && b ? Math.round((new Date(b + "T12:00:00") - new Date(a + "T12:00:00")) / 86400000) : null;
const ddFmt = n => n === null ? "—" : n + " dia(s)";

// RN01: a rodada só é distribuída com todos os casos ordinários processados
function ddPronta(casos){ return casos.filter(c=>c.tipo === "ordinario").every(c=>DD_PROCESSADO.includes(c.status)); }
teste("RN01: rodada com ordinário aguardando não está pronta", ()=>{
  return !ddPronta([{tipo: "ordinario", status: "aguardando"}]) && ddPronta([{tipo: "ordinario", status: "processado"}, {tipo: "cobranca", status: "aguardando"}]);
});
// RN04: rotação, sem repetir o perito da rodada anterior
function ddSugerirPerito(peritos, ultimoId){
  const ativos = peritos.filter(p=>p.ativo !== false);
  if (!ativos.length) return null;
  if (!ultimoId) return ativos[0];
  const i = ativos.findIndex(p=>p.id_perito === ultimoId);
  return ativos[(i + 1) % ativos.length];
}
teste("RN04: a sugestão pula o perito da rodada anterior", ()=>{
  const ps = [{id_perito: "P1"}, {id_perito: "P2"}, {id_perito: "P3"}];
  return ddSugerirPerito(ps, "P1").id_perito === "P2" && ddSugerirPerito(ps, "P3").id_perito === "P1" && ddSugerirPerito(ps, null).id_perito === "P1";
});
teste("Exemplo com 4 peritos e 6 rodadas", ()=> dadosEmbutidos("seed").peritos.length === 4 && dadosEmbutidos("seed").rodadas.length === 6);

async function ddPeritos(){ return Object.fromEntries((await db.list("peritos")).map(p=>[p.id_perito, p])); }
async function ddCasos(rodada_id){ return (await db.porIndice("casos", "rodada_id", rodada_id)).sort((a, b)=>a.protocolo.localeCompare(b.protocolo)); }
async function ddUltimoPerito(){ const rs = (await db.list("rodadas")).filter(r=>r.perito_id).sort((a, b)=>(a.data || "").localeCompare(b.data || "")); return rs.length ? rs[rs.length - 1].perito_id : null; }
// tempo médio entre o processamento e a distribuição
function ddTempoMedio(casos){ const cs = casos.filter(c=>c.distribuido_em && c.data_processamento); return cs.length ? Math.round(cs.reduce((a, c)=>a + ddDias(c.data_processamento, c.distribuido_em.slice(0, 10)), 0) / cs.length * 10) / 10 : null; }

TELAS["#/painel"] = async ()=>{
  const [rs, cs, ps] = await Promise.all([db.list("rodadas"), db.list("casos"), ddPeritos()]);
  const semPerito = cs.filter(c=>!c.perito_id), abertas = rs.filter(r=>r.status !== "concluida");
  return `<h1>Painel da rodada</h1><p class="sub">${abertas.length} rodadas abertas. <a href="#/rodada/nova">Montar rodada</a></p>
    <div class="grade"><div class="card kpi"><div class="v" data-sem-perito>${semPerito.length}</div><div class="r">casos sem perito</div></div>
      <div class="card kpi"><div class="v">${cs.filter(c=>c.tipo === "cobranca" && !c.perito_id).length}</div><div class="r">cobranças na fila</div></div>
      <div class="card kpi"><div class="v">${ddFmt(ddTempoMedio(cs))}</div><div class="r">média processamento → distribuição</div></div>
      <div class="card kpi"><div class="v">${Object.keys(ps).length}</div><div class="r">peritos ativos</div></div></div>
    <div class="card tabela-wrap"><h2 style="margin-top:0">Rodadas</h2><table><tr><th>Rodada</th><th>Placa</th><th>Data</th><th class="num">Casos</th><th>Perito</th><th>Situação</th></tr>
      ${rs.sort((a, b)=>(b.data || "").localeCompare(a.data || "")).map(r=>{ const k = cs.filter(c=>c.rodada_id === r.id_rodada);
        return `<tr><td><a href="#/rodada/${encodeURIComponent(r.id_rodada)}">${esc(r.id_rodada)}</a></td><td class="mono">${esc(r.placa)}</td><td>${dataCurtaBR(r.data)}</td>
          <td class="num">${k.length}</td><td>${esc(ps[r.perito_id]?.nome || "—")}</td>
          <td><span class="selo ${r.status === "distribuida" ? "ok" : r.status === "concluida" ? "info" : "alerta"}">${esc(r.status)}</span></td></tr>`; }).join("")
        || '<tr><td colspan="6" class="vazio">Nenhuma rodada.</td></tr>'}</table></div>`;
};

TELAS["#/rodadas"] = async ()=>{
  const [rs, cs, ps] = await Promise.all([db.list("rodadas"), db.list("casos"), ddPeritos()]);
  return `<h1>Rodadas</h1><p class="sub"><a href="#/rodada/nova">Montar rodada</a></p>
    <div class="card tabela-wrap"><table><tr><th>Rodada</th><th>Placa</th><th>Data</th><th class="num">Ordinários</th><th class="num">Cobranças</th><th>Perito</th></tr>
      ${rs.sort((a, b)=>(b.data || "").localeCompare(a.data || "")).map(r=>{ const k = cs.filter(c=>c.rodada_id === r.id_rodada);
        return `<tr><td><a href="#/rodada/${encodeURIComponent(r.id_rodada)}">${esc(r.id_rodada)}</a></td><td class="mono">${esc(r.placa)}</td><td>${dataCurtaBR(r.data)}</td>
          <td class="num">${k.filter(c=>c.tipo === "ordinario").length}</td><td class="num">${k.filter(c=>c.tipo === "cobranca").length}</td><td>${esc(ps[r.perito_id]?.nome || "—")}</td></tr>`; }).join("")}</table></div>`;
};

TELAS["#/rodada/nova"] = async ()=>{
  const ps = await db.list("peritos");
  return `<h1>Montar rodada</h1><p class="sub">Cole os protocolos de cada fila. A rodada só é distribuída com os ordinários processados (RN01).</p>
    <form class="card" id="formDdNova" novalidate><div class="campos">
      ${campo("ddPlaca", "Placa de análise", {obrigatorio: true, ajuda: "Ex.: PL-2026-11."})}
      ${campo("ddData", "Data da rodada", {tipo: "date", valor: hojeISO(), obrigatorio: true})}
      ${campo("ddProcesso", "Processamento dos ordinários", {tipo: "select", opcoes: [["processado", "Já processados"], ["aguardando", "Aguardando processamento"]]})}</div>
    ${campo("ddOrdinarios", "Protocolos ordinários", {tipo: "textarea", linhas: 4, obrigatorio: true, ajuda: "Um por linha, ou separados por vírgula."})}
    ${campo("ddCobrancas", "Protocolos de cobrança", {tipo: "textarea", linhas: 3, ajuda: "Fila separada (RN03)."})}
    <div id="ddErros"></div><div class="linha-botoes"><button class="prim" type="submit">Criar rodada</button></div></form>
    <p class="sub">Peritos ativos: ${ps.map(p=>esc(p.nome)).join(", ") || "nenhum"}.</p>`;
};
TELAS_DEPOIS["#/rodada/nova"] = ()=>{
  $("#formDdNova").addEventListener("submit", async e=>{
    e.preventDefault();
    const rs = await db.list("rodadas"), cs = await db.list("casos");
    const nums = t => t.split(/[\s,;]+/).map(s=>s.trim()).filter(Boolean);
    const ordinarios = nums(valorDe("ddOrdinarios")), cobrancas = nums(valorDe("ddCobrancas")), erros = [];
    if (!valorDe("ddPlaca")) erros.push("Informe a placa.");
    if (!valorDe("ddData") || valorDe("ddData") > hojeISO()) erros.push("Informe a data da rodada (não pode ser futura).");
    if (!ordinarios.length) erros.push("Informe ao menos um protocolo ordinário.");
    const repetidos = [...ordinarios, ...cobrancas].filter(n=>cs.some(c=>c.protocolo === n));
    if (repetidos.length) erros.push(`Protocolo já cadastrado: ${[...new Set(repetidos)].slice(0, 5).join(", ")}.`);
    if (!mostrarErros("#ddErros", erros)) return;
    const id = "RD-" + String(rs.length + 1).padStart(3, "0"), processado = valorDe("ddProcesso");
    await db.put("rodadas", {id_rodada: id, placa: valorDe("ddPlaca"), data: valorDe("ddData"), perito_id: null, status: "aberta", criado_em: agora()});
    for (const n of ordinarios) await db.put("casos", {id_caso: uuid(), rodada_id: id, protocolo: n, tipo: "ordinario", status: processado, data_processamento: processado === "processado" ? valorDe("ddData") : null, perito_id: null, distribuido_em: null});
    for (const n of cobrancas) await db.put("casos", {id_caso: uuid(), rodada_id: id, protocolo: n, tipo: "cobranca", status: "processado", data_processamento: valorDe("ddData"), perito_id: null, distribuido_em: null});
    await db.put("log", {id: uuid(), rodada_id: id, acao: "rodada criada", perfil: estado.perfil || "", data_hora: agora()});
    await registrar("rodada criada", {detalhe: `${id} · ${ordinarios.length} ordinários e ${cobrancas.length} cobranças`});
    toast(`Rodada ${id} criada.`); location.hash = "#/rodada/" + encodeURIComponent(id);
  });
};

TELAS["#/rodada/:id"] = async ({id})=>{
  const r = await db.get("rodadas", id);
  if (!r) return `<div class="card vazio">Rodada não encontrada. <a href="#/rodadas">Voltar</a></div>`;
  const [cs, ps, ultimo] = await Promise.all([ddCasos(id), ddPeritos(), ddUltimoPerito()]);
  const ord = cs.filter(c=>c.tipo === "ordinario"), cob = cs.filter(c=>c.tipo === "cobranca"), pronta = ddPronta(cs);
  const sug = ddSugerirPerito(Object.values(ps), ultimo), pendCob = cob.filter(c=>!c.perito_id);
  const ls = (await db.porIndice("log", "rodada_id", id)).sort((a, b)=>b.data_hora.localeCompare(a.data_hora));
  return `<h1>Rodada ${esc(r.id_rodada)} <span class="selo ${r.status === "distribuida" ? "ok" : "alerta"}" id="ddStatus">${esc(r.status)}</span></h1>
    <p class="sub">Placa ${esc(r.placa)} · ${dataCurtaBR(r.data)} · ${ord.length} ordinários e ${cob.length} cobranças · perito ${esc(ps[r.perito_id]?.nome || "—")}</p>
    ${r.status !== "distribuida" ? `<form class="card" id="formDdDistribuir"><h2 style="margin-top:0">Distribuir a rodada ordinária (RN02)</h2>
      <p class="sub">${pronta ? "Todos os ordinários estão processados." : '<b class="erro-txt">Há ordinário sem processamento; a rodada não pode ser distribuída (RN01).</b>'} Sugestão pela rotação (RN04): <b>${esc(sug?.nome || "—")}</b>.</p>
      <div class="campos">${campo("ddPerito", "Perito", {tipo: "select", opcoes: [["", "Escolha"], ...Object.values(ps).map(p=>[p.id_perito, p.nome])], valor: sug?.id_perito || ""})}</div>
      <div id="ddErrosDist"></div><div class="linha-botoes"><button class="prim" type="submit" ${pronta ? "" : "disabled"}>Distribuir os ${ord.length} ordinários</button>
        ${pronta ? "" : '<button type="button" id="btnDdProcessar">Registrar o processamento dos ordinários</button>'}</div></form>`
    : `<div class="card"><b>Rodada distribuída</b> para ${esc(ps[r.perito_id]?.nome || "")}.</div>`}
    ${pendCob.length ? `<div class="card"><h2 style="margin-top:0">Fila de cobranças (RN03)</h2><p class="sub">${pendCob.length} cobrança(s) aguardando perito, em fila separada.</p>
      <div class="linha-botoes"><button id="btnDdCobrancas">Distribuir as cobranças em rodízio</button></div></div>` : ""}
    <div class="card tabela-wrap"><h2 style="margin-top:0">Casos (${cs.length})</h2><table id="tabelaCasos"><tr><th>Protocolo</th><th>Tipo</th><th>Processamento</th><th>Perito</th><th>Distribuído em</th><th>Espera</th></tr>
      ${cs.map(c=>`<tr><td class="mono">${esc(c.protocolo)}</td><td>${esc(c.tipo)}</td><td>${dataCurtaBR(c.data_processamento) || "—"}</td>
        <td>${esc(ps[c.perito_id]?.nome || "—")}</td><td>${dataCurtaBR(c.distribuido_em) || "—"}</td>
        <td>${c.distribuido_em ? ddFmt(ddDias(c.data_processamento, c.distribuido_em.slice(0, 10))) : "—"}</td></tr>`).join("")}</table></div>
    <div class="card tabela-wrap"><h2 style="margin-top:0">Histórico</h2><table><tr><th>Data e hora</th><th>Ação</th></tr>
      ${ls.map(x=>`<tr><td>${dataBR(x.data_hora)}</td><td>${esc(x.acao)}</td></tr>`).join("")}</table></div>`;
};
TELAS_DEPOIS["#/rodada/:id"] = ({id})=>{
  $("#formDdDistribuir")?.addEventListener("submit", async e=>{
    e.preventDefault();
    const r = await db.get("rodadas", id), cs = await ddCasos(id), perito = valorDe("ddPerito"), erros = [];
    if (!perito) erros.push("Escolha o perito da rodada.");
    if (!ddPronta(cs)) erros.push("Há caso ordinário sem processamento (RN01).");
    if (!mostrarErros("#ddErrosDist", erros)) return;
    const quando = agora();
    for (const c of cs.filter(x=>x.tipo === "ordinario")) await db.put("casos", {...c, perito_id: perito, distribuido_em: quando, status: "distribuido"});
    await db.put("rodadas", {...r, perito_id: perito, status: "distribuida"});
    await db.put("log", {id: uuid(), rodada_id: id, acao: `rodada distribuída (${cs.filter(x=>x.tipo === "ordinario").length} ordinários)`, perfil: estado.perfil || "", data_hora: quando});
    await registrar("rodada distribuída", {detalhe: `${id} · ${perito}`});
    toast("Rodada distribuída."); navegar();
  });
  $("#btnDdProcessar")?.addEventListener("click", async ()=>{
    const cs = await ddCasos(id), hoje = hojeISO();
    for (const c of cs.filter(x=>x.tipo === "ordinario" && x.status === "aguardando")) await db.put("casos", {...c, status: "processado", data_processamento: hoje});
    await db.put("log", {id: uuid(), rodada_id: id, acao: "processamento dos ordinários registrado", perfil: estado.perfil || "", data_hora: agora()});
    toast("Processamento registrado. A rodada pode ser distribuída."); navegar();
  });
  $("#btnDdCobrancas")?.addEventListener("click", async ()=>{
    const cs = await ddCasos(id), ps = Object.values(await ddPeritos()), pend = cs.filter(c=>c.tipo === "cobranca" && !c.perito_id);
    const quando = agora();
    for (const [k, c] of pend.entries()) await db.put("casos", {...c, perito_id: ps[k % ps.length].id_perito, distribuido_em: quando, status: "distribuido"});
    await db.put("log", {id: uuid(), rodada_id: id, acao: `${pend.length} cobrança(s) distribuída(s)`, perfil: estado.perfil || "", data_hora: quando});
    toast("Cobranças distribuídas na fila separada."); navegar();
  });
};
