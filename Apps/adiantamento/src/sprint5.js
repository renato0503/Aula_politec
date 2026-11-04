/* ================= Sprint 5 · Feedback 03/11/2026 =================
   Afastamento (férias/licença-prêmio), pedido urgente e recurso de 24 h.
   Premissas registradas em Apps/PREMISSAS.md:
   - afastamento marcado manualmente na Configuração (RH/SIGRH fica para depois);
   - urgência autorizada pela chefia da unidade, com justificativa na trilha;
   - recurso conta da aprovação da chefia. */

const AD_TIPOS_AFASTAMENTO = [["férias", "Férias"], ["licença-prêmio", "Licença-prêmio"]];

function adAfastamentoAtivo(lista, matricula, hoje = hojeISO()){
  const m = String(matricula || "").trim();
  if (!m) return null;
  return (lista || []).find(a => String(a.matricula || "").trim() === m && a.inicio <= hoje && a.fim >= hoje) || null;
}

function adRecursoInfo(p, agora = new Date()){
  if (!p?.recurso_ate) return null;
  const fim = new Date(p.recurso_ate);
  if (Number.isNaN(fim.getTime())) return null;
  const encerrado = !!p.recurso_em;
  const vencido = !encerrado && fim.getTime() <= agora.getTime();
  return {
    fim,
    encerrado,
    vencido,
    aberto: !encerrado && !vencido,
    horas: Math.max(0, Math.ceil((fim.getTime() - agora.getTime()) / 3600000))
  };
}

teste("AD: afastamento ativo bloqueia pelo período", ()=>{
  const l = [{matricula: "123", tipo: "férias", inicio: "2026-10-01", fim: "2026-10-31", motivo: "Férias"}];
  return !!adAfastamentoAtivo(l, "123", "2026-10-15")
    && !adAfastamentoAtivo(l, "123", "2026-11-01")
    && !adAfastamentoAtivo(l, "456", "2026-10-15");
});
teste("AD: recurso aberto até o prazo de 24 h", ()=>{
  const p = {recurso_ate: "2026-10-02T12:00:00.000Z"};
  return adRecursoInfo(p, new Date("2026-10-02T10:00:00.000Z")).aberto
    && !adRecursoInfo(p, new Date("2026-10-02T10:00:00.000Z")).vencido
    && adRecursoInfo(p, new Date("2026-10-03T13:00:00.000Z")).vencido
    && adRecursoInfo({...p, recurso_em: "2026-10-02T11:00:00.000Z"}, new Date("2026-10-03T13:00:00.000Z")).encerrado;
});

/* ---------- 1. afastamentos na configuração ---------- */
const adConfigExtraS4 = configExtra;
configExtra = async ()=>{
  const base = await adConfigExtraS4();
  const afs = (await db.list("afastamentos")).sort((a, b)=>String(b.inicio).localeCompare(String(a.inicio)));
  const linhas = afs.map(a=>`<tr><td class="mono">${esc(a.matricula)}</td><td>${esc(a.tipo)}</td>
    <td>${dataCurtaBR(a.inicio)}</td><td>${dataCurtaBR(a.fim)}</td><td>${esc(a.motivo)}</td>
    <td><button type="button" class="perigo" data-ad-af-del="${esc(a.id)}">Excluir</button></td></tr>`).join("");
  return base + `<div class="card"><h2 style="margin-top:0">Afastamentos (férias e licença-prêmio)</h2>
    <p class="sub">Marcação manual nesta cópia. Na versão institucional, o afastamento deve vir do RH/SIGRH; o pedido de quem está afastado é bloqueado no período.</p>
    <div class="campos">
      ${campo("adAfMat", "Matrícula", {attrs: 'inputmode="numeric" placeholder="somente números"'})}
      ${campo("adAfTipo", "Tipo", {tipo: "select", opcoes: AD_TIPOS_AFASTAMENTO})}
      ${campo("adAfInicio", "Início", {tipo: "date", valor: hojeISO()})}
      ${campo("adAfFim", "Fim", {tipo: "date", valor: hojeISO()})}
    </div>
    ${campo("adAfMotivo", "Motivo", {attrs: 'placeholder="Ex.: férias regulamentares"'})}
    <div id="adAfErros"></div><div class="linha-botoes"><button class="prim" type="button" id="btnAdAf">Registrar afastamento</button></div>
    <div class="tabela-wrap"><table><thead><tr><th>Matrícula</th><th>Tipo</th><th>Início</th><th>Fim</th><th>Motivo</th><th></th></tr></thead>
      <tbody>${linhas || '<tr><td colspan="6" class="vazio">Nenhum afastamento marcado.</td></tr>'}</tbody></table></div></div>`;
};

