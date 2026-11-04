/* ================= Sprint 7 · Dashboard orçamentário =================
   Execução do portfólio por ano e eixo (empenhado, liquidado, saldo e %),
   com edição dos lançamentos, exclusão, filtro e importação de .xlsx/.csv. */

const TAP_EIXOS = [...OBJETIVOS_ESTRATEGICOS, "Infraestrutura", "Outros"];

function tapNumero(v){
  if (typeof v === "number") return v;
  let s = String(v ?? "").trim().replace(/^R\$\s*/, "").replace(/\s/g, "");
  if (!s) return NaN;
  const temVirgula = s.includes(","), temPonto = s.includes(".");
  if (temVirgula && temPonto){
    if (s.lastIndexOf(",") > s.lastIndexOf(".")) s = s.replace(/\./g, "").replace(",", ".");
    else s = s.replace(/,/g, "");
  } else if (temVirgula){
    if (/^\d{1,3}(,\d{3})+$/.test(s)) s = s.replace(/,/g, "");
    else s = s.replace(",", ".");
  } else if (temPonto && /^\d{1,3}(\.\d{3})+$/.test(s)){
    s = s.replace(/\./g, "");
  }
  const n = Number(s);
  return Number.isFinite(n) ? n : NaN;
}
teste("Sprint 7: lê empenhado em formato brasileiro e norte-americano", ()=>
  tapNumero("1.234.567,89") === 1234567.89 && tapNumero("1,234.56") === 1234.56 && tapNumero("250000") === 250000);

function tapResumoOrc(rows, filtro = {}){
  const linhas = rows.filter(r=>(!filtro.ano || String(r.ano) === String(filtro.ano)) && (!filtro.eixo || r.eixo === filtro.eixo));
  const soma = k => linhas.reduce((a, r)=>a + Number(r[k] || 0), 0);
  const empenhado = soma("empenhado"), liquidado = soma("liquidado");
  return {linhas, empenhado, liquidado, saldo: empenhado - liquidado,
    percentual: empenhado ? liquidado / empenhado * 100 : 0, lancamentos: linhas.length};
}
function tapPorGrupo(rows, campo, filtro = {}){
  const mapa = new Map();
  for (const r of rows.filter(r=>(!filtro.ano || String(r.ano) === String(filtro.ano)) && (!filtro.eixo || r.eixo === filtro.eixo))){
    const chave = String(r[campo] || "—");
    const g = mapa.get(chave) || {nome: chave, empenhado: 0, liquidado: 0, lancamentos: 0};
    g.empenhado += Number(r.empenhado || 0); g.liquidado += Number(r.liquidado || 0); g.lancamentos++;
    mapa.set(chave, g);
  }
  return [...mapa.values()].sort((a, b)=>campo === "ano" ? a.nome.localeCompare(b.nome) : b.empenhado - a.empenhado);
}
teste("Sprint 7: o resumo soma empenhado, liquidado e saldo", ()=>{
  const r = tapResumoOrc([{ano: 2026, eixo: "A", empenhado: 1000, liquidado: 600}, {ano: 2026, eixo: "A", empenhado: 500, liquidado: 500},
    {ano: 2025, eixo: "B", empenhado: 900, liquidado: 100}], {ano: "2026"});
  return r.empenhado === 1500 && r.liquidado === 1100 && r.saldo === 400 && r.lancamentos === 2 && Math.round(r.percentual) === 73;
});

function tapBarras(grupos){
  const max = Math.max(1, ...grupos.flatMap(g=>[g.empenhado, g.liquidado]));
  return grupos.map(g=>`<div class="orc-grupo"><span class="orc-rot" title="${esc(g.nome)}">${esc(g.nome)}</span>
    <div class="orc-barras"><i class="orc-b emp" style="width:${g.empenhado / max * 100}%" title="Empenhado ${dinheiro.fmt(Math.round(g.empenhado * 100))}"></i>
      <i class="orc-b liq" style="width:${g.liquidado / max * 100}%" title="Liquidado ${dinheiro.fmt(Math.round(g.liquidado * 100))}"></i></div>
    <span class="orc-val">${dinheiro.fmt(Math.round(g.liquidado * 100))}<small> de ${dinheiro.fmt(Math.round(g.empenhado * 100))}</small></span></div>`).join("")
    || '<p class="sub">Nenhum lançamento no recorte.</p>';
}
const tapReal = v => dinheiro.fmt(Math.round(Number(v || 0) * 100));

