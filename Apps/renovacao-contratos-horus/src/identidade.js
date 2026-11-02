/* Identidade da Renovação de Contratos · Hórus.
   Entra por último no build. A tela-assinatura é a régua de vencimentos de 0 a
   180 dias com a barra empilhada do semáforo; a ficha vira abas e o fiscal tem
   a caixa “Meus contratos”. */

function rcRegua(cs, hoje){
  const ativos = cs.filter(c=>!RC_FORA.includes(c.status));
  const pontos = ativos.map(c=>{
    const d = rcDias(c.data_fim, hoje);
    if (d < 0 || d > 180) return "";
    const f = rcFaixa(c, hoje), cls = f ? f.selo : "info";
    return `<a class="rc-ponto ${cls}" style="left:${(d / 180 * 100).toFixed(2)}%" href="#/contrato/${encodeURIComponent(c.id_contrato)}"
      title="${esc(c.numero)} · ${esc(c.fornecedor)} · ${plural(d, "dia", "dias")}"></a>`;
  }).join("");
  const marcas = [0, 30, 60, 90, 120, 150, 180].map(d=>`<span style="left:${(d / 180 * 100).toFixed(2)}%">${d}</span>`).join("");
  return `<div class="card rc-regua-card"><h2 style="margin-top:0">Régua de vencimentos</h2>
    <p class="sub">Cada ponto é um contrato ativo, posicionado pelos dias que faltam. Clique no ponto para abrir a ficha.</p>
    <div class="rc-regua"><div class="rc-trilho"></div>${marcas}${pontos}</div>
    <p class="sub" style="margin:0">0 a 180 dias · ${ativos.filter(c=>{ const d = rcDias(c.data_fim, hoje); return d >= 0 && d <= 180; }).length} contratos na régua.</p></div>`;
}
function rcBarraEmpilhada(cs, hoje){
  const ativos = cs.filter(c=>!RC_FORA.includes(c.status));
  const por = Object.fromEntries(RC_FAIXAS.map(f=>[f.id, ativos.filter(c=>rcFaixa(c, hoje)?.id === f.id).length]));
  const total = ativos.length || 1;
  return `<div class="card rc-semaforo-card"><h2 style="margin-top:0">Semáforo em uma barra</h2>
    <div class="rc-stack">${RC_FAIXAS.map(f=>por[f.id] ? `<a class="rc-seg ${f.selo}" style="flex:${por[f.id]};background:var(--${f.selo === "ok" ? "verde" : f.selo === "erro" ? "vermelho" : f.selo === "alerta" ? "ambar" : "accent"})"
      href="#/contratos" data-rc-faixa="${f.id}" title="${esc(f.rotulo)}: ${por[f.id]} contrato(s)">${por[f.id]}</a>` : "").join("")}</div>
    <div class="rc-legenda">${RC_FAIXAS.map(f=>`<a href="#/contratos" data-rc-faixa="${f.id}"><i class="rc-cor ${f.selo}"></i>${esc(f.rotulo.split(" (")[0])} <b>${por[f.id]}</b></a>`).join("")}</div>
    <p class="sub" style="margin:0">${ativos.length} contratos ativos · clique na faixa para filtrar a lista.</p></div>`;
}
async function rcMeusContratos(){
  if (estado.perfil !== "fiscal") return "";
  const nome = await db.meta("fiscal_nome");
  const cs = await db.list("contratos"), hoje = hojeISO();
  const meus = [];
  if (nome) for (const c of cs){
    const fs = await db.porIndice("fiscais", "contrato_id", c.id_contrato);
    if (fs.some(f=>!f.ate && normalizar(f.nome) === normalizar(nome))) meus.push(c);
  }
  return `<div class="card rc-meus"><div class="rc-meus-topo"><div><span class="sub">Meus contratos</span>
      <h2>${nome ? esc(nome) : "Informe o seu nome de fiscal"} <span class="conta">${meus.length}</span></h2></div>
      <div class="rc-meus-nome"><input id="rcMeuNome" placeholder="Nome do fiscal" value="${esc(nome || "")}" autocomplete="off">
        <button type="button" id="btnRcMeuNome">Salvar</button></div></div>
    ${nome ? (meus.length ? `<div class="rc-meus-lista">${meus.map(c=>{ const f = rcFaixa(c, hoje); return `<a href="#/contrato/${encodeURIComponent(c.id_contrato)}">
      <b class="mono">${esc(c.numero)}</b><span>${esc(c.fornecedor)}</span><span class="selo ${f ? f.selo : "info"}">${f ? esc(f.rotulo.split(" (")[0]) : "—"}</span>
      <span class="sub">${plural(rcDias(c.data_fim, hoje), "dia", "dias")}</span></a>`; }).join("")}</div>` : '<p class="sub">Nenhum contrato atribuído a este fiscal.</p>')
      : '<p class="sub">Salve o nome para ver os contratos em que você é o fiscal atual.</p>'}</div>`;
}

