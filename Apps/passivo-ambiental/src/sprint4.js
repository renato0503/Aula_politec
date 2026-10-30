/* ================= Sprint 4 · Conclusão com assinatura ================= */
const PA_META_HORAS = 12;
const PA_COMPLEXIDADE = {"desmatamento": 3, "queimada": 2, "extração irregular de madeira": 3, "ocupação irregular de área de preservação": 2,
                         "poluição de curso d'água": 3, "mineração irregular": 3};

async function paAssinaturas(id){ return (await db.porIndice("assinaturas", "requisicao_id", id)).sort((a, b)=>(a.data || "").localeCompare(b.data || "")); }
function paFaltaAssinatura(assinatura){
  const falta = [];
  if (!assinatura) return ["assinatura do perito"];
  if (!String(assinatura.nome || "").trim()) falta.push("nome do perito");
  if (!String(assinatura.cargo || "").trim()) falta.push("cargo ou matrícula");
  return falta;
}
teste("Sprint 4: a conclusão exige nome e cargo do perito", ()=>{
  return paFaltaAssinatura(null).length === 1 && paFaltaAssinatura({nome: "", cargo: ""}).length === 2
    && paFaltaAssinatura({nome: "Perito", cargo: "Perito criminal"}).length === 0;
});

const paLaudoAntigoDepois = TELAS_DEPOIS["#/laudo/:id"];
const paLaudoAntigo = TELAS["#/laudo/:id"];
TELAS["#/laudo/:id"] = async (p)=>{
  let html = await paLaudoAntigo(p);
  const {r, l, mapas} = await paLaudoDe(p.id);
  if (!r) return html;
  const assin = await paAssinaturas(p.id);
  const card = `<div class="card" id="paAssinatura"><h2 style="margin-top:0">Assinatura do laudo (Sprint 4)</h2>
    ${assin.length ? `<p class="ok-txt">Assinado por <b>${esc(assin[assin.length - 1].nome)}</b> (${esc(assin[assin.length - 1].cargo)}) em ${dataBR(assin[assin.length - 1].data)}.</p>`
      : `<p class="sub">A conclusão registra a assinatura do perito responsável.</p>
        <div class="campos">${campo("paAssNome", "Perito responsável", {valor: "Perito Fictício"})}${campo("paAssCargo", "Cargo ou matrícula", {valor: "Perito criminal"})}</div>`}
    <p class="sub">Mapas anexados: <b>${mapas.length}</b> · cabeçalho ${paCabecalho(r, l).every(([, v])=>String(v || "").trim() && !/não informad/i.test(v)) ? "completo" : "incompleto"}.</p></div>`;
  return html + card;
};
TELAS_DEPOIS["#/laudo/:id"] = async (p)=>{
  await paLaudoAntigoDepois(p);
  const btn = $("#btnPaConcluir"); if (!btn) return;
  const novo = btn.cloneNode(true); btn.replaceWith(novo);   // troca o comportamento do Sprint 2
  novo.addEventListener("click", async ()=>{
    const {r, l, mapas} = await paLaudoDe(p.id);
    const assinatura = {nome: valorDe("paAssNome"), cargo: valorDe("paAssCargo"), data: agora(), perfil: estado.perfil};
    const cab = paCabecalho(r, l);
    const semCab = cab.filter(([, v])=>!String(v || "").trim() || /não informad/i.test(v)).map(([k])=>k);
    const erros = [
      ...semCab.map(k=>`Cabeçalho incompleto: ${k}.`),
      !mapas.length && "Anexe pelo menos 1 mapa temático (RN03).",
      ...paFaltaAssinatura($("#paAssNome") ? assinatura : (await paAssinaturas(p.id)).pop() || null).map(f=>`Falta ${f}.`),
    ].filter(Boolean);
    if (!mostrarErros("#paErrosLaudo", erros)) return;
    if (!(await paAssinaturas(p.id)).length)
      await db.put("assinaturas", {id: uuid(), requisicao_id: p.id, laudo_id: l.id_laudo, nome: assinatura.nome, cargo: assinatura.cargo, data: assinatura.data, perfil: estado.perfil});
    await db.put("laudos", {...l, status: "concluido", concluido_em: agora()});
    await db.put("requisicoes", {...r, status: "concluida"});
    await registrar("laudo concluído com assinatura", {detalhe: l.id_laudo});
    toast("Laudo concluído e assinado."); navegar();
  });
};

