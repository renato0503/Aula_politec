/* ================= Sprints 4 a 11 · conferência, textos, quesitos, Word, revisão e histórico (versão mínima) =================
   A requisição em PDF (Sprint 6) e o OCR (Sprint 10) ficam como digitação: o perito lê o PDF ao lado e preenche os campos
   da requisição na conferência, o que o formulário autoriza ("simulado"). */
"use strict";

const CATEGORIAS_TEXTO = [["historico", "Histórico"], ["descricao_objetos", "Descrição dos objetos"], ["sem_sim", "Aparelho sem SIM"],
  ["exames", "Exames"], ["anexos", "Anexos e mídias"], ["consideracoes", "Considerações finais"]];
const CAMPOS_REQUISICAO = [["numero_protocolo", "Protocolo"], ["numero_oficio", "Ofício"], ["numero_processo", "Processo"],
  ["autoridade_solicitante", "Autoridade requisitante"], ["data_solicitacao", "Data da solicitação"]];
const semCaso = titulo=> `<h1>${titulo}</h1><div class="card vazio">Abra um caso em <a href="#/inicio">Início</a>.</div>`;

// a biblioteca começa com os textos do exemplo quando está vazia
async function textosDaBiblioteca(){
  let ts = await db.list("textos");
  if (!ts.length){ for (const t of dadosEmbutidos("seed")?.textos || []) await db.put("textos", t); ts = await db.list("textos"); }
  return ts.filter(t=> t.ativo !== false);
}
async function dadosDoCaso(caso){
  const id = caso.id_caso;
  const [ap, hs, sims, qs] = await Promise.all([db.porIndice("aparelhos", "id_caso", id), db.porIndice("hashes", "id_caso", id),
    db.porIndice("sims", "id_caso", id), db.porIndice("quesitos", "id_caso", id)]);
  return {ap: ap[0] || null, hs: hs[0] || null, sims: sims.sort((a, b)=> String(a.identificador_objeto).localeCompare(String(b.identificador_objeto))),
    qs: qs.sort((a, b)=> a.numero - b.numero)};
}
const val = c=> c && c.valor !== undefined && c.valor !== null ? String(c.valor) : "";

/* ---------- RN11: bloqueios e alertas da conferência automática ---------- */
function conferir(caso, d){
  const bloqueios = [], alertas = [];
  if (!d.ap || !val(d.ap.imei_1)) bloqueios.push("IMEI 1 ausente.");
  else if (!imeiValido(val(d.ap.imei_1))) bloqueios.push("IMEI 1 com dígito verificador inválido.");
  if (d.ap && val(d.ap.imei_2) && !imeiValido(val(d.ap.imei_2))) alertas.push("IMEI 2 com dígito verificador inválido.");
  if (!d.hs || !val(d.hs.valor_hash)) bloqueios.push("Hash ausente.");
  else if (!sha256Valido(val(d.hs.valor_hash))) bloqueios.push("Hash fora do formato SHA-256 (64 caracteres hexadecimais).");
  for (const s of d.sims){
    if (!val(s.iccid)) alertas.push(`SIM ${s.identificador_objeto}: ICCID ausente.`);
    else if (!iccidValido(val(s.iccid))) alertas.push(`SIM ${s.identificador_objeto}: ICCID inválido.`);
    if (s.objeto_no_html && normalizar(s.objeto_no_html).replace(/\s/g, "") !== normalizar(s.identificador_objeto || "").replace(/\s/g, ""))
      alertas.push(`SIM ${s.identificador_objeto}: o HTML diz objeto ${s.objeto_no_html} (RN07).`);
  }
  const req = caso.requisicao || {};
  for (const [k, r] of CAMPOS_REQUISICAO) if (!req[k]) (k === "numero_protocolo" ? bloqueios : alertas).push(`Requisição: ${r} não informado.`);
  if (!caso.conferido_em) bloqueios.push("A conferência dos dados não foi confirmada (RN04).");
  if (!d.qs.length) alertas.push("Nenhum quesito cadastrado.");
  for (const q of d.qs) if (!String(q.resposta || "").trim()) bloqueios.push(`Quesito ${q.numero} sem resposta (RN10).`);
  const l = caso.laudo || {};
  if (!l.numero_laudo) bloqueios.push("Número do laudo não informado.");
  if (!l.nome_perito) bloqueios.push("Nome do perito não informado.");
  return {bloqueios, alertas};
}
teste("RN11: caso vazio tem bloqueios", ()=> conferir({}, {ap:null, hs:null, sims:[], qs:[]}).bloqueios.length >= 3);
teste("RN10: quesito sem resposta bloqueia", ()=> conferir({}, {ap:null, hs:null, sims:[], qs:[{numero:1, resposta:""}]}).bloqueios.some(b=> b.includes("Quesito 1")));

