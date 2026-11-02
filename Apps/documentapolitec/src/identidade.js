/* Identidade do DOCUMENTAPOLITEC.
   Entra por último no build. A tela-assinatura é a estante de caixas com a
   conferência por leitura sequencial; a ficha da caixa vira abas e o menu cai
   de oito para cinco itens. */

TELAS["#/caixas"] = async ()=>{
  const cs = (await db.list("caixas")).sort((a, b)=>String(a.id_caixa).localeCompare(String(b.id_caixa)));
  const ps = await db.list("prontuarios");
  const conferidas = cs.filter(c=>c.status === "conferida").length;
  return `<h1>Estante de caixas</h1>
    <p class="sub">${cs.length} caixas · ${conferidas} conferidas. Cada lombada é uma caixa; clique para abrir. <a class="doc-nova" href="#/caixa/nova">＋ Nova caixa</a></p>
    <div class="doc-estante">${cs.map(c=>{
      const lista = ps.filter(p=>p.caixa_id === c.id_caixa), ok = lista.filter(p=>p.conferido).length;
      const pct = lista.length ? Math.round(ok / lista.length * 100) : 0;
      const cls = c.status === "conferida" ? "ok" : c.status === "divergencia" ? "erro" : "alerta";
      return `<a class="doc-lombada ${cls}" href="#/caixa/${encodeURIComponent(c.id_caixa)}">
        <span class="doc-lombada-cod">${esc(c.id_caixa)}</span>
        <span class="doc-lombada-setor">${esc(c.setor_origem)}</span>
        <span class="doc-lombada-selo selo ${cls}" title="${esc(DOC_STATUS[c.status] || c.status)}">${c.status === "conferida" ? "Conferida" : c.status === "divergencia" ? "Divergência" : "Pendente"}</span>
        <span class="barra ${cls}"><i style="width:${pct}%"></i></span>
        <span class="doc-lombada-conta">${ok} de ${lista.length} conferidos</span></a>`;
    }).join("") || '<div class="card vazio">Nenhuma caixa cadastrada. <a href="#/caixa/nova">Cadastrar caixa</a></div>'}</div>`;
};

/* atalhos que saíram do menu: nova caixa, relatório da importação e busca por nome */
function docAtalhos(itens){
  return `<p class="doc-atalhos">${itens.map(([href, rot])=>`<a href="${href}">${rot}</a>`).join(" · ")}</p>`;
}
const docBuscaAntes = TELAS["#/busca"];
TELAS["#/busca"] = async (p)=>{
  const html = await docBuscaAntes(p);
  const extra = estado.perfil === "gestor" ? docAtalhos([["#/busca-nome", "Busca por nome (gestor)"]]) : "";
  return html.replace(/<h1>/, extra + "<h1>");
};
const docImportarAntes = TELAS["#/importar"];
TELAS["#/importar"] = async (p)=>{
  const html = await docImportarAntes(p);
  return html + docAtalhos([["#/relatorio-importacao", "Ver o relatório da última importação"]]);
};

/* ---------- ficha da caixa: conferência por leitura e abas ---------- */
function docLigarLeituraPront(id){
  const ir = async ()=>{
    const q = valorDe("docLeituraPront").replace(/\s+/g, "");
    if (!q) return;
    const ps = await db.porIndice("prontuarios", "caixa_id", id);
    const p = ps.find(x=>String(x.numero) === q);
    if (!p) return mostrarErros("#docErrosLeituraPront", [`Prontuário ${q} não está na relação desta caixa.`]);
    await db.put("prontuarios", {...p, conferido: true});
    await db.put("log", {id: uuid(), caixa_id: id, acao: "prontuário conferido por leitura", perfil: estado.perfil || "", data_hora: agora(), detalhe: q});
    if (!p.digital) toast(`Prontuário ${q} sem correspondência no arquivo digital.`, 5000);
    else toast(`Prontuário ${q} conferido.`);
    navegar();
  };
  $("#btnDocLeituraPront")?.addEventListener("click", ir);
  $("#docLeituraPront")?.addEventListener("keydown", e=>{ if (e.key === "Enter"){ e.preventDefault(); ir(); } });
  $("#docLeituraCod")?.addEventListener("keydown", e=>{ if (e.key === "Enter"){ e.preventDefault(); $("#btnDocLeitura")?.click(); } });
  setTimeout(()=>$("#docLeituraPront")?.focus(), 60);
}

const docFichaAntes = TELAS["#/caixa/:id"];
TELAS["#/caixa/:id"] = async (p)=>{
  const html = await docFichaAntes(p);
  if (typeof abas !== "function" || html.includes('class="abas"')) return html;
  const doc = new DOMParser().parseFromString(`<div id="docRaiz">${html}</div>`, "text/html");
  const raiz = doc.getElementById("docRaiz");
  if (!raiz) return html;
  const c = await db.get("caixas", p.id);
  if (c && c.status !== "conferida"){
    const card = doc.createElement("div");
    card.className = "card"; card.id = "docConferenciaLeitura";
    card.innerHTML = `<h2 style="margin-top:0">Conferência por leitura</h2>
      <p class="sub">Digite ou leia o número do prontuário e tecle Enter. Cada leitura marca o item da relação; número fora da relação avisa na hora.</p>
      <div class="doc-leitura"><input id="docLeituraPront" type="search" autocomplete="off" autofocus placeholder="Número do prontuário. Ex.: 2019.000001" aria-label="Número do prontuário">
        <button class="prim" type="button" id="btnDocLeituraPront">Marcar como conferido</button></div>
      <div id="docErrosLeituraPront"></div>`;
    const conf = [...raiz.children].find(n=>n.classList?.contains("card") && /conferência/i.test(n.querySelector("h2")?.textContent || ""));
    if (conf) conf.parentNode.insertBefore(card, conf.nextSibling); else raiz.appendChild(card);
  }
  const antes = [], cards = [];
  const colher = node=>{
    if (node.nodeType !== 1) return;
    if (node.classList.contains("duas-colunas")){ [...node.children].forEach(colher); return; }
    if (node.id === "docConferenciaLeitura"){ antes.push(node); return; }
    if (node.classList.contains("card") && !node.classList.contains("kpi")) cards.push(node);
    else antes.push(node);
  };
  [...raiz.children].forEach(colher);
  if (!cards.length) return html;
  const grupos = {prontuarios: [], conferencia: [], etiqueta: [], historico: []};
  const destino = h=>{
    if (/etiqueta/.test(h)) return "etiqueta";
    if (/histórico|historico/.test(h)) return "historico";
    if (/confer|leitura/.test(h)) return "conferencia";
    return "prontuarios";
  };
  cards.forEach(c2=>grupos[destino((c2.querySelector("h2")?.textContent || "").toLowerCase())].push(c2.outerHTML));
  const nomes = [["prontuarios", "Prontuários", grupos.prontuarios.length], ["conferencia", "Conferência", grupos.conferencia.length],
    ["etiqueta", "Etiqueta", grupos.etiqueta.length], ["historico", "Histórico", grupos.historico.length]];
  const lista = nomes.filter(([id])=>grupos[id].length).map(([id, titulo])=>({id, titulo, html: grupos[id].join("")}));
  return antes.map(n=>n.outerHTML).join("") + abas("ficha", lista);
};
const docFichaDepoisAntes = TELAS_DEPOIS["#/caixa/:id"];
TELAS_DEPOIS["#/caixa/:id"] = async (p)=>{
  await docFichaDepoisAntes?.(p);
  docLigarLeituraPront(p.id);
};
