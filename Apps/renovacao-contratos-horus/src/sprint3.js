/* ================= Sprint 3 · Checklist de instrução, repositório de documentos e aviso de 60 dias ================= */
/* Itens do checklist de instrução do processo de renovação (R7). */
const RC_ITENS = [
  {id: "solicitacao", titulo: "Solicitação de renovação assinada", obrigatorio: true},
  {id: "justificativa", titulo: "Justificativa da necessidade", obrigatorio: true},
  {id: "regularidade", titulo: "Certidão de regularidade fiscal", obrigatorio: true},
  {id: "trabalhista", titulo: "Certidão de débitos trabalhistas", obrigatorio: true},
  {id: "parecer", titulo: "Parecer jurídico", obrigatorio: true},
  {id: "minuta", titulo: "Minuta do termo aditivo", obrigatorio: true},
  {id: "publicacao", titulo: "Publicação do aditivo", obrigatorio: false},
];
const RC_VISIBILIDADES = {todos: "Todos os perfis", gestao: "Somente gestão e administrador"};

/* R7: a instrução está completa quando todos os itens obrigatórios foram marcados */
function rcFaltando(itens){
  const feitos = new Set((itens || []).filter(i=>i.feito).map(i=>i.item));
  return RC_ITENS.filter(i=>i.obrigatorio && !feitos.has(i.id)).map(i=>i.titulo);
}
function rcProgresso(itens){
  const feitos = (itens || []).filter(i=>i.feito).length;
  return {feitos, total: RC_ITENS.length, pct: Math.round(feitos / RC_ITENS.length * 100), completa: rcFaltando(itens).length === 0};
}
teste("R7: a instrução só fica completa com todos os itens obrigatórios marcados", ()=>{
  const todos = RC_ITENS.map(i=>({item: i.id, feito: true}));
  const semParecer = todos.filter(i=>i.item !== "parecer");
  return rcFaltando(todos).length === 0 && rcFaltando(semParecer).join() === "Parecer jurídico" && rcProgresso(semParecer).pct === 86;
});
teste("R7: item facultativo não entra na falta", ()=>{
  const itens = RC_ITENS.filter(i=>i.obrigatorio).map(i=>({item: i.id, feito: true}));
  return rcFaltando(itens).length === 0;
});

/* R8: o fiscal não vê o que é restrito à gestão */
function rcPodeVerAnexo(a, perfil){ return a.visibilidade !== "gestao" || perfil === "gestor" || perfil === "admin"; }
// aviso: contrato que vence em 60 dias e ainda não tem instrução completa
function rcSemInstrucao(c, itens, hoje = hojeISO()){
  if (RC_FORA.includes(c.status)) return false;
  const d = rcDias(c.data_fim, hoje);
  return d >= 0 && d <= 60 && !rcProgresso(itens).completa;
}
teste("Aviso de 60 dias: só entra o contrato vigente, não instruído e perto do fim", ()=>{
  const c = {data_fim: "2026-11-20", status: "Vigente"}, vazio = [], pronto = RC_ITENS.map(i=>({item: i.id, feito: true}));
  const hoje = "2026-10-29";
  return rcSemInstrucao(c, vazio, hoje) && !rcSemInstrucao(c, pronto, hoje) && !rcSemInstrucao({...c, status: "Encerrado"}, vazio, hoje)
    && !rcSemInstrucao({data_fim: "2027-05-20", status: "Vigente"}, vazio, hoje);
});

async function rcItens(contrato_id){ return (await db.porIndice("instrucao", "contrato_id", contrato_id)).sort((a, b)=>a.ordem - b.ordem); }
async function rcAnexos(contrato_id){ return (await db.porIndice("anexos", "contrato_id", contrato_id)).sort((a, b)=>(b.data_hora || "").localeCompare(a.data_hora || "")); }

