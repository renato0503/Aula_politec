/* ================= Sprint 4 · Trilha de aprovação e modalidade ================= */
const CA_APROVACOES = {
  tecnica: {rotulo: "Análise técnica", etapa: "Análise técnica"},
  orcamentaria: {rotulo: "Análise orçamentária", etapa: "Análise técnica"},
  juridica: {rotulo: "Análise jurídica", etapa: "Análise jurídica"},
};
const CA_MODALIDADES = ["Pregão eletrônico", "Concorrência", "Dispensa", "Inexigibilidade", "Credenciamento", "Pré-qualificação"];
const CA_CRITERIOS = ["Menor preço", "Maior desconto", "Melhor técnica", "Técnica e preço", "Maior retorno econômico"];

async function caAprovacoes(id){ return (await db.porIndice("aprovacoes", "processo_id", id)).sort((a, b)=>(a.data || "").localeCompare(b.data || "")); }
teste("Sprint 4: os três tipos de análise estão definidos", ()=> Object.keys(CA_APROVACOES).length === 3 && CA_MODALIDADES.length === 6);

const caFichaAntiga = TELAS["#/processo/:id"], caFichaAntigaDepois = TELAS_DEPOIS["#/processo/:id"];
TELAS["#/processo/:id"] = async (p)=>{
  let html = await caFichaAntiga(p);
  const proc = await db.get("processos", p.id); if (!proc) return html;
  const aps = await caAprovacoes(p.id);
  const tem = t => aps.some(a=>a.tipo === t && a.decisao === "favorável");
  const alerta = ([]) => "";
  const card = `<div class="card" id="caAprovacoes"><h2 style="margin-top:0">Trilha de aprovação</h2>
    <p class="sub">Cada análise registra setor, perfil, data e parecer. Sem o parecer favorável da etapa, o processo não deveria avançar.</p>
    <ul class="check-lista">${Object.entries(CA_APROVACOES).map(([t, d])=>{
      const a = aps.filter(x=>x.tipo === t).pop();
      return `<li class="${a ? (a.decisao === "favorável" ? "feito" : "falta") : "falta"}">${icone(a && a.decisao === "favorável" ? "check" : "alerta")}
        <span><b>${esc(d.rotulo)}</b>${a ? ` · ${esc(a.decisao)} · ${dataCurtaBR(a.data)} · ${esc(a.setor)}` : " · pendente"}</span></li>`;
    }).join("")}</ul>
    ${["Análise técnica", "Análise jurídica"].includes(proc.etapa) && !tem(proc.etapa === "Análise jurídica" ? "juridica" : "tecnica")
      ? `<div class="card pendente"><b>Atenção:</b> a etapa ${esc(proc.etapa)} está aberta sem o parecer favorável correspondente.</div>` : ""}
    <form id="formCaAprovacao"><div class="campos">
      ${campo("caApTipo", "Análise", {tipo: "select", opcoes: Object.entries(CA_APROVACOES).map(([k, d])=>[k, d.rotulo])})}
      ${campo("caApDecisao", "Decisão", {tipo: "select", opcoes: [["favorável", "Favorável"], ["desfavorável", "Desfavorável"]]})}
      ${campo("caApSetor", "Setor", {valor: "", ajuda: "Ex.: Aquisições, Contabilidade, Assessoria jurídica."})}</div>
      ${campo("caApParecer", "Parecer (mínimo de 20 caracteres)", {tipo: "textarea", linhas: 3})}
      <div id="caErrosAprovacao"></div><div class="linha-botoes"><button class="prim" type="submit">Registrar análise</button></div></form></div>
    <div class="card" id="caModalidade"><h2 style="margin-top:0">Modalidade e critério de julgamento</h2>
    ${proc.modalidade ? `<p><b>${esc(proc.modalidade)}</b> · critério: ${esc(proc.criterio_julgamento || "não informado")} · registrada em ${dataCurtaBR(proc.modalidade_em)}</p>`
      : '<p class="sub">A modalidade ainda não foi registrada.</p>'}
    <form id="formCaModalidade"><div class="campos">
      ${campo("caMod", "Modalidade", {tipo: "select", opcoes: [["", "Escolha"], ...CA_MODALIDADES.map(m=>[m, m])], valor: proc.modalidade || ""})}
      ${campo("caCrit", "Critério de julgamento", {tipo: "select", opcoes: [["", "Escolha"], ...CA_CRITERIOS.map(c=>[c, c])], valor: proc.criterio_julgamento || ""})}</div>
      <div id="caErrosModalidade"></div><div class="linha-botoes"><button type="submit">Registrar modalidade</button></div></form></div>`;
  return html + card;
};
TELAS_DEPOIS["#/processo/:id"] = async (p)=>{
  await caFichaAntigaDepois(p);
  $("#formCaAprovacao")?.addEventListener("submit", async e=>{
    e.preventDefault();
    const tipo = valorDe("caApTipo"), parecer = valorDe("caApParecer"), setor = valorDe("caApSetor");
    const erros = [];
    if (parecer.length < 20) erros.push("Escreva o parecer com pelo menos 20 caracteres.");
    if (!setor) erros.push("Informe o setor que analisou.");
    if (!mostrarErros("#caErrosAprovacao", erros)) return;
    await db.put("aprovacoes", {id: uuid(), processo_id: p.id, tipo, decisao: valorDe("caApDecisao"), setor, parecer, data: agora(), perfil: estado.perfil});
    await db.put("log", {id: uuid(), processo_id: p.id, acao: `análise registrada: ${CA_APROVACOES[tipo].rotulo}`, perfil: estado.perfil || "", data_hora: agora()});
    await registrar("análise registrada", {processo_id: p.id, detalhe: tipo});
    toast("Análise registrada."); navegar();
  });
  $("#formCaModalidade")?.addEventListener("submit", async e=>{
    e.preventDefault();
    const mod = valorDe("caMod"), crit = valorDe("caCrit"), erros = [];
    if (!mod) erros.push("Escolha a modalidade.");
    if (!crit) erros.push("Escolha o critério de julgamento.");
    if (!mostrarErros("#caErrosModalidade", erros)) return;
    const proc = await db.get("processos", p.id);
    await db.put("processos", {...proc, modalidade: mod, criterio_julgamento: crit, modalidade_em: hojeISO()});
    await db.put("log", {id: uuid(), processo_id: p.id, acao: `modalidade definida: ${mod}`, perfil: estado.perfil || "", data_hora: agora()});
    await registrar("modalidade definida", {processo_id: p.id, detalhe: mod});
    toast("Modalidade registrada."); navegar();
  });
};

