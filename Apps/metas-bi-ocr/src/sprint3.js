/* ================= Sprint 3 · Conferência (RN02 a RN05) ================= */
const LIMITE_VARIACAO = 0.30;  // RN04
const mesAnterior = mes => { const [a, m] = mes.split("-").map(Number); return m === 1 ? `${a - 1}-12` : `${a}-${String(m - 1).padStart(2, "0")}`; };
teste("mês anterior de 2026-01 é 2025-12", ()=> mesAnterior("2026-01") === "2025-12" && mesAnterior("2026-09") === "2026-08");

// situação da conferência do mês: linhas com variação e alertas, e o que impede a aprovação
async function conferir(mes){
  const rel = await db.get("relatorios", mes), ps = (await db.porIndice("pendencias", "mes_ref", mes)).sort((a, b)=>a.unidade.localeCompare(b.unidade));
  const ant = Object.fromEntries((await db.porIndice("pendencias", "mes_ref", mesAnterior(mes))).map(p=>[p.unidade, p.pendentes]));
  const conf = new Set(rel?.variacoes_confirmadas || []);
  const linhas = ps.map(p=>{
    const a = ant[p.unidade], v = a ? (p.pendentes - a) / a : null, alertas = [], avisos = [];
    if (p.desconhecida) alertas.push("RN03: unidade fora do cadastro");
    if (v !== null && Math.abs(v) > LIMITE_VARIACAO && !conf.has(p.unidade)) alertas.push(`RN04: variação de ${(v * 100).toFixed(0)}% sobre o mês anterior`);
    // a confiança baixa do OCR não bloqueia: avisa para conferir o número
    if (p.origem !== "corrigido" && confiancaBaixa(p.confianca ?? 1)) avisos.push(`OCR com ${Math.round((p.confianca ?? 0) * 100)}% de confiança: confira o número`);
    return {...p, anterior: a ?? null, variacao: v, alertas, avisos, variacaoAlta: v !== null && Math.abs(v) > LIMITE_VARIACAO};
  });
  const soma = ps.reduce((x, p)=>x + p.pendentes, 0), total = rel?.total_relatorio_aceito ?? rel?.total_relatorio;
  const bloqueios = [];
  if (total !== null && total !== undefined && soma !== total) bloqueios.push(`RN02: a soma das unidades (${soma}) difere do total do relatório (${total}).`);
  linhas.filter(l=>l.alertas.length).forEach(l=>bloqueios.push(`${l.unidade}: ${l.alertas.join("; ")}`));
  const rn03 = linhas.filter(l=>l.alertas.some(a=>a.startsWith("RN03"))), rn04 = linhas.filter(l=>l.alertas.some(a=>a.startsWith("RN04")));
  return {rel, linhas, soma, total, bloqueios, rn02: total !== null && total !== undefined && soma !== total, rn03, rn04};
}

// o que resolver para aprovar, com o botão de cada caso
function painelBloqueios(c, ocultos){
  if (!c.bloqueios.length) return '<p class="ok-txt" id="semBloqueio">Conferência sem pendências. O mês pode ser aprovado.</p>';
  return `<p class="erro-txt"><b>Para aprovar, resolva:</b></p><ol class="bloqueios-lista">
    ${c.rn02 ? `<li><b>RN02 · soma ≠ total.</b> A soma das unidades é <b>${c.soma}</b> e o total do relatório é <b>${c.total}</b>.
      Se as correções estão certas, escreva o motivo acima e use <button type="button" id="btnAceitarSoma2">Aceitar a soma (${c.soma}) como total</button></li>` : ""}
    ${c.rn04.length ? `<li><b>RN04 · variação acima de ${LIMITE_VARIACAO * 100}%</b> em ${c.rn04.length} unidade(s): ${c.rn04.map(l=>esc(l.unidade)).join(", ")}.
      Corrija o número ou <button type="button" id="btnConfirmarTodas">Confirmar as ${c.rn04.length} variações</button></li>` : ""}
    ${c.rn03.length ? `<li><b>RN03 · fora do cadastro</b>: ${c.rn03.map(l=>esc(l.unidade_lida || l.unidade)).join(", ")}.
      Use <b>Editar</b> na linha para escolher a unidade, ou <button type="button" id="btnCadastrarTodas">${c.rn03.length === 1 ? "Cadastrar como unidade" : `Cadastrar as ${c.rn03.length} como unidades`}</button>
      <button type="button" class="perigo" id="btnExcluirForaCadastro">${c.rn03.length === 1 ? "Excluir a linha" : `Excluir as ${c.rn03.length} linhas`}</button></li>` : ""}</ol>
    ${ocultos ? `<p class="sub">${ocultos} linha(s) com pendência estão fora do filtro da tabela. A aprovação vale para o mês inteiro.</p>` : ""}`;
}

