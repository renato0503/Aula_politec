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
    </tr>`;
  }).join("");
  return `<div class="card tabela-wrap">
    <h2 style="margin-top:0">${fmtNum(lista.length)} registro(s) <span class="sub" style="font-weight:400">· exibindo ${fmtNum(visiveis.length)}</span></h2>
    <table>
      <thead><tr><th>Nome</th><th class="num">Idade</th><th>Sexo</th><th>Local</th><th>Desaparecido em</th><th>Tempo</th><th>Situação</th></tr></thead>
      <tbody>${linhas || `<tr><td colspan="7" class="vazio">Nenhum registro com estes filtros.</td></tr>`}</tbody>
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
      <div class="des-mapa-pe"><span id="desMapaNota">Carregando o mapa…</span><span>Sem ruas: o app não acessa a rede.</span></div>
    </div>
    ${desTabela(lista)}
    ${lista.length > DES.visiveis ? `<div class="linha-botoes"><button type="button" class="prim" id="desMais">Mostrar mais ${fmtNum(Math.min(80, lista.length - DES.visiveis))}</button></div>` : ""}
    <p class="sub">Os nomes e links abrem o cadastro oficial. A foto não é baixada: o app funciona offline e a CSP bloqueia imagens externas.</p>`;
}

function desPopup(grupo){
  const itens = grupo.itens.slice(0, 6).map(p=>`<li><a href="${esc(p.url)}" target="_blank" rel="noopener">${esc(p.nome)}</a></li>`).join("");
  const resto = grupo.itens.length > 6 ? `<li>… e mais ${fmtNum(grupo.itens.length - 6)}</li>` : "";
  return `<div class="des-pop"><b>${esc(grupo.local)}</b><br><span>${fmtNum(grupo.itens.length)} registro(s)</span><ul>${itens}${resto}</ul></div>`;
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
    m.bindTooltip(`${esc(g.local)} · ${fmtNum(n)}`, { direction: "top" });
    m.bindPopup(desPopup(g), { maxWidth: 300 });
    m.addTo(mapa);
  });

  const nota = $("#desMapaNota");
  if (nota) nota.textContent = `${fmtNum(lista.length - sem)} registros no mapa · ${fmtNum(grupos.size)} localidade(s)` + (sem ? ` · ${fmtNum(sem)} sem coordenada` : "");
  setTimeout(()=>{ try { mapa.invalidateSize(); } catch(e){} }, 120);
}

function desCsv(){
  const lista = desFiltrados();
  const cols = ["fonte", "id", "nome", "idade", "sexo", "local", "uf", "data_desaparecimento", "situacao", "url"];
  const linhas = [cols.join(";")].concat(lista.map(p=>[
    DES_INFO[DES.fonte].nome, p.id, p.nome, p.idadeAtual ?? "", p.sexo || "",
    p.localRegistro || "", p.ufRegistro || "", p.dataDesaparecimento || "",
    p.flLocalizacaoConfirmada || "", p.url || ""
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
      <p class="sub" style="margin:0">O painel público do CNPD devolve um recorte, não o total nacional. O NamUs é dos Estados Unidos e a amostra não representa o país. SINALID, CADÊ, SINESP, RIBPG, SINAB e Atena exigem credencial institucional e não foram coletados. Os dados são pessoais: use apenas para busca e identificação, sem contato com famílias nem cruzamento nominal fora da finalidade (LGPD).</p>
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
  $("#desMais")?.addEventListener("click", ()=>{ DES.visiveis += 80; trocar(); });
  if (DES.fonte !== "fontes") desIniciarMapa(desFiltrados());
};
