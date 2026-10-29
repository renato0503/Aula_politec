/* Agiliza + · código do app (o construir.py junta com a base comum) */
"use strict";
teste("Biblioteca de textos do exemplo tem 11 textos", ()=> (dadosEmbutidos("seed")?.textos || []).length === 11);
teste("Página sem acesso à rede (CSP connect-src 'none')", ()=> /connect-src 'none'/.test(document.querySelector('meta[http-equiv="Content-Security-Policy"]')?.content || ""));

async function casoAtual(){ const id = await db.meta("caso_atual"); return id ? await db.get("casos", id) : null; }

/* ================= Sprint 1 · Início ================= */
TELAS["#/inicio"] = async ()=>{
  const casos = (await db.list("casos")).sort((a, b)=>(b.inicio_em || "").localeCompare(a.inicio_em || ""));
  const atual = await db.meta("caso_atual");
  return `<h1>Início</h1><p class="sub">Cada caso corresponde a um laudo de um aparelho celular (RN05).</p>
    <div class="card"><h2 style="margin-top:0">Novo laudo</h2>
      <label for="novoProtocolo">Protocolo (pode ser preenchido depois, a partir da requisição)</label>
      <input id="novoProtocolo" placeholder="2026.0001001">
      <div class="linha-botoes"><button class="prim" id="btnNovoCaso">Criar caso e selecionar a pasta</button></div></div>
    <div class="card tabela-wrap"><h2 style="margin-top:0">Casos</h2>
      ${casos.length ? `<table><tr><th>Protocolo</th><th>Pasta</th><th>Início</th><th>Situação</th><th></th></tr>${casos.map(c=>`<tr><td>${esc(c.numero_protocolo || "(sem protocolo)")}
        ${c.id_caso === atual ? ' <span class="selo ok">atual</span>' : ""}</td><td>${esc(c.pasta_nome || "")}</td>
        <td>${esc(dataBR(c.inicio_em))}</td><td><span class="selo info">${esc(c.status)}</span></td>
        <td><button data-retomar="${esc(c.id_caso)}">Retomar</button></td></tr>`).join("")}</table>`
      : `<div class="vazio">Nenhum caso ainda.</div>`}</div>`;
};
TELAS_DEPOIS["#/inicio"] = ()=>{
  $("#btnNovoCaso").addEventListener("click", async ()=>{
    const caso = {id_caso: uuid(), numero_protocolo: $("#novoProtocolo").value.trim(), status: "em elaboração", inicio_em: null, fim_em: null, criado_em: agora()};
    await db.put("casos", caso); await db.meta("caso_atual", caso.id_caso); await registrar("caso criado", {id_caso: caso.id_caso});
    location.hash = "#/arquivos";
  });
  $$("[data-retomar]").forEach(b=>b.addEventListener("click", async ()=>{ await db.meta("caso_atual", b.dataset.retomar); location.hash = "#/arquivos"; }));
};

/* ================= Sprint 2 · Pasta do caso (RN01, RN02) ================= */
// Arquivos esperados na pasta do caso (formato em exemplos/FORMATOS.md).
const ESPERADOS = [
  {chave: "requisicao", rotulo: "Requisição em PDF", obrigatorio: true, casa: c=>/\.pdf$/i.test(c) && /requisi/i.test(normalizar(nomeDe(c))), varios: true},
  {chave: "device", rotulo: "DEVICE INFO.txt", obrigatorio: true, casa: c=>normalizar(nomeDe(c)) === "device info.txt"},
  {chave: "hash", rotulo: "HASHDOHASH.txt", obrigatorio: true, casa: c=>normalizar(nomeDe(c)) === "hashdohash.txt"}
];
const nomeDe = caminho => caminho.split("/").pop();
const RE_OBJ = /^obj\s*(\d{2}-[a-z])$/i;
const arquivosDaSessao = new Map();  // caminho -> File (os extratores do Sprint 3 leem daqui)

