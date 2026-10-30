/* ================= Sprint 3 · Pesquisa de preços, alerta de inconsistência e histórico por objeto ================= */
/* Regra: a pesquisa de preços exige três cotações (RN04) e o alerta entra quando o cotado foge do estimado. */
const CA_COTACOES_MIN = 3;
const CA_TOLERANCIA = 0.30;   // 30% de diferença entre o estimado e a média cotada

/* RN04: só há pesquisa válida com três cotações, valor estimado e objeto */
function caFaltandoPesquisa(est){
  const falta = [];
  if (!est.objeto) falta.push("objeto");
  if (!(Number(est.valor_estimado_c) > 0)) falta.push("valor estimado");
  const cot = (est.cotacoes || []).filter(c=>Number(c.valor_c) > 0);
  if (cot.length < CA_COTACOES_MIN) falta.push(`${CA_COTACOES_MIN} cotações com valor`);
  return falta;
}
// média, mediana e o quanto a média foge do estimado
function caResumoPesquisa(est){
  const vals = (est.cotacoes || []).map(c=>Number(c.valor_c || 0)).filter(v=>v > 0).sort((a, b)=>a - b);
  const n = vals.length;
  const media = n ? Math.round(vals.reduce((a, v)=>a + v, 0) / n) : 0;
  const mediana = n ? (n % 2 ? vals[(n - 1) / 2] : Math.round((vals[n / 2 - 1] + vals[n / 2]) / 2)) : 0;
  const est_c = Number(est.valor_estimado_c || 0);
  const desvio = est_c && media ? (media - est_c) / est_c : 0;
  return {n, media, mediana, menor: vals[0] || 0, maior: vals[n - 1] || 0, desvio, variacao: Math.round(desvio * 100)};
}
// alerta: o cotado difere do estimado acima da tolerância
function caAlertaEstimado(est){
  const r = caResumoPesquisa(est);
  return r.n >= CA_COTACOES_MIN && Math.abs(r.desvio) > CA_TOLERANCIA;
}
teste("Pesquisa: sem três cotações ou sem valor estimado, a pesquisa é recusada", ()=>{
  const base = {objeto: "Notebooks", valor_estimado_c: 1000000};
  return caFaltandoPesquisa(base).join() === "3 cotações com valor" && caFaltandoPesquisa({...base, cotacoes: [{valor_c: 1}, {valor_c: 2}]}).length === 1
    && caFaltandoPesquisa({objeto: "", valor_estimado_c: 0, cotacoes: [{valor_c: 1}, {valor_c: 2}, {valor_c: 3}]}).join() === "objeto,valor estimado";
});
teste("Pesquisa: a média e a mediana das cotações", ()=>{
  const r = caResumoPesquisa({valor_estimado_c: 1000000, cotacoes: [{valor_c: 900000}, {valor_c: 1000000}, {valor_c: 1100000}]});
  return r.media === 1000000 && r.mediana === 1000000 && r.menor === 900000 && r.maior === 1100000;
});
teste("Alerta: o cotado 40% acima do estimado é alertado; 10% não", ()=>{
  const alta = {valor_estimado_c: 1000000, cotacoes: [{valor_c: 1400000}, {valor_c: 1400000}, {valor_c: 1400000}]};
  const baixa = {valor_estimado_c: 1000000, cotacoes: [{valor_c: 1100000}, {valor_c: 1100000}, {valor_c: 1100000}]};
  return caAlertaEstimado(alta) && !caAlertaEstimado(baixa) && caResumoPesquisa(alta).variacao === 40;
});

async function caPesquisas(processo_id){ return (await db.porIndice("pesquisas", "processo_id", processo_id)).sort((a, b)=>(b.data_hora || "").localeCompare(a.data_hora || "")); }

