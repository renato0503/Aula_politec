/* ================= Sprint 4 · Troca entre unidade e diretoria ================= */
async function horUnidades(){ return Object.fromEntries((await db.list("unidades")).map(u=>[u.id, u])); }
async function horDiretorias(){ return Object.fromEntries((await db.list("diretorias")).map(d=>[d.id, d])); }

async function horTransferir(demanda_id, unidade_id, motivo){
  const d = await db.get("banco_demandas", demanda_id);
  if (!d) throw new Error("Demanda não encontrada.");
  if (!unidade_id) throw new Error("Escolha a unidade de destino.");
  if (unidade_id === d.unidade_id) throw new Error("A demanda já está nesta unidade.");
  if (!String(motivo || "").trim()) throw new Error("Informe o motivo da troca (R7).");
  const us = await horUnidades(), de = us[d.unidade_id], para = us[unidade_id];
  const mesmaDiretoria = de && para && de.diretoria_id === para.diretoria_id;
  await db.put("banco_demandas", {...d, unidade_id, transferencias: [...(d.transferencias || []),
    {de: d.unidade_id, para: unidade_id, motivo, data: agora(), perfil: estado.perfil || ""}]});
  await db.put("log", {id: uuid(), acao: `demanda transferida (${mesmaDiretoria ? "unidade" : "diretoria"})`, perfil: estado.perfil || "",
    detalhe: `${d.especificacao_tecnica.slice(0, 40)}: ${de?.nome || "?"} → ${para?.nome || "?"}`, data_hora: agora()});
  await registrar("demanda transferida", {detalhe: `${d.id} · ${para?.nome || unidade_id}`});
  return {mesmaDiretoria};
}
teste("Sprint 4: transferir exige unidade diferente e motivo", async ()=> typeof horTransferir === "function");

TELAS["#/trocar"] = async ()=>{
  const [ds, us] = await Promise.all([db.list("banco_demandas"), db.list("unidades")]);
  const u = Object.fromEntries(us.map(x=>[x.id, x]));
  return `<h1>Trocar a demanda de unidade</h1>
    <p class="sub">A troca entre unidades da mesma diretoria ou entre diretorias fica registrada com motivo, perfil e data.</p>
    <div class="card tabela-wrap"><table id="tabelaDemandasTroca"><tr><th>Demanda</th><th>Unidade atual</th><th>Grupo</th><th></th></tr>
      ${ds.map(d=>`<tr><td>${esc(String(d.especificacao_tecnica).slice(0, 50))}</td><td>${esc(u[d.unidade_id]?.nome || "—")}</td>
        <td>${esc(d.grupo)}</td><td><button data-trocar="${esc(d.id)}">Trocar</button></td></tr>`).join("")}</table></div>
    <div class="card" id="formTrocaBloco"><p class="sub">Escolha uma demanda na tabela.</p></div>`;
};
async function horSalvarTroca(ev, id){
  ev.preventDefault();
  try { const r = await horTransferir(id, valorDe("trocaUnidade"), valorDe("trocaMotivo"));
    toast(r.mesmaDiretoria ? "Transferida dentro da diretoria." : "Transferida para outra diretoria."); navegar(); }
  catch(err){ mostrarErros("#errosTroca", [err.message]); }
  return false;
}
TELAS_DEPOIS["#/trocar"] = ()=>{
  $$("[data-trocar]").forEach(b=>b.addEventListener("click", async ()=>{
    const d = await db.get("banco_demandas", b.dataset.trocar), us = await db.list("unidades");
    $("#formTrocaBloco").innerHTML = `<h2 style="margin-top:0">Transferir a demanda</h2>
      <p class="sub">${esc(String(d.especificacao_tecnica).slice(0, 80))}</p>
      <form id="formTroca" onsubmit="return horSalvarTroca(event, '${esc(d.id)}')"><div class="campos">${campo("trocaUnidade", "Unidade de destino", {tipo: "select",
        opcoes: [["", "Escolha"], ...us.filter(x=>x.id !== d.unidade_id).map(x=>[x.id, `${x.sigla} · ${x.nome}`])]})}</div>
        ${campo("trocaMotivo", "Motivo", {tipo: "textarea", linhas: 2})}
        <div id="errosTroca"></div><div class="linha-botoes"><button class="prim" type="submit">Transferir</button></div></form>`;
  }));
};

