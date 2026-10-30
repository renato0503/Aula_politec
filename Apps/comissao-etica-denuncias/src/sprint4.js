/* ================= Sprint 4 · Admissibilidade (RN03, RN04) e Sprint 5 · Oitivas ================= */
/* Prazos do art. 8º da LC nº 112/2002-MT: manifestação em 5 dias (§ 1º) e nova manifestação em 3 dias (§ 4º). */
const CE_PRAZO_MANIFESTACAO = 5;
const CE_PRAZO_NOVA = 3;
const CE_VIAS = {
  acatada: "Acatada (prossegue)",
  sem_enquadramento: "Não acatada (sem enquadramento no Código)",
  corregedoria: "Encaminhada à corregedoria",
};
const cePrazo = (dias)=> new Date(Date.now() + dias * 86400000).toISOString().slice(0, 10);
function ceDias(iso){ return iso ? Math.max(0, Math.round((Date.now() - new Date(iso)) / 86400000)) : null; }

async function ceClassificacao(id){ return (await db.porIndice("classificacoes", "denuncia_id", id)).filter(c=>c.confirmada).pop(); }
async function ceDeliberacoes(id){ return (await db.porIndice("deliberacoes", "denuncia_id", id)).sort((a, b)=>(a.data || "").localeCompare(b.data || "")); }
async function ceAdmissao(id){ return (await ceDeliberacoes(id)).filter(d=>d.tipo === "admissibilidade").pop(); }
async function ceOitivas(id){ return (await db.porIndice("oitivas", "denuncia_id", id)).sort((a, b)=>(a.data || "").localeCompare(b.data || "")); }

// RN03: admissibilidade só depois da classificação confirmada
function cePodeAdmitir(cls){ return !!cls; }
teste("RN03: sem classificação confirmada não há admissibilidade", ()=> !cePodeAdmitir(null) && cePodeAdmitir({confirmada: true}));

