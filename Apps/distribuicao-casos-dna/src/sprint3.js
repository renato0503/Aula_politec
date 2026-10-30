/* ================= Sprint 3 · Sugestão por histórico de rotação, fila de urgência e alerta de rodada parada ================= */
/* A sugestão do Sprint 3 usa o histórico de rotação: o perito que faz mais tempo sem rodada e que
   recebeu menos casos é o primeiro da lista. A rotação do Sprint 2 (RN04) continua valendo como desempate. */
function ddHistorico(peritos, rodadas, casos){
  const hoje = hojeISO();
  return peritos.map(p=>{
    const rs = rodadas.filter(r=>r.perito_id === p.id_perito).sort((a, b)=>(b.data || "").localeCompare(a.data || ""));
    const meus = casos.filter(c=>c.perito_id === p.id_perito);
    const ultima = rs[0]?.data || null;
    const dias = ultima ? ddDias(ultima, hoje) : 999;
    return {perito: p, id_perito: p.id_perito, nome: p.nome, ultima, dias, carga: meus.length, rodadas: rs.length};
  }).sort((a, b)=>b.dias - a.dias || a.carga - b.carga || a.id_perito.localeCompare(b.id_perito));
}
function ddSugerir3(peritos, rodadas, casos, ultimoId){
  const ativos = peritos.filter(p=>p.ativo !== false);
  if (!ativos.length) return null;
  const hist = ddHistorico(ativos, rodadas, casos);
  const candidatos = hist.filter(h=>h.id_perito !== ultimoId);
  return (candidatos[0] || hist[0]);
}
teste("Sugestão: o perito que está há mais tempo sem rodada vem primeiro", ()=>{
  const peritos = [{id_perito: "P1", ativo: true}, {id_perito: "P2", ativo: true}, {id_perito: "P3", ativo: true}];
  const rodadas = [{perito_id: "P1", data: "2026-10-20"}, {perito_id: "P2", data: "2026-10-05"}, {perito_id: "P3", data: "2026-10-25"}];
  const hist = ddHistorico(peritos, rodadas, []);
  return hist[0].id_perito === "P2" && hist[1].id_perito === "P1" && hist[2].id_perito === "P3";
});
teste("Sugestão: perito inativo sai da lista e o da rodada anterior fica de fora", ()=>{
  const peritos = [{id_perito: "P1", ativo: true}, {id_perito: "P2", ativo: true}, {id_perito: "P3", ativo: false}];
  const rodadas = [{perito_id: "P1", data: "2026-10-20"}, {perito_id: "P2", data: "2026-10-05"}, {perito_id: "P3", data: "2026-10-01"}];
  const s = ddSugerir3(peritos, rodadas, [], "P2");
  return s.id_perito === "P1" && ddSugerir3(peritos, rodadas, [], "P1").id_perito === "P2";
});

/* Fila de urgência: só entra com justificativa (RN05) e a ordem é por prioridade declarada. */
const DD_PRIORIDADES = {critico: 3, alta: 2, media: 1};
const DD_ROTULO = {critico: "Crítico", alta: "Alta", media: "Média"};
function ddFaltandoUrgencia(c){
  const falta = [];
  if (!c.prioridade) falta.push("prioridade");
  if (!String(c.justificativa || "").trim()) falta.push("justificativa");
  return falta;
}
function ddOrdenarUrgencia(casos){
  return (casos || []).filter(c=>c.urgente).sort((a, b)=>(DD_PRIORIDADES[b.prioridade] || 0) - (DD_PRIORIDADES[a.prioridade] || 0)
    || String(a.urgencia_em || "").localeCompare(String(b.urgencia_em || "")));
}
teste("Urgência: a fila só aceita caso com prioridade e justificativa (RN05)", ()=>{
  return ddFaltandoUrgencia({prioridade: "alta", justificativa: "prazo"}).length === 0
    && ddFaltandoUrgencia({prioridade: "alta"}).join() === "justificativa"
    && ddFaltandoUrgencia({justificativa: "x"}).join() === "prioridade";
});
teste("Urgência: a fila ordena por prioridade (crítico, alta, média)", ()=>{
  const fila = ddOrdenarUrgencia([
    {id_caso: "a", urgente: true, prioridade: "media"}, {id_caso: "b", urgente: true, prioridade: "critico"},
    {id_caso: "c", urgente: true, prioridade: "alta"}, {id_caso: "d", urgente: false, prioridade: "critico"}]);
  return fila.map(c=>c.id_caso).join() === "b,c,a";
});