/* ---------- ficha do processo: pesquisa de preços ---------- */
const caFichaS2 = TELAS["#/processo/:id"], caFichaDepoisS2 = TELAS_DEPOIS["#/processo/:id"];
TELAS["#/processo/:id"] = async ({id})=>{
  let html = await caFichaS2({id});
  const p = await db.get("processos", id);
  if (!p) return html;
  const pesquisas = await caPesquisas(id);
  const card = `<div class="card" id="caCardPesquisa"><h2 style="margin-top:0">Pesquisa de preços (RN04)</h2>
    <p class="sub">Três cotações com o valor de cada fornecedor. O app calcula a média e a mediana e avisa quando o cotado foge do estimado.</p>
    <form id="formCaPesquisa" novalidate><div class="campos">
      ${campo("caPesqObjeto", "Objeto da pesquisa", {valor: p.objeto, obrigatorio: true})}
      ${campo("caPesqEstimado", "Valor estimado (R$)", {tipo: "number", attrs: 'min="0" step="0.01"', obrigatorio: true})}</div>
      <h3>Cotações</h3>
      <div class="campos">
        ${[1, 2, 3].map(k=>campo("caCotFornecedor" + k, `Fornecedor ${k}`, {})).join("")}
        ${[1, 2, 3].map(k=>campo("caCotValor" + k, `Valor cotado ${k} (R$)`, {tipo: "number", attrs: 'min="0" step="0.01"'})).join("")}
        ${[1, 2, 3].map(k=>campo("caCotData" + k, `Data da cotação ${k}`, {tipo: "date", valor: hojeISO()})).join("")}</div>
    <div id="caErrosPesquisa"></div><div class="linha-botoes"><button class="prim" type="submit">Registrar pesquisa</button></div></form>
    ${pesquisas.length ? `<div id="caHistoricoPrecos">${pesquisas.map(q=>{ const r = caResumoPesquisa(q), alerta = caAlertaEstimado(q);
      return `<div class="card ${alerta ? "pendente" : ""}" style="margin-bottom:10px"><b>${esc(q.objeto)}</b> · ${dataCurtaBR(q.data_hora)}
        <div class="grade" style="margin-top:8px">
          <div class="card kpi"><div class="v">${dinheiro.fmt(r.media)}</div><div class="r">média das cotações</div></div>
          <div class="card kpi"><div class="v">${dinheiro.fmt(r.mediana)}</div><div class="r">mediana</div></div>
          <div class="card kpi"><div class="v">${r.variacao > 0 ? "+" : ""}${r.variacao}%</div><div class="r">diferença do estimado</div></div></div>
        ${alerta ? `<p class="erro-txt"><b>Alerta:</b> a média cotada está ${Math.abs(r.variacao)}% ${r.variacao > 0 ? "acima" : "abaixo"} do estimado (tolerância de ${Math.round(CA_TOLERANCIA * 100)}%). A justificativa vai no relatório.</p>` : ""}
        <table><tr><th>Fornecedor</th><th>Valor</th><th>Data</th></tr>${q.cotacoes.map(c=>`<tr><td>${esc(c.fornecedor)}</td><td class="num">${dinheiro.fmt(Number(c.valor_c || 0))}</td><td>${dataCurtaBR(c.data)}</td></tr>`).join("")}</table>
      </div>`; }).join("")}</div>` : '<p class="sub" id="caSemPesquisa">Nenhuma pesquisa de preços registrada neste processo.</p>'}</div>`;
  return html + card;
};
TELAS_DEPOIS["#/processo/:id"] = async ({id})=>{
  await caFichaDepoisS2({id});
  $("#formCaPesquisa")?.addEventListener("submit", async e=>{
    e.preventDefault();
    const cotacoes = [1, 2, 3].map(k=>({fornecedor: valorDe("caCotFornecedor" + k), valor_c: dinheiro.de(valorDe("caCotValor" + k)), data: valorDe("caCotData" + k)}));
    const est = {objeto: valorDe("caPesqObjeto"), valor_estimado_c: dinheiro.de(valorDe("caPesqEstimado")), cotacoes};
    const falta = caFaltandoPesquisa(est);
    if (!mostrarErros("#caErrosPesquisa", falta.map(f=>`Pesquisa incompleta: falta ${f} (RN04).`))) return;
    await db.put("pesquisas", {id_pesquisa: uuid(), processo_id: id, ...est, data_hora: agora(), perfil: estado.perfil || ""});
    await db.put("log", {id: uuid(), processo_id: id, acao: `pesquisa de preços registrada (${est.cotacoes.length} cotações)`, perfil: estado.perfil || "", data_hora: agora()});
    await registrar("pesquisa de preços registrada", {detalhe: id});
    toast("Pesquisa registrada."); navegar();
  });
};

/* ---------- histórico de preços por objeto ---------- */
TELAS["#/precos"] = async ()=>{
  const [ps, pr] = await Promise.all([db.list("processos"), db.list("pesquisas")]);
  const porObjeto = {};
  for (const q of pr){ const chave = normalizar(q.objeto || "sem objeto"); (porObjeto[chave] ||= []).push(q); }
  const linhas = Object.entries(porObjeto).map(([chave, qs])=>{
    const ordenadas = qs.sort((a, b)=>(a.data_hora || "").localeCompare(b.data_hora || ""));
    const primeira = caResumoPesquisa(ordenadas[0]), ultima = caResumoPesquisa(ordenadas[ordenadas.length - 1]);
    const var_pct = primeira.media ? Math.round((ultima.media - primeira.media) / primeira.media * 100) : 0;
    const variacao = (var_pct > 0 ? "+" : "") + var_pct + "%";
    return {chave, rotulo: ordenadas[0].objeto, n: ordenadas.length, primeira, ultima, variacao, ultimaQ: ordenadas[ordenadas.length - 1]};
  }).sort((a, b)=>b.n - a.n);
  return `<h1>Histórico de preços por objeto</h1>
    <p class="sub">Cada pesquisa de preços registrada no app, agrupada pelo objeto. Compara a primeira e a última.</p>
    <div class="card tabela-wrap"><table id="tabelaHistoricoPrecos"><tr><th>Objeto</th><th class="num">Pesquisas</th><th>Primeira média</th><th>Última média</th><th class="num">Variação</th><th>Processo</th></tr>
      ${linhas.map(l=>`<tr><td>${esc(l.rotulo)}</td><td class="num">${l.n}</td>
        <td class="num">${dinheiro.fmt(l.primeira.media)}</td><td class="num">${dinheiro.fmt(l.ultima.media)}</td>
        <td class="num">${esc(l.variacao)}</td>
        <td><a href="#/processo/${encodeURIComponent(l.ultimaQ.processo_id)}">${esc(l.ultimaQ.processo_id)}</a></td></tr>`).join("")
        || '<tr><td colspan="6" class="vazio">Nenhuma pesquisa de preços registrada.</td></tr>'}</table></div>`;
};
