/* Identidade da Distribuição de Casos de DNA.
   Entra por último no build. A tela-assinatura é a placa de 96 poços com a cor
   do perito; o perito ganha a tela “Meus casos” e a rodada fica em abas. */

const DD_CORES = ["#86198f", "#0f766e", "#b45309", "#1d4ed8", "#be123c", "#4d7c0f", "#7c3aed", "#0e7490"];
function ddCorPerito(idPerito, peritos){
  const i = peritos.findIndex(p=>p.id_perito === idPerito);
  return DD_CORES[(i < 0 ? 0 : i) % DD_CORES.length];
}
function ddPlaca(casos, peritos){
  const usados = casos.slice(0, 96);
  const porPerito = peritos.map(p=>({p, n: usados.filter(c=>c.perito_id === p.id_perito).length}));
  const wells = Array.from({length: 96}, (_, i)=>{
    const c = usados[i];
    if (!c) return '<span class="dd-poco vazio" aria-hidden="true"></span>';
    const cor = c.perito_id ? ddCorPerito(c.perito_id, peritos) : "";
    const quem = peritos.find(p=>p.id_perito === c.perito_id)?.nome || "sem perito";
    return `<button type="button" class="dd-poco ${c.perito_id ? "" : "sem"}" style="${c.perito_id ? `background:${cor}` : ""}"
      data-dd-poco="${esc(c.protocolo)}" data-dd-perito="${esc(quem)}" data-dd-tipo="${esc(c.tipo || "ordinario")}"
      title="${esc(c.protocolo)} · ${esc(quem)}${c.tipo === "cobranca" ? " · cobrança" : ""}"></button>`;
  }).join("");
  return `<div class="card dd-placa-card"><h2 style="margin-top:0">Placa de 96 poços</h2>
    <p class="sub">Cada poço é um caso da rodada, na cor do perito. Poço vazio fica cinza.</p>
    <div class="dd-placa">${wells}</div>
    <div class="dd-poco-info" id="ddPocoInfo" aria-live="polite"></div>
    <div class="dd-placa-legenda">${porPerito.map(({p, n})=>`<span><i style="background:${ddCorPerito(p.id_perito, peritos)}"></i>${esc(p.nome)} <b>${n}</b></span>`).join("")}
      ${usados.some(c=>!c.perito_id) ? '<span><i class="sem"></i>sem perito <b>' + usados.filter(c=>!c.perito_id).length + "</b></span>" : ""}</div></div>`;
}

const ddRodadaAntes = TELAS["#/rodada/:id"];
TELAS["#/rodada/:id"] = async (p)=>{
  const html = await ddRodadaAntes(p);
  const casos = await db.porIndice("casos", "rodada_id", p.id);
  const peritos = await db.list("peritos");
  const doc = new DOMParser().parseFromString(`<div id="ddRaiz">${html}</div>`, "text/html");
  const raiz = doc.getElementById("ddRaiz");
  if (!raiz) return html;
  const placa = doc.createElement("div"); placa.innerHTML = ddPlaca(casos, peritos);
  const primeiro = [...raiz.children].find(n=>n.classList?.contains("card"));
  raiz.insertBefore(placa.firstElementChild, primeiro || null);
  // abas: Distribuição · Casos · Urgências · Histórico
  const antes = [], cards = [];
  const colher = node=>{
    if (node.nodeType !== 1) return;
    if (node.id === "ddPlaca" || node.classList.contains("dd-placa-card")){ antes.push(node); return; }
    if (node.classList.contains("card") && !node.classList.contains("kpi")) cards.push(node);
    else antes.push(node);
  };
  [...raiz.children].forEach(colher);
  if (!cards.length) return raiz.innerHTML;
  const grupos = {distribuicao: [], casos: [], urgencias: [], historico: []};
  const destino = h=>{
    if (/cobran|fila/.test(h)) return "distribuicao";
    if (/urgên|urgen/.test(h)) return "urgencias";
    if (/caso/.test(h)) return "casos";
    if (/histórico|historico/.test(h)) return "historico";
    return "distribuicao";
  };
  cards.forEach(node=>grupos[destino((node.querySelector("h2")?.textContent || "").toLowerCase())].push(node.outerHTML));
  const nomes = [["distribuicao", "Distribuição"], ["casos", "Casos"], ["urgencias", "Urgências"], ["historico", "Histórico"]];
  const lista = nomes.filter(([id])=>grupos[id].length).map(([id, titulo])=>({id, titulo, html: grupos[id].join("")}));
  return antes.map(n=>n.outerHTML).join("") + abas("ficha", lista);
};

