/* ================= Sprints 5, 7, 9 e 10 · parâmetros, gráficos do painel, cópia, LGPD e acessibilidade ================= */
"use strict";

/* ---------- RN09: varredura de CPF em texto livre ---------- */
const PADRAO_CPF = /\b\d{3}\.?\d{3}\.?\d{3}-?\d{2}\b/;
const temCPF = txt=> PADRAO_CPF.test(String(txt || ""));
teste("RN09: acha CPF com e sem pontuação", ()=> temCPF("servidor 529.982.247-25 levou") && temCPF("52998224725") && !temCPF("PAT-100000"));
// antes de qualquer formulário salvar, avisa se algum campo de texto traz um número com cara de CPF
document.addEventListener("submit", ev=>{
  const form = ev.target;
  if (!(form instanceof HTMLFormElement) || form.dataset.cpfOk === "1") return;
  const suspeitos = [...form.querySelectorAll("input[type=text], input:not([type]), textarea")].filter(c=> temCPF(c.value));
  if (!suspeitos.length) return;
  const nomes = suspeitos.map(c=> form.querySelector(`label[for="${c.id}"]`)?.textContent.replace(" *", "") || c.id).join(", ");
  if (!confirm(`O campo ${nomes} tem um número com formato de CPF. O app não guarda dado pessoal (RN09). Salvar mesmo assim?`)){
    ev.preventDefault(); ev.stopImmediatePropagation(); suspeitos[0].focus();
  }
}, true);

/* ---------- Sprint 5 e 9: parâmetros de custo, perfil da cópia, unidade dona e privacidade ---------- */
const PARAMETROS_EQ = [
  ["valor_referencia_atendimento", "Valor de referência por atendimento (R$)", "Entra no custo diário da parada (RN02): atendimentos perdidos x este valor."],
  ["custo_alternativo_padrao_dia", "Custo alternativo padrão por dia (R$)", "Terceirização ou deslocamento, quando a parada não informa o próprio valor."],
];
async function configExtra(){
  const [ps, unis, dona] = await Promise.all([db.list("parametros"), db.list("unidades"), db.meta("unidade_dona")]);
  const pv = chave=> ps.find(p=> p.chave === chave) || {};
  const linhas = PARAMETROS_EQ.map(([chave, rotulo, ajuda])=>{
    const p = pv(chave);
    return campo("par_" + chave, rotulo, {valor: p.valor ?? "", attrs:'inputmode="decimal"',
      ajuda: ajuda + (p.alterado_em ? ` Última alteração: ${dataBR(p.alterado_em)}${p.alterado_por ? " (" + p.alterado_por + ")" : ""}.` : " Ainda não alterado nesta cópia.")});
  }).join("");
  const coord = estado.perfil === "coordenadoria";
  return `<form class="card" id="formParametros"><h2 style="margin-top:0">Parâmetros de custo</h2>
      <p class="sub">A coordenadoria define os valores. Cada alteração fica com a data e entra no histórico.</p>
      <div class="campos">${linhas}</div>
      <div id="errosParametros"></div>
      <div class="linha-botoes"><button class="prim" type="submit" ${coord ? "" : "disabled"}>Salvar os parâmetros</button></div>
      ${coord ? "" : '<p class="sub">Só o perfil Coordenadoria altera os parâmetros.</p>'}</form>
    <div class="card"><h2 style="margin-top:0">Unidade dona desta cópia</h2>
      <p class="sub">Na cópia de uma unidade, os registros novos saem com a marca da unidade, e o <span class="mono">.json</span> enviado à coordenadoria vai só com ela.</p>
      <div class="campos">${campo("cfgUnidadeDona", "Unidade dona", {tipo:"select",
        opcoes:[["", "Nenhuma (cópia da coordenadoria)"], ...unis.filter(u=> !u.excluido).map(u=> [u.id, u.nome])], valor: dona || ""})}</div></div>
    <div class="card" id="privacidade"><h2 style="margin-top:0">Privacidade</h2>
      <p>O app guarda equipamentos, contratos, paradas e fotos dos equipamentos. Ele não guarda nome, CPF ou matrícula de servidor
        nem dado de pessoa atendida. Os dados ficam só neste navegador e saem apenas pelos arquivos que você baixar.</p>
      <p class="sub">Se um campo de texto receber um número com formato de CPF, o app avisa antes de salvar (RN09).
        Para limpar a cópia, use "Apagar todos os dados", no fim desta página.</p></div>`;
}
async function ligarConfigExtra(){
  $("#formParametros")?.addEventListener("submit", async ev=>{
    ev.preventDefault();
    const erros = [], novos = [];
    for (const [chave, rotulo] of PARAMETROS_EQ){
      const txt = valorDe("par_" + chave);
      const v = txt === "" ? 0 : (dinheiro.de(txt) ?? NaN) / 100;
      if (!Number.isFinite(v) || v < 0) erros.push(`${rotulo}: valor inválido.`);
      else novos.push([chave, v]);
    }
    if (!mostrarErros("#errosParametros", erros)) return;
    const ps = await db.list("parametros");
    for (const [chave, v] of novos){
      const ant = ps.find(p=> p.chave === chave) || {chave};
      if (Number(ant.valor) === v) continue;
      await db.put("parametros", {...ant, valor:v, alterado_em:agora(), alterado_por:estado.perfil || ""});
      await registrar("parâmetro alterado", {detalhe:chave, de:ant.valor ?? null, para:v});
    }
    toast("Parâmetros salvos."); navegar();
  });
  $("#cfgUnidadeDona")?.addEventListener("change", async e=>{
    await db.meta("unidade_dona", e.target.value || null);
    await registrar("unidade dona alterada", {detalhe:e.target.value || "coordenadoria"});
    toast(e.target.value ? "Esta cópia passou a ser da unidade escolhida." : "Esta cópia passou a ser da coordenadoria.");
  });
}

