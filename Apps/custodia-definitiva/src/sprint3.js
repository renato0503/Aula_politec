/* ================= Sprint 3 · Busca, filtros, CSV e histórico de movimentações ================= */
const CD_TIPOS_MOV = {transferencia: "Transferência de contêiner", saida: "Saída para perícia ou juízo", retorno: "Retorno ao acervo"};

// CSV com ; e BOM (abre direto no Excel em pt-BR)
function cdCSV(cab, linhas){
  const c = v=>{ const s = String(v ?? ""); return /[;"\n]/.test(s) ? `"${s.replace(/"/g, '""')}"` : s; };
  return "﻿" + [cab, ...linhas].map(l=>l.map(c).join(";")).join("\r\n");
}

// um texto procura em lacre, protocolo, id, descrição, nome da categoria e contêiner
function cdCasa(v, termo, cats){
  if (!termo) return true;
  const alvo = normalizar([v.id_vestigio, v.protocolo, v.lacre, v.descricao, cats[v.categoria_id]?.nome, v.categoria_id, v.conteiner_id, v.posicao].join(" "));
  return normalizar(termo).split(" ").every(p=>alvo.includes(p));
}
function cdFiltrar(vs, f, cats){
  return vs.filter(v=>(!f.categoria || v.categoria_id === f.categoria) && (!f.conteiner || v.conteiner_id === f.conteiner)
      && (!f.status || v.status === f.status) && (!f.local || (f.local === "fora" ? !!v.fora : !v.fora))
      && (!f.de || (v.data_entrada || "") >= f.de) && (!f.ate || (v.data_entrada || "") <= f.ate) && cdCasa(v, f.busca, cats))
    .sort((a, b)=>(b.data_entrada || "").localeCompare(a.data_entrada || "") || b.id_vestigio.localeCompare(a.id_vestigio));
}
teste("Sprint 3: a busca casa lacre, protocolo, categoria e contêiner, com todas as palavras", ()=>{
  const cats = {roupas: {nome: "Roupas e têxteis"}}, v = {id_vestigio: "V-1", protocolo: "PROC-9", lacre: "LC-77", categoria_id: "roupas", conteiner_id: "C-03", posicao: "P001"};
  return cdCasa(v, "lc-77", cats) && cdCasa(v, "proc-9", cats) && cdCasa(v, "texteis c-03", cats) && !cdCasa(v, "texteis c-04", cats);
});
teste("Sprint 3: filtros combinados (categoria + período + local)", ()=>{
  const vs = [{id_vestigio: "A", categoria_id: "x", data_entrada: "2026-01-10", status: "armazenado"},
              {id_vestigio: "B", categoria_id: "x", data_entrada: "2026-03-10", status: "armazenado", fora: true},
              {id_vestigio: "C", categoria_id: "y", data_entrada: "2026-03-10", status: "armazenado"}];
  const f = {categoria: "x", de: "2026-02-01", ate: "", status: "", conteiner: "", local: "", busca: ""};
  return cdFiltrar(vs, f, {}).map(v=>v.id_vestigio).join() === "B" && cdFiltrar(vs, {...f, local: "acervo"}, {}).length === 0;
});
teste("Sprint 3: CSV com ponto e vírgula, aspas e BOM", ()=>cdCSV(["a", "b"], [["1;2", 'x"y']]) === '﻿a;b\r\n"1;2";"x""y"');

function cdFiltros3(){ return estado.cdFiltros3 || (estado.cdFiltros3 = {categoria: "", conteiner: "", status: "", local: "", de: "", ate: "", busca: ""}); }
function cdSeloStatus(v){
  return `<span class="selo ${v.status === "pendencia" ? "alerta" : v.status === "descartado" ? "info" : "ok"}">${esc(v.status)}</span>${v.fora ? ' <span class="selo alerta">fora do acervo</span>' : ""}`;
}

TELAS["#/vestigios"] = async ()=>{
  const f = cdFiltros3(), [vs, cs, cats] = await Promise.all([db.list("vestigios"), cdConteineres(), cdCategorias()]);
  const lista = cdFiltrar(vs, f, cats), vol = lista.reduce((a, v)=>a + Number(v.volume_ocupado || 0), 0);
  const ativos = Object.values(f).filter(Boolean).length;
  return `<h1>Acervo de vestígios</h1><p class="sub">Busque por lacre, protocolo, categoria ou contêiner e combine os filtros. <a href="#/vestigio/novo">Cadastrar vestígio</a></p>
    <div class="card"><div class="busca-grande">${icone("busca")}<input id="cdBusca" type="search" value="${esc(f.busca)}" placeholder="Lacre, protocolo, categoria ou contêiner (ex.: LC-20260001, PROC-2026-004, C-03)" aria-label="Buscar no acervo"></div>
      <div class="campos">
      ${campo("cdCat", "Categoria", {tipo: "select", opcoes: [["", "Todas"], ...Object.values(cats).map(c=>[c.id_categoria, c.nome])], valor: f.categoria})}
      ${campo("cdCont", "Contêiner", {tipo: "select", opcoes: [["", "Todos"], ...Object.keys(cs).sort()], valor: f.conteiner})}
      ${campo("cdStatus", "Situação", {tipo: "select", opcoes: [["", "Todas"], ...CD_STATUS.map(s=>[s, s])], valor: f.status})}
      ${campo("cdLocal", "Onde está", {tipo: "select", opcoes: [["", "Todos"], ["acervo", "No acervo"], ["fora", "Fora do acervo"]], valor: f.local})}
      ${campo("cdDe", "Entrada de", {tipo: "date", valor: f.de})}
      ${campo("cdAte", "Entrada até", {tipo: "date", valor: f.ate})}</div>
      <div class="linha-botoes"><span class="sub" style="margin:0 auto 0 0"><b id="cdQtd">${lista.length}</b> de ${vs.length} vestígios · volume ${vol}${ativos ? ` · ${ativos} filtro(s) ativo(s)` : ""}</span>
        ${ativos ? '<button id="cdLimpar" type="button">Limpar filtros</button>' : ""}
        <button class="prim" id="btnCdCsv" type="button">${icone("download")} Exportar CSV (${lista.length})</button></div></div>
    <div class="card tabela-wrap"><table id="cdTabelaAcervo"><tr><th>Vestígio</th><th>Protocolo</th><th>Lacre</th><th>Categoria</th><th>Endereço</th><th>Entrada</th><th>Situação</th></tr>
      ${lista.map(v=>`<tr><td><a href="#/vestigio/${encodeURIComponent(v.id_vestigio)}">${esc(v.id_vestigio)}</a></td><td>${esc(v.protocolo)}</td>
        <td class="mono">${esc(v.lacre)}</td><td>${esc(cats[v.categoria_id]?.nome || v.categoria_id)}</td>
        <td>${v.endereco_efetivo ? esc(cdEnderecoCompleto(v.endereco_efetivo, cs)) : v.conteiner_id ? `<span class="selo alerta">sugerido</span> ${esc(cdEnderecoCompleto(v, cs))}` : '<span class="selo erro">sem endereço</span>'}</td>
        <td>${dataCurtaBR(v.data_entrada)}</td><td>${cdSeloStatus(v)}</td></tr>`).join("")
        || '<tr><td colspan="7" class="vazio">Nenhum vestígio com estes filtros.</td></tr>'}</table></div>`;
};
TELAS_DEPOIS["#/vestigios"] = ()=>{
  const f = cdFiltros3();
  [["cdCat", "categoria"], ["cdCont", "conteiner"], ["cdStatus", "status"], ["cdLocal", "local"], ["cdDe", "de"], ["cdAte", "ate"]].forEach(([id, k])=>
    $("#" + id).addEventListener("change", e=>{ f[k] = e.target.value; navegar(); }));
  let t; $("#cdBusca").addEventListener("input", e=>{ clearTimeout(t); t = setTimeout(async ()=>{ f.busca = e.target.value; await navegar(); const b = $("#cdBusca"); b.focus(); b.setSelectionRange(b.value.length, b.value.length); }, 250); });
  $("#cdLimpar")?.addEventListener("click", ()=>{ estado.cdFiltros3 = null; navegar(); });
  $("#btnCdCsv").addEventListener("click", async ()=>{
    const [vs, cs, cats] = await Promise.all([db.list("vestigios"), cdConteineres(), cdCategorias()]);
    const lista = cdFiltrar(vs, f, cats);
    const csv = cdCSV(["id_vestigio", "protocolo", "lacre", "categoria", "conteiner", "posicao", "localizacao_fisica", "volume_ocupado", "data_entrada", "situacao", "fora_do_acervo", "descricao"],
      lista.map(v=>[v.id_vestigio, v.protocolo, v.lacre, cats[v.categoria_id]?.nome || v.categoria_id, v.conteiner_id || "", v.posicao || "",
        cs[v.conteiner_id]?.localizacao_fisica || "", v.volume_ocupado, v.data_entrada, v.status, v.fora ? "sim" : "não", v.descricao || ""]));
    baixar(`acervo-custodia-${hojeISO()}.csv`, csv, "text/csv;charset=utf-8");
    await registrar("acervo exportado em CSV", {detalhe: `${lista.length} vestígios`}); toast(`${lista.length} vestígios exportados.`);
  });
};

// RN02/RN03 valem também na transferência: contêiner compatível e com folga
async function cdMovimentar(id, tipo, {destino, motivo, responsavel}){
  const v = await db.get("vestigios", id); if (!v) throw new Error("Vestígio não encontrado.");
  if (v.status === "descartado") throw new Error("Vestígio descartado não se movimenta.");
  if (!motivo) throw new Error("Informe o motivo ou o documento da movimentação (RN04).");
  const origem = v.fora ? (v.fora_destino || "fora do acervo") : `${v.conteiner_id || "sem endereço"} · ${v.posicao || ""}`;
  let novo = {...v}, dest;
  if (tipo === "transferencia"){
    if (v.fora) throw new Error("O vestígio está fora do acervo. Registre o retorno antes.");
    const [vs, cs] = await Promise.all([db.list("vestigios"), db.list("conteineres")]);
    const c = cs.find(x=>x.id_conteiner === destino);
    if (!c) throw new Error("Escolha o contêiner de destino.");
    if (c.id_conteiner === v.conteiner_id) throw new Error("O destino é o contêiner atual.");
    if (!(c.categoria_permitida === v.categoria_id || c.categoria_permitida === "todas")) throw new Error(`O contêiner ${c.id_conteiner} não aceita esta categoria (RN02).`);
    if (cdFolga(c, vs) < Number(v.volume_ocupado)) throw new Error(`O contêiner ${c.id_conteiner} não tem folga para o volume ${v.volume_ocupado} (RN03).`);
    const pos = "P" + String(cdOcupados(vs, c.id_conteiner) + 1).padStart(3, "0");
    novo = {...v, conteiner_id: c.id_conteiner, posicao: pos}; dest = `${c.id_conteiner} · ${pos}`;
  } else if (tipo === "saida"){
    if (v.fora) throw new Error("O vestígio já está fora do acervo.");
    if (!destino) throw new Error("Informe para onde o vestígio vai (laboratório, juízo, perito).");
    novo = {...v, fora: true, fora_destino: destino, fora_desde: agora()}; dest = destino;
  } else if (tipo === "retorno"){
    if (!v.fora) throw new Error("O vestígio já está no acervo.");
    novo = {...v, fora: false, fora_destino: "", fora_desde: ""}; dest = `${v.conteiner_id} · ${v.posicao}`;
  } else throw new Error("Tipo de movimentação desconhecido.");
  await db.put("vestigios", novo);
  await db.put("movimentacoes", {id_movimentacao: uuid(), vestigio_id: id, tipo, data_hora: agora(), responsavel: responsavel || estado.perfil || "custodia", origem, destino: dest, motivo});
  await registrar("movimentação registrada", {detalhe: `${id} · ${tipo} · ${dest}`});
  return novo;
}

const CD_ROTULO_MOV = {entrada: "Entrada", ...CD_TIPOS_MOV};
TELAS["#/vestigio/:id"] = async ({id})=>{
  const v = await db.get("vestigios", id);
  if (!v) return `<div class="card vazio">Vestígio não encontrado. <a href="#/vestigios">Voltar ao acervo</a></div>`;
  const [cats, cs, vs] = await Promise.all([cdCategorias(), db.list("conteineres"), db.list("vestigios")]);
  const csm = Object.fromEntries(cs.map(c=>[c.id_conteiner, c]));
  const movs = (await db.porIndice("movimentacoes", "vestigio_id", id)).sort((a, b)=>b.data_hora.localeCompare(a.data_hora));
  const efetivo = v.endereco_efetivo || null;
  const sugerido = v.endereco_sugerido || (v.conteiner_id ? {conteiner_id: v.conteiner_id, posicao: v.posicao} : null);
  const endereco = efetivo ? cdEnderecoCompleto(efetivo, csm) : sugerido ? cdEnderecoCompleto(sugerido, csm) : "sem endereço";
  const pendenciasCadastro = [
    ["Procedência", v.procedencia], ["Conferência documental", v.conferencia_documental],
    ["Integridade do lacre", v.lacre_integro], ["Embalagem", v.embalagem],
    ["Quantidade", v.quantidade > 0 ? v.quantidade : ""], ["Dimensões", v.dimensoes], ["Conservação", v.conservacao]
  ].filter(([, valor])=> !String(valor || "").trim()).map(([rotulo])=> rotulo);
  const destinos = cs.filter(c=>c.id_conteiner !== v.conteiner_id && (c.categoria_permitida === v.categoria_id || c.categoria_permitida === "todas"))
    .map(c=>[c.id_conteiner, `${c.id_conteiner} · folga ${cdFolga(c, vs)}${cdFolga(c, vs) < Number(v.volume_ocupado) ? " (sem folga)" : ""}`]);
  const tipos = v.fora ? [["retorno", CD_TIPOS_MOV.retorno]] : [["transferencia", CD_TIPOS_MOV.transferencia], ["saida", CD_TIPOS_MOV.saida]];
  return `<p class="sub nao-imprimir" style="margin-bottom:6px"><a href="#/vestigios">← Acervo</a></p>
    <h1>${esc(v.id_vestigio)} ${cdSeloStatus(v)}</h1>
    <p class="sub">Protocolo ${esc(v.protocolo)} · lacre <span class="mono">${esc(v.lacre)}</span> · entrada em ${dataCurtaBR(v.data_entrada)}</p>
    <div class="grade"><div class="card kpi"><div class="v">${esc(cats[v.categoria_id]?.nome || v.categoria_id)}</div><div class="r">categoria</div></div>
      <div class="card kpi"><div class="v" id="cdEndereco">${v.fora ? "Fora" : esc(endereco)}</div><div class="r">${v.fora ? "com " + esc(v.fora_destino) : efetivo ? "endereço efetivo" : sugerido ? "endereço sugerido (não confirmado)" : "sem endereço"}</div></div>
      <div class="card kpi"><div class="v">${v.volume_ocupado}</div><div class="r">volume ocupado</div></div>
      <div class="card kpi"><div class="v">${movs.length}</div><div class="r">movimentações</div></div></div>
    <div class="card" id="cdCadastro"><h2 style="margin-top:0">Cadastro e conferência física</h2>
      <div class="tabela-wrap"><table><tr><th>Etapa</th><th>Valor</th></tr>
        ${pendenciasCadastro.length ? pendenciasCadastro.map(x=>`<tr><td>${esc(x)}</td><td><span class="selo alerta">pendente</span></td></tr>`).join("") : '<tr><td colspan="2"><span class="selo ok">cadastro completo</span></td></tr>'}
        ${v.procedencia ? `<tr><td>Procedência</td><td>${esc(v.procedencia)}</td></tr>` : ""}
        ${v.embalagem ? `<tr><td>Embalagem</td><td>${esc(v.embalagem)}</td></tr>` : ""}
        ${v.dimensoes ? `<tr><td>Dimensões</td><td>${esc(v.dimensoes)}</td></tr>` : ""}
        ${v.quantidade ? `<tr><td>Quantidade</td><td>${esc(v.quantidade)}</td></tr>` : ""}</table></div>
      ${!efetivo && sugerido && v.status !== "descartado" ? `<h3>Confirmar o acondicionamento</h3>
        <p class="sub">Endereço sugerido: <b>${esc(endereco)}</b>. A confirmação só deve ser feita depois da conferência física e documental.</p>
        <div class="campos">${campo("cdConfResp", "Responsável pela conferência física", {valor: estado.perfil || ""})}</div>
        <div id="cdErrosConf"></div><div class="linha-botoes"><button type="button" class="prim" id="btnCdConfirmar">Confirmar e armazenar</button></div>`
        : v.confirmacao ? `<p class="sub"><span class="selo ok">endereço confirmado</span> por ${esc(v.confirmacao.por)} em ${dataBR(v.confirmacao.em)}.</p>` : ""}</div>
    <div class="duas-colunas">
      <div class="card"><h2 style="margin-top:0">Material</h2><p>${esc(v.descricao || "Sem descrição.")}</p>
        <p class="sub">Conservação: ${esc(v.conservacao || csm[v.conteiner_id]?.tipo_conservacao || "—")} · localização física: ${esc(endereco)}</p>
        ${v.status === "descartado" ? "" : `<h3>Registrar movimentação</h3>
        <form id="formCdMov" novalidate><div class="campos">
          ${campo("cdMovTipo", "Tipo", {tipo: "select", opcoes: tipos})}
          <div id="cdMovDestCont">${campo("cdMovCont", "Contêiner de destino", {tipo: "select", opcoes: [["", destinos.length ? "Escolha" : "Nenhum compatível"], ...destinos]})}</div>
          <div id="cdMovDestTxt" hidden>${campo("cdMovPara", "Para onde vai", {ajuda: "Ex.: Laboratório de Química Forense, 2ª Vara Criminal."})}</div></div>
          ${campo("cdMovMotivo", "Motivo ou documento", {obrigatorio: true, ajuda: "Ofício, requisição ou despacho que autoriza (RN04)."})}
          <div id="cdMovErros"></div><div class="linha-botoes"><button class="prim" type="submit">Registrar</button></div></form>`}</div>
      <div class="card"><h2 style="margin-top:0">Histórico de movimentações (RN04)</h2>
        <ol class="linha-do-tempo" id="cdMovs">${movs.map(m=>`<li class="ldt-${m.tipo === "saida" ? "alerta" : m.tipo === "retorno" || m.tipo === "entrada" ? "ok" : "info"}"><div class="ldt-quando">${dataBR(m.data_hora)}</div>
          <b>${esc(CD_ROTULO_MOV[m.tipo] || m.tipo)}</b> · ${esc(m.origem)} → ${esc(m.destino)}
          <div class="sub" style="margin:0">${esc(m.responsavel)}${m.motivo ? " · " + esc(m.motivo) : ""}</div></li>`).join("") || '<li class="vazio">Sem movimentações.</li>'}</ol>
        <div class="linha-botoes"><button id="btnCdMovCsv" type="button">${icone("download")} Histórico em CSV</button></div></div></div>`;
};
TELAS_DEPOIS["#/vestigio/:id"] = ({id})=>{
  $("#btnCdConfirmar")?.addEventListener("click", async ()=>{
    const resp = valorDe("cdConfResp").trim();
    if (!resp) return mostrarErros("#cdErrosConf", ["Informe o responsável pela conferência física."]);
    const v = await db.get("vestigios", id);
    if (!v) return;
    const end = v.endereco_sugerido || (v.conteiner_id ? {conteiner_id: v.conteiner_id, posicao: v.posicao, estante: "", prateleira: "", nivel: ""} : null);
    if (!end) return mostrarErros("#cdErrosConf", ["Não há endereço sugerido para confirmar."]);
    await db.put("vestigios", {...v, endereco_efetivo: end, status: "armazenado", confirmacao: {por: resp, em: agora()}});
    await db.put("movimentacoes", {id_movimentacao: uuid(), vestigio_id: id, tipo: "confirmacao", data_hora: agora(), responsavel: resp,
      origem: "conferência física", destino: `${end.conteiner_id || ""} · ${end.posicao || ""}`});
    await registrar("acondicionamento confirmado", {detalhe: `${id} · ${resp}`});
    toast("Acondicionamento confirmado; vestígio armazenado."); navegar();
  });
  const ajustar = ()=>{ const t = $("#cdMovTipo")?.value; if (!t) return; $("#cdMovDestCont").hidden = t !== "transferencia"; $("#cdMovDestTxt").hidden = t !== "saida"; };
  $("#cdMovTipo")?.addEventListener("change", ajustar); ajustar();
  $("#formCdMov")?.addEventListener("submit", async e=>{
    e.preventDefault();
    const tipo = valorDe("cdMovTipo");
    try {
      await cdMovimentar(id, tipo, {destino: tipo === "transferencia" ? valorDe("cdMovCont") : valorDe("cdMovPara"), motivo: valorDe("cdMovMotivo")});
      toast("Movimentação registrada."); navegar();
    } catch(err){ mostrarErros("#cdMovErros", [err.message]); }
  });
  $("#btnCdMovCsv")?.addEventListener("click", async ()=>{
    const movs = (await db.porIndice("movimentacoes", "vestigio_id", id)).sort((a, b)=>a.data_hora.localeCompare(b.data_hora));
    baixar(`movimentacoes-${id}.csv`, cdCSV(["data_hora", "tipo", "responsavel", "origem", "destino", "motivo"], movs.map(m=>[m.data_hora, m.tipo, m.responsavel, m.origem, m.destino, m.motivo || ""])), "text/csv;charset=utf-8");
  });
};
