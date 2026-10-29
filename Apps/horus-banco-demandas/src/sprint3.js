/* ================= Sprint 3 · Grade e ficha ================= */
// situação do item no repositório: livre, com interesse de outras unidades, aprovada no ciclo
function situacaoDemanda(d, manifs, incls){
  if (incls.some(i=>i.banco_demanda_id === d.id)) return "aprovada";
  if (manifs.some(m=>m.banco_demanda_id === d.id)) return "interesse";
  return "livre";
}
const ROT_SIT = {livre: "Livre", interesse: "Com interesse", aprovada: "Aprovada no ciclo"};
const reaisFmt = v => dinheiro.fmt(Math.round((v || 0) * 100));
function filtrosBanco(){ return estado.filtrosBanco || (estado.filtrosBanco = {grupo: "", unidade: "", situacao: "", busca: ""}); }

TELAS["#/banco"] = async ()=>{
  const f = filtrosBanco(), [dem, manifs, incls, unidades, medidas, ciclos] = await Promise.all(
    ["banco_demandas", "banco_demanda_manifestacoes", "banco_demanda_inclusoes", "unidades", "unidades_medida", "ciclos"].map(s=>db.list(s)));
  const nomeU = Object.fromEntries(unidades.map(u=>[u.id, u.nome])), sigla = Object.fromEntries(medidas.map(m=>[m.id, m.sigla]));
  const anoCiclo = Object.fromEntries(ciclos.map(c=>[c.id, c.ano])), b = normalizar(f.busca);
  const vis = dem.map(d=>({...d, sit: situacaoDemanda(d, manifs, incls)})).filter(d=>(!f.grupo || d.grupo === f.grupo) && (!f.unidade || d.unidade_id === f.unidade)
    && (!f.situacao || d.sit === f.situacao) && (!b || normalizar(d.especificacao_tecnica + " " + d.justificativa).includes(b)))
    .sort((x, y)=>(y.updated_at || "").localeCompare(x.updated_at || ""));
  const card = d=>{
    const ms = manifs.filter(m=>m.banco_demanda_id === d.id), qtdTotal = d.quantidade + ms.reduce((a, m)=>a + m.quantidade, 0);
    const anos = incls.filter(i=>i.banco_demanda_id === d.id).map(i=>anoCiclo[i.quadro_id]).filter(Boolean);
    return `<a class="card cartao-demanda" href="#/demanda/${encodeURIComponent(d.id)}/ver" data-sit="${d.sit}" style="text-decoration:none;color:inherit;display:block">
      <p style="margin:0 0 6px"><span class="selo ${d.grupo === "CUSTEIO" ? "info" : "alerta"}">${d.grupo === "CUSTEIO" ? "Custeio" : "Investimento"}</span>
        ${anos.length ? anos.map(a=>`<span class="selo ok">Aprovada no ciclo ${a}</span>`).join(" ") : d.sit === "interesse" ? `<span class="selo info">${ms.length} com interesse</span>` : ""}</p>
      <b>${esc(d.especificacao_tecnica.slice(0, 90))}${d.especificacao_tecnica.length > 90 ? "…" : ""}</b>
      <p class="sub" style="margin:6px 0 0">${esc(nomeU[d.unidade_id] || "")}</p>
      <p style="margin:6px 0 0"><b>${reaisFmt(d.valor_global)}</b> · ${qtdTotal} ${esc(sigla[d.unidade_medida_id] || "")}${ms.length ? " (com adesões)" : ""}</p></a>`;
  };
  return `<h1>Banco de Demandas · repositório (<span id="qtdBanco">${vis.length}</span>)</h1>
    <p class="sub">${dem.length} demandas no total. <a href="#/demanda/nova">Nova demanda</a></p>
    <div class="card"><div class="campos">
      ${campo("fbBusca", "Busca na especificação e justificativa", {valor: f.busca})}
      ${campo("fbGrupo", "Grupo", {tipo: "select", opcoes: [["", "Todos"], ["CUSTEIO", "Custeio"], ["INVESTIMENTO", "Investimento"]], valor: f.grupo})}
      ${campo("fbUnidade", "Unidade", {tipo: "select", opcoes: [["", "Todas"], ...unidades.map(u=>[u.id, u.nome])], valor: f.unidade})}
      ${campo("fbSituacao", "Situação", {tipo: "select", opcoes: [["", "Todas"], ...Object.entries(ROT_SIT)], valor: f.situacao})}</div>
      <p class="sub">Valor global dos itens filtrados: <b id="valorFiltrado">${reaisFmt(vis.reduce((a, d)=>a + d.valor_global, 0))}</b></p></div>
    <div class="grade">${vis.map(card).join("") || '<div class="card vazio">Nenhuma demanda com estes filtros.</div>'}</div>`;
};
TELAS_DEPOIS["#/banco"] = ()=>{
  const f = filtrosBanco();
  [["fbBusca", "busca", "change"], ["fbGrupo", "grupo", "input"], ["fbUnidade", "unidade", "input"], ["fbSituacao", "situacao", "input"]].forEach(([id, k, ev])=>
    $("#" + id).addEventListener(ev, e=>{ f[k] = e.target.value; navegar(); }));
};

