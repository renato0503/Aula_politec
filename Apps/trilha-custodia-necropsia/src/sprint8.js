/* ================= Sprint 8 · Sistema de Controle de Necropsia (versão de 02/11/2026) =================
   Sete etapas, três perfis do projeto (Técnico, Médico Legista e Gestor ADM, além dos
   papéis antigos do CIOP e do plantão), confirmação de recebimento de lacre e de laudo
   só pelo Gestor ADM, assinatura no canvas, sepultamento pelo Estado com justificativa
   e Resumo por agente causal. As regras antigas continuam valendo. */

const TC_ETAPAS = [
  {n: 1, nome: "Acionamento"},
  {n: 2, nome: "Ocorrência e possível vítima"},
  {n: 3, nome: "Aguardando necropsia"},
  {n: 4, nome: "Necropsia em andamento"},
  {n: 5, nome: "Identificação"},
  {n: 6, nome: "Família e liberação"},
  {n: 7, nome: "Entrega do laudo à ADM"},
];
const TC_AGENTES = ["Causa natural", "Acidente", "Homicídio", "Suicídio", "Indeterminada", "Óbito administrativo"];
const TC_JUSTIFICATIVA_MIN = 20;

function tcEtapa(c){
  const n = Number(c?.etapa);
  if (Number.isFinite(n) && n >= 1) return Math.min(7, Math.max(1, Math.round(n)));
  if (c?.laudo?.recebido_em || c?.custodia_finalizada) return 7;
  if (c?.sepultamento || c?.familia?.liberado_em || c?.situacao === "liberado") return 7;
  if (c?.identificacao?.resultado === "obito_adm") return 6;
  if (c?.familia?.busca_iniciada_em) return 6;
  return 5;
}
function tcJustificativaOk(t){ return String(t || "").trim().length >= TC_JUSTIFICATIVA_MIN; }
function tcPodeReceber(perfil){ return perfil === "gestor"; }
function tcEtapaVisivel(perfil, etapa){ return perfil !== "medico" || etapa <= 5; }
function tcResumoPorAgente(cs){
  const mapa = new Map();
  for (const c of cs){
    const chave = c.agente_causal || "Não informado";
    const r = mapa.get(chave) || {total: 0, familia: 0, sepultado: 0, aguardando: 0, nao_reclamado: 0, finalizada: 0};
    r.total++;
    const destino = c.destino_final || (c.familia?.liberado_em ? "família" : c.sepultamento ? "sepultamento" : "");
    if (destino === "família") r.familia++;
    if (c.sepultamento) r.sepultado++;
    if (!c.identificado && !c.sepultamento && c.situacao !== "liberado") r.aguardando++;
    if (c.situacao === "não reclamado") r.nao_reclamado++;
    if (c.laudo?.recebido_em || c.custodia_finalizada) r.finalizada++;
    mapa.set(chave, r);
  }
  return [...mapa.entries()].sort((a, b)=>b[1].total - a[1].total || a[0].localeCompare(b[0]));
}

teste("Sprint 8: a justificativa do sepultamento exige 20 caracteres", ()=>
  !tcJustificativaOk("curta") && tcJustificativaOk("Justificativa registrada com vinte caracteres ou mais."));
teste("Sprint 8: só o Gestor ADM confirma recebimento", ()=>
  tcPodeReceber("gestor") && !tcPodeReceber("tecnico") && !tcPodeReceber("medico"));
teste("Sprint 8: o Médico Legista não vê as etapas 6 e 7", ()=>
  tcEtapaVisivel("medico", 5) && !tcEtapaVisivel("medico", 6) && !tcEtapaVisivel("medico", 7) && tcEtapaVisivel("tecnico", 7));
teste("Sprint 8: o Resumo por agente causal soma as colunas", ()=>{
  const r = tcResumoPorAgente([
    {agente_causal: "Acidente", identificado: true, familia: {liberado_em: "x"}, laudo: {recebido_em: "y"}},
    {agente_causal: "Acidente", identificado: false, situacao: "aguardando identificação"},
    {agente_causal: "Homicídio", identificado: false, sepultamento: {justificativa: "x"}, situacao: "liberado"},
  ]);
  const a = r.find(x=>x[0] === "Acidente")[1];
  return a.total === 2 && a.familia === 1 && a.aguardando === 1 && a.finalizada === 1
    && r.find(x=>x[0] === "Homicídio")[1].sepultado === 1;
});

