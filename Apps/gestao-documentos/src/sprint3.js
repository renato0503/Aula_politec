/* ================= Sprint 3 · Minutas padronizadas, ofício e despacho, checklist de instrução (RN04) ================= */
/* Minutas do Gabinete. Cada minuta sai com os dados do processo (RN04). */
const GD_MINUTAS = {
  oficio_encaminhamento: {
    rotulo: "Ofício de encaminhamento",
    texto: p => `Ofício nº ${p.numero_processo}
À lotação ${p.lotacao}

Assunto: ${p.assunto}

Senhor(a) responsável,

Encaminhamos, para instrução e PROVIDÊNCIA, o processo nº ${p.numero_processo}, autuado em ${dataCurtaBR(p.data_autuacao)}, cujo requerente é ${p.requerente}.

O prazo para a instrução termina em ${dataCurtaBR(gdSomar(p.data_autuacao, Number(p.dias_prazo || GD_PRAZO)))}.

Atenciosamente,
${p.responsavel_nome || "Responsável pela instrução"}
Gabinete de Direção · POLITEC/MT`,
  },
  oficio_resposta: {
    rotulo: "Ofício de resposta ao requerente",
    texto: p => `Ofício nº ${p.numero_processo}
Ao(à) requerente ${p.requerente}

Assunto: resposta ao pedido referente ao processo nº ${p.numero_processo}

Senhor(a),

Informamos que o processo nº ${p.numero_processo}, autuado em ${dataCurtaBR(p.data_autuacao)}, encontra-se em andamento na lotação ${p.lotacao}.

${p.conclusao || "A decisão será comunicada assim que a instrução for concluída."}

Atenciosamente,
${p.responsavel_nome || "Responsável pela instrução"}
Gabinete de Direção · POLITEC/MT`,
  },
  despacho: {
    rotulo: "Despacho",
    texto: p => `Despacho no processo nº ${p.numero_processo}

Em ${dataCurtaBR(hojeISO())}.

1.ERVERBA-SE a análise do processo nº ${p.numero_processo}, autuado em ${dataCurtaBR(p.data_autuacao)}, requerente ${p.requerente}.
2. DETERMINA-SE a instrução pela lotação ${p.lotacao}, com prazo até ${dataCurtaBR(gdSomar(p.data_autuacao, Number(p.dias_prazo || GD_PRAZO)))}.
3. Após a instrução, retorno para decisão.

${p.responsavel_nome || "Responsável pela instrução"}
Gabinete de Direção · POLITEC/MT`,
  },
};
/* Checklist de instrução por etapa do processo. */
const GD_CHECKLIST = [
  {etapa: "Instrução", itens: ["Anexos conferidos com o processo", "Diligências solicitadas", "Parecer da área técnica", "Minuta de resposta preparada"]},
  {etapa: "Decisão", itens: ["Relatório de instrução na pasta", "Decisão da autoridade registrada", "Comunicação ao requerente"]},
];
/* RN04: a minuta só é emitida com os dados obrigatórios do processo preenchidos */
function gdFaltandoMinuta(p){
  const falta = [];
  if (!p.numero_processo) falta.push("número do processo");
  if (!p.assunto) falta.push("assunto");
  if (!p.requerente) falta.push("requerente");
  if (!p.lotacao) falta.push("lotação de destino");
  if (!p.responsavel) falta.push("responsável pela instrução");
  if (!p.data_autuacao) falta.push("data de autuação");
  return falta;
}
teste("RN04: a minuta exige número, assunto, requerente, lotação, responsável e data", ()=>{
  const completo = {numero_processo: "2026.0001-SD", assunto: "Pedido", requerente: "Requerente", lotacao: "Gabinete", responsavel: "U1", data_autuacao: "2026-10-01"};
  return gdFaltandoMinuta(completo).length === 0 && gdFaltandoMinuta({...completo, requerente: "", lotacao: ""}).join() === "requerente,lotação de destino";
});
teste("RN04: a minuta sai com os dados do processo dentro do texto", ()=>{
  const p = {numero_processo: "2026.0001-SD", assunto: "Pedido de informações", requerente: "Requerente Fictício", lotacao: "Gabinete de Direção",
    responsavel: "U1", data_autuacao: "2026-10-01", dias_prazo: 15};
  const t = GD_MINUTAS.oficio_encaminhamento.texto(p);
  return t.includes("2026.0001-SD") && t.includes("Pedido de informações") && t.includes("Requerente Fictício") && t.includes("Gabinete de Direção");
});
teste("Checklist: as duas etapas trazem os itens da instrução", ()=>{
  return GD_CHECKLIST.length === 2 && GD_CHECKLIST[0].itens.length === 4 && GD_CHECKLIST[1].itens.length === 3;
});

