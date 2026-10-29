/* Custódia Definitiva · código do app (Sprints 1 e 2) */
"use strict";
const CD_STATUS = ["armazenado", "pendencia", "descartado"];
const CD_DIAS = (a, b)=> Math.round((new Date(b) - new Date(a)) / 86400000);
const cdSomarDias = (iso, n)=>{ const d = new Date(iso + "T12:00:00"); d.setDate(d.getDate() + n); return d.toISOString().slice(0, 10); };

teste("Exemplo com 5 categorias, 5 contêineres e 30 vestígios", ()=>{
  const s = dadosEmbutidos("seed");
  return s.categorias.length === 5 && s.conteineres.length === 5 && s.vestigios.length === 30 && s.historico_mensal.length === 12;
});

async function cdCategorias(){ return Object.fromEntries((await db.list("categorias")).map(c=>[c.id_categoria, c])); }
async function cdConteineres(){ return Object.fromEntries((await db.list("conteineres")).map(c=>[c.id_conteiner, c])); }

// ocupação é sempre calculada a partir dos vestígios armazenados (nunca de um número digitado)
function cdOcupados(vestigios, conteinerId){
  const v = vestigios.filter(x=>x.status !== "descartado" && x.conteiner_id && (!conteinerId || x.conteiner_id === conteinerId));
  return v.reduce((a, x)=>a + Number(x.volume_ocupado || 0), 0);
}
function cdFolga(c, vestigios){ return Math.max(0, Number(c.capacidade) - cdOcupados(vestigios, c.id_conteiner)); }

// RN02: contêiner compatível com a categoria; RN03: precisa de folga para o volume
function cdSugerir(vestigios, categoriaId, volume, conteineres){
  const c = (categoriaId && conteineres.find(x=>x.id_conteiner === categoriaId));
  const compativeis = conteineres.filter(x=>x.status !== "inativo" && (x.categoria_permitida === categoriaId || x.categoria_permitida === "todas"));
  const cabe = compativeis.filter(x=>cdFolga(x, vestigios) >= volume).sort((a, b)=>cdFolga(a, vestigios) - cdFolga(b, vestigios));
  return {conteiner: cabe[0] || null, categoria: c || null, compativeis: compativeis.length};
}
teste("RN02/RN03: sugere o contêiner compatível com folga e recusa volume acima da capacidade", ()=>{
  const cs = [{id_conteiner: "A", categoria_permitida: "cat1", capacidade: 10, status: "ativo"},
              {id_conteiner: "B", categoria_permitida: "cat1", capacidade: 20, status: "ativo"},
              {id_conteiner: "C", categoria_permitida: "cat2", capacidade: 50, status: "ativo"}];
  const vs = [{conteiner_id: "A", volume_ocupado: 6, status: "armazenado"}];
  const s = cdSugerir(vs, "cat1", 5, cs);
  return s.conteiner.id_conteiner === "B" && cdSugerir(vs, "cat1", 3, cs).conteiner.id_conteiner === "A" && cdSugerir(vs, "cat1", 60, cs).conteiner === null && s.compativeis === 2;
});

function cdSemaforo(pct){ return pct >= 100 ? "erro" : pct >= 85 ? "alerta" : "ok"; }

