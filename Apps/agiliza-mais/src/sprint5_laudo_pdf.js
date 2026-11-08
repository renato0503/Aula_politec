/* ================= Sprint 16 · Laudo timbrado e saída em PDF =================
   Campos da folha de rosto, textos padrão da POLITEC e conversão do .docx gerado
   em uma página de impressão com o timbre do próprio modelo: o PDF tem o mesmo
   conteúdo do Word, porque nasce do mesmo arquivo. */
const CAMPO_EM_BRANCO = "______";

const TEXTOS_POLITEC = [
  {id_texto: "P01", categoria: "historico", titulo: "Histórico padrão POLITEC", tipo_dispositivo: "Celular", versao: "1", ativo: true,
    conteudo: "Em atendimento ao ofício da autoridade supramencionada e cumprindo a designação nº {numero_designacao} desta Diretoria Metropolitana de Criminalística, o perito oficial criminal signatário do presente laudo realizou os exames que se fizeram necessários, passando a expor o que verificou."},
  {id_texto: "P02", categoria: "exames", titulo: "Extração completa padrão POLITEC", tipo_dispositivo: "Celular", versao: "1", ativo: true,
    conteudo: "A aquisição foi realizada pelo método de extração completa de sistema de arquivos, metodologia que, por sua natureza, não assegura a recuperação de dados previamente apagados. Por conseguinte, os dados obtidos com êxito foram gravados no anexo digital para análise da autoridade requisitante."},
  {id_texto: "P03", categoria: "consideracoes", titulo: "Considerações padrão POLITEC", tipo_dispositivo: "Celular", versao: "1", ativo: true,
    conteudo: "Os objetos encaminhados para exame são remetidos à autoridade requisitante em envelope de segurança lacrado pelo signatário, apresentando número de série mencionado na folha de rosto deste documento.\nNada mais havendo a lavrar, é encerrado o presente Laudo Pericial que, relatado pelo signatário segue assinado digitalmente."},
  {id_texto: "P04", categoria: "resposta", titulo: "Resposta: extração de dados padrão POLITEC", tipo_dispositivo: "Celular", versao: "1", ativo: true,
    conteudo: "Os dados extraídos seguem encaminhados através do anexo digital deste laudo pericial para análise da autoridade requisitante. Ademais, os dados excluídos e recuperados com êxito dos aparelhos apresentam o símbolo (x) no relatório e seguem gravados no anexo digital para análise da autoridade requisitante. Para que a contextualização do conteúdo dos arquivos seja feita com maior eficiência, seguindo orientações do Manual de orientação de quesitos da Perícia Criminal (BRASIL. Departamento de Polícia Federal, Diretoria Técnico-Científica. 1. ed. Brasília: Instituto Nacional de Criminalística, 2012), “A análise e contextualização do conteúdo dos arquivos são feitas com mais eficiência pelo requisitante do laudo, e não pelos Peritos Criminais, uma vez que o requisitante é que possui conhecimento do contexto da investigação e das demais provas colhidas”."},
];

const UNIDADES_EXT = ["", "um", "duas", "três", "quatro", "cinco", "seis", "sete", "oito", "nove", "dez", "onze", "doze", "treze", "quatorze", "quinze", "dezesseis", "dezessete", "dezoito", "dezenove"];
const DEZENAS_EXT = ["", "", "vinte", "trinta", "quarenta", "cinquenta", "sessenta", "setenta", "oitenta", "noventa"];
function folhasPorExtenso(n){
  const v = Number(n);
  if (!Number.isInteger(v) || v < 1 || v > 99) return "";
  const nome = v < 20 ? UNIDADES_EXT[v] : DEZENAS_EXT[Math.floor(v / 10)] + (v % 10 ? " e " + UNIDADES_EXT[v % 10] : "");
  return `${nome} (${String(v).padStart(2, "0")})`;
}
teste("Folha de rosto: total de folhas por extenso", ()=> folhasPorExtenso(5) === "cinco (05)" && folhasPorExtenso(21) === "vinte e um (21)" && folhasPorExtenso("") === "");

