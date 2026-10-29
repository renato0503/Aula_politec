/* ================= Sprint 3 · Fila do servidor (RN05) ================= */
const MOTIVOS_RECUSA = ["Foto ilegível", "CIN vencida", "Mudança de dados", "Dados divergentes do cadastro", "Outro"];
const SITUACOES = ["recebido", "aceito", "recusado"];
const fmtCpf = c => String(c || "").replace(/^(\d{3})(\d{3})(\d{3})(\d{2})$/, "$1.$2.$3-$4");
// elegibilidade conferida de novo pelo servidor (RN03)
const eleg = p => ({validade: !!p.validade_cin && p.validade_cin >= hojeISO(), dados: !p.mudou_dados, cpf: cpfValido(p.cpf)});

function filtroFila(){ return estado.filtroFila || (estado.filtroFila = {situacao: "recebido"}); }
TELAS["#/fila"] = async ()=>{
  const f = filtroFila(), todos = await db.list("pedidos");
  const lista = todos.filter(p=>!f.situacao || p.situacao === f.situacao).sort((a, b)=>a.criado_em.localeCompare(b.criado_em));
  const sel = estado.pedidoSel && await db.get("pedidos", estado.pedidoSel);
  let ficha = "";
  if (sel){
    const fotos = await db.porIndice("fotos", "protocolo", sel.protocolo), e = eleg(sel);
    const decs = (await db.porIndice("decisoes", "protocolo", sel.protocolo)).sort((a, b)=>b.data.localeCompare(a.data));
    ficha = `<div class="card" id="fichaPedido"><h2 style="margin-top:0">Pedido ${esc(sel.protocolo)} <span class="selo info" id="sitPedido">${esc(sel.situacao)}</span></h2>
      <p><b>${esc(sel.nome)}</b> · CPF ${esc(fmtCpf(sel.cpf))} · nascimento ${dataCurtaBR(sel.nascimento)} · contato ${esc(sel.contato)}</p>
      <p>Elegibilidade: <span class="selo ${e.validade ? "ok" : "erro"}">CIN ${e.validade ? "válida até " + dataCurtaBR(sel.validade_cin) : "vencida"}</span>
        <span class="selo ${e.dados ? "ok" : "erro"}">${e.dados ? "sem mudança de dados" : "dados mudaram"}</span>
        <span class="selo ${e.cpf ? "ok" : "erro"}">CPF ${e.cpf ? "válido" : "inválido"}</span></p>
      <div style="display:flex;gap:10px;flex-wrap:wrap">${fotos.map(ft=>`<figure style="margin:0"><img src="${URL.createObjectURL(ft.conteudo)}" alt="Foto: ${esc(ft.tipo)}" style="max-width:200px;border-radius:8px"><figcaption class="sub">${esc(ft.tipo)}</figcaption></figure>`).join("")
        || '<p class="sub">Sem fotos (pedido do exemplo).</p>'}</div>
      ${sel.situacao === "recebido" ? `<div class="campos">${campo("fMotivo", "Motivo da recusa", {tipo: "select", opcoes: [["", "Escolha"], ...MOTIVOS_RECUSA]})}${campo("fObs", "Observação")}</div>
        <div id="errosFila"></div><div class="linha-botoes"><button class="prim" id="btnAceitar">Aceitar</button><button class="perigo" id="btnRecusar">Recusar</button>
        <a class="botao" href="#/pedido/${encodeURIComponent(sel.protocolo)}/resumo">Resumo para o sistema</a></div>`
      : `<p>${sel.motivo ? `Motivo: <b>${esc(sel.motivo)}</b>` : ""}</p><a class="botao" href="#/pedido/${encodeURIComponent(sel.protocolo)}/resumo">Resumo para o sistema</a>`}
      ${decs.length ? `<p class="sub">Decisões: ${decs.map(d=>`${dataBR(d.data)} · ${esc(d.resultado)}${d.motivo ? " (" + esc(d.motivo) + ")" : ""} · ${esc(d.servidor)}`).join("<br>")}</p>` : ""}</div>`;
  }
  return `<h1>Fila de pedidos</h1><div class="linha-botoes" style="margin-top:0">${["", ...SITUACOES].map(s=>`<button data-sit="${s}" ${s === f.situacao ? 'class="prim"' : ""}>
    ${s || "todos"} (<span data-qtd="${s || "todos"}">${s ? todos.filter(p=>p.situacao === s).length : todos.length}</span>)</button>`).join("")}</div>
    ${ficha}
    <div class="card tabela-wrap"><table><tr><th>Protocolo</th><th>Pedido em</th><th>Nome</th><th>Elegível</th><th>Situação</th></tr>
      ${lista.map(p=>{ const e = eleg(p), ok = e.validade && e.dados && e.cpf; return `<tr><td><a href="#" data-sel="${esc(p.protocolo)}">${esc(p.protocolo)}</a></td>
        <td>${dataBR(p.criado_em)}</td><td>${esc(p.nome)}</td><td>${ok ? '<span class="selo ok">sim</span>' : '<span class="selo erro">não</span>'}</td><td>${esc(p.situacao)}</td></tr>`; }).join("")
        || '<tr><td colspan="5" class="vazio">Nenhum pedido nesta situação.</td></tr>'}</table></div>`;
};
TELAS_DEPOIS["#/fila"] = ()=>{
  $$("[data-sit]").forEach(b=>b.addEventListener("click", ()=>{ filtroFila().situacao = b.dataset.sit; navegar(); }));
  $$("[data-sel]").forEach(a=>a.addEventListener("click", e=>{ e.preventDefault(); estado.pedidoSel = a.dataset.sel; navegar(); }));
  const decidir = resultado => async ()=>{
    const p = await db.get("pedidos", estado.pedidoSel), motivo = valorDe("fMotivo"), obs = valorDe("fObs");
    if (resultado === "recusado" && !motivo) return mostrarErros("#errosFila", ["A recusa precisa de motivo (RN05)."]);
    if (resultado === "recusado" && motivo === "Outro" && !obs) return mostrarErros("#errosFila", ["Descreva o motivo na observação."]);
    const servidor = (await db.meta("servidor_nome")) || estado.perfil;
    const texto = resultado === "recusado" ? (motivo === "Outro" ? obs : motivo + (obs ? ": " + obs : "")) : "";
    await db.put("decisoes", {id: uuid(), protocolo: p.protocolo, resultado, motivo: texto, servidor, data: agora()});
    await db.put("pedidos", {...p, situacao: resultado, motivo: texto, decidido_em: agora()});
    await registrar("pedido " + resultado, {protocolo: p.protocolo, detalhe: texto});
    toast(`Pedido ${resultado}.`); navegar();
  };
  $("#btnAceitar")?.addEventListener("click", decidir("aceito")); $("#btnRecusar")?.addEventListener("click", decidir("recusado"));
};

