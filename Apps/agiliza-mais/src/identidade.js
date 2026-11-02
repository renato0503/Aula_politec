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
    <ol>${AG_PASSOS.map(([rota, nome], i)=>`<li class="${i < indice ? "feito" : i === indice ? "atual" : ""}">
      <a href="${rota}"><span class="n">${i + 1}</span><span>${nome}</span></a></li>`).join("")}</ol></aside>`;
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
  if (!casos.length) return html;
  const doc = new DOMParser().parseFromString(`<div id="agRaiz">${html}</div>`, "text/html");
  const raiz = doc.getElementById("agRaiz");
  if (!raiz) return html;
  const tabela = [...raiz.querySelectorAll("table")][0];
  const cards = doc.createElement("div"); cards.className = "ag-casos";
  cards.innerHTML = casos.map(c=>`<a class="card ag-caso" href="#/arquivos" data-ag-caso="${esc(c.id)}">
    <span class="mono">${esc(c.protocolo || c.id)}</span>
    <b>${esc(c.aparelho?.marca || c.nome || "Caso sem aparelho identificado")}</b>
    <span class="sub">${c.inicio_em ? "aberto em " + dataBR(c.inicio_em) : "sem cronômetro"}</span></a>`).join("");
  if (tabela) tabela.closest(".card")?.replaceWith(cards); else raiz.insertBefore(cards, raiz.querySelector("h1")?.nextSibling);
  return raiz.innerHTML;
};
const agInicioDepoisAntes = TELAS_DEPOIS["#/inicio"];
TELAS_DEPOIS["#/inicio"] = async ()=>{
  await agInicioDepoisAntes?.();
  $$("[data-ag-caso]").forEach(a=>a.addEventListener("click", async e=>{
    e.preventDefault(); await db.meta("caso_atual", a.dataset.agCaso); location.hash = "#/arquivos";
  }));
};