const MESES_EXT = ["janeiro", "fevereiro", "março", "abril", "maio", "junho", "julho", "agosto", "setembro", "outubro", "novembro", "dezembro"];
function dataDoLaudoExtenso(txt){
  const m = String(txt || "").match(/^(\d{2})\/(\d{2})\/(\d{4})$/);
  return m && MESES_EXT[Number(m[2]) - 1] ? `${m[1]} de ${MESES_EXT[Number(m[2]) - 1]} de ${m[3]}` : String(txt || "");
}
teste("Folha de rosto: data por extenso", ()=> dataDoLaudoExtenso("01/10/2026") === "01 de outubro de 2026");

function camposDaFolhaDeRosto(caso, base, d){
  const l = caso.laudo || {}, req = caso.requisicao || {}, folhas = folhasPorExtenso(l.total_folhas);
  const qtd = d.sims.length, objetos = ["01", ...d.sims.map(s=> s.identificador_objeto).filter(Boolean)];
  const titulo = objetos.length === 1 ? "Objeto 01" : `Objetos ${objetos.slice(0, -1).join(", ")} e ${objetos[objetos.length - 1]}`;
  return {
    numero_laudo: l.numero_laudo || CAMPO_EM_BRANCO,
    procedimento: String(req.procedimento || "").replace(/^\s*I\.?\s*P\.?\s*/i, ""),
    boletim_ocorrencia: String(req.boletim_ocorrencia || "").replace(/^\s*B\.?\s*O\.?\s*/i, ""),
    numero_requisicao: req.numero_requisicao || req.numero_oficio || CAMPO_EM_BRANCO,
    natureza_exame: req.natureza_exame || "Exame em Celular e cartão SIM",
    destinacao_laudo: req.destinacao_laudo || CAMPO_EM_BRANCO,
    total_folhas_texto: folhas || `${CAMPO_EM_BRANCO} (__)`,
    ultima_folha: folhas ? String(l.total_folhas).padStart(2, "0") : "__",
    numero_designacao: l.numero_designacao || CAMPO_EM_BRANCO,
    lacre_entrada: l.lacre_entrada || (caso.itens_requisicao || []).find(i=> i.lacre)?.lacre || CAMPO_EM_BRANCO,
    lacre_saida: l.lacre_saida || CAMPO_EM_BRANCO,
    texto_capa: l.cor_capa ? `, com capa protetora de cor ${l.cor_capa}` : "",
    frase_itens: qtd ? ", e continha o(s) seguinte(s) item(ns):" : ".",
    titulo_objetos: titulo,
    data_extenso: dataDoLaudoExtenso(base.data_laudo),
    tem_quesitos: d.qs.length > 0,
    sims: base.sims.map((s, i)=> ({...s, fim: i === qtd - 1 ? "." : ";"})),
  };
}

/* ---------- leitura do .docx ---------- */
const NS_W = "http://schemas.openxmlformats.org/wordprocessingml/2006/main";
const NS_R = "http://schemas.openxmlformats.org/officeDocument/2006/relationships";
const lerXml = s=> new DOMParser().parseFromString(s, "application/xml");
const filhos = (el, nome)=> el ? [...el.children].filter(x=> x.localName === nome) : [];
const filho = (el, nome)=> filhos(el, nome)[0] || null;
const valW = (el, at = "val")=> el ? el.getAttributeNS(NS_W, at) : null;
const numW = (el, at)=> { const v = valW(el, at); return v === null || v === "" ? undefined : Number(v); };
const liga = el=> el ? !["0", "false"].includes(valW(el)) : undefined;
const semVazios = o=> Object.fromEntries(Object.entries(o).filter(([, v])=> v !== undefined && v !== null));

