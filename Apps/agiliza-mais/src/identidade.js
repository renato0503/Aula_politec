/* Identidade do Agiliza +.
   Entra por último no build. A tela-assinatura é a bancada do caso: os passos
   ficam à esquerda e o trabalho à direita; o menu fica com quatro itens. */

const AG_PASSOS = [["#/arquivos", "Pasta do caso"], ["#/dados", "Conferência"], ["#/textos", "Textos"],
  ["#/quesitos", "Quesitos"], ["#/gerar", "Gerar laudo"], ["#/revisao", "Revisão final"]];
async function agBancada(atual, html){
  const id = await db.meta("caso_atual");
  const caso = id ? await db.get("casos", id) : null;
  const indice = AG_PASSOS.findIndex(([r])=>r === atual);
  const rail = `<aside class="ag-rail"><a class="ag-voltar" href="#/inicio">← Casos</a>
    <p class="sub">${caso ? esc(caso.protocolo || caso.id) : "sem caso aberto"}</p>
    <ol>${AG_PASSOS.map(([rota, nome], i)=>{
      const pronta = typeof TELAS[rota] === "function";
      const cls = i < indice ? "feito" : i === indice ? "atual" : "";
      return `<li class="${cls} ${pronta ? "" : "pendente"}">${pronta ? `<a href="${rota}"><span class="n">${i + 1}</span><span>${nome}</span></a>`
        : `<span class="em-breve"><span class="n">${i + 1}</span><span>${nome} · em breve</span></span>`}</li>`;
    }).join("")}</ol></aside>`;
  return `<div class="ag-bancada">${rail}<div class="ag-trabalho">${html}</div></div>`;
}
for (const [rota] of AG_PASSOS){
  const antes = TELAS[rota];
  if (typeof antes !== "function") continue;
  TELAS[rota] = async (p)=>agBancada(rota, await antes(p));
}

/* a lista de casos vira cartões com o passo em que o perito parou,
   filtro por pasta e as ações de continuar, renomear, mover e excluir */
function agDialogo({titulo, html, rotuloOk, aoConfirmar}){
  const dlg = document.createElement("dialog"); dlg.className = "ag-dialog";
  dlg.innerHTML = `<form method="dialog" class="ag-dialog-form"><h2>${esc(titulo)}</h2>
    <div class="ag-dialog-corpo">${html}</div>
    <div class="linha-botoes"><button type="submit" class="prim" value="ok">${esc(rotuloOk || "Salvar")}</button>
      <button type="button" class="sec" data-fechar>Cancelar</button></div></form>`;
  document.body.appendChild(dlg);
  const fechar = ()=>dlg.remove();
  dlg.querySelector("[data-fechar]").addEventListener("click", fechar);
  dlg.addEventListener("cancel", e=>{ e.preventDefault(); fechar(); });
  dlg.querySelector("form").addEventListener("submit", async e=>{
    e.preventDefault();
    try { await aoConfirmar(dlg); dlg.remove(); }
    catch(err){ alert(err.message); }
  });
  dlg.showModal();
  dlg.querySelector("input, select")?.focus();
  return dlg;
}
const agCasoRota = c => c.inventario ? "#/dados" : "#/arquivos";