/* ---------- Meus casos (perito) ---------- */
TELAS["#/meus-casos"] = async ()=>{
  const peritos = await db.list("peritos");
  const meu = estado.ddPerito || await db.meta("perito_id") || peritos[0]?.id_perito;
  const casos = (await db.list("casos")).filter(c=>c.perito_id === meu)
    .sort((a, b)=>String(b.distribuido_em || "").localeCompare(String(a.distribuido_em || "")));
  const porRodada = {};
  casos.forEach(c=>(porRodada[c.rodada_id] = porRodada[c.rodada_id] || []).push(c));
  return `<h1>Meus casos <span class="conta">${casos.length}</span></h1>
    <p class="sub">Casos distribuídos ao perito. O seletor abaixo é a sua identificação neste protótipo.</p>
    <div class="card dd-meus"><div class="campos">${campo("ddMeuPerito", "Perito", {tipo: "select", opcoes: peritos.map(p=>[p.id_perito, p.nome]), valor: meu})}
      <p class="sub" style="align-self:end;margin:0">${peritos.find(p=>p.id_perito === meu)?.especialidade || ""}</p></div></div>
    ${Object.keys(porRodada).length ? Object.entries(porRodada).map(([rid, lista])=>`<div class="card">
      <h2 style="margin-top:0">Rodada ${esc(rid)} <span class="conta">${lista.length}</span></h2>
      <div class="tabela-wrap"><table><tr><th>Protocolo</th><th>Tipo</th><th>Distribuído em</th><th>Espera</th><th>Situação</th></tr>
        ${lista.map(c=>{ const e = ddEspera(c); return `<tr><td class="mono">${esc(c.protocolo)}</td><td>${esc(c.tipo)}</td>
          <td>${c.distribuido_em ? dataCurtaBR(c.distribuido_em) : "—"}</td><td>${e === null ? "—" : plural(Math.round(e), "dia", "dias")}</td>
          <td>${c.urgente ? '<span class="selo alerta">urgente</span>' : '<span class="selo ok">ordinário</span>'}</td></tr>`; }).join("")}</table></div></div>`).join("")
      : '<div class="card vazio">Nenhum caso distribuído a este perito.</div>'}`;
};
TELAS_DEPOIS["#/meus-casos"] = ()=>{
  $("#ddMeuPerito")?.addEventListener("change", async e=>{ estado.ddPerito = e.target.value; await db.meta("perito_id", e.target.value); navegar(); });
};

const ddRodadaDepoisAntes = TELAS_DEPOIS["#/rodada/:id"];
TELAS_DEPOIS["#/rodada/:id"] = async (p)=>{
  await ddRodadaDepoisAntes?.(p);
  const info = document.getElementById("ddPocoInfo");
  document.querySelectorAll("[data-dd-poco]").forEach(b=>b.addEventListener("click", ()=>{
    if (!info) return;
    info.innerHTML = `<b>${esc(b.dataset.ddPoco)}</b> · ${esc(b.dataset.ddPerito)} · ${b.dataset.ddTipo === "cobranca" ? "cobrança" : "ordinário"}`;
    info.classList.add("mostra");
  }));
};
