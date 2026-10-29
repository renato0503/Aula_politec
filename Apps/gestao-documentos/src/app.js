/* Gestão de Documentos · código do app (Sprints 1 e 2) */
"use strict";
const GD_ANEXOS = ["Requerimento", "Documento de identificação", "Anexos obrigatórios"];
const GD_PRAZO = 15;
const gdDias = (a, b = hojeISO())=> Math.round((new Date(b + "T12:00:00") - new Date(a + "T12:00:00")) / 86400000);
const gdSomar = (iso, n)=>{ const d = new Date(iso + "T12:00:00"); d.setDate(d.getDate() + n); return d.toISOString().slice(0, 10); };
// RN02: número único de autuação no formato YYYY.NNNN-SD
const gdNumero = (ano, seq)=> `${ano}.${String(seq).padStart(4, "0")}-SD`;
teste("RN02: número no formato YYYY.NNNN-SD", ()=> gdNumero(2026, 7) === "2026.0007-SD");

// RN06/RN07: percentual decorrido e o sinal visual
function gdPrazo(p, hoje = hojeISO()){
  const dias = Number(p.dias_prazo || GD_PRAZO), decorridos = gdDias(p.data_autuacao, hoje);
  const pct = dias ? Math.round(decorridos / dias * 100) : 0;
  const sinal = p.status === "concluido" ? "concluido" : pct >= 100 ? "vermelho" : pct >= 70 ? "amarelo" : "verde";
  return {dias, decorridos, pct, sinal, limite: gdSomar(p.data_autuacao, dias)};
}
teste("RN06/RN07: 60% verde, 80% amarelo, 110% vermelho", ()=>{
  const base = {data_autuacao: "2026-10-01", dias_prazo: 10, status: "em andamento"};
  return gdPrazo(base, "2026-10-07").sinal === "verde" && gdPrazo(base, "2026-10-09").sinal === "amarelo" && gdPrazo(base, "2026-10-12").sinal === "vermelho";
});
teste("Concluído não entra no sinal", ()=> gdPrazo({data_autuacao: "2026-01-01", dias_prazo: 10, status: "concluido"}).sinal === "concluido");
teste("Exemplo com 12 processos", ()=> dadosEmbutidos("seed").processos.length === 12);

const GD_SINAL = {verde: "No prazo", amarelo: "Atenção (70% do prazo)", vermelho: "Vencido", concluido: "Concluído"};
const gdSelo = s => s === "vermelho" ? "erro" : s === "amarelo" ? "alerta" : s === "concluido" ? "info" : "ok";

async function gdUsuarios(){ return Object.fromEntries((await db.list("usuarios")).map(u=>[u.id_usuario, u])); }

TELAS["#/painel"] = async ()=>{
  const ps = (await db.list("processos")).filter(p=>p.status !== "arquivado"), us = await gdUsuarios();
  const hoje = hojeISO(), infos = ps.map(p=>({p, ...gdPrazo(p, hoje)}));
  const por = s => infos.filter(x=>x.sinal === s);
  return `<h1>Painel do Gabinete</h1><p class="sub">${ps.length} processos em acompanhamento. <a href="#/processo/novo">Cadastrar processo</a></p>
    <div class="grade"><div class="card kpi"><div class="v" data-vencidos>${por("vermelho").length}</div><div class="r">vencidos</div></div>
      <div class="card kpi"><div class="v" data-amarelos>${por("amarelo").length}</div><div class="r">em atenção (70% do prazo)</div></div>
      <div class="card kpi"><div class="v">${por("verde").length}</div><div class="r">no prazo</div></div>
      <div class="card kpi"><div class="v">${por("concluido").length}</div><div class="r">concluídos</div></div></div>
    <div class="card tabela-wrap"><h2 style="margin-top:0">Mesa virtual</h2><table><tr><th>Processo</th><th>Assunto</th><th>Responsável</th><th>Limite</th><th class="num">Decorrido</th><th>Sinal</th></tr>
      ${infos.sort((a, b)=>b.pct - a.pct).map(x=>`<tr><td><a href="#/processo/${encodeURIComponent(x.p.id_processo)}">${esc(x.p.numero_processo)}</a></td>
        <td>${esc(x.p.assunto)}</td><td>${esc(us[x.p.responsavel]?.nome || x.p.responsavel || "—")}</td><td>${dataCurtaBR(x.limite)}</td>
        <td class="num">${x.pct}%</td><td><span class="selo ${gdSelo(x.sinal)}">${esc(GD_SINAL[x.sinal])}</span></td></tr>`).join("")}</table></div>`;
};

