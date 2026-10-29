/* ================= Sprint 4 · Exportar o mês (RN06) ================= */
// Só o mês aprovado pode ser exportado; o arquivo sai no layout da planilha do Google.
async function linhasDoMes(mes){
  const ps = (await db.porIndice("pendencias", "mes_ref", mes)).sort((a, b)=>a.unidade.localeCompare(b.unidade));
  return ps.map(p=>({Unidade: p.unidade, "Laudos pendentes": p.pendentes}));
}
TELAS["#/exportar/:mes"] = async ({mes})=>{
  const rel = await db.get("relatorios", mes);
  if (!rel) return `<div class="card vazio">Mês ${esc(mes)} não importado. <a href="#/importar">Importar</a></div>`;
  const linhas = await linhasDoMes(mes), soma = linhas.reduce((a, l)=>a + l["Laudos pendentes"], 0);
  return `<h1>Exportar · ${esc(mes)}</h1>
    <p class="sub">${esc(rel.arquivo)} · versão ${rel.versao} · ${rel.aprovado_em ? `<span class="selo ok">aprovado por ${esc(rel.aprovado_por)}</span>` : '<span class="selo alerta">mês ainda não aprovado</span>'}</p>
    <div class="grade"><div class="card kpi"><div class="v">${linhas.length}</div><div class="r">unidades</div></div>
      <div class="card kpi"><div class="v">${soma}</div><div class="r">laudos pendentes</div></div>
      <div class="card kpi"><div class="v">${rel.total_relatorio_aceito ?? rel.total_relatorio ?? "—"}</div><div class="r">total do relatório</div></div></div>
    <div class="card tabela-wrap"><table id="tabelaExport"><tr><th>Unidade</th><th class="num">Laudos pendentes</th></tr>
      ${linhas.map(l=>`<tr><td>${esc(l.Unidade)}</td><td class="num">${l["Laudos pendentes"]}</td></tr>`).join("")}</table></div>
    <div class="card"><h2 style="margin-top:0">Baixar para a planilha</h2>
      ${rel.aprovado_em ? `<p class="sub">O arquivo tem o mesmo cabeçalho da planilha do Google (Unidade;Laudos pendentes).</p>
        <div class="linha-botoes"><button class="prim" id="btnCsv">Baixar CSV</button><button id="btnXlsx">Baixar Excel</button><button id="btnCopiar">Copiar</button></div>`
      : `<p class="sub" id="avisoNaoAprovado">O mês precisa ser aprovado na conferência antes de exportar (RN05). <a href="#/conferencia/${esc(mes)}">Conferir</a></p>`}</div>`;
};
TELAS_DEPOIS["#/exportar/:mes"] = async ({mes})=>{
  const texto = async ()=> "Unidade;Laudos pendentes\r\n" + (await linhasDoMes(mes)).map(l=>`${l.Unidade};${l["Laudos pendentes"]}`).join("\r\n") + "\r\n";
  $("#btnCsv")?.addEventListener("click", async ()=>{ baixar(`metas-${mes}.csv`, "\ufeff" + await texto(), "text/csv"); toast("CSV gerado."); });
  $("#btnXlsx")?.addEventListener("click", async ()=>{
    const livro = XLSX.utils.book_new(), ws = XLSX.utils.json_to_sheet(await linhasDoMes(mes));
    XLSX.utils.book_append_sheet(livro, ws, "Pendentes");
    XLSX.writeFile(livro, `metas-${mes}.xlsx`); toast("Excel gerado.");
  });
  $("#btnCopiar")?.addEventListener("click", async ()=>{
    const tsv = (await linhasDoMes(mes)).map(l=>`${l.Unidade}\t${l["Laudos pendentes"]}`).join("\n");
    try { await navigator.clipboard.writeText(tsv); toast("Tabela copiada. Cole na planilha."); } catch(e){ toast("Não consegui copiar."); }
  });
};