async function tcAvancarEtapa(id, para, dados, acao){
  const c = await db.get("corpos", id);
  if (!c) throw new Error("Corpo não encontrado.");
  if (para > 7) para = 7;
  if (para !== tcEtapa(c) + 1) throw new Error("A etapa avança uma por vez.");
  await db.put("corpos", {...c, ...dados, etapa: para, etapa_em: agora()});
  await db.put("log", {id: uuid(), corpo_id: id, acao: acao || `etapa ${para}: ${TC_ETAPAS[para - 1].nome}`, perfil: estado.perfil || "", data_hora: agora()});
}

function tcAssinaturaHtml(id, rotulo){
  return `<div class="campo"><span class="rotulo">${esc(rotulo)}</span>
    <canvas id="${id}" width="560" height="150" style="width:100%;max-width:560px;height:150px;border:1px dashed var(--linha);border-radius:10px;touch-action:none;background:var(--superficie)" aria-label="${esc(rotulo)}"></canvas>
    <input type="hidden" id="${id}Valor">
    <div class="linha-botoes"><button type="button" class="sec" data-limpar="${id}">Limpar assinatura</button></div>
    <small class="sub" id="${id}Estado">Assine no campo com o dedo ou o mouse.</small></div>`;
}
function tcLigarAssinatura(id){
  const cv = $("#" + id); if (!cv) return;
  const ctx = cv.getContext("2d");
  ctx.lineWidth = 2.4; ctx.lineCap = "round"; ctx.lineJoin = "round"; ctx.strokeStyle = "#123b54";
  let desenhando = false;
  const pos = e => { const r = cv.getBoundingClientRect(); return {x: (e.clientX - r.left) * cv.width / r.width, y: (e.clientY - r.top) * cv.height / r.height}; };
  cv.addEventListener("pointerdown", e=>{ desenhando = true; cv.setPointerCapture(e.pointerId); const p = pos(e); ctx.beginPath(); ctx.moveTo(p.x, p.y); e.preventDefault(); });
  cv.addEventListener("pointermove", e=>{ if (!desenhando) return; const p = pos(e); ctx.lineTo(p.x, p.y); ctx.stroke(); e.preventDefault(); });
  const fim = ()=>{ if (!desenhando) return; desenhando = false; $("#" + id + "Valor").value = cv.toDataURL("image/png"); $("#" + id + "Estado").textContent = "Assinatura capturada."; };
  cv.addEventListener("pointerup", fim); cv.addEventListener("pointercancel", fim);
  $(`[data-limpar="${id}"]`)?.addEventListener("click", ()=>{ ctx.clearRect(0, 0, cv.width, cv.height); $("#" + id + "Valor").value = ""; $("#" + id + "Estado").textContent = "Assine no campo com o dedo ou o mouse."; });
}

const TC_EXAMES_COMPL = ["DNA", "odontologia legal", "antropologia forense"];
const tcTentativas = c => c?.identificacao?.tentativas || [];
// RN11: os métodos só se esgotam depois de pelo menos um exame complementar sem resultado
const tcPodeEsgotar = tent => (tent || []).some(t=>TC_EXAMES_COMPL.includes(t.metodo) && t.resultado !== "identificou");

function tcAcoesEtapa5(c){
  const pend = c.identificacao?.pendente, tent = tcTentativas(c);
  const hist = tent.length ? `<p class="sub" id="tcTentativas">Tentativas: ${tent.map(t=>`${esc(t.metodo)} (${esc(t.resultado)})`).join(" · ")}.</p>` : "";
  if (pend) return `${hist}<div class="card pendente" id="tcExamePendente"><b>Exame complementar em andamento:</b> ${esc(pend.metodo)}, solicitado em ${dataBR(pend.enviado_em)}.</div>
    <div class="campos">
    ${campo("tcResultadoExame", "Resultado do exame", {tipo: "select", opcoes: [["", "Escolha"], ["identificou", "Identificou a pessoa"], ["sem_resultado", "Não identificou"]]})}
    ${campo("tcNomeExame", "Nome (fictício)")}${campo("tcDocExame", "Documento (fictício)")}</div>
    <div class="linha-botoes"><button class="prim" id="btnTcResultadoExame">Registrar o resultado do exame</button></div>`;
  return `${hist}<p class="sub">A identificação começa pela necropapiloscopia. Sem resultado, o caso segue para exame complementar (DNA, odontologia legal ou antropologia forense). Os métodos só se esgotam depois de pelo menos um exame complementar.</p>
    <div class="campos">
    ${campo("tcResultadoIdent", "Resultado da identificação", {tipo: "select", opcoes: [["", "Escolha"], ["identificado", "Identificado"], ["exame", "Não identificado: encaminhar a exame complementar"], ["esgotado", "Métodos esgotados: não identificado"]]})}
    ${campo("tcMetodoIdent8", "Método usado ou exame solicitado", {tipo: "select", opcoes: [["", "Escolha"], ...TC_METODOS, ...TC_EXAMES_COMPL.filter(x=>!TC_METODOS.includes(x))]})}
    ${campo("tcNomeIdent8", "Nome (fictício)", {valor: c.nome || ""})}
    ${campo("tcDocIdent8", "Documento (fictício)", {valor: c.documento || ""})}</div>
    <div class="linha-botoes"><button class="prim" id="btnTcIdent8">Registrar o resultado</button></div>`;
}

