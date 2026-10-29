/* Comissão de Ética · código do app (o construir.py junta com a base comum) */
"use strict";
teste("Exemplo com 8 categorias e 10 casos", ()=>{ const s = dadosEmbutidos("seed"); return s.categorias.length === 8 && s.denuncias.length === 10; });

/* ================= Sprint 2 · Registro da denúncia ================= */
const ETAPAS_CE = ["registro", "classificação", "admissibilidade", "oitivas", "deliberação", "recomendações", "encerrado"];
const CANAIS = ["e-mail", "presencial", "ofício", "outro"];
const LIMITE_ANEXO_CE = 10 * 1024 * 1024;

// RN05: toda ação registra perfil, data, hora e, quando muda dado, a justificativa
async function trilha(acao, denuncia_id, justificativa=""){ await registrar(acao, {denuncia_id, justificativa}); }

async function novoProtocolo(){
  const ano = new Date().getFullYear(), usados = new Set((await db.list("denuncias")).map(d=>d.protocolo));
  let n = 1; while (usados.has(`CE-${ano}-${String(n).padStart(3, "0")}`)) n++;
  return `CE-${ano}-${String(n).padStart(3, "0")}`;
}

TELAS["#/painel"] = async ()=>{
  const ds = await db.list("denuncias");
  const porEtapa = ETAPAS_CE.map(e=>({e, lista: ds.filter(d=>d.etapa === e)}));
  return `<h1>Painel</h1><p class="sub">${ds.length} casos. <a href="#/denuncia/nova">Registrar denúncia</a></p>
    <div class="grade">${porEtapa.map(x=>`<div class="card kpi"><div class="v" data-etapa-qtd="${x.e}">${x.lista.length}</div><div class="r">${esc(x.e)}</div></div>`).join("")}</div>
    <div class="card tabela-wrap"><table><tr><th>Protocolo</th><th>Recebida em</th><th>Canal</th><th>Etapa</th><th>Situação</th></tr>
      ${ds.sort((a, b)=>b.data_recebimento.localeCompare(a.data_recebimento)).map(d=>`<tr><td><a href="#/caso/${encodeURIComponent(d.id)}">${esc(d.protocolo)}</a></td>
        <td>${dataCurtaBR(d.data_recebimento)}</td><td>${esc(d.canal)}</td><td><span class="selo info">${esc(d.etapa)}</span></td><td>${esc(d.situacao)}</td></tr>`).join("") || '<tr><td colspan="5" class="vazio">Nenhum caso.</td></tr>'}</table></div>`;
};

TELAS["#/denuncia/nova"] = async ()=> `<h1>Registrar denúncia</h1><p class="sub">Use apenas dados fictícios. O protocolo é gerado ao salvar.</p>
  <form class="card" id="formDenuncia"><div class="campos">
    ${campo("dCanal", "Canal de recebimento", {tipo: "select", opcoes: CANAIS})}
    ${campo("dData", "Data de recebimento", {tipo: "date", valor: hojeISO(), obrigatorio: true})}
    ${campo("dDenunciante", "Denunciante", {obrigatorio: true, ajuda: "Nome fictício."})}
    ${campo("dDenunciado", "Denunciado(a)", {obrigatorio: true, ajuda: "Nome fictício."})}</div>
    ${campo("dRelato", "Relato dos fatos", {tipo: "textarea", linhas: 6, obrigatorio: true, ajuda: "Transcreva o relato recebido. Mínimo de 50 caracteres."})}
    <div class="campo"><label for="dAnexos">Anexos (provas, prints, escalas), até 10 MB cada</label><input type="file" id="dAnexos" multiple></div>
    <div id="errosDenuncia"></div><div class="linha-botoes"><button class="prim" type="submit">Registrar</button></div></form>`;
TELAS_DEPOIS["#/denuncia/nova"] = ()=>{
  $("#formDenuncia").addEventListener("submit", async e=>{
    e.preventDefault();
    const d = {canal: valorDe("dCanal"), data_recebimento: valorDe("dData"), denunciante: valorDe("dDenunciante"), denunciado: valorDe("dDenunciado"), relato: valorDe("dRelato")};
    const arqs = Array.from($("#dAnexos").files), erros = [];
    if (!d.data_recebimento || d.data_recebimento > hojeISO()) erros.push("Informe a data de recebimento (não pode ser futura).");
    if (!d.denunciante) erros.push("Informe o denunciante.");
    if (!d.denunciado) erros.push("Informe o denunciado.");
    if (d.relato.length < 50) erros.push(`O relato precisa de pelo menos 50 caracteres; tem ${d.relato.length}.`);
    arqs.filter(a=>a.size > LIMITE_ANEXO_CE).forEach(a=>erros.push(`O anexo ${a.name} passa de 10 MB.`));
    if (!mostrarErros("#errosDenuncia", erros)) return;
    const protocolo = await novoProtocolo();
    await db.put("denuncias", {id: protocolo, protocolo, ...d, etapa: "registro", situacao: "aberto", sigilo: true, criado_em: agora()});
    for (const a of arqs) await db.put("anexos", {id: uuid(), denuncia_id: protocolo, nome: a.name, tipo: a.type, tamanho: a.size, conteudo: a});
    await trilha("denúncia registrada", protocolo);
    toast(`Denúncia ${protocolo} registrada.`); location.hash = "#/caso/" + encodeURIComponent(protocolo);
  });
};

TELAS["#/caso/:id"] = async ({id})=>{
  const d = await db.get("denuncias", id);
  if (!d) return `<div class="card vazio">Caso não encontrado. <a href="#/painel">Voltar</a></div>`;
  const anexos = await db.porIndice("anexos", "denuncia_id", id), hist = (await db.porIndice("log", "denuncia_id", id)).sort((a, b)=>a.data_hora.localeCompare(b.data_hora));
  return `<h1>Caso ${esc(d.protocolo)}</h1><p class="sub">Recebida em ${dataCurtaBR(d.data_recebimento)} por ${esc(d.canal)} · etapa <span class="selo info">${esc(d.etapa)}</span></p>
    <div class="linha-botoes"><a class="botao" href="#/caso/${encodeURIComponent(id)}/classificacao">Classificação</a>
      <a class="botao" href="#/caso/${encodeURIComponent(id)}/admissibilidade">Admissibilidade</a></div>
    <div class="card"><h2 style="margin-top:0">Partes (fictícias)</h2><p><b>Denunciante:</b> ${esc(d.denunciante)}<br><b>Denunciado(a):</b> ${esc(d.denunciado)}</p></div>
    <div class="card"><h2 style="margin-top:0">Relato</h2><p style="white-space:pre-wrap">${esc(d.relato)}</p></div>
    <div class="card"><h2 style="margin-top:0">Anexos (${anexos.length})</h2>${anexos.map(a=>`<p>${esc(a.nome)} · ${(a.tamanho / 1024).toFixed(0)} KB</p>`).join("") || '<p class="sub">Nenhum.</p>'}</div>
    <div class="card tabela-wrap"><h2 style="margin-top:0">Histórico (RN05)</h2><table id="historico"><tr><th>Data e hora</th><th>Perfil</th><th>Ação</th><th>Justificativa</th></tr>
      ${hist.map(h=>`<tr><td>${dataBR(h.data_hora)}</td><td>${esc(h.perfil)}</td><td>${esc(h.acao)}</td><td>${esc(h.justificativa || "")}</td></tr>`).join("")}</table></div>`;
};
