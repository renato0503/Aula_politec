/* Identidade da Segunda via da CIN.
   Entra por último no build. A tela-assinatura é a caixa de entrada do servidor:
   a fila à esquerda e o pedido aberto à direita, com “Aceitar e próximo” e
   “Recusar e próximo”, busca por protocolo, nome ou CPF e espera em horas. */

function cin2Horas(iso){
  if (!iso) return null;
  return Math.max(0, Math.round((Date.now() - new Date(iso).getTime()) / 3600000));
}
function cin2Espera(iso){
  const h = cin2Horas(iso);
  if (h === null) return "";
  if (h < 24) return `${h} h`;
  const d = Math.floor(h / 24);
  return `${d} ${d === 1 ? "dia" : "dias"}`;
}
function cin2Selo(situacao){
  const cls = situacao === "aceito" ? "ok" : situacao === "recusado" ? "erro" : "alerta";
  return `<span class="selo ${cls}">${esc(situacao)}</span>`;
}
function cin2Elegivel(p){ const e = eleg(p); return e.validade && e.dados && e.cpf; }

TELAS["#/fila"] = async ()=>{
  const f = filtroFila();
  const todos = await db.list("pedidos");
  const busca = normalizar(estado.buscaFila || "");
  const lista = todos.filter(p=>!f.situacao || p.situacao === f.situacao)
    .filter(p=>!busca || normalizar(`${p.protocolo} ${p.nome} ${p.cpf || ""}`).includes(busca))
    .sort((a, b)=>a.criado_em.localeCompare(b.criado_em));
  const sel = estado.pedidoSel ? await db.get("pedidos", estado.pedidoSel) : null;
  let ficha = `<div class="card cin2-vazio"><b>Selecione um pedido na lista</b>
    <p class="sub">Abra o pedido para ver as fotos, conferir a elegibilidade e decidir. Use J e K para percorrer a fila.</p></div>`;
  if (sel){
    const fotos = await db.porIndice("fotos", "protocolo", sel.protocolo), e = eleg(sel);
    const decs = (await db.porIndice("decisoes", "protocolo", sel.protocolo)).sort((a, b)=>b.data.localeCompare(a.data));
    ficha = `<div class="card cin2-ficha" id="fichaPedido">
      <div class="cin2-ficha-topo"><div><span class="sub">Pedido</span><h2>${esc(sel.protocolo)}</h2></div>${cin2Selo(sel.situacao)}</div>
      <p><b>${esc(sel.nome)}</b> · CPF ${esc(fmtCpf(sel.cpf))} · nascimento ${dataCurtaBR(sel.nascimento)} · contato ${esc(sel.contato)}</p>
      <p>Elegibilidade: <span class="selo ${e.validade ? "ok" : "erro"}">CIN ${e.validade ? "válida até " + dataCurtaBR(sel.validade_cin) : "vencida"}</span>
        <span class="selo ${e.dados ? "ok" : "erro"}">${e.dados ? "sem mudança de dados" : "dados mudaram"}</span>
        <span class="selo ${e.cpf ? "ok" : "erro"}">CPF ${e.cpf ? "válido" : "inválido"}</span></p>
      <div class="cin2-fotos">${fotos.map(ft=>`<figure><img src="${URL.createObjectURL(ft.conteudo)}" alt="Foto: ${esc(ft.tipo)}"><figcaption class="sub">${esc(ft.tipo)}</figcaption></figure>`).join("")
        || '<p class="sub">Sem fotos (pedido do exemplo).</p>'}</div>
      ${sel.situacao === "recebido" ? `<div class="campos">${campo("fMotivo", "Motivo da recusa", {tipo: "select", opcoes: [["", "Escolha"], ...MOTIVOS_RECUSA]})}${campo("fObs", "Observação")}</div>
        <div id="errosFila"></div><div class="linha-botoes">
          <button class="prim" id="btnAceitar">Aceitar e próximo</button>
          <button class="perigo" id="btnRecusar">Recusar e próximo</button>
          <a class="botao" href="#/pedido/${encodeURIComponent(sel.protocolo)}/resumo">Resumo para o sistema</a></div>`
      : `<p>${sel.motivo ? `Motivo: <b>${esc(sel.motivo)}</b>` : ""}</p><div class="linha-botoes"><a class="botao" href="#/pedido/${encodeURIComponent(sel.protocolo)}/resumo">Resumo para o sistema</a></div>`}
      ${decs.length ? `<p class="sub">Decisões: ${decs.map(d=>`${dataBR(d.data)} · ${esc(d.resultado)}${d.motivo ? " (" + esc(d.motivo) + ")" : ""} · ${esc(d.servidor)}`).join("<br>")}</p>` : ""}</div>`;
  }
  const situacoes = ["", "recebido", "aceito", "recusado"];
  return `<h1>Caixa de entrada</h1>
    <p class="sub">A fila da segunda via. Decida sem voltar à lista: ao aceitar ou recusar, o próximo pedido já abre.</p>
    <div class="cin2-ferramentas">
      <div class="cin2-filtros">${situacoes.map(s=>`<button data-sit="${s}" class="${s === f.situacao ? "prim" : ""}">
        ${s || "todos"} (<span data-qtd="${s || "todos"}">${s ? todos.filter(p=>p.situacao === s).length : todos.length}</span>)</button>`).join("")}</div>
      ${campo("fBusca", "Buscar por protocolo, nome ou CPF", {valor: estado.buscaFila || "", attrs: 'autocomplete="off"'})}
    </div>
    <div class="cin2-caixa">
      <div class="card cin2-lista"><div class="cin2-lista-topo"><b>${lista.length} pedido(s)</b><span class="sub">mais antigo primeiro</span></div>
        ${lista.map(p=>`<a href="#" class="cin2-item ${p.protocolo === estado.pedidoSel ? "escolhido" : ""}" data-sel="${esc(p.protocolo)}">
          <span class="cin2-item-nome">${esc(p.nome)}</span>
          <span class="cin2-item-prot mono">${esc(p.protocolo)}</span>
          <span class="cin2-item-meta">${cin2Elegivel(p) ? '<span class="selo ok">elegível</span>' : '<span class="selo erro">não elegível</span>'}
            ${cin2Selo(p.situacao)} <span class="sub">espera ${cin2Espera(p.criado_em)}</span></span></a>`).join("")
        || '<p class="sub">Nenhum pedido nesta situação.</p>'}</div>
      ${ficha}
    </div>`;
};
TELAS_DEPOIS["#/fila"] = ()=>{
  $$("[data-sit]").forEach(b=>b.addEventListener("click", ()=>{ filtroFila().situacao = b.dataset.sit; estado.pedidoSel = null; navegar(); }));
  $$("[data-sel]").forEach(a=>a.addEventListener("click", e=>{ e.preventDefault(); estado.pedidoSel = a.dataset.sel; navegar(); }));
  let t = null;
  $("#fBusca")?.addEventListener("input", e=>{
    clearTimeout(t); const v = e.target.value;
    t = setTimeout(()=>{ estado.buscaFila = v; navegar(); }, 350);
  });
  const proximo = async (atual)=>{
    const recebidos = (await db.list("pedidos")).filter(p=>p.situacao === "recebido" && p.protocolo !== atual).sort((a, b)=>a.criado_em.localeCompare(b.criado_em));
    return recebidos[0]?.protocolo || null;
  };
  const decidir = resultado => async ()=>{
    const p = await db.get("pedidos", estado.pedidoSel), motivo = valorDe("fMotivo"), obs = valorDe("fObs");
    if (!p) return mostrarErros("#errosFila", ["Selecione um pedido."]);
    if (resultado === "recusado" && !motivo) return mostrarErros("#errosFila", ["A recusa precisa de motivo (RN05)."]);
    if (resultado === "recusado" && motivo === "Outro" && !obs) return mostrarErros("#errosFila", ["Descreva o motivo na observação."]);
    const servidor = (await db.meta("servidor_nome")) || estado.perfil;
    const texto = resultado === "recusado" ? (motivo === "Outro" ? obs : motivo + (obs ? ": " + obs : "")) : "";
    await db.put("decisoes", {id: uuid(), protocolo: p.protocolo, resultado, motivo: texto, servidor, data: agora()});
    await db.put("pedidos", {...p, situacao: resultado, motivo: texto, decidido_em: agora()});
    await registrar("pedido " + resultado, {protocolo: p.protocolo, detalhe: texto});
    const prox = await proximo(p.protocolo);
    estado.pedidoSel = prox;
    toast(prox ? `Pedido ${resultado}. Abrindo o próximo.` : `Pedido ${resultado}. Fila desta situação vazia.`);
    navegar();
  };
  $("#btnAceitar")?.addEventListener("click", decidir("aceito"));
  $("#btnRecusar")?.addEventListener("click", decidir("recusado"));
};
// atalhos da fila: J/K percorrem, A aceita, R leva ao motivo da recusa.
// Registra uma vez só, senão cada render acrescenta outro ouvinte.
document.addEventListener("keydown", function cin2Atalhos(e){
  if (document.body.dataset.rota !== "fila") return;
  if (["INPUT", "SELECT", "TEXTAREA"].includes(document.activeElement?.tagName)) return;
  const itens = $$("[data-sel]"), i = itens.findIndex(a=>a.dataset.sel === estado.pedidoSel);
  if (e.key === "j" || e.key === "k"){
    e.preventDefault();
    const alvo = itens[i + (e.key === "j" ? 1 : -1)];
    if (alvo){ estado.pedidoSel = alvo.dataset.sel; navegar(); }
  }
  if (e.key === "a" && $("#btnAceitar")) { e.preventDefault(); $("#btnAceitar").click(); }
  if (e.key === "r" && $("#btnRecusar")) { e.preventDefault(); $("#btnRecusar").focus(); }
});
