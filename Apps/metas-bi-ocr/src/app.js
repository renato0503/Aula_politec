/* Metas pelo BI · código do app (o construir.py junta com a base comum) */
"use strict";
teste("SheetJS embutido", ()=> typeof XLSX !== "undefined" && typeof XLSX.read === "function");
teste("Exemplo de setembro tem a divergência de total (RN02)", ()=>{
  const m = (dadosEmbutidos("seed")?.exemplos || []).find(x=>x.id === "2026-09");
  return !!m && m.linhas.reduce((a, l)=>a + l.pendentes, 0) !== m.total_relatorio;
});

/* ================= Sprint 2 · Leitura de CSV/Excel ================= */
const COLS_PBI = {mes: ["mes", "competencia", "periodo", "mes de referencia"], unidade: ["unidade", "lotacao", "nucleo"],
                  pendentes: ["laudos pendentes", "pendentes", "passivo", "quantidade", "total de laudos"]};
// "2026-07", "07/2026", "7/2026", "2026/07" -> "2026-07" (RN01)
function mesDeTexto(t){
  const s = String(t ?? "").trim();
  let m = s.match(/^(\d{4})[-/](\d{1,2})$/); if (m && +m[2] >= 1 && +m[2] <= 12) return `${m[1]}-${m[2].padStart(2, "0")}`;
  m = s.match(/^(\d{1,2})[-/](\d{4})$/); if (m && +m[1] >= 1 && +m[1] <= 12) return `${m[2]}-${m[1].padStart(2, "0")}`;
  m = s.match(/(\d{4})-(\d{2})/); return m && +m[2] >= 1 && +m[2] <= 12 ? `${m[1]}-${m[2]}` : null;
}
teste("RN01: mês de referência em vários formatos", ()=> mesDeTexto("07/2026") === "2026-07" && mesDeTexto("2026-7") === "2026-07" && mesDeTexto("13/2026") === null);
const inteiro = v => { if (typeof v === "number") return Math.round(v); const s = String(v ?? "").replace(/\./g, "").replace(",", ".").trim(); return s === "" ? NaN : Math.round(Number(s)); };

// arquivo -> {mes, linhas: [{unidade_lida, pendentes}], total} ou {erro}
function lerRelatorio(nome, linhas, mesForcado, mesTexto){
  const iCab = linhas.findIndex(l=>l.some(c=>COLS_PBI.unidade.some(s=>normalizar(c).includes(s))));
  if (iCab < 0) return {erro: "Não achei a coluna da unidade no arquivo."};
  const cab = linhas[iCab], col = sugerirColunas(cab, COLS_PBI);
  if (col.pendentes < 0) return {erro: "Não achei a coluna de laudos pendentes."};
  let mes = null, total = null; const out = [], erros = [];
  linhas.slice(iCab + 1).forEach((l, i)=>{
    const u = String(l[col.unidade] ?? "").trim(); if (!u) return;
    const v = inteiro(l[col.pendentes]);
    if (col.mes >= 0 && !mes) mes = mesDeTexto(l[col.mes]);
    if (normalizar(u) === "total"){ total = v; return; }
    if (Number.isNaN(v) || v < 0) return erros.push(`linha ${iCab + i + 2}: número de pendentes ilegível para ${u}`);
    out.push({unidade_lida: u, pendentes: v, linha: iCab + i + 2});
  });
  const mesArquivo = mes || mesTexto || mesDeTexto(nome);
  mes = mesForcado || mesArquivo;
  if (!mes) return {erro: "O arquivo não tem um mês de referência e nenhum mês foi escolhido (RN01). Escolha o mês na tela e importe de novo."};
  if (!out.length) return {erro: "Nenhuma unidade com número de pendentes."};
  return {mes, mes_arquivo: mesArquivo, linhas: out, total, erros};
}

// rótulo curto da lotação, para a coluna da tabela (a gerência; se faltar, a coordenadoria ou a diretoria)
const rotuloLotacao = lot => lot.gerencia || lot.coordenadoria || lot.diretoria || "Outras";
const gerenciaDe = nome => rotuloLotacao(lotacaoDe(nome));

