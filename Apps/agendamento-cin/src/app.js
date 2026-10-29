/* Agendamento CIN · código do app (o construir.py junta com a base comum) */
"use strict";
/* ---------- grade de horários (a mesma regra está no Code.gs) ---------- */
// grade = {de, ate, dias: [1..5] (0 = domingo), inicio: "08:00", fim: "16:00", intervalo: 30, vagas: 2}
function horariosDaGrade(postoId, g){
  const out = [], [hi, mi] = g.inicio.split(":").map(Number), [hf, mf] = g.fim.split(":").map(Number);
  for (let t = Date.UTC(...g.de.split("-").map((n, i)=>i === 1 ? n - 1 : +n)); ; t += 86400000){
    const d = new Date(t), data = d.toISOString().slice(0, 10); if (data > g.ate) break;
    if (!g.dias.includes(d.getUTCDay())) continue;
    for (let m = hi * 60 + mi; m < hf * 60 + mf; m += g.intervalo){
      const hora = String(Math.floor(m / 60)).padStart(2, "0") + ":" + String(m % 60).padStart(2, "0");
      out.push({horario_id: `${postoId}-${data}-${hora.replace(":", "")}`, posto_id: postoId, data, hora, capacidade: g.vagas, ocupadas: 0, situacao: "aberto"});
    }
  }
  return out;
}
teste("grade de 2 semanas úteis, 08h às 16h de 30 em 30 = 160 horários", ()=>
  horariosDaGrade("P01", {de: "2026-11-16", ate: "2026-11-27", dias: [1, 2, 3, 4, 5], inicio: "08:00", fim: "16:00", intervalo: 30, vagas: 2}).length === 160);
teste("grade não inclui sábado e domingo", ()=>
  horariosDaGrade("P01", {de: "2026-11-21", ate: "2026-11-22", dias: [1, 2, 3, 4, 5], inicio: "08:00", fim: "09:00", intervalo: 30, vagas: 1}).length === 0);

/* ---------- API: Apps Script quando publicado, IndexedDB no teste local ---------- */
const NO_APPS_SCRIPT = typeof google !== "undefined" && google.script && google.script.run;
// RN05 no modo local: mesma conferência que o Code.gs faz no servidor
async function exigirPosto(postoId){
  const eu = await api.quemSou();
  if (eu.perfil === "gestao") return eu;
  if (eu.perfil !== "posto" || eu.posto_id !== postoId) throw new Error(`Sem permissão para o posto ${postoId} (RN05).`);
  return eu;
}
async function exigirGestao(){ const eu = await api.quemSou(); if (eu.perfil !== "gestao") throw new Error("Só a gestão cadastra postos."); return eu; }
const api = NO_APPS_SCRIPT ? new Proxy({}, {
  get: (_, fn)=>(...args)=>new Promise((ok, erro)=>google.script.run.withSuccessHandler(ok).withFailureHandler(erro)[fn](...args))
}) : {
  // Modo local: as mesmas funções do Code.gs, sobre os dados fictícios da planilha modelo.
  async listarPostos(){ return (await db.list("postos")).filter(p=>p.ativo === true || p.ativo === "TRUE"); },
  async listarHorarios(posto_id){ return (await db.porIndice("horarios", "posto_id", posto_id)).filter(h=>h.situacao === "aberto"); },
  async quemSou(){ return {email: "teste.local", perfil: (await db.meta("perfil")) || null, posto_id: (await db.meta("posto_id")) || "P01"}; },
  async listarTodosPostos(){ await exigirGestao(); return db.list("postos"); },
  async salvarPosto(p){
    await exigirGestao();
    if (!p.posto_id || !p.nome || !p.municipio) throw new Error("Informe código, nome e município do posto.");
    await db.put("postos", {...(await db.get("postos", p.posto_id) || {}), ...p}); await registrar("posto salvo", {detalhe: p.posto_id}); return true;
  },
  async listarHorariosPosto(posto_id, de, ate){
    await exigirPosto(posto_id);
    return (await db.porIndice("horarios", "posto_id", posto_id)).filter(h=>h.data >= de && h.data <= ate).sort((a, b)=>(a.data + a.hora).localeCompare(b.data + b.hora));
  },
  async gerarHorarios(posto_id, grade){
    await exigirPosto(posto_id);
    let criados = 0, existentes = 0;
    for (const h of horariosDaGrade(posto_id, grade)){
      if (await db.get("horarios", h.horario_id)) existentes++; else { await db.put("horarios", h); criados++; }
    }
    await registrar("horários gerados", {detalhe: `${posto_id}: ${criados} novos`}); return {criados, existentes};
  },
  async bloquear(posto_id, alvo, bloquear){
    await exigirPosto(posto_id);
    const hs = (await db.porIndice("horarios", "posto_id", posto_id)).filter(h=>alvo.horario_id ? h.horario_id === alvo.horario_id : h.data === alvo.data);
    for (const h of hs) await db.put("horarios", {...h, situacao: bloquear ? "bloqueado" : "aberto"});
    await registrar(bloquear ? "bloqueio" : "desbloqueio", {detalhe: alvo.horario_id || `${posto_id} ${alvo.data}`}); return hs.length;
  }
};
async function iniciarApp(){
  if (NO_APPS_SCRIPT){
    APP.perfilDoServidor = true;
    const eu = await api.quemSou(); estado.perfil = eu.perfil; estado.posto_id = eu.posto_id;
  } else {
    if (!(await db.list("postos")).length) await db.importar({app: APP.id, dados: dadosEmbutidos("seed")}, true);
    estado.posto_id = (await db.meta("posto_id")) || "P01";
  }
}
teste("Modo local carrega 2 postos ativos", async ()=> (await api.listarPostos()).length === 2);
teste("Horários abertos do posto P01", async ()=> (await api.listarHorarios("P01")).length > 0);

