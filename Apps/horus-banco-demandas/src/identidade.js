/* Identidade do Banco de Demandas · Hórus.
   Entra por último no build. A tela-assinatura é a vitrine do repositório:
   filtros em uma linha, facetas com contagem, ordenação, alternância entre
   cartões e tabela e o contexto de unidade do perfil. */

function horusUnidadeUsuario(){
  return ["GERENTE", "USUARIO_SETORIAL"].includes(estado.perfil);
}
function horusVista(){ return estado.vistaBanco === "tabela" ? "tabela" : "cartoes"; }

TELAS["#/banco"] = async ()=>{
  const f = filtrosBanco();
  const [dem, manifs, incls, unidades, medidas, ciclos] = await Promise.all(
    ["banco_demandas", "banco_demanda_manifestacoes", "banco_demanda_inclusoes", "unidades", "unidades_medida", "ciclos"].map(s=>db.list(s)));
  const nomeU = Object.fromEntries(unidades.map(u=>[u.id, u.nome])), sigla = Object.fromEntries(medidas.map(m=>[m.id, m.sigla]));
  const anoCiclo = Object.fromEntries(ciclos.map(c=>[c.id, c.ano])), b = normalizar(f.busca);
  const contexto = estado.contexto || (horusUnidadeUsuario() ? (await db.meta("unidade_id")) : null);
  const unidadeFiltro = f.unidade || contexto;
  const todos = dem.map(d=>({...d, sit: situacaoDemanda(d, manifs, incls)}));
  const buscaOk = d=>!b || normalizar(`${d.especificacao_tecnica} ${d.justificativa}`).includes(b);
  let vis = todos.filter(d=>(!f.grupo || d.grupo === f.grupo) && (!unidadeFiltro || d.unidade_id === unidadeFiltro) && buscaOk(d))
    .filter(d=>!f.situacao || d.sit === f.situacao);
  const ordem = f.ordem || "recentes";
  vis = vis.sort((x, y)=>{
    if (ordem === "valor") return y.valor_global - x.valor_global;
    if (ordem === "quantidade") return y.quantidade - x.quantidade;
    if (ordem === "unidade") return (nomeU[x.unidade_id] || "").localeCompare(nomeU[y.unidade_id] || "", "pt-BR");
    if (ordem === "especificacao") return x.especificacao_tecnica.localeCompare(y.especificacao_tecnica, "pt-BR");
    return (y.updated_at || "").localeCompare(x.updated_at || "");
  });
  const cont = {livre: 0, interesse: 0, aprovada: 0, CUSTEIO: 0, INVESTIMENTO: 0};
  todos.forEach(d=>{ cont[d.sit] = (cont[d.sit] || 0) + 1; cont[d.grupo] = (cont[d.grupo] || 0) + 1; });
  const qtdManifestacoes = d=>manifs.filter(m=>m.banco_demanda_id === d.id).length;
  const anosDe = d=>incls.filter(i=>i.banco_demanda_id === d.id).map(i=>anoCiclo[i.quadro_id]).filter(Boolean);
  const card = d=>{
    const ms = qtdManifestacoes(d), anos = anosDe(d);
    return `<a class="card cartao-demanda" href="#/demanda/${encodeURIComponent(d.id)}/ver" data-sit="${d.sit}">
      <p class="horus-selos"><span class="selo ${d.grupo === "CUSTEIO" ? "info" : "alerta"}">${d.grupo === "CUSTEIO" ? "Custeio" : "Investimento"}</span>
        ${anos.length ? anos.map(a=>`<span class="selo ok">Aprovada no ciclo ${a}</span>`).join(" ") : d.sit === "interesse" ? `<span class="selo info">${ms} com interesse</span>` : '<span class="selo">Livre</span>'}</p>
      <b class="cartao-titulo" title="${esc(d.especificacao_tecnica)}">${esc(d.especificacao_tecnica)}</b>
      <p class="sub cartao-unidade">${esc(nomeU[d.unidade_id] || "")}</p>
      <p class="cartao-valor"><b>${reaisFmt(d.valor_global)}</b> · ${d.quantidade} ${esc(sigla[d.unidade_medida_id] || "")}${ms ? " (com adesões)" : ""}</p></a>`;
  };
  const linha = d=>{
    const anos = anosDe(d);
    return `<tr><td><a href="#/demanda/${encodeURIComponent(d.id)}/ver">${esc(d.especificacao_tecnica)}</a></td>
      <td>${esc(nomeU[d.unidade_id] || "")}</td><td>${d.grupo === "CUSTEIO" ? "Custeio" : "Investimento"}</td>
      <td>${anos.length ? "Aprovada " + anos.join(", ") : ROT_SIT[d.sit]}</td><td class="num">${reaisFmt(d.valor_global)}</td></tr>`;
  };
  const facetas = [["grupo", "CUSTEIO", "Custeio", cont.CUSTEIO], ["grupo", "INVESTIMENTO", "Investimento", cont.INVESTIMENTO],
    ["situacao", "livre", "Livre", cont.livre], ["situacao", "interesse", "Com interesse", cont.interesse], ["situacao", "aprovada", "Aprovada", cont.aprovada]];
  return `<h1>Banco de Demandas <span class="conta" id="qtdBanco">${vis.length}</span></h1>
    <p class="sub">${dem.length} demandas no total${contexto ? ` · vendo a unidade <b>${esc(nomeU[contexto] || contexto)}</b>` : ""}.
      <a href="#/demanda/nova">Nova demanda</a></p>
    <div class="horus-facetas">${facetas.map(([chave, valor, rot, n])=>`<button type="button" class="horus-faceta ${f[chave] === valor ? "escolhida" : ""}" data-faceta="${chave}" data-valor="${valor}">
      ${rot} <span class="conta">${n}</span></button>`).join("")}
      ${contexto ? `<button type="button" class="horus-faceta" data-limpar-unidade="1">Minha unidade</button>` : ""}</div>
    <div class="card horus-barra"><div class="campos">
      ${campo("fbBusca", "Busca na especificação e justificativa", {valor: f.busca || "", attrs: 'autocomplete="off"'})}
      ${campo("fbGrupo", "Grupo", {tipo: "select", opcoes: [["", "Todos"], ["CUSTEIO", "Custeio"], ["INVESTIMENTO", "Investimento"]], valor: f.grupo})}
      ${campo("fbUnidade", "Unidade", {tipo: "select", opcoes: [["", "Todas"], ...unidades.map(u=>[u.id, u.nome])], valor: f.unidade})}
      ${campo("fbSituacao", "Situação", {tipo: "select", opcoes: [["", "Todas"], ...Object.entries(ROT_SIT)], valor: f.situacao})}
      ${campo("fbOrdem", "Ordenar por", {tipo: "select", opcoes: [["recentes", "Mais recentes"], ["valor", "Maior valor"], ["quantidade", "Maior quantidade"], ["unidade", "Unidade"], ["especificacao", "Especificação"]], valor: ordem})}</div>
      <div class="horus-rodape"><p class="sub" style="margin:0">Valor global dos itens filtrados: <b id="valorFiltrado">${reaisFmt(vis.reduce((a, d)=>a + d.valor_global, 0))}</b></p>
        <div class="horus-vista" role="group" aria-label="Forma de exibição">
          <button type="button" data-vista="cartoes" class="${horusVista() === "cartoes" ? "prim" : ""}">Cartões</button>
          <button type="button" data-vista="tabela" class="${horusVista() === "tabela" ? "prim" : ""}">Tabela</button></div></div></div>
    ${horusVista() === "cartoes"
      ? `<div class="grade horus-vitrine">${vis.map(card).join("") || '<div class="card vazio">Nenhuma demanda com estes filtros.</div>'}</div>`
      : `<div class="card tabela-wrap"><table id="tabelaBanco"><thead><tr><th>Especificação</th><th>Unidade</th><th>Grupo</th><th>Situação</th><th class="num">Valor global</th></tr></thead>
          <tbody>${vis.map(linha).join("") || '<tr><td colspan="5" class="vazio">Nenhuma demanda com estes filtros.</td></tr>'}</tbody></table></div>`}`;
};
TELAS_DEPOIS["#/banco"] = ()=>{
  const f = filtrosBanco();
  [["fbGrupo", "grupo"], ["fbUnidade", "unidade"], ["fbSituacao", "situacao"], ["fbOrdem", "ordem"]].forEach(([id, k])=>
    $("#" + id)?.addEventListener("change", e=>{ f[k] = e.target.value; navegar(); }));
  let t = null;
  $("#fbBusca")?.addEventListener("input", e=>{
    clearTimeout(t); const v = e.target.value;
    t = setTimeout(()=>{ f.busca = v; navegar(); }, 350);
  });
  $$("[data-faceta]").forEach(b=>b.addEventListener("click", ()=>{
    const k = b.dataset.faceta, v = b.dataset.valor;
    f[k] = f[k] === v ? "" : v; navegar();
  }));
  $("[data-limpar-unidade]")?.addEventListener("click", async ()=>{ estado.contexto = null; await db.meta("perfil_contexto", null); navegar(); });
  $$("[data-vista]").forEach(b=>b.addEventListener("click", ()=>{ estado.vistaBanco = b.dataset.vista; navegar(); }));
};