/* ================= Sprint 5 e 6 · Painel do gestor, tempo por etapa e relatório ================= */
const caDiasCalc = (a, b)=> a && b ? Math.max(0, Math.round((new Date(b) - new Date(a)) / 86400000)) : null;

// tempo por etapa a partir do log ("etapa concluída: X")
function caTempoPorEtapa(ps, logs){
  const acc = {};
  for (const p of ps){
    const feitos = logs.filter(l=>l.processo_id === p.id && /^etapa concluída:|^processo concluído/.test(l.acao))
      .sort((a, b)=>a.data_hora.localeCompare(b.data_hora));
    let anterior = p.data_abertura ? new Date(p.data_abertura + "T12:00:00").toISOString() : null;
    for (const l of feitos){
      const etapa = l.acao.replace(/^etapa concluída: /, "").replace(/^processo concluído$/, "Modalidade definida");
      const dias = caDiasCalc(anterior, l.data_hora);
      if (dias !== null){ (acc[etapa] ||= []).push(dias); }
      anterior = l.data_hora;
    }
  }
  return Object.fromEntries(Object.entries(acc).map(([k, v])=>[k, Math.round(v.reduce((a, b)=>a + b, 0) / v.length * 10) / 10]));
}
teste("Sprint 6: tempo médio por etapa calculado", ()=>{
  const ps = [{id: "A", data_abertura: "2026-10-01"}];
  const logs = [{processo_id: "A", acao: "etapa concluída: DFD", data_hora: "2026-10-04T10:00:00"},
                {processo_id: "A", acao: "etapa concluída: ETP", data_hora: "2026-10-10T10:00:00"}];
  const r = caTempoPorEtapa(ps, logs);
  return r["DFD"] === 3 && r["ETP"] === 6;
});