/* ---------- Sprint 7: gráficos em SVG próprio, fórmula no hover e KPI que filtra o mapa ---------- */
function svgBarras(itens, fmt){
  if (!itens.length) return '<p class="sub">Sem dados no período.</p>';
  const L = 640, alt = 26, rot = 190, H = itens.length * alt + 8, max = Math.max(1, ...itens.map(i=> i.v));
  const barras = itens.map((i, k)=>{
    const w = (L - rot - 110) * i.v / max, y = 4 + k * alt;
    return `<g><title>${esc(i.r)}: ${esc(fmt(i.v))}</title>
      <text x="${rot - 8}" y="${y + 16}" text-anchor="end" class="eq-g-rot">${esc(i.r.length > 28 ? i.r.slice(0, 27) + "…" : i.r)}</text>
      <rect x="${rot}" y="${y + 3}" width="${Math.max(1, w).toFixed(1)}" height="${alt - 9}" rx="3" class="eq-g-barra"></rect>
      <text x="${(rot + w + 6).toFixed(1)}" y="${y + 16}" class="eq-g-val">${esc(fmt(i.v))}</text></g>`;
  }).join("");
  return `<svg class="eq-grafico" viewBox="0 0 ${L} ${H}" role="img" aria-label="Gráfico de barras: custo de parada por unidade">${barras}</svg>`;
}
function svgLinha(pontos){
  if (!pontos.length) return '<p class="sub">Sem paradas no período.</p>';
  const L = 640, H = 200, m = {e:40, d:16, t:14, b:34}, max = Math.max(1, ...pontos.map(p=> p.v));
  const x = k=> m.e + (pontos.length === 1 ? (L - m.e - m.d) / 2 : k * (L - m.e - m.d) / (pontos.length - 1));
  const y = v=> m.t + (H - m.t - m.b) * (1 - v / max);
  const linha = pontos.map((p, k)=> `${k ? "L" : "M"}${x(k).toFixed(1)},${y(p.v).toFixed(1)}`).join("");
  const grade = [0, Math.ceil(max / 2), max].map(v=> `<line x1="${m.e}" x2="${L - m.d}" y1="${y(v).toFixed(1)}" y2="${y(v).toFixed(1)}" class="eq-g-grade"></line>
    <text x="${m.e - 6}" y="${(y(v) + 4).toFixed(1)}" text-anchor="end" class="eq-g-val">${v}</text>`).join("");
  const marcas = pontos.map((p, k)=> `<g><title>${esc(p.r)}: ${p.v} ${p.v === 1 ? "parada" : "paradas"}</title>
    <circle cx="${x(k).toFixed(1)}" cy="${y(p.v).toFixed(1)}" r="4" class="eq-g-ponto"></circle>
    <text x="${x(k).toFixed(1)}" y="${H - 12}" text-anchor="middle" class="eq-g-rot">${esc(p.r)}</text></g>`).join("");
  return `<svg class="eq-grafico" viewBox="0 0 ${L} ${H}" role="img" aria-label="Gráfico de linha: paradas por mês">${grade}<path d="${linha}" class="eq-g-linha"></path>${marcas}</svg>`;
}
const MESES_EQ = ["jan", "fev", "mar", "abr", "mai", "jun", "jul", "ago", "set", "out", "nov", "dez"];
function paradasPorMes(paradas, desde){
  const conta = {};
  for (const p of paradas){ const k = dataDe(p.inicio).slice(0, 7); if (k && k >= desde.slice(0, 7)) conta[k] = (conta[k] || 0) + 1; }
  const meses = [];
  const d = new Date(desde.slice(0, 7) + "-01T00:00:00"), fim = hojeISO().slice(0, 7);
  while (d.toISOString().slice(0, 7) <= fim){
    const k = `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, "0")}`;
    meses.push({r: `${MESES_EQ[d.getMonth()]}/${String(d.getFullYear()).slice(2)}`, v: conta[k] || 0});
    d.setMonth(d.getMonth() + 1);
    if (meses.length > 24) break;
  }
  return meses;
}
teste("paradas por mês conta no mês do início", ()=>{
  const m = paradasPorMes([{inicio: hojeISO()}, {inicio: hojeISO()}], hojeISO());
  return m.length === 1 && m[0].v === 2;
});

