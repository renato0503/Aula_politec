/* ================= Sprint 4 · Proposta, parecer e decisão (RN07) ================= */
const TAP_TIPOS_DECISAO = {aprovacao: "Aprovação", rejeicao: "Rejeição", readequacao: "Readequação"};
const TAP_SIT_PORTFOLIO = ["em prospecção", "em captação", "captado", "não captado"];

// RN08: prioridade no portfólio só existe com justificativa
function tapFaltaPrioridade(pri){
  const falta = [];
  if (!(Number(pri.prioridade) >= 1 && Number(pri.prioridade) <= 5)) falta.push("prioridade de 1 a 5");
  if (String(pri.justificativa_prioridade || "").trim().length < 20) falta.push("justificativa da prioridade (20 caracteres)");
  if (!String(pri.fonte_recurso || "").trim()) falta.push("fonte de recurso");
  if (!TAP_SIT_PORTFOLIO.includes(pri.situacao_captacao)) falta.push("situação da captação");
  return falta;
}
teste("RN08: prioridade sem justificativa é recusada", ()=>{
  const ok = {prioridade: 1, justificativa_prioridade: "Impacto direto no atendimento e urgência da unidade.", fonte_recurso: "Tesouro estadual", situacao_captacao: "em captação"};
  return tapFaltaPrioridade(ok).length === 0 && tapFaltaPrioridade({...ok, justificativa_prioridade: "curta"}).length === 1
    && tapFaltaPrioridade({...ok, prioridade: 9}).length === 1;
});

async function tapPareceres(id){ return (await db.porIndice("pareceres", "proposta_id", id)).sort((a, b)=>(a.data || "").localeCompare(b.data || "")); }

