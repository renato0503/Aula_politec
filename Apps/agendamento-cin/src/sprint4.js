/* ================= Sprint 4 · Trava de vagas, RN06 e e-mail de confirmação ================= */
/* O que depende do Apps Script (LockService e MailApp) fica enfileirado e com o
   passo a passo no botão escondido (3 cliques no nome do app, no rodapé). */

// RN06: um agendamento ativo por telefone e por CPF (4 últimos dígitos), no mesmo posto
function cinAtivoDuplicado(agendamentos, novo){
  const ativos = agendamentos.filter(a=>a.status === "confirmado" && a.posto_id === novo.posto_id);
  const tel = String(novo.telefone || "").replace(/\D/g, ""), cpf4 = String(novo.cpf || "").slice(-4);
  return ativos.some(a=>(tel && String(a.telefone || "").replace(/\D/g, "") === tel) || (cpf4 && a.cpf_final4 === cpf4));
}
teste("RN06: o segundo agendamento ativo do mesmo telefone no posto é recusado", ()=>{
  const ativos = [{posto_id: "P1", status: "confirmado", telefone: "(65) 99999-1111", cpf_final4: ""}];
  return cinAtivoDuplicado(ativos, {posto_id: "P1", telefone: "65999991111"})
    && !cinAtivoDuplicado(ativos, {posto_id: "P2", telefone: "65999991111"})
    && !cinAtivoDuplicado(ativos, {posto_id: "P1", telefone: "65999992222"});
});
teste("RN06: o CPF (4 dígitos) também bloqueia o segundo agendamento", ()=>{
  const ativos = [{posto_id: "P1", status: "confirmado", telefone: "", cpf_final4: "1234"}];
  return cinAtivoDuplicado(ativos, {posto_id: "P1", cpf: "00000001234"});
});

// fila do que depende do Google: e-mail e sincronização. O aluno liga depois.
async function cinEnfileirar(tipo, dados){
  await db.put("fila", {id: uuid(), tipo, dados, estado: "pendente", criado_em: agora()});
}
async function cinPendentes(){ return (await db.list("fila")).filter(f=>f.estado === "pendente"); }
async function cinMarcarEnviado(id){ const f = await db.get("fila", id); if (f) await db.put("fila", {...f, estado: "enviado", enviado_em: agora()}); }

if (!NO_APPS_SCRIPT) Object.assign(api, {
  async reservar(d){
    // releitura da capacidade imediatamente antes de gravar (a trava de verdade é o LockService no Code.gs)
    const h = await db.get("horarios", d.horario_id);
    if (!h || h.situacao !== "aberto" || !dentroDaJanela(h.data)) throw new Error("Este horário não está disponível.");
    if (Number(h.ocupadas) >= Number(h.capacidade)) throw new Error("Este horário acabou de ser preenchido. Escolha outro.");
    const todos = await db.list("agendamentos");
    if (cinAtivoDuplicado(todos, {...d, posto_id: h.posto_id})) throw new Error("Já existe um agendamento ativo para este telefone ou CPF neste posto (RN06).");
    let protocolo; do { protocolo = novoProtocoloCin(); } while (await db.get("agendamentos", protocolo));
    await db.put("horarios", {...h, ocupadas: Number(h.ocupadas) + 1});
    const ag = {protocolo, posto_id: h.posto_id, horario_id: h.horario_id, nome: d.nome, telefone: d.telefone || "", email: d.email || "",
      cpf_final4: d.cpf ? d.cpf.slice(-4) : "", status: "confirmado", criado_em: agora(), cancelado_em: "", compareceu_em: ""};
    await db.put("agendamentos", ag);
    await cinEnfileirar("email_confirmacao", {protocolo, email: ag.email, nome: ag.nome, data: h.data, hora: h.hora, posto_id: h.posto_id});
    await registrar("agendamento criado", {detalhe: protocolo});
    return {protocolo};
  }
});

/* ================= Sprint 5 · Consulta e cancelamento (RN07) ================= */
function cinHorasAte(dataISO, hora, agoraMs = Date.now()){
  if (!dataISO || !hora) return null;
  return (new Date(`${dataISO}T${hora}:00`) - agoraMs) / 3600000;
}
teste("RN07: cancelar a 3 h pode, a 1 h não", ()=>{
  const base = new Date("2026-11-10T08:00:00").getTime();
  return cinHorasAte("2026-11-10", "11:00", base) === 3 && cinHorasAte("2026-11-10", "09:00", base) === 1;
});

