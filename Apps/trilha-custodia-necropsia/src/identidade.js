/* Sistema de Controle de Necropsia · interface do espelho.
   Este arquivo é o espelho do protótipo "Sistema de Controle de Necropsia —
   DMML / POLITEC": a faixa de cabeçalho, o painel de cartões, a lista de corpos
   com filtros, o resumo por agente causal e a ficha do caso com as sete etapas,
   a gaveta lateral, a assinatura no canvas e a janela de justificativa.
   Entra por último no build, depois das regras de src/app.js. */

"use strict";

/* ================= blocos de tela ================= */

function espHero(){
  const p = estado.perfil || "tecnico";
  const perfis = (APP.perfis || []).map(x => `<option value="${esc(x.id)}" ${x.id === p ? "selected" : ""}>${esc(x.nome)}</option>`).join("");
  return `<div class="esp-hero">
    <div class="esp-hero-texto">
      <span class="esp-pill">Protótipo — dados de exemplo</span>
      <h1>Sistema de Controle de Necropsia</h1>
      <p>Gerência de Necropsia — DMML / POLITEC</p>
    </div>
    <div class="esp-hero-perfil">
      <label for="espPerfil">Perfil de acesso</label>
      <select class="esp-input esp-perfil" id="espPerfil" data-esp-perfil>${perfis}</select>
    </div>
    <div class="esp-demo">Protótipo — dados de exemplo</div>
  </div>`;
}

function espTitulo(titulo, sub){
  return `<h2 class="esp-titulo">${esc(titulo)}</h2>${sub ? `<p class="esp-sub">${esc(sub)}</p>` : ""}`;
}

// liga o seletor de perfil da faixa do espelho e volta ao topo da tela
function espLigarHero(){
  if (typeof window !== "undefined") window.scrollTo(0, 0);
  const sel = $("#espPerfil");
  if (sel && !sel.dataset.espLigado){
    sel.dataset.espLigado = "1";
    sel.addEventListener("change", e => trocarPerfil(e.target.value));
  }
}

function espCampo(label, id, valor, tipo = "text", extra = ""){
  return `<div class="esp-field"><label for="${id}">${esc(label)}</label>
    <input class="esp-input" id="${id}" type="${tipo}" value="${esc(valor ?? "")}" data-esp-campo="${id}" ${extra}></div>`;
}
function espArea(label, id, valor){
  return `<div class="esp-field esp-full"><label for="${id}">${esc(label)}</label>
    <textarea class="esp-input" id="${id}" rows="4" data-esp-campo="${id}">${esc(valor ?? "")}</textarea></div>`;
}
function espSel(label, id, opcoes, valor){
  return `<div class="esp-field"><label for="${id}">${esc(label)}</label>
    <select class="esp-input" id="${id}" data-esp-campo="${id}">
      ${opcoes.map(o => { const [v, t] = Array.isArray(o) ? o : [o, o]; return `<option value="${esc(v)}" ${String(v) === String(valor ?? "") ? "selected" : ""}>${esc(t)}</option>`; }).join("")}
    </select></div>`;
}
function espLeitura(label, valor){
  return `<div class="esp-field"><label>${esc(label)}</label><div class="esp-leitura">${esc(valor ?? "—")}</div></div>`;
}
function espSelLeitura(label, opcoes, valor){
  const achado = opcoes.find(o => o[0] === valor);
  return espLeitura(label, achado ? achado[1] : valor);
}

// um selo com a situação do caso
function espSelo(s){
  let cls = "esp-badge";
  if (s === "Custódia finalizada") cls += " esp-badge-ok";
  else if (["Sepultado pelo Estado", "Aguardando identificação", "Aguardando família", "Não reclamado", "Não identificado"].includes(s)) cls += " esp-badge-warn";
  return `<span class="${cls}">${esc(s)}</span>`;
}

/* ================= painel ================= */

const espKPIs = [
  {chave: "todos", titulo: "Casos totais", sub: "todos os registros"},
  {chave: "Ocorrência em andamento", titulo: "Ocorrência em andamento", sub: "em campo"},
  {chave: "Aguardando necropsia", titulo: "Aguardando necropsia", sub: "na fila da base"},
  {chave: "Necropsia em andamento", titulo: "Necropsia em andamento", sub: "bancada ativa"},
  {chave: "Aguardando identificação", titulo: "Aguardando identificação", sub: "sem nome confirmado"},
  {chave: "Aguardando família", titulo: "Aguardando família", sub: "para liberação"},
  {chave: "Aguardando funerária", titulo: "Aguardando funerária", sub: "retirada pendente"},
  {chave: "Sepultado pelo Estado", titulo: "Sepultados pelo Estado", sub: "sepultamento público"},
  {chave: "Custódia finalizada", titulo: "Custódia finalizada", sub: "casos encerrados"},
  {chave: "lacres", titulo: "Lacres pendentes de recebimento", sub: "aguardando ADM", especial: true},
];

function espConta(cs, ls, chave){
  if (chave === "todos") return cs.length;
  if (chave === "lacres") return ls.filter(l => l.coletado !== false && l.codigo && !l.recebido_em).length;
  return cs.filter(c => tcStatus(c) === chave).length;
}

TELAS["#/painel"] = async ()=>{
  const [cs, ls, ms] = await Promise.all([db.list("corpos"), db.list("lacres"), db.list("marcos")]);
  const perfil = estado.perfil || "tecnico";
  const grade = espKPIs.map(k => {
    const n = espConta(cs, ls, k.chave);
    const alerta = k.especial && n > 0 ? " esp-kpi-alerta" : "";
    return `<div class="esp-kpi${alerta}" role="button" tabindex="0" data-esp-kpi="${esc(k.chave)}"
      aria-label="${esc(k.titulo)}: ${n}. ${esc(k.sub)}">
      <div class="esp-kpi-num">${n}</div><div class="esp-kpi-titulo">${esc(k.titulo)}</div><div class="esp-kpi-sub">${esc(k.sub)}</div></div>`;
  }).join("");

  const abertos = cs.filter(c => !c.custodia_finalizada);
  const extra = espBlocosPerfil(perfil, cs, ls, ms, abertos);

  return `<div class="esp">${espHero()}
    <div class="esp-card">
      ${espTitulo("Painel de situação", "Clique em um indicador para ver os casos correspondentes na aba Corpos.")}
      <div class="esp-kpis" id="espKpiGrid">${grade}</div>
      <p class="esp-helper">Os números são calculados a partir dos registros em tempo real.</p>
    </div>
    ${extra}</div>`;
};

// as telas que o app já tinha, por perfil: quadro das etapas, sala de necropsia e fila da ADM
function espBlocosPerfil(perfil, cs, ls, ms, abertos){
  const ultimo = id => ms.filter(m => m.corpo_id === id).sort((a, b) => b.data_hora.localeCompare(a.data_hora))[0];
  const linha = (c) => {
    const u = ultimo(c.id_corpo);
    return `<tr>
      <td><a href="#/corpo/${encodeURIComponent(c.id_corpo)}">${esc(c.protocolo)}</a></td>
      <td>${esc(tcRotuloLista(c))}</td>
      <td><span class="esp-mini">${tcEtapa(c)}. ${esc(TC_ETAPAS[tcEtapa(c) - 1].nome)}</span>
        ${c.identificacao?.pendente ? `<span class="esp-mini esp-mini-alerta">exame complementar: ${esc(c.identificacao.pendente.metodo)}</span>` : ""}</td>
      <td>${esc(c.agente_causal || "—")}</td>
      <td class="num">${tcDias(c)}</td>
      <td class="esp-mini">${u ? esc(u.tipo) + " · " + dataBR(u.data_hora) : "sem movimentação"}</td></tr>`;
  };
  const cabecalho = `<tr><th>Protocolo</th><th>Identificação</th><th>Etapa</th><th>Agente causal</th><th class="num">Dias no IML</th><th>Último marco</th></tr>`;

  if (perfil === "gestor"){
    const lacresPend = ls.filter(l => l.coletado !== false && l.codigo && !l.recebido_em);
    const laudosPend = cs.filter(c => c.laudo?.entregue_em && !c.laudo?.recebido_em);
    const decisoes = cs.filter(c => tcEtapa(c) === 6 && !c.sepultamento && (!c.identificado || c.familia?.busca_sem_sucesso));
    const corpoDe = id => cs.find(c => c.id_corpo === id);
    const fila = [
      ...decisoes.map(c => [c, `decisão de sepultamento (${c.identificado ? "não reclamado" : "não identificado"})`, c.etapa_em]),
      ...laudosPend.map(c => [c, "recebimento do laudo", c.laudo.entregue_em]),
      ...lacresPend.map(l => [corpoDe(l.corpo_id), `recebimento do lacre ${l.codigo} (${l.destino})`, l.data_hora]),
    ].filter(([c]) => c);
    return `<div class="esp-card esp-mt">
      ${espTitulo("Fila da ADM", "Lacres, laudos e decisões de sepultamento que dependem do Gestor ADM.")}
      <div class="esp-kpis">
        <div class="esp-kpi"><div class="esp-kpi-num" data-esp-adm="lacres">${lacresPend.length}</div><div class="esp-kpi-titulo">lacres pendentes</div></div>
        <div class="esp-kpi"><div class="esp-kpi-num" data-esp-adm="laudos">${laudosPend.length}</div><div class="esp-kpi-titulo">laudos aguardando</div></div>
        <div class="esp-kpi"><div class="esp-kpi-num" data-esp-adm="decisoes">${decisoes.length}</div><div class="esp-kpi-titulo">decisões de sepultamento</div></div>
        <div class="esp-kpi"><div class="esp-kpi-num" data-esp-adm="finalizadas">${cs.filter(c => c.custodia_finalizada).length}</div><div class="esp-kpi-titulo">custódias finalizadas</div></div>
      </div>
      <div class="esp-tabela-wrap esp-mt"><table class="esp-tabela">
        <thead><tr><th>Protocolo</th><th>Pendência</th><th>Desde</th></tr></thead>
        <tbody>${fila.map(([c, t, d]) => `<tr><td><a href="#/corpo/${encodeURIComponent(c.id_corpo)}">${esc(c.protocolo)}</a></td>
          <td>${esc(t)}</td><td>${dataBR(d)}</td></tr>`).join("") || '<tr><td colspan="3" class="esp-vazio">Nada pendente na ADM.</td></tr>'}</tbody>
      </table></div>
      <div class="esp-acoes esp-mt">
        <button class="esp-btn esp-btn-outline" id="btnTcCsv" type="button">Exportar CSV</button>
        <button class="esp-btn esp-btn-outline" type="button" onclick="window.print()">Imprimir em A4</button>
      </div>
    </div>`;
  }
  if (perfil === "medico"){
    const sala = cs.filter(c => [3, 4, 5].includes(tcEtapa(c)) && !c.custodia_finalizada).sort((a, b) => tcDias(b) - tcDias(a));
    return `<div class="esp-card esp-mt">
      ${espTitulo("Sala de necropsia", "Corpos da fila da necropsia à identificação. O perfil lê até a etapa 5.")}
      <div class="esp-tabela-wrap"><table class="esp-tabela">
        <thead>${cabecalho}</thead><tbody>${sala.map(linha).join("") || '<tr><td colspan="6" class="esp-vazio">Nenhum corpo na sala.</td></tr>'}</tbody>
      </table></div></div>`;
  }
  const colunas = TC_ETAPAS.map(et => {
    const lista = abertos.filter(c => tcEtapa(c) === et.n);
    return `<section class="esp-coluna"><h3>${et.n}. ${esc(et.nome)} <span class="esp-conta">${lista.length}</span></h3>
      ${lista.length ? lista.map(c => `<a class="esp-cartao" href="#/corpo/${encodeURIComponent(c.id_corpo)}">
        <b class="mono">${esc(c.protocolo)}</b><span>${esc(tcRotuloLista(c))}</span>
        <span class="esp-mini">${plural(tcDias(c), "dia", "dias")} no IML</span></a>`).join("") : '<p class="esp-sub">Nenhum corpo.</p>'}</section>`;
  }).join("");
  return `<div class="esp-card esp-mt">
    ${espTitulo("Quadro das sete etapas", "Casos abertos por etapa, com os dias no IML. Serve também para a passagem de plantão.")}
    <div class="esp-quadro" id="espQuadro">${colunas}</div></div>`;
};