async function acharUnidade(nomeLido){
  const n = normalizar(nomeLido), unidades = await db.list("unidades");
  const u = unidades.find(x=>normalizar(x.nome) === n || (x.apelidos || []).some(a=>normalizar(a) === n));
  if (u) return u;
  // pelo organograma: "PERÍCIAS EM LABORATÓRIOS DE MATERIAIS" -> Coordenadoria do Laboratório de Materiais
  const lot = lotacaoDe(nomeLido), alvo = lot.gerencia || lot.coordenadoria;
  const pelaLotacao = alvo && unidades.find(x=>x.nome === alvo);
  if (!pelaLotacao) return null;
  pelaLotacao.apelidos = [...new Set([...(pelaLotacao.apelidos || []), nomeLido])];
  await db.put("unidades", pelaLotacao);
  await registrar("unidade associada pelo organograma", {detalhe: `${nomeLido} -> ${alvo}`});
  return pelaLotacao;
}

TELAS["#/importar"] = async ()=>{
  const n = (await db.list("unidades")).length;
  return `<h1>Importar o mês</h1><p class="sub">Escolha o arquivo do Power BI 1: a exportação do visual (CSV ou Excel) ou o PDF mensal. O PDF pode ter texto ou ser imagem: nesse caso o app lê pelo OCR e mostra a leitura para você conferir antes de gravar.</p>
    <div class="card"><p style="margin-top:0"><b>${n}</b> unidade(s) cadastrada(s).
      ${n ? "" : "Carregue as gerências do organograma ou os dados fictícios em <a href=\"#/config\">Configuração</a>."}</p>
      <button type="button" id="btnOrganograma">Cadastrar as gerências do organograma (Decreto nº 2.180/2026)</button></div>
    <div class="card"><div class="campos">${campo("mesImportar", "Mês de referência", {tipo: "month", valor: estado.importMes || "", ajuda: "Opcional. Vazio: o app usa o mês do arquivo. Escolha para importar o arquivo em outro mês."})}</div>
      <h3>Recorte pelo organograma</h3>${filtroOrg("imp", estado.impOrg || {})}
      <label class="sub"><input type="checkbox" id="somenteMonitoradas"> Importar somente as unidades monitoradas (descarta as que não estão no cadastro)</label>
      <div class="linha-botoes"><label class="botao prim">Escolher arquivo do mês<input type="file" id="arqMes" accept=".csv,.xlsx,.xls,.pdf" hidden></label>
      <button type="button" id="btnExemploMes">Usar arquivo de exemplo</button></div>
      <p class="sub">O exemplo é o CSV de julho/2026, com 10 unidades.</p>
      <div id="progressoMes" class="sub" aria-live="polite"></div><div id="errosMes"></div><div id="resMes"></div></div>
    <div id="historicoCurto">${await tabelaMeses()}</div>`;
};
async function tabelaMeses(){
  const rels = (await db.list("relatorios")).sort((a, b)=>b.id.localeCompare(a.id));
  if (!rels.length) return "";
  const linhas = [];
  for (const r of rels){
    const ps = await db.porIndice("pendencias", "mes_ref", r.id), total = r.total_relatorio_aceito ?? r.total_relatorio;
    const soma = ps.reduce((a, p)=>a + p.pendentes, 0);
    linhas.push(`<tr><td>${r.id}</td><td>${esc(r.arquivo)}</td><td>${esc(r.gerencia || "Todas")}</td><td class="num">${ps.length}</td><td class="num">${soma}</td>
      <td class="num">${total ?? "—"}${r.total_relatorio_aceito !== undefined ? ' <small class="sub">(aceito)</small>' : ""}
        ${r.total_original !== undefined && r.total_original !== null && r.total_original !== total ? `<br><small class="sub">no arquivo: ${r.total_original}</small>` : ""}</td>
      <td>${r.aprovado_em ? '<span class="selo ok">aprovado</span>' : total !== null && total !== undefined && total !== soma ? '<span class="selo alerta">soma ≠ total</span>' : '<span class="selo info">a conferir</span>'}</td>
      <td class="meses-acoes"><a href="#/conferencia/${encodeURIComponent(r.id)}">Abrir</a>
        ${r.aprovado_em ? "" : `<button type="button" data-excluir-mes="${esc(r.id)}">Excluir</button>`}</td></tr>`);
  }
  return `<div class="card tabela-wrap"><h2 style="margin-top:0">Meses importados</h2><table><tr><th>Mês</th><th>Arquivo</th><th>Recorte</th><th class="num">Unidades</th>
    <th class="num">Soma</th><th class="num">Total do relatório</th><th>Situação</th><th>Ações</th></tr>${linhas.join("")}</table>
    <p class="sub">Soma = soma das unidades gravadas no mês. Total = o do arquivo, ajustado ao recorte quando houver filtro, ou o aceito na conferência.</p></div>`;
}
async function desenharDesconhecidas(mes){
  const ps = (await db.porIndice("pendencias", "mes_ref", mes)).filter(p=>p.desconhecida);
  const unidades = await db.list("unidades");
  $("#resMes").insertAdjacentHTML("beforeend", ps.length ? `<h3>Unidades que não estão no cadastro (RN03)</h3>${ps.map(p=>`<div class="campos" style="align-items:end">
    <div class="campo"><label>Lido no relatório</label><b>${esc(p.unidade_lida)}</b> (${p.pendentes})</div>
    ${campo("assoc-" + p.id.replace(/\W/g, "_"), "Associar a", {tipo: "select", opcoes: [["", "Escolha"], ...unidades.map(u=>[u.nome, u.nome])]})}
    <div class="campo"><button data-assoc="${esc(p.id)}">Associar e lembrar</button>
      <button data-cadastrar="${esc(p.id)}">Cadastrar como unidade</button></div></div>`).join("")}` : "");
  $$("[data-assoc]").forEach(b=>b.addEventListener("click", async ()=>{
    const p = await db.get("pendencias", b.dataset.assoc), alvo = valorDe("assoc-" + p.id.replace(/\W/g, "_"));
    if (!alvo) return toast("Escolha a unidade.");
    const u = await db.get("unidades", alvo); u.apelidos = [...new Set([...(u.apelidos || []), p.unidade_lida])]; await db.put("unidades", u);
    await db.del("pendencias", p.id);
    const lot = u.lotacao || lotacaoDe(alvo);
    await db.put("pendencias", {...p, id: `${p.mes_ref}|${alvo}`, unidade: alvo, desconhecida: false, lotacao: lot, gerencia: rotuloLotacao(lot)});
    await registrar("unidade associada", {detalhe: `${p.unidade_lida} -> ${alvo}`}); toast(`"${p.unidade_lida}" agora é ${alvo}.`);
    b.closest(".campos").remove(); $("#historicoCurto").innerHTML = await tabelaMeses();
  }));
  $$("[data-cadastrar]").forEach(b=>b.addEventListener("click", async ()=>{
    const p = await db.get("pendencias", b.dataset.cadastrar); if (!p) return;
    const lot = lotacaoDe(p.unidade_lida);
    await db.put("unidades", {nome: p.unidade_lida, apelidos: [], lotacao: lot});
    await db.put("pendencias", {...p, desconhecida: false, lotacao: lot, gerencia: rotuloLotacao(lot)});
    await registrar("unidade cadastrada", {detalhe: p.unidade_lida}); toast(`"${p.unidade_lida}" cadastrada.`);
    b.closest(".campos").remove(); $("#historicoCurto").innerHTML = await tabelaMeses();
  }));
}

