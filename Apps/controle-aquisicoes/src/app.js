/* Controle do Processo de Aquisição · código do app (Sprints 1 e 2) */
"use strict";
const CA_ETAPAS = ["DFD", "ETP", "Análise de riscos", "TR", "Pesquisa de preços", "SIGADOC e SIAG", "Análise técnica", "Análise jurídica", "Modalidade definida"];
const CA_DOCS = {"DFD": ["DFD"], "ETP": ["ETP"], "Análise de riscos": ["Análise de riscos"], "TR": ["TR"],
                 "Pesquisa de preços": ["Pesquisa de preços"], "SIGADOC e SIAG": [], "Análise técnica": [], "Análise jurídica": [], "Modalidade definida": []};
// Prazo de cada etapa, em dias úteis, e o artigo da Lei nº 14.133/2021 que a fundamenta.
// Os dias são elucubração (ver modelos/fluxo-e-prazos.md); os artigos são da lei.
const CA_PRAZO_ETAPA = {"DFD": 3, "ETP": 5, "Análise de riscos": 3, "TR": 5, "Pesquisa de preços": 7, "SIGADOC e SIAG": 2,
                        "Análise técnica": 5, "Análise jurídica": 10, "Modalidade definida": 3};
const CA_BASE_LEGAL = {"DFD": "art. 18, I e § 1º", "ETP": "art. 18, § 1º", "Análise de riscos": "art. 18, X", "TR": "art. 18, II",
                       "Pesquisa de preços": "art. 23, § 1º, IV", "SIGADOC e SIAG": "art. 12", "Análise técnica": "art. 11, I",
                       "Análise jurídica": "art. 53", "Modalidade definida": "art. 18, VIII"};
const CA_CICLO_DIAS = Object.values(CA_PRAZO_ETAPA).reduce((a, b) => a + b, 0);
teste("As 9 etapas têm prazo e base legal (Lei nº 14.133/2021)", ()=>{
  return CA_ETAPAS.every(e=>CA_PRAZO_ETAPA[e] > 0 && CA_BASE_LEGAL[e]) && CA_CICLO_DIAS === 43;
});
const CA_ATRAS = ["Documento incompleto", "Pesquisa de preços insuficiente", "Aguardando assinatura", "Aguardando análise jurídica", "Aguardando análise técnica"];
const caDias = (a, b = hojeISO())=> Math.round((new Date(b + "T12:00:00") - new Date(a + "T12:00:00")) / 86400000);
function caAtrasado(p, hoje = hojeISO()){ return p.status !== "concluido" && caDias(p.data_abertura, hoje) > Number(p.prazo_dias || 30); }
teste("Processo com prazo 30 e 40 dias está atrasado; concluído não", ()=>{
  const p = {data_abertura: "2026-09-19", prazo_dias: 30, status: "em andamento"}, hoje = "2026-10-29";
  return caAtrasado(p, hoje) && !caAtrasado({...p, data_abertura: "2026-10-10"}, hoje) && !caAtrasado({...p, status: "concluido"}, hoje);
});
// RN02: só conclui a etapa com os documentos exigidos por ela
function caFaltando(etapa, docs){ return (CA_DOCS[etapa] || []).filter(d=>!docs.some(x=>x.tipo_documento === d)); }
teste("RN02: ETP sem o documento fica faltando; etapa sem exigência não", ()=> caFaltando("ETP", []).join() === "ETP" && caFaltando("SIGADOC e SIAG", []).length === 0);
teste("Exemplo com 10 processos", ()=> dadosEmbutidos("seed").processos.length === 10);

