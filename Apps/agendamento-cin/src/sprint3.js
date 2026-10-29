/* ================= Sprint 3 · Agendamento do cidadão (RN02, RN03, RN09) ================= */
// Mesmas regras do Code.gs (listarVagas, reservar, comprovante). A trava contra reserva simultânea entra no Sprint 4.
const JANELA = {min: 1, max: 30};  // RN09: de 1 a 30 dias de antecedência
function dentroDaJanela(data, hoje = hojeISO()){ return data >= somarDias(hoje, JANELA.min) && data <= somarDias(hoje, JANELA.max); }
teste("RN09: hoje não pode, amanhã pode, 31 dias não pode", ()=> !dentroDaJanela("2026-10-29", "2026-10-29") && dentroDaJanela("2026-10-30", "2026-10-29") && !dentroDaJanela("2026-11-29", "2026-10-29"));
const novoProtocoloCin = ()=> "CIN-" + Array.from(crypto.getRandomValues(new Uint8Array(6)), b=>"ABCDEFGHJKLMNPQRSTUVWXYZ23456789"[b % 32]).join("");

if (!NO_APPS_SCRIPT) Object.assign(api, {
  async listarVagas(posto_id){
    return (await db.porIndice("horarios", "posto_id", posto_id))
      .filter(h=>h.situacao === "aberto" && Number(h.ocupadas) < Number(h.capacidade) && dentroDaJanela(h.data))
      .sort((a, b)=>(a.data + a.hora).localeCompare(b.data + b.hora));
  },
  async reservar(d){
    const h = await db.get("horarios", d.horario_id);
    if (!h || h.situacao !== "aberto" || !dentroDaJanela(h.data)) throw new Error("Este horário não está disponível.");
    if (Number(h.ocupadas) >= Number(h.capacidade)) throw new Error("Este horário acabou de ser preenchido. Escolha outro.");
    let protocolo; do { protocolo = novoProtocoloCin(); } while (await db.get("agendamentos", protocolo));
    await db.put("horarios", {...h, ocupadas: Number(h.ocupadas) + 1});
    await db.put("agendamentos", {protocolo, posto_id: h.posto_id, horario_id: h.horario_id, nome: d.nome, telefone: d.telefone || "", email: d.email || "",
      cpf_final4: d.cpf ? d.cpf.slice(-4) : "", status: "confirmado", criado_em: agora(), cancelado_em: "", compareceu_em: ""});
    return {protocolo};
  },
  async comprovante(protocolo){
    const a = await db.get("agendamentos", protocolo); if (!a) return null;
    const h = await db.get("horarios", a.horario_id), p = await db.get("postos", a.posto_id);
    return {protocolo, primeiro_nome: a.nome.split(" ")[0], data: h?.data, hora: h?.hora, status: a.status, posto: p?.nome, endereco: p?.endereco, documentos: p?.documentos_orientacao};
  }
});

