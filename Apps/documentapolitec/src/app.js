/* DOCUMENTAPOLITEC · código do app (Sprints 1 e 2) */
"use strict";
const DOC_STATUS = {pendente: "Pendente de conferência", conferida: "Conferida e lacrada", divergencia: "Com divergência"};
const docNumeros = texto => texto.split(/[\s,;]+/).map(s=>s.trim()).filter(Boolean);
// RN01: o mesmo prontuário não pode estar em duas caixas
function docDuplicados(numeros){ const vistos = new Set(), rep = []; for (const n of numeros){ if (vistos.has(n)) rep.push(n); vistos.add(n); } return [...new Set(rep)]; }
teste("Relação aceita linha, vírgula e ponto e vírgula", ()=> docNumeros("1001\n1002, 1003;1004").join("|") === "1001|1002|1003|1004");
teste("RN01: aponta prontuário repetido na relação", ()=> docDuplicados(["10", "11", "10"]).join() === "10");
teste("Exemplo com 12 caixas", ()=> dadosEmbutidos("seed").caixas.length === 12);

async function docResumoCaixa(c){
  const ps = await db.porIndice("prontuarios", "caixa_id", c.id_caixa);
  const conferidos = ps.filter(p=>p.conferido).length, divergentes = ps.filter(p=>p.conferido && !p.digital).length;
  return {total: ps.length, conferidos, divergentes, prontuarios: ps};
}

TELAS["#/painel"] = async ()=>{
  const cs = await db.list("caixas"), ps = await db.list("prontuarios");
  const conf = cs.filter(c=>c.status === "conferida").length, pend = cs.filter(c=>c.status !== "conferida").length;
  const div = ps.filter(p=>p.conferido && !p.digital).length;
  return `<h1>Painel do DOCUMENTAPOLITEC</h1><p class="sub">${cs.length} caixas no recorte, de um acervo de 1.000 caixas. <a href="#/caixa/nova">Cadastrar caixa</a></p>
    <div class="grade"><div class="card kpi"><div class="v">${cs.length}</div><div class="r">caixas cadastradas</div></div>
      <div class="card kpi"><div class="v" data-conferidas>${conf}</div><div class="r">conferidas e lacradas</div></div>
      <div class="card kpi"><div class="v">${pend}</div><div class="r">pendentes</div></div>
      <div class="card kpi"><div class="v">${ps.length}</div><div class="r">prontuários na relação</div></div></div>
    ${div ? `<div class="card pendente"><b>${div} prontuário(s)</b> conferido(s) sem correspondência no arquivo digital. Corrija antes de lacrar (RN02).</div>` : ""}
    <div class="card tabela-wrap"><table><tr><th>Caixa</th><th>Setor de origem</th><th class="num">Prontuários</th><th>Conferência</th><th>Lacre</th></tr>
      ${cs.sort((a, b)=>String(a.id_caixa).localeCompare(String(b.id_caixa))).map(c=>`<tr><td><a href="#/caixa/${encodeURIComponent(c.id_caixa)}">${esc(c.id_caixa)}</a></td>
        <td>${esc(c.setor_origem)}</td><td class="num">${ps.filter(p=>p.caixa_id === c.id_caixa).length}</td>
        <td><span class="selo ${c.status === "conferida" ? "ok" : c.status === "divergencia" ? "erro" : "info"}">${esc(DOC_STATUS[c.status] || c.status)}</span></td>
        <td>${c.lacrada_por ? esc(c.lacrada_por) + " · " + dataCurtaBR(c.lacrada_em) : "—"}</td></tr>`).join("")
        || '<tr><td colspan="5" class="vazio">Nenhuma caixa.</td></tr>'}</table></div>`;
};

TELAS["#/caixas"] = async ()=>{
  const cs = (await db.list("caixas")).sort((a, b)=>String(a.id_caixa).localeCompare(String(b.id_caixa)));
  return `<h1>Caixas</h1><p class="sub"><a href="#/caixa/nova">Cadastrar caixa</a></p>
    <div class="card tabela-wrap"><table><tr><th>Caixa</th><th>Setor</th><th>Situação</th><th class="num">Prontuários</th><th>Lacre</th></tr>
      ${cs.map(c=>`<tr><td><a href="#/caixa/${encodeURIComponent(c.id_caixa)}">${esc(c.id_caixa)}</a></td><td>${esc(c.setor_origem)}</td>
        <td><span class="selo ${c.status === "conferida" ? "ok" : c.status === "divergencia" ? "erro" : "info"}">${esc(c.status)}</span></td>
        <td class="num" data-qtd="${esc(c.id_caixa)}">${c.qtd}</td><td>${c.lacrada_por ? esc(c.lacrada_por) : "—"}</td></tr>`).join("")}</table></div>`;
};

