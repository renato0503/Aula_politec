/* ================= Sprint 3 · Importar a planilha de prontuários, ler o arquivo digital e comparar ================= */
/* Campos da planilha de prontuários e seus sinônimos de coluna (a associação é sugerida e pode ser corrigida). */
const DOC_CAMPOS = {
  numero: {rotulo: "Número do prontuário", sinonimos: ["numero do prontuario", "numero", "prontuario", "nº", "no"]},
  caixa: {rotulo: "Caixa", sinonimos: ["caixa", "caixa de arquivo", "identificacao da caixa", "id caixa"]},
  ano: {rotulo: "Ano", sinonimos: ["ano", "ano do prontuario", "exercicio"]},
};
const DOC_DIGITAIS = {numero: {rotulo: "Número do prontuário (no arquivo digital)", sinonimos: ["numero do prontuario", "numero", "prontuario", "nº", "no"]}};
const docNum = v => String(v ?? "").trim().replace(/[.\s]/g, "");
function docNumeroValido(v){ return /^\d{4,12}$/.test(docNum(v)); }

/* Relê a planilha e devolve o que entra, o que é recusado e o que diverge do arquivo digital. */
function docConferirPlanilha(linhas, cabecalho, mapa, jaCadastrados, digitais){
  const aceitas = [], recusadas = [], divergentes = [], vistos = new Set();
  const col = (l, k)=> mapa[k] >= 0 ? l[mapa[k]] : "";
  linhas.forEach((l, i)=>{
    const n = i + 2;   // linha do arquivo (1 é o cabeçalho)
    if (l.every(c=>String(c ?? "").trim() === "")) return;
    const bruto = String(col(l, "numero") ?? "").trim(), numero = docNum(bruto), motivo = m => recusadas.push({linha: n, numero: bruto, motivo: m});
    if (!numero) return motivo("número do prontuário vazio");
    if (!docNumeroValido(numero)) return motivo(`número "${bruto}" fora do formato`);
    if (vistos.has(numero)) return motivo("prontuário repetido na planilha");
    vistos.add(numero);
    if (jaCadastrados.has(numero)) return motivo("prontuário já cadastrado em outra caixa (RN01)");
    aceitas.push({numero: bruto, chave: numero, linha: n, caixa: String(col(l, "caixa") || "").trim(), ano: String(col(l, "ano") || "").trim()});
  });
  const noDigital = new Set(digitais);
  for (const a of aceitas) if (!noDigital.has(a.chave)) divergentes.push({...a, motivo: "não localizado no arquivo digital"});
  for (const d of noDigital) if (!vistos.has(d)) divergentes.push({numero: d, chave: d, linha: 0, motivo: "está no arquivo digital e não veio na planilha"});
  return {aceitas, recusadas, divergentes};
}
teste("Conferência: aceita a linha válida, recusa a repetida e aponta a divergente", ()=>{
  const r = docConferirPlanilha([["2019.000010", "CX-001", "2019"], ["2019.000011", "CX-001", "2019"], ["2019.000010", "CX-001", "2019"], ["abc", "CX-001", "2019"]],
    ["numero", "caixa", "ano"], {numero: 0, caixa: 1, ano: 2}, new Set(), new Set(["2019000010"]));
  return r.aceitas.length === 2 && r.recusadas.length === 2 && r.divergentes.length === 1
    && r.divergentes[0].chave === "2019000011" && r.recusadas.map(x=>x.motivo).join("|").includes("repetido");
});
teste("Conferência: prontuário já cadastrado em outra caixa é recusado (RN01)", ()=>{
  const r = docConferirPlanilha([["2019.000010", "CX-001", "2019"]], ["numero"], {numero: 0, caixa: 1, ano: 2}, new Set(["2019000010"]), new Set(["2019000010"]));
  return r.aceitas.length === 0 && r.recusadas[0].motivo.includes("RN01");
});
teste("Número de prontuário: aceita 2019.000010 e recusa 19.1", ()=> docNumeroValido("2019.000010") && !docNumeroValido("19.1") && !docNumeroValido(""));

/* grava vários registros numa transação só (850 linhas não podem ir uma a uma) */
function docGravarLote(store, linhas){
  return new Promise((ok, erro)=>{
    const tx = db.con.transaction(store, "readwrite"), st = tx.objectStore(store);
    for (const l of linhas) st.put(l);
    tx.oncomplete = ()=> ok(linhas.length);
    tx.onerror = ()=> erro(tx.error);
  });
}

