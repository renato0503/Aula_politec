/* NIHDE · desaparecidos e fontes (CNPD/MJ e NamUs)
   Módulo de consulta dos dados públicos coletados fora do MVP.
   Fundo do mapa: malhas do IBGE (Brasil) e dos EUA, embutidas; sem tiles e sem rede. */
"use strict";

const DES_CNPD = dadosEmbutidos("cnpd");
const DES_NAMUS = dadosEmbutidos("namus");
const DES_CATALOGO = dadosEmbutidos("fontes");
const DES_MUNICIPIOS = dadosEmbutidos("municipios_cnpd") || {};
const DES_GEO_BR = dadosEmbutidos("brasil_ufs");
const DES_GEO_US = dadosEmbutidos("eua_ufs");

const DES_INFO = {
  cnpd: {
    nome: "CNPD/MJ",
    curto: "CNPD · Brasil",
    cor: "#5b4b8a",
    malha: "IBGE",
    geo: DES_GEO_BR,
    nota: "Recorte público do CNPD em 03/11/2026: 381 registros em 16 UFs. Não é o total nacional."
  },
  namus: {
    nome: "NamUs",
    curto: "NamUs · EUA",
    cor: "#b7791f",
    malha: "US Census",
    geo: DES_GEO_US,
    nota: "Amostra de 300 dos 26.607 casos publicados no NamUs (os mais recentes por data do último contato)."
  }
};

const DES = { fonte: "cnpd", q: "", uf: "", sexo: "", faixa: "", ordem: "recente", visiveis: 80 };
let DES_MAPA = null;

const DES_FAIXAS = ["0-11", "12-17", "18-29", "30-44", "45-59", "60+", "sem"];
const DES_FAIXA_ROTULO = {
  "0-11": "0 a 11 anos", "12-17": "12 a 17 anos", "18-29": "18 a 29 anos",
  "30-44": "30 a 44 anos", "45-59": "45 a 59 anos", "60+": "60 anos ou mais", "sem": "Sem informação"
};
const DES_STATUS = {
  integrada: ["ok", "integrada"],
  restrita: ["erro", "acesso restrito"],
  pesquisada: ["info", "pesquisada"],
  planejada: ["alerta", "planejada"],
  referencia: ["info", "referência"]
};

teste("Desaparecidos: CNPD carregado", ()=> (DES_CNPD?.registros || []).length >= 300);
teste("Desaparecidos: NamUs com coordenadas", ()=> (DES_NAMUS?.registros || []).length >= 100 && (DES_NAMUS.registros || []).every(p=>p.lat != null && p.lon != null));
teste("Desaparecidos: malha do Brasil tem 27 UFs", ()=> (DES_GEO_BR?.features || []).length === 27);
teste("Desaparecidos: todo registro do CNPD tem coordenada", ()=>{
  const lista = DES_CNPD?.registros || [];
  return lista.every(p=>{
    const { cidade, uf } = desLocal(p);
    return !!(DES_MUNICIPIOS[uf] || {})[desChave(cidade)];
  });
});

function desChave(texto){
  return normalizar(texto).replace(/[^a-z0-9]+/g, " ").replace(/\s+/g, " ").trim();
}

function desLocal(pessoa){
  const local = String(pessoa?.localRegistro || "");
  const uf = String(pessoa?.ufRegistro || "").trim().toUpperCase();
  if (!local.includes("/")) return { cidade: local, uf, local };
  const [cidade, ufLocal] = [local.slice(0, local.lastIndexOf("/")), local.slice(local.lastIndexOf("/") + 1)];
  return { cidade: cidade.trim(), uf: (ufLocal || uf).trim().toUpperCase(), local };
}

function desData(valor){
  if (!valor) return null;
  const s = String(valor).trim();
  let m = /^(\d{2})\/(\d{2})\/(\d{4})$/.exec(s);
  if (m) return new Date(+m[3], +m[2] - 1, +m[1]);
  m = /^(\d{4})-(\d{2})-(\d{2})/.exec(s);
  if (m) return new Date(+m[1], +m[2] - 1, +m[3]);
  return null;
}

const DES_HOJE = (()=>{ const d = new Date(); d.setHours(0, 0, 0, 0); return d; })();