async function gdChecklist(processo_id){ return (await db.porIndice("checklist", "processo_id", processo_id)).sort((a, b)=>a.ordem - b.ordem); }
async function gdMinutas(processo_id){ return (await db.porIndice("minutas", "processo_id", processo_id)).sort((a, b)=>(b.data_hora || "").localeCompare(a.data_hora || "")); }

/* ---------- ficha do processo: minutas, checklist e emissão ---------- */
const gdFichaS2 = TELAS["#/processo/:id"], gdFichaDepoisS2 = TELAS_DEPOIS["#/processo/:id"];
const gdFichaDepoisS2Safe = typeof gdFichaDepoisS2 === "function" ? gdFichaDepoisS2 : async ()=>{};
TELAS["#/processo/:id"] = async ({id})=>{
  let html = await gdFichaS2({id});
  const p = await db.get("processos", id);
  if (!p) return html;
  const us = await gdUsuarios(), checklist = await gdChecklist(id), minutas = await gdMinutas(id);
  const falta = gdFaltandoMinuta(p);
  const card = `<div class="card" id="gdCardMinutas"><h2 style="margin-top:0">Minutas padronizadas (RN04)</h2>
    <p class="sub">A minuta sai preenchida com os dados do processo. Sem número, assunto, requerente, lotação, responsável e data, não há emissão.</p>
    ${falta.length ? `<div class="card pendente" id="gdErrosMinuta"><b>Minuta bloqueada (RN04):</b> falta ${falta.map(esc).join(", ")}.</div>` : ""}
    <form id="formGdMinuta" novalidate><div class="campos">
      ${campo("gdTipoMinuta", "Tipo de minuta", {tipo: "select", opcoes: Object.entries(GD_MINUTAS).map(([k, m])=>[k, m.rotulo])})}
      ${campo("gdConclusaoMinuta", "Conclusão (entra na minuta de resposta)", {tipo: "textarea", linhas: 2, ajuda: "Opcional; só o ofício de resposta usa."})}</div>
      <div id="gdErrosEmissao"></div><div class="linha-botoes"><button class="prim" type="submit">Emitir minuta</button></div></form>
    ${minutas.length ? `<ul class="check-lista" id="gdListaMinutas">${minutas.map(m=>`<li class="feito">${icone("documento")}
      <span><b>${esc(m.tipo_rotulo)}</b> · ${dataCurtaBR(m.data_hora)} · ${esc(m.perfil || "—")}
      <br><small class="sub">${esc(m.texto.split("\n")[0])}</small></span>
      <button type="button" class="gdMinutaAbrir" data-minuta="${esc(m.id_minuta)}">Abrir</button></li>`).join("")}</ul>` : '<p class="sub">Nenhuma minuta emitida.</p>'}
    <div id="gdMinutaAberta"></div></div>
    <div class="card" id="gdCardChecklist"><h2 style="margin-top:0">Checklist de instrução</h2>
    <p class="sub">Itens marcados por etapa. O item marcado não some quando a etapa avança.</p>
    ${GD_CHECKLIST.map(e=>`<h3>${esc(e.etapa)}</h3><ul class="check-lista" id="gdCheck_${e.etapa.replace(/\s/g, "_")}">
      ${e.itens.map((item, k)=>{ const c = checklist.find(x=>x.item === item); const feito = !!c?.feito;
        return `<li class="${feito ? "feito" : "falta"}">${icone(feito ? "check" : "alerta")}<span>${esc(item)}${feito ? ` · ${dataCurtaBR(c.data_hora)}` : ""}</span>
          <button type="button" class="gdCheckItem" data-etapa="${esc(e.etapa)}" data-item="${esc(item)}" data-feito="${feito ? "1" : "0"}">${feito ? "Desmarcar" : "Marcar"}</button></li>`; }).join("")}</ul>`).join("")}
    </div>`;
  return html + card;
};
TELAS_DEPOIS["#/processo/:id"] = async ({id})=>{
  await gdFichaDepoisS2Safe({id});
  $$(".gdCheckItem").forEach(b=>b.addEventListener("click", async ()=>{
    const itens = await gdChecklist(id), feito = b.dataset.feito !== "1", item = b.dataset.item, etapa = b.dataset.etapa;
    const antes = itens.find(x=>x.item === item);
    if (feito){
      const ordem = GD_CHECKLIST.findIndex(e=>e.etapa === etapa) * 10 + GD_CHECKLIST.find(e=>e.etapa === etapa).itens.indexOf(item);
      await db.put("checklist", {id_item: uuid(), processo_id: id, etapa, item, ordem, feito: true, data_hora: agora(), perfil: estado.perfil || ""});
    } else if (antes) await db.del("checklist", antes.id_item);
    await db.put("log", {id: uuid(), processo_id: id, tipo_evento: feito ? "checklist: item marcado" : "checklist: item desmarcado",
      descricao: `${etapa} · ${item}`, perfil: estado.perfil || "", data_hora: agora()});
    toast("Checklist atualizado."); navegar();
  }));
  $("#formGdMinuta")?.addEventListener("submit", async e=>{
    e.preventDefault();
    const p = await db.get("processos", id), tipo = valorDe("gdTipoMinuta"), us = await gdUsuarios();
    const falta = gdFaltandoMinuta(p);
    if (falta.length) return mostrarErros("#gdErrosEmissao", [`A minuta está bloqueada (RN04): falta ${falta.join(", ")}.`]);
    const modelo = GD_MINUTAS[tipo];
    if (!modelo) return mostrarErros("#gdErrosEmissao", ["Escolha o tipo de minuta."]);
    const completo = {...p, responsavel_nome: us[p.responsavel]?.nome || "", conclusao: valorDe("gdConclusaoMinuta")};
    const texto = modelo.texto(completo);
    await db.put("minutas", {id_minuta: uuid(), processo_id: id, tipo, tipo_rotulo: modelo.rotulo, texto, data_hora: agora(), perfil: estado.perfil || ""});
    await db.put("documentos", {id_documento: uuid(), processo_id: id, tipo_documento: modelo.rotulo, data_criacao: agora(), assinado: false});
    await db.put("log", {id: uuid(), processo_id: id, tipo_evento: "minuta emitida", descricao: `${modelo.rotulo} · ${p.numero_processo}`, perfil: estado.perfil || "", data_hora: agora()});
    await registrar("minuta emitida", {detalhe: `${p.numero_processo} · ${modelo.rotulo}`});
    toast("Minuta emitida."); navegar();
  });
  $$(".gdMinutaAbrir").forEach(b=>b.addEventListener("click", async ()=>{
    const m = await db.get("minutas", b.dataset.minuta);
    if (!m) return;
    $("#gdMinutaAberta").innerHTML = `<div class="documento-a4" id="gdMinutaTexto"><div class="doc-cab">Gabinete de Direção · POLITEC/MT<br>${esc(m.tipo_rotulo)}</div>
      <pre style="white-space:pre-wrap;font-family:Georgia,serif;font-size:15px;line-height:1.6">${esc(m.texto)}</pre></div>
      <div class="linha-botoes nao-imprimir"><button onclick="window.print()">Imprimir</button></div>`;
    $("#gdMinutaAberta").scrollIntoView({block: "nearest"});
  }));
};
