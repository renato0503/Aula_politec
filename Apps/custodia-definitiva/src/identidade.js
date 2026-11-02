/* Identidade da Custódia Definitiva.
   Entra por último no build. A tela-assinatura é o balcão de leitura do lacre
   com o mapa das prateleiras; o painel do gestor fica só para o gestor. */

function cdBalcao(){
  return `<div class="card cd-balcao">
    <div class="cd-balcao-rot"><span class="cd-ponto" aria-hidden="true"></span> Balcão de leitura do lacre</div>
    <div class="cd-balcao-linha">
      <input id="cdLacreRapido" type="search" autocomplete="off" autofocus placeholder="Aponte o leitor ou digite o lacre. Ex.: LC-20260001" aria-label="Ler o lacre">
      <button class="prim" type="button" id="btnCdLacreRapido">Abrir a ficha</button></div>
    <div id="cdLacreMsg"></div>
    <p class="sub" style="margin:0">Enter abre o vestígio; lacre não encontrado avisa na hora.</p></div>`;
}
function cdLigarBalcao(){
  const ir = async ()=>{
    const q = valorDe("cdLacreRapido");
    if (!q) return mostrarErros("#cdLacreMsg", ["Digite ou leia o lacre."]);
    const vs = await db.list("vestigios"), n = normalizar(q);
    const v = vs.find(x=>normalizar(x.lacre) === n) || vs.find(x=>normalizar(x.lacre).includes(n));
    if (v) return location.hash = "#/vestigio/" + encodeURIComponent(v.id_vestigio);
    mostrarErros("#cdLacreMsg", [`Lacre ${q} não encontrado no acervo.`]);
  };
  $("#btnCdLacreRapido")?.addEventListener("click", ir);
  $("#cdLacreRapido")?.addEventListener("keydown", e=>{ if (e.key === "Enter"){ e.preventDefault(); ir(); } });
}
function cdMapaPrateleiras(vs, cs, cats){
  return `<div class="card" id="cdMapa"><h2 style="margin-top:0">Mapa das prateleiras</h2>
    <p class="sub">Cada prateleira é um contêiner. A barra mostra a ocupação; clique para ver os vestígios dele.</p>
    <div class="cd-prateleiras">${cs.map(c=>{
      const o = cdOcupados(vs, c.id_conteiner), cap = Number(c.capacidade) || 0, pct = cap ? Math.round(o / cap * 100) : 0;
      const cls = cdSemaforo(pct);
      return `<a class="cd-prateleira ${cls}" href="#/vestigios" data-cd-cont="${esc(c.id_conteiner)}">
        <span class="cd-prateleira-topo"><b class="mono">${esc(c.id_conteiner)}</b><span class="selo ${cls}">${pct}%</span></span>
        <span class="sub">${esc(cats[c.categoria_permitida]?.nome || (c.categoria_permitida === "todas" ? "todas as categorias" : c.categoria_permitida))}</span>
        <span class="barra ${cls}"><i style="width:${Math.min(100, pct)}%"></i></span>
        <span class="sub">${o} de ${cap} · folga ${Math.max(0, cap - o)}</span></a>`;
    }).join("")}</div></div>`;
}

const cdPainelAntes = TELAS["#/painel"];
TELAS["#/painel"] = async ()=>{
  let html = await cdPainelAntes();
  const [vs, cs, cats] = await Promise.all([db.list("vestigios"), db.list("conteineres"), cdCategorias()]);
  const doc = new DOMParser().parseFromString(`<div id="cdRaiz">${html}</div>`, "text/html");
  const raiz = doc.getElementById("cdRaiz");
  if (!raiz) return html;
  if (estado.perfil !== "gestor") doc.getElementById("cdGestor")?.remove();
  const balcao = doc.createElement("div"); balcao.innerHTML = cdBalcao();
  const h1 = raiz.querySelector("h1");
  raiz.insertBefore(balcao.firstElementChild, h1);
  const mapa = doc.createElement("div"); mapa.innerHTML = cdMapaPrateleiras(vs, cs, cats);
  const tabela = doc.getElementById("tabelaOcupacao")?.closest(".card");
  if (tabela) tabela.parentNode.insertBefore(mapa.firstElementChild, tabela);
  else raiz.appendChild(mapa.firstElementChild);
  return raiz.innerHTML;
};
const cdPainelDepoisAntes = TELAS_DEPOIS["#/painel"];
TELAS_DEPOIS["#/painel"] = async ()=>{
  await cdPainelDepoisAntes?.();
  cdLigarBalcao();
  $$("[data-cd-cont]").forEach(a=>a.addEventListener("click", e=>{
    e.preventDefault(); estado.cdFiltros = {...cdFiltros(), conteiner: a.dataset.cdCont}; location.hash = "#/vestigios";
  }));
};

const cdVestigiosAntes = TELAS["#/vestigios"], cdVestigiosDepoisAntes = TELAS_DEPOIS["#/vestigios"];
TELAS["#/vestigios"] = async (p)=>{
  const html = await cdVestigiosAntes(p);
  return html.replace(/<h1>/, cdBalcao() + "<h1>");
};
TELAS_DEPOIS["#/vestigios"] = async (p)=>{
  await cdVestigiosDepoisAntes(p);
  cdLigarBalcao();
};