function desDias(pessoa){
  const d = desData(pessoa?.dataDesaparecimento);
  if (!d) return null;
  return Math.max(0, Math.floor((DES_HOJE - d) / 86400000));
}

function desTempo(dias){
  if (dias == null) return "—";
  if (dias === 0) return "hoje";
  if (dias === 1) return "1 dia";
  if (dias < 30) return dias + " dias";
  if (dias < 365) return Math.round(dias / 30) + " meses";
  const anos = Math.floor(dias / 365);
  return anos === 1 ? "1 ano" : anos + " anos";
}

function desFaixa(idade){
  if (idade == null || idade === "" || Number.isNaN(+idade)) return "sem";
  const n = +idade;
  if (n <= 11) return "0-11";
  if (n <= 17) return "12-17";
  if (n <= 29) return "18-29";
  if (n <= 44) return "30-44";
  if (n <= 59) return "45-59";
  return "60+";
}

function desDataBR(valor){
  const d = desData(valor);
  return d ? d.toLocaleDateString("pt-BR") : "—";
}

function desDados(){
  if (DES.fonte === "namus") {
    return (DES_NAMUS?.registros || []).map(p=>({...p, url: p.url || `https://www.namus.gov/MissingPersons/Case#/${p.id}`}));
  }
  return (DES_CNPD?.registros || []).map(p=>({...p, url: `https://cnpd.mj.gov.br/painel-publico/card/${p.id}`}));
}

function desFiltrados(){
  const q = normalizar(DES.q.trim());
  const lista = desDados().filter(p=>{
    if (q && !normalizar(p.nome).includes(q)) return false;
    if (DES.uf && p.ufRegistro !== DES.uf) return false;
    if (DES.sexo && (p.sexo || "Sem informação") !== DES.sexo) return false;
    if (DES.faixa && desFaixa(p.idadeAtual) !== DES.faixa) return false;
    return true;
  });
  const data = p => desData(p.dataRegistroDesaparecimento) || desData(p.dataDesaparecimento) || new Date(0);
  lista.sort((a, b)=>{
    if (DES.ordem === "nome") return String(a.nome).localeCompare(String(b.nome), "pt-BR");
    if (DES.ordem === "tempo") {
      const da = desData(a.dataDesaparecimento), db = desData(b.dataDesaparecimento);
      if (!da && !db) return 0;
      if (!da) return 1;
      if (!db) return -1;
      return da - db;
    }
    return DES.ordem === "antigo" ? data(a) - data(b) : data(b) - data(a);
  });
  return lista;
}

function desAbas(){
  const totalCnpd = DES_CNPD?.total_registros_coletado || (DES_CNPD?.registros || []).length;
  const totalNamus = DES_NAMUS?.total_registros_coletado || (DES_NAMUS?.registros || []).length;
  const totalFontes = (DES_CATALOGO?.fontes || []).length;
  const b = (id, texto, conta) => `<button type="button" class="botao ${DES.fonte === id ? "prim" : ""}" data-des-fonte="${id}" role="tab" aria-selected="${DES.fonte === id}">${esc(texto)} <span class="mono">${conta}</span></button>`;
  return `<div class="des-abas" id="desAbas" role="tablist" aria-label="Fonte de dados">
    ${b("cnpd", "CNPD · Brasil", totalCnpd)}
    ${b("namus", "NamUs · EUA", totalNamus)}
    ${b("fontes", "Fontes", totalFontes)}
  </div>`;
}

function desKpis(lista){
  const criancas = lista.filter(p=>{ const f = desFaixa(p.idadeAtual); return f === "0-11" || f === "12-17"; }).length;
  const idosos = lista.filter(p=>desFaixa(p.idadeAtual) === "60+").length;
  const mulheres = lista.filter(p=>(p.sexo || "").toLowerCase() === "feminino").length;
  const ufs = new Set(lista.map(p=>p.ufRegistro).filter(Boolean)).size;
  const limite = new Date(DES_HOJE); limite.setDate(limite.getDate() - 30);
  const recentes = lista.filter(p=>{ const d = desData(p.dataDesaparecimento); return d && d >= limite; }).length;
  const itens = [
    ["Registros", lista.length, "no recorte filtrado"],
    ["Mulheres", mulheres, "sexo feminino"],
    ["Crianças e adolescentes", criancas, "até 17 anos"],
    ["Idosos", idosos, "60 anos ou mais"],
    ["UFs / estados", ufs, "com registro"],
    ["Últimos 30 dias", recentes, "por data do desaparecimento"]
  ];
  return itens.map(([r, v, n])=>`<div class="card kpi"><div class="v">${fmtNum(v)}</div><div class="r">${esc(r)}</div><div class="sub" style="font-size:11.5px;margin:2px 0 0">${esc(n)}</div></div>`).join("");
}

