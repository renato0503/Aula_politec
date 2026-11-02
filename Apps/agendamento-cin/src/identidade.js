/* Identidade do Agendamento CIN.
   Entra por último no build. Redefine as telas do cidadão para o calendário do
   mês com as vagas por dia, os passos 1-2-3 e os horários em botões grandes,
   a grade semanal de ocupação do posto e a busca por protocolo, nome ou CPF. */

function cinPassos(atual){
  const itens = ["Posto e data", "Seus dados", "Comprovante"];
  return `<ol class="cin-passos" aria-label="Passos do agendamento">${itens.map((t, i)=>{
    const n = i + 1, cls = n < atual ? "feito" : n === atual ? "atual" : "";
    return `<li class="${cls}" ${n === atual ? 'aria-current="step"' : ""}><span class="n">${n < atual ? "✓" : n}</span><span class="t">${t}</span></li>`;
  }).join("")}</ol>`;
}

function cinMesNome(chave){
  const nomes = ["janeiro", "fevereiro", "março", "abril", "maio", "junho", "julho", "agosto", "setembro", "outubro", "novembro", "dezembro"];
  const [a, m] = chave.split("-").map(Number);
  return `${nomes[m - 1]} de ${a}`;
}

function cinCalendario(dias, escolhido){
  const hoje = hojeISO();
  const meses = [...new Set(Object.keys(dias).sort().map(d=>d.slice(0, 7)))];
  if (!meses.length) return `<p class="sub">Sem vagas nos próximos 30 dias neste posto.</p>`;
  return meses.map(chave=>{
    const [a, m] = chave.split("-").map(Number);
    const primeiro = new Date(Date.UTC(a, m - 1, 1));
    const vazios = (primeiro.getUTCDay() + 6) % 7;
    const total = new Date(Date.UTC(a, m, 0)).getUTCDate();
    const celulas = [];
    for (let i = 0; i < vazios; i++) celulas.push('<span class="cin-dia fora" aria-hidden="true"></span>');
    for (let d = 1; d <= total; d++){
      const iso = `${a}-${String(m).padStart(2, "0")}-${String(d).padStart(2, "0")}`;
      const n = (dias[iso] || []).length;
      if (n && dentroDaJanela(iso, hoje)){
        celulas.push(`<button type="button" class="cin-dia ${n <= 2 ? "ultima" : "livre"} ${iso === escolhido ? "escolhido" : ""}" data-dia="${iso}"
          aria-label="${d} de ${cinMesNome(chave)}, ${plural(n, "vaga", "vagas")}"><b>${d}</b><small>${n} ${n === 1 ? "vaga" : "vagas"}</small></button>`);
      } else {
        celulas.push(`<span class="cin-dia ${iso < hoje ? "fora" : "vazio"}"><b>${d}</b><small>${iso < hoje ? "passou" : "sem vaga"}</small></span>`);
      }
    }
    return `<div class="cin-mes"><h3>${cinMesNome(chave)}</h3>
      <div class="cin-cabecalho"><span>seg</span><span>ter</span><span>qua</span><span>qui</span><span>sex</span><span>sáb</span><span>dom</span></div>
      <div class="cin-grade">${celulas.join("")}</div></div>`;
  }).join("");
}