/* ---------- painel: instrução e aviso de 60 dias ---------- */
const rcPainelS2 = TELAS["#/painel"];
TELAS["#/painel"] = async ()=>{
  let html = await rcPainelS2();
  const cs = await db.list("contratos"), hoje = hojeISO();
  const semInstrucao = [];
  for (const c of cs){ const itens = await rcItens(c.id_contrato); if (rcSemInstrucao(c, itens, hoje)) semInstrucao.push({c, itens}); }
  const bloco = `<div class="card" id="rcAvisoInstrucao"><h2 style="margin-top:0">Aviso de instrução (Sprint 3)</h2>
    <p class="sub">Contrato que vence em até 60 dias e ainda não tem a instrução completa. Um item facultativo não conta como falta.</p>
    ${semInstrucao.length ? `<table id="tabelaAviso"><tr><th>Contrato</th><th>Fornecedor</th><th>Término</th><th class="num">Dias</th><th>Instrução</th></tr>
      ${semInstrucao.sort((a, b)=>a.c.data_fim.localeCompare(b.c.data_fim)).map(({c, itens})=>{ const pr = rcProgresso(itens);
        return `<tr><td><a href="#/contrato/${encodeURIComponent(c.id_contrato)}">${esc(c.numero)}</a></td><td>${esc(c.fornecedor)}</td>
          <td>${dataCurtaBR(c.data_fim)}</td><td class="num">${rcDias(c.data_fim, hoje)}</td>
          <td><div class="barra ${pr.completa ? "ok" : "alerta"}"><i style="width:${pr.pct}%"></i></div> <span class="sub">${pr.feitos}/${pr.total}</span></td></tr>`; }).join("")}</table>`
      : '<p class="sub">Nenhum contrato vence nos próximos 60 dias sem instrução completa.</p>'}
    <div class="linha-botoes"><a class="botao prim" href="#/instrucao">Ver as instruções</a></div></div>`;
  return html + bloco;
};

/* ---------- tela de instrução ---------- */
TELAS["#/instrucao"] = async ()=>{
  const cs = (await db.list("contratos")).filter(c=>!RC_FORA.includes(c.status)).sort((a, b)=>a.data_fim.localeCompare(b.data_fim));
  const linhas = [];
  for (const c of cs){ const itens = await rcItens(c.id_contrato); linhas.push({c, pr: rcProgresso(itens), falta: rcFaltando(itens).length}); }
  return `<h1>Instrução dos contratos</h1>
    <p class="sub">Checklist padrão do processo de renovação. A instrução está completa quando todos os itens obrigatórios estão marcados.</p>
    <div class="card tabela-wrap"><table id="tabelaInstrucao"><tr><th>Contrato</th><th>Fornecedor</th><th>Término</th><th>Itens</th><th>Situação</th><th></th></tr>
      ${linhas.map(({c, pr, falta})=>`<tr><td><a href="#/contrato/${encodeURIComponent(c.id_contrato)}">${esc(c.numero)}</a></td><td>${esc(c.fornecedor)}</td>
        <td>${dataCurtaBR(c.data_fim)}</td><td class="num">${pr.feitos}/${pr.total}</td>
        <td>${pr.completa ? '<span class="selo ok">instrução completa</span>' : `<span class="selo alerta">faltam ${falta}</span>`}</td>
        <td><a href="#/contrato/${encodeURIComponent(c.id_contrato)}">abrir</a></td></tr>`).join("")}
      </table></div>`;
};

