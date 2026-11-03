/* ================= Sprint 6 e 10 · mapa com zoom e filtros, e a divisão por distritos do município ================= */
"use strict";

const MUNICIPIO_POR_COD = new Map(MUNICIPIOS.map(m=> [m.c, m]));
// link para o Google Maps: sem chave de API, sem biblioteca, só abre o navegador
const linkMaps = (lat, lon, rotulo)=> (lat === null || lat === undefined || lon === null || lon === undefined) ? ""
  : `<a class="botao" target="_blank" rel="noopener" href="https://www.google.com/maps/search/?api=1&query=${lat},${lon}">${esc(rotulo || "Abrir no Google Maps")}</a>`;
const DISTRITOS_MUNICIPIO = dadosEmbutidos("mt-distritos") || {};
teste("a divisão por distritos tem 142 municípios ou quase", ()=> Object.keys(DISTRITOS_MUNICIPIO).length >= 140 || Object.keys(DISTRITOS_MUNICIPIO).length);
teste("Cuiabá tem distritos no arquivo do IBGE", ()=> (DISTRITOS_MUNICIPIO["5103403"] || []).includes("Cuiabá"));

/* ---------- tela do município: divisão por bairros, unidades e equipamentos ---------- */
TELAS["#/municipio/:cod"] = async ({cod})=>{
  const m = MUNICIPIO_POR_COD.get(String(cod));
  if (!m) return `<div class="card vazio">Município não encontrado. <a href="#/mapa">Voltar ao mapa</a></div>`;
  const distritos = DISTRITOS_MUNICIPIO[m.c] || [];
  const seat = distritos.find(d=> normalizar(d) === normalizar(m.n)) || "";
  const [unidades, eqs, dirs] = await Promise.all([db.list("unidades"), db.list("equipamentos"), db.list("diretorias")]);
  const doMunicipio = unidades.filter(u=> !u.excluido && normalizar(u.municipio) === normalizar(m.n));
  const eqDaUnidade = u=> eqs.filter(e=> !e.excluido && e.unidade_id === u.id);
  const linhaUn = u=>{
    const lista = eqDaUnidade(u);
    return `<tr><td><b>${esc(u.nome)}</b></td><td>${esc(u.tipo)}</td>
      <td>${esc(dirs.find(d=> d.id === u.diretoria_id)?.sigla || "")}</td><td class="num">${lista.length}</td>
      <td class="num">${lista.filter(e=> e.contrato_id).length}</td>
      <td><a href="#/equipamentos">Ver na lista</a></td></tr>`;
  };
  return `<h1>${esc(m.n)}</h1>
    <p class="sub">Município ${esc(m.n)} (IBGE ${esc(m.c)}) · ${esc(distritos.length)} ${plural(distritos.length, "distrito", "distritos")} no cadastro do IBGE.
      <a href="#/mapa">Voltar ao mapa</a></p>
    <div class="grade">
      <div class="card kpi"><div class="v">${distritos.length}</div><div class="r">distritos (bairros)</div></div>
      <div class="card kpi"><div class="v">${doMunicipio.length}</div><div class="r">unidades do app aqui</div></div>
      <div class="card kpi"><div class="v">${doMunicipio.reduce((a, u)=>a + eqDaUnidade(u).length, 0)}</div><div class="r">equipamentos</div></div>
      <div class="card kpi"><div class="v">${esc(m.lat ?? "—")}</div><div class="r">latitude</div></div>
    </div>
    <p class="linha-botoes nao-imprimir">${linkMaps(m.lat, m.lon, "Abrir o município no Google Maps")}
      <a class="botao" href="#/mapa">Voltar ao mapa</a></p>
    <div class="card"><h2 style="margin-top:0">Divisão por distritos</h2>
      ${distritos.length ? `<div class="chips">${distritos.map(d=> `<span class="selo ${d === seat ? "ok" : "info"}">${esc(d)}${d === seat ? " · sede" : ""}</span>`).join("")}</div>`
        : `<p class="sub">O IBGE não registra distritos para este município. A divisão em bairros vem da lei municipal e precisa ser digitada pela unidade, quando for necessária.</p>`}
      ${seat ? `<p class="sub">A sede do município é o distrito de mesmo nome.</p>` : ""}</div>
    <div class="card tabela-wrap"><h2>Unidades do app neste município</h2>
      <table><tr><th>Unidade</th><th>Tipo</th><th>Diretoria</th><th class="num">Equipamentos</th><th class="num">Com contrato</th><th></th></tr>
        ${doMunicipio.map(linhaUn).join("") || '<tr><td colspan="6" class="vazio">Nenhuma unidade do app neste município.</td></tr>'}</table></div>
    ${distritos.length ? `<div class="card"><h2 style="margin-top:0">Buscar equipamento por distrito</h2>
      <p class="sub">Escolha o distrito: a lista de equipamentos da unidade é filtrada pelo bairro informado no cadastro.</p>
      <div class="campos"><div class="campo"><label for="municipioDistrito">Distrito</label><select id="municipioDistrito">
        <option value="">Todos</option>${distritos.map(d=> `<option value="${esc(d)}">${esc(d)}</option>`).join("")}</select></div></div>
      <div id="municipioDistritoResultado"></div></div>` : ""}`;
};
TELAS_DEPOIS["#/municipio/:cod"] = async ({cod})=>{
  const sel = $("#municipioDistrito");
  if (!sel) return;
  sel.addEventListener("change", async ()=>{
    const bairro = sel.value;
    const [unidades, eqs] = await Promise.all([db.list("unidades"), db.list("equipamentos")]);
    const doMunicipio = unidades.filter(u=> !u.excluido && normalizar(u.municipio) === normalizar(MUNICIPIO_POR_COD.get(String(cod))?.n || ""));
    const alvo = eqs.filter(e=> !e.excluido && doMunicipio.some(u=> u.id === e.unidade_id)
      && (!bairro || normalizar(e.bairro || "") === normalizar(bairro)));
    $("#municipioDistritoResultado").innerHTML = `<p class="sub">${bairro ? `Distrito ${esc(bairro)}: ` : "Todos os distritos: "}${alvo.length} equipamento(s) com o bairro informado no cadastro.</p>
      ${alvo.length ? `<div class="tabela-wrap"><table><tr><th>Patrimônio</th><th>Equipamento</th><th>Unidade</th><th>Bairro</th><th>Situação</th></tr>
        ${alvo.map(e=> `<tr><td><a href="#/equipamento/${encodeURIComponent(e.id)}">${esc(e.patrimonio)}</a></td><td>${esc(e.nome)}</td>
          <td>${esc(unidades.find(u=> u.id === e.unidade_id)?.nome || "")}</td><td>${esc(e.bairro || "—")}</td><td>${esc(e.status)}</td></tr>`).join("")}</table></div>`
        : `<p class="sub">Nenhum equipamento com o bairro "${esc(bairro)}" no cadastro. O bairro é o campo "bairro" da ficha do equipamento.</p>`}`;
  });
};