/* Alerta de rodada parada: rodada aberta há mais de N dias sem distribuição. */
const DD_DIAS_PARADA = 5;
function ddParada(r, hoje = hojeISO()){
  if (r.status === "distribuida" || r.status === "concluida") return false;
  const d = ddDias(r.data, hoje);
  return d !== null && d > DD_DIAS_PARADA;
}
teste("Rodada parada: só a rodada aberta há mais de 5 dias entra no alerta", ()=>{
  const hoje = "2026-10-29";
  return ddParada({data: "2026-10-20", status: "aberta"}, hoje) && !ddParada({data: "2026-10-27", status: "aberta"}, hoje)
    && !ddParada({data: "2026-10-20", status: "distribuida"}, hoje);
});

async function ddUrgencias(rodada_id){ return db.porIndice("urgencias", "rodada_id", rodada_id); }

/* ---------- painel: alerta de rodada parada e fila de urgência ---------- */
const ddPainelS2 = TELAS["#/painel"];
TELAS["#/painel"] = async ()=>{
  let html = await ddPainelS2();
  const [rs, cs, ps] = await Promise.all([db.list("rodadas"), db.list("casos"), ddPeritos()]);
  const paradas = rs.filter(r=>ddParada(r)), urg = ddOrdenarUrgencia(cs);
  const bloco = `<div class="card" id="ddCardParada"><h2 style="margin-top:0">Alerta de rodada parada</h2>
    <p class="sub">Rodada aberta há mais de ${DD_DIAS_PARADA} dias sem distribuição.</p>
    ${paradas.length ? `<table id="tabelaParadas"><tr><th>Rodada</th><th>Placa</th><th>Data</th><th class="num">Dias</th></tr>
      ${paradas.sort((a, b)=>(a.data || "").localeCompare(b.data || "")).map(r=>`<tr><td><a href="#/rodada/${encodeURIComponent(r.id_rodada)}">${esc(r.id_rodada)}</a></td>
        <td class="mono">${esc(r.placa)}</td><td>${dataCurtaBR(r.data)}</td><td class="num">${ddDias(r.data)}</td></tr>`).join("")}</table>`
      : '<p class="sub">Nenhuma rodada parada.</p>'}</div>
    <div class="card" id="ddCardUrgencia"><h2 style="margin-top:0">Fila de urgência (RN05)</h2>
    <p class="sub">Casos marcados como urgentes, com a justificativa registrada. A ordem é por prioridade.</p>
    ${urg.length ? `<table id="tabelaUrgencia"><tr><th>Protocolo</th><th>Rodada</th><th>Prioridade</th><th>Justificativa</th></tr>
      ${urg.map(c=>`<tr><td class="mono">${esc(c.protocolo)}</td><td><a href="#/rodada/${encodeURIComponent(c.rodada_id)}">${esc(c.rodada_id)}</a></td>
        <td><span class="selo ${c.prioridade === "critico" ? "erro" : c.prioridade === "alta" ? "alerta" : "info"}">${esc(DD_ROTULO[c.prioridade] || c.prioridade)}</span></td>
        <td>${esc(c.justificativa)}</td></tr>`).join("")}</table>`
      : '<p class="sub">Nenhum caso marcado como urgente.</p>'}</div>`;
  return html + bloco;
};