// No teste local, a configuração escolhe de qual posto é esta cópia.
async function configExtra(){
  if (NO_APPS_SCRIPT) return "";
  const postos = await db.list("postos");
  return `<div class="card"><h2 style="margin-top:0">Posto desta cópia (teste local)</h2>
    ${campo("cfgPosto", "Posto", {tipo: "select", opcoes: postos.map(p=>[p.posto_id, `${p.posto_id} · ${p.nome}`]), valor: estado.posto_id})}</div>`;
}
async function ligarConfigExtra(){
  $("#cfgPosto")?.addEventListener("change", async e=>{ await db.meta("posto_id", e.target.value); estado.posto_id = e.target.value; toast("Posto da cópia: " + e.target.value); });
}

TELAS["#/agendar"] = async ()=>{
  const postos = await api.listarPostos();
  return `<h1>Agendar a Carteira de Identidade</h1><p class="sub">Escolha o posto. O calendário com as vagas chega no Sprint 3.</p>
    ${NO_APPS_SCRIPT ? "" : `<p class="selo alerta">Modo de teste local, com dados fictícios</p>`}
    <div class="grade">${postos.map(p=>`<div class="card"><b>${esc(p.nome)}</b><br><span class="sub">${esc(p.municipio)} · ${esc(p.endereco)}</span></div>`).join("")}</div>
    <p class="sub"><a href="#/consultar">Consultar ou cancelar uma reserva</a>${NO_APPS_SCRIPT ? "" : ` · <a href="#/posto">Área do posto (teste)</a>`}</p>`;
};

/* ================= Sprint 2 · Postos e horários ================= */
const DIAS = [["1", "seg"], ["2", "ter"], ["3", "qua"], ["4", "qui"], ["5", "sex"], ["6", "sáb"], ["0", "dom"]];
const somarDias = (iso, n)=> new Date(Date.UTC(...iso.split("-").map((x, i)=>i === 1 ? x - 1 : +x)) + n * 86400000).toISOString().slice(0, 10);
const proximaSegunda = ()=>{ const h = hojeISO(), d = new Date(h + "T12:00:00Z").getUTCDay(); return somarDias(h, ((8 - d) % 7) || 7); };

