/* Identidade da Trilha de Custódia e Identificação (TCIN).
   Entra por último no build. O painel passa a ser por perfil e o plantonista
   ganha o quadro de plantão em colunas por situação; a ficha vira abas. */

function tcinUltimoMarco(ms, id){
  return ms.filter(m=>m.corpo_id === id).sort((a, b)=>b.data_hora.localeCompare(a.data_hora))[0];
}
function tcinCorpoCard(c, ms){
  const u = tcinUltimoMarco(ms, c.id_corpo), d = tcDias(c);
  return `<a class="tc-corpo" href="#/corpo/${encodeURIComponent(c.id_corpo)}">
    <span class="tc-corpo-topo"><b class="mono">${esc(c.protocolo)}</b><span class="selo ${tcSel(c.situacao)}">${esc(c.situacao)}</span></span>
    <span class="tc-corpo-nome">${esc(tcRotuloLista(c))}</span>
    <span class="tc-corpo-dias ${d > 30 ? "erro-txt" : d > 10 ? "alerta-txt" : ""}">${c.situacao === "liberado" ? "liberado" : `${plural(d, "dia", "dias")} no IML`}</span>
    <span class="sub">${u ? esc(u.tipo) + " · " + dataBR(u.data_hora) : "sem movimentação"}</span></a>`;
}
function tcinCabecalho(perfil){
  const titulos = {
    operador: ["Painel do CIOP", "Acionamentos em deslocamento e corpos que chegaram ao IML."],
    tecnico: ["Sala de necropsia", "Corpos na sala, dias no IML e último marco de cada um."],
    plantonista: ["Passagem de plantão", "Quadro por situação, com os dias no IML e o último marco."],
    gestor: ["Painel do gestor", "Tempos do percurso, permanência e corpos sem movimentação."],
    medico: ["Painel do médico legista", "Corpos na sala de necropsia, com leitura até a etapa 5."],
  };
  const [t, s] = titulos[perfil] || titulos.tecnico;
  return `<h1>${t}</h1><p class="sub">${s} <a href="#/corpo/novo">Novo acionamento</a></p>`;
}
function tcinKpi(valor, rotulo, attr){
  return `<div class="card kpi"><div class="v"${attr ? ` ${attr}` : ""}>${valor}</div><div class="r">${rotulo}</div></div>`;
}

