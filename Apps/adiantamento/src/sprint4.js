/* ================= Sprint 4 · Motor de prazos ================= */
const AD_PRAZO = {compra: {dias: 10, uteis: true}, "serviço": {dias: 15, uteis: true}, predial: {dias: 180, uteis: false}};
const AD_SELOS = {
  noprazo: {rotulo: "No prazo", selo: "ok"},
  vence7: {rotulo: "Vence em até 7 dias", selo: "alerta"},
  vencido: {rotulo: "Vencido", selo: "erro"},
};

function adISO(d){ return new Date(d.getTime() - d.getTimezoneOffset() * 60000).toISOString().slice(0, 10); }
function somarDiasCorridos(iso, n){ const d = new Date(iso + "T12:00:00"); d.setDate(d.getDate() + n); return adISO(d); }
// feriados que contam: nacional e estadual (o municipal fica na lista, mas não entra)
function adFeriadosQueContam(feriados){ return new Set((feriados || []).filter(f=>f.escopo !== "municipal").map(f=>f.data)); }
function somarDiasUteis(iso, n, feriados){
  const fora = adFeriadosQueContam(feriados); let d = new Date(iso + "T12:00:00"), c = 0;
  while (c < n){ d.setDate(d.getDate() + 1); const s = d.getDay(), t = adISO(d); if (s === 0 || s === 6 || fora.has(t)) continue; c++; }
  return adISO(d);
}
teste("RN03: 10 dias úteis com um feriado no meio", ()=>{
  // 2026-10-26 (segunda) + 10 dias úteis, com 2026-11-02 (Finados) no meio, chega em 2026-11-10
  return somarDiasUteis("2026-10-26", 10, [{data: "2026-11-02", escopo: "nacional"}]) === "2026-11-10";
});
teste("Dia útil pula o fim de semana", ()=> somarDiasUteis("2026-10-23", 1, []) === "2026-10-26" && somarDiasCorridos("2026-10-23", 1) === "2026-10-24");

// RN03/RN04: o prazo conta da data do pagamento (ou da abertura) e depende do tipo
function prazosDoProcesso(p, feriados, hoje = hojeISO()){
  const regra = AD_PRAZO[p.tipo] || AD_PRAZO.compra;
  const base = p.pago_em || p.criado_em || hoje;
  const limite = regra.uteis ? somarDiasUteis(base, regra.dias, feriados) : somarDiasCorridos(base, regra.dias);
  const restam = Math.round((new Date(limite + "T12:00:00") - new Date(hoje + "T12:00:00")) / 86400000);
  const selo = p.situacao === "encerrado" ? null : restam < 0 ? "vencido" : restam <= 7 ? "vence7" : "noprazo";
  return {base, limite, restam, selo, regra};
}
teste("Saldo do prazo: 3 dias restantes fica em aten.., -1 fica vencido", ()=>{
  const f = [];
  const p = {tipo: "compra", criado_em: "2026-10-01", situacao: "em andamento"};
  const r1 = prazosDoProcesso(p, f, "2026-10-13");   // limite 2026-10-15
  const r2 = prazosDoProcesso(p, f, "2026-10-16");
  return r1.restam === 2 && r1.selo === "vence7" && r2.selo === "vencido" && prazosDoProcesso({...p, situacao: "encerrado"}, f).selo === null;
});

async function adFeriados(){ return (await db.list("feriados")).sort((a, b)=>a.data.localeCompare(b.data)); }
const adSelo = s => { const d = AD_SELOS[s]; return d ? `<span class="selo ${d.selo}">${esc(d.rotulo)}</span>` : ""; };

