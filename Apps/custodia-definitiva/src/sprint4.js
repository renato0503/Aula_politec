/* ================= Sprint 4 · Projeção de ocupação e saturação ================= */
// regra de descarte por categoria (anos após a entrada) — premissa, ver PREMISSAS.md
const CD_DESCARTE_ANOS = {entorpecentes: 5, "armas-brancas": 10, roupas: 2, eletronicos: 5, biologicos: 1};

function cdProjecao(historico, meses = 6){
  const serie = [...historico].sort((a, b)=>a.mes.localeCompare(b.mes));
  if (!serie.length) return {mensal: [], saldo: 0, ocupacao: 0};
  const janela = serie.slice(-12);
  const entradas = janela.reduce((a, h)=>a + Number(h.entradas || 0), 0) / janela.length;
  const saidas = janela.reduce((a, h)=>a + Number(h.saidas || 0), 0) / janela.length;
  const saldo = Math.round(entradas - saidas);
  let atual = Number(serie[serie.length - 1].ocupacao_final || 0);
  const mensal = [];
  for (let i = 1; i <= meses; i++){ atual = Math.max(0, atual + saldo); mensal.push({mes: "M+" + i, ocupacao: Math.round(atual)}); }
  return {mensal, saldo, entradas: Math.round(entradas), saidas: Math.round(saidas), ocupacao: Number(serie[serie.length - 1].ocupacao_final || 0)};
}
teste("Sprint 4: a projeção soma o saldo médio mês a mês", ()=>{
  const h = [{mes: "2026-01-01", entradas: 100, saidas: 100, ocupacao_final: 200},
             {mes: "2026-02-01", entradas: 120, saidas: 80, ocupacao_final: 240}];
  const r = cdProjecao(h, 2);
  return r.saldo === 20 && r.mensal[0].ocupacao === 260 && r.mensal[1].ocupacao === 280 && r.ocupacao === 240;
});

function cdOcupacaoConteiner(c, vestigios){ return Math.round(vestigios.filter(v=>v.conteiner_id === c.id_conteiner).reduce((a, v)=>a + Number(v.volume_ocupado || 0), 0)); }
function cdSaturacao(c, vestigios, limite = 85){
  const ocupado = cdOcupacaoConteiner(c, vestigios), cap = Number(c.capacidade || 0);
  const pct = cap ? Math.round(ocupado / cap * 100) : 0;
  return {ocupado, cap, pct, alerta: pct >= limite};
}
teste("Sprint 4: contêiner acima de 85% entra em alerta", ()=>{
  const c = {id_conteiner: "C1", capacidade: 100}, vs = [{conteiner_id: "C1", volume_ocupado: 90}];
  return cdSaturacao(c, vs).alerta && !cdSaturacao({...c, capacidade: 200}, vs).alerta;
});

/* ================= Sprint 5 · Descarte com autorização humana ================= */
function cdIdadeAnos(v, hoje = hojeISO()){ return v?.data_entrada ? Math.floor((new Date(hoje) - new Date(v.data_entrada)) / (365.25 * 86400000) * 10) / 10 : 0; }
function cdDescarteApto(v, categoria, hoje = hojeISO()){
  const anos = CD_DESCARTE_ANOS[categoria?.id_categoria] ?? 5;
  const idade = cdIdadeAnos(v, hoje);
  const apto = idade >= anos;
  return {apto, idade, anos, motivo: apto ? `passou ${anos} ano(s) na guarda` : `faltam ${Math.round((anos - idade) * 10) / 10} ano(s)`};
}
teste("Sprint 5: descarte só depois do prazo da categoria", ()=>{
  const cat = {id_categoria: "roupas"};
  return cdDescarteApto({data_entrada: "2020-01-01"}, cat, "2026-10-30").apto
    && !cdDescarteApto({data_entrada: "2026-01-01"}, cat, "2026-10-30").apto;
});
// sem autorização registrada, o descarte é bloqueado
function cdPodeDescartar(v, autorizacao){ return !!(autorizacao && autorizacao.autorizado_por); }
teste("Sprint 5: descarte sem autorização é bloqueado", ()=>{
  return !cdPodeDescartar({}, null) && !cdPodeDescartar({}, {autorizado_por: ""}) && cdPodeDescartar({}, {autorizado_por: "Gestor"});
});

async function cdDescartes(id){ return (await db.porIndice("descartes", "vestigio_id", id)).sort((a, b)=>(a.autorizado_em || "").localeCompare(b.autorizado_em || "")); }