TELAS["#/caixa/nova"] = async ()=> `<h1>Cadastrar caixa</h1><p class="sub">Cole a relação de prontuários da caixa (um por linha, ou separados por vírgula). Use números fictícios.</p>
  <form class="card" id="formDocNova" novalidate><div class="campos">
    ${campo("docCaixa", "Identificação da caixa", {obrigatorio: true, ajuda: "Ex.: CX-001."})}
    ${campo("docSetor", "Setor de origem", {obrigatorio: true})}
    ${campo("docResponsavel", "Responsável pela conferência", {obrigatorio: true, ajuda: "Quem assina o lacre (RN02)."})}
    ${campo("docData", "Data", {tipo: "date", valor: hojeISO(), obrigatorio: true})}</div>
  ${campo("docRelacao", "Relação de prontuários", {tipo: "textarea", linhas: 8, obrigatorio: true, ajuda: "Ex.: 2019.000123, 2019.000124..."})}
  <div id="docErros"></div><div class="linha-botoes"><button class="prim" type="submit">Cadastrar caixa</button></div></form>`;
TELAS_DEPOIS["#/caixa/nova"] = ()=>{
  $("#formDocNova").addEventListener("submit", async e=>{
    e.preventDefault();
    const id = valorDe("docCaixa"), setor = valorDe("docSetor"), resp = valorDe("docResponsavel"), data = valorDe("docData");
    const nums = docNumeros(valorDe("docRelacao")), cs = await db.list("caixas"), ps = await db.list("prontuarios");
    const erros = [];
    if (!id) erros.push("Informe a identificação da caixa.");
    else if (cs.some(c=>normalizar(c.id_caixa) === normalizar(id))) erros.push("Esta caixa já está cadastrada.");
    if (!setor) erros.push("Informe o setor de origem.");
    if (!resp) erros.push("Informe o responsável pela conferência (RN02).");
    if (!data || data > hojeISO()) erros.push("Informe uma data que não seja futura.");
    if (!nums.length) erros.push("Cole a relação de prontuários.");
    const rep = docDuplicados(nums); if (rep.length) erros.push(`Prontuário repetido na relação: ${rep.join(", ")} (RN01).`);
    const jaExiste = nums.filter(n=>ps.some(p=>p.numero === n)); if (jaExiste.length) erros.push(`Já cadastrado em outra caixa: ${jaExiste.slice(0, 5).join(", ")} (RN01).`);
    if (!mostrarErros("#docErros", erros)) return;
    // no protótipo, o arquivo digital é o próprio número: 1 a cada 12 fica sem correspondência (divergência do exemplo)
    for (const [i, n] of nums.entries()) await db.put("prontuarios", {numero: n, caixa_id: id, conferido: false, digital: (i + 1) % 12 !== 0});
    await db.put("caixas", {id_caixa: id, setor_origem: setor, responsavel: resp, data, qtd: nums.length, status: "pendente", criado_em: agora(), lacrada_por: null, lacrada_em: null});
    await db.put("log", {id: uuid(), caixa_id: id, acao: "caixa cadastrada", perfil: estado.perfil || "", data_hora: agora(), detalhe: `${nums.length} prontuários`});
    await registrar("caixa cadastrada", {detalhe: `${id} · ${nums.length} prontuários`});
    toast(`Caixa ${id} cadastrada com ${nums.length} prontuários.`); location.hash = "#/caixa/" + encodeURIComponent(id);
  });
};

