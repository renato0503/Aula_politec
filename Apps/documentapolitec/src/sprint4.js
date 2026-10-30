/* ================= Sprint 4 · Busca por nome com índice autorizado (RN03) ================= */
/* O app não guarda nome em claro. O índice autorizado traz número + nome; o app
   guarda só o hash do nome normalizado, e a busca hasheia o que foi digitado. */
const DOC_SAL = "politec-arquivo";
function docHash(texto){
  const s = DOC_SAL + "|" + normalizar(texto);
  let h1 = 0x811c9dc5, h2 = 0x1000193;
  for (const b of new TextEncoder().encode(s)){ h1 ^= b; h1 = Math.imul(h1, 0x01000193) >>> 0; h2 = Math.imul(h2 ^ b, 0x85ebca6b) >>> 0; }
  return h1.toString(16).padStart(8, "0") + h2.toString(16).padStart(8, "0");
}
teste("Sprint 4: o hash do nome é estável e ignora caixa e acento", ()=>{
  return docHash("José  da Silva") === docHash("jose da silva") && docHash("a") !== docHash("b") && docHash("Maria") !== "Maria";
});
function docIniciais(nome){ return String(nome || "").trim().split(/\s+/).filter(Boolean).map(p=>p[0].toUpperCase()).join(". "); }

// trilha de consultas: toda busca por nome fica registrada (RN03)
async function docConsultarNome(termo){
  const h = docHash(termo);
  const idx = (await db.list("indice_nomes")).filter(i=>i.nome_hash === h);
  await db.put("consultas", {id: uuid(), termo_hash: h, termo_iniciais: docIniciais(termo), resultados: idx.length, data: agora(), perfil: estado.perfil});
  const caixas = await db.list("caixas");
  return idx.map(i=>({numero: i.numero, caixa: caixas.find(c=>c.id_caixa === i.caixa_id) || null}));
}
const docPodeBuscarNome = perfil => perfil === "gestor";
teste("RN03: só o gestor consulta o índice de nomes", ()=> docPodeBuscarNome("gestor") && !docPodeBuscarNome("papiloscopista"));