const cdFichaAntiga = TELAS["#/vestigio/:id"], cdFichaAntigaDepois = TELAS_DEPOIS["#/vestigio/:id"];
TELAS["#/vestigio/:id"] = async (p)=>{
  let html = await cdFichaAntiga(p);
  const v = await db.get("vestigios", p.id); if (!v) return html;
  const cats = await cdCategorias(), ds = await cdDescartes(p.id), apto = cdDescarteApto(v, cats[v.categoria_id]);
  const auth = ds.filter(d=>d.autorizado_por).pop();
  const card = `<div class="card" id="cdDescarte"><h2 style="margin-top:0">Descarte (Sprint 5)</h2>
    <p>Idade na guarda: <b>${apto.idade} ano(s)</b> · regra da categoria: <b>${apto.anos} ano(s)</b> ·
      ${apto.apto ? '<span class="selo ok">apto</span>' : `<span class="selo info">não apto (${esc(apto.motivo)})</span>`}</p>
    ${v.status === "descartado" ? '<p class="sub">Vestígio já descartado.</p>' : `
      ${auth ? `<p class="ok-txt">Autorizado por ${esc(auth.autorizado_por)} em ${dataCurtaBR(auth.autorizado_em)}.</p>`
        : apto.apto ? `<form id="formCdAutorizar"><div class="campos">${campo("cdAuthPor", "Autorizado por", {valor: "Gestor da custódia"})}</div>
            ${campo("cdAuthMotivo", "Motivo (mínimo de 15 caracteres)", {tipo: "textarea", linhas: 2})}
            <div id="cdErrosDescarte"></div><div class="linha-botoes"><button type="submit">Autorizar o descarte</button></div></form>`
          : '<p class="sub">O descarte só é possível depois do prazo da categoria.</p>'}
      ${auth ? `<div class="linha-botoes"><button class="perigo" id="btnCdDescartar">Descartar o vestígio</button></div>` : ""}`}</div>`;
  return html + card;
};
TELAS_DEPOIS["#/vestigio/:id"] = async (p)=>{
  await cdFichaAntigaDepois(p);
  $("#formCdAutorizar")?.addEventListener("submit", async e=>{
    e.preventDefault();
    const motivo = valorDe("cdAuthMotivo"), por = valorDe("cdAuthPor");
    if (motivo.length < 15) return mostrarErros("#cdErrosDescarte", ["Escreva o motivo com pelo menos 15 caracteres."]);
    await db.put("descartes", {id: uuid(), vestigio_id: p.id, autorizado_por: por || "Gestor", motivo, autorizado_em: hojeISO(), perfil: estado.perfil});
    await registrar("descarte autorizado", {detalhe: p.id}); toast("Descarte autorizado."); navegar();
  });
  $("#btnCdDescartar")?.addEventListener("click", async ()=>{
    if (!confirm("Descartar este vestígio? A ação fica registrada.")) return;
    const v = await db.get("vestigios", p.id);
    await db.put("vestigios", {...v, status: "descartado"});
    await db.put("movimentacoes", {id_movimentacao: uuid(), vestigio_id: p.id, tipo: "descarte", data_hora: agora(), responsavel: estado.perfil || "",
      origem: `${v.conteiner_id} · ${v.posicao}`, destino: "descarte", motivo: "descarte autorizado"});
    await registrar("vestígio descartado", {detalhe: p.id}); toast("Vestígio descartado."); navegar();
  });
};

/* ================= Sprint 6 · Painel do gestor e relatório ================= */
function cdBarras(titulo, pares, cor = "var(--accent)"){
  const max = Math.max(1, ...pares.map(([, n])=>n)), w = 420, h = 26;
  return `<div class="card"><h2 style="margin-top:0">${esc(titulo)}</h2>
    <svg viewBox="0 0 ${w} ${Math.max(60, pares.length * h + 10)}" role="img" aria-label="${esc(titulo)}" style="width:100%;height:auto">
      ${pares.map(([rot, n], i)=>{ const d = Math.round(n / max * (w - 170)), y = i * h + 6;
        return `<text x="0" y="${y + 13}" font-size="12" fill="var(--ink2)">${esc(String(rot).slice(0, 22))}</text>
          <rect x="150" y="${y + 2}" width="${d}" height="14" rx="3" fill="${cor}"></rect>
          <text x="${156 + d}" y="${y + 13}" font-size="12" fill="var(--ink)">${n}</text>`; }).join("")}
    </svg></div>`;
}

