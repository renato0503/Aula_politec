/* Renovação de Contratos · código do app (Sprints 1 e 2) */
"use strict";
const RC_FAIXAS = [
  {id: "normal", rotulo: "Normal", de: 121, ate: Infinity, selo: "ok"},
  {id: "acompanhamento", rotulo: "Acompanhamento (91 a 120 dias)", de: 91, ate: 120, selo: "info"},
  {id: "atencao", rotulo: "Atenção (61 a 90 dias)", de: 61, ate: 90, selo: "alerta"},
  {id: "providencias", rotulo: "Providências (31 a 60 dias)", de: 31, ate: 60, selo: "alerta"},
  {id: "urgente", rotulo: "Urgente (0 a 30 dias)", de: 0, ate: 30, selo: "erro"},
  {id: "vencido", rotulo: "Vencido", de: -Infinity, ate: -1, selo: "erro"},
];
const RC_FORA = ["Encerrado", "Rescindido", "Expirado"];
const rcDias = (iso, hoje = hojeISO())=> Math.round((new Date(iso + "T12:00:00") - new Date(hoje + "T12:00:00")) / 86400000);
// R3: semáforo de seis faixas; encerrado, rescindido e expirado saem da contagem
function rcFaixa(c, hoje = hojeISO()){
  if (RC_FORA.includes(c.status)) return null;
  const d = rcDias(c.data_fim, hoje);
  return RC_FAIXAS.find(f=>d >= f.de && d <= f.ate);
}
teste("Semáforo: 130 normal, 100 acompanhamento, 75 atenção, 45 providências, 10 urgente, -2 vencido", ()=>{
  const base = {data_inicio: "2020-01-01", status: "Vigente"}, hoje = "2026-10-29", fim = n => { const d = new Date("2026-10-29T12:00:00"); d.setDate(d.getDate() + n); return d.toISOString().slice(0, 10); };
  return [130, 100, 75, 45, 10, -2].map(n=>rcFaixa({...base, data_fim: fim(n)}, hoje).id).join() === "normal,acompanhamento,atencao,providencias,urgente,vencido";
});
teste("Contrato encerrado não entra no semáforo", ()=> rcFaixa({data_fim: "2026-12-01", status: "Encerrado"}) === null);
teste("Exemplo com 15 contratos", ()=> dadosEmbutidos("seed").contratos.length === 15);

// R2: data_fim = data_inicio + vigencia_meses (dia preservado, ajustado ao fim do mês)
function rcFim(dataInicio, meses){
  const d = new Date(dataInicio + "T12:00:00"), dia = d.getDate();
  d.setDate(1); d.setMonth(d.getMonth() + Number(meses));
  const ultimo = new Date(d.getFullYear(), d.getMonth() + 1, 0).getDate();
  d.setDate(Math.min(dia, ultimo));
  return d.toISOString().slice(0, 10);
}
teste("R2: 31/01 + 1 mês vira 28/02 (2027)", ()=> rcFim("2027-01-31", 1) === "2027-02-28" && rcFim("2026-08-15", 12) === "2027-08-15");

async function rcAuditar(contrato_id, acao, detalhe){
  await db.put("auditoria", {id_evento: uuid(), contrato_id, acao, detalhe: detalhe || "", perfil: estado.perfil || "sistema", data_hora: agora()});
}