const agInicioAntes = TELAS["#/inicio"];
TELAS["#/inicio"] = async (p)=>{
  const html = await agInicioAntes(p);
  const casos = await db.list("casos"), pastas = await agPastas();
  const doc = new DOMParser().parseFromString(`<div id="agRaiz">${html}</div>`, "text/html");
  const raiz = doc.getElementById("agRaiz");
  if (!raiz) return html;
  const exemplo = doc.createElement("div"); exemplo.className = "card";
  exemplo.innerHTML = `<h2 style="margin-top:0">Caso de exemplo</h2>
    <p class="sub">Carrega o caso fictício 001 (requisição em PDF, DEVICE INFO, hash e dois SIMs) sem precisar escolher a pasta.</p>
    <button class="prim" type="button" id="btnCasoExemplo">Carregar caso de exemplo</button>`;
  const primeira = [...raiz.children].find(n=>n.classList?.contains("card"));
  raiz.insertBefore(exemplo, primeira || null);
  if (casos.length){
    const tabela = [...raiz.querySelectorAll("table")][0];
    const filtro = estado.agPasta || "";
    const vis = casos.filter(c=>!filtro || agPasta(c) === filtro)
      .sort((a, b)=>String(b.inicio_em || "").localeCompare(String(a.inicio_em || "")));
    const conta = p => casos.filter(c=>!p || agPasta(c) === p).length;
    const bloco = doc.createElement("div"); bloco.className = "ag-casos-bloco";
    bloco.innerHTML = `<div class="chips ag-pastas" role="group" aria-label="Pastas dos casos">
      <button type="button" class="${filtro === "" ? "prim" : ""}" data-ag-pasta="">Todas (${casos.length})</button>
      ${pastas.map(p=>`<button type="button" class="${filtro === p ? "prim" : ""}" data-ag-pasta="${esc(p)}">${esc(p)} (${conta(p)})</button>`).join("")}
      <button type="button" class="sec" data-ag-nova-pasta>+ Nova pasta</button></div>
      <div class="ag-casos">${vis.map(c=>`<div class="card ag-caso" data-ag-card="${esc(c.id_caso)}">
        <div class="ag-caso-topo"><span class="mono">${esc(c.numero_protocolo || c.id_caso)}</span><span class="selo info">${esc(c.status || "em elaboração")}</span></div>
        <b>${esc(agTituloCaso(c))}</b>
        <span class="sub">${esc(agPasta(c))}${c.pasta_nome && c.pasta_nome !== agPasta(c) ? " · " + esc(c.pasta_nome) : ""} · ${c.inicio_em ? "aberto em " + dataBR(c.inicio_em) : "sem cronômetro"}</span>
        <div class="linha-botoes ag-caso-acoes">
          <button type="button" class="prim" data-ag-abrir="${esc(c.id_caso)}">Continuar</button>
          <button type="button" data-ag-renomear="${esc(c.id_caso)}">Renomear</button>
          <button type="button" data-ag-mover="${esc(c.id_caso)}">Pasta</button>
          <button type="button" class="perigo" data-ag-excluir="${esc(c.id_caso)}">Excluir</button></div></div>`).join("")
        || '<div class="card vazio">Nenhum caso nesta pasta.</div>'}</div>`;
    if (tabela) tabela.closest(".card")?.replaceWith(bloco); else raiz.appendChild(bloco);
  }
  return raiz.innerHTML;
};
const agInicioDepoisAntes = TELAS_DEPOIS["#/inicio"];
TELAS_DEPOIS["#/inicio"] = async ()=>{
  await agInicioDepoisAntes?.();
  $("#btnCasoExemplo")?.addEventListener("click", async ()=>{
    // os arquivos do caso fictício 001 vão embutidos (exemplos/caso-exemplo.json): os extratores leem como se a pasta tivesse sido escolhida
    const pacote = dadosEmbutidos("caso-exemplo");
    arquivosDaSessao.clear();
    for (const a of pacote?.arquivos || []){
      const bytes = Uint8Array.from(atob(a.b64), ch=> ch.charCodeAt(0));
      arquivosDaSessao.set(a.caminho, new File([bytes], a.caminho.split("/").pop()));
    }
    const caminhos = arquivosDaSessao.size ? [...arquivosDaSessao.keys()]
      : ["Requisicao.pdf", "Requisicao-digitalizada.pdf", "DEVICE INFO.txt", "HASHDOHASH.txt", "OBJ 01-A/SIM.html", "OBJ 01-B/SIM.html"];
    const caso = {id_caso: uuid(), numero_protocolo: "EXEMPLO-001", status: "em elaboração", inicio_em: agora(), fim_em: null, criado_em: agora(),
      pasta: "Sem pasta", pasta_nome: pacote?.pasta || "caso-ficticio-001", inventariado_em: agora(), informar_manual: [], inventario: inventariar(caminhos)};
    await db.put("casos", caso); await db.meta("caso_atual", caso.id_caso);
    await registrar("caso de exemplo carregado", {id_caso: caso.id_caso});
    location.hash = "#/arquivos";
  });
  $$("[data-ag-pasta]").forEach(b=>b.addEventListener("click", ()=>{ estado.agPasta = b.dataset.agPasta; navegar(); }));
  $("[data-ag-nova-pasta]")?.addEventListener("click", ()=>agDialogo({
    titulo: "Nova pasta", rotuloOk: "Criar pasta",
    html: `<label for="agNovaPasta">Nome da pasta</label><input id="agNovaPasta" maxlength="40" required placeholder="Ex.: 2026-10">`,
    aoConfirmar: async dlg=>{
      const nome = dlg.querySelector("#agNovaPasta").value.trim();
      if (!nome) throw new Error("Informe o nome da pasta.");
      const ps = await agPastas(); if (!ps.includes(nome)){ ps.push(nome); await db.meta("ag_pastas", ps); }
      estado.agPasta = nome; await registrar("pasta criada", {observacao: nome}); await navegar();
    }
  }));
  $$("[data-ag-abrir]").forEach(b=>b.addEventListener("click", async ()=>{
    const c = await db.get("casos", b.dataset.agAbrir); if (!c) return;
    await db.meta("caso_atual", c.id_caso); location.hash = agCasoRota(c);
  }));
  $$("[data-ag-renomear]").forEach(b=>b.addEventListener("click", async ()=>{
    const c = await db.get("casos", b.dataset.agRenomear); if (!c) return;
    agDialogo({titulo: "Renomear o caso", rotuloOk: "Salvar nome",
      html: `<label for="agNomeCaso">Nome do caso</label><input id="agNomeCaso" maxlength="80" value="${esc(agTituloCaso(c))}">
        <p class="sub">O protocolo continua no cadastro; este nome é o apelido que aparece na lista.</p>`,
      aoConfirmar: async dlg=>{
        const nome = dlg.querySelector("#agNomeCaso").value.trim();
        if (!nome) throw new Error("Informe o nome do caso.");
        await db.put("casos", {...c, nome}); await registrar("caso renomeado", {id_caso: c.id_caso, observacao: nome}); await navegar();
      }});
  }));
  $$("[data-ag-mover]").forEach(b=>b.addEventListener("click", async ()=>{
    const c = await db.get("casos", b.dataset.agMover); if (!c) return;
    const ps = await agPastas(), atual = agPasta(c);
    agDialogo({titulo: "Mover para uma pasta", rotuloOk: "Mover",
      html: `<label for="agMoverPasta">Pasta</label><select id="agMoverPasta">${ps.map(p=>`<option value="${esc(p)}" ${p === atual ? "selected" : ""}>${esc(p)}</option>`).join("")}</select>
        <label for="agMoverNova">Ou criar uma pasta nova</label><input id="agMoverNova" maxlength="40" placeholder="Deixe vazio para usar a pasta escolhida">`,
      aoConfirmar: async dlg=>{
        let pasta = dlg.querySelector("#agMoverPasta").value;
        const nova = dlg.querySelector("#agMoverNova").value.trim();
        if (nova){ pasta = nova; const lista = await agPastas(); if (!lista.includes(nova)){ lista.push(nova); await db.meta("ag_pastas", lista); } }
        await db.put("casos", {...c, pasta}); await registrar("caso movido de pasta", {id_caso: c.id_caso, observacao: pasta}); await navegar();
      }});
  }));
  $$("[data-ag-excluir]").forEach(b=>b.addEventListener("click", async ()=>{
    const c = await db.get("casos", b.dataset.agExcluir); if (!c) return;
    agDialogo({titulo: "Excluir o caso", rotuloOk: "Excluir",
      html: `<p>Tem certeza de que quer excluir <b>${esc(agTituloCaso(c))}</b>?</p>
        <p class="sub">Os dados do caso, a conferência, os quesitos e os laudos gerados neste navegador são apagados. Os arquivos originais da pasta não mudam.</p>`,
      aoConfirmar: async ()=>{ await agExcluirCaso(c.id_caso); await navegar(); }});
  }));
};