TELAS["#/agendar"] = async ()=>{
  const postos = await api.listarPostos(), escolhido = estado.agPosto && postos.find(p=>p.posto_id === estado.agPosto);
  let dias = {}, dia = null, horas = [];
  if (escolhido){
    const vagas = await api.listarVagas(escolhido.posto_id);
    vagas.forEach(h=>(dias[h.data] = dias[h.data] || []).push(h));
    dia = estado.agDia && dias[estado.agDia] ? estado.agDia : null;
    horas = dia ? dias[dia] : [];
  }
  const totalVagas = Object.values(dias).reduce((a, hs)=>a + hs.length, 0);
  return `<h1>Agendar a Carteira de Identidade</h1>
    <p class="sub">Escolha o posto, o dia no calendário e o horário. O agendamento abre de 1 a 30 dias à frente.</p>
    ${cinPassos(1)}
    ${NO_APPS_SCRIPT ? "" : `<p class="selo alerta">Modo de teste local, com dados fictícios</p>`}
    <div class="card"><h2 style="margin-top:0">1. Posto de atendimento</h2>
      <div class="cin-postos">${postos.map(p=>`<button type="button" class="cin-posto ${p.posto_id === estado.agPosto ? "escolhido" : ""}" data-posto="${esc(p.posto_id)}">
        <b>${esc(p.nome)}</b><small>${esc(p.municipio)} · ${esc(p.endereco)}</small></button>`).join("")}</div></div>
    ${escolhido ? `<div class="card"><h2 style="margin-top:0">2. Dia${totalVagas ? ` <span class="conta">${plural(totalVagas, "horário livre", "horários livres")}</span>` : ""}</h2>
      ${cinCalendario(dias, dia)}
      ${dia ? `<div class="cin-dia-escolhido"><b>${dataCurtaBR(dia)}</b> · ${plural(horas.length, "horário livre", "horários livres")}
        <button type="button" class="cin-trocar" data-dia-limpar="1">Trocar o dia</button></div>` : ""}</div>` : ""}
    ${dia ? `<div class="card"><h2 style="margin-top:0">3. Horário em ${dataCurtaBR(dia)}</h2>
      <div class="cin-horas">${horas.map(h=>`<button type="button" class="cin-hora" data-horario="${esc(h.horario_id)}" data-hora="${esc(h.hora)}">
        <b>${esc(h.hora)}</b><small>${plural(Math.max(0, Number(h.capacidade) - Number(h.ocupadas)), "vaga", "vagas")}</small></button>`).join("")}</div></div>` : ""}
    <p class="sub"><a href="#/consultar">Consultar ou cancelar uma reserva</a>${NO_APPS_SCRIPT ? "" : ` · <a href="#/posto">Área do servidor</a>`}</p>`;
};
TELAS_DEPOIS["#/agendar"] = ()=>{
  $$("[data-posto]").forEach(b=>b.addEventListener("click", ()=>{ estado.agPosto = b.dataset.posto; estado.agDia = null; navegar(); }));
  $$("[data-dia]").forEach(b=>b.addEventListener("click", ()=>{ estado.agDia = b.dataset.dia; navegar(); }));
  $("[data-dia-limpar]")?.addEventListener("click", ()=>{ estado.agDia = null; navegar(); });
  $$("[data-horario]").forEach(b=>b.addEventListener("click", ()=>{
    estado.agReserva = {posto_id: estado.agPosto, horario_id: b.dataset.horario, data: estado.agDia, hora: b.dataset.hora};
    location.hash = "#/agendar/dados";
  }));
};