function tcFunerariaCampos(pref){
  return `<div class="campos">${campo(pref + "Funeraria", "Funerária (fictícia)")}${campo(pref + "Auto", "Nº do Auto de Entrega da funerária")}</div>`;
}

function tcAcoesFamilia(c){
  const f = c.familia || {}, semIdent = !c.identificado;
  const partes = [];
  if (!semIdent && !f.encontrada && !f.busca_sem_sucesso) partes.push(`<p class="sub">${f.busca_iniciada_em ? "Busca de familiares em andamento desde " + dataBR(f.busca_iniciada_em) + "." : "A busca de familiares ainda não começou."}</p>
    <div class="linha-botoes">${f.busca_iniciada_em ? "" : '<button class="sec" id="btnTcFamBusca">Registrar o início da busca</button>'}</div>
    <div class="campos">${campo("tcFamNome", "Familiar localizado (fictício)")}${campo("tcFamParentesco", "Parentesco")}${campo("tcFamDoc", "Documento do familiar (fictício)")}</div>
    <div class="linha-botoes"><button class="prim" id="btnTcFamEncontrado">Familiar localizado</button><button class="sec" id="btnTcFamSem">Busca sem êxito (prazo esgotado)</button></div>`);
  if (!semIdent && f.encontrada && !f.liberado_em) partes.push(`<div id="tcBlocoFamilia"><h3>Liberação à família</h3>
    <p class="sub">Confira o familiar, capture a assinatura do termo de liberação e registre a funerária que retira o corpo.</p>
    ${tcAssinaturaHtml("tcAssinaturaFamilia", "Assinatura do familiar (termo de liberação)")}
    ${tcFunerariaCampos("tcFam")}
    <div class="linha-botoes"><button class="prim" id="btnTcLiberarFamilia">Registrar a liberação à família (etapa 7)</button></div></div>`);
  if ((semIdent || f.busca_sem_sucesso) && !c.sepultamento){
    const motivo = semIdent ? "Corpo não identificado depois dos exames complementares." : "Corpo identificado e não reclamado: busca de familiares sem êxito.";
    partes.push(`<div id="tcBlocoSepultamento"><h3>Decisão do Gestor ADM: sepultamento pelo Estado</h3>
    <p class="sub">${motivo} A decisão é do Gestor ADM, com justificativa de no mínimo ${TC_JUSTIFICATIVA_MIN} caracteres, número da autorização e Auto de Entrega da funerária.</p>
    ${tcPodeReceber(estado.perfil) ? `${campo("tcJustSepult", "Justificativa", {tipo: "textarea", linhas: 3, ajuda: `Mínimo de ${TC_JUSTIFICATIVA_MIN} caracteres.`})}
      <div class="campos">${campo("tcAutSepult", "Nº da autorização de sepultamento")}</div>
      ${tcFunerariaCampos("tcSep")}
      <div class="linha-botoes"><button class="prim" id="btnTcSepultar">Autorizar o sepultamento pelo Estado (etapa 7)</button></div>`
      : '<p class="alerta-txt" id="tcAguardaGestor">Aguardando a decisão do Gestor ADM.</p>'}</div>`);
  }
  return partes.join("") || '<p class="sub">Etapa concluída.</p>';
}

