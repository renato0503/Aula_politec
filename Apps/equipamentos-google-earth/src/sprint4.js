/* ================= Sprints 4, 5, 7, 8 e 9 · contratos, paradas, painel, exportação e importação ================= */
"use strict";

/* ---------- motor de cálculo (RN01 a RN07) ---------- */
function diasUteis(ini, fim){  // dias de segunda a sexta entre as datas
  if (!ini || !fim) return 0;
  let d = new Date(ini + "T00:00:00"), f = new Date(fim + "T00:00:00"), n = 0;
  if (f < d) return 0;
  while (d <= f){ const ds = d.getDay(); if (ds !== 0 && ds !== 6) n++; d.setDate(d.getDate() + 1); }
  return n;
}
const dataDe = iso=> iso ? String(iso).slice(0, 10) : "";
teste("dias úteis entre duas datas", ()=> diasUteis("2026-01-05", "2026-01-09") === 5);
teste("dias úteis de um fim de semana é zero", ()=> diasUteis("2026-01-10", "2026-01-11") === 0);

async function parametros(){
  const ps = await db.list("parametros");
  const valor = (chave, padrao)=>{ const p = ps.find(x=> x.chave === chave); return p && p.valor !== null && p.valor !== undefined ? Number(p.valor) : padrao; };
  return {valorRef: valor("valor_referencia_atendimento", 0), custoAlt: valor("custo_alternativo_padrao_dia", 0), ps};
}
async function baseDeCalculo(){
  const [eqs, unis, dirs, contratos, manut, paradas, params] = await Promise.all([
    db.list("equipamentos"), db.list("unidades"), db.list("diretorias"), db.list("contratos"),
    db.list("manutencoes"), db.list("paradas"), parametros()]);
  const hoje = hojeISO();
  const uniPorId = Object.fromEntries(unis.map(u=> [u.id, u]));
  const dirPorId = Object.fromEntries(dirs.map(d=> [d.id, d]));
  const eqPorId = Object.fromEntries(eqs.map(e=> [e.id, e]));
  // RN05: contrato vigente quando início <= hoje <= fim
  const contratoDe = e=> contratos.find(c=> (c.equipamento_ids || []).includes(e.id) || c.id === e.contrato_id);
  const vigente = c=> !!c && dataDe(c.inicio) <= hoje && hoje <= dataDe(c.fim);
  const manutPorEq = {}, paradasPorEq = {};
  for (const m of manut) (manutPorEq[m.equipamento_id] = manutPorEq[m.equipamento_id] || []).push(m);
  for (const p of paradas) (paradasPorEq[p.equipamento_id] = paradasPorEq[p.equipamento_id] || []).push(p);
  const custoDiario = (e, p)=>{
    const u = uniPorId[e.unidade_id] || {};
    const perdidos = p && p.atendimentos_perdidos_dia !== null && p.atendimentos_perdidos_dia !== undefined ? Number(p.atendimentos_perdidos_dia) : Number(u.atendimentos_dia || 0);
    const alternativo = p && p.custo_alternativo_dia !== null && p.custo_alternativo_dia !== undefined ? Number(p.custo_alternativo_dia) : params.custoAlt;
    return perdidos * params.valorRef + alternativo;
  };
  const custoParada = (p)=>{
    const e = eqPorId[p.equipamento_id] || {};
    const fim = p.fim ? dataDe(p.fim) : hoje;
    const dias = diasUteis(dataDe(p.inicio), fim);
    return custoDiario(e, p) * dias;
  };
  const calc = eqs.filter(e=> !e.excluido).map(e=>{
    const u = uniPorId[e.unidade_id] || {}, d = dirPorId[u.diretoria_id] || {};
    const contrato = contratoDe(e), temContrato = vigente(contrato);
    const pontos = Number(e.criticidade) >= 4 && !e.tem_redundancia;   // RN01
    const minhasParadas = paradasPorEq[e.id] || [];
    const abertas = minhasParadas.filter(p=> !p.fim);
    const custoParadas = minhasParadas.reduce((a, p)=>a + custoParada(p), 0);
    const horasParadas = minhasParadas.reduce((a, p)=> a + (diasUteis(dataDe(p.inicio), p.fim ? dataDe(p.fim) : hoje) * Number(u.horas_uteis_dia || 8)), 0);
    const corretivas = (manutPorEq[e.id] || []).filter(m=> m.tipo === "corretiva" && m.abertura && m.conclusao);
    const mttr = corretivas.length ? Math.round(corretivas.reduce((a, m)=>a + (new Date(m.conclusao) - new Date(m.abertura)) / 86400000, 0) / corretivas.length) : null;
    const diasPeriodo = diasUteis(hoje, hoje);
    const horasUtilesPeriodo = diasPeriodo * Number(u.horas_uteis_dia || 8);
    const disponibilidade = horasUtilesPeriodo ? Math.max(0, 1 - horasParadas / horasUtilesPeriodo) : null;
    // RN04: risco = criticidade x 2 (sem contrato) x 2 (ponto único de falha)
    const risco = Number(e.criticidade) * (temContrato ? 1 : 2) * (pontos ? 2 : 1);
    const diasParaFim = contrato ? Math.round((new Date(dataDe(contrato.fim) + "T00:00:00") - new Date(hoje + "T00:00:00")) / 86400000) : null;
    return {...e, unidade:u, diretoria:d, contrato, temContrato, pontoUnico:pontos, risco,
      custoDiario:custoDiario(e, null), custoParadas, horasParadas, mttr, disponibilidade,
      paradas:minhasParadas, abertas:abertas.length, manutencoes:manutPorEq[e.id] || [],
      diasParaFim, vencendo: diasParaFim !== null && diasParaFim >= 0 && diasParaFim <= 60};
  });
  return {eqs:calc, unis, dirs, contratos, manut, paradas, params, uniPorId, dirPorId};
}
const cardKpiEq = (v, r, id)=> `<div class="card kpi"${id ? ` id="${id}"` : ""}><div class="v">${v}</div><div class="r">${esc(r)}</div></div>`;