/* ---------- feriados na configuração ---------- */
async function configExtra(){
  const fs = await adFeriados();
  return `<div class="card"><h2 style="margin-top:0">Feriados do prazo</h2>
    <p class="sub">Só os feriados <b>nacionais e estaduais</b> entram no prazo. O municipal fica na lista, mas não suspende a contagem (o recurso é federal).</p>
    <div class="campos">${campo("feData", "Data", {tipo: "date"})}${campo("feNome", "Nome", {})}
      ${campo("feEscopo", "Escopo", {tipo: "select", opcoes: [["nacional", "Nacional"], ["estadual", "Estadual"], ["municipal", "Municipal (não conta)"]]})}</div>
    <div class="linha-botoes"><button id="btnAddFeriado">Acrescentar feriado</button></div>
    <div class="tabela-wrap" style="margin-top:12px"><table id="tabelaFeriados"><tr><th>Data</th><th>Nome</th><th>Escopo</th><th></th></tr>
      ${fs.map(f=>`<tr><td>${dataCurtaBR(f.data)}</td><td>${esc(f.nome)}</td><td>${esc(f.escopo || "nacional")}</td>
        <td><button data-del-feriado="${esc(f.data)}">Remover</button></td></tr>`).join("")}</table></div></div>`;
}
async function ligarConfigExtra(){
  $("#btnAddFeriado")?.addEventListener("click", async ()=>{
    const data = valorDe("feData"), nome = valorDe("feNome");
    if (!data || !nome) return toast("Informe a data e o nome do feriado.");
    if ((await db.list("feriados")).some(f=>f.data === data)) return toast("Este feriado já está na lista.");
    await db.put("feriados", {data, nome, escopo: valorDe("feEscopo") || "nacional"});
    await registrar("feriado acrescentado", {detalhe: `${data} · ${nome}`}); toast("Feriado acrescentado."); navegar();
  });
  $$("[data-del-feriado]").forEach(b=>b.addEventListener("click", async ()=>{
    await db.del("feriados", b.dataset.delFeriado); await registrar("feriado removido", {detalhe: b.dataset.delFeriado}); navegar();
  }));
}

/* ---------- selo do prazo na ficha do processo ---------- */
const adFichaS3 = TELAS["#/processo/:id"];
TELAS["#/processo/:id"] = async (p)=>{
  let html = await adFichaS3(p);
  const proc = await db.get("processos", p.id); if (!proc) return html;
  const pr = prazosDoProcesso(proc, await adFeriados());
  const bloco = `<div class="card" id="adPrazo"><h2 style="margin-top:0">Prazo (RN03, RN04)</h2>
    <p>Base de contagem: <b>${dataCurtaBR(pr.base)}</b> · regra: ${pr.regra.dias} ${pr.regra.uteis ? "dias úteis" : "dias corridos"} para ${esc(proc.tipo)}
      · limite: <b>${dataCurtaBR(pr.limite)}</b></p>
    <p>${pr.selo ? `${adSelo(pr.selo)} · <b data-ad-restam>${pr.restam}</b> dia(s)` : '<span class="selo info">encerrado</span>'}</p></div>`;
  return html + bloco;
};

/* ================= Sprint 5 · Pendências e prestação de contas ================= */
const AD_PRAZO_PENDENCIA = 10;

async function adAbrirPendencia(pid, motivo, feriados){
  const hoje = hojeISO(), prazo = somarDiasUteis(hoje, AD_PRAZO_PENDENCIA, feriados);
  await db.put("pendencias", {id: uuid(), processo_id: pid, motivo, aberta_em: hoje, prazo, resolvida_em: null});
  await registrar("pendência aberta (RN05)", {processo_id: pid, detalhe: `${motivo} · prazo ${prazo}`});
  return prazo;
}
function adPendenciaVencida(p, hoje = hojeISO()){ return !p.resolvida_em && p.prazo && p.prazo < hoje; }
teste("RN05: pendência sem resolução e com prazo passado está vencida", ()=>{
  return adPendenciaVencida({prazo: "2026-10-01", resolvida_em: null}, "2026-10-10")
    && !adPendenciaVencida({prazo: "2026-10-20", resolvida_em: null}, "2026-10-10")
    && !adPendenciaVencida({prazo: "2026-10-01", resolvida_em: "2026-10-02"}, "2026-10-10");
});