/* ---------- ficha do contrato: checklist e repositório de documentos ---------- */
const rcFichaS2 = TELAS["#/contrato/:id"], rcFichaDepoisS2 = TELAS_DEPOIS["#/contrato/:id"];
TELAS["#/contrato/:id"] = async ({id})=>{
  let html = await rcFichaS2({id});
  const c = await db.get("contratos", id);
  if (!c) return html;
  const itens = await rcItens(id), anexos = await rcAnexos(id), pr = rcProgresso(itens);
  const visiveis = anexos.filter(a=>rcPodeVerAnexo(a, estado.perfil));
  const card = `<div class="card" id="rcCardInstrucao"><h2 style="margin-top:0">Checklist de instrução (R7)</h2>
    <div class="linha-botoes"><span class="sub" style="margin:0 auto 0 0"><b id="rcProgresso">${pr.feitos}/${pr.total}</b> itens marcados (${pr.pct}%)</span>
      <div class="barra ${pr.completa ? "ok" : "alerta"}" style="max-width:260px"><i style="width:${pr.pct}%"></i></div></div>
    <ul class="check-lista" id="rcListaInstrucao">
      ${RC_ITENS.map(i=>{ const it = itens.find(x=>x.item === i.id); const feito = !!it?.feito;
        return `<li class="${feito ? "feito" : "falta"}">${icone(feito ? "check" : "alerta")}<span><b>${esc(i.titulo)}</b>
          ${i.obrigatorio ? '<span class="selo alerta">obrigatório</span>' : '<span class="selo info">facultativo</span>'}
          <br><small class="sub">${feito ? `Marcado em ${dataCurtaBR(it.data_hora)} por ${esc(it.responsavel || "—")}` : "Pendente"}</small></span>
          <button type="button" class="rcItem" data-item="${esc(i.id)}" data-obrigatorio="${i.obrigatorio ? "1" : "0"}" data-feito="${feito ? "1" : "0"}">${feito ? "Desmarcar" : "Marcar"}</button></li>`; }).join("")}
    </ul>
    ${pr.completa ? '<div class="card ok" style="margin-top:12px" id="rcInstrucaoOk"><b>Instrução completa.</b> Todos os itens obrigatórios estão marcados.</div>'
      : `<div class="card pendente" style="margin-top:12px"><b>Falta concluir a instrução:</b> ${rcFaltando(itens).map(esc).join(", ")}.</div>`}</div>
    <div class="card" id="rcCardAnexos"><h2 style="margin-top:0">Repositório de documentos (R8)</h2>
    <p class="sub">Os arquivos ficam neste navegador. O item restrito à gestão não aparece para o fiscal.</p>
    <form id="formRcAnexo" novalidate><div class="campos">
      ${campo("rcAnexoNome", "Nome do documento", {obrigatorio: true, ajuda: "Ex.: oficio-solicitacao.pdf"})}
      ${campo("rcAnexoVis", "Quem pode ver", {tipo: "select", opcoes: Object.entries(RC_VISIBILIDADES)})}</div>
      ${campo("rcAnexoTexto", "Conteúdo do documento (fictício)", {tipo: "textarea", linhas: 3, ajuda: "No protótipo, o conteúdo é texto guardado no navegador."})}
      <div id="rcErrosAnexo"></div><div class="linha-botoes"><button class="prim" type="submit">Guardar documento</button></div></form>
    <ul class="check-lista" id="rcListaAnexos">
      ${visiveis.map(a=>`<li class="feito">${icone("documento")}<span><b>${esc(a.nome)}</b> · ${dataCurtaBR(a.data_hora)} · ${esc(a.responsavel || "—")}
        <br><small class="sub">${esc(RC_VISIBILIDADES[a.visibilidade] || a.visibilidade)}${a.visibilidade === "gestao" ? " · restrito à gestão" : ""}</small>
        ${a.texto ? `<br><small class="sub">${esc(a.texto)}</small>` : ""}</span></li>`).join("")
      || '<li class="vazio">Nenhum documento visível para este perfil.</li>'}</ul></div>`;
  return html + card;
};
TELAS_DEPOIS["#/contrato/:id"] = async ({id})=>{
  await rcFichaDepoisS2({id});
  $$(".rcItem").forEach(b=>b.addEventListener("click", async ()=>{
    const itens = await rcItens(id), feito = b.dataset.feito !== "1", item = b.dataset.item;
    const antes = itens.find(x=>x.item === item);
    if (feito) await db.put("instrucao", {id_item: uuid(), contrato_id: id, item, ordem: RC_ITENS.findIndex(x=>x.id === item), feito: true, data_hora: agora(), responsavel: estado.perfil || "gestor"});
    else if (antes) await db.del("instrucao", antes.id_item);
    await rcAuditar(id, feito ? `item de instrução marcado: ${item}` : `item de instrução desmarcado: ${item}`);
    await registrar("instrução atualizada", {detalhe: `${id} · ${item}`});
    toast("Instrução atualizada."); navegar();
  }));
  $("#formRcAnexo")?.addEventListener("submit", async e=>{
    e.preventDefault();
    const nome = valorDe("rcAnexoNome"), erros = [];
    if (!nome) erros.push("Informe o nome do documento.");
    if (!mostrarErros("#rcErrosAnexo", erros)) return;
    await db.put("anexos", {id_anexo: uuid(), contrato_id: id, nome, visibilidade: valorDe("rcAnexoVis") || "todos", texto: valorDe("rcAnexoTexto"), data_hora: agora(), responsavel: estado.perfil || "gestor"});
    await rcAuditar(id, `documento guardado: ${nome}`);
    await registrar("documento guardado", {detalhe: `${id} · ${nome}`});
    toast("Documento guardado."); navegar();
  });
};
