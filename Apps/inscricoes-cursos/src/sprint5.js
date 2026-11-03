/* ================= Sprints 7 e 8 · convocação, turma, indicadores e LGPD ================= */
"use strict";

/* ================= Sprint 7 · Convocação (RN06, RN07, RN08) ================= */
async function listaDeConvocacao(curso){
  const [triagens, insc, convocacoes] = await Promise.all([
    db.porIndice("triagens", "curso_id", curso), db.porIndice("inscricoes", "curso_id", curso), db.list("convocacoes")]);
  const c = await db.get("cursos", curso);
  const dirs = Object.keys(c?.vagas_por_diretoria || {});
  const saida = [];
  for (const dir of dirs){
    const tri = triagens.find(t=> t.diretoria === dir);
    if (!tri) continue;
    const ordem = [...(tri.ordem || []), ...(tri.titulares || []), ...(tri.reservas || [])];
    const tit = (tri.titulares || []).filter(p=> ordem.includes(p));
    const res = (tri.reservas || []).filter(p=> ordem.includes(p));
    // RN06: a efetivação segue a ordem de indicação da diretoria
    tit.forEach((p, i)=> saida.push({protocolo:p, inscricao:insc.find(x=> x.protocolo === p), diretoria:dir, tipo:"titular", ordem:i + 1, tri}));
    res.forEach((p, i)=> saida.push({protocolo:p, inscricao:insc.find(x=> x.protocolo === p), diretoria:dir, tipo:"reserva", ordem:i + 1, tri}));
  }
  for (const l of saida){
    l.conv = convocacoes.find(x=> x.protocolo === l.protocolo) || null;
    l.status = l.conv ? l.conv.status : "pendente";
    // RN08: o link do grupo só vai para o titular e para a reserva já chamada
    l.chamada = l.tipo === "titular" || l.status === "chamada";
  }
  return saida;
}

function mensagemConvocacao(c, l){
  const link = l.chamada && c.link_grupo ? `\n\nLink do grupo da turma: ${c.link_grupo}` : "";
  const reserva = l.tipo === "reserva" ? "\nVocê está na lista de reserva. O link do grupo entra quando houver chamação." : "";
  return `Assunto: Convocação — ${c.nome} (${periodo(c)})

Prezado(a) ${l.inscricao?.nome || ""},

Informamos a sua convocação para o curso ${c.nome}, com carga horária de ${c.carga_horaria} h, de ${periodo(c)}, em ${c.local}.

Protocolo da inscrição: ${l.protocolo}
${reserva}${link}

Confirme a presença respondendo este e-mail.

Gerência de Formação Inicial e Continuada`;
}

