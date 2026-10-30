/* ================= Sprint 4 · Cobrança automática (RN08) ================= */
async function gdCobrancasDesligadas(){ return (await db.meta("cobrancas_desligadas")) || []; }
function gdPodeCobrar(p, desligadas){ return !desligadas.includes(p.lotacao); }
teste("RN08: a cobrança respeita a lotação desligada", ()=>{
  return gdPodeCobrar({lotacao: "Gabinete de Direção"}, []) && !gdPodeCobrar({lotacao: "Gabinete de Direção"}, ["Gabinete de Direção"]);
});

// registra a cobrança no vencimento, uma vez por processo
async function gdCobrarVencidos(hoje = hojeISO()){
  const ps = (await db.list("processos")).filter(p=>p.status === "em andamento");
  const desligadas = await gdCobrancasDesligadas(), cobs = await db.list("cobrancas");
  let n = 0;
  for (const p of ps){
    if (!gdPodeCobrar(p, desligadas)) continue;
    if (gdPrazo(p, hoje).sinal !== "vermelho") continue;
    if (cobs.some(c=>c.processo_id === p.id_processo && c.tipo === "automatica")) continue;
    await db.put("cobrancas", {id: uuid(), processo_id: p.id_processo, tipo: "automatica", data: hoje,
      texto: `Processo ${p.numero_processo} venceu o prazo de ${p.dias_prazo} dias (RN08).`, perfil: "sistema"});
    await db.put("log", {id: uuid(), processo_id: p.id_processo, tipo_evento: "cobrança automática", descricao: "prazo vencido (RN08)", perfil: "sistema", data_hora: agora()});
    n++;
  }
  if (n) await registrar("cobranças automáticas registradas", {detalhe: `${n} processo(s)`});
  return n;
}

/* ================= Sprint 5 · Assinatura, notificação e arquivamento ================= */
function gdFaltaAssinatura(p, assinatura){
  const falta = [];
  if (!assinatura) falta.push("assinatura da autoridade");
  else {
    if (!String(assinatura.nome || "").trim()) falta.push("nome da autoridade");
    if (!String(assinatura.cargo || "").trim()) falta.push("cargo da autoridade");
  }
  if (String(p.conclusao || "").trim().length < 20) falta.push("conclusão do processo (20 caracteres)");
  return falta;
}
teste("RN09: concluir exige assinatura da autoridade e conclusão", ()=>{
  const p = {conclusao: "Instrução concluída e requerente atendido integralmente."};
  return gdFaltaAssinatura(p, null).length === 1 && gdFaltaAssinatura(p, {nome: "", cargo: ""}).length === 2
    && gdFaltaAssinatura(p, {nome: "Autoridade", cargo: "Diretor"}).length === 0;
});

async function gdAssinaturas(id){ return (await db.porIndice("assinaturas", "processo_id", id)).sort((a, b)=>(a.data || "").localeCompare(b.data || "")); }
async function gdCobrancas(id){ return (await db.porIndice("cobrancas", "processo_id", id)).sort((a, b)=>(b.data || "").localeCompare(a.data || "")); }