TELAS["#/busca-nome"] = async ()=>{
  const autorizado = docPodeBuscarNome(estado.perfil);
  const r = estado.docBuscaNome || null;
  const cons = (await db.list("consultas")).sort((a, b)=>(b.data || "").localeCompare(a.data || "")).slice(0, 5);
  return `<h1>Buscar por nome do cidadão</h1>
    <p class="sub">Consulta ao <b>índice autorizado</b>. O app guarda só o hash do nome, nunca o nome em claro (LGPD). Toda consulta fica na trilha (RN03).</p>
    ${!autorizado ? `<div class="card pendente" id="docSemAcesso"><b>Acesso restrito ao gestor documental.</b> O perfil ${esc(estado.perfil || "—")} não consulta o índice de nomes.</div>`
    : `<div class="card"><label class="botao">Carregar o índice autorizado (CSV número;nome)<input type="file" id="arqIndice" accept=".csv,.txt" hidden></label>
        <div id="docErrosIndice"></div><div id="docResIndice"></div></div>
      <form class="card" id="formBuscaNome"><div class="campos">${campo("docNome", "Nome do cidadão", {valor: r?.termo || ""})}</div>
        <div class="linha-botoes"><button class="prim" type="submit">Buscar</button></div></form>
      ${r ? `<div class="card" id="docResNome"><h2 style="margin-top:0">${r.itens.length} resultado(s)</h2>
        ${r.itens.length ? `<table><tr><th>Prontuário</th><th>Caixa</th><th>Setor</th><th>Situação</th></tr>
          ${r.itens.map(x=>`<tr><td class="mono">${esc(x.numero)}</td><td><a href="#/caixa/${encodeURIComponent(x.caixa?.id_caixa || "")}">${esc(x.caixa?.id_caixa || "—")}</a></td>
            <td>${esc(x.caixa?.setor_origem || "—")}</td><td>${esc(DOC_STATUS[x.caixa?.status] || x.caixa?.status || "—")}</td></tr>`).join("")}</table>`
          : '<p class="sub">Nenhum prontuário com esse nome no índice autorizado.</p>'}</div>` : ""}
      <div class="card tabela-wrap"><h2 style="margin-top:0">Trilha de consultas (RN03)</h2><table id="tabelaConsultas"><tr><th>Data</th><th>Perfil</th><th>Iniciais</th><th class="num">Resultados</th></tr>
        ${cons.map(c=>`<tr><td>${dataBR(c.data)}</td><td>${esc(c.perfil)}</td><td>${esc(c.termo_iniciais || "—")}</td><td class="num">${c.resultados}</td></tr>`).join("")
          || '<tr><td colspan="4" class="vazio">Nenhuma consulta.</td></tr>'}</table></div>`}`;
};
TELAS_DEPOIS["#/busca-nome"] = ()=>{
  $("#arqIndice")?.addEventListener("change", async e=>{
    const f = e.target.files[0]; if (!f) return;
    const linhas = lerCSV(await lerArquivoTexto(f)).slice(1).filter(l=>l.some(c=>String(c ?? "").trim()));
    let n = 0, semCaixa = 0;
    const caixas = new Set((await db.list("caixas")).map(c=>c.id_caixa));
    for (const l of linhas){
      const numero = String(l[0] ?? "").trim(), nome = String(l[1] ?? "").trim(), caixa = String(l[2] ?? "").trim();
      if (!numero || !nome) continue;
      if (caixa && !caixas.has(caixa)) semCaixa++;
      await db.put("indice_nomes", {numero, nome_hash: docHash(nome), nome_iniciais: docIniciais(nome), caixa_id: caixa || null});
      n++;
    }
    await registrar("índice de nomes carregado", {detalhe: `${n} nomes`});
    $("#docResIndice").innerHTML = `<p class="ok-txt">${n} nome(s) no índice${semCaixa ? ` · ${semCaixa} com caixa fora do cadastro` : ""}.</p>`;
  });
  $("#formBuscaNome")?.addEventListener("submit", async e=>{
    e.preventDefault();
    const termo = valorDe("docNome"); if (!termo) return;
    const itens = await docConsultarNome(termo);
    estado.docBuscaNome = {termo, itens}; navegar();
  });
};

/* ================= Sprint 5 · Etiqueta com código de conferência ================= */
/* QR Code exige biblioteca embutida: fica como "a implementar" no botão escondido.
   O app gera um código de conferência e um código de barras Code 39 em SVG. */
const CODE39 = {"0":"101001101101","1":"110100101011","2":"101100101011","3":"110110010101","4":"101001101011","5":"110100110101",
  "6":"101100110101","7":"101001011011","8":"110100101101","9":"101100101101","A":"110101001011","B":"101101001011",
  "C":"110110100101","D":"101011001011","E":"110101100101","F":"101101100101","G":"101010011011","H":"110101001101",
  "I":"101101001101","J":"101011001101","K":"110101010011","L":"101101010011","M":"110110101001","N":"101011010011",
  "O":"110101101001","P":"101101101001","Q":"101010110011","R":"110101011001","S":"101101011001","T":"101011011001",
  "U":"110010101011","V":"100110101011","W":"110011010101","X":"100101101011","Y":"110010110101","Z":"100110110101",
  "-":"100101011011",".":"110010101101"," ":"100110101101","$":"100100100101","/":"100100101001","+":"100101001001",
  "%":"101001001001","*":"100101101101"};
