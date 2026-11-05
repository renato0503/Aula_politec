/* ================= Sprint 9 · Fluxograma da Silmara (05/11/2026) =================
   O fluxo segue o fluxograma revisado de `entregas/2026-11-05/`:
   - três perfis só (Técnico, Médico Legista e Gestor ADM);
   - identificação com laço de exame complementar (RN11), no sprint8.js;
   - sepultamento pelo Estado só por decisão do Gestor ADM, com autorização e funerária (RN09);
   - funerária com Auto de Entrega nos dois destinos;
   - laudo em paralelo e encerramento com três condições (RN10), no sprint8.js;
   - caso encerrado não se edita: correção entra como retificação (RN12), aqui;
   - a liberação só acontece pela etapa 6: os atalhos antigos dos Sprints 3 e 4 ficam fechados. */

const TC_RETIFICACOES = ["Familiar localizado após o sepultamento", "Correção de dado do corpo", "Correção da identificação",
  "Correção de lacre ou laudo", "Outra correção"];
const TC_RETIFICACAO_MIN = 20;

// RN12: retificação exige tipo, o que muda e motivo com 20 caracteres ou mais
function tcFaltaRetificacao(r){
  const falta = [];
  if (!TC_RETIFICACOES.includes(r?.tipo)) falta.push("o tipo da retificação");
  if (!String(r?.texto || "").trim()) falta.push("o que muda");
  if (String(r?.motivo || "").trim().length < TC_RETIFICACAO_MIN) falta.push(`o motivo, com ${TC_RETIFICACAO_MIN} caracteres ou mais`);
  return falta;
}
const tcPodeRetificar = c => !!(c?.custodia_finalizada || c?.sepultamento);

teste("Sprint 9: o app tem só os três perfis do projeto", ()=>
  (APP.perfis || []).map(p=>p.id).sort().join() === "gestor,medico,tecnico");
teste("Sprint 9 (RN10): a custódia só se encerra com destino, laudo e lacres", ()=>{
  const ok = {destino_final: "família", laudo: {recebido_em: "x"}};
  return tcPendenciasEncerramento(ok, [{recebido_em: "y"}]).length === 0
    && tcPendenciasEncerramento(ok, [{recebido_em: "y"}, {}]).length === 1
    && tcPendenciasEncerramento({laudo: {recebido_em: "x"}}, []).length === 1
    && tcPendenciasEncerramento({destino_final: "sepultamento"}, []).length === 1;
});
teste("Sprint 9 (RN11): métodos só se esgotam depois de exame complementar", ()=>
  !tcPodeEsgotar([]) && !tcPodeEsgotar([{metodo: "papiloscopia", resultado: "sem resultado"}])
  && tcPodeEsgotar([{metodo: "papiloscopia", resultado: "sem resultado"}, {metodo: "DNA", resultado: "sem resultado"}]));
teste("Sprint 9 (RN12): retificação exige tipo, texto e motivo", ()=>
  tcFaltaRetificacao({tipo: "Outra correção", texto: "x", motivo: "curto"}).length === 1
  && tcFaltaRetificacao({tipo: TC_RETIFICACOES[0], texto: "Familiar procurou o IML", motivo: "Familiar localizado depois do sepultamento."}).length === 0);

function tcCardRetificacao(c){
  const lista = c.retificacoes || [];
  const pode = tcPodeRetificar(c) && ["tecnico", "gestor"].includes(estado.perfil);
  return `<div class="card" id="tcRetificacao"><h2 style="margin-top:0">Retificações</h2>
    <p class="sub">Depois do encerramento (ou do sepultamento), o caso não é editado. A correção entra como retificação: uma nova entrada no histórico, sem apagar a anterior.</p>
    ${lista.length ? `<ol class="linha-do-tempo" id="tcListaRetificacoes">${lista.map(r=>`<li><div class="ldt-quando">${dataBR(r.data_hora)} · ${esc(r.perfil)}</div>
      <b>${esc(r.tipo)}</b><div>${esc(r.texto)}</div><div class="sub" style="margin:0">Motivo: ${esc(r.motivo)}</div></li>`).join("")}</ol>` : '<p class="sub">Nenhuma retificação registrada.</p>'}
    ${pode ? `<div class="campos">${campo("tcRetTipo", "Tipo", {tipo: "select", opcoes: [["", "Escolha"], ...TC_RETIFICACOES.map(t=>[t, t])]})}</div>
      ${campo("tcRetTexto", "O que muda", {tipo: "textarea", linhas: 2})}
      ${campo("tcRetMotivo", "Motivo", {tipo: "textarea", linhas: 2, ajuda: `Mínimo de ${TC_RETIFICACAO_MIN} caracteres.`})}
      <div id="tcErrosRet"></div><div class="linha-botoes"><button class="prim" id="btnTcRetificar">Registrar a retificação</button></div>` : ""}</div>`;
}

const tcFichaS9 = TELAS["#/corpo/:id"], tcFichaS9Depois = TELAS_DEPOIS["#/corpo/:id"];
TELAS["#/corpo/:id"] = async p=>{
  const html = await tcFichaS9(p);
  const c = await db.get("corpos", p.id); if (!c) return html;
  return html + (tcPodeRetificar(c) || (c.retificacoes || []).length ? tcCardRetificacao(c) : "");
};
TELAS_DEPOIS["#/corpo/:id"] = async p=>{
  await tcFichaS9Depois(p);
  const c = await db.get("corpos", p.id); if (!c) return;

  // a liberação só acontece pela etapa 6 (assinatura, funerária e, no sepultamento, decisão do Gestor ADM)
  const form = $("#formTcAuto");
  if (form) form.outerHTML = '<p class="sub" id="tcLiberacaoNaEtapa">A liberação é registrada na etapa 6 do caso: termo assinado pelo familiar e Auto de Entrega da funerária, ou decisão do Gestor ADM para o sepultamento pelo Estado.</p>';
  $$('#tcNovaSit option[value="liberado"]').forEach(o=>{ if (c.situacao !== "liberado") o.remove(); });
  const blocoEntrega = $("#tcBlocoEntrega"); if (blocoEntrega) blocoEntrega.hidden = true;

  // RN12: caso encerrado não se edita
  if (c.custodia_finalizada){
    const aviso = document.createElement("div");
    aviso.className = "card"; aviso.id = "tcCasoEncerrado";
    aviso.innerHTML = "<b>Caso encerrado.</b> Os dados não podem ser editados. Correções entram como retificação.";
    $("#conteudo").prepend(aviso);
    $$("#conteudo button, #conteudo input, #conteudo select, #conteudo textarea").forEach(x=>{
      if (!x.closest(".abas-nav, [role=tablist], #tcRetificacao") && !x.matches("[data-aba]")) x.disabled = true;
    });
  }

  $("#btnTcRetificar")?.addEventListener("click", async ()=>{
    const at = await db.get("corpos", p.id);
    const r = {tipo: valorDe("tcRetTipo"), texto: valorDe("tcRetTexto"), motivo: valorDe("tcRetMotivo"), perfil: estado.perfil || "", data_hora: agora()};
    const falta = tcFaltaRetificacao(r);
    if (falta.length) return mostrarErros("#tcErrosRet", [`Informe ${falta.join(", ")}.`]);
    await db.put("corpos", {...at, retificacoes: [...(at.retificacoes || []), r]});
    await db.put("log", {id: uuid(), corpo_id: p.id, acao: `retificação: ${r.tipo}`, motivo: `${r.texto} · ${r.motivo}`, perfil: r.perfil, data_hora: r.data_hora});
    toast("Retificação registrada."); navegar();
  });
};
