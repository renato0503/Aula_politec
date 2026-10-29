/* Mapa de Equipamentos · código do app (o construir.py junta com a base comum) */
"use strict";
const MUNICIPIOS = dadosEmbutidos("municipios") || [];
// Todo registro leva id, datas, origem e exclusão lógica (a consolidação depende disso).
async function novoRegistro(obj){
  const t = agora();
  return {id: uuid(), criadoEm: t, atualizadoEm: t, origem: (await db.meta("unidade_dona")) || estado.perfil || "", excluido: false, ...obj};
}
teste("142 municípios de MT embutidos", ()=> MUNICIPIOS.length === 142 || "recebidos " + MUNICIPIOS.length);
teste("Cuiabá com coordenadas", ()=>{ const c = MUNICIPIOS.find(m=>m.n === "Cuiabá"); return !!(c && c.lat < -15 && c.lon < -55); });
teste("JSZip embutido", ()=> typeof JSZip === "function");
teste("novoRegistro tem id, datas e exclusão lógica", async ()=>{ const r = await novoRegistro({nome: "x"}); return !!(r.id && r.criadoEm && r.excluido === false); });

TELAS["#/mapa"] = async ()=> `<h1>Mapa</h1><p class="sub">O mapa de MT com os pinos chega no Sprint 6. Por enquanto, o resumo da base.</p>
  ${await resumoBase(["unidades", "equipamentos", "contratos", "manutencoes", "paradas"])}
  <p class="sub">${MUNICIPIOS.length} municípios de MT embutidos. Para testar, carregue os dados fictícios em <a href="#/config">Configuração</a>.</p>`;

/* ================= Sprint 2 · Unidades e base de MT ================= */
// RN08: ponto dentro de algum município de MT (teste do raio nos polígonos embutidos)
function dentroDoPoligono(lon, lat, p){
  let dentro = false;
  for (let i = 0, j = p.length - 1; i < p.length; j = i++){
    const [xi, yi] = p[i], [xj, yj] = p[j];
    if ((yi > lat) !== (yj > lat) && lon < (xj - xi) * (lat - yi) / (yj - yi) + xi) dentro = !dentro;
  }
  return dentro;
}
function municipioDoPonto(lat, lon){ return MUNICIPIOS.find(m=>m.p.length && dentroDoPoligono(lon, lat, m.p)) || null; }
const dentroDeMT = (lat, lon)=> !!municipioDoPonto(lat, lon);
teste("RN08: Cuiabá dentro de MT", ()=> dentroDeMT(-15.60, -56.10));
teste("RN08: Goiânia fora de MT", ()=> !dentroDeMT(-16.68, -49.25));
teste("RN08: Porto Velho fora de MT", ()=> !dentroDeMT(-8.76, -63.90));

const TIPOS_UNIDADE = ["sede", "regional", "núcleo", "posto"];