TELAS["#/painel"] = async ()=>{
  const cs = await db.list("contratos"), hoje = hojeISO();
  const ativos = cs.filter(c=>!RC_FORA.includes(c.status));
  const porFaixa = Object.fromEntries(RC_FAIXAS.map(f=>[f.id, ativos.filter(c=>rcFaixa(c, hoje)?.id === f.id)]));
  const vencendo = ativos.filter(c=>{ const d = rcDias(c.data_fim, hoje); return d >= 0 && d <= 90; });
  return `<h1>Painel de Contratos</h1><p class="sub">${ativos.length} contratos na contagem regressiva. <a href="#/contrato/novo">Cadastrar contrato</a></p>
    <div class="grade"><div class="card kpi"><div class="v" data-vencendo90>${vencendo.length}</div><div class="r">vencendo em até 90 dias</div></div>
      <div class="card kpi"><div class="v">${porFaixa.urgente.length}</div><div class="r">urgentes (0 a 30 dias)</div></div>
      <div class="card kpi"><div class="v">${porFaixa.vencido.length}</div><div class="r">vencidos</div></div>
      <div class="card kpi"><div class="v">${cs.length - ativos.length}</div><div class="r">fora da contagem</div></div></div>
    <div class="card tabela-wrap"><h2 style="margin-top:0">Semáforo (R3)</h2><table id="tabelaFaixas"><tr><th>Faixa</th><th class="num">Contratos</th><th class="num">Valor</th></tr>
      ${RC_FAIXAS.map(f=>`<tr><td><span class="selo ${f.selo}">${esc(f.rotulo)}</span></td><td class="num">${porFaixa[f.id].length}</td>
        <td class="num">${dinheiro.fmt(porFaixa[f.id].reduce((a, c)=>a + Number(c.valor_c || 0), 0))}</td></tr>`).join("")}</table></div>
    <div class="card tabela-wrap"><h2 style="margin-top:0">Próximos do vencimento</h2><table><tr><th>Contrato</th><th>Fornecedor</th><th>Término</th><th class="num">Dias</th><th>Faixa</th></tr>
      ${vencendo.sort((a, b)=>a.data_fim.localeCompare(b.data_fim)).map(c=>{ const f = rcFaixa(c); return `<tr><td><a href="#/contrato/${encodeURIComponent(c.id_contrato)}">${esc(c.numero)}</a></td>
        <td>${esc(c.fornecedor)}</td><td>${dataCurtaBR(c.data_fim)}</td><td class="num">${rcDias(c.data_fim)}</td><td><span class="selo ${f.selo}">${esc(f.rotulo.split(" (")[0])}</span></td></tr>`; }).join("")
        || '<tr><td colspan="5" class="vazio">Nenhum contrato vence nos próximos 90 dias.</td></tr>'}</table></div>`;
};

function rcFiltros(){ return estado.rcFiltros || (estado.rcFiltros = {faixa: "", status: "", busca: ""}); }
TELAS["#/contratos"] = async ()=>{
  const f = rcFiltros(), cs = await db.list("contratos"), b = normalizar(f.busca);
  const lista = cs.filter(c=>{
    const faixa = rcFaixa(c)?.id || "fora";
    return (!f.faixa || faixa === f.faixa) && (!f.status || c.status === f.status) && (!b || normalizar(`${c.numero} ${c.objeto} ${c.fornecedor}`).includes(b));
  }).sort((a, b2)=>a.data_fim.localeCompare(b2.data_fim));
  return `<h1>Contratos <span class="sub">(${lista.length})</span></h1><p class="sub"><a href="#/contrato/novo">Cadastrar contrato</a></p>
    <div class="card"><div class="campos">
      ${campo("rcBusca", "Busca por número, objeto ou fornecedor", {valor: f.busca})}
      ${campo("rcFaixa", "Faixa do semáforo", {tipo: "select", opcoes: [["", "Todas"], ...RC_FAIXAS.map(x=>[x.id, x.rotulo]), ["fora", "Fora da contagem"]], valor: f.faixa})}
      ${campo("rcStatus", "Situação", {tipo: "select", opcoes: [["", "Todas"], ...["Vigente", ...RC_FORA].map(s=>[s, s])], valor: f.status})}</div></div>
    <div class="card tabela-wrap"><table><tr><th>Contrato</th><th>Fornecedor</th><th class="num">Valor</th><th>Término</th><th class="num">Dias</th><th>Situação</th></tr>
      ${lista.map(c=>{ const fx = rcFaixa(c); return `<tr><td><a href="#/contrato/${encodeURIComponent(c.id_contrato)}">${esc(c.numero)}</a></td><td>${esc(c.fornecedor)}</td>
        <td class="num">${dinheiro.fmt(Number(c.valor_c || 0))}</td><td>${dataCurtaBR(c.data_fim)}</td><td class="num">${rcDias(c.data_fim)}</td>
        <td>${fx ? `<span class="selo ${fx.selo}">${esc(fx.rotulo.split(" (")[0])}</span>` : `<span class="selo info">${esc(c.status)}</span>`}</td></tr>`; }).join("")
        || '<tr><td colspan="6" class="vazio">Nenhum contrato com estes filtros.</td></tr>'}</table></div>`;
};
TELAS_DEPOIS["#/contratos"] = ()=>{
  const f = rcFiltros();
  [["rcBusca", "busca", "change"], ["rcFaixa", "faixa", "input"], ["rcStatus", "status", "input"]].forEach(([id, k, ev])=>
    $("#" + id).addEventListener(ev, e=>{ f[k] = e.target.value; navegar(); }));
};