TELAS["#/conferencia/:mes"] = async ({mes})=>{
  const c = await conferir(mes);
  if (!c.rel) return `<div class="card vazio">Mês ${esc(mes)} não importado. <a href="#/importar">Importar</a></div>`;
  const travado = !!c.rel.aprovado_em, sel = estado.confOrg || {};
  const visiveis = c.linhas.filter(l=>noRecorte(lotacaoPend(l), sel));
  const ocultos = c.linhas.filter(l=>l.alertas.length && !visiveis.includes(l)).length;
  const monitoradas = c.linhas.filter(l=>!l.desconhecida), somaMonitorada = monitoradas.reduce((a, l)=>a + l.pendentes, 0);
  const somaVisivel = visiveis.reduce((a, l)=>a + l.pendentes, 0);
  return `<h1>Conferência · ${esc(mes)}</h1><p class="sub">${esc(c.rel.arquivo)} · versão ${c.rel.versao} · recorte: ${esc(c.rel.gerencia || "Todas")} ·
    ${travado ? `<span class="selo ok" id="situacaoMes">aprovado por ${esc(c.rel.aprovado_por)} em ${dataBR(c.rel.aprovado_em)}</span>` : '<span class="selo info" id="situacaoMes">a conferir</span>'}</p>
    <div class="card"><h3 style="margin-top:0">Filtrar a tabela pelo organograma</h3>${filtroOrg("conf", sel)}
      ${sel.diretoria ? `<p class="sub">Mostrando ${visiveis.length} de ${c.linhas.length} unidades · soma do filtro: <b id="somaFiltro">${somaVisivel}</b></p>` : ""}</div>
    <div class="grade"><div class="card kpi"><div class="v" id="kpiPendentes">${somaMonitorada}</div><div class="r">Pendentes (unidades monitoradas)</div></div>
      <div class="card kpi"><div class="v" id="kpiSoma">${c.soma}</div><div class="r">soma de todas as unidades do mês</div></div>
      <div class="card kpi"><div class="v" id="kpiTotal">${c.total ?? "—"}</div><div class="r">total do relatório${c.rel.total_relatorio_aceito !== undefined ? " (aceito)" : ""}</div></div></div>
    <div class="card tabela-wrap"><table id="tabelaConf"><tr><th>Unidade</th><th>Lotação</th><th class="num">Mês anterior</th><th class="num">Lido</th><th class="num">Variação</th><th>Alertas</th>${travado ? "" : "<th>Corrigir</th><th>Ações</th>"}</tr>
      ${visiveis.map(l=>{ const lot = lotacaoPend(l);
        return `<tr data-unidade="${esc(l.unidade)}"><td>${esc(l.unidade)}${l.unidade_lida && l.unidade_lida !== l.unidade ? `<br><small class="sub">lido: ${esc(l.unidade_lida)}</small>` : ""}</td>
        <td><small>${lot.gerencia && normalizar(lot.gerencia) === normalizar(l.unidade) ? "" : esc(rotuloLotacao(lot)) + "<br>"}<span class="sub">${esc([lot.coordenadoria, lot.diretoria].filter(Boolean).join(" · ") || (lot.gerencia ? "" : "fora do organograma"))}</span></small></td>
        <td class="num">${l.anterior ?? "—"}</td><td class="num"><b>${l.pendentes}</b>${l.origem === "corrigido" ? ' <span class="selo alerta">corrigido</span>' : l.origem === "ocr" ? ' <span class="selo info">OCR</span>' : ""}</td>
        <td class="num ${l.variacaoAlta ? "alerta-txt" : ""}">${l.variacao === null ? "—" : (l.variacao * 100).toFixed(0) + "%"}</td>
        <td>${l.alertas.map(a=>`<span class="selo alerta">${esc(a)}</span>`).join(" ")} ${l.avisos.map(a=>`<span class="selo info">${esc(a)}</span>`).join(" ")}
          ${!travado && l.variacaoAlta && l.alertas.some(a=>a.startsWith("RN04")) ? `<button data-confirmar="${esc(l.unidade)}">Confirmar valor</button>` : ""}</td>
        ${travado ? "" : `<td><input type="number" min="0" data-novo="${esc(l.id)}" style="width:110px" aria-label="Novo valor para ${esc(l.unidade)}"></td>
          <td class="metas-acoes"><button type="button" data-editar-pend="${esc(l.id)}">Editar</button>
            <button type="button" class="perigo" data-excluir-pend="${esc(l.id)}">Excluir</button></td>`}</tr>`; }).join("")}</table></div>
    ${travado ? `<div class="card"><p>O mês aprovado não muda (RN05). Uma correção abre uma nova versão.</p>
      ${campo("motivoVersao", "Motivo da nova versão", {tipo: "textarea", linhas: 2})}<div id="errosVersao"></div><button id="btnNovaVersao">Abrir nova versão para correção</button>
      <p><a class="botao prim" href="#/exportar/${encodeURIComponent(mes)}">Gerar a planilha</a></p></div>`
    : `<div class="card"><h2 style="margin-top:0">Correções e aprovação</h2>
      ${campo("motivoCorrecao", "Motivo da correção (obrigatório para corrigir ou aceitar a soma)", {tipo: "textarea", linhas: 2})}
      <div class="linha-botoes"><button id="btnCorrigir">Aplicar correções</button>
        ${c.rn02 ? `<button id="btnAceitarSoma">Aceitar a soma (${c.soma}) como total</button>` : ""}</div>
      <hr><div id="bloqueios">${painelBloqueios(c, ocultos)}</div>
      ${campo("aprovador", "Aprovado por (chefe de núcleo)", {valor: (await db.meta("aprovador")) || ""})}
      <div id="errosAprovar"></div><button class="prim" id="btnAprovar" ${c.bloqueios.length ? 'aria-describedby="bloqueios" data-bloqueado="1"' : ""}>Aprovar o mês</button></div>`}`;
};
async function editarPendencia(mes, id){
  const p = await db.get("pendencias", id); if (!p) return;
  const unidades = (await db.list("unidades")).map(u=>u.nome);
  if (p.unidade && !unidades.includes(p.unidade)) unidades.unshift(p.unidade);
  const dlg = document.createElement("dialog"); dlg.className = "metas-dialogo";
  dlg.innerHTML = `<form method="dialog" class="metas-form"><h2>Editar ${esc(p.unidade)}</h2>
    <div class="campos"><div class="campo"><label for="edUnidade">Unidade</label><select id="edUnidade">${unidades.map(u=>`<option value="${esc(u)}" ${u === p.unidade ? "selected" : ""}>${esc(u)}</option>`).join("")}</select></div>
      ${campo("edLida", "Nome lido no relatório", {valor: p.unidade_lida || p.unidade})}
      ${campo("edPend", "Laudos pendentes", {tipo: "number", valor: p.pendentes, attrs: 'min="0"'})}</div>
    ${campo("edMotivo", "Motivo da alteração (obrigatório)", {tipo: "textarea", linhas: 2})}
    <div id="edErros"></div><div class="linha-botoes"><button type="submit" class="prim">Salvar</button>
      <button type="button" class="sec" data-fechar>Cancelar</button></div></form>`;
  document.body.appendChild(dlg);
  dlg.querySelector("[data-fechar]").addEventListener("click", ()=>dlg.remove());
  dlg.addEventListener("cancel", e=>{ e.preventDefault(); dlg.remove(); });
  dlg.querySelector("form").addEventListener("submit", async e=>{
    e.preventDefault();
    const unidade = dlg.querySelector("#edUnidade").value, lida = dlg.querySelector("#edLida").value.trim();
    const pend = Number(dlg.querySelector("#edPend").value), motivo = dlg.querySelector("#edMotivo").value.trim();
    const erros = [];
    if (!(pend >= 0)) erros.push("Informe os laudos pendentes.");
    if (!motivo) erros.push("Escreva o motivo da alteração.");
    if (!unidade) erros.push("Escolha a unidade.");
    if (erros.length) return mostrarErros(dlg.querySelector("#edErros"), erros);
    const novoId = `${mes}|${unidade}`;
    if (novoId !== p.id && await db.get("pendencias", novoId)) return mostrarErros(dlg.querySelector("#edErros"), ["Já existe uma linha desta unidade no mês."]);
    await db.put("correcoes", {id: uuid(), pendencia_id: novoId, valor_lido: p.pendentes, valor_final: pend, motivo, data: agora(), tipo: "edicao"});
    if (novoId !== p.id) await db.del("pendencias", p.id);
    const uCad = await db.get("unidades", unidade), lot = uCad?.lotacao || lotacaoDe(unidade);
    await db.put("pendencias", {...p, id: novoId, unidade, unidade_lida: lida || unidade, pendentes: pend, origem: "corrigido", desconhecida: false, lotacao: lot, gerencia: rotuloLotacao(lot)});
    await registrar("linha editada", {detalhe: `${mes}: ${p.unidade} -> ${unidade} (${pend})`});
    dlg.remove(); toast("Linha atualizada."); navegar();
  });
  dlg.showModal();
  dlg.querySelector("#edPend")?.focus();
}

