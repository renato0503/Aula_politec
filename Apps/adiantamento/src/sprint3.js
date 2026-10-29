/* ================= Sprint 3 · Etapas e linha do tempo ================= */
const RESPONSAVEL_PADRAO = ["Unidade", "DAS", "Servidor", "Chefia", "SESP Financeiro", "NGER", "Ordenador", "SESP Financeiro", "Servidor", "Servidor", "SESP Contabilidade", "SESP Contabilidade"];
const IDX_SICAD = ETAPAS.indexOf("Cadastro no SICAD"), IDX_PAGAMENTO = ETAPAS.indexOf("Pagamento");
const diasEntre = (a, b)=> Math.round((new Date(b) - new Date(a)) / 86400000);

async function etapasDo(pid){ return (await db.porIndice("etapas", "processo_id", pid)).sort((a, b)=>(a.entrada_em + a.id).localeCompare(b.entrada_em + b.id)); }

// avança (+1) ou devolve (-1) o processo, fechando a etapa aberta e abrindo a próxima
async function moverEtapa(pid, sentido, {data, responsavel, observacao}){
  const p = await db.get("processos", pid), es = await etapasDo(pid), aberta = es.filter(e=>!e.saida_em).pop();
  const i = ETAPAS.indexOf(p.etapa_atual), j = i + sentido;
  if (j < 0 || j >= ETAPAS.length) throw new Error("Não há etapa nessa direção.");
  if (aberta && data < aberta.entrada_em) throw new Error(`A data não pode ser antes da entrada na etapa atual (${dataCurtaBR(aberta.entrada_em)}).`);
  if (sentido > 0 && i === IDX_SICAD && !p.numero_sicad) throw new Error("Informe o número do processo no SICAD antes de seguir.");
  if (sentido < 0 && !observacao) throw new Error("A devolução precisa do motivo.");
  if (aberta) await db.put("etapas", {...aberta, saida_em: data});
  const fim = ETAPAS[j] === "Encerrado";
  await db.put("etapas", {id: uuid(), processo_id: pid, etapa: ETAPAS[j], entrada_em: data, saida_em: fim ? data : null, responsavel: responsavel || RESPONSAVEL_PADRAO[j],
                          observacao: observacao || "", devolucao: sentido < 0});
  const mud = {etapa_atual: ETAPAS[j], situacao: fim ? "encerrado" : "em andamento"};
  if (sentido > 0 && i === IDX_PAGAMENTO) mud.pago_em = data;
  await db.put("processos", {...p, ...mud});
  await registrar(sentido > 0 ? "etapa avançada" : "processo devolvido", {processo_id: pid, detalhe: `${ETAPAS[i]} → ${ETAPAS[j]}${observacao ? ": " + observacao : ""}`});
}