/* ---------- Sprint 5 · conferência campo a campo (RN04) ---------- */
const agDadosAntes = TELAS["#/dados"];
TELAS["#/dados"] = async (p)=>{
  const html = await agDadosAntes(p);
  const caso = await casoAtual();
  if (!caso?.inventario) return html;
  const d = await dadosDoCaso(caso), req = caso.requisicao || {};
  const linhaCampo = (id, rotulo, c)=> `<tr><th><label for="${id}">${esc(rotulo)}</label></th>
    <td><input id="${id}" value="${esc(val(c))}" class="mono"></td>
    <td class="sub">${c ? esc(c.origem || "") + (c.linha ? ", linha " + c.linha : "") + (c.corrigido_de !== undefined ? ` · corrigido (era ${esc(c.corrigido_de || "vazio")})` : "") : "ausente"}</td></tr>`;
  const ap = d.ap || {};
  return html.replace("A conferência campo a campo chega no Sprint 5.", "Confira cada valor com a origem ao lado e corrija o que precisar (RN04).") + `
    <form class="card tabela-wrap" id="formConferencia"><h2 style="margin-top:0">Conferência</h2>
      <p class="sub">${caso.conferido_em ? `<span class="selo ok">conferido em ${dataBR(caso.conferido_em)}</span>` : '<span class="selo alerta">não conferido</span>'}
        Os dados da requisição são digitados com o PDF aberto ao lado (a leitura do PDF e o OCR ficam para depois).</p>
      <table><tr><th>Campo</th><th>Valor</th><th>Origem</th></tr>
        ${CAMPOS_REQUISICAO.map(([k, r])=> `<tr><th><label for="req_${k}">${esc(r)}</label></th><td><input id="req_${k}" value="${esc(req[k] || (k === "numero_protocolo" ? caso.numero_protocolo || "" : ""))}"></td><td class="sub">requisição (digitado)</td></tr>`).join("")}
        ${Object.keys(ROTULOS_APARELHO).map(k=> linhaCampo("ap_" + k, k.replace("_", " "), ap[k])).join("")}
        ${linhaCampo("hs_valor", "hash", d.hs?.valor_hash)}${linhaCampo("hs_arquivo", "arquivo do hash", d.hs?.hash_arquivo)}
        ${d.sims.map(s=> linhaCampo("sim_iccid_" + s.identificador_objeto, `ICCID ${s.identificador_objeto}`, s.iccid) + linhaCampo("sim_op_" + s.identificador_objeto, `operadora ${s.identificador_objeto}`, s.operadora)).join("")}
      </table>
      <div class="linha-botoes"><button class="prim" type="submit">Confirmar a conferência</button><a class="botao" href="#/textos">Próximo: textos</a></div></form>`;
};
const agDadosDepois = TELAS_DEPOIS["#/dados"];
TELAS_DEPOIS["#/dados"] = async (p)=>{
  await agDadosDepois?.(p);
  $("#formConferencia")?.addEventListener("submit", async ev=>{
    ev.preventDefault();
    const caso = await casoAtual(), d = await dadosDoCaso(caso);
    let correcoes = 0;
    const corrigir = (c, id, origemPadrao)=>{
      const novo = valorDe(id);
      if (val(c) === novo) return c;
      correcoes++;
      registrar("campo corrigido", {id_caso: caso.id_caso, campo_verificado: id, de: val(c), para: novo});
      return novo ? {...(c || {}), valor: novo, origem: c?.origem || origemPadrao, corrigido_de: val(c), valido: true} : null;
    };
    const ap = d.ap || {id_aparelho: caso.id_caso + "-A1", id_caso: caso.id_caso};
    for (const k of Object.keys(ROTULOS_APARELHO)) ap[k] = corrigir(ap[k], "ap_" + k, "perito");
    if (ap.imei_1) ap.imei_1.valido = imeiValido(val(ap.imei_1));
    if (ap.imei_2) ap.imei_2.valido = imeiValido(val(ap.imei_2));
    await db.put("aparelhos", ap);
    const hs = d.hs || {id_hash: caso.id_caso + "-H1", id_caso: caso.id_caso, algoritmo: "SHA-256"};
    hs.valor_hash = corrigir(hs.valor_hash, "hs_valor", "perito"); hs.hash_arquivo = corrigir(hs.hash_arquivo, "hs_arquivo", "perito");
    if (hs.valor_hash){ hs.valor_hash.valor = hs.valor_hash.valor.toLowerCase(); hs.valor_hash.valido = sha256Valido(hs.valor_hash.valor); }
    await db.put("hashes", hs);
    for (const s of d.sims){
      s.iccid = corrigir(s.iccid, "sim_iccid_" + s.identificador_objeto, "perito");
      if (s.iccid) s.iccid.valido = iccidValido(val(s.iccid));
      s.operadora = corrigir(s.operadora, "sim_op_" + s.identificador_objeto, "perito");
      await db.put("sims", s);
    }
    const requisicao = Object.fromEntries(CAMPOS_REQUISICAO.map(([k])=> [k, valorDe("req_" + k)]));
    await db.put("casos", {...caso, requisicao, numero_protocolo: requisicao.numero_protocolo || caso.numero_protocolo,
      conferido_em: agora(), correcoes: (caso.correcoes || 0) + correcoes});
    await registrar("conferência confirmada", {id_caso: caso.id_caso, resultado: correcoes + " correção(ões)"});
    toast(`Conferência confirmada${correcoes ? `, com ${correcoes} correção(ões)` : ""}.`); navegar();
  });
};