/* ================= lista de corpos ================= */

function espFiltros(){
  return estado.espFiltros || (estado.espFiltros = {status: "", busca: "", de: "", ate: "", lacres: false});
}

function espCasosFiltrados(cs, ls, f){
  return cs.filter(c => {
    if (f.lacres){
      const temPendente = ls.some(l => l.corpo_id === c.id_corpo && l.coletado !== false && l.codigo && !l.recebido_em);
      if (!temPendente) return false;
    } else if (f.status && tcStatus(c) !== f.status) return false;
    if (f.busca){
      const q = normalizar(f.busca);
      const alvo = normalizar([c.protocolo, c.numero_necropsia, c.nome, c.documento, c.municipio, c.ocorrencia?.delegacia].join(" "));
      if (!alvo.includes(q)) return false;
    }
    if (f.de && (c.entrada || "") < f.de) return false;
    if (f.ate && (c.entrada || "") > f.ate) return false;
    return true;
  }).sort((a, b) => (b.entrada || "").localeCompare(a.entrada || ""));
}

TELAS["#/corpos"] = async ()=>{
  const [cs, ls] = await Promise.all([db.list("corpos"), db.list("lacres")]);
  const f = espFiltros();
  const linhas = espCasosFiltrados(cs, ls, f);
  const chip = (f.lacres || f.status)
    ? `<span class="esp-chip">Filtrando por: ${esc(f.lacres ? "Lacres pendentes de recebimento" : f.status)} (${linhas.length} casos)
        <button type="button" data-esp-acao="esp-limpar-filtros" aria-label="Remover filtro">×</button></span>`
    : "";
  const tabela = linhas.length ? `<div class="esp-tabela-wrap">
      <table class="esp-tabela"><thead><tr>
        <th>Protocolo</th><th>Data entrada</th><th>Nome / Possível vítima</th><th>Agente causal</th><th>Status</th><th>Etapa</th><th>Ações</th>
      </tr></thead><tbody>${linhas.map(c => `<tr>
        <td><b>${esc(c.protocolo)}</b></td>
        <td>${esc(dataCurtaBR(c.entrada))}</td>
        <td>${esc(tcRotuloLista(c))}</td>
        <td>${esc(c.agente_causal || "—")}</td>
        <td>${espSelo(tcStatus(c))}</td>
        <td>${espEtapaTexto(c)}</td>
        <td><button class="esp-btn esp-btn-sm esp-btn-outline" type="button" data-esp-acao="esp-ver-detalhes" data-esp-id="${esc(c.id_corpo)}">Ver detalhes</button></td>
      </tr>`).join("")}</tbody></table></div>`
    : `<div class="esp-vazio-caixa"><p>Nenhum caso encontrado para este filtro.</p>
        <button class="esp-btn esp-btn-outline" type="button" data-esp-acao="esp-limpar-filtros">Ver todos os casos</button></div>`;
  const cartoes = linhas.length ? `<div class="esp-cartoes">${linhas.map(c => `<div class="esp-cartao-caso">
      <div class="esp-topo"><div><b>${esc(c.protocolo)}</b><div class="esp-sub">${esc(tcRotuloLista(c))} · ${esc(dataCurtaBR(c.entrada))}</div></div>${espSelo(tcStatus(c))}</div>
      <div class="esp-sub">Agente: ${esc(c.agente_causal || "—")} · Etapa ${espEtapaTexto(c)}</div>
      <button class="esp-btn esp-btn-sm esp-btn-outline" type="button" data-esp-acao="esp-ver-detalhes" data-esp-id="${esc(c.id_corpo)}">Ver detalhes</button>
    </div>`).join("")}</div>` : "";

  const gaveta = estado.espCaso ? await espGaveta(estado.espCaso) : "";

  return `<div class="esp">${espHero()}
    <div class="esp-card">
      ${espTitulo("Corpos registrados", "Busque por protocolo ou nome, filtre por status e período.")}
      <div class="esp-filtros">
        <div class="esp-field esp-flex2"><label for="espBusca">Buscar</label>
          <input class="esp-input" id="espBusca" type="text" placeholder="Protocolo ou nome" value="${esc(f.busca)}">
          <small>Digite o protocolo (ex.: 000125/2026) ou o nome.</small></div>
        <div class="esp-field"><label for="espStatus">Status</label>
          <select class="esp-input" id="espStatus">
            <option value="">Todos os status</option>
            ${TC_STATUS.map(s => `<option value="${esc(s)}" ${s === f.status ? "selected" : ""}>${esc(s)}</option>`).join("")}
          </select></div>
        <div class="esp-field"><label for="espDe">De</label><input class="esp-input" id="espDe" type="date" value="${esc(f.de)}"></div>
        <div class="esp-field"><label for="espAte">Até</label><input class="esp-input" id="espAte" type="date" value="${esc(f.ate)}"></div>
        <div class="esp-field esp-auto"><label>&nbsp;</label>
          <button class="esp-btn esp-btn-outline" type="button" data-esp-acao="esp-limpar-filtros">Limpar filtros</button></div>
      </div>
      <div id="espChip">${chip}</div>
      <p class="esp-sub" id="espContagem">Exibindo ${linhas.length} de ${cs.length} corpos registrados.</p>
      ${tabela}${cartoes}
    </div>
    ${gaveta}</div>`;
};

function espEtapaTexto(c){
  if (c.custodia_finalizada) return '<span class="esp-ok">Concluído</span>';
  return `${tcEtapa(c)}/7`;
}

TELAS_DEPOIS["#/corpos"] = ()=>{
  espLigarHero();
  const f = espFiltros();
  const mudar = async ()=>{
    f.busca = valorDe("espBusca"); f.status = valorDe("espStatus"); f.de = valorDe("espDe"); f.ate = valorDe("espAte");
    if (f.status) f.lacres = false;
    await registrar("filtro da lista", {detalhe: f.status || f.busca || ""});
    navegar();
  };
  ["espBusca", "espStatus", "espDe", "espAte"].forEach(id => $("#" + id)?.addEventListener("change", mudar));
  $$("[data-esp-acao]").forEach(b => b.addEventListener("click", async ()=>{
    const acao = b.dataset.espAcao;
    if (acao === "esp-limpar-filtros"){
      estado.espFiltros = {status: "", busca: "", de: "", ate: "", lacres: false};
      toast("Filtros limpos."); return navegar();
    }
    if (acao === "esp-ver-detalhes"){ estado.espCaso = b.dataset.espId; return navegar(); }
    if (acao === "esp-fechar-gaveta"){ estado.espCaso = null; return navegar(); }
  }));
};

// a tecla Escape fecha a gaveta da lista
document.addEventListener("keydown", e=>{
  if (e.key !== "Escape" || !estado.espCaso) return;
  estado.espCaso = null;
  navegar();
});

/* ================= resumo por agente causal ================= */

TELAS["#/resumo"] = async ()=>{
  const cs = await db.list("corpos");
  const {linhas, tot} = tcResumo(cs);
  return `<div class="esp">${espHero()}
    <div class="esp-card">
      ${espTitulo("Resumo por agente causal", "Distribuição dos corpos e situação administrativa por agente causal.")}
      <div class="esp-tabela-wrap"><table class="esp-tabela esp-soma">
        <thead><tr><th>Agente causal</th><th>Total de corpos</th><th>Liberado para a família</th><th>Sepultados pelo Estado</th>
          <th>Aguardando identificação</th><th>Identificados mas não reclamados</th><th>Custódia finalizada</th></tr></thead>
        <tbody>${linhas.map(([agente, r]) => `<tr><td>${esc(agente)}</td><td>${r.total}</td><td>${r.familia}</td>
          <td>${r.sepultado}</td><td>${r.aguardando}</td><td>${r.nao_reclamado}</td><td>${r.finalizada}</td></tr>`).join("")}
          <tr class="esp-total"><td>Total geral</td><td>${tot.total}</td><td>${tot.familia}</td><td>${tot.sepultado}</td>
            <td>${tot.aguardando}</td><td>${tot.nao_reclamado}</td><td>${tot.finalizada}</td></tr></tbody>
      </table></div>
    </div></div>`;
};

/* ================= a ficha do caso ================= */

// a gaveta lateral: a mesma ficha, aberta por cima da lista
async function espGaveta(id){
  const c = await db.get("corpos", id);
  if (!c) return "";
  const [ls, ms, logs] = await Promise.all([
    db.porIndice("lacres", "corpo_id", id), db.porIndice("marcos", "corpo_id", id), db.porIndice("log", "corpo_id", id)]);
  const conteudo = await espCasoHTML(c, ls, ms, logs, true);
  return `<div class="esp-overlay" data-esp-acao="esp-fechar-gaveta"></div>
    <aside class="esp-gaveta" role="dialog" aria-label="Detalhes do caso">
      <div class="esp-gaveta-topo">
        <div><div class="esp-gaveta-titulo">${esc(c.protocolo)} — ${esc(c.nome || "NÃO IDENTIFICADO")}</div>
          <div class="esp-gaveta-sub">Status: ${esc(tcStatus(c))} · Entrada ${esc(dataCurtaBR(c.entrada))}</div>
          <div class="esp-selos">${espSelos(c)}</div></div>
        <button class="esp-btn esp-btn-sm esp-btn-outline" type="button" data-esp-acao="esp-fechar-gaveta">Fechar ×</button>
      </div>
      <div class="esp-gaveta-corpo">${conteudo}</div>
      <div class="esp-gaveta-rodape"><a class="esp-btn esp-btn-sm" href="#/corpo/${encodeURIComponent(id)}">Abrir a ficha completa</a></div>
    </aside>`;
}

function espSelos(c){
  let html = "";
  if (tcStatus(c) === "Sepultado pelo Estado") html += '<span class="esp-selo esp-selo-ambar">SEPULTADO PELO ESTADO</span>';
  if (c.custodia_finalizada) html += '<span class="esp-selo esp-selo-verde">CASO CONCLUÍDO</span>';
  return html;
}