TELAS["#/posto/horarios"] = async ()=>{
  const de = proximaSegunda(), ate = somarDias(de, 11);
  const posto = (await api.listarPostos()).find(p=>p.posto_id === estado.posto_id);
  return `<h1>Horários · ${esc(posto?.nome || estado.posto_id)}</h1><p class="sub">Monte a grade da semana e gere os horários do período. Horário que já existe não é duplicado.</p>
    <form class="card" id="formGrade"><h2 style="margin-top:0">Grade</h2><div class="campos">
      ${campo("gDe", "De", {tipo: "date", valor: de, obrigatorio: true})}${campo("gAte", "Até", {tipo: "date", valor: ate, obrigatorio: true})}
      ${campo("gInicio", "Primeiro horário", {tipo: "time", valor: "08:00"})}${campo("gFim", "Encerra às", {tipo: "time", valor: "16:00"})}
      ${campo("gIntervalo", "Intervalo (min)", {tipo: "number", valor: 30, attrs: 'min="5" step="5"'})}${campo("gVagas", "Vagas por horário", {tipo: "number", valor: 2, attrs: 'min="1"'})}</div>
      <p>Dias: ${DIAS.map(([v, n])=>`<label style="display:inline-flex;gap:4px;margin-right:10px"><input type="checkbox" data-dia="${v}" style="width:auto" ${+v >= 1 && +v <= 5 ? "checked" : ""}>${n}</label>`).join("")}</p>
      <div id="errosGrade"></div><div class="linha-botoes"><button class="prim" type="submit">Gerar horários</button></div></form>
    <div class="card"><h2 style="margin-top:0">Agenda do período</h2><div class="campos">
      ${campo("vDe", "De", {tipo: "date", valor: de})}${campo("vAte", "Até", {tipo: "date", valor: ate})}</div><div id="agendaPosto"></div></div>`;
};
async function desenharAgendaPosto(){
  const hs = await api.listarHorariosPosto(estado.posto_id, valorDe("vDe"), valorDe("vAte"));
  const porDia = {}; hs.forEach(h=>(porDia[h.data] = porDia[h.data] || []).push(h));
  $("#agendaPosto").innerHTML = Object.keys(porDia).length ? Object.entries(porDia).map(([data, lista])=>{
    const todos = lista.every(h=>h.situacao === "bloqueado");
    return `<div style="margin:10px 0"><b>${dataCurtaBR(data)}</b> <button data-dia-bloq="${data}" data-acao="${todos ? 0 : 1}">${todos ? "Desbloquear o dia" : "Bloquear o dia"}</button>
      <div style="display:flex;flex-wrap:wrap;gap:4px;margin-top:4px">${lista.map(h=>`<button data-hor="${h.horario_id}" data-acao="${h.situacao === "bloqueado" ? 0 : 1}"
        class="selo ${h.situacao === "bloqueado" ? "erro" : "ok"}" title="${h.ocupadas}/${h.capacidade} ocupadas">${h.hora}</button>`).join("")}</div></div>`;
  }).join("") : `<p class="sub">Nenhum horário no período.</p>`;
  $$("[data-hor]").forEach(b=>b.addEventListener("click", async ()=>{ await api.bloquear(estado.posto_id, {horario_id: b.dataset.hor}, b.dataset.acao === "1"); desenharAgendaPosto(); }));
  $$("[data-dia-bloq]").forEach(b=>b.addEventListener("click", async ()=>{ await api.bloquear(estado.posto_id, {data: b.dataset.diaBloq}, b.dataset.acao === "1"); desenharAgendaPosto(); }));
}
TELAS_DEPOIS["#/posto/horarios"] = async ()=>{
  $("#formGrade").addEventListener("submit", async e=>{
    e.preventDefault();
    const g = {de: valorDe("gDe"), ate: valorDe("gAte"), inicio: valorDe("gInicio"), fim: valorDe("gFim"), intervalo: Number(valorDe("gIntervalo")),
               vagas: Number(valorDe("gVagas")), dias: $$("[data-dia]").filter(c=>c.checked).map(c=>Number(c.dataset.dia))};
    const erros = [];
    if (!g.de || !g.ate || g.ate < g.de) erros.push("O fim do período deve ser depois do início.");
    if (g.ate && g.de && (new Date(g.ate) - new Date(g.de)) / 86400000 > 62) erros.push("Gere no máximo 2 meses de cada vez.");
    if (!g.inicio || !g.fim || g.fim <= g.inicio) erros.push("O encerramento deve ser depois do primeiro horário.");
    if (!(g.intervalo >= 5)) erros.push("Intervalo mínimo de 5 minutos.");
    if (!(g.vagas >= 1)) erros.push("Ao menos 1 vaga por horário.");
    if (!g.dias.length) erros.push("Escolha ao menos um dia da semana.");
    if (!mostrarErros("#errosGrade", erros)) return;
    try { const r = await api.gerarHorarios(estado.posto_id, g); toast(`${r.criados} horários criados, ${r.existentes} já existiam.`); }
    catch(err){ return mostrarErros("#errosGrade", [err.message]); }
    $("#vDe").value = g.de; $("#vAte").value = g.ate; desenharAgendaPosto();
  });
  ["vDe", "vAte"].forEach(i=>$("#" + i).addEventListener("change", desenharAgendaPosto));
  await desenharAgendaPosto();
};