/* ================= Sprint 5 e 6 · Fila, prioridade e produtividade ================= */
function paComplexidade(r){ return PA_COMPLEXIDADE[r.tipo_infracao] || 2; }
// fila: primeiro o atraso, depois a complexidade (maior primeiro)
function paFila(requisicoes, hoje = hojeISO()){
  return requisicoes.filter(r=>r.status !== "concluida").map(r=>({r, dias: paDias(r.data_requisicao, hoje), atraso: paAtrasada(r, hoje), complexidade: paComplexidade(r)}))
    .sort((a, b)=>(b.atraso - a.atraso) || (b.complexidade - a.complexidade) || (b.dias - a.dias));
}
teste("Sprint 5: a fila põe o atrasado antes, e o mais complexo primeiro", ()=>{
  const hoje = "2026-10-30";
  const rs = [{id_requisicao: "A", data_requisicao: "2026-10-28", prazo_dias: 10, tipo_infracao: "desmatamento", status: "laudo"},
              {id_requisicao: "B", data_requisicao: "2026-10-01", prazo_dias: 10, tipo_infracao: "queimada", status: "laudo"},
              {id_requisicao: "C", data_requisicao: "2026-10-01", prazo_dias: 10, tipo_infracao: "desmatamento", status: "laudo"}];
  return paFila(rs, hoje).map(x=>x.r.id_requisicao).join() === "C,B,A";
});

function paDiasEntre(a, b){ return Math.max(0, Math.round((new Date(b + "T12:00:00") - new Date(a + "T12:00:00")) / 86400000)); }
// tempo por laudo: dias da requisição até a conclusão
function paTempoLaudo(rs, ls){
  const concluidos = ls.filter(l=>l.status === "concluido" && l.concluido_em);
  return concluidos.map(l=>{
    const r = rs.find(x=>x.id_requisicao === l.requisicao_id);
    return r ? {id: l.id_laudo, tipo: r.tipo_infracao, horas: Number(l.horas_trabalhadas || 0),
      dias: paDiasEntre(r.data_requisicao, l.concluido_em.slice(0, 10))} : null;
  }).filter(Boolean);
}
teste("Sprint 6: o tempo do laudo conta da requisição à conclusão", ()=>{
  const rs = [{id_requisicao: "R1", tipo_infracao: "queimada", data_requisicao: "2026-10-01"}];
  const ls = [{id_laudo: "L1", requisicao_id: "R1", status: "concluido", horas_trabalhadas: 16, concluido_em: "2026-10-05T10:00:00"}];
  const t = paTempoLaudo(rs, ls); return t.length === 1 && t[0].dias === 4 && t[0].horas === 16;
});

function paBarras(titulo, pares, cor = "var(--accent)"){
  const max = Math.max(1, ...pares.map(([, n])=>n)), w = 420, h = 26;
  return `<div class="card"><h2 style="margin-top:0">${esc(titulo)}</h2>
    <svg viewBox="0 0 ${w} ${Math.max(60, pares.length * h + 10)}" role="img" aria-label="${esc(titulo)}" style="width:100%;height:auto">
      ${pares.map(([rot, n], i)=>{ const d = Math.round(n / max * (w - 170)), y = i * h + 6;
        return `<text x="0" y="${y + 13}" font-size="12" fill="var(--ink2)">${esc(String(rot).slice(0, 22))}</text>
          <rect x="150" y="${y + 2}" width="${d}" height="14" rx="3" fill="${cor}"></rect>
          <text x="${156 + d}" y="${y + 13}" font-size="12" fill="var(--ink)">${n}</text>`; }).join("")}
    </svg></div>`;
}