async function cinCancelar(protocolo, motivo, quem){
  const a = await db.get("agendamentos", protocolo);
  if (!a) throw new Error("Reserva não encontrada.");
  if (a.status !== "confirmado") throw new Error(`Esta reserva está ${a.status}.`);
  const h = await db.get("horarios", a.horario_id);
  const horas = cinHorasAte(h?.data, h?.hora);
  if (quem !== "posto" && horas !== null && horas < 2) throw new Error("O cancelamento pelo cidadão só é possível até 2 horas antes (RN07).");
  await db.put("agendamentos", {...a, status: "cancelado", cancelado_em: agora(), motivo_cancelamento: motivo || ""});
  if (h) await db.put("horarios", {...h, ocupadas: Math.max(0, Number(h.ocupadas) - 1)});
  await cinEnfileirar("email_cancelamento", {protocolo, email: a.email, motivo: motivo || ""});
  await registrar("agendamento cancelado", {detalhe: `${protocolo}${motivo ? " · " + motivo : ""}`});
  return true;
}

TELAS["#/consultar"] = async ()=>{
  const q = estado.cinConsulta || null;
  let achado = "", resultados = [];
  if (q){
    const a = await db.get("agendamentos", q.protocolo);
    if (!a) achado = `<div class="card pendente" id="cinNaoAchado">Reserva <b class="mono">${esc(q.protocolo)}</b> não encontrada.</div>`;
    else {
      const tel = String(q.contato || "").replace(/\D/g, ""), okTel = tel.length >= 8 && String(a.telefone || "").replace(/\D/g, "").endsWith(tel.slice(-8));
      const okCpf = String(q.contato || "").replace(/\D/g, "").length === 4 && a.cpf_final4 === String(q.contato).replace(/\D/g, "");
      if (!okTel && !okCpf) achado = `<div class="card pendente" id="cinNaoConfere">Os dados não conferem com a reserva. Use o telefone completo ou os 4 últimos dígitos do CPF.</div>`;
      else resultados = [a];
    }
  }
  return `<h1>Consultar ou cancelar</h1><p class="sub">Informe o protocolo e o telefone (ou os 4 últimos dígitos do CPF).</p>
    <form class="card" id="formConsulta"><div class="campos">
      ${campo("qProtocolo", "Protocolo", {valor: q?.protocolo || "", obrigatorio: true})}
      ${campo("qContato", "Telefone ou 4 últimos dígitos do CPF", {valor: q?.contato || "", obrigatorio: true})}</div>
      <div id="cinErrosConsulta"></div><div class="linha-botoes"><button class="prim" type="submit">Consultar</button></div></form>
    ${achado}
    ${resultados.map(a=>{
      const h = a.horario; return "";
    }).join("")}
    <div id="cinResultado">${await Promise.all(resultados.map(async a=>{
      const h = await db.get("horarios", a.horario_id), p = await db.get("postos", a.posto_id);
      const horas = cinHorasAte(h?.data, h?.hora), podeCancelar = a.status === "confirmado" && (horas === null || horas >= 2);
      return `<div class="card" id="cinReserva"><h2 style="margin-top:0">Reserva ${esc(a.protocolo)}
        <span class="selo ${a.status === "confirmado" ? "ok" : a.status === "compareceu" ? "info" : "erro"}">${esc(a.status)}</span></h2>
        <p><b>${esc(a.nome.split(" ")[0])}</b> · ${esc(p?.nome || "")}<br>${dataCurtaBR(h?.data)} às ${esc(h?.hora || "")}</p>
        ${a.status === "confirmado" ? `<p class="sub">Faltam ${Math.max(0, Math.round(horas))} h para o atendimento. O cancelamento é possível até 2 h antes (RN07).</p>
          <div class="linha-botoes"><input id="cinMotivo" placeholder="Motivo (opcional)" style="max-width:260px">
          <button class="perigo" id="btnCinCancelar" ${podeCancelar ? "" : "disabled"}>Cancelar a reserva</button></div>` : ""}
        <div id="cinErrosCancelar"></div></div>`;
    })).then(x=>x.join(""))}</div>`;
};
TELAS_DEPOIS["#/consultar"] = ()=>{
  $("#formConsulta")?.addEventListener("submit", async e=>{
    e.preventDefault();
    const protocolo = valorDe("qProtocolo").toUpperCase(), contato = valorDe("qContato");
    const erros = [!protocolo && "Informe o protocolo.", !contato && "Informe o telefone ou os 4 últimos dígitos do CPF."].filter(Boolean);
    if (!mostrarErros("#cinErrosConsulta", erros)) return;
    estado.cinConsulta = {protocolo, contato}; navegar();
  });
  $("#btnCinCancelar")?.addEventListener("click", async ()=>{
    try { await cinCancelar(estado.cinConsulta.protocolo, valorDe("cinMotivo"), "cidadao"); toast("Reserva cancelada. A vaga voltou para o calendário."); navegar(); }
    catch(err){ mostrarErros("#cinErrosCancelar", [err.message]); }
  });
};