TELAS["#/demanda/:id/ver"] = async ({id})=>{
  const d = await db.get("banco_demandas", id);
  if (!d) return `<div class="card vazio">Demanda não encontrada. <a href="#/banco">Voltar</a></div>`;
  const [manifs, incls, unidades, medidas, ciclos] = await Promise.all([db.porIndice("banco_demanda_manifestacoes", "banco_demanda_id", id),
    db.porIndice("banco_demanda_inclusoes", "banco_demanda_id", id), db.list("unidades"), db.list("unidades_medida"), db.list("ciclos")]);
  const nomeU = Object.fromEntries(unidades.map(u=>[u.id, u.nome])), med = medidas.find(m=>m.id === d.unidade_medida_id);
  const pode = await podeEditar(d), ehDaCopia = d.unidade_id === (await db.meta("unidade_id"));
  return `<h1>${d.grupo === "CUSTEIO" ? "Custeio" : "Investimento"} · ${esc(nomeU[d.unidade_id] || "")}</h1>
    <p class="sub">Autor: ${esc(d.criado_por)} · criada em ${dataBR(d.created_at)} · atualizada em ${dataBR(d.updated_at)}</p>
    <div class="linha-botoes">${pode ? `<a class="botao" href="#/demanda/${encodeURIComponent(id)}">Editar</a>` : ""}
      ${!ehDaCopia ? `<a class="botao prim" href="#/demanda/${encodeURIComponent(id)}/interesse">Manifestar interesse</a>` : ""}<a class="botao" href="#/banco">Voltar ao banco</a></div>
    <div class="grade"><div class="card kpi"><div class="v">${reaisFmt(d.valor_unitario)}</div><div class="r">valor unitário</div></div>
      <div class="card kpi"><div class="v">${d.quantidade} ${esc(med?.sigla || "")}</div><div class="r">quantidade</div></div>
      <div class="card kpi"><div class="v">${reaisFmt(d.valor_global)}</div><div class="r">valor global</div></div></div>
    <div class="card"><h2 style="margin-top:0">Especificação técnica</h2><p style="white-space:pre-wrap">${esc(d.especificacao_tecnica)}</p>
      <h2>Justificativa</h2><p style="white-space:pre-wrap">${esc(d.justificativa)}</p>
      <h2>Referências</h2><ul>${(d.links_referencia || []).map((l, i)=>`<li><a href="${esc(l)}" target="_blank" rel="noopener">${esc(i === 0 && d.preview_title ? d.preview_title : l)}</a></li>`).join("")}</ul>
      <h2>Orçamento</h2>${d.arquivo_pdf ? `<button id="btnVerPdf">Abrir ${esc(d.arquivo_pdf_nome || "orçamento.pdf")}</button>` : '<p class="sub">Sem PDF anexado.</p>'}</div>
    <div class="card tabela-wrap"><h2 style="margin-top:0">Manifestações de interesse (${manifs.length})</h2>
      ${manifs.length ? `<table><tr><th>Unidade</th><th class="num">Quantidade</th><th>Justificativa</th><th>Data</th></tr>${manifs.map(m=>`<tr><td>${esc(nomeU[m.unidade_id] || "")}</td>
        <td class="num">${m.quantidade}</td><td>${esc(m.justificativa)}</td><td>${dataCurtaBR(m.created_at)}</td></tr>`).join("")}</table>` : '<p class="sub">Nenhuma.</p>'}</div>
    <div class="card"><h2 style="margin-top:0">Ciclos em que entrou</h2>
      ${incls.length ? incls.map(i=>`<span class="selo ok">Aprovada no ciclo ${esc(ciclos.find(c=>c.id === i.quadro_id)?.ano || "")}</span>`).join(" ") : '<p class="sub">Ainda não aprovada para um ciclo.</p>'}</div>`;
};
TELAS_DEPOIS["#/demanda/:id/ver"] = async ({id})=>{
  $("#btnVerPdf")?.addEventListener("click", async ()=>{ const d = await db.get("banco_demandas", id); window.open(URL.createObjectURL(d.arquivo_pdf), "_blank"); });
};
