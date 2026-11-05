/* ================= Sprints 4 a 11 · conferência, requisição em PDF, textos, quesitos, Word, revisão e histórico =================
   A requisição é lida página a página: camada de texto quando existe e OCR embutido (src/ocr.js) nas páginas escaneadas. */
"use strict";

const CATEGORIAS_TEXTO = [["historico", "Histórico"], ["descricao_objetos", "Descrição dos objetos"], ["sem_sim", "Aparelho sem SIM"],
  ["exames", "Exames"], ["anexos", "Anexos e mídias"], ["consideracoes", "Considerações finais"]];
const CAMPOS_REQUISICAO = [["numero_protocolo", "Protocolo"], ["numero_oficio", "Ofício"], ["numero_processo", "Processo"],
  ["autoridade_solicitante", "Autoridade requisitante"], ["data_solicitacao", "Data da solicitação"]];
// campos do modelo de requisição da Polícia Civil; aparecem na conferência, mas não geram alerta quando faltam
const CAMPOS_REQUISICAO_EXTRA = [["numero_requisicao", "Requisição de perícia nº"], ["natureza_exame", "Natureza do exame"],
  ["procedimento", "Procedimento policial"], ["boletim_ocorrencia", "Boletim de ocorrência"], ["enquadramento", "Enquadramento"],
  ["destinacao_laudo", "Destinação do laudo"], ["data_fato", "Data/hora do fato"], ["local_fato", "Local do fato"]];
const TODOS_CAMPOS_REQUISICAO = [...CAMPOS_REQUISICAO, ...CAMPOS_REQUISICAO_EXTRA];
const semCaso = titulo=> `<h1>${titulo}</h1><div class="card vazio">Abra um caso em <a href="#/inicio">Início</a>.</div>`;

// a biblioteca começa com os textos do exemplo quando está vazia
async function textosDaBiblioteca(){
  let ts = await db.list("textos");
  if (!ts.length){ for (const t of dadosEmbutidos("seed")?.textos || []) await db.put("textos", t); ts = await db.list("textos"); }
  return ts.filter(t=> t.ativo !== false);
}
async function dadosDoCaso(caso){
  const id = caso.id_caso;
  const [ap, hs, sims, qs] = await Promise.all([db.porIndice("aparelhos", "id_caso", id), db.porIndice("hashes", "id_caso", id),
    db.porIndice("sims", "id_caso", id), db.porIndice("quesitos", "id_caso", id)]);
  return {ap: ap[0] || null, hs: hs[0] || null, sims: sims.sort((a, b)=> String(a.identificador_objeto).localeCompare(String(b.identificador_objeto))),
    qs: qs.sort((a, b)=> a.numero - b.numero)};
}
const val = c=> c && c.valor !== undefined && c.valor !== null ? String(c.valor) : "";

/* ---------- RN11: bloqueios e alertas da conferência automática ---------- */
function conferir(caso, d){
  const bloqueios = [], alertas = [];
  if (!d.ap || !val(d.ap.imei_1)) bloqueios.push("IMEI 1 ausente.");
  else if (!imeiValido(val(d.ap.imei_1))) bloqueios.push("IMEI 1 com dígito verificador inválido.");
  if (d.ap && val(d.ap.imei_2) && !imeiValido(val(d.ap.imei_2))) alertas.push("IMEI 2 com dígito verificador inválido.");
  if (!d.hs || !val(d.hs.valor_hash)) bloqueios.push("Hash ausente.");
  else if (!sha256Valido(val(d.hs.valor_hash))) bloqueios.push("Hash fora do formato SHA-256 (64 caracteres hexadecimais).");
  for (const s of d.sims){
    if (!val(s.iccid)) alertas.push(`SIM ${s.identificador_objeto}: ICCID ausente.`);
    else if (!iccidValido(val(s.iccid))) alertas.push(`SIM ${s.identificador_objeto}: ICCID inválido.`);
    if (s.objeto_no_html && normalizar(s.objeto_no_html).replace(/\s/g, "") !== normalizar(s.identificador_objeto || "").replace(/\s/g, ""))
      alertas.push(`SIM ${s.identificador_objeto}: o HTML diz objeto ${s.objeto_no_html} (RN07).`);
  }
  const req = caso.requisicao || {};
  for (const [k, r] of CAMPOS_REQUISICAO) if (!req[k]) (k === "numero_protocolo" ? bloqueios : alertas).push(`Requisição: ${r} não informado.`);
  if (!caso.conferido_em) bloqueios.push("A conferência dos dados não foi confirmada (RN04).");
  for (const q of d.qs){
    if (!String(q.resposta || "").trim()) bloqueios.push(`Quesito ${q.numero} sem resposta (RN10).`);
    else if (!q.aprovada) bloqueios.push(`Quesito ${q.numero}: resposta não aprovada pelo perito (RN10).`);
  }
  const l = caso.laudo || {};
  if (!l.numero_laudo) bloqueios.push("Número do laudo não informado.");
  if (!l.nome_perito) bloqueios.push("Nome do perito não informado.");
  return {bloqueios, alertas};
}
teste("RN11: caso vazio tem bloqueios", ()=> conferir({}, {ap:null, hs:null, sims:[], qs:[]}).bloqueios.length >= 3);
teste("RN10: quesito sem resposta bloqueia", ()=> conferir({}, {ap:null, hs:null, sims:[], qs:[{numero:1, resposta:""}]}).bloqueios.some(b=> b.includes("Quesito 1")));
teste("RN10: caso sem quesito não gera alerta de quesito", ()=> !conferir({}, {ap:null, hs:null, sims:[], qs:[]}).alertas.some(a=> /quesito/i.test(a)));

/* ---------- Sprint 5 e 6 · conferência campo a campo (RN04) e requisição em PDF ---------- */
// selo de cada campo: extraído do arquivo, corrigido pelo perito, digitado (sem arquivo) e confirmado
function seloCampo(c, conferido){
  if (!c || !val(c)) return '<span class="selo alerta">ausente</span>';
  const tipo = c.corrigido_de !== undefined ? ["alerta", "corrigido"] : c.origem === "perito" ? ["info", "digitado"] : ["ok", "extraído"];
  return `<span class="selo ${tipo[0]}">${tipo[1]}</span>${conferido ? ' <span class="selo ok">confirmado</span>' : ""}`;
}
// validação em tempo real: devolve a mensagem ou ""
const VALIDA_CAMPO = {imei: v=> !v ? "" : imeiValido(v) ? "" : "IMEI precisa de 15 dígitos com o dígito verificador certo (Luhn).",
  iccid: v=> !v ? "" : iccidValido(v) ? "" : "ICCID começa com 89, tem 19 ou 20 dígitos e o último confere pelo Luhn.",
  hash: v=> !v ? "" : sha256Valido(v) ? "" : "SHA-256 tem 64 caracteres de 0 a 9 e de a a f.",
  obrigatorio: v=> v ? "" : "Campo obrigatório."};
teste("validação: IMEI certo não gera mensagem", ()=> VALIDA_CAMPO.imei("358735742761447") === "" && VALIDA_CAMPO.imei("358735742761448") !== "");

/* requisição em PDF: camada de texto pelo pdf.js (o worker embutido roda na própria página) */
async function textoDoPdf(file){
  if (typeof pdfjsLib === "undefined") throw new Error("pdf.js não embutido");
  const pdf = await pdfjsLib.getDocument({data: new Uint8Array(await lerArrayBuffer(file)), isEvalSupported: false}).promise;
  const paginas = [];
  for (let i = 1; i <= pdf.numPages; i++){
    const c = await (await pdf.getPage(i)).getTextContent();
    paginas.push(c.items.map(it=> it.str + (it.hasEOL ? "\n" : "")).join(""));
  }
  return paginas.join("\n");
}
/* Campos da requisição. Os rótulos são achados sem diferença de maiúsculas, minúsculas e acentos
   ("Natureza do Exame", "NATUREZA DO EXAME" e "natureza do exame" são o mesmo rótulo).
   Atende dois modelos: o "Protocolo: / Ofício nº / QUESITOS" e a requisição de perícia da Polícia Civil
   (Natureza do Exame, Item(ns) a ser(em) periciado(s), Quesitos Específicos, Procedimento, BO...). */
