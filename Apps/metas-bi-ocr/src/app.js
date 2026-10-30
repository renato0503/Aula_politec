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
function lerRelatorio(nome, linhas){
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
  mes = mes || mesDeTexto(nome);
  if (!mes) return {erro: "O arquivo não tem um mês de referência válido (RN01). Ele foi recusado."};
  if (!out.length) return {erro: "Nenhuma unidade com número de pendentes."};
  return {mes, linhas: out, total, erros};
}

async function acharUnidade(nomeLido){
  const n = normalizar(nomeLido);
  return (await db.list("unidades")).find(u=>normalizar(u.nome) === n || (u.apelidos || []).some(a=>normalizar(a) === n)) || null;
}

TELAS["#/importar"] = async ()=>{
  const n = (await db.list("unidades")).length;
  return `<h1>Importar o mês</h1><p class="sub">Escolha o arquivo do Power BI 1: a exportação do visual (CSV ou Excel) ou o PDF mensal. O PDF precisa ter camada de texto.</p>
    ${n ? "" : `<div class="card pendente">Nenhuma unidade cadastrada. Carregue os dados fictícios em <a href="#/config">Configuração</a> ou cadastre as unidades.</div>`}
    <div class="card"><label class="botao prim">Escolher arquivo do mês<input type="file" id="arqMes" accept=".csv,.xlsx,.xls,.pdf" hidden></label>
      <div id="errosMes"></div><div id="resMes"></div></div>
    <div id="historicoCurto">${await tabelaMeses()}</div>`;
};
async function tabelaMeses(){
  const rels = (await db.list("relatorios")).sort((a, b)=>b.id.localeCompare(a.id));
  if (!rels.length) return "";
  const linhas = [];
  for (const r of rels){
    const ps = await db.porIndice("pendencias", "mes_ref", r.id);
    linhas.push(`<tr><td>${r.id}</td><td>${esc(r.arquivo)}</td><td class="num">${ps.length}</td><td class="num">${ps.reduce((a, p)=>a + p.pendentes, 0)}</td>
      <td class="num">${r.total_relatorio ?? "—"}</td><td>${r.aprovado_em ? '<span class="selo ok">aprovado</span>' : '<span class="selo info">a conferir</span>'}</td></tr>`);
  }
  return `<div class="card tabela-wrap"><h2 style="margin-top:0">Meses importados</h2><table><tr><th>Mês</th><th>Arquivo</th><th class="num">Unidades</th>
    <th class="num">Soma</th><th class="num">Total do relatório</th><th>Situação</th></tr>${linhas.join("")}</table></div>`;
}
async function desenharDesconhecidas(mes){
  const ps = (await db.porIndice("pendencias", "mes_ref", mes)).filter(p=>p.desconhecida);
  const unidades = await db.list("unidades");
  $("#resMes").insertAdjacentHTML("beforeend", ps.length ? `<h3>Unidades que não estão no cadastro (RN03)</h3>${ps.map(p=>`<div class="campos" style="align-items:end">
    <div class="campo"><label>Lido no relatório</label><b>${esc(p.unidade_lida)}</b> (${p.pendentes})</div>
    ${campo("assoc-" + p.id.replace(/\W/g, "_"), "Associar a", {tipo: "select", opcoes: [["", "Escolha"], ...unidades.map(u=>[u.nome, u.nome])]})}
    <div class="campo"><button data-assoc="${esc(p.id)}">Associar e lembrar</button></div></div>`).join("")}` : "");
  $$("[data-assoc]").forEach(b=>b.addEventListener("click", async ()=>{
    const p = await db.get("pendencias", b.dataset.assoc), alvo = valorDe("assoc-" + p.id.replace(/\W/g, "_"));
    if (!alvo) return toast("Escolha a unidade.");
    const u = await db.get("unidades", alvo); u.apelidos = [...new Set([...(u.apelidos || []), p.unidade_lida])]; await db.put("unidades", u);
    await db.del("pendencias", p.id);
    await db.put("pendencias", {...p, id: `${p.mes_ref}|${alvo}`, unidade: alvo, desconhecida: false});
    await registrar("unidade associada", {detalhe: `${p.unidade_lida} -> ${alvo}`}); toast(`"${p.unidade_lida}" agora é ${alvo}.`);
    b.closest(".campos").remove(); $("#historicoCurto").innerHTML = await tabelaMeses();
  }));
}
TELAS_DEPOIS["#/importar"] = ()=>{
  $("#arqMes").addEventListener("change", async e=>{
    const f = e.target.files[0]; if (!f) return; e.target.value = "";
    $("#resMes").innerHTML = "";
    let linhas;
    try {
      if (/\.csv$/i.test(f.name)) linhas = lerCSV(await lerArquivoTexto(f));
      else if (/\.pdf$/i.test(f.name)){
        const {texto, temCamada} = await lerPdfTexto(await lerArrayBuffer(f));
        linhas = (temCamada && texto.trim()) ? linhasDoPdf(texto) : [];
        if (linhas.length < 2) return mostrarErros("#errosMes", ["O PDF não tem camada de texto (é imagem ou não traz a tabela de unidades). O OCR automático não está embutido nesta versão: use a exportação CSV/Excel ou digite os números na conferência."]);
      }
      else { const livro = XLSX.read(await lerArrayBuffer(f), {type: "array"}); linhas = XLSX.utils.sheet_to_json(livro.Sheets[livro.SheetNames[0]], {header: 1, raw: true, defval: ""}); }
    } catch(err){ return mostrarErros("#errosMes", ["Não consegui ler o arquivo: " + err.message]); }
    const r = lerRelatorio(f.name, linhas);
    if (r.erro) return mostrarErros("#errosMes", [r.erro]);
    const antes = await db.get("relatorios", r.mes);
    if (antes?.aprovado_em) return mostrarErros("#errosMes", [`O mês ${r.mes} já foi aprovado e não muda (RN05). Uma correção gera nova versão na conferência.`]);
    mostrarErros("#errosMes", []);
    for (const p of await db.porIndice("pendencias", "mes_ref", r.mes)) await db.del("pendencias", p.id);
    let desconhecidas = 0;
    for (const l of r.linhas){
      const u = await acharUnidade(l.unidade_lida); if (!u) desconhecidas++;
      await db.put("pendencias", {id: `${r.mes}|${u ? u.nome : l.unidade_lida}`, mes_ref: r.mes, unidade: u ? u.nome : l.unidade_lida, unidade_lida: l.unidade_lida,
        pendentes: l.pendentes, origem: /\.csv$/i.test(f.name) ? "csv" : /\.pdf$/i.test(f.name) ? "pdf" : "excel", confianca: 1, desconhecida: !u, linha: l.linha});
    }
    await db.put("relatorios", {id: r.mes, arquivo: f.name, tipo: /\.csv$/i.test(f.name) ? "csv" : /\.pdf$/i.test(f.name) ? "pdf" : "excel", importado_em: agora(), total_relatorio: r.total,
      versao: (antes?.versao || 0) + 1, aprovado_por: null, aprovado_em: null});
    await registrar("mês importado", {detalhe: `${r.mes}: ${r.linhas.length} unidades (${f.name})`});
    const soma = r.linhas.reduce((a, l)=>a + l.pendentes, 0);
    $("#resMes").innerHTML = `<h2 id="mesLido">Mês ${r.mes}</h2><p><span class="selo ok">${r.linhas.length} unidades lidas</span>
      ${desconhecidas ? `<span class="selo alerta" id="qtdDesconhecidas">${desconhecidas} fora do cadastro</span>` : ""}
      ${r.erros.length ? `<span class="selo erro">${r.erros.length} linhas ilegíveis</span>` : ""}</p>
      <p>Soma das unidades: <b>${soma}</b> · Total do relatório: <b>${r.total ?? "não informado"}</b></p>
      <p class="sub">A conferência (RN02 a RN04) chega no Sprint 3. <a href="#/conferencia/${r.mes}">Conferência do mês</a></p>`;
    await desenharDesconhecidas(r.mes);
    $("#historicoCurto").innerHTML = await tabelaMeses();
  });
};