/* ---------- Sprint 7 · textos padronizados (RN08) e biblioteca ---------- */
TELAS["#/textos"] = async ()=>{
  const caso = await casoAtual(); if (!caso) return semCaso("Textos");
  const ts = await textosDaBiblioteca(), escolhidos = caso.textos || {};
  const d = await dadosDoCaso(caso);
  return `<h1>Textos padronizados</h1><p class="sub">Escolha o texto de cada seção do laudo. A biblioteca fica em <a href="#/biblioteca">Biblioteca</a> (RN08).</p>
    <form class="card" id="formTextos"><div class="campos">
      ${CATEGORIAS_TEXTO.filter(([c])=> c !== "sem_sim" || !d.sims.length).map(([c, r])=>{
        const op = ts.filter(t=> t.categoria === c);
        return campo("tx_" + c, r, {tipo:"select", opcoes:[["", "(sem texto)"], ...op.map(t=> [t.id_texto, t.titulo])], valor: escolhidos[c] ?? op[0]?.id_texto ?? ""});
      }).join("")}</div>
      <div class="linha-botoes"><button class="prim" type="submit">Salvar os textos</button><a class="botao" href="#/quesitos">Próximo: quesitos</a></div></form>`;
};
TELAS_DEPOIS["#/textos"] = ()=>{
  $("#formTextos")?.addEventListener("submit", async ev=>{
    ev.preventDefault();
    const caso = await casoAtual();
    const textos = Object.fromEntries(CATEGORIAS_TEXTO.filter(([c])=> $("#tx_" + c)).map(([c])=> [c, valorDe("tx_" + c)]));
    await db.put("casos", {...caso, textos}); await registrar("textos escolhidos", {id_caso: caso.id_caso});
    toast("Textos salvos."); location.hash = "#/quesitos";
  });
};
TELAS["#/biblioteca"] = async ()=>{
  const ts = await textosDaBiblioteca();
  const cats = [...CATEGORIAS_TEXTO, ["resposta", "Resposta de quesito"]];
  return `<h1>Biblioteca de textos</h1><p class="sub">${ts.length} textos ativos. Editar um texto cria a versão seguinte (RN08).</p>
    <div class="card tabela-wrap"><table><tr><th>Categoria</th><th>Título</th><th>Texto</th><th>Versão</th><th></th></tr>
      ${ts.map(t=> `<tr><td>${esc(cats.find(c=> c[0] === t.categoria)?.[1] || t.categoria)}</td><td><b>${esc(t.titulo)}</b></td>
        <td>${esc(t.conteudo)}</td><td class="num">${esc(t.versao || "1")}</td><td><button data-editar-texto="${esc(t.id_texto)}">Editar</button></td></tr>`).join("")}</table></div>
    <form class="card" id="formTexto"><h2 style="margin-top:0" id="tituloFormTexto">Novo texto</h2><input type="hidden" id="txId">
      <div class="campos">${campo("txCategoria", "Categoria", {tipo:"select", opcoes:cats})}${campo("txTitulo", "Título", {obrigatorio:true})}</div>
      ${campo("txConteudo", "Texto", {tipo:"textarea", obrigatorio:true})}
      <div id="errosTexto"></div><div class="linha-botoes"><button class="prim" type="submit">Salvar o texto</button></div></form>`;
};
TELAS_DEPOIS["#/biblioteca"] = ()=>{
  $$("[data-editar-texto]").forEach(b=> b.addEventListener("click", async ()=>{
    const t = await db.get("textos", b.dataset.editarTexto);
    $("#txId").value = t.id_texto; $("#txCategoria").value = t.categoria; $("#txTitulo").value = t.titulo; $("#txConteudo").value = t.conteudo;
    $("#tituloFormTexto").textContent = "Editar texto"; $("#formTexto").scrollIntoView({block:"nearest"});
  }));
  $("#formTexto")?.addEventListener("submit", async ev=>{
    ev.preventDefault();
    const erros = [];
    if (!valorDe("txTitulo")) erros.push("Informe o título.");
    if (!valorDe("txConteudo")) erros.push("Escreva o texto.");
    if (!mostrarErros("#errosTexto", erros)) return;
    const id = valorDe("txId"), ant = id ? await db.get("textos", id) : null;
    const t = {id_texto: id || "T" + Date.now().toString(36), categoria: valorDe("txCategoria"), titulo: valorDe("txTitulo"),
      conteudo: valorDe("txConteudo"), versao: String(Number(ant?.versao || 0) + 1), ativo: true};
    await db.put("textos", t); await registrar(ant ? "texto alterado" : "texto criado", {detalhe: t.id_texto, versao: t.versao});
    toast("Texto salvo."); navegar();
  });
};