const ehLinhaDeRotulo = l=> /^[^:\d]{2,40}:/.test(l) && !/^\s*\d+\s*[).\-–]/.test(l);
// valor do rótulo: o que vem depois dos dois-pontos; com multilinha, segue nas linhas seguintes até o próximo rótulo
function campoPorRotulo(linhas, rotulos, {multilinha = false, max = 4} = {}){
  const alvos = rotulos.map(normalizar);
  for (let i = 0; i < linhas.length; i++){
    const n = normalizar(linhas[i]), alvo = alvos.find(a=> n.startsWith(a) && /^\s*(\([^)]*\))?\s*:/.test(n.slice(a.length)));
    if (!alvo) continue;
    let valor = linhas[i].slice(linhas[i].indexOf(":") + 1).trim();
    if (multilinha || !valor){
      for (let k = i + 1; k < linhas.length && k <= i + max; k++){
        const l = linhas[k].trim();
        if (!l || ehLinhaDeRotulo(l) || /^[\p{L} ]+\/[A-Z]{2},\s*\d{1,2}\s+de\s/u.test(l)) break;
        valor += (valor ? " " : "") + l;
        if (!multilinha) break;
      }
    }
    return valor.replace(/\s+/g, " ").trim();
  }
  return "";
}
const MESES = ["janeiro", "fevereiro", "marco", "abril", "maio", "junho", "julho", "agosto", "setembro", "outubro", "novembro", "dezembro"];
// "Cuiabá/MT, 31 de julho de 2025." -> 31/07/2025
function dataPorExtenso(linhas){
  for (const l of linhas){
    const m = normalizar(l).match(/^[a-z .'-]+\/[a-z]{2},?\s*(\d{1,2})\s+de\s+([a-z]+)\s+de\s+(\d{4})/);
    if (m && MESES.includes(m[2])) return `${m[1].padStart(2, "0")}/${String(MESES.indexOf(m[2]) + 1).padStart(2, "0")}/${m[3]}`;
  }
  return "";
}
// itens a periciar: cada "01(um) unidade(s) ..." vira um item com lacre, identificador e código de apreensão
function itensDaRequisicao(linhas){
  const ini = linhas.findIndex(l=> /^ite(m|ns)\b.*periciad/.test(normalizar(l)));
  if (ini < 0) return [];
  const bloco = [];
  for (let k = ini + 1; k < linhas.length; k++){
    const n = normalizar(linhas[k]);
    if (/^(local|quesitos|informacoes do procedimento)\b/.test(n)) break;
    bloco.push(linhas[k].trim());
  }
  return bloco.join(" ").split(/\s*(?:[*•·]\s*)?(?:\b[a-z][.)]\s*)?(?:[O0o]{1,2}1?\s*\(um\)\s*)?unidade\(s\)\s*/i).map(s=> s.trim()).filter(s=> s.length > 8).map(s=>{
    const pega = re=> (s.match(re) || [])[1] || "";
    s = s.replace(/(\d)[lI|](\d)/g, "$1$2");   // OCR: "A1l4g" é "A14g"
    return {descricao: s.split(/\s+-\s+Obs/i)[0].replace(/\(Encaminhad[oa] para Per[íi]cia\)/i, "").replace(/[\s,;.]+$/, "").trim(),
      lacre: pega(/Lacre\s*:?\s*([\w-]+)/i), identificador: pega(/Identificador\s*:?\s*([\w/.-]+)/i),
      imei: pega(/Imei\s*\d*\s*:?\s*(\d{15})/i), codigo_apreensao: pega(/C[óo]digo de Apreens[ãa]o\s*:?\s*(\w+)/i)};
  });
}
function quesitosDaRequisicao(linhas){
  const ini = linhas.findIndex(l=> /^quesitos\b/.test(normalizar(l)));
  if (ini < 0) return [];
  const resto = linhas[ini].includes(":") ? linhas[ini].slice(linhas[ini].indexOf(":") + 1).trim() : "";
  const bloco = resto ? [resto] : [];
  for (let k = ini + 1; k < linhas.length; k++){
    const l = linhas[k].trim(), n = normalizar(l);
    if (/^(informacoes do procedimento|documento|atenciosamente)\b/.test(n) || ehLinhaDeRotulo(l) || /^[\p{L} ]+\/[A-Z]{2},\s*\d{1,2}\s+de\s/u.test(l)) break;
    if (l) bloco.push(l);
  }
  const quesitos = [];
  for (const l of bloco){
    if (/^\s*\d+\s*[).\-–]/.test(l)) quesitos.push(l.replace(/^\s*\d+\s*[).\-–:]\s*/, "").trim());
    else if (quesitos.length) quesitos[quesitos.length - 1] += " " + l;   // quesito quebrado em duas linhas
    else quesitos.push(l);
  }
  // sem numeração: o bloco inteiro é um quesito só
  return quesitos.length > 1 && !bloco.some(l=> /^\s*\d+\s*[).\-–]/.test(l)) ? [quesitos.join(" ")] : quesitos;
}
function extrairRequisicao(txt, nomeArquivo = ""){
  const texto = String(txt), linhas = texto.split(/\r?\n/).map(l=> l.trim()).filter(Boolean);
  const pega = re=> (texto.match(re) || [])[1]?.trim() || "";
  const numReq = (normalizar(texto).match(/requisicao de pericia\s*n\S{0,2}\s*([\d.]{6,})/) || [])[1]?.replace(/\.$/, "") || "";
  // autoridade: a linha acima de "Delegado(a) de Polícia"
  const iDel = linhas.findIndex(l=> /^delegad[oa]\b/.test(normalizar(l)));
  const autoridade = campoPorRotulo(linhas, ["autoridade requisitante", "autoridade solicitante", "autoridade"])
    || (iDel > 0 ? `${linhas[iDel - 1]}, ${linhas[iDel]}` : "");
  const protocoloArquivo = (String(nomeArquivo).match(/-(\d{4,6}\.\d{4})(?!\d)/) || [])[1] || "";
  const r = {
    numero_protocolo: pega(/Protocolo\s*:?\s*([\d./-]+)/i) || protocoloArquivo || numReq,
    numero_oficio: pega(/Of[ií]cio\s*(?:n[ºo°.]*)?\s*:?\s*(\d[\w/.-]*)/i),
    numero_processo: pega(/\b(\d{7}-\d{2}\.\d{4}\.\d\.\d{2}\.\d{4})\b/) || pega(/Processo\s*(?:n[ºo°.]*)?\s*:?\s*(\d[\d.-]+\d)/i),
    autoridade_solicitante: autoridade,
    data_solicitacao: pega(/Data da solicita[cç][aã]o\s*:\s*(\d{2}\/\d{2}\/\d{4})/i) || dataPorExtenso(linhas),
    numero_requisicao: numReq,
    natureza_exame: campoPorRotulo(linhas, ["natureza do exame", "natureza da pericia"]),
    procedimento: campoPorRotulo(linhas, ["procedimento", "inquerito policial"]).replace(/^[1l|]\.\s?P\./i, "I.P."),
    boletim_ocorrencia: campoPorRotulo(linhas, ["boletim de ocorrencia", "b.o."]),
    enquadramento: campoPorRotulo(linhas, ["enquadramento"], {multilinha: true}),
    destinacao_laudo: campoPorRotulo(linhas, ["destinacao do laudo"], {multilinha: true}),
    data_fato: campoPorRotulo(linhas, ["data/hora do fato", "data do fato"]),
    local_fato: campoPorRotulo(linhas, ["local do fato"], {multilinha: true}),
  };
  return {...r, quesitos: quesitosDaRequisicao(linhas), itens: itensDaRequisicao(linhas)};
}
teste("requisição (Polícia Civil): rótulos em qualquer caixa, itens, quesito sem número, autoridade e data", ()=>{
  const r = extrairRequisicao("REQUISIÇÃO DE PERÍCIA Nº 2026.10.00001\nnatureza do exame: COMPUTAÇÃO FORENSE\nITEM(NS) A SER(EM) PERICIADO(S):\n"
    + "* a. 01(um) unidade(s) Celular Fictício X1, Azul, Imei 02 351234567890126, Lacre: 00000001, Código de Apreensão 11111 (Encaminhado para Perícia) - Obs.: na sala\n"
    + "b. O1(um) unidade(s) Cartão Sd 2gb, Lacre: 00000002, Código de Apreensão 11112 - Obs.: x\nLocal:\nRua Exemplo, 1\nQUESITOS ESPECÍFICOS:\n"
    + "p/ extração de dados dos aparelhos.\nInformações do Procedimento Policial:\nProcedimento: 1.P. 100.1.2026.1\nBOLETIM DE OCORRÊNCIA: BO 2026.1\n"
    + "Enquadramento: FURTO, tipificado no Art. 155 do DECRETO LEI Nº\n2.848/1940\nData/Hora do Fato: 01/01/2026 10:00\nLocal do Fato: Rua Exemplo, 1\nBairro Centro - Cuiabá/MT\n"
    + "Cuiabá/MT, 5 de março de 2026.\nFULANO DE TAL\nDelegado(a) de Polícia\nProcesso: 0001231-56.2026.8.11.0041.", "REQUISIÇÃO 2026.10.00001-000123.2026.pdf");
  return r.numero_requisicao === "2026.10.00001" && r.numero_protocolo === "000123.2026" && r.natureza_exame === "COMPUTAÇÃO FORENSE"
    && r.itens.length === 2 && r.itens[0].lacre === "00000001" && r.itens[0].imei === "351234567890126" && r.itens[1].codigo_apreensao === "11112"
    && r.quesitos.length === 1 && r.quesitos[0] === "p/ extração de dados dos aparelhos." && r.procedimento === "I.P. 100.1.2026.1"
    && r.boletim_ocorrencia === "BO 2026.1" && r.enquadramento.endsWith("2.848/1940") && r.local_fato === "Rua Exemplo, 1 Bairro Centro - Cuiabá/MT"
    && r.data_solicitacao === "05/03/2026" && r.autoridade_solicitante === "FULANO DE TAL, Delegado(a) de Polícia" && r.numero_processo === "0001231-56.2026.8.11.0041";
});
teste("requisição: protocolo, ofício, processo, data e 2 quesitos", ()=>{
  const r = extrairRequisicao("Protocolo: 2026.0001001\nOfício nº 101/2026/DPF-CBA\nProcesso nº 0001231-56.2026.8.11.0041\nAutoridade requisitante: Delegado X\nData da solicitação: 19/10/2026\nQUESITOS\n1) Qual a marca?\n2) Havia SIM? Em caso\npositivo, qual?\nDocumento fictício.");
  return r.numero_protocolo === "2026.0001001" && r.numero_oficio === "101/2026/DPF-CBA" && r.numero_processo === "0001231-56.2026.8.11.0041"
    && r.data_solicitacao === "19/10/2026" && r.quesitos.length === 2 && r.quesitos[1] === "Havia SIM? Em caso positivo, qual?";
});
// o PDF com texto vem antes do digitalizado
const arquivoRequisicao = caso=> (caso.inventario?.itens.find(i=> i.chave === "requisicao")?.arquivos || [])
  .filter(c=> arquivosDaSessao.get(c)).sort((a, b)=> /digitaliz/i.test(a) - /digitaliz/i.test(b))[0];

