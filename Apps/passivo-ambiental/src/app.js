/* Passivo Ambiental · código do app (Sprints 1 e 2) */
"use strict";
const PA_PRAZO_PADRAO = 10;
const paDias = (a, b = hojeISO())=> Math.round((new Date(b + "T12:00:00") - new Date(a + "T12:00:00")) / 86400000);
// atrasada: passou o prazo e o laudo não foi concluído
function paAtrasada(r, hoje = hojeISO()){ return r.status !== "concluida" && paDias(r.data_requisicao, hoje) > Number(r.prazo_dias || PA_PRAZO_PADRAO); }
function paRestantes(r, hoje = hojeISO()){ return Number(r.prazo_dias || PA_PRAZO_PADRAO) - paDias(r.data_requisicao, hoje); }
teste("Prazo: 12 dias com prazo 10 está atrasada; 5 dias não", ()=>{
  const r = {status: "recebida", data_requisicao: "2026-10-17", prazo_dias: 10}, hoje = "2026-10-29";
  return paAtrasada(r, hoje) && !paAtrasada({...r, data_requisicao: "2026-10-24"}, hoje) && !paAtrasada({...r, status: "concluida"}, hoje);
});
teste("Exemplo com 12 requisições e 2 mapas", ()=> dadosEmbutidos("seed").requisicoes.length === 12);

const PA_STATUS = {recebida: "Recebida", laudo: "Laudo em elaboração", concluida: "Concluída"};

TELAS["#/painel"] = async ()=>{
  const rs = await db.list("requisicoes"), ls = await db.list("laudos"), hoje = hojeISO();
  const atras = rs.filter(r=>paAtrasada(r, hoje)), abertas = rs.filter(r=>r.status !== "concluida");
  const horas = ls.reduce((a, l)=>a + Number(l.horas_trabalhadas || 0), 0), concl = rs.filter(r=>r.status === "concluida").length;
  return `<h1>Painel do Passivo Ambiental</h1><p class="sub">${rs.length} requisições no recorte. <a href="#/requisicao/nova">Registrar requisição</a></p>
    <div class="grade"><div class="card kpi"><div class="v">${abertas.length}</div><div class="r">requisições abertas</div></div>
      <div class="card kpi"><div class="v" data-atrasadas>${atras.length}</div><div class="r">fora do prazo</div></div>
      <div class="card kpi"><div class="v">${concl}</div><div class="r">laudos concluídos</div></div>
      <div class="card kpi"><div class="v">${horas}h</div><div class="r">horas de elaboração registradas</div></div></div>
    <div class="card tabela-wrap"><h2 style="margin-top:0">Fora do prazo</h2><table><tr><th>Requisição</th><th>Órgão</th><th>Recebida</th><th class="num">Dias</th><th>Situação</th></tr>
      ${atras.sort((a, b)=>a.data_requisicao.localeCompare(b.data_requisicao)).map(r=>`<tr><td><a href="#/laudo/${encodeURIComponent(r.id_requisicao)}">${esc(r.numero_processo)}</a></td>
        <td>${esc(r.orgao)}</td><td>${dataCurtaBR(r.data_requisicao)}</td><td class="num">${paDias(r.data_requisicao)}</td><td><span class="selo erro">atrasada</span></td></tr>`).join("")
        || '<tr><td colspan="5" class="vazio">Nenhuma requisição fora do prazo.</td></tr>'}</table></div>`;
};