/* ================= Sprint 4 · Contratos e manutenções ================= */
TELAS["#/contratos"] = async ()=>{
  const b = await baseDeCalculo();
  const linhas = b.contratos.map(c=>{
    const eqs = b.eqs.filter(e=> (c.equipamento_ids || []).includes(e.id) || e.contrato_id === c.id);
    const semContrato = eqs.filter(e=> !e.temContrato).length;
    const fim = dataDe(c.fim), hoje = hojeISO();
    const vencido = fim < hoje, vencendo = !vencido && fim <= new Date(Date.now() + 60 * 86400000).toISOString().slice(0, 10);
    return {c, eqs, semContrato, vencido, vencendo, dias: Math.round((new Date(fim + "T00:00:00") - new Date(hoje + "T00:00:00")) / 86400000)};
  }).sort((a, x)=> a.dias - x.dias);
  const vencendo = linhas.filter(l=> l.vencendo), vencidos = linhas.filter(l=> l.vencido);
  const linha = l=> `<tr><td><b>${esc(l.c.numero)}</b></td><td>${esc(l.c.fornecedor)}</td><td>${dataCurtaBR(l.c.inicio)} a ${dataCurtaBR(l.c.fim)}</td>
    <td class="num">${dinheiro.fmt(Math.round((l.c.valor_mensal || 0) * 100))}</td><td class="num">${l.c.sla_horas ?? "—"} h</td>
    <td class="num">${l.eqs.length}</td>
    <td>${l.vencido ? '<span class="selo erro">vencido</span>' : l.vencendo ? `<span class="selo alerta">vence em ${l.dias} dias</span>` : '<span class="selo ok">vigente</span>'}</td>
    <td><button data-contrato="${esc(l.c.id)}">Abrir</button></td></tr>`;
  return `<h1>Contratos</h1><p class="sub">Cobertura e vencimento. Contrato vigente é o que está entre o início e o fim (RN05); o alerta aparece 60 dias antes.</p>
    <div class="grade">${cardKpiEq(b.contratos.length, "contratos")}${cardKpiEq(vencendo.length, "vencendo em 60 dias")}
      ${cardKpiEq(vencidos.length, "vencidos")}${cardKpiEq(b.eqs.filter(e=> !e.temContrato).length, "equipamentos sem contrato")}</div>
    ${vencendo.length ? `<div class="card pendente"><b>${vencendo.length} contrato(s) vencem em até 60 dias.</b> ${vencendo.map(l=> esc(l.c.numero)).join(", ")}.</div>` : ""}
    <div class="card tabela-wrap"><table><tr><th>Número</th><th>Fornecedor</th><th>Vigência</th><th class="num">Valor mensal</th><th class="num">SLA</th>
      <th class="num">Equipamentos</th><th>Situação</th><th></th></tr>${linhas.map(linha).join("")}</table></div>
    <form class="card" id="formContrato"><h2 style="margin-top:0">Novo contrato</h2><div class="campos">
      ${campo("ctNumero", "Número", {obrigatorio:true})}${campo("ctFornecedor", "Fornecedor", {obrigatorio:true})}
      ${campo("ctObjeto", "Objeto", {obrigatorio:true})}${campo("ctInicio", "Início da vigência", {tipo:"date", obrigatorio:true})}
      ${campo("ctFim", "Fim da vigência", {tipo:"date", obrigatorio:true})}${campo("ctValor", "Valor mensal (R$)", {attrs:'inputmode="decimal"'})}
      ${campo("ctSla", "SLA (horas)", {tipo:"number", attrs:'min="1"'})}</div>
      <div id="errosContrato"></div><div class="linha-botoes"><button class="prim" type="submit">Salvar contrato</button></div></form>
    <div id="detalheContrato"></div>`;
};
TELAS_DEPOIS["#/contratos"] = async ()=>{
  $("#formContrato")?.addEventListener("submit", async ev=>{
    ev.preventDefault();
    const d = {numero:valorDe("ctNumero"), fornecedor:valorDe("ctFornecedor"), objeto:valorDe("ctObjeto"),
      inicio:valorDe("ctInicio"), fim:valorDe("ctFim"),
      valor_mensal: valorDe("ctValor") ? (dinheiro.de(valorDe("ctValor")) || 0) / 100 : 0,
      sla_horas: Number(valorDe("ctSla")) || null};
    const erros = [];
    if (!d.numero) erros.push("Informe o número.");
    if (!d.fornecedor) erros.push("Informe o fornecedor.");
    if (!d.inicio || !d.fim || d.fim < d.inicio) erros.push("O fim da vigência deve ser depois do início.");
    if (!mostrarErros("#errosContrato", erros)) return;
    const reg = await novoRegistro({...d, equipamento_ids:[]});
    await db.put("contratos", reg); await registrar("contrato criado", {detalhe:d.numero});
    toast("Contrato salvo."); navegar();
  });
  $$("[data-contrato]").forEach(b=> b.addEventListener("click", async ()=>{
    const c = await db.get("contratos", b.dataset.contrato);
    const b2 = await baseDeCalculo();
    const eqs = b2.eqs.filter(e=> (c.equipamento_ids || []).includes(e.id) || e.contrato_id === c.id);
    $("#detalheContrato").innerHTML = `<div class="card"><h2 style="margin-top:0">${esc(c.numero)} · ${esc(c.fornecedor)}</h2>
      <p class="sub">${esc(c.objeto || "")} · vigência ${dataCurtaBR(c.inicio)} a ${dataCurtaBR(c.fim)} · SLA ${c.sla_horas ?? "—"} h</p>
      <div class="tabela-wrap"><table><tr><th>Patrimônio</th><th>Equipamento</th><th>Unidade</th><th>Situação</th><th class="num">Risco</th></tr>
        ${eqs.map(e=> `<tr><td>${esc(e.patrimonio)}</td><td>${esc(e.nome)}</td><td>${esc(e.unidade.nome || "")}</td>
          <td>${e.temContrato ? '<span class="selo ok">coberto</span>' : '<span class="selo alerta">sem cobertura</span>'}</td><td class="num">${e.risco}</td></tr>`).join("")}</table></div></div>`;
    $("#detalheContrato").scrollIntoView({block:"nearest"});
  }));
};

