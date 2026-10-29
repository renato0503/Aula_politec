/* ================= Sprint 4 · Protocolo do cidadão ================= */
const SIT_PROTOCOLO = {recebido: "Recebido, aguardando conferência", aceito: "Aceito", recusado: "Recusado"};

TELAS["#/protocolo/:id"] = async ({id})=>{
  const p = await db.get("pedidos", id);
  if (!p) return `<div class="card vazio">Protocolo <span class="mono">${esc(id)}</span> não encontrado. <a href="#/pedido">Fazer um pedido</a></div>`;
  const decs = (await db.porIndice("decisoes", "protocolo", id)).sort((a, b)=>b.data.localeCompare(a.data));
  const selo = p.situacao === "aceito" ? "ok" : p.situacao === "recusado" ? "erro" : "info";
  return `<h1>Protocolo <span class="mono" id="numProtocolo">${esc(p.protocolo)}</span></h1>
    <p class="sub">Pedido de segunda via da CIN · enviado em ${dataBR(p.criado_em)}</p>
    <div class="card"><p>Situação: <span class="selo ${selo}" id="sitProtocolo">${esc(SIT_PROTOCOLO[p.situacao] || p.situacao)}</span></p>
      ${p.motivo ? `<p><b>Motivo:</b> <span id="motivoProtocolo">${esc(p.motivo)}</span></p>` : ""}
      <p class="sub">${p.situacao === "recebido" ? "O servidor confere o pedido e a situação muda aqui." : p.situacao === "aceito" ? "O pedido foi aceito e segue para o resumo do sistema." : "O pedido precisa ser feito de novo, corrigindo o motivo acima."}</p>
      <div class="linha-botoes nao-imprimir">
        ${p.situacao === "aceito" ? `<a class="botao prim" href="#/pedido/${encodeURIComponent(p.protocolo)}/resumo">Ver o resumo</a>` : ""}
        <a class="botao" href="#/pedido">Novo pedido</a>
        <button onclick="window.print()">Imprimir</button></div></div>
    <div class="card tabela-wrap"><h2 style="margin-top:0">Dados do pedido</h2><table>
      <tr><th>Nome</th><td>${esc(p.nome)}</td></tr><tr><th>CPF</th><td class="mono">${esc(fmtCpf(p.cpf))}</td></tr>
      <tr><th>Nascimento</th><td>${dataCurtaBR(p.nascimento)}</td></tr><tr><th>Validade da CIN</th><td>${dataCurtaBR(p.validade_cin)}</td></tr>
      <tr><th>Contato</th><td>${esc(p.contato)}</td></tr></table></div>
    ${decs.length ? `<div class="card tabela-wrap"><h2 style="margin-top:0">Decisões</h2><table><tr><th>Data</th><th>Resultado</th><th>Motivo</th><th>Servidor</th></tr>
      ${decs.map(d=>`<tr><td>${dataBR(d.data)}</td><td>${esc(d.resultado)}</td><td>${esc(d.motivo || "—")}</td><td>${esc(d.servidor)}</td></tr>`).join("")}</table></div>` : ""}`;
};