// RN06: a soma das notas não pode passar do valor concedido
function adConferirPrestacao(notas, valor_concedido){
  const soma = Math.round((notas || []).reduce((a, n)=>a + Number(n.valor || 0), 0) * 100) / 100;
  const concedido = Math.round(Number(valor_concedido || 0) * 100) / 100;
  return {soma, concedido, diferenca: Math.round((concedido - soma) * 100) / 100, excedeu: soma > concedido + 0.004};
}
teste("RN06: notas acima do valor concedido marcam excedente", ()=>{
  const a = adConferirPrestacao([{valor: 100}, {valor: 150}], 300), b = adConferirPrestacao([{valor: 200}], 300);
  return a.soma === 250 && a.diferenca === 50 && !a.excedeu && adConferirPrestacao([{valor: 400}], 300).excedeu && b.diferenca === 100;
});

TELAS["#/processo/:id/prestacao"] = async ({id})=>{
  const p = await db.get("processos", id);
  if (!p) return `<div class="card vazio">Processo não encontrado.</div>`;
  const notas = (await db.porIndice("notas", "processo_id", id)).sort((a, b)=>(a.data || "").localeCompare(b.data || ""));
  const r = adConferirPrestacao(notas, p.valor_concedido);
  const pends = (await db.porIndice("pendencias", "processo_id", id)).sort((a, b)=>b.aberta_em.localeCompare(a.aberta_em));
  const encerrado = p.situacao === "encerrado";
  return `<p class="sub nao-imprimir" style="margin-bottom:6px"><a href="#/processo/${encodeURIComponent(id)}">← Processo</a></p>
    <h1>Prestação de contas · ${esc(p.id)}</h1>
    <p class="sub">${esc(p.unidade)} · ${esc(p.finalidade)}</p>
    <div class="grade"><div class="card kpi"><div class="v" data-ad-concedido>${dinheiro.fmt(Math.round(r.concedido * 100))}</div><div class="r">valor concedido</div></div>
      <div class="card kpi"><div class="v" data-ad-soma>${dinheiro.fmt(Math.round(r.soma * 100))}</div><div class="r">soma das notas</div></div>
      <div class="card kpi"><div class="v" data-ad-dif>${dinheiro.fmt(Math.round(r.diferenca * 100))}</div><div class="r">saldo</div></div></div>
    ${r.excedeu ? '<div class="card pendente" id="adExcedeu"><b>Atenção (RN06):</b> a soma das notas passa do valor concedido. Corrija antes de encerrar.</div>' : ""}
    <form class="card" id="formNota"><h2 style="margin-top:0">Nota fiscal</h2><div class="campos">
      ${campo("noNumero", "Número", {obrigatorio: true})}${campo("noCnpj", "CNPJ", {attrs: 'inputmode="numeric"'})}
      ${campo("noValor", "Valor (R$)", {obrigatorio: true, attrs: 'inputmode="decimal"'})}${campo("noData", "Data", {tipo: "date", valor: hojeISO()})}</div>
      <div id="adErrosNota"></div><div class="linha-botoes"><button class="prim" type="submit">Acrescentar nota</button></div></form>
    <div class="card tabela-wrap"><table id="tabelaNotas"><tr><th>Número</th><th>CNPJ</th><th class="num">Valor</th><th>Data</th></tr>
      ${notas.map(n=>`<tr><td>${esc(n.numero)}</td><td class="mono">${esc(n.cnpj || "—")}</td><td class="num">${dinheiro.fmt(Math.round((n.valor || 0) * 100))}</td><td>${dataCurtaBR(n.data)}</td></tr>`).join("")
        || '<tr><td colspan="4" class="vazio">Nenhuma nota registrada.</td></tr>'}</table></div>
    <div class="card"><h2 style="margin-top:0">Pendências (RN05)</h2>
      <ul class="check-lista">${pends.map(x=>`<li class="${x.resolvida_em ? "feito" : adPendenciaVencida(x) ? "falta" : "falta"}">${icone(x.resolvida_em ? "check" : "alerta")}
        <span><b>${esc(x.motivo)}</b> · aberta em ${dataCurtaBR(x.aberta_em)} · prazo ${dataCurtaBR(x.prazo)}${x.resolvida_em ? " · resolvida em " + dataCurtaBR(x.resolvida_em) : adPendenciaVencida(x) ? ' · <span class="erro-txt">vencida</span>' : ""}</span>
        ${x.resolvida_em ? "" : `<button data-resolver="${esc(x.id)}">Resolver</button>`}</li>`).join("") || '<li class="vazio">Nenhuma pendência.</li>'}</ul>
      <form id="formPendencia" class="campos" style="align-items:end">${campo("peMotivo", "Nova pendência (motivo)", {})}
        <div class="campo"><label>&nbsp;</label><button id="btnPendencia">Abrir pendência (10 dias úteis)</button></div></form></div>
    ${encerrado ? `<div class="card ok"><b>Processo encerrado.</b> Decisão: ${esc(p.decisao_prestacao || "não registrada")}.</div>`
      : `<form class="card" id="formEncerrar"><h2 style="margin-top:0">Encerrar a prestação</h2>
        <p class="sub">A decisão do ordenador é só registrada no app.</p>
        <div class="campos">${campo("enDecisao", "Decisão", {tipo: "select", opcoes: [["aprovado sem ressalvas", "Aprovado sem ressalvas"], ["aprovado com ressalvas", "Aprovado com ressalvas"]]})}</div>
        <div id="adErrosEncerrar"></div><div class="linha-botoes"><button class="prim" type="submit">Encerrar</button></div></form>`}`;
};
TELAS_DEPOIS["#/processo/:id/prestacao"] = ({id})=>{
  $("#formNota")?.addEventListener("submit", async e=>{
    e.preventDefault();
    const valor = dinheiro.de(valorDe("noValor"));
    const erros = [];
    if (!valorDe("noNumero")) erros.push("Informe o número da nota.");
    if (!(valor > 0)) erros.push("Informe o valor da nota.");
    if (valorDe("noCnpj") && !cnpjValido(valorDe("noCnpj"))) erros.push("CNPJ inválido.");
    if (!mostrarErros("#adErrosNota", erros)) return;
    await db.put("notas", {id: uuid(), processo_id: id, numero: valorDe("noNumero"), cnpj: valorDe("noCnpj").replace(/\D/g, ""),
      valor: valor / 100, data: valorDe("noData") || hojeISO()});
    await registrar("nota registrada", {processo_id: id, detalhe: valorDe("noNumero")}); toast("Nota registrada."); navegar();
  });
  $("#btnPendencia")?.addEventListener("click", async ()=>{
    const motivo = valorDe("peMotivo"); if (!motivo) return toast("Escreva o motivo da pendência.");
    const prazo = await adAbrirPendencia(id, motivo, await adFeriados());
    toast(`Pendência aberta; prazo em ${dataCurtaBR(prazo)}.`); navegar();
  });
  $$("[data-resolver]").forEach(b=>b.addEventListener("click", async ()=>{
    const x = await db.get("pendencias", b.dataset.resolver);
    await db.put("pendencias", {...x, resolvida_em: hojeISO()});
    await registrar("pendência resolvida", {processo_id: id}); toast("Pendência resolvida."); navegar();
  }));
  $("#formEncerrar")?.addEventListener("submit", async e=>{
    e.preventDefault();
    const p = await db.get("processos", id), notas = await db.porIndice("notas", "processo_id", id), r = adConferirPrestacao(notas, p.valor_concedido);
    const abertas = (await db.porIndice("pendencias", "processo_id", id)).filter(x=>!x.resolvida_em);
    const erros = [];
    if (r.excedeu) erros.push("A soma das notas passa do valor concedido (RN06).");
    if (abertas.length) erros.push(`Resolva as ${abertas.length} pendência(s) abertas (RN05).`);
    if (!notas.length) erros.push("Registre as notas fiscais.");
    if (!mostrarErros("#adErrosEncerrar", erros)) return;
    await db.put("processos", {...p, situacao: "encerrado", etapa_atual: "Encerrado", decisao_prestacao: valorDe("enDecisao"), encerrado_em: agora()});
    await registrar("prestação encerrada", {processo_id: id, detalhe: valorDe("enDecisao")}); toast("Prestação encerrada."); navegar();
  });
};

