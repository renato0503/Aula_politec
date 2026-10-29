/* ================= Sprint 3 · Etapas e prazos (RN02, RN03, RN04) ================= */
const ETAPAS_RNC = ["validação", "plano", "avaliação", "encerramento"];
const PRAZO_ETAPA = {validação: 5, plano: 30, avaliação: 10, encerramento: 5};
const etapasRnc = async n => (await db.porIndice("etapas", "rnc", n)).sort((a, b)=>(a.inicio + a.id).localeCompare(b.inicio + b.id));

// RN02: complemento pedido e não respondido em 5 dias anula a RNC (conferido sempre que a RNC é aberta)
async function aplicarPrazosRnc(r, hoje = hojeISO()){
  if (r.situacao === "aguardando complemento" && r.complemento_prazo && hoje > r.complemento_prazo){
    const e = (await etapasRnc(r.numero)).filter(x=>!x.fim).pop();
    if (e) await db.put("etapas", {...e, fim: r.complemento_prazo});
    r = {...r, situacao: "anulada", anulada_em: hoje, motivo_anulacao: "sem resposta ao pedido de complemento em 5 dias (RN02)"};
    await db.put("rncs", r); await registrar("RNC anulada (RN02)", {detalhe: r.numero});
  }
  return r;
}

async function acaoRnc(numero, acao, {data, texto, eficaz}){
  let r = await db.get("rncs", numero); const e = (await etapasRnc(numero)).filter(x=>!x.fim).pop();
  const abrir = async (etapa, prazoDias)=> db.put("etapas", {id: `${numero}#${Date.now().toString(36)}`, rnc: numero, etapa, inicio: data, fim: null, prazo: somarDiasRnc(data, prazoDias)});
  const fechar = async ()=>{ if (e){ if (data < e.inicio) throw new Error(`A data não pode ser antes do início da etapa (${dataCurtaBR(e.inicio)}).`); await db.put("etapas", {...e, fim: data}); } };
  if (["anulada", "encerrada", "encaminhada à corregedoria"].includes(r.situacao)) throw new Error(`A RNC está ${r.situacao}.`);
  switch (acao){
    case "aprovar": await fechar(); await abrir("plano", PRAZO_ETAPA.plano); r = {...r, etapa: "plano", situacao: "aberta"}; break;
    case "complemento":
      r = {...r, situacao: "aguardando complemento", complemento_pedido_em: data, complemento_prazo: somarDiasRnc(data, 5)};
      if (e) await db.put("etapas", {...e, prazo: somarDiasRnc(data, 5)}); break;
    case "complemento_recebido": r = {...r, situacao: "aberta", complemento_recebido_em: data}; break;
    case "prorrogar":
      if (!texto) throw new Error("A prorrogação precisa da justificativa (RN03).");
      if (r.etapa !== "plano" || !e) throw new Error("Só o prazo do plano de ação é prorrogado.");
      await db.put("etapas", {...e, prazo: somarDiasRnc(e.prazo, 15), prorrogado: true});
      await db.put("planos", {id: numero + "-plano", rnc: numero, ...(await db.get("planos", numero + "-plano") || {}), prorrogado_ate: somarDiasRnc(e.prazo, 15), justificativa_prorrogacao: texto});
      break;
    case "plano_recebido":
      await db.put("planos", {id: numero + "-plano", rnc: numero, ...(await db.get("planos", numero + "-plano") || {}), enviado_em: data, acoes: texto || ""});
      await fechar(); await abrir("avaliação", PRAZO_ETAPA.avaliação); r = {...r, etapa: "avaliação"}; break;
    case "avaliacao":
      await db.put("avaliacoes", {id: numero + "-aval", rnc: numero, eficaz: eficaz === "sim", observacao: texto || "", avaliado_em: data});
      await fechar(); await abrir("encerramento", PRAZO_ETAPA.encerramento); r = {...r, etapa: "encerramento"}; break;
    case "encerrar": await fechar(); r = {...r, situacao: "encerrada", encerrada_em: data}; break;
    case "grave":
      if (!texto) throw new Error("Registre o motivo do encaminhamento à corregedoria.");
      await fechar(); r = {...r, gravidade: "grave", situacao: "encaminhada à corregedoria", corregedoria_em: data, motivo_corregedoria: texto}; break;
    default: throw new Error("Ação desconhecida.");
  }
  await db.put("rncs", r); await registrar("RNC: " + acao, {detalhe: `${numero}${texto ? " · " + texto : ""}`});
}