TELAS["#/proposta/:id"] = async ({id})=>{
  const p = await db.get("propostas", id);
  if (!p) return `<div class="card vazio">Proposta ${esc(id)} não encontrada. <a href="#/portfolio">Portfólio</a></div>`;
  const [anexos, pends, decs, pares, docs] = await Promise.all([
    db.porIndice("anexos", "proposta_id", id), db.porIndice("pendencias", "proposta_id", id),
    db.porIndice("decisoes", "proposta_id", id), tapPareceres(id), documentosChecklist()]);
  const abertas = pends.filter(x=>!x.resolvida_em), falta = pendenciasTap(p, anexos, docs);
  const podeDecidir = ["em análise", "em analise", "aprovada"].includes(p.status);
  return `<p class="sub nao-imprimir" style="margin-bottom:6px"><a href="#/portfolio">← Portfólio</a></p>
    <h1>${esc(p.id)} · ${esc(p.titulo)} <span class="selo ${p.status === "aprovada" ? "ok" : p.status === "devolvida" ? "erro" : "info"}" id="tapStatus">${esc(p.status)}</span></h1>
    <p class="sub">${esc(p.unidade)} · ${esc(p.responsavel)} · ${dataCurtaBR(p.criado_em)} · ${dinheiro.fmt(Math.round((p.valor_estimado || 0) * 100))} · ${p.prazo_meses} meses</p>
    <div class="grade"><div class="card kpi"><div class="v">${anexos.length}</div><div class="r">anexos</div></div>
      <div class="card kpi"><div class="v" data-tap-abertas>${abertas.length}</div><div class="r">pendências abertas</div></div>
      <div class="card kpi"><div class="v">${pares.length}</div><div class="r">pareceres</div></div>
      <div class="card kpi"><div class="v">${decs.length}</div><div class="r">decisões</div></div></div>
    <div class="card"><h2 style="margin-top:0">TAP</h2>
      <table class="tabela-wrap"><tr><th>Objetivo</th><td>${esc(p.objetivo || "—")}</td></tr>
        <tr><th>Justificativa</th><td>${esc(p.justificativa || "—")}</td></tr>
        <tr><th>Objetivo estratégico</th><td>${esc(p.objetivo_estrategico || "—")}</td></tr>
        <tr><th>Contato</th><td>${esc(p.contato || "—")}</td></tr></table></div>
    <div class="card"><h2 style="margin-top:0">Anexos</h2>
      ${docs.map(d=>{ const a = anexos.find(x=>x.tipo === d.tipo); return `<p>${esc(d.nome)}${d.obrigatorio ? " *" : ""}: ${a ? '<span class="ok-txt">anexado</span>' : p.ausencias?.[d.tipo] ? '<span class="alerta-txt">ausência justificada</span>' : '<span class="erro-txt">falta</span>'}</p>`; }).join("")}
      ${falta.length ? `<p class="erro-txt">Falta: ${falta.map(esc).join(" · ")}</p>` : ""}</div>
    ${abertas.length ? `<div class="card pendente"><h2 style="margin-top:0">Pendências abertas</h2><ul>${abertas.map(x=>`<li>${esc(x.motivo)} · ${dataCurtaBR(x.aberta_em)}</li>`).join("")}</ul></div>` : ""}
    <div class="card"><h2 style="margin-top:0">Parecer da equipe</h2>
      <ul class="check-lista" id="tapPareceres">${pares.map(x=>`<li class="feito">${icone("check")}<span><b>${esc(x.resultado)}</b> · ${dataCurtaBR(x.data)} · ${esc(x.autor)}
        <br><small class="sub">${esc(x.texto)}</small></span></li>`).join("") || '<li class="vazio">Nenhum parecer.</li>'}</ul>
      ${["equipe"].includes(estado.perfil) && p.status !== "aprovada" ? `<form id="formTapParecer"><div class="campos">
        ${campo("tpResultado", "Resultado", {tipo: "select", opcoes: ["favorável", "favorável com ressalvas", "desfavorável"]})}
        ${campo("tpAutor", "Autor do parecer", {valor: "Equipe de projetos"})}</div>
        ${campo("tpTexto", "Parecer (mínimo de 30 caracteres)", {tipo: "textarea", linhas: 4})}
        <div id="tapErrosParecer"></div><div class="linha-botoes"><button class="prim" type="submit">Registrar parecer</button></div></form>` : ""}</div>
    <div class="card"><h2 style="margin-top:0">Decisão da autoridade (RN07)</h2>
      <ul class="check-lista" id="tapDecisoes">${decs.map(x=>`<li class="feito">${icone("check")}<span><b>${esc(TAP_TIPOS_DECISAO[x.tipo] || x.tipo)}</b> · ${dataCurtaBR(x.data)} · ${esc(x.autor)}
        <br><small class="sub">${esc(x.texto)}</small></span></li>`).join("") || '<li class="vazio">Nenhuma decisão.</li>'}</ul>
      ${["autoridade"].includes(estado.perfil) && podeDecidir ? `<form id="formTapDecisao"><div class="campos">
        ${campo("tdTipo", "Decisão", {tipo: "select", opcoes: Object.entries(TAP_TIPOS_DECISAO)})}
        ${campo("tdAutor", "Autoridade", {valor: "Autoridade competente"})}</div>
        ${campo("tdTexto", "Fundamento (mínimo de 20 caracteres)", {tipo: "textarea", linhas: 3})}
        <div id="tapErrosDecisao"></div><div class="linha-botoes"><button class="prim" type="submit">Registrar decisão</button></div></form>` : ""}</div>
    <div class="card tabela-wrap"><h2 style="margin-top:0">Histórico</h2><table><tr><th>Data e hora</th><th>Perfil</th><th>Ação</th></tr>
      ${(await db.list("log")).filter(l=>l.proposta_id === id).sort((a, b)=>(b.data_hora || "").localeCompare(a.data_hora || "")).map(l=>`<tr><td>${dataBR(l.data_hora)}</td><td>${esc(l.perfil)}</td><td>${esc(l.acao)}</td></tr>`).join("")}</table></div>`;
};
TELAS_DEPOIS["#/proposta/:id"] = ({id})=>{
  $("#formTapParecer")?.addEventListener("submit", async e=>{
    e.preventDefault();
    const texto = valorDe("tpTexto"), erros = [];
    if (texto.length < 30) erros.push("Escreva o parecer com pelo menos 30 caracteres.");
    if (!mostrarErros("#tapErrosParecer", erros)) return;
    const p = await db.get("propostas", id);
    await db.put("pareceres", {id: uuid(), proposta_id: id, resultado: valorDe("tpResultado"), texto, autor: valorDe("tpAutor") || "Equipe de projetos", data: agora(), perfil: estado.perfil});
    if (p.status === "em análise") await db.put("propostas", {...p, status: "em análise"});
    await registrar("parecer registrado", {proposta_id: id, detalhe: valorDe("tpResultado")});
    toast("Parecer registrado."); navegar();
  });
  $("#formTapDecisao")?.addEventListener("submit", async e=>{
    e.preventDefault();
    const tipo = valorDe("tdTipo"), texto = valorDe("tdTexto"), erros = [];
    if (texto.length < 20) erros.push("Escreva o fundamento com pelo menos 20 caracteres (RN07).");
    if (!mostrarErros("#tapErrosDecisao", erros)) return;
    const p = await db.get("propostas", id);
    const status = tipo === "aprovacao" ? "aprovada" : tipo === "rejeicao" ? "rejeitada" : "em análise";
    await db.put("decisoes", {id: uuid(), proposta_id: id, tipo, texto, autor: valorDe("tdAutor") || "Autoridade competente", data: agora(), perfil: estado.perfil});
    await db.put("propostas", {...p, status});
    await registrar("decisão registrada", {proposta_id: id, detalhe: TAP_TIPOS_DECISAO[tipo]});
    toast(`Decisão registrada: ${TAP_TIPOS_DECISAO[tipo]}.`); navegar();
  });
};

