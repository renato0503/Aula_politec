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

/* a lista de casos vira cartões com o passo em que o perito parou */
const agInicioAntes = TELAS["#/inicio"];
TELAS["#/inicio"] = async (p)=>{
  const html = await agInicioAntes(p);
  const casos = await db.list("casos");
  const doc = new DOMParser().parseFromString(`<div id="agRaiz">${html}</div>`, "text/html");
  const raiz = doc.getElementById("agRaiz");
  if (!raiz) return html;
  const exemplo = doc.createElement("div"); exemplo.className = "card";
  exemplo.innerHTML = `<h2 style="margin-top:0">Caso de exemplo</h2>
    <p class="sub">Carrega um caso com a pasta fictícia do caso 001, sem precisar escolher arquivos. Os extratores continuam exigindo a pasta real.</p>
    <button class="prim" type="button" id="btnCasoExemplo">Carregar caso de exemplo</button>`;
  const primeira = [...raiz.children].find(n=>n.classList?.contains("card"));
  raiz.insertBefore(exemplo, primeira || null);
  if (casos.length){
    const tabela = [...raiz.querySelectorAll("table")][0];
    const cards = doc.createElement("div"); cards.className = "ag-casos";
    cards.innerHTML = casos.map(c=>`<a class="card ag-caso" href="#/arquivos" data-ag-caso="${esc(c.id)}">
      <span class="mono">${esc(c.numero_protocolo || c.id_caso || c.id)}</span>
      <b>${esc(c.aparelho?.marca || c.nome || "Caso sem aparelho identificado")}</b>
      <span class="sub">${c.inicio_em ? "aberto em " + dataBR(c.inicio_em) : "sem cronômetro"}</span></a>`).join("");
    if (tabela) tabela.closest(".card")?.replaceWith(cards); else raiz.insertBefore(cards, raiz.querySelector("h1")?.nextSibling);
  }
  return raiz.innerHTML;
};
const agInicioDepoisAntes = TELAS_DEPOIS["#/inicio"];
TELAS_DEPOIS["#/inicio"] = async ()=>{
  await agInicioDepoisAntes?.();
  $("#btnCasoExemplo")?.addEventListener("click", async ()=>{
    const caso = {id_caso: uuid(), numero_protocolo: "EXEMPLO-001", status: "em elaboração", inicio_em: null, fim_em: null, criado_em: agora(),
      pasta_nome: "caso-ficticio-001", inventariado_em: agora(), informar_manual: [],
      inventario: inventariar(["Requisicao.pdf", "Requisicao-digitalizada.pdf", "DEVICE INFO.txt", "HASHDOHASH.txt", "OBJ 01-A/SIM.html", "OBJ 01-B/SIM.html"])};
    await db.put("casos", caso); await db.meta("caso_atual", caso.id_caso);
    await registrar("caso de exemplo carregado", {id_caso: caso.id_caso});
    location.hash = "#/arquivos";
  });
  $$("[data-ag-caso]").forEach(a=>a.addEventListener("click", async e=>{
    e.preventDefault(); await db.meta("caso_atual", a.dataset.agCaso); location.hash = "#/arquivos";
  }));
};
