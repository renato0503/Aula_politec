/* ================= Sprint 3 · Situação, identificação e busca (RN02, RN04, RN05) ================= */
const TC_METODOS = ["papiloscopia", "DNA", "odontologia legal", "reconhecimento por familiar", "documento encontrado com o corpo"];

// RN05: fora da ficha, o nome aparece só pelas iniciais
const tcRotuloLista = c => c.identificado && c.nome ? tcIniciais(c.nome) : "sem identificação";

// transições de situação: devolve o erro ou "" quando a mudança é permitida
function tcTransicao(c, nova, {identificado, entrega, motivo}){
  if (!TC_SIT.includes(nova)) return "Situação desconhecida.";
  if (c.situacao === "liberado" && nova !== "liberado") return "O corpo já foi liberado. A liberação encerra a trilha.";
  if (nova === "liberado") return tcPodeLiberar({...c, identificado}, entrega) ? "" : "A liberação exige identificação e auto de entrega com responsável e documento (RN02).";
  if ((nova === "em custódia" || nova === "não reclamado") && !identificado) return `"${nova}" vale só para corpo identificado. Registre a identificação antes.`;
  if ((nova === "aguardando identificação" || nova === "não identificado") && identificado) return `"${nova}" vale só para corpo sem identificação.`;
  if ((nova === "não identificado" || nova === "não reclamado") && nova !== c.situacao && !motivo) return "Informe o motivo da mudança (prazo esgotado, edital, ofício).";
  return "";
}
teste("Sprint 3: transições de situação", ()=>{
  const sem = {situacao: "aguardando identificação", identificado: false}, com = {situacao: "em custódia", identificado: true};
  return tcTransicao(sem, "não identificado", {identificado: false, motivo: "30 dias"}) === ""
    && tcTransicao(sem, "não identificado", {identificado: false, motivo: ""}) !== ""
    && tcTransicao(sem, "em custódia", {identificado: false}) !== ""
    && tcTransicao(com, "não reclamado", {identificado: true, motivo: "edital"}) === ""
    && tcTransicao({situacao: "liberado", identificado: true}, "em custódia", {identificado: true}) !== "";
});
teste("RN05: iniciais no lugar do nome completo", ()=> tcRotuloLista({identificado: true, nome: "Maria Fictícia Souza"}) === "M. F. S" && tcRotuloLista({identificado: false}) === "sem identificação");

// RN04: protocolo, nome, documento ou lacre; todas as palavras precisam casar
async function tcBuscar(q){
  const n = normalizar(q).split(" ").filter(Boolean); if (!n.length) return [];
  const [cs, ls] = await Promise.all([db.list("corpos"), db.list("lacres")]);
  return cs.filter(c=>{
    const alvo = normalizar([c.protocolo, c.nome, c.documento, c.municipio, ...ls.filter(l=>l.corpo_id === c.id_corpo).map(l=>l.codigo)].join(" "));
    return n.every(p=>alvo.includes(p));
  }).sort((a, b)=>b.criado_em.localeCompare(a.criado_em));
}

function tcDias(c){ return Math.max(0, Math.floor((Date.now() - new Date(c.criado_em)) / 86400000)); }
function tcFiltroPainel(){ return estado.tcPainel ?? (estado.tcPainel = ""); }