/* ================= Sprint 5 · Portfólio ================= */
TELAS["#/portfolio"] = async ()=>{
  const aprovadas = (await db.list("propostas")).filter(p=>p.status === "aprovada");
  const pri = Object.fromEntries((await db.list("portfolio")).map(x=>[x.proposta_id, x]));
  const linhas = aprovadas.map(p=>({p, x: pri[p.id] || null})).sort((a, b)=>(a.x?.prioridade ?? 99) - (b.x?.prioridade ?? 99));
  return `<h1>Portfólio</h1><p class="sub">${aprovadas.length} proposta(s) aprovada(s). A prioridade só entra com justificativa (RN08).</p>
    <div class="card tabela-wrap"><table id="tabelaPortfolio"><tr><th>Prioridade</th><th>TAP</th><th>Título</th><th class="num">Valor</th><th>Fonte de recurso</th><th>Captação</th></tr>
      ${linhas.map(({p, x})=>`<tr><td class="num">${x ? esc(x.prioridade) : '<span class="selo alerta">sem prioridade</span>'}</td><td>${esc(p.id)}</td>
        <td><a href="#/proposta/${encodeURIComponent(p.id)}">${esc(p.titulo)}</a></td><td class="num">${dinheiro.fmt(Math.round((p.valor_estimado || 0) * 100))}</td>
        <td>${esc(x?.fonte_recurso || "—")}</td><td>${esc(x?.situacao_captacao || "—")}</td></tr>`).join("")
        || '<tr><td colspan="6" class="vazio">Nenhuma proposta aprovada.</td></tr>'}</table></div>
    ${["equipe", "autoridade"].includes(estado.perfil) ? `<form class="card" id="formTapPrioridade"><h2 style="margin-top:0">Definir prioridade</h2><div class="campos">
      ${campo("prTap", "Proposta aprovada", {tipo: "select", opcoes: [["", "Escolha"], ...aprovadas.map(p=>[p.id, `${p.id} · ${p.titulo}`])]})}
      ${campo("prOrdem", "Prioridade (1 a 5)", {tipo: "number", attrs: 'min="1" max="5" step="1"'})}
      ${campo("prFonte", "Fonte de recurso", {ajuda: "Ex.: Tesouro estadual, emenda parlamentar."})}
      ${campo("prCaptacao", "Situação da captação", {tipo: "select", opcoes: [["", "Escolha"], ...TAP_SIT_PORTFOLIO.map(s=>[s, s])]})}</div>
      ${campo("prJust", "Justificativa da prioridade (mínimo de 20 caracteres)", {tipo: "textarea", linhas: 3})}
      <div id="tapErrosPrioridade"></div><div class="linha-botoes"><button class="prim" type="submit">Salvar prioridade</button>
        <button type="button" id="btnTapXlsx">${icone("download")} Exportar o portfólio (.xlsx)</button></div></form>`
      : `<div class="linha-botoes"><button id="btnTapXlsx">${icone("download")} Exportar o portfólio (.xlsx)</button></div>`}`;
};
TELAS_DEPOIS["#/portfolio"] = ()=>{
  $("#formTapPrioridade")?.addEventListener("submit", async e=>{
    e.preventDefault();
    const id = valorDe("prTap"), pri = {prioridade: Number(valorDe("prOrdem")), fonte_recurso: valorDe("prFonte"),
      situacao_captacao: valorDe("prCaptacao"), justificativa_prioridade: valorDe("prJust")};
    const erros = [!id && "Escolha a proposta."].concat(tapFaltaPrioridade(pri).map(f=>`Falta ${f} (RN08).`)).filter(Boolean);
    if (!mostrarErros("#tapErrosPrioridade", erros)) return;
    const antes = await db.get("portfolio", id);
    await db.put("portfolio", {proposta_id: id, ...pri, atualizado_em: agora(), perfil: estado.perfil});
    await registrar(antes ? "prioridade alterada" : "prioridade definida", {proposta_id: id, detalhe: `prioridade ${pri.prioridade}`});
    toast("Prioridade salva."); navegar();
  });
  $("#btnTapXlsx")?.addEventListener("click", async ()=>{
    const aprovadas = (await db.list("propostas")).filter(p=>p.status === "aprovada");
    const pri = Object.fromEntries((await db.list("portfolio")).map(x=>[x.proposta_id, x]));
    const dados = [["Prioridade", "TAP", "Título", "Unidade", "Valor estimado (R$)", "Fonte de recurso", "Situação da captação"]].concat(
      aprovadas.sort((a, b)=>(pri[a.id]?.prioridade ?? 99) - (pri[b.id]?.prioridade ?? 99))
        .map(p=>[pri[p.id]?.prioridade ?? "", p.id, p.titulo, p.unidade, Number(p.valor_estimado || 0), pri[p.id]?.fonte_recurso || "", pri[p.id]?.situacao_captacao || ""]));
    const livro = XLSX.utils.book_new(), aba = XLSX.utils.aoa_to_sheet(dados);
    XLSX.utils.book_append_sheet(livro, aba, "Portfólio");
    XLSX.writeFile(livro, `portfolio-${hojeISO()}.xlsx`);
    await registrar("portfólio exportado", {detalhe: `${aprovadas.length} propostas`});
  });
};

