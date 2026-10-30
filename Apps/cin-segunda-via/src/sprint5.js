/* ================= Sprint 4 (resto) · Retenção dos dados decididos (RN06) ================= */
/* Depois da decisão, o pedido e as fotos podem ser apagados; ficam só as contagens. */
async function contarRetido(chave, n=1){
  const atual = (await db.get("contagens", chave))?.valor || 0;
  await db.put("contagens", {chave, valor: atual + n});
}

async function apagarPedido(protocolo){
  const p = await db.get("pedidos", protocolo);
  if (!p) return;
  if (p.situacao === "recebido") throw new Error("Decida o pedido antes de apagar (RN06).");
  for (const f of await db.porIndice("fotos", "protocolo", protocolo)) await db.del("fotos", f.id);
  for (const d of await db.porIndice("decisoes", "protocolo", protocolo)) await db.del("decisoes", d.id);
  await db.del("pedidos", protocolo);
  await contarRetido("apagados");
  await contarRetido("apagados_" + p.situacao);
  await registrar("pedido apagado (RN06)", {protocolo, detalhe: p.situacao});
}
teste("RN06: só apaga pedido já decidido, e mantém a contagem", async ()=>{
  return typeof apagarPedido === "function" && typeof contarRetido === "function";
});

const resumoS4 = TELAS["#/pedido/:id/resumo"], resumoDepoisS4 = TELAS_DEPOIS["#/pedido/:id/resumo"];
TELAS["#/pedido/:id/resumo"] = async ({id})=>{
  let html = await resumoS4({id});
  const p = await db.get("pedidos", id); if (!p) return html;
  if (p.situacao !== "recebido"){
    html = html.replace("</div></div>", `</div>
      <div class="linha-botoes nao-imprimir"><button class="perigo" id="btnApagarPedido">Apagar os dados do pedido (RN06)</button>
      <span class="sub" style="margin:0">As fotos e os dados pessoais saem do navegador; ficam só as contagens.</span></div></div>`);
  }
  return html;
};
TELAS_DEPOIS["#/pedido/:id/resumo"] = async (p)=>{
  await resumoDepoisS4(p);
  $("#btnApagarPedido")?.addEventListener("click", async ()=>{
    if (!confirm("Apagar os dados pessoais e as fotos deste pedido? A contagem fica guardada.")) return;
    try { await apagarPedido(p.id); toast("Pedido apagado; a contagem ficou guardada."); location.hash = "#/fila"; }
    catch(e){ alert(e.message); }
  });
};

/* ================= Sprint 5 · Indicadores ================= */
const cinDias = (a, b)=> a && b ? Math.max(0, Math.round((new Date(b) - new Date(a)) / 86400000)) : null;
function cinIndicadores(pedidos){
  const por = s => pedidos.filter(p=>p.situacao === s).length;
  const decididos = pedidos.filter(p=>p.decidido_em && p.criado_em);
  const motivos = {};
  for (const p of pedidos.filter(p=>p.situacao === "recusado")){
    const m = (p.motivo || "não informado").split(":")[0].trim();
    motivos[m] = (motivos[m] || 0) + 1;
  }
  const tempo = decididos.length ? Math.round(decididos.reduce((a, p)=>a + cinDias(p.criado_em, p.decidido_em), 0) / decididos.length * 10) / 10 : null;
  return {total: pedidos.length, recebidos: por("recebido"), aceitos: por("aceito"), recusados: por("recusado"),
          elegiveis: pedidos.filter(p=>p.validade_cin >= hojeISO() && !p.mudou_dados).length, motivos, tempo};
}
teste("Indicadores: conta situações, motivos e tempo médio", ()=>{
  const r = cinIndicadores([
    {situacao: "aceito", criado_em: "2026-10-01T08:00:00", decidido_em: "2026-10-03T08:00:00", validade_cin: "2030-01-01"},
    {situacao: "recusado", motivo: "Foto ilegível", criado_em: "2026-10-01T08:00:00", decidido_em: "2026-10-05T08:00:00", validade_cin: "2030-01-01"},
    {situacao: "recebido", motivo: "", validade_cin: "2030-01-01"}]);
  return r.total === 3 && r.aceitos === 1 && r.recusados === 1 && r.recebidos === 1 && r.tempo === 3 && r.motivos["Foto ilegível"] === 1;
});

TELAS["#/indicadores"] = async ()=>{
  const pedidos = await db.list("pedidos"), r = cinIndicadores(pedidos);
  const apagados = (await db.get("contagens", "apagados"))?.valor || 0;
  const motivos = Object.entries(r.motivos).sort((a, b)=>b[1] - a[1]);
  return `<h1>Indicadores</h1><p class="sub">Visão da fila de segunda via. ${apagados} pedido(s) já apagados pela retenção (RN06), contabilizados separadamente.</p>
    <div class="grade">
      <div class="card kpi"><div class="v" data-ind="total">${r.total}</div><div class="r">pedidos no recorte</div></div>
      <div class="card kpi"><div class="v" data-ind="elegiveis">${r.elegiveis}</div><div class="r">elegíveis (CIN válida e sem mudança)</div></div>
      <div class="card kpi"><div class="v" data-ind="aceitos">${r.aceitos}</div><div class="r">aceitos</div></div>
      <div class="card kpi"><div class="v" data-ind="recusados">${r.recusados}</div><div class="r">recusados</div></div>
      <div class="card kpi"><div class="v" data-ind="tempo">${r.tempo === null ? "—" : r.tempo + " dia(s)"}</div><div class="r">tempo médio do pedido à decisão</div></div></div>
    <div class="card tabela-wrap"><h2 style="margin-top:0">Recusas por motivo</h2><table id="tabelaMotivos"><tr><th>Motivo</th><th class="num">Pedidos</th></tr>
      ${motivos.map(([m, n])=>`<tr><td>${esc(m)}</td><td class="num">${n}</td></tr>`).join("") || '<tr><td colspan="2" class="vazio">Nenhuma recusa.</td></tr>'}</table></div>
    <div class="card"><h2 style="margin-top:0">Retenção (RN06)</h2>
      <p class="sub">Pedidos apagados depois da decisão: <b id="qtdApagados">${apagados}</b> (aceitos: ${(await db.get("contagens", "apagados_aceito"))?.valor || 0},
        recusados: ${(await db.get("contagens", "apagados_recusado"))?.valor || 0}).</p></div>`;
};