/* ================= Sprint 5 · Paradas e custo (RN02, RN03) ================= */
TELAS["#/paradas"] = async ()=>{
  const b = await baseDeCalculo();
  const eqPorId = Object.fromEntries(b.eqs.map(e=> [e.id, e]));
  const abertas = b.paradas.filter(p=> !p.fim).map(p=> ({...p, eq: eqPorId[p.equipamento_id]}));
  const custoDe = p=>{
    const e = eqPorId[p.equipamento_id];
    if (!e) return 0;
    const perdidos = p.atendimentos_perdidos_dia ?? e.unidade.atendimentos_dia ?? 0;
    const alt = p.custo_alternativo_dia ?? b.params.custoAlt;
    const dias = diasUteis(dataDe(p.inicio), p.fim ? dataDe(p.fim) : hojeISO());
    return (perdidos * b.params.valorRef + alt) * dias;
  };
  const linha = p=>{
    const e = eqPorId[p.equipamento_id] || {};
    return `<tr><td>${esc(e.patrimonio || "—")}<br><span class="sub">${esc(e.nome || "")}</span></td>
      <td>${esc(e.unidade?.nome || "")}</td><td>${dataCurtaBR(p.inicio)}</td><td>${p.fim ? dataCurtaBR(p.fim) : '<span class="selo erro">aberta</span>'}</td>
      <td>${esc(p.motivo || "")}</td><td class="num">${dinheiro.fmt(Math.round(custoDe(p)))}</td>
      <td>${p.fim ? "" : `<button data-fechar="${esc(p.id)}">Fechar parada</button>`}</td></tr>`;
  };
  const custoAberto = abertas.reduce((a, p)=>a + custoDe(p), 0);
  return `<h1>Paradas</h1><p class="sub">Cada parada tem custo diário (RN02) e custo acumulado em dias úteis (RN03). Parada aberta conta até hoje.</p>
    <div class="grade">${cardKpiEq(b.paradas.length, "paradas registradas")}${cardKpiEq(abertas.length, "paradas abertas")}
      ${cardKpiEq(dinheiro.fmt(Math.round(custoAberto)), "custo das abertas")}${cardKpiEq(dinheiro.fmt(Math.round(b.params.valorRef)), "valor por atendimento")}</div>
    <form class="card" id="formParada"><h2 style="margin-top:0">Abrir parada</h2><div class="campos">
      ${campo("paEq", "Equipamento", {tipo:"select", opcoes:[["", "Escolha"], ...b.eqs.map(e=> [e.id, `${e.patrimonio} · ${e.nome}`])], obrigatorio:true})}
      ${campo("paInicio", "Início", {tipo:"datetime-local", obrigatorio:true})}
      ${campo("paMotivo", "Motivo", {obrigatorio:true})}
      ${campo("paPerdidos", "Atendimentos perdidos por dia", {tipo:"number", attrs:'min="0"', ajuda:"Em branco, usa o valor da unidade."})}
      ${campo("paAlternativo", "Custo alternativo por dia (R$)", {attrs:'inputmode="decimal"', ajuda:"Em branco, usa o parâmetro da coordenadoria."})}</div>
      <div id="errosParada"></div><div class="linha-botoes"><button class="prim" type="submit">Abrir parada</button></div></form>
    <div class="card tabela-wrap"><h2>Paradas</h2><table><tr><th>Equipamento</th><th>Unidade</th><th>Início</th><th>Fim</th><th>Motivo</th><th class="num">Custo</th><th></th></tr>
      ${b.paradas.slice().sort((a, x)=> String(b.inicio).localeCompare(String(a.inicio))).map(linha).join("") || '<tr><td colspan="7" class="vazio">Nenhuma parada registrada.</td></tr>'}</table></div>`;
};
TELAS_DEPOIS["#/paradas"] = async ()=>{
  $("#formParada")?.addEventListener("submit", async ev=>{
    ev.preventDefault();
    const eqId = valorDe("paEq"), inicio = valorDe("paInicio"), motivo = valorDe("paMotivo");
    const erros = [];
    if (!eqId) erros.push("Escolha o equipamento.");
    if (!inicio) erros.push("Informe o início da parada.");
    if (!motivo) erros.push("Informe o motivo.");
    if (!mostrarErros("#errosParada", erros)) return;
    const reg = await novoRegistro({equipamento_id:eqId, inicio:inicio, fim:null, motivo,
      atendimentos_perdidos_dia: valorDe("paPerdidos") ? Number(valorDe("paPerdidos")) : null,
      custo_alternativo_dia: valorDe("paAlternativo") ? (dinheiro.de(valorDe("paAlternativo")) || 0) / 100 : null});
    await db.put("paradas", reg);
    const e = await db.get("equipamentos", eqId);
    if (e) await db.put("equipamentos", {...e, status:"parado", atualizadoEm:agora()});
    await registrar("parada aberta", {detalhe:eqId});
    toast("Parada aberta. O equipamento ficou parado.");
    navegar();
  });
  $$("[data-fechar]").forEach(b=> b.addEventListener("click", async ()=>{
    const p = await db.get("paradas", b.dataset.fechar);
    await db.put("paradas", {...p, fim:agora()});
    const e = await db.get("equipamentos", p.equipamento_id);
    if (e){
      const outras = (await db.porIndice("paradas", "equipamento_id", p.equipamento_id)).filter(x=> x.id !== p.id && !x.fim);
      if (!outras.length) await db.put("equipamentos", {...e, status:"operando", atualizadoEm:agora()});
    }
    await registrar("parada fechada", {detalhe:p.equipamento_id});
    toast("Parada fechada."); navegar();
  }));
};

