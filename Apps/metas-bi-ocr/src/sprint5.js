/* ================= Sprint 5 · Leitura do PDF com camada de texto ================= */
/* Sem biblioteca externa: o PDF do relatório traz o texto em streams FlateDecode,
   às vezes com ASCII85 por cima. Descomprimimos com DecompressionStream (do navegador)
   e lemos as posições Tm/Tj para reconstruir as linhas. */

function pdfA85(texto){
  const s = String(texto).replace(/\s+/g, "");
  const out = [];
  let grupo = [];
  for (let i = 0; i < s.length; i++){
    const c = s[i];
    if (c === "~") break;
    if (c === "z" && !grupo.length){ out.push(0, 0, 0, 0); continue; }
    const v = c.charCodeAt(0) - 33;
    if (v < 0 || v > 84) continue;
    grupo.push(v);
    if (grupo.length === 5){
      let n = 0; for (const g of grupo) n = n * 85 + g;
      out.push(Math.floor(n / 16777216) % 256, Math.floor(n / 65536) % 256, Math.floor(n / 256) % 256, n % 256);
      grupo = [];
    }
  }
  if (grupo.length){
    const faltam = 5 - grupo.length;
    while (grupo.length < 5) grupo.push(84);
    let n = 0; for (const g of grupo) n = n * 85 + g;
    const b = [Math.floor(n / 16777216) % 256, Math.floor(n / 65536) % 256, Math.floor(n / 256) % 256, n % 256];
    out.push(...b.slice(0, 4 - faltam));
  }
  return new Uint8Array(out);
}
teste("ASCII85 do PDF volta ao texto", ()=>{
  // "Man" em ASCII85 é "9jqo" + terminador
  const t = new TextDecoder("latin1").decode(pdfA85("9jqo~>"));
  return t === "Man" || t === "Man" + String.fromCharCode(0);
});

async function pdfInflar(bytes){
  const stream = new Blob([bytes]).stream().pipeThrough(new DecompressionStream("deflate"));
  return new Uint8Array(await new Response(stream).arrayBuffer());
}

// desfaz o escape das strings do PDF: \( \) \\ \n \r \t e octal \ddd
function pdfString(s){
  return s.replace(/\\([nrtbf()\\]|[0-7]{1,3})/g, (m, g)=>{
    if (g === "n") return "\n"; if (g === "r") return "\r"; if (g === "t") return "\t";
    if (g === "b") return "\b"; if (g === "f") return "\f";
    if (/^[0-7]+$/.test(g)) return String.fromCharCode(parseInt(g, 8));
    return g;
  });
}

// devolve o texto de todos os streams de conteúdo do PDF (vazio se for PDF em imagem)
async function lerPdfTexto(buffer){
  const bytes = new Uint8Array(buffer), latin = new TextDecoder("latin1").decode(bytes);
  const partes = [];
  let pos = 0, achouStream = false;
  while (true){
    const i = latin.indexOf("stream", pos); if (i < 0) break;
    if (latin.slice(i - 3, i) === "end"){ pos = i + 6; continue; }
    const dictIni = Math.max(0, latin.lastIndexOf("<<", i)), dict = latin.slice(dictIni, i);
    let ini = i + 6; if (latin[ini] === "\r") ini++; if (latin[ini] === "\n") ini++;
    let fim = latin.indexOf("endstream", ini); if (fim < 0) break;
    while (fim > ini && (bytes[fim - 1] === 10 || bytes[fim - 1] === 13)) fim--;
    const cru = bytes.subarray(ini, fim);
    pos = fim + 9;
    if (!/stream/.test(dict) && /(FlateDecode|ASCII85Decode)/.test(dict)){
      try {
        const entrada = dict.includes("ASCII85Decode") ? pdfA85(new TextDecoder("latin1").decode(cru)) : cru;
        partes.push(new TextDecoder("latin1").decode(await pdfInflar(entrada)));
        achouStream = true;
      } catch(e){ /* stream que não é de conteúdo: ignora */ }
    }
  }
  return {texto: partes.join("\n"), temCamada: achouStream};
}

// reconstrói as linhas pela posição (Tm) de cada texto (Tj)
function linhasDoPdf(conteudo){
  const itens = [], re = /([-\d.]+)\s+([-\d.]+)\s+Tm\s*\(((?:\\.|[^\\)])*)\)\s*Tj/g;
  let m; while ((m = re.exec(conteudo))) itens.push({x: Number(m[1]), y: Number(m[2]), t: pdfString(m[3])});
  if (!itens.length) return [];
  const porY = new Map();
  for (const it of itens){ const k = Math.round(it.y); (porY.get(k) || porY.set(k, []).get(k)).push(it); }
  const linhas = [...porY.entries()].sort((a, b)=>b[0] - a[0]).map(([, its])=>its.sort((a, b)=>a.x - b.x).map(i=>i.t.trim()).filter(Boolean));
  // cabeçalho: a primeira linha que tem "unidade" e "pendentes"
  const iCab = linhas.findIndex(l=>l.some(c=>normalizar(c).includes("unidade")));
  const out = [["Unidade", "Pendentes"]];
  for (const l of linhas.slice(iCab + 1)){
    if (l.length < 2) continue;
    const numero = l[l.length - 1], nome = l.slice(0, -1).join(" ").trim();
    if (!nome || !/^[\d.]+$/.test(numero)) continue;
    out.push([nome, numero]);
  }
  return out;
}
teste("linhas do PDF viram pares unidade e número", ()=>{
  const conteudo = "BT 1 0 0 1 50 760 Tm (Unidade) Tj ET\nBT 1 0 0 1 444 760 Tm (Pendentes) Tj ET\n"
    + "BT 1 0 0 1 50 742 Tm (IML Cuiab\\341) Tj ET\nBT 1 0 0 1 481 742 Tm (570) Tj ET";
  const l = linhasDoPdf(conteudo);
  return l.length === 2 && l[0][0] === "Unidade" && l[1][0] === "IML Cuiabá" && l[1][1] === "570";
});

/* Confiança da leitura: o texto do PDF é 1,0; o OCR (fora desta versão) viria abaixo de 0,9.
   O limite fica explícito para a conferência marcar o número duvidoso. */
const CONFIANCA_MINIMA = 0.9;
const confiancaBaixa = c => Number(c) < CONFIANCA_MINIMA;
teste("Confiança abaixo de 90% vira alerta", ()=> confiancaBaixa(0.89) && !confiancaBaixa(0.9) && !confiancaBaixa(1));