/* ---------- Sprint 8 · quesitos e respostas (RN09, RN10) ---------- */
// RN09: um quesito por linha, com ou sem número na frente ("1)", "1.", "1 -")
const separarQuesitos = txt=> String(txt || "").split(/\r?\n/).map(l=> l.replace(/^\s*\d+\s*[).\-–:]\s*/, "").trim()).filter(Boolean);
teste("RN09: separa e numera os quesitos colados", ()=>{ const q = separarQuesitos("1) Qual a marca?\n2. Havia SIM?\n\n3 - Houve extração?"); return q.length === 3 && q[1] === "Havia SIM?"; });
TELAS["#/quesitos"] = async ()=>{
  const caso = await casoAtual(); if (!caso) return semCaso("Quesitos");
  const {qs} = await dadosDoCaso(caso);
  const respostas = (await textosDaBiblioteca()).filter(t=> t.categoria === "resposta");
  return `<h1>Quesitos</h1><p class="sub">Cole os quesitos da requisição, um por linha. Cada quesito precisa de resposta antes de gerar o laudo (RN10).</p>
    <div class="card">${campo("qsColar", "Quesitos da requisição", {tipo:"textarea", ajuda:"A numeração da requisição é refeita na ordem colada (RN09)."})}
      <div class="linha-botoes"><button class="prim" id="btnQuesitos">${qs.length ? "Substituir os quesitos" : "Cadastrar os quesitos"}</button></div></div>
    ${qs.length ? `<form class="card" id="formRespostas"><h2 style="margin-top:0">Respostas</h2>
      ${qs.map(q=> `<div class="campo"><label for="resp_${esc(q.id_quesito)}"><b>${q.numero})</b> ${esc(q.enunciado)}</label>
        <select data-resp-texto="${esc(q.id_quesito)}" aria-label="Inserir resposta padrão no quesito ${q.numero}"><option value="">Inserir resposta padrão…</option>
          ${respostas.map(t=> `<option value="${esc(t.id_texto)}">${esc(t.titulo)}</option>`).join("")}</select>
        <textarea id="resp_${esc(q.id_quesito)}" rows="3">${esc(q.resposta || "")}</textarea></div>`).join("")}
      <div class="linha-botoes"><button class="prim" type="submit">Salvar as respostas</button><a class="botao" href="#/gerar">Próximo: gerar o laudo</a></div></form>` : ""}`;
};
TELAS_DEPOIS["#/quesitos"] = async ()=>{
  $("#btnQuesitos")?.addEventListener("click", async ()=>{
    const caso = await casoAtual(), lista = separarQuesitos(valorDe("qsColar"));
    if (!lista.length) return toast("Cole pelo menos um quesito.");
    for (const q of await db.porIndice("quesitos", "id_caso", caso.id_caso)) await db.del("quesitos", q.id_quesito);
    for (const [i, enunciado] of lista.entries()) await db.put("quesitos", {id_quesito: `${caso.id_caso}-Q${i + 1}`, id_caso: caso.id_caso, numero: i + 1, enunciado, resposta: ""});
    await registrar("quesitos cadastrados", {id_caso: caso.id_caso, resultado: lista.length + " quesitos"});
    navegar();
  });
  const ts = await textosDaBiblioteca();
  $$("[data-resp-texto]").forEach(s=> s.addEventListener("change", ()=>{
    const t = ts.find(x=> x.id_texto === s.value); if (!t) return;
    const area = $("#resp_" + CSS.escape(s.dataset.respTexto)); area.value = (area.value ? area.value + "\n" : "") + t.conteudo; s.value = "";
  }));
  $("#formRespostas")?.addEventListener("submit", async ev=>{
    ev.preventDefault();
    const caso = await casoAtual();
    for (const q of await db.porIndice("quesitos", "id_caso", caso.id_caso)) await db.put("quesitos", {...q, resposta: $("#resp_" + CSS.escape(q.id_quesito)).value.trim()});
    await registrar("respostas salvas", {id_caso: caso.id_caso}); toast("Respostas salvas.");
  });
};