/* ================= Sprint 7 · Painel de KPIs ================= */
TELAS["#/painel"] = async ()=>{
  const b = await baseDeCalculo();
  const dias = Number(estado.eqPeriodo || 90);
  const desde = new Date(Date.now() - dias * 86400000).toISOString().slice(0, 10);
  const noPeriodo = b.paradas.filter(p=> dataDe(p.inicio) >= desde);
  const custoDe = p=>{
    const e = b.eqs.find(x=> x.id === p.equipamento_id);
    if (!e) return 0;
    const perdidos = p.atendimentos_perdidos_dia ?? e.unidade.atendimentos_dia ?? 0;
    const alt = p.custo_alternativo_dia ?? b.params.custoAlt;
    return (perdidos * b.params.valorRef + alt) * diasUteis(dataDe(p.inicio), p.fim ? dataDe(p.fim) : hojeISO());
  };
  const custoParadas = noPeriodo.reduce((a, p)=>a + custoDe(p), 0);
  const semContrato = b.eqs.filter(e=> !e.temContrato);
  const pontos = b.eqs.filter(e=> e.pontoUnico);
  const semContratoPontos = pontos.filter(e=> !e.temContrato);
  const exposicao = semContratoPontos.reduce((a, e)=>a + e.custoDiario, 0);
  const manutPeriodo = b.manut.filter(m=> dataDe(m.abertura) >= desde);
  const gastoManut = manutPeriodo.reduce((a, m)=>a + (m.custo_rs || 0), 0);
  const comManut = b.eqs.filter(e=> e.mttr !== null);
  const mttrGeral = comManut.length ? Math.round(comManut.reduce((a, e)=>a + e.mttr, 0) / comManut.length) : 0;
  const disp = b.eqs.filter(e=> e.disponibilidade !== null);
  const dispGeral = disp.length ? disp.reduce((a, e)=>a + e.disponibilidade, 0) / disp.length : null;
  const porUnidade = {};
  for (const e of b.eqs){
    const k = e.unidade.nome || "sem unidade";
    porUnidade[k] = porUnidade[k] || {nome:k, custo:0, eqs:0, paradas:0};
    porUnidade[k].eqs++;
  }
  for (const p of noPeriodo){
    const e = b.eqs.find(x=> x.id === p.equipamento_id); if (!e) continue;
    const k = e.unidade.nome || "sem unidade";
    porUnidade[k].custo += custoDe(p); porUnidade[k].paradas++;
  }
  const ranking = Object.values(porUnidade).sort((a, x)=> x.custo - a.custo);
  const maxCusto = Math.max(1, ...ranking.map(r=> r.custo));
  const barras = ranking.map(r=> `<div class="eq-barra"><span class="eq-barra-nome">${esc(r.nome)}</span>
    <span class="eq-barra-trilho"><span class="eq-barra-fill" style="width:${(r.custo / maxCusto * 100).toFixed(1)}%"></span></span>
    <span class="eq-barra-valor">${dinheiro.fmt(Math.round(r.custo))}</span></div>`).join("");
  const linhaPonto = e=> `<tr><td><a href="#/equipamento/${encodeURIComponent(e.id)}">${esc(e.patrimonio)}</a></td><td>${esc(e.nome)}</td>
    <td>${esc(e.unidade.nome || "")}</td><td class="num">${e.criticidade}</td><td class="num">${dinheiro.fmt(Math.round(e.custoDiario))}</td>
    <td class="num">${e.risco}</td></tr>`;
  return `<h1>Painel</h1><p class="sub">Os 7 indicadores do projeto, no período escolhido. A exposição diária é o número da defesa: quanto se perde por dia se os pontos únicos de falha sem contrato pararem.</p>
    <div class="card"><div class="campos">${campo("eqPeriodo", "Período", {tipo:"select", opcoes:[["30","Últimos 30 dias"],["90","Últimos 90 dias"],["180","Últimos 180 dias"],["365","Último ano"]], valor:String(dias)})}</div></div>
    <div class="grade">
      ${cardKpiEq(b.eqs.length ? numBR(semContrato.length / b.eqs.length * 100, 1) + "%" : "0%", "equipamentos sem contrato", "kpiSemContrato")}
      ${cardKpiEq(pontos.length, "pontos únicos de falha", "kpiPontos")}
      ${cardKpiEq(dinheiro.fmt(Math.round(custoParadas)), "custo estimado de parada", "kpiCusto")}
      ${cardKpiEq(dinheiro.fmt(Math.round(exposicao)), "exposição diária", "kpiExposicao")}
      ${cardKpiEq(mttrGeral + " dias", "MTTR", "kpiMttr")}
      ${cardKpiEq(dispGeral === null ? "—" : numBR(dispGeral * 100, 1) + "%", "disponibilidade", "kpiDisp")}
      ${cardKpiEq(dinheiro.fmt(Math.round(gastoManut * 100)), "gasto com manutenção", "kpiGasto")}
    </div>
    <div class="card"><h2 style="margin-top:0">Custo de parada por unidade</h2>
      ${barras || '<p class="sub">Sem paradas no período.</p>'}</div>
    <div class="card tabela-wrap"><h2>Pontos únicos de falha sem contrato</h2>
      <table><tr><th>Patrimônio</th><th>Equipamento</th><th>Unidade</th><th class="num">Crit.</th><th class="num">Custo diário</th><th class="num">Risco</th></tr>
        ${semContratoPontos.map(linhaPonto).join("") || '<tr><td colspan="6" class="vazio">Nenhum ponto único de falha sem contrato.</td></tr>'}</table></div>
    <div class="card tabela-wrap"><h2>Unidades no período</h2>
      <table><tr><th>Unidade</th><th class="num">Equipamentos</th><th class="num">Paradas</th><th class="num">Custo</th></tr>
        ${ranking.map(r=> `<tr><td>${esc(r.nome)}</td><td class="num">${r.eqs}</td><td class="num">${r.paradas}</td><td class="num">${dinheiro.fmt(Math.round(r.custo))}</td></tr>`).join("")}</table></div>`;
};
TELAS_DEPOIS["#/painel"] = ()=>{
  $("#eqPeriodo")?.addEventListener("change", e=>{ estado.eqPeriodo = Number(e.target.value); navegar(); });
};

