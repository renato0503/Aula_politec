/* Identidade do Controle do Processo de Aquisição.
   Entra por último no build. A tela-assinatura é o kanban das 9 etapas da Lei
   14.133; a ficha do processo vira abas e o perfil requisitante deixa de ver a
   conclusão de etapa e o registro de análise. */

TELAS["#/processos"] = async ()=>{
  const f = caFiltros(), ps = await db.list("processos"), hoje = hojeISO(), b = normalizar(f.busca || "");
  const vis = ps.filter(p=>(!f.status || p.status === f.status)
    && (!b || normalizar(`${p.numero_sigadoc} ${p.numero_siag} ${p.objeto} ${p.unidade}`).includes(b)));
  const card = p=>{
    const atras = caAtrasado(p, hoje), dias = caDias(p.data_abertura);
    return `<a class="ca-card ${p.status === "concluido" ? "concluido" : ""}" href="#/processo/${encodeURIComponent(p.id_processo)}">
      <span class="ca-card-topo"><b class="mono">${esc(p.numero_sigadoc)}</b>${p.status === "concluido" ? '<span class="selo info">concluído</span>' : atras ? '<span class="selo erro">atrasado</span>' : '<span class="selo ok">em prazo</span>'}</span>
      <span class="ca-card-obj" title="${esc(p.objeto)}">${esc(p.objeto)}</span>
      <span class="sub">${esc(p.unidade)} · ${plural(dias, "dia", "dias")}</span>
      <span class="sub mono">SIAG ${esc(p.numero_siag)}</span></a>`;
  };
  return `<h1>Kanban da aquisição <span class="conta">${vis.length}</span></h1>
    <p class="sub">As 9 etapas da Lei 14.133/2021. Clique no cartão para abrir o processo; o cartão vermelho está fora do prazo.</p>
    <div class="card ca-barra"><div class="campos">
      ${campo("caBusca", "Busca por número, objeto ou unidade", {valor: f.busca || "", attrs: 'autocomplete="off"'})}
      ${campo("caStatus", "Situação", {tipo: "select", opcoes: [["", "Todas"], ["em andamento", "Em andamento"], ["concluido", "Concluído"]], valor: f.status})}
      <p class="sub" style="margin:0;align-self:end"><a href="#/processo/novo">Nova aquisição</a> · <a href="#/painel">Painel</a></p></div></div>
    <div class="ca-kanban">${CA_ETAPAS.map((e, i)=>{
      const lista = vis.filter(p=>p.etapa === e);
      return `<section class="ca-col"><h3><span class="n">${i + 1}</span>${esc(e)} <span class="conta">${lista.length}</span></h3>
        <div class="ca-col-lista">${lista.map(card).join("") || '<p class="sub">Nenhum processo.</p>'}</div></section>`;
    }).join("")}</div>`;
};
TELAS_DEPOIS["#/processos"] = ()=>{
  const f = caFiltros();
  $("#caStatus")?.addEventListener("change", e=>{ f.status = e.target.value; navegar(); });
  let t = null;
  $("#caBusca")?.addEventListener("input", e=>{
    clearTimeout(t); const v = e.target.value;
    t = setTimeout(()=>{ f.busca = v; navegar(); }, 350);
  });
};

/* ---------- ficha em abas e ações por perfil ---------- */
const caFichaAntes = TELAS["#/processo/:id"];
TELAS["#/processo/:id"] = async (p)=>{
  const html = await caFichaAntes(p);
  if (typeof abas !== "function" || html.includes('class="abas"')) return html;
  const doc = new DOMParser().parseFromString(`<div id="caRaiz">${html}</div>`, "text/html");
  const raiz = doc.getElementById("caRaiz");
  if (!raiz) return html;
  const requisitante = estado.perfil === "requisitante";
  if (requisitante){
    doc.getElementById("formCaAprovacao")?.remove();
    doc.getElementById("btnCaAvancar")?.remove();
  }
  // o cartão do objeto também trazia as etapas: separa para a aba Etapas
  [...raiz.children].filter(n=>n.classList?.contains("card")).forEach(card=>{
    const h2s = [...card.children].filter(n=>n.tagName === "H2");
    const corte = h2s.find(h=>/^etapas/.test((h.textContent || "").toLowerCase().trim()));
    if (!corte) return;
    const depois = doc.createElement("div"); depois.className = card.className;
    const antesCard = doc.createElement("div"); antesCard.className = card.className;
    let movendo = false;
    [...card.childNodes].forEach(n=>{ if (n === corte) movendo = true; (movendo ? depois : antesCard).appendChild(n); });
    if (depois.children.length){
      if (antesCard.children.length) card.replaceWith(antesCard, depois); else card.replaceWith(depois);
    } else if (antesCard.children.length) card.replaceWith(antesCard);
  });
  // barra horizontal de etapas (o detalhe com a base legal fica logo abaixo)
  const listaEtapas = doc.getElementById("caEtapas");
  if (listaEtapas){
    const barra = doc.createElement("div"); barra.className = "etapas";
    [...listaEtapas.children].forEach(li=>{
      const span = doc.createElement("span");
      span.className = li.classList.contains("etapa-feita") ? "feita" : li.classList.contains("etapa-atual") ? "atual" : "";
      span.textContent = (li.querySelector("b")?.textContent || li.textContent || "").replace(/^\d+\.\s*/, "");
      barra.appendChild(span);
    });
    listaEtapas.parentNode.insertBefore(barra, listaEtapas);
  }
  const antes = [], cards = [];
  const colher = node=>{
    if (node.nodeType !== 1) return;
    if (node.classList.contains("duas-colunas")){ [...node.children].forEach(colher); return; }
    if (node.classList.contains("card") && !node.classList.contains("kpi") && node.id !== "caCicloAviso") cards.push(node);
    else antes.push(node);
  };
  [...raiz.children].forEach(colher);
  if (!cards.length) return html;
  const grupos = {resumo: [], etapas: [], documentos: [], pendencias: [], precos: [], aprovacoes: [], historico: []};
  const destino = h=>{
    if (/etapa/.test(h)) return "etapas";
    if (/anexar|document/.test(h)) return "documentos";
    if (/pend/.test(h)) return "pendencias";
    if (/pesquisa|preço|preco/.test(h)) return "precos";
    if (/aprova|análise|modalidade|critério/.test(h)) return "aprovacoes";
    if (/histórico|historico/.test(h)) return "historico";
    return "resumo";
  };
  cards.forEach(c=>grupos[destino((c.querySelector("h2")?.textContent || "").toLowerCase())].push(c.outerHTML));
  if (requisitante && grupos.pendencias.length){
    grupos.pendencias.push('<p class="sub">A conclusão da etapa e o registro de análise são da equipe de aquisições.</p>');
  }
  const nomes = [["resumo", "Resumo", grupos.resumo.length], ["etapas", "Etapas", grupos.etapas.length], ["documentos", "Documentos", grupos.documentos.length],
    ["pendencias", "Pendências", grupos.pendencias.length], ["precos", "Preços", grupos.precos.length], ["aprovacoes", "Aprovações", grupos.aprovacoes.length],
    ["historico", "Histórico", grupos.historico.length]];
  const lista = nomes.filter(([id])=>grupos[id].length).map(([id, titulo, n])=>({id, titulo: n > 1 ? `${titulo}` : titulo, html: grupos[id].join("")}));
  return antes.map(n=>n.outerHTML).join("") + abas("ficha", lista);
};
