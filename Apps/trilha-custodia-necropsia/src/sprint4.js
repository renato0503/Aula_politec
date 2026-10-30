/* ================= Sprint 4 · Auto de entrega e liberação (RN02) ================= */
// a liberação exige identificação, responsável, documento e data
function tcFaltaAuto(c, auto){
  const falta = [];
  if (!c.identificado) falta.push("corpo identificado");
  if (!String(auto?.responsavel || "").trim()) falta.push("responsável pela entrega");
  if (!String(auto?.documento || "").trim()) falta.push("documento do auto");
  if (!String(auto?.data || "").trim()) falta.push("data e hora da entrega");
  return falta;
}
teste("RN02: liberar exige identificação e o auto completo", ()=>{
  const c = {identificado: true}, ok = {responsavel: "Familiar", documento: "AUTO-1", data: "2026-10-30T10:00"};
  return tcFaltaAuto(c, ok).length === 0 && tcFaltaAuto({identificado: false}, ok).join() === "corpo identificado"
    && tcFaltaAuto(c, {responsavel: "Familiar"}).length === 2;
});

async function tcLiberar(id, auto, motivo){
  const c = await db.get("corpos", id);
  if (!c) throw new Error("Corpo não encontrado.");
  if (c.situacao === "liberado") throw new Error("Este corpo já foi liberado.");
  const falta = tcFaltaAuto(c, auto);
  if (falta.length) throw new Error(`A liberação exige ${falta.join(", ")} (RN02).`);
  await db.put("corpos", {...c, situacao: "liberado", entrega: {...auto, motivo: motivo || ""}});
  await db.put("log", {id: uuid(), corpo_id: id, acao: "liberação registrada", perfil: estado.perfil || "", data_hora: agora(),
    motivo: `auto ${auto.documento} · ${auto.responsavel}`});
  await registrar("corpo liberado", {detalhe: `${c.protocolo} · ${auto.documento}`});
  return true;
}

const tcFichaAntiga = TELAS["#/corpo/:id"], tcFichaAntigaDepois = TELAS_DEPOIS["#/corpo/:id"];
TELAS["#/corpo/:id"] = async (p)=>{
  let html = await tcFichaAntiga(p);
  const c = await db.get("corpos", p.id); if (!c) return html;
  const hist = (await db.porIndice("log", "corpo_id", p.id)).filter(l=>/^liberação|^situação/.test(l.acao)).sort((a, b)=>b.data_hora.localeCompare(a.data_hora));
  const card = `<div class="card" id="tcLiberacao"><h2 style="margin-top:0">Auto de entrega e liberação (RN02)</h2>
    ${c.situacao === "liberado" ? `<p class="ok-txt"><b>Liberado</b> para ${esc(c.entrega?.responsavel || "")} · auto ${esc(c.entrega?.documento || "")} · ${dataBR(c.entrega?.data)}</p>`
      : `<p class="sub">${c.identificado ? "O corpo está identificado." : '<b class="erro-txt">O corpo não está identificado: a liberação fica bloqueada (RN02).</b>'}</p>
        <form id="formTcAuto"><div class="campos">
          ${campo("tcAutoResp", "Responsável pela entrega", {valor: c.entrega?.responsavel || ""})}
          ${campo("tcAutoDoc", "Documento do auto", {valor: c.entrega?.documento || ""})}
          ${campo("tcAutoData", "Data e hora", {tipo: "datetime-local", valor: tcAgora()})}</div>
          ${campo("tcAutoMotivo", "Observação", {ajuda: "Ex.: entrega à família, ao IML ou à autoridade."})}
          <div id="tcErrosAuto"></div><div class="linha-botoes"><button class="prim" type="submit" ${c.identificado ? "" : "disabled"}>Registrar a liberação</button></div></form>`}
    ${hist.length ? `<h3>Trilha da liberação</h3><ul class="linha-do-tempo">${hist.map(l=>`<li class="${/liberado/.test(l.acao + " " + (l.motivo || "")) ? "ldt-ok" : "ldt-alerta"}">
      <div class="ldt-quando">${dataBR(l.data_hora)} · ${esc(l.perfil)}</div><b>${esc(l.acao)}</b>${l.motivo ? `<div class="sub" style="margin:0">${esc(l.motivo)}</div>` : ""}</li>`).join("")}</ul>` : ""}</div>`;
  return html + card;
};
TELAS_DEPOIS["#/corpo/:id"] = async (p)=>{
  await tcFichaAntigaDepois(p);
  $("#formTcAuto")?.addEventListener("submit", async e=>{
    e.preventDefault();
    const auto = {responsavel: valorDe("tcAutoResp"), documento: valorDe("tcAutoDoc"), data: valorDe("tcAutoData")};
    try { await tcLiberar(p.id, auto, valorDe("tcAutoMotivo")); toast("Liberação registrada."); navegar(); }
    catch(err){ mostrarErros("#tcErrosAuto", [err.message]); }
  });
};