function propsParagrafo(pPr){
  if (!pPr) return {};
  const ind = filho(pPr, "ind"), sp = filho(pPr, "spacing"), np = filho(pPr, "numPr");
  return semVazios({jc: valW(filho(pPr, "jc")), esq: numW(ind, "left"), dir: numW(ind, "right"), prim: numW(ind, "firstLine"), susp: numW(ind, "hanging"),
    antes: numW(sp, "before"), depois: numW(sp, "after"), linha: numW(sp, "line"), regra: valW(sp, "lineRule"),
    numId: valW(filho(np, "numId")), nivel: numW(filho(np, "ilvl"), "val"), quebra: liga(filho(pPr, "pageBreakBefore")), manter: liga(filho(pPr, "keepNext"))});
}
function propsTexto(rPr){
  if (!rPr) return {};
  const f = filho(rPr, "rFonts"), u = filho(rPr, "u"), c = filho(rPr, "color");
  return semVazios({b: liga(filho(rPr, "b")), i: liga(filho(rPr, "i")), caps: liga(filho(rPr, "caps")), small: liga(filho(rPr, "smallCaps")),
    u: u && valW(u) !== "none" ? true : undefined, sz: numW(filho(rPr, "sz"), "val"), cor: c && valW(c) !== "auto" ? valW(c) : undefined,
    fonte: valW(f, "ascii"), vert: valW(filho(rPr, "vertAlign"))});
}
function lerEstilos(zip){
  const x = zip.file("word/styles.xml"); const mapa = {padraoP: null, base: {p: {}, r: {}}, por: {}};
  if (!x) return mapa;
  const raiz = lerXml(x.asText()).documentElement, dd = filho(raiz, "docDefaults");
  mapa.base = {p: propsParagrafo(filho(filho(dd, "pPrDefault"), "pPr")), r: propsTexto(filho(filho(dd, "rPrDefault"), "rPr"))};
  for (const s of filhos(raiz, "style")){
    const id = valW(s, "styleId");
    mapa.por[id] = {pai: valW(filho(s, "basedOn")), p: propsParagrafo(filho(s, "pPr")), r: propsTexto(filho(s, "rPr"))};
    if (valW(s, "type") === "paragraph" && valW(s, "default") === "1") mapa.padraoP = id;
  }
  return mapa;
}
function estiloCompleto(mapa, id, tipo){
  const cadeia = []; for (let e = mapa.por[id], g = 0; e && g < 20; e = mapa.por[e.pai], g++) cadeia.unshift(e[tipo]);
  return Object.assign({}, ...cadeia);
}
function lerNumeracao(zip){
  const x = zip.file("word/numbering.xml"), mapa = {};
  if (!x) return mapa;
  const raiz = lerXml(x.asText()).documentElement, abstr = {};
  for (const a of filhos(raiz, "abstractNum")) abstr[valW(a, "abstractNumId")] = Object.fromEntries(filhos(a, "lvl").map(l=>
    [valW(l, "ilvl"), {fmt: valW(filho(l, "numFmt")), texto: valW(filho(l, "lvlText")) || "", p: propsParagrafo(filho(l, "pPr"))}]));
  for (const n of filhos(raiz, "num")) mapa[valW(n, "numId")] = abstr[valW(filho(n, "abstractNumId"))];
  return mapa;
}
function lerRels(zip, parte){
  const pasta = parte.replace(/[^/]+$/, ""), x = zip.file(`${pasta}_rels/${parte.split("/").pop()}.rels`), mapa = {};
  if (!x) return mapa;
  for (const r of filhos(lerXml(x.asText()).documentElement, "Relationship")) mapa[r.getAttribute("Id")] = pasta + r.getAttribute("Target");
  return mapa;
}
function imagemDataUri(zip, caminho){
  const f = zip.file(caminho); if (!f) return "";
  const ext = caminho.split(".").pop().toLowerCase();
  return `data:image/${ext === "jpg" ? "jpeg" : ext};base64,${btoa(f.asBinary())}`;
}
const primeiraImagem = (zip, rels, raiz)=> {
  const b = raiz.getElementsByTagNameNS("*", "blip")[0];
  return b ? imagemDataUri(zip, rels[b.getAttributeNS(NS_R, "embed")]) : "";
};