const fmtNum = n => new Intl.NumberFormat("pt-BR").format(n);

function desOpcoesUf(){
  return [...new Set(desDados().map(p=>p.ufRegistro).filter(Boolean))].sort((a, b)=>String(a).localeCompare(String(b), "pt-BR"));
}

function desOpcoesSexo(){
  return [...new Set(desDados().map(p=>p.sexo || "Sem informação").filter(Boolean))].sort();
}

function desAlturaCm(valor){
  if (valor == null || valor === "") return null;
  const n = Number(String(valor).replace(",", ".").replace(/[^0-9.]/g, ""));
  if (!n) return null;
  return n < 10 ? Math.round(n * 100) : n;
}

function desScore(des, corpo){
  if (!des || !corpo || corpo.identificado || corpo.situacao === "identificado") return null;
  const sd = String(des.sexo || "").toLowerCase(), sc = String(corpo.sexo || "").toLowerCase();
  if (sd && sc && sd !== sc) return null;
  const dd = desData(des.dataDesaparecimento), dc = desData(corpo.data_localizacao);
  if (dd && dc && dc < dd) return null;
  let pontos = 0; const motivos = [];
  if (sd && sc) { pontos += 30; motivos.push("sexo"); }
  const ida = Number(des.idadeAtual), idc = Number(corpo.idade);
  if (Number.isFinite(ida) && Number.isFinite(idc)) {
    const dif = Math.abs(ida - idc);
    if (dif <= 5) { pontos += 25; motivos.push(`idade ±${dif} ano(s)`); }
    else if (dif <= 10) { pontos += 10; motivos.push(`idade ±${dif} anos`); }
  }
  const ad = desAlturaCm(des.altura || des.alturaCm), ac = desAlturaCm(corpo.altura);
  if (ad && ac) {
    const dif = Math.abs(ad - ac);
    if (dif <= 10) { pontos += 20; motivos.push(`altura ±${dif} cm`); }
    else if (dif <= 20) { pontos += 8; motivos.push(`altura ±${dif} cm`); }
  }
  const cidade = normalizar(desLocal(des).cidade), municipio = normalizar(corpo.municipio || "");
  if (cidade && municipio && (cidade === municipio || cidade.includes(municipio) || municipio.includes(cidade))) { pontos += 15; motivos.push("município"); }
  if (dd && dc) {
    const dias = Math.round((dc - dd) / 86400000);
    if (dias >= 0 && dias <= 365) { pontos += 10; motivos.push(`${dias} dia(s) entre o desaparecimento e a localização`); }
  }
  for (const [campo, rotulo] of [["olhos", "olhos"], ["cabelo", "cabelo"], ["pele", "pele"]]) {
    const a = normalizar(des[campo]), b = normalizar(corpo[campo]);
    if (a && b && a === b) { pontos += 3; motivos.push(rotulo); }
  }
  const sinais = normalizar(corpo.sinais || "").split(/\W+/).filter(x=>x.length >= 4);
  const textoDes = normalizar([des.caracteristicas, des.nome].filter(Boolean).join(" "));
  if (sinais.some(s=>textoDes.includes(s))) { pontos += 5; motivos.push("sinais"); }
  return {pontos, motivos};
}