TELAS["#/painel"] = async ()=>{
  const cs = await db.list("corpos"), ms = await db.list("marcos"), f = tcFiltroPainel();
  const por = s => cs.filter(c=>c.situacao === s).length;
  const ultimo = c => ms.filter(m=>m.corpo_id === c.id_corpo).sort((a, b)=>b.data_hora.localeCompare(a.data_hora))[0];
  const lista = cs.filter(c=>!f || c.situacao === f).sort((a, b)=>b.criado_em.localeCompare(a.criado_em));
  return `<h1>Painel do IML</h1><p class="sub">${cs.length} corpos no recorte. A lista mostra só as iniciais (RN05). <a href="#/corpo/novo">Novo acionamento</a></p>
    <div class="grade"><div class="card kpi"><div class="v" data-em-custodia>${por("em custódia")}</div><div class="r">em custódia</div></div>
      <div class="card kpi"><div class="v">${por("aguardando identificação")}</div><div class="r">aguardando identificação</div></div>
      <div class="card kpi"><div class="v">${por("não identificado") + por("não reclamado")}</div><div class="r">não identificados ou não reclamados</div></div>
      <div class="card kpi"><div class="v">${por("liberado")}</div><div class="r">liberados</div></div></div>
    <div class="card tabela-wrap"><h2 style="margin-top:0">Situação dos corpos</h2>
      <div class="chips" style="margin-bottom:12px">${[["", "Todas"], ...TC_SIT.map(s=>[s, s])].map(([v, t])=>`<button type="button" class="${f === v ? "prim" : ""}" data-tc-chip="${esc(v)}">${esc(t)} (${v ? por(v) : cs.length})</button>`).join("")}</div>
      <table id="tcTabelaPainel"><tr><th>Protocolo</th><th>Identificação</th><th>Origem</th><th>Situação</th><th class="num">Dias no IML</th><th>Último marco</th></tr>
      ${lista.map(c=>{ const u = ultimo(c), d = tcDias(c); return `<tr><td><a href="#/corpo/${encodeURIComponent(c.id_corpo)}">${esc(c.protocolo)}</a></td>
        <td>${esc(tcRotuloLista(c))}</td><td>${esc(c.municipio || c.origem)}</td><td><span class="selo ${tcSel(c.situacao)}">${esc(c.situacao)}</span></td>
        <td class="num">${c.situacao === "liberado" ? "—" : `<span class="${d > 30 ? "erro-txt" : d > 10 ? "alerta-txt" : ""}">${d}</span>`}</td>
        <td>${u ? esc(u.tipo) + " · " + dataBR(u.data_hora) : "—"}</td></tr>`; }).join("")
        || '<tr><td colspan="6" class="vazio">Nenhum corpo nesta situação.</td></tr>'}</table></div>`;
};
TELAS_DEPOIS["#/painel"] = ()=>{ $$("[data-tc-chip]").forEach(b=>b.addEventListener("click", ()=>{ estado.tcPainel = b.dataset.tcChip; navegar(); })); };

// a lista também segue a RN05
const tcCorposS2 = TELAS["#/corpos"];
TELAS["#/corpos"] = async p=>(await tcCorposS2(p))
  .replace("<th>Origem</th>", "<th>Identificação</th><th>Origem</th>")
  .replace(/(<tr><td><a href="#\/corpo\/([^"]+)">[^<]*<\/a><\/td>)/g, (m, ini, id)=>`${ini}<td data-tc-ini="${id}"></td>`);
TELAS_DEPOIS["#/corpos"] = async ()=>{
  $("#tcSit").addEventListener("change", e=>{ tcFiltros().situacao = e.target.value; navegar(); });
  for (const td of $$("[data-tc-ini]")){ const c = await db.get("corpos", decodeURIComponent(td.dataset.tcIni)); td.textContent = c ? tcRotuloLista(c) : ""; }
};