// lista de caminhos relativos à pasta do caso -> inventário
function inventariar(caminhos){
  const itens = ESPERADOS.map(e=>{
    const arquivos = caminhos.filter(e.casa);
    const status = !arquivos.length ? "ausente" : (arquivos.length > 1 && !e.varios ? "duplicado" : "presente");
    return {chave: e.chave, rotulo: e.rotulo, obrigatorio: e.obrigatorio, arquivos, status};
  });
  const sims = {};
  for (const c of caminhos){
    const partes = c.split("/"); if (partes.length < 2 || !/\.html?$/i.test(c)) continue;
    const m = partes[partes.length - 2].match(RE_OBJ); if (!m) continue;
    const obj = m[1].toUpperCase(); (sims[obj] = sims[obj] || []).push(c);
  }
  itens.push(...Object.keys(sims).sort().map(obj=>({chave: "sim:" + obj, rotulo: `Cartão SIM · objeto ${obj}`, obrigatorio: false,
    arquivos: sims[obj], status: sims[obj].length > 1 ? "duplicado" : "presente"})));
  return {itens, qtdSims: Object.keys(sims).length, faltando: itens.filter(i=>i.obrigatorio && i.status === "ausente").map(i=>i.chave)};
}
teste("inventário do caso 001: completo, 2 SIMs", ()=>{
  const r = inventariar(["Requisicao.pdf", "Requisicao-digitalizada.pdf", "DEVICE INFO.txt", "HASHDOHASH.txt", "OBJ 01-A/SIM.html", "OBJ 01-B/SIM.html", "GABARITO.json"]);
  return r.faltando.length === 0 && r.qtdSims === 2;
});
teste("inventário do caso 003: falta o hash (RN02)", ()=> inventariar(["Requisicao.pdf", "DEVICE INFO.txt", "OBJ 01-A/SIM.html"]).faltando.join() === "hash");
teste("inventário: dois DEVICE INFO.txt é duplicado", ()=> inventariar(["DEVICE INFO.txt", "copia/DEVICE INFO.txt"]).itens.find(i=>i.chave === "device").status === "duplicado");
teste("caso sem SIM não é erro (RN06)", ()=> inventariar(["Requisicao.pdf", "DEVICE INFO.txt", "HASHDOHASH.txt"]).faltando.length === 0);

async function lerPastaPorHandle(handle, prefixo=""){
  const out = [];
  for await (const [nome, h] of handle.entries()){
    if (h.kind === "file") out.push({caminho: prefixo + nome, file: await h.getFile()});
    else out.push(...await lerPastaPorHandle(h, prefixo + nome + "/"));
  }
  return out;
}
// webkitRelativePath começa pelo nome da pasta escolhida; tira esse primeiro trecho
const lerPastaPorInput = files => Array.from(files).map(f=>({caminho: f.webkitRelativePath.split("/").slice(1).join("/") || f.name, file: f}));