function docCodigo39(texto){
  const t = "*" + String(texto).toUpperCase().replace(/[^0-9A-Z\-. $/+%]/g, "") + "*";
  return [...t].map(c=>CODE39[c] || CODE39["-"]).join("0");
}
teste("Sprint 5: o Code 39 começa e termina com o caractere de início", ()=>{
  const b = docCodigo39("CX-001"); return b.startsWith(CODE39["*"]) && b.endsWith(CODE39["*"]) && /^[01]+$/.test(b);
});
function docBarrasSVG(texto, altura = 44){
  const bits = docCodigo39(texto), w = bits.length * 2;
  return `<svg viewBox="0 0 ${w} ${altura}" role="img" aria-label="Código de barras ${esc(texto)}" style="width:100%;max-width:340px;height:auto">
    <rect width="${w}" height="${altura}" fill="#fff"/>
    ${[...bits].map((b, i)=>b === "1" ? `<rect x="${i * 2}" y="2" width="2" height="${altura - 12}" fill="#000"/>` : "").join("")}
    <text x="${w / 2}" y="${altura - 2}" font-size="9" text-anchor="middle" fill="#000">${esc(texto)}</text></svg>`;
}
// código de conferência: soma dos prontuários da caixa + 4 primeiros do hash
function docCodigoConferencia(caixa, prontuarios){
  const nums = prontuarios.map(p=>p.numero).sort().join("|");
  return `${String(caixa.id_caixa).replace(/[^A-Za-z0-9]/g, "").slice(-3).toUpperCase()}-${docHash(nums).slice(0, 4).toUpperCase()}`;
}
teste("Sprint 5: o código de conferência muda com a relação", ()=>{
  const c = {id_caixa: "CX-001"};
  return docCodigoConferencia(c, [{numero: "A"}]) !== docCodigoConferencia(c, [{numero: "B"}]);
});

const docCaixaAntiga = TELAS["#/caixa/:id"], docCaixaAntigaDepois = TELAS_DEPOIS["#/caixa/:id"];
TELAS["#/caixa/:id"] = async (p)=>{
  let html = await docCaixaAntiga(p);
  const c = await db.get("caixas", p.id); if (!c) return html;
  const ps = await db.porIndice("prontuarios", "caixa_id", p.id);
  const cod = docCodigoConferencia(c, ps);
  const card = `<div class="card" id="docEtiqueta"><h2 style="margin-top:0">Etiqueta da caixa (Sprint 5)</h2>
    <p class="sub">Código de conferência: <b class="mono" id="docCodConf">${esc(cod)}</b>. O QR Code depende de biblioteca embutida e está no passo a passo do botão escondido.</p>
    <div class="documento-a4" style="padding:22px 26px;max-width:420px">
      <div style="font:600 11px/1.4 var(--ui);letter-spacing:.06em;text-transform:uppercase;color:#0a2f5c">POLITEC/MT · Arquivo central</div>
      <div style="font:700 20px/1.3 var(--ui);margin:6px 0">Caixa ${esc(c.id_caixa)}</div>
      <div style="font-size:13px">${esc(c.setor_origem)} · ${ps.length} prontuários<br>Conferência: ${esc(c.responsavel)} · ${dataCurtaBR(c.data)}</div>
      <div style="margin-top:10px">${docBarrasSVG(cod)}</div>
      <div style="font:700 14px/1.4 var(--ui);margin-top:4px">${esc(cod)}</div>
    </div>
    <div class="linha-botoes nao-imprimir"><button onclick="window.print()">${icone("imprimir")} Imprimir a etiqueta</button></div></div>
    <div class="card" id="docLeitura"><h2 style="margin-top:0">Leitura na conferência</h2>
      <p class="sub">Digite ou leia o código da etiqueta para confirmar que é esta caixa.</p>
      <div class="campos">${campo("docLeituraCod", "Código lido", {attrs: 'placeholder="CX0-1A2B"'})}</div>
      <div id="docErrosLeitura"></div><div class="linha-botoes"><button id="btnDocLeitura">Conferir o código</button></div></div>`;
  return html + card;
};
TELAS_DEPOIS["#/caixa/:id"] = async (p)=>{
  await docCaixaAntigaDepois(p);
  $("#btnDocLeitura")?.addEventListener("click", async ()=>{
    const c = await db.get("caixas", p.id), ps = await db.porIndice("prontuarios", "caixa_id", p.id);
    const cod = docCodigoConferencia(c, ps);
    const lido = valorDe("docLeituraCod").toUpperCase();
    if (lido === cod){
      await db.put("log", {id: uuid(), caixa_id: p.id, acao: "código de conferência lido", perfil: estado.perfil || "", data_hora: agora(), detalhe: cod});
      mostrarErros("#docErrosLeitura", []); alert("Código confere com a caixa.");
    } else mostrarErros("#docErrosLeitura", [`O código não confere. O desta caixa é ${cod}.`]);
  });
};

