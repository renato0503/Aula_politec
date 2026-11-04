/* Não Conformidades · código do app (o construir.py junta com a base comum) */
"use strict";
TELAS["#/painel"] = async ()=> `<h1>Painel</h1><p class="sub">Os indicadores chegam no Sprint 5. Resumo da base:</p>
  ${await resumoBase(["rncs", "etapas", "setores"])}
  <p class="sub">Para testar, carregue os dados fictícios em <a href="#/config">Configuração</a>.</p>`;
teste("RN07: exemplo sem nome de servidor", ()=> (dadosEmbutidos("seed")?.rncs || []).every(r=>!("nome" in r) && !("servidor" in r)));
teste("RN01: números DIRETORIA/ANO-SEQ únicos", ()=>{ const n = (dadosEmbutidos("seed")?.rncs || []).map(r=>r.numero); return n.length === 20 && new Set(n).size === 20 && n.every(x=>/^[A-Z]+\/\d{4}-\d{3}$/.test(x)); });

/* ================= Sprint 2 · Importar a planilha do Forms ================= */
const CAMPOS_RNC = {
  aberta_em: ["carimbo de data/hora", "data/hora", "data de abertura"],
  setor_relator: ["setor relator", "relator", "gerência/coordenadoria", "gerencia/coordenadoria"],
  setor_notificado: ["setor notificado", "notificado", "pessoas ou setores envolvidos"],
  categoria: ["categoria relacionada à não conformidade", "categoria relacionada", "categoria", "tipo de nao conformidade"],
  descricao: ["descrição detalhada do ocorrido", "descricao detalhada", "descricao da ocorrencia", "descricao"],
  gravidade: ["criticidade", "gravidade"],
  numero: ["id ocorrência", "id ocorrencia", "numero", "n da rnc", "rnc"],
  data_ocorrido: ["data do ocorrido"],
  local: ["localização exata", "localizacao exata"],
  processo: ["processo de trabalho onde"],
  onde: ["onde está o problema", "onde esta o problema"],
  requisito: ["qual requisito, procedimento ou condição", "qual requisito"],
  requisito_detalhe: ["se aplicável, informe qual é o requisito", "informe qual é o requisito"],
  envolvidos: ["pessoas ou setores envolvidos"],
  frequencia: ["qual a frequência", "frequencia"],
  anexos: ["anexos"],
  consequencias: ["consequências da ocorrência", "consequencias da ocorrencia"],
  medidas: ["medida que poderia prevenir"],
  status_trello: ["status trello"],
  doc_id: ["merged doc id"],
  doc_url: ["merged doc url", "link to merged doc"],
  doc_merge_status: ["document merge status"],
  cargo: ["cargo"]
};
const ROTULOS_RNC = {aberta_em: "Data de abertura", setor_relator: "Setor relator", setor_notificado: "Setor notificado", categoria: "Categoria",
  descricao: "Descrição", gravidade: "Gravidade (criticidade)", numero: "Número (ID ocorrência)", data_ocorrido: "Data do ocorrido",
  local: "Local", processo: "Processo de trabalho", onde: "Onde está o problema", requisito: "Requisito não atendido",
  requisito_detalhe: "Requisito ou documento", envolvidos: "Pessoas ou setores envolvidos", frequencia: "Frequência", anexos: "Anexos",
  consequencias: "Consequências", medidas: "Medidas preventivas", status_trello: "Status no Trello", doc_id: "ID do documento",
  doc_url: "Link do documento", doc_merge_status: "Status do documento", cargo: "Cargo do relator"};
const OPCIONAIS_RNC = ["gravidade", "numero", "data_ocorrido", "local", "processo", "onde", "requisito", "requisito_detalhe",
  "envolvidos", "frequencia", "anexos", "consequencias", "medidas", "status_trello", "doc_id", "doc_url", "doc_merge_status", "cargo"];
const EXTRAS_RNC = ["data_ocorrido", "local", "processo", "onde", "requisito", "requisito_detalhe", "envolvidos", "frequencia",
  "anexos", "consequencias", "medidas", "status_trello", "doc_id", "doc_url", "doc_merge_status", "cargo"];