TELAS["#/caso/:id/admissibilidade"] = async ({id})=>{
  const d = await db.get("denuncias", id);
  if (!d) return `<div class="card vazio">Caso não encontrado.</div>`;
  const cls = await ceClassificacao(id), admissao = await ceAdmissao(id), cats = await categoriasAtivas();
  const cat = cats.find(c=>c.id === (cls?.categoria_final || d.categoria));
  const pendencias = (await ceDeliberacoes(id)).filter(x=>x.tipo === "prova_pendente" && !x.resolvido_em);
  return `<p class="sub nao-imprimir" style="margin-bottom:6px"><a href="#/caso/${encodeURIComponent(id)}">← Caso ${esc(d.protocolo)}</a></p>
    <h1>Admissibilidade · ${esc(d.protocolo)}</h1>
    <p class="sub">Art. 8º da LC nº 112/2002-MT: o processo é instaurado pela Comissão, de ofício ou por denúncia fundamentada.</p>
    ${!cls ? `<div class="card pendente"><b>Bloqueado (RN03).</b> Confirme a classificação antes de decidir a admissibilidade.
      <div class="linha-botoes"><a class="botao prim" href="#/caso/${encodeURIComponent(id)}/classificacao">Ir para a classificação</a></div></div>`
    : `<div class="card"><h2 style="margin-top:0">Classificação confirmada</h2>
        <p><b>${esc(cat?.nome || cls.categoria_final)}</b> · ${esc(cat?.artigos || "")}</p>
        <p class="sub">${esc(cat?.texto_artigo || "")}</p></div>
      ${admissao ? `<div class="card" id="admissaoFeita"><h2 style="margin-top:0">Decisão de admissibilidade</h2>
        <p><span class="selo ${admissao.via === "acatada" ? "ok" : admissao.via === "corregedoria" ? "alerta" : "erro"}">${esc(CE_VIAS[admissao.via] || admissao.via)}</span>
        · ${dataBR(admissao.data)} · ${esc(admissao.membros || "")}</p>
        <p>${esc(admissao.justificativa)}</p>
        <div class="linha-botoes">${admissao.via === "acatada" ? `<a class="botao prim" href="#/caso/${encodeURIComponent(id)}/oitivas">Ir para as oitivas</a>` : ""}</div></div>`
      : `<form class="card" id="formAdmissao"><h2 style="margin-top:0">Decidir a admissibilidade</h2>
          <div class="campos">${campo("adVia", "Via", {tipo: "select", opcoes: Object.entries(CE_VIAS)})}
            ${campo("adMembros", "Membros presentes", {ajuda: "A comissão tem 3 servidores efetivos e suplentes (art. 6º)."})}</div>
          ${campo("adJust", "Fundamento da decisão (mínimo de 20 caracteres)", {tipo: "textarea", linhas: 4})}
          <label style="display:flex;gap:8px;align-items:center;margin:12px 0"><input type="checkbox" id="adProvaPendente" style="width:auto">
            <span>Prova pendente: aguardando o denunciante (RN04, prazo de ${CE_PRAZO_MANIFESTACAO} dias)</span></label>
          ${campo("adProvaTexto", "O que falta da prova", {ajuda: "Só se a prova estiver pendente."})}
          <div id="ceErrosAdmissao"></div>
          <div class="linha-botoes"><button class="prim" type="submit">Registrar a decisão</button></div></form>`}
      ${pendencias.length ? `<div class="card pendente"><h2 style="margin-top:0">Prova pendente (RN04)</h2>
        ${pendencias.map(x=>`<p><b>${esc(x.texto)}</b> · prazo ${dataCurtaBR(x.prazo)}${x.prazo < hojeISO() ? ' · <span class="erro-txt">vencido</span>' : ""}</p>`).join("")}
        <div class="linha-botoes"><button id="btnProvaRecebida">Registrar que a prova chegou</button></div></div>` : ""}`}`;
};
TELAS_DEPOIS["#/caso/:id/admissibilidade"] = ({id})=>{
  $("#formAdmissao")?.addEventListener("submit", async e=>{
    e.preventDefault();
    const via = valorDe("adVia"), just = valorDe("adJust"), membros = valorDe("adMembros");
    const pendente = $("#adProvaPendente").checked, texto = valorDe("adProvaTexto");
    const erros = [];
    if (just.length < 20) erros.push("Escreva o fundamento com pelo menos 20 caracteres (art. 12: a Comissão não se exime de fundamentar).");
    if (pendente && !texto) erros.push("Diga o que falta da prova (RN04).");
    if (!mostrarErros("#ceErrosAdmissao", erros)) return;
    const d = await db.get("denuncias", id);
    await db.put("deliberacoes", {id: uuid(), denuncia_id: id, tipo: "admissibilidade", via, justificativa: just, membros, data: agora(), perfil: estado.perfil});
    if (pendente) await db.put("deliberacoes", {id: uuid(), denuncia_id: id, tipo: "prova_pendente", texto, prazo: cePrazo(CE_PRAZO_MANIFESTACAO), resolvido_em: null, data: agora(), perfil: estado.perfil});
    const etapa = via === "acatada" ? "oitivas" : "encerrado";
    await db.put("denuncias", {...d, etapa, situacao: via === "acatada" ? "admitida" : via === "corregedoria" ? "encaminhada à corregedoria" : "arquivada", admissao_via: via});
    await trilha("admissibilidade: " + via, id, just);
    toast("Admissibilidade registrada."); navegar();
  });
  $("#btnProvaRecebida")?.addEventListener("click", async ()=>{
    for (const x of (await ceDeliberacoes(id)).filter(y=>y.tipo === "prova_pendente" && !y.resolvido_em))
      await db.put("deliberacoes", {...x, resolvido_em: agora()});
    await trilha("prova recebida", id); toast("Prova registrada como recebida."); navegar();
  });
};