TELAS["#/agendar/dados"] = async ()=>{
  const r = estado.agReserva;
  if (!r) return `<div class="card vazio">Escolha primeiro o posto, o dia e o horário. <a href="#/agendar">Agendar</a></div>`;
  const p = (await api.listarPostos()).find(x=>x.posto_id === r.posto_id);
  return `<h1>Seus dados</h1>${cinPassos(2)}
    <p class="sub">${esc(p?.nome || "")} · <b>${dataCurtaBR(r.data)} às ${esc(r.hora)}</b> · <a href="#/agendar">trocar</a></p>
    <form class="card" id="formAgDados" novalidate><div class="campos">
      ${campo("aNome", "Nome completo", {obrigatorio: true, attrs: 'autocomplete="name"'})}
      ${campo("aTel", "Telefone com DDD", {tipo: "tel", attrs: 'autocomplete="tel"', ajuda: "Informe telefone ou e-mail."})}
      ${campo("aEmail", "E-mail", {tipo: "email", attrs: 'autocomplete="email"', ajuda: "Recebe a confirmação."})}
      ${campo("aCpf", "CPF (opcional)", {attrs: 'inputmode="numeric" autocomplete="off"', ajuda: "Guardamos só os 4 últimos dígitos, para consultar a reserva."})}</div>
    <label class="cin-aviso"><input type="checkbox" id="aAviso">
      <span>Li o aviso: os dados servem só para organizar o atendimento da CIN e são apagados 90 dias depois do atendimento.</span></label>
    <div id="errosAg"></div><div class="linha-botoes"><button class="prim" type="submit">Confirmar agendamento</button></div></form>`;
};
TELAS_DEPOIS["#/agendar/dados"] = ()=>{
  $("#formAgDados")?.addEventListener("submit", async e=>{
    e.preventDefault();
    const d = {nome: valorDe("aNome"), telefone: valorDe("aTel"), email: valorDe("aEmail"), cpf: valorDe("aCpf").replace(/\D/g, ""), horario_id: estado.agReserva.horario_id};
    const erros = [];
    if (d.nome.split(/\s+/).length < 2) erros.push("Informe o nome completo.");
    if (!d.telefone && !d.email) erros.push("Informe um telefone ou um e-mail.");
    if (d.telefone && d.telefone.replace(/\D/g, "").length < 10) erros.push("Telefone com DDD (10 ou 11 dígitos).");
    if (d.email && !/^\S+@\S+\.\S+$/.test(d.email)) erros.push("E-mail inválido.");
    if (d.cpf && !cpfValido(d.cpf)) erros.push("CPF inválido. Corrija ou deixe em branco.");
    if (!$("#aAviso").checked) erros.push("Confirme que leu o aviso de privacidade.");
    if (!mostrarErros("#errosAg", erros)) return;
    try { const r = await api.reservar(d); estado.agReserva = null; location.hash = "#/comprovante/" + encodeURIComponent(r.protocolo); }
    catch(err){ mostrarErros("#errosAg", [err.message]); }
  });
};

TELAS["#/comprovante/:protocolo"] = async ({protocolo})=>{
  const c = await api.comprovante(protocolo);
  if (!c) return `<div class="card vazio">Protocolo não encontrado.</div>`;
  return `<h1>Agendamento confirmado</h1>${cinPassos(3)}
    <div class="card cin-comprovante" id="cardComprovanteCin">
    <p>Protocolo: <b class="mono" id="protCin">${esc(c.protocolo)}</b></p>
    <p><b>${esc(c.primeiro_nome)}</b>, seu atendimento é em <b>${dataCurtaBR(c.data)} às ${esc(c.hora)}</b>.</p>
    <p><b>Posto:</b> ${esc(c.posto)}<br>${esc(c.endereco || "")}</p>
    <h2>Documentos para levar</h2><p>${esc(c.documentos || "Consulte o posto.")}</p>
    <p class="sub">Chegue 10 minutos antes. Depois de 15 minutos de atraso, o horário é liberado.</p>
    <div class="linha-botoes nao-imprimir"><button onclick="window.print()">Imprimir</button><a class="botao" href="#/consultar">Consultar ou cancelar</a><a class="botao" href="#/agendar">Novo agendamento</a></div></div>`;
};