// processo parado: dias na etapa atual acima do prazo daquela etapa
function caParado(p, logs, hoje = hojeISO()){
  if (p.status === "concluido") return false;
  const ult = logs.filter(l=>l.processo_id === p.id).map(l=>l.data_hora.slice(0, 10)).sort().pop() || p.data_abertura;
  const dias = caDiasCalc(ult + "T12:00:00", hoje + "T12:00:00");
  return dias !== null && dias > Number(CA_PRAZO_ETAPA[p.etapa] || 30);
}
teste("Sprint 5: processo parado acima do prazo da etapa", ()=>{
  const p = {id: "A", status: "em andamento", etapa: "DFD", data_abertura: "2026-10-01"};
  return caParado(p, [], "2026-10-10") && !caParado(p, [], "2026-10-02");
});

function caBarras(titulo, pares, cor = "var(--accent)"){
  const max = Math.max(1, ...pares.map(([, n])=>n)), w = 420, h = 26;
  return `<div class="card"><h2 style="margin-top:0">${esc(titulo)}</h2>
    <svg viewBox="0 0 ${w} ${Math.max(60, pares.length * h + 10)}" role="img" aria-label="${esc(titulo)}" style="width:100%;height:auto">
      ${pares.map(([rot, n], i)=>{ const d = Math.round(n / max * (w - 170)), y = i * h + 6;
        return `<text x="0" y="${y + 13}" font-size="12" fill="var(--ink2)">${esc(String(rot).slice(0, 22))}</text>
          <rect x="150" y="${y + 2}" width="${d}" height="14" rx="3" fill="${cor}"></rect>
          <text x="${156 + d}" y="${y + 13}" font-size="12" fill="var(--ink)">${n}</text>`; }).join("")}
    </svg></div>`;
}