function gdFiltros(){ return estado.gdFiltros || (estado.gdFiltros = {sinal: "", status: "", busca: ""}); }
TELAS["#/processos"] = async ()=>{
  const f = gdFiltros(), ps = await db.list("processos"), us = await gdUsuarios(), hoje = hojeISO(), b = normalizar(f.busca);
  const lista = ps.map(p=>({p, ...gdPrazo(p, hoje), resp: us[p.responsavel]?.nome || p.responsavel || ""}))
    .filter(x=>(!f.sinal || x.sinal === f.sinal) && (!f.status || x.p.status === f.status)
      && (!b || normalizar(`${x.p.numero_processo} ${x.p.assunto} ${x.p.requerente} ${x.resp}`).includes(b)))
    .sort((a, b2)=>b2.pct - a.pct);
  return `<h1>Processos <span class="sub">(${lista.length})</span></h1><p class="sub"><a href="#/processo/novo">Cadastrar processo</a></p>
    <div class="card"><div class="campos">
      ${campo("gdBusca", "Busca por número, assunto ou requerente", {valor: f.busca})}
      ${campo("gdSinal", "Sinal do prazo", {tipo: "select", opcoes: [["", "Todos"], ...Object.entries(GD_SINAL)], valor: f.sinal})}
      ${campo("gdStatus", "Situação", {tipo: "select", opcoes: [["", "Todas"], ["em andamento", "Em andamento"], ["concluido", "Concluído"], ["arquivado", "Arquivado"]], valor: f.status})}</div></div>
    <div class="card tabela-wrap"><table><tr><th>Processo</th><th>Assunto</th><th>Requerente</th><th>Responsável</th><th>Limite</th><th>Sinal</th></tr>
      ${lista.map(x=>`<tr><td><a href="#/processo/${encodeURIComponent(x.p.id_processo)}">${esc(x.p.numero_processo)}</a></td><td>${esc(x.p.assunto)}</td>
        <td>${esc(x.p.requerente)}</td><td>${esc(x.resp || "—")}</td><td>${dataCurtaBR(x.limite)}</td>
        <td><span class="selo ${gdSelo(x.sinal)}">${esc(GD_SINAL[x.sinal])}</span></td></tr>`).join("")
        || '<tr><td colspan="6" class="vazio">Nenhum processo com estes filtros.</td></tr>'}</table></div>`;
};
TELAS_DEPOIS["#/processos"] = ()=>{
  const f = gdFiltros();
  [["gdBusca", "busca", "change"], ["gdSinal", "sinal", "input"], ["gdStatus", "status", "input"]].forEach(([id, k, ev])=>
    $("#" + id).addEventListener(ev, e=>{ f[k] = e.target.value; navegar(); }));
};