TELAS["#/painel"] = async ()=>{
  const ps = await db.list("processos"), pends = await db.list("pendencias"), hoje = hojeISO();
  const ativos = ps.filter(p=>p.status !== "concluido"), atras = ativos.filter(p=>caAtrasado(p, hoje));
  const porEtapa = CA_ETAPAS.map(e=>({e, n: ativos.filter(p=>p.etapa === e).length}));
  return `<h1>Painel de Aquisições</h1><p class="sub">${ativos.length} processos em andamento. <a href="#/processo/novo">Nova aquisição</a></p>
    <div class="grade"><div class="card kpi"><div class="v">${ativos.length}</div><div class="r">em andamento</div></div>
      <div class="card kpi"><div class="v" data-atrasados>${atras.length}</div><div class="r">fora do prazo</div></div>
      <div class="card kpi"><div class="v">${pends.filter(x=>!x.resolvida_em).length}</div><div class="r">pendências abertas</div></div>
      <div class="card kpi"><div class="v">${ps.filter(p=>p.status === "concluido").length}</div><div class="r">concluídos</div></div></div>
    <div class="card tabela-wrap"><h2 style="margin-top:0">Processos por etapa</h2><table><tr><th>Etapa</th><th class="num">Processos</th></tr>
      ${porEtapa.map(x=>`<tr><td>${esc(x.e)}</td><td class="num">${x.n}</td></tr>`).join("")}</table></div>
    <div class="card tabela-wrap"><h2 style="margin-top:0">Fora do prazo</h2><table><tr><th>Processo</th><th>Objeto</th><th>Etapa</th><th class="num">Dias</th></tr>
      ${atras.sort((a, b)=>a.data_abertura.localeCompare(b.data_abertura)).map(p=>`<tr><td><a href="#/processo/${encodeURIComponent(p.id_processo)}">${esc(p.numero_sigadoc)}</a></td>
        <td>${esc(p.objeto)}</td><td>${esc(p.etapa)}</td><td class="num">${caDias(p.data_abertura)}</td></tr>`).join("")
        || '<tr><td colspan="4" class="vazio">Nenhum processo fora do prazo.</td></tr>'}</table></div>`;
};

function caFiltros(){ return estado.caFiltros || (estado.caFiltros = {etapa: "", status: "", busca: ""}); }
TELAS["#/processos"] = async ()=>{
  const f = caFiltros(), ps = await db.list("processos"), hoje = hojeISO(), b = normalizar(f.busca);
  const lista = ps.filter(p=>(!f.etapa || p.etapa === f.etapa) && (!f.status || p.status === f.status)
    && (!b || normalizar(`${p.numero_sigadoc} ${p.numero_siag} ${p.objeto} ${p.unidade}`).includes(b)))
    .sort((a, b2)=>b2.data_abertura.localeCompare(a.data_abertura));
  return `<h1>Processos <span class="sub">(${lista.length})</span></h1><p class="sub"><a href="#/processo/novo">Nova aquisição</a></p>
    <div class="card"><div class="campos">
      ${campo("caBusca", "Busca por número, objeto ou unidade", {valor: f.busca})}
      ${campo("caEtapa", "Etapa", {tipo: "select", opcoes: [["", "Todas"], ...CA_ETAPAS.map(e=>[e, e])], valor: f.etapa})}
      ${campo("caStatus", "Situação", {tipo: "select", opcoes: [["", "Todas"], ["em andamento", "Em andamento"], ["concluido", "Concluído"]], valor: f.status})}</div></div>
    <div class="card tabela-wrap"><table><tr><th>SIGADOC</th><th>SIAG</th><th>Objeto</th><th>Etapa</th><th class="num">Dias</th><th>Situação</th></tr>
      ${lista.map(p=>`<tr><td><a href="#/processo/${encodeURIComponent(p.id_processo)}">${esc(p.numero_sigadoc)}</a></td><td class="mono">${esc(p.numero_siag)}</td>
        <td>${esc(p.objeto)}</td><td>${esc(p.etapa)}</td><td class="num">${caDias(p.data_abertura)}</td>
        <td>${p.status === "concluido" ? '<span class="selo info">concluído</span>' : caAtrasado(p, hoje) ? '<span class="selo erro">atrasado</span>' : '<span class="selo ok">em prazo</span>'}</td></tr>`).join("")
        || '<tr><td colspan="6" class="vazio">Nenhum processo com estes filtros.</td></tr>'}</table></div>`;
};
TELAS_DEPOIS["#/processos"] = ()=>{
  const f = caFiltros();
  [["caBusca", "busca", "change"], ["caEtapa", "etapa", "input"], ["caStatus", "status", "input"]].forEach(([id, k, ev])=>
    $("#" + id).addEventListener(ev, e=>{ f[k] = e.target.value; navegar(); }));
};

