/* Identidade do Controle de Adiantamentos.
   Entra por último no build. A tela-assinatura é a régua de prazos por processo
   e o prazo em destaque no topo da ficha. */

const adDiasEntre = (de, ate)=> Math.round((new Date(ate + "T12:00:00") - new Date(de + "T12:00:00")) / 86400000);
TELAS["#/processos"] = async ()=>{
  const [ps, fs] = await Promise.all([db.list("processos"), db.list("feriados")]);
  const hoje = hojeISO(), busca = normalizar(estado.adBusca || ""), filtro = estado.adFiltro || "";
  const infos = ps.map(p=>({p, ...prazosDoProcesso(p, fs, hoje)}))
    .filter(({p})=>!busca || normalizar(`${p.id} ${p.unidade} ${p.solicitante} ${p.etapa_atual}`).includes(busca))
    .filter(({selo})=>filtro === "vencidos" ? selo === "vencido" : filtro === "vence7" ? selo === "vence7" : true)
    .sort((a, b)=>a.restam - b.restam);
  return `<h1>Processos <span class="conta">${infos.length}</span></h1>
    <p class="sub">Régua de prazos: cada linha mostra a posição do processo entre a abertura e o limite. <a href="#/pedido/novo">Novo pedido</a></p>
    <div class="card ad-barra"><div class="campos">
      ${campo("adBuscaProc", "Busca por número, unidade, servidor ou etapa", {valor: estado.adBusca || "", attrs: 'autocomplete="off"'})}
      ${campo("adFiltroProc", "Filtro", {tipo: "select", opcoes: [["", "Todos"], ["vencidos", "Vencidos"], ["vence7", "Vencem em 7 dias"]], valor: filtro})}</div></div>
    ${infos.length ? `<div class="card ad-reguas">${infos.map(({p, base, limite, restam, selo, regra})=>{
      const total = Math.max(1, adDiasEntre(base, limite)), decorridos = Math.max(0, adDiasEntre(base, hoje));
      const pct = Math.max(0, Math.min(100, Math.round(decorridos / total * 100)));
      const cls = selo === "vencido" ? "erro" : selo === "vence7" ? "alerta" : "ok";
      return `<a class="ad-regua ${cls}" href="#/processo/${encodeURIComponent(p.id)}">
        <span class="ad-regua-info"><b class="mono">${esc(p.id)}</b><span>${esc(p.solicitante || "")} · ${esc(p.unidade || "")}</span>
          <small class="sub">${esc(p.etapa_atual || "")}</small></span>
        <span class="ad-regua-trilho"><span class="barra ${cls}"><i style="width:${pct}%"></i></span>
          <small class="sub">${esc(dataCurtaBR(base))} → ${esc(dataCurtaBR(limite))} · ${regra.uteis ? "dias úteis" : "dias corridos"}</small></span>
        <span class="ad-regua-prazo"><span class="selo ${p.situacao === "encerrado" ? "info" : cls}">${p.situacao === "encerrado" ? "encerrado" : selo === "vencido" ? `${plural(Math.abs(restam), "dia", "dias")} vencido` : plural(restam, "dia", "dias")}</span>
          <small class="sub">${p.situacao === "encerrado" ? "fora da contagem" : selo === "vencido" ? "fora do prazo" : "até o limite"}</small></span></a>`;
    }).join("")}</div>` : '<div class="card vazio">Nenhum processo com estes filtros.</div>'}`;
};
TELAS_DEPOIS["#/processos"] = ()=>{
  let t = null;
  $("#adBuscaProc")?.addEventListener("input", e=>{
    clearTimeout(t); const v = e.target.value;
    t = setTimeout(()=>{ estado.adBusca = v; navegar(); }, 350);
  });
  $("#adFiltroProc")?.addEventListener("change", e=>{ estado.adFiltro = e.target.value; navegar(); });
};

/* prazo em destaque no topo da ficha */
const adFichaAntes = TELAS["#/processo/:id"];
TELAS["#/processo/:id"] = async (p)=>{
  const html = await adFichaAntes(p);
  const proc = await db.get("processos", p.id);
  if (!proc) return html;
  const r = prazosDoProcesso(proc, await db.list("feriados"));
  const cls = r.selo === "vencido" ? "erro" : r.selo === "vence7" ? "alerta" : "ok";
  const dica = proc.etapa_atual === "Prestação de contas" || proc.pago_em ? "Prazo para a prestação de contas" : "Prazo do processo";
  const doc = new DOMParser().parseFromString(`<div id="adRaiz">${html}</div>`, "text/html");
  const raiz = doc.getElementById("adRaiz");
  if (!raiz) return html;
  const card = doc.createElement("div");
  card.className = "card ad-topo"; card.id = "adPrazoTopo";
  const encerrado = proc.situacao === "encerrado";
  card.innerHTML = `<div><span class="sub">${dica}</span><h2>${encerrado ? "Processo encerrado" : r.restam < 0 ? `${plural(Math.abs(r.restam), "dia", "dias")} vencido` : `${plural(r.restam, "dia", "dias")} restantes`}</h2>
    <p class="sub">${encerrado ? "O processo saiu da contagem de prazo." : `Limite ${dataCurtaBR(r.limite)} · base de contagem ${dataCurtaBR(r.base)} · ${r.regra.uteis ? "dias úteis" : "dias corridos"}`}</p></div>
    <div class="ad-topo-barra"><span class="barra ${cls}"><i style="width:${Math.max(0, Math.min(100, Math.round((r.regra.dias - Math.max(0, r.restam)) / Math.max(1, r.regra.dias) * 100)))}%"></i></span>
      <span class="selo ${cls}">${r.selo === "vencido" ? "vencido" : r.selo === "vence7" ? "vence em até 7 dias" : "no prazo"}</span></div>`;
  const h1 = raiz.querySelector("h1");
  if (h1) h1.after(card); else raiz.insertBefore(card, raiz.firstChild);
  return raiz.innerHTML;
};