// o corpo da ficha: stepper, sete etapas, funerária, encerramento, retificações e histórico
async function espCasoHTML(c, ls, ms, logs, naGaveta){
  const perfil = estado.perfil || "tecnico";
  const medico = perfil === "medico";
  const encerrado = !!c.custodia_finalizada;
  const editavel = !medico && !encerrado;
  const gestor = tcPodeReceber(perfil);
  const etapa = tcEtapa(c);
  const oc = c.ocorrencia || {};
  const id = c.id_corpo;
  const partes = [];

  if (medico) partes.push('<div class="esp-aviso esp-azul">Perfil Médico Legista — acesso somente para consulta, até a etapa 5. Edição disponível apenas para o perfil Técnico.</div>');
  if (encerrado) partes.push('<div class="esp-aviso">Caso encerrado. Os dados não podem ser editados: correções entram como retificação (RN12).</div>');

  // stepper das sete etapas
  const passos = TC_ETAPAS.map(et => {
    let estadoPasso = "locked";
    if (encerrado) estadoPasso = "done";
    else if (et.n < etapa) estadoPasso = "done";
    else if (et.n === etapa) estadoPasso = "current";
    return `<div class="esp-passo ${estadoPasso}"><span class="esp-passo-num">${estadoPasso === "done" ? "✓" : et.n}</span>${esc(et.nome)}</div>`;
  }).join("");
  partes.push(`<div class="esp-stepper">${passos}</div>
    <div class="esp-passo-compacto">Etapa ${etapa} de 7 — ${esc(TC_ETAPAS[etapa - 1].nome)}</div>`);

  // ---------- etapa 1 ----------
  const ac = c.acionamento || {};
  partes.push(`<div class="esp-bloco" id="espEtapa1">
    <h3>Etapa 1 — Acionamento</h3><p class="esp-sub">Registro do horário em que o caso foi acionado e número da necropsia.</p>
    <div class="esp-grid-2">${editavel
      ? espCampo("Horário de acionamento", "espAcHorario", ac.horario, "time") + espCampo("Número da necropsia", "espAcNumero", ac.numero)
      : espLeitura("Horário de acionamento", ac.horario) + espLeitura("Número da necropsia", ac.numero)}</div></div>`);

  // ---------- etapa 2 ----------
  const fotos = (lista, tag) => lista && lista.length
    ? `<div class="esp-fotos">${lista.map((f, i) => `<img class="esp-miniatura" src="${esc(f.url || f)}" alt="Foto ${esc(tag)} ${i + 1}" data-esp-foto="${esc(f.url || f)}">`).join("")}</div>`
    : '<p class="esp-nota">Nenhuma foto anexada.</p>';
  partes.push(`<div class="esp-bloco" id="espEtapa2">
    <h3>Etapa 2 — Ocorrência e possível vítima</h3><p class="esp-sub">Dados da ocorrência no local e informações sobre a possível vítima.</p>
    <div class="esp-grid-2">
      ${editavel ? espCampo("Data e hora da chegada ao local", "espChegada", oc.chegada, "datetime-local")
        : espLeitura("Data e hora da chegada ao local", oc.chegada ? dataCurtaBR(oc.chegada.slice(0, 10)) + " " + oc.chegada.slice(11, 16) : "")}
      ${editavel ? espSel("Agente causal", "espAgente", TC_AGENTES, c.agente_causal)
        : espLeitura("Agente causal", c.agente_causal)}
      ${editavel ? espCampo("Delegacia", "espDelegacia", oc.delegacia) : espLeitura("Delegacia", oc.delegacia)}
      ${editavel ? espCampo("Autoridade policial", "espAutoridade", oc.autoridade) : espLeitura("Autoridade policial", oc.autoridade)}
      ${editavel ? espCampo("Endereço", "espEndereco", oc.endereco) : espLeitura("Endereço", oc.endereco)}
      ${editavel ? espCampo("Município", "espMunicipio", oc.municipio) : espLeitura("Município", oc.municipio)}
      ${editavel ? espCampo("UF", "espUf", oc.uf) : espLeitura("UF", oc.uf)}
      ${editavel ? espCampo("Possível nome", "espPossivel", oc.possivel_nome) : espLeitura("Possível nome", oc.possivel_nome)}
      ${editavel ? espCampo("Filiação", "espFiliacao", oc.filiacao) : espLeitura("Filiação", oc.filiacao)}
      ${editavel ? espCampo("Data de nascimento", "espNascimento", oc.nascimento, "date") : espLeitura("Data de nascimento", oc.nascimento)}
      ${editavel ? espCampo("Idade", "espIdade", oc.idade) : espLeitura("Idade", oc.idade)}
      ${editavel ? espSel("Sexo", "espSexo", ["M", "F", "Indeterminado"], oc.sexo) : espLeitura("Sexo", oc.sexo)}
      ${editavel ? espCampo("Fonte da informação", "espFonte", oc.fonte) : espLeitura("Fonte da informação", oc.fonte)}
      ${editavel ? espCampo("Documento encontrado", "espDocumento", oc.documento) : espLeitura("Documento encontrado", oc.documento)}
      ${editavel ? espCampo("Telefone de familiar", "espTelefone", oc.telefone) : espLeitura("Telefone de familiar", oc.telefone)}
      ${editavel ? espArea("Observações", "espObservacoes", oc.observacoes) : `<div class="esp-full"><label>Observações</label><div class="esp-leitura">${esc(oc.observacoes || "—")}</div></div>`}
    </div>
    <h4 class="esp-subtitulo">Fotos do documento</h4>${fotos(oc.fotos_doc, "do documento")}
    <h4 class="esp-subtitulo">Fotos do cenário</h4>${fotos(oc.fotos_cena, "do cenário")}
    ${editavel ? `<div class="esp-acoes esp-mt">
      <button class="esp-btn esp-btn-sm esp-btn-outline" type="button" data-esp-acao="esp-anexar-foto" data-esp-alvo="fotos_cena">Anexar foto do cenário</button>
      <button class="esp-btn esp-btn-sm esp-btn-outline" type="button" data-esp-acao="esp-anexar-foto" data-esp-alvo="fotos_doc">Anexar foto do documento</button>
      <input type="file" id="espArquivoFoto" accept="image/*" hidden></div>` : ""}
    ${espBlocoMarcos(ms, editavel)}
  </div>`);

  // ---------- etapa 3 ----------
  const entradaOk = c.confirmado_entrada === true;
  partes.push(`<div class="esp-bloco" id="espEtapa3">
    <h3>Etapa 3 — Aguardando necropsia</h3><p class="esp-sub">Alocação do corpo na câmara fria e registro do lacre do corpo.</p>
    <div class="esp-grid-3">
      ${editavel ? espCampo("Câmara fria", "espCamara", c.camara) : espLeitura("Câmara fria", c.camara)}
      ${editavel ? espCampo("Gaveta", "espGaveta", c.gaveta) : espLeitura("Gaveta", c.gaveta)}
      ${editavel ? espSel("Estado do corpo", "espEstadoCorpo", ["Conservado", "Putrefeito", "Esqueletizado", "Carbonizado"], c.estado_corpo)
        : espLeitura("Estado do corpo", c.estado_corpo)}
      <div class="esp-full">${editavel ? espCampo("Lacre do corpo", "espLacreCorpo", c.lacre_corpo) : espLeitura("Lacre do corpo", c.lacre_corpo)}</div>
    </div>
    ${entradaOk ? '<p class="esp-nota">Entrada confirmada na base.</p>'
      : (editavel ? '<div class="esp-acoes"><button class="esp-btn" type="button" data-esp-acao="esp-confirmar-entrada">Confirmar entrada na base</button></div>' : "")}
  </div>`);

  // ---------- etapa 4 ----------
  const nec = c.necropsia || {};
  const coletados = ls.filter(l => l.coletado !== false && l.codigo);
  const recebidos = coletados.filter(l => l.recebido_em);
  const pct = coletados.length ? Math.round(recebidos.length / coletados.length * 100) : 0;
  const materiais = TC_MATERIAIS.map(m => {
    const l = ls.find(x => x.tipo === m.id) || {};
    const temLacre = l.coletado !== false && l.codigo;
    const checar = gestor && editavel
      ? `<span class="esp-check"><input type="checkbox" id="espRec-${esc(m.id)}" data-esp-lacre="${esc(l.id_lacre || "")}" ${l.recebido_em ? "checked" : ""}>
          <label for="espRec-${esc(m.id)}">Recebido pela ADM</label></span>`
      : (l.recebido_em ? '<span class="esp-check"><span>✓ Recebido pela ADM</span></span>' : "");
    return `<div class="esp-material">
      <div class="esp-material-topo"><b>${esc(m.nome)}</b>${temLacre ? '<span class="esp-badge esp-badge-ok">Coletado</span>' : '<span class="esp-badge">Não coletado</span>'}</div>
      <div class="esp-material-linha">
        ${editavel ? `<span class="esp-check"><input type="checkbox" id="espCol-${esc(m.id)}" data-esp-material="${esc(m.id)}" ${temLacre ? "checked" : ""}>
            <label for="espCol-${esc(m.id)}">Coletado</label></span>` : ""}
        ${editavel ? espCampo("Número do lacre", "espLacre-" + m.id, l.codigo) : espLeitura("Lacre", l.codigo)}
      </div>
      ${checar}
      ${l.recebido_em ? `<p class="esp-nota">Recebido pela ADM em ${esc(dataBR(l.recebido_em))} — ${esc(l.recebido_por || "")}</p>`
        : (gestor ? '<p class="esp-nota">Somente o gestor da ADM pode confirmar o recebimento.</p>' : "")}
    </div>`;
  }).join("");
  partes.push(`<div class="esp-bloco" id="espEtapa4">
    <h3>Etapa 4 — Necropsia em andamento</h3><p class="esp-sub">Equipe responsável, horários e coleta de materiais com lacres.</p>
    <div class="esp-grid-3">
      ${editavel ? espCampo("Médico legista", "espMedico", nec.medico) : espLeitura("Médico legista", nec.medico)}
      ${editavel ? espCampo("Técnico de necropsia", "espTecnicoNec", nec.tecnico) : espLeitura("Técnico de necropsia", nec.tecnico)}
      ${editavel ? espCampo("Odonto legista", "espOdonto", nec.odonto) : espLeitura("Odonto legista", nec.odonto)}
      ${editavel ? espCampo("Horário de início", "espInicio", nec.inicio, "time") : espLeitura("Início", nec.inicio)}
      ${editavel ? espCampo("Horário de término", "espTermino", nec.termino, "time") : espLeitura("Término", nec.termino)}
    </div>
    <h4 class="esp-subtitulo">Materiais coletados</h4>
    <div class="esp-contador">${recebidos.length} de ${coletados.length} lacres recebidos pela ADM</div>
    <div class="esp-progresso"><div class="esp-progresso-fill" style="width:${pct}%"></div></div>
    ${(coletados.length - recebidos.length) > 0 ? '<div class="esp-alerta-ambar">Há lacres aguardando confirmação de recebimento pela ADM.</div>' : ""}
    ${gestor && editavel && (coletados.length - recebidos.length) > 0
      ? '<div class="esp-acoes"><button class="esp-btn esp-btn-outline" type="button" data-esp-acao="esp-marcar-todos">Marcar todos como recebidos</button></div>' : ""}
    ${materiais}
    ${editavel ? '<div class="esp-acoes"><button class="esp-btn" type="button" data-esp-acao="esp-concluir-necropsia">Concluir necropsia</button></div>' : ""}
  </div>`);

  // ---------- etapa 5 ----------
  const ident = c.identificacao || {};
  const resultado = ident.resultado || "";
  const tentativas = (ident.tentativas || []).map(t => `${t.metodo} (${t.resultado})`).join(" · ");
  const metodos = [...TC_METODOS, "Não identificado"];
  let bloco5 = "";
  if (editavel){
    bloco5 += `<div class="esp-field esp-mb"><label for="espResultado">Resultado da identificação *</label>
      <select class="esp-input" id="espResultado" data-esp-campo="espResultado">
        <option value="">Escolha</option>
        <option value="identificado" ${resultado === "identificado" ? "selected" : ""}>Identificado</option>
        <option value="nao_identificado" ${resultado === "nao_identificado" ? "selected" : ""}>Não identificado — seguir para sepultamento pelo Estado</option>
      </select><small class="esp-nota">Define o encaminhamento do corpo.</small></div>`;
  } else {
    bloco5 += espLeitura("Resultado da identificação", resultado === "identificado" ? "Identificado"
      : resultado === "nao_identificado" ? "Não identificado — seguir para sepultamento pelo Estado" : "—");
  }
  if (resultado === "identificado"){
    bloco5 += `<div class="esp-grid-2">
      ${editavel ? espSel("Método de identificação", "espMetodo", metodos, ident.metodo) : espSelLeitura("Método de identificação", metodos, ident.metodo)}
      ${editavel ? espCampo("Nome confirmado", "espNomeConfirmado", ident.nome_confirmado) : espLeitura("Nome confirmado", ident.nome_confirmado)}
      ${editavel ? espCampo("Responsável pela identificação", "espResponsavel", ident.responsavel) : espLeitura("Responsável pela identificação", ident.responsavel)}
      ${editavel ? espCampo("Data da confirmação", "espDataConfirmacao", ident.data_confirmacao, "date") : espLeitura("Data da confirmação", ident.data_confirmacao)}
    </div>`;
    if (editavel) bloco5 += '<div class="esp-acoes"><button class="esp-btn" type="button" data-esp-acao="esp-confirmar-identificacao">Confirmar identificação</button></div>';
  } else if (resultado === "nao_identificado"){
    bloco5 += `<div class="esp-grid-2">${editavel ? espSel("Método de identificação", "espMetodo", ["Não identificado"], "Não identificado")
      : espLeitura("Método de identificação", "Não identificado")}</div>
      <div class="esp-aviso esp-azul">Corpo não identificado. O sepultamento será realizado pelo Estado, com registro para fins de rastreabilidade e eventual identificação posterior.</div>`;
  }
  if (tentativas) bloco5 += `<p class="esp-nota">Tentativas: ${esc(tentativas)}.</p>`;
  // a busca de familiares e o pedido de exame complementar
  const busca = ident.busca || {};
  if (editavel){
    bloco5 += `<h4 class="esp-subtitulo">Busca de familiares</h4>
      <div class="esp-grid-3">
        ${espCampo("Data de início da busca", "espBuscaInicio", busca.inicio, "date")}
        ${espCampo("Prazo em dias", "espBuscaPrazo", busca.prazo ?? 30, "number")}
        ${espSel("Resultado da busca", "espBuscaResultado", [["", "Selecione"], ["Familiar localizado", "Familiar localizado"], ["Sem êxito", "Sem êxito"]], busca.resultado)}
      </div>
      <div class="esp-acoes">
        <button class="esp-btn esp-btn-outline" type="button" data-esp-acao="esp-busca-iniciada">Registrar o início da busca</button>
        ${espSel("Exame complementar", "espExameMetodo", TC_EXAMES_COMPL, "DNA")}
        <button class="esp-btn esp-btn-outline" type="button" data-esp-acao="esp-exame-complementar">Solicitar exame complementar</button>
        ${tcPodeEsgotar(tcTentativas(c)) ? '<button class="esp-btn esp-btn-outline" type="button" data-esp-acao="esp-esgotar">Métodos esgotados: não identificado</button>' : ""}
      </div>
      ${ident.pendente ? `<div class="esp-aviso esp-ambar" id="espExamePendente"><b>Exame complementar em andamento:</b> ${esc(ident.pendente.metodo)}, solicitado em ${esc(dataBR(ident.pendente.enviado_em))}.</div>
        <div class="esp-grid-2">
          ${espSel("Resultado do exame", "espResultadoExame", [["", "Escolha"], ["identificou", "Identificou a pessoa"], ["sem_resultado", "Não identificou"]], "")}
          ${espCampo("Nome confirmado pelo exame", "espNomeExame", "")}
        </div>
        <div class="esp-acoes"><button class="esp-btn" type="button" data-esp-acao="esp-resultado-exame">Registrar o resultado do exame</button></div>` : ""}`;
  }
  // a decisão administrativa do Gestor ADM (RN09)
  if (gestor && editavel && !c.sepultamento && etapa <= 5){
    bloco5 += `<div class="esp-bloco esp-tracejado" id="espDecisaoAdm">
      <h4 class="esp-subtitulo esp-sem-margem">Decisão administrativa</h4>
      <p class="esp-nota">Se o corpo não puder ser identificado, a ADM pode autorizar o encaminhamento direto para sepultamento pelo Estado, sem preencher os campos de identificação.</p>
      <div class="esp-acoes esp-mt"><button class="esp-btn esp-btn-outline" type="button" data-esp-acao="esp-decisao-sepultamento">Encaminhar para sepultamento pelo Estado</button></div></div>`;
  }
  if (c.sepultamento) bloco5 += '<div class="esp-aviso esp-azul esp-mt">Decisão administrativa registrada: corpo encaminhado para sepultamento pelo Estado.</div>';
  partes.push(`<div class="esp-bloco" id="espEtapa5">
    <h3>Etapa 5 — Identificação</h3><p class="esp-sub">Resultado da identificação e, se necessário, busca de familiares e sepultamento pelo Estado.</p>
    ${bloco5}</div>`);

  // ---------- etapa 6 ----------
  if (etapa >= 6 || c.sepultamento || c.familia?.liberado_em){
    const fam = c.familia || {};
    const tipo = fam.tipo || "familiar";
    const tipos = [["familiar", "Liberação a familiar"], ["semFamiliar", "Liberação sem familiar — Sepultamento pelo Estado"]];
    let bloco6 = `<div class="esp-field esp-mb"><label for="espTipoLiberacao">Tipo de liberação *</label>
      ${editavel ? `<select class="esp-input" id="espTipoLiberacao" data-esp-campo="espTipoLiberacao">
        ${tipos.map(o => `<option value="${o[0]}" ${o[0] === tipo ? "selected" : ""}>${esc(o[1])}</option>`).join("")}</select>`
        : `<div class="esp-leitura">${esc(tipo === "familiar" ? "Liberação a familiar" : "Liberação sem familiar — Sepultamento pelo Estado")}</div>`}</div>`;
    if (tipo === "familiar"){
      bloco6 += `<div class="esp-grid-2">
        ${editavel ? espCampo("Nome do familiar", "espFamNome", fam.nome) : espLeitura("Nome do familiar", fam.nome)}
        ${editavel ? espCampo("Parentesco", "espParentesco", fam.parentesco) : espLeitura("Parentesco", fam.parentesco)}
        ${editavel ? espCampo("Documento", "espFamDocumento", fam.documento) : espLeitura("Documento", fam.documento)}
        ${editavel ? espCampo("Telefone", "espFamTelefone", fam.telefone) : espLeitura("Telefone", fam.telefone)}
        ${editavel ? espCampo("Data de liberação", "espFamData", fam.data_liberacao, "date") : espLeitura("Data de liberação", fam.data_liberacao)}
      </div>
      <div class="esp-mt"><label class="esp-rotulo">Assinatura digital do familiar</label>
        ${fam.assinatura ? `<img class="esp-assinatura" src="${esc(fam.assinatura)}" alt="Assinatura do familiar">`
          : '<p class="esp-nota">Assinatura não registrada.</p>'}
        ${editavel ? `<div class="esp-acoes esp-alinha-esquerda"><button class="esp-btn esp-btn-sm esp-btn-outline" type="button" data-esp-acao="esp-assinar" data-esp-alvo="familia">${fam.assinatura ? "Refazer" : "Assinar"}</button></div>` : ""}
      </div>
      ${editavel ? '<div class="esp-acoes"><button class="esp-btn" type="button" data-esp-acao="esp-confirmar-familia">Confirmar recebimento pelo familiar</button></div>' : ""}`;
    } else {
      const fb = fam.busca || {}, aut = fam.autorizacao || {};
      bloco6 += `<h4 class="esp-subtitulo">Busca de familiares</h4><div class="esp-grid-3">
        ${editavel ? espCampo("Data de início da busca", "espFamBuscaInicio", fb.inicio, "date")
          : espLeitura("Início da busca", fb.inicio)}
        ${editavel ? espCampo("Prazo em dias", "espFamBuscaPrazo", fb.prazo ?? 30, "number")
          : espLeitura("Prazo (dias)", String(fb.prazo ?? 30))}
        ${editavel ? espSel("Resultado da busca", "espFamBuscaResultado", [["", "Selecione"], ["Familiar localizado", "Familiar localizado"], ["Sem êxito", "Sem êxito"]], fb.resultado)
          : espLeitura("Resultado da busca", fb.resultado)}
      </div>`;
      if (fb.resultado === "Sem êxito"){
        bloco6 += `<div class="esp-grid-3">
          ${editavel ? espCampo("Número da autorização", "espAutNumero", aut.numero) : espLeitura("Número da autorização", aut.numero)}
          ${editavel ? espCampo("Data da autorização", "espAutData", aut.data, "date") : espLeitura("Data da autorização", aut.data)}
          ${editavel ? espCampo("Local de sepultamento", "espAutLocal", aut.local) : espLeitura("Local de sepultamento", aut.local)}
        </div>
        <div class="esp-aviso esp-azul">Corpo não reclamado. O sepultamento será realizado pelo Estado, com registro para fins de rastreabilidade e eventual identificação posterior.</div>
        ${editavel ? '<div class="esp-acoes"><button class="esp-btn" type="button" data-esp-acao="esp-confirmar-semfamilia">Confirmar sepultamento pelo Estado</button></div>' : ""}`;
      }
    }
    partes.push(`<div class="esp-bloco" id="espEtapa6">
      <h3>Etapa 6 — Família e liberação</h3><p class="esp-sub">Liberação do corpo a familiar ou, na ausência de familiares, sepultamento pelo Estado.</p>
      ${bloco6}</div>`);
  }

  // ---------- funerária ----------
  if (etapa >= 6 || c.sepultamento || c.funeraria?.data_entrega){
    const fu = c.funeraria || {};
    const destino = fu.destino || "familia";
    const destinos = [["familia", "Funerária contratada pela família"], ["estado", "Sepultamento pelo Estado"]];
    let corpo = `<div class="esp-field esp-mb"><label for="espDestino">Destino do corpo *</label>
      ${editavel ? `<select class="esp-input" id="espDestino" data-esp-campo="espDestino">
        ${destinos.map(o => `<option value="${o[0]}" ${o[0] === destino ? "selected" : ""}>${esc(o[1])}</option>`).join("")}</select>`
        : `<div class="esp-leitura">${esc(destino === "familia" ? "Funerária contratada pela família" : "Sepultamento pelo Estado")}</div>`}</div>`;
    if (destino === "familia"){
      corpo += `<div class="esp-grid-3">
        ${editavel ? espCampo("Nome da funerária", "espFunNome", fu.nome) : espLeitura("Nome da funerária", fu.nome)}
        ${editavel ? espCampo("Número do Auto de Entrega", "espFunAuto", fu.auto) : espLeitura("Auto de Entrega", fu.auto)}
        ${editavel ? espCampo("Data da entrega", "espFunData", fu.data_entrega, "date") : espLeitura("Data da entrega", fu.data_entrega)}
        ${editavel ? espCampo("Hora da entrega", "espFunHora", fu.hora_entrega, "time") : espLeitura("Hora da entrega", fu.hora_entrega)}
      </div>
      ${editavel ? '<div class="esp-acoes"><button class="esp-btn" type="button" data-esp-acao="esp-confirmar-funeraria">Confirmar entrega à funerária</button></div>' : ""}`;
    } else {
      corpo += `<div class="esp-grid-3">
        ${editavel ? espCampo("Funerária responsável pelo sepultamento", "espFunNome", fu.nome) : espLeitura("Funerária responsável", fu.nome)}
        ${editavel ? espCampo("Número do Auto de Entrega", "espFunAuto", fu.auto) : espLeitura("Auto de Entrega", fu.auto)}
        ${editavel ? espCampo("Data da entrega", "espFunData", fu.data_entrega, "date") : espLeitura("Data da entrega", fu.data_entrega)}
        ${editavel ? espCampo("Hora da entrega", "espFunHora", fu.hora_entrega, "time") : espLeitura("Hora da entrega", fu.hora_entrega)}
        ${editavel ? espCampo("Número da autorização de sepultamento", "espFunAutorizacao", fu.autorizacao) : espLeitura("Autorização", fu.autorizacao)}
        ${editavel ? espCampo("Data da autorização", "espFunAutData", fu.data_autorizacao, "date") : espLeitura("Data da autorização", fu.data_autorizacao)}
        <div class="esp-full">${editavel ? espCampo("Local de sepultamento", "espFunLocal", fu.local) : espLeitura("Local", fu.local)}</div>
      </div>
      ${editavel ? '<div class="esp-acoes"><button class="esp-btn" type="button" data-esp-acao="esp-confirmar-sepultamento-estado">Confirmar sepultamento pelo Estado</button></div>' : ""}`;
    }
    partes.push(`<div class="esp-bloco" id="espFuneraria">
      <h3>Funerária</h3><p class="esp-sub">Entrega do corpo à funerária responsável e registro do Auto de Entrega.</p>
      ${corpo}</div>`);
  }

  // ---------- etapa 7 ----------
  if (etapa >= 7 || c.laudo?.entregue_em || c.laudo?.recebido_em){
    const l = c.laudo || {};
    let bloco7 = `<h4 class="esp-subtitulo">Quem entrega</h4><div class="esp-grid-2">
        ${editavel ? espCampo("Nome do responsável pela entrega *", "espLaudoEntreguePor", l.entregue_por)
          : espLeitura("Responsável pela entrega", l.entregue_por)}</div>
      <h4 class="esp-subtitulo">Quem recebe</h4><div class="esp-grid-2">
        ${editavel ? espCampo("Nome de quem recebeu *", "espLaudoRecebeuPor", l.recebido_por) : espLeitura("Quem recebeu", l.recebido_por)}
        ${editavel ? espCampo("Data do recebimento *", "espLaudoData", l.recebido_data || (l.recebido_em ? l.recebido_em.slice(0, 10) : ""), "date")
          : espLeitura("Data do recebimento", l.recebido_em ? l.recebido_em.slice(0, 10) : (l.recebido_data || ""))}
      </div>
      <div class="esp-mt"><label class="esp-rotulo">Assinatura de quem recebeu</label>
        ${l.assinatura_recebimento ? `<img class="esp-assinatura" src="${esc(l.assinatura_recebimento)}" alt="Assinatura de quem recebeu">`
          : '<p class="esp-nota">Assinatura não registrada.</p>'}
        ${editavel ? `<div class="esp-acoes esp-alinha-esquerda"><button class="esp-btn esp-btn-sm esp-btn-outline" type="button" data-esp-acao="esp-assinar" data-esp-alvo="laudo">${l.assinatura_recebimento ? "Refazer" : "Assinar"}</button></div>` : ""}
      </div>`;
    if (l.recebido_em){
      bloco7 += `<div class="esp-mt"><span class="esp-check"><span>✓ Recebimento confirmado pela ADM</span></span>
        <span class="esp-selo esp-selo-verde">RECEBIDO PELA ADM</span></div>`;
    } else if (editavel){
      bloco7 += `<div class="esp-mt"><span class="esp-check">
        <input type="checkbox" id="espLaudoAdm" data-esp-lacre-laudo="1" ${l.confirmado_perfil ? "checked" : ""} ${gestor ? "" : "disabled"}>
        <label for="espLaudoAdm">Recebimento confirmado pela ADM</label></span>
        ${gestor ? "" : '<p class="esp-nota">Somente o gestor da ADM pode confirmar o recebimento.</p>'}</div>
        <div class="esp-aviso esp-azul esp-mt">Registre quem entregou e quem recebeu o laudo. Após confirmar, o caso será encerrado.</div>
        <div id="espErroLaudo"></div>
        <div class="esp-acoes"><button class="esp-btn" type="button" data-esp-acao="esp-confirmar-laudo">Confirmar entrega do laudo à ADM</button></div>`;
    }
    partes.push(`<div class="esp-bloco" id="espEtapa7">
      <h3>Etapa 7 — Entrega de laudo para ADM</h3><p class="esp-sub">Registro de quem entregou e de quem recebeu o laudo.</p>
      ${bloco7}</div>`);
  }

  // ---------- encerramento (RN10) ----------
  if (etapa >= 5){
    const pend = tcPendenciasEncerramento(c, ls);
    partes.push(`<div class="esp-bloco" id="espEncerramento">
      <h3>Encerramento da custódia</h3>
      <p class="esp-sub">O caso só se encerra quando as três condições estão confirmadas. Depois disso, nada é editado: correções entram como retificação.</p>
      <ul class="esp-checklist">${pend.map(p => `<li class="esp-pendente">○ ${esc(p)}</li>`).join("") || '<li class="esp-ok">✓ destino do corpo, laudo e lacres confirmados</li>'}
        ${c.custodia_finalizada ? `<li class="esp-ok">✓ Custódia finalizada${c.finalizada_em ? " em " + esc(dataBR(c.finalizada_em)) : ""}</li>` : ""}</ul>
    </div>`);
  }

  // ---------- retificações (RN12) ----------
  if (tcPodeRetificar(c) || (c.retificacoes || []).length){
    const lista = c.retificacoes || [];
    const pode = tcPodeRetificar(c) && ["tecnico", "gestor"].includes(estado.perfil);
    partes.push(`<div class="esp-bloco" id="espRetificacao">
      <h3>Retificações</h3>
      <p class="esp-sub">Depois do encerramento (ou do sepultamento), o caso não é editado. A correção entra como retificação: uma nova entrada no histórico, sem apagar a anterior.</p>
      ${lista.length ? `<ol class="esp-linha-do-tempo" id="espListaRetificacoes">${lista.map(r => `<li>
        <div class="esp-quando">${esc(dataBR(r.data_hora))} · ${esc(tcNomePerfil(r.perfil))}</div>
        <b>${esc(r.tipo)}</b><div>${esc(r.texto)}</div><div class="esp-nota">Motivo: ${esc(r.motivo)}</div></li>`).join("")}</ol>`
        : '<p class="esp-sub">Nenhuma retificação registrada.</p>'}
      ${pode ? `<div class="esp-grid-2">${espSel("Tipo", "espRetTipo", [["", "Escolha"], ...TC_RETIFICACOES.map(t => [t, t])], "")}</div>
        ${espArea("O que muda", "espRetTexto", "")}${espArea("Motivo", "espRetMotivo", "")}
        <div id="espErroRet"></div>
        <div class="esp-acoes"><button class="esp-btn" type="button" data-esp-acao="esp-retificar">Registrar a retificação</button></div>` : ""}
    </div>`);
  }

  // ---------- histórico ----------
  const trilha = (logs || []).slice().sort((a, b) => (b.data_hora || "").localeCompare(a.data_hora || ""));
  const visiveis = medico ? trilha.filter(l => !/funerária|sepultamento|laudo|liberação|familiar|entrega/i.test(l.acao || "")) : trilha;
  partes.push(`<div class="esp-bloco" id="espHistorico">
    <h3>Histórico</h3><p class="esp-sub">Mudanças de status, lacres recebidos e decisões registradas, da mais recente à mais antiga.</p>
    <ul class="esp-timeline">${visiveis.map(l => `<li><div class="esp-quando">${esc(dataBR(l.data_hora))}</div>
      <div class="esp-quem">${esc(tcNomePerfil(l.perfil))}</div><div>${esc(l.acao)}</div></li>`).join("")
      || "<li>Sem registros.</li>"}</ul></div>`);

  return partes.join("");
}