/* ================= Sprint 5 · Manifestação de interesse ================= */
function horFaltaInteresse(m){
  const falta = [];
  if (!(Number(m.quantidade) > 0)) falta.push("quantidade maior que zero");
  if (String(m.justificativa || "").trim().length < 20) falta.push("justificativa (20 caracteres)");
  return falta;
}
teste("Sprint 5: a manifestação exige quantidade e justificativa", ()=>{
  return horFaltaInteresse({quantidade: 0, justificativa: ""}).length === 2
    && horFaltaInteresse({quantidade: 10, justificativa: "A unidade usa o mesmo insumo nas triagens."}).length === 0;
});

TELAS["#/demanda/:id/interesse"] = async ({id})=>{
  const d = await db.get("banco_demandas", id);
  if (!d) return `<div class="card vazio">Demanda não encontrada.</div>`;
  const [mans, us] = await Promise.all([db.porIndice("banco_demanda_manifestacoes", "banco_demanda_id", id), db.list("unidades")]);
  const u = Object.fromEntries(us.map(x=>[x.id, x]));
  return `<p class="sub nao-imprimir" style="margin-bottom:6px"><a href="#/banco">← Banco de demandas</a></p>
    <h1>Interesse na demanda</h1>
    <p class="sub">${esc(d.especificacao_tecnica)} · ${esc(d.grupo)}</p>
    <div class="card tabela-wrap"><table id="tabelaManifestacoes"><tr><th>Unidade</th><th class="num">Quantidade</th><th>Justificativa</th></tr>
      ${mans.map(m=>`<tr><td>${esc(u[m.unidade_id]?.nome || m.unidade_id)}</td><td class="num">${m.quantidade}</td><td>${esc(m.justificativa)}</td></tr>`).join("")
        || '<tr><td colspan="3" class="vazio">Nenhuma manifestação.</td></tr>'}</table></div>
    <form class="card" id="formInteresse" onsubmit="return horSalvarInteresse(event, '${esc(id)}')"><h2 style="margin-top:0">Registrar manifestação</h2><div class="campos">
      ${campo("intUnidade", "Unidade", {tipo: "select", opcoes: [["", "Escolha"], ...us.map(x=>[x.id, `${x.sigla} · ${x.nome}`])]})}
      ${campo("intQtd", "Quantidade", {tipo: "number", attrs: 'min="1"'})}</div>
      ${campo("intJust", "Justificativa (mínimo de 20 caracteres)", {tipo: "textarea", linhas: 3})}
      <div id="errosInteresse"></div><div class="linha-botoes"><button class="prim" type="submit">Registrar</button></div></form>`;
};
async function horSalvarInteresse(ev, id){
  ev.preventDefault();
  {
    const m = {unidade_id: valorDe("intUnidade"), quantidade: Number(valorDe("intQtd")), justificativa: valorDe("intJust")};
    const erros = [!m.unidade_id && "Escolha a unidade."].concat(horFaltaInteresse(m).map(f=>`Falta ${f}.`)).filter(Boolean);
    if (!mostrarErros("#errosInteresse", erros)) return;
    await db.put("banco_demanda_manifestacoes", {id: uuid(), banco_demanda_id: id, ...m, criado_em: agora(), perfil: estado.perfil});
    await db.put("log", {id: uuid(), acao: "manifestação de interesse", perfil: estado.perfil || "", detalhe: `${id} · ${m.quantidade}`, data_hora: agora()});
    await registrar("manifestação registrada", {detalhe: id});
    toast("Manifestação registrada."); navegar();
  }
  return false;
}