TELAS["#/gestao"] = async ()=>{
  const postos = await api.listarTodosPostos();
  return `<h1>Gestão</h1><p class="sub">Postos de identificação. Os indicadores chegam no Sprint 7.</p>
    <div class="card tabela-wrap"><table><tr><th>Código</th><th>Posto</th><th>Município</th><th>Situação</th><th></th></tr>
      ${postos.map(p=>{ const at = p.ativo === true || p.ativo === "TRUE"; return `<tr><td>${esc(p.posto_id)}</td><td>${esc(p.nome)}</td><td>${esc(p.municipio)}</td>
        <td><span class="selo ${at ? "ok" : "erro"}">${at ? "ativo" : "inativo"}</span></td>
        <td><button data-ativo="${esc(p.posto_id)}" data-valor="${at ? 0 : 1}">${at ? "Desativar" : "Ativar"}</button></td></tr>`; }).join("")}</table></div>
    <form class="card" id="formPosto"><h2 style="margin-top:0">Novo posto</h2><div class="campos">
      ${campo("pId", "Código", {obrigatorio: true, attrs: 'placeholder="P03"'})}${campo("pNome", "Nome", {obrigatorio: true})}
      ${campo("pMunicipio", "Município", {obrigatorio: true})}${campo("pEndereco", "Endereço")}${campo("pEmail", "E-mail do posto", {tipo: "email"})}</div>
      ${campo("pDocs", "Documentos que o cidadão deve levar", {tipo: "textarea", linhas: 2})}
      <div id="errosPosto"></div><div class="linha-botoes"><button class="prim" type="submit">Salvar posto</button></div></form>`;
};
TELAS_DEPOIS["#/gestao"] = ()=>{
  $$("[data-ativo]").forEach(b=>b.addEventListener("click", async ()=>{
    const p = (await api.listarTodosPostos()).find(x=>x.posto_id === b.dataset.ativo);
    await api.salvarPosto({...p, ativo: b.dataset.valor === "1"}); navegar();
  }));
  $("#formPosto").addEventListener("submit", async e=>{
    e.preventDefault();
    try {
      await api.salvarPosto({posto_id: valorDe("pId").toUpperCase(), nome: valorDe("pNome"), municipio: valorDe("pMunicipio"), endereco: valorDe("pEndereco"),
                             email: valorDe("pEmail"), documentos_orientacao: valorDe("pDocs"), ativo: true});
      toast("Posto salvo."); navegar();
    } catch(err){ mostrarErros("#errosPosto", [err.message]); }
  });
};
