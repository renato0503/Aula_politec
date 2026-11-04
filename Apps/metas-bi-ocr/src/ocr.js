/* ================= Sprint 9 · PDF pelo pdf.js e OCR embutido (Tesseract.js 5) =================
   O relatório do Power BI 1 chega em PDF de dois jeitos:
   - com camada de texto: o pdf.js devolve cada texto com a posição;
   - como imagem (print do painel): a página é desenhada num canvas e o Tesseract lê.
   Nos dois casos as palavras viram linhas (pela altura) e a tabela é montada pelas
   colunas de números. A prévia mostra o que foi lido antes de gravar. Tudo offline:
   o worker, o núcleo WebAssembly e o idioma português ficam embutidos no index.html. */

const blobTexto = id => document.getElementById("blob-" + id)?.textContent || "";

let _ocr = null;
async function ocrWorker(aviso){
  if (_ocr) return _ocr;
  if (typeof Tesseract === "undefined" || !blobTexto("tesseract-worker.min.js")) throw new Error("o OCR não está embutido nesta versão do app");
  /* Um Blob só com: (1) um fetch local que entrega o idioma embutido; (2) o núcleo WebAssembly,
     que deixa o TesseractCore pronto; (3) o worker. Nada sai para a rede. */
  const shim = `self.__POR = ${JSON.stringify(blobTexto("por.traineddata.gz").trim())};
self.fetch = (function(orig){ return function(url, o){
  if (String(url).indexOf("embutido.invalid") >= 0){
    var bin = atob(self.__POR), out = new Uint8Array(bin.length);
    for (var i = 0; i < bin.length; i++) out[i] = bin.charCodeAt(i);
    return Promise.resolve(new Response(out, {status: 200}));
  }
  return orig ? orig(url, o) : Promise.reject(new Error("sem rede"));
}; })(self.fetch);\n`;
  const codigo = shim + blobTexto("tesseract-core-simd-lstm.wasm.js") + "\n;\n" + blobTexto("tesseract-worker.min.js");
  const url = URL.createObjectURL(new Blob([codigo], {type: "application/javascript"}));
  _ocr = await Tesseract.createWorker("por", 1, {
    workerPath: url, workerBlobURL: false, corePath: "embutido.js", langPath: "https://embutido.invalid/tessdata", cacheMethod: "none", gzip: true,
    logger: m=>{ if (aviso && m.status) aviso(m.status, m.progress); },
  });
  await _ocr.setParameters({tessedit_pageseg_mode: "6", preserve_interword_spaces: "1"});
  return _ocr;
}