TELAS["#/painel"] = async ()=>{
  const [cs, ms] = await Promise.all([db.list("corpos"), db.list("marcos")]);
  const por = s => cs.filter(c=>c.situacao === s).length;
  const perfil = estado.perfil || "tecnico";
  const liberados = cs.filter(c=>c.situacao === "liberado").length;
  const plantao = cs.filter(c=>{
    if (c.situacao === "liberado") return false;
    const ultimo = ms.filter(m=>m.corpo_id === c.id_corpo).map(m=>m.data_hora).sort().pop() || c.criado_em;
    return tcHoras(ultimo) > TC_PLANTao_HORAS;
  });
  if (perfil === "gestor"){
    const tempos = tcTempos(cs, ms);
    const permanencia = cs.filter(c=>c.situacao !== "liberado").map(c=>({c, dias: Math.max(0, Math.round((Date.now() - new Date(c.criado_em)) / 86400000))}))
      .sort((a, b)=>b.dias - a.dias);
    return `${tcinCabecalho(perfil)}
      <div class="grade">${tcinKpi(tempos.remocao === null ? "—" : tempos.remocao + " h", "tempo médio de remoção", 'data-tc-ind="remocao"')}
        ${tcinKpi(tempos.identificacao === null ? "—" : tempos.identificacao + " h", "tempo médio de identificação", 'data-tc-ind="identificacao"')}
        ${tcinKpi(tempos.liberacao === null ? "—" : tempos.liberacao + " h", "tempo médio de liberação", 'data-tc-ind="liberacao"')}
        ${tcinKpi(plantao.length, `sem movimentação há mais de ${TC_PLANTao_HORAS} h`, 'data-tc-ind="plantao"')}</div>
      <div class="card tabela-wrap"><h2 style="margin-top:0">Permanência por corpo</h2>
        <table id="tabelaPermanencia"><tr><th>Protocolo</th><th>Identificação</th><th>Situação</th><th class="num">Dias no IML</th><th>Último marco</th></tr>
        ${permanencia.map(({c, dias})=>{ const u = tcinUltimoMarco(ms, c.id_corpo); return `<tr><td><a href="#/corpo/${encodeURIComponent(c.id_corpo)}">${esc(c.protocolo)}</a></td>
          <td>${esc(tcRotuloLista(c))}</td>
          <td><span class="selo ${tcSel(c.situacao)}">${esc(c.situacao)}</span></td>
          <td class="num">${dias > 30 ? `<span class="erro-txt">${dias}</span>` : dias}</td>
          <td>${u ? esc(u.tipo) + " · " + dataBR(u.data_hora) : "—"}</td></tr>`; }).join("") || '<tr><td colspan="5" class="vazio">Nenhum corpo no IML.</td></tr>'}</table></div>
      ${plantao.length ? `<div class="card pendente" id="tcAlertaPlantao"><b>Alerta de passagem de plantão:</b> ${plantao.length} corpo(s) sem movimentação há mais de ${TC_PLANTao_HORAS} h.
        <ul>${plantao.map(c=>`<li>${esc(c.protocolo)} · ${esc(tcRotuloLista(c))} · ${esc(c.situacao)}</li>`).join("")}</ul></div>` : ""}
      <div class="linha-botoes nao-imprimir"><button class="prim" id="btnTcCsv">${icone("download")} Exportar CSV</button>
        <button onclick="window.print()">${icone("imprimir")} Imprimir em A4</button></div>`;
  }
  if (perfil === "plantonista"){
    const colunas = TC_SIT.map(sit=>{
      const lista = cs.filter(c=>c.situacao === sit);
      return `<section class="tc-col"><h3>${esc(sit)} <span class="conta">${lista.length}</span></h3>
        <div class="tc-col-lista">${lista.length ? lista.map(c=>tcinCorpoCard(c, ms)).join("") : '<p class="sub">Nenhum corpo.</p>'}</div></section>`;
    }).join("");
    return `${tcinCabecalho(perfil)}
      <div class="grade">${tcinKpi(por("em custódia"), "em custódia", "data-em-custodia")}
        ${tcinKpi(plantao.length, `sem movimentação há mais de ${TC_PLANTao_HORAS} h`)}
        ${tcinKpi(liberados, "liberados")}</div>
      ${plantao.length ? `<div class="card pendente" id="tcAlertaPlantao"><b>Passagem de plantão:</b> ${plantao.length} corpo(s) sem movimentação há mais de ${TC_PLANTao_HORAS} h.
        ${plantao.map(c=>`<a class="botao" href="#/corpo/${encodeURIComponent(c.id_corpo)}">${esc(c.protocolo)}</a>`).join(" ")}</div>` : ""}
      <div class="tc-quadro" id="tcTabelaPainel">${colunas}</div>`;
  }
  const lista = cs.filter(c=>c.situacao !== "liberado").sort((a, b)=>tcDias(b) - tcDias(a));
  const deslocamento = cs.filter(c=>{ const u = tcinUltimoMarco(ms, c.id_corpo); return u && ["Saída da base", "Saída do local"].includes(u.tipo); }).length;
  return `${tcinCabecalho(perfil)}
    <div class="grade">${tcinKpi(por("em custódia"), "em custódia", "data-em-custodia")}
      ${tcinKpi(deslocamento, "em deslocamento")}
      ${tcinKpi(por("aguardando identificação") + por("não identificado") + por("não reclamado"), "sem identificação ou não reclamados")}</div>
    <div class="card tabela-wrap"><h2 style="margin-top:0">${perfil === "operador" ? "Acionamentos" : "Corpos na sala"}</h2>
      <table id="tcTabelaPainel"><tr><th>Protocolo</th><th>Identificação</th><th>Origem</th><th>Situação</th><th class="num">Dias no IML</th><th>Último marco</th></tr>
      ${lista.map(c=>{ const u = tcinUltimoMarco(ms, c.id_corpo), d = tcDias(c); return `<tr><td><a href="#/corpo/${encodeURIComponent(c.id_corpo)}">${esc(c.protocolo)}</a></td>
        <td>${esc(tcRotuloLista(c))}</td><td>${esc(c.municipio || c.origem)}</td><td><span class="selo ${tcSel(c.situacao)}">${esc(c.situacao)}</span></td>
        <td class="num"><span class="${d > 30 ? "erro-txt" : d > 10 ? "alerta-txt" : ""}">${d}</span></td>
        <td>${u ? esc(u.tipo) + " · " + dataBR(u.data_hora) : "—"}</td></tr>`; }).join("") || '<tr><td colspan="6" class="vazio">Nenhum corpo na sala.</td></tr>'}</table></div>`;
};
TELAS_DEPOIS["#/painel"] = ()=>{
  $("#btnTcCsv")?.addEventListener("click", async ()=>{
    const [cs, ms] = await Promise.all([db.list("corpos"), db.list("marcos")]);
    const linhas = [["id", "protocolo", "situacao", "identificado", "entrada", "dias", "ultimo_marco", "entrega_responsavel", "entrega_documento"]].concat(
      cs.map(c=>{ const ult = ms.filter(m=>m.corpo_id === c.id_corpo).map(m=>m.data_hora).sort().pop() || "";
        return [c.id_corpo, c.protocolo, c.situacao, c.identificado ? "sim" : "não", c.criado_em,
          Math.max(0, Math.round((Date.now() - new Date(c.criado_em)) / 86400000)), ult, c.entrega?.responsavel || "", c.entrega?.documento || ""]; }));
    const csv = "﻿" + linhas.map(l=>l.map(x=>/[;"\n]/.test(String(x)) ? `"${String(x).replace(/"/g, '""')}"` : String(x)).join(";")).join("\r\n");
    baixar(`tcin-${hojeISO()}.csv`, csv, "text/csv;charset=utf-8");
    await registrar("relatório exportado", {detalhe: `${cs.length} corpos`});
  });
};

/* ---------- ficha em abas, sem reescrever as regras dos sprints ---------- */
const tcinFichaAntes = TELAS["#/corpo/:id"];
TELAS["#/corpo/:id"] = async (p)=>{
  const html = await tcinFichaAntes(p);
  if (typeof abas !== "function" || html.includes('class="abas"')) return html;
  const doc = new DOMParser().parseFromString(`<div id="tcinRaiz">${html}</div>`, "text/html");
  const raiz = doc.getElementById("tcinRaiz");
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
  const grupos = {resumo: [], marcos: [], lacres: [], situacao: [], liberacao: [], auditoria: []};
  const destino = h=>{
    if (/marco/.test(h)) return "marcos";
    if (/lacre/.test(h)) return "lacres";
    if (/situa|histórico da situa/.test(h)) return "situacao";
    if (/auto|libera/.test(h)) return "liberacao";
    if (/auditoria|privacidade|reten/.test(h)) return "auditoria";
    return "resumo";
  };
  cards.forEach(c=>grupos[destino((c.querySelector("h2")?.textContent || "").toLowerCase())].push(c.outerHTML));
  const nomes = [["resumo", "Resumo"], ["marcos", "Marcos"], ["lacres", "Lacres"], ["situacao", "Situação"], ["liberacao", "Liberação"], ["auditoria", "Auditoria"]];
  const lista = nomes.filter(([id])=>grupos[id].length).map(([id, titulo])=>({id, titulo, html: grupos[id].join("")}));
  return antes.map(n=>n.outerHTML).join("") + abas("ficha", lista);
};