/* ================= Sprint 6 · Painel, espaço liberado e CSV ================= */
const docPainelAntigo = TELAS["#/painel"];
TELAS["#/painel"] = async ()=>{
  let html = await docPainelAntigo();
  const [cs, ps, log] = await Promise.all([db.list("caixas"), db.list("prontuarios"), db.list("log")]);
  const conferidas = cs.filter(c=>c.status === "conferida"), pendentes = cs.filter(c=>c.status !== "conferida");
  const prontConferidos = ps.filter(p=>p.conferido).length;
  // tempo médio de conferência: entre o cadastro e o lacre
  const tempos = conferidas.filter(c=>c.lacrada_em && c.criado_em).map(c=>Math.max(0, Math.round((new Date(c.lacrada_em) - new Date(c.criado_em)) / 3600000)));
  const tempoMedio = tempos.length ? Math.round(tempos.reduce((a, b)=>a + b, 0) / tempos.length * 10) / 10 : null;
  // espaço liberado (premissa: 0,03 m³ por prontuário digitalizado e conferido)
  const espaco = Math.round(prontConferidos * 0.03 * 100) / 100;
  const porPeriodo = Object.entries(cs.reduce((a, c)=>{ const k = (c.data || "").slice(0, 7) || "—"; a[k] = (a[k] || 0) + Number(c.qtd || 0); return a; }, {})).sort((a, b)=>b[0].localeCompare(a[0]));
  return html + `<div class="card" id="docGestor"><h2 style="margin-top:0">Painel do gestor documental (Sprint 6)</h2>
      <div class="grade">
        <div class="card kpi"><div class="v" data-doc-ind="conferidas">${conferidas.length}</div><div class="r">caixas conferidas</div></div>
        <div class="card kpi"><div class="v" data-doc-ind="pendentes">${pendentes.length}</div><div class="r">caixas pendentes</div></div>
        <div class="card kpi"><div class="v" data-doc-ind="espaco">${espaco} m³</div><div class="r">espaço liberado</div></div>
        <div class="card kpi"><div class="v" data-doc-ind="tempo">${tempoMedio === null ? "—" : tempoMedio + " h"}</div><div class="r">tempo médio de conferência</div></div></div>
      <div class="card tabela-wrap"><h2 style="margin-top:0">Prontuários por período</h2><table id="tabelaPeriodo"><tr><th>Mês da caixa</th><th class="num">Prontuários</th></tr>
        ${porPeriodo.map(([m, n])=>`<tr><td>${esc(m)}</td><td class="num">${n}</td></tr>`).join("")}</table></div>
      <div class="linha-botoes nao-imprimir"><button class="prim" id="btnDocCsv">${icone("download")} Exportar CSV</button>
        <button id="btnDocEtiquetas">${icone("imprimir")} Imprimir etiquetas das caixas pendentes</button>
        <button onclick="window.print()">${icone("imprimir")} Imprimir em A4</button></div></div>`;
};
TELAS_DEPOIS["#/painel"] = ()=>{
  $("#btnDocCsv")?.addEventListener("click", async ()=>{
    const cs = await db.list("caixas"), ps = await db.list("prontuarios");
    const linhas = [["caixa", "setor", "data", "qtd", "situacao", "lacrada_por", "lacrada_em", "conferidos"]].concat(
      cs.map(c=>[c.id_caixa, c.setor_origem, c.data, c.qtd, c.status, c.lacrada_por || "", c.lacrada_em || "",
        ps.filter(p=>p.caixa_id === c.id_caixa && p.conferido).length]));
    const csv = "﻿" + linhas.map(l=>l.map(x=>/[;"\n]/.test(String(x)) ? `"${String(x).replace(/"/g, '""')}"` : String(x)).join(";")).join("\r\n");
    baixar(`caixas-${hojeISO()}.csv`, csv, "text/csv;charset=utf-8");
    await registrar("relatório exportado", {detalhe: `${cs.length} caixas`});
  });
  $("#btnDocEtiquetas")?.addEventListener("click", async ()=>{
    const cs = (await db.list("caixas")).filter(c=>c.status !== "conferida");
    const ps = await db.list("prontuarios");
    const html = cs.map(c=>{ const cod = docCodigoConferencia(c, ps.filter(p=>p.caixa_id === c.id_caixa));
      return `<div class="documento-a4" style="padding:18px;margin:0 0 8px"><b>Caixa ${esc(c.id_caixa)}</b> · ${esc(c.setor_origem)} · ${c.qtd} prontuários<br>${docBarrasSVG(cod)}<div class="mono">${esc(cod)}</div></div>`; }).join("");
    const w = window.open("", "_blank");
    if (!w) return alert("Permita a janela para imprimir as etiquetas.");
    w.document.write(`<!doctype html><html lang="pt-BR"><head><meta charset="utf-8"><title>Etiquetas</title>
      <style>body{font-family:system-ui,sans-serif;margin:10px}@media print{@page{size:A4;margin:8mm}}</style></head><body>${html}</body></html>`);
    w.document.close(); w.focus(); w.print();
    await registrar("etiquetas impressas em lote", {detalhe: `${cs.length} caixas`});
  });
};

/* ================= Passo a passo do que depende de fora ================= */
const AJUDA_TECNICA = [
  {titulo: "1. QR Code na etiqueta", resumo: "O app gera o código de conferência e o código de barras Code 39 (que qualquer leitor lê). O QR Code precisa de biblioteca embutida e ficou como a implementar.",
   passos: [
     "Baixe o <code>qrcode.min.js</code> (davidshimjs ou similar, licença MIT) e salve em <code>Apps/documentapolitec/vendor/</code>.",
     "Registre a versão e o SHA-256 em <code>vendor/VERSOES.md</code>.",
     "Acrescente <code>\"qrcode.min.js\"</code> em <code>libs</code> no <code>app.json</code>.",
     "No bloco da etiqueta em <code>src/sprint4.js</code>, troque o <code>docBarrasSVG(cod)</code> por um <code>QRCode</code> gerado com o mesmo código de conferência.",
     "Rode <code>python Apps/_base/construir.py documentapolitec</code> e confira que o QR abre no leitor.",
   ], arquivos: ["app.json", "vendor/", "src/sprint4.js"]},
  {titulo: "2. Ler o QR na conferência", resumo: "Hoje a leitura é digitada. Com a biblioteca, dá para ler pela câmera.",
   passos: [
     "Acrescente um <code>&lt;input type=\"file\" accept=\"image/*\" capture=\"environment\"&gt;</code> no bloco de leitura.",
     "Decodifique a imagem com a biblioteca de QR e compare com <code>docCodigoConferencia</code>.",
     "A leitura por câmera contínua precisa de <code>getUserMedia</code> e só funciona em HTTPS.",
   ], arquivos: ["src/sprint4.js"]},
  {titulo: "3. Índice autorizado de nomes", resumo: "A busca por nome depende de a DMIT liberar o índice (número e nome). O app guarda só o hash.",
   passos: [
     "Peça à DMIT a relação autorizada em CSV, com número do prontuário, nome e caixa.",
     "Carregue em <code>#/busca-nome</code>, com o perfil gestor.",
     "Confira a trilha de consultas em <code>#/busca-nome</code> e o registro no <code>log</code>.",
     "Se a DMIT exigir base legal escrita, registre no <code>Apps/PREMISSAS.md</code>.",
   ], arquivos: ["src/sprint4.js"]},
];
