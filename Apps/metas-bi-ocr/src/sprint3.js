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
    const a = ant[p.unidade], v = a ? (p.pendentes - a) / a : null, alertas = [];
    if (p.desconhecida) alertas.push("RN03: unidade fora do cadastro");
    if (v !== null && Math.abs(v) > LIMITE_VARIACAO && !conf.has(p.unidade)) alertas.push(`RN04: variação de ${(v * 100).toFixed(0)}% sobre o mês anterior`);
    return {...p, anterior: a ?? null, variacao: v, alertas, variacaoAlta: v !== null && Math.abs(v) > LIMITE_VARIACAO};
  });
  const soma = ps.reduce((x, p)=>x + p.pendentes, 0), total = rel?.total_relatorio_aceito ?? rel?.total_relatorio;
  const bloqueios = [];
  if (total !== null && total !== undefined && soma !== total) bloqueios.push(`RN02: a soma das unidades (${soma}) difere do total do relatório (${total}).`);
  linhas.filter(l=>l.alertas.length).forEach(l=>bloqueios.push(`${l.unidade}: ${l.alertas.join("; ")}`));
  return {rel, linhas, soma, total, bloqueios};
}

TELAS["#/conferencia/:mes"] = async ({mes})=>{
  const c = await conferir(mes);
  if (!c.rel) return `<div class="card vazio">Mês ${esc(mes)} não importado. <a href="#/importar">Importar</a></div>`;
  const travado = !!c.rel.aprovado_em, unidades = await db.list("unidades");
  return `<h1>Conferência · ${esc(mes)}</h1><p class="sub">${esc(c.rel.arquivo)} · versão ${c.rel.versao} ·
    ${travado ? `<span class="selo ok" id="situacaoMes">aprovado por ${esc(c.rel.aprovado_por)} em ${dataBR(c.rel.aprovado_em)}</span>` : '<span class="selo info" id="situacaoMes">a conferir</span>'}</p>
    <div class="grade"><div class="card kpi"><div class="v">${c.soma}</div><div class="r">soma das unidades</div></div>
      <div class="card kpi"><div class="v">${c.total ?? "—"}</div><div class="r">total do relatório${c.rel.total_relatorio_aceito !== undefined ? " (ajustado)" : ""}</div></div></div>
    <div class="card tabela-wrap"><table id="tabelaConf"><tr><th>Unidade</th><th class="num">Mês anterior</th><th class="num">Lido</th><th class="num">Variação</th><th>Alertas</th>${travado ? "" : "<th>Corrigir</th>"}</tr>
      ${c.linhas.map(l=>`<tr data-unidade="${esc(l.unidade)}"><td>${esc(l.unidade)}${l.desconhecida ? `<br><small class="sub">lido: ${esc(l.unidade_lida)}</small>` : ""}</td>
        <td class="num">${l.anterior ?? "—"}</td><td class="num"><b>${l.pendentes}</b>${l.origem === "corrigido" ? ' <span class="selo alerta">corrigido</span>' : ""}</td>
        <td class="num ${l.variacaoAlta ? "alerta-txt" : ""}">${l.variacao === null ? "—" : (l.variacao * 100).toFixed(0) + "%"}</td>
        <td>${l.alertas.map(a=>`<span class="selo alerta">${esc(a)}</span>`).join(" ")}
          ${!travado && l.variacaoAlta && l.alertas.some(a=>a.startsWith("RN04")) ? `<button data-confirmar="${esc(l.unidade)}">Confirmar valor</button>` : ""}</td>
        ${travado ? "" : `<td><input type="number" min="0" data-novo="${esc(l.id)}" style="width:110px" aria-label="Novo valor para ${esc(l.unidade)}"></td>`}</tr>`).join("")}</table></div>
    ${travado ? `<div class="card"><p>O mês aprovado não muda (RN05). Uma correção abre uma nova versão.</p>
      ${campo("motivoVersao", "Motivo da nova versão", {tipo: "textarea", linhas: 2})}<div id="errosVersao"></div><button id="btnNovaVersao">Abrir nova versão para correção</button></div>`
    : `<div class="card"><h2 style="margin-top:0">Correções e aprovação</h2>
      ${campo("motivoCorrecao", "Motivo da correção (obrigatório para corrigir)", {tipo: "textarea", linhas: 2})}
      <div class="linha-botoes"><button id="btnCorrigir">Aplicar correções</button>
        ${c.total !== null && c.total !== c.soma ? `<button id="btnAceitarSoma">Aceitar a soma (${c.soma}) como total</button>` : ""}</div>
      <hr><div id="bloqueios">${c.bloqueios.length ? `<p class="erro-txt"><b>Não pode aprovar ainda:</b></p><ul>${c.bloqueios.map(b=>`<li>${esc(b)}</li>`).join("")}</ul>` : '<p class="ok-txt">Conferência sem pendências.</p>'}</div>
      ${campo("aprovador", "Aprovado por (chefe de núcleo)", {valor: (await db.meta("aprovador")) || ""})}
      <div id="errosAprovar"></div><button class="prim" id="btnAprovar" ${c.bloqueios.length ? "disabled" : ""}>Aprovar o mês</button></div>`}`;
};
TELAS_DEPOIS["#/conferencia/:mes"] = ({mes})=>{
  $$("[data-confirmar]").forEach(b=>b.addEventListener("click", async ()=>{
    const r = await db.get("relatorios", mes); r.variacoes_confirmadas = [...new Set([...(r.variacoes_confirmadas || []), b.dataset.confirmar])];
    await db.put("relatorios", r); await registrar("variação confirmada", {detalhe: `${mes} ${b.dataset.confirmar}`}); navegar();
  }));
  $("#btnCorrigir")?.addEventListener("click", async ()=>{
    const novos = $$("[data-novo]").filter(i=>i.value !== ""), motivo = valorDe("motivoCorrecao");
    if (!novos.length) return toast("Digite o novo valor na coluna Corrigir.");
    if (!motivo) return toast("Escreva o motivo da correção.");
    for (const i of novos){
      const p = await db.get("pendencias", i.dataset.novo), v = Number(i.value);
      await db.put("correcoes", {id: uuid(), pendencia_id: p.id, valor_lido: p.pendentes, valor_final: v, motivo, data: agora()});
      await db.put("pendencias", {...p, pendentes: v, origem: "corrigido"});
    }
    await registrar("correção", {detalhe: `${mes}: ${novos.length} valor(es) · ${motivo}`}); toast("Correção registrada."); navegar();
  });
  $("#btnAceitarSoma")?.addEventListener("click", async ()=>{
    const motivo = valorDe("motivoCorrecao"); if (!motivo) return toast("Escreva o motivo para aceitar a soma como total.");
    const r = await db.get("relatorios", mes), c = await conferir(mes);
    await db.put("correcoes", {id: uuid(), pendencia_id: mes + "|TOTAL", valor_lido: r.total_relatorio, valor_final: c.soma, motivo, data: agora()});
    await db.put("relatorios", {...r, total_relatorio_aceito: c.soma}); await registrar("total ajustado", {detalhe: `${mes}: ${r.total_relatorio} → ${c.soma}`}); navegar();
  });
  $("#btnAprovar")?.addEventListener("click", async ()=>{
    const quem = valorDe("aprovador"); if (!quem) return mostrarErros("#errosAprovar", ["Informe quem aprova."]);
    const c = await conferir(mes); if (c.bloqueios.length) return mostrarErros("#errosAprovar", c.bloqueios);
    await db.meta("aprovador", quem); await db.put("relatorios", {...c.rel, aprovado_por: quem, aprovado_em: agora()});
    await registrar("mês aprovado", {detalhe: `${mes} por ${quem}`}); toast(`Mês ${mes} aprovado.`); navegar();
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