TELAS["#/processo/novo"] = async ()=> `<h1>Nova aquisição</h1><p class="sub">O processo começa no DFD. Os números do SIGADOC e do SIAG são obrigatórios e únicos (RN01).</p>
  <form class="card" id="formCaNovo" novalidate><div class="campos">
    ${campo("caSigadoc", "Número no SIGADOC", {obrigatorio: true})}
    ${campo("caSiag", "Número no SIAG", {obrigatorio: true})}
    ${campo("caData", "Data de abertura", {tipo: "date", valor: hojeISO(), obrigatorio: true})}
    ${campo("caPrazo", "Prazo (dias corridos)", {tipo: "number", valor: 30, attrs: 'min="1" step="1"', obrigatorio: true})}
    ${campo("caUnidade", "Unidade requisitante", {obrigatorio: true})}
    ${campo("caResponsavel", "Responsável pela instrução", {obrigatorio: true})}</div>
  ${campo("caObjeto", "Objeto da aquisição", {tipo: "textarea", linhas: 2, obrigatorio: true})}
  ${campo("caDFD", "Documento DFD já anexado?", {tipo: "select", opcoes: [["sim", "Sim"], ["nao", "Não"]], ajuda: "Sem o DFD o processo não avança do DFD (RN02)."})}
  <div id="caErros"></div><div class="linha-botoes"><button class="prim" type="submit">Registrar aquisição</button></div></form>`;
TELAS_DEPOIS["#/processo/novo"] = ()=>{
  $("#formCaNovo").addEventListener("submit", async e=>{
    e.preventDefault();
    const ps = await db.list("processos");
    const d = {numero_sigadoc: valorDe("caSigadoc"), numero_siag: valorDe("caSiag"), data_abertura: valorDe("caData"), prazo_dias: Number(valorDe("caPrazo")),
      unidade: valorDe("caUnidade"), responsavel: valorDe("caResponsavel"), objeto: valorDe("caObjeto")};
    const erros = [];
    if (!d.numero_sigadoc) erros.push("Informe o número no SIGADOC (RN01).");
    else if (ps.some(p=>normalizar(p.numero_sigadoc) === normalizar(d.numero_sigadoc))) erros.push("Este processo já está cadastrado (RN01).");
    if (!d.numero_siag) erros.push("Informe o número no SIAG (RN01).");
    if (!d.data_abertura || d.data_abertura > hojeISO()) erros.push("Informe a data de abertura (não pode ser futura).");
    if (!(d.prazo_dias > 0)) erros.push("O prazo precisa ser de pelo menos 1 dia.");
    if (!d.unidade) erros.push("Informe a unidade requisitante.");
    if (!d.responsavel) erros.push("Informe o responsável pela instrução.");
    if (!d.objeto) erros.push("Informe o objeto da aquisição.");
    if (!mostrarErros("#caErros", erros)) return;
    const id = "AQ-" + String(ps.length + 1).padStart(4, "0");
    await db.put("processos", {id_processo: id, ...d, etapa: "DFD", status: "em andamento", criado_em: agora()});
    if (valorDe("caDFD") === "sim") await db.put("documentos", {id_documento: uuid(), processo_id: id, tipo_documento: "DFD", data: agora()});
    await db.put("log", {id: uuid(), processo_id: id, acao: "processo registrado", perfil: estado.perfil || "", data_hora: agora()});
    await registrar("aquisição registrada", {detalhe: d.numero_sigadoc});
    toast(`Processo ${id} registrado na etapa DFD.`); location.hash = "#/processo/" + encodeURIComponent(id);
  });
};