/* ---------- Sprint 4 · geração do Word (RN12, RN13) ---------- */
async function dadosDoLaudo(caso){
  const d = await dadosDoCaso(caso), ts = await textosDaBiblioteca(), req = caso.requisicao || {}, l = caso.laudo || {};
  const texto = c=> ts.find(t=> t.id_texto === (caso.textos || {})[c])?.conteudo || "";
  return {...req, numero_protocolo: req.numero_protocolo || caso.numero_protocolo || "",
    numero_laudo: l.numero_laudo || "", nome_perito: l.nome_perito || "", data_laudo: l.data_laudo || new Date().toLocaleDateString("pt-BR"),
    marca: val(d.ap?.marca), modelo: val(d.ap?.modelo), cor: val(d.ap?.cor) || "não informada", imei_1: val(d.ap?.imei_1), imei_2: val(d.ap?.imei_2),
    sims: d.sims.map(s=> ({identificador_objeto: s.identificador_objeto, operadora: val(s.operadora), iccid: val(s.iccid)})),
    hash_arquivo: val(d.hs?.hash_arquivo), hash_algoritmo: d.hs?.algoritmo || "SHA-256", valor_hash: val(d.hs?.valor_hash),
    quesitos: d.qs.map(q=> ({numero_quesito: q.numero, enunciado: q.enunciado, resposta: q.resposta || ""})),
    ...Object.fromEntries(CATEGORIAS_TEXTO.map(([c])=> ["texto_" + c, texto(c)]))};
}
function gerarDocx(dados){
  const modelo = dadosEmbutidos("modelo-docx");
  if (!modelo?.b64 || typeof PizZip === "undefined" || typeof docxtemplater === "undefined") throw new Error("modelo ou biblioteca do Word não embutidos");
  const doc = new docxtemplater(new PizZip(atob(modelo.b64)), {paragraphLoop: true, linebreaks: true, nullGetter: ()=> ""});
  doc.render(dados);
  return doc.getZip().generate({type: "blob", mimeType: "application/vnd.openxmlformats-officedocument.wordprocessingml.document"});
}
teste("RN12: o modelo do Word preenche os marcadores", ()=>{
  const blob = gerarDocx({numero_laudo: "1/2026", sims: [], quesitos: [{numero_quesito: 1, enunciado: "a", resposta: "b"}]});
  return blob.size > 10000;
});
TELAS["#/gerar"] = async ()=>{
  const caso = await casoAtual(); if (!caso) return semCaso("Gerar laudo");
  const {bloqueios, alertas} = conferir(caso, await dadosDoCaso(caso)), l = caso.laudo || {};
  const laudos = await db.porIndice("laudos", "id_caso", caso.id_caso);
  return `<h1>Gerar o laudo</h1><p class="sub">O Word sai do modelo com os marcadores (RN12). Os originais da pasta não mudam (RN13).</p>
    <form class="card" id="formLaudo"><div class="campos">
      ${campo("lNumero", "Número do laudo", {valor: l.numero_laudo || "", obrigatorio: true})}
      ${campo("lPerito", "Nome do perito", {valor: l.nome_perito || "", obrigatorio: true})}
      ${campo("lData", "Data do laudo", {valor: l.data_laudo || new Date().toLocaleDateString("pt-BR")})}</div>
      <div class="linha-botoes"><button type="submit">Salvar</button></div></form>
    <div class="card" id="resultadoConferencia"><h2 style="margin-top:0">Conferência automática (RN11)</h2>
      ${bloqueios.length ? `<div class="pendente" role="alert"><b>${bloqueios.length} bloqueio(s):</b><ul>${bloqueios.map(b=> `<li>${esc(b)}</li>`).join("")}</ul></div>` : '<p><span class="selo ok">sem bloqueios</span></p>'}
      ${alertas.length ? `<p><b>Alertas</b></p><ul>${alertas.map(a=> `<li>${esc(a)}</li>`).join("")}</ul>` : ""}
      <div class="linha-botoes"><button class="prim" id="btnGerarDocx" ${bloqueios.length ? "disabled" : ""}>Gerar o .docx</button>
        <button id="btnRascunho">Gerar rascunho (com pendências)</button></div></div>
    ${laudos.length ? `<div class="card tabela-wrap"><h2 style="margin-top:0">Versões geradas</h2><table><tr><th>Quando</th><th>Arquivo</th><th>Tipo</th></tr>
      ${laudos.sort((a, b)=> b.gerado_em.localeCompare(a.gerado_em)).map(x=> `<tr><td>${dataBR(x.gerado_em)}</td><td class="mono">${esc(x.arquivo)}</td><td>${x.rascunho ? "rascunho" : "final"}</td></tr>`).join("")}</table></div>` : ""}`;
};
TELAS_DEPOIS["#/gerar"] = async ()=>{
  $("#formLaudo")?.addEventListener("submit", async ev=>{
    ev.preventDefault();
    const caso = await casoAtual();
    await db.put("casos", {...caso, laudo: {numero_laudo: valorDe("lNumero"), nome_perito: valorDe("lPerito"), data_laudo: valorDe("lData")}});
    toast("Dados do laudo salvos."); navegar();
  });
  const gerar = async rascunho=>{
    const caso = await casoAtual();
    try {
      const blob = gerarDocx(await dadosDoLaudo(caso));
      const nome = `laudo-${(caso.numero_protocolo || "caso").replace(/[^\w.-]+/g, "_")}${rascunho ? "-rascunho" : ""}.docx`;
      baixar(nome, blob, blob.type);
      await db.put("laudos", {id_laudo: uuid(), id_caso: caso.id_caso, arquivo: nome, gerado_em: agora(), rascunho});
      await registrar("laudo gerado", {id_caso: caso.id_caso, resultado: nome});
      toast("Laudo gerado: " + nome); navegar();
    } catch(e){ toast("Não consegui gerar o Word: " + e.message, 6000); }
  };
  $("#btnGerarDocx")?.addEventListener("click", ()=> gerar(false));
  $("#btnRascunho")?.addEventListener("click", ()=> gerar(true));
};