const agDadosAntes = TELAS["#/dados"];
TELAS["#/dados"] = async (p)=>{
  const html = await agDadosAntes(p);
  const caso = await casoAtual();
  if (!caso?.inventario) return html;
  const d = await dadosDoCaso(caso), req = caso.requisicao || {}, conf = !!caso.conferido_em;
  const linhaCampo = (id, rotulo, c, valida)=> `<tr><th><label for="${id}">${esc(rotulo)}</label></th>
    <td><input id="${id}" value="${esc(val(c))}" class="mono" ${valida ? `data-valida="${valida}" aria-describedby="${id}-msg"` : ""}><small class="erro-campo" id="${id}-msg" aria-live="polite"></small></td>
    <td>${seloCampo(c, conf)}<br><small class="sub">${c ? esc(c.origem || "") + (c.linha ? ", linha " + c.linha : "") + (c.corrigido_de !== undefined ? ` · era ${esc(c.corrigido_de || "vazio")}` : "") : ""}</small></td></tr>`;
  const ap = d.ap || {}, pdf = arquivoRequisicao(caso);
  const doPdf = String(caso.requisicao_origem || "").includes("PDF");
  return html.replace("A conferência campo a campo chega no Sprint 5.", "Confira cada valor com a origem ao lado e corrija o que precisar (RN04).") + `
    <div class="card"><h2 style="margin-top:0">Requisição</h2>
      ${pdf ? `<div class="linha-botoes" style="margin-top:0"><button id="btnLerPdf" class="prim">${caso.requisicao_paginas ? "Ler a requisição de novo" : "Ler a requisição (todas as páginas, com OCR)"}</button>
        <button id="btnVerPdf">Ver o PDF ao lado</button></div><div id="avisoPdf" aria-live="polite"></div>
        <p class="sub">Páginas escaneadas são lidas pelo OCR embutido, sem internet (cerca de 5 a 15 s por página). ${caso.requisicao_paginas ? `Última leitura: ${caso.requisicao_paginas.length} página(s), ${caso.requisicao_paginas.filter(x=> x.origem === "ocr").length} pelo OCR.` : ""}</p>`
        : '<p class="sub">A requisição em PDF não está na sessão (selecione a pasta de novo para ler o PDF). Os campos podem ser digitados.</p>'}</div>
    <div class="ag-conf">
    <form class="card tabela-wrap" id="formConferencia"><h2 style="margin-top:0">Conferência</h2>
      <p class="sub">${conf ? `<span class="selo ok">conferido em ${dataBR(caso.conferido_em)}</span>` : '<span class="selo alerta">não conferido</span>'}
        O botão confirma todos os campos de uma vez e só libera com IMEI 1 e hash válidos.</p>
      <table><tr><th>Campo</th><th>Valor</th><th>Situação e origem</th></tr>
        ${TODOS_CAMPOS_REQUISICAO.map(([k, r])=> `<tr><th><label for="req_${k}">${esc(r)}</label></th><td><input id="req_${k}" value="${esc(req[k] || (k === "numero_protocolo" ? caso.numero_protocolo || "" : ""))}"
          ${k === "numero_protocolo" ? `data-valida="obrigatorio" aria-describedby="req_${k}-msg"` : ""}><small class="erro-campo" id="req_${k}-msg" aria-live="polite"></small></td>
          <td>${req[k] ? `<span class="selo ${doPdf ? "ok" : "info"}">${doPdf ? "extraído" : "digitado"}</span>${conf ? ' <span class="selo ok">confirmado</span>' : ""}` : '<span class="selo alerta">vazio</span>'}
          <br><small class="sub">${esc(caso.requisicao_origem || "digitado pelo perito")}</small></td></tr>`).join("")}
        ${Object.keys(ROTULOS_APARELHO).map(k=> linhaCampo("ap_" + k, k.replace("_", " "), ap[k], k.startsWith("imei") ? "imei" : "")).join("")}
        ${linhaCampo("hs_valor", "hash", d.hs?.valor_hash, "hash")}${linhaCampo("hs_arquivo", "arquivo do hash", d.hs?.hash_arquivo)}
        ${d.sims.map(s=> linhaCampo("sim_iccid_" + s.identificador_objeto, `ICCID ${s.identificador_objeto}`, s.iccid, "iccid")
          + linhaCampo("sim_op_" + s.identificador_objeto, `operadora ${s.identificador_objeto}`, s.operadora)
          + `<tr><td></td><td colspan="2"><button type="button" data-remover-sim="${esc(s.id_sim)}">Remover o SIM ${esc(s.identificador_objeto)}</button></td></tr>`).join("")}
      </table>
      ${d.sims.length ? "" : `<p class="sub"><label style="display:inline-flex;gap:6px"><input type="checkbox" id="semSimConfirmado" style="width:auto" ${caso.sem_sim_confirmado ? "checked" : ""}> confirmo que o aparelho não tem cartão SIM (RN06)</label></p>`}
      <div class="linha-botoes"><button type="button" id="btnAdicionarSim">Adicionar SIM à mão</button></div>
      <div class="card"><h2 style="margin-top:0">Outras informações do perito</h2>
        <p class="sub">Campo livre; entra no laudo como complemento das considerações finais.</p>
        <textarea id="outrasInfo" rows="3">${esc(caso.outras_informacoes || "")}</textarea></div>
      <div id="errosConferencia"></div>
      <div class="linha-botoes"><button class="prim" type="submit" id="btnConfirmarTodos">Confirmar todos os campos</button><a class="botao" href="#/textos">Próximo: textos</a></div></form>
    <div id="painelPdf"></div></div>
    ${(caso.itens_requisicao || []).length ? `<div class="card tabela-wrap"><h2 style="margin-top:0">Itens a periciar (${caso.itens_requisicao.length}), lidos da requisição</h2>
      <table><tr><th>#</th><th>Descrição</th><th>Lacre</th><th>Identificador / IMEI</th><th>Apreensão</th></tr>
      ${caso.itens_requisicao.map((it, i)=> `<tr><td>${i + 1}</td><td>${esc(it.descricao)}</td><td class="mono">${esc(it.lacre || "—")}</td>
        <td class="mono">${esc([it.identificador, it.imei].filter(Boolean).join(" · ") || "—")}</td><td class="mono">${esc(it.codigo_apreensao || "—")}</td></tr>`).join("")}</table></div>` : ""}
    ${(caso.requisicao_paginas || []).length ? `<div class="card"><h2 style="margin-top:0">Texto lido da requisição (${caso.requisicao_paginas.length} páginas)</h2>
      <p class="sub">Confira aqui o que o OCR leu em cada página.</p>
      ${caso.requisicao_paginas.map(pg=> `<details><summary>Página ${pg.n} · ${pg.origem === "ocr" ? `OCR, confiança ${pg.confianca}%` : "texto do PDF"} · ${pg.texto.length} caracteres</summary>
        <pre class="mono" style="white-space:pre-wrap;max-height:320px;overflow:auto">${esc(pg.texto)}</pre></details>`).join("")}</div>` : ""}
    <div class="card" id="cardFoto"><h2 style="margin-top:0">Foto do aparelho</h2>
      <p class="sub">A sugestão de cor é assistida; o perito confirma no campo “cor”. A foto fica neste navegador e não vai para o Word.</p>
      <div id="prevFoto" class="sub">Sem foto.</div>
      <label class="botao">Tirar ou escolher foto<input type="file" accept="image/*" id="fotoAparelho" hidden></label>
      <p class="sub" id="sugestaoCor"></p></div>`;
};
function corPredominante(r, g, b){
  const max = Math.max(r, g, b), min = Math.min(r, g, b), l = (max + min) / 510;
  const s = max === min ? 0 : (max - min) / (255 * (1 - Math.abs(2 * l - 1)) || 1);
  let h = 0;
  if (max !== min) {
    const d = max - min;
    if (max === r) h = ((g - b) / d) % 6;
    else if (max === g) h = (b - r) / d + 2;
    else h = (r - g) / d + 4;
    h *= 60;
    if (h < 0) h += 360;
  }
  const hex = "#" + [r, g, b].map(x=>Math.round(x).toString(16).padStart(2, "0")).join("");
  if (l < .18) return {nome: "preto", hex};
  if (l > .92 && s < .12) return {nome: "branco", hex};
  if (s < .12) return {nome: "cinza", hex};
  if (s < .22 && l > .6) return {nome: "prata", hex};
  if (h >= 20 && h < 45 && l > .65) return {nome: "dourado", hex};
  if (h < 15 || h >= 345) return {nome: "vermelho", hex};
  if (h < 45) return {nome: "laranja", hex};
  if (h < 70) return {nome: "amarelo", hex};
  if (h < 165) return {nome: "verde", hex};
  if (h < 255) return {nome: "azul", hex};
  if (h < 300) return {nome: "roxo", hex};
  return {nome: "rosa", hex};
}
teste("AG: sugestão de cor do aparelho", ()=> corPredominante(10, 10, 10).nome === "preto"
  && corPredominante(245, 245, 245).nome === "branco" && corPredominante(210, 25, 25).nome === "vermelho"
  && corPredominante(30, 90, 200).nome === "azul");