TELAS["#/processo/:id"] = async ({id})=>{
  const p = await db.get("processos", id);
  if (!p) return `<div class="card vazio">Processo não encontrado. <a href="#/processos">Voltar</a></div>`;
  const docs = await db.porIndice("documentos", "processo_id", id), pends = (await db.porIndice("pendencias", "processo_id", id)).sort((a, b)=>b.aberta_em.localeCompare(a.aberta_em));
  const ls = (await db.porIndice("log", "processo_id", id)).sort((a, b)=>b.data_hora.localeCompare(a.data_hora));
  const i = CA_ETAPAS.indexOf(p.etapa), falta = caFaltando(p.etapa, docs), abertas = pends.filter(x=>!x.resolvida_em);
  const pode = p.status !== "concluido";
  return `<h1>${esc(p.numero_sigadoc)} · ${esc(p.etapa)} ${p.status === "concluido" ? '<span class="selo info">concluído</span>' : ''}</h1>
    <p class="sub">SIAG ${esc(p.numero_siag)} · ${esc(p.unidade)} · responsável ${esc(p.responsavel)} · aberto em ${dataCurtaBR(p.data_abertura)}</p>
    <div class="grade"><div class="card kpi"><div class="v">${caDias(p.data_abertura)}</div><div class="r">dias desde a abertura (prazo ${p.prazo_dias})</div></div>
      <div class="card kpi"><div class="v">${i + 1}/${CA_ETAPAS.length}</div><div class="r">etapa atual</div></div>
      <div class="card kpi"><div class="v">${docs.length}</div><div class="r">documentos anexados</div></div>
      <div class="card kpi"><div class="v">${abertas.length}</div><div class="r">pendências abertas</div></div></div>
    <div class="card"><h2 style="margin-top:0">Objeto</h2><p>${esc(p.objeto)}</p>
      <h2>Etapas</h2><ol class="linha-tempo" id="caEtapas">${CA_ETAPAS.map((e, k)=>`<li class="${k < i ? "etapa-feita" : k === i ? "etapa-atual" : "etapa-futura"}"><b>${k + 1}. ${esc(e)}</b>${k === i ? " · atual" : ""}
        <br><small class="sub">prazo de ${CA_PRAZO_ETAPA[e]} dia(s) · ${esc(CA_BASE_LEGAL[e])}</small></li>`).join("")}</ol>
      <p class="sub">Ciclo pelas 9 etapas: <b>${CA_CICLO_DIAS} dias</b> de prazo interno, contra ${p.prazo_dias} dias do processo. ${CA_CICLO_DIAS > p.prazo_dias ? "<b class=erro-txt>O ciclo não cabe no prazo: é preciso revisar os prazos das etapas ou ampliar o prazo do processo.</b>" : ""}</p>
      ${pode ? `<p class="sub">Documentos exigidos nesta etapa: ${(CA_DOCS[p.etapa] || []).join(", ") || "nenhum"}. ${falta.length ? `<b class="erro-txt">Falta: ${falta.map(esc).join(", ")}</b>` : '<b class="ok-txt">Completo</b>'}</p>` : ""}</div>
    ${pode ? `<form class="card" id="formCaDoc"><h2 style="margin-top:0">Anexar documento</h2><div class="campos">
        ${campo("caTipo", "Tipo", {tipo: "select", opcoes: [["", "Escolha"], ...Object.keys(CA_DOCS).map(x=>[x, x])]})}
        ${campo("caNome", "Nome do arquivo (fictício)", {ajuda: "Ex.: DFD-assinado.pdf"})}</div>
      <div id="caErrosDoc"></div><div class="linha-botoes"><button class="prim" type="submit">Anexar</button></div></form>` : ""}
    <div class="card tabela-wrap"><h2 style="margin-top:0">Documentos (${docs.length})</h2><table><tr><th>Tipo</th><th>Nome</th><th>Data</th></tr>
      ${docs.map(d=>`<tr><td>${esc(d.tipo_documento)}</td><td>${esc(d.nome || "—")}</td><td>${dataCurtaBR(d.data)}</td></tr>`).join("") || '<tr><td colspan="3" class="vazio">Nenhum documento.</td></tr>'}</table></div>
    ${pode ? `<form class="card" id="formCaPend"><h2 style="margin-top:0">Registrar pendência</h2>${campo("caMotivo", "Motivo", {tipo: "select", opcoes: [["", "Escolha"], ...CA_ATRAS.map(x=>[x, x])]})}
      <div id="caErrosPend"></div><div class="linha-botoes"><button id="btnCaPend">Abrir pendência</button><button class="prim" type="button" id="btnCaAvancar">Concluir a etapa ${esc(p.etapa)}</button></div></form>` : ""}
    <div class="card tabela-wrap"><h2 style="margin-top:0">Pendências</h2><table><tr><th>Motivo</th><th>Aberta em</th><th>Situação</th></tr>
      ${pends.map(x=>`<tr><td>${esc(x.motivo)}</td><td>${dataCurtaBR(x.aberta_em)}</td><td>${x.resolvida_em ? "resolvida em " + dataCurtaBR(x.resolvida_em) : '<span class="selo erro">aberta</span>'}</td></tr>`).join("") || '<tr><td colspan="3" class="vazio">Nenhuma pendência.</td></tr>'}</table></div>
    <div class="card tabela-wrap"><h2 style="margin-top:0">Histórico</h2><table id="caHistorico"><tr><th>Data e hora</th><th>Ação</th></tr>
      ${ls.map(x=>`<tr><td>${dataBR(x.data_hora)}</td><td>${esc(x.acao)}</td></tr>`).join("")}</table></div>`;
};
TELAS_DEPOIS["#/processo/:id"] = ({id})=>{
  $("#formCaDoc")?.addEventListener("submit", async e=>{
    e.preventDefault();
    const tipo = valorDe("caTipo"), p = await db.get("processos", id), erros = [];
    if (!tipo) erros.push("Escolha o tipo de documento.");
    if (!mostrarErros("#caErrosDoc", erros)) return;
    await db.put("documentos", {id_documento: uuid(), processo_id: id, tipo_documento: tipo, nome: valorDe("caNome"), data: agora()});
    await db.put("log", {id: uuid(), processo_id: id, acao: `documento anexado: ${tipo}`, perfil: estado.perfil || "", data_hora: agora()});
    toast(`${tipo} anexado.`); navegar();
  });
  $("#btnCaPend")?.addEventListener("click", async ()=>{
    const motivo = valorDe("caMotivo");
    if (!motivo) return mostrarErros("#caErrosPend", ["Escolha o motivo da pendência."]);
    await db.put("pendencias", {id_pendencia: uuid(), processo_id: id, motivo, aberta_em: hojeISO(), resolvida_em: null});
    await db.put("log", {id: uuid(), processo_id: id, acao: `pendência: ${motivo}`, perfil: estado.perfil || "", data_hora: agora()});
    toast("Pendência registrada."); navegar();
  });
  $("#btnCaAvancar")?.addEventListener("click", async ()=>{
    const p = await db.get("processos", id), docs = await db.porIndice("documentos", "processo_id", id), pends = await db.porIndice("pendencias", "processo_id", id);
    const falta = caFaltando(p.etapa, docs), abertas = pends.filter(x=>!x.resolvida_em).length, erros = [];
    if (falta.length) erros.push(`Anexe antes de avançar: ${falta.join(", ")} (RN02).`);
    if (abertas) erros.push(`Resolva as ${abertas} pendência(s) abertas antes de avançar (RN03).`);
    if (!mostrarErros("#caErrosPend", erros)) return;
    const i = CA_ETAPAS.indexOf(p.etapa), fim = i === CA_ETAPAS.length - 1;
    await db.put("processos", {...p, etapa: fim ? p.etapa : CA_ETAPAS[i + 1], status: fim ? "concluido" : p.status});
    await db.put("log", {id: uuid(), processo_id: id, acao: fim ? "processo concluído" : `etapa concluída: ${p.etapa}`, perfil: estado.perfil || "", data_hora: agora()});
    toast(fim ? "Processo concluído." : `Avançou para ${CA_ETAPAS[i + 1]}.`); navegar();
  });
};