/* ================= Sprint 5 · Oitivas (art. 8º, §§ 2º a 4º) ================= */
TELAS["#/caso/:id/oitivas"] = async ({id})=>{
  const d = await db.get("denuncias", id);
  if (!d) return `<div class="card vazio">Caso não encontrado.</div>`;
  const admissao = await ceAdmissao(id), oitivas = await ceOitivas(id), cats = await categoriasAtivas();
  const cat = cats.find(c=>c.id === d.categoria);
  const pendencias = (await ceDeliberacoes(id)).filter(x=>x.tipo === "prova_pendente" && !x.resolvido_em);
  if (!admissao || admissao.via !== "acatada")
    return `<p class="sub"><a href="#/caso/${encodeURIComponent(id)}">← Caso</a></p><h1>Oitivas</h1>
      <div class="card pendente"><b>Bloqueado (RN03).</b> A oitiva só acontece depois da admissibilidade acatada.</div>`;
  if (pendencias.length)
    return `<p class="sub"><a href="#/caso/${encodeURIComponent(id)}">← Caso</a></p><h1>Oitivas</h1>
      <div class="card pendente"><b>Prova pendente (RN04).</b> Registre que a prova chegou antes de marcar a oitiva.</div>`;
  const roteiro = cat?.roteiro_base || ["Descreva, com suas palavras, o que aconteceu.", "Quando e onde o fato ocorreu?", "Quem estava presente?", "Existe registro do fato?", "O fato já tinha acontecido antes?"];
  return `<p class="sub nao-imprimir" style="margin-bottom:6px"><a href="#/caso/${encodeURIComponent(id)}">← Caso ${esc(d.protocolo)}</a></p>
    <h1>Oitivas · ${esc(d.protocolo)}</h1>
    <p class="sub">Roteiro sugerido pela categoria ${esc(cat?.nome || "")}. A oitiva gera um termo com o que foi dito.</p>
    <div class="card"><h2 style="margin-top:0">Roteiro sugerido</h2><ol>${roteiro.map(p=>`<li>${esc(p)}</li>`).join("")}</ol></div>
    <form class="card" id="formOitiva"><h2 style="margin-top:0">Registrar oitiva</h2><div class="campos">
      ${campo("oiQuem", "Quem foi ouvido", {tipo: "select", opcoes: [["denunciante", "Denunciante"], ["denunciado", "Denunciado(a)"], ["testemunha", "Testemunha"]]})}
      ${campo("oiData", "Data", {tipo: "date", valor: hojeISO()})}
      ${campo("oiPrazo", "Prazo para nova manifestação (dias)", {tipo: "number", valor: CE_PRAZO_NOVA, attrs: 'min="1" step="1"', ajuda: "Art. 8º, § 4º: 3 dias."})}</div>
      ${campo("oiTermo", "Termo da oitiva (sem nomes de terceiros)", {tipo: "textarea", linhas: 5, obrigatorio: true, ajuda: "Mínimo de 30 caracteres."})}
      <div id="ceErrosOitiva"></div><div class="linha-botoes"><button class="prim" type="submit">Registrar e gerar o termo</button></div></form>
    <div class="card" id="listaOitivas"><h2 style="margin-top:0">Oitivas registradas (${oitivas.length})</h2>
      ${oitivas.map(o=>`<div class="card"><b>${esc(o.quem)}</b> · ${dataBR(o.data)} · prazo da nova manifestação ${dataCurtaBR(o.prazo_nova)}
        <p class="sub" style="white-space:pre-wrap">${esc(o.termo)}</p></div>`).join("") || '<p class="sub">Nenhuma oitiva registrada.</p>'}</div>`;
};
TELAS_DEPOIS["#/caso/:id/oitivas"] = ({id})=>{
  $("#formOitiva")?.addEventListener("submit", async e=>{
    e.preventDefault();
    const termo = valorDe("oiTermo"), quem = valorDe("oiQuem"), data = valorDe("oiData") || hojeISO(), dias = Number(valorDe("oiPrazo") || CE_PRAZO_NOVA);
    if (termo.length < 30) return mostrarErros("#ceErrosOitiva", ["Escreva o termo com pelo menos 30 caracteres."]);
    await db.put("oitivas", {id: uuid(), denuncia_id: id, quem, data, termo, prazo_nova: cePrazo(dias), perfil: estado.perfil});
    const d = await db.get("denuncias", id);
    await db.put("denuncias", {...d, etapa: "deliberação"});
    await trilha("oitiva registrada (" + quem + ")", id);
    toast("Oitiva registrada."); navegar();
  });
};