async function desMatchCard(desId){
  const des = desDados().find(p=>String(p.id) === String(desId));
  if (!des) return "";
  const corpos = await db.list("corpos");
  const candidatos = corpos.map(c=>({c, s:desScore(des, c)})).filter(x=>x.s).sort((a, b)=>b.s.pontos - a.s.pontos).slice(0, 10);
  const anteriores = await db.porIndice("correspondencias", "desaparecido_id", des.id);
  return `<h2 style="margin-top:0">Corpos compatíveis · ${esc(des.nome)}</h2>
    <p class="sub">${esc(des.sexo || "")}${des.idadeAtual ? ` · ${esc(des.idadeAtual)} anos` : ""}${des.altura ? ` · ${esc(des.altura)} m` : ""} · ${esc(desLocal(des).local)}. A lista é indício, não identificação; confirme ou descarte com justificativa.</p>
    ${candidatos.length ? `<div class="tabela-wrap"><table id="tabelaMatches"><tr><th>Corpo</th><th>Unidade</th><th>Sexo/idade</th><th>Altura</th><th>Motivos</th><th>Ação</th></tr>
      ${candidatos.map(({c, s})=>`<tr><td><b>${esc(c.protocolo || c.id)}</b><br><span class="sub">${esc(c.municipio || "")}</span></td><td>${esc(c.unidade || "")}</td>
        <td>${esc(c.sexo || "—")} · ${esc(c.idade ?? "—")}</td><td>${esc(c.altura || "—")}</td><td>${esc(s.motivos.join("; "))} · <b>${s.pontos} ponto(s)</b></td>
        <td><button type="button" data-des-confirmar="${esc(c.id)}" data-des-pessoa="${esc(des.id)}">Confirmar</button>
          <button type="button" data-des-descartar="${esc(c.id)}" data-des-pessoa="${esc(des.id)}">Descartar</button>
          <button type="button" data-des-exame="${esc(c.id)}" data-des-pessoa="${esc(des.id)}">Pedir exame</button></td></tr>`).join("")}</table></div>`
      : '<p class="ok-txt">Nenhum corpo compatível pelos filtros atuais.</p>'}
    ${candidatos.length ? `${campo("desMatchJust", "Justificativa da decisão (mínimo de 20 caracteres)", {tipo: "textarea", linhas: 2})}` : ""}
    ${anteriores.length ? `<h3>Decisões registradas</h3><ul>${anteriores.map(x=>`<li><b>${esc(x.corpo_id)}</b> · ${esc(x.status)} · ${dataBR(x.data)} · ${esc(x.justificativa)}</li>`).join("")}</ul>` : ""}
    <div class="linha-botoes"><button type="button" class="sec" id="desMatchFechar">Fechar</button></div>`;
}

async function desRegistrarMatch(desId, corpoId, status){
  const just = (valorDe("desMatchJust") || "").trim();
  if (just.length < 20) return toast("Escreva a justificativa com pelo menos 20 caracteres.");
  const des = desDados().find(p=>String(p.id) === String(desId));
  const corpo = await db.get("corpos", corpoId);
  if (!des || !corpo) return toast("Registro não encontrado.");
  await db.put("correspondencias", {id: uuid(), desaparecido_id: des.id, nome_desaparecido: des.nome, corpo_id: corpoId,
    status, justificativa: just, data: agora(), perfil: estado.perfil});
  await db.put("corpos", {...corpo, correspondencias: [...(corpo.correspondencias || []), {desaparecido_id: des.id, nome_desaparecido: des.nome, status, justificativa: just, data: agora()}]});
  await registrar(`correspondência ${status}`, {corpo_id: corpoId, desaparecido_id: des.id, detalhe: just});
  toast(`Correspondência registrada como ${status}.`);
  const alvo = $("#desMatch"); if (alvo) { alvo.innerHTML = await desMatchCard(desId); alvo.hidden = false; }
}