const adLigarConfigS4 = ligarConfigExtra;
ligarConfigExtra = async ()=>{
  await adLigarConfigS4();
  $("#btnAdAf")?.addEventListener("click", async ()=>{
    const matricula = valorDe("adAfMat"), tipo = valorDe("adAfTipo"), inicio = valorDe("adAfInicio"), fim = valorDe("adAfFim"), motivo = valorDe("adAfMotivo").trim();
    const erros = [];
    if (!/^\d{3,}$/.test(matricula)) erros.push("A matrícula só aceita números (mínimo 3).");
    if (!inicio || !fim) erros.push("Informe o início e o fim do afastamento.");
    else if (fim < inicio) erros.push("O fim não pode ser antes do início.");
    if (!motivo) erros.push("Informe o motivo.");
    if (!mostrarErros("#adAfErros", erros)) return;
    await db.put("afastamentos", {id: uuid(), matricula, tipo, inicio, fim, motivo, criado_em: agora()});
    await registrar("afastamento registrado", {detalhe: `${matricula} · ${tipo} · ${inicio} a ${fim}`});
    toast("Afastamento registrado."); navegar();
  });
  $$("[data-ad-af-del]").forEach(b=>b.addEventListener("click", async ()=>{
    await db.del("afastamentos", b.dataset.adAfDel);
    await registrar("afastamento removido", {detalhe: b.dataset.adAfDel});
    toast("Afastamento removido."); navegar();
  }));
};

/* ---------- 2. recurso de 24 h ao sair da aprovação da chefia ---------- */
const adMoverEtapaS3 = moverEtapa;
moverEtapa = async (pid, sentido, opts = {})=>{
  const antes = await db.get("processos", pid);
  const indice = antes ? ETAPAS.indexOf(antes.etapa_atual) : -1;
  const r = await adMoverEtapaS3(pid, sentido, opts);
  if (antes && sentido > 0 && ETAPAS[indice] === "Aprovação da chefia") {
    const data = opts.data || hojeISO();
    const fim = new Date(data + "T12:00:00");
    fim.setDate(fim.getDate() + 1);
    const p = await db.get("processos", pid);
    await db.put("processos", {...p, aprovado_em: data, recurso_ate: fim.toISOString(), recurso_em: "", recurso_texto: ""});
    await registrar("recurso aberto (24 h)", {processo_id: pid, detalhe: `até ${fim.toISOString()}`});
  }
  return r;
};

/* ---------- 3. ficha: urgência e recurso ---------- */
function adBlocoRecurso(p){
  const r = adRecursoInfo(p);
  if (!r) return "";
  const quando = r.fim.toLocaleString("pt-BR", {dateStyle: "short", timeStyle: "short"});
  const selo = r.encerrado ? '<span class="selo ok">recurso registrado</span>'
    : r.vencido ? '<span class="selo erro">prazo encerrado</span>'
    : `<span class="selo alerta">aberto · ${r.horas} h</span>`;
  return `<div class="card" id="adRecurso"><h2 style="margin-top:0">Recurso de 24 h</h2>
    <p class="sub">Aprovado em ${dataCurtaBR(p.aprovado_em)} · prazo até ${quando}. ${selo}</p>
    ${r.encerrado ? `<p>${esc(p.recurso_texto || "")}</p>`
      : r.aberto ? `${campo("adRecursoTexto", "Recurso", {tipo: "textarea", linhas: 2})}
        <div class="linha-botoes"><button type="button" class="prim" id="adBtnRecurso">Registrar recurso</button></div>`
      : '<p class="sub">O prazo de 24 h terminou; o recurso não pode mais ser registrado neste app.</p>'}</div>`;
}