async function sugerirCorDeImagem(blob){
  const bmp = await createImageBitmap(blob);
  const cv = document.createElement("canvas"); cv.width = 32; cv.height = 32;
  const g = cv.getContext("2d"); g.drawImage(bmp, 0, 0, 32, 32);
  const px = g.getImageData(0, 0, 32, 32).data;
  let r = 0, gc = 0, b = 0, n = 0;
  for (let i = 0; i < px.length; i += 4){ if (px[i + 3] < 128) continue; r += px[i]; gc += px[i + 1]; b += px[i + 2]; n++; }
  return corPredominante(r / Math.max(1, n), gc / Math.max(1, n), b / Math.max(1, n));
}
const agDadosDepois = TELAS_DEPOIS["#/dados"];
TELAS_DEPOIS["#/dados"] = async (p)=>{
  await agDadosDepois?.(p);
  const form = $("#formConferencia"); if (!form) return;
  // validação em tempo real e o botão "Confirmar todos" preso aos identificadores essenciais
  const essenciais = ()=> !!valorDe("ap_imei_1") && !VALIDA_CAMPO.imei(valorDe("ap_imei_1")) && !!valorDe("hs_valor") && !VALIDA_CAMPO.hash(valorDe("hs_valor"));
  const validar = el=>{ const msg = VALIDA_CAMPO[el.dataset.valida]?.(el.value.trim()) || ""; $("#" + CSS.escape(el.id) + "-msg").textContent = msg; el.setAttribute("aria-invalid", msg ? "true" : "false"); };
  const atualizar = ()=>{ $$("[data-valida]").forEach(validar); $("#btnConfirmarTodos").disabled = !essenciais(); };
  $$("[data-valida]").forEach(el=> el.addEventListener("input", atualizar)); atualizar();
  $("#btnAdicionarSim")?.addEventListener("click", async ()=>{
    const obj = (prompt("Identificador do objeto do SIM (ex.: 01-A)") || "").trim().toUpperCase();
    if (!/^\d{2}-[A-Z]$/.test(obj)) return obj && toast("Use o formato 01-A (RN07).");
    const caso = await casoAtual();
    await db.put("sims", {id_sim: `${caso.id_caso}-${obj}`, id_caso: caso.id_caso, identificador_objeto: obj, objeto_no_html: null,
      iccid: null, operadora: null, incluido_a_mao: true});
    await registrar("SIM incluído à mão", {id_caso: caso.id_caso, campo_verificado: "SIM " + obj}); navegar();
  });
  $$("[data-remover-sim]").forEach(b=> b.addEventListener("click", async ()=>{
    if (!confirm("Remover este SIM do laudo?")) return;
    const caso = await casoAtual();
    await db.del("sims", b.dataset.removerSim); await registrar("SIM removido", {id_caso: caso.id_caso, campo_verificado: b.dataset.removerSim}); navegar();
  }));
  $("#btnVerPdf")?.addEventListener("click", async ()=>{
    const caso = await casoAtual(), f = arquivosDaSessao.get(arquivoRequisicao(caso));
    $("#painelPdf").innerHTML = `<div class="card"><h2 style="margin-top:0">Requisição</h2><iframe class="ag-pdf" title="Requisição em PDF" src="${URL.createObjectURL(new Blob([f], {type: "application/pdf"}))}"></iframe></div>`;
  });
  const casoFoto = await casoAtual();
  if (casoFoto?.foto_aparelho) {
    $("#prevFoto").innerHTML = `<img src="${URL.createObjectURL(casoFoto.foto_aparelho)}" alt="Foto do aparelho" style="max-width:180px;border-radius:8px">`;
    if (casoFoto.cor_sugerida) $("#sugestaoCor").textContent = `Última sugestão: ${casoFoto.cor_sugerida}.`;
  }
  $("#fotoAparelho")?.addEventListener("change", async e=>{
    const f = e.target.files[0]; if (!f) return;
    try {
      const blob = await reduzirImagem(f, 800, .8);
      const cor = await sugerirCorDeImagem(blob);
      const caso = await casoAtual(); if (!caso) return;
      await db.put("casos", {...caso, foto_aparelho: blob, cor_sugerida: cor.nome});
      $("#prevFoto").innerHTML = `<img src="${URL.createObjectURL(blob)}" alt="Foto do aparelho" style="max-width:180px;border-radius:8px">`;
      $("#sugestaoCor").textContent = `Sugestão: ${cor.nome} (${cor.hex}). Confira no campo cor.`;
      if (!$("#ap_cor").value) $("#ap_cor").value = cor.nome;
      toast("Foto adicionada; confira a cor sugerida.");
      await registrar("foto do aparelho enviada", {id_caso: caso.id_caso, resultado: cor.nome});
    } catch(err){ toast("Não consegui ler a imagem: " + err.message); }
  });
  $("#btnLerPdf")?.addEventListener("click", async ()=>{
    const caso = await casoAtual(), caminho = arquivoRequisicao(caso), btn = $("#btnLerPdf");
    const aviso = (msg, frac)=>{ const el = $("#avisoPdf"); if (el) el.innerHTML = `<div class="card" role="status"><b>${esc(msg)}</b>${frac !== undefined ? ` <progress max="1" value="${frac}" style="width:100%"></progress>` : ""}</div>`; };
    btn.disabled = true; const t0 = Date.now();
    try {
      const lido = await lerPdfCompleto(arquivosDaSessao.get(caminho), aviso);
      if (lido.texto.replace(/\s/g, "").length < 20){
        aviso("Não foi possível ler texto do PDF, nem pelo OCR. Digite os dados com o PDF aberto ao lado.");
        return registrar("requisição sem texto", {id_caso: caso.id_caso, resultado: caminho});
      }
      const r = extrairRequisicao(lido.texto, nomeDe(caminho));
      const atual = await casoAtual();
      await db.put("casos", {...atual, requisicao: Object.fromEntries(TODOS_CAMPOS_REQUISICAO.map(([k])=> [k, r[k] || (atual.requisicao || {})[k] || ""])),
        numero_protocolo: r.numero_protocolo || atual.numero_protocolo, requisicao_origem: `requisição em PDF (${caminho})`, quesitos_requisicao: r.quesitos,
        itens_requisicao: r.itens, requisicao_paginas: lido.paginas, requisicao_lida_em: agora()});
      const nCampos = TODOS_CAMPOS_REQUISICAO.filter(([k])=> r[k]).length, nOcr = lido.paginas.filter(x=> x.origem === "ocr").length;
      await registrar("requisição lida do PDF", {id_caso: caso.id_caso, resultado: `${lido.paginas.length} páginas (${nOcr} por OCR), ${nCampos} campos, ${r.itens.length} itens, ${r.quesitos.length} quesitos, ${Math.round((Date.now() - t0) / 1000)} s`});
      toast(`Requisição lida: ${lido.paginas.length} página(s), ${nCampos} campos, ${r.itens.length} item(ns) e ${r.quesitos.length} quesito(s).`, 6000); navegar();
    } catch(e){ aviso("Não consegui ler o PDF: " + e.message); }
    finally { if (btn) btn.disabled = false; }
  });
  form.addEventListener("submit", async ev=>{
    ev.preventDefault();
    const caso = await casoAtual(), d = await dadosDoCaso(caso);
    if (!d.sims.length && !$("#semSimConfirmado")?.checked) return mostrarErros("#errosConferencia", ["Confirme que o aparelho não tem cartão SIM, ou adicione o SIM (RN06)."]);
    let correcoes = 0;
    const corrigir = (c, id, origemPadrao)=>{
      const novo = valorDe(id);
      if (val(c) === novo) return c;
      correcoes++;
      registrar("campo corrigido", {id_caso: caso.id_caso, campo_verificado: id, de: val(c), para: novo});
      if (!novo) return null;
      return c ? {...c, valor: novo, corrigido_de: val(c), valido: true} : {valor: novo, origem: origemPadrao, valido: true};
    };
    const ap = d.ap || {id_aparelho: caso.id_caso + "-A1", id_caso: caso.id_caso};
    for (const k of Object.keys(ROTULOS_APARELHO)) ap[k] = corrigir(ap[k], "ap_" + k, "perito");
    if (ap.imei_1) ap.imei_1.valido = imeiValido(val(ap.imei_1));
    if (ap.imei_2) ap.imei_2.valido = imeiValido(val(ap.imei_2));
    await db.put("aparelhos", ap);
    const hs = d.hs || {id_hash: caso.id_caso + "-H1", id_caso: caso.id_caso, algoritmo: "SHA-256"};
    hs.valor_hash = corrigir(hs.valor_hash, "hs_valor", "perito"); hs.hash_arquivo = corrigir(hs.hash_arquivo, "hs_arquivo", "perito");
    if (hs.valor_hash){ hs.valor_hash.valor = hs.valor_hash.valor.toLowerCase(); hs.valor_hash.valido = sha256Valido(hs.valor_hash.valor); }
    await db.put("hashes", hs);
    for (const s of d.sims){
      s.iccid = corrigir(s.iccid, "sim_iccid_" + s.identificador_objeto, "perito");
      if (s.iccid) s.iccid.valido = iccidValido(val(s.iccid));
      s.operadora = corrigir(s.operadora, "sim_op_" + s.identificador_objeto, "perito");
      await db.put("sims", s);
    }
    const requisicao = Object.fromEntries(TODOS_CAMPOS_REQUISICAO.map(([k])=> [k, valorDe("req_" + k)]));
    const reqCorrigidos = TODOS_CAMPOS_REQUISICAO.filter(([k])=> (caso.requisicao || {})[k] && caso.requisicao[k] !== requisicao[k]).length;
    const total = correcoes + reqCorrigidos;
    await db.put("casos", {...caso, requisicao, numero_protocolo: requisicao.numero_protocolo || caso.numero_protocolo,
      outras_informacoes: valorDe("outrasInfo"), conferido_em: agora(), sem_sim_confirmado: !d.sims.length, correcoes: (caso.correcoes || 0) + total,
      campos_conferidos: (caso.campos_conferidos || 0) + $$("#formConferencia input:not([type=checkbox])").length});
    await registrar("conferência confirmada", {id_caso: caso.id_caso, resultado: total + " correção(ões)"});
    toast(`Conferência confirmada${total ? `, com ${total} correção(ões)` : ""}.`); navegar();
  });
};

/* ---------- Sprint 7 · textos padronizados (RN08) e biblioteca ---------- */
// marcadores dentro dos textos ({marca}, {qtd_sims}...) recebem os dados confirmados
function preencherMarcadores(texto, dados){
  return String(texto || "").replace(/\{(\w+)\}/g, (m, k)=> dados[k] !== undefined && dados[k] !== null && typeof dados[k] !== "object" ? String(dados[k]) : m);
}
teste("RN08: marcador dentro do texto recebe o dado", ()=> preencherMarcadores("Aparelho {marca} com {qtd_sims} SIM", {marca: "Xiaomi", qtd_sims: 2}) === "Aparelho Xiaomi com 2 SIM");
// sugestão por condição: sem SIM, a seção "Aparelho sem SIM" entra; com SIM, sai
const secoesDoCaso = d=> CATEGORIAS_TEXTO.filter(([c])=> c !== "sem_sim" || !d.sims.length);