/* ---------- grade semanal de ocupação (Horários do posto) ---------- */
async function desenharAgendaPosto(){
  const de = valorDe("vDe"), ate = valorDe("vAte");
  const hs = await api.listarHorariosPosto(estado.posto_id, de, ate);
  const alvo = $("#agendaPosto");
  if (!alvo) return;
  if (!hs.length){ alvo.innerHTML = '<p class="sub">Nenhum horário no período. Gere a grade acima.</p>'; return; }
  const datas = [...new Set(hs.map(h=>h.data))].sort();
  const horas = [...new Set(hs.map(h=>h.hora))].sort();
  const mapa = Object.fromEntries(hs.map(h=>[h.data + "|" + h.hora, h]));
  const legenda = `<div class="cin-legenda"><span class="livre">livre</span><span class="parcial">parcial</span>
    <span class="lotado">lotado</span><span class="bloqueado">bloqueado</span>
    <span class="sub">Clique no horário para bloquear ou liberar; clique na data para o dia inteiro.</span></div>`;
  const cabecalho = datas.map(d=>{
    const todos = datas.length && horas.every(h=>mapa[d + "|" + h]?.situacao === "bloqueado");
    return `<th><button type="button" class="cin-dia-cab" data-dia-bloq="${d}" data-acao="${todos ? 0 : 1}"
      title="${todos ? "Desbloquear" : "Bloquear"} o dia ${dataCurtaBR(d)}">${dataCurtaBR(d)}</button></th>`;
  }).join("");
  const linhas = horas.map(h=>`<tr><th scope="row">${esc(h)}</th>${datas.map(d=>{
    const x = mapa[d + "|" + h];
    if (!x) return '<td class="cin-vazio">—</td>';
    const ocup = Number(x.ocupadas) || 0, cap = Number(x.capacidade) || 1, resta = Math.max(0, cap - ocup);
    const estadoCls = x.situacao === "bloqueado" ? "bloqueado" : resta === 0 ? "lotado" : ocup > 0 ? "parcial" : "livre";
    const texto = estadoCls === "bloqueado" ? "bloqueado" : estadoCls === "lotado" ? "cheio" : plural(resta, "vaga", "vagas");
    return `<td><button type="button" class="cin-slot ${estadoCls}" data-hor="${esc(x.horario_id)}" data-acao="${x.situacao === "bloqueado" ? 0 : 1}"
      title="${ocup}/${cap} ocupadas · ${estadoCls}">${texto}</button></td>`;
  }).join("")}</tr>`).join("");
  alvo.innerHTML = `${legenda}<div class="tabela-wrap"><table class="cin-grade-posto"><thead><tr><th>Hora</th>${cabecalho}</tr></thead><tbody>${linhas}</tbody></table></div>`;
  $$("[data-hor]").forEach(b=>b.addEventListener("click", async ()=>{ await api.bloquear(estado.posto_id, {horario_id: b.dataset.hor}, b.dataset.acao === "1"); desenharAgendaPosto(); }));
  $$("[data-dia-bloq]").forEach(b=>b.addEventListener("click", async ()=>{ await api.bloquear(estado.posto_id, {data: b.dataset.diaBloq}, b.dataset.acao === "1"); desenharAgendaPosto(); }));
}