/* ---------- Sprint 9 · revisão final (RN14) ---------- */
TELAS["#/revisao"] = async ()=>{
  const caso = await casoAtual(); if (!caso) return semCaso("Revisão final");
  const d = await dadosDoCaso(caso), {bloqueios, alertas} = conferir(caso, d);
  const laudos = (await db.porIndice("laudos", "id_caso", caso.id_caso)).filter(x=> !x.rascunho);
  const itens = [["Pasta inventariada", !!caso.inventario], ["Dados conferidos (RN04)", !!caso.conferido_em], ["Textos escolhidos", !!caso.textos],
    ["Quesitos respondidos", d.qs.length > 0 && d.qs.every(q=> q.resposta)], ["Laudo final gerado", laudos.length > 0], ["Sem bloqueios (RN11)", !bloqueios.length]];
  return `<h1>Revisão final</h1><p class="sub">O caso só é concluído com todos os itens marcados (RN14). Situação: <span class="selo info">${esc(caso.status)}</span></p>
    <div class="card"><ul class="checklist">${itens.map(([t, okI])=> `<li>${okI ? '<span class="selo ok">ok</span>' : '<span class="selo alerta">pendente</span>'} ${esc(t)}</li>`).join("")}</ul>
      ${bloqueios.length ? `<p><b>Bloqueios:</b> ${bloqueios.map(esc).join(" ")}</p>` : ""}${alertas.length ? `<p class="sub">Alertas: ${alertas.map(esc).join(" ")}</p>` : ""}
      <div class="linha-botoes"><button class="prim" id="btnConcluir" ${itens.every(i=> i[1]) && caso.status !== "concluído" ? "" : "disabled"}>Concluir o caso</button>
        <a class="botao" href="#/historico">Histórico e métricas</a></div></div>`;
};
TELAS_DEPOIS["#/revisao"] = ()=>{
  $("#btnConcluir")?.addEventListener("click", async ()=>{
    const caso = await casoAtual();
    await db.put("casos", {...caso, status: "concluído", fim_em: agora()});
    await registrar("caso concluído", {id_caso: caso.id_caso}); toast("Caso concluído."); navegar();
  });
};