/* ================= Sprint 6 · Painel do posto ================= */
function cinSemana(dataISO){
  const d = new Date(dataISO + "T12:00:00"), dia = (d.getDay() + 6) % 7;
  const ini = new Date(d); ini.setDate(d.getDate() - dia);
  const fim = new Date(ini); fim.setDate(ini.getDate() + 6);
  return {ini: ini.toISOString().slice(0, 10), fim: fim.toISOString().slice(0, 10)};
}
TELAS["#/posto"] = async ()=>{
  const postos = await api.listarPostos(), posto = estado.cinPosto || postos[0]?.posto_id;
  if (!posto) return `<div class="card vazio">Nenhum posto cadastrado. Carregue os dados fictícios.</div>`;
  const todos = (await db.list("agendamentos")).filter(a=>a.posto_id === posto);
  const horarios = Object.fromEntries((await db.list("horarios")).map(h=>[h.horario_id, h]));
  const busca = normalizar(estado.cinBusca || "");
  const semana = cinSemana(hojeISO());
  const doDia = todos.filter(a=>horarios[a.horario_id]?.data === hojeISO());
  const daSemana = todos.filter(a=>{ const d = horarios[a.horario_id]?.data; return d >= semana.ini && d <= semana.fim; });
  const lista = todos.filter(a=>!busca || normalizar(`${a.protocolo} ${a.nome}`).includes(busca))
    .filter(a=>{ const d = horarios[a.horario_id]?.data; return d && d >= semana.ini && d <= semana.fim; })
    .sort((a, b)=>(horarios[a.horario_id].data + horarios[a.horario_id].hora).localeCompare(horarios[b.horario_id].data + horarios[b.horario_id].hora));
  const pendentes = await cinPendentes();
  // guarda a agenda do dia no IndexedDB (funciona sem internet)
  for (const a of doDia) await db.put("fila", {id: "agenda:" + a.protocolo, tipo: "agenda_local", dados: {protocolo: a.protocolo, horario_id: a.horario_id, nome: a.nome}, estado: "local", criado_em: agora()});
  return `<h1>Agenda do posto</h1>
    <div class="card"><div class="campos">${campo("cinPostoSel", "Posto", {tipo: "select", opcoes: postos.map(p=>[p.posto_id, p.nome]), valor: posto})}
      ${campo("cinBuscaPosto", "Buscar por nome ou protocolo", {valor: estado.cinBusca || ""})}</div></div>
    <div class="grade"><div class="card kpi"><div class="v" data-cin-posto="hoje">${doDia.length}</div><div class="r">agendamentos hoje</div></div>
      <div class="card kpi"><div class="v" data-cin-posto="semana">${daSemana.length}</div><div class="r">na semana</div></div>
      <div class="card kpi"><div class="v" data-cin-posto="pendentes">${pendentes.length}</div><div class="r">pendentes de envio</div></div></div>
    ${pendentes.length ? `<div class="card pendente" id="cinFilaLocal"><b>${pendentes.length} item(ns) pendente(s) de envio.</b>
      <p class="sub">Sem internet, o posto trabalha na fila local e envia quando a conexão volta.</p>
      <div class="linha-botoes"><button id="btnCinEnviar">Marcar como enviados (simulação)</button></div></div>` : ""}
    <div class="card tabela-wrap"><table id="tabelaPosto"><tr><th>Protocolo</th><th>Data</th><th>Hora</th><th>Nome</th><th>Situação</th><th></th></tr>
      ${lista.map(a=>{ const h = horarios[a.horario_id]; return `<tr><td class="mono">${esc(a.protocolo)}</td><td>${dataCurtaBR(h.data)}</td><td>${esc(h.hora)}</td>
        <td>${esc(a.nome)}</td><td><span class="selo ${a.status === "compareceu" ? "ok" : a.status === "ausente" ? "erro" : a.status === "cancelado" ? "info" : "alerta"}">${esc(a.status)}</span></td>
        <td>${a.status === "confirmado" ? `<button data-compareceu="${esc(a.protocolo)}">Compareceu</button><button data-ausente="${esc(a.protocolo)}">Ausente</button><button data-cancelar-posto="${esc(a.protocolo)}">Cancelar</button>` : ""}</td></tr>`; }).join("")
        || '<tr><td colspan="6" class="vazio">Nenhum agendamento nesta semana.</td></tr>'}</table></div>
    <div id="cinErrosPosto"></div>`;
};
TELAS_DEPOIS["#/posto"] = ()=>{
  $("#cinPostoSel")?.addEventListener("change", e=>{ estado.cinPosto = e.target.value; navegar(); });
  $("#cinBuscaPosto")?.addEventListener("change", e=>{ estado.cinBusca = e.target.value; navegar(); });
  $("#btnCinEnviar")?.addEventListener("click", async ()=>{
    for (const f of await cinPendentes()) await cinMarcarEnviado(f.id);
    await registrar("fila local enviada", {detalhe: "simulação, sem Apps Script"}); toast("Fila local marcada como enviada."); navegar();
  });
  const marcar = (status)=>(protocolo)=>async ()=>{
    const a = await db.get("agendamentos", protocolo);
    if (!a) return;
    await db.put("agendamentos", {...a, status, compareceu_em: status === "compareceu" ? agora() : a.compareceu_em});
    await registrar("posto: " + status, {detalhe: protocolo});
    await cinEnfileirar("sincronizar_status", {protocolo, status});
    toast(status === "compareceu" ? "Comparecimento registrado." : "Ausência registrada."); navegar();
  };
  $$("[data-compareceu]").forEach(b=>b.addEventListener("click", marcar("compareceu")(b.dataset.compareceu)));
  $$("[data-ausente]").forEach(b=>b.addEventListener("click", marcar("ausente")(b.dataset.ausente)));
  $$("[data-cancelar-posto]").forEach(b=>b.addEventListener("click", async ()=>{
    const motivo = prompt("Motivo do cancelamento pelo posto:");
    if (motivo === null) return;
    try { await cinCancelar(b.dataset.cancelarPosto, motivo, "posto"); toast("Reserva cancelada pelo posto."); navegar(); }
    catch(err){ mostrarErros("#cinErrosPosto", [err.message]); }
  }));
};

