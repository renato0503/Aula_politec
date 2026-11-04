/* ================= Sprint 8 · Fluxo, prazos e avisos ================= */
async function iniciarApp(){
  try { const v = await db.meta("tap_objetivos"); if (Array.isArray(v) && v.length) TAP_OBJETIVOS = v; } catch(e){}
}

function tapPrazo(iso, dias){
  const d = new Date(iso + "T12:00:00"); let n = 0;
  while (n < dias){ d.setDate(d.getDate() + 1); const w = d.getDay(); if (w !== 0 && w !== 6) n++; }
  return d.toISOString().slice(0, 10);
}
function tapDiasAte(iso){
  if (!iso) return null;
  return Math.round((new Date(iso + "T12:00:00") - new Date(hojeISO() + "T12:00:00")) / 86400000);
}
async function tapAviso(proposta_id, para, texto){
  await db.put("avisos", {id: uuid(), proposta_id, para, texto, criado_em: agora(), lido_em: null, canal: "fila local"});
}
async function tapAvisosDe(id){
  return (await db.porIndice("avisos", "proposta_id", id)).sort((a, b)=>String(b.criado_em).localeCompare(String(a.criado_em)));
}

/* ---------- ficha: sanar pendências e reenviar ---------- */
const tapFichaS4 = TELAS["#/proposta/:id"];
TELAS["#/proposta/:id"] = async (p)=>{
  const html = await tapFichaS4(p);
  const prop = await db.get("propostas", p.id); if (!prop) return html;
  const abertas = (await db.porIndice("pendencias", "proposta_id", p.id)).filter(x=>!x.resolvida_em);
  const avisos = await tapAvisosDe(p.id);
  const podeSanar = prop.status === "devolvida" && abertas.length;
  return html + `<div class="card" id="tapPosPendencia">
    <h2 style="margin-top:0">Pendências, prazos e avisos</h2>
    ${abertas.length ? `<ul>${abertas.map(x=>{ const d = tapDiasAte(x.prazo_limite); return `<li>${esc(x.motivo)} · prazo ${x.prazo_limite ? dataCurtaBR(x.prazo_limite) : "não definido"}${d !== null ? ` (${d < 0 ? Math.abs(d) + " dia(s) em atraso" : d + " dia(s)"})` : ""}</li>`; }).join("")}</ul>` : '<p class="ok-txt">Sem pendências abertas.</p>'}
    ${podeSanar ? `<p class="sub">Ao reenviar, o app marca as pendências como resolvidas, volta o TAP para a análise e avisa a equipe e a autoridade na fila local.</p><button class="prim" type="button" id="btnTapSanar">Sanar pendências e reenviar para análise</button>` : ""}
    <h3>Avisos</h3><ul class="check-lista">${avisos.map(a=>`<li class="${a.lido_em ? "feito" : "falta"}">${icone(a.lido_em ? "check" : "alerta")}<span><b>${esc(a.para)}</b> · ${dataBR(a.criado_em)}<br><small class="sub">${esc(a.texto)}</small>
      ${a.lido_em ? ' · <span class="selo ok">lido</span>' : ` · <button type="button" data-tap-lido="${esc(a.id)}">Marcar como lido</button>`}</span></li>`).join("") || '<li class="vazio">Nenhum aviso.</li>'}</ul>
    <p class="sub">A fila é local. O envio real por e-mail usa MailApp/Apps Script; o passo a passo fica na Ajuda Técnica (três cliques no nome do app no rodapé).</p></div>`;
};
const tapFichaDepoisS4 = TELAS_DEPOIS["#/proposta/:id"];
TELAS_DEPOIS["#/proposta/:id"] = async (p)=>{
  await tapFichaDepoisS4?.(p);
  $("#btnTapSanar")?.addEventListener("click", async ()=>{
    const prop = await db.get("propostas", p.id);
    const abertas = (await db.porIndice("pendencias", "proposta_id", p.id)).filter(x=>!x.resolvida_em);
    for (const x of abertas) await db.put("pendencias", {...x, resolvida_em: hojeISO()});
    await db.put("propostas", {...prop, status: "em análise", pendencias_sanadas_em: agora()});
    await tapAviso(p.id, "equipe de projetos", `A unidade demandante sanou as pendências do ${p.id} e reenviou o TAP para análise.`);
    await tapAviso(p.id, "autoridade", `O ${p.id} · ${prop.titulo} voltou para análise e aguarda decisão.`);
    await registrar("pendências sanadas e TAP reenviado", {proposta_id: p.id});
    toast("Pendências sanadas. TAP em análise; equipe e autoridade avisadas na fila local."); navegar();
  });
  $$("[data-tap-lido]").forEach(b=>b.addEventListener("click", async ()=>{
    const a = await db.get("avisos", b.dataset.tapLido);
    await db.put("avisos", {...a, lido_em: agora()});
    await registrar("aviso lido", {proposta_id: a.proposta_id, detalhe: a.para});
    toast("Aviso marcado como lido."); navegar();
  }));
};

