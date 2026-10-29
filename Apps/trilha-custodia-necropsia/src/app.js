/* TCIN · Trilha de Custódia e Identificação · código do app (Sprints 1 e 2) */
"use strict";
const TC_SIT = ["em custódia", "aguardando identificação", "não identificado", "não reclamado", "liberado"];
const TC_MARCOS = ["Saída da base", "Chegada ao local", "Saída do local", "Retorno ao IML"];
const tcAgora = ()=>{ const d = new Date(), z = n=>String(n).padStart(2, "0"); return `${d.getFullYear()}-${z(d.getMonth() + 1)}-${z(d.getDate())}T${z(d.getHours())}:${z(d.getMinutes())}`; };
const tcIniciais = n => String(n || "").trim().split(/\s+/).filter(Boolean).map(p=>p[0].toUpperCase()).join(". ");
// RN01: o protocolo é único
async function tcProtocolo(){
  const ano = new Date().getFullYear(), usados = new Set((await db.list("corpos")).map(c=>c.protocolo));
  let n = 1; while (usados.has(`NEC-${ano}-${String(n).padStart(3, "0")}`)) n++;
  return `NEC-${ano}-${String(n).padStart(3, "0")}`;
}
// RN02: só libera com identificação e auto de entrega
function tcPodeLiberar(c, entrega){
  return !!c.identificado && !!String(entrega?.responsavel || "").trim() && !!String(entrega?.documento || "").trim();
}
teste("RN02: liberação exige identificação e auto de entrega", ()=>{
  return !tcPodeLiberar({identificado: false}, {responsavel: "X", documento: "Y"}) && !tcPodeLiberar({identificado: true}, {responsavel: "", documento: "Y"}) && tcPodeLiberar({identificado: true}, {responsavel: "X", documento: "Y"});
});
teste("Exemplo com 12 corpos", ()=> dadosEmbutidos("seed").corpos.length === 12);
const tcSel = s => s === "liberado" ? "info" : s === "não identificado" || s === "não reclamado" ? "alerta" : "ok";

async function tcMarcos(corpo_id){ return (await db.porIndice("marcos", "corpo_id", corpo_id)).sort((a, b)=>a.data_hora.localeCompare(b.data_hora)); }
async function tcLacres(corpo_id){ return (await db.porIndice("lacres", "corpo_id", corpo_id)).sort((a, b)=>a.data_hora.localeCompare(b.data_hora)); }
async function tcAuditar(corpo_id, acao){ await db.put("log", {id: uuid(), corpo_id, acao, perfil: estado.perfil || "", data_hora: agora()}); }

TELAS["#/painel"] = async ()=>{
  const cs = await db.list("corpos"), ms = await db.list("marcos");
  const por = s => cs.filter(c=>c.situacao === s).length;
  const ultimo = c => ms.filter(m=>m.corpo_id === c.id_corpo).sort((a, b)=>b.data_hora.localeCompare(a.data_hora))[0];
  return `<h1>Painel do IML</h1><p class="sub">${cs.length} corpos no recorte. <a href="#/corpo/novo">Novo acionamento</a></p>
    <div class="grade"><div class="card kpi"><div class="v" data-em-custodia>${por("em custódia")}</div><div class="r">em custódia</div></div>
      <div class="card kpi"><div class="v">${por("aguardando identificação")}</div><div class="r">aguardando identificação</div></div>
      <div class="card kpi"><div class="v">${por("não identificado") + por("não reclamado")}</div><div class="r">não identificados ou não reclamados</div></div>
      <div class="card kpi"><div class="v">${por("liberado")}</div><div class="r">liberados</div></div></div>
    <div class="card tabela-wrap"><h2 style="margin-top:0">Situação dos corpos</h2><table><tr><th>Protocolo</th><th>Origem</th><th>Situação</th><th>Último marco</th></tr>
      ${cs.sort((a, b)=>b.criado_em.localeCompare(a.criado_em)).map(c=>{ const u = ultimo(c); return `<tr><td><a href="#/corpo/${encodeURIComponent(c.id_corpo)}">${esc(c.protocolo)}</a></td>
        <td>${esc(c.municipio || c.origem)}</td><td><span class="selo ${tcSel(c.situacao)}">${esc(c.situacao)}</span></td>
        <td>${u ? esc(u.tipo) + " · " + dataBR(u.data_hora) : "—"}</td></tr>`; }).join("")
        || '<tr><td colspan="4" class="vazio">Nenhum corpo.</td></tr>'}</table></div>`;
};