TELAS["#/processo/:id"] = async ({id})=>{
  const p = await db.get("processos", id);
  if (!p) return `<div class="card vazio">Processo não encontrado. <a href="#/painel">Voltar</a></div>`;
  const es = await etapasDo(id), orcs = await db.porIndice("orcamentos", "processo_id", id), atual = ETAPAS.indexOf(p.etapa_atual);
  const hist = (await db.list("log")).filter(l=>l.processo_id === id).sort((a, b)=>b.data_hora.localeCompare(a.data_hora));
  const linhaEtapa = (nome, k)=>{
    const regs = es.filter(e=>e.etapa === nome), ult = regs[regs.length - 1];
    const estadoE = k < atual ? "feita" : k === atual ? "atual" : "futura";
    const dur = ult ? diasEntre(ult.entrada_em, ult.saida_em || hojeISO()) : null;
    return `<li class="etapa-${estadoE}" data-etapa-nome="${esc(nome)}"><b>${k + 1}. ${esc(nome)}</b>
      ${ult ? `<span class="sub"> · ${dataCurtaBR(ult.entrada_em)}${ult.saida_em ? " a " + dataCurtaBR(ult.saida_em) : ""} · ${dur} dia(s)${estadoE === "atual" ? " parado" : ""} · ${esc(ult.responsavel)}</span>` : ""}
      ${regs.some(r=>r.devolucao) ? ' <span class="selo alerta">devolvido</span>' : ""}${ult?.observacao ? `<br><small>${esc(ult.observacao)}</small>` : ""}</li>`;
  };
  return `<h1>${esc(p.id)} · ${esc(p.finalidade)}</h1>
    <p class="sub">${esc(p.unidade)} · ${esc(p.solicitante)} · ${dinheiro.fmt(Math.round(p.valor_solicitado * 100))} · <span class="selo info" id="etapaAtual">${esc(p.etapa_atual)}</span></p>
    <div class="card"><div class="campos">${campo("pSicad", "Número do processo no SICAD", {valor: p.numero_sicad || "", ajuda: "Preencha quando o servidor cadastrar no SICAD."})}
      <div class="campo"><label>&nbsp;</label><button id="btnSicad">Salvar número</button></div></div></div>
    <div class="grade"><div class="card"><h2 style="margin-top:0">Linha do tempo</h2><ol class="linha-tempo">${ETAPAS.map(linhaEtapa).join("")}</ol></div>
    ${p.situacao !== "encerrado" ? `<form class="card" id="formEtapa"><h2 style="margin-top:0">Movimentar</h2>
      ${campo("mData", "Data", {tipo: "date", valor: hojeISO(), obrigatorio: true})}
      ${campo("mResp", "Responsável pela próxima etapa", {valor: RESPONSAVEL_PADRAO[Math.min(atual + 1, ETAPAS.length - 1)]})}
      ${campo("mObs", "Observação (obrigatória na devolução)", {tipo: "textarea", linhas: 2})}
      <div id="errosEtapa"></div><div class="linha-botoes">
        <button class="prim" type="button" id="btnAvancar">Avançar para ${esc(ETAPAS[atual + 1] || "")}</button>
        ${atual > 0 ? `<button type="button" id="btnDevolver">Devolver para ${esc(ETAPAS[atual - 1])}</button>` : ""}</div></form>` : `<div class="card"><b>Processo encerrado.</b></div>`}</div>
    <div class="card tabela-wrap"><h2 style="margin-top:0">Orçamentos</h2><table><tr><th>Fornecedor</th><th>CNPJ</th><th class="num">Valor</th></tr>
      ${orcs.map(o=>`<tr><td>${esc(o.fornecedor)}</td><td class="mono">${esc(o.cnpj)}</td><td class="num">${dinheiro.fmt(Math.round(o.valor * 100))}</td></tr>`).join("")}</table></div>
    <div class="card tabela-wrap"><h2 style="margin-top:0">Histórico</h2><table id="historicoAd"><tr><th>Data e hora</th><th>Ação</th><th>Detalhe</th></tr>
      ${hist.map(h=>`<tr><td>${dataBR(h.data_hora)}</td><td>${esc(h.acao)}</td><td>${esc(h.detalhe || "")}</td></tr>`).join("")}</table></div>`;
};
TELAS_DEPOIS["#/processo/:id"] = ({id})=>{
  if (!$("#pSicad")) return;
  $("#btnSicad").addEventListener("click", async ()=>{
    const p = await db.get("processos", id); await db.put("processos", {...p, numero_sicad: valorDe("pSicad")});
    await registrar("número SICAD", {processo_id: id, detalhe: valorDe("pSicad")}); toast("Número SICAD salvo."); navegar();
  });
  const mover = s => async ()=>{
    try { await moverEtapa(id, s, {data: valorDe("mData"), responsavel: valorDe("mResp"), observacao: valorDe("mObs")}); toast(s > 0 ? "Etapa avançada." : "Processo devolvido."); navegar(); }
    catch(err){ mostrarErros("#errosEtapa", [err.message]); }
  };
  $("#btnAvancar")?.addEventListener("click", mover(1)); $("#btnDevolver")?.addEventListener("click", mover(-1));
};

// o painel do Sprint 1 ganha a lista com o link de cada processo (o painel completo chega no Sprint 6)
TELAS["#/painel"] = async ()=>{
  const ps = (await db.list("processos")).sort((a, b)=>b.criado_em.localeCompare(a.criado_em));
  return `<h1>Painel</h1><p class="sub">${ps.length} processos. <a href="#/pedido/novo">Novo pedido</a> · O painel com prazos chega no Sprint 6.</p>
    <div class="card tabela-wrap"><table><tr><th>Processo</th><th>Unidade</th><th>Finalidade</th><th>Etapa</th><th class="num">Valor</th></tr>
      ${ps.map(p=>`<tr><td><a href="#/processo/${encodeURIComponent(p.id)}">${esc(p.id)}</a></td><td>${esc(p.unidade)}</td><td>${esc(p.finalidade)}</td>
        <td><span class="selo ${p.situacao === "encerrado" ? "ok" : "info"}">${esc(p.etapa_atual)}</span></td><td class="num">${dinheiro.fmt(Math.round(p.valor_solicitado * 100))}</td></tr>`).join("")
        || '<tr><td colspan="5" class="vazio">Nenhum processo. Registre um pedido ou carregue os dados fictícios.</td></tr>'}</table></div>`;
};