const cdPainelAntigo = TELAS["#/painel"];
TELAS["#/painel"] = async ()=>{
  let html = await cdPainelAntigo();
  const [vs, cs, cats, hist, movs] = await Promise.all([db.list("vestigios"), db.list("conteineres"), cdCategorias(),
    db.list("historico_mensal"), db.list("movimentacoes")]);
  const proj = cdProjecao(hist, 6);
  const sat = cs.map(c=>({c, ...cdSaturacao(c, vs)})).sort((a, b)=>b.pct - a.pct);
  const porCategoria = Object.values(cats).map(c=>[c.nome, vs.filter(v=>v.categoria_id === c.id_categoria).length]).sort((a, b)=>b[1] - a[1]);
  const porConteiner = cs.map(c=>[c.id_conteiner, vs.filter(v=>v.conteiner_id === c.id_conteiner).length]).sort((a, b)=>b[1] - a[1]);
  const entradasPorMes = hist.sort((a, b)=>a.mes.localeCompare(b.mes)).slice(-6).map(h=>[h.id_periodo, Number(h.entradas || 0)]);
  // tempo de localização: dias entre a entrada e a primeira movimentação (premissa antes/depois)
  const tempos = vs.map(v=>{
    const m = movs.filter(x=>x.vestigio_id === v.id_vestigio).map(x=>x.data_hora.slice(0, 10)).sort()[0];
    return m ? Math.max(0, Math.round((new Date(m) - new Date(v.data_entrada)) / 86400000)) : null;
  }).filter(x=>x !== null);
  const tempoMedio = tempos.length ? Math.round(tempos.reduce((a, b)=>a + b, 0) / tempos.length * 10) / 10 : null;
  return html + `<div class="card" id="cdGestor"><h2 style="margin-top:0">Painel do gestor (Sprint 6)</h2>
      <p class="sub">Ocupação projetada a partir da série de 12 meses. Saldo médio de ${proj.saldo} item(ns) por mês (${proj.entradas} entradas e ${proj.saidas} saídas).</p>
      <div class="grade">
        <div class="card kpi"><div class="v" data-cd-ind="ocupacao">${proj.ocupacao}</div><div class="r">itens no acervo</div></div>
        <div class="card kpi"><div class="v" data-cd-ind="projecao">${proj.mensal.length ? proj.mensal[proj.mensal.length - 1].ocupacao : "—"}</div><div class="r">projeção em 6 meses</div></div>
        <div class="card kpi"><div class="v" data-cd-ind="saturados">${sat.filter(x=>x.alerta).length}</div><div class="r">contêineres em alerta (85%)</div></div>
        <div class="card kpi"><div class="v" data-cd-ind="localizacao">${tempoMedio === null ? "—" : tempoMedio + " dia(s)"}</div><div class="r">tempo médio até a 1ª movimentação</div></div></div>
      ${cdBarras("Itens por categoria", porCategoria)}
      ${cdBarras("Itens por contêiner", porConteiner, "var(--verde)")}
      ${cdBarras("Entradas por mês (últimos 6)", entradasPorMes, "var(--ambar)")}
      <div class="card tabela-wrap"><h2 style="margin-top:0">Saturação por contêiner</h2><table id="tabelaSat"><tr><th>Contêiner</th><th class="num">Ocupado</th><th class="num">Capacidade</th><th class="num">%</th><th></th></tr>
        ${sat.map(({c, ocupado, cap, pct, alerta})=>`<tr><td>${esc(c.id_conteiner)}</td><td class="num">${ocupado}</td><td class="num">${cap}</td>
          <td class="num">${pct}%</td><td>${alerta ? '<span class="selo erro">saturação</span>' : '<span class="selo ok">ok</span>'}</td></tr>`).join("")}</table></div>
      <div class="linha-botoes nao-imprimir"><button class="prim" id="btnCdCsvGestor">${icone("download")} Exportar CSV</button>
        <button onclick="window.print()">${icone("imprimir")} Imprimir em A4</button></div></div>`;
};
TELAS_DEPOIS["#/painel"] = ()=>{
  $("#btnCdCsvGestor")?.addEventListener("click", async ()=>{
    const [vs, cs, cats] = await Promise.all([db.list("vestigios"), db.list("conteineres"), cdCategorias()]);
    const linhas = [["id", "protocolo", "lacre", "categoria", "conteiner", "posicao", "volume", "entrada", "situacao", "dias_na_guarda"]].concat(
      vs.map(v=>[v.id_vestigio, v.protocolo, v.lacre, cats[v.categoria_id]?.nome || v.categoria_id, v.conteiner_id || "", v.posicao || "",
        v.volume_ocupado, v.data_entrada, v.status, Math.round((new Date() - new Date(v.data_entrada)) / 86400000)]));
    const csv = "﻿" + linhas.map(l=>l.map(c=>/[;"\n]/.test(String(c)) ? `"${String(c).replace(/"/g, '""')}"` : String(c)).join(";")).join("\r\n");
    baixar(`custodia-${hojeISO()}.csv`, csv, "text/csv;charset=utf-8");
    await registrar("relatório de ocupação exportado", {detalhe: `${vs.length} vestígios`});
  });
};