// a fórmula de cada KPI, com os parâmetros em uso, e o filtro do mapa que ele aplica
const KPI_EQ = {
  kpiSemContrato: {formula: "equipamentos sem contrato vigente (RN05) ÷ equipamentos ativos", filtro: {semContrato:true}},
  kpiPontos: {formula: "criticidade 4 ou 5 e sem redundância (RN01)", filtro: {pontoUnico:true}},
  kpiCusto: {formula: "Σ paradas do período: (atendimentos perdidos/dia × valor de referência + custo alternativo/dia) × dias úteis (RN02, RN03)", filtro: {parados:true}},
  kpiExposicao: {formula: "Σ custo diário dos pontos únicos de falha sem contrato", filtro: {pontoUnico:true, semContrato:true}},
  kpiMttr: {formula: "média, por equipamento, de (conclusão − abertura) das corretivas, em dias (RN06)"},
  kpiDisp: {formula: "1 − horas paradas ÷ horas úteis do período (RN07)"},
  kpiGasto: {formula: "Σ custo das manutenções abertas no período"},
};
const eqPainelAntes = TELAS["#/painel"];
TELAS["#/painel"] = async (p)=>{
  const html = await eqPainelAntes(p);
  const b = await baseDeCalculo();
  const dias = Number(estado.eqPeriodo || 90);
  const desde = new Date(Date.now() - dias * 86400000).toISOString().slice(0, 10);
  const porUnidade = {};
  for (const par of b.paradas.filter(x=> dataDe(x.inicio) >= desde)){
    const e = b.eqs.find(x=> x.id === par.equipamento_id); if (!e) continue;
    const perdidos = par.atendimentos_perdidos_dia ?? e.unidade.atendimentos_dia ?? 0;
    const alt = par.custo_alternativo_dia ?? b.params.custoAlt;
    const k = e.unidade.nome || "sem unidade";
    porUnidade[k] = (porUnidade[k] || 0) + (perdidos * b.params.valorRef + alt) * diasUteis(dataDe(par.inicio), par.fim ? dataDe(par.fim) : hojeISO());
  }
  const barras = Object.entries(porUnidade).map(([r, v])=> ({r, v})).sort((a, x)=> x.v - a.v);
  const graficos = `<div class="card"><h2 style="margin-top:0">Custo de parada por unidade</h2>
      ${svgBarras(barras, v=> dinheiro.fmt(Math.round(v)))}
      <p class="sub">Parâmetros em uso: ${dinheiro.fmt(Math.round(b.params.valorRef * 100))} por atendimento e ${dinheiro.fmt(Math.round(b.params.custoAlt * 100))} de custo alternativo por dia (editáveis em Configuração).</p></div>
    <div class="card"><h2 style="margin-top:0">Paradas por mês</h2>${svgLinha(paradasPorMes(b.paradas, desde))}</div>`;
  // troca o bloco de barras em HTML pelos gráficos em SVG
  const ini = html.indexOf('<div class="card"><h2 style="margin-top:0">Custo de parada por unidade</h2>');
  const fim = html.indexOf('<div class="card tabela-wrap"><h2>Pontos únicos', ini);
  const novo = ini >= 0 && fim > ini ? html.slice(0, ini) + graficos + html.slice(fim) : html + graficos;
  return novo.replace('<p class="sub">Os 7 indicadores', '<p class="sub">Passe o mouse num indicador para ver a fórmula. Clique para abrir o mapa com o filtro correspondente. Os 7 indicadores');
};
const eqPainelDepois = TELAS_DEPOIS["#/painel"];
TELAS_DEPOIS["#/painel"] = async (p)=>{
  await eqPainelDepois?.(p);
  for (const [id, k] of Object.entries(KPI_EQ)){
    const el = $("#" + id); if (!el) continue;
    el.title = "Fórmula: " + k.formula;
    el.setAttribute("aria-description", k.formula);
    if (!k.filtro) continue;
    el.classList.add("eq-kpi-link"); el.tabIndex = 0; el.setAttribute("role", "link");
    el.setAttribute("aria-label", `${el.querySelector(".r")?.textContent}: ${el.querySelector(".v")?.textContent}. Abrir no mapa.`);
    const ir = ()=>{
      estado.eqFiltroMapa = {semContrato:false, parados:false, pontoUnico:false, diretoria:"", tipo:"", ...k.filtro};
      location.hash = "#/mapa";
    };
    el.addEventListener("click", ir);
    el.addEventListener("keydown", e=>{ if (e.key === "Enter" || e.key === " "){ e.preventDefault(); ir(); } });
  }
};