// ficha: linha do tempo dos marcos, identificação e situação com histórico
const tcFichaS2 = TELAS["#/corpo/:id"], tcFichaS2Depois = TELAS_DEPOIS["#/corpo/:id"];
TELAS["#/corpo/:id"] = async ({id})=>{
  let html = await tcFichaS2({id});
  const c = await db.get("corpos", id); if (!c) return html;
  html = html.replace('<ol class="linha-tempo">', '<ol class="linha-do-tempo" id="tcMarcos">').replace(/class="etapa-feita"/g, 'class="ldt-ok"').replace(/class="etapa-futura"/g, 'class="ldt-futuro"');
  const hist = (await db.porIndice("log", "corpo_id", id)).filter(l=>/^situação|^identificação/.test(l.acao)).sort((a, b)=>b.data_hora.localeCompare(a.data_hora));
  const final = c.situacao === "liberado";
  const card = `<div class="duas-colunas" style="margin-bottom:16px"><div class="card"><h2 style="margin-top:0">Situação e identificação</h2>
      <div class="etapas">${["acionamento", c.identificado ? "identificado" : "sem identificação", c.situacao].map((t, i, a)=>`<span class="${i < a.length - 1 || final ? "feita" : "atual"}">${esc(t)}</span>`).join("")}</div>
      ${final ? `<p class="ok-txt"><b>Liberado</b> para ${esc(c.entrega?.responsavel || "")} · auto ${esc(c.entrega?.documento || "")} · ${dataBR(c.entrega?.data)}</p>` : ""}
      <div class="campos">${campo("tcNovaSit", "Nova situação", {tipo: "select", opcoes: TC_SIT.map(s=>[s, s]), valor: c.situacao, attrs: final ? "disabled" : ""})}
        ${campo("tcMotivo", "Motivo ou documento", {ajuda: "Obrigatório para não identificado e não reclamado."})}</div>
      <label style="display:flex;gap:8px;align-items:center;margin:12px 0 4px"><input type="checkbox" id="tcIdent" ${c.identificado ? "checked" : ""} ${final ? "disabled" : ""}>
        <span>Corpo identificado</span></label>
      <div id="tcBlocoIdent" ${c.identificado && c.nome ? "hidden" : ""}><div class="campos">
        ${campo("tcIdNome", "Nome (fictício)", {valor: c.nome || ""})}${campo("tcIdDoc", "Documento (fictício)", {valor: c.documento || ""})}
        ${campo("tcIdMetodo", "Método de identificação", {tipo: "select", opcoes: [["", "Escolha"], ...TC_METODOS], valor: c.metodo_identificacao || ""})}</div></div>
      <div id="tcBlocoEntrega"><div class="campos">${campo("tcResp", "Responsável pela entrega", {valor: c.entrega?.responsavel || ""})}
        ${campo("tcDocEntrega", "Documento do auto", {valor: c.entrega?.documento || ""})}</div></div>
      <div id="tcErrosSit"></div>${final ? "" : '<div class="linha-botoes"><button class="prim" id="btnTcSit">Salvar situação</button></div>'}</div>
    <div class="card"><h2 style="margin-top:0">Histórico da situação</h2>
      <ol class="linha-do-tempo" id="tcHistSit">${hist.map(l=>`<li class="${/liberado/.test(l.acao) ? "ldt-ok" : /não /.test(l.acao) ? "ldt-alerta" : ""}"><div class="ldt-quando">${dataBR(l.data_hora)} · ${esc(l.perfil)}</div>
        <b>${esc(l.acao)}</b>${l.motivo ? `<div class="sub" style="margin:0">${esc(l.motivo)}</div>` : ""}</li>`).join("") || '<li class="vazio">Sem mudanças registradas.</li>'}</ol></div></div>`;
  const ini = html.indexOf('<div class="card"><h2 style="margin-top:0">Situação e liberação (RN02)</h2>'), fim = html.indexOf('<div class="card tabela-wrap"><h2 style="margin-top:0">Trilha de auditoria');
  return ini > 0 && fim > ini ? html.slice(0, ini) + card + html.slice(fim) : html + card;
};
TELAS_DEPOIS["#/corpo/:id"] = async ({id})=>{
  await tcFichaS2Depois({id});
  const btn = $("#btnTcSit"); if (!btn) return;
  const novo = btn.cloneNode(true); btn.replaceWith(novo);   // troca o comportamento do Sprint 2 pelo do Sprint 3
  const ajustar = ()=>{ $("#tcBlocoEntrega").hidden = valorDe("tcNovaSit") !== "liberado"; if ($("#tcIdent").checked) $("#tcBlocoIdent").hidden = false; };
  $("#tcNovaSit").addEventListener("change", ajustar); $("#tcIdent").addEventListener("change", ajustar); ajustar();
  novo.addEventListener("click", async ()=>{
    const c = await db.get("corpos", id), nova = valorDe("tcNovaSit"), identificado = $("#tcIdent").checked, motivo = valorDe("tcMotivo");
    const entrega = {responsavel: valorDe("tcResp"), documento: valorDe("tcDocEntrega")};
    const ident = {nome: valorDe("tcIdNome") || c.nome || "", documento: valorDe("tcIdDoc") || c.documento || "", metodo: valorDe("tcIdMetodo")};
    const erros = [];
    if (identificado && !c.identificado){ if (!ident.nome) erros.push("Informe o nome da pessoa identificada."); if (!ident.metodo) erros.push("Informe o método de identificação."); }
    const e = tcTransicao(c, nova, {identificado, entrega, motivo}); if (e) erros.push(e);
    if (!mostrarErros("#tcErrosSit", erros)) return;
    const novoC = {...c, situacao: nova, identificado};
    if (identificado && !c.identificado){
      Object.assign(novoC, {nome: ident.nome, documento: ident.documento, desconhecido: false, metodo_identificacao: ident.metodo, identificado_em: agora()});
      await db.put("log", {id: uuid(), corpo_id: id, acao: `identificação por ${ident.metodo}`, perfil: estado.perfil || "", data_hora: agora()});
    }
    if (nova === "liberado") novoC.entrega = {...entrega, data: agora()};
    await db.put("corpos", novoC);
    if (nova !== c.situacao) await db.put("log", {id: uuid(), corpo_id: id, acao: `situação: ${nova}`, motivo: motivo || (nova === "liberado" ? `auto ${entrega.documento}` : ""), perfil: estado.perfil || "", data_hora: agora()});
    await registrar("situação do corpo", {detalhe: `${c.protocolo} · ${nova}`});
    toast("Situação atualizada."); navegar();
  });
};