function tcAcoesLaudo(c){
  const l = c.laudo || {}, entregue = !!l.entregue_em, recebido = !!l.recebido_em;
  if (recebido) return `<p class="ok-txt"><b>Laudo recebido na ADM</b> em ${dataBR(l.recebido_em)}, por ${esc(l.recebido_por || "")}. A confirmação não pode ser desfeita.</p>`;
  if (entregue) return `<p class="sub">Entrega registrada por <b>${esc(l.entregue_por || "")}</b> em ${dataBR(l.entregue_em)}. O recebimento é confirmado apenas pelo Gestor ADM.</p>
     ${tcPodeReceber(estado.perfil) ? `${tcAssinaturaHtml("tcAssinaturaLaudo", "Assinatura de quem recebe na ADM")}
       <div class="linha-botoes"><button class="prim" id="btnTcReceberLaudo">Confirmar o recebimento (Gestor ADM)</button></div>`
      : '<p class="sub">Troque para o perfil Gestor ADM para confirmar o recebimento.</p>'}`;
  return `<div class="campos">${campo("tcLaudoEntreguePor", "Quem entrega o laudo", {valor: c.tecnico || ""})}${campo("tcLaudoRecebidoPor", "Quem recebe na ADM")}</div>
     <div class="linha-botoes"><button class="prim" id="btnTcEntregaLaudo">Registrar a entrega do laudo</button></div>`;
}

// RN10: a custódia só se encerra com destino do corpo, laudo recebido e todos os lacres recebidos
function tcPendenciasEncerramento(c, ls){
  const p = [];
  if (!c.destino_final) p.push("destino do corpo (liberação à família ou sepultamento pelo Estado)");
  if (!c.laudo?.recebido_em) p.push("laudo recebido pela ADM");
  const sem = (ls || []).filter(l=>!l.recebido_em).length;
  if (sem) p.push(`${sem} lacre(s) sem recebimento confirmado pela ADM`);
  return p;
}
async function tcTentarFinalizar(id){
  const c = await db.get("corpos", id);
  if (!c || c.custodia_finalizada) return false;
  if (tcPendenciasEncerramento(c, await tcLacres(id)).length) return false;
  await db.put("corpos", {...c, custodia_finalizada: true, finalizada_em: agora(), etapa: 7});
  await db.put("log", {id: uuid(), corpo_id: id, acao: "custódia finalizada", motivo: "destino, laudo e lacres confirmados", perfil: estado.perfil || "", data_hora: agora()});
  return true;
}

function tcCardEncerramento(c, ls){
  const sem = ls.filter(l=>!l.recebido_em).length;
  const itens = [
    [!!c.destino_final, c.destino_final ? `Destino do corpo: ${c.destino_final === "família" ? "liberado à família" : "sepultamento pelo Estado"}` : "Destino do corpo (etapa 6)"],
    [!!c.laudo?.recebido_em, c.laudo?.recebido_em ? `Laudo recebido pela ADM em ${dataBR(c.laudo.recebido_em)}` : "Laudo recebido pela ADM"],
    [!sem, ls.length ? `${ls.length - sem} de ${ls.length} lacre(s) recebidos pela ADM` : "Nenhum lacre registrado"],
  ];
  return `<div class="card" id="tcEncerramento"><h2 style="margin-top:0">Encerramento da custódia</h2>
    <p class="sub">O caso só se encerra quando as três condições estão confirmadas. Depois disso, nada é editado: correções entram como retificação.</p>
    <ul class="tc-checklist">${itens.map(([ok, t])=>`<li class="${ok ? "ok-txt" : "alerta-txt"}">${ok ? "✓" : "○"} ${esc(t)}</li>`).join("")}</ul>
    ${c.custodia_finalizada ? `<p class="ok-txt" id="tcFinalizada"><b>Custódia finalizada</b>${c.finalizada_em ? " em " + dataBR(c.finalizada_em) : ""}.</p>` : ""}</div>`;
}