TELAS["#/painel"] = async ()=>{
  const [vs, cs, cats] = await Promise.all([db.list("vestigios"), db.list("conteineres"), cdCategorias()]);
  const ativos = vs.filter(v=>v.status !== "descartado"), ocup = cdOcupados(vs), cap = cs.reduce((a, c)=>a + Number(c.capacidade), 0);
  const pct = cap ? Math.round(ocup / cap * 100) : 0;
  const cheios = cs.filter(c=>cdFolga(c, vs) === 0).length, pend = vs.filter(v=>v.status === "pendencia").length;
  return `<h1>Painel da Central de Custódia</h1><p class="sub">${ativos.length} vestígios armazenados. <a href="#/vestigio/novo">Cadastrar vestígio</a></p>
    <div class="grade"><div class="card kpi"><div class="v">${ativos.length}</div><div class="r">vestígios no acervo</div></div>
      <div class="card kpi"><div class="v">${pct}%</div><div class="r">ocupação total (${ocup} de ${cap})</div></div>
      <div class="card kpi"><div class="v">${cheios}</div><div class="r">contêineres cheios</div></div>
      <div class="card kpi"><div class="v">${pend}</div><div class="r">com pendência documental</div></div></div>
    <div class="card tabela-wrap"><h2 style="margin-top:0">Ocupação por contêiner</h2><table id="tabelaOcupacao"><tr><th>Contêiner</th><th>Categoria permitida</th><th class="num">Ocupado</th><th class="num">Capacidade</th><th>Ocupação</th></tr>
      ${cs.map(c=>{ const o = cdOcupados(vs, c.id_conteiner), p = Number(c.capacidade) ? Math.round(o / Number(c.capacidade) * 100) : 0;
        return `<tr><td><a href="#/conteineres">${esc(c.id_conteiner)}</a></td><td>${esc(cats[c.categoria_permitida]?.nome || (c.categoria_permitida === "todas" ? "todas" : c.categoria_permitida))}</td>
          <td class="num">${o}</td><td class="num">${c.capacidade}</td><td><span class="selo ${cdSemaforo(p)}">${p}%</span></td></tr>`; }).join("")}</table></div>`;
};

TELAS["#/conteineres"] = async ()=>{
  const [vs, cs, cats] = await Promise.all([db.list("vestigios"), db.list("conteineres"), cdCategorias()]);
  return `<h1>Contêineres</h1><p class="sub">Capacidade e condição de conservação de cada unidade de armazenamento.</p>
    <div class="grade">${cs.map(c=>{ const o = cdOcupados(vs, c.id_conteiner), f = cdFolga(c, vs), p = Number(c.capacidade) ? Math.round(o / Number(c.capacidade) * 100) : 0;
      return `<div class="card"><b>${esc(c.id_conteiner)}</b> <span class="selo ${cdSemaforo(p)}">${p}%</span>
        <p class="sub">${esc(c.tipo_conservacao)} · ${esc(c.localizacao_fisica || "")}</p>
        <p>Categoria: ${esc(cats[c.categoria_permitida]?.nome || "todas")}<br>Ocupado: ${o} de ${c.capacidade} (folga ${f})</p></div>`; }).join("")}</div>`;
};

function cdFiltros(){ return estado.cdFiltros || (estado.cdFiltros = {categoria: "", conteiner: "", status: "", busca: ""}); }
TELAS["#/vestigios"] = async ()=>{
  const f = cdFiltros(), [vs, cs, cats] = await Promise.all([db.list("vestigios"), cdConteineres(), cdCategorias()]);
  const b = normalizar(f.busca);
  const lista = vs.filter(v=>(!f.categoria || v.categoria_id === f.categoria) && (!f.conteiner || v.conteiner_id === f.conteiner)
      && (!f.status || v.status === f.status) && (!b || normalizar(`${v.id_vestigio} ${v.protocolo} ${v.lacre} ${v.descricao || ""}`).includes(b)))
    .sort((a, b2)=>(b2.data_entrada || "").localeCompare(a.data_entrada || ""));
  return `<h1>Vestígios <span class="sub">(${lista.length})</span></h1><p class="sub"><a href="#/vestigio/novo">Cadastrar vestígio</a></p>
    <div class="card"><div class="campos">
      ${campo("cdBusca", "Busca por protocolo, lacre ou descrição", {valor: f.busca})}
      ${campo("cdCat", "Categoria", {tipo: "select", opcoes: [["", "Todas"], ...Object.values(cats).map(c=>[c.id_categoria, c.nome])], valor: f.categoria})}
      ${campo("cdCont", "Contêiner", {tipo: "select", opcoes: [["", "Todos"], ...Object.keys(cs).sort()], valor: f.conteiner})}
      ${campo("cdStatus", "Situação", {tipo: "select", opcoes: [["", "Todas"], ...CD_STATUS.map(s=>[s, s])], valor: f.status})}</div></div>
    <div class="card tabela-wrap"><table><tr><th>Vestígio</th><th>Protocolo</th><th>Lacre</th><th>Categoria</th><th>Endereço</th><th>Situação</th></tr>
      ${lista.map(v=>`<tr><td><a href="#/vestigio/${encodeURIComponent(v.id_vestigio)}">${esc(v.id_vestigio)}</a></td><td>${esc(v.protocolo)}</td>
        <td class="mono">${esc(v.lacre)}</td><td>${esc(cats[v.categoria_id]?.nome || v.categoria_id)}</td>
        <td>${v.conteiner_id ? esc(v.conteiner_id) + " · " + esc(v.posicao || "") : '<span class="selo alerta">sem endereço</span>'}</td>
        <td><span class="selo ${v.status === "pendencia" ? "alerta" : v.status === "descartado" ? "info" : "ok"}">${esc(v.status)}</span></td></tr>`).join("")
        || '<tr><td colspan="6" class="vazio">Nenhum vestígio com estes filtros.</td></tr>'}</table></div>`;
};
TELAS_DEPOIS["#/vestigios"] = ()=>{
  const f = cdFiltros();
  [["cdBusca", "busca", "change"], ["cdCat", "categoria", "input"], ["cdCont", "conteiner", "input"], ["cdStatus", "status", "input"]].forEach(([id, k, ev])=>
    $("#" + id).addEventListener(ev, e=>{ f[k] = e.target.value; navegar(); }));
};

