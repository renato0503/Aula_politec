/* ================= Sprint 3 · Editor de mapa, anexo ao laudo e exportação em PDF (RN02, RN03) ================= */
/* Modelos de mapa temático aceitos pela_POLITEC (RN02). */
const PA_MODELOS = [
  {id: "delimitacao", rotulo: "Delimitação da área de dano", extra: "area_ha", rotulo_extra: "Área delimitada (ha)"},
  {id: "localizacao", rotulo: "Localização do evento", extra: "distancia_km", rotulo_extra: "Distância até o evento (km)"},
  {id: "ocupacao", rotulo: "Ocupação irregular", extra: "area_ha", rotulo_extra: "Área ocupada (ha)"},
  {id: "app", rotulo: "Faixa de APP e nascente", extra: "area_ha", rotulo_extra: "Área em APP (ha)"},
];
/* Elementos obrigatórios de todo mapa (RN02). */
const PA_ELEMENTOS = [
  {id: "norte", rotulo: "Indicação do norte"},
  {id: "escala", rotulo: "Escala gráfica"},
  {id: "legenda", rotulo: "Legenda"},
  {id: "data", rotulo: "Data do levantamento"},
  {id: "fonte", rotulo: "Fonte da imagem"},
];
const paModelo = id => PA_MODELOS.find(m => m.id === id) || PA_MODELOS[0];

// RN02: devolve a lista de elementos que faltam no mapa
function paMapaFaltando(m){
  const el = m?.elementos || {}, falta = [];
  for (const e of PA_ELEMENTOS) if (!String(el[e.id] || "").trim()) falta.push(e.rotulo);
  const mod = paModelo(m?.modelo_id);
  if (!String(m?.valor_extra || "").trim()) falta.push(mod.rotulo_extra);
  return falta;
}
function paMapaCompleto(m){ return paMapaFaltando(m).length === 0; }
// RN03: o laudo só exporta com cabeçalho completo e pelo menos 1 mapa anexado
function paPodeExportar(cab, mapas){ return cab.every(([, v])=>String(v || "").trim() && !/não informad/i.test(v)) && (mapas || []).length > 0; }
teste("RN02: mapa sem os elementos obrigatórios é recusado", ()=>{
  const vazio = {modelo_id: "delimitacao", elementos: {}, valor_extra: ""};
  return paMapaFaltando(vazio).length === PA_ELEMENTOS.length + 1;
});
teste("RN02: mapa com norte, escala, legenda, data, fonte e área passa", ()=>{
  const m = {modelo_id: "delimitacao", elementos: {norte: "N", escala: "1:25.000", legenda: "azul = dano", data: "2026-10-20", fonte: "satélite"}, valor_extra: "12,5"};
  return paMapaCompleto(m);
});
teste("RN03: sem cabeçalho completo ou sem mapa, a exportação não abre", ()=>{
  const cab = [["Número", "2026.000001-1"], ["Local", "não informadas"]];
  return !paPodeExportar(cab, [{id_mapa: "M1"}]) && !paPodeExportar([["Número", "1"], ["Local", "x"]], []) && paPodeExportar([["Número", "1"], ["Local", "x"]], [{id_mapa: "M1"}]);
});
function paElementos(m){
  const el = m.elementos || {};
  return PA_ELEMENTOS.map(e=>`<li class="${String(el[e.id] || "").trim() ? "feito" : "falta"}">${icone(String(el[e.id] || "").trim() ? "check" : "alerta")}
    <span><b>${esc(e.rotulo)}:</b> ${esc(el[e.id] || "não informado")}</span></li>`).join("");
}

async function paLaudoDe(id){
  const r = await db.get("requisicoes", id), ls = await db.porIndice("laudos", "requisicao_id", id);
  const l = ls[0] || {id_laudo: "L-" + id, status: "rascunho", horas_trabalhadas: 0};
  const mapas = l.id_laudo ? await db.porIndice("mapas", "laudo_id", l.id_laudo) : [];
  return {r, l, mapas};
}