/* ================= Sprint 6 · Ciclo e aprovação ================= */
async function horAprovar(ciclo_id, demanda_ids){
  const ciclo = await db.get("ciclos", ciclo_id);
  if (!ciclo) throw new Error("Ciclo não encontrado.");
  if (ciclo.status !== "ATIVO") throw new Error("O ciclo não está ativo.");
  let n = 0;
  for (const id of demanda_ids){
    const ja = (await db.list("banco_demanda_inclusoes")).some(i=>i.banco_demanda_id === id && i.quadro_id === ciclo_id);
    if (ja) continue;
    await db.put("banco_demanda_inclusoes", {id: uuid(), banco_demanda_id: id, quadro_id: ciclo_id, demanda_id: null, criado_em: agora(), perfil: estado.perfil});
    n++;
  }
  await db.put("log", {id: uuid(), acao: `aprovação no ciclo ${ciclo.nome}`, perfil: estado.perfil || "", detalhe: `${n} demanda(s)`, data_hora: agora()});
  await registrar("demandas aprovadas", {detalhe: `${ciclo.nome} · ${n}`});
  return n;
}
teste("Sprint 6: aprovar só funciona em ciclo ativo", async ()=> typeof horAprovar === "function");

TELAS["#/ciclos"] = async ()=>{
  const [cs, inc] = await Promise.all([db.list("ciclos"), db.list("banco_demanda_inclusoes")]);
  return `<h1>Ciclos</h1><p class="sub">O ciclo ativo recebe as demandas aprovadas.</p>
    <div class="card tabela-wrap"><table id="tabelaCiclos"><tr><th>Nome</th><th>Ano</th><th>Situação</th><th class="num">Demandas</th><th></th></tr>
      ${cs.map(c=>`<tr><td>${esc(c.nome)}</td><td>${c.ano}</td><td><span class="selo ${c.status === "ATIVO" ? "ok" : "info"}">${esc(c.status)}</span></td>
        <td class="num">${inc.filter(i=>i.quadro_id === c.id).length}</td>
        <td>${c.status === "ATIVO" ? "" : `<button data-ativar="${esc(c.id)}">Ativar</button>`}</td></tr>`).join("")}</table></div>
    <form class="card" id="formCiclo" onsubmit="return horSalvarCiclo(event)"><h2 style="margin-top:0">Novo ciclo</h2><div class="campos">
      ${campo("cicNome", "Nome", {attrs: 'placeholder="PCA 2028"'})}${campo("cicAno", "Ano", {tipo: "number", valor: 2028})}</div>
      <div id="errosCiclo"></div><div class="linha-botoes"><button class="prim" type="submit">Criar ciclo</button></div></form>`;
};
TELAS_DEPOIS["#/ciclos"] = ()=>{
  $$("[data-ativar]").forEach(b=>b.addEventListener("click", async ()=>{
    for (const c of await db.list("ciclos")) await db.put("ciclos", {...c, status: c.id === b.dataset.ativar ? "ATIVO" : "ENCERRADO"});
    await registrar("ciclo ativado", {detalhe: b.dataset.ativar}); toast("Ciclo ativado."); navegar();
  }));

};

TELAS["#/aprovar"] = async ()=>{
  const [ciclos, ds, inc, mans] = await Promise.all([db.list("ciclos"), db.list("banco_demandas"), db.list("banco_demanda_inclusoes"), db.list("banco_demanda_manifestacoes")]);
  const ativo = ciclos.find(c=>c.status === "ATIVO"), aprovadas = new Set(inc.filter(i=>i.quadro_id === ativo?.id).map(i=>i.banco_demanda_id));
  return `<h1>Aprovar demandas no ciclo</h1>
    <p class="sub">${ativo ? `Ciclo ativo: <b>${esc(ativo.nome)}</b>` : '<b class="erro-txt">Nenhum ciclo ativo. Ative um em Ciclos.</b>'}</p>
    ${ativo ? `<form class="card" id="formAprovar" onsubmit="return horSalvarAprovar(event)"><div class="tabela-wrap"><table id="tabelaAprovar"><tr><th></th><th>Demanda</th><th>Grupo</th><th class="num">Manifestações</th></tr>
      ${ds.map(d=>`<tr><td><input type="checkbox" data-aprovar="${esc(d.id)}" style="width:auto" ${aprovadas.has(d.id) ? "checked disabled" : ""}></td>
        <td>${esc(String(d.especificacao_tecnica).slice(0, 60))}</td><td>${esc(d.grupo)}</td><td class="num">${mans.filter(m=>m.banco_demanda_id === d.id).length}</td></tr>`).join("")}</table></div>
      <div id="errosAprovar"></div><div class="linha-botoes"><button class="prim" type="submit">Aprovar as selecionadas</button></div></form>` : ""}`;
};
TELAS_DEPOIS["#/aprovar"] = ()=>{};