TELAS["#/vestigio/novo"] = async ()=>{
  const [cs, cats, vs] = await Promise.all([db.list("conteineres"), db.list("categorias"), db.list("vestigios")]);
  return `<h1>Cadastrar vestígio</h1><p class="sub">Use apenas dados fictícios. O endereço é sugerido pela categoria e pela capacidade.</p>
    <form class="card" id="formCdNovo" novalidate><div class="campos">
      ${campo("cdProtocolo", "Protocolo", {obrigatorio: true, ajuda: "Número do procedimento ou da requisição (fictício)."})}
      ${campo("cdLacre", "Lacre", {obrigatorio: true, ajuda: "Identificação única do lacre (RN01)."})}
      ${campo("cdCategoria", "Categoria", {tipo: "select", opcoes: [["", "Escolha"], ...cats.map(c=>[c.id_categoria, c.nome])], obrigatorio: true})}
      ${campo("cdVolume", "Volume ocupado", {tipo: "number", attrs: 'min="1" step="1"', obrigatorio: true, ajuda: "Unidades de ocupação (caixa, alíquota, volume)."})}
      ${campo("cdData", "Data de entrada", {tipo: "date", valor: hojeISO(), obrigatorio: true})}
      ${campo("cdPendencia", "Situação", {tipo: "select", opcoes: [["armazenado", "Armazenado"], ["pendencia", "Pendência documental"]]})}</div>
    ${campo("cdDesc", "Descrição do material", {tipo: "textarea", linhas: 2, ajuda: "Ex.: 12 alíquotas de contraprova de entorpecente."})}
    <div id="cdErros"></div><div class="linha-botoes"><button class="prim" type="submit">Cadastrar e endereçar</button></div></form>`;
};
TELAS_DEPOIS["#/vestigio/novo"] = ()=>{
  $("#formCdNovo").addEventListener("submit", async e=>{
    e.preventDefault();
    const d = {protocolo: valorDe("cdProtocolo"), lacre: valorDe("cdLacre"), categoria_id: valorDe("cdCategoria"), volume_ocupado: Number(valorDe("cdVolume")),
      data_entrada: valorDe("cdData"), status: valorDe("cdPendencia"), descricao: valorDe("cdDesc")};
    const [vs, cs, cats] = await Promise.all([db.list("vestigios"), db.list("conteineres"), db.list("categorias")]);
    const erros = [];
    if (!d.protocolo) erros.push("Informe o protocolo.");
    if (!d.lacre) erros.push("Informe o lacre (RN01).");
    else if (vs.some(v=>v.status !== "descartado" && normalizar(v.lacre) === normalizar(d.lacre))) erros.push(`O lacre ${d.lacre} já está em uso (RN01).`);
    if (!cats.some(c=>c.id_categoria === d.categoria_id)) erros.push("Escolha a categoria.");
    if (!(d.volume_ocupado > 0)) erros.push("O volume precisa ser maior que zero.");
    if (!d.data_entrada || d.data_entrada > hojeISO()) erros.push("Informe uma data de entrada que não seja futura.");
    const s = cdSugerir(vs, d.categoria_id, d.volume_ocupado, cs);
    if (!erros.length && !s.conteiner) erros.push(s.compativeis ? "Não há contêiner compatível com folga para este volume (RN03)." : "Não há contêiner compatível com esta categoria (RN02).");
    if (!mostrarErros("#cdErros", erros)) return;
    const id = "V-" + String(vs.length + 1).padStart(4, "0");
    const pos = String(cdOcupados(vs, s.conteiner.id_conteiner) + 1).padStart(3, "0");
    await db.put("vestigios", {id_vestigio: id, ...d, conteiner_id: s.conteiner.id_conteiner, posicao: `P${pos}`, criado_em: agora()});
    await db.put("movimentacoes", {id_movimentacao: uuid(), vestigio_id: id, tipo: "entrada", data_hora: agora(), responsavel: estado.perfil || "custodia",
      origem: "recebimento", destino: `${s.conteiner.id_conteiner} · P${pos}`});
    await registrar("vestígio cadastrado", {detalhe: `${id} · lacre ${d.lacre}`});
    toast(`Vestígio ${id} endereçado em ${s.conteiner.id_conteiner} (P${pos}).`); location.hash = "#/vestigio/" + encodeURIComponent(id);
  });
};