/* grava o mês a partir das linhas (formato do CSV). origem: csv, excel, pdf ou ocr.
   conf: {nome normalizado: confiança da leitura} (o OCR traz abaixo de 1). */
async function gravarImportacao(arquivo, linhas, origem, {mesTexto = null, conf = {}} = {}){
  const mesEscolhido = valorDe("mesImportar");
  estado.importMes = mesEscolhido;
  const r = lerRelatorio(arquivo, linhas, mesEscolhido, mesTexto);
  if (r.erro) return mostrarErros("#errosMes", [r.erro]);
  const antes = await db.get("relatorios", r.mes);
  if (antes?.aprovado_em) return mostrarErros("#errosMes", [`O mês ${r.mes} já foi aprovado e não muda (RN05). Uma correção gera nova versão na conferência.`]);
  mostrarErros("#errosMes", []);
  const sel = lerFiltroOrg("imp"), somente = !!$("#somenteMonitoradas")?.checked;
  estado.impOrg = sel;
  let desconhecidas = 0, ignoradas = 0; const validas = [];
  for (const l of r.linhas){
    const u = await acharUnidade(l.unidade_lida), lot = u?.lotacao || lotacaoDe(u ? u.nome : l.unidade_lida);
    if (!noRecorte(lot, sel)) { ignoradas++; continue; }
    if (!u && somente) { ignoradas++; continue; }
    if (!u) desconhecidas++;
    validas.push({l, u, lot});
  }
  if (!validas.length) return mostrarErros("#errosMes", ["Nenhuma unidade do recorte escolhido entrou na importação. Confira a diretoria, a coordenadoria e a gerência escolhidas."]);
  for (const p of await db.porIndice("pendencias", "mes_ref", r.mes)) await db.del("pendencias", p.id);
  for (const {l, u, lot} of validas){
    const nome = u ? u.nome : l.unidade_lida;
    await db.put("pendencias", {id: `${r.mes}|${nome}`, mes_ref: r.mes, unidade: nome, unidade_lida: l.unidade_lida,
      pendentes: l.pendentes, gerencia: rotuloLotacao(lot), lotacao: lot, origem, confianca: conf[normalizar(l.unidade_lida)] ?? 1, desconhecida: !u, linha: l.linha});
  }
  const soma = validas.reduce((a, {l})=>a + l.pendentes, 0), recorte = !!sel.diretoria || (somente && ignoradas > 0);
  await db.put("relatorios", {id: r.mes, arquivo, tipo: origem, importado_em: agora(), total_relatorio: recorte ? soma : r.total, total_original: r.total,
    gerencia: textoRecorte(sel), recorte: sel, versao: (antes?.versao || 0) + 1, aprovado_por: null, aprovado_em: null, variacoes_confirmadas: []});
  await registrar("mês importado", {detalhe: `${r.mes}: ${validas.length} unidades · ${textoRecorte(sel)} · ${origem} (${arquivo})`});
  const avisoMes = mesEscolhido && r.mes_arquivo && r.mes_arquivo !== mesEscolhido
    ? `<div class="aviso alerta">O arquivo indica <b>${esc(r.mes_arquivo)}</b>; importei como <b>${esc(r.mes)}</b>, como você escolheu.</div>` : "";
  const baixa = validas.filter(({l})=>confiancaBaixa(conf[normalizar(l.unidade_lida)] ?? 1)).length;
  $("#resMes").innerHTML = `${avisoMes}<h2 id="mesLido">Mês ${r.mes}</h2><p><span class="selo ok">${validas.length} unidades no recorte</span>
    ${desconhecidas ? `<span class="selo alerta" id="qtdDesconhecidas">${desconhecidas} fora do cadastro</span>` : ""}
    ${ignoradas ? `<span class="selo info">${ignoradas} fora do recorte</span>` : ""}
    ${baixa ? `<span class="selo alerta">${baixa} com confiança do OCR abaixo de 90%</span>` : ""}
    ${r.erros.length ? `<span class="selo erro">${r.erros.length} linhas ilegíveis</span>` : ""}</p>
    <p>Soma do recorte: <b>${soma}</b> · Total do relatório${recorte ? " (ajustado ao recorte)" : ""}: <b>${recorte ? soma : r.total ?? "não informado"}</b>
      ${recorte && r.total !== null ? `<small class="sub">(no arquivo: ${r.total})</small>` : ""}</p>
    <p><a class="botao prim" href="#/conferencia/${r.mes}">Ir para a conferência do mês</a></p>`;
  await desenharDesconhecidas(r.mes);
  $("#historicoCurto").innerHTML = await tabelaMeses();
}