/* ================= Sprint 6 · Painel e relatório ================= */
function adBarras(titulo, pares, cor = "var(--accent)"){
  const max = Math.max(1, ...pares.map(([, n])=>n)), w = 420, h = 26;
  return `<div class="card"><h2 style="margin-top:0">${esc(titulo)}</h2>
    <svg viewBox="0 0 ${w} ${Math.max(60, pares.length * h + 10)}" role="img" aria-label="${esc(titulo)}" style="width:100%;height:auto">
      ${pares.map(([rot, n], i)=>{ const d = Math.round(n / max * (w - 170)), y = i * h + 6;
        return `<text x="0" y="${y + 13}" font-size="12" fill="var(--ink2)">${esc(String(rot).slice(0, 22))}</text>
          <rect x="150" y="${y + 2}" width="${d}" height="14" rx="3" fill="${cor}"></rect>
          <text x="${156 + d}" y="${y + 13}" font-size="12" fill="var(--ink)">${n}</text>`; }).join("")}
    </svg></div>`;
}

const adPainelS1 = TELAS["#/painel"];
TELAS["#/painel"] = async ()=>{
  const ps = await db.list("processos"), es = await db.list("etapas"), feriados = await adFeriados(), hoje = hojeISO();
  const infos = ps.map(p=>({p, ...prazosDoProcesso(p, feriados, hoje)}));
  const porSelo = s => infos.filter(x=>x.selo === s);
  const conta = campo => Object.entries(ps.reduce((a, p)=>{ const k = p[campo] || "—"; a[k] = (a[k] || 0) + 1; return a; }, {})).sort((a, b)=>b[1] - a[1]);
  const tempos = {};
  for (const e of es.filter(x=>x.saida_em)){ const d = Math.round((new Date(e.saida_em) - new Date(e.entrada_em)) / 86400000); (tempos[e.etapa] ||= []).push(d); }
  const medias = Object.entries(tempos).map(([k, v])=>[k, Math.round(v.reduce((a, b)=>a + b, 0) / v.length * 10) / 10]).sort((a, b)=>b[1] - a[1]);
  return `<h1>Painel</h1><p class="sub">${ps.length} processos no recorte · ${porSelo("vencido").length} vencidos · ${porSelo("vence7").length} vencendo em até 7 dias.</p>
    <div class="grade">
      <div class="card kpi"><div class="v" data-ad-ind="total">${ps.length}</div><div class="r">processos</div></div>
      <div class="card kpi"><div class="v" data-ad-ind="vencidos">${porSelo("vencido").length}</div><div class="r">vencidos</div></div>
      <div class="card kpi"><div class="v" data-ad-ind="vencendo">${porSelo("vence7").length}</div><div class="r">vencem em até 7 dias</div></div>
      <div class="card kpi"><div class="v" data-ad-ind="encerrados">${ps.filter(p=>p.situacao === "encerrado").length}</div><div class="r">encerrados</div></div></div>
    ${adBarras("Processos por etapa", conta("etapa_atual"))}
    ${adBarras("Tempo médio por etapa (dias)", medias, "var(--verde)")}
    <div class="card tabela-wrap"><h2 style="margin-top:0">Vencidos e a vencer</h2><table id="tabelaPrazos"><tr><th>Processo</th><th>Unidade</th><th>Tipo</th><th>Limite</th><th class="num">Dias</th><th>Situação</th></tr>
      ${infos.filter(x=>x.selo).sort((a, b)=>a.restam - b.restam).map(({p, limite, restam, selo})=>`<tr><td><a href="#/processo/${encodeURIComponent(p.id)}">${esc(p.id)}</a></td>
        <td>${esc(p.unidade)}</td><td>${esc(p.tipo)}</td><td>${dataCurtaBR(limite)}</td><td class="num">${restam}</td><td>${adSelo(selo)}</td></tr>`).join("")
        || '<tr><td colspan="6" class="vazio">Nenhum processo com prazo correndo.</td></tr>'}</table></div>`;
};