/* ---------- conversão para HTML ---------- */
function novoConversor(zip){
  const estilos = lerEstilos(zip), numeracao = lerNumeracao(zip), contadores = {};
  const estiloDe = pPr=> valW(filho(pPr, "pStyle")) || estilos.padraoP;
  const marca = (numId, nivel)=>{
    const def = numeracao[numId]?.[nivel || 0]; if (!def || def.fmt === "none") return {texto: "", p: def?.p || {}};
    const c = contadores[numId] || (contadores[numId] = []);
    c[nivel || 0] = (c[nivel || 0] || 0) + 1; c.length = (nivel || 0) + 1;
    if (def.fmt === "bullet") return {texto: /^[-]/.test(def.texto) ? "•" : def.texto, p: def.p};
    return {texto: def.texto.replace(/%(\d)/g, (m, n)=> c[Number(n) - 1] || 1), p: def.p};
  };
  const cssTexto = r=> [r.b ? "font-weight:700" : "", r.i ? "font-style:italic" : "", r.u ? "text-decoration:underline" : "", r.caps ? "text-transform:uppercase" : "", r.small ? "font-variant:small-caps" : "",
    r.sz ? `font-size:${r.sz / 2}pt` : "", r.cor ? `color:#${r.cor}` : "", r.fonte ? `font-family:'${r.fonte}',Arial,sans-serif` : "", r.vert === "superscript" ? "vertical-align:super;font-size:70%" : ""].filter(Boolean).join(";");
  function paragrafo(p, rels){
    const pPr = filho(p, "pPr"), idE = estiloDe(pPr), sp = estiloCompleto(estilos, idE, "p"), sr = estiloCompleto(estilos, idE, "r"), dir = propsParagrafo(pPr);
    const numId = dir.numId ?? sp.numId, nivel = dir.nivel ?? sp.nivel;
    const num = numId && numId !== "0" ? marca(numId, nivel) : null;
    const f = {...estilos.base.p, ...sp, ...(num?.p || {}), ...dir};
    const pr = {...estilos.base.r, ...sr, ...propsTexto(filho(pPr, "rPr"))};
    const entra = c=> c.localName === "r" ? [c] : c.localName === "hyperlink" ? filhos(c, "r") : [];
    let html = "", texto = "";
    for (const r of [...p.children].flatMap(entra)){
      const prop = {...estilos.base.r, ...sr, ...propsTexto(filho(r, "rPr"))}, css = cssTexto(prop);
      let peca = "";
      for (const c of r.children){
        if (c.localName === "t"){ peca += esc(c.textContent); texto += c.textContent; }
        else if (c.localName === "tab") peca += '<span class="tab"></span>';
        else if (c.localName === "br" && valW(c, "type") !== "page") peca += "<br>";
        else if (c.localName === "drawing"){
          const b = c.getElementsByTagNameNS("*", "blip")[0], ex = c.getElementsByTagNameNS("*", "extent")[0];
          if (b && ex) peca += `<img alt="" src="${imagemDataUri(zip, rels[b.getAttributeNS(NS_R, "embed")])}" style="width:${Number(ex.getAttribute("cx")) / 12700}pt;height:${Number(ex.getAttribute("cy")) / 12700}pt">`;
        }
      }
      if (peca) html += css ? `<span style="${css}">${peca}</span>` : peca;
    }
    const pt = v=> `${(v || 0) / 20}pt`, recuo = (f.prim || 0) - (f.susp || 0);
    const estilo = [`text-align:${({both: "justify", center: "center", right: "right"})[f.jc] || "left"}`, `margin:${pt(f.antes)} ${pt(f.dir)} ${pt(f.depois)} ${pt(f.esq)}`, `text-indent:${pt(recuo)}`,
      f.regra === "exact" || f.regra === "atLeast" ? `line-height:${pt(f.linha)}` : f.linha ? `line-height:${(f.linha / 240).toFixed(3)}` : "", cssTexto(pr), f.manter ? "break-after:avoid" : ""].filter(Boolean).join(";");
    const pre = num?.texto ? `<span class="num">${esc(num.texto)}</span> ` : "";
    return {html: `<p style="${estilo}">${pre}${html || "&nbsp;"}</p>`, vazio: !texto.trim() && !html.includes("<img"), quebra: !!f.quebra || [...p.getElementsByTagNameNS(NS_W, "br")].some(b=> valW(b, "type") === "page")};
  }
  function tabela(t, rels){
    const pr = filho(t, "tblPr"), larg = numW(filho(pr, "tblW"), "w"), rec = numW(filho(pr, "tblInd"), "w");
    const linhas = filhos(t, "tr").map(tr=> `<tr>${filhos(tr, "tc").map(tc=>{
      const tcPr = filho(tc, "tcPr"), span = numW(filho(tcPr, "gridSpan"), "val"), w = numW(filho(tcPr, "tcW"), "w");
      const lados = ["top", "right", "bottom", "left"].filter(l=> { const v = valW(filho(filho(tcPr, "tcBorders"), l)); return v && !["nil", "none"].includes(v); });
      const css = [w ? `width:${w / 20}pt` : "", ...lados.map(l=> `border-${l}:.5pt solid #000`), lados.length ? "padding:2pt 5pt" : ""].filter(Boolean).join(";");
      return `<td${span ? ` colspan="${span}"` : ""} style="${css}">${filhos(tc, "p").map(p=> paragrafo(p, rels).html).join("")}</td>`;
    }).join("")}</tr>`).join("");
    return `<table class="dados" style="${larg ? `width:${larg / 20}pt;` : ""}${rec ? `margin-left:${rec / 20}pt` : ""}">${linhas}</table>`;
  }
  return {paragrafo, tabela};
}

// bloco do timbre: brasão + coluna da unidade + coluna do endereço
function timbreDe(zip, rels, ps){
  const textoP = p=> [...p.getElementsByTagNameNS(NS_W, "t")].map(t=> t.textContent.trim()).filter(Boolean);
  let i = 0, img = "";
  for (; i < ps.length && !textoP(ps[i]).length; i++) img = img || primeiraImagem(zip, rels, ps[i]);
  img = img || (ps[i] ? primeiraImagem(zip, rels, ps[i]) : "");
  const esq = [], dir = [];
  for (; i < ps.length && textoP(ps[i]).length; i++){
    if (valW(filho(filho(ps[i], "pPr"), "jc")) === "center") break;
    const t = textoP(ps[i]);
    if (t.length === 1 && valW(filho(filho(ps[i], "pPr"), "jc")) === "right") dir.push(t[0]);
    else { esq.push(t[0]); if (t.length > 1) dir.push(t.slice(1).join(" ")); }
  }
  if (!esq.length) return {html: "", resto: i};
  return {resto: i, html: `<div class="timbre">${img ? `<img alt="Brasão da POLITEC" src="${img}">` : ""}
    <div class="unid">${esq.map((t, n)=> `<div class="${n ? "" : "forte"}">${esc(t)}</div>`).join("")}</div>
    <div class="ender">${dir.map(t=> `<div>${esc(t)}</div>`).join("")}</div></div>`};
}

function htmlDoLaudo(zip, titulo){
  const conv = novoConversor(zip), relsDoc = lerRels(zip, "word/document.xml");
  const raiz = lerXml(zip.file("word/document.xml").asText()).documentElement, corpo = filho(raiz, "body");
  const sect = filho(corpo, "sectPr"), ref = (tipo, qual)=> filhos(sect, tipo + "Reference").find(r=> valW(r, "type") === qual)?.getAttributeNS(NS_R, "id");
  const blocos = [...corpo.children].filter(c=> ["p", "tbl"].includes(c.localName));
  // a folha de rosto vai até o primeiro parágrafo com quebra de página antes
  const render = lista=> lista.map(c=> c.localName === "tbl" ? {html: conv.tabela(c, relsDoc), quebra: false} : conv.paragrafo(c, relsDoc));
  const fim = (()=>{ const i = render(blocos).findIndex(b=> b.quebra); return i > 0 ? i : 0; })();
  // o contador da numeração recomeça porque render() acima já passou uma vez pelos parágrafos
  const conv2 = novoConversor(zip);
  const pintar = lista=> lista.map(c=> c.localName === "tbl" ? conv2.tabela(c, relsDoc) : conv2.paragrafo(c, relsDoc).html).join("");
  const parRosto = blocos.slice(0, fim).filter(c=> c.localName === "p");
  const tRosto = timbreDe(zip, relsDoc, parRosto);
  const rosto = fim ? `<section class="rosto">${tRosto.html}${pintar(blocos.slice(0, fim).slice(tRosto.resto))}</section>` : "";

  let cab = "", imgRodape = "";
  const parteCab = ref("header", "default") && relsDoc[ref("header", "default")], parteRod = ref("footer", "default") && relsDoc[ref("footer", "default")];
  if (parteCab && zip.file(parteCab)){
    const relsC = lerRels(zip, parteCab), ps = filhos(lerXml(zip.file(parteCab).asText()).documentElement, "p");
    const t = timbreDe(zip, relsC, ps), conv3 = novoConversor(zip);
    cab = t.html + ps.slice(t.resto).map(p=> conv3.paragrafo(p, relsC)).filter(b=> !b.vazio).map(b=> b.html).join("");
  }
  if (parteRod && zip.file(parteRod)) imgRodape = primeiraImagem(zip, lerRels(zip, parteRod), lerXml(zip.file(parteRod).asText()).documentElement);

  const css = `html{print-color-adjust:exact;-webkit-print-color-adjust:exact}
    @page{size:A4;margin:12mm 18mm 25mm 20mm;
      @bottom-center{content:"Página " counter(page) " de " counter(pages);font:9pt Arial,sans-serif;vertical-align:top;padding-top:2mm;print-color-adjust:exact;-webkit-print-color-adjust:exact;
        ${imgRodape ? `background:url("${imgRodape}") center 7mm/100% auto no-repeat;` : ""}}}
    @page:first{@bottom-center{content:none;background:none}}
    html,body{margin:0;background:#fff;color:#000}
    body{font:12pt Arial,sans-serif}
    p{orphans:2;widows:2}
    .tab{display:inline-block;width:36pt}
    .num{font-weight:inherit}
    .timbre{display:flex;align-items:center;gap:10pt;font-size:9pt;line-height:1.3}
    .timbre img{height:25mm;width:auto}
    .timbre .unid{flex:1;text-align:right;padding-right:10pt;border-right:2pt solid #1f3a7a}
    .timbre .unid .forte{font-weight:700}
    .timbre .ender{flex:none;min-width:40mm}
    .rosto{break-after:page}
    .paginas{width:100%;border-collapse:collapse}
    .paginas>thead>tr>td,.paginas>tbody>tr>td{padding:0;border:0}
    .paginas>thead>tr>td{padding-bottom:10pt}
    .dados{border-collapse:collapse;margin:6pt 0;table-layout:fixed}
    .dados td{vertical-align:top;overflow-wrap:anywhere}`;
  return `<!doctype html><html lang="pt-BR"><head><meta charset="utf-8"><title>${esc(titulo)}</title><style>${css}</style></head><body>${rosto}
    <table class="paginas"><thead><tr><td>${cab}</td></tr></thead><tbody><tr><td>${pintar(blocos.slice(fim))}</td></tr></tbody></table></body></html>`;
}

// imprime em um quadro escondido: a página do app não muda e o nome sugerido é o do laudo
function imprimirLaudo(html, nome){
  document.getElementById("quadroLaudo")?.remove();
  const q = document.createElement("iframe"), tituloApp = document.title;
  q.id = "quadroLaudo"; q.title = "Laudo para impressão"; q.style.cssText = "position:fixed;right:0;bottom:0;width:0;height:0;border:0";
  q.addEventListener("load", ()=>{
    document.title = nome;
    q.contentWindow.addEventListener("afterprint", ()=> { document.title = tituloApp; });
    q.contentWindow.focus(); q.contentWindow.print();
  }, {once: true});
  q.srcdoc = html;
  document.body.appendChild(q);
}