/* ================= Sprint 8 · Exportação para o Google Earth (.kml e .kmz) ================= */
function kmlDe(b, filtro){
  const dirs = b.dirs, porDir = {};
  for (const e of b.eqs){
    if (filtro && filtro(e) === false) continue;
    const sigla = e.diretoria.sigla || "SEM DIRETORIA";
    const unidade = e.unidade.nome || "sem unidade";
    (porDir[sigla] = porDir[sigla] || {})[unidade] = porDir[sigla][unidade] || [];
    porDir[sigla][unidade].push(e);
  }
  const esc2 = s=> String(s ?? "").replace(/[<>&]/g, c=> ({ "<":"&lt;", ">":"&gt;", "&":"&amp;" }[c]));
  let pasta = "";
  for (const [sigla, unidades] of Object.entries(porDir)){
    pasta += `<Folder><name>${esc2(sigla)}</name>`;
    for (const [unidade, eqs] of Object.entries(unidades)){
      pasta += `<Folder><name>${esc2(unidade)}</name>`;
      for (const e of eqs){
        const lat = e.latitude ?? e.unidade.latitude, lon = e.longitude ?? e.unidade.longitude;
        if (lat === null || lon === null) continue;
        const desc = [`Patrimônio: ${e.patrimonio}`, `Equipamento: ${e.nome}`, `Tipo: ${e.tipo}`, `Situação: ${e.status}`,
          `Contrato: ${e.temContrato ? e.contrato.numero : "sem contrato"}`, `Custo diário: ${dinheiro.fmt(Math.round(e.custoDiario))}`,
          `Risco: ${e.risco}`].join("<br/>");
        pasta += `<Placemark><name>${esc2(e.patrimonio)} - ${esc2(e.nome)}</name><description>${desc}</description>
          <Point><coordinates>${lon},${lat},0</coordinates></Point>
          <Style id="eq${e.temContrato ? "ok" : "erro"}"><IconStyle><color>${e.temContrato ? "ff00aa00" : "ff0000ff"}</color></IconStyle></Style></Placemark>`;
      }
      pasta += `</Folder>`;
    }
    pasta += `</Folder>`;
  }
  return `<?xml version="1.0" encoding="UTF-8"?>
<kml xmlns="http://www.opengis.net/kml/2.2"><Document><name>Equipamentos POLITEC</name>
<Style id="eqok"><IconStyle><color>ff00aa00</color></IconStyle></Style>
<Style id="eqerro"><IconStyle><color>ff0000ff</color></IconStyle></Style>
${pasta}</Document></kml>`;
}

