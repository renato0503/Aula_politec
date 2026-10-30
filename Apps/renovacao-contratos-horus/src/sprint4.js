/* ================= Sprint 4 · Reajuste, repactuação e reequilíbrio ================= */
const RC_LIMITE = 0.25;   // Lei nº 14.133/2021, art. 125: acréscimo e supressão até 25%
const RC_TIPOS_AJUSTE = {reajuste: "Reajuste", repactuacao: "Repactuação", reequilibrio: "Reequilíbrio econômico-financeiro"};
const RC_FLUXO = ["solicitado", "em análise", "aprovado", "aplicado"];

// memória de cálculo: valor anterior, percentual e valor novo, com centavos inteiros
function rcMemoria(valor_anterior_c, percentual){
  const novo = Math.round(valor_anterior_c * (1 + Number(percentual) / 100));
  return {anterior_c: valor_anterior_c, percentual: Number(percentual), novo_c: novo, diferenca_c: novo - valor_anterior_c};
}
teste("Sprint 4: a memória de cálculo aplica o percentual sobre o valor anterior", ()=>{
  const m = rcMemoria(1000000, 5); return m.novo_c === 1050000 && m.diferenca_c === 50000;
});
// limites legais de acréscimo e supressão
function rcLimite(valor_original_c, valor_novo_c){
  const delta = (valor_novo_c - valor_original_c) / valor_original_c;
  return {delta, pct: Math.round(delta * 1000) / 10, excede: Math.abs(delta) > RC_LIMITE};
}
teste("Sprint 4: acima de 25% excede o limite legal", ()=>{
  return rcLimite(1000000, 1200000).excede === false && rcLimite(1000000, 1300000).excede === true
    && rcLimite(1000000, 700000).excede === true;
});

async function rcReajustes(id){ return (await db.porIndice("reajustes", "contrato_id", id)).sort((a, b)=>(b.data || "").localeCompare(a.data || "")); }
async function rcFiscais(id){ return (await db.porIndice("fiscais", "contrato_id", id)).sort((a, b)=>(b.desde || "").localeCompare(a.desde || "")); }

const rcFichaAntiga = TELAS["#/contrato/:id"], rcFichaAntigaDepois = TELAS_DEPOIS["#/contrato/:id"];
TELAS["#/contrato/:id"] = async (p)=>{
  let html = await rcFichaAntiga(p);
  const c = await db.get("contratos", p.id); if (!c) return html;
  const [aj, fiscais] = await Promise.all([rcReajustes(p.id), rcFiscais(p.id)]);
  const card = `<div class="card" id="rcAjustes"><h2 style="margin-top:0">Reajuste, repactuação e reequilíbrio</h2>
    <p class="sub">Acréscimo ou supressão acima de 25% excede o limite legal (art. 125 da Lei nº 14.133/2021).</p>
    <form id="formRcAjuste"><div class="campos">
      ${campo("rcAjTipo", "Tipo", {tipo: "select", opcoes: Object.entries(RC_TIPOS_AJUSTE)})}
      ${campo("rcAjPercentual", "Percentual (%)", {tipo: "number", attrs: 'step="0.01"'})}
      ${campo("rcAjIndice", "Índice ou fundamento", {ajuda: "Ex.: IPCA, INCC, art. 25, III."})}</div>
      ${campo("rcAjMemoria", "Memória de cálculo (mínimo de 20 caracteres)", {tipo: "textarea", linhas: 3})}
      <div id="rcErrosAjuste"></div>
      <div class="linha-botoes"><button class="prim" type="submit">Registrar o pedido</button></div></form>
    ${aj.length ? `<div class="tabela-wrap"><table id="tabelaAjustes"><tr><th>Tipo</th><th class="num">%</th><th class="num">Valor</th><th>Situação</th><th>Autor</th><th></th></tr>
      ${aj.map(a=>{ const i = RC_FLUXO.indexOf(a.status); return `<tr><td>${esc(RC_TIPOS_AJUSTE[a.tipo] || a.tipo)}</td><td class="num">${a.percentual}</td>
        <td class="num">${dinheiro.fmt(a.valor_novo_c)}</td><td><span class="selo ${a.status === "aplicado" ? "ok" : a.status === "aprovado" ? "info" : "alerta"}">${esc(a.status)}</span></td>
        <td>${esc(a.autor)}</td><td>${i < RC_FLUXO.length - 1 ? `<button data-rc-avancar="${esc(a.id)}">${RC_FLUXO[i + 1]}</button>` : ""}</td></tr>`; }).join("")}</table></div>` : ""}
    </div>
    <div class="card" id="rcFiscais"><h2 style="margin-top:0">Fiscais do contrato</h2>
      <ul class="check-lista">${fiscais.map(f=>`<li class="${f.ate ? "falta" : "feito"}">${icone(f.ate ? "alerta" : "check")}
        <span><b>${esc(f.nome)}</b> · desde ${dataCurtaBR(f.desde)}${f.ate ? ` · até ${dataCurtaBR(f.ate)}` : " · atual"}${f.motivo ? ` · ${esc(f.motivo)}` : ""}</span></li>`).join("")
        || '<li class="vazio">Nenhum fiscal registrado.</li>'}</ul>
      <form id="formRcFiscal" class="campos" style="align-items:end">
        ${campo("rcFisNome", "Novo fiscal", {})}<div class="campo"><label>&nbsp;</label><button id="btnRcFiscal">Substituir o fiscal</button></div></form></div>`;
  return html + card;
};
TELAS_DEPOIS["#/contrato/:id"] = async (p)=>{
  await rcFichaAntigaDepois(p);
  $("#formRcAjuste")?.addEventListener("submit", async e=>{
    e.preventDefault();
    const c = await db.get("contratos", p.id), pct = Number(valorDe("rcAjPercentual")), memoria = valorDe("rcAjMemoria");
    const erros = [];
    if (!pct) erros.push("Informe o percentual.");
    if (memoria.length < 20) erros.push("Escreva a memória de cálculo (20 caracteres).");
    const m = rcMemoria(Number(c.valor_c || 0), pct);
    const lim = rcLimite(Number(c.valor_c || 0), m.novo_c);
    if (lim.excede) erros.push(`O percentual de ${lim.pct}% excede o limite legal de 25% (art. 125).`);
    if (!mostrarErros("#rcErrosAjuste", erros)) return;
    await db.put("reajustes", {id: uuid(), contrato_id: p.id, tipo: valorDe("rcAjTipo"), percentual: pct, indice: valorDe("rcAjIndice"),
      valor_anterior_c: m.anterior_c, valor_novo_c: m.novo_c, diferenca_c: m.diferenca_c, memoria, status: "solicitado",
      autor: estado.perfil || "gestor", data: agora(), historico: [{status: "solicitado", data: agora(), perfil: estado.perfil}]});
    await rcAuditar(p.id, "ajuste solicitado", `${valorDe("rcAjTipo")} · ${pct}%`);
    await registrar("ajuste solicitado", {detalhe: `${c.numero} · ${pct}%`});
    toast("Pedido de ajuste registrado."); navegar();
  });
  $$("[data-rc-avancar]").forEach(b=>b.addEventListener("click", async ()=>{
    const a = await db.get("reajustes", b.dataset.rcAvancar);
    const i = RC_FLUXO.indexOf(a.status), novo = RC_FLUXO[i + 1];
    const hist = [...(a.historico || []), {status: novo, data: agora(), perfil: estado.perfil}];
    await db.put("reajustes", {...a, status: novo, historico: hist});
    if (novo === "aplicado"){
      const c = await db.get("contratos", a.contrato_id);
      await db.put("contratos", {...c, valor_c: a.valor_novo_c});
    }
    await rcAuditar(b.dataset.rcAvancar, `ajuste ${novo}`, a.tipo);
    await registrar("ajuste avançou", {detalhe: `${a.contrato_id} · ${novo}`});
    toast(`Ajuste ${novo}.`); navegar();
  }));
  $("#btnRcFiscal")?.addEventListener("click", async ()=>{
    const nome = valorDe("rcFisNome"); if (!nome) return toast("Informe o nome do fiscal.");
    for (const f of await rcFiscais(p.id)) if (!f.ate) await db.put("fiscais", {...f, ate: hojeISO()});
    await db.put("fiscais", {id: uuid(), contrato_id: p.id, nome, desde: hojeISO(), ate: null, motivo: "substituição"});
    await rcAuditar(p.id, "fiscal substituído", nome);
    toast("Fiscal substituído."); navegar();
  });
};