TELAS["#/textos"] = async ()=>{
  const caso = await casoAtual(); if (!caso) return semCaso("Textos");
  const ts = await textosDaBiblioteca(), escolhidos = caso.textos || {}, editados = caso.textos_editados || {};
  const d = await dadosDoCaso(caso), dados = await dadosDoLaudo(caso, true);
  return `<h1>Textos padronizados</h1><p class="sub">Escolha o texto de cada seção. A prévia traz os dados do caso; o texto pode ser editado para este caso sem mudar a biblioteca. A biblioteca fica em <a href="#/biblioteca">Biblioteca</a> (RN08).
    ${d.sims.length ? "" : '<br><span class="selo info">sugestão</span> O caso não tem SIM: a seção "Aparelho sem SIM" entrou na lista.'}</p>
    <form class="card" id="formTextos">
      ${secoesDoCaso(d).map(([c, r])=>{
        const op = ts.filter(t=> t.categoria === c), atual = escolhidos[c] ?? op[0]?.id_texto ?? "";
        const t = op.find(x=> x.id_texto === atual), bruto = editados[c] ?? t?.conteudo ?? "";
        return `<div class="ag-texto">${campo("tx_" + c, r, {tipo:"select", opcoes:[["", "(sem texto)"], ...op.map(x=> [x.id_texto, `${x.titulo} · v${x.versao || 1}`])], valor: atual})}
          <p class="ag-previa" id="previa_${c}">${esc(preencherMarcadores(bruto, dados)) || '<span class="sub">sem texto</span>'}</p>
          <details class="ag-editar-texto"><summary>Editar o texto desta seção</summary>
            <textarea id="edit_${c}" rows="4" placeholder="Texto que vai para o laudo; aceita os marcadores {marca}, {modelo}, {cor}...">${esc(bruto)}</textarea>
            <div class="linha-botoes"><button type="button" class="sec" data-adaptar="${c}">Adaptar ao caso</button>
              <button type="button" class="sec" data-restaurar="${c}">Usar o texto da biblioteca</button></div></details></div>`;
      }).join("")}
      <div class="linha-botoes"><button class="prim" type="submit">Salvar os textos</button><a class="botao" href="#/quesitos">Próximo: quesitos</a></div></form>`;
};
TELAS_DEPOIS["#/textos"] = async ()=>{
  const caso = await casoAtual(); if (!caso) return;
  const ts = await textosDaBiblioteca(), dados = await dadosDoLaudo(caso, true);
  const textoAtual = (c)=> ts.find(x=> x.id_texto === (valorDe("tx_" + c) || ""))?.conteudo || "";
  const atualizar = c => { const el = $("#edit_" + c), p = $("#previa_" + c); if (!el || !p) return; p.textContent = preencherMarcadores(el.value, dados); };
  $$("#formTextos select").forEach(s=> s.addEventListener("change", ()=>{
    const c = s.id.slice(3); $("#edit_" + c).value = textoAtual(c); atualizar(c);
  }));
  $$("#formTextos textarea").forEach(t=> t.addEventListener("input", ()=> atualizar(t.id.slice(5))));
  $$("[data-adaptar]").forEach(b=> b.addEventListener("click", ()=>{
    const c = b.dataset.adaptar, el = $("#edit_" + c); el.value = preencherMarcadores(el.value || textoAtual(c), dados); atualizar(c);
    toast("Texto adaptado ao caso; edite se precisar e salve.");
  }));
  $$("[data-restaurar]").forEach(b=> b.addEventListener("click", ()=>{
    const c = b.dataset.restaurar; $("#edit_" + c).value = textoAtual(c); atualizar(c); toast("Voltou ao texto da biblioteca.");
  }));
  $("#formTextos")?.addEventListener("submit", async ev=>{
    ev.preventDefault();
    const c = await casoAtual(), textos = {}, textos_editados = {};
    for (const [k] of CATEGORIAS_TEXTO){
      if (!$("#tx_" + k)) continue;
      textos[k] = valorDe("tx_" + k);
      const v = $("#edit_" + k)?.value ?? "", lib = textoAtual(k);
      if (v.trim() && v !== lib) textos_editados[k] = v;
    }
    await db.put("casos", {...c, textos, textos_editados}); await registrar("textos escolhidos", {id_caso: c.id_caso});
    toast("Textos salvos."); location.hash = "#/quesitos";
  });
};
const TIPOS_DISPOSITIVO = ["Celular", "Tablet", "Notebook", "Outros"];
TELAS["#/biblioteca"] = async ()=>{
  let ts = await textosDaBiblioteca(); ts = await db.list("textos");
  const cats = [...CATEGORIAS_TEXTO, ["resposta", "Resposta de quesito"]];
  return `<h1>Biblioteca de textos</h1><p class="sub">${ts.filter(t=> t.ativo !== false).length} textos ativos de ${ts.length}. Editar um texto cria a versão seguinte; desativar tira o texto das listas sem apagar (RN08).
    Marcadores aceitos no texto: <span class="mono">{marca} {modelo} {cor} {imei_1} {qtd_sims} {numero_protocolo} {hash_arquivo}</span>. Respostas de quesito usam o campo "palavras-chave" para a sugestão.
    A adaptação ao caso é local, por marcadores; a IA externa fica para a versão institucional.</p>
    <div class="card"><div class="linha-botoes" style="margin-top:0"><button id="btnExportarTextos">Exportar a biblioteca (textos.json)</button>
      <label class="botao">Importar textos.json<input type="file" id="arqTextos" accept=".json" hidden></label></div>
      <div class="campos">${campo("filtroTipo", "Filtrar por tipo de dispositivo", {tipo:"select", opcoes:[["", "Todos"], ...TIPOS_DISPOSITIVO.map(t=>[t, t])]})}</div></div>
    <div class="card tabela-wrap"><table id="tabelaTextos"><tr><th>Categoria</th><th>Tipo</th><th>Título</th><th>Texto</th><th>Versão</th><th>Situação</th><th></th></tr>
      ${ts.map(t=> `<tr data-tipo="${esc(t.tipo_dispositivo || "Celular")}"><td>${esc(cats.find(c=> c[0] === t.categoria)?.[1] || t.categoria)}</td><td>${esc(t.tipo_dispositivo || "Celular")}</td><td><b>${esc(t.titulo)}</b></td>
        <td>${esc(t.conteudo)}</td><td class="num">${esc(t.versao || "1")}</td><td>${t.ativo === false ? '<span class="selo alerta">inativo</span>' : '<span class="selo ok">ativo</span>'}</td>
        <td><button data-editar-texto="${esc(t.id_texto)}">Editar</button> <button data-ativar-texto="${esc(t.id_texto)}">${t.ativo === false ? "Ativar" : "Desativar"}</button></td></tr>`).join("")}</table></div>
    <form class="card" id="formTexto"><h2 style="margin-top:0" id="tituloFormTexto">Novo texto</h2><input type="hidden" id="txId">
      <div class="campos">${campo("txCategoria", "Categoria", {tipo:"select", opcoes:cats})}${campo("txTipo", "Tipo de dispositivo", {tipo:"select", opcoes:TIPOS_DISPOSITIVO})}
        ${campo("txTitulo", "Título", {obrigatorio:true})}${campo("txChaves", "Palavras-chave (respostas)", {ajuda: "Separadas por vírgula, ex.: marca, modelo, imei"})}</div>
      ${campo("txConteudo", "Texto", {tipo:"textarea", obrigatorio:true})}
      <div id="errosTexto"></div><div class="linha-botoes"><button class="prim" type="submit">Salvar o texto</button></div></form>`;
};
TELAS_DEPOIS["#/biblioteca"] = ()=>{
  $("#filtroTipo")?.addEventListener("change", e=>{
    const tipo = e.target.value;
    $$("#tabelaTextos tr[data-tipo]").forEach(tr=>{ tr.hidden = !!tipo && tr.dataset.tipo !== tipo; });
  });
  $$("[data-editar-texto]").forEach(b=> b.addEventListener("click", async ()=>{
    const t = await db.get("textos", b.dataset.editarTexto);
    $("#txId").value = t.id_texto; $("#txCategoria").value = t.categoria; $("#txTipo").value = t.tipo_dispositivo || "Celular";
    $("#txTitulo").value = t.titulo; $("#txConteudo").value = t.conteudo;
    $("#txChaves").value = (t.palavras_chave || []).join(", ");
    $("#tituloFormTexto").textContent = "Editar texto"; $("#formTexto").scrollIntoView({block:"nearest"});
  }));
  $$("[data-ativar-texto]").forEach(b=> b.addEventListener("click", async ()=>{
    const t = await db.get("textos", b.dataset.ativarTexto);
    await db.put("textos", {...t, ativo: t.ativo === false}); await registrar(t.ativo === false ? "texto ativado" : "texto desativado", {detalhe: t.id_texto}); navegar();
  }));
  $("#btnExportarTextos")?.addEventListener("click", async ()=> baixar("textos.json", JSON.stringify(await db.list("textos"), null, 2), "application/json"));
  $("#arqTextos")?.addEventListener("change", async e=>{
    const f = e.target.files[0]; if (!f) return;
    try {
      const lista = JSON.parse(await lerArquivoTexto(f)), arr = Array.isArray(lista) ? lista : lista.textos || [];
      let n = 0;
      for (const t of arr) if (t.id_texto && t.conteudo){ await db.put("textos", {ativo: true, versao: "1", ...t}); n++; }
      await registrar("biblioteca importada", {detalhe: f.name, resultado: n + " textos"}); toast(`${n} textos importados.`); navegar();
    } catch(err){ toast("Arquivo ilegível: " + err.message, 5000); }
  });
  $("#formTexto")?.addEventListener("submit", async ev=>{
    ev.preventDefault();
    const erros = [];
    if (!valorDe("txTitulo")) erros.push("Informe o título.");
    if (!valorDe("txConteudo")) erros.push("Escreva o texto.");
    if (!mostrarErros("#errosTexto", erros)) return;
    const id = valorDe("txId"), ant = id ? await db.get("textos", id) : null;
    const t = {id_texto: id || "T" + Date.now().toString(36), categoria: valorDe("txCategoria"), tipo_dispositivo: valorDe("txTipo") || "Celular",
      titulo: valorDe("txTitulo"), conteudo: valorDe("txConteudo"), versao: String(Number(ant?.versao || 0) + 1), ativo: ant ? ant.ativo !== false : true,
      palavras_chave: valorDe("txChaves").split(",").map(x=> x.trim()).filter(Boolean)};
    if (ant) t.versoes_anteriores = [...(ant.versoes_anteriores || []), {versao: ant.versao, conteudo: ant.conteudo}];
    await db.put("textos", t); await registrar(ant ? "texto alterado" : "texto criado", {detalhe: t.id_texto, versao: t.versao});
    toast("Texto salvo."); navegar();
  });
};