TELAS["#/dashboard"] = async ()=>{
  const rows = (await db.list("orcamentos")).sort((a, b)=>String(a.ano).localeCompare(String(b.ano)) || String(a.eixo).localeCompare(String(b.eixo)));
  const anos = [...new Set(rows.map(r=>String(r.ano)))].sort();
  const eixos = [...new Set(rows.map(r=>r.eixo))].sort();
  const filtro = {ano: estado.dashAno || "", eixo: estado.dashEixo || ""};
  const res = tapResumoOrc(rows, filtro);
  const porAno = tapPorGrupo(rows, "ano", filtro), porEixo = tapPorGrupo(rows, "eixo", filtro);
  const edit = estado.orcEdit ? rows.find(r=>r.id === estado.orcEdit) : null;
  const v = (k, d = "")=>edit ? edit[k] ?? d : d;
  return `<h1>Dashboard orçamentário</h1><p class="sub">Execução do portfólio por ano e eixo. Edite um lançamento na tabela ou use o formulário; a planilha pode ser importada em .xlsx ou .csv.</p>
    <div class="card orc-filtros"><div class="campos">
      ${campo("dashAno", "Ano", {tipo: "select", opcoes: [["", "Todos"], ...anos.map(a=>[a, a])], valor: filtro.ano})}
      ${campo("dashEixo", "Eixo", {tipo: "select", opcoes: [["", "Todos"], ...eixos.map(e=>[e, e])], valor: filtro.eixo})}
      <div class="campo"><label>&nbsp;</label><div class="linha-botoes" style="margin:0"><button type="button" class="sec" id="btnDashLimpar">Limpar filtros</button>
        <button type="button" id="btnDashCsv">${icone("download")} Exportar CSV</button></div></div></div></div>
    <div class="grade orc-kpis">
      <div class="card kpi"><div class="v" data-dash="empenhado">${tapReal(res.empenhado)}</div><div class="r">empenhado</div></div>
      <div class="card kpi"><div class="v" data-dash="liquidado">${tapReal(res.liquidado)}</div><div class="r">liquidado</div></div>
      <div class="card kpi"><div class="v" data-dash="saldo">${tapReal(res.saldo)}</div><div class="r">saldo a liquidar</div></div>
      <div class="card kpi"><div class="v" data-dash="percentual">${res.percentual.toFixed(1).replace(".", ",")}%</div><div class="r">% liquidado</div></div>
      <div class="card kpi"><div class="v" data-dash="lancamentos">${res.lancamentos}</div><div class="r">lançamentos</div></div></div>
    <div class="orc-duas">
      <div class="card"><h2 style="margin-top:0">Empenhado e liquidado por ano</h2><div class="orc-legenda"><span><i class="emp"></i>empenhado</span><span><i class="liq"></i>liquidado</span></div>${tapBarras(porAno)}</div>
      <div class="card"><h2 style="margin-top:0">Empenhado e liquidado por eixo</h2><div class="orc-legenda"><span><i class="emp"></i>empenhado</span><span><i class="liq"></i>liquidado</span></div>${tapBarras(porEixo)}</div></div>
    <div class="card tabela-wrap"><h2 style="margin-top:0">Resumo por ano e eixo</h2>
      <table id="tabelaOrcResumo"><tr><th>Ano</th><th>Eixo</th><th class="num">Empenhado</th><th class="num">Liquidado</th><th class="num">Saldo</th><th class="num">% liquidado</th><th class="num">Lançamentos</th></tr>
      ${(()=>{ const m = new Map(); for (const r of res.linhas){ const k = `${r.ano}|${r.eixo}`; const g = m.get(k) || {ano: r.ano, eixo: r.eixo, empenhado: 0, liquidado: 0, n: 0}; g.empenhado += Number(r.empenhado || 0); g.liquidado += Number(r.liquidado || 0); g.n++; m.set(k, g); }
        return [...m.values()].sort((a, b)=>String(a.ano).localeCompare(String(b.ano)) || a.eixo.localeCompare(b.eixo)).map(g=>`<tr><td>${esc(g.ano)}</td><td>${esc(g.eixo)}</td>
          <td class="num">${tapReal(g.empenhado)}</td><td class="num">${tapReal(g.liquidado)}</td><td class="num">${tapReal(g.empenhado - g.liquidado)}</td>
          <td class="num">${g.empenhado ? (g.liquidado / g.empenhado * 100).toFixed(1).replace(".", ",") : "0,0"}%</td><td class="num">${g.n}</td></tr>`).join("")
          || '<tr><td colspan="7" class="vazio">Nenhum lançamento.</td></tr>'; })()}</table></div>
    <form class="card" id="formOrc"><h2 style="margin-top:0">${edit ? "Editar lançamento" : "Adicionar lançamento"}</h2>
      <input type="hidden" id="orcId" value="${esc(edit?.id || "")}">
      <div class="campos">${campo("orcAno", "Ano", {tipo: "number", valor: v("ano", new Date().getFullYear()), obrigatorio: true, attrs: 'min="2000" max="2100"'})}
        ${campo("orcEixo", "Eixo", {tipo: "select", opcoes: [["", "Escolha"], ...TAP_EIXOS.map(e=>[e, e])], valor: v("eixo"), obrigatorio: true})}
        ${campo("orcProjeto", "Projeto ou ação", {valor: v("projeto")})}
        ${campo("orcEmpenhado", "Empenhado (R$)", {valor: edit ? tapReal(edit.empenhado).replace("R$ ", "") : "", obrigatorio: true, attrs: 'inputmode="decimal"'})}
        ${campo("orcLiquidado", "Liquidado (R$)", {valor: edit ? tapReal(edit.liquidado).replace("R$ ", "") : "", obrigatorio: true, attrs: 'inputmode="decimal"'})}</div>
      <div id="errosOrc"></div><div class="linha-botoes"><button class="prim" type="submit">${edit ? "Salvar alteração" : "Adicionar"}</button>
        ${edit ? '<button type="button" class="sec" id="btnOrcCancelar">Cancelar edição</button>' : ""}</div></form>
    <div class="card tabela-wrap"><h2 style="margin-top:0">Lançamentos</h2>
      <table id="tabelaOrc"><tr><th>Ano</th><th>Eixo</th><th>Projeto</th><th class="num">Empenhado</th><th class="num">Liquidado</th><th class="num">Saldo</th><th></th></tr>
      ${res.linhas.map(r=>`<tr><td>${esc(r.ano)}</td><td>${esc(r.eixo)}</td><td>${esc(r.projeto || "—")}</td>
        <td class="num">${tapReal(r.empenhado)}</td><td class="num">${tapReal(r.liquidado)}</td><td class="num">${tapReal(r.empenhado - r.liquidado)}</td>
        <td class="orc-acoes"><button type="button" data-orc-editar="${esc(r.id)}">Editar</button><button type="button" class="perigo" data-orc-excluir="${esc(r.id)}">Excluir</button></td></tr>`).join("")
        || '<tr><td colspan="7" class="vazio">Nenhum lançamento no recorte.</td></tr>'}</table></div>
    <div class="card"><h2 style="margin-top:0">Importar planilha</h2>
      <p class="sub">Colunas: <b>ano</b>, <b>eixo</b>, <b>empenhado</b>, <b>liquidado</b> (e, se houver, <b>projeto</b>). O que já existe, pelo ano + eixo + projeto, é atualizado; o resto entra como novo.</p>
      <label class="botao">Escolher .xlsx ou .csv<input type="file" id="arqOrc" accept=".xlsx,.csv,text/csv" hidden></label>
      <div id="errosOrcImport"></div><div id="resOrcImport"></div></div>`;
};
TELAS_DEPOIS["#/dashboard"] = ()=>{
  $("#dashAno").addEventListener("change", e=>{ estado.dashAno = e.target.value; estado.orcEdit = null; navegar(); });
  $("#dashEixo").addEventListener("change", e=>{ estado.dashEixo = e.target.value; estado.orcEdit = null; navegar(); });
  $("#btnDashLimpar").addEventListener("click", ()=>{ estado.dashAno = ""; estado.dashEixo = ""; estado.orcEdit = null; navegar(); });
  $("#btnDashCsv")?.addEventListener("click", async ()=>{
    const rows = (await db.list("orcamentos")).filter(r=>(!estado.dashAno || String(r.ano) === estado.dashAno) && (!estado.dashEixo || r.eixo === estado.dashEixo));
    const csv = "\ufeff" + [["ano", "eixo", "projeto", "empenhado", "liquidado", "saldo"].join(";"),
      ...rows.map(r=>[r.ano, r.eixo, r.projeto || "", String(r.empenhado).replace(".", ","), String(r.liquidado).replace(".", ","), String(r.empenhado - r.liquidado).replace(".", ",")]
        .map(x=>/[;"\n]/.test(String(x)) ? `"${String(x).replace(/"/g, '""')}"` : x).join(";"))].join("\r\n");
    baixar(`orcamento-portfolio-${hojeISO()}.csv`, csv, "text/csv;charset=utf-8");
    await registrar("dashboard exportado", {detalhe: `${rows.length} lançamentos`});
  });
  $("#formOrc").addEventListener("submit", async e=>{
    e.preventDefault();
    const id = valorDe("orcId"), ano = Number(valorDe("orcAno")), eixo = valorDe("orcEixo"), projeto = valorDe("orcProjeto");
    const empenhado = (dinheiro.de(valorDe("orcEmpenhado")) || 0) / 100, liquidado = (dinheiro.de(valorDe("orcLiquidado")) || 0) / 100;
    const erros = [];
    if (!(ano >= 2000 && ano <= 2100)) erros.push("Informe um ano entre 2000 e 2100.");
    if (!eixo) erros.push("Escolha o eixo.");
    if (!(empenhado > 0)) erros.push("Informe o empenhado.");
    if (liquidado < 0) erros.push("O liquidado não pode ser negativo.");
    if (liquidado > empenhado) erros.push("O liquidado não pode ser maior que o empenhado.");
    if (!mostrarErros("#errosOrc", erros)) return;
    const antes = id ? await db.get("orcamentos", id) : null;
    await db.put("orcamentos", {id: id || "ORC-" + uuid().slice(0, 8), ano, eixo, projeto, empenhado, liquidado, atualizado_em: agora()});
    await registrar(antes ? "lançamento orçamentário atualizado" : "lançamento orçamentário criado", {detalhe: `${ano} · ${eixo} · ${projeto || "sem projeto"}`});
    estado.orcEdit = null; toast(antes ? "Lançamento atualizado." : "Lançamento adicionado."); navegar();
  });
  $("#btnOrcCancelar")?.addEventListener("click", ()=>{ estado.orcEdit = null; navegar(); });
  $$("[data-orc-editar]").forEach(b=>b.addEventListener("click", async ()=>{
    estado.orcEdit = b.dataset.orcEditar; await navegar();
    $("#formOrc")?.scrollIntoView({behavior: "smooth", block: "start"});
  }));
  $$("[data-orc-excluir]").forEach(b=>b.addEventListener("click", async ()=>{
    const r = await db.get("orcamentos", b.dataset.orcExcluir); if (!r) return;
    if (!confirm(`Excluir o lançamento ${r.ano} · ${r.eixo} · ${r.projeto || "sem projeto"}?`)) return;
    await db.del("orcamentos", r.id); await registrar("lançamento orçamentário excluído", {detalhe: `${r.ano} · ${r.eixo}`});
    toast("Lançamento excluído."); navegar();
  }));
  $("#arqOrc").addEventListener("change", async e=>{
    const f = e.target.files[0]; if (!f) return;
    try {
      let linhas;
      if (/\.xlsx$/i.test(f.name)){
        const livro = XLSX.read(await lerArrayBuffer(f), {type: "array"}), aba = livro.Sheets[livro.SheetNames[0]];
        linhas = XLSX.utils.sheet_to_json(aba, {header: 1, raw: false, defval: ""});
      } else {
        linhas = lerCSV(await lerArquivoTexto(f));
      }
      if (!linhas.length) throw new Error("a planilha está vazia.");
      const cab = linhas[0].map(x=>normalizar(x)), idx = nome => cab.findIndex(c=>c === normalizar(nome));
      const iAno = idx("ano"), iEixo = idx("eixo"), iEmp = idx("empenhado"), iLiq = idx("liquidado");
      const iProj = idx("projeto") >= 0 ? idx("projeto") : idx("projeto ou ação");
      if ([iAno, iEixo, iEmp, iLiq].some(i=>i < 0)) throw new Error("faltam as colunas ano, eixo, empenhado e liquidado.");
      const existentes = await db.list("orcamentos");
      const chave = r => `${r.ano}|${normalizar(r.eixo)}|${normalizar(r.projeto || "")}`;
      const mapa = new Map(existentes.map(r=>[chave(r), r]));
      let novos = 0, atualizados = 0, invalidos = 0;
      for (const l of linhas.slice(1)){
        if (!l.some(x=>String(x ?? "").trim())) continue;
        const ano = Number(String(l[iAno] ?? "").trim()), eixo = String(l[iEixo] ?? "").trim(), projeto = iProj >= 0 ? String(l[iProj] ?? "").trim() : "";
        const empenhado = tapNumero(l[iEmp]), liquidado = tapNumero(l[iLiq]);
        if (!(ano >= 2000 && ano <= 2100) || !eixo || Number.isNaN(empenhado) || Number.isNaN(liquidado) || liquidado < 0 || liquidado > empenhado){ invalidos++; continue; }
        const k = `${ano}|${normalizar(eixo)}|${normalizar(projeto)}`, antes = mapa.get(k);
        const r = {id: antes?.id || "ORC-" + uuid().slice(0, 8), ano, eixo, projeto, empenhado, liquidado, atualizado_em: agora()};
        await db.put("orcamentos", r); mapa.set(k, r);
        antes ? atualizados++ : novos++;
      }
      await registrar("planilha orçamentária importada", {detalhe: `${f.name}: ${novos} novos, ${atualizados} atualizados, ${invalidos} inválidos`});
      $("#resOrcImport").innerHTML = `<p><span class="selo ok">${novos} novos</span> <span class="selo info">${atualizados} atualizados</span>
        <span class="selo ${invalidos ? "erro" : "alerta"}">${invalidos} inválidos</span></p>`;
      toast("Planilha importada."); setTimeout(navegar, 400);
    } catch(err){ mostrarErros("#errosOrcImport", ["Não consegui importar: " + err.message]); }
  });
};