TELAS["#/unidades"] = async ()=>{
  const verExcluidas = (await db.meta("ver_excluidas")) === true;
  const dirs = (await db.list("diretorias")).filter(d=>verExcluidas || !d.excluido);
  const unis = (await db.list("unidades")).filter(u=>verExcluidas || !u.excluido).sort((a, b)=>a.nome.localeCompare(b.nome));
  const nomeDir = id => dirs.find(d=>d.id === id)?.sigla || "";
  return `<h1>Unidades</h1><p class="sub">Diretorias e unidades da POLITEC, com o município e as coordenadas usadas no mapa.</p>
    <div class="card"><h2 style="margin-top:0">Diretorias</h2>
      ${dirs.length ? `<p>${dirs.map(d=>`<span class="selo ${d.excluido ? "erro" : "info"}">${esc(d.sigla)} · ${esc(d.nome)}</span>`).join(" ")}</p>` : `<p class="sub">Nenhuma diretoria.</p>`}
      <form id="formDiretoria" class="campos">${campo("dirNome", "Nome", {obrigatorio: true})}${campo("dirSigla", "Sigla", {obrigatorio: true})}
        <div class="campo"><label>&nbsp;</label><button class="prim" type="submit">Acrescentar diretoria</button></div></form></div>
    <div class="card tabela-wrap"><h2 style="margin-top:0">Unidades (${unis.length})</h2>
      ${unis.length ? `<table><tr><th>Unidade</th><th>Tipo</th><th>Diretoria</th><th>Município</th><th class="num">Latitude</th><th class="num">Longitude</th><th class="num">Atend./dia</th><th></th></tr>
        ${unis.map(u=>`<tr${u.excluido ? ' class="sub"' : ""}><td>${esc(u.nome)}${u.excluido ? ' <span class="selo erro">excluída</span>' : ""}</td><td>${esc(u.tipo)}</td>
          <td>${esc(nomeDir(u.diretoria_id))}</td><td>${esc(u.municipio)}</td><td class="num">${u.latitude ?? ""}</td><td class="num">${u.longitude ?? ""}</td>
          <td class="num">${u.atendimentos_dia ?? ""}</td><td><button data-editar="${esc(u.id)}">Editar</button>
          ${u.excluido ? `<button data-restaurar="${esc(u.id)}">Restaurar</button>` : `<button class="perigo" data-excluir="${esc(u.id)}">Excluir</button>`}</td></tr>`).join("")}</table>`
        : `<p class="sub">Nenhuma unidade. Cadastre abaixo ou carregue os dados fictícios em <a href="#/config">Configuração</a>.</p>`}
      <label style="display:inline-flex;gap:6px;align-items:center;margin-top:10px"><input type="checkbox" id="verExcluidas" style="width:auto" ${verExcluidas ? "checked" : ""}> Mostrar excluídas</label></div>
    <form class="card" id="formUnidade"><h2 style="margin-top:0" id="tituloFormUnidade">Nova unidade</h2>
      <input type="hidden" id="uniId"><div class="campos">
      ${campo("uniNome", "Nome", {obrigatorio: true})}
      ${campo("uniTipo", "Tipo", {tipo: "select", opcoes: TIPOS_UNIDADE})}
      ${campo("uniDiretoria", "Diretoria", {tipo: "select", opcoes: [["", "Escolha"], ...dirs.filter(d=>!d.excluido).map(d=>[d.id, d.sigla + " · " + d.nome])], obrigatorio: true})}
      ${campo("uniMunicipio", "Município", {obrigatorio: true, attrs: 'list="listaMunicipios" autocomplete="off"', ajuda: "Digite para buscar entre os 142 municípios de MT."})}
      ${campo("uniLat", "Latitude", {tipo: "number", attrs: 'step="0.0001"', ajuda: "Vem do município; ajuste se precisar."})}
      ${campo("uniLon", "Longitude", {tipo: "number", attrs: 'step="0.0001"'})}
      ${campo("uniHoras", "Horas úteis por dia", {tipo: "number", valor: 8, attrs: 'min="1" max="24"'})}
      ${campo("uniAtend", "Atendimentos por dia", {tipo: "number", valor: 0, attrs: 'min="0"'})}
      </div><datalist id="listaMunicipios">${MUNICIPIOS.map(m=>`<option value="${esc(m.n)}">`).join("")}</datalist>
      <div id="errosUnidade"></div>
      <div class="linha-botoes"><button class="prim" type="submit">Salvar unidade</button><button type="button" id="btnLimparUnidade">Limpar</button></div></form>`;
};