/* ---------- palavras -> linhas -> tabela ---------- */
const RE_NUM = /^\d{1,3}(?:[.,]\d{3})+$|^\d+$/;
const numeroDe = t => Number(String(t).replace(/[.,]/g, ""));
// OCR troca O por 0, l/I por 1 dentro de números: só corrige quando o resto do token é número
// na coluna de números (forte = true), também T->7, S->5, B->8, Z->2 e g->9
function limparNumero(t, forte = false){
  const s = String(t).replace(/[|»«"'`]/g, "").trim();
  const letras = forte ? /^[\dOoIlTSBZg.,]+$/ : /^[\dOoIl.,]+$/;
  if (!letras.test(s) || !/\d/.test(s)) return s;
  let r = s.replace(/[Oo]/g, "0").replace(/[Il]/g, "1");
  if (forte) r = r.replace(/T/g, "7").replace(/S/g, "5").replace(/B/g, "8").replace(/Z/g, "2").replace(/g/g, "9");
  return r;
}

// palavras [{t, x0, x1, y, conf}] -> linhas (agrupa por altura, tolerância de meia linha)
function agruparLinhas(palavras){
  const ps = palavras.filter(p=>String(p.t).trim()).sort((a, b)=>a.y - b.y);
  const alturas = ps.map(p=>p.h || 10).sort((a, b)=>a - b), tol = (alturas[Math.floor(alturas.length / 2)] || 10) * 0.6;
  const linhas = [];
  for (const p of ps){
    const l = linhas.find(x=>Math.abs(x.y - p.y) <= tol);
    if (l){ l.itens.push(p); l.y = (l.y * (l.itens.length - 1) + p.y) / l.itens.length; }
    else linhas.push({y: p.y, itens: [p]});
  }
  return linhas.sort((a, b)=>a.y - b.y).map(l=>l.itens.sort((a, b)=>a.x0 - b.x0));
}

/* linhas -> {cabecalho: [rótulos das colunas de número], linhas: [{nome, nums: [{v, conf}]}], total, colPadrao}
   O nome é o texto antes dos números; as colunas de número são contadas da direita. */
function tabelaDeLinhas(linhas){
  const dados = [], centros = [];
  let total = null;
  for (const l of linhas){
    const toks = l.map(p=>({...p, t: limparNumero(p.t)}));
    let k = toks.length; while (k > 0 && RE_NUM.test(toks[k - 1].t)) k--;
    const nums = toks.slice(k), nome = toks.slice(0, k).map(p=>p.t).join(" ").replace(/\s+/g, " ").replace(/^[^\p{L}\d]+|[^\p{L}\d)]+$/gu, "").trim();
    if (!nums.length || !/\p{L}/u.test(nome)) continue;
    const linha = {nome, nums: nums.map(p=>({v: numeroDe(p.t), conf: p.conf ?? 1, x: (p.x0 + p.x1) / 2})), y: l[0].y};
    if (normalizar(nome) === "total" || normalizar(nome).startsWith("total ")) { total = linha; continue; }
    dados.push(linha);
  }
  if (!dados.length) return {cabecalho: [], linhas: [], total: null, colPadrao: 0};
  // quantidade de colunas = a mais comum entre as linhas
  const freq = {}; dados.forEach(d=>freq[d.nums.length] = (freq[d.nums.length] || 0) + 1);
  const ncol = Number(Object.entries(freq).sort((a, b)=>b[1] - a[1] || b[0] - a[0])[0][0]);
  for (let j = 0; j < ncol; j++){
    const xs = dados.filter(d=>d.nums.length === ncol).map(d=>d.nums[j].x);
    centros.push(xs.reduce((a, b)=>a + b, 0) / xs.length);
  }
  /* Segunda passada, pela geometria: o que fica à esquerda das colunas é o nome; cada palavra
     dentro da faixa das colunas vai para a coluna mais próxima. Assim um "77" lido como "T7"
     não contamina o nome (vira célula duvidosa) e um título com "2026" fora das colunas é descartado. */
  const passo = ncol > 1 ? Math.min(...centros.slice(1).map((c, j)=>c - centros[j])) : 200;
  const inicioCols = Math.min(...centros) - passo / 2;
  const reparse = [];
  let totalGeo = null;
  for (const l of linhas){
    const nomeToks = [], cel = Array(ncol).fill(null); let fora = false;
    for (const p of l){
      const cx = (p.x0 + p.x1) / 2;
      if (cx < inicioCols){ nomeToks.push(p.t); continue; }
      let j = 0; centros.forEach((c, i)=>{ if (Math.abs(cx - c) < Math.abs(cx - centros[j])) j = i; });
      if (Math.abs(cx - centros[j]) > passo / 2){ fora = true; continue; }
      // letra trocada por dígito é palpite: a confiança cai para no máximo 60%
      const t = limparNumero(p.t, true), ok = RE_NUM.test(t), trocou = t !== String(p.t).replace(/[|»«"'`]/g, "").trim();
      cel[j] = ok ? {v: numeroDe(t), conf: trocou ? Math.min(p.conf ?? 1, 0.6) : (p.conf ?? 1), x: cx} : {v: null, conf: 0, x: cx, lido: p.t};
    }
    const nome = nomeToks.join(" ").replace(/\s+/g, " ").replace(/^[^\p{L}\d]+|[^\p{L}\d)]+$/gu, "").trim();
    // linha sem nenhum número legível (cabeçalho, título) não é dado
    if (fora || !cel.some(c=>c && c.v !== null)) continue;
    const linha = {nome, nums: cel, y: l[0].y};
    if (!nome || /(^|\s)total( geral)?$/.test(normalizar(nome)) || normalizar(nome).startsWith("total ")){ if (!nome && totalGeo) continue; totalGeo = linha; continue; }
    if (!/\p{L}/u.test(nome)) continue;
    reparse.push(linha);
  }
  if (reparse.length){ dados.splice(0, dados.length, ...reparse); if (totalGeo) total = totalGeo; }
  else {
    const alinhar = d => d.nums.length >= ncol ? d.nums.slice(-ncol) : [...Array(ncol - d.nums.length).fill(null), ...d.nums];
    dados.forEach(d=>d.nums = alinhar(d)); if (total) total.nums = alinhar(total);
  }
  // cabeçalho: a linha de texto acima da primeira linha de dados com palavras sobre as colunas
  const y0 = dados[0].y;
  const cab = linhas.filter(l=>l[0].y < y0).reverse().find(l=>l.some(p=>(p.x0 + p.x1) / 2 >= inicioCols && /\p{L}/u.test(p.t)));
  const cabecalho = centros.map((c, j)=>cab ? cab.filter(p=>{
    const cx = (p.x0 + p.x1) / 2; if (cx < inicioCols) return false;
    return centros.every((o, i)=>i === j || Math.abs(cx - c) <= Math.abs(cx - o));
  }).map(p=>p.t).join(" ") : "");
  let colPadrao = cabecalho.findIndex(h=>/pendente/i.test(normalizar(h)));
  if (colPadrao < 0) colPadrao = ncol - 1;
  return {cabecalho: cabecalho.map((h, j)=>h || `Coluna ${j + 1}`), linhas: dados, total, colPadrao};
}
teste("Tabela do OCR: nome à esquerda, coluna de pendentes pelo cabeçalho", ()=>{
  const w = (t, x, y, conf = 0.95)=>({t, x0: x, x1: x + t.length * 8, y, h: 12, conf});
  const t = tabelaDeLinhas(agruparLinhas([w("Unidade", 10, 10), w("Recebidos", 300, 10), w("Laudos", 420, 10), w("pendentes", 480, 10),
    w("Gerência", 10, 40), w("de", 80, 40), w("Necropsia", 100, 40), w("1.204", 300, 40), w("57O", 450, 40, 0.6),
    w("Total", 10, 70), w("1.204", 300, 70), w("570", 450, 70)]));
  return t.linhas.length === 1 && t.linhas[0].nome === "Gerência de Necropsia" && t.colPadrao === 1
    && t.linhas[0].nums[1].v === 570 && t.linhas[0].nums[0].v === 1204 && t.total.nums[1].v === 570;
});

// mês de referência no texto do relatório: "2026-07", "07/2026", "julho de 2026", "jul/2026"
const MESES_PT = ["jan", "fev", "mar", "abr", "mai", "jun", "jul", "ago", "set", "out", "nov", "dez"];
function mesNoTexto(texto){
  const s = normalizar(texto);
  let m = s.match(/\b(20\d{2})-(0[1-9]|1[0-2])\b/); if (m) return `${m[1]}-${m[2]}`;
  m = s.match(/\b(0?[1-9]|1[0-2])\/(20\d{2})\b/); if (m) return `${m[2]}-${m[1].padStart(2, "0")}`;
  m = s.match(/\b(jan|fev|mar|abr|mai|jun|jul|ago|set|out|nov|dez)[a-z]*\.?(?:\s+de)?\s*[\/ ]\s*(20\d{2})\b/);
  return m ? `${m[2]}-${String(MESES_PT.indexOf(m[1]) + 1).padStart(2, "0")}` : null;
}
teste("Mês no texto do relatório", ()=> mesNoTexto("Posição em julho de 2026") === "2026-07" && mesNoTexto("ref. 09/2026") === "2026-09" && mesNoTexto("sem data") === null);

/* Cabeçalho do Power BI costuma ser texto claro sobre faixa escura: o OCR perde.
   Cada linha de pixels em que 45% ou mais dos pontos são escuros (luminância < 110) é invertida. */
function clarearFaixasEscuras(ctx, w, h){
  const img = ctx.getImageData(0, 0, w, h), d = img.data;
  for (let y = 0; y < h; y++){
    let escuros = 0; const ini = y * w * 4;
    for (let x = 0; x < w; x += 4) if (0.299 * d[ini + x * 4] + 0.587 * d[ini + x * 4 + 1] + 0.114 * d[ini + x * 4 + 2] < 110) escuros++;
    if (escuros / Math.ceil(w / 4) < 0.45) continue;
    for (let x = 0; x < w; x++){ const i = ini + x * 4; d[i] = 255 - d[i]; d[i + 1] = 255 - d[i + 1]; d[i + 2] = 255 - d[i + 2]; }
  }
  ctx.putImageData(img, 0, 0);
}

/* ---------- leitura do PDF ---------- */
// devolve {tabela, texto, origem: "pdf"|"ocr", paginas}
async function lerPdfRelatorio(buffer, aviso = ()=>{}){
  if (typeof pdfjsLib === "undefined") throw new Error("o leitor de PDF não está embutido");
  const doc = await pdfjsLib.getDocument({data: new Uint8Array(buffer), isEvalSupported: false}).promise;
  const palavras = [], textos = [];
  let yBase = 0;
  for (let n = 1; n <= doc.numPages; n++){
    const pag = await doc.getPage(n), vp = pag.getViewport({scale: 1}), tc = await pag.getTextContent();
    for (const it of tc.items){
      const s = String(it.str || ""); if (!s.trim()) continue;
      textos.push(s);
      // quebra o item em palavras, com a posição proporcional ao número de letras
      const x = it.transform[4], y = yBase + (vp.height - it.transform[5]), larg = it.width || s.length * 5, h = it.height || 10;
      let pos = 0;
      for (const parte of s.split(/(\s+)/)){
        if (parte.trim()) palavras.push({t: parte, x0: x + larg * pos / s.length, x1: x + larg * (pos + parte.length) / s.length, y, h, conf: 1});
        pos += parte.length;
      }
    }
    yBase += vp.height + 50;
  }
  let tabela = tabelaDeLinhas(agruparLinhas(palavras));
  if (tabela.linhas.length) return {tabela, texto: textos.join(" "), origem: "pdf", paginas: doc.numPages};
  // sem texto aproveitável: OCR página a página
  aviso("Preparando o OCR (a primeira leitura leva alguns segundos)...");
  const w = await ocrWorker((st, p)=>aviso(`OCR: ${st}${p ? ` ${Math.round(p * 100)}%` : ""}`));
  const pOcr = []; let txt = ""; yBase = 0;
  for (let n = 1; n <= doc.numPages; n++){
    aviso(`Lendo a página ${n} de ${doc.numPages} pelo OCR...`);
    const pag = await doc.getPage(n), v1 = pag.getViewport({scale: 1});
    const escala = Math.min(4, Math.max(2, 2400 / v1.width)), vp = pag.getViewport({scale: escala});
    const cv = document.createElement("canvas"); cv.width = Math.ceil(vp.width); cv.height = Math.ceil(vp.height);
    const ctx = cv.getContext("2d"); ctx.fillStyle = "#fff"; ctx.fillRect(0, 0, cv.width, cv.height);
    await pag.render({canvasContext: ctx, viewport: vp}).promise;
    clarearFaixasEscuras(ctx, cv.width, cv.height);
    const {data} = await w.recognize(cv);
    txt += " " + (data.text || "");
    for (const p of data.words || []) pOcr.push({t: p.text, x0: p.bbox.x0, x1: p.bbox.x1, y: yBase + (p.bbox.y0 + p.bbox.y1) / 2, h: p.bbox.y1 - p.bbox.y0, conf: (p.confidence ?? 0) / 100});
    yBase += cv.height + 100;
  }
  tabela = tabelaDeLinhas(agruparLinhas(pOcr));
  return {tabela, texto: txt, origem: "ocr", paginas: doc.numPages};
}

/* ---------- prévia: o que foi lido, antes de gravar ---------- */
function previaLeitura(arquivo, r){
  const t = r.tabela, op = t.cabecalho.map((h, j)=>[String(j), h]);
  const baixa = t.linhas.filter(l=>l.nums[t.colPadrao] && confiancaBaixa(l.nums[t.colPadrao].conf)).length;
  return `<div class="card" id="previaPdf"><h2 style="margin-top:0">Conferir a leitura do PDF</h2>
    <p class="sub">${esc(arquivo)} · ${r.paginas} página(s) · ${r.origem === "ocr" ? "lido por <b>OCR</b> (o PDF é imagem)" : "lido pela camada de texto"} ·
      ${t.linhas.length} linhas${baixa ? ` · <span class="selo alerta">${baixa} número(s) com confiança abaixo de 90%</span>` : ""}</p>
    <p class="sub">Confira os nomes e os números, desmarque o que não é unidade e escolha a coluna dos laudos pendentes. O que você corrigir aqui entra como lido.</p>
    <div class="campos">${campo("colPendentes", "Coluna dos laudos pendentes", {tipo: "select", valor: String(t.colPadrao), opcoes: op})}</div>
    <div class="tabela-wrap"><table id="tabelaPrevia"><tr><th>Usar</th><th>Unidade lida</th>${t.cabecalho.map((h, j)=>`<th class="num" data-col="${j}">${esc(h)}</th>`).join("")}<th>Lotação</th></tr>
      ${t.linhas.map((l, i)=>{ const lot = lotacaoDe(l.nome);
        return `<tr data-i="${i}"><td><input type="checkbox" data-usar checked aria-label="Usar a linha ${esc(l.nome)}"></td>
        <td><input type="text" data-nome value="${esc(l.nome)}" aria-label="Unidade" style="min-width:16rem"></td>
        ${l.nums.map((n, j)=>`<td class="num" data-col="${j}"><input type="number" min="0" data-num="${j}" value="${n && n.v !== null ? n.v : ""}" style="width:7rem" aria-label="${esc(t.cabecalho[j])}">
          ${n && confiancaBaixa(n.conf) ? `<span class="selo alerta" title="${n.lido ? `o OCR leu “${esc(n.lido)}”` : "confiança do OCR"}">${n.v === null ? "ilegível" : Math.round(n.conf * 100) + "%"}</span>` : ""}</td>`).join("")}
        <td><small>${esc(lot.gerencia || lot.coordenadoria || lot.diretoria || "fora do organograma")}</small></td></tr>`; }).join("")}
      ${t.total ? `<tr class="total"><td></td><td><b>Total do relatório</b></td>${t.total.nums.map((n, j)=>`<td class="num" data-col="${j}"><input type="number" min="0" data-total="${j}" value="${n && n.v !== null ? n.v : ""}" style="width:7rem" aria-label="Total ${esc(t.cabecalho[j])}"></td>`).join("")}<td></td></tr>` : ""}
    </table></div>
    <div class="linha-botoes"><button type="button" class="prim" id="btnUsarPrevia">Importar estas linhas</button><button type="button" id="btnDescartarPrevia">Descartar</button></div></div>`;
}
// lê a prévia (com as correções da pessoa) e devolve linhas no formato do CSV + a confiança de cada uma
function linhasDaPrevia(r){
  const col = Number(valorDe("colPendentes") || r.tabela.colPadrao), linhas = [["Unidade", "Laudos pendentes"]], conf = {}, editadas = [];
  $$("#tabelaPrevia tr[data-i]").forEach(tr=>{
    if (!tr.querySelector("[data-usar]").checked) return;
    const i = Number(tr.dataset.i), orig = r.tabela.linhas[i], nome = tr.querySelector("[data-nome]").value.trim();
    const v = tr.querySelector(`[data-num="${col}"]`)?.value ?? "";
    if (!nome || v === "") return;
    linhas.push([nome, v]);
    const n = orig.nums[col], mudou = !n || String(n.v) !== String(v) || nome !== orig.nome;
    conf[normalizar(nome)] = mudou ? 1 : (n ? n.conf : 1);
    if (mudou) editadas.push(nome);
  });
  const tot = $(`#tabelaPrevia [data-total="${col}"]`)?.value;
  if (tot !== undefined && tot !== "") linhas.push(["Total", tot]);
  return {linhas, conf, editadas};
}