// os marcos do deslocamento (RN03)
function espBlocoMarcos(ms, editavel){
  const feitos = ms.slice().sort((a, b) => (a.data_hora || "").localeCompare(b.data_hora || ""));
  const registro = `<ol class="esp-linha-do-tempo">${feitos.map(m => `<li><div class="esp-quando">${esc(dataBR(m.data_hora))}</div>
    <b>${esc(m.tipo)}</b><div class="esp-nota">${esc(tcNomePerfil(m.perfil))}</div></li>`).join("") || "<li>Sem deslocamentos registrados.</li>"}</ol>`;
  if (!editavel) return `<h4 class="esp-subtitulo">Deslocamento (RN03)</h4>${registro}`;
  const faltando = ["Saída da base", "Chegada ao local", "Saída do local", "Retorno ao IML"].filter(t => !feitos.some(m => m.tipo === t));
  if (!faltando.length) return `<h4 class="esp-subtitulo">Deslocamento (RN03)</h4>${registro}`;
  return `<h4 class="esp-subtitulo">Deslocamento (RN03)</h4>${registro}
    <div class="esp-grid-2">
      ${espSel("Marco", "espMarco", [["", "Escolha"], ...faltando.map(t => [t, t])], "")}
      ${espCampo("Data e hora", "espMarcoData", tcAgora(), "datetime-local")}
    </div>
    <div class="esp-acoes"><button class="esp-btn esp-btn-sm" type="button" data-esp-acao="esp-registrar-marco">Registrar marco</button></div>`;
}