/* ---------- ficha do laudo: conclusão, mapa e links do Sprint 3 ---------- */
const paLaudoS2 = TELAS["#/laudo/:id"], paLaudoDepoisS2 = TELAS_DEPOIS["#/laudo/:id"];
TELAS["#/laudo/:id"] = async ({id})=>{
  let html = await paLaudoS2({id});
  const {r, l, mapas} = await paLaudoDe(id);
  const completos = mapas.filter(paMapaCompleto).length;
  const card = `<div class="card" id="paCardMapa"><h2 style="margin-top:0">Mapas temáticos (RN02)</h2>
    <p class="sub">Cada mapa tem um modelo pré-definido e os elementos obrigatórios: ${PA_ELEMENTOS.map(e=>esc(e.rotulo.toLowerCase())).join(", ")}.</p>
    <div class="grade"><div class="card kpi"><div class="v">${mapas.length}</div><div class="r">mapas anexados</div></div>
      <div class="card kpi"><div class="v">${completos}</div><div class="r">mapas completos</div></div></div>
    ${mapas.length ? `<ul class="check-lista" id="paListaMapas">${mapas.map(m=>`<li class="${paMapaCompleto(m) ? "feito" : "falta"}">${icone(paMapaCompleto(m) ? "check" : "alerta")}
      <span><b>${esc(paModelo(m.modelo_id).rotulo)}</b> · ${dataCurtaBR(m.criado_em)} · ${esc(m.elementos?.legenda || "sem legenda")}</span></li>`).join("")}</ul>` : '<p class="sub">Nenhum mapa anexado.</p>'}
    <div class="linha-botoes"><a class="botao prim" href="#/mapa/${encodeURIComponent(id)}">${icone("mapa")} Criar mapa</a>
      <a class="botao" href="#/pdf/${encodeURIComponent(id)}">${icone("download")} Ver o laudo para impressão</a></div></div>
    <div class="card" id="paCardConclusao"><h2 style="margin-top:0">Conclusão do laudo</h2>
      <form id="formPaConclusao" novalidate>${campo("paConclusao", "Descrição da área e do dano (RN03)", {tipo: "textarea", linhas: 5, valor: l.conclusao || "", ajuda: "Esse texto vai para a versão impressa do laudo."})}
      <div id="paErrosConclusao"></div><div class="linha-botoes"><button class="prim" type="submit">Salvar conclusão</button></div></form></div>`;
  return html + card;
};
TELAS_DEPOIS["#/laudo/:id"] = async ({id})=>{
  await paLaudoDepoisS2({id});
  $("#formPaConclusao")?.addEventListener("submit", async e=>{
    e.preventDefault();
    const {l} = await paLaudoDe(id);
    await db.put("laudos", {...l, conclusao: valorDe("paConclusao")});
    await registrar("conclusão do laudo salva", {detalhe: l.id_laudo});
    toast("Conclusão salva."); navegar();
  });
};

/* ---------- editor de mapa (RN02) ---------- */
TELAS["#/mapa/:id"] = async ({id})=>{
  const {r, l} = await paLaudoDe(id);
  if (!r) return `<div class="card vazio">Requisição não encontrada. <a href="#/requisicoes">Voltar</a></div>`;
  return `<p class="sub nao-imprimir" style="margin-bottom:6px"><a href="#/laudo/${encodeURIComponent(id)}">← Laudo ${esc(l.id_laudo)}</a></p>
    <h1>Novo mapa temático</h1>
    <p class="sub">${esc(r.numero_processo)} · ${esc(r.tipo_infracao)} · ${esc(l.local || r.local)}</p>
    <form class="card" id="formPaMapa" novalidate><div class="campos">
      ${campo("paModelo", "Modelo do mapa (RN02)", {tipo: "select", opcoes: PA_MODELOS.map(m=>[m.id, m.rotulo])})}
      ${campo("paExtra", "Medida do modelo", {ajuda: "Preenchida conforme o modelo escolhido."})}</div>
    <fieldset class="card"><legend><b>Elementos obrigatórios (RN02)</b></legend>
      ${PA_ELEMENTOS.map(e=>campo("paEl_" + e.id, e.rotulo, {ajuda: "Vai impresso no mapa."})).join("")}</fieldset>
    <div id="paErrosMapa"></div><div class="linha-botoes"><button class="prim" type="submit">Anexar mapa ao laudo</button></div></form>`;
};
TELAS_DEPOIS["#/mapa/:id"] = ({id})=>{
  const extra = ()=>{ if (!$("#paExtra")) return; const mod = paModelo(valorDe("paModelo")); $("#paExtra").value = ""; $("#paExtra").previousElementSibling.textContent = mod.rotulo_extra; };
  $("#paModelo")?.addEventListener("change", extra); extra();
  $("#formPaMapa")?.addEventListener("submit", async e=>{
    e.preventDefault();
    const {l} = await paLaudoDe(id);
    const modelo_id = valorDe("paModelo"), mod = paModelo(modelo_id);
    const elementos = {};
    for (const el of PA_ELEMENTOS) elementos[el.id] = valorDe("paEl_" + el.id);
    const mapa = {id_mapa: uuid(), laudo_id: l.id_laudo, modelo_id, modelo: mod.rotulo, elementos, valor_extra: valorDe("paExtra"), criado_em: agora()};
    const falta = paMapaFaltando(mapa);
    if (!mostrarErros("#paErrosMapa", falta.map(x=>`Falta no mapa: ${x} (RN02).`))) return;
    await db.put("mapas", mapa);
    await registrar("mapa anexado ao laudo", {detalhe: `${l.id_laudo} · ${mod.rotulo}`});
    toast("Mapa anexado ao laudo."); location.hash = "#/laudo/" + encodeURIComponent(id);
  });
};

