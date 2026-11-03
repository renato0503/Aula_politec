/* ================= Sprint 4 · Painel do coordenador ================= */
const DD_META_DIAS = 1;
const DD_NATUREZAS_SV = ["DNA", "sexual", "identificação humana"];

function ddMedia(lista){ const v = lista.filter(x=>x !== null && x !== undefined); return v.length ? Math.round(v.reduce((a, b)=>a + b, 0) / v.length * 10) / 10 : null; }
function ddEspera(c){ return c.distribuido_em && c.data_processamento ? ddDias(c.data_processamento, c.distribuido_em.slice(0, 10)) : null; }

// média por chave, para comparar rodada, perito e natureza
function ddAgrupar(casos, chave){
  const g = {};
  for (const c of casos){ const k = chave(c) || "—"; (g[k] ||= []).push(ddEspera(c)); }
  return Object.entries(g).map(([k, v])=>({k, media: ddMedia(v), n: v.filter(x=>x !== null).length})).sort((a, b)=>(b.media ?? -1) - (a.media ?? -1));
}
teste("Sprint 4: a média por perito ignora caso sem distribuição", ()=>{
  const cs = [{perito_id: "P1", distribuido_em: "2026-10-03T10:00:00", data_processamento: "2026-10-01"},
              {perito_id: "P1", distribuido_em: "2026-10-05T10:00:00", data_processamento: "2026-10-03"},
              {perito_id: "P2"}];
  const r = ddAgrupar(cs, c=>c.perito_id);
  return r.length === 2 && r[0].k === "P1" && r[0].media === 2 && r[1].n === 0;
});

function ddBarras(titulo, pares, cor = "var(--accent)"){
  const max = Math.max(1, ...pares.map(([, n])=>n)), w = 420, h = 26;
  return `<div class="card"><h2 style="margin-top:0">${esc(titulo)}</h2>
    <svg viewBox="0 0 ${w} ${Math.max(60, pares.length * h + 10)}" role="img" aria-label="${esc(titulo)}" style="width:100%;height:auto">
      ${pares.map(([rot, n], i)=>{ const d = Math.round(n / max * (w - 170)), y = i * h + 6;
        return `<text x="0" y="${y + 13}" font-size="12" fill="var(--ink2)">${esc(String(rot).slice(0, 22))}</text>
          <rect x="150" y="${y + 2}" width="${d}" height="14" rx="3" fill="${cor}"></rect>
          <text x="${156 + d}" y="${y + 13}" font-size="12" fill="var(--ink)">${n}</text>`; }).join("")}
    </svg></div>`;
}