/* ================= a ficha como tela ================= */

TELAS["#/corpo/:id"] = async ({id})=>{
  const c = await db.get("corpos", id);
  if (!c) return `<div class="esp"><div class="esp-card"><p class="esp-sub">Corpo não encontrado.</p>
    <p><a href="#/corpos">Voltar para a lista</a></p></div></div>`;
  const [ls, ms, logs] = await Promise.all([
    db.porIndice("lacres", "corpo_id", id), db.porIndice("marcos", "corpo_id", id), db.porIndice("log", "corpo_id", id)]);
  const conteudo = await espCasoHTML(c, ls, ms, logs, false);
  return `<div class="esp">${espHero()}
    <div class="esp-cabecalho-ficha">
      <div><h1 class="esp-titulo-escuro">${esc(c.protocolo)} — ${esc(c.nome || "NÃO IDENTIFICADO")}</h1>
        <p class="esp-sub">Status: ${esc(tcStatus(c))} · Entrada ${esc(dataCurtaBR(c.entrada))} · Etapa ${tcEtapa(c)}/7</p>
        <div class="esp-selos">${espSelos(c)}</div></div>
      <a class="esp-btn esp-btn-sm esp-btn-outline" href="#/corpos">Voltar para a lista</a>
    </div>
    ${conteudo}</div>`;
};