/* ---------- tela de importação ---------- */
const docEstado = ()=> estado.docImport || (estado.docImport = {relacao: null, digital: null, relMapa: {}, digMapa: {}, relErro: "", digErro: ""});
TELAS["#/importar"] = async ()=>{
  const st = docEstado(), cs = (await db.list("caixas")).sort((a, b)=>String(a.id_caixa).localeCompare(String(b.id_caixa)));
  return `<h1>Importar a planilha de prontuários</h1>
    <p class="sub">Duas entradas: a planilha de prontuários da caixa e o índice do arquivo digital. A comparação mostra o que entrou, o que foi recusado e o que diverge.</p>
    <div class="card" id="docBlocoRelacao"><h2 style="margin-top:0">1. Planilha de prontuários</h2>
      <label class="botao">Escolher a planilha<input type="file" id="arqRelacao" accept=".csv,.txt" hidden></label>
      ${st.relacao ? `<p class="sub">Arquivo: <b>${esc(st.relacao.arquivo)}</b> · ${st.relacao.linhas.length} linha(s) de dados.</p>
        <div class="campos">${Object.entries(DOC_CAMPOS).map(([k, c])=>campo("mapRel_" + k, c.rotulo, {tipo: "select",
          opcoes: [["", "Sem esta coluna"], ...st.relacao.cabecalho.map((h, i)=>[String(i), h])], valor: String(st.relMapa[k] ?? "")})).join("")}</div>`
        : '<p class="sub">Nenhuma planilha carregada.</p>'}
      <div id="docErrosRel"></div></div>
    <div class="card" id="docBlocoDigital"><h2 style="margin-top:0">2. Índice do arquivo digital</h2>
      <p class="sub">Relação dos prontuários localizados no PDF digitalizado (o arquivo que o DMIT entrega, já extraído para texto).</p>
      <label class="botao">Escolher o índice<input type="file" id="arqDigital" accept=".csv,.txt" hidden></label>
      ${st.digital ? `<p class="sub">Arquivo: <b>${esc(st.digital.arquivo)}</b> · ${st.digital.linhas.length} prontuário(s) no índice.</p>
        <div class="campos">${Object.entries(DOC_DIGITAIS).map(([k, c])=>campo("mapDig_" + k, c.rotulo, {tipo: "select",
          opcoes: [["", "Sem esta coluna"], ...st.digital.cabecalho.map((h, i)=>[String(i), h])], valor: String(st.digMapa[k] ?? "")})).join("")}</div>`
        : '<p class="sub">Nenhum índice carregado.</p>'}
      <div id="docErrosDig"></div></div>
    <form class="card" id="formDocImport"><div class="campos">
      ${campo("docCaixaDestino", "Caixa que recebe os prontuários", {tipo: "select", opcoes: [["nova", "Nova caixa (identificação abaixo)"], ...cs.map(c=>[c.id_caixa, `${c.id_caixa} · ${c.setor_origem}`])]})}
      ${campo("docIdCaixa", "Identificação da nova caixa", {valor: "", ajuda: "Ex.: CX-013."})}
      ${campo("docSetor", "Setor de origem", {valor: ""})}
      ${campo("docResponsavel", "Responsável pela conferência", {valor: ""})}</div>
    <div id="docErrosImport"></div><div class="linha-botoes"><button class="prim" type="submit">Importar e conferir</button></div></form>`;
};
TELAS_DEPOIS["#/importar"] = ()=>{
  const st = docEstado();
  const ler = async (arq, chave, mapaId, sinonimos, alvoErro)=>{
    const texto = await lerArquivoTexto(arq), linhas = lerCSV(texto);
    if (!linhas.length) return mostrarErros(alvoErro, ["O arquivo está vazio."]);
    const cabecalho = linhas[0].map(c=>String(c ?? "").trim());
    st[chave] = {arquivo: arq.name, cabecalho, linhas: linhas.slice(1)};
    st[mapaId] = sugerirColunas(cabecalho, sinonimos);
    navegar();
  };
  $("#arqRelacao")?.addEventListener("change", async e=>{
    const f = e.target.files[0]; if (!f) return;
    await ler(f, "relacao", "relMapa", Object.fromEntries(Object.entries(DOC_CAMPOS).map(([k, c])=>[k, c.sinonimos])), "#docErrosRel");
  });
  $("#arqDigital")?.addEventListener("change", async e=>{
    const f = e.target.files[0]; if (!f) return;
    await ler(f, "digital", "digMapa", Object.fromEntries(Object.entries(DOC_DIGITAIS).map(([k, c])=>[k, c.sinonimos])), "#docErrosDig");
  });
  Object.keys(DOC_CAMPOS).forEach(k=>$("#mapRel_" + k)?.addEventListener("change", e=>{ st.relMapa[k] = Number(e.target.value); }));
  Object.keys(DOC_DIGITAIS).forEach(k=>$("#mapDig_" + k)?.addEventListener("change", e=>{ st.digMapa[k] = Number(e.target.value); }));
  $("#formDocImport")?.addEventListener("submit", async e=>{
    e.preventDefault();
    const erros = [];
    if (!st.relacao) erros.push("Carregue a planilha de prontuários.");
    if (!st.digital) erros.push("Carregue o índice do arquivo digital.");
    if (st.relacao && !(st.relMapa.numero >= 0)) erros.push("Associe a coluna do número do prontuário.");
    const destino = valorDe("docCaixaDestino");
    let idCaixa = destino;
    if (destino === "nova"){
      idCaixa = valorDe("docIdCaixa");
      if (!idCaixa) erros.push("Informe a identificação da nova caixa.");
      if (!valorDe("docSetor")) erros.push("Informe o setor de origem.");
      if (!valorDe("docResponsavel")) erros.push("Informe o responsável pela conferência.");
    }
    if (!mostrarErros("#docErrosImport", erros)) return;
    const existentes = await db.list("prontuarios"), jaCadastrados = new Set(existentes.map(p=>docNum(p.numero)));
    const digCol = st.digMapa.numero;
    const digitais = new Set((st.digital.linhas || []).map(l=>docNum(l[digCol])).filter(Boolean));
    const r = docConferirPlanilha(st.relacao.linhas, st.relacao.cabecalho, st.relMapa, jaCadastrados, digitais);
    // grava o que entrou
    const novas = r.aceitas.map(a=>({numero: a.numero, caixa_id: idCaixa, conferido: false, digital: true, importado_em: agora()}));
    if (novas.length) await docGravarLote("prontuarios", novas);
    let caixa = await db.get("caixas", idCaixa);
    if (!caixa){
      caixa = {id_caixa: idCaixa, setor_origem: valorDe("docSetor"), responsavel: valorDe("docResponsavel"), data: hojeISO(),
        qtd: novas.length, status: "pendente", criado_em: agora(), lacrada_por: null, lacrada_em: null};
      await db.put("caixas", caixa);
    } else {
      await db.put("caixas", {...caixa, qtd: (await db.porIndice("prontuarios", "caixa_id", idCaixa)).length});
    }
    await db.put("log", {id: uuid(), caixa_id: idCaixa, acao: "planilha importada", perfil: estado.perfil || "", data_hora: agora(),
      detalhe: `${novas.length} aceitas, ${r.recusadas.length} recusadas, ${r.divergentes.length} divergentes`});
    await registrar("planilha importada", {detalhe: `${idCaixa} · ${novas.length} prontuários`});
    estado.docRelatorio = {caixa_id: idCaixa, ...r};
    toast(`Importação concluída: ${novas.length} prontuário(s).`); location.hash = "#/importar";
    await navegar();
  });
};