/* ================= Sprint 5 · Painel do gestor ================= */
const TC_PLANTao_HORAS = 12;
function tcHoras(iso, ate = agora()){ return iso ? Math.max(0, Math.round((new Date(ate) - new Date(iso)) / 3600000 * 10) / 10) : null; }
function tcTempoMedio(lista){ const v = lista.filter(x=>x !== null); return v.length ? Math.round(v.reduce((a, b)=>a + b, 0) / v.length * 10) / 10 : null; }

function tcTempos(cs, ms){
  const remocao = [], identificacao = [], liberacao = [];
  for (const c of cs){
    const marcos = ms.filter(m=>m.corpo_id === c.id_corpo).sort((a, b)=>a.data_hora.localeCompare(b.data_hora));
    const saida = marcos.find(m=>m.tipo === "Saída da base"), chegada = marcos.find(m=>m.tipo === "Chegada ao local");
    if (saida && chegada) remocao.push(tcHoras(saida.data_hora, chegada.data_hora));
    if (c.identificado_em) identificacao.push(tcHoras(c.criado_em, c.identificado_em));
    if (c.entrega?.data && c.identificado_em) liberacao.push(tcHoras(c.identificado_em, c.entrega.data));
  }
  return {remocao: tcTempoMedio(remocao), identificacao: tcTempoMedio(identificacao), liberacao: tcTempoMedio(liberacao)};
}
teste("Sprint 5: o tempo de remoção sai dos marcos de saída e chegada", ()=>{
  const cs = [{id_corpo: "C1", criado_em: "2026-10-01T08:00:00"}];
  const ms = [{corpo_id: "C1", tipo: "Saída da base", data_hora: "2026-10-01T09:00:00"}, {corpo_id: "C1", tipo: "Chegada ao local", data_hora: "2026-10-01T13:00:00"}];
  return tcTempos(cs, ms).remocao === 4;
});