TELAS["#/relatorio"] = async ()=>{
  const ps = await db.list("processos"), es = await db.list("etapas"), pends = await db.list("pendencias");
  const devolvidas = es.filter(e=>e.devolucao);
  const porMotivo = Object.entries(devolvidas.reduce((a, e)=>{ const k = (e.observacao || "sem motivo").split(":")[0]; a[k] = (a[k] || 0) + 1; return a; }, {})).sort((a, b)=>b[1] - a[1]);
  const ciclo = ps.filter(p=>p.pago_em).map(p=>Math.round((new Date(p.pago_em) - new Date(p.criado_em)) / 86400000));
  const media = ciclo.length ? Math.round(ciclo.reduce((a, b)=>a + b, 0) / ciclo.length * 10) / 10 : null;
  return `<h1>Relatório</h1><p class="sub">Devoluções, tempo do pedido ao pagamento e pendências.</p>
    <div class="grade">
      <div class="card kpi"><div class="v" data-ad-rel="devolucoes">${devolvidas.length}</div><div class="r">devoluções registradas</div></div>
      <div class="card kpi"><div class="v" data-ad-rel="ciclo">${media === null ? "—" : media + " dia(s)"}</div><div class="r">média do pedido ao pagamento</div></div>
      <div class="card kpi"><div class="v" data-ad-rel="pendencias">${pends.filter(p=>!p.resolvida_em).length}</div><div class="r">pendências abertas</div></div></div>
    <div class="card tabela-wrap"><h2 style="margin-top:0">Devoluções por motivo</h2><table id="tabelaMotivosAd"><tr><th>Motivo</th><th class="num">Devoluções</th></tr>
      ${porMotivo.map(([m, n])=>`<tr><td>${esc(m)}</td><td class="num">${n}</td></tr>`).join("") || '<tr><td colspan="2" class="vazio">Nenhuma devolução.</td></tr>'}</table></div>
    <div class="linha-botoes nao-imprimir"><button class="prim" id="btnAdCsv">${icone("download")} Exportar CSV</button>
      <button onclick="window.print()">${icone("imprimir")} Imprimir em A4</button></div>`;
};
TELAS_DEPOIS["#/relatorio"] = ()=>{
  $("#btnAdCsv")?.addEventListener("click", async ()=>{
    const ps = await db.list("processos");
    const linhas = [["id", "unidade", "tipo", "situacao", "etapa", "criado_em", "pago_em", "valor_concedido"]].concat(
      ps.map(p=>[p.id, p.unidade, p.tipo, p.situacao, p.etapa_atual, p.criado_em, p.pago_em || "", p.valor_concedido ?? ""]));
    const csv = "﻿" + linhas.map(l=>l.map(c=>/[;"\n]/.test(String(c)) ? `"${String(c).replace(/"/g, '""')}"` : String(c)).join(";")).join("\r\n");
    baixar(`adiantamentos-${hojeISO()}.csv`, csv, "text/csv;charset=utf-8");
    await registrar("relatório exportado", {detalhe: `${ps.length} processos`});
  });
};