/* ================= ações da ficha ================= */

// aplica um campo da ficha no modelo do caso
function espAplicarCampo(c, dados, campo, valor){
  // a base é o que já foi acumulado na gravação, para um campo não apagar o outro
  const oc = {...(dados.ocorrencia || c.ocorrencia || {})};
  const ac = {...(dados.acionamento || c.acionamento || {})};
  const nec = {...(dados.necropsia || c.necropsia || {})};
  const ident = {...(dados.identificacao || c.identificacao || {})};
  const fam = {...(dados.familia || c.familia || {})};
  const fu = {...(dados.funeraria || c.funeraria || {})};
  const laudo = {...(dados.laudo || c.laudo || {})};
  let redesenhar = false;
  switch (campo){
    case "espAcHorario": ac.horario = valor; dados.acionamento = ac; break;
    case "espAcNumero": ac.numero = valor; dados.acionamento = ac; dados.numero_necropsia = valor; break;
    case "espChegada": oc.chegada = valor; dados.ocorrencia = oc; dados.entrada = valor.slice(0, 10); break;
    case "espAgente": oc.agente = valor; dados.ocorrencia = oc; dados.agente_causal = valor; dados.natureza = valor; break;
    case "espDelegacia": oc.delegacia = valor; dados.ocorrencia = oc; dados.origem = valor; break;
    case "espAutoridade": oc.autoridade = valor; dados.ocorrencia = oc; break;
    case "espEndereco": oc.endereco = valor; dados.ocorrencia = oc; dados.local = valor; break;
    case "espMunicipio": oc.municipio = valor; dados.ocorrencia = oc; dados.municipio = valor; break;
    case "espUf": oc.uf = valor; dados.ocorrencia = oc; break;
    case "espPossivel": oc.possivel_nome = valor; dados.ocorrencia = oc; break;
    case "espFiliacao": oc.filiacao = valor; dados.ocorrencia = oc; break;
    case "espNascimento": oc.nascimento = valor; dados.ocorrencia = oc; break;
    case "espIdade": oc.idade = valor; dados.ocorrencia = oc; dados.idade = valor; break;
    case "espSexo": oc.sexo = valor; dados.ocorrencia = oc; dados.sexo = valor; break;
    case "espFonte": oc.fonte = valor; dados.ocorrencia = oc; break;
    case "espDocumento": oc.documento = valor; dados.ocorrencia = oc; break;
    case "espTelefone": oc.telefone = valor; dados.ocorrencia = oc; break;
    case "espObservacoes": oc.observacoes = valor; dados.ocorrencia = oc; break;
    case "espCamara": dados.camara = valor; break;
    case "espGaveta": dados.gaveta = valor; break;
    case "espEstadoCorpo": dados.estado_corpo = valor; break;
    case "espLacreCorpo": dados.lacre_corpo = valor; break;
    case "espMedico": nec.medico = valor; dados.necropsia = nec; break;
    case "espTecnicoNec": nec.tecnico = valor; dados.necropsia = nec; break;
    case "espOdonto": nec.odonto = valor; dados.necropsia = nec; break;
    case "espInicio": nec.inicio = valor; dados.necropsia = nec; break;
    case "espTermino": nec.termino = valor; dados.necropsia = nec; break;
    case "espResultado":
      ident.resultado = valor;
      ident.metodo = valor === "identificado" ? (ident.metodo && ident.metodo !== "Não identificado" ? ident.metodo : "Necropapiloscopia") : "Não identificado";
      dados.identificacao = ident; redesenhar = true; break;
    case "espMetodo": ident.metodo = valor; dados.identificacao = ident; redesenhar = true; break;
    case "espBuscaInicio":
      ident.busca = {...(ident.busca || {}), inicio: valor};
      dados.identificacao = ident; break;
    case "espBuscaPrazo":
      ident.busca = {...(ident.busca || {}), prazo: Number(valor) || 30};
      dados.identificacao = ident; break;
    case "espBuscaResultado":
      ident.busca = {...(ident.busca || {}), resultado: valor};
      dados.identificacao = ident; redesenhar = true; break;
    case "espTipoLiberacao": fam.tipo = valor; dados.familia = fam; redesenhar = true; break;
    case "espFamNome": fam.nome = valor; dados.familia = fam; break;
    case "espParentesco": fam.parentesco = valor; dados.familia = fam; break;
    case "espFamDocumento": fam.documento = valor; dados.familia = fam; break;
    case "espFamTelefone": fam.telefone = valor; dados.familia = fam; break;
    case "espFamData": fam.data_liberacao = valor; dados.familia = fam; break;
    case "espFamBuscaInicio":
      fam.busca = {...(fam.busca || {}), inicio: valor};
      dados.familia = fam; break;
    case "espFamBuscaPrazo":
      fam.busca = {...(fam.busca || {}), prazo: Number(valor) || 30};
      dados.familia = fam; break;
    case "espFamBuscaResultado":
      fam.busca = {...(fam.busca || {}), resultado: valor};
      dados.familia = fam; redesenhar = true; break;
    case "espAutNumero":
      fam.autorizacao = {...(fam.autorizacao || {}), numero: valor};
      dados.familia = fam; break;
    case "espAutData":
      fam.autorizacao = {...(fam.autorizacao || {}), data: valor};
      dados.familia = fam; break;
    case "espAutLocal":
      fam.autorizacao = {...(fam.autorizacao || {}), local: valor};
      dados.familia = fam; break;
    case "espDestino": fu.destino = valor; dados.funeraria = fu; redesenhar = true; break;
    case "espFunNome": fu.nome = valor; dados.funeraria = fu; break;
    case "espFunAuto": fu.auto = valor; dados.funeraria = fu; break;
    case "espFunData": fu.data_entrega = valor; dados.funeraria = fu; break;
    case "espFunHora": fu.hora_entrega = valor; dados.funeraria = fu; break;
    case "espFunAutorizacao": fu.autorizacao = valor; dados.funeraria = fu; break;
    case "espFunAutData": fu.data_autorizacao = valor; dados.funeraria = fu; break;
    case "espFunLocal": fu.local = valor; dados.funeraria = fu; break;
    case "espLaudoEntreguePor": laudo.entregue_por = valor; dados.laudo = laudo; break;
    case "espLaudoRecebeuPor": laudo.recebido_por = valor; dados.laudo = laudo; break;
    case "espLaudoData": laudo.recebido_data = valor; dados.laudo = laudo; break;
    default: return false;
  }
  return redesenhar;
}

// grava o que está na tela antes de uma ação, para o redesenho não perder o que foi digitado
async function espSalvarTudo(id){
  const c = await db.get("corpos", id);
  if (!c) return;
  const dados = {};
  $$("[data-esp-campo]").forEach(el => espAplicarCampo(c, dados, el.dataset.espCampo, el.value));
  if (Object.keys(dados).length) await tcGravar(id, dados, "campos da ficha", "");
}

TELAS_DEPOIS["#/corpo/:id"] = async ({id})=>{
  const c = await db.get("corpos", id);
  if (!c) return;
  await tcAuditar(id, "consulta ao caso");
  espLigarHero();

  // salvar os campos editados: o que está na tela inteira vai para o modelo em uma gravação só
  $$("[data-esp-campo]").forEach(el => el.addEventListener("change", async ()=>{
    const c = await db.get("corpos", id);
    if (!c) return;
    const dados = {};
    const campos = $$("[data-esp-campo]");
    let redesenhar = false;
    campos.forEach(o => { if (o.dataset.espCampo === el.dataset.espCampo) redesenhar = espAplicarCampo(c, dados, o.dataset.espCampo, o.value); });
    campos.forEach(o => { if (o.dataset.espCampo !== el.dataset.espCampo) espAplicarCampo(c, dados, o.dataset.espCampo, o.value); });
    if (Object.keys(dados).length) await tcGravar(id, dados, "campo alterado", el.dataset.espCampo);
    if (redesenhar) navegar(); else toast("Alteração salva.");
  }));

  $$("[data-esp-acao]").forEach(b => b.addEventListener("click", () => espAcao(id, b)));

  // o recebimento de um lacre é exclusivo do Gestor ADM
  $$("[data-esp-lacre]").forEach(el => el.addEventListener("change", async ()=>{
    const l = await db.get("lacres", el.dataset.espLacre);
    if (!l) return;
    if (!tcPodeReceber(estado.perfil)){ toast("Somente o gestor da ADM pode confirmar o recebimento.", "err"); return navegar(); }
    await espSalvarTudo(id);
    if (el.checked){
      await db.put("lacres", {...l, recebido_em: agora(), recebido_por: tcNomePerfil(estado.perfil), recebido_perfil: estado.perfil});
      await tcAuditar(id, `lacre ${l.codigo} recebido pela ADM`, l.nome || "");
    } else {
      await db.put("lacres", {...l, recebido_em: "", recebido_por: "", recebido_perfil: ""});
      await tcAuditar(id, `recebimento do lacre ${l.codigo} desfeito`, "");
    }
    toast("Recebimento atualizado."); navegar();
  }));

  // a confirmação do laudo recebido pela ADM
  const laudoAdm = $("#espLaudoAdm");
  if (laudoAdm) laudoAdm.addEventListener("change", async ()=>{
    const atual = await db.get("corpos", id);
    if (!tcPodeReceber(estado.perfil)){ toast("Somente o gestor da ADM pode confirmar o recebimento.", "err"); return navegar(); }
    await espSalvarTudo(id);
    const l = atual.laudo || {};
    await tcGravar(id, {laudo: {...l, confirmado_perfil: laudoAdm.checked ? "gestor" : "", recebido_em: laudoAdm.checked ? agora() : l.recebido_em}},
      laudoAdm.checked ? "recebimento do laudo confirmado pela ADM" : "confirmação do laudo desfeita");
    if (laudoAdm.checked){
      const fim = await tcTentarFinalizar(id);
      toast(fim ? "Recebimento confirmado. Custódia finalizada." : "Recebimento confirmado.");
    } else toast("Recebimento atualizado.");
    navegar();
  });

  // a foto anexada
  const arq = $("#espArquivoFoto");
  if (arq) arq.addEventListener("change", async e=>{
    const file = e.target.files[0];
    if (!file) return;
    const atual = await db.get("corpos", id);
    const alvo = arq.dataset.espAlvo || "fotos_cena";
    const url = await new Promise(res => { const r = new FileReader(); r.onload = () => res(r.result); r.readAsDataURL(file); });
    const oc = {...(atual.ocorrencia || {})};
    oc[alvo] = [...(oc[alvo] || []), {url, nome: file.name}];
    await tcGravar(id, {ocorrencia: oc}, "foto anexada", file.name);
    toast("Foto anexada."); navegar();
  });

  // o material coletado e o número do lacre
  $$("[data-esp-material]").forEach(el => el.addEventListener("change", async ()=>{
    const tipo = el.dataset.espMaterial;
    const ls = await db.porIndice("lacres", "corpo_id", id);
    const l = ls.find(x => x.tipo === tipo);
    if (!l) return;
    await espSalvarTudo(id);
    const codigo = valorDe("espLacre-" + tipo);
    await db.put("lacres", {...l, coletado: el.checked, codigo: el.checked ? codigo : "", destino: el.checked ? (l.destino || "Laboratório de destino") : ""});
    await tcAuditar(id, `material ${tipo}: ${el.checked ? "coletado" : "não coletado"}`, codigo);
    toast("Material atualizado."); navegar();
  }));
};