/* ---------- relatório da conferência ---------- */
TELAS["#/relatorio-importacao"] = async ()=>{
  const rel = estado.docRelatorio;
  if (!rel) return `<div class="card vazio">Nenhuma importação neste navegador. <a href="#/importar">Importar planilha</a></div>`;
  return `<h1>Relatório da importação</h1>
    <p class="sub">Caixa ${esc(rel.caixa_id)} · ${rel.aceitas.length} aceitas, ${rel.recusadas.length} recusadas e ${rel.divergentes.length} divergentes.</p>
    <div class="grade"><div class="card kpi"><div class="v" id="docQtdAceitas">${rel.aceitas.length}</div><div class="r">linhas aceitas</div></div>
      <div class="card kpi"><div class="v" id="docQtdRecusadas">${rel.recusadas.length}</div><div class="r">linhas recusadas</div></div>
      <div class="card kpi"><div class="v" id="docQtdDivergentes">${rel.divergentes.length}</div><div class="r">prontuários divergentes</div></div></div>
    <div class="card tabela-wrap"><h2 style="margin-top:0">Aceitas</h2><table id="tabelaAceitas"><tr><th>Linha</th><th>Prontuário</th><th>Caixa</th><th>Ano</th></tr>
      ${rel.aceitas.map(a=>`<tr><td class="num">${a.linha}</td><td class="mono">${esc(a.numero)}</td><td>${esc(a.caixa || "—")}</td><td>${esc(a.ano || "—")}</td></tr>`).join("")
        || '<tr><td colspan="4" class="vazio">Nenhuma linha aceita.</td></tr>'}</table></div>
    <div class="card tabela-wrap"><h2 style="margin-top:0">Recusadas</h2><table id="tabelaRecusadas"><tr><th>Linha</th><th>Prontuário</th><th>Motivo</th></tr>
      ${rel.recusadas.map(a=>`<tr><td class="num">${a.linha}</td><td class="mono">${esc(a.numero || "—")}</td><td>${esc(a.motivo)}</td></tr>`).join("")
        || '<tr><td colspan="3" class="vazio">Nenhuma linha recusada.</td></tr>'}</table></div>
    <div class="card tabela-wrap"><h2 style="margin-top:0">Divergentes</h2><table id="tabelaDivergentes"><tr><th>Linha</th><th>Prontuário</th><th>Motivo</th></tr>
      ${rel.divergentes.map(a=>`<tr><td class="num">${a.linha || "—"}</td><td class="mono">${esc(a.numero)}</td><td>${esc(a.motivo)}</td></tr>`).join("")
        || '<tr><td colspan="3" class="vazio">Nenhuma divergência.</td></tr>'}</table></div>
    <div class="linha-botoes"><a class="botao prim" href="#/importar">Nova importação</a></div>`;
};