TELAS["#/processo/novo"] = async ()=>{
  const us = await db.list("usuarios");
  return `<h1>Cadastrar processo</h1><p class="sub">Todos os anexos obrigatórios precisam estar presentes (RN01). O número de autuação é gerado no formato AAAA.NNNN-SD (RN02).</p>
    <form class="card" id="formGdNovo" novalidate><div class="campos">
      ${campo("gdNumero", "Número do processo", {ajuda: "Deixe em branco para gerar automaticamente."})}
      ${campo("gdData", "Data de autuação", {tipo: "date", valor: hojeISO(), obrigatorio: true})}
      ${campo("gdPrazo", "Prazo (dias corridos)", {tipo: "number", valor: GD_PRAZO, attrs: 'min="1" step="1"', obrigatorio: true})}
      ${campo("gdResponsavel", "Responsável pela instrução", {tipo: "select", opcoes: [["", "Escolha"], ...us.map(u=>[u.id_usuario, u.nome])]})}</div>
    ${campo("gdAssunto", "Assunto", {obrigatorio: true})}
    <div class="campos">${campo("gdRequerente", "Requerente (nome fictício)", {obrigatorio: true})}${campo("gdLotacao", "Lotação de destino", {obrigatorio: true})}</div>
    <fieldset class="card"><legend><b>Anexos obrigatórios (RN01)</b></legend>
      ${GD_ANEXOS.map((a, i)=>`<label style="display:flex;gap:8px;align-items:center;margin:6px 0"><input type="checkbox" class="gdAnexo" id="gdAnexo${i}" style="width:auto"> <span>${esc(a)}</span></label>`).join("")}</fieldset>
    <div id="gdErros"></div><div class="linha-botoes"><button class="prim" type="submit">Autuar processo</button></div></form>`;
};
TELAS_DEPOIS["#/processo/novo"] = ()=>{
  $("#formGdNovo").addEventListener("submit", async e=>{
    e.preventDefault();
    const ps = await db.list("processos"), ano = (valorDe("gdData") || hojeISO()).slice(0, 4);
    const d = {numero_processo: valorDe("gdNumero") || gdNumero(ano, ps.length + 1), assunto: valorDe("gdAssunto"), requerente: valorDe("gdRequerente"),
      lotacao: valorDe("gdLotacao"), data_autuacao: valorDe("gdData"), dias_prazo: Number(valorDe("gdPrazo")), responsavel: valorDe("gdResponsavel")};
    const anexos = GD_ANEXOS.filter((_, i)=>$("#gdAnexo" + i).checked), erros = [];
    if (!d.assunto) erros.push("Informe o assunto.");
    if (!d.requerente) erros.push("Informe o requerente.");
    if (!d.lotacao) erros.push("Informe a lotação de destino.");
    if (!d.data_autuacao || d.data_autuacao > hojeISO()) erros.push("Informe a data de autuação (não pode ser futura).");
    if (!(d.dias_prazo > 0)) erros.push("O prazo precisa ser de pelo menos 1 dia.");
    if (anexos.length < GD_ANEXOS.length) erros.push(`Faltam anexos obrigatórios: ${GD_ANEXOS.filter(a=>!anexos.includes(a)).join(", ")} (RN01).`);
    if (ps.some(p=>normalizar(p.numero_processo) === normalizar(d.numero_processo))) erros.push("Este número de processo já está cadastrado.");
    if (d.responsavel && normalizar(d.responsavel) === normalizar(d.requerente)) erros.push("O requerente não pode ser o responsável pela instrução (RN05).");
    if (!mostrarErros("#gdErros", erros)) return;
    const id = "PR-" + String(ps.length + 1).padStart(4, "0");
    await db.put("processos", {id_processo: id, ...d, anexos, status: "em andamento", criado_em: agora()});
    for (const a of anexos) await db.put("documentos", {id_documento: uuid(), processo_id: id, tipo_documento: a, data_criacao: agora(), assinado: false});
    await db.put("log", {id: uuid(), processo_id: id, tipo_evento: "autuação", descricao: `${d.numero_processo} · ${d.assunto}`, perfil: estado.perfil || "", data_hora: agora()});
    await registrar("processo autuado", {detalhe: d.numero_processo});
    toast(`Processo ${d.numero_processo} autuado.`); location.hash = "#/processo/" + encodeURIComponent(id);
  });
};

TELAS["#/processo/:id"] = async ({id})=>{
  const p = await db.get("processos", id);
  if (!p) return `<div class="card vazio">Processo não encontrado. <a href="#/processos">Voltar</a></div>`;
  const us = await gdUsuarios(), pr = gdPrazo(p), docs = await db.porIndice("documentos", "processo_id", id);
  const ls = (await db.porIndice("log", "processo_id", id)).sort((a, b)=>b.data_hora.localeCompare(a.data_hora));
  return `<h1>${esc(p.numero_processo)} <span class="selo ${gdSelo(pr.sinal)}" id="gdSinalAtual">${esc(GD_SINAL[pr.sinal])}</span></h1>
    <p class="sub">${esc(p.assunto)} · autuado em ${dataCurtaBR(p.data_autuacao)} · prazo de ${pr.dias} dias</p>
    <div class="grade"><div class="card kpi"><div class="v" id="gdPct">${pr.pct}%</div><div class="r">do prazo decorrido</div></div>
      <div class="card kpi"><div class="v">${dataCurtaBR(pr.limite)}</div><div class="r">data limite</div></div>
      <div class="card kpi"><div class="v">${esc(us[p.responsavel]?.nome || p.responsavel || "—")}</div><div class="r">responsável pela instrução</div></div></div>
    <div class="card"><h2 style="margin-top:0">Dados</h2><p>Requerente: ${esc(p.requerente)} · Lotação: ${esc(p.lotacao)} · Situação: <b>${esc(p.status)}</b></p>
      <h2>Documentos</h2><ul>${docs.map(d=>`<li>${esc(d.tipo_documento)} · ${dataCurtaBR(d.data_criacao)} · ${d.assinado ? "assinado" : "sem assinatura"}</li>`).join("") || '<li class="sub">Nenhum.</li>'}</ul></div>
    <div class="card tabela-wrap"><h2 style="margin-top:0">Histórico</h2><table><tr><th>Data e hora</th><th>Evento</th><th>Descrição</th></tr>
      ${ls.map(x=>`<tr><td>${dataBR(x.data_hora)}</td><td>${esc(x.tipo_evento)}</td><td>${esc(x.descricao)}</td></tr>`).join("")}</table></div>`;
};
