/* Identidade do Mapa de Equipamentos.
   Entra por último no build. A tela-assinatura é o mapa de MT em SVG, com os
   municípios do arquivo embutido e os pinos das unidades; o perfil Unidade tem
   o contexto de unidade. */

const EQ_UNIDADE_ANTES = TELAS["#/equipamentos"];
TELAS["#/equipamentos"] = async (p)=>{
  if (estado.perfil === "unidade" && estado.contexto) await db.meta("unidade_dona", estado.contexto);
  return EQ_UNIDADE_ANTES(p);
};

TELAS["#/mapa"] = async ()=>{
  const mun = dadosEmbutidos("municipios") || [];
  const [unidades, eqs] = await Promise.all([db.list("unidades"), db.list("equipamentos")]);
  const ativas = unidades.filter(u=>!u.excluido);
  const comUnidade = new Set(ativas.map(u=>normalizar(u.municipio)));
  const xs = mun.flatMap(m=>m.p.map(q=>q[0])), ys = mun.flatMap(m=>m.p.map(q=>q[1]));
  const minX = Math.min(...xs), maxX = Math.max(...xs), minY = Math.min(...ys), maxY = Math.max(...ys);
  const W = 900, H = 620, pad = 12;
  const sx = lon => pad + (lon - minX) / (maxX - minX) * (W - pad * 2);
  const sy = lat => pad + (maxY - lat) / (maxY - minY) * (H - pad * 2);
  const caminho = p => "M" + p.map(([lon, lat])=>`${sx(lon).toFixed(1)},${sy(lat).toFixed(1)}`).join("L") + "Z";
  const eqPorUnidade = Object.fromEntries(ativas.map(u=>[u.id, eqs.filter(e=>!e.excluido && e.unidade_id === u.id).length]));
  const paths = mun.filter(m=>Array.isArray(m.p) && m.p.length).map(m=>`<path d="${caminho(m.p)}" class="eq-mun ${comUnidade.has(normalizar(m.n)) ? "tem" : ""}" data-mun="${esc(m.n)}"><title>${esc(m.n)}</title></path>`).join("");
  const pinos = ativas.map(u=>{
    if (!u.latitude || !u.longitude) return "";
    const n = eqPorUnidade[u.id] || 0;
    return `<a class="eq-pino" href="#/equipamentos" data-eq-unidade="${esc(u.id)}" title="${esc(u.nome)} · ${plural(n, "equipamento", "equipamentos")}">
      <circle cx="${sx(u.longitude).toFixed(1)}" cy="${sy(u.latitude).toFixed(1)}" r="${n ? 11 : 8}"></circle>
      <text x="${sx(u.longitude).toFixed(1)}" y="${(sy(u.latitude) + 4).toFixed(1)}">${n}</text></a>`;
  }).join("");
  const semCoord = ativas.filter(u=>!u.latitude || !u.longitude).length;
  return `<h1>Mapa de Mato Grosso</h1>
    <p class="sub">Municípios do arquivo embutido (${mun.length}) e pinos das unidades. O número dentro do pino é a quantidade de equipamentos. Clique para abrir a lista filtrada.</p>
    <div class="grade"><div class="card kpi"><div class="v">${ativas.length}</div><div class="r">unidades</div></div>
      <div class="card kpi"><div class="v">${mun.length}</div><div class="r">municípios no mapa</div></div>
      <div class="card kpi"><div class="v">${eqs.filter(e=>!e.excluido).length}</div><div class="r">equipamentos</div></div>
      <div class="card kpi"><div class="v">${semCoord}</div><div class="r">unidades sem coordenada</div></div></div>
    <div class="card eq-mapa-card"><div class="eq-mapa-legenda"><span><i class="tem"></i>com unidade</span><span><i></i>sem unidade</span>
      <span><i class="pino"></i>unidade com equipamentos</span></div>
      <svg class="eq-mapa" viewBox="0 0 ${W} ${H}" role="img" aria-label="Mapa de Mato Grosso com as unidades">
        <g class="eq-muns">${paths}</g><g class="eq-pinos">${pinos}</g></svg></div>`;
};
TELAS_DEPOIS["#/mapa"] = ()=>{
  $$("[data-eq-unidade]").forEach(a=>a.addEventListener("click", e=>{
    e.preventDefault(); estado.filtrosEq = {...filtrosEq(), unidade: a.dataset.eqUnidade}; location.hash = "#/equipamentos";
  }));
};