function desTabela(lista){
  const visiveis = lista.slice(0, DES.visiveis);
  const linhas = visiveis.map(p=>{
    const dias = desDias(p);
    return `<tr>
      <td><a href="${esc(p.url)}" target="_blank" rel="noopener">${esc(p.nome)}</a></td>
      <td class="num">${p.idadeAtual == null || p.idadeAtual === "" ? "—" : esc(p.idadeAtual)}</td>
      <td>${esc(p.sexo || "—")}</td>
      <td>${esc(desLocal(p).cidade)}${p.ufRegistro ? "/" + esc(p.ufRegistro) : ""}</td>
      <td>${desDataBR(p.dataDesaparecimento)}</td>
      <td>${esc(desTempo(dias))}</td>
      <td><span class="selo ${p.flLocalizacaoConfirmada && p.flLocalizacaoConfirmada !== "NAO_CONFIRMADO" ? "ok" : "info"}">${p.flLocalizacaoConfirmada && p.flLocalizacaoConfirmada !== "NAO_CONFIRMADO" ? "localizado" : "não confirmado"}</span></td>
      <td><button type="button" data-des-match="${esc(p.id)}">Ver corpos</button></td>
    </tr>`;
  }).join("");
  return `<div class="card tabela-wrap">
    <h2 style="margin-top:0">${fmtNum(lista.length)} registro(s) <span class="sub" style="font-weight:400">· exibindo ${fmtNum(visiveis.length)}</span></h2>
    <table>
      <thead><tr><th>Nome</th><th class="num">Idade</th><th>Sexo</th><th>Local</th><th>Desaparecido em</th><th>Tempo</th><th>Situação</th><th>Corpos</th></tr></thead>
      <tbody>${linhas || `<tr><td colspan="8" class="vazio">Nenhum registro com estes filtros.</td></tr>`}</tbody>
    </table>
  </div>`;
}

function desTelaFonte(){
  const info = DES_INFO[DES.fonte];
  const lista = desFiltrados();
  const ufs = desOpcoesUf(), sexos = desOpcoesSexo();
  return `<h1>Desaparecidos e fontes</h1>
    <p class="sub">Dados públicos para a busca e a identificação. O CNPD é a fonte nacional do Brasil; o NamUs é a base dos Estados Unidos. O mapa usa a malha das UFs e não acessa a internet.</p>
    ${desAbas()}
    <div class="card" style="border-left:4px solid ${info.cor}">
      <p class="sub" style="margin:0"><b>${esc(info.nome)}</b> · ${esc(info.nota)} <span class="mono">coleta ${esc((DES.fonte === "namus" ? DES_NAMUS?.coletado_em : DES_CNPD?.coletado_em) || "").slice(0, 10)}</span></p>
    </div>
    <div class="grade">${desKpis(lista)}</div>
    <div class="card"><div class="campos">
      ${campo("desQ", "Buscar por nome", {valor: DES.q, attrs: 'autocomplete="off" placeholder="Ex.: Maria, Silva…"'})}
      ${campo("desUf", "UF / estado", {tipo: "select", opcoes: [["", "Todas"], ...ufs.map(u=>[u, u])], valor: DES.uf})}
      ${campo("desSexo", "Sexo", {tipo: "select", opcoes: [["", "Todos"], ...sexos.map(s=>[s, s])], valor: DES.sexo})}
      ${campo("desFaixa", "Faixa etária", {tipo: "select", opcoes: [["", "Todas"], ...DES_FAIXAS.map(f=>[f, DES_FAIXA_ROTULO[f]])], valor: DES.faixa})}
      ${campo("desOrdem", "Ordenar por", {tipo: "select", opcoes: [["recente", "Desaparecimento mais recente"], ["antigo", "Desaparecimento mais antigo"], ["nome", "Nome (A-Z)"], ["tempo", "Mais tempo desaparecido"]], valor: DES.ordem})}
    </div>
    <div class="linha-botoes" style="margin-bottom:0">
      <button type="button" class="prim" id="desCsv">Baixar CSV do recorte</button>
      <button type="button" id="desLimpar">Limpar filtros</button>
    </div></div>
    <div class="card des-mapa-card">
      <div class="des-mapa-topo">
        <div><b>Mapa dos registros</b><p class="sub" style="margin:2px 0 0">Cada círculo é uma localidade; o tamanho acompanha o número de registros.</p></div>
        <div class="des-legenda"><span><i class="des-bolha" style="background:${info.cor}"></i> ${esc(info.nome)}</span><span>Fundo: ${esc(info.malha)}</span></div>
      </div>
      <div id="desMapa" class="des-mapa" role="application" aria-label="Mapa dos registros de desaparecidos"></div>
      <div id="desDetalhe" class="des-detalhe" hidden></div>
      <div class="des-mapa-pe"><span id="desMapaNota">Carregando o mapa…</span><span>Clique em um círculo para ver os nomes · sem ruas: o app não acessa a rede.</span></div>
    </div>
    ${desTabela(lista)}
    <div class="card" id="desMatch" hidden></div>
    ${lista.length > DES.visiveis ? `<div class="linha-botoes"><button type="button" class="prim" id="desMais">Mostrar mais ${fmtNum(Math.min(80, lista.length - DES.visiveis))}</button></div>` : ""}
    <p class="sub">Os nomes e links abrem o cadastro oficial. A foto não é baixada: o app funciona offline e a CSP bloqueia imagens externas. <b>A correspondência entre um desaparecido e um corpo do NIHDE é indício, não identificação</b>; qualquer match passa por revisão humana e auditoria.</p>`;
}