const tcPainelAntigo = TELAS["#/painel"];
TELAS["#/painel"] = async ()=>{
  let html = await tcPainelAntigo();
  const [cs, ms] = await Promise.all([db.list("corpos"), db.list("marcos")]);
  const tempos = tcTempos(cs, ms);
  const permanencia = cs.filter(c=>c.situacao !== "liberado").map(c=>({c, dias: Math.max(0, Math.round((Date.now() - new Date(c.criado_em)) / 86400000))}))
    .sort((a, b)=>b.dias - a.dias);
  const plantao = cs.filter(c=>{
    if (c.situacao === "liberado") return false;
    const ultimo = ms.filter(m=>m.corpo_id === c.id_corpo).map(m=>m.data_hora).sort().pop() || c.criado_em;
    return tcHoras(ultimo) > TC_PLANTao_HORAS;
  });
  return html + `<div class="card" id="tcGestor"><h2 style="margin-top:0">Painel do gestor (Sprint 5)</h2>
      <div class="grade">
        <div class="card kpi"><div class="v" data-tc-ind="remocao">${tempos.remocao === null ? "—" : tempos.remocao + " h"}</div><div class="r">tempo médio de remoção</div></div>
        <div class="card kpi"><div class="v" data-tc-ind="identificacao">${tempos.identificacao === null ? "—" : tempos.identificacao + " h"}</div><div class="r">tempo médio de identificação</div></div>
        <div class="card kpi"><div class="v" data-tc-ind="liberacao">${tempos.liberacao === null ? "—" : tempos.liberacao + " h"}</div><div class="r">tempo médio de liberação</div></div>
        <div class="card kpi"><div class="v" data-tc-ind="plantao">${plantao.length}</div><div class="r">sem movimentação há mais de ${TC_PLANTao_HORAS} h</div></div></div>
      <div class="card tabela-wrap"><h2 style="margin-top:0">Permanência por corpo</h2><table id="tabelaPermanencia"><tr><th>Protocolo</th><th>Situação</th><th class="num">Dias no IML</th></tr>
        ${permanencia.map(({c, dias})=>`<tr><td><a href="#/corpo/${encodeURIComponent(c.id_corpo)}">${esc(c.protocolo)}</a></td>
          <td><span class="selo ${c.situacao === "não reclamado" ? "alerta" : "info"}">${esc(c.situacao)}</span></td>
          <td class="num">${dias > 30 ? `<span class="erro-txt">${dias}</span>` : dias}</td></tr>`).join("") || '<tr><td colspan="3" class="vazio">Nenhum corpo no IML.</td></tr>'}</table></div>
      ${plantao.length ? `<div class="card pendente" id="tcAlertaPlantao"><b>Alerta de passagem de plantão:</b> ${plantao.length} corpo(s) sem movimentação há mais de ${TC_PLANTao_HORAS} h.
        <ul>${plantao.map(c=>`<li>${esc(c.protocolo)} · ${esc(c.situacao)}</li>`).join("")}</ul></div>` : ""}
      <div class="linha-botoes nao-imprimir"><button class="prim" id="btnTcCsv">${icone("download")} Exportar CSV</button>
        <button onclick="window.print()">${icone("imprimir")} Imprimir em A4</button></div></div>`;
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

/* ================= Sprint 6 · Retenção e privacidade ================= */
async function tcApagarCaso(id){
  const c = await db.get("corpos", id);
  if (!c) throw new Error("Corpo não encontrado.");
  if (c.situacao !== "liberado") throw new Error("Só apaga os dados de um caso encerrado (liberado).");
  for (const m of await db.porIndice("marcos", "corpo_id", id)) await db.del("marcos", m.id_marco);
  for (const l of await db.porIndice("lacres", "corpo_id", id)) await db.del("lacres", l.id_lacre);
  for (const x of (await db.list("log")).filter(l=>l.corpo_id === id)) await db.del("log", x.id);
  await db.del("corpos", id);
  const atual = (await db.get("contagens", "tcin_apagados"))?.valor || 0;
  await db.put("contagens", {chave: "tcin_apagados", valor: atual + 1});
  await registrar("caso encerrado apagado", {detalhe: c.protocolo});
}
teste("Sprint 6: só apaga caso liberado", async ()=> typeof tcApagarCaso === "function");

const tcFichaDepoisS6 = TELAS_DEPOIS["#/corpo/:id"];
TELAS_DEPOIS["#/corpo/:id"] = async (p)=>{
  await tcFichaDepoisS6(p);
  const c = await db.get("corpos", p.id); if (!c || c.situacao !== "liberado") return;
  const bloco = document.createElement("div");
  bloco.className = "card";
  bloco.innerHTML = `<h2 style="margin-top:0">Privacidade e retenção</h2>
    <p class="sub">Depois da liberação, os dados pessoais do caso podem ser apagados. Fica só a contagem. O texto de privacidade está em <code>modelos/privacidade.md</code>.</p>
    <div class="linha-botoes"><button class="perigo" id="btnTcApagar">Apagar os dados deste caso</button></div>`;
  $("#conteudo").appendChild(bloco);
  $("#btnTcApagar").addEventListener("click", async ()=>{
    if (!confirm("Apagar os dados deste caso liberado? A contagem fica guardada.")) return;
    try { await tcApagarCaso(p.id); toast("Caso apagado; a contagem ficou guardada."); location.hash = "#/painel"; }
    catch(err){ alert(err.message); }
  });
};