TELAS_DEPOIS["#/unidades"] = ()=>{
  $("#verExcluidas").addEventListener("change", async e=>{ await db.meta("ver_excluidas", e.target.checked); navegar(); });
  $("#formDiretoria").addEventListener("submit", async e=>{
    e.preventDefault(); const nome = valorDe("dirNome"), sigla = valorDe("dirSigla").toUpperCase();
    if (!nome || !sigla) return toast("Informe nome e sigla.");
    await db.put("diretorias", await novoRegistro({nome, sigla})); await registrar("diretoria criada", {detalhe: sigla}); navegar();
  });
  $("#uniMunicipio").addEventListener("change", ()=>{
    const m = MUNICIPIOS.find(x=>normalizar(x.n) === normalizar(valorDe("uniMunicipio")));
    if (m && m.lat !== null){ $("#uniLat").value = m.lat; $("#uniLon").value = m.lon; }
  });
  $("#btnLimparUnidade").addEventListener("click", ()=>{ $("#formUnidade").reset(); $("#uniId").value = ""; $("#tituloFormUnidade").textContent = "Nova unidade"; });
  $$("[data-editar]").forEach(b=>b.addEventListener("click", async ()=>{
    const u = await db.get("unidades", b.dataset.editar);
    $("#uniId").value = u.id; $("#uniNome").value = u.nome; $("#uniTipo").value = u.tipo; $("#uniDiretoria").value = u.diretoria_id;
    $("#uniMunicipio").value = u.municipio; $("#uniLat").value = u.latitude ?? ""; $("#uniLon").value = u.longitude ?? "";
    $("#uniHoras").value = u.horas_uteis_dia ?? 8; $("#uniAtend").value = u.atendimentos_dia ?? 0;
    $("#tituloFormUnidade").textContent = "Editar " + u.nome; $("#formUnidade").scrollIntoView();
  }));
  const marcar = (attr, valor, acao)=> $$(`[${attr}]`).forEach(b=>b.addEventListener("click", async ()=>{
    const u = await db.get("unidades", b.getAttribute(attr));
    await db.put("unidades", {...u, excluido: valor, atualizadoEm: agora()}); await registrar(acao, {detalhe: u.nome}); navegar();
  }));
  marcar("data-excluir", true, "unidade excluída"); marcar("data-restaurar", false, "unidade restaurada");
  $("#formUnidade").addEventListener("submit", async e=>{
    e.preventDefault();
    const m = MUNICIPIOS.find(x=>normalizar(x.n) === normalizar(valorDe("uniMunicipio")));
    const lat = Number(valorDe("uniLat")), lon = Number(valorDe("uniLon"));
    const erros = [];
    if (!valorDe("uniNome")) erros.push("Informe o nome da unidade.");
    if (!valorDe("uniDiretoria")) erros.push("Escolha a diretoria.");
    if (!m) erros.push("Escolha um município de MT da lista.");
    if (!valorDe("uniLat") || !valorDe("uniLon") || Number.isNaN(lat) || Number.isNaN(lon)) erros.push("Informe latitude e longitude.");
    else if (!dentroDeMT(lat, lon)) erros.push(`A coordenada ${lat}, ${lon} fica fora de Mato Grosso (RN08).`);
    if (!mostrarErros("#errosUnidade", erros)) return;
    const id = valorDe("uniId"), antes = id ? await db.get("unidades", id) : null;
    const dados = {nome: valorDe("uniNome"), tipo: valorDe("uniTipo"), diretoria_id: valorDe("uniDiretoria"), municipio: m.n, municipio_ibge: m.c,
      latitude: lat, longitude: lon, horas_uteis_dia: Number(valorDe("uniHoras")) || 8, atendimentos_dia: Number(valorDe("uniAtend")) || 0};
    const reg = antes ? {...antes, ...dados, atualizadoEm: agora()} : await novoRegistro(dados);
    await db.put("unidades", reg); await registrar(antes ? "unidade alterada" : "unidade criada", {detalhe: reg.nome});
    toast("Unidade salva."); navegar();
  });
};