function desMostrarDetalhe(grupo){
  const el = $("#desDetalhe");
  if (!el) return;
  const itens = grupo.itens.map(p=>{
    const dias = desDias(p);
    return `<li><a href="${esc(p.url)}" target="_blank" rel="noopener">${esc(p.nome)}</a> <span class="sub">· ${esc(desTempo(dias))}</span></li>`;
  }).join("");
  el.hidden = false;
  el.innerHTML = `<div class="des-detalhe-cab"><div><b>${esc(grupo.local)}</b><span class="sub"> · ${fmtNum(grupo.itens.length)} registro(s)</span></div>
    <button type="button" id="desDetalheFechar" aria-label="Fechar a lista">×</button></div>
    <ul>${itens}</ul>`;
  $("#desDetalheFechar")?.addEventListener("click", ()=>{ el.hidden = true; el.innerHTML = ""; });
  el.scrollIntoView({ block: "nearest", behavior: "smooth" });
}

function desIniciarMapa(lista){
  const el = $("#desMapa");
  if (!el) return;
  if (typeof L === "undefined" || !DES_INFO[DES.fonte].geo) {
    el.innerHTML = '<div class="vazio" style="margin:16px">Mapa indisponível: biblioteca ou malha não carregada.</div>';
    return;
  }
  if (DES_MAPA) { try { DES_MAPA.remove(); } catch(e){} DES_MAPA = null; }
  const info = DES_INFO[DES.fonte];
  const mapa = L.map(el, { zoomControl: true, attributionControl: true, minZoom: 2, maxZoom: 9 });
  DES_MAPA = mapa;
  const base = L.geoJSON(info.geo, {
    style: { color: "#93a8c4", weight: 0.8, fillColor: "#e9eff7", fillOpacity: 0.92 },
    interactive: false
  }).addTo(mapa);
  try { mapa.fitBounds(base.getBounds(), { padding: [10, 10] }); } catch(e){}
  mapa.attributionControl.setPrefix(false);
  mapa.attributionControl.addAttribution("Malha: " + info.malha);

  const grupos = new Map();
  let sem = 0;
  lista.forEach(p=>{
    let lat = p.lat, lon = p.lon;
    if (DES.fonte === "cnpd") {
      const { cidade, uf } = desLocal(p);
      const coord = (DES_MUNICIPIOS[uf] || {})[desChave(cidade)];
      if (!coord) { sem++; return; }
      [lat, lon] = coord;
    } else if (lat == null || lon == null) {
      sem++; return;
    }
    const k = (p.localRegistro || "?") + "|" + (p.ufRegistro || "");
    if (!grupos.has(k)) grupos.set(k, { local: p.localRegistro || "?", itens: [], lat: 0, lon: 0 });
    const g = grupos.get(k);
    g.itens.push(p); g.lat += lat; g.lon += lon;
  });

  grupos.forEach(g=>{
    const n = g.itens.length;
    g.lat /= n; g.lon /= n;
    const raio = 6 + Math.sqrt(n) * 3;
    const m = L.circleMarker([g.lat, g.lon], {
      radius: raio, color: "#fff", weight: 1, fillColor: info.cor, fillOpacity: 0.72
    });
    m.bindTooltip(`${esc(g.local)} · ${fmtNum(n)}`, { direction: "auto", offset: [0, -4], opacity: 1 });
    m.on("click", ()=> desMostrarDetalhe(g));
    m.addTo(mapa);
  });

  const nota = $("#desMapaNota");
  if (nota) nota.textContent = `${fmtNum(lista.length - sem)} registros no mapa · ${fmtNum(grupos.size)} localidade(s)` + (sem ? ` · ${fmtNum(sem)} sem coordenada` : "");
  setTimeout(()=>{ try { mapa.invalidateSize(); } catch(e){} }, 120);
}