const adFichaS4 = TELAS["#/processo/:id"];
TELAS["#/processo/:id"] = async (params)=>{
  const html = await adFichaS4(params);
  const p = await db.get("processos", params.id);
  if (!p) return html;
  let extra = "";
  if (p.urgente) extra += `<div class="card" id="adUrgente"><h2 style="margin-top:0">Pedido urgente</h2>
    <p class="sub">Fora da fila normal; a chefia da unidade autoriza e a justificativa fica na trilha.</p>
    <p>${esc(p.urgencia_justificativa || "")}</p></div>`;
  extra += adBlocoRecurso(p);
  return html + extra;
};

const adFichaDepoisS4 = TELAS_DEPOIS["#/processo/:id"];
TELAS_DEPOIS["#/processo/:id"] = (params)=>{
  adFichaDepoisS4?.(params);
  $("#adBtnRecurso")?.addEventListener("click", async ()=>{
    const txt = valorDe("adRecursoTexto").trim();
    if (txt.length < 10) { toast("Escreva o recurso com pelo menos 10 caracteres."); return; }
    const p = await db.get("processos", params.id);
    if (!p) return;
    await db.put("processos", {...p, recurso_em: agora(), recurso_texto: txt});
    await registrar("recurso registrado", {processo_id: params.id, detalhe: txt.slice(0, 100)});
    toast("Recurso registrado."); navegar();
  });
};

/* ---------- 4. painel: urgentes, recursos e afastados ---------- */
const adPainelS4 = TELAS["#/painel"];
TELAS["#/painel"] = async ()=>{
  const html = await adPainelS4();
  const ps = await db.list("processos"), hoje = hojeISO();
  const urgentes = ps.filter(p=>p.urgente && p.situacao !== "encerrado");
  const recursos = ps.map(p=>({p, r: adRecursoInfo(p)})).filter(x=>x.r && !x.r.encerrado);
  const afastados = (await db.list("afastamentos")).filter(a=>a.inicio <= hoje && a.fim >= hoje);
  let extra = "";
  if (urgentes.length) extra += `<div class="card tabela-wrap"><h2 style="margin-top:0">Pedidos urgentes</h2>
    <table><thead><tr><th>Processo</th><th>Unidade</th><th>Etapa</th><th>Justificativa</th></tr></thead><tbody>
    ${urgentes.map(p=>`<tr><td><a href="#/processo/${encodeURIComponent(p.id)}">${esc(p.id)}</a></td><td>${esc(p.unidade)}</td>
      <td>${esc(p.etapa_atual)}</td><td>${esc(p.urgencia_justificativa || "")}</td></tr>`).join("")}</tbody></table></div>`;
  if (recursos.length) extra += `<div class="card tabela-wrap"><h2 style="margin-top:0">Recursos de 24 h</h2>
    <table><thead><tr><th>Processo</th><th>Aprovado em</th><th>Prazo</th><th>Situação</th></tr></thead><tbody>
    ${recursos.map(({p, r})=>`<tr><td><a href="#/processo/${encodeURIComponent(p.id)}">${esc(p.id)}</a></td>
      <td>${dataCurtaBR(p.aprovado_em)}</td><td>${r.fim.toLocaleString("pt-BR", {dateStyle: "short", timeStyle: "short"})}</td>
      <td>${r.vencido ? '<span class="selo erro">vencido</span>' : `<span class="selo alerta">aberto · ${r.horas} h</span>`}</td></tr>`).join("")}</tbody></table></div>`;
  if (afastados.length) extra += `<div class="card"><h2 style="margin-top:0">Afastamentos hoje</h2>
    <p class="sub">${afastados.map(a=>`${esc(a.matricula)} · ${esc(a.tipo)} · ${dataCurtaBR(a.inicio)} a ${dataCurtaBR(a.fim)} · ${esc(a.motivo)}`).join("<br>")}</p></div>`;
  return html + extra;
};