TELAS["#/convocacao/:curso"] = async ({curso})=>{
  const c = await db.get("cursos", curso);
  if (!c) return `<div class="card vazio">Curso não encontrado. <a href="#/cursos">Voltar</a></div>`;
  const lista = await listaDeConvocacao(curso);
  const enviados = lista.filter(l=> ["enviada", "confirmou"].includes(l.status)).length;
  const confirmados = lista.filter(l=> l.status === "confirmou").length;
  const desistiu = lista.filter(l=> l.status === "desistiu");
  const linha = l=> `<tr data-conv="${esc(l.protocolo)}">
    <td class="num">${l.ordem}</td><td><b>${esc(l.inscricao?.nome || "—")}</b><br><span class="sub mono">${esc(l.protocolo)}</span></td>
    <td>${esc(l.diretoria)}</td><td>${l.tipo === "titular" ? '<span class="selo ok">titular</span>' : '<span class="selo info">reserva</span>'}</td>
    <td>${l.status === "confirmou" ? '<span class="selo ok">confirmou</span>' : l.status === "desistiu" ? '<span class="selo erro">desistiu</span>'
      : l.status === "enviada" ? '<span class="selo info">convocação enviada</span>' : l.status === "chamada" ? '<span class="selo alerta">reserva chamada</span>'
      : '<span class="selo">pendente</span>'}</td>
    <td class="nao-imprimir"><button data-mail="${esc(l.protocolo)}">E-mail</button> <button data-copiar="${esc(l.protocolo)}">Copiar</button>
      <button data-enviada="${esc(l.protocolo)}">Marcar enviada</button> <button data-confirmou="${esc(l.protocolo)}">Confirmou</button>
      ${l.tipo === "titular" ? `<button data-desistiu="${esc(l.protocolo)}">Desistiu</button>` : ""}
      ${l.tipo === "reserva" ? `<button data-chamar="${esc(l.protocolo)}">Chamar da reserva</button>` : ""}</td></tr>`;
  return `<h1>Convocação · ${esc(c.nome)}</h1><p class="sub">${periodo(c)} · a efetivação segue a ordem de indicação da diretoria (RN06). O link do grupo só vai para o titular e para a reserva chamada (RN08).</p>
    <p class="linha-botoes"><a class="botao" href="#/inscritos/${encodeURIComponent(c.id)}">Inscritos</a>
      <a class="botao" href="#/turma/${encodeURIComponent(c.id)}">Turma</a></p>
    <div class="grade"><div class="card kpi"><div class="v">${lista.length}</div><div class="r">convocados</div></div>
      <div class="card kpi"><div class="v">${enviados}</div><div class="r">convocações enviadas</div></div>
      <div class="card kpi"><div class="v">${confirmados}</div><div class="r">confirmaram presença</div></div>
      <div class="card kpi"><div class="v">${desistiu.length}</div><div class="r">desistências</div></div></div>
    ${desistiu.length ? `<div class="card pendente"><b>${desistiu.length} desistência(s).</b> Chame o próximo da reserva da mesma diretoria (RN07). Se não houver reserva, a vaga volta para a gerência.</div>` : ""}
    <div class="card tabela-wrap"><h2>Convocação por ordem</h2><table id="tabelaConvocacao"><tr><th class="num">Ordem</th><th>Servidor</th><th>Diretoria</th><th>Tipo</th><th>Situação</th><th class="nao-imprimir">Ações</th></tr>
      ${lista.map(linha).join("") || '<tr><td colspan="6" class="vazio">Nenhuma decisão de diretoria recebida ainda.</td></tr>'}</table></div>`;
};
TELAS_DEPOIS["#/convocacao/:curso"] = async ({curso})=>{
  if (!$("#tabelaConvocacao")) return;
  const c = await db.get("cursos", curso);
  const lista = await listaDeConvocacao(curso);
  const porProtocolo = new Map(lista.map(l=> [l.protocolo, l]));
  const marcar = async (protocolo, dados, acao)=>{
    const l = porProtocolo.get(protocolo);
    const anterior = l.conv ? l.conv.status : "pendente";
    await db.put("convocacoes", {id:protocolo, protocolo, curso_id:curso, diretoria:l.diretoria, tipo:l.tipo,
      ...(l.conv || {}), ...dados, status:dados.status || l.status, atualizado_em:agora()});
    await registrar(acao, {curso_id:curso, protocolo, situacao_anterior:anterior, situacao_nova:dados.status || l.status});
    navegar();
  };
  $$("[data-mail]").forEach(b=> b.addEventListener("click", ()=>{
    const l = porProtocolo.get(b.dataset.mail), corpo = mensagemConvocacao(c, l);
    const assunto = `[CONVOCACAO] ${c.nome} ${l.protocolo}`;
    location.href = `mailto:${encodeURIComponent(l.inscricao?.email || "")}?subject=${encodeURIComponent(assunto)}&body=${encodeURIComponent(corpo)}`;
  }));
  $$("[data-copiar]").forEach(b=> b.addEventListener("click", async ()=>{
    const l = porProtocolo.get(b.dataset.copiar);
    try { await navigator.clipboard.writeText(mensagemConvocacao(c, l)); toast("Mensagem copiada."); }
    catch(e){ toast("Selecione e copie com Ctrl+C."); }
  }));
  $$("[data-enviada]").forEach(b=> b.addEventListener("click", ()=> marcar(b.dataset.enviada, {status:"enviada", enviada_em:agora()}, "convocação enviada")));
  $$("[data-confirmou]").forEach(b=> b.addEventListener("click", ()=> marcar(b.dataset.confirmou, {status:"confirmou", confirmada_em:agora()}, "presença confirmada")));
  $$("[data-desistiu]").forEach(b=> b.addEventListener("click", ()=> marcar(b.dataset.desistiu, {status:"desistiu", desistiu_em:agora()}, "desistência registrada")));
  $$("[data-chamar]").forEach(b=> b.addEventListener("click", async ()=>{
    // RN07: a desistência de um titular chama o próximo da reserva da mesma diretoria
    const desistidos = lista.filter(l=> l.tipo === "titular" && l.status === "desistiu");
    const l = porProtocolo.get(b.dataset.chamar);
    if (!desistidos.some(d=> d.diretoria === l.diretoria)){
      await registrar("chamada de reserva sem desistência na mesma diretoria", {curso_id:curso, protocolo:l.protocolo});
      return toast("Não há titular desistido nesta diretoria para trocar.");
    }
    await marcar(l.protocolo, {status:"chamada", chamada_em:agora()}, "reserva chamada");
  }));
};