const RE_PESSOAL = /\b(nome|servidor|matricula|cpf|e-?mail|telefone)\b/;  // RN07: colunas descartadas
const RE_NUMERO = /^[A-Z]+\/\d{4}-\d{3}$/;
const somarDiasRnc = (iso, n)=> new Date(Date.UTC(...iso.slice(0, 10).split("-").map((x, i)=>i === 1 ? x - 1 : +x)) + n * 86400000).toISOString().slice(0, 10);
function somarDiasUteisRnc(iso, n){
  const d = new Date(iso.slice(0, 10) + "T12:00:00Z");
  let add = 0;
  while (add < n){ d.setUTCDate(d.getUTCDate() + 1); const w = d.getUTCDay(); if (w !== 0 && w !== 6) add++; }
  return d.toISOString().slice(0, 10);
}
const CATEGORIAS_RNC = [
  {sigla: "ADM", nome: "Administração", descricao: "Procedimentos administrativos, como elaboração e tramitação de documentos."},
  {sigla: "AMB", nome: "Ambiente e Segurança", descricao: "Procedimentos relacionados ao ambiente e à segurança do trabalho."},
  {sigla: "PES", nome: "Pessoal", descricao: "Procedimentos de gestão de pessoas e de qualidade de vida no trabalho.", aliases: ["pessoas"]},
  {sigla: "REA", nome: "Reagentes", descricao: "Preparo, armazenamento, utilização e descarte de reagentes."},
  {sigla: "EQP", nome: "Equipamentos", descricao: "Operação e manutenção de equipamentos."},
  {sigla: "MPA", nome: "Métodos de Procedimento e Análise", descricao: "Métodos de procedimento e análise.", aliases: ["metodos de processamento e analise", "amostras"]}
];
function categoriaOficial(txt){
  const n = normalizar(txt);
  if (!n) return null;
  return CATEGORIAS_RNC.find(c=>[c.nome, c.sigla, ...(c.aliases || [])].some(a=>n === normalizar(a) || n.startsWith(normalizar(a)))) || null;
}
teste("Categorias oficiais da RNC", ()=> categoriaOficial("Administração")?.sigla === "ADM" && categoriaOficial("Pessoas")?.sigla === "PES"
  && categoriaOficial("Métodos de Processamento e Análise")?.sigla === "MPA" && categoriaOficial("Outra") === null);
teste("RN03: complemento em 5 dias úteis pula o fim de semana", ()=> somarDiasUteisRnc("2026-10-02", 5) === "2026-10-09" && somarDiasUteisRnc("2026-10-05", 5) === "2026-10-12");
/* ---------- setores da planilha oficial ----------
   A planilha traz o setor por extenso e escrito de vários jeitos ("GML de Rondonópolis",
   "GERÊNCIA DE MEDICINA LEGAL DE RONDONÓPOLIS"...), às vezes com nome de pessoa junto.
   O catálogo junta as grafias numa sigla só; a lista é premissa (Apps/PREMISSAS.md, seção 18). */