TELAS_DEPOIS["#/conferencia/:mes"] = ({mes})=>{
  ligarFiltroOrg("conf", sel=>{ estado.confOrg = sel; navegar(); });
  $$("[data-editar-pend]").forEach(b=>b.addEventListener("click", ()=>editarPendencia(mes, b.dataset.editarPend)));
  $$("[data-excluir-pend]").forEach(b=>b.addEventListener("click", async ()=>{
    const p = await db.get("pendencias", b.dataset.excluirPend); if (!p) return;
    if (!confirm(`Excluir a linha ${p.unidade} (${p.pendentes}) do mês ${mes}?`)) return;
    await db.del("pendencias", p.id);
    await registrar("linha excluída", {detalhe: `${mes}: ${p.unidade}`});
    toast("Linha excluída."); navegar();
  }));
  const confirmarVariacoes = async unidades=>{
    const r = await db.get("relatorios", mes); r.variacoes_confirmadas = [...new Set([...(r.variacoes_confirmadas || []), ...unidades])];
    await db.put("relatorios", r); await registrar("variação confirmada", {detalhe: `${mes} ${unidades.join(", ")}`}); navegar();
  };
  $$("[data-confirmar]").forEach(b=>b.addEventListener("click", ()=>confirmarVariacoes([b.dataset.confirmar])));
  $("#btnConfirmarTodas")?.addEventListener("click", async ()=>confirmarVariacoes((await conferir(mes)).rn04.map(l=>l.unidade)));
  $("#btnCadastrarTodas")?.addEventListener("click", async ()=>{
    const c = await conferir(mes);
    for (const l of c.rn03){
      const lot = lotacaoDe(l.unidade_lida || l.unidade);
      if (!await db.get("unidades", l.unidade)) await db.put("unidades", {nome: l.unidade, apelidos: [], lotacao: lot});
      const p = await db.get("pendencias", l.id); await db.put("pendencias", {...p, desconhecida: false, lotacao: lot, gerencia: rotuloLotacao(lot)});
    }
    await registrar("unidades cadastradas", {detalhe: `${mes}: ${c.rn03.map(l=>l.unidade).join(", ")}`}); toast(`${c.rn03.length} unidade(s) cadastrada(s).`); navegar();
  });
  $("#btnExcluirForaCadastro")?.addEventListener("click", async ()=>{
    const c = await conferir(mes);
    if (!confirm(`Excluir ${c.rn03.length} linha(s) fora do cadastro do mês ${mes}?`)) return;
    for (const l of c.rn03) await db.del("pendencias", l.id);
    await registrar("linhas fora do cadastro excluídas", {detalhe: `${mes}: ${c.rn03.map(l=>l.unidade).join(", ")}`}); navegar();
  });
  $("#btnCorrigir")?.addEventListener("click", async ()=>{
    const novos = $$("[data-novo]").filter(i=>i.value !== ""), motivo = valorDe("motivoCorrecao");
    if (!novos.length) return toast("Digite o novo valor na coluna Corrigir.");
    if (!motivo) return toast("Escreva o motivo da correção.");
    for (const i of novos){
      const p = await db.get("pendencias", i.dataset.novo), v = Number(i.value);
      await db.put("correcoes", {id: uuid(), pendencia_id: p.id, valor_lido: p.pendentes, valor_final: v, motivo, data: agora()});
      await db.put("pendencias", {...p, pendentes: v, origem: "corrigido"});
    }
    await registrar("correção", {detalhe: `${mes}: ${novos.length} valor(es) · ${motivo}`});
    const c = await conferir(mes);
    toast(c.rn02 ? `Correção registrada. A soma agora é ${c.soma} e o total é ${c.total}: use "Aceitar a soma" se o total do relatório estiver desatualizado.` : "Correção registrada.", 6000);
    navegar();
  });
  const aceitarSoma = async ()=>{
    const motivo = valorDe("motivoCorrecao");
    if (!motivo){ $("#motivoCorrecao")?.focus(); return mostrarErros("#errosAprovar", ["Escreva o motivo (campo acima) para aceitar a soma como total."]); }
    const r = await db.get("relatorios", mes), c = await conferir(mes);
    await db.put("correcoes", {id: uuid(), pendencia_id: mes + "|TOTAL", valor_lido: r.total_relatorio, valor_final: c.soma, motivo, data: agora()});
    await db.put("relatorios", {...r, total_relatorio_aceito: c.soma}); await registrar("total ajustado", {detalhe: `${mes}: ${r.total_relatorio} → ${c.soma}`}); navegar();
  };
  $("#btnAceitarSoma")?.addEventListener("click", aceitarSoma);
  $("#btnAceitarSoma2")?.addEventListener("click", aceitarSoma);
  // o botão não fica desabilitado: um clique sempre responde (aprova ou diz o que falta)
  $("#btnAprovar")?.addEventListener("click", async ()=>{
    const c = await conferir(mes);
    if (c.bloqueios.length){
      mostrarErros("#errosAprovar", ["O mês ainda não pode ser aprovado. Resolva os itens da lista acima:", ...c.bloqueios]);
      return $("#bloqueios").scrollIntoView({block: "center"});
    }
    const quem = valorDe("aprovador"); if (!quem){ $("#aprovador")?.focus(); return mostrarErros("#errosAprovar", ["Informe quem aprova (chefe de núcleo)."]); }
    await db.meta("aprovador", quem); await db.put("relatorios", {...c.rel, aprovado_por: quem, aprovado_em: agora()});
    await registrar("mês aprovado", {detalhe: `${mes} por ${quem}`}); toast(`Mês ${mes} aprovado. Planilha liberada.`);
    location.hash = "#/exportar/" + encodeURIComponent(mes);
  });
  $("#btnNovaVersao")?.addEventListener("click", async ()=>{
    const motivo = valorDe("motivoVersao"); if (!motivo) return mostrarErros("#errosVersao", ["Escreva o motivo da nova versão (RN05)."]);
    const r = await db.get("relatorios", mes);
    await db.put("relatorios", {...r, versao: r.versao + 1, aprovado_por: null, aprovado_em: null, versoes_anteriores: [...(r.versoes_anteriores || []), {versao: r.versao, aprovado_por: r.aprovado_por, aprovado_em: r.aprovado_em, motivo_reabertura: motivo}]});
    await registrar("nova versão", {detalhe: `${mes} v${r.versao + 1}: ${motivo}`}); navegar();
  });
};

TELAS["#/historico"] = async ()=>{
  const rels = (await db.list("relatorios")).sort((a, b)=>b.id.localeCompare(a.id));
  return `<h1>Histórico</h1><p class="sub">Meses importados, conferidos e aprovados.</p>${await tabelaMeses()}
    ${rels.length ? `<div class="card"><p>Abrir a conferência: ${rels.map(r=>`<a href="#/conferencia/${r.id}">${r.id}</a>`).join(" · ")}</p></div>` : ""}`;
};