/* ================= Sprint 7 · Gestão, retenção e usuários ================= */
const CIN_RETENCAO_DIAS = 90;
// a gestão do Sprint 2 (postos) continua embaixo dos indicadores
const cinGestaoAntiga = TELAS["#/gestao"], cinGestaoAntigaDepois = TELAS_DEPOIS["#/gestao"];
async function cinGestaoNova(){
  const [ags, horarios, postos] = await Promise.all([db.list("agendamentos"), db.list("horarios"), db.list("postos")]);
  const hmap = Object.fromEntries(horarios.map(h=>[h.horario_id, h]));
  const linhas = postos.map(p=>{
    const lista = ags.filter(a=>a.posto_id === p.posto_id);
    const confirmados = lista.filter(a=>a.status === "confirmado").length, compareceu = lista.filter(a=>a.status === "compareceu").length;
    const cancelados = lista.filter(a=>a.status === "cancelado").length, ausentes = lista.filter(a=>a.status === "ausente").length;
    const base = compareceu + ausentes || 1;
    return {p, lista: lista.length, confirmados, compareceu, cancelados, ausentes, taxaComparecimento: Math.round(compareceu / base * 100)};
  });
  const vagas = horarios.reduce((a, h)=>a + Number(h.capacidade || 0), 0);
  const ocupadas = horarios.reduce((a, h)=>a + Number(h.ocupadas || 0), 0);
  const ocupacao = vagas ? Math.round(ocupadas / vagas * 100) : 0;
  return `<h1>Gestão</h1><p class="sub">Ocupação, comparecimento, cancelamento e antecedência por posto.</p>
    <div class="grade">
      <div class="card kpi"><div class="v" data-cin-gest="ocupacao">${ocupacao}%</div><div class="r">ocupação das vagas</div></div>
      <div class="card kpi"><div class="v" data-cin-gest="reservas">${ags.length}</div><div class="r">reservas no recorte</div></div>
      <div class="card kpi"><div class="v" data-cin-gest="retidos">${(await db.get("contagens", "cin_retidos"))?.valor || 0}</div><div class="r">registros apagados pela retenção</div></div></div>
    <div class="card tabela-wrap"><h2 style="margin-top:0">Por posto</h2><table id="tabelaGestao"><tr><th>Posto</th><th class="num">Reservas</th><th class="num">Compareceu</th><th class="num">Ausente</th><th class="num">Cancelou</th><th class="num">Comparecimento</th></tr>
      ${linhas.map(l=>`<tr><td>${esc(l.p.nome)}</td><td class="num">${l.lista}</td><td class="num">${l.compareceu}</td><td class="num">${l.ausentes}</td>
        <td class="num">${l.cancelados}</td><td class="num">${l.taxaComparecimento}%</td></tr>`).join("")}</table></div>
    <div class="card"><h2 style="margin-top:0">Usuários do app</h2>
      <ul class="check-lista">${(await db.list("usuarios")).map(u=>`<li class="${u.ativo === false ? "falta" : "feito"}">${icone(u.ativo === false ? "alerta" : "check")}
        <span><b>${esc(u.nome || u.email || u.id)}</b> · ${esc(u.perfil || "posto")}${u.ativo === false ? " · desativado" : ""}</span>
        ${u.ativo === false ? "" : `<button data-desativar="${esc(u.id)}">Desativar</button>`}</li>`).join("") || '<li class="vazio">Nenhum usuário.</li>'}</ul></div>
    <div class="card"><h2 style="margin-top:0">Retenção (RN10)</h2>
      <p class="sub">Apaga os dados do cidadão ${CIN_RETENCAO_DIAS} dias depois do atendimento, mantendo as contagens. No Apps Script, isso roda por gatilho diário.</p>
      <div class="linha-botoes"><button id="btnCinRetencao">Apagar os registros com mais de ${CIN_RETENCAO_DIAS} dias</button></div>
      <div id="cinResRetencao"></div></div>`;
};
const cinGestaoLigar = ()=>{
  $$("[data-desativar]").forEach(b=>b.addEventListener("click", async ()=>{
    const u = await db.get("usuarios", b.dataset.desativar);
    await db.put("usuarios", {...u, ativo: false}); await registrar("usuário desativado", {detalhe: u.id}); toast("Usuário desativado."); navegar();
  }));
  $("#btnCinRetencao")?.addEventListener("click", async ()=>{
    const limite = new Date(Date.now() - CIN_RETENCAO_DIAS * 86400000).toISOString().slice(0, 10);
    let n = 0;
    for (const a of await db.list("agendamentos")){
      const h = await db.get("horarios", a.horario_id);
      if (h && h.data && h.data < limite && ["compareceu", "ausente", "cancelado"].includes(a.status)){
        await db.del("agendamentos", a.protocolo); n++;
      }
    }
    const atual = (await db.get("contagens", "cin_retidos"))?.valor || 0;
    await db.put("contagens", {chave: "cin_retidos", valor: atual + n});
    await registrar("retenção executada", {detalhe: `${n} registros apagados`});
    $("#cinResRetencao").innerHTML = `<p class="ok-txt">${n} registro(s) apagado(s). As contagens ficaram.</p>`;
    toast(`${n} registro(s) apagados.`);
  });
};
TELAS["#/gestao"] = async (p)=>{ const antiga = await cinGestaoAntiga(p); return (await cinGestaoNova()) + antiga; };
TELAS_DEPOIS["#/gestao"] = async (p)=>{ cinGestaoLigar(); await cinGestaoAntigaDepois(p); };