TELAS["#/contrato/novo"] = async ()=> `<h1>Cadastrar contrato</h1><p class="sub">A data de término é calculada pelos meses de vigência (R2) e pode ser ajustada.</p>
  <form class="card" id="formRcNovo" novalidate><div class="campos">
    ${campo("rcNumero", "Número do contrato", {obrigatorio: true})}
    ${campo("rcFornecedor", "Fornecedor", {obrigatorio: true})}
    ${campo("rcCnpj", "CNPJ", {obrigatorio: true, attrs: 'inputmode="numeric"'})}
    ${campo("rcValor", "Valor do contrato (R$)", {tipo: "number", attrs: 'min="0" step="0.01"'})}
    ${campo("rcInicio", "Data de início", {tipo: "date", valor: hojeISO(), obrigatorio: true})}
    ${campo("rcMeses", "Vigência (meses)", {tipo: "number", valor: 12, attrs: 'min="1" step="1"', obrigatorio: true})}
    ${campo("rcFim", "Data de término (calculada)", {tipo: "date", obrigatorio: true})}
    ${campo("rcProrroga", "Permite prorrogação? (R1)", {tipo: "select", opcoes: [["sim", "Sim"], ["nao", "Não"]]})}</div>
  ${campo("rcObjeto", "Objeto", {tipo: "textarea", linhas: 2, obrigatorio: true})}
  <div id="rcErros"></div><div class="linha-botoes"><button class="prim" type="submit">Cadastrar</button></div></form>`;
TELAS_DEPOIS["#/contrato/novo"] = ()=>{
  const calc = ()=>{ const i = valorDe("rcInicio"), m = valorDe("rcMeses"); if (i && m) $("#rcFim").value = rcFim(i, Number(m)); };
  $("#rcInicio").addEventListener("change", calc); $("#rcMeses").addEventListener("change", calc); calc();
  $("#formRcNovo").addEventListener("submit", async e=>{
    e.preventDefault();
    const cs = await db.list("contratos");
    const d = {numero: valorDe("rcNumero"), fornecedor: valorDe("rcFornecedor"), cnpj: valorDe("rcCnpj").replace(/\D/g, ""), valor_c: dinheiro.de(valorDe("rcValor")),
      data_inicio: valorDe("rcInicio"), vigencia_meses: Number(valorDe("rcMeses")), data_fim: valorDe("rcFim"), objeto: valorDe("rcObjeto"),
      permite_prorrogacao: valorDe("rcProrroga") === "sim", alerta_dias: 90, status: "Vigente"};
    const erros = [];
    if (!d.numero) erros.push("Informe o número do contrato.");
    else if (cs.some(c=>normalizar(c.numero) === normalizar(d.numero))) erros.push("Este contrato já está cadastrado.");
    if (!d.fornecedor) erros.push("Informe o fornecedor.");
    if (!cnpjValido(d.cnpj)) erros.push("CNPJ inválido.");
    if (!(d.vigencia_meses > 0)) erros.push("A vigência precisa ser de pelo menos 1 mês.");
    if (!d.data_inicio) erros.push("Informe a data de início.");
    if (!d.data_fim || d.data_fim <= d.data_inicio) erros.push("A data de término precisa ser depois do início.");
    if (!d.objeto) erros.push("Informe o objeto.");
    if (!mostrarErros("#rcErros", erros)) return;
    const id = "CT-" + String(cs.length + 1).padStart(3, "0");
    await db.put("contratos", {id_contrato: id, ...d, criado_em: agora()});
    await rcAuditar(id, "contrato cadastrado", `${d.numero} · término ${d.data_fim}`);
    await registrar("contrato cadastrado", {detalhe: d.numero});
    toast(`Contrato ${id} cadastrado.`); location.hash = "#/contrato/" + encodeURIComponent(id);
  });
};