/* ---------- Sprint 9: .json com ou sem fotos ---------- */
const eqExportarDepois = TELAS_DEPOIS["#/exportar"];
TELAS_DEPOIS["#/exportar"] = async (p)=>{
  await eqExportarDepois?.(p);
  const btn = $("#btnJsonUnidade"); if (!btn) return;
  btn.insertAdjacentHTML("afterend", `<label style="display:inline-flex;gap:6px;align-items:center"><input type="checkbox" id="jsonComFotos" style="width:auto" checked> com as fotos</label>`);
  // troca o ouvinte do botão: o novo considera a caixa "com as fotos" e a unidade dona
  const novo = btn.cloneNode(true); btn.replaceWith(novo);
  novo.addEventListener("click", async ()=>{
    const pacote = await db.exportar();
    const comFotos = $("#jsonComFotos").checked;
    const dona = await db.meta("unidade_dona");
    if (!comFotos){ pacote.dados.arquivos = []; for (const e of pacote.dados.equipamentos || []) e.foto_ids = []; }
    if (dona){
      const eqs = (pacote.dados.equipamentos || []).filter(e=> e.unidade_id === dona), ids = new Set(eqs.map(e=> e.id));
      pacote.dados.unidades = (pacote.dados.unidades || []).filter(u=> u.id === dona);
      pacote.dados.equipamentos = eqs;
      pacote.dados.paradas = (pacote.dados.paradas || []).filter(x=> ids.has(x.equipamento_id));
      pacote.dados.manutencoes = (pacote.dados.manutencoes || []).filter(x=> ids.has(x.equipamento_id));
    }
    // o arquivo com fotos leva os blobs em base64; o IndexedDB guarda o Blob
    if (comFotos) pacote.dados.arquivos = await Promise.all((pacote.dados.arquivos || []).map(async a=>
      a.blob instanceof Blob ? {...a, blob: undefined, base64: await blobParaBase64(a.blob), tipo: a.blob.type} : a));
    const nome = `mapa-equipamentos${dona ? "-unidade" : ""}${comFotos ? "" : "-sem-fotos"}.json`;
    baixar(nome, JSON.stringify(pacote, null, 2), "application/json");
    await registrar("JSON da base exportado", {detalhe:nome, com_fotos:comFotos});
    toast("Arquivo gerado: " + nome);
  });
};
function blobParaBase64(blob){
  return new Promise((ok, erro)=>{ const r = new FileReader(); r.onload = ()=> ok(String(r.result).split(",")[1] || ""); r.onerror = erro; r.readAsDataURL(blob); });
}