TELAS["#/painel"] = async ()=>{
  const [ps, pends, logs, aps] = await Promise.all([db.list("processos"), db.list("pendencias"), db.list("log"), db.list("aprovacoes")]);
  const hoje = hojeISO(), ativos = ps.filter(p=>p.status !== "concluido"), atras = ativos.filter(p=>caAtrasado(p, hoje));
  const porEtapa = CA_ETAPAS.map(e=>[e, ativos.filter(p=>p.etapa === e).length]);
  const tempos = caTempoPorEtapa(ps, logs);
  const parados = ps.filter(p=>caParado(p, logs, hoje));
  const abertas = pends.filter(x=>!x.resolvida_em);
  const porUnidade = Object.entries(abertas.reduce((a, x)=>{
    const p = ps.find(y=>y.id_processo === x.processo_id); const k = p?.unidade || "—"; a[k] = (a[k] || 0) + 1; return a; }, {})).sort((a, b)=>b[1] - a[1]);
  const porResp = Object.entries(abertas.reduce((a, x)=>{
    const p = ps.find(y=>y.id_processo === x.processo_id); const k = p?.responsavel || "—"; a[k] = (a[k] || 0) + 1; return a; }, {})).sort((a, b)=>b[1] - a[1]);
  const concluidos = ps.filter(p=>p.status === "concluido");
  const prazoMedio = concluidos.length ? Math.round(concluidos.reduce((a, p)=>{
    const ult = logs.filter(l=>l.processo_id === p.id).map(l=>l.data_hora.slice(0, 10)).sort().pop();
    return a + (caDiasCalc(p.data_abertura + "T12:00:00", (ult || hoje) + "T12:00:00") || 0); }, 0) / concluidos.length * 10) / 10 : null;
  return `<h1>Painel de Aquisições</h1><p class="sub">${ativos.length} processos em andamento · ${parados.length} parado(s) · ${abertas.length} pendência(s) aberta(s).</p>
    <div class="grade">
      <div class="card kpi"><div class="v" data-ca-ind="ativos">${ativos.length}</div><div class="r">em andamento</div></div>
      <div class="card kpi"><div class="v" data-ca-ind="atrasados" data-atrasados>${atras.length}</div><div class="r">fora do prazo</div></div>
      <div class="card kpi"><div class="v" data-ca-ind="parados">${parados.length}</div><div class="r">parados na etapa</div></div>
      <div class="card kpi"><div class="v" data-ca-ind="retrabalho">${pends.length}</div><div class="r">retrabalho (pendências)</div></div>
      <div class="card kpi"><div class="v" data-ca-ind="prazo">${prazoMedio === null ? "—" : prazoMedio + " dia(s)"}</div><div class="r">prazo médio dos concluídos</div></div>
      <div class="card kpi"><div class="v" data-ca-ind="analises">${aps.length}</div><div class="r">análises registradas</div></div></div>
    ${caBarras("Processos por etapa", porEtapa)}
    ${caBarras("Tempo médio por etapa (dias)", Object.entries(tempos), "var(--verde)")}
    <div class="duas-colunas">
      <div class="card tabela-wrap"><h2 style="margin-top:0">Pendências por unidade</h2><table id="tabelaUnidade"><tr><th>Unidade</th><th class="num">Pendências</th></tr>
        ${porUnidade.map(([k, n])=>`<tr><td>${esc(k)}</td><td class="num">${n}</td></tr>`).join("") || '<tr><td colspan="2" class="vazio">Nenhuma pendência.</td></tr>'}</table></div>
      <div class="card tabela-wrap"><h2 style="margin-top:0">Pendências por responsável</h2><table id="tabelaResp"><tr><th>Responsável</th><th class="num">Pendências</th></tr>
        ${porResp.map(([k, n])=>`<tr><td>${esc(k)}</td><td class="num">${n}</td></tr>`).join("") || '<tr><td colspan="2" class="vazio">Nenhuma pendência.</td></tr>'}</table></div></div>
    <div class="card tabela-wrap"><h2 style="margin-top:0">Processos parados</h2><table id="tabelaParados"><tr><th>Processo</th><th>Etapa</th><th>Unidade</th><th class="num">Dias na etapa</th><th class="num">Prazo da etapa</th></tr>
      ${parados.map(p=>`<tr><td><a href="#/processo/${encodeURIComponent(p.id_processo)}">${esc(p.numero_sigadoc)}</a></td><td>${esc(p.etapa)}</td>
        <td>${esc(p.unidade)}</td><td class="num"><span class="erro-txt">${caDiasCalc((logs.filter(l=>l.processo_id === p.id_processo).map(l=>l.data_hora.slice(0, 10)).sort().pop() || p.data_abertura) + "T12:00:00", hoje + "T12:00:00")}</span></td>
        <td class="num">${CA_PRAZO_ETAPA[p.etapa] || 30}</td></tr>`).join("") || '<tr><td colspan="5" class="vazio">Nenhum processo parado.</td></tr>'}</table></div>
    <div class="linha-botoes nao-imprimir"><button class="prim" id="btnCaCsv">${icone("download")} Exportar CSV</button>
      <button onclick="window.print()">${icone("imprimir")} Imprimir em A4</button></div>`;
};
TELAS_DEPOIS["#/painel"] = ()=>{
  $("#btnCaCsv")?.addEventListener("click", async ()=>{
    const ps = await db.list("processos"), logs = await db.list("log");
    const linhas = [["id", "sigadoc", "siag", "objeto", "unidade", "etapa", "situacao", "abertura", "dias", "atrasado", "parado"]].concat(
      ps.map(p=>[p.id_processo, p.numero_sigadoc, p.numero_siag, p.objeto, p.unidade, p.etapa, p.status, p.data_abertura,
        caDias(p.data_abertura), caAtrasado(p) ? "sim" : "não", caParado(p, logs) ? "sim" : "não"]));
    const csv = "﻿" + linhas.map(l=>l.map(c=>/[;"\n]/.test(String(c)) ? `"${String(c).replace(/"/g, '""')}"` : String(c)).join(";")).join("\r\n");
    baixar(`aquisicoes-${hojeISO()}.csv`, csv, "text/csv;charset=utf-8");
    await registrar("relatório exportado", {detalhe: `${ps.length} processos`});
  });
};