const paPainelAntigo = TELAS["#/painel"];
TELAS["#/painel"] = async ()=>{
  let html = await paPainelAntigo();
  const [rs, ls] = await Promise.all([db.list("requisicoes"), db.list("laudos")]);
  const fila = paFila(rs), tempos = paTempoLaudo(rs, ls);
  const porTipo = Object.entries(ls.reduce((a, l)=>{
    const r = rs.find(x=>x.id_requisicao === l.requisicao_id); const k = r?.tipo_infracao || "—";
    a[k] = (a[k] || 0) + Number(l.horas_trabalhadas || 0); return a; }, {})).sort((a, b)=>b[1] - a[1]);
  const diasMedios = tempos.length ? Math.round(tempos.reduce((a, t)=>a + t.dias, 0) / tempos.length * 10) / 10 : null;
  const horasMedias = tempos.length ? Math.round(tempos.reduce((a, t)=>a + t.horas, 0) / tempos.length * 10) / 10 : null;
  return html + `<div class="card" id="paGestor"><h2 style="margin-top:0">Fila e produtividade (Sprint 5 e 6)</h2>
      <div class="grade">
        <div class="card kpi"><div class="v" data-pa-ind="fila">${fila.length}</div><div class="r">na fila</div></div>
        <div class="card kpi"><div class="v" data-pa-ind="atrasados">${fila.filter(x=>x.atraso).length}</div><div class="r">atrasados</div></div>
        <div class="card kpi"><div class="v" data-pa-ind="dias">${diasMedios === null ? "—" : diasMedios + " dia(s)"}</div><div class="r">tempo médio do laudo</div></div>
        <div class="card kpi"><div class="v" data-pa-ind="horas">${horasMedias === null ? "—" : horasMedias + " h"}</div><div class="r">horas médias por laudo (meta ${PA_META_HORAS} h)</div></div></div>
      <div class="card tabela-wrap"><h2 style="margin-top:0">Fila priorizada (prazo e complexidade)</h2><table id="tabelaFila"><tr><th>#</th><th>Requisição</th><th>Tipo</th><th class="num">Dias</th><th class="num">Complexidade</th><th>Alerta</th></tr>
        ${fila.map((x, i)=>`<tr><td class="num">${i + 1}</td><td><a href="#/laudo/${encodeURIComponent(x.r.id_requisicao)}">${esc(x.r.numero_processo)}</a></td>
          <td>${esc(x.r.tipo_infracao)}</td><td class="num">${x.dias}</td><td class="num">${x.complexidade}</td>
          <td>${x.atraso ? '<span class="selo erro">fora do prazo</span>' : paRestantes(x.r) <= 3 ? '<span class="selo alerta">vence em até 3 dias</span>' : '<span class="selo ok">no prazo</span>'}</td></tr>`).join("")
          || '<tr><td colspan="6" class="vazio">Fila vazia.</td></tr>'}</table></div>
      ${paBarras("Horas por tipo de infração", porTipo, "var(--verde)")}
      <div class="linha-botoes nao-imprimir"><button class="prim" id="btnPaCsv">${icone("download")} Exportar CSV</button>
        <button onclick="window.print()">${icone("imprimir")} Imprimir em A4</button></div></div>`;
};
TELAS_DEPOIS["#/painel"] = ()=>{
  $("#btnPaCsv")?.addEventListener("click", async ()=>{
    const [rs, ls] = await Promise.all([db.list("requisicoes"), db.list("laudos")]);
    const linhas = [["requisicao", "numero", "orgao", "tipo", "requisicao_data", "prazo_dias", "situacao", "dias_decorridos", "laudo", "horas", "laudo_status"]].concat(
      rs.map(r=>{ const l = ls.find(x=>x.requisicao_id === r.id_requisicao);
        return [r.id_requisicao, r.numero_processo, r.orgao, r.tipo_infracao, r.data_requisicao, r.prazo_dias, r.status,
          paDias(r.data_requisicao), l?.id_laudo || "", l?.horas_trabalhadas ?? "", l?.status || ""]; }));
    const csv = "﻿" + linhas.map(l=>l.map(x=>/[;"\n]/.test(String(x)) ? `"${String(x).replace(/"/g, '""')}"` : String(x)).join(";")).join("\r\n");
    baixar(`passivo-${hojeISO()}.csv`, csv, "text/csv;charset=utf-8");
    await registrar("relatório de produtividade exportado", {detalhe: `${rs.length} requisições`});
  });
};