/* ================= Sprint 8 · Turma, indicadores e LGPD (RN08) ================= */
function csvTexto(cabecalho, linhas){
  const celula = v=> `"${String(v ?? "").replace(/"/g, '""')}"`;
  return "﻿" + [cabecalho, ...linhas].map(l=> l.map(celula).join(";")).join("\r\n");
}

TELAS["#/turma/:curso"] = async ({curso})=>{
  const c = await db.get("cursos", curso);
  if (!c) return `<div class="card vazio">Curso não encontrado. <a href="#/cursos">Voltar</a></div>`;
  const [insc, lista, log] = await Promise.all([
    db.porIndice("inscricoes", "curso_id", curso), listaDeConvocacao(curso), db.list("log")]);
  const confirmados = lista.filter(l=> l.status === "confirmou" || (l.tipo === "titular" && l.status !== "desistiu"));
  const desistidos = lista.filter(l=> l.status === "desistiu");
  const horas = (fim, inicio)=> fim && inicio ? Math.max(0, Math.round((new Date(fim) - new Date(inicio)) / 86400000)) : null;
  const fimLista = confirmados.find(l=> l.conv?.atualizado_em)?.conv?.atualizado_em || "";
  const tempoLista = horas(fimLista, c.criado_em);
  const exportacoes = log.filter(x=> x.acao === "arquivo de triagem exportado" && x.curso_id === curso);
  const correcoes = log.filter(x=> x.acao === "inscrição corrigida pela gerência" && x.curso_id === curso);
  const triagens = await db.porIndice("triagens", "curso_id", curso);
  const esperas = triagens.map(t=>{
    const exp = exportacoes.filter(x=> x.diretoria === t.diretoria).map(x=> x.data_hora).sort().pop();
    return exp && t.decidido_em ? horas(t.decidido_em, exp) : null;
  }).filter(x=> x !== null);
  const esperaMedia = esperas.length ? Math.round(esperas.reduce((a, b)=>a + b, 0) / esperas.length) : null;
  const vagas = totalVagas(c), ociosas = Math.max(0, vagas - confirmados.length);
  const encerradoHa = c.fim ? Math.round((Date.now() - new Date(c.fim + "T00:00:00").getTime()) / 86400000) : 0;
  const retencao = encerradoHa > 30;
  const cabecalho = ["Protocolo", "Matrícula", "Nome", "Diretoria", "Lotação", "E-mail", "Situação"];
  const linhas = confirmados.map(l=> [l.protocolo, l.inscricao?.matricula || "", l.inscricao?.nome || "", l.diretoria,
    l.inscricao?.lotacao || "", l.inscricao?.email || "", l.status]);
  const kpi = (v, r)=> `<div class="card kpi"><div class="v">${v}</div><div class="r">${esc(r)}</div></div>`;
  return `<h1>Turma · ${esc(c.nome)}</h1><p class="sub">${periodo(c)} · ${confirmados.length} confirmados de ${vagas} vagas.</p>
    <p class="linha-botoes"><a class="botao" href="#/convocacao/${encodeURIComponent(c.id)}">Convocação</a>
      <a class="botao" href="#/inscritos/${encodeURIComponent(c.id)}">Inscritos</a></p>
    <div class="grade">
      ${kpi(tempoLista === null ? "—" : tempoLista + " dias", "tempo até a lista final")}
      ${kpi(esperaMedia === null ? "—" : esperaMedia + " h", "espera pela indicação")}
      ${kpi(insc.length ? numBR(correcoes.length / insc.length * 100, 1) + "%" : "0%", "inscrições corrigidas")}
      ${kpi(ociosas, "vagas ociosas")}
    </div>
    ${retencao ? `<div class="card pendente" id="avisoRetencao"><b>Curso encerrado há ${encerradoHa} dias.</b> Os dados dos inscritos devem ser apagados (RN08).
      <div class="linha-botoes nao-imprimir"><button class="prim" id="btnLimpar">Apagar os dados deste curso</button></div></div>` : ""}
    <div class="card"><h2 style="margin-top:0">Lista final</h2>
      <p class="sub">${linhas.length} pessoas. O arquivo sai em CSV, com BOM e ponto e vírgula, como a planilha da equipe.</p>
      <div class="linha-botoes nao-imprimir"><button class="prim" id="btnCsv" ${linhas.length ? "" : "disabled"}>Baixar lista final (CSV)</button></div></div>
    <div class="card tabela-wrap"><h2>Confirmados</h2><table><tr><th>Protocolo</th><th>Matrícula</th><th>Nome</th><th>Diretoria</th><th>Situação</th></tr>
      ${linhas.map(l=> `<tr><td class="mono">${esc(l[0])}</td><td>${esc(l[1])}</td><td>${esc(l[2])}</td><td>${esc(l[3])}</td><td>${esc(l[6])}</td></tr>`).join("")
        || '<tr><td colspan="5" class="vazio">Nenhum confirmado ainda.</td></tr>'}</table></div>
    ${desistidos.length ? `<div class="card"><h2 style="margin-top:0">Desistências</h2>
      <ul>${desistidos.map(l=> `<li>${esc(l.inscricao?.nome || l.protocolo)} (${esc(l.diretoria)})</li>`).join("")}</ul></div>` : ""}`;
};
TELAS_DEPOIS["#/turma/:curso"] = async ({curso})=>{
  const c = await db.get("cursos", curso);
  if (!c) return;
  $("#btnCsv")?.addEventListener("click", async ()=>{
    const lista = await listaDeConvocacao(curso);
    const confirmados = lista.filter(l=> l.status === "confirmou" || (l.tipo === "titular" && l.status !== "desistiu"));
    const cabecalho = ["Protocolo", "Matrícula", "Nome", "Diretoria", "Lotação", "E-mail", "Situação"];
    const linhas = confirmados.map(l=> [l.protocolo, l.inscricao?.matricula || "", l.inscricao?.nome || "", l.diretoria,
      l.inscricao?.lotacao || "", l.inscricao?.email || "", l.status]);
    baixar(`turma-${String(c.nome).replace(/[^\w-]+/g, "_")}.csv`, csvTexto(cabecalho, linhas), "text/csv;charset=utf-8");
    await registrar("lista final gerada", {curso_id:curso, confirmados:confirmados.length});
    toast("Lista final baixada.");
  });
  $("#btnLimpar")?.addEventListener("click", async ()=>{
    const insc = await db.porIndice("inscricoes", "curso_id", curso);
    for (const i of insc) await db.del("inscricoes", i.protocolo);
    const tri = await db.porIndice("triagens", "curso_id", curso);
    for (const t of tri) await db.del("triagens", t.id);
    const conv = (await db.list("convocacoes")).filter(x=> x.curso_id === curso);
    for (const x of conv) await db.del("convocacoes", x.id);
    await registrar("dados do curso apagados", {curso_id:curso, inscricoes:insc.length});
    toast("Dados apagados (RN08)."); navegar();
  });
};

/* ================= Sprint 8 · Aviso de privacidade na tela de inscrição ================= */
const inscricaoAntes = TELAS["#/inscricao"];
if (typeof inscricaoAntes === "function"){
  TELAS["#/inscricao"] = async ()=>{
    const html = await inscricaoAntes();
    const bloco = `<div class="card" id="privacidadeInscricao"><h2 style="margin-top:0">Privacidade dos dados</h2>
      <ul><li><b>Finalidade:</b> selecionar os servidores para o curso e formar a turma.</li>
        <li><b>Dados tratados:</b> matrícula, nome, lotação, diretoria, e-mail institucional e telefone.</li>
        <li><b>Quem acessa:</b> a Gerência de Formação e a diretoria do servidor, só durante a seleção.</li>
        <li><b>Prazo de retenção:</b> os dados são apagados 30 dias depois do fim do curso (RN08).</li>
        <li><b>Contato:</b> ${esc(EMAIL_GERENCIA)}.</li></ul></div>`;
    return html.includes("</div>") ? html.replace(/(<div id="comprovante">)/, bloco + "$1") : html + bloco;
  };
}