function tcCardEtapas(c, ls){
  const e = tcEtapa(c), atual = TC_ETAPAS[e - 1];
  const recebidos = ls.filter(l=>l.recebido_em).length;
  const lacres = ls.length ? `<h3>Recebimento dos lacres pela ADM</h3>
    <table><tr><th>Código</th><th>Destino</th><th>Recebimento</th><th></th></tr>
    ${ls.map(l=>`<tr><td class="mono">${esc(l.codigo)}</td><td>${esc(l.destino)}</td>
      <td>${l.recebido_em ? `${dataBR(l.recebido_em)} · ${esc(l.recebido_por || "")}` : '<span class="alerta-txt">pendente</span>'}</td>
      <td>${!l.recebido_em && estado.perfil === "gestor" ? `<button class="sec" data-tc-receber-lacre="${esc(l.id_lacre)}">Confirmar recebimento</button>` : ""}</td></tr>`).join("")}
    </table><p class="sub">${recebidos} de ${ls.length} lacre(s) com recebimento confirmado. A confirmação é exclusiva do Gestor ADM e não pode ser desfeita.</p>` : "";
  const acoes7 = c.custodia_finalizada ? '<p class="ok-txt">Caso concluído.</p>'
    : `<p class="sub">Destino registrado. Falta: ${esc(tcPendenciasEncerramento(c, ls).join("; ") || "nada")}.</p>`;
  const laudo = e >= 5 ? `<div class="card" id="tcBlocoLaudo"><h2 style="margin-top:0">Laudo à ADM</h2>
    <p class="sub">O laudo nasce na necropsia e corre em paralelo ao destino do corpo. Ele pode ser entregue à ADM a partir da etapa 5.</p>${tcAcoesLaudo(c)}</div>` : "";
  return `<div class="card" id="tcEtapasCard"><h2 style="margin-top:0">Etapas do caso</h2>
    <p class="sub">Etapa atual: <b>${e}. ${esc(atual.nome)}</b>. ${c.etapa_em ? "Desde " + dataBR(c.etapa_em) + "." : ""}</p>
    <div class="etapas">${TC_ETAPAS.map(x=>`<span class="${x.n < e || c.custodia_finalizada ? "feita" : x.n === e ? "atual" : ""}" title="${esc(x.nome)}">${x.n}. ${esc(x.nome)}</span>`).join("")}</div>
    <div id="tcEtapaAcoes">${e === 1 ? `<p class="sub">Registre a ocorrência e a possível vítima para seguir.</p>
        ${campo("tcOcorrencia8", "Ocorrência e possível vítima", {tipo: "textarea", linhas: 3})}
        <div class="linha-botoes"><button class="prim" id="btnTcE2">Registrar a ocorrência (etapa 2)</button></div>`
      : e === 2 ? `<p class="sub">O corpo aguarda a fila da necropsia.</p><div class="linha-botoes"><button class="prim" id="btnTcE3">Enviar para a fila da necropsia (etapa 3)</button></div>`
      : e === 3 ? `<p class="sub">Necropsia ainda não iniciada.</p><div class="linha-botoes"><button class="prim" id="btnTcE4">Iniciar a necropsia (etapa 4)</button></div>`
      : e === 4 ? `<p class="sub">Necropsia em andamento. Os lacres coletados entram na aba Lacres.</p><div class="linha-botoes"><button class="prim" id="btnTcE5">Concluir a necropsia (etapa 5)</button></div>`
      : e === 5 ? tcAcoesEtapa5(c)
      : e === 6 ? tcAcoesFamilia(c)
      : acoes7}</div>
    <div id="tcErrosEtapa8"></div>${lacres}</div>${laudo}${e >= 5 ? tcCardEncerramento(c, ls) : ""}`;
}

const tcFichaEtapa7 = TELAS["#/corpo/:id"];
TELAS["#/corpo/:id"] = async p=>{
  const html = await tcFichaEtapa7(p);
  const c = await db.get("corpos", p.id); if (!c) return html;
  const ls = await tcLacres(p.id);
  return html + tcCardEtapas(c, ls);
};