function desCsv(){
  const lista = desFiltrados();
  const cols = ["fonte", "id", "nome", "idade", "sexo", "local", "uf", "data_desaparecimento", "situacao", "url", "coletado_em"];
  const coleta = DES.fonte === "namus" ? (DES_NAMUS?.coletado_em || "") : (DES_CNPD?.coletado_em || "");
  const linhas = [cols.join(";")].concat(lista.map(p=>[
    DES_INFO[DES.fonte].nome, p.id, p.nome, p.idadeAtual ?? "", p.sexo || "",
    p.localRegistro || "", p.ufRegistro || "", p.dataDesaparecimento || "",
    p.flLocalizacaoConfirmada || "", p.url || "", coleta
  ].map(v=>/[;"\n]/.test(String(v)) ? `"${String(v).replace(/"/g, '""')}"` : String(v)).join(";")));
  baixar(`desaparecidos-${DES.fonte}-${hojeISO()}.csv`, "\ufeff" + linhas.join("\r\n"), "text/csv;charset=utf-8");
  toast(`${fmtNum(lista.length)} registros exportados.`);
}

function desTelaFontes(){
  const fontes = DES_CATALOGO?.fontes || [];
  const conta = s => fontes.filter(f=>f.status === s).length;
  const linhas = fontes.map(f=>{
    const [classe, rotulo] = DES_STATUS[f.status] || ["info", f.status];
    const link = f.url ? `<a href="${esc(f.url)}" target="_blank" rel="noopener">abrir</a>` : "—";
    return `<tr>
      <td><b>${esc(f.nome)}</b><br><span class="sub" style="font-size:11.5px">${esc(f.ref)}</span></td>
      <td>${esc(f.pais)}</td>
      <td>${esc(f.dados)}</td>
      <td>${esc(f.acesso)}</td>
      <td><span class="selo ${classe}">${esc(rotulo)}</span></td>
      <td>${link}</td>
    </tr>`;
  }).join("");
  return `<h1>Fontes de dados</h1>
    <p class="sub">O que existe para buscar pessoas desaparecidas e corpos não identificados, o que é público e o que exige credencial. A leitura parte do guia Rede PCI Conecta (CONDPCI/MJSP, 2025) e de pesquisa nas fontes oficiais.</p>
    ${desAbas()}
    <div class="grade">
      <div class="card kpi"><div class="v">${conta("integrada")}</div><div class="r">integradas neste módulo</div></div>
      <div class="card kpi"><div class="v">${conta("pesquisada")}</div><div class="r">pesquisadas, prontas para integrar</div></div>
      <div class="card kpi"><div class="v">${conta("restrita")}</div><div class="r">com acesso restrito</div></div>
      <div class="card kpi"><div class="v">${conta("planejada") + conta("referencia")}</div><div class="r">em implantação ou referência</div></div>
    </div>
    <div class="card tabela-wrap">
      <h2 style="margin-top:0">Catálogo</h2>
      <table>
        <thead><tr><th>Fonte</th><th>Escopo</th><th>O que oferece</th><th>Acesso</th><th>Status</th><th>Link</th></tr></thead>
        <tbody>${linhas}</tbody>
      </table>
    </div>
    <div class="card">
      <h2 style="margin-top:0">Como os dados chegam aqui</h2>
      <p class="sub">O CNPD é lido pelo endpoint público do painel; o NamUs é lido pela API do próprio site com <b>Scrapling</b>. A coleta roda fora do app, grava um JSON e o <code>construir.py</code> embute o resultado no <code>index.html</code>. O app não faz requisição de rede.</p>
      <pre class="mono" style="white-space:pre-wrap;margin:0 0 10px">python coletar_dados.py              # CNPD: 13 páginas, 381 registros
python coletar_namus.py --limite 300  # NamUs: amostra com Scrapling
python preparar_mapa.py              # malhas e municípios do mapa
python construir.py                  # gera o index.html</pre>
      <p class="sub" style="margin:0">O catálogo completo, com páginas do guia e observações de acesso, está em <a href="FONTES.md" target="_blank" rel="noopener">FONTES.md</a>. A análise da API do CNPD está em <a href="ANALISE-API-CNPD.md" target="_blank" rel="noopener">ANALISE-API-CNPD.md</a>.</p>
    </div>
    <div class="card">
      <h2 style="margin-top:0">Limites e cuidados</h2>
      <p class="sub" style="margin:0">O painel público do CNPD devolve um recorte, não o total nacional. O NamUs é dos Estados Unidos e a amostra não representa o país. SINALID, CADÊ, SINESP, RIBPG, SINAB e Atena exigem credencial institucional e não foram coletados. Os dados são pessoais: use apenas para busca e identificação, sem contato com famílias nem cruzamento nominal fora da finalidade (LGPD). <b>A correspondência com um corpo do NIHDE é indício, não identificação</b>; o servidor do NIHDE confirma ou descarta, com justificativa na auditoria.</p>
    </div>`;
}

TELAS["#/desaparecidos"] = async ()=>{
  if (DES.fonte === "fontes") return desTelaFontes();
  return desTelaFonte();
};

TELAS_DEPOIS["#/desaparecidos"] = ()=>{
  if (DES_MAPA) { try { DES_MAPA.remove(); } catch(e){} DES_MAPA = null; }
  const trocar = ()=> navegar();
  $$("#desAbas [data-des-fonte]").forEach(b=>b.addEventListener("click", ()=>{
    DES.fonte = b.dataset.desFonte;
    DES.q = ""; DES.uf = ""; DES.sexo = ""; DES.faixa = ""; DES.ordem = "recente"; DES.visiveis = 80;
    navegar();
  }));
  let timer = null;
  $("#desQ")?.addEventListener("input", e=>{
    clearTimeout(timer);
    const v = e.target.value;
    timer = setTimeout(()=>{ DES.q = v; DES.visiveis = 80; trocar(); }, 260);
  });
  for (const [id, chave] of [["desUf", "uf"], ["desSexo", "sexo"], ["desFaixa", "faixa"], ["desOrdem", "ordem"]]) {
    $("#" + id)?.addEventListener("change", e=>{
      DES[chave] = e.target.value; DES.visiveis = 80; trocar();
    });
  }
  $("#desLimpar")?.addEventListener("click", ()=>{
    DES.q = ""; DES.uf = ""; DES.sexo = ""; DES.faixa = ""; DES.ordem = "recente"; DES.visiveis = 80;
    trocar();
  });
  $("#desCsv")?.addEventListener("click", desCsv);
  $$("[data-des-match]").forEach(b=>b.addEventListener("click", async ()=>{
    const alvo = $("#desMatch"); if (!alvo) return;
    alvo.innerHTML = await desMatchCard(b.dataset.desMatch); alvo.hidden = false; alvo.scrollIntoView({block: "nearest", behavior: "smooth"});
  }));
  $$("[data-des-confirmar], [data-des-descartar], [data-des-exame]").forEach(b=>b.addEventListener("click", ()=>{
    const status = b.dataset.desConfirmar ? "confirmado" : b.dataset.desDescartar ? "descartado" : "exame complementar";
    const corpoId = b.dataset.desConfirmar || b.dataset.desDescartar || b.dataset.desExame;
    desRegistrarMatch(b.dataset.desPessoa, corpoId, status);
  }));
  $("#desMatch")?.addEventListener("click", async e=>{
    if (e.target.id === "desMatchFechar") { const el = $("#desMatch"); el.hidden = true; el.innerHTML = ""; return; }
    const b = e.target.closest("[data-des-confirmar], [data-des-descartar], [data-des-exame]");
    if (!b) return;
    const status = b.dataset.desConfirmar ? "confirmado" : b.dataset.desDescartar ? "descartado" : "exame complementar";
    const corpoId = b.dataset.desConfirmar || b.dataset.desDescartar || b.dataset.desExame;
    await desRegistrarMatch(b.dataset.desPessoa, corpoId, status);
  });
  $("#desMais")?.addEventListener("click", ()=>{ DES.visiveis += 80; trocar(); });
  if (DES.fonte !== "fontes") desIniciarMapa(desFiltrados());
};