const ddPainelAntigo = TELAS["#/painel"];
TELAS["#/painel"] = async ()=>{
  let html = await ddPainelAntigo();
  const [cs, ps, rs] = await Promise.all([db.list("casos"), ddPeritos(), db.list("rodadas")]);
  const distribuidos = cs.filter(c=>c.distribuido_em);
  const porPerito = ddAgrupar(distribuidos, c=>ps[c.perito_id]?.nome || c.perito_id);
  const porNatureza = ddAgrupar(distribuidos, c=>c.natureza);
  const porRodada = ddAgrupar(distribuidos, c=>c.rodada_id);
  const tempo = ddMedia(distribuidos.map(ddEspera));
  const foraMeta = distribuidos.filter(c=>{ const e = ddEspera(c); return e !== null && e > DD_META_DIAS; }).length;
  return html + `<div class="card" id="ddCoordenador"><h2 style="margin-top:0">Painel do coordenador (Sprint 4)</h2>
      <p class="sub">Tempo entre o processamento e a distribuição. Meta: até ${DD_META_DIAS} dia.</p>
      <div class="grade">
        <div class="card kpi"><div class="v" data-dd-ind="tempo">${tempo === null ? "—" : tempo + " dia(s)"}</div><div class="r">tempo médio</div></div>
        <div class="card kpi"><div class="v" data-dd-ind="meta">${tempo !== null && tempo <= DD_META_DIAS ? '<span class="ok-txt">na meta</span>' : '<span class="erro-txt">fora da meta</span>'}</div><div class="r">meta de ${DD_META_DIAS} dia</div></div>
        <div class="card kpi"><div class="v" data-dd-ind="fora">${foraMeta}</div><div class="r">casos acima da meta</div></div>
        <div class="card kpi"><div class="v" data-dd-ind="distribuidos">${distribuidos.length}</div><div class="r">casos distribuídos</div></div></div>
      <div class="duas-colunas">
        <div class="card tabela-wrap"><h2 style="margin-top:0">Por perito (dias)</h2><table id="tabelaPerito"><tr><th>Perito</th><th class="num">Casos</th><th class="num">Média</th></tr>
          ${porPerito.map(x=>`<tr><td>${esc(x.k)}</td><td class="num">${x.n}</td><td class="num">${x.media ?? "—"}</td></tr>`).join("")}</table></div>
        <div class="card tabela-wrap"><h2 style="margin-top:0">Por natureza (dias)</h2><table id="tabelaNatureza"><tr><th>Natureza</th><th class="num">Casos</th><th class="num">Média</th></tr>
          ${porNatureza.map(x=>`<tr><td>${esc(x.k)}</td><td class="num">${x.n}</td><td class="num">${x.media ?? "—"}</td></tr>`).join("")}</table></div></div>
      <div class="card tabela-wrap"><h2 style="margin-top:0">Por rodada (dias)</h2><table id="tabelaRodada"><tr><th>Rodada</th><th class="num">Casos</th><th class="num">Média</th></tr>
        ${porRodada.map(x=>`<tr><td>${esc(x.k)}</td><td class="num">${x.n}</td><td class="num">${x.media ?? "—"}</td></tr>`).join("")}</table></div>
      ${ddBarras("Casos por natureza", DD_NATUREZAS_SV.map(n=>[n, cs.filter(c=>c.natureza === n).length]), "var(--verde)")}
      <div class="linha-botoes nao-imprimir"><button class="prim" id="btnDdCsv">${icone("download")} Exportar CSV</button>
        <button onclick="window.print()">${icone("imprimir")} Imprimir em A4</button></div></div>`;
};
TELAS_DEPOIS["#/painel"] = ()=>{
  $("#btnDdCsv")?.addEventListener("click", async ()=>{
    const [cs, ps] = await Promise.all([db.list("casos"), ddPeritos()]);
    const linhas = [["id_caso", "protocolo", "rodada", "tipo", "natureza", "status", "processamento", "perito", "distribuido_em", "espera_dias"]].concat(
      cs.map(c=>[c.id_caso, c.protocolo, c.rodada_id, c.tipo, c.natureza || "", c.status, c.data_processamento || "",
        ps[c.perito_id]?.nome || "", c.distribuido_em || "", ddEspera(c) ?? ""]));
    const csv = "﻿" + linhas.map(l=>l.map(x=>/[;"\n]/.test(String(x)) ? `"${String(x).replace(/"/g, '""')}"` : String(x)).join(";")).join("\r\n");
    baixar(`dna-${hojeISO()}.csv`, csv, "text/csv;charset=utf-8");
    await registrar("relatório exportado", {detalhe: `${cs.length} casos`});
  });
};

/* ================= Sprint 5 · Importar a planilha de protocolos ================= */
const DD_CAMPOS_PLANILHA = {
  protocolo: {rotulo: "Protocolo", sinonimos: ["protocolo", "numero", "n do protocolo"]},
  tipo: {rotulo: "Tipo (ordinario ou cobranca)", sinonimos: ["tipo", "fila"]},
  rodada: {rotulo: "Rodada", sinonimos: ["rodada", "placa", "id da rodada"]},
  processamento: {rotulo: "Data do processamento", sinonimos: ["processamento", "data do processamento", "data"]},
};

// devolve aceitas e recusadas, comparando com os protocolos já cadastrados
function ddConferirPlanilha(linhas, mapa, jaCadastrados){
  const aceitas = [], recusadas = [], vistos = new Set(jaCadastrados);
  linhas.forEach((l, i)=>{
    const n = i + 2;
    if (l.every(c=>String(c ?? "").trim() === "")) return;
    const col = k => mapa[k] >= 0 ? String(l[mapa[k]] ?? "").trim() : "";
    const protocolo = col("protocolo"), tipo = normalizar(col("tipo")) || "ordinario";
    if (!protocolo) return recusadas.push({linha: n, protocolo: "", motivo: "protocolo vazio"});
    if (jaCadastrados.has(protocolo)) return recusadas.push({linha: n, protocolo, motivo: "protocolo já cadastrado"});
    if (vistos.has(protocolo)) return recusadas.push({linha: n, protocolo, motivo: "protocolo repetido na planilha"});
    vistos.add(protocolo);
    if (!["ordinario", "cobranca"].includes(tipo)) return recusadas.push({linha: n, protocolo, motivo: `tipo "${col("tipo")}" inválido`});
    const proc = dataDeTexto(col("processamento"));
    if (col("processamento") && !proc) return recusadas.push({linha: n, protocolo, motivo: "data do processamento ilegível"});
    aceitas.push({protocolo, tipo, rodada: col("rodada"), data_processamento: proc ? proc.slice(0, 10) : null});
  });
  return {aceitas, recusadas};
}
teste("Sprint 5: a planilha recusa protocolo repetido e tipo inválido", ()=>{
  const r = ddConferirPlanilha([["2026.1", "ordinario"], ["2026.1", "ordinario"], ["2026.2", "xyz"]],
    {protocolo: 0, tipo: 1, rodada: -1, processamento: -1}, new Set(["2026.1"]));
  return r.aceitas.length === 0 && r.recusadas.length === 3;
});

let ddPlanilha = null;
TELAS["#/importar"] = async ()=>{
  const hist = (await db.list("importacoes")).sort((a, b)=>(b.data || "").localeCompare(a.data || "")).slice(0, 5);
  return `<h1>Importar a planilha de protocolos</h1>
    <p class="sub">A planilha de controle dos protocolos entra como CSV. O app associa as colunas e compara com os casos já cadastrados.</p>
    <div class="card"><label class="botao">Escolher o CSV<input type="file" id="arqDd" accept=".csv,.txt" hidden></label>
      <div id="ddMapa"></div><div id="ddErrosPlanilha"></div><div id="ddRelatorio"></div></div>
    <div class="card tabela-wrap"><h2 style="margin-top:0">Últimas importações</h2><table id="tabelaHistoricoDd"><tr><th>Data</th><th>Arquivo</th><th class="num">Aceitas</th><th class="num">Recusadas</th></tr>
      ${hist.map(h=>`<tr><td>${dataBR(h.data)}</td><td>${esc(h.arquivo)}</td><td class="num">${h.aceitas}</td><td class="num">${h.recusadas}</td></tr>`).join("")
        || '<tr><td colspan="4" class="vazio">Nenhuma importação.</td></tr>'}</table></div>`;
};
TELAS_DEPOIS["#/importar"] = ()=>{
  $("#arqDd")?.addEventListener("change", async e=>{
    const f = e.target.files[0]; if (!f) return;
    const linhas = lerCSV(await lerArquivoTexto(f));
    if (!linhas.length) return mostrarErros("#ddErrosPlanilha", ["O arquivo está vazio."]);
    const cabecalho = linhas[0].map(c=>String(c ?? "").trim());
    const mapa = sugerirColunas(cabecalho, Object.fromEntries(Object.entries(DD_CAMPOS_PLANILHA).map(([k, c])=>[k, c.sinonimos])));
    ddPlanilha = {arquivo: f.name, linhas: linhas.slice(1), cabecalho, mapa};
    $("#ddMapa").innerHTML = `<p class="sub"><b>${esc(f.name)}</b> · ${ddPlanilha.linhas.length} linha(s)</p>
      <div class="campos">${Object.entries(DD_CAMPOS_PLANILHA).map(([k, c])=>campo("ddMap-" + k, c.rotulo, {tipo: "select",
        opcoes: [["-1", "Sem esta coluna"], ...cabecalho.map((h, i)=>[String(i), h])], valor: String(mapa[k] ?? -1)})).join("")}</div>
      <div class="linha-botoes"><button class="prim" id="btnDdImportar">Importar e conferir</button></div>`;
    Object.keys(DD_CAMPOS_PLANILHA).forEach(k=>$("#ddMap-" + k).addEventListener("change", ev=>{ ddPlanilha.mapa[k] = Number(ev.target.value); }));
    $("#btnDdImportar").addEventListener("click", async ()=>{
      const P = ddPlanilha, ja = new Set((await db.list("casos")).map(c=>c.protocolo));
      const r = ddConferirPlanilha(P.linhas, P.mapa, ja);
      const hoje = agora();
      for (const a of r.aceitas) await db.put("casos", {id_caso: uuid(), rodada_id: a.rodada || "IMPORTADO", protocolo: a.protocolo, tipo: a.tipo,
        natureza: "", status: "processado", data_processamento: a.data_processamento, perito_id: null, distribuido_em: null, importado_em: hoje});
      await db.put("importacoes", {id: uuid(), arquivo: P.arquivo, data: hoje, aceitas: r.aceitas.length, recusadas: r.recusadas.length,
        detalhe: r.recusadas.slice(0, 20)});
      await registrar("planilha de protocolos importada", {detalhe: `${r.aceitas.length} aceitas, ${r.recusadas.length} recusadas`});
      $("#ddRelatorio").innerHTML = `<h2 style="margin-top:0" id="ddTituloRel">Relatório da importação</h2>
        <p><span class="selo ok">${r.aceitas.length} aceitas</span> <span class="selo erro">${r.recusadas.length} recusadas</span></p>
        <div class="tabela-wrap"><table id="tabelaRecusadasDd"><tr><th>Linha</th><th>Protocolo</th><th>Motivo</th></tr>
        ${r.recusadas.map(x=>`<tr><td class="num">${x.linha}</td><td class="mono">${esc(x.protocolo || "—")}</td><td>${esc(x.motivo)}</td></tr>`).join("")
          || '<tr><td colspan="3" class="vazio">Nenhuma linha recusada.</td></tr>'}</table></div>`;
      toast(`${r.aceitas.length} protocolo(s) importado(s).`);
    });
  });
};