const tcFichaDepoisEtapa7 = TELAS_DEPOIS["#/corpo/:id"];
TELAS_DEPOIS["#/corpo/:id"] = async p=>{
  await tcFichaDepoisEtapa7(p);
  const c = await db.get("corpos", p.id); if (!c) return;
  await tcAuditar(p.id, "consulta ao caso");
  tcLigarAssinatura("tcAssinaturaFamilia"); tcLigarAssinatura("tcAssinaturaLaudo");
  const erro = msg => mostrarErros("#tcErrosEtapa8", [msg]);

  const avancar = async (para, dados, acao)=>{
    try { await tcAvancarEtapa(p.id, para, dados, acao); toast("Etapa registrada."); navegar(); }
    catch(e){ erro(e.message); }
  };
  $("#btnTcE2")?.addEventListener("click", ()=>avancar(2, {ocorrencia: valorDe("tcOcorrencia8")}, "etapa 2: ocorrência registrada"));
  $("#btnTcE3")?.addEventListener("click", ()=>avancar(3, {}, "etapa 3: aguardando necropsia"));
  $("#btnTcE4")?.addEventListener("click", ()=>avancar(4, {}, "etapa 4: necropsia iniciada"));
  $("#btnTcE5")?.addEventListener("click", ()=>avancar(5, {}, "etapa 5: necropsia concluída"));
  $("#btnTcIdent8")?.addEventListener("click", async ()=>{
    const r = valorDe("tcResultadoIdent"), metodo = valorDe("tcMetodoIdent8");
    const at = await db.get("corpos", p.id), tent = tcTentativas(at);
    if (!r) return erro("Escolha o resultado da identificação.");
    if (r === "identificado"){
      const nome = valorDe("tcNomeIdent8");
      if (!nome) return erro("Informe o nome da pessoa identificada.");
      if (!metodo) return erro("Informe o método de identificação.");
      return avancar(6, {identificado: true, desconhecido: false, nome, documento: valorDe("tcDocIdent8"), metodo_identificacao: metodo, identificado_em: agora(),
        identificacao: {resultado: r, metodo, em: agora(), tentativas: [...tent, {metodo, resultado: "identificou", em: agora()}]}, situacao: "em custódia"}, `identificação por ${metodo}`);
    }
    if (r === "exame"){
      if (!TC_EXAMES_COMPL.includes(metodo)) return erro("Escolha o exame complementar: DNA, odontologia legal ou antropologia forense.");
      const anteriores = tent.length ? tent : [{metodo: "papiloscopia", resultado: "sem resultado", em: agora()}];
      try {
        await db.put("corpos", {...at, situacao: "aguardando identificação",
          identificacao: {resultado: "pendente", tentativas: anteriores, pendente: {metodo, enviado_em: agora()}}});
        await tcAuditar(p.id, `exame complementar solicitado: ${metodo}`); toast("Exame complementar registrado."); navegar();
      } catch(e){ erro(e.message); }
      return;
    }
    if (!tcPodeEsgotar(tent)) return erro("Encaminhe a pelo menos um exame complementar (DNA, odontologia legal ou antropologia forense) antes de declarar os métodos esgotados.");
    return avancar(6, {identificado: false, desconhecido: true, nome: "", documento: "",
      identificacao: {resultado: "nao_identificado", em: agora(), tentativas: tent}, situacao: "não identificado"}, "identificação: métodos esgotados, não identificado");
  });
  $("#btnTcResultadoExame")?.addEventListener("click", async ()=>{
    const at = await db.get("corpos", p.id), pend = at?.identificacao?.pendente, r = valorDe("tcResultadoExame");
    if (!pend) return;
    if (!r) return erro("Escolha o resultado do exame.");
    const tent = [...tcTentativas(at), {metodo: pend.metodo, resultado: r === "identificou" ? "identificou" : "sem resultado", em: agora()}];
    if (r === "identificou"){
      const nome = valorDe("tcNomeExame");
      if (!nome) return erro("Informe o nome da pessoa identificada.");
      return avancar(6, {identificado: true, desconhecido: false, nome, documento: valorDe("tcDocExame"), metodo_identificacao: pend.metodo, identificado_em: agora(),
        identificacao: {resultado: "identificado", metodo: pend.metodo, em: agora(), tentativas: tent}, situacao: "em custódia"}, `identificação por ${pend.metodo}`);
    }
    try {
      await db.put("corpos", {...at, identificacao: {resultado: "pendente", tentativas: tent}});
      await tcAuditar(p.id, `exame complementar sem resultado: ${pend.metodo}`); toast("Resultado registrado."); navegar();
    } catch(e){ erro(e.message); }
  });
  $("#btnTcFamBusca")?.addEventListener("click", async ()=>{
    try { const at = await db.get("corpos", p.id);
      await db.put("corpos", {...at, familia: {...(at.familia || {}), busca_iniciada_em: agora()}});
      await tcAuditar(p.id, "busca de familiares iniciada"); toast("Busca registrada."); navegar();
    } catch(e){ erro(e.message); }
  });
  $("#btnTcFamEncontrado")?.addEventListener("click", async ()=>{
    const nome = valorDe("tcFamNome"), parentesco = valorDe("tcFamParentesco"), documento = valorDe("tcFamDoc");
    if (!nome || !parentesco || !documento) return erro("Informe o familiar, o parentesco e o documento.");
    try { const at = await db.get("corpos", p.id);
      await db.put("corpos", {...at, familia: {...(at.familia || {}), encontrada: true, nome, parentesco, documento, busca_encerrada_em: agora()}});
      await tcAuditar(p.id, `familiar localizado: ${nome}`); toast("Familiar registrado."); navegar();
    } catch(e){ erro(e.message); }
  });
  $("#btnTcFamSem")?.addEventListener("click", async ()=>{
    try { const at = await db.get("corpos", p.id);
      await db.put("corpos", {...at, situacao: "não reclamado", familia: {...(at.familia || {}), encontrada: false, busca_sem_sucesso: true, busca_encerrada_em: agora()}});
      await db.put("log", {id: uuid(), corpo_id: p.id, acao: "situação: não reclamado", motivo: "busca de familiares sem êxito", perfil: estado.perfil || "", data_hora: agora()});
      toast("Busca encerrada sem familiar. O caso aguarda a decisão do Gestor ADM."); navegar();
    } catch(e){ erro(e.message); }
  });
  $("#btnTcLiberarFamilia")?.addEventListener("click", async ()=>{
    const at = await db.get("corpos", p.id), assinatura = valorDe("tcAssinaturaFamiliaValor");
    const fun = {nome: valorDe("tcFamFuneraria"), auto: valorDe("tcFamAuto"), data_hora: agora()};
    if (!at?.familia?.encontrada) return erro("Registre o familiar localizado antes da liberação.");
    if (!assinatura) return erro("Capture a assinatura do familiar no campo.");
    if (!fun.nome || !fun.auto) return erro("Informe a funerária e o número do Auto de Entrega.");
    try {
      const entrega = {responsavel: at.familia.nome, documento: at.familia.documento, data: agora()};
      await db.put("corpos", {...at, etapa: 7, etapa_em: agora(), situacao: "liberado", destino_final: "família",
        familia: {...at.familia, liberado_em: agora(), assinatura}, entrega, funeraria: fun});
      await db.put("log", {id: uuid(), corpo_id: p.id, acao: "liberação à família", motivo: `${entrega.responsavel} · funerária ${fun.nome} · auto ${fun.auto}`, perfil: estado.perfil || "", data_hora: agora()});
      await tcTentarFinalizar(p.id);
      toast("Liberação registrada."); navegar();
    } catch(e){ erro(e.message); }
  });
  $("#btnTcSepultar")?.addEventListener("click", async ()=>{
    const at = await db.get("corpos", p.id), just = valorDe("tcJustSepult"), aut = valorDe("tcAutSepult");
    const fun = {nome: valorDe("tcSepFuneraria"), auto: valorDe("tcSepAuto"), data_hora: agora()};
    if (!tcPodeReceber(estado.perfil)) return erro("Somente o Gestor ADM autoriza o sepultamento pelo Estado.");
    if (!tcJustificativaOk(just)) return erro(`A justificativa precisa de ${TC_JUSTIFICATIVA_MIN} caracteres ou mais.`);
    if (!aut) return erro("Informe o número da autorização de sepultamento.");
    if (!fun.nome || !fun.auto) return erro("Informe a funerária e o número do Auto de Entrega.");
    try {
      const sep = {justificativa: just, autorizacao: aut, autorizado_em: agora(), perfil: estado.perfil || ""};
      await db.put("corpos", {...at, etapa: 7, etapa_em: agora(), situacao: "liberado", destino_final: "sepultamento", sepultamento: sep, funeraria: fun});
      await db.put("log", {id: uuid(), corpo_id: p.id, acao: "sepultamento pelo Estado autorizado", motivo: `${aut} · ${just}`, perfil: estado.perfil || "", data_hora: agora()});
      await tcTentarFinalizar(p.id);
      toast("Sepultamento autorizado."); navegar();
    } catch(e){ erro(e.message); }
  });
  $("#btnTcEntregaLaudo")?.addEventListener("click", async ()=>{
    const por = valorDe("tcLaudoEntreguePor"), para = valorDe("tcLaudoRecebidoPor");
    if (!por || !para) return erro("Informe quem entrega e quem recebe o laudo.");
    try { const at = await db.get("corpos", p.id);
      await db.put("corpos", {...at, laudo: {entregue_por: por, recebido_por: para, entregue_em: agora()}});
      await tcAuditar(p.id, `laudo entregue à ADM por ${por}`); toast("Entrega do laudo registrada."); navegar();
    } catch(e){ erro(e.message); }
  });
  $("#btnTcReceberLaudo")?.addEventListener("click", async ()=>{
    const at = await db.get("corpos", p.id), assinatura = valorDe("tcAssinaturaLaudoValor");
    if (!tcPodeReceber(estado.perfil)) return erro("Somente o Gestor ADM confirma o recebimento.");
    if (!assinatura) return erro("Capture a assinatura de quem recebe na ADM.");
    if (at.laudo?.recebido_em) return erro("O recebimento do laudo já foi confirmado e não pode ser alterado.");
    try {
      await db.put("corpos", {...at, laudo: {...at.laudo, recebido_em: agora(), confirmado_perfil: estado.perfil, assinatura_recebimento: assinatura}});
      await db.put("log", {id: uuid(), corpo_id: p.id, acao: "laudo recebido pela ADM", motivo: at.laudo?.recebido_por || "", perfil: estado.perfil || "", data_hora: agora()});
      const fim = await tcTentarFinalizar(p.id);
      toast(fim ? "Recebimento confirmado. Custódia finalizada." : "Recebimento confirmado."); navegar();
    } catch(e){ erro(e.message); }
  });
  $$("[data-tc-receber-lacre]").forEach(b=>b.addEventListener("click", async ()=>{
    if (!tcPodeReceber(estado.perfil)) return erro("Somente o Gestor ADM confirma o recebimento.");
    const l = await db.get("lacres", b.dataset.tcReceberLacre); if (!l || l.recebido_em) return;
    await db.put("lacres", {...l, recebido_em: agora(), recebido_por: estado.perfil, recebido_perfil: estado.perfil});
    await tcAuditar(p.id, `lacre recebido pela ADM: ${l.codigo}`);
    const fim = await tcTentarFinalizar(p.id);
    toast(fim ? "Lacre recebido. Custódia finalizada." : "Recebimento do lacre confirmado."); navegar();
  }));

  if (estado.perfil === "medico"){
    const aviso = document.createElement("div");
    aviso.className = "card pendente"; aviso.id = "tcModoMedico";
    aviso.innerHTML = "<b>Perfil Médico Legista:</b> leitura até a etapa 5. As etapas 6 e 7, o laudo à ADM, o encerramento e as ações de escrita ficam bloqueados.";
    $("#conteudo").prepend(aviso);
    $$("#tcBlocoFamilia, #tcBlocoSepultamento, #tcBlocoLaudo, #tcEncerramento").forEach(x=>x.hidden = true);
    $$("#conteudo button").forEach(b=>{ if (!b.closest(".abas")) b.disabled = true; });
    $$("#conteudo input, #conteudo select, #conteudo textarea").forEach(x=>x.disabled = true);
  }
};