TELAS["#/busca"] = async ()=>{
  const q = estado.tcBusca || "", achados = q ? await tcBuscar(q) : [];
  return `<h1>Buscar corpo</h1><p class="sub">Por protocolo, nome, documento ou lacre (RN04). Use apenas dados fictícios.</p>
    <div class="card"><div class="busca-grande">${icone("busca")}<input id="tcBusca" type="search" value="${esc(q)}" placeholder="Ex.: NEC-2026-004, Maria, DOC-001, LC-0011" aria-label="Protocolo, nome, documento ou lacre">
      <button class="prim" id="btnTcBuscar">Buscar</button></div></div>
    ${q ? `<div class="card tabela-wrap" id="tcResultado"><h2 style="margin-top:0">${achados.length} resultado(s) para “${esc(q)}”</h2>
      <table><tr><th>Protocolo</th><th>Nome</th><th>Documento</th><th>Município</th><th>Situação</th></tr>
      ${achados.map(c=>`<tr><td><a href="#/corpo/${encodeURIComponent(c.id_corpo)}">${esc(c.protocolo)}</a></td><td>${esc(c.nome || "não identificado")}</td><td>${esc(c.documento || "—")}</td>
        <td>${esc(c.municipio)}</td><td><span class="selo ${tcSel(c.situacao)}">${esc(c.situacao)}</span></td></tr>`).join("") || '<tr><td colspan="5" class="vazio">Nenhum corpo encontrado.</td></tr>'}</table></div>` : ""}`;
};
TELAS_DEPOIS["#/busca"] = ()=>{
  const ir = async ()=>{ estado.tcBusca = valorDe("tcBusca"); await registrar("busca", {detalhe: estado.tcBusca}); navegar(); };
  $("#btnTcBuscar").addEventListener("click", ir);
  $("#tcBusca").addEventListener("keydown", e=>{ if (e.key === "Enter") ir(); });
};