function tcFiltros(){ return estado.tcFiltros || (estado.tcFiltros = {situacao: ""}); }
TELAS["#/corpos"] = async ()=>{
  const f = tcFiltros(), cs = (await db.list("corpos")).filter(c=>!f.situacao || c.situacao === f.situacao)
    .sort((a, b)=>b.criado_em.localeCompare(a.criado_em));
  return `<h1>Corpos <span class="sub">(${cs.length})</span></h1><p class="sub"><a href="#/corpo/novo">Novo acionamento</a></p>
    <div class="card"><div class="campos">${campo("tcSit", "Situação", {tipo: "select", opcoes: [["", "Todas"], ...TC_SIT.map(s=>[s, s])], valor: f.situacao})}</div></div>
    <div class="card tabela-wrap"><table><tr><th>Protocolo</th><th>Origem</th><th>Natureza</th><th>Situação</th><th>Entrada</th></tr>
      ${cs.map(c=>`<tr><td><a href="#/corpo/${encodeURIComponent(c.id_corpo)}">${esc(c.protocolo)}</a></td><td>${esc(c.municipio || c.origem)}</td>
        <td>${esc(c.natureza)}</td><td><span class="selo ${tcSel(c.situacao)}">${esc(c.situacao)}</span></td><td>${dataCurtaBR(c.criado_em)}</td></tr>`).join("")
        || '<tr><td colspan="5" class="vazio">Nenhum corpo com esta situação.</td></tr>'}</table></div>`;
};
TELAS_DEPOIS["#/corpos"] = ()=>{ $("#tcSit").addEventListener("change", e=>{ tcFiltros().situacao = e.target.value; navegar(); }); };

TELAS["#/corpo/novo"] = async ()=>{
  const prot = await tcProtocolo();
  return `<h1>Novo acionamento</h1><p class="sub">Use apenas dados fictícios. O protocolo é gerado no acionamento (RN01).</p>
    <form class="card" id="formTcNovo" novalidate><div class="campos">
      ${campo("tcProt", "Protocolo", {valor: prot, obrigatorio: true})}
      ${campo("tcOrigem", "Autoridade/origem", {obrigatorio: true, ajuda: "Ex.: Delegacia de Polícia de Cuiabá."})}
      ${campo("tcNat", "Natureza", {obrigatorio: true, ajuda: "Ex.: local de crime, morte natural, acidente."})}
      ${campo("tcMun", "Município", {obrigatorio: true})}
      ${campo("tcTec", "Técnico responsável", {obrigatorio: true})}
      ${campo("tcData", "Data do acionamento", {tipo: "datetime-local", valor: tcAgora(), obrigatorio: true})}</div>
    ${campo("tcLocal", "Local da ocorrência", {obrigatorio: true})}
    <label style="display:flex;gap:8px;align-items:center;margin:8px 0"><input type="checkbox" id="tcDesc" style="width:auto" checked>
      <span>Corpo sem identificação (não informar nome)</span></label>
    <div class="campos">${campo("tcNome", "Nome (fictício)", {ajuda: "Obrigatório se o corpo estiver identificado."})}${campo("tcDoc", "Documento (fictício)")}
      ${campo("tcSexo", "Sexo", {tipo: "select", opcoes: [["", "Não informado"], ["Feminino", "Feminino"], ["Masculino", "Masculino"]]})}
      ${campo("tcIdade", "Idade aparente", {tipo: "number", attrs: 'min="0" max="120"'})}</div>
    <div id="tcErros"></div><div class="linha-botoes"><button class="prim" type="submit">Registrar corpo</button></div></form>`;
};
TELAS_DEPOIS["#/corpo/novo"] = ()=>{
  $("#tcDesc").addEventListener("change", e=>{ $("#tcNome").disabled = e.target.checked; if (e.target.checked) $("#tcNome").value = ""; });
  $("#formTcNovo").addEventListener("submit", async e=>{
    e.preventDefault();
    const desconhecido = $("#tcDesc").checked;
    const d = {protocolo: valorDe("tcProt"), origem: valorDe("tcOrigem"), natureza: valorDe("tcNat"), municipio: valorDe("tcMun"), tecnico: valorDe("tcTec"),
      criado_em: (valorDe("tcData") || tcAgora()) + ":00", local: valorDe("tcLocal"), nome: desconhecido ? "" : valorDe("tcNome"), documento: valorDe("tcDoc"),
      desconhecido, sexo: valorDe("tcSexo"), idade: valorDe("tcIdade")};
    const cs = await db.list("corpos"), erros = [];
    if (!d.protocolo) erros.push("Informe o protocolo.");
    else if (cs.some(c=>normalizar(c.protocolo) === normalizar(d.protocolo))) erros.push("Este protocolo já está registrado (RN01).");
    if (!d.origem) erros.push("Informe a autoridade/origem.");
    if (!d.natureza) erros.push("Informe a natureza.");
    if (!d.municipio) erros.push("Informe o município.");
    if (!d.tecnico) erros.push("Informe o técnico responsável.");
    if (!d.local) erros.push("Informe o local.");
    if (!desconhecido && !d.nome) erros.push("Informe o nome ou marque o corpo como sem identificação.");
    if (!mostrarErros("#tcErros", erros)) return;
    const id = "C-" + String(cs.length + 1).padStart(4, "0");
    const situacao = desconhecido ? "aguardando identificação" : "em custódia";
    await db.put("corpos", {id_corpo: id, ...d, identificado: !desconhecido, situacao});
    await tcAuditar(id, "corpo registrado");
    await registrar("corpo registrado", {detalhe: d.protocolo});
    toast(`Corpo ${d.protocolo} registrado.`); location.hash = "#/corpo/" + encodeURIComponent(id);
  });
};