/* ================= Passo a passo do que depende do Google ================= */
const AJUDA_TECNICA = [
  {titulo: "1. Trava de vaga (LockService) — RN04", resumo: "Sem a trava, duas abas podem reservar a última vaga ao mesmo tempo. O app local já relê a capacidade antes de gravar; a trava de verdade fica no servidor.",
   passos: [
     "Abra o projeto no Apps Script (script.google.com) com a conta institucional.",
     "No arquivo <code>Code.gs</code>, na função <code>reservar</code>, envolva o trecho de leitura e gravação em <code>const trava = LockService.getScriptLock();</code>.",
     "Peça a trava com espera: <code>trava.waitLock(10000)</code>. Se der erro, devolva a mensagem de vaga ocupada.",
     "Depois de gravar o agendamento e atualizar o horário, chame <code>trava.releaseLock()</code> no <code>finally</code>.",
     "Teste com 5 abas na última vaga: só uma reserva pode ser gravada.",
   ], arquivos: ["Code.gs"]},
  {titulo: "2. E-mail de confirmação e de cancelamento (MailApp) — RN03", resumo: "O app já enfileira os e-mails na aba fila, com estado pendente. Falta o envio.",
   passos: [
     "No <code>Code.gs</code>, crie a função <code>enviarPendentes()</code> que lê a aba <code>fila</code> com estado <code>pendente</code>.",
     "Para cada item do tipo <code>email_confirmacao</code>, monte o assunto com o protocolo e chame <code>MailApp.sendEmail(email, assunto, corpo)</code>.",
     "Para <code>email_cancelamento</code>, envie o motivo e o link de novo agendamento.",
     "Depois do envio, marque o item como <code>enviado</code> e grave a data.",
     "Confira a cota diária de e-mail da conta institucional com a TI antes do piloto.",
   ], arquivos: ["Code.gs"]},
  {titulo: "3. Gatilho diário da retenção (RN10)", resumo: "O botão em #/gestao apaga na hora. Em produção, isso roda sozinho todo dia.",
   passos: [
     "No Apps Script, menu <b>Acionadores</b> > <b>Adicionar acionador</b>.",
     "Escolha a função <code>retencao</code>, evento <b>Baseado em tempo</b>, <b>Diariamente</b>, entre 2 h e 3 h da manhã.",
     "A função apaga os agendamentos com mais de 90 dias do atendimento, nas situações compareceu, ausente e cancelado, e soma em <code>contagens</code>.",
     "Teste rodando a função manualmente uma vez e confira a aba <code>log</code>.",
   ], arquivos: ["Code.gs"]},
  {titulo: "4. Publicar o app (clasp + implantação)", resumo: "O index.html local é a versão de teste. O app do cidadão é servido pelo Apps Script.",
   passos: [
     "Instale o clasp: <code>npm i -g @google/clasp</code> e faça <code>clasp login</code>.",
     "Crie o projeto: <code>clasp create --type webapp --title \"Agendamento CIN\"</code>.",
     "Copie <code>Code.gs</code>, <code>appsscript.json</code> e o HTML para a pasta do projeto e rode <code>clasp push</code>.",
     "No editor, <b>Implantar</b> > <b>Nova implantação</b> > tipo <b>App da Web</b>; execute como <b>você</b> e acesso <b>qualquer pessoa</b> (ou só o domínio).",
     "Copie a URL da implantação e coloque no lugar do link do app.",
   ], arquivos: ["Code.gs", "appsscript.json", "DEPLOY.md"]},
  {titulo: "5. Conferir no piloto", resumo: "Só depois dos quatro passos acima o app está pronto para dado real.",
   passos: [
     "Peça à TI a autorização da conta institucional e a confirmação das cotas.",
     "Rode o roteiro de aceite do Sprint 8 com um posto e com a gestão.",
     "Confira as metas: 70% de ocupação e 85% de comparecimento.",
     "Registre no <code>PREMISSAS.md</code> o que foi confirmado.",
   ], arquivos: ["modelos/roteiro-aceite.md"]},
];