const gdFichaAntiga = TELAS["#/processo/:id"], gdFichaAntigaDepois = TELAS_DEPOIS["#/processo/:id"];
TELAS["#/processo/:id"] = async (p)=>{
  let html = await gdFichaAntiga(p);
  const proc = await db.get("processos", p.id); if (!proc) return html;
  const [cobs, assin] = await Promise.all([gdCobrancas(p.id), gdAssinaturas(p.id)]);
  const ultima = assin[assin.length - 1], falta = gdFaltaAssinatura(proc, ultima);
  const card = `<div class="card" id="gdConclusao"><h2 style="margin-top:0">Conclusão e assinatura (RN09)</h2>
    ${proc.status === "arquivado" || proc.status === "concluido" ? `<p class="ok-txt">Processo ${esc(proc.status)}${ultima ? ` · assinado por ${esc(ultima.nome)} (${esc(ultima.cargo)}) em ${dataBR(ultima.data)}` : ""}.</p>`
      : `<p class="sub">A conclusão exige a assinatura da autoridade decisora e a conclusão escrita (RN09).</p>
        <form id="formGdFechar"><div class="campos">
          ${campo("gdAssNome", "Autoridade", {valor: "Autoridade competente"})}${campo("gdAssCargo", "Cargo", {valor: "Diretor"})}</div>
          ${campo("gdConclusaoTexto", "Conclusão do processo", {tipo: "textarea", linhas: 3, valor: proc.conclusao || ""})}
          <div id="gdErrosFechar"></div>
          <div class="linha-botoes"><button class="prim" type="submit">Assinar e concluir</button></div></form>`}
    ${cobs.length ? `<h3>Cobranças (${cobs.length})</h3><ul class="check-lista">${cobs.map(c=>`<li class="feito">${icone("alerta")}
      <span><b>${esc(c.tipo)}</b> · ${dataCurtaBR(c.data)}<br><small class="sub">${esc(c.texto)}</small></span></li>`).join("")}</ul>` : ""}
    ${assin.length ? `<h3>Trilha de aprovação</h3><ul class="check-lista">${assin.map(a=>`<li class="feito">${icone("check")}
      <span><b>${esc(a.nome)}</b> · ${esc(a.cargo)} · ${dataBR(a.data)}<br><small class="sub">${esc(a.conclusao)}</small></span></li>`).join("")}</ul>` : ""}</div>`;
  return html + card;
};
TELAS_DEPOIS["#/processo/:id"] = async (p)=>{
  await gdFichaAntigaDepois(p);
  $("#formGdFechar")?.addEventListener("submit", async e=>{
    e.preventDefault();
    const proc = await db.get("processos", p.id);
    const conclusao = valorDe("gdConclusaoTexto");
    const assinatura = {nome: valorDe("gdAssNome"), cargo: valorDe("gdAssCargo"), conclusao, data: agora(), perfil: estado.perfil};
    const falta = gdFaltaAssinatura({...proc, conclusao}, assinatura);
    if (!mostrarErros("#gdErrosFechar", falta.map(f=>`Falta ${f} (RN09).`))) return;
    await db.put("assinaturas", {id: uuid(), processo_id: p.id, ...assinatura});
    // RN10: notificação ao requerente e arquivamento
    await db.put("log", {id: uuid(), processo_id: p.id, tipo_evento: "notificação ao requerente",
      descricao: `Conclusão comunicada a ${proc.requerente}`, perfil: estado.perfil || "", data_hora: agora()});
    await db.put("log", {id: uuid(), processo_id: p.id, tipo_evento: "arquivamento", descricao: "Processo concluído e arquivado", perfil: estado.perfil || "", data_hora: agora()});
    await db.put("processos", {...proc, conclusao, status: "arquivado", concluido_em: agora()});
    await registrar("processo concluído e arquivado", {detalhe: proc.numero_processo});
    toast("Processo assinado, comunicado e arquivado."); navegar();
  });
};