const SETORES_POLITEC = [
  {sigla: "CPBM", nome: "Coordenadoria de Perícias em Biologia Molecular", diretoria: "DLF", re: /biologia molecular|\bcpbm\b/},
  {sigla: "GPTF", nome: "Gerência de Perícias em Toxicologia Forense", diretoria: "DLF", re: /toxicologia/},
  {sigla: "GPQF", nome: "Gerência de Perícias em Química Forense", diretoria: "DLF", re: /quimica forense/},
  {sigla: "GPEN", nome: "Gerência de Perícias em Entorpecentes", diretoria: "DLF", re: /entorpecentes/},
  {sigla: "GNEC", nome: "Gerência de Necropsia de Cuiabá (DMML)", diretoria: "DMML", re: /necrop/},
  {sigla: "GPVV", nome: "Gerência de Perícias em Vítimas de Violência Sexual e de Gênero", diretoria: "DMML", re: /violencia sexual|vitimas de violencia/},
  {sigla: "GPVI", nome: "Gerência de Perícia em Vivos (DMML)", diretoria: "DMML", re: /pericias? em vivos/},
  {sigla: "GMLROO", nome: "Gerência de Medicina Legal de Rondonópolis", diretoria: "Regionais", re: /(medicina legal|\bgml\b).*rondonopolis|rondonopolis.*(medicina legal|\bgml\b)/},
  {sigla: "GMLAGB", nome: "Medicina Legal da POLITEC de Água Boa", diretoria: "Regionais", re: /agua boa/},
  {sigla: "GRCONF", nome: "Gerência Regional da POLITEC de Confresa", diretoria: "Regionais", re: /confresa/},
  {sigla: "GRNMT", nome: "Gerência Regional de Nova Mutum", diretoria: "Regionais", re: /nova mutum/}
];
const SETOR_A_DEFINIR = {sigla: "ADEF", nome: "Setor a definir na validação", diretoria: "CQUAL"};
const RE_UNIDADE = /\b(gerencia|coordenadoria|coordenacao|diretoria|laboratorio|nucleo|setor|secao|divisao|superintendencia|medicina legal|gml|iml|dmml|regional|almoxarifado|custodia|recepcao)\b/;
// separa as partes do texto e devolve só as que são unidade; o resto (nome de pessoa, cargo) fica de fora (RN07)
function partesDeUnidade(txt){
  return String(txt || "").split(/\n|;|\s+-\s+|,/).map(x=>x.trim()).filter(x=>RE_UNIDADE.test(normalizar(x)));
}
// "GERÊNCIA DE BALÍSTICA" -> "Gerência de Balística" (mantém os acentos)
const titulo = s => String(s || "").trim().replace(/\s+/g, " ").toLocaleLowerCase("pt-BR")
  .replace(/(^|[\s(])(\p{L})/gu, (m, a, b)=>a + b.toLocaleUpperCase("pt-BR")).replace(/ (De|Da|Do|Das|Dos|E|Em)(?= )/g, x=>x.toLowerCase());
function siglaGerada(nome, ocupadas){
  const base = normalizar(nome).split(/[^a-z]+/).filter(w=>w.length > 2 && !["das", "dos", "politec"].includes(w)).map(w=>w[0]).join("").toUpperCase().slice(0, 6) || "SET";
  let s = base, n = 2; while (ocupadas.has(s)) s = base + n++;
  return s;
}
// texto da planilha -> {setor (do cadastro, do catálogo, novo ou a definir), envolvidos sem nome de pessoa}
function resolverSetor(txt, setores){
  const n = normalizar(txt);
  if (!n) return {setor: null};
  const cad = setores.find(s=>normalizar(s.sigla) === n || normalizar(s.nome) === n);
  if (cad) return {setor: cad};
  const cat = SETORES_POLITEC.find(s=>s.re.test(n));
  if (cat) return {setor: {sigla: cat.sigla, nome: cat.nome, diretoria: cat.diretoria}, novo: !setores.some(s=>s.sigla === cat.sigla)};
  const partes = partesDeUnidade(txt);
  if (!partes.length) return {setor: SETOR_A_DEFINIR, novo: !setores.some(s=>s.sigla === SETOR_A_DEFINIR.sigla), semUnidade: true};
  const nome = titulo(partes[0]);
  const igual = setores.find(s=>normalizar(s.nome) === normalizar(nome));
  if (igual) return {setor: igual};
  return {setor: {sigla: siglaGerada(nome, new Set(setores.map(s=>s.sigla))), nome, diretoria: ""}, novo: true};
}
// "Pessoas ou setores envolvidos": guarda só as unidades; nome de pessoa não entra no app (RN07)
function envolvidosSemNome(txt){
  const t = String(txt || "").trim(); if (!t) return "";
  const cat = SETORES_POLITEC.filter(s=>s.re.test(normalizar(t))).map(s=>s.nome);
  const unidades = cat.length ? cat : partesDeUnidade(t).map(titulo);
  return unidades.length ? unidades.join("; ") : "(texto omitido: pode conter nome de pessoa, RN07)";
}
teste("Setor: grafias diferentes viram a mesma sigla", ()=> ["GML de Rondonópolis ", "GERÊNCIA DE MEDICINA LEGAL DE RONDONÓPOLIS", "Gerência de medicina legal de Rondonópolis "].every(t=>resolverSetor(t, []).setor.sigla === "GMLROO")
  && resolverSetor("Gerência de necropsia (DMML - Cuiabá) ", []).setor.sigla === "GNEC" && resolverSetor("GERÊNCIA DE NECROPSIA DE CUIABA", []).setor.sigla === "GNEC");
teste("RN07: nome de pessoa sai do setor e dos envolvidos", ()=>{
  const t = "MARIA FICTÍCIA DE SOUZA - PERITA OFICIAL MÉDICA LEGISTA\nGERÊNCIA DE NECRÓPSIA DE CUIABÁ";
  return resolverSetor(t, []).setor.sigla === "GNEC" && !/maria/i.test(envolvidosSemNome(t)) && !/neimar/i.test(envolvidosSemNome("Gerência Regional de Nova Mutum-Neimar de Souza"))
    && resolverSetor("Fulana e ciclano ", []).setor.sigla === "ADEF" && !/fulana/i.test(envolvidosSemNome("Fulana e ciclano"));
});
teste("Setor fora do catálogo vira setor novo, sem o nome da pessoa", ()=>{
  const r = resolverSetor("João da Silva - Gerência de Balística Forense", []);
  return r.novo && r.setor.nome === "Gerência de Balística Forense" && r.setor.sigla === "GBF";
});

let planilhaRnc = null;  // {nome, linhas, cabecalho, mapa}

function colunasDescartadas(cab){ return cab.map((c, i)=>({c, i})).filter(x=>RE_PESSOAL.test(normalizar(x.c)) && !/setor/.test(normalizar(x.c))); }
teste("RN07: coluna 'Nome do servidor' é descartada", ()=> colunasDescartadas(["Setor relator", "Nome do servidor", "Matrícula"]).length === 2);
teste("RN07: 'Setor relator' não é descartada", ()=> colunasDescartadas(["Setor relator", "Setor notificado"]).length === 0);

const URL_PLANILHA = "https://docs.google.com/spreadsheets/d/10-Oqfv6x9GY4VDz3ZfVKxmipz0ev0fyyNzThi_A4DSI/edit?usp=drivesdk";
const idPlanilha = url => {
  const m = String(url || "").match(/\/spreadsheets\/d\/([\w-]+)/);
  return m ? m[1] : (/^[\w-]{20,}$/.test(String(url || "").trim()) ? String(url).trim() : "");
};
const urlCsvPlanilha = id => `https://docs.google.com/spreadsheets/d/${id}/gviz/tq?tqx=out:csv`;
teste("Google: extrai o id de um link de planilha", ()=> idPlanilha("https://docs.google.com/spreadsheets/d/10-Oqfv6x9GY4VDz3ZfVKxmipz0ev0fyyNzThi_A4DSI/edit?usp=drivesdk") === "10-Oqfv6x9GY4VDz3ZfVKxmipz0ev0fyyNzThi_A4DSI" && idPlanilha("https://example.com") === "");

function dataPlanilha(txt){
  const s = String(txt || "").trim(); if (!s) return null;
  const m = s.match(/^(\d{1,2})\/(\d{1,2})\/(\d{4})(?:[ ,]+(\d{1,2}):(\d{2})(?::(\d{2}))?)?/);
  if (!m) return null;
  let a = +m[1], b = +m[2];
  if (b > 12 && a <= 12) [a, b] = [b, a];
  return `${m[3]}-${String(b).padStart(2, "0")}-${String(a).padStart(2, "0")}${m[4] ? "T" + m[4].padStart(2, "0") + ":" + m[5] + ":" + (m[6] || "00") : ""}`;
}
function xmlTextoRnc(s){ return String(s || "").replace(/<[^>]+>/g, "").replace(/&lt;/g, "<").replace(/&gt;/g, ">").replace(/&quot;/g, '"').replace(/&apos;/g, "'").replace(/&amp;/g, "&"); }
const colunaNum = letras => [...letras].reduce((n, c)=>n * 26 + (c.charCodeAt(0) - 64), 0) - 1;
const serialDia = (n, comHora)=>{
  const d = new Date(Date.UTC(1899, 11, 30) + Math.round(n * 86400000));
  return d.toISOString().slice(0, comHora ? 19 : 10);
};
// lê o .xlsx oficial sem biblioteca de planilha: PizZip abre o zip e aqui só os XML da primeira aba são lidos
function lerXlsx(buf){
  const zip = new PizZip(buf), shared = [];
  const ss = zip.file("xl/sharedStrings.xml");
  if (ss) for (const m of ss.asText().matchAll(/<si>([\s\S]*?)<\/si>/g)) shared.push(xmlTextoRnc(m[1]));
  const abas = Object.keys(zip.files).filter(n=>/^xl\/worksheets\/sheet\d+\.xml$/.test(n));
  if (!abas.length) throw new Error("o arquivo não tem aba de planilha");
  let melhor = "", maior = -1;
  for (const nome of abas){ const x = zip.file(nome).asText(), n = (x.match(/<row/g) || []).length; if (n > maior){ maior = n; melhor = x; } }
  const tabela = [];
  for (const rm of melhor.matchAll(/<row[^>]*>([\s\S]*?)<\/row>/g)){
    const linha = [];
    for (const cm of rm[1].matchAll(/<c\b([^>]*?)(?:\/>|>([\s\S]*?)<\/c>)/g)){
      const attrs = cm[1], dentro = cm[2] || "", ref = (attrs.match(/\br="([A-Z]+)\d+"/) || [])[1];
      const i = ref ? colunaNum(ref) : linha.length;
      const tipo = (attrs.match(/\bt="([^"]+)"/) || [])[1];
      const v = (dentro.match(/<v>([\s\S]*?)<\/v>/) || [])[1];
      let valor = "";
      if (tipo === "s") valor = shared[Number(v)] ?? "";
      else if (tipo === "inlineStr") { const is = dentro.match(/<is>([\s\S]*?)<\/is>/); valor = is ? xmlTextoRnc(is[1]) : ""; }
      else if (tipo === "str") valor = xmlTextoRnc(v || "");
      else if (tipo === "b") valor = v === "1" ? "sim" : "não";
      else if (v !== undefined) { const n = Number(v); valor = Number.isFinite(n) ? n : xmlTextoRnc(v); }
      linha[i] = valor;
    }
    tabela.push(linha);
  }
  const largura = Math.max(...tabela.map(l=>l.length));
  const linhas = tabela.map(l=>Array.from({length: largura}, (_, i)=>l[i] ?? ""));
  const cab = linhas[0] || [];
  const colData = cab.map(h=>/data|carimbo|timestamp/i.test(normalizar(h)));
  for (const l of linhas.slice(1)) for (let i = 0; i < l.length; i++) if (colData[i] && typeof l[i] === "number") l[i] = serialDia(l[i], /carimbo|timestamp/i.test(cab[i] || ""));
  return linhas;
}
teste("Data da planilha aceita DD/MM e MM/DD", ()=> dataPlanilha("30/09/2026") === "2026-09-30" && dataPlanilha("9/30/2026 8:17:44") === "2026-09-30T08:17:44");

TELAS["#/importar"] = async ()=>{
  const diretoria = (await db.meta("diretoria")) || "DLF";
  const link = (await db.meta("rnc_planilha_url")) || URL_PLANILHA;
  return `<h1>Importar a planilha do Forms</h1><p class="sub">Escolha o <b>.xlsx</b> oficial ou o CSV exportado. O app lê o cabeçalho, traduz as colunas para os campos do sistema e descarta nome e e-mail (RN07).</p>
    <div class="card"><div class="campos">${campo("rncDiretoria", "Diretoria (para numerar)", {valor: diretoria, ajuda: "Usada quando a planilha não traz o número da RNC."})}</div>
      <div class="linha-botoes"><label class="botao">Escolher .xlsx ou .csv<input type="file" id="arqRnc" accept=".csv,.xlsx,text/csv,application/vnd.openxmlformats-officedocument.spreadsheetml.sheet" hidden></label></div>
      <div id="mapaRnc"></div><div id="errosRnc"></div><div id="relRnc"></div></div>
    <div class="card" id="rncGoogle"><h2 style="margin-top:0">Conectar ao Google Planilhas</h2>
      <p class="sub">Cole o link da planilha. A leitura usa a exportação CSV pública: a planilha precisa estar compartilhada como <b>qualquer pessoa com o link pode ver</b> (ou publicada na web). O app não guarda credencial e só busca quando você clica.</p>
      <div class="campos">${campo("rncPlanilha", "Link da planilha", {valor: link, ajuda: "Ex.: https://docs.google.com/spreadsheets/d/.../edit"})}</div>
      <div class="linha-botoes"><button class="prim" type="button" id="btnRncGoogle">Sincronizar agora</button>
        <a class="botao" id="linkRncGoogle" href="${esc(link)}" target="_blank" rel="noopener">Abrir a planilha</a></div>
      <div id="rncGoogleStatus"></div></div>`;
};
function desenharMapaRnc(){
  const P = planilhaRnc, opts = [["-1", "(não tem)"], ...P.cabecalho.map((c, i)=>[String(i), c || `coluna ${i + 1}`])];
  const desc = colunasDescartadas(P.cabecalho);
  const sel = k => campo("rmap-" + k, ROTULOS_RNC[k] + (OPCIONAIS_RNC.includes(k) ? "" : " *"), {tipo: "select", opcoes: opts, valor: String(P.mapa[k] ?? -1)});
  const obrig = Object.keys(CAMPOS_RNC).filter(k=>!OPCIONAIS_RNC.includes(k));
  const opc = Object.keys(CAMPOS_RNC).filter(k=>OPCIONAIS_RNC.includes(k));
  $("#mapaRnc").innerHTML = `<p class="sub"><b>${esc(P.nome)}</b> · ${P.linhas.length - 1} linhas${P.url ? " · lida do Google Planilhas" : ""}</p>
    <div class="campos">${obrig.map(sel).join("")}</div>
    <details class="rnc-opcionais"><summary>Campos adicionais da planilha oficial (${opc.length})</summary><div class="campos">${opc.map(sel).join("")}</div></details>
    ${desc.length ? `<p><span class="selo alerta">descartadas (RN07)</span> ${desc.map(d=>esc(d.c)).join(", ")}: dado pessoal não entra no app.</p>` : ""}
    <div class="linha-botoes"><button class="prim" id="btnImportarRnc">Importar</button></div>`;
  Object.keys(CAMPOS_RNC).forEach(k=>$("#rmap-" + k).addEventListener("change", e=>{ P.mapa[k] = Number(e.target.value); }));
  $("#btnImportarRnc").addEventListener("click", importarRnc);
}
async function prepararPlanilha(nome, linhas, url = ""){
  const cabecalho = (linhas[0] || []).map(x=>String(x ?? "").trim());
  if (!cabecalho.some(Boolean)) throw new Error("o cabeçalho está vazio");
  const salvo = await db.meta("modelo:forms"), sug = sugerirColunas(cabecalho, CAMPOS_RNC), mapa = {};
  const desc = new Set(colunasDescartadas(cabecalho).map(d=>d.i));
  for (const k of Object.keys(CAMPOS_RNC)){
    const i = salvo?.[k] ? cabecalho.findIndex(c=>normalizar(c) === normalizar(salvo[k])) : -1;
    mapa[k] = i >= 0 ? i : (desc.has(sug[k]) ? -1 : sug[k]);
  }
  planilhaRnc = {nome, linhas, cabecalho, mapa, url};
  desenharMapaRnc(); $("#relRnc").innerHTML = ""; $("#errosRnc").innerHTML = "";
}
async function sincronizarGoogle(){
  const url = valorDe("rncPlanilha"), id = idPlanilha(url);
  const status = $("#rncGoogleStatus");
  if (!id) return status.innerHTML = '<div class="aviso erro">Cole o link da planilha do Google.</div>';
  await db.meta("rnc_planilha_url", url);
  status.innerHTML = '<div class="aviso info">Buscando a planilha…</div>';
  try {
    const r = await fetch(urlCsvPlanilha(id), {cache: "no-store"});
    if (!r.ok) throw new Error(`HTTP ${r.status}`);
    const txt = await r.text();
    if (!txt.trim() || /^\s*</.test(txt)) throw new Error("o link não devolveu CSV (a planilha está privada)");
    const linhas = lerCSV(txt);
    if (linhas.length < 2) throw new Error("a planilha está vazia");
    await prepararPlanilha("Google Planilhas", linhas, url);
    status.innerHTML = `<div class="aviso ok"><b>${linhas.length - 1} linha(s) lidas.</b> Confira a tradução das colunas e clique em Importar.</div>`;
  } catch(e){
    status.innerHTML = `<div class="aviso erro"><b>Não consegui ler a planilha.</b> ${esc(e.message)}. Compartilhe como "qualquer pessoa com o link" ou baixe o .xlsx e use o seletor acima.</div>`;
  }
}
TELAS_DEPOIS["#/importar"] = ()=>{
  $("#arqRnc").addEventListener("change", async e=>{
    const f = e.target.files[0]; if (!f) return;
    try {
      const linhas = /\.xlsx$/i.test(f.name) ? lerXlsx(await lerArrayBuffer(f)) : lerCSV(await lerArquivoTexto(f));
      await prepararPlanilha(f.name, linhas);
    } catch(err){ mostrarErros("#errosRnc", ["Não consegui ler o arquivo: " + err.message]); }
  });
  $("#btnRncGoogle").addEventListener("click", sincronizarGoogle);
  $("#rncPlanilha").addEventListener("input", e=>{ $("#linkRncGoogle").href = e.target.value; });
};

async function importarRnc(){
  const P = planilhaRnc, diretoria = valorDe("rncDiretoria").toUpperCase() || "DLF";
  const falta = Object.keys(CAMPOS_RNC).filter(k=>!OPCIONAIS_RNC.includes(k) && !(P.mapa[k] >= 0));
  if (!mostrarErros("#errosRnc", falta.length ? [`Associe as colunas: ${falta.map(k=>ROTULOS_RNC[k]).join(", ")}.`] : [])) return;
  const desc = new Set(colunasDescartadas(P.cabecalho).map(d=>d.i));
  if (Object.values(P.mapa).some(i=>desc.has(i))) return mostrarErros("#errosRnc", ["Uma coluna de dado pessoal foi associada a um campo. Escolha outra coluna (RN07)."]);
  await db.meta("diretoria", diretoria);
  const nomes = {}; Object.entries(P.mapa).forEach(([k, i])=>{ if (i >= 0) nomes[k] = P.cabecalho[i]; }); await db.meta("modelo:forms", nomes);
  const setores = await db.list("setores");
  // setor da planilha -> sigla do cadastro; o que não está cadastrado entra no cadastro (catálogo ou setor novo)
  const novosSetores = new Set(), semUnidade = [];
  const siglaDe = async (txt, linha, papel)=>{
    const r = resolverSetor(txt, setores);
    if (r.novo){ await db.put("setores", r.setor); setores.push(r.setor); novosSetores.add(`${r.setor.sigla} · ${r.setor.nome}`); }
    if (r.semUnidade) semUnidade.push({linha, motivo: `setor ${papel} sem unidade identificável: ficou como "${SETOR_A_DEFINIR.nome}"`});
    return r.setor.sigla;
  };
  const existentes = await db.list("rncs"), chaves = new Set(existentes.map(r=>r.chave_importacao).filter(Boolean)), numeros = new Set(existentes.map(r=>r.numero));
  const porNumero = new Map(existentes.map(r=>[r.numero, r])), porChave = new Map(existentes.filter(r=>r.chave_importacao).map(r=>[r.chave_importacao, r]));
  const rel = {novas: 0, existentes: 0, recusadas: [], alertas: []};
  const col = (l, k)=> P.mapa[k] >= 0 ? String(l[P.mapa[k]] ?? "").trim() : "";
  for (const [n, l] of P.linhas.slice(1).entries()){
    if (!l.some(x=>String(x ?? "").trim())) continue;
    const linha = n + 2, aberta = dataDeTexto(col(l, "aberta_em")) || dataPlanilha(col(l, "aberta_em"));
    if (!aberta) { rel.recusadas.push({linha, motivo: "data de abertura ilegível"}); continue; }
    const relT = col(l, "setor_relator"), notT = col(l, "setor_notificado") || relT;
    if (!relT || !notT) { rel.recusadas.push({linha, motivo: "setor relator ou notificado vazio"}); continue; }
    if (!col(l, "descricao")) { rel.recusadas.push({linha, motivo: "descrição vazia"}); continue; }
    const chave = fnvRnc([aberta, normalizar(relT), normalizar(col(l, "descricao"))].join("|"));
    // o número da planilha (ID ocorrência) é a fonte de verdade: só é gerado quando a célula está vazia
    let numero = numeroDaPlanilha(col(l, "numero"));
    if (numero && !RE_NUMERO.test(numero)) rel.alertas.push({linha, motivo: `número "${numero}" fora do padrão DIRETORIA/ANO-SEQ; mantido como está na planilha`});
    const siglaRel = await siglaDe(relT, linha, "relator"), siglaNot = await siglaDe(notT, linha, "notificado");
    const envolvidos = envolvidosSemNome(col(l, "envolvidos"));
    const mesma = porChave.get(chave);
    if (mesma){
      // já importada: atualiza só os setores e os envolvidos (as etapas da CQUAL ficam como estão)
      const atual = await db.get("rncs", mesma.numero);
      if (atual && (atual.setor_relator !== siglaRel || atual.setor_notificado !== siglaNot || atual.envolvidos !== envolvidos))
        await db.put("rncs", {...atual, setor_relator: siglaRel, setor_notificado: siglaNot, envolvidos});
      // a linha já entrou antes com outro número (gerado pelo app): passa a usar o da planilha
      if (numero && mesma.numero !== numero && !porNumero.get(numero)?.chave_importacao){
        if (porNumero.has(numero)) await removerRnc(numero);
        await renumerarRnc(mesma.numero, numero);
        rel.alertas.push({linha, motivo: `RNC ${mesma.numero} renumerada para ${numero}, como está na planilha`});
        numeros.delete(mesma.numero); numeros.add(numero); porNumero.delete(mesma.numero); porNumero.set(numero, {...mesma, numero});
      }
      rel.existentes++; continue;
    }
    if (numero && porNumero.has(numero)){
      if (porNumero.get(numero).chave_importacao) { rel.existentes++; continue; }
      // o número está ocupado por um registro fictício (não veio de planilha): a planilha real ocupa o lugar
      await removerRnc(numero);
      rel.alertas.push({linha, motivo: `registro fictício ${numero} substituído pela linha da planilha`});
    }
    if (!numero){
      const ano = aberta.slice(0, 4); let seq = 1;
      while (numeros.has(`${diretoria}/${ano}-${String(seq).padStart(3, "0")}`)) seq++;
      numero = `${diretoria}/${ano}-${String(seq).padStart(3, "0")}`;
    }
    const extras = Object.fromEntries(EXTRAS_RNC.map(k=>[k, col(l, k)]));
    extras.envolvidos = envolvidos;
    if (extras.data_ocorrido) extras.data_ocorrido = dataDeTexto(extras.data_ocorrido) || dataPlanilha(extras.data_ocorrido) || extras.data_ocorrido;
    await db.put("rncs", {numero, aberta_em: aberta, setor_relator: siglaRel, setor_notificado: siglaNot,
      categoria: col(l, "categoria"), categoria_sigla: categoriaOficial(col(l, "categoria"))?.sigla || "",
      gravidade: col(l, "gravidade") || "não informada", descricao: col(l, "descricao"),
      ...extras, planilha: {nome: P.nome, url: P.url || ""},
      etapa: "validação", situacao: "aberta", chave_importacao: chave, registrado_por: estado.perfil || "importação", registrado_em: agora(), origem: {arquivo: P.nome, linha, url: P.url || ""}});
    await db.put("etapas", {id: `${numero}#0`, rnc: numero, etapa: "validação", inicio: aberta.slice(0, 10), fim: null, prazo: somarDiasRnc(aberta, 5)});
    numeros.add(numero); chaves.add(chave); rel.novas++;
    porNumero.set(numero, {numero, chave_importacao: chave}); porChave.set(chave, {numero, chave_importacao: chave});
  }
  rel.alertas.push(...semUnidade);
  if (novosSetores.size) rel.alertas.push({linha: "—", motivo: `setores cadastrados a partir da planilha: ${[...novosSetores].join("; ")}`});
  await registrar("planilha importada", {detalhe: `${P.nome}: ${rel.novas} novas, ${rel.existentes} já existentes, ${rel.recusadas.length} recusadas`});
  const lista = [...rel.recusadas.map(x=>({...x, t: "recusada"})), ...rel.alertas.map(x=>({...x, t: "alerta"}))];
  $("#relRnc").innerHTML = `<h2>Resultado</h2><p><span class="selo ok" id="qtdNovas">${rel.novas} novas</span>
    <span class="selo info" id="qtdExistentes">${rel.existentes} já existentes</span> <span class="selo erro">${rel.recusadas.length} recusadas</span>
    <span class="selo alerta">${rel.alertas.length} alertas</span></p>
    ${lista.length ? `<div class="tabela-wrap"><table><tr><th>Linha</th><th>Tipo</th><th>Motivo</th></tr>${lista.map(x=>`<tr><td class="num">${x.linha}</td><td>${x.t}</td><td>${esc(x.motivo)}</td></tr>`).join("")}</table></div>` : ""}`;
}
// "dlf / 2026-008 " -> "DLF/2026-008": tira espaços e põe em maiúsculas, sem trocar o número
const numeroDaPlanilha = txt => String(txt ?? "").toUpperCase().replace(/\s+/g, "");
teste("Número da planilha é mantido (só tira espaços)", ()=> numeroDaPlanilha(" dlf / 2026-008 ") === "DLF/2026-008" && numeroDaPlanilha("CPBM/2026-10") === "CPBM/2026-10" && numeroDaPlanilha("") === "");
async function removerRnc(numero){
  await db.del("rncs", numero);
  for (const loja of ["etapas", "planos", "avaliacoes"]) for (const x of (await db.list(loja)).filter(x=>x.rnc === numero)) await db.del(loja, x.id);
}
async function renumerarRnc(antigo, novo){
  const r = await db.get("rncs", antigo); if (!r) return;
  await db.put("rncs", {...r, numero: novo, numero_anterior: antigo}); await db.del("rncs", antigo);
  for (const loja of ["etapas", "planos", "avaliacoes"]) for (const x of (await db.list(loja)).filter(x=>x.rnc === antigo)){
    await db.del(loja, x.id); await db.put(loja, {...x, id: String(x.id).replace(antigo, novo), rnc: novo});
  }
}
function fnvRnc(txt){ let h = 0x811c9dc5; for (const b of new TextEncoder().encode(txt)){ h ^= b; h = Math.imul(h, 0x01000193) >>> 0; } return h.toString(16); }