/* ---------- triagem: prazos vencidos e projetos para aprovar ---------- */
const tapPainelAntes = TELAS["#/triagem"];
TELAS["#/triagem"] = async ()=>{
  const html = await tapPainelAntes();
  const [ps, pends, avisos] = await Promise.all([db.list("propostas"), db.list("pendencias"), db.list("avisos")]);
  const atrasadas = pends.filter(x=>!x.resolvida_em && x.prazo_limite && tapDiasAte(x.prazo_limite) < 0);
  const emAnalise = ps.filter(p=>p.status === "em análise");
  return html + `<div class="card tabela-wrap" id="tapPainelAvisos"><h2 style="margin-top:0">Prazos e avisos</h2>
    <p class="sub">${atrasadas.length} pendência(s) fora do prazo de 5 dias · ${emAnalise.length} projeto(s) em análise · ${avisos.filter(a=>!a.lido_em).length} aviso(s) não lido(s).</p>
    <table><thead><tr><th>TAP</th><th>Pendência</th><th>Prazo</th><th>Situação</th><th></th></tr></thead><tbody>
    ${atrasadas.map(x=>{ const p = ps.find(y=>y.id === x.proposta_id); return `<tr><td>${esc(x.proposta_id)}</td><td>${esc(x.motivo)}</td><td>${dataCurtaBR(x.prazo_limite)}</td>
      <td><span class="selo erro">${Math.abs(tapDiasAte(x.prazo_limite))} dia(s) em atraso</span></td><td><button type="button" data-tap-cobrar="${esc(x.id)}">Avisar a equipe</button></td></tr>`; }).join("") || '<tr><td colspan="5" class="vazio">Nenhuma pendência em atraso.</td></tr>'}
    </tbody></table>
    <h3>Em análise</h3><ul class="check-lista">${emAnalise.map(p=>`<li class="feito">${icone("check")}<span><a href="#/proposta/${encodeURIComponent(p.id)}">${esc(p.id)} · ${esc(p.titulo)}</a>
      <br><small class="sub">${esc(p.unidade)} · ${esc(p.objetivo_estrategico || "")}</small></span></li>`).join("") || '<li class="vazio">Nenhum projeto em análise.</li>'}</ul></div>`;
};
const tapPainelDepois = TELAS_DEPOIS["#/triagem"];
TELAS_DEPOIS["#/triagem"] = async ()=>{
  await tapPainelDepois?.();
  $$("[data-tap-cobrar]").forEach(b=>b.addEventListener("click", async ()=>{
    const x = await db.get("pendencias", b.dataset.tapCobrar);
    await tapAviso(x.proposta_id, "equipe de projetos", `O prazo da pendência "${x.motivo}" do ${x.proposta_id} venceu em ${dataCurtaBR(x.prazo_limite)}.`);
    await registrar("cobrança de prazo registrada", {proposta_id: x.proposta_id});
    toast("Aviso de prazo registrado na fila local."); navegar();
  }));
};

/* ---------- configuração dos objetivos estratégicos ---------- */
const tapConfigAntes = TELAS["#/config"];
TELAS["#/config"] = async ()=>{
  const html = await tapConfigAntes();
  return html + `<div class="card" id="tapObjetivosCard"><h2 style="margin-top:0">Objetivos estratégicos</h2>
    <p class="sub">Um objetivo por linha. A lista vale para os próximos TAPs; o TAP já gravado mantém o texto escolhido.</p>
    ${campo("tapObjetivos", "Objetivos do plano estratégico", {tipo: "textarea", linhas: 6, valor: TAP_OBJETIVOS.join("\n")})}
    <div id="tapObjErros"></div><div class="linha-botoes"><button type="button" class="prim" id="btnTapObjetivos">Salvar objetivos</button></div></div>`;
};
const tapConfigDepois = TELAS_DEPOIS["#/config"];
TELAS_DEPOIS["#/config"] = async ()=>{
  await tapConfigDepois?.();
  $("#btnTapObjetivos")?.addEventListener("click", async ()=>{
    const lista = [...new Set(valorDe("tapObjetivos").split("\n").map(x=>x.trim()).filter(Boolean))];
    if (!lista.length) return mostrarErros("#tapObjErros", ["Informe pelo menos um objetivo."]);
    TAP_OBJETIVOS = lista; await db.meta("tap_objetivos", lista);
    await registrar("objetivos estratégicos atualizados", {detalhe: `${lista.length} objetivos`});
    toast("Objetivos atualizados."); navegar();
  });
};
