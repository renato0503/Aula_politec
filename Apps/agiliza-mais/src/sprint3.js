/* ================= Sprint 3 · Extratores TXT e HTML (RN03, RN06, RN07) ================= */
// Formato SUPOSTO dos arquivos: ver exemplos/FORMATOS.md. Ajustar as listas de rótulos quando chegarem as amostras reais.

// Texto do arquivo: BOM de UTF-8 ou UTF-16; sem BOM, UTF-8 estrito e, se falhar, Windows-1252.
function decodificar(buffer){
  const b = new Uint8Array(buffer);
  if (b[0] === 0xFF && b[1] === 0xFE) return new TextDecoder("utf-16le").decode(b.subarray(2));
  if (b[0] === 0xFE && b[1] === 0xFF) return new TextDecoder("utf-16be").decode(b.subarray(2));
  if (b[0] === 0xEF && b[1] === 0xBB && b[2] === 0xBF) return new TextDecoder("utf-8").decode(b.subarray(3));
  // UTF-16 sem BOM: muitos zeros nas posições ímpares
  if (b.length > 8 && b.filter((x, i)=>i % 2 === 1 && x === 0).length > b.length / 4) return new TextDecoder("utf-16le").decode(b);
  try { return new TextDecoder("utf-8", {fatal: true}).decode(b); } catch(e){ return new TextDecoder("windows-1252").decode(b); }
}
// RN03: identificadores como texto, só dígitos; Luhn confere o último dígito
function luhnValido(s){
  const d = String(s || "").replace(/\D/g, ""); if (d.length < 2) return false;
  let soma = 0;
  for (let i = 0; i < d.length; i++){ let n = Number(d[d.length - 1 - i]); if (i % 2 === 1){ n *= 2; if (n > 9) n -= 9; } soma += n; }
  return soma % 10 === 0;
}
const imeiValido = s => /^\d{15}$/.test(s) && luhnValido(s);
const iccidValido = s => /^89\d{17,18}$/.test(s) && luhnValido(s);
const sha256Valido = s => /^[a-f0-9]{64}$/i.test(s);

// linhas "Rótulo: valor" -> [{rotulo, valor, linha}]
const linhasRotuladas = txt => txt.split(/\r?\n/).map((l, i)=>{ const m = l.match(/^\s*([^:]{1,40}):\s*(.*?)\s*$/); return m ? {rotulo: normalizar(m[1]), valor: m[2], linha: i + 1} : null; }).filter(Boolean);
const ROTULOS_APARELHO = {marca: ["manufacturer", "fabricante", "marca"], modelo: ["model", "modelo"], cor: ["color", "cor"],
                          imei_1: ["imei 1", "imei1", "imei"], imei_2: ["imei 2", "imei2"]};

// cada valor sai com a origem (arquivo e linha) e se é válido; ausente = null
function extrairAparelho(txt, arquivo="DEVICE INFO.txt"){
  const ls = linhasRotuladas(txt), out = {};
  for (const [campoA, rots] of Object.entries(ROTULOS_APARELHO)){
    const l = ls.find(x=>rots.includes(x.rotulo));
    if (!l || !l.valor){ out[campoA] = null; continue; }
    let valor = l.valor;
    if (campoA.startsWith("imei")) valor = valor.replace(/\D/g, "");  // texto só com dígitos, sem perder zero à esquerda
    out[campoA] = {valor, origem: arquivo, linha: l.linha, valido: campoA.startsWith("imei") ? imeiValido(valor) : true};
  }
  return out;
}
function extrairHash(txt, arquivo="HASHDOHASH.txt"){
  const ls = linhasRotuladas(txt);
  const lh = ls.find(x=>["hash", "sha-256", "sha256", "valor"].includes(x.rotulo));
  let valor = lh?.valor?.trim().toLowerCase(), linha = lh?.linha;
  if (!valor){ const i = txt.split(/\r?\n/).findIndex(x=>/\b[a-f0-9]{64}\b/i.test(x)); if (i >= 0){ valor = txt.split(/\r?\n/)[i].match(/\b[a-f0-9]{64}\b/i)[0].toLowerCase(); linha = i + 1; } }
  if (!valor) return null;
  const arq = ls.find(x=>["arquivo", "file", "nome do arquivo"].includes(x.rotulo)), alg = ls.find(x=>["algoritmo", "algorithm"].includes(x.rotulo));
  return {valor_hash: {valor, origem: arquivo, linha, valido: sha256Valido(valor)}, hash_arquivo: arq ? {valor: arq.valor, origem: arquivo, linha: arq.linha, valido: true} : null,
          algoritmo: alg ? alg.valor : "SHA-256"};
}
// RN07: o identificador do objeto vem do nome da pasta (OBJ 01-A)
function extrairSim(html, caminho){
  const pasta = caminho.split("/").slice(-2, -1)[0] || "", m = pasta.match(/obj\s*(\d{2}-[a-z])/i);
  const doc = new DOMParser().parseFromString(html, "text/html"), pares = {};
  doc.querySelectorAll("tr").forEach(tr=>{ const td = tr.querySelectorAll("td,th"); if (td.length >= 2) pares[normalizar(td[0].textContent)] = td[1].textContent.trim(); });
  const iccid = (pares["iccid"] || "").replace(/\D/g, "");
  return {identificador_objeto: m ? m[1].toUpperCase() : null, objeto_no_html: pares["objeto"] || null,
          iccid: iccid ? {valor: iccid, origem: caminho, valido: iccidValido(iccid)} : null,
          operadora: pares["operadora"] ? {valor: pares["operadora"], origem: caminho, valido: true} : null};
}