/* ---------- ficha da rodada: sugestão por histórico, urgência e parada ---------- */
const ddRodadaS2 = TELAS["#/rodada/:id"], ddRodadaDepoisS2 = TELAS_DEPOIS["#/rodada/:id"];
TELAS["#/rodada/:id"] = async ({id})=>{
  let html = await ddRodadaS2({id});
  const [cs, ps, rs] = await Promise.all([ddCasos(id), ddPeritos(), db.list("rodadas")]);
  const hist = ddHistorico(Object.values(ps), rs, cs), sug3 = ddSugerir3(Object.values(ps), rs, cs, null);
  const rodada = await db.get("rodadas", id);
  const parada = rodada ? ddParada(rodada) : false;
  const card = `<div class="card" id="ddCardSugestao"><h2 style="margin-top:0">Sugestão do próximo perito</h2>
    <p class="sub">Ordem pelo histórico de rotação: primeiro quem está há mais tempo sem rodada, depois quem tem menos casos.</p>
    <table id="tabelaSugestao"><tr><th>Perito</th><th>Última rodada</th><th class="num">Dias sem rodada</th><th class="num">Casos</th></tr>
      ${hist.map(h=>`<tr${h.id_perito === sug3?.id_perito ? ' id="ddSugerido"' : ""}><td>${esc(h.nome)}${h.id_perito === sug3?.id_perito ? ' <span class="selo ok">sugerido</span>' : ""}</td>
        <td>${h.ultima ? dataCurtaBR(h.ultima) : "—"}</td><td class="num">${h.dias === 999 ? "—" : h.dias}</td><td class="num">${h.carga}</td></tr>`).join("")}</table></div>
    <div class="card" id="ddCardUrgenciaRodada"><h2 style="margin-top:0">Marcar caso como urgente (RN05)</h2>
    ${parada ? `<div class="card pendente"><b>Rodada parada:</b> aberta há ${ddDias(rodada.data)} dias sem distribuição.</div>` : ""}
    <form id="formDdUrgencia" novalidate><div class="campos">
      ${campo("ddUrgCaso", "Caso", {tipo: "select", opcoes: [["", "Escolha"], ...cs.filter(c=>!c.perito_id).map(c=>[c.id_caso, `${c.protocolo} · ${c.tipo}`])]})}
      ${campo("ddUrgPrioridade", "Prioridade", {tipo: "select", opcoes: [["", "Escolha"], ["critico", "Crítico"], ["alta", "Alta"], ["media", "Média"]]})}</div>
      ${campo("ddUrgJustificativa", "Justificativa", {obrigatorio: true, ajuda: "Ex.: prazo judicial em 5 dias."})}
      <div id="ddErrosUrgencia"></div><div class="linha-botoes"><button class="prim" type="submit">Marcar como urgente</button></div></form>
    <ul class="check-lista" id="ddListaUrgencia">
      ${ddOrdenarUrgencia(cs).map(c=>`<li class="feito">${icone("alerta")}<span><b class="mono">${esc(c.protocolo)}</b> · ${esc(c.prioridade)}
        <br><small class="sub">${esc(c.justificativa || "")}</small></span></li>`).join("") || '<li class="vazio">Nenhum caso urgente nesta rodada.</li>'}</ul></div>`;
  return html + card;
};
TELAS_DEPOIS["#/rodada/:id"] = async ({id})=>{
  await ddRodadaDepoisS2({id});
  $("#formDdUrgencia")?.addEventListener("submit", async e=>{
    e.preventDefault();
    const caso_id = valorDe("ddUrgCaso"), dados = {urgente: true, prioridade: valorDe("ddUrgPrioridade"), justificativa: valorDe("ddUrgJustificativa")};
    const erros = [];
    if (!caso_id) erros.push("Escolha o caso.");
    for (const f of ddFaltandoUrgencia(dados)) erros.push(`Falta ${f} (RN05).`);
    if (!mostrarErros("#ddErrosUrgencia", erros)) return;
    const c = await db.get("casos", caso_id);
    await db.put("casos", {...c, ...dados, urgencia_em: agora()});
    await db.put("urgencias", {id_urgencia: uuid(), rodada_id: id, caso_id, prioridade: dados.prioridade, justificativa: dados.justificativa, data_hora: agora(), perfil: estado.perfil || ""});
    await db.put("log", {id: uuid(), rodada_id: id, acao: `caso marcado como urgente (${dados.prioridade})`, perfil: estado.perfil || "", data_hora: agora()});
    await registrar("caso marcado como urgente", {detalhe: `${id} · ${c.protocolo}`});
    toast("Caso marcado como urgente."); navegar();
  });
};