TELAS["#/contrato/:id"] = async ({id})=>{
  const c = await db.get("contratos", id);
  if (!c) return `<div class="card vazio">Contrato não encontrado. <a href="#/contratos">Voltar</a></div>`;
  const fx = rcFaixa(c), adits = (await db.porIndice("aditivos", "contrato_id", id)).sort((a, b)=>b.data_assinatura.localeCompare(a.data_assinatura));
  const aud = (await db.porIndice("auditoria", "contrato_id", id)).sort((a, b)=>b.data_hora.localeCompare(a.data_hora));
  const pode = c.status === "Vigente" && c.permite_prorrogacao;
  return `<h1>${esc(c.numero)} ${fx ? `<span class="selo ${fx.selo}" id="rcFaixaAtual">${esc(fx.rotulo.split(" (")[0])}</span>` : `<span class="selo info">${esc(c.status)}</span>`}</h1>
    <p class="sub">${esc(c.fornecedor)} · ${esc(c.objeto)}</p>
    <div class="grade"><div class="card kpi"><div class="v">${dataCurtaBR(c.data_fim)}</div><div class="r">término da vigência</div></div>
      <div class="card kpi"><div class="v" id="rcDiasAtual">${rcDias(c.data_fim)}</div><div class="r">dias restantes</div></div>
      <div class="card kpi"><div class="v">${dinheiro.fmt(Number(c.valor_c || 0))}</div><div class="r">valor do contrato</div></div></div>
    <div class="card"><h2 style="margin-top:0">Dados</h2><p>Início: ${dataCurtaBR(c.data_inicio)} · Vigência: ${c.vigencia_meses} meses · CNPJ: ${esc(c.cnpj)}<br>
      Prorrogação: <b>${c.permite_prorrogacao ? "permitida" : "não permitida"}</b> · Situação: ${esc(c.status)}</p></div>
    ${pode ? `<form class="card" id="formRcAditivo"><h2 style="margin-top:0">Registrar termo aditivo de prorrogação</h2><div class="campos">
        ${campo("rcAditivo", "Número do aditivo", {obrigatorio: true})}
        ${campo("rcAssinatura", "Data de assinatura", {tipo: "date", valor: hojeISO(), obrigatorio: true})}
        ${campo("rcNovaVigencia", "Nova data de término", {tipo: "date", valor: rcFim(c.data_fim, 12), obrigatorio: true})}</div>
      ${campo("rcFundamento", "Fundamento legal", {valor: "Lei nº 14.133/2021, art. 107"})}
      <div id="rcErrosAditivo"></div><div class="linha-botoes"><button class="prim" type="submit">Registrar aditivo publicado</button></div></form>`
    : `<div class="card"><p class="sub">${c.status !== "Vigente" ? `Contrato ${esc(c.status)} não entra em renovação (R1).` : "Contrato sem permissão de prorrogação (R1): avaliar nova contratação."}</p></div>`}
    <div class="card tabela-wrap"><h2 style="margin-top:0">Termos aditivos (${adits.length})</h2><table><tr><th>Aditivo</th><th>Assinatura</th><th>Nova vigência</th><th>Fundamento</th></tr>
      ${adits.map(a=>`<tr><td>${esc(a.numero_aditivo)}</td><td>${dataCurtaBR(a.data_assinatura)}</td><td>${dataCurtaBR(a.nova_vigencia)}</td><td>${esc(a.fundamento || "")}</td></tr>`).join("")
        || '<tr><td colspan="4" class="vazio">Nenhum aditivo.</td></tr>'}</table></div>
    <div class="card tabela-wrap"><h2 style="margin-top:0">Trilha de auditoria (R6)</h2><table id="tabelaAuditoria"><tr><th>Data e hora</th><th>Perfil</th><th>Ação</th><th>Detalhe</th></tr>
      ${aud.map(a=>`<tr><td>${dataBR(a.data_hora)}</td><td>${esc(a.perfil)}</td><td>${esc(a.acao)}</td><td>${esc(a.detalhe)}</td></tr>`).join("")}</table></div>`;
};
TELAS_DEPOIS["#/contrato/:id"] = ({id})=>{
  $("#formRcAditivo")?.addEventListener("submit", async e=>{
    e.preventDefault();
    const c = await db.get("contratos", id), d = {numero_aditivo: valorDe("rcAditivo"), data_assinatura: valorDe("rcAssinatura"),
      nova_vigencia: valorDe("rcNovaVigencia"), fundamento: valorDe("rcFundamento")};
    const erros = [];
    if (!d.numero_aditivo) erros.push("Informe o número do aditivo.");
    if (!d.data_assinatura || d.data_assinatura > hojeISO()) erros.push("A data de assinatura não pode ser futura.");
    if (!d.nova_vigencia || d.nova_vigencia <= c.data_fim) erros.push("A nova vigência precisa ser depois do término atual.");
    if (!mostrarErros("#rcErrosAditivo", erros)) return;
    await db.put("aditivos", {id_aditivo: uuid(), contrato_id: id, ...d, status: "Publicado", criado_em: agora()});
    await db.put("contratos", {...c, data_fim: d.nova_vigencia, status: "Vigente"});
    await rcAuditar(id, "aditivo publicado", `${d.numero_aditivo} · nova vigência ${d.nova_vigencia}`);
    await registrar("aditivo registrado", {detalhe: `${c.numero} · ${d.numero_aditivo}`});
    toast("Aditivo registrado e vigência atualizada."); navegar();
  });
};