/* ================= Sprint 6 · Indicadores ================= */
TELAS["#/indicadores"] = async ()=>{
  const ps = await db.list("propostas"), pri = await db.list("portfolio");
  const porStatus = {}; for (const p of ps) porStatus[p.status] = (porStatus[p.status] || 0) + 1;
  const aprovadas = ps.filter(p=>p.status === "aprovada");
  const valorAprovado = aprovadas.reduce((a, p)=>a + Number(p.valor_estimado || 0), 0);
  const semPrioridade = aprovadas.filter(p=>!pri.some(x=>x.proposta_id === p.id)).length;
  const captados = pri.filter(x=>x.situacao_captacao === "captado").length;
  return `<h1>Indicadores do portfólio</h1><p class="sub">Visão do portfólio de projetos da POLITEC.</p>
    <div class="grade">
      <div class="card kpi"><div class="v" data-tap-ind="total">${ps.length}</div><div class="r">propostas no recorte</div></div>
      <div class="card kpi"><div class="v" data-tap-ind="aprovadas">${aprovadas.length}</div><div class="r">aprovadas</div></div>
      <div class="card kpi"><div class="v" data-tap-ind="valor">${dinheiro.fmt(Math.round(valorAprovado * 100))}</div><div class="r">valor do portfólio</div></div>
      <div class="card kpi"><div class="v" data-tap-ind="sem-prioridade">${semPrioridade}</div><div class="r">aprovadas sem prioridade</div></div>
      <div class="card kpi"><div class="v" data-tap-ind="captados">${captados}</div><div class="r">recursos captados</div></div></div>
    <div class="card tabela-wrap"><h2 style="margin-top:0">Propostas por situação</h2><table id="tabelaStatus"><tr><th>Situação</th><th class="num">Propostas</th></tr>
      ${Object.entries(porStatus).sort((a, b)=>b[1] - a[1]).map(([s, n])=>`<tr><td>${esc(s)}</td><td class="num">${n}</td></tr>`).join("")}</table></div>`;
};