/* ---------- agenda do posto com busca por protocolo, nome ou CPF ---------- */
TELAS["#/posto"] = async ()=>{
  const postos = await api.listarPostos();
  const posto = (estado.cinPosto && postos.some(p=>p.posto_id === estado.cinPosto)) ? estado.cinPosto
    : (postos.find(p=>p.posto_id === estado.posto_id)?.posto_id || postos[0]?.posto_id);
  if (!posto) return `<div class="card vazio">Nenhum posto cadastrado. Carregue os dados fictícios.</div>`;
  const todos = (await db.list("agendamentos")).filter(a=>a.posto_id === posto);
  const horarios = Object.fromEntries((await db.list("horarios")).map(h=>[h.horario_id, h]));
  const busca = normalizar(estado.cinBusca || "");
  const semana = cinSemana(hojeISO());
  const doDia = todos.filter(a=>horarios[a.horario_id]?.data === hojeISO());
  const daSemana = todos.filter(a=>{ const d = horarios[a.horario_id]?.data; return d >= semana.ini && d <= semana.fim; });
  const lista = todos.filter(a=>!busca || normalizar(`${a.protocolo} ${a.nome} ${a.cpf_final4 || ""}`).includes(busca))
    .filter(a=>{ const d = horarios[a.horario_id]?.data; return d && d >= semana.ini && d <= semana.fim; })
    .sort((a, b)=>(horarios[a.horario_id].data + horarios[a.horario_id].hora).localeCompare(horarios[b.horario_id].data + horarios[b.horario_id].hora));
  const pendentes = await cinPendentes();
  for (const a of doDia) await db.put("fila", {id: "agenda:" + a.protocolo, tipo: "agenda_local", dados: {protocolo: a.protocolo, horario_id: a.horario_id, nome: a.nome}, estado: "local", criado_em: agora()});
  return `<h1>Agenda do posto</h1>
    <div class="card cin-busca"><div class="campos">
      ${campo("cinPostoSel", "Posto", {tipo: "select", opcoes: postos.map(p=>[p.posto_id, p.nome]), valor: posto})}
      ${campo("cinBuscaPosto", "Buscar por protocolo, nome ou CPF (4 dígitos)", {valor: estado.cinBusca || "", attrs: 'autofocus autocomplete="off"'})}</div></div>
    <div class="grade"><div class="card kpi"><div class="v" data-cin-posto="hoje">${doDia.length}</div><div class="r">agendamentos hoje</div></div>
      <div class="card kpi"><div class="v" data-cin-posto="semana">${daSemana.length}</div><div class="r">na semana</div></div>
      <div class="card kpi"><div class="v" data-cin-posto="pendentes">${pendentes.length}</div><div class="r">pendentes de envio</div></div></div>
    ${pendentes.length ? `<div class="card pendente" id="cinFilaLocal"><b>${pendentes.length} item(ns) pendente(s) de envio.</b>
      <p class="sub">Sem internet, o posto trabalha na fila local e envia quando a conexão volta.</p>
      <div class="linha-botoes"><button id="btnCinEnviar">Marcar como enviados (simulação)</button></div></div>` : ""}
    <div class="card"><p class="sub">${busca ? `${lista.length} resultado(s) para “${esc(estado.cinBusca)}”.` : "Agendamentos desta semana. Busque pelo protocolo, pelo nome ou pelos 4 últimos dígitos do CPF."}</p>
    <div class="tabela-wrap"><table id="tabelaPosto"><tr><th>Protocolo</th><th>Data</th><th>Hora</th><th>Nome</th><th>Situação</th><th></th></tr>
      ${lista.map(a=>{ const h = horarios[a.horario_id]; return `<tr><td class="mono">${esc(a.protocolo)}</td><td>${dataCurtaBR(h.data)}</td><td>${esc(h.hora)}</td>
        <td>${esc(a.nome)}${a.cpf_final4 ? `<br><small class="sub">CPF ····${esc(a.cpf_final4)}</small>` : ""}</td>
        <td><span class="selo ${a.status === "compareceu" ? "ok" : a.status === "ausente" ? "erro" : a.status === "cancelado" ? "info" : "alerta"}">${esc(a.status)}</span></td>
        <td>${a.status === "confirmado" ? `<button data-compareceu="${esc(a.protocolo)}">Compareceu</button><button data-ausente="${esc(a.protocolo)}">Ausente</button><button data-cancelar-posto="${esc(a.protocolo)}">Cancelar</button>` : ""}</td></tr>`; }).join("")
        || '<tr><td colspan="6" class="vazio">Nenhum agendamento nesta semana.</td></tr>'}</table></div></div>
    <div id="cinErrosPosto"></div>`;
};
TELAS_DEPOIS["#/posto"] = ()=>{
  $("#cinPostoSel")?.addEventListener("change", e=>{ estado.cinPosto = e.target.value; navegar(); });
  let t = null;
  $("#cinBuscaPosto")?.addEventListener("input", e=>{
    clearTimeout(t); const v = e.target.value;
    t = setTimeout(()=>{ estado.cinBusca = v; navegar(); }, 350);
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
    try { await cinCancelar(b.dataset.cancelarPosto, "cancelado pelo posto", "posto"); toast("Reserva cancelada."); navegar(); }
    catch(err){ mostrarErros("#cinErrosPosto", [err.message]); }
  }));
  $("#btnCinEnviar")?.addEventListener("click", async ()=>{
    for (const f of await cinPendentes()) await cinMarcarEnviado(f.id);
    await registrar("fila local enviada", {detalhe: "simulação, sem Apps Script"});
    toast("Fila local marcada como enviada."); navegar();
  });
};