TELAS_DEPOIS["#/painel"] = async ()=>{
  espLigarHero();
  $$("[data-esp-kpi]").forEach(el => {
    const abrir = async ()=>{
      const chave = el.dataset.espKpi;
      estado.espFiltros = {status: "", busca: "", de: "", ate: "", lacres: false};
      if (chave !== "todos"){
        if (chave === "lacres") estado.espFiltros.lacres = true;
        else estado.espFiltros.status = chave;
      }
      location.hash = "#/corpos";
    };
    el.addEventListener("click", abrir);
    el.addEventListener("keydown", e=>{ if (e.key === "Enter" || e.key === " "){ e.preventDefault(); abrir(); } });
  });
  $("#btnTcCsv")?.addEventListener("click", async ()=>{
    const [cs, ls] = await Promise.all([db.list("corpos"), db.list("lacres")]);
    const linhas = [["protocolo", "numero_necropsia", "situacao", "etapa", "identificado", "agente_causal", "entrada", "destino"]].concat(
      cs.map(c => [c.protocolo, c.numero_necropsia, tcStatus(c), tcEtapa(c), c.identificado ? "sim" : "não",
        c.agente_causal || "", c.entrada || "", c.destino_final || ""]));
    const csv = "﻿" + linhas.map(l => l.map(x => /[;"\n]/.test(String(x)) ? `"${String(x).replace(/"/g, '""')}"` : String(x)).join(";")).join("\r\n");
    baixar(`necropsia-${hojeISO()}.csv`, csv, "text/csv;charset=utf-8");
    await registrar("relatório exportado", {detalhe: `${cs.length} corpos`});
  });
};

/* ================= as ações ================= */

async function espAcao(id, b){
  const acao = b.dataset.espAcao;
  await espSalvarTudo(id);   // grava o que está na tela antes de agir
  const c = await db.get("corpos", id);
  if (!c) return;
  const alvo = b.dataset.espAlvo;
  const ls = await db.porIndice("lacres", "corpo_id", id);

  if (acao === "esp-confirmar-entrada"){
    await tcGravar(id, {confirmado_entrada: true, camara: c.camara || "Câmara 1", etapa: 3, etapa_em: agora()},
      "entrada do corpo confirmada na base");
    toast("Entrada na base confirmada."); return navegar();
  }
  if (acao === "esp-concluir-necropsia"){
    await tcGravar(id, {etapa: 5, etapa_em: agora(), necropsia: {...(c.necropsia || {}), termino: valorDe("espTermino") || tcAgora().slice(11, 16)}},
      "necropsia concluída");
    toast("Necropsia concluída."); return navegar();
  }
  if (acao === "esp-marcar-todos"){
    if (!tcPodeReceber(estado.perfil)) return toast("Somente o gestor da ADM pode confirmar o recebimento.", "err");
    for (const l of ls){
      if (l.coletado !== false && l.codigo && !l.recebido_em){
        await db.put("lacres", {...l, recebido_em: agora(), recebido_por: tcNomePerfil(estado.perfil), recebido_perfil: estado.perfil});
        await tcAuditar(id, `lacre ${l.codigo} recebido pela ADM`, l.nome || "");
      }
    }
    toast("Lacres marcados como recebidos."); return navegar();
  }
  if (acao === "esp-confirmar-identificacao"){
    const nome = valorDe("espNomeConfirmado"), responsavel = valorDe("espResponsavel"), data = valorDe("espDataConfirmacao");
    const metodo = valorDe("espMetodo");
    if (!nome || !responsavel || !data || !metodo) return toast("Preencha método, nome confirmado, responsável e data.", "err");
    const ident = {...(c.identificacao || {}), resultado: "identificado", metodo, nome_confirmado: nome,
      responsavel, data_confirmacao: data, em: agora(),
      tentativas: [...(c.identificacao?.tentativas || []), {metodo, resultado: "identificou", em: agora()}]};
    await tcGravar(id, {identificacao: ident, identificado: true, desconhecido: false, nome, documento: c.ocorrencia?.documento || "",
      metodo_identificacao: metodo, identificado_em: agora(), etapa: 6, etapa_em: agora(), situacao: "em custódia"},
      `identificação confirmada por ${metodo}`, nome);
    toast("Identificação confirmada."); return navegar();
  }
  if (acao === "esp-esgotar"){
    if (!tcPodeEsgotar(tcTentativas(c))) return toast("Encaminhe a pelo menos um exame complementar antes de declarar os métodos esgotados.", "err");
    const ident = {...(c.identificacao || {}), resultado: "nao_identificado", em: agora()};
    await tcGravar(id, {identificacao: ident, identificado: false, desconhecido: true, nome: "", etapa: 6, etapa_em: agora(), situacao: "não identificado"},
      "identificação: métodos esgotados, não identificado");
    toast("Métodos esgotados: o caso segue para a decisão do Gestor ADM."); return navegar();
  }
  if (acao === "esp-exame-complementar"){
    const escolhido = valorDe("espExameMetodo");
    if (!TC_EXAMES_COMPL.includes(escolhido)) return toast("Escolha DNA, Odontologia legal ou Antropologia forense.", "err");
    const ident = {...(c.identificacao || {}), resultado: "pendente",
      tentativas: (c.identificacao?.tentativas || []).length ? c.identificacao.tentativas
        : [{metodo: "Necropapiloscopia", resultado: "sem resultado", em: agora()}],
      pendente: {metodo: escolhido, enviado_em: agora()}};
    await tcGravar(id, {identificacao: ident, situacao: "aguardando identificação"}, `exame complementar solicitado: ${escolhido}`);
    toast("Exame complementar registrado."); return navegar();
  }
  if (acao === "esp-resultado-exame"){
    const pend = c.identificacao?.pendente;
    if (!pend) return toast("Não há exame complementar em andamento.", "err");
    const resultado = valorDe("espResultadoExame"), nome = valorDe("espNomeExame");
    if (!resultado) return toast("Escolha o resultado do exame.", "err");
    const tentativas = [...(c.identificacao?.tentativas || []), {metodo: pend.metodo, resultado: resultado === "identificou" ? "identificou" : "sem resultado", em: agora()}];
    if (resultado === "identificou"){
      if (!nome) return toast("Informe o nome da pessoa identificada.", "err");
      const ident = {...c.identificacao, resultado: "identificado", metodo: pend.metodo, nome_confirmado: nome,
        responsavel: c.tecnico, data_confirmacao: agora().slice(0, 10), tentativas, em: agora()};
      await tcGravar(id, {identificacao: ident, identificado: true, desconhecido: false, nome, etapa: 6, etapa_em: agora(), situacao: "em custódia"},
        `identificação confirmada por ${pend.metodo}`, nome);
      toast("Identificação confirmada."); return navegar();
    }
    const ident = {...c.identificacao, resultado: "pendente", tentativas};
    await tcGravar(id, {identificacao: ident}, `exame complementar sem resultado: ${pend.metodo}`);
    toast("Resultado registrado."); return navegar();
  }
  if (acao === "esp-busca-iniciada"){
    const ident = {...(c.identificacao || {}), busca: {...((c.identificacao || {}).busca || {}),
      inicio: valorDe("espBuscaInicio") || agora().slice(0, 10), prazo: Number(valorDe("espBuscaPrazo")) || 30,
      resultado: valorDe("espBuscaResultado")}};
    await tcGravar(id, {identificacao: ident}, "busca de familiares iniciada");
    toast("Busca registrada."); return navegar();
  }
  if (acao === "esp-decisao-sepultamento"){
    const justificativa = await espJanelaJustificativa();
    if (!justificativa) return;
    const ident = {...(c.identificacao || {}), resultado: "nao_identificado", metodo: "Não identificado"};
    await tcGravar(id, {identificacao: ident, etapa: 6, etapa_em: agora(), situacao: "não identificado",
      funeraria: {...(c.funeraria || {}), destino: "estado"}},
      "decisão administrativa: encaminhamento para sepultamento pelo Estado", justificativa);
    toast("Corpo encaminhado para sepultamento pelo Estado."); return navegar();
  }
  if (acao === "esp-confirmar-familia"){
    const fam = c.familia || {};
    const nome = valorDe("espFamNome"), parentesco = valorDe("espParentesco"), documento = valorDe("espFamDocumento");
    const data = valorDe("espFamData"), assinatura = fam.assinatura;
    if (!c.identificado) return toast("O corpo não está identificado: a liberação fica bloqueada (RN02).", "err");
    if (!nome || !documento || !data) return toast("Preencha nome, documento e data de liberação do familiar.", "err");
    if (!assinatura) return toast("Capture a assinatura do familiar no campo.", "err");
    const novaFamilia = {...fam, tipo: "familiar", nome, parentesco, documento, data_liberacao: data, assinatura,
      encontrada: true, busca_iniciada_em: fam.busca_iniciada_em || agora(), busca_encerrada_em: agora(),
      busca_sem_sucesso: false, liberado_em: agora()};
    await tcGravar(id, {familia: novaFamilia, etapa: 6, etapa_em: agora(), situacao: "em custódia",
      entrega: {responsavel: nome, documento, data}},
      "liberação à família", `${nome} (${parentesco || ""})`);
    toast("Recebimento pelo familiar confirmado."); return navegar();
  }
  if (acao === "esp-confirmar-semfamilia"){
    const fam = c.familia || {};
    const aut = {numero: valorDe("espAutNumero"), data: valorDe("espAutData"), local: valorDe("espAutLocal")};
    if (valorDe("espFamBuscaResultado") !== "Sem êxito" || !aut.numero || !aut.data || !aut.local)
      return toast("Preencha a autorização e marque a busca como 'Sem êxito'.", "err");
    const novaFamilia = {...fam, tipo: "semFamiliar", busca: {inicio: valorDe("espFamBuscaInicio"), prazo: Number(valorDe("espFamBuscaPrazo")) || 30, resultado: "Sem êxito"},
      autorizacao: aut, busca_sem_sucesso: true, busca_encerrada_em: agora()};
    await tcGravar(id, {familia: novaFamilia, etapa: 6, etapa_em: agora(), situacao: "não reclamado"},
      "busca de familiares encerrada sem êxito", aut.numero);
    toast("Busca encerrada sem familiar. O caso aguarda a decisão do Gestor ADM."); return navegar();
  }
  if (acao === "esp-confirmar-funeraria"){
    const fu = {destino: "familia", nome: valorDe("espFunNome"), auto: valorDe("espFunAuto"),
      data_entrega: valorDe("espFunData"), hora_entrega: valorDe("espFunHora")};
    if (!fu.nome || !fu.auto || !fu.data_entrega || !fu.hora_entrega)
      return toast("Preencha funerária, Auto de Entrega, data e hora da entrega.", "err");
    await tcGravar(id, {funeraria: fu, etapa: 7, etapa_em: agora(), destino_final: "família", situacao: "liberado"},
      `entrega à funerária ${fu.nome} confirmada`, `Auto ${fu.auto}`);
    toast("Entrega à funerária confirmada."); return navegar();
  }
  if (acao === "esp-confirmar-sepultamento-estado"){
    if (!tcPodeReceber(estado.perfil)) return toast("Somente o Gestor ADM autoriza o sepultamento pelo Estado.", "err");
    const fu = {destino: "estado", nome: valorDe("espFunNome"), auto: valorDe("espFunAuto"),
      data_entrega: valorDe("espFunData"), hora_entrega: valorDe("espFunHora"),
      autorizacao: valorDe("espFunAutorizacao"), data_autorizacao: valorDe("espFunAutData"), local: valorDe("espFunLocal")};
    const sep = {justificativa: (c.familia?.autorizacao?.numero ? "Busca de familiares encerrada sem êxito. " : "") + "Sepultamento pelo Estado autorizado pelo Gestor ADM.",
      autorizacao: fu.autorizacao, autorizado_em: agora(), perfil: estado.perfil};
    if (!fu.nome || !fu.auto || !fu.data_entrega || !fu.hora_entrega || !fu.autorizacao || !fu.data_autorizacao || !fu.local)
      return toast("Preencha todos os campos do sepultamento pelo Estado.", "err");
    await tcGravar(id, {funeraria: fu, sepultamento: sep, destino_final: "sepultamento", etapa: 6, etapa_em: agora(), situacao: "liberado"},
      "sepultamento pelo Estado autorizado", `${fu.autorizacao} · ${fu.nome}`);
    await tcTentarFinalizar(id);
    toast("Sepultamento pelo Estado registrado."); return navegar();
  }
  if (acao === "esp-confirmar-laudo"){
    const l = c.laudo || {};
    const por = valorDe("espLaudoEntreguePor"), para = valorDe("espLaudoRecebeuPor"), data = valorDe("espLaudoData");
    if (!por || !para) return toast("Informe quem entrega e quem recebe o laudo.", "err");
    await tcGravar(id, {laudo: {...l, entregue_por: por, recebido_por: para, entregue_em: agora(), recebido_em: l.recebido_em || ""}},
      "laudo entregue à ADM", `${por} → ${para}`);
    toast("Entrega do laudo registrada."); return navegar();
  }
  if (acao === "esp-assinar"){
    const assinatura = await espJanelaAssinatura();
    if (!assinatura) return;
    if (alvo === "familia") await tcGravar(id, {familia: {...(c.familia || {}), assinatura}}, "assinatura do familiar capturada");
    else await tcGravar(id, {laudo: {...(c.laudo || {}), assinatura_recebimento: assinatura}}, "assinatura de quem recebe o laudo capturada");
    toast("Assinatura registrada."); return navegar();
  }
  if (acao === "esp-retificar"){
    const r = {tipo: valorDe("espRetTipo"), texto: valorDe("espRetTexto"), motivo: valorDe("espRetMotivo"),
      perfil: estado.perfil || "", data_hora: agora()};
    const falta = tcFaltaRetificacao(r);
    if (falta.length){ const el = $("#espErroRet"); if (el) el.innerHTML = `<div class="esp-alerta-vermelha">Faltam: ${esc(falta.join(", "))}.</div>`; return; }
    await db.put("corpos", {...c, retificacoes: [...(c.retificacoes || []), r]});
    await tcAuditar(id, `retificação: ${r.tipo}`, `${r.texto} · ${r.motivo}`);
    toast("Retificação registrada."); return navegar();
  }
  if (acao === "esp-registrar-marco"){
    const tipo = valorDe("espMarco"), quando = valorDe("espMarcoData");
    if (!tipo) return toast("Escolha o marco.", "err");
    if (!quando) return toast("Informe a data e a hora.", "err");
    await db.put("marcos", {id_marco: uuid(), corpo_id: id, tipo, data_hora: quando + ":00", perfil: estado.perfil || "", observacao: ""});
    await tcAuditar(id, `marco: ${tipo}`);
    toast("Marco registrado."); return navegar();
  }
  if (acao === "esp-anexar-foto"){
    const input = $("#espArquivoFoto");
    if (!input) return;
    input.dataset.espAlvo = alvo;
    input.click();
    return;
  }
}


/* ================= janelas ================= */

// a assinatura no canvas
function espJanelaAssinatura(){
  return new Promise(resolve => {
    const alvo = document.createElement("div");
    alvo.className = "esp-janela-fundo";
    alvo.innerHTML = `<div class="esp-janela esp-janela-cheia" role="dialog" aria-label="Assinatura digital">
      <h3 class="esp-titulo">Assinatura digital</h3>
      <p class="esp-sub">Assine no campo abaixo com o dedo ou mouse. Limpe e refaça se necessário.</p>
      <canvas id="espCanvas"></canvas>
      <div class="esp-acoes">
        <button class="esp-btn esp-btn-outline" type="button" data-esp-janela="limpar">Limpar</button>
        <button class="esp-btn esp-btn-outline" type="button" data-esp-janela="cancelar">Cancelar</button>
        <button class="esp-btn" type="button" data-esp-janela="confirmar">Confirmar assinatura</button>
      </div></div>`;
    document.body.appendChild(alvo);
    const canvas = $("#espCanvas", alvo);
    const ajustar = ()=>{ const r = canvas.getBoundingClientRect(); canvas.width = Math.max(300, Math.round(r.width)); canvas.height = 300; };
    ajustar();
    const ctx = canvas.getContext("2d");
    ctx.lineWidth = 2.5; ctx.lineCap = "round"; ctx.strokeStyle = "#1e3a5f";
    let desenhando = false, ultimoPonto = null, sujo = false;
    const pos = ev => { const r = canvas.getBoundingClientRect(); return {x: (ev.clientX - r.left) * canvas.width / r.width, y: (ev.clientY - r.top) * canvas.height / r.height}; };
    canvas.addEventListener("pointerdown", ev=>{ desenhando = true; ultimoPonto = pos(ev); canvas.setPointerCapture(ev.pointerId); ev.preventDefault(); });
    canvas.addEventListener("pointermove", ev=>{
      if (!desenhando) return;
      const p = pos(ev); ctx.beginPath(); ctx.moveTo(ultimoPonto.x, ultimoPonto.y); ctx.lineTo(p.x, p.y); ctx.stroke();
      ultimoPonto = p; sujo = true; ev.preventDefault();
    });
    const fim = ()=>{ desenhando = false; };
    canvas.addEventListener("pointerup", fim); canvas.addEventListener("pointerleave", fim); canvas.addEventListener("pointercancel", fim);
    const fechar = valor => { document.removeEventListener("keydown", teclado); alvo.remove(); resolve(valor); };
    const teclado = ev => { if (ev.key === "Escape"){ ev.preventDefault(); $("[data-esp-janela=cancelar]", alvo)?.click(); } };
    document.addEventListener("keydown", teclado);
    $$("[data-esp-janela]", alvo).forEach(b => b.addEventListener("click", ()=>{
      const acao = b.dataset.espJanela;
      if (acao === "limpar"){ ctx.clearRect(0, 0, canvas.width, canvas.height); sujo = false; }
      if (acao === "cancelar") fechar(null);
      if (acao === "confirmar") fechar(sujo ? canvas.toDataURL("image/png") : null);
    }));
  });
}

// a justificativa do sepultamento pelo Estado (RN09)
function espJanelaJustificativa(){
  return new Promise(resolve => {
    const alvo = document.createElement("div");
    alvo.className = "esp-janela-fundo";
    alvo.innerHTML = `<div class="esp-janela" role="dialog" aria-label="Justificativa do sepultamento">
      <h3 class="esp-titulo">Encaminhar para sepultamento pelo Estado</h3>
      <p class="esp-sub">Esta ação encerra a etapa de identificação sem confirmação de identidade. O corpo seguirá para a funerária e depois para sepultamento pelo Estado.</p>
      <div class="esp-field"><label for="espJustText">Justificativa *</label>
        <textarea class="esp-input" id="espJustText" rows="4" placeholder="Ex.: Busca por familiares e métodos de identificação esgotados após 30 dias."></textarea>
        <small class="esp-nota">Mínimo de ${TC_JUSTIFICATIVA_MIN} caracteres.</small></div>
      <div id="espErroJust"></div>
      <div class="esp-acoes">
        <button class="esp-btn esp-btn-outline" type="button" data-esp-janela="cancelar">Cancelar</button>
        <button class="esp-btn esp-btn-perigo" type="button" data-esp-janela="confirmar">Confirmar encaminhamento</button>
      </div></div>`;
    document.body.appendChild(alvo);
    const fechar = valor => { document.removeEventListener("keydown", teclado); alvo.remove(); resolve(valor); };
    const teclado = ev => { if (ev.key === "Escape"){ ev.preventDefault(); $("[data-esp-janela=cancelar]", alvo)?.click(); } };
    document.addEventListener("keydown", teclado);
    $$("[data-esp-janela]", alvo).forEach(b => b.addEventListener("click", ()=>{
      const acao = b.dataset.espJanela;
      if (acao === "cancelar") return fechar(null);
      const texto = valorDe("espJustText");
      if (texto.length < TC_JUSTIFICATIVA_MIN){
        const el = $("#espErroJust", alvo);
        if (el) el.innerHTML = `<div class="esp-alerta-vermelha">A justificativa deve ter no mínimo ${TC_JUSTIFICATIVA_MIN} caracteres.</div>`;
        return;
      }
      fechar(texto.trim());
    }));
  });
}