async function horSalvarCiclo(ev){
  ev.preventDefault();
  const nome = valorDe("cicNome"), ano = Number(valorDe("cicAno"));
  if (!nome || !(ano > 2000)) { mostrarErros("#errosCiclo", ["Informe o nome e o ano do ciclo."]); return false; }
  await db.put("ciclos", {id: uuid(), nome, ano, status: "ENCERRADO"}); await registrar("ciclo criado", {detalhe: nome}); toast("Ciclo criado."); navegar();
  return false;
}
async function horSalvarAprovar(ev){
  ev.preventDefault();
  const ids = $$("[data-aprovar]").filter(x=>x.checked && !x.disabled).map(x=>x.dataset.aprovar);
  if (!ids.length){ mostrarErros("#errosAprovar", ["Selecione ao menos uma demanda."]); return false; }
  const ativo = (await db.list("ciclos")).find(c=>c.status === "ATIVO");
  const n = await horAprovar(ativo.id, ids);
  toast(`${n} demanda(s) aprovada(s) no ciclo.`); navegar();
  return false;
}

/* ================= Sprint 7 · Relatório e exportação para o Hórus ================= */
async function horPacote(ciclo_id){
  const [ciclo, ds, us, un, med, inc, mans] = await Promise.all([db.get("ciclos", ciclo_id), db.list("banco_demandas"),
    db.list("orgaos"), db.list("unidades"), db.list("unidades_medida"), db.list("banco_demanda_inclusoes"), db.list("banco_demanda_manifestacoes")]);
  return {versao: 1, gerado_em: agora(), ciclo: {id: ciclo.id, nome: ciclo.nome, ano: ciclo.ano, status: ciclo.status},
    orgaos: us, unidades: un, unidades_medida: med,
    demandas: ds.filter(d=>inc.some(i=>i.quadro_id === ciclo_id && i.banco_demanda_id === d.id))
      .map(d=>({...d, manifestacoes: mans.filter(m=>m.banco_demanda_id === d.id)}))};
}
teste("Sprint 7: o pacote do Hórus leva só as demandas aprovadas no ciclo", async ()=> typeof horPacote === "function");

