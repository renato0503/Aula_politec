/* Identidade da Gestão de Documentos.
   Entra por último no build. A tela-assinatura é a caixa por perfil (a instruir,
   a revisar, a assinar); a ficha vira abas, o checklist fica com caixa de
   seleção e a assinatura fica só para a autoridade decisora. */

async function gdMinhaCaixa(){
  const ps = (await db.list("processos")).filter(p=>p.status === "em andamento");
  const hoje = hojeISO();
  const conjuntos = {
    servidor: {titulo: "A instruir", texto: "Processos que esperam a instrução e o checklist.", lista: ps},
    gestor: {titulo: "A revisar", texto: "Processos em andamento para conferir antes da decisão.", lista: ps},
    autoridade: {titulo: "A assinar", texto: "Processos em andamento que esperam a assinatura e o arquivamento.", lista: ps},
  };
  const c = conjuntos[estado.perfil] || conjuntos.servidor;
  const lista = c.lista.sort((a, b)=>String(a.data_autuacao).localeCompare(String(b.data_autuacao))).slice(0, 6);
  return `<div class="card gd-caixa"><div class="gd-caixa-topo"><div><span class="sub">Minha caixa</span><h2>${c.titulo} <span class="conta">${c.lista.length}</span></h2></div>
    <a class="botao" href="#/processos">Ver todos</a></div>
    <p class="sub">${c.texto}</p>
    ${lista.length ? `<div class="gd-caixa-lista">${lista.map(p=>{
      const pr = gdPrazo(p, hoje), cls = pr.sinal === "vermelho" ? "erro" : pr.sinal === "amarelo" ? "alerta" : "ok";
      return `<a class="gd-caixa-item" href="#/processo/${encodeURIComponent(p.id_processo)}">
        <span class="gd-caixa-num mono">${esc(p.numero_processo)}</span>
        <span class="gd-caixa-ass">${esc(p.assunto)}</span>
        <span class="gd-caixa-barra"><span class="barra ${cls}"><i style="width:${Math.min(100, Math.max(0, pr.pct))}%"></i></span>
          <small class="sub">${pr.pct}% do prazo · ${pr.limite < hoje ? "venceu em " + dataCurtaBR(pr.limite) : "até " + dataCurtaBR(pr.limite)}</small></span></a>`;
    }).join("")}</div>` : '<p class="sub">Nenhum processo nesta caixa.</p>'}</div>`;
}
const gdPainelAntes = TELAS["#/painel"];
TELAS["#/painel"] = async ()=>{
  const html = await gdPainelAntes();
  const doc = new DOMParser().parseFromString(`<div id="gdRaiz">${html}</div>`, "text/html");
  const raiz = doc.getElementById("gdRaiz");
  if (!raiz) return html;
  if (estado.perfil !== "gestor") doc.getElementById("gdPainelGestor")?.remove();
  const caixa = doc.createElement("div"); caixa.innerHTML = await gdMinhaCaixa();
  raiz.insertBefore(caixa.firstElementChild, raiz.querySelector("h1"));
  return raiz.innerHTML;
};

/* ---------- ficha em abas, checklist com caixa e assinatura por perfil ---------- */
const gdFichaAntes = TELAS["#/processo/:id"];
TELAS["#/processo/:id"] = async (p)=>{
  const html = await gdFichaAntes(p);
  if (typeof abas !== "function" || html.includes('class="abas"')) return html;
  const doc = new DOMParser().parseFromString(`<div id="gdRaiz">${html}</div>`, "text/html");
  const raiz = doc.getElementById("gdRaiz");
  if (!raiz) return html;
  const checklist = await db.porIndice("checklist", "processo_id", p.id);
  raiz.querySelectorAll("#gdCardChecklist li").forEach(li=>{
    const b = li.querySelector(".gdCheckItem"); if (!b) return;
    const rec = checklist.find(x=>x.item === b.dataset.item);
    if (rec){
      const s = doc.createElement("small"); s.className = "gd-quem";
      s.textContent = `por ${rec.perfil || "—"}`; li.appendChild(s);
    }
  });
  if (estado.perfil !== "autoridade"){
    const box = doc.getElementById("gdConclusao");
    if (box) box.innerHTML = `<h2 style="margin-top:0">Conclusão e assinatura</h2>
      <p class="sub">A assinatura e o arquivamento são da autoridade decisora. O processo segue para ela depois da instrução e da revisão.</p>`;
    const aviso = doc.createElement("div");
    aviso.className = "card pendente";
    aviso.innerHTML = "<b>A assinatura e o arquivamento são da autoridade decisora.</b> A instrução e a revisão continuam com você.";
    const h1 = doc.querySelector("h1");
    if (h1) h1.after(aviso);
  }
  const antes = [], cards = [];
  const colher = node=>{
    if (node.nodeType !== 1) return;
    if (node.classList.contains("duas-colunas")){ [...node.children].forEach(colher); return; }
    if (node.classList.contains("card") && !node.classList.contains("kpi")) cards.push(node);
    else antes.push(node);
  };
  [...raiz.children].forEach(colher);
  if (!cards.length) return html;
  const grupos = {resumo: [], minutas: [], checklist: [], conclusao: [], historico: []};
  const destino = h=>{
    if (/minuta/.test(h)) return "minutas";
    if (/checklist/.test(h)) return "checklist";
    if (/conclus|assinatura/.test(h)) return "conclusao";
    if (/histórico|historico/.test(h)) return "historico";
    return "resumo";
  };
  cards.forEach(c=>grupos[destino((c.querySelector("h2")?.textContent || "").toLowerCase())].push(c.outerHTML));
  const nomes = [["resumo", "Resumo"], ["minutas", "Minutas"], ["checklist", "Checklist"], ["conclusao", "Conclusão"], ["historico", "Histórico"]];
  const lista = nomes.filter(([id])=>grupos[id].length).map(([id, titulo])=>({id, titulo, html: grupos[id].join("")}));
  return antes.map(n=>n.outerHTML).join("") + abas("ficha", lista);
};