TELAS["#/resumo"] = async ()=>{
  const cs = await db.list("corpos"), linhas = tcResumoPorAgente(cs);
  const total = linhas.reduce((a, x)=>({total: a.total + x[1].total, familia: a.familia + x[1].familia,
    sepultado: a.sepultado + x[1].sepultado, aguardando: a.aguardando + x[1].aguardando,
    nao_reclamado: a.nao_reclamado + x[1].nao_reclamado, finalizada: a.finalizada + x[1].finalizada}),
    {total: 0, familia: 0, sepultado: 0, aguardando: 0, nao_reclamado: 0, finalizada: 0});
  return `<h1>Resumo por agente causal</h1><p class="sub">Distribuição dos corpos e situação administrativa por agente causal. Os números saem dos registros do app.</p>
    <div class="grade">${[["total", "corpos"], ["familia", "liberados para a família"], ["sepultado", "sepultados pelo Estado"], ["aguardando", "aguardando identificação"], ["nao_reclamado", "identificados não reclamados"], ["finalizada", "custódia finalizada"]]
      .map(([k, t])=>`<div class="card kpi"><div class="v" data-tc-resumo="${k}">${total[k]}</div><div class="r">${t}</div></div>`).join("")}</div>
    <div class="card tabela-wrap"><h2 style="margin-top:0">Por agente causal</h2>
      <table id="tcTabelaResumo"><tr><th>Agente causal</th><th class="num">Total</th><th class="num">Família</th><th class="num">Sepultados</th><th class="num">Aguardando identificação</th><th class="num">Não reclamados</th><th class="num">Custódia finalizada</th></tr>
      ${linhas.map(([ag, r])=>`<tr><td>${esc(ag)}</td><td class="num">${r.total}</td><td class="num">${r.familia}</td><td class="num">${r.sepultado}</td>
        <td class="num">${r.aguardando}</td><td class="num">${r.nao_reclamado}</td><td class="num">${r.finalizada}</td></tr>`).join("")
        || '<tr><td colspan="7" class="vazio">Nenhum corpo registrado.</td></tr>'}</table></div>`;
};