const BOTOES_ETAPA = {
  "validação": [["aprovar", "Aprovar a RNC", "prim"], ["complemento", "Pedir complemento (5 dias)"], ["complemento_recebido", "Complemento recebido"]],
  "plano": [["plano_recebido", "Plano de ação recebido (FOR 2)", "prim"], ["prorrogar", "Prorrogar 15 dias"]],
  "avaliação": [["avaliacao", "Avaliação registrada (FOR 3)", "prim"]],
  "encerramento": [["encerrar", "Encerrar a RNC", "prim"]]
};
TELAS["#/rnc/:id"] = async ({id})=>{
  let r = await db.get("rncs", id);
  if (!r) return `<div class="card vazio">RNC não encontrada. <a href="#/painel">Voltar</a></div>`;
  r = await aplicarPrazosRnc(r);
  const es = await etapasRnc(id), hoje = hojeISO(), ativa = !["anulada", "encerrada", "encaminhada à corregedoria"].includes(r.situacao);
  const plano = await db.get("planos", id + "-plano"), aval = await db.get("avaliacoes", id + "-aval");
  return `<h1>RNC ${esc(r.numero)}</h1>
    <p class="sub">Aberta em ${dataCurtaBR(r.aberta_em)} · relator <b>${esc(r.setor_relator)}</b> · notificado <b>${esc(r.setor_notificado)}</b> · ${esc(r.categoria)} ·
      gravidade ${esc(r.gravidade)} · <span class="selo ${ativa ? "info" : r.situacao === "encerrada" ? "ok" : "erro"}" id="situacaoRnc">${esc(r.situacao)}</span></p>
    <div class="card"><h2 style="margin-top:0">Ocorrência</h2><p>${esc(r.descricao)}</p>${r.motivo_anulacao ? `<p class="erro-txt">${esc(r.motivo_anulacao)}</p>` : ""}
      ${r.motivo_corregedoria ? `<p class="erro-txt">Corregedoria: ${esc(r.motivo_corregedoria)}</p>` : ""}</div>
    <div class="card tabela-wrap"><h2 style="margin-top:0">Etapas</h2><table id="tabelaEtapas"><tr><th>Etapa</th><th>Início</th><th>Fim</th><th>Prazo</th><th>Situação</th></tr>
      ${es.map(e=>{ const venc = !e.fim && e.prazo < hoje; return `<tr><td>${esc(e.etapa)}</td><td>${dataCurtaBR(e.inicio)}</td><td>${dataCurtaBR(e.fim) || "—"}</td>
        <td>${dataCurtaBR(e.prazo)}${e.prorrogado ? ' <span class="selo alerta">prorrogado</span>' : ""}</td>
        <td>${e.fim ? '<span class="selo ok">concluída</span>' : venc ? '<span class="selo erro">vencida</span>' : '<span class="selo info">em andamento</span>'}</td></tr>`; }).join("")}</table>
      ${plano ? `<p><b>Plano (FOR 2):</b> ${plano.enviado_em ? "recebido em " + dataCurtaBR(plano.enviado_em) : "aguardando"}${plano.prorrogado_ate ? ` · prorrogado até ${dataCurtaBR(plano.prorrogado_ate)} (${esc(plano.justificativa_prorrogacao)})` : ""}</p>` : ""}
      ${aval ? `<p><b>Avaliação (FOR 3):</b> ${aval.eficaz ? "ações eficazes" : "ações não eficazes"} · ${dataCurtaBR(aval.avaliado_em)}</p>` : ""}</div>
    ${ativa && estado.perfil === "cqual" ? `<form class="card" id="formAcaoRnc" onsubmit="return false"><h2 style="margin-top:0">Registrar</h2><div class="campos">
      ${campo("rData", "Data", {tipo: "date", valor: hoje})}
      ${r.etapa === "avaliação" ? campo("rEficaz", "As ações foram eficazes?", {tipo: "select", opcoes: [["sim", "Sim"], ["nao", "Não"]]}) : ""}</div>
      ${campo("rTexto", "Observação, justificativa ou motivo", {tipo: "textarea", linhas: 2})}
      <div id="errosAcaoRnc"></div><div class="linha-botoes">
        ${(BOTOES_ETAPA[r.etapa] || []).map(([a, t, cls])=>`<button type="button" data-acao="${a}" class="${cls || ""}">${t}</button>`).join("")}
        <button type="button" data-acao="grave" class="perigo">Grave: encaminhar à corregedoria</button></div></form>` : ""}`;
};
TELAS_DEPOIS["#/rnc/:id"] = ({id})=>{
  $$("[data-acao]").forEach(b=>b.addEventListener("click", async ()=>{
    try { await acaoRnc(id, b.dataset.acao, {data: valorDe("rData"), texto: valorDe("rTexto"), eficaz: valorDe("rEficaz")}); toast("Registrado."); navegar(); }
    catch(err){ mostrarErros("#errosAcaoRnc", [err.message]); }
  }));
};

// o painel do Sprint 1 ganha a lista das RNCs (os indicadores chegam no Sprint 5)
TELAS["#/painel"] = async ()=>{
  const rs = (await db.list("rncs")).sort((a, b)=>b.aberta_em.localeCompare(a.aberta_em)), hoje = hojeISO();
  const etapasAbertas = (await db.list("etapas")).filter(e=>!e.fim);
  const prazo = n => etapasAbertas.find(e=>e.rnc === n)?.prazo;
  return `<h1>Painel</h1><p class="sub">${rs.length} RNCs. Os indicadores chegam no Sprint 5.</p>
    <div class="card tabela-wrap"><table><tr><th>RNC</th><th>Notificado</th><th>Categoria</th><th>Etapa</th><th>Prazo</th><th>Situação</th></tr>
      ${rs.map(r=>{ const p = prazo(r.numero); return `<tr><td><a href="#/rnc/${encodeURIComponent(r.numero)}">${esc(r.numero)}</a></td><td>${esc(r.setor_notificado)}</td>
        <td>${esc(r.categoria)}</td><td>${esc(r.etapa)}</td><td>${p ? `<span class="${p < hoje ? "erro-txt" : ""}">${dataCurtaBR(p)}</span>` : "—"}</td><td>${esc(r.situacao)}</td></tr>`; }).join("")
        || '<tr><td colspan="6" class="vazio">Nenhuma RNC. Importe a planilha do Forms.</td></tr>'}</table></div>`;
};