TELAS["#/corpo/:id"] = async ({id})=>{
  const c = await db.get("corpos", id);
  if (!c) return `<div class="card vazio">Corpo não encontrado. <a href="#/corpos">Voltar</a></div>`;
  const [ms, ls, logs] = await Promise.all([tcMarcos(id), tcLacres(id), db.porIndice("log", "corpo_id", id)]);
  const feitos = new Set(ms.map(m=>m.tipo));
  return `<h1>${esc(c.protocolo)} <span class="selo ${tcSel(c.situacao)}" id="tcSitAtual">${esc(c.situacao)}</span></h1>
    <p class="sub">${esc(c.municipio)} · ${esc(c.natureza)} · entrada em ${dataBR(c.criado_em)} · técnico ${esc(c.tecnico)}</p>
    <div class="grade"><div class="card kpi"><div class="v">${ms.length}/4</div><div class="r">marcos registrados</div></div>
      <div class="card kpi"><div class="v">${ls.length}</div><div class="r">lacres</div></div>
      <div class="card kpi"><div class="v">${c.desconhecido ? "sem nome" : esc(tcIniciais(c.nome))}</div><div class="r">${c.identificado ? "identificado" : "sem identificação"}</div></div></div>
    <div class="card"><h2 style="margin-top:0">Corpo</h2><p>Origem: ${esc(c.origem)}<br>Local: ${esc(c.local)}<br>
      Nome: <b>${c.nome ? esc(c.nome) : "não identificado"}</b> · documento ${esc(c.documento || "—")} · ${esc(c.sexo || "sexo não informado")} · ${c.idade ? esc(c.idade) + " anos" : "idade não informada"}</p></div>
    <div class="card"><h2 style="margin-top:0">Marcos do deslocamento (RN03)</h2>
      <ol class="linha-tempo">${TC_MARCOS.map(t=>{ const m = ms.filter(x=>x.tipo === t).pop(); return `<li class="${m ? "etapa-feita" : "etapa-futura"}"><b>${esc(t)}</b>${m ? ` · ${dataBR(m.data_hora)} · ${esc(m.perfil)}` : " · pendente"}</li>`; }).join("")}</ol>
      <div class="campos">${campo("tcMarco", "Marco", {tipo: "select", opcoes: [["", "Escolha"], ...TC_MARCOS.filter(t=>!feitos.has(t)).map(t=>[t, t])]})}
        ${campo("tcMarcoData", "Data e hora", {tipo: "datetime-local", valor: tcAgora()})}</div>
      <div id="tcErrosMarco"></div><div class="linha-botoes"><button id="btnTcMarco">Registrar marco</button></div></div>
    <div class="card"><h2 style="margin-top:0">Lacres e amostras</h2>
      ${ls.length ? `<table><tr><th>Código</th><th>Destino</th><th>Data</th><th>Perfil</th></tr>${ls.map(l=>`<tr><td class="mono">${esc(l.codigo)}</td><td>${esc(l.destino)}</td><td>${dataBR(l.data_hora)}</td><td>${esc(l.perfil)}</td></tr>`).join("")}</table>` : '<p class="sub">Nenhum lacre registrado.</p>'}
      <div class="campos">${campo("tcLacre", "Código do lacre", {attrs: 'placeholder="LC-0001"'})}${campo("tcDestino", "Destino", {attrs: 'placeholder="Laboratório de DNA"'})}</div>
      <div id="tcErrosLacre"></div><div class="linha-botoes"><button id="btnTcLacre">Registrar lacre</button></div></div>
    <div class="card"><h2 style="margin-top:0">Situação e liberação (RN02)</h2>
      <div class="campos">${campo("tcNovaSit", "Nova situação", {tipo: "select", opcoes: TC_SIT.map(s=>[s, s]), valor: c.situacao})}
        ${campo("tcResp", "Responsável pela entrega", {valor: c.entrega?.responsavel || ""})}
        ${campo("tcDocEntrega", "Documento do auto", {valor: c.entrega?.documento || ""})}</div>
      <label style="display:flex;gap:8px;align-items:center;margin:8px 0"><input type="checkbox" id="tcIdent" style="width:auto" ${c.identificado ? "checked" : ""}>
        <span>Corpo identificado</span></label>
      <div id="tcErrosSit"></div><div class="linha-botoes"><button id="btnTcSit">Salvar situação</button></div></div>
    <div class="card tabela-wrap"><h2 style="margin-top:0">Trilha de auditoria</h2><table id="tcAuditoria"><tr><th>Data e hora</th><th>Perfil</th><th>Ação</th></tr>
      ${logs.sort((a, b)=>b.data_hora.localeCompare(a.data_hora)).map(l=>`<tr><td>${dataBR(l.data_hora)}</td><td>${esc(l.perfil)}</td><td>${esc(l.acao)}</td></tr>`).join("")}</table></div>`;
};
TELAS_DEPOIS["#/corpo/:id"] = ({id})=>{
  $("#btnTcMarco")?.addEventListener("click", async ()=>{
    const tipo = valorDe("tcMarco"), quando = valorDe("tcMarcoData");
    if (!tipo) return mostrarErros("#tcErrosMarco", ["Escolha o marco."]);
    if (!quando) return mostrarErros("#tcErrosMarco", ["Informe a data e a hora."]);
    await db.put("marcos", {id_marco: uuid(), corpo_id: id, tipo, data_hora: quando + ":00", perfil: estado.perfil || "", observacao: ""});
    await tcAuditar(id, `marco: ${tipo}`); toast("Marco registrado."); navegar();
  });
  $("#btnTcLacre")?.addEventListener("click", async ()=>{
    const codigo = valorDe("tcLacre"), destino = valorDe("tcDestino");
    if (!codigo || !destino) return mostrarErros("#tcErrosLacre", ["Informe o código do lacre e o destino."]);
    await db.put("lacres", {id_lacre: uuid(), corpo_id: id, codigo, destino, data_hora: agora(), perfil: estado.perfil || ""});
    await tcAuditar(id, `lacre ${codigo}`); toast("Lacre registrado."); navegar();
  });
  $("#btnTcSit")?.addEventListener("click", async ()=>{
    const c = await db.get("corpos", id), nova = valorDe("tcNovaSit"), entrega = {responsavel: valorDe("tcResp"), documento: valorDe("tcDocEntrega")};
    const identificado = $("#tcIdent").checked;
    if (nova === "liberado" && !tcPodeLiberar({...c, identificado}, entrega)) return mostrarErros("#tcErrosSit", ["A liberação exige identificação e auto de entrega com responsável e documento (RN02)."]);
    await db.put("corpos", {...c, situacao: nova, identificado, entrega: nova === "liberado" ? {...entrega, data: agora()} : c.entrega});
    await tcAuditar(id, `situação: ${nova}`); toast("Situação atualizada."); navegar();
  });
};