TELAS["#/agendar"] = async ()=>{
  const postos = await api.listarPostos(), escolhido = estado.agPosto && postos.find(p=>p.posto_id === estado.agPosto);
  let corpo = "";
  if (escolhido){
    const vagas = await api.listarVagas(escolhido.posto_id), dias = {};
    vagas.forEach(h=>(dias[h.data] = dias[h.data] || []).push(h));
    const dia = estado.agDia && dias[estado.agDia] ? estado.agDia : null;
    corpo = `<div class="card"><h2 style="margin-top:0">2. Dia</h2>${Object.keys(dias).length ? `<div style="display:flex;flex-wrap:wrap;gap:6px">${Object.entries(dias).map(([d, hs])=>
        `<button data-dia="${d}" ${d === dia ? 'class="prim"' : ""}>${dataCurtaBR(d)}<br><small>${hs.length} horários</small></button>`).join("")}</div>`
      : '<p class="sub">Sem vagas nos próximos 30 dias neste posto.</p>'}</div>
      ${dia ? `<div class="card"><h2 style="margin-top:0">3. Horário · ${dataCurtaBR(dia)}</h2><div style="display:flex;flex-wrap:wrap;gap:6px">
        ${dias[dia].map(h=>`<button data-horario="${h.horario_id}" data-hora="${h.hora}">${h.hora}</button>`).join("")}</div></div>` : ""}`;
  }
  return `<h1>Agendar a Carteira de Identidade</h1><p class="sub">Escolha o posto, o dia e o horário. Agendamento de 1 a 30 dias à frente.</p>
    ${NO_APPS_SCRIPT ? "" : `<p class="selo alerta">Modo de teste local, com dados fictícios</p>`}
    <div class="card"><h2 style="margin-top:0">1. Posto</h2><div class="grade">${postos.map(p=>`<button class="card" data-posto="${esc(p.posto_id)}" style="text-align:left;${p.posto_id === estado.agPosto ? "border-color:var(--accent);border-width:2px" : ""}">
      <b>${esc(p.nome)}</b><br><span class="sub">${esc(p.municipio)} · ${esc(p.endereco)}</span></button>`).join("")}</div></div>${corpo}
    <p class="sub"><a href="#/consultar">Consultar ou cancelar uma reserva</a>${NO_APPS_SCRIPT ? "" : ` · <a href="#/posto">Área do posto (teste)</a>`}</p>`;
};
TELAS_DEPOIS["#/agendar"] = ()=>{
  $$("[data-posto]").forEach(b=>b.addEventListener("click", ()=>{ estado.agPosto = b.dataset.posto; estado.agDia = null; navegar(); }));
  $$("[data-dia]").forEach(b=>b.addEventListener("click", ()=>{ estado.agDia = b.dataset.dia; navegar(); }));
  $$("[data-horario]").forEach(b=>b.addEventListener("click", ()=>{
    estado.agReserva = {posto_id: estado.agPosto, horario_id: b.dataset.horario, data: estado.agDia, hora: b.dataset.hora}; location.hash = "#/agendar/dados";
  }));
};

TELAS["#/agendar/dados"] = async ()=>{
  const r = estado.agReserva;
  if (!r) return `<div class="card vazio">Escolha primeiro o posto, o dia e o horário. <a href="#/agendar">Agendar</a></div>`;
  const p = (await api.listarPostos()).find(x=>x.posto_id === r.posto_id);
  return `<h1>Seus dados</h1><p class="sub">${esc(p?.nome || "")} · <b>${dataCurtaBR(r.data)} às ${esc(r.hora)}</b> · <a href="#/agendar">trocar</a></p>
    <form class="card" id="formAgDados" novalidate><div class="campos">
      ${campo("aNome", "Nome completo", {obrigatorio: true, attrs: 'autocomplete="name"'})}
      ${campo("aTel", "Telefone com DDD", {tipo: "tel", attrs: 'autocomplete="tel"', ajuda: "Informe telefone ou e-mail."})}
      ${campo("aEmail", "E-mail", {tipo: "email", attrs: 'autocomplete="email"', ajuda: "Recebe a confirmação (a partir do Sprint 4)."})}
      ${campo("aCpf", "CPF (opcional)", {attrs: 'inputmode="numeric" autocomplete="off"', ajuda: "Guardamos só os 4 últimos dígitos, para consultar a reserva."})}</div>
    <label style="display:flex;gap:8px;align-items:flex-start;margin-top:12px"><input type="checkbox" id="aAviso" style="width:auto;margin-top:4px">
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
  return `<h1>Agendamento confirmado</h1><div class="card" id="cardComprovanteCin">
    <p>Protocolo: <b class="mono" id="protCin">${esc(c.protocolo)}</b></p>
    <p><b>${esc(c.primeiro_nome)}</b>, seu atendimento é em <b>${dataCurtaBR(c.data)} às ${esc(c.hora)}</b>.</p>
    <p><b>Posto:</b> ${esc(c.posto)}<br>${esc(c.endereco || "")}</p>
    <h2>Documentos para levar</h2><p>${esc(c.documentos || "Consulte o posto.")}</p>
    <p class="sub">Chegue 10 minutos antes. Depois de 15 minutos de atraso, o horário é liberado.</p>
    <div class="linha-botoes nao-imprimir"><button onclick="window.print()">Imprimir</button><a class="botao" href="#/consultar">Consultar ou cancelar</a></div></div>`;
};