TELAS["#/vestigio/:id"] = async ({id})=>{
  const v = await db.get("vestigios", id);
  if (!v) return `<div class="card vazio">Vestígio não encontrado. <a href="#/vestigios">Voltar</a></div>`;
  const cats = await cdCategorias(), cs = await cdConteineres(), movs = (await db.porIndice("movimentacoes", "vestigio_id", id)).sort((a, b)=>b.data_hora.localeCompare(a.data_hora));
  return `<h1>${esc(v.id_vestigio)} <span class="selo ${v.status === "pendencia" ? "alerta" : v.status === "descartado" ? "info" : "ok"}">${esc(v.status)}</span></h1>
    <p class="sub">Protocolo ${esc(v.protocolo)} · lacre <span class="mono">${esc(v.lacre)}</span> · entrada em ${dataCurtaBR(v.data_entrada)}</p>
    <div class="grade"><div class="card kpi"><div class="v">${esc(cats[v.categoria_id]?.nome || v.categoria_id)}</div><div class="r">categoria</div></div>
      <div class="card kpi"><div class="v">${v.conteiner_id ? esc(v.conteiner_id) + " · " + esc(v.posicao) : "—"}</div><div class="r">endereço digital</div></div>
      <div class="card kpi"><div class="v">${v.volume_ocupado}</div><div class="r">volume ocupado</div></div></div>
    <div class="card"><h2 style="margin-top:0">Material</h2><p>${esc(v.descricao || "Sem descrição.")}</p>
      <p class="sub">Condição de conservação: ${esc(cs[v.conteiner_id]?.tipo_conservacao || "—")} · localização física: ${esc(cs[v.conteiner_id]?.localizacao_fisica || "—")}</p></div>
    <div class="card tabela-wrap"><h2 style="margin-top:0">Movimentações (RN04)</h2><table id="cdMovs"><tr><th>Data e hora</th><th>Tipo</th><th>Responsável</th><th>Origem</th><th>Destino</th></tr>
      ${movs.map(m=>`<tr><td>${dataBR(m.data_hora)}</td><td>${esc(m.tipo)}</td><td>${esc(m.responsavel)}</td><td>${esc(m.origem)}</td><td>${esc(m.destino)}</td></tr>`).join("")}</table></div>`;
};