const SELO = {presente: "ok", ausente: "erro", duplicado: "alerta"};
TELAS["#/arquivos"] = async ()=>{
  let caso = await casoAtual();
  const inv = caso?.inventario;
  return `<h1>Pasta do caso</h1><p class="sub">${caso ? `Caso ${esc(caso.numero_protocolo || "(sem protocolo)")}` : "Nenhum caso aberto: a pasta escolhida cria um caso novo."}
    A pasta é aberta só para leitura (os originais não mudam).</p>
    <div class="card"><div class="linha-botoes" style="margin-top:0">
      ${window.showDirectoryPicker ? `<button class="prim" id="btnPasta">Selecionar pasta do caso</button>` : ""}
      <label class="botao">${window.showDirectoryPicker ? "Ou escolher pelo seletor do sistema" : "Selecionar pasta do caso"}
        <input type="file" id="inpPasta" webkitdirectory multiple hidden></label></div>
      ${caso?.pasta_nome ? `<p class="sub">Pasta: <b>${esc(caso.pasta_nome)}</b> · lida em ${esc(dataBR(caso.inventariado_em))}
        ${arquivosDaSessao.size ? "" : " · selecione de novo para os extratores lerem os arquivos"}</p>` : ""}</div>
    ${inv ? `<div class="card tabela-wrap"><h2 style="margin-top:0">Inventário</h2><table><tr><th>Arquivo</th><th>Situação</th><th>Encontrado</th><th></th></tr>
      ${inv.itens.map(i=>`<tr><td>${esc(i.rotulo)}${i.obrigatorio ? " *" : ""}</td><td><span class="selo ${SELO[i.status]}">${i.status}</span></td>
        <td class="mono">${i.arquivos.map(esc).join("<br>") || "—"}</td>
        <td>${i.obrigatorio && i.status === "ausente" ? `<label style="display:inline-flex;gap:6px"><input type="checkbox" data-manual="${i.chave}" style="width:auto"
          ${(caso.informar_manual || []).includes(i.chave) ? "checked" : ""}> informar manualmente</label>` : ""}</td></tr>`).join("")}
      ${inv.qtdSims ? "" : `<tr><td>Cartão SIM</td><td><span class="selo info">nenhum</span></td><td colspan="2">Aparelho sem SIM: a descrição dos objetos registra isso (RN06).</td></tr>`}
      </table><p class="sub">* obrigatório (RN02)</p>
      <div id="avisoAvancar"></div>
      <div class="linha-botoes"><button class="prim" id="btnAvancar">Avançar para a extração dos dados</button></div></div>` : ""}`;
};
TELAS_DEPOIS["#/arquivos"] = ()=>{
  const processar = async (lista, nomePasta, handle)=>{
    arquivosDaSessao.clear(); lista.forEach(x=>arquivosDaSessao.set(x.caminho, x.file));
    let caso = await casoAtual();
    if (!caso){ caso = {id_caso: uuid(), numero_protocolo: "", status: "em elaboração", criado_em: agora()}; await db.meta("caso_atual", caso.id_caso); }
    const inv = inventariar(lista.map(x=>x.caminho));
    caso = {...caso, pasta_nome: nomePasta, inventario: inv, inventariado_em: agora(), informar_manual: [], inicio_em: caso.inicio_em || agora()};
    if (handle) caso.pasta_handle = handle;  // o handle volta numa próxima sessão, com nova permissão
    await db.put("casos", caso);
    await registrar("pasta inventariada", {id_caso: caso.id_caso, campo_verificado: "inventário", resultado: inv.faltando.length ? "faltando: " + inv.faltando.join(", ") : "completo"});
    navegar();
  };
  $("#btnPasta")?.addEventListener("click", async ()=>{
    try { const h = await window.showDirectoryPicker({mode: "read"}); await processar(await lerPastaPorHandle(h), h.name, h); }
    catch(e){ if (e.name !== "AbortError") toast("Não consegui abrir a pasta: " + e.message, 5000); }
  });
  $("#inpPasta").addEventListener("change", async e=>{
    const files = e.target.files; if (!files.length) return;
    await processar(lerPastaPorInput(files), files[0].webkitRelativePath.split("/")[0] || "pasta", null);
  });
  $$("[data-manual]").forEach(cb=>cb.addEventListener("change", async ()=>{
    const caso = await casoAtual();
    caso.informar_manual = $$("[data-manual]").filter(x=>x.checked).map(x=>x.dataset.manual);
    await db.put("casos", caso);
  }));
  $("#btnAvancar")?.addEventListener("click", async ()=>{
    const caso = await casoAtual(), pend = caso.inventario.faltando.filter(c=>!(caso.informar_manual || []).includes(c));
    if (pend.length){
      const nomes = pend.map(c=>ESPERADOS.find(e=>e.chave === c).rotulo);
      return mostrarErros("#avisoAvancar", [`Falta ${nomes.join(", ")}. Coloque o arquivo na pasta e selecione de novo, ou marque "informar manualmente" (RN02).`]);
    }
    await registrar("avançou para a extração", {id_caso: caso.id_caso, observacao: (caso.informar_manual || []).length ? "informar manualmente: " + caso.informar_manual.join(", ") : ""});
    location.hash = "#/dados";
  });
};