/* ---------- versão impressa (RN03) ---------- */
TELAS["#/pdf/:id"] = async ({id})=>{
  const {r, l, mapas} = await paLaudoDe(id);
  if (!r) return `<div class="card vazio">Requisição não encontrada. <a href="#/requisicoes">Voltar</a></div>`;
  const cab = paCabecalho(r, l), pode = paPodeExportar(cab, mapas), faltando = cab.filter(([, v])=>!String(v || "").trim() || /não informad/i.test(v)).map(([k])=>k);
  if (!pode){
    return `<p class="sub nao-imprimir" style="margin-bottom:6px"><a href="#/laudo/${encodeURIComponent(id)}">← Laudo ${esc(l.id_laudo)}</a></p>
      <h1>Laudo em PDF</h1>
      <div class="card pendente"><b>A exportação está bloqueada (RN03).</b>
        <ul>${faltando.map(k=>`<li>Cabeçalho incompleto: ${esc(k)}.</li>`).join("")}
        ${!mapas.length ? "<li>Nenhum mapa temático anexado.</li>" : ""}</ul>
        <p class="sub">A versão impressa sai com o cabeçalho completo e os mapas anexados.</p>
        <div class="linha-botoes"><a class="botao prim" href="#/mapa/${encodeURIComponent(id)}">Criar mapa</a></div></div>`;
  }
  return `<div class="linha-botoes nao-imprimir"><button class="prim" onclick="window.print()">${icone("imprimir")} Imprimir ou salvar em PDF</button>
    <a class="botao" href="#/laudo/${encodeURIComponent(id)}">Voltar ao laudo</a></div>
    <div class="documento-a4" id="paDocumento">
      <div class="doc-cab">Governo de Mato Grosso · SESP/MT · POLITEC/MT<br>Laudo pericial ambiental</div>
      <h2 style="text-align:center">LAUDO Nº ${esc(l.id_laudo)}</h2>
      <table style="font-family:var(--ui);font-size:13px">${cab.map(([k, v])=>`<tr><th style="width:38%">${esc(k)}</th><td>${esc(v)}</td></tr>`).join("")}</table>
      <h3>Conclusão</h3>
      <p>${esc(l.conclusao || "Conclusão não registrada.")}</p>
      <h3>Mapas anexados (${mapas.length})</h3>
      <ul>${mapas.map(m=>`<li>${esc(paModelo(m.modelo_id).rotulo)} — ${esc(m.valor_extra)} ${esc(paModelo(m.modelo_id).rotulo_extra.toLowerCase())}
        · ${esc(m.elementos.escala || "")} · ${esc(m.elementos.fonte || "")}</li>`).join("")}</ul>
      <p style="margin-top:40px">Politec/MT — Perícia Oficial e Identificação Técnica · Responsável: ${esc(l.tecnico || "—")}</p>
    </div>`;
};