/* ---- testes dos extratores: valor certo, ausente e malformado ---- */
const TXT_OK = "Manufacturer: Samsung\r\nModel: SM-A325M\r\nColor: Preto\r\nIMEI 1: 351234567890126\r\nIMEI 2: 356938035643809\r\n";
teste("aparelho: marca, modelo e IMEIs com linha de origem", ()=>{ const a = extrairAparelho(TXT_OK); return a.marca.valor === "Samsung" && a.imei_1.linha === 4 && a.imei_2.valor === "356938035643809"; });
teste("aparelho: IMEI 2 ausente vira null, sem erro", ()=> extrairAparelho("Manufacturer: X\nIMEI 1: 351234567890126\n").imei_2 === null);
teste("aparelho: IMEI com dígito errado é marcado inválido", ()=> extrairAparelho("IMEI 1: 351234567890127\n").imei_1.valido === false);
teste("aparelho: IMEI com zero à esquerda continua texto", ()=> extrairAparelho("IMEI 1: 012345678901237\n").imei_1.valor === "012345678901237");
teste("hash: SHA-256 e arquivo", ()=>{ const h = extrairHash("Arquivo: OBJ01.zip\nAlgoritmo: SHA-256\nHash: " + "ab".repeat(32) + "\n"); return h.valor_hash.valido && h.hash_arquivo.valor === "OBJ01.zip"; });
teste("hash: arquivo sem hash devolve null", ()=> extrairHash("Arquivo: x.zip\n") === null);
teste("hash: 63 caracteres é inválido", ()=> extrairHash("Hash: " + "a".repeat(63) + "\n").valor_hash.valido === false);
teste("SIM: ICCID, operadora e objeto da pasta", ()=>{ const s = extrairSim('<table><tr><td>ICCID</td><td>8955100000000000009</td></tr><tr><td>Operadora</td><td>VIVO</td></tr></table>', "OBJ 01-A/SIM.html");
  return s.identificador_objeto === "01-A" && s.operadora.valor === "VIVO" && s.iccid.valor === "8955100000000000009"; });
teste("SIM: HTML sem ICCID devolve null no campo", ()=> extrairSim("<table><tr><td>Operadora</td><td>TIM</td></tr></table>", "OBJ 01-B/x.html").iccid === null);
teste("SIM: ICCID que não começa com 89 é inválido", ()=> extrairSim("<table><tr><td>ICCID</td><td>1234567890123456789</td></tr></table>", "OBJ 01-A/x.html").iccid.valido === false);
teste("texto UTF-16 com BOM", ()=>{ const s = "Model: Moto ç"; const b = new Uint8Array(2 + s.length * 2); b[0] = 0xFF; b[1] = 0xFE; for (let i = 0; i < s.length; i++){ b[2 + i * 2] = s.charCodeAt(i) & 255; b[3 + i * 2] = s.charCodeAt(i) >> 8; } return decodificar(b.buffer) === s; });
teste("texto Windows-1252", ()=> decodificar(new Uint8Array([77, 111, 100, 101, 108, 58, 32, 231]).buffer) === "Model: ç");