TELAS_DEPOIS["#/importar"] = ()=>{
  ligarFiltroOrg("imp", sel=>{ estado.impOrg = sel; });
  $("#btnOrganograma")?.addEventListener("click", async ()=>{
    const n = await carregarOrganograma(); toast(n ? `${n} gerências e núcleos cadastrados.` : "As gerências do organograma já estavam cadastradas."); navegar();
  });
  $("#btnExemploMes")?.addEventListener("click", ()=>{
    const ex = dadosEmbutidos("exemplo");
    if (!ex) return toast("Arquivo de exemplo não encontrado.");
    try {
      const f = new File([ex.texto], ex.nome, {type: "text/csv"});
      const dt = new DataTransfer(); dt.items.add(f);
      const inp = $("#arqMes"); inp.files = dt.files; inp.dispatchEvent(new Event("change", {bubbles: true}));
    } catch (err) { toast("Não consegui usar o exemplo: " + err.message, 5000); }
  });
  $("#arqMes").addEventListener("change", async e=>{
    const f = e.target.files[0]; if (!f) return; e.target.value = "";
    $("#resMes").innerHTML = ""; mostrarErros("#errosMes", []);
    const progresso = t => { const el = $("#progressoMes"); if (el) el.textContent = t || ""; };
    try {
      if (/\.csv$/i.test(f.name)) return await gravarImportacao(f.name, lerCSV(await lerArquivoTexto(f)), "csv");
      if (!/\.pdf$/i.test(f.name)){
        const livro = XLSX.read(await lerArrayBuffer(f), {type: "array"});
        return await gravarImportacao(f.name, XLSX.utils.sheet_to_json(livro.Sheets[livro.SheetNames[0]], {header: 1, raw: true, defval: ""}), "excel");
      }
      progresso("Lendo o PDF...");
      const r = await lerPdfRelatorio(await lerArrayBuffer(f), progresso);
      progresso("");
      if (!r.tabela.linhas.length) return mostrarErros("#errosMes", [r.origem === "ocr"
        ? "Li o PDF pelo OCR, mas não achei linhas com nome de unidade e número. Confira se a página traz a tabela de unidades (e não só o gráfico) ou use a exportação CSV/Excel do visual."
        : "O PDF não traz a tabela de unidades."]);
      const mesTexto = mesNoTexto(r.texto);
      // PDF com texto e uma só coluna de número: grava direto, como o CSV. Nos demais, mostra a prévia.
      if (r.origem === "pdf" && r.tabelas.length === 1 && r.tabela.cabecalho.length === 1){
        const linhas = [["Unidade", "Laudos pendentes"], ...r.tabela.linhas.map(l=>[l.nome, l.nums[0].v]), ...(r.tabela.total ? [["Total", r.tabela.total.nums[0]?.v ?? ""]] : [])];
        return await gravarImportacao(f.name, linhas, "pdf", {mesTexto});
      }
      const desenhar = ()=>{
        $("#resMes").innerHTML = previaLeitura(f.name, r);
        $("#tabelaPdf")?.addEventListener("change", e=>{ r.escolhida = Number(e.target.value); r.tabela = r.tabelas[r.escolhida].tabela; desenhar(); });
        ligarPrevia();
      };
      const ligarPrevia = ()=>{
      $("#btnDescartarPrevia").addEventListener("click", ()=>{ $("#resMes").innerHTML = ""; });
      $("#btnUsarPrevia").addEventListener("click", async ()=>{
        const {linhas, conf, editadas} = linhasDaPrevia(r);
        if (linhas.length < 2) return mostrarErros("#errosMes", ["Marque ao menos uma linha com nome e número."]);
        await gravarImportacao(f.name, linhas, r.origem, {mesTexto, conf});
        if (editadas.length) await registrar("leitura do PDF corrigida na prévia", {detalhe: `${f.name}: ${editadas.join(", ")}`});
      });
      };
      desenhar();
      $("#previaPdf").scrollIntoView({block: "start"});
    } catch(err){ progresso(""); return mostrarErros("#errosMes", ["Não consegui ler o arquivo: " + err.message]); }
  });
};
/* ---------- exclusão de um mês importado (na lista e no histórico) ---------- */
document.addEventListener("click", async e=>{
  const b = e.target.closest("[data-excluir-mes]"); if (!b) return;
  const mes = b.dataset.excluirMes, r = await db.get("relatorios", mes); if (!r) return;
  if (r.aprovado_em) return toast("Mês aprovado não pode ser excluído (RN05).", 5000);
  if (!confirm(`Excluir o mês ${mes} (${r.arquivo}) e os valores já importados?`)) return;
  for (const p of await db.porIndice("pendencias", "mes_ref", mes)) await db.del("pendencias", p.id);
  for (const c of (await db.list("correcoes")).filter(x=>String(x.pendencia_id || "").startsWith(mes + "|"))) await db.del("correcoes", c.id);
  await db.del("relatorios", mes);
  await registrar("mês excluído", {detalhe: mes});
  toast(`Mês ${mes} excluído.`);
  if (location.hash.includes(mes)) location.hash = "#/importar"; else navegar();
});