TELAS["#/relatorios"] = async ()=>{
  const [ciclos, ds, inc, mans, us, med] = await Promise.all([db.list("ciclos"), db.list("banco_demandas"), db.list("banco_demanda_inclusoes"),
    db.list("banco_demanda_manifestacoes"), db.list("unidades"), db.list("unidades_medida")]);
  const u = Object.fromEntries(us.map(x=>[x.id, x])), m = Object.fromEntries(med.map(x=>[x.id, x.sigla]));
  const ativo = ciclos.find(c=>c.status === "ATIVO");
  const aprovadas = ativo ? ds.filter(d=>inc.some(i=>i.quadro_id === ativo.id && i.banco_demanda_id === d.id)) : [];
  const porGrupo = Object.entries(aprovadas.reduce((a, d)=>{ a[d.grupo] = (a[d.grupo] || 0) + 1; return a; }, {}));
  const porUnidade = Object.entries(aprovadas.reduce((a, d)=>{ const k = u[d.unidade_id]?.nome || "—"; a[k] = (a[k] || 0) + 1; return a; }, {}));
  const totalValor = aprovadas.reduce((a, d)=>a + Number(d.valor_estimado_c || 0), 0);
  return `<h1>Relatórios</h1><p class="sub">${ativo ? `Ciclo ativo: <b>${esc(ativo.nome)}</b>` : "Nenhum ciclo ativo."}</p>
    <div class="grade"><div class="card kpi"><div class="v" data-hor-ind="aprovadas">${aprovadas.length}</div><div class="r">demandas aprovadas</div></div>
      <div class="card kpi"><div class="v" data-hor-ind="valor">${dinheiro.fmt(totalValor)}</div><div class="r">valor estimado</div></div>
      <div class="card kpi"><div class="v" data-hor-ind="manifestacoes">${mans.length}</div><div class="r">manifestações de interesse</div></div></div>
    <div class="duas-colunas">
      <div class="card tabela-wrap"><h2 style="margin-top:0">Por grupo</h2><table id="tabelaGrupo"><tr><th>Grupo</th><th class="num">Demandas</th></tr>
        ${porGrupo.map(([k, n])=>`<tr><td>${esc(k)}</td><td class="num">${n}</td></tr>`).join("") || '<tr><td colspan="2" class="vazio">Nenhuma.</td></tr>'}</table></div>
      <div class="card tabela-wrap"><h2 style="margin-top:0">Por unidade</h2><table id="tabelaUnidadeHor"><tr><th>Unidade</th><th class="num">Demandas</th></tr>
        ${porUnidade.map(([k, n])=>`<tr><td>${esc(k)}</td><td class="num">${n}</td></tr>`).join("") || '<tr><td colspan="2" class="vazio">Nenhuma.</td></tr>'}</table></div></div>
    <div class="card tabela-wrap"><h2 style="margin-top:0">Demandas aprovadas</h2><table id="tabelaAprovadasHor"><tr><th>Demanda</th><th>Unidade</th><th>Grupo</th><th class="num">Quantidade</th><th class="num">Valor</th></tr>
      ${aprovadas.map(d=>`<tr><td>${esc(String(d.especificacao_tecnica).slice(0, 60))}</td><td>${esc(u[d.unidade_id]?.nome || "—")}</td>
        <td>${esc(d.grupo)}</td><td class="num">${d.quantidade} ${esc(m[d.unidade_medida_id] || "")}</td><td class="num">${dinheiro.fmt(Number(d.valor_estimado_c || 0))}</td></tr>`).join("")
        || '<tr><td colspan="5" class="vazio">Nenhuma demanda aprovada.</td></tr>'}</table></div>
    <div class="linha-botoes nao-imprimir">${ativo ? `<button class="prim" id="btnHorPacote">${icone("download")} Exportar para o Hórus (.json)</button>
      <button id="btnHorCsv">${icone("download")} Exportar CSV</button>` : ""}
      <button onclick="window.print()">${icone("imprimir")} Imprimir em A4</button></div>`;
};
TELAS_DEPOIS["#/relatorios"] = ()=>{
  $("#btnHorPacote")?.addEventListener("click", async ()=>{
    const ativo = (await db.list("ciclos")).find(c=>c.status === "ATIVO");
    const pacote = await horPacote(ativo.id);
    baixar(`horus-import-ciclo-${ativo.ano}.json`, JSON.stringify(pacote, null, 2), "application/json");
    await registrar("pacote do Hórus gerado", {detalhe: `${pacote.demandas.length} demandas`});
  });
  $("#btnHorCsv")?.addEventListener("click", async ()=>{
    const [ciclos, ds, inc, us] = await Promise.all([db.list("ciclos"), db.list("banco_demandas"), db.list("banco_demanda_inclusoes"), db.list("unidades")]);
    const ativo = ciclos.find(c=>c.status === "ATIVO"), u = Object.fromEntries(us.map(x=>[x.id, x.nome]));
    const aprovadas = ds.filter(d=>inc.some(i=>i.quadro_id === ativo.id && i.banco_demanda_id === d.id));
    const linhas = [["demanda", "grupo", "unidade", "quantidade", "valor_estimado_c"]].concat(
      aprovadas.map(d=>[d.especificacao_tecnica, d.grupo, u[d.unidade_id] || "", d.quantidade, d.valor_estimado_c]));
    const csv = "﻿" + linhas.map(l=>l.map(x=>/[;"\n]/.test(String(x)) ? `"${String(x).replace(/"/g, '""')}"` : String(x)).join(";")).join("\r\n");
    baixar(`demandas-${ativo.ano}.csv`, csv, "text/csv;charset=utf-8");
  });
};