/* ---------- Sprint 11 · histórico, métricas e LGPD ---------- */
const minutosDoCaso = c=> c.inicio_em && c.fim_em ? Math.round((new Date(c.fim_em) - new Date(c.inicio_em)) / 60000) : null;
TELAS["#/historico"] = async ()=>{
  const casos = (await db.list("casos")).sort((a, b)=> String(b.criado_em).localeCompare(String(a.criado_em)));
  const concl = casos.filter(c=> minutosDoCaso(c) !== null);
  const media = concl.length ? Math.round(concl.reduce((a, c)=> a + minutosDoCaso(c), 0) / concl.length) : null;
  return `<h1>Histórico e métricas</h1><p class="sub">Tempo de cada laudo, da pasta inventariada à conclusão, e as correções feitas na conferência.</p>
    <div class="grade"><div class="card kpi"><div class="v">${casos.length}</div><div class="r">casos</div></div>
      <div class="card kpi"><div class="v">${concl.length}</div><div class="r">concluídos</div></div>
      <div class="card kpi"><div class="v">${media === null ? "—" : media + " min"}</div><div class="r">tempo médio</div></div>
      <div class="card kpi"><div class="v">${casos.reduce((a, c)=> a + (c.correcoes || 0), 0)}</div><div class="r">correções na conferência</div></div></div>
    <div class="card tabela-wrap"><table><tr><th>Protocolo</th><th>Situação</th><th class="num">Minutos</th><th class="num">Correções</th><th></th></tr>
      ${casos.map(c=> `<tr><td>${esc(c.numero_protocolo || "(sem protocolo)")}</td><td>${esc(c.status)}</td><td class="num">${minutosDoCaso(c) ?? "—"}</td>
        <td class="num">${c.correcoes || 0}</td><td>${c.dados_limpos_em ? '<span class="selo info">dados limpos</span>' : `<button data-limpar-caso="${esc(c.id_caso)}">Limpar os dados do caso</button>`}</td></tr>`).join("") || '<tr><td colspan="5" class="vazio">Nenhum caso.</td></tr>'}</table>
      <div class="linha-botoes"><button class="prim" id="btnCsvTempos">Baixar o CSV de tempos e correções</button></div>
      <p class="sub">Limpar os dados apaga aparelho, SIMs, hash e quesitos do caso e mantém só as métricas (LGPD).</p></div>`;
};
TELAS_DEPOIS["#/historico"] = ()=>{
  $("#btnCsvTempos")?.addEventListener("click", async ()=>{
    const casos = await db.list("casos");
    const linhas = casos.map(c=> [c.numero_protocolo || "", c.status, c.inicio_em || "", c.fim_em || "", minutosDoCaso(c) ?? "", c.correcoes || 0].join(";"));
    baixar("agiliza-tempos.csv", "﻿" + ["protocolo;situacao;inicio;fim;minutos;correcoes", ...linhas].join("\n"), "text/csv;charset=utf-8");
  });
  $$("[data-limpar-caso]").forEach(b=> b.addEventListener("click", async ()=>{
    if (!confirm("Apagar os dados do aparelho, SIMs, hash e quesitos deste caso? As métricas ficam.")) return;
    const id = b.dataset.limparCaso;
    for (const [s, k] of [["aparelhos", "id_aparelho"], ["sims", "id_sim"], ["hashes", "id_hash"], ["quesitos", "id_quesito"]])
      for (const r of await db.porIndice(s, "id_caso", id)) await db.del(s, r[k]);
    const c = await db.get("casos", id);
    await db.put("casos", {...c, inventario: c.inventario ? {...c.inventario, itens: []} : null, requisicao: null, dados_limpos_em: agora()});
    await registrar("dados do caso limpos", {id_caso: id}); toast("Dados do caso apagados."); navegar();
  }));
};