/* ================= Sprint 6 · Painel, cobrança e relatório ================= */
const gdPainelAntigo = TELAS["#/painel"];
TELAS["#/painel"] = async ()=>{
  await gdCobrarVencidos();
  let html = await gdPainelAntigo();
  const [ps, cobs, assin, desligadas] = await Promise.all([db.list("processos"), db.list("cobrancas"), db.list("assinaturas"), gdCobrancasDesligadas()]);
  const hoje = hojeISO(), ativos = ps.filter(p=>p.status === "em andamento");
  const infos = ativos.map(p=>({p, ...gdPrazo(p, hoje)}));
  const amarelos = infos.filter(x=>x.sinal === "amarelo").length, vermelhos = infos.filter(x=>x.sinal === "vermelho").length;
  const arquivados = ps.filter(p=>p.status === "arquivado" || p.status === "concluido");
  const tempoMedio = arquivados.length ? Math.round(arquivados.reduce((a, p)=>{
    const ini = p.data_autuacao, fim = (p.concluido_em || agora()).slice(0, 10);
    return a + Math.max(0, Math.round((new Date(fim) - new Date(ini)) / 86400000)); }, 0) / arquivados.length * 10) / 10 : null;
  const porLotacao = Object.entries(ativos.reduce((a, p)=>{ a[p.lotacao] = (a[p.lotacao] || 0) + 1; return a; }, {})).sort((a, b)=>b[1] - a[1]);
  return html + `<div class="card" id="gdPainelGestor"><h2 style="margin-top:0">Painel da chefia (Sprint 6)</h2>
      <div class="grade">
        <div class="card kpi"><div class="v" data-gd-ind="amarelos">${amarelos}</div><div class="r">alertas amarelos</div></div>
        <div class="card kpi"><div class="v" data-gd-ind="vencidos">${vermelhos}</div><div class="r">vencidos</div></div>
        <div class="card kpi"><div class="v" data-gd-ind="cobrancas">${cobs.length}</div><div class="r">cobranças registradas</div></div>
        <div class="card kpi"><div class="v" data-gd-ind="tempo">${tempoMedio === null ? "—" : tempoMedio + " dia(s)"}</div><div class="r">tempo médio até a conclusão</div></div>
        <div class="card kpi"><div class="v" data-gd-ind="assinados">${assin.length}</div><div class="r">processos assinados</div></div></div>
      <div class="card"><h2 style="margin-top:0">Cobrança por lotação (RN08)</h2>
        <p class="sub">Desligue a cobrança de uma lotação quando ela não deve receber alerta automático.</p>
        <form id="formGdCobranca"><div class="campos">${campo("gdLotacaoCobranca", "Lotação", {tipo: "select",
          opcoes: [["", "Todas ativas"], ...porLotacao.map(([l])=>[l, l])]})}
          ${campo("gdCobrancaAcao", "Ação", {tipo: "select", opcoes: [["desligar", "Desligar a cobrança"], ["ligar", "Ligar a cobrança"]]})}</div>
          <div class="linha-botoes"><button type="submit">Aplicar</button></div></form>
        <p class="sub" id="gdListaDesligadas">Desligadas: ${desligadas.length ? desligadas.map(esc).join(", ") : "nenhuma"}.</p></div>
      <div class="card tabela-wrap"><h2 style="margin-top:0">Processos por lotação</h2><table id="tabelaLotacao"><tr><th>Lotação</th><th class="num">Em andamento</th></tr>
        ${porLotacao.map(([l, n])=>`<tr><td>${esc(l)}</td><td class="num">${n}</td></tr>`).join("")}</table></div>
      <div class="linha-botoes nao-imprimir"><button class="prim" id="btnGdCsv">${icone("download")} Exportar CSV</button>
        <button onclick="window.print()">${icone("imprimir")} Imprimir em A4</button></div></div>`;
};
TELAS_DEPOIS["#/painel"] = ()=>{
  $("#formGdCobranca")?.addEventListener("submit", async e=>{
    e.preventDefault();
    const lot = valorDe("gdLotacaoCobranca"), acao = valorDe("gdCobrancaAcao");
    if (!lot) return toast("Escolha a lotação.");
    let ds = await gdCobrancasDesligadas();
    ds = acao === "desligar" ? [...new Set([...ds, lot])] : ds.filter(x=>x !== lot);
    await db.meta("cobrancas_desligadas", ds);
    await registrar("cobrança da lotação alterada", {detalhe: `${lot}: ${acao}`});
    toast(acao === "desligar" ? "Cobrança desligada para a lotação." : "Cobrança ligada para a lotação."); navegar();
  });
  $("#btnGdCsv")?.addEventListener("click", async ()=>{
    const [ps, cobs] = await Promise.all([db.list("processos"), db.list("cobrancas")]);
    const linhas = [["id", "numero", "assunto", "requerente", "lotacao", "autuacao", "prazo", "situacao", "pct", "sinal", "cobrancas"]].concat(
      ps.map(p=>{ const pr = gdPrazo(p); return [p.id_processo, p.numero_processo, p.assunto, p.requerente, p.lotacao, p.data_autuacao,
        p.dias_prazo, p.status, pr.pct, pr.sinal, cobs.filter(c=>c.processo_id === p.id_processo).length]; }));
    const csv = "﻿" + linhas.map(l=>l.map(x=>/[;"\n]/.test(String(x)) ? `"${String(x).replace(/"/g, '""')}"` : String(x)).join(";")).join("\r\n");
    baixar(`processos-${hojeISO()}.csv`, csv, "text/csv;charset=utf-8");
    await registrar("relatório exportado", {detalhe: `${ps.length} processos`});
  });
};