TELAS["#/requisicoes"] = async ()=>{
  const rs = (await db.list("requisicoes")).sort((a, b)=>b.data_requisicao.localeCompare(a.data_requisicao)), hoje = hojeISO();
  return `<h1>Requisições</h1><p class="sub"><a href="#/requisicao/nova">Registrar requisição</a></p>
    <div class="card tabela-wrap"><table id="tabelaReq"><tr><th>Requisição</th><th>Órgão</th><th>Tipo</th><th>Recebida</th><th>Prazo</th><th>Situação</th></tr>
      ${rs.map(r=>{ const rest = paRestantes(r, hoje), atras = paAtrasada(r, hoje);
        return `<tr><td><a href="#/laudo/${encodeURIComponent(r.id_requisicao)}">${esc(r.numero_processo)}</a></td><td>${esc(r.orgao)}</td>
          <td>${esc(r.tipo_infracao)}</td><td>${dataCurtaBR(r.data_requisicao)}</td>
          <td>${r.status === "concluida" ? "—" : atras ? '<span class="selo erro">vencido</span>' : `<span class="selo ${rest <= 3 ? "alerta" : "ok"}">${rest} dia(s)</span>`}</td>
          <td>${esc(PA_STATUS[r.status] || r.status)}</td></tr>`; }).join("")}</table></div>`;
};

TELAS["#/requisicao/nova"] = async ()=> `<h1>Registrar requisição</h1><p class="sub">Use apenas dados fictícios. Ao salvar, o laudo abre com o cabeçalho preenchido (RN01).</p>
  <form class="card" id="formPaNova" novalidate><div class="campos">
    ${campo("paNumero", "Número do processo/requisição", {obrigatorio: true})}
    ${campo("paOrgao", "Órgão requisitante", {obrigatorio: true, ajuda: "Ex.: Delegacia de Polícia de Cuiabá."})}
    ${campo("paData", "Data da requisição", {tipo: "date", valor: hojeISO(), obrigatorio: true})}
    ${campo("paTipo", "Tipo de infração ambiental", {obrigatorio: true})}
    ${campo("paPrazo", "Prazo (dias)", {tipo: "number", valor: PA_PRAZO_PADRAO, attrs: 'min="1" step="1"', obrigatorio: true})}</div>
  ${campo("paLocal", "Local do dano", {obrigatorio: true})}
  ${campo("paCoord", "Coordenadas (latitude, longitude)", {ajuda: "Opcional; usadas no mapa do laudo."})}
  <div id="paErros"></div><div class="linha-botoes"><button class="prim" type="submit">Registrar e abrir o laudo</button></div></form>`;
TELAS_DEPOIS["#/requisicao/nova"] = ()=>{
  $("#formPaNova").addEventListener("submit", async e=>{
    e.preventDefault();
    const d = {numero_processo: valorDe("paNumero"), orgao: valorDe("paOrgao"), data_requisicao: valorDe("paData"), tipo_infracao: valorDe("paTipo"),
      prazo_dias: Number(valorDe("paPrazo")), local: valorDe("paLocal"), coordenadas: valorDe("paCoord")};
    const rs = await db.list("requisicoes"), erros = [];
    if (!d.numero_processo) erros.push("Informe o número do processo.");
    else if (rs.some(r=>normalizar(r.numero_processo) === normalizar(d.numero_processo))) erros.push("Esta requisição já está cadastrada.");
    if (!d.orgao) erros.push("Informe o órgão requisitante.");
    if (!d.data_requisicao || d.data_requisicao > hojeISO()) erros.push("Informe a data da requisição (não pode ser futura).");
    if (!(d.prazo_dias > 0)) erros.push("O prazo precisa ser de pelo menos 1 dia.");
    if (!d.tipo_infracao) erros.push("Informe o tipo de infração.");
    if (!d.local) erros.push("Informe o local do dano.");
    if (!mostrarErros("#paErros", erros)) return;
    const id = "REQ-" + String(rs.length + 1).padStart(4, "0");
    await db.put("requisicoes", {id_requisicao: id, ...d, status: "laudo", criado_em: agora()});
    await db.put("laudos", {id_laudo: "L-" + id, requisicao_id: id, status: "rascunho", local: d.local, coordenadas: d.coordenadas,
      tipo_infracao: d.tipo_infracao, criado_em: agora(), horas_trabalhadas: 0});
    await registrar("requisição registrada", {detalhe: `${d.numero_processo} · ${d.orgao}`});
    toast(`Requisição registrada. Laudo L-${id} aberto.`); location.hash = "#/laudo/" + encodeURIComponent(id);
  });
};