/* ================= Sprint 6 · Valor em risco e relatório ================= */
const rcPainelAntigo = TELAS["#/painel"];
TELAS["#/painel"] = async ()=>{
  let html = await rcPainelAntigo();
  const cs = await db.list("contratos"), hoje = hojeISO();
  const ativos = cs.filter(c=>!RC_FORA.includes(c.status));
  const emRisco = ativos.filter(c=>{ const d = rcDias(c.data_fim, hoje); return d >= 0 && d <= 90; });
  const valorRisco = emRisco.reduce((a, c)=>a + Number(c.valor_c || 0), 0);
  const tempos = ativos.map(c=>rcDias(c.data_fim, hoje)).filter(d=>d >= 0);
  const tempoMedio = tempos.length ? Math.round(tempos.reduce((a, b)=>a + b, 0) / tempos.length) : null;
  return html + `<div class="card" id="rcGestor"><h2 style="margin-top:0">Valor em risco e renovação (Sprint 6)</h2>
      <div class="grade">
        <div class="card kpi"><div class="v" data-rc-ind="risco">${dinheiro.fmt(Math.round(valorRisco))}</div><div class="r">valor em risco (90 dias)</div></div>
        <div class="card kpi"><div class="v" data-rc-ind="contratos">${emRisco.length}</div><div class="r">contratos na janela de 90 dias</div></div>
        <div class="card kpi"><div class="v" data-rc-ind="tempo">${tempoMedio === null ? "—" : tempoMedio + " dia(s)"}</div><div class="r">tempo médio até a renovação</div></div></div>
      <div class="linha-botoes nao-imprimir"><button class="prim" id="btnRcCsv">${icone("download")} Exportar CSV</button>
        <button onclick="window.print()">${icone("imprimir")} Imprimir em A4</button></div></div>`;
};
TELAS_DEPOIS["#/painel"] = ()=>{
  $("#btnRcCsv")?.addEventListener("click", async ()=>{
    const cs = await db.list("contratos");
    const linhas = [["contrato", "numero", "fornecedor", "objeto", "valor", "inicio", "fim", "dias", "faixa", "situacao"]].concat(
      cs.map(c=>[c.id_contrato, c.numero, c.fornecedor, c.objeto, Number(c.valor_c || 0), c.data_inicio, c.data_fim,
        rcDias(c.data_fim), rcFaixa(c)?.rotulo || "fora da contagem", c.status]));
    const csv = "﻿" + linhas.map(l=>l.map(x=>/[;"\n]/.test(String(x)) ? `"${String(x).replace(/"/g, '""')}"` : String(x)).join(";")).join("\r\n");
    baixar(`contratos-${hojeISO()}.csv`, csv, "text/csv;charset=utf-8");
    await registrar("relatório exportado", {detalhe: `${cs.length} contratos`});
  });
};
