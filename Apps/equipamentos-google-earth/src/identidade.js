/* Identidade do Mapa de Equipamentos.
   Entra por último no build. A tela-assinatura é o mapa de MT em SVG, com os
   municípios do arquivo embutido e os pinos das unidades; o perfil Unidade tem
   o contexto de unidade. Clicar no município abre a divisão por distritos. */

const EQ_UNIDADE_ANTES = TELAS["#/equipamentos"];
TELAS["#/equipamentos"] = async (p)=>{
  if (estado.perfil === "unidade" && estado.contexto) await db.meta("unidade_dona", estado.contexto);
  return EQ_UNIDADE_ANTES(p);
};

const filtroMapa = ()=> estado.eqFiltroMapa || (estado.eqFiltroMapa = {semContrato:false, parados:false, pontoUnico:false, diretoria:"", tipo:""});
const viewMapa = ()=> estado.eqView || (estado.eqView = {x:0, y:0, w:900, h:620});

TELAS["#/mapa"] = async ()=>{
  const mun = dadosEmbutidos("municipios") || [];
  const [unidades, eqs, dirs] = await Promise.all([db.list("unidades"), db.list("equipamentos"), db.list("diretorias")]);
  const base = await baseDeCalculo();
  const f = filtroMapa();
  const ativas = unidades.filter(u=> !u.excluido);
  const comUnidade = new Set(ativas.map(u=> normalizar(u.municipio)));
  const xs = mun.flatMap(m=> m.p.map(q=> q[0])), ys = mun.flatMap(m=> m.p.map(q=> q[1]));
  const minX = Math.min(...xs), maxX = Math.max(...xs), minY = Math.min(...ys), maxY = Math.max(...ys);
  const W = 900, H = 620, pad = 12;
  const sx = lon => pad + (lon - minX) / (maxX - minX) * (W - pad * 2);
  const sy = lat => pad + (maxY - lat) / (maxY - minY) * (H - pad * 2);
  const caminho = p => "M" + p.map(([lon, lat])=>`${sx(lon).toFixed(1)},${sy(lat).toFixed(1)}`).join("L") + "Z";
  // o filtro do mapa vale para os equipamentos que ele mostra
  const combina = e=>{
    if (f.semContrato && e.temContrato) return false;
    if (f.parados && e.status !== "parado") return false;
    if (f.pontoUnico && !e.pontoUnico) return false;
    if (f.diretoria && (e.diretoria?.sigla || "") !== f.diretoria) return false;
    if (f.tipo && e.tipo !== f.tipo) return false;
    return true;
  };
  const eqBase = base.eqs.filter(e=> !e.excluido);
  const eqVisiveis = eqBase.filter(combina);
  const porUnidade = {};
  for (const e of eqVisiveis){ (porUnidade[e.unidade_id] = porUnidade[e.unidade_id] || []).push(e); }
  const corRisco = r=> r >= 10 ? "vermelho" : r >= 5 ? "ambar" : "verde";
  const paths = mun.filter(m=> Array.isArray(m.p) && m.p.length).map(m=>{
    const nome = normalizar(m.n);
    const daUnidade = ativas.filter(u=> normalizar(u.municipio) === nome);
    return `<path d="${caminho(m.p)}" class="eq-mun ${daUnidade.length ? "tem" : ""}" data-mun="${esc(m.n)}" data-cod="${esc(m.c)}"
      role="button" tabindex="0" aria-label="Abrir ${esc(m.n)}"><title>${esc(m.n)} · ${daUnidade.length ? plural(daUnidade.length, "unidade", "unidades") : "sem unidade"}</title></path>`;
  }).join("");
  const pinos = ativas.map(u=>{
    if (!u.latitude || !u.longitude) return "";
    const lista = porUnidade[u.id] || [];
    const n = lista.length, risco = Math.max(0, ...lista.map(e=> e.risco));
    const cor = n ? corRisco(risco) : "neutro";
    return `<a class="eq-pino eq-pino-${cor}" href="#/equipamentos" data-eq-unidade="${esc(u.id)}" data-eq-nome="${esc(u.nome)}"
      title="${esc(u.nome)} · ${plural(n, "equipamento", "equipamentos")}${n ? " · risco " + risco : ""}">
      <circle cx="${sx(u.longitude).toFixed(1)}" cy="${sy(u.latitude).toFixed(1)}" r="${n ? 9 + Math.min(8, n / 3) : 6}"></circle>
      <text x="${sx(u.longitude).toFixed(1)}" y="${(sy(u.latitude) + 4).toFixed(1)}">${n}</text></a>`;
  }).join("");
  const semCoord = ativas.filter(u=> !u.latitude || !u.longitude).length;
  const tipos = [...new Set(eqBase.map(e=> e.tipo))].sort();
  const siglaDir = d=> dirs.find(x=> x.id === d)?.sigla || "";
  const linhaMun = m=>{
    const daUnidade = ativas.filter(u=> normalizar(u.municipio) === normalizar(m.n));
    const lista = daUnidade.flatMap(u=> porUnidade[u.id] || []);
    return `<tr><td><a href="#/municipio/${encodeURIComponent(m.c)}"><b>${esc(m.n)}</b></a></td>
      <td>${daUnidade.length}</td><td class="num">${lista.length}</td>
      <td>${daUnidade.map(u=> esc(u.nome)).join(", ") || "—"}</td>
      <td>${(DISTRITOS_MUNICIPIO?.[m.c] || []).length || "—"}</td></tr>`;
  };
  return `<h1>Mapa de Mato Grosso</h1>
    <p class="sub">Municípios do arquivo embutido (${mun.length}) e pinos das unidades. O número dentro do pino é a quantidade de equipamentos que passam pelo filtro.
      Clique no município para abrir a divisão por distritos; clique no pino para ver os equipamentos da unidade.</p>
    <div class="card"><h2 style="margin-top:0">Filtros do mapa</h2>
      <div class="campos">
        <div class="campo"><label for="mfDiretoria">Diretoria</label><select id="mfDiretoria">
          <option value="">Todas</option>${dirs.map(d=> `<option value="${esc(d.sigla)}" ${f.diretoria === d.sigla ? "selected" : ""}>${esc(d.sigla)}</option>`).join("")}</select></div>
        <div class="campo"><label for="mfTipo">Tipo de equipamento</label><select id="mfTipo">
          <option value="">Todos</option>${tipos.map(t=> `<option value="${esc(t)}" ${f.tipo === t ? "selected" : ""}>${esc(t)}</option>`).join("")}</select></div>
      </div>
      <div class="chips" style="margin-top:8px">
        <label style="display:inline-flex;gap:6px"><input type="checkbox" id="mfSemContrato" style="width:auto" ${f.semContrato ? "checked" : ""}> sem contrato</label>
        <label style="display:inline-flex;gap:6px"><input type="checkbox" id="mfParados" style="width:auto" ${f.parados ? "checked" : ""}> parados</label>
        <label style="display:inline-flex;gap:6px"><input type="checkbox" id="mfPontoUnico" style="width:auto" ${f.pontoUnico ? "checked" : ""}> ponto único de falha</label>
      </div>
      <div class="linha-botoes nao-imprimir"><button id="mfLimpar">Limpar os filtros</button>
        <button id="mfZoomMais">Zoom +</button><button id="mfZoomMenos">Zoom −</button><button id="mfZoomTudo">Ver tudo</button></div>
      <p class="sub" id="mfResumo">${eqVisiveis.length} de ${eqBase.length} equipamentos no mapa.</p></div>
    <div class="grade">
      <div class="card kpi"><div class="v">${ativas.length}</div><div class="r">unidades</div></div>
      <div class="card kpi"><div class="v">${mun.length}</div><div class="r">municípios no mapa</div></div>
      <div class="card kpi"><div class="v">${eqVisiveis.length}</div><div class="r">equipamentos no filtro</div></div>
      <div class="card kpi"><div class="v">${semCoord}</div><div class="r">unidades sem coordenada</div></div>
    </div>
    <div class="card eq-mapa-card"><div class="eq-mapa-legenda"><span><i class="tem"></i>com unidade</span><span><i></i>sem unidade</span>
      <span><i class="pino verde"></i>risco baixo</span><span><i class="pino ambar"></i>risco médio</span><span><i class="pino vermelho"></i>risco alto</span></div>
      <svg class="eq-mapa" id="svgMapa" viewBox="0 0 ${W} ${H}" role="img" aria-label="Mapa de Mato Grosso com as unidades">
        <g class="eq-muns">${paths}</g><g class="eq-pinos">${pinos}</g></svg>
      <div id="painelUnidade"></div></div>
    <div class="card tabela-wrap"><h2>Municípios (a mesma informação do mapa, em tabela)</h2>
      <table><tr><th>Município</th><th class="num">Unidades</th><th class="num">Equipamentos no filtro</th><th>Unidades</th><th class="num">Distritos</th></tr>
        ${mun.filter(m=> comUnidade.has(normalizar(m.n)) || (DISTRITOS_MUNICIPIO?.[m.c] || []).length).map(linhaMun).join("")}</table></div>`;
};
TELAS_DEPOIS["#/mapa"] = async ()=>{
  const svg = $("#svgMapa"); if (!svg) return;
  const f = filtroMapa();
  const mud = id=>{ const el = $("#" + id); if (!el) return; el.addEventListener("change", ()=>{
    f.semContrato = $("#mfSemContrato").checked; f.parados = $("#mfParados").checked; f.pontoUnico = $("#mfPontoUnico").checked;
    f.diretoria = $("#mfDiretoria").value; f.tipo = $("#mfTipo").value; navegar(); }); };
  ["mfSemContrato", "mfParados", "mfPontoUnico", "mfDiretoria", "mfTipo"].forEach(mud);
  $("#mfLimpar")?.addEventListener("click", ()=>{ estado.eqFiltroMapa = {semContrato:false, parados:false, pontoUnico:false, diretoria:"", tipo:""}; navegar(); });
  // zoom e arrasto no viewBox
  const v = viewMapa();
  const aplicar = ()=> svg.setAttribute("viewBox", `${v.x.toFixed(1)} ${v.y.toFixed(1)} ${v.w.toFixed(1)} ${v.h.toFixed(1)}`);
  const zoom = fator=>{
    const cx = v.x + v.w / 2, cy = v.y + v.h / 2;
    const nw = Math.min(900, Math.max(120, v.w * fator)), nh = nw * (620 / 900);
    v.w = nw; v.h = nh; v.x = cx - nw / 2; v.y = cy - nh / 2; aplicar();
  };
  $("#mfZoomMais")?.addEventListener("click", ()=> zoom(0.75));
  $("#mfZoomMenos")?.addEventListener("click", ()=> zoom(1.35));
  $("#mfZoomTudo")?.addEventListener("click", ()=>{ v.x = 0; v.y = 0; v.w = 900; v.h = 620; aplicar(); });
  // roda do mouse amplia e reduz, com o ponteiro como centro
  svg.addEventListener("wheel", e=>{
    e.preventDefault();
    const r = svg.getBoundingClientRect();
    const px = (e.clientX - r.left) / r.width, py = (e.clientY - r.top) / r.height;
    const cx = v.x + px * v.w, cy = v.y + py * v.h;
    const nw = Math.min(900, Math.max(120, v.w * (e.deltaY > 0 ? 1.12 : 0.89))), nh = nw * (620 / 900);
    v.w = nw; v.h = nh; v.x = cx - px * nw; v.y = cy - py * nh; aplicar();
  }, {passive:false});
  let arrastando = null;
  svg.addEventListener("pointerdown", e=>{ if (e.target.closest("a")) return; arrastando = {x:e.clientX, y:e.clientY, vx:v.x, vy:v.y}; svg.setPointerCapture(e.pointerId); });
  svg.addEventListener("pointermove", e=>{
    if (!arrastando) return;
    const escala = v.w / svg.clientWidth;
    v.x = arrastando.vx - (e.clientX - arrastando.x) * escala;
    v.y = arrastando.vy - (e.clientY - arrastando.y) * escala; aplicar();
  });
  svg.addEventListener("pointerup", ()=>{ arrastando = null; });
  // clicar no município abre a divisão por distritos
  $$("[data-cod]").forEach(p=>{
    const abrir = ()=>{ location.hash = "#/municipio/" + encodeURIComponent(p.dataset.cod); };
    p.addEventListener("click", abrir);
    p.addEventListener("keydown", e=>{ if (e.key === "Enter" || e.key === " ") { e.preventDefault(); abrir(); } });
  });
  // clicar no pino abre o painel lateral da unidade
  $$("[data-eq-unidade]").forEach(a=> a.addEventListener("click", async e=>{
    e.preventDefault();
    const id = a.dataset.eqUnidade, u = await db.get("unidades", id);
    const eqs = (await db.porIndice("equipamentos", "unidade_id", id)).filter(x=> !x.excluido);
    $("#painelUnidade").innerHTML = `<div class="card eq-painel"><h2 style="margin-top:0">${esc(u?.nome || "Unidade")}</h2>
      <p class="sub">${esc(u?.municipio || "")} · ${plural(eqs.length, "equipamento", "equipamentos")}.</p>
      <div class="tabela-wrap"><table><tr><th>Patrimônio</th><th>Equipamento</th><th>Situação</th><th class="num">Risco</th></tr>
        ${eqs.slice(0, 20).map(x=> `<tr><td><a href="#/equipamento/${encodeURIComponent(x.id)}">${esc(x.patrimonio)}</a></td><td>${esc(x.nome)}</td>
          <td>${esc(x.status)}</td><td class="num">${x.criticidade}</td></tr>`).join("")}</table></div>
      <div class="linha-botoes nao-imprimir"><a class="botao" href="#/equipamentos">Ver todos na lista</a>
        <a class="botao" href="#/municipio/${encodeURIComponent(u?.municipio_ibge || "")}">Município e distritos</a></div></div>`;
  }));
};