TELAS["#/exportar"] = async ()=>{
  const b = await baseDeCalculo();
  const semContrato = b.eqs.filter(e=> !e.temContrato).length;
  return `<h1>Exportar</h1><p class="sub">O Google Earth lê o arquivo <span class="mono">.kmz</span>, que é o KML zipado com as miniaturas. As pastas seguem diretoria e unidade.</p>
    <div class="grade">${cardKpiEq(b.eqs.length, "equipamentos")}${cardKpiEq(b.unis.length, "unidades")}
      ${cardKpiEq(b.dirs.length, "diretorias")}${cardKpiEq(semContrato, "sem contrato")}</div>
    <div class="card"><h2 style="margin-top:0">Google Earth</h2>
      <div class="linha-botoes nao-imprimir"><button class="prim" id="btnKmz">Baixar .kmz (com miniaturas)</button>
        <button id="btnKml">Baixar .kml (só os dados)</button>
        <button id="btnKmzSemContrato">Baixar só os sem contrato</button></div>
      <p class="sub">O balão traz patrimônio, situação, contrato, custo diário e risco. A cor do ponto é verde com contrato e vermelho sem contrato.</p></div>
    <div class="card"><h2 style="margin-top:0">Outros arquivos</h2>
      <div class="linha-botoes nao-imprimir"><button id="btnJsonUnidade">Baixar o .json da base</button>
        <button id="btnCsvEquip">Baixar o CSV dos equipamentos</button>
        <button onclick="window.print()">Imprimir o relatório</button></div></div>
    <div class="card documento-a4"><div class="impressao-cab"><b>Mapa de Equipamentos</b><span>Relatório de ${dataBR(agora())}</span></div>
      <h2 style="margin-top:0">Resumo da base</h2>
      <p class="sub">${b.eqs.length} equipamentos · ${b.unis.length} unidades · ${b.contratos.length} contratos · ${b.paradas.length} paradas registradas.</p>
      <div class="tabela-wrap"><table><tr><th>Unidade</th><th class="num">Equipamentos</th><th class="num">Sem contrato</th><th class="num">Paradas abertas</th></tr>
        ${b.unis.map(u=>{ const eqs = b.eqs.filter(e=> e.unidade_id === u.id); return `<tr><td>${esc(u.nome)}</td><td class="num">${eqs.length}</td>
          <td class="num">${eqs.filter(e=> !e.temContrato).length}</td><td class="num">${eqs.filter(e=> e.abertas > 0).length}</td></tr>`;}).join("")}</table></div></div>`;
};
TELAS_DEPOIS["#/exportar"] = async ()=>{
  if (!$("#btnKmz")) return;
  const b = await baseDeCalculo();
  $("#btnKml").addEventListener("click", ()=>{
    baixar("equipamentos-politec.kml", kmlDe(b), "application/vnd.google-earth.kml+xml");
    registrar("KML exportado", {detalhe:"completo"});
  });
  const kmz = async (filtro, nome)=>{
    const zip = new JSZip();
    zip.file("doc.kml", kmlDe(b, filtro));
    const eqs = b.eqs.filter(e=> !filtro || filtro(e));
    for (const e of eqs){
      for (const fid of e.foto_ids || []){
        const arq = await db.get("arquivos", fid + "-mini");
        if (arq) zip.file(`fotos/${fid}.jpg`, arq.blob);
      }
    }
    const blob = await zip.generateAsync({type:"blob"});
    baixar(nome, blob, "application/vnd.google-earth.kmz");
    await registrar("KMZ exportado", {detalhe:nome, equipamentos:eqs.length});
    toast("Arquivo gerado: " + nome);
  };
  $("#btnKmz").addEventListener("click", ()=> kmz(null, "equipamentos-politec.kmz"));
  $("#btnKmzSemContrato").addEventListener("click", ()=> kmz(e=> !e.temContrato, "equipamentos-sem-contrato.kmz"));
  $("#btnJsonUnidade").addEventListener("click", async ()=>{
    const pacote = await db.exportar();
    baixar("mapa-equipamentos.json", JSON.stringify(pacote, null, 2), "application/json");
    await registrar("JSON da base exportado", {});
  });
  $("#btnCsvEquip").addEventListener("click", ()=>{
    const cols = ["patrimonio", "nome", "tipo", "unidade", "diretoria", "criticidade", "status", "contrato", "custo_diario", "risco"];
    const nomeU = Object.fromEntries(b.unis.map(u=> [u.id, u.nome]));
    const nomeD = Object.fromEntries(b.dirs.map(d=> [d.id, d.sigla]));
    const cel = v=> { const s = String(v ?? ""); return /[;"\n]/.test(s) ? `"${s.replace(/"/g, '""')}"` : s; };
    const linhas = b.eqs.map(e=> [e.patrimonio, e.nome, e.tipo, nomeU[e.unidade_id] || "", nomeD[e.unidade.diretoria_id] || "",
      e.criticidade, e.status, e.temContrato ? e.contrato.numero : "", (e.custoDiario || 0).toFixed(2).replace(".", ","), e.risco]);
    baixar("equipamentos.csv", "﻿" + [cols.join(";"), ...linhas.map(l=> l.map(cel).join(";"))].join("\n"), "text/csv;charset=utf-8");
  });
};

/* ================= Sprint 9 · Importação e consolidação (RN10) ================= */
TELAS["#/importar"] = async ()=>{
  const [unis, dirs] = await Promise.all([db.list("unidades"), db.list("diretorias")]);
  const contagem = {};
  for (const u of unis) contagem[u.id] = (await db.porIndice("equipamentos", "unidade_id", u.id)).length;
  return `<h1>Importar</h1><p class="sub">A planilha atual da coordenadoria entra por CSV, com associação de colunas. O arquivo <span class="mono">.json</span> de uma unidade é mesclado (RN10), com a tela de conflito para escolher a versão.</p>
    <div class="card"><h2 style="margin-top:0">Planilha de equipamentos</h2>
      <p class="sub">CSV com as colunas patrimônio, nome, tipo, unidade, criticidade e situação.</p>
      <label class="botao">Escolher CSV<input type="file" accept=".csv,text/csv" id="arqEqCsv" hidden></label>
      <div id="csvEqRelatorio"></div></div>
    <div class="card"><h2 style="margin-top:0">Arquivo de uma unidade</h2>
      <p class="sub">O <span class="mono">.json</span> exportado pela unidade, com os equipamentos e as paradas dela.</p>
      <label class="botao">Escolher .json da unidade<input type="file" accept=".json,application/json" id="arqUnidade" hidden></label>
      <div id="mergeRelatorio"></div></div>
    <div class="card"><h2 style="margin-top:0">Unidades desta cópia</h2>
      <div class="tabela-wrap"><table><tr><th>Unidade</th><th>Município</th><th class="num">Equipamentos</th></tr>
        ${unis.map(u=> `<tr><td>${esc(u.nome)}</td><td>${esc(u.municipio)}</td>
          <td class="num">${contagem[u.id]}</td></tr>`).join("")}</table></div></div>`;
};
TELAS_DEPOIS["#/importar"] = async ()=>{
  $("#arqEqCsv")?.addEventListener("change", async ev=>{
    const arq = ev.target.files[0]; if (!arq) return;
    const linhas = lerCSV(await lerArquivoTexto(arq));
    if (linhas.length < 2) return $("#csvEqRelatorio").innerHTML = `<div class="card pendente">O arquivo está vazio.</div>`;
    const cab = linhas[0].map(c=> normalizar(c));
    const achar = (...n)=> cab.findIndex(c=> n.some(x=> c.includes(x)));
    const col = {patrimonio:achar("patrim"), nome:achar("nome"), tipo:achar("tipo"), unidade:achar("unidade"),
      criticidade:achar("critic"), status:achar("situacao") || achar("status")};
    if (col.patrimonio < 0 || col.nome < 0){ return $("#csvEqRelatorio").innerHTML = `<div class="card pendente">Faltam as colunas de patrimônio e nome.</div>`; }
    const unis = (await db.list("unidades")).filter(u=>!u.excluido);
    const aceitas = [], recusadas = [];
    for (const l of linhas.slice(1)){
      const patrimonio = String(l[col.patrimonio] || "").trim(), nome = String(l[col.nome] || "").trim();
      if (!patrimonio || !nome){ recusadas.push({linha: l, motivo:"patrimônio ou nome vazio"}); continue; }
      const nomeUnidade = col.unidade >= 0 ? String(l[col.unidade] || "").trim() : "";
      const u = unis.find(x=> normalizar(x.nome) === normalizar(nomeUnidade)) || unis[0];
      if (!u){ recusadas.push({linha:l, motivo:"unidade não encontrada"}); continue; }
      const crit = col.criticidade >= 0 ? Number(l[col.criticidade]) : 3;
      if (!(crit >= 1 && crit <= 5)){ recusadas.push({linha:l, motivo:`criticidade ${l[col.criticidade]} fora de 1 a 5`}); continue; }
      const status = col.status >= 0 ? String(l[col.status] || "").trim() : "operando";
      aceitas.push({patrimonio, nome, tipo: col.tipo >= 0 ? String(l[col.tipo] || "").trim() : "", unidade_id:u.id,
        criticidade:crit, status:STATUS_EQ.includes(status) ? status : "operando", setor:"", fabricante:"", modelo:"", numero_serie:"",
        tem_redundancia:false, data_aquisicao:"", valor_aquisicao:null, contrato_id:null});
    }
    $("#csvEqRelatorio").innerHTML = `<div class="card"><p><b>${esc(arq.name)}</b>: ${aceitas.length} aceitas, ${recusadas.length} recusadas.</p>
      ${recusadas.length ? `<div class="tabela-wrap"><table><tr><th>Linha</th><th>Motivo</th></tr>
        ${recusadas.map(r=> `<tr><td>${recusadas.indexOf(r) + 2}</td><td>${esc(r.motivo)}</td></tr>`).join("")}</table></div>` : ""}
      <div class="linha-botoes nao-imprimir"><button class="prim" id="btnGravarCsv" ${aceitas.length ? "" : "disabled"}>Gravar ${aceitas.length} equipamentos</button></div></div>`;
    $("#btnGravarCsv")?.addEventListener("click", async ()=>{
      let novos = 0, atualizados = 0;
      for (const a of aceitas){
        const existentes = await db.porIndice("equipamentos", "patrimonio", a.patrimonio);
        if (existentes.length){ await db.put("equipamentos", {...existentes[0], ...a, atualizadoEm:agora()}); atualizados++; }
        else { await db.put("equipamentos", await novoRegistro({...a, foto_ids:[]})); novos++; }
      }
      await registrar("importação por planilha", {arquivo:arq.name, novos, atualizados, recusadas:recusadas.length});
      toast(`${novos} novos e ${atualizados} atualizados.`); navegar();
    });
  });
  $("#arqUnidade")?.addEventListener("change", async ev=>{
    const arq = ev.target.files[0]; if (!arq) return;
    try {
      const pacote = JSON.parse(await lerArquivoTexto(arq));
      const dados = pacote.dados || {};
      const uni = (dados.unidades || [])[0];
      if (!uni) return $("#mergeRelatorio").innerHTML = `<div class="card pendente">O arquivo não traz unidades.</div>`;
      const local = (await db.list("unidades")).find(u=> u.id === uni.id || normalizar(u.nome) === normalizar(uni.nome));
      const eqs = dados.equipamentos || [];
      const Info = {uni, local, eqs:eqs.length, paradas:(dados.paradas || []).length, mantens:(dados.manutencoes || []).length};
      $("#mergeRelatorio").innerHTML = `<div class="card"><h2 style="margin-top:0">Arquivo recebido</h2>
        <p>Unidade <b>${esc(uni.nome)}</b> · ${Info.eqs} equipamentos · ${Info.paradas} paradas · ${Info.mantens} manutenções.</p>
        ${local ? `<p class="sub">Esta cópia já tem uma unidade com esse nome (${esc(local.municipio || "")}). O app pergunta qual versão vale.</p>
          <div class="linha-botoes nao-imprimir"><button class="prim" id="btnMergeLocal">Manter a versão desta cópia</button>
            <button id="btnMergeArquivo">Usar a versão do arquivo</button></div>` : `<div class="linha-botoes nao-imprimir"><button class="prim" id="btnMergeArquivo">Importar a unidade do arquivo</button></div>`}
        <div id="mergeDetalhe"></div></div>`;
      $("#btnMergeArquivo")?.addEventListener("click", async ()=>{
        // a versão do arquivo entra; quando o patrimônio já existe, a do arquivo prevalece
        const reg = await novoRegistro({...uni, id: local ? local.id : uni.id});
        await db.put("unidades", {...(local || {}), ...reg, id: local ? local.id : reg.id});
        let novos = 0, atualizados = 0;
        for (const e of eqs){
          const ex = (await db.porIndice("equipamentos", "patrimonio", e.patrimonio))[0];
          if (ex){ await db.put("equipamentos", {...ex, ...e, id:ex.id, atualizadoEm:agora()}); atualizados++; }
          else { await db.put("equipamentos", await novoRegistro({...e, foto_ids:[]})); novos++; }
        }
        for (const p of (dados.paradas || [])) await db.put("paradas", p);
        for (const m of (dados.manutencoes || [])) await db.put("manutencoes", m);
        await registrar("unidade mesclada (RN10)", {detalhe:uni.nome, versao:"arquivo", novos, atualizados});
        toast(`Unidade do arquivo: ${novos} equipamentos novos, ${atualizados} atualizados.`); navegar();
      });
      $("#btnMergeLocal")?.addEventListener("click", async ()=>{
        for (const e of eqs){
          const ex = (await db.porIndice("equipamentos", "patrimonio", e.patrimonio))[0];
          if (ex) await db.put("equipamentos", {...ex, atualizadoEm:agora()});
          else await db.put("equipamentos", await novoRegistro({...e, foto_ids:[]}));
        }
        await registrar("unidade mesclada (RN10)", {detalhe:uni.nome, versao:"local"});
        toast("Equipamentos do arquivo mesclados com a base local."); navegar();
      });
    } catch(err){ $("#mergeRelatorio").innerHTML = `<div class="card pendente">Arquivo ilegível: ${esc(err.message)}</div>`; }
  });
};

/* ================= Sprint 4 e 5 na ficha do equipamento: histórico, MTTR e custo ================= */
const eqFichaAntes = TELAS["#/equipamento/:id"];
TELAS["#/equipamento/:id"] = async (p)=>{
  const html = await eqFichaAntes(p);
  if (p.id === "novo") return html;
  const b = await baseDeCalculo();
  const e = b.eqs.find(x=> x.id === p.id);
  if (!e) return html;
  const linhaMan = m=> `<tr><td>${dataCurtaBR(m.abertura)}</td><td>${m.tipo}</td><td>${m.conclusao ? dataCurtaBR(m.conclusao) : "aberta"}</td>
    <td class="num">${m.custo_rs ? dinheiro.fmt(Math.round(m.custo_rs * 100)) : "—"}</td><td>${esc(m.fornecedor || "")}</td></tr>`;
  const linhaPar = p2=> `<tr><td>${dataCurtaBR(p2.inicio)}</td><td>${p2.fim ? dataCurtaBR(p2.fim) : '<span class="selo erro">aberta</span>'}</td>
    <td>${esc(p2.motivo || "")}</td><td class="num">${dinheiro.fmt(Math.round((e.custoDiario || 0) * Math.max(1, diasUteis(dataDe(p2.inicio), p2.fim ? dataDe(p2.fim) : hojeISO()))))}</td></tr>`;
  const card = `<div class="card" id="historicoEq"><h2 style="margin-top:0">Histórico, MTTR e custo</h2>
    <div class="grade">
      ${cardKpiEq(e.temContrato ? e.contrato.numero : "sem contrato", "contrato vigente")}
      ${cardKpiEq(e.mttr === null ? "—" : e.mttr + " dias", "MTTR (RN06)")}
      ${cardKpiEq(dinheiro.fmt(Math.round(e.custoDiario)), "custo diário (RN02)")}
      ${cardKpiEq(dinheiro.fmt(Math.round(e.custoParadas)), "custo das paradas (RN03)")}
    </div>
    <h3>Manutenções (${e.manutencoes.length})</h3>
    <div class="tabela-wrap"><table><tr><th>Abertura</th><th>Tipo</th><th>Conclusão</th><th class="num">Custo</th><th>Fornecedor</th></tr>
      ${e.manutencoes.slice().sort((a, x)=> String(b.abertura).localeCompare(String(a.abertura))).map(linhaMan).join("") || '<tr><td colspan="5" class="vazio">Sem manutenções registradas.</td></tr>'}</table></div>
    <h3>Paradas (${e.paradas.length})</h3>
    <div class="tabela-wrap"><table><tr><th>Início</th><th>Fim</th><th>Motivo</th><th class="num">Custo</th></tr>
      ${e.paradas.map(linhaPar).join("") || '<tr><td colspan="4" class="vazio">Sem paradas registradas.</td></tr>'}</table></div></div>`;
  return html.replace('<div id="historicoEq"></div>', card);
};