/* ---------- Sprint 8 · quesitos e respostas (RN09, RN10) ---------- */
// RN09: um quesito por linha, com ou sem número na frente ("1)", "1.", "1 -")
const separarQuesitos = txt=> String(txt || "").split(/\r?\n/).map(l=> l.replace(/^\s*\d+\s*[).\-–:]\s*/, "").trim()).filter(Boolean);
teste("RN09: separa e numera os quesitos colados", ()=>{ const q = separarQuesitos("1) Qual a marca?\n2. Havia SIM?\n\n3 - Houve extração?"); return q.length === 3 && q[1] === "Havia SIM?"; });
// palavras-chave das respostas do exemplo, quando o texto da biblioteca não traz as dele
const CHAVES_PADRAO = {T08: ["marca", "modelo", "imei", "aparelho examinado"], T09: ["sim", "operadora", "iccid", "chip"],
  T10: ["extrair", "extração", "dados armazenados"], T11: ["integridade", "preservad", "hash"]};
function sugerirResposta(enunciado, respostas){
  const e = normalizar(enunciado);
  let melhor = null, pontos = 0;
  for (const t of respostas){
    const chaves = (t.palavras_chave && t.palavras_chave.length ? t.palavras_chave : CHAVES_PADRAO[t.id_texto] || []).map(normalizar);
    const n = chaves.filter(k=> k && (k.length <= 3 ? new RegExp(`\\b${k}\\b`).test(e) : e.includes(k))).length;
    if (n > pontos){ melhor = t; pontos = n; }
  }
  return melhor;
}
teste("RN10: sugestão de resposta por palavra-chave", ()=> sugerirResposta("O aparelho continha cartão SIM? Qual o ICCID?", [{id_texto: "T08"}, {id_texto: "T09"}])?.id_texto === "T09");

async function gravarQuesitos(caso, lista){
  const dados = await dadosDoLaudo(caso, true), respostas = (await textosDaBiblioteca()).filter(t=> t.categoria === "resposta");
  for (const q of await db.porIndice("quesitos", "id_caso", caso.id_caso)) await db.del("quesitos", q.id_quesito);
  for (const [i, enunciado] of lista.entries()){
    const s = sugerirResposta(enunciado, respostas);
    // a resposta sugerida nasce como "sugestão, não aprovada" e só entra no laudo depois de aprovada
    await db.put("quesitos", {id_quesito: `${caso.id_caso}-Q${uuid().slice(0, 8)}`, id_caso: caso.id_caso, numero: i + 1, enunciado,
      resposta: s ? preencherMarcadores(s.conteudo, dados) : "", sugestao: !!s, aprovada: false, texto_sugerido: s?.id_texto || null});
  }
}
async function renumerar(caso, ordem){
  for (const [i, q] of ordem.entries()) await db.put("quesitos", {...q, numero: i + 1});
}
TELAS["#/quesitos"] = async ()=>{
  const caso = await casoAtual(); if (!caso) return semCaso("Quesitos");
  const {qs} = await dadosDoCaso(caso);
  const respostas = (await textosDaBiblioteca()).filter(t=> t.categoria === "resposta");
  const daReq = caso.quesitos_requisicao || [];
  return `<h1>Quesitos</h1><p class="sub">Os quesitos vêm da requisição em PDF ou são colados, um por linha (RN09). O app sugere a resposta pela biblioteca; a sugestão só entra no laudo depois de aprovada (RN10).</p>
    ${daReq.length ? `<div class="card"><p><b>${daReq.length} quesito(s)</b> lidos da requisição em PDF.</p>
      <div class="linha-botoes" style="margin-top:0"><button class="prim" id="btnQuesitosPdf">Usar os quesitos da requisição</button></div></div>` : ""}
    <div class="card">${campo("qsColar", "Colar quesitos", {tipo:"textarea", ajuda:"A numeração é refeita na ordem colada (RN09)."})}
      <div class="linha-botoes"><button ${daReq.length ? "" : 'class="prim"'} id="btnQuesitos">${qs.length ? "Substituir os quesitos" : "Cadastrar os quesitos"}</button></div></div>
    ${qs.length ? `<form class="card" id="formRespostas"><h2 style="margin-top:0">Respostas</h2>
      ${qs.map((q, i)=> `<div class="campo ag-quesito"><label for="resp_${esc(q.id_quesito)}"><b>${q.numero})</b> ${esc(q.enunciado)}
          ${q.sugestao && !q.aprovada ? '<span class="selo alerta">sugestão, não aprovada</span>' : q.aprovada ? '<span class="selo ok">aprovada</span>' : ""}</label>
        <div class="linha-botoes" style="margin:4px 0">
          <button type="button" data-mover="${esc(q.id_quesito)}" data-dir="-1" ${i ? "" : "disabled"} aria-label="Subir o quesito ${q.numero}">↑</button>
          <button type="button" data-mover="${esc(q.id_quesito)}" data-dir="1" ${i < qs.length - 1 ? "" : "disabled"} aria-label="Descer o quesito ${q.numero}">↓</button>
          <button type="button" data-excluir-quesito="${esc(q.id_quesito)}" aria-label="Excluir o quesito ${q.numero}">Excluir</button>
          <select data-resp-texto="${esc(q.id_quesito)}" aria-label="Inserir resposta padrão no quesito ${q.numero}"><option value="">Inserir resposta padrão…</option>
            ${respostas.map(t=> `<option value="${esc(t.id_texto)}">${esc(t.titulo)}</option>`).join("")}</select></div>
        <textarea id="resp_${esc(q.id_quesito)}" rows="3">${esc(q.resposta || "")}</textarea>
        <label style="display:inline-flex;gap:6px"><input type="checkbox" data-aprovar="${esc(q.id_quesito)}" style="width:auto" ${q.aprovada ? "checked" : ""}> resposta aprovada pelo perito</label></div>`).join("")}
      <div class="linha-botoes"><button type="button" id="btnNovoQuesito">Inserir quesito</button></div>
      <div class="linha-botoes"><button class="prim" type="submit">Salvar as respostas</button><a class="botao" href="#/gerar">Próximo: gerar o laudo</a></div></form>` : ""}`;
};
TELAS_DEPOIS["#/quesitos"] = async ()=>{
  $("#btnQuesitosPdf")?.addEventListener("click", async ()=>{
    const caso = await casoAtual(); await gravarQuesitos(caso, caso.quesitos_requisicao || []);
    await registrar("quesitos da requisição", {id_caso: caso.id_caso, resultado: (caso.quesitos_requisicao || []).length + " quesitos"}); navegar();
  });
  $("#btnQuesitos")?.addEventListener("click", async ()=>{
    const caso = await casoAtual(), lista = separarQuesitos(valorDe("qsColar"));
    if (!lista.length) return toast("Cole pelo menos um quesito.");
    await gravarQuesitos(caso, lista);
    await registrar("quesitos cadastrados", {id_caso: caso.id_caso, resultado: lista.length + " quesitos"});
    navegar();
  });
  const salvarTudo = async ()=>{
    const caso = await casoAtual();
    for (const q of await db.porIndice("quesitos", "id_caso", caso.id_caso)){
      const area = $("#resp_" + CSS.escape(q.id_quesito)); if (!area) continue;
      await db.put("quesitos", {...q, resposta: area.value.trim(), aprovada: $(`[data-aprovar="${CSS.escape(q.id_quesito)}"]`).checked});
    }
    return caso;
  };
  $$("[data-mover]").forEach(b=> b.addEventListener("click", async ()=>{
    const caso = await salvarTudo(), {qs} = await dadosDoCaso(caso);
    const i = qs.findIndex(q=> q.id_quesito === b.dataset.mover), j = i + Number(b.dataset.dir);
    [qs[i], qs[j]] = [qs[j], qs[i]]; await renumerar(caso, qs); navegar();
  }));
  $$("[data-excluir-quesito]").forEach(b=> b.addEventListener("click", async ()=>{
    if (!confirm("Excluir este quesito?")) return;
    const caso = await salvarTudo();
    await db.del("quesitos", b.dataset.excluirQuesito);
    await renumerar(caso, (await dadosDoCaso(caso)).qs); await registrar("quesito excluído", {id_caso: caso.id_caso}); navegar();
  }));
  $("#btnNovoQuesito")?.addEventListener("click", async ()=>{
    const enunciado = (prompt("Texto do quesito") || "").trim(); if (!enunciado) return;
    const caso = await salvarTudo(), {qs} = await dadosDoCaso(caso);
    await db.put("quesitos", {id_quesito: `${caso.id_caso}-Q${uuid().slice(0, 8)}`, id_caso: caso.id_caso, numero: qs.length + 1, enunciado, resposta: "", sugestao: false, aprovada: false});
    navegar();
  });
  const ts = await textosDaBiblioteca();
  const caso = await casoAtual(), dados = caso ? await dadosDoLaudo(caso, true) : {};
  $$("[data-resp-texto]").forEach(s=> s.addEventListener("change", ()=>{
    const t = ts.find(x=> x.id_texto === s.value); if (!t) return;
    const area = $("#resp_" + CSS.escape(s.dataset.respTexto)); area.value = (area.value ? area.value + "\n" : "") + preencherMarcadores(t.conteudo, dados); s.value = "";
  }));
  $("#formRespostas")?.addEventListener("submit", async ev=>{
    ev.preventDefault();
    const c = await salvarTudo();
    await registrar("respostas salvas", {id_caso: c.id_caso}); toast("Respostas salvas."); navegar();
  });
};