// RN01: o cabeçalho vem da requisição e pode ser ajustado antes de salvar
function paCabecalho(r, l){
  return [
    ["Número do processo", r.numero_processo], ["Órgão requisitante", r.orgao], ["Data da requisição", dataCurtaBR(r.data_requisicao)],
    ["Tipo de infração ambiental", l.tipo_infracao || r.tipo_infracao], ["Local do dano", l.local || r.local], ["Coordenadas", l.coordenadas || r.coordenadas || "não informadas"]
  ];
}
TELAS["#/laudo/:id"] = async ({id})=>{
  const r = await db.get("requisicoes", id);
  if (!r) return `<div class="card vazio">Requisição não encontrada. <a href="#/requisicoes">Voltar</a></div>`;
  const ls = await db.porIndice("laudos", "requisicao_id", id), l = ls[0] || {id_laudo: "L-" + id, status: "rascunho", horas_trabalhadas: 0};
  const cab = paCabecalho(r, l), completo = cab.every(([, v])=>String(v || "").trim() && !/não informad/i.test(v));
  return `<h1>Laudo ${esc(l.id_laudo)} <span class="selo ${l.status === "concluido" ? "ok" : "info"}" id="paStatusLaudo">${esc(l.status)}</span></h1>
    <p class="sub">Requisição ${esc(r.numero_processo)} · ${esc(r.orgao)} · recebida em ${dataCurtaBR(r.data_requisicao)} · prazo ${r.prazo_dias} dias</p>
    <form class="card" id="formPaLaudo"><h2 style="margin-top:0">Cabeçalho (RN01)</h2>
      <div class="tabela-wrap"><table id="tabelaCabecalho">${cab.map(([k, v])=>`<tr><th>${esc(k)}</th><td>${esc(v)}</td></tr>`).join("")}</table></div>
      <div class="campos">${campo("paLocalL", "Local do dano (ajuste)", {valor: l.local || r.local})}
        ${campo("paCoordL", "Coordenadas (ajuste)", {valor: l.coordenadas || r.coordenadas || ""})}</div>
      ${campo("paHoras", "Horas trabalhadas neste laudo", {tipo: "number", valor: l.horas_trabalhadas || 0, attrs: 'min="0" step="0.5"'})}
      <div id="paErrosLaudo"></div><div class="linha-botoes"><button class="prim" type="submit">Salvar rascunho</button>
        <button type="button" id="btnPaConcluir">Concluir o laudo</button></div></form>`;
};
TELAS_DEPOIS["#/laudo/:id"] = ({id})=>{
  const salvar = async ()=> {
    const r = await db.get("requisicoes", id), ls = await db.porIndice("laudos", "requisicao_id", id);
    const l = {...(ls[0] || {id_laudo: "L-" + id, requisicao_id: id}), local: valorDe("paLocalL"), coordenadas: valorDe("paCoordL"),
      horas_trabalhadas: Number(valorDe("paHoras") || 0)};
    await db.put("laudos", l); return l;
  };
  $("#formPaLaudo")?.addEventListener("submit", async e=>{ e.preventDefault(); const l = await salvar(); await registrar("laudo salvo", {detalhe: l.id_laudo}); toast("Rascunho salvo."); navegar(); });
  $("#btnPaConcluir")?.addEventListener("click", async ()=>{
    const r = await db.get("requisicoes", id), mapas = await db.porIndice("mapas", "laudo_id", "L-" + id), l = await salvar();
    const cab = paCabecalho(r, l), semCab = cab.filter(([, v])=>!String(v || "").trim() || /não informad/i.test(v)).map(([k])=>k);
    const erros = [...semCab.map(k=>`Cabeçalho incompleto: ${k}.`), !mapas.length && "Anexe pelo menos 1 mapa temático (RN03)."].filter(Boolean);
    if (!mostrarErros("#paErrosLaudo", erros)) return;
    await db.put("laudos", {...l, status: "concluido", concluido_em: agora()});
    await db.put("requisicoes", {...r, status: "concluida"});
    await registrar("laudo concluído", {detalhe: l.id_laudo}); toast("Laudo concluído."); navegar();
  });
};