TELAS["#/caixa/:id"] = async ({id})=>{
  const c = await db.get("caixas", id);
  if (!c) return `<div class="card vazio">Caixa não encontrada. <a href="#/caixas">Voltar</a></div>`;
  const {total, conferidos, divergentes, prontuarios} = await docResumoCaixa(c);
  const ls = (await db.porIndice("log", "caixa_id", id)).sort((a, b)=>b.data_hora.localeCompare(a.data_hora));
  return `<h1>Caixa ${esc(c.id_caixa)} <span class="selo ${c.status === "conferida" ? "ok" : c.status === "divergencia" ? "erro" : "info"}" id="docStatus">${esc(DOC_STATUS[c.status] || c.status)}</span></h1>
    <p class="sub">${esc(c.setor_origem)} · ${total} prontuários · responsável ${esc(c.responsavel)}</p>
    <div class="grade"><div class="card kpi"><div class="v">${total}</div><div class="r">prontuários na relação</div></div>
      <div class="card kpi"><div class="v">${conferidos}</div><div class="r">conferidos</div></div>
      <div class="card kpi"><div class="v">${divergentes}</div><div class="r">sem correspondência digital</div></div></div>
    <div class="card"><h2 style="margin-top:0">Conferência</h2>
      <p class="sub">O app compara a relação com o arquivo digital (simulado). Prontuário sem correspondência impede o lacre (RN02).</p>
      ${c.status === "conferida" ? `<p>Lacrada por <b>${esc(c.lacrada_por)}</b> em ${dataBR(c.lacrada_em)}.</p>`
        : `<div class="linha-botoes"><button class="prim" id="btnDocConferir">Conferir relação</button></div><div id="docErrosConf"></div>`}</div>
    <div class="card tabela-wrap"><table id="tabelaProntuarios"><tr><th>Prontuário</th><th>Arquivo digital</th><th>Situação</th></tr>
      ${prontuarios.map(p=>`<tr><td class="mono">${esc(p.numero)}</td><td>${p.conferido ? (p.digital ? '<span class="selo ok">localizado</span>' : '<span class="selo erro">ausente</span>') : "—"}</td>
        <td>${p.conferido ? (p.digital ? "conferido" : "divergência") : "pendente"}</td></tr>`).join("")}</table></div>
    <div class="card tabela-wrap"><h2 style="margin-top:0">Histórico</h2><table><tr><th>Data e hora</th><th>Ação</th><th>Detalhe</th></tr>
      ${ls.map(x=>`<tr><td>${dataBR(x.data_hora)}</td><td>${esc(x.acao)}</td><td>${esc(x.detalhe)}</td></tr>`).join("")}</table></div>`;
};
TELAS_DEPOIS["#/caixa/:id"] = ({id})=>{
  $("#btnDocConferir")?.addEventListener("click", async ()=>{
    const c = await db.get("caixas", id), ps = await db.porIndice("prontuarios", "caixa_id", id);
    for (const p of ps) await db.put("prontuarios", {...p, conferido: true});
    const falta = ps.filter(p=>!p.digital).length;
    const status = falta ? "divergencia" : "conferida";
    const lacre = falta ? {} : {lacrada_por: c.responsavel, lacrada_em: agora()};
    await db.put("caixas", {...c, status, ...lacre});
    await db.put("log", {id: uuid(), caixa_id: id, acao: falta ? "conferência com divergência" : "caixa conferida e lacrada",
      perfil: estado.perfil || "", data_hora: agora(), detalhe: falta ? `${falta} prontuário(s) sem correspondência` : c.responsavel});
    await registrar("conferência", {detalhe: `${id} · ${falta ? falta + " divergência(s)" : "lacrada"}`});
    if (falta) mostrarErros("#docErrosConf", [`${falta} prontuário(s) sem correspondência no arquivo digital. Corrija a relação antes de lacrar (RN02).`]);
    else toast("Caixa conferida e lacrada.");
    navegar();
  });
};

TELAS["#/busca"] = async ()=>{
  const q = estado.docBusca || "";
  let caixa = null;
  if (q) { const p = await db.get("prontuarios", q); caixa = p ? await db.get("caixas", p.caixa_id) : {nao: true}; }
  return `<h1>Buscar prontuário</h1><p class="sub">Localiza em qual caixa o prontuário físico está arquivado.</p>
    <div class="card"><div class="campos">${campo("docBusca", "Número do prontuário", {valor: q})}
      <div class="campo"><label>&nbsp;</label><button class="prim" id="btnDocBuscar">Buscar</button></div></div></div>
    ${q ? (caixa?.nao ? `<div class="card pendente">Prontuário ${esc(q)} não está na relação de nenhuma caixa cadastrada.</div>`
      : `<div class="card" id="resultadoBusca"><p>Prontuário <b class="mono">${esc(q)}</b> está na caixa
        <a href="#/caixa/${encodeURIComponent(caixa.id_caixa)}"><b>${esc(caixa.id_caixa)}</b></a> (${esc(caixa.setor_origem)}).</p></div>`) : ""}`;
};
TELAS_DEPOIS["#/busca"] = ()=>{
  $("#btnDocBuscar")?.addEventListener("click", ()=>{ estado.docBusca = valorDe("docBusca"); navegar(); });
};