TELAS["#/busca"] = async ()=>{
  const q = estado.tcBusca || "";
  let achados = [];
  if (q) { const n = normalizar(q); achados = (await db.list("corpos")).filter(c=>normalizar(c.protocolo).includes(n) || normalizar(c.nome).includes(n) || normalizar(c.documento).includes(n)); }
  return `<h1>Buscar corpo</h1><p class="sub">Por protocolo, nome ou documento (RN04). Use apenas dados fictícios.</p>
    <div class="card"><div class="campos">${campo("tcBusca", "Protocolo, nome ou documento", {valor: q})}
      <div class="campo"><label>&nbsp;</label><button class="prim" id="btnTcBuscar">Buscar</button></div></div></div>
    ${q ? `<div class="card tabela-wrap" id="tcResultado"><table><tr><th>Protocolo</th><th>Nome</th><th>Situação</th></tr>
      ${achados.map(c=>`<tr><td><a href="#/corpo/${encodeURIComponent(c.id_corpo)}">${esc(c.protocolo)}</a></td><td>${esc(c.nome || "não identificado")}</td>
        <td><span class="selo ${tcSel(c.situacao)}">${esc(c.situacao)}</span></td></tr>`).join("") || '<tr><td colspan="3" class="vazio">Nenhum corpo encontrado.</td></tr>'}</table></div>` : ""}`;
};
TELAS_DEPOIS["#/busca"] = ()=>{ $("#btnTcBuscar")?.addEventListener("click", ()=>{ estado.tcBusca = valorDe("tcBusca"); navegar(); }); };