const rcPainelAntes = TELAS["#/painel"];
TELAS["#/painel"] = async ()=>{
  const html = await rcPainelAntes();
  const cs = await db.list("contratos"), hoje = hojeISO();
  const doc = new DOMParser().parseFromString(`<div id="rcRaiz">${html}</div>`, "text/html");
  const raiz = doc.getElementById("rcRaiz");
  if (!raiz) return html;
  const bloco = doc.createElement("div");
  bloco.innerHTML = rcBarraEmpilhada(cs, hoje) + rcRegua(cs, hoje) + await rcMeusContratos();
  const alvo = doc.getElementById("tabelaFaixas")?.closest(".card");
  if (alvo) alvo.parentNode.insertBefore(bloco, alvo); else raiz.insertBefore(bloco, raiz.querySelector("h1"));
  return raiz.innerHTML;
};
const rcPainelDepoisAntes = TELAS_DEPOIS["#/painel"];
TELAS_DEPOIS["#/painel"] = async ()=>{
  await rcPainelDepoisAntes?.();
  $("#btnRcMeuNome")?.addEventListener("click", async ()=>{
    const nome = valorDe("rcMeuNome");
    if (!nome) return toast("Informe o nome do fiscal.");
    await db.meta("fiscal_nome", nome); toast("Nome do fiscal salvo."); navegar();
  });
  $$("[data-rc-faixa]").forEach(a=>a.addEventListener("click", e=>{
    e.preventDefault(); estado.rcFiltros = {...rcFiltros(), faixa: a.dataset.rcFaixa}; location.hash = "#/contratos";
  }));
};

/* ---------- ficha em abas ---------- */
const rcFichaAntes = TELAS["#/contrato/:id"];
TELAS["#/contrato/:id"] = async (p)=>{
  const html = await rcFichaAntes(p);
  if (typeof abas !== "function" || html.includes('class="abas"')) return html;
  const doc = new DOMParser().parseFromString(`<div id="rcFichaRaiz">${html}</div>`, "text/html");
  const raiz = doc.getElementById("rcFichaRaiz");
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
  const grupos = {resumo: [], aditivos: [], instrucao: [], ajustes: [], fiscais: [], auditoria: []};
  const destino = h=>{
    if (/aditivo/.test(h)) return "aditivos";
    if (/instru|checklist|reposit/.test(h)) return "instrucao";
    if (/reajuste|repactua|reequil/.test(h)) return "ajustes";
    if (/fiscal/.test(h)) return "fiscais";
    if (/auditoria/.test(h)) return "auditoria";
    return "resumo";
  };
  cards.forEach(node=>{
    const fixo = {rcAjustes: "ajustes", rcFiscais: "fiscais"}[node.id];
    grupos[fixo || destino((node.querySelector("h2")?.textContent || "").toLowerCase())].push(node.outerHTML);
  });
  const nomes = [["resumo", "Resumo"], ["aditivos", "Aditivos"], ["instrucao", "Instrução"], ["ajustes", "Ajustes"], ["fiscais", "Fiscais"], ["auditoria", "Auditoria"]];
  const lista = nomes.filter(([id])=>grupos[id].length).map(([id, titulo])=>({id, titulo, html: grupos[id].join("")}));
  return antes.map(n=>n.outerHTML).join("") + abas("ficha", lista);
};
