/* ================= Leitura completa do PDF: camada de texto + OCR embutido (Tesseract.js 5) =================
   A requisição chega de dois jeitos:
   - com camada de texto: o pdf.js devolve o texto da página;
   - escaneada (cada página é uma imagem): a página é desenhada num canvas e o Tesseract lê.
   Todas as páginas são lidas, uma a uma, e cada página guarda de onde veio o texto (texto ou OCR).
   Tudo offline: o worker, o núcleo WebAssembly e o idioma português ficam embutidos no index.html. */

const NL = String.fromCharCode(10);
const blobTexto = id => document.getElementById("blob-" + id)?.textContent || "";

// um worker por vez é lento (cerca de 15 s por página); as páginas são divididas entre até 3 workers
const _ocrs = [];
let _ocrUrl = null;
async function ocrWorker(indice = 0){
  if (_ocrs[indice]) return _ocrs[indice];
  if (typeof Tesseract === "undefined" || !blobTexto("tesseract-worker.min.js")) throw new Error("o OCR não está embutido nesta versão do app");
  /* Um Blob só com: (1) um fetch local que entrega o idioma embutido; (2) o núcleo WebAssembly;
     (3) o worker. Nada sai para a rede. */
  if (!_ocrUrl){
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
    _ocrUrl = URL.createObjectURL(new Blob([codigo], {type: "application/javascript"}));
  }
  const w = await Tesseract.createWorker("por", 1, {workerPath: _ocrUrl, workerBlobURL: false, corePath: "embutido.js",
    langPath: "https://embutido.invalid/tessdata", cacheMethod: "none", gzip: true});
  await w.setParameters({tessedit_pageseg_mode: "3", preserve_interword_spaces: "1"});
  return (_ocrs[indice] = w);
}
const qtdWorkersOcr = () => Math.max(1, Math.min(3, (navigator.hardwareConcurrency || 2) - 1));

// palavras com posição -> linhas de texto (agrupa pela altura; a ordem é da esquerda para a direita)
function linhasDePalavras(palavras){
  const ps = palavras.filter(p=>String(p.t).trim()).sort((a, b)=>a.y - b.y);
  const alturas = ps.map(p=>p.h || 10).sort((a, b)=>a - b), tol = (alturas[Math.floor(alturas.length / 2)] || 10) * 0.55;
  const linhas = [];
  for (const p of ps){
    const l = linhas.find(x=>Math.abs(x.y - p.y) <= tol);
    if (l){ l.itens.push(p); l.y = (l.y * (l.itens.length - 1) + p.y) / l.itens.length; }
    else linhas.push({y: p.y, itens: [p]});
  }
  return linhas.sort((a, b)=>a.y - b.y).map(l=>l.itens.sort((a, b)=>a.x0 - b.x0).map(p=>p.t).join(" ").replace(/\s+/g, " ").trim()).filter(Boolean);
}
teste("OCR: palavras na mesma altura viram uma linha, na ordem", ()=> linhasDePalavras([
  {t: "Natureza", x0: 0, y: 10, h: 10}, {t: "Exame:", x0: 50, y: 11, h: 10}, {t: "COMPUTAÇÃO", x0: 100, y: 9, h: 10}, {t: "Item", x0: 0, y: 40, h: 10}]).join("|") === "Natureza Exame: COMPUTAÇÃO|Item");

// o texto vertical da assinatura digital (margem direita) e o QR Code viram lixo: ficam de fora
function palavraUtil(w, largura){
  const b = w.bbox, larg = b.x1 - b.x0, alt = b.y1 - b.y0, t = String(w.text || "").trim();
  if (!t || (w.confidence ?? 0) < 35) return false;
  if (b.x0 > largura * 0.93) return false;                 // faixa da assinatura digital
  if (t.length > 2 && alt > larg * 1.4) return false;       // texto girado 90 graus
  return true;
}

/* Lê todas as páginas. aviso(texto) recebe o andamento.
   Devolve {texto, paginas: [{n, origem: "texto"|"ocr", texto, confianca}]} na ordem das páginas. */
async function lerPdfCompleto(file, aviso = ()=>{}){
  if (typeof pdfjsLib === "undefined") throw new Error("o leitor de PDF (pdf.js) não está embutido");
  const doc = await pdfjsLib.getDocument({data: new Uint8Array(await lerArrayBuffer(file)), isEvalSupported: false}).promise;
  const total = doc.numPages, paginas = new Array(total), fila = [];
  for (let n = 1; n <= total; n++){
    const pag = await doc.getPage(n), tc = await pag.getTextContent();
    const txt = tc.items.map(it=> it.str + (it.hasEOL ? NL : "")).join("");
    if (txt.replace(/\s/g, "").length >= 40) paginas[n - 1] = {n, origem: "texto", texto: txt, confianca: 100};
    else fila.push(n);   // página escaneada: vai para o OCR
  }
  let prontas = total - fila.length;
  const andamento = ()=> aviso(`Lidas ${prontas} de ${total} página(s).`, prontas / total);
  andamento();
  if (fila.length){
    aviso(`Preparando o OCR para ${fila.length} página(s) escaneada(s)...`, prontas / total);
    const nw = Math.min(qtdWorkersOcr(), fila.length);
    await Promise.all(Array.from({length: nw}, async (_, k)=>{
      const w = await ocrWorker(k);
      while (fila.length){
        const n = fila.shift(), pag = await doc.getPage(n);
        const v1 = pag.getViewport({scale: 1}), escala = Math.min(3, Math.max(1.2, 1400 / Math.min(v1.width, v1.height))), vp = pag.getViewport({scale: escala});
        const cv = document.createElement("canvas"); cv.width = Math.ceil(vp.width); cv.height = Math.ceil(vp.height);
        const ctx = cv.getContext("2d"); ctx.fillStyle = "#fff"; ctx.fillRect(0, 0, cv.width, cv.height);
        await pag.render({canvasContext: ctx, viewport: vp}).promise;
        const {data} = await w.recognize(cv);
        const palavras = (data.words || []).filter(p=> palavraUtil(p, cv.width))
          .map(p=>({t: p.text, x0: p.bbox.x0, y: (p.bbox.y0 + p.bbox.y1) / 2, h: p.bbox.y1 - p.bbox.y0}));
        paginas[n - 1] = {n, origem: "ocr", texto: palavras.length ? linhasDePalavras(palavras).join(NL) : (data.text || ""), confianca: Math.round(data.confidence || 0)};
        cv.width = cv.height = 0; prontas++; andamento();
      }
    }));
  }
  return {texto: paginas.map(p=> p.texto).join(NL), paginas};
}