/* ---- extração do caso a partir da pasta lida no Sprint 2 ---- */
async function extrairCaso(caso){
  const ler = async c => decodificar(await lerArrayBuffer(arquivosDaSessao.get(c)));
  const inv = caso.inventario, achar = ch => inv.itens.find(i=>i.chave === ch)?.arquivos[0];
  const id = caso.id_caso, log = [];
  for (const s of ["aparelhos", "sims", "hashes"]) for (const r of await db.porIndice(s, "id_caso", id)) await db.del(s, r[s === "aparelhos" ? "id_aparelho" : s === "sims" ? "id_sim" : "id_hash"]);
  if (achar("device")){ const a = extrairAparelho(await ler(achar("device")), achar("device")); await db.put("aparelhos", {id_aparelho: id + "-A1", id_caso: id, ...a}); log.push("aparelho"); }
  if (achar("hash")){ const h = extrairHash(await ler(achar("hash")), achar("hash")); if (h) { await db.put("hashes", {id_hash: id + "-H1", id_caso: id, ...h}); log.push("hash"); } }
  for (const it of inv.itens.filter(i=>i.chave.startsWith("sim:"))){
    const s = extrairSim(await ler(it.arquivos[0]), it.arquivos[0]);
    await db.put("sims", {id_sim: `${id}-${s.identificador_objeto}`, id_caso: id, ...s}); log.push("sim " + s.identificador_objeto);
  }
  await db.put("casos", {...caso, extraido_em: agora()});
  await registrar("extração", {id_caso: id, campo_verificado: "extratores", resultado: log.join(", ") || "nada extraído"});
}

const celula = c => !c ? '<span class="selo alerta">ausente</span>'
  : `<span class="mono">${esc(c.valor)}</span> ${c.valido ? "" : '<span class="selo erro">inválido</span>'}<br><small class="sub">${esc(c.origem)}${c.linha ? `, linha ${c.linha}` : ""}</small>`;
TELAS["#/dados"] = async ()=>{
  let caso = await casoAtual();
  if (!caso?.inventario) return `<h1>Dados extraídos</h1><div class="card vazio">Selecione a pasta do caso em <a href="#/arquivos">Pasta do caso</a>.</div>`;
  if (!caso.extraido_em && arquivosDaSessao.size){ await extrairCaso(caso); caso = await casoAtual(); }
  const ap = (await db.porIndice("aparelhos", "id_caso", caso.id_caso))[0], hs = (await db.porIndice("hashes", "id_caso", caso.id_caso))[0];
  const sims = await db.porIndice("sims", "id_caso", caso.id_caso);
  return `<h1>Dados extraídos</h1><p class="sub">Caso ${esc(caso.numero_protocolo || "(sem protocolo)")} · extraído em ${dataBR(caso.extraido_em)}.
    A conferência campo a campo chega no Sprint 5. ${arquivosDaSessao.size ? `<button id="btnReextrair">Extrair de novo</button>` : ""}</p>
    <div class="card tabela-wrap"><h2 style="margin-top:0">Aparelho</h2>${ap ? `<table>${Object.keys(ROTULOS_APARELHO).map(k=>`<tr><th>${k.replace("_", " ")}</th><td>${celula(ap[k])}</td></tr>`).join("")}</table>` : '<p class="sub">DEVICE INFO.txt não lido.</p>'}</div>
    <div class="card tabela-wrap"><h2 style="margin-top:0">Hash</h2>${hs ? `<table><tr><th>valor</th><td>${celula(hs.valor_hash)}</td></tr><tr><th>arquivo</th><td>${celula(hs.hash_arquivo)}</td></tr></table>` : '<p class="sub">Sem HASHDOHASH.txt (informar manualmente na conferência).</p>'}</div>
    <div class="card tabela-wrap"><h2 style="margin-top:0">Cartões SIM (${sims.length})</h2>${sims.length ? `<table><tr><th>Objeto</th><th>ICCID</th><th>Operadora</th></tr>
      ${sims.map(s=>`<tr><td>${esc(s.identificador_objeto)}</td><td>${celula(s.iccid)}</td><td>${celula(s.operadora)}</td></tr>`).join("")}</table>` : '<p class="sub">Aparelho sem cartão SIM (RN06).</p>'}</div>`;
};
TELAS_DEPOIS["#/dados"] = ()=>{ $("#btnReextrair")?.addEventListener("click", async ()=>{ await extrairCaso(await casoAtual()); navegar(); }); };