/* ================= Sprint 3 · Equipamentos e fotos ================= */
const STATUS_EQ = ["operando", "parado", "em manutenção", "baixado"];
const SETORES_EQ = ["Laboratório", "Identificação", "Necropsia", "Local de crime", "Administrativo"];
const MAX_FOTOS = 3;
async function guardarFoto(file){
  const grande = await reduzirImagem(file, 1280, 0.75), mini = await reduzirImagem(file, 240, 0.7);
  const id = uuid();
  await db.put("arquivos", {id, tipo: "foto", mime: "image/jpeg", blob: grande, tamanho: grande.size, criadoEm: agora()});
  await db.put("arquivos", {id: id + "-mini", tipo: "miniatura", mime: "image/jpeg", blob: mini, tamanho: mini.size, criadoEm: agora()});
  return id;
}
const urlFoto = async (id, mini)=>{ const a = await db.get("arquivos", mini ? id + "-mini" : id); return a ? URL.createObjectURL(a.blob) : ""; };

function filtrosEq(){ return estado.filtrosEq || (estado.filtrosEq = {busca: "", unidade: "", tipo: "", status: "", crit: "", ordem: "patrimonio"}); }
TELAS["#/equipamentos"] = async ()=>{
  const f = filtrosEq(), unidades = (await db.list("unidades")).filter(u=>!u.excluido), nomeU = Object.fromEntries(unidades.map(u=>[u.id, u.nome]));
  let eqs = (await db.list("equipamentos")).filter(e=>!e.excluido);
  if (estado.perfil === "unidade"){ const dona = await db.meta("unidade_dona"); if (dona) eqs = eqs.filter(e=>e.unidade_id === dona); }
  const tipos = [...new Set(eqs.map(e=>e.tipo))].sort();
  const b = normalizar(f.busca);
  const vis = eqs.filter(e=>(!b || normalizar(`${e.patrimonio} ${e.nome} ${e.modelo} ${e.numero_serie}`).includes(b)) && (!f.unidade || e.unidade_id === f.unidade)
    && (!f.tipo || e.tipo === f.tipo) && (!f.status || e.status === f.status) && (!f.crit || String(e.criticidade) === f.crit))
    .sort((x, y)=> f.ordem === "criticidade" ? y.criticidade - x.criticidade : String(x[f.ordem] ?? "").localeCompare(String(y[f.ordem] ?? "")));
  estado.eqVisiveis = vis.map(e=>({...e, unidade: nomeU[e.unidade_id] || ""}));
  return `<h1>Equipamentos</h1><p class="sub"><span id="qtdEq">${vis.length}</span> de ${eqs.length} equipamentos.
    <a href="#/equipamento/novo">Cadastrar equipamento</a></p>
    <div class="card"><div class="campos">
      ${campo("fBusca", "Busca (patrimônio, nome, modelo, série)", {valor: f.busca})}
      ${campo("fUnidade", "Unidade", {tipo: "select", opcoes: [["", "Todas"], ...unidades.map(u=>[u.id, u.nome])], valor: f.unidade})}
      ${campo("fTipo", "Tipo", {tipo: "select", opcoes: [["", "Todos"], ...tipos], valor: f.tipo})}
      ${campo("fStatus", "Situação", {tipo: "select", opcoes: [["", "Todas"], ...STATUS_EQ], valor: f.status})}
      ${campo("fCrit", "Criticidade", {tipo: "select", opcoes: [["", "Todas"], "5", "4", "3", "2", "1"], valor: f.crit})}
      ${campo("fOrdem", "Ordenar por", {tipo: "select", opcoes: [["patrimonio", "Patrimônio"], ["nome", "Nome"], ["criticidade", "Criticidade"], ["status", "Situação"]], valor: f.ordem})}
    </div><div class="linha-botoes"><button id="btnCsvEq">Exportar CSV</button></div></div>
    <div class="card tabela-wrap"><table><tr><th>Patrimônio</th><th>Equipamento</th><th>Unidade</th><th>Setor</th><th class="num">Crit.</th><th>Contrato</th><th>Situação</th></tr>
      ${vis.slice(0, 300).map(e=>`<tr><td><a href="#/equipamento/${encodeURIComponent(e.id)}">${esc(e.patrimonio)}</a></td><td>${esc(e.nome)}<br><span class="sub">${esc(e.modelo || "")}</span></td>
        <td>${esc(nomeU[e.unidade_id] || "")}</td><td>${esc(e.setor || "")}</td><td class="num">${e.criticidade}</td><td>${e.contrato_id ? '<span class="selo ok">sim</span>' : '<span class="selo alerta">não</span>'}</td>
        <td><span class="selo ${e.status === "operando" ? "ok" : e.status === "baixado" ? "info" : "erro"}">${esc(e.status)}</span></td></tr>`).join("")}</table>
      ${vis.length > 300 ? `<p class="sub">Mostrando 300; refine a busca.</p>` : ""}</div>`;
};
TELAS_DEPOIS["#/equipamentos"] = ()=>{
  const f = filtrosEq();
  [["fBusca", "busca"], ["fUnidade", "unidade"], ["fTipo", "tipo"], ["fStatus", "status"], ["fCrit", "crit"], ["fOrdem", "ordem"]].forEach(([id, k])=>
    $("#" + id).addEventListener(id === "fBusca" ? "change" : "input", e=>{ f[k] = e.target.value; navegar(); }));
  $("#btnCsvEq").addEventListener("click", ()=>{
    const cols = ["patrimonio", "nome", "tipo", "fabricante", "modelo", "numero_serie", "unidade", "setor", "criticidade", "tem_redundancia", "status", "data_aquisicao", "valor_aquisicao", "latitude", "longitude"];
    const cel = v => { const s = String(v ?? ""); return /[;"\n]/.test(s) ? `"${s.replace(/"/g, '""')}"` : s; };
    baixar(`equipamentos-${hojeISO()}.csv`, "﻿" + [cols.join(";"), ...estado.eqVisiveis.map(e=>cols.map(c=>cel(c === "valor_aquisicao" && e[c] != null ? String(e[c]).replace(".", ",") : e[c])).join(";"))].join("\n"), "text/csv;charset=utf-8");
  });
};

async function telaEquipamento({id}){
  const novo = id === "novo", e = novo ? null : await db.get("equipamentos", id);
  if (!novo && !e) return `<div class="card vazio">Equipamento não encontrado. <a href="#/equipamentos">Voltar</a></div>`;
  const unidades = (await db.list("unidades")).filter(u=>!u.excluido), contratos = await db.list("contratos");
  const v = e || {criticidade: 3, status: "operando", tem_redundancia: false, foto_ids: [], unidade_id: (await db.meta("unidade_dona")) || ""};
  const fotos = [];
  for (const fid of v.foto_ids || []) fotos.push({id: fid, url: await urlFoto(fid, true)});
  const unidade = unidades.find(u=>u.id === v.unidade_id);
  const manut = novo ? [] : await db.porIndice("manutencoes", "equipamento_id", id), paradas = novo ? [] : await db.porIndice("paradas", "equipamento_id", id);
  const contrato = contratos.find(c=>c.id === v.contrato_id);
  return `<h1>${novo ? "Novo equipamento" : esc(e.patrimonio + " · " + e.nome)}</h1>
    ${novo ? "" : `<p class="sub">${esc(unidade?.nome || "")} · ${esc(e.setor || "")} · criticidade ${e.criticidade} · <span class="selo info">${esc(e.status)}</span></p>`}
    <div class="card"><h2 style="margin-top:0">Fotos (${fotos.length} de ${MAX_FOTOS})</h2>
      <div style="display:flex;gap:8px;flex-wrap:wrap" id="galeria">${fotos.map(f=>`<figure style="margin:0"><a href="#" data-ver="${f.id}"><img src="${f.url}" alt="Foto do equipamento" style="width:160px;border-radius:8px"></a>
        <figcaption><button data-tirar-foto="${f.id}">Tirar</button></figcaption></figure>`).join("") || '<p class="sub">Sem fotos.</p>'}</div>
      ${fotos.length < MAX_FOTOS ? `<label class="botao" style="margin-top:8px">Tirar ou escolher foto<input type="file" id="inpFoto" accept="image/*" capture="environment" multiple hidden></label>` : ""}
      <p class="sub">Cada foto é reduzida para 1280 px no próprio navegador antes de ser guardada.</p></div>
    <form class="card" id="formEq"><h2 style="margin-top:0">Dados</h2><div class="campos">
      ${campo("ePat", "Patrimônio", {valor: v.patrimonio || "", obrigatorio: true})}
      ${campo("eNome", "Nome", {valor: v.nome || "", obrigatorio: true})}
      ${campo("eTipo", "Tipo", {valor: v.tipo || "", obrigatorio: true, attrs: 'list="listaTipos"'})}
      ${campo("eFab", "Fabricante", {valor: v.fabricante || ""})}${campo("eModelo", "Modelo", {valor: v.modelo || ""})}${campo("eSerie", "Número de série", {valor: v.numero_serie || ""})}
      ${campo("eUnidade", "Unidade", {tipo: "select", opcoes: [["", "Escolha"], ...unidades.map(u=>[u.id, u.nome])], valor: v.unidade_id, obrigatorio: true})}
      ${campo("eSetor", "Setor", {tipo: "select", opcoes: SETORES_EQ, valor: v.setor || SETORES_EQ[0]})}
      ${campo("eCrit", "Criticidade (1 a 5)", {tipo: "select", opcoes: ["1", "2", "3", "4", "5"], valor: String(v.criticidade), ajuda: "5: a parada interrompe o setor."})}
      ${campo("eRed", "Existe outro igual na unidade?", {tipo: "select", opcoes: [["nao", "Não"], ["sim", "Sim"]], valor: v.tem_redundancia ? "sim" : "nao"})}
      ${campo("eStatus", "Situação", {tipo: "select", opcoes: STATUS_EQ, valor: v.status})}
      ${campo("eAquis", "Data de aquisição", {tipo: "date", valor: v.data_aquisicao || ""})}
      ${campo("eValor", "Valor de aquisição (R$)", {valor: v.valor_aquisicao ? dinheiro.fmt(Math.round(v.valor_aquisicao * 100)).replace("R$ ", "") : "", attrs: 'inputmode="decimal"'})}
      ${campo("eContrato", "Contrato de manutenção", {tipo: "select", opcoes: [["", "Sem contrato"], ...contratos.map(c=>[c.id, `${c.numero} · ${c.fornecedor}`])], valor: v.contrato_id || ""})}
    </div><datalist id="listaTipos">${[...new Set((await db.list("equipamentos")).map(x=>x.tipo))].map(t=>`<option value="${esc(t)}">`).join("")}</datalist>
    <div id="errosEq"></div><div class="linha-botoes"><button class="prim" type="submit">Salvar</button><a class="botao" href="#/equipamentos">Voltar</a></div></form>
    ${novo ? "" : `<div class="card"><h2 style="margin-top:0">Contrato</h2>${contrato ? `${esc(contrato.numero)} · ${esc(contrato.fornecedor)} · vigência ${dataCurtaBR(contrato.inicio)} a ${dataCurtaBR(contrato.fim)}` : '<p class="sub">Sem contrato. O controle de contratos chega no Sprint 4.</p>'}</div>
      <div class="card"><h2 style="margin-top:0">Manutenções (${manut.length})</h2><p class="sub">O histórico com comprovantes chega no Sprint 4.</p></div>
      <div class="card"><h2 style="margin-top:0">Paradas (${paradas.length})</h2><p class="sub">O registro de paradas e o custo chegam no Sprint 5.</p></div>`}`;
}
TELAS["#/equipamento/:id"] = telaEquipamento;
TELAS_DEPOIS["#/equipamento/:id"] = async ({id})=>{
  if (!$("#formEq")) return;
  const novo = id === "novo";
  $("#inpFoto")?.addEventListener("change", async ev=>{
    let e = novo ? null : await db.get("equipamentos", id);
    if (!e) return toast("Salve os dados do equipamento antes de acrescentar fotos.");
    const livres = MAX_FOTOS - (e.foto_ids || []).length, arqs = Array.from(ev.target.files).slice(0, livres);
    toast("Reduzindo as fotos...");
    for (const f of arqs){ try { e.foto_ids = [...(e.foto_ids || []), await guardarFoto(f)]; } catch(err){ toast(err.message); } }
    await db.put("equipamentos", {...e, atualizadoEm: agora()}); await registrar("fotos", {detalhe: `${e.patrimonio}: ${arqs.length}`}); navegar();
  });
  $$("[data-tirar-foto]").forEach(b=>b.addEventListener("click", async ()=>{
    const e = await db.get("equipamentos", id), fid = b.dataset.tirarFoto;
    await db.del("arquivos", fid); await db.del("arquivos", fid + "-mini");
    await db.put("equipamentos", {...e, foto_ids: e.foto_ids.filter(x=>x !== fid), atualizadoEm: agora()}); navegar();
  }));
  $$("[data-ver]").forEach(a=>a.addEventListener("click", async ev=>{ ev.preventDefault(); window.open(await urlFoto(a.dataset.ver, false), "_blank"); }));
  $("#formEq").addEventListener("submit", async ev=>{
    ev.preventDefault();
    const d = {patrimonio: valorDe("ePat"), nome: valorDe("eNome"), tipo: valorDe("eTipo"), fabricante: valorDe("eFab"), modelo: valorDe("eModelo"),
      numero_serie: valorDe("eSerie"), unidade_id: valorDe("eUnidade"), setor: valorDe("eSetor"), criticidade: Number(valorDe("eCrit")),
      tem_redundancia: valorDe("eRed") === "sim", status: valorDe("eStatus"), data_aquisicao: valorDe("eAquis"),
      valor_aquisicao: valorDe("eValor") ? (dinheiro.de(valorDe("eValor")) || 0) / 100 : null, contrato_id: valorDe("eContrato") || null};
    const erros = [];
    if (!d.patrimonio) erros.push("Informe o patrimônio.");
    if (!d.nome) erros.push("Informe o nome.");
    if (!d.tipo) erros.push("Informe o tipo.");
    if (!d.unidade_id) erros.push("Escolha a unidade.");
    const dup = (await db.porIndice("equipamentos", "patrimonio", d.patrimonio)).filter(x=>x.id !== id && !x.excluido);
    if (dup.length) erros.push(`O patrimônio ${d.patrimonio} já está cadastrado (${dup[0].nome}).`);
    if (!mostrarErros("#errosEq", erros)) return;
    const u = await db.get("unidades", d.unidade_id), antes = novo ? null : await db.get("equipamentos", id);
    const reg = antes ? {...antes, ...d, atualizadoEm: agora()} : await novoRegistro({...d, foto_ids: [], latitude: u?.latitude ?? null, longitude: u?.longitude ?? null});
    if (antes && antes.unidade_id !== d.unidade_id){ reg.latitude = u?.latitude ?? null; reg.longitude = u?.longitude ?? null; }
    // a cobertura fica nos dois lados: equipamento.contrato_id e contrato.equipamento_ids
    for (const c of await db.list("contratos")){
      const tem = (c.equipamento_ids || []).includes(reg.id), deve = c.id === reg.contrato_id;
      if (tem !== deve) await db.put("contratos", {...c, equipamento_ids: deve ? [...(c.equipamento_ids || []), reg.id] : c.equipamento_ids.filter(x=>x !== reg.id)});
    }
    await db.put("equipamentos", reg); await registrar(antes ? "equipamento alterado" : "equipamento criado", {detalhe: reg.patrimonio});
    toast("Equipamento salvo."); location.hash = "#/equipamento/" + encodeURIComponent(reg.id);
  });
};
