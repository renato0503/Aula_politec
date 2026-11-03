/* Identidade do Passivo Ambiental.
   Entra por último no build. A tela-assinatura é a fila de laudos do perito,
   com prazo e miniatura do mapa; o painel do perito não mostra o bloco do
   gestor, e o laudo vira abas. */

function paMiniMapa(req){
  const pin = req.coordenadas ? '<circle cx="40" cy="27" r="4" class="pa-pin"/><circle cx="40" cy="27" r="9" class="pa-pin-halo"/>' : "";
  return `<svg class="pa-mini" viewBox="0 0 80 56" role="img" aria-label="Miniatura do mapa do laudo">
    <rect x="1" y="1" width="78" height="54" rx="6" class="pa-mini-fundo"/>
    <path d="M6 40c10-8 18-6 26-13s16-9 24-5 12 10 18 9" class="pa-curva"/>
    <path d="M4 28c9-5 16-3 23-8s15-7 22-4 14 8 22 6" class="pa-curva"/>
    <path d="M10 50c8-4 15-3 22-7s13-6 20-3 14 6 22 5" class="pa-curva"/>
    ${pin}</svg>`;
}
async function paFilaPerito(){
  const [rs, ls] = await Promise.all([db.list("requisicoes"), db.list("laudos")]);
  const hoje = hojeISO();
  const laudoDe = rid => ls.find(l=>l.requisicao_id === rid);
  const busca = normalizar(estado.paBusca || "");
  const fila = rs.filter(r=>r.status !== "concluida").map(r=>{
    const dias = Math.round((new Date(hoje + "T12:00:00") - new Date(r.data_requisicao + "T12:00:00")) / 86400000);
    return {...r, restam: Number(r.prazo_dias) - dias, l: laudoDe(r.id_requisicao)};
  }).filter(r=>!estado.paSoAtrasados || r.restam < 0)
    .filter(r=>!busca || normalizar(`${r.numero_processo} ${r.local} ${r.tipo_infracao} ${r.orgao}`).includes(busca))
    .sort((a, b)=>a.restam - b.restam);
  return `<div class="card pa-fila"><div class="pa-fila-topo"><div><span class="sub">Minha fila</span>
      <h2>Laudos por prazo <span class="conta">${fila.length}</span></h2></div><a class="botao" href="#/requisicoes">Ver todas</a></div>
    <p class="sub">Ordenada pelo prazo. O mapa é a miniatura do laudo; clique para abrir.</p>
    <div class="card pa-filtro"><div class="campos">${campo("paBuscaFila", "Buscar por número, local, tipo ou órgão", {valor: estado.paBusca || "", attrs: 'autocomplete="off"'})}
      <label style="display:flex;gap:8px;align-items:center;margin-top:10px"><input type="checkbox" id="paSoAtrasados" style="width:auto" ${estado.paSoAtrasados ? "checked" : ""}> só atrasados</label></div></div>
    ${fila.length ? `<div class="pa-fila-lista">${fila.map(r=>{
      const cls = r.restam < 0 ? "erro" : r.restam <= 3 ? "alerta" : "ok";
      return `<a class="pa-fila-item" href="#/laudo/${encodeURIComponent(r.id_requisicao)}">
        ${paMiniMapa(r)}
        <span class="pa-fila-info"><b class="mono">${esc(r.numero_processo)}</b><span>${esc(r.tipo_infracao)} · ${esc(r.local)}</span>
          <small class="sub">${esc(r.orgao)}</small></span>
        <span class="pa-fila-prazo"><span class="selo ${cls}">${r.restam < 0 ? `${plural(Math.abs(r.restam), "dia", "dias")} atrasado` : `vence em ${plural(r.restam, "dia", "dias")}`}</span>
          <small class="sub">${r.l?.status || "sem laudo"}</small></span></a>`;
    }).join("")}</div>` : '<p class="sub">Nenhum laudo na fila.</p>'}</div>`;
}

const paPainelAntes = TELAS["#/painel"];
TELAS["#/painel"] = async ()=>{
  const html = await paPainelAntes();
  const doc = new DOMParser().parseFromString(`<div id="paRaiz">${html}</div>`, "text/html");
  const raiz = doc.getElementById("paRaiz");
  if (!raiz) return html;
  if (estado.perfil === "perito"){
    doc.getElementById("paGestor")?.remove();
    const bloco = doc.createElement("div"); bloco.innerHTML = await paFilaPerito();
    raiz.insertBefore(bloco.firstElementChild, raiz.querySelector("h1"));
  }
  return raiz.innerHTML;
};

/* ---------- laudo em abas ---------- */
const paLaudoAntes = TELAS["#/laudo/:id"];
TELAS["#/laudo/:id"] = async (p)=>{
  const html = await paLaudoAntes(p);
  if (typeof abas !== "function" || html.includes('class="abas"')) return html;
  const doc = new DOMParser().parseFromString(`<div id="paLaudoRaiz">${html}</div>`, "text/html");
  const raiz = doc.getElementById("paLaudoRaiz");
  if (!raiz) return html;
  const antes = [], cards = [];
  const colher = node=>{
    if (node.nodeType !== 1) return;
    if (node.classList.contains("duas-colunas")){ [...node.children].forEach(colher); return; }
    if (node.classList.contains("card") && !node.classList.contains("kpi")) cards.push(node);
    else antes.push(node);
  };
  [...raiz.children].forEach(colher);
  if (!cards.length) return html;
  const grupos = {cabecalho: [], mapas: [], conclusao: [], assinatura: []};
  const destino = h=>{
    if (/mapa/.test(h)) return "mapas";
    if (/conclus/.test(h)) return "conclusao";
    if (/assinatura/.test(h)) return "assinatura";
    return "cabecalho";
  };
  cards.forEach(node=>{
    const fixo = {paCardMapa: "mapas", paCardConclusao: "conclusao", paAssinatura: "assinatura"}[node.id];
    grupos[fixo || destino((node.querySelector("h2")?.textContent || "").toLowerCase())].push(node.outerHTML);
  });
  const nomes = [["cabecalho", "Cabeçalho"], ["mapas", "Mapas"], ["conclusao", "Conclusão"], ["assinatura", "Assinatura"]];
  const lista = nomes.filter(([id])=>grupos[id].length).map(([id, titulo])=>({id, titulo, html: grupos[id].join("")}));
  return antes.map(n=>n.outerHTML).join("") + abas("ficha", lista);
};

const paPainelDepoisAntes = TELAS_DEPOIS["#/painel"];
TELAS_DEPOIS["#/painel"] = async ()=>{
  await paPainelDepoisAntes?.();
  let t = null;
  $("#paBuscaFila")?.addEventListener("input", e=>{
    clearTimeout(t); const v = e.target.value;
    t = setTimeout(()=>{ estado.paBusca = v; navegar(); }, 350);
  });
  $("#paSoAtrasados")?.addEventListener("change", e=>{ estado.paSoAtrasados = e.target.checked; navegar(); });
};