TELAS["#/pedido/:id/resumo"] = async ({id})=>{
  const p = await db.get("pedidos", id);
  if (!p) return `<div class="card vazio">Pedido não encontrado.</div>`;
  const linhas = [["Protocolo", p.protocolo], ["Nome", p.nome], ["CPF", fmtCpf(p.cpf)], ["Data de nascimento", dataCurtaBR(p.nascimento)],
    ["Número da CIN", fmtCpf(p.numero_cin)], ["Validade da CIN", dataCurtaBR(p.validade_cin)], ["Contato", p.contato], ["Pedido em", dataBR(p.criado_em)],
    ["Situação", p.situacao + (p.motivo ? " · " + p.motivo : "")], ["Serviço", "Segunda via da CIN, sem nova coleta (dados sem mudança)"]];
  const texto = linhas.map(([k, v])=>`${k}: ${v}`).join("\n");
  return `<h1>Resumo para o sistema de identificação civil</h1><p class="sub">Confira e lance no sistema. O envio automático não faz parte do MVP.</p>
    <div class="card tabela-wrap"><table id="tabelaResumo">${linhas.map(([k, v])=>`<tr><th>${esc(k)}</th><td>${esc(v)}</td></tr>`).join("")}</table>
    <textarea id="textoResumo" hidden>${esc(texto)}</textarea>
    <div class="linha-botoes nao-imprimir"><button class="prim" id="btnCopiarResumo">Copiar</button><button onclick="window.print()">Imprimir</button><a class="botao" href="#/fila">Voltar à fila</a></div></div>`;
};
TELAS_DEPOIS["#/pedido/:id/resumo"] = ()=>{
  $("#btnCopiarResumo")?.addEventListener("click", async ()=>{ try { await navigator.clipboard.writeText($("#textoResumo").value); toast("Resumo copiado."); } catch(e){ toast("Não consegui copiar."); } });
};