/* ---------- Sprint 4 · geração do Word (RN12, RN13) ---------- */
// rascunho = true devolve os dados mesmo sem a conferência (para as prévias)
async function dadosDoLaudo(caso, rascunho){
  const d = await dadosDoCaso(caso), ts = await textosDaBiblioteca(), req = caso.requisicao || {}, l = caso.laudo || {};
  const base = {...req, numero_protocolo: req.numero_protocolo || caso.numero_protocolo || "",
    numero_laudo: l.numero_laudo || "", nome_perito: l.nome_perito || "", data_laudo: l.data_laudo || new Date().toLocaleDateString("pt-BR"),
    marca: val(d.ap?.marca), modelo: val(d.ap?.modelo), cor: val(d.ap?.cor) || "não informada", imei_1: val(d.ap?.imei_1), imei_2: val(d.ap?.imei_2),
    qtd_sims: d.sims.length, sims: d.sims.map(s=> ({identificador_objeto: s.identificador_objeto, operadora: val(s.operadora), iccid: val(s.iccid)})),
    hash_arquivo: val(d.hs?.hash_arquivo), hash_algoritmo: d.hs?.algoritmo || "SHA-256", valor_hash: val(d.hs?.valor_hash)};
  const texto = c=> preencherMarcadores(((caso.textos_editados || {})[c] ?? ts.find(t=> t.id_texto === (caso.textos || {})[c])?.conteudo) || "", base);
  // só respostas aprovadas entram no laudo final (RN10)
  base.quesitos = d.qs.map(q=> ({numero_quesito: q.numero, enunciado: q.enunciado, resposta: q.aprovada || rascunho ? q.resposta || "" : ""}));
  for (const [c] of CATEGORIAS_TEXTO) base["texto_" + c] = texto(c);
  base.itens_requisicao = (caso.itens_requisicao || []).map((it, i)=> ({numero_item: i + 1, ...it}));
  base.qtd_itens = base.itens_requisicao.length;
  base.outras_informacoes = caso.outras_informacoes || "";
  if (base.outras_informacoes && base.texto_consideracoes)
    base.texto_consideracoes += `\n\nOutras informações: ${base.outras_informacoes}`;
  return base;
}
async function modeloAtual(){
  const m = await db.get("modelos", "atual");
  if (m?.b64) return m;
  const e = dadosEmbutidos("modelo-docx");
  return e ? {id_modelo: "embutido", nome: e.nome + " (fictício, embutido)", b64: e.b64} : null;
}
// marcadores encontrados no modelo: o texto do document.xml sem as tags
function marcadoresDoModelo(b64){
  const xml = new PizZip(atob(b64)).file("word/document.xml").asText();
  const txt = xml.replace(/<[^>]+>/g, "");
  return [...new Set([...txt.matchAll(/\{[#^/]?(\w+)\}/g)].map(m=> m[1]))].sort();
}
function gerarDocx(dados, b64){
  if (!b64 || typeof PizZip === "undefined" || typeof docxtemplater === "undefined") throw new Error("modelo ou biblioteca do Word não embutidos");
  const doc = new docxtemplater(new PizZip(atob(b64)), {paragraphLoop: true, linebreaks: true, nullGetter: ()=> ""});
  doc.render(dados);
  return doc.getZip().generate({type: "blob", mimeType: "application/vnd.openxmlformats-officedocument.wordprocessingml.document"});
}
teste("RN12: o modelo do Word preenche os marcadores", ()=>{
  const blob = gerarDocx({numero_laudo: "1/2026", sims: [], quesitos: [{numero_quesito: 1, enunciado: "a", resposta: "b"}]}, dadosEmbutidos("modelo-docx")?.b64);
  return blob.size > 10000;
});
teste("RN12: o modelo embutido tem os marcadores do laço de SIMs e de quesitos", ()=>{
  const m = marcadoresDoModelo(dadosEmbutidos("modelo-docx").b64); return m.includes("sims") && m.includes("quesitos") && m.includes("imei_1");
});
// RN13: os originais não mudam; o laudo vai para LAUDO_GERADO dentro da pasta, se o perito permitir
async function gravarNaPasta(caso, nome, blob){
  const h = caso.pasta_handle;
  if (!h || !h.requestPermission) return false;
  try {
    if (await h.requestPermission({mode: "readwrite"}) !== "granted") return false;
    const dir = await h.getDirectoryHandle("LAUDO_GERADO", {create: true});
    const w = await (await dir.getFileHandle(nome, {create: true})).createWritable();
    await w.write(blob); await w.close(); return true;
  } catch(e){ return false; }
}
TELAS["#/gerar"] = async ()=>{
  const caso = await casoAtual(); if (!caso) return semCaso("Gerar laudo");
  const {bloqueios, alertas} = conferir(caso, await dadosDoCaso(caso)), l = caso.laudo || {};
  const laudos = await db.porIndice("laudos", "id_caso", caso.id_caso);
  const modelo = await modeloAtual(), dados = await dadosDoLaudo(caso, true);
  const marc = modelo ? marcadoresDoModelo(modelo.b64) : [];
  const ITENS = new Set(["identificador_objeto", "operadora", "iccid", "numero_quesito", "enunciado", "resposta"]);
  const semDado = marc.filter(m=> !ITENS.has(m) && (dados[m] === undefined || dados[m] === "" || (Array.isArray(dados[m]) && !dados[m].length && m !== "sims")));
  return `<h1>Gerar o laudo</h1><p class="sub">O Word sai do modelo com os marcadores (RN12). Os originais da pasta não mudam: o arquivo vai para <span class="mono">LAUDO_GERADO</span>, quando o navegador permite, ou para Downloads (RN13).</p>
    <form class="card" id="formLaudo"><div class="campos">
      ${campo("lNumero", "Número do laudo", {valor: l.numero_laudo || "", obrigatorio: true})}
      ${campo("lPerito", "Nome do perito", {valor: l.nome_perito || "", obrigatorio: true})}
      ${campo("lData", "Data do laudo", {valor: l.data_laudo || new Date().toLocaleDateString("pt-BR")})}</div>
      <div class="linha-botoes"><button type="submit">Salvar</button></div></form>
    <div class="card"><h2 style="margin-top:0">Modelo</h2><p class="sub">${esc(modelo?.nome || "nenhum")} · ${marc.length} marcadores.
      ${semDado.length ? `<span class="selo alerta">${semDado.length} sem dado</span> <span class="mono">${semDado.map(esc).join(", ")}</span>` : '<span class="selo ok">todos os marcadores com dado</span>'}
      Troque o modelo em <a href="#/config">Configuração</a>.</p></div>
    <div class="card" id="resultadoConferencia"><h2 style="margin-top:0">Conferência automática (RN11)</h2>
      ${bloqueios.length ? `<div class="pendente" role="alert"><b>Bloqueia (${bloqueios.length}):</b><ul>${bloqueios.map(b=> `<li>${esc(b)}</li>`).join("")}</ul></div>` : '<p><span class="selo ok">sem bloqueios</span></p>'}
      ${alertas.length ? `<p><b>Alerta (${alertas.length})</b></p><ul>${alertas.map(a=> `<li>${esc(a)}</li>`).join("")}</ul>` : ""}
      <p class="sub"><b>Informa:</b> ${dados.qtd_sims} SIM(s), ${dados.quesitos.length} quesito(s), ${laudos.length} versão(ões) já gerada(s).</p>
      <div class="linha-botoes"><button class="prim" id="btnGerarDocx" ${bloqueios.length ? "disabled" : ""}>Gerar o .docx</button>
        <button id="btnRascunho">Gerar rascunho (com pendências)</button></div></div>
    ${laudos.length ? `<div class="card tabela-wrap"><h2 style="margin-top:0">Versões geradas</h2><table><tr><th>Versão</th><th>Quando</th><th>Arquivo</th><th>Tipo</th><th>Onde</th></tr>
      ${laudos.sort((a, b)=> (b.versao || 0) - (a.versao || 0)).map(x=> `<tr><td class="num">${x.versao || ""}</td><td>${dataBR(x.gerado_em)}</td><td class="mono">${esc(x.arquivo)}</td><td>${x.rascunho ? "rascunho" : "final"}</td><td>${x.na_pasta ? "LAUDO_GERADO" : "Downloads"}</td></tr>`).join("")}</table></div>` : ""}`;
};
TELAS_DEPOIS["#/gerar"] = async ()=>{
  $("#formLaudo")?.addEventListener("submit", async ev=>{
    ev.preventDefault();
    const caso = await casoAtual();
    await db.put("casos", {...caso, laudo: {numero_laudo: valorDe("lNumero"), nome_perito: valorDe("lPerito"), data_laudo: valorDe("lData")}});
    toast("Dados do laudo salvos."); navegar();
  });
  const gerar = async rascunho=>{
    const caso = await casoAtual();
    try {
      const blob = gerarDocx(await dadosDoLaudo(caso, rascunho), (await modeloAtual())?.b64);
      const versao = (await db.porIndice("laudos", "id_caso", caso.id_caso)).length + 1;
      const nome = `laudo_${(caso.numero_protocolo || "caso").replace(/[^\w.-]+/g, "_")}_v${versao}${rascunho ? "_rascunho" : ""}.docx`;
      const naPasta = await gravarNaPasta(caso, nome, blob);
      if (!naPasta) baixar(nome, blob, blob.type);
      await db.put("laudos", {id_laudo: uuid(), id_caso: caso.id_caso, versao, arquivo: nome, gerado_em: agora(), rascunho, na_pasta: naPasta});
      await registrar("laudo gerado", {id_caso: caso.id_caso, resultado: nome});
      toast((naPasta ? "Laudo gravado em LAUDO_GERADO: " : "Laudo baixado: ") + nome); navegar();
    } catch(e){ toast("Não consegui gerar o Word: " + e.message, 6000); }
  };
  $("#btnGerarDocx")?.addEventListener("click", ()=> gerar(false));
  $("#btnRascunho")?.addEventListener("click", ()=> gerar(true));
};

/* ---------- configuração: modelo .docx da unidade e privacidade ---------- */
async function configExtra(){
  const m = await modeloAtual();
  return `<div class="card"><h2 style="margin-top:0">Modelo do laudo</h2>
      <p class="sub">Em uso: <b>${esc(m?.nome || "nenhum")}</b>. O modelo institucional precisa ter os marcadores de <span class="mono">modelos/MARCADORES.md</span>, escritos de uma vez no Word.</p>
      <div class="linha-botoes"><label class="botao">Carregar modelo .docx ou .dotx<input type="file" id="arqModelo" accept=".docx,.dotx" hidden></label>
        ${m?.id_modelo === "atual" ? '<button id="btnModeloPadrao">Voltar ao modelo fictício</button>' : ""}</div><div id="modeloInfo"></div></div>
    <div class="card"><h2 style="margin-top:0">Privacidade</h2>
      <p><b>Finalidade:</b> montar o laudo de exame em aparelho celular a partir dos arquivos da extração. <b>Dados tratados:</b> IMEI, ICCID, operadora, hash e os dados da requisição.
        <b>Onde ficam:</b> só neste navegador; o app não acessa a rede. <b>Retenção:</b> depois de concluído o laudo, use "Limpar os dados do caso" no Histórico; as métricas ficam.
        <b>Base legal:</b> execução de competência legal da perícia oficial (art. 7º, III e art. 23 da LGPD), <i>a validar com o encarregado de dados</i>.</p></div>`;
}
async function ligarConfigExtra(){
  $("#arqModelo")?.addEventListener("change", async e=>{
    const f = e.target.files[0]; if (!f) return;
    const buf = new Uint8Array(await lerArrayBuffer(f));
    let bin = ""; for (let i = 0; i < buf.length; i += 32768) bin += String.fromCharCode(...buf.subarray(i, i + 32768));
    let b64 = btoa(bin), nome = f.name;
    try {
      if (/\.dotx$/i.test(f.name)){
        const zip = new PizZip(atob(b64)), ct = zip.file("[Content_Types].xml")?.asText() || "";
        zip.file("[Content_Types].xml", ct.replace(/application\/vnd\.openxmlformats-officedocument\.wordprocessingml\.template\.main\+xml/g,
          "application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml"));
        b64 = zip.generate({type: "base64"}); nome = f.name.replace(/\.dotx$/i, ".docx");
      }
      const marc = marcadoresDoModelo(b64);
      await db.put("modelos", {id_modelo: "atual", nome, b64, carregado_em: agora(), marcadores: marc});
      await registrar("modelo carregado", {detalhe: nome, resultado: marc.length + " marcadores"});
      if (!marc.length) toast("Modelo carregado, mas sem marcadores: o laudo sai com o texto fixo. Veja modelos/MARCADORES.md.", 7000);
      else toast(`Modelo carregado: ${marc.length} marcadores.`);
      navegar();
    } catch(err){ $("#modeloInfo").innerHTML = `<div class="card pendente">O arquivo não é um .docx/.dotx válido: ${esc(err.message)}</div>`; }
  });
  $("#btnModeloPadrao")?.addEventListener("click", async ()=>{ await db.del("modelos", "atual"); toast("Voltou ao modelo fictício."); navegar(); });
}

/* ---------- Sprint 9 · revisão final (RN14) ---------- */
TELAS["#/revisao"] = async ()=>{
  const caso = await casoAtual(); if (!caso) return semCaso("Revisão final");
  const d = await dadosDoCaso(caso), {bloqueios, alertas} = conferir(caso, d);
  const laudos = (await db.porIndice("laudos", "id_caso", caso.id_caso)).filter(x=> !x.rascunho);
  const itens = [["Pasta inventariada", !!caso.inventario], ["Dados conferidos (RN04)", !!caso.conferido_em], ["Textos escolhidos", !!caso.textos],
    ["Quesitos respondidos e aprovados (quando houver)", d.qs.length === 0 || d.qs.every(q=> q.resposta && q.aprovada)],
    ["Laudo final gerado", laudos.length > 0], ["Sem bloqueios (RN11)", !bloqueios.length]];
  const prontos = itens.every(i=> i[1]);
  return `<h1>Revisão final</h1><p class="sub">Abra o <span class="mono">.docx</span> no Word e confira o laudo. Só a marcação de revisão encerra o caso e para o cronômetro (RN14). Situação: <span class="selo info">${esc(caso.status)}</span></p>
    <div class="card"><ul class="checklist">${itens.map(([t, okI])=> `<li>${okI ? '<span class="selo ok">ok</span>' : '<span class="selo alerta">pendente</span>'} ${esc(t)}</li>`).join("")}</ul>
      ${bloqueios.length ? `<p><b>Bloqueios:</b> ${bloqueios.map(esc).join(" ")}</p>` : ""}${alertas.length ? `<p class="sub">Alertas: ${alertas.map(esc).join(" ")}</p>` : ""}</div>
    <form class="card" id="formRevisao">
      <label style="display:inline-flex;gap:6px"><input type="checkbox" id="revOk" style="width:auto" ${prontos ? "" : "disabled"}> revisei o laudo e ele está pronto para assinatura</label>
      <div class="linha-botoes"><button class="prim" type="submit" id="btnConcluir" ${prontos && caso.status !== "concluído" ? "" : "disabled"}>Concluir o caso</button>
        <a class="botao" href="#/historico">Histórico e Metas</a></div></form>`;
};
TELAS_DEPOIS["#/revisao"] = ()=>{
  $("#formRevisao")?.addEventListener("submit", async ev=>{
    ev.preventDefault();
    if (!$("#revOk").checked) return toast("Marque a revisão para concluir o caso.");
    const caso = await casoAtual();
    await db.put("casos", {...caso, status: "concluído", fim_em: agora(), revisado_em: agora()});
    await registrar("caso concluído", {id_caso: caso.id_caso, resultado: "revisado"}); toast("Caso concluído."); navegar();
  });
};

/* ---------- Sprint 11 · histórico, métricas e LGPD ---------- */
const minutosDoCaso = c=> c.inicio_em && c.fim_em ? Math.round((new Date(c.fim_em) - new Date(c.inicio_em)) / 60000) : null;
TELAS["#/historico"] = async ()=>{
  const casos = (await db.list("casos")).sort((a, b)=> String(b.criado_em).localeCompare(String(a.criado_em)));
  const laudos = await db.list("laudos");
  const concl = casos.filter(c=> minutosDoCaso(c) !== null);
  const media = concl.length ? Math.round(concl.reduce((a, c)=> a + minutosDoCaso(c), 0) / concl.length) : null;
  const corr = casos.reduce((a, c)=> a + (c.correcoes || 0), 0), conf = casos.reduce((a, c)=> a + (c.campos_conferidos || 0), 0);
  const conferidos = casos.filter(c=> c.conferido_em).length;
  return `<h1>Histórico e métricas</h1><p class="sub">Tempo de cada laudo, da pasta inventariada à revisão, e as correções feitas na conferência e no Word.</p>
    <div class="grade"><div class="card kpi"><div class="v">${casos.length}</div><div class="r">casos (${concl.length} concluídos)</div></div>
      <div class="card kpi"><div class="v">${media === null ? "—" : media + " min"}</div><div class="r">tempo médio</div></div>
      <div class="card kpi"><div class="v">${conf ? numBR(corr / conf * 100, 1) + "%" : "—"}</div><div class="r">taxa de correção dos campos</div></div>
      <div class="card kpi"><div class="v">${conferidos ? numBR(corr / conferidos, 1) : "—"}</div><div class="r">campos corrigidos por caso</div></div></div>
    <div class="card tabela-wrap"><table><tr><th>Protocolo</th><th>Situação</th><th class="num">Minutos</th><th class="num">Correções</th><th class="num">No Word</th><th class="num">Versões</th><th></th></tr>
      ${casos.map(c=> `<tr><td>${esc(c.numero_protocolo || "(sem protocolo)")}</td><td>${esc(c.status)}</td><td class="num">${minutosDoCaso(c) ?? "—"}</td>
        <td class="num">${c.correcoes || 0}</td><td class="num">${c.correcoes_word ?? "—"}</td><td class="num">${laudos.filter(l=> l.id_caso === c.id_caso).length}</td>
        <td>${c.dados_limpos_em ? '<span class="selo info">dados limpos</span>' : `<button data-abrir-caso="${esc(c.id_caso)}">Abrir</button> <button data-limpar-caso="${esc(c.id_caso)}">Limpar os dados do caso</button>`}</td></tr>`).join("") || '<tr><td colspan="7" class="vazio">Nenhum caso.</td></tr>'}</table>
      <div class="linha-botoes"><button class="prim" id="btnCsvTempos">Baixar historico.csv</button></div>
      <p class="sub">Limpar os dados apaga aparelho, SIMs, hash, quesitos e a requisição do caso e mantém só as métricas (LGPD).</p></div>`;
};
TELAS_DEPOIS["#/historico"] = ()=>{
  $("#btnCsvTempos")?.addEventListener("click", async ()=>{
    const [casos, laudos] = await Promise.all([db.list("casos"), db.list("laudos")]);
    const linhas = casos.map(c=> [c.numero_protocolo || "", c.status, c.inicio_em || "", c.fim_em || "", minutosDoCaso(c) ?? "", c.campos_conferidos || 0,
      c.correcoes || 0, c.correcoes_word ?? "", laudos.filter(l=> l.id_caso === c.id_caso).length].join(";"));
    baixar("historico.csv", "﻿" + ["protocolo;situacao;inicio;fim;minutos;campos_conferidos;correcoes;correcoes_word;versoes", ...linhas].join("\n"), "text/csv;charset=utf-8");
  });
  $$("[data-abrir-caso]").forEach(b=> b.addEventListener("click", async ()=>{
    await db.meta("caso_atual", b.dataset.abrirCaso);
    location.hash = "#/dados";
  }));
  $$("[data-limpar-caso]").forEach(b=> b.addEventListener("click", async ()=>{
    if (!confirm("Apagar os dados do aparelho, SIMs, hash e quesitos deste caso? As métricas ficam.")) return;
    const id = b.dataset.limparCaso;
    for (const [s, k] of [["aparelhos", "id_aparelho"], ["sims", "id_sim"], ["hashes", "id_hash"], ["quesitos", "id_quesito"]])
      for (const r of await db.porIndice(s, "id_caso", id)) await db.del(s, r[k]);
    const c = await db.get("casos", id);
    await db.put("casos", {...c, inventario: c.inventario ? {...c.inventario, itens: []} : null, requisicao: null, quesitos_requisicao: null, dados_limpos_em: agora()});
    await registrar("dados do caso limpos", {id_caso: id}); toast("Dados do caso apagados."); navegar();
  }));
};
