/* ================= Sprints 4 a 6 · importação, conferência com o SEAP e triagem ================= */
"use strict";

const DOMINIO_POLITEC = "@politec.mt.gov.br";
const emailInstitucional = e=> /^\S+@\S+$/.test(String(e || "")) && String(e).toLowerCase().endsWith(DOMINIO_POLITEC);

/* ================= Sprint 4 · Importação das inscrições (RN01, RN02, RN03) ================= */
// classifica um bloco lido: devolve {dados, curso, erros}
function classificarBloco(dados, cursos){
  const erros = [];
  if (!dados.m) erros.push("sem matrícula (RN01)");
  if (!dados.n) erros.push("sem nome (RN01)");
  if (!dados.l) erros.push("sem lotação (RN01)");
  if (!dados.d) erros.push("sem diretoria (RN01)");
  if (!emailInstitucional(dados.e)) erros.push("e-mail fora do domínio institucional (RN02)");
  const curso = cursos.find(c=> c.id === dados.c) || null;
  if (!curso) erros.push("curso que não está no cadastro");
  return {dados, curso, erros};
}

// lê os blocos de um texto colado e classifica: novas, duplicadas (RN03) e recusadas
function analisarInscricoes(texto, cursos){
  const blocos = blocoInscricao.ler(texto);
  const linhas = [];
  for (const b of blocos){
    if (b.erro){ linhas.push({tipo:"recusada", motivo:b.erro, trecho:b.trecho || ""}); continue; }
    const cls = classificarBloco(b.dados, cursos);
    if (cls.erros.length){ linhas.push({tipo:"recusada", motivo:cls.erros.join("; "), dados:b.dados}); continue; }
    linhas.push({tipo:"nova", dados:b.dados, curso:cls.curso});
  }
  // RN03: uma inscrição por matrícula e curso; na dúvida, vence o reenvio mais recente
  const porChave = new Map();
  for (const l of linhas.filter(x=>x.tipo === "nova")){
    const chave = l.dados.c + "|" + l.dados.m;
    if (!porChave.has(chave)) porChave.set(chave, []);
    porChave.get(chave).push(l);
  }
  for (const grupo of porChave.values()){
    if (grupo.length < 2) continue;
    grupo.sort((a, b)=> String(b.dados.s || "").localeCompare(String(a.dados.s || "")));
    grupo.forEach((l, i)=> l.tipo = i === 0 ? "nova" : "duplicada");
  }
  return linhas;
}
teste("análise: 60 e-mails do exemplo dão 50 novas, 5 duplicadas e 5 recusadas", ()=>{
  const s = dadosEmbutidos("seed");
  if (!s?.emails) return true;
  const l = analisarInscricoes(s.emails, s.cursos);
  const novas = l.filter(x=>x.tipo === "nova").length, dup = l.filter(x=>x.tipo === "duplicada").length, rec = l.filter(x=>x.tipo === "recusada").length;
  return (novas === 50 && dup === 5 && rec === 5) || `novas ${novas} · duplicadas ${dup} · recusadas ${rec}`;
});
teste("análise: o reenvio mais recente do mesmo par vence (RN03)", ()=>{
  const s = dadosEmbutidos("seed");
  if (!s?.emails) return true;
  const l = analisarInscricoes(s.emails, s.cursos);
  const dup = l.filter(x=>x.tipo === "duplicada");
  if (!dup.length) return true;
  const venc = l.filter(x=>x.tipo === "nova" && x.dados.m === dup[0].dados.m)[0];
  return venc && String(venc.dados.s) >= String(dup[0].dados.s);
});

function inscricaoDe(dados, recebido){
  return {protocolo:dados.p, curso_id:dados.c, matricula:dados.m, nome:dados.n, lotacao:dados.l, diretoria:dados.d,
    email:dados.e, telefone:dados.t || "", pre:dados.r || [], enviado_em:dados.s || "", recebido_em:recebido || agora(),
    status:"importada"};
}

async function gravarInscricoes(linhas){
  let novas = 0, substituidas = 0;
  for (const l of linhas.filter(x=>x.tipo === "nova")){
    const insc = inscricaoDe(l.dados);
    const antigas = await db.porIndice("inscricoes", "matricula", insc.matricula);
    for (const a of antigas) if (a.curso_id === insc.curso_id){ await db.del("inscricoes", a.protocolo); substituidas++; }
    await db.put("inscricoes", insc); novas++;
  }
  return {novas, substituidas};
}

TELAS["#/importar"] = async ()=>{
  const cursos = await db.list("cursos");
  return `<h1>Importar inscrições</h1><p class="sub">Cole os e-mails recebidos (o app acha todos os blocos de inscrição), ou importe uma planilha CSV.
    O bloco de cada inscrição tem um código de verificação: bloco cortado ou alterado é recusado e apontado.</p>
    <div class="card"><h2 style="margin-top:0">1 · Colar os e-mails</h2>
      <textarea id="txtEmails" rows="10" placeholder="Cole aqui os e-mails de inscrição, um abaixo do outro"></textarea>
      <div class="linha-botoes nao-imprimir"><button class="prim" id="btnLer">Ler e classificar</button>
        <button id="btnExemploEmails">Carregar os 60 e-mails de exemplo</button></div></div>
    <div class="card"><h2 style="margin-top:0">2 · Importar planilha (alternativa)</h2>
      <p class="sub">CSV com as colunas matrícula, nome, lotação, diretoria, e-mail e telefone. A primeira linha é o cabeçalho.</p>
      <label class="botao">Escolher CSV<input type="file" accept=".csv,text/csv" id="arqCsv" hidden></label>
      <div id="csvResumo"></div></div>
    <div id="resultadoImport"></div>
    <div id="resumoInscricoes"></div>`;
};
TELAS_DEPOIS["#/importar"] = ()=>{
  const txt = $("#txtEmails");
  if (!txt) return;
  let analise = null;
  $("#btnExemploEmails").addEventListener("click", ()=>{
    const s = dadosEmbutidos("seed");
    txt.value = s?.emails || "";
    toast(s?.emails ? "Exemplo carregado: 60 e-mails." : "O exemplo não está neste build.");
  });
  $("#btnLer").addEventListener("click", async ()=>{
    const cursos = await db.list("cursos");
    analise = analisarInscricoes(txt.value, cursos);
    const novas = analise.filter(l=>l.tipo === "nova"), dup = analise.filter(l=>l.tipo === "duplicada"), rec = analise.filter(l=>l.tipo === "recusada");
    $("#resultadoImport").innerHTML = `<div class="card"><h2 style="margin-top:0">3 · Conferir e importar</h2>
      <div class="grade"><div class="card kpi"><div class="v">${novas.length}</div><div class="r">novas</div></div>
        <div class="card kpi"><div class="v">${dup.length}</div><div class="r">duplicadas (RN03)</div></div>
        <div class="card kpi"><div class="v">${rec.length}</div><div class="r">recusadas</div></div></div>
      ${rec.length ? `<div class="tabela-wrap"><table><tr><th>Motivo</th><th>Detalhe</th></tr>
        ${rec.map(l=>`<tr><td><span class="selo erro">recusada</span></td><td>${esc(l.motivo)}</td></tr>`).join("")}</table></div>` : ""}
      ${dup.length ? `<p class="sub">Nas ${dup.length} duplicadas, vale o reenvio mais recente (RN03).</p>` : ""}
      <div class="linha-botoes nao-imprimir"><button class="prim" id="btnGravar" ${novas.length ? "" : "disabled"}>Importar ${novas.length} inscrições</button></div></div>`;
    $("#btnGravar")?.addEventListener("click", async ()=>{
      const r = await gravarInscricoes(analise);
      await registrar("importação de inscrições", {novas:r.novas, substituidas:r.substituidas, recusadas:rec.length});
      toast(`Importadas ${r.novas} inscrições${r.substituidas ? `, ${r.substituidas} substituídas` : ""}.`);
      $("#resumoInscricoes").innerHTML = await resumoInscricoes();
    });
  });
  $("#arqCsv").addEventListener("change", async e=>{
    const arq = e.target.files[0]; if (!arq) return;
    const linhas = lerCSV(await lerArquivoTexto(arq));
    if (linhas.length < 2) return $("#csvResumo").innerHTML = `<div class="card pendente">O arquivo está vazio.</div>`;
    const cab = linhas[0].map(c=> normalizar(c)), dados = linhas.slice(1);
    const achar = (...nomes)=> cab.findIndex(c=> nomes.some(n=> c.includes(n)));
    const col = {matricula:achar("matricul"), nome:achar("nome"), lotacao:achar("lotac"), diretoria:achar("diret"),
      email:achar("email"), telefone:achar("telefone")};
    const faltando = ["matricula", "nome", "diretoria"].filter(k=> col[k] < 0);
    if (faltando.length) return $("#csvResumo").innerHTML = `<div class="card pendente">Falta a coluna: ${faltando.join(", ")}.</div>`;
    const cursos = await db.list("cursos"), curso = cursos[0];
    const linhasNovas = dados.map(l=>{
      const dados1 = {p:"CSV-" + Date.now().toString(36).toUpperCase() + Math.random().toString(36).slice(2, 6).toUpperCase(),
        c: curso ? curso.id : "", m:(l[col.matricula] || "").trim(), n:(l[col.nome] || "").trim(), l:(l[col.lotacao] || "").trim(),
        d:(l[col.diretoria] || "").trim(), e:(l[col.email] || "").trim(), t:col.telefone >= 0 ? (l[col.telefone] || "").trim() : "", r:[], s:agora()};
      const cls = classificarBloco(dados1, cursos);
      return cls.erros.length ? {tipo:"recusada", motivo:cls.erros.join("; ")} : {tipo:"nova", dados:dados1};
    });
    analise = linhasNovas;
    const rec = linhasNovas.filter(l=>l.tipo === "recusada"), novas = linhasNovas.filter(l=>l.tipo === "nova");
    $("#csvResumo").innerHTML = `<div class="card"><p><b>${arq.name}</b>: ${dados.length} linhas lidas, ${novas.length} válidas, ${rec.length} recusadas.</p>
      ${rec.length ? `<ul>${rec.map(l=>`<li>${esc(l.motivo)}</li>`).join("")}</ul>` : ""}
      <div class="linha-botoes nao-imprimir"><button class="prim" id="btnGravarCsv" ${novas.length ? "" : "disabled"}>Importar ${novas.length} inscrições</button></div></div>`;
    $("#btnGravarCsv")?.addEventListener("click", async ()=>{
      const r = await gravarInscricoes(analise);
      await registrar("importação por planilha", {arquivo:arq.name, novas:r.novas});
      toast(`Importadas ${r.novas} inscrições.`);
      $("#resumoInscricoes").innerHTML = await resumoInscricoes();
    });
  });
};

async function resumoInscricoes(){
  const insc = await db.list("inscricoes");
  if (!insc.length) return "";
  const porCurso = {};
  insc.forEach(i=> porCurso[i.curso_id] = (porCurso[i.curso_id] || 0) + 1);
  return `<div class="card"><h2 style="margin-top:0">Inscrições no banco</h2>
    <div class="grade">${Object.entries(porCurso).map(([id, n])=> `<div class="card kpi"><div class="v">${n}</div><div class="r">${esc(id)}</div></div>`).join("")}</div>
    <p class="linha-botoes"><a class="botao prim" href="#/inscritos/${encodeURIComponent(Object.keys(porCurso)[0])}">Conferir com o SEAP</a></p></div>`;
}

/* ================= Sprint 5 · Conferência com o SEAP (RN04) ================= */
function alertasDaInscricao(insc, seap){
  const alertas = [];
  const s = seap.find(x=> x.matricula === insc.matricula);
  if (!s) alertas.push({cod:"RN04", texto:"matrícula não consta no SEAP"});
  else {
    if (!s.vinculo_ativo) alertas.push({cod:"RN04", texto:"vínculo não ativo no SEAP"});
    if (s.diretoria && insc.diretoria && s.diretoria !== insc.diretoria)
      alertas.push({cod:"RN04", texto:`diretoria diferente do SEAP (${s.diretoria})`});
  }
  if (!emailInstitucional(insc.email)) alertas.push({cod:"RN02", texto:"e-mail fora do domínio institucional"});
  return alertas;
}

async function importarSeap(texto){
  const linhas = lerCSV(texto);
  if (linhas.length < 2) return {ok:0, erro:"O arquivo do SEAP está vazio."};
  const cab = linhas[0].map(c=> normalizar(c));
  const achar = (...n)=> cab.findIndex(c=> n.some(x=> c.includes(x)));
  const col = {matricula:achar("matricul"), nome:achar("nome"), cargo:achar("cargo"), lotacao:achar("lotac"),
    diretoria:achar("diret"), vinculo:achar("vinculo")};
  if (col.matricula < 0 || col.nome < 0) return {ok:0, erro:"O arquivo do SEAP precisa ter, pelo menos, matrícula e nome."};
  let ok = 0;
  for (const l of linhas.slice(1)){
    const m = String(l[col.matricula] || "").trim(); if (!m) continue;
    const vinculo = col.vinculo >= 0 ? String(l[col.vinculo] || "").trim().toUpperCase() : "S";
    await db.put("seap", {matricula:m, nome:String(l[col.nome] || "").trim(), cargo:col.cargo >= 0 ? String(l[col.cargo] || "").trim() : "",
      lotacao:col.lotacao >= 0 ? String(l[col.lotacao] || "").trim() : "", diretoria:col.diretoria >= 0 ? String(l[col.diretoria] || "").trim() : "",
      vinculo_ativo: vinculo === "S" || vinculo === "SIM" || vinculo === "TRUE" || vinculo === "1"});
    ok++;
  }
  return {ok};
}

TELAS["#/inscritos/:curso"] = async ({curso})=>{
  const c = await db.get("cursos", curso);
  if (!c) return `<div class="card vazio">Curso não encontrado. <a href="#/cursos">Voltar</a></div>`;
  const [insc, seap, triagens, dirs] = await Promise.all([
    db.porIndice("inscricoes", "curso_id", curso), db.list("seap"), db.porIndice("triagens", "curso_id", curso), db.list("diretorias")]);
  const comAlerta = insc.map(i=> ({i, alertas: alertasDaInscricao(i, seap)}));
  const filtro = estado.inscFiltro || "todas";
  const lista = comAlerta.filter(x=> filtro === "todas" ? true
    : filtro === "alerta" ? x.alertas.length > 0 : x.i.diretoria === filtro);
  const respostas = dirs.map(d=>({d, tri: triagens.find(t=> t.diretoria === d.sigla) || null}));
  const linha = x=> `<tr><td><b>${esc(x.i.nome)}</b><br><span class="sub mono">${esc(x.i.matricula)}</span></td>
    <td>${esc(x.i.diretoria || "—")}</td><td>${esc(x.i.lotacao || "—")}</td><td class="mono">${esc(x.i.email || "—")}</td>
    <td>${x.alertas.length ? x.alertas.map(a=>`<span class="selo alerta">${esc(a.cod)}: ${esc(a.texto)}</span>`).join(" ") : '<span class="selo ok">sem alerta</span>'}</td>
    <td><button data-corrigir="${esc(x.i.protocolo)}">Corrigir</button></td></tr>`;
  return `<h1>Inscritos · ${esc(c.nome)}</h1><p class="sub">${periodo(c)} · ${insc.length} inscrições. A conferência com o SEAP avisa, mas não recusa (RN04).</p>
    <p class="linha-botoes"><a class="botao" href="#/curso/${encodeURIComponent(c.id)}">Esteira do curso</a>
      <a class="botao" href="#/triagem">Triagem pelas diretorias</a>
      <a class="botao" href="#/convocacao/${encodeURIComponent(c.id)}">Convocação</a>
      <a class="botao" href="#/turma/${encodeURIComponent(c.id)}">Turma</a></p>
    <div class="card"><h2 style="margin-top:0">Relatório do SEAP</h2>
      <p class="sub">${seap.length} servidores no banco. O app confere matrícula, vínculo e diretoria.</p>
      <div class="linha-botoes nao-imprimir"><label class="botao">Importar relatório do SEAP (CSV)<input type="file" accept=".csv,text/csv" id="arqSeap" hidden></label>
        <button id="btnSeapExemplo">Carregar o SEAP de exemplo</button></div>
      <div id="seapResumo"></div></div>
    <div class="card"><h2 style="margin-top:0">Resposta das diretorias</h2>
      <div class="tabela-wrap"><table><tr><th>Diretoria</th><th class="num">Vagas</th><th class="num">Inscritos</th><th>Situação</th><th></th></tr>
        ${respostas.map(({d, tri})=>{
          const n = insc.filter(i=>i.diretoria === d.sigla).length, vagas = Number(c.vagas_por_diretoria?.[d.sigla] || 0);
          return `<tr><td><b>${esc(d.sigla)}</b> · ${esc(d.nome)}</td><td class="num">${vagas}</td><td class="num">${n}</td>
            <td>${tri ? `<span class="selo ok">respondeu ${dataCurtaBR(tri.decidido_em || "")}</span>` : (vagas ? '<span class="selo alerta">não respondeu</span>' : '<span class="sub">sem vagas</span>')}</td>
            <td><button data-exportar="${esc(d.sigla)}">Exportar triagem</button></td></tr>`;}).join("")}</table></div>
      <div class="linha-botoes nao-imprimir"><label class="botao">Importar decisão de diretoria (JSON)<input type="file" accept=".json,application/json" id="arqDecisao" hidden></label></div>
      <div id="decisaoResumo"></div></div>
    <div class="card"><h2 style="margin-top:0">Inscrições</h2>
      <div class="campos"><div class="campo"><label for="filtroInsc">Filtro</label><select id="filtroInsc">
        <option value="todas">Todas</option><option value="alerta">Com alerta</option>
        ${dirs.map(d=>`<option value="${esc(d.sigla)}">${esc(d.sigla)}</option>`).join("")}</select></div></div>
      <div class="tabela-wrap"><table id="tabelaInscritos"><tr><th>Servidor</th><th>Diretoria</th><th>Lotação</th><th>E-mail</th><th>Alertas</th><th></th></tr>
        ${lista.map(linha).join("") || '<tr><td colspan="6" class="vazio">Nenhuma inscrição neste filtro.</td></tr>'}</table></div></div>
    <div id="editorInscricao"></div>`;
};
TELAS_DEPOIS["#/inscritos/:curso"] = async ({curso})=>{
  const filtro = $("#filtroInsc");
  if (!filtro) return;
  filtro.value = estado.inscFiltro || "todas";
  filtro.addEventListener("change", e=>{ estado.inscFiltro = e.target.value; navegar(); });
  $("#btnSeapExemplo")?.addEventListener("click", async ()=>{
    const s = dadosEmbutidos("seed");
    let ok = 0;
    for (const servidor of (s?.seap || [])){ await db.put("seap", servidor); ok++; }
    await registrar("SEAP de exemplo carregado", {servidores:ok});
    toast(`${ok} servidores no SEAP.`); navegar();
  });
  $("#arqSeap")?.addEventListener("change", async e=>{
    const arq = e.target.files[0]; if (!arq) return;
    const r = await importarSeap(await lerArquivoTexto(arq));
    if (r.erro){ $("#seapResumo").innerHTML = `<div class="card pendente">${esc(r.erro)}</div>`; return; }
    await registrar("SEAP importado", {arquivo:arq.name, servidores:r.ok});
    toast(`${r.ok} servidores importados do SEAP.`); navegar();
  });
  $("#arqDecisao")?.addEventListener("change", async e=>{
    const arq = e.target.files[0]; if (!arq) return;
    try {
      const d = JSON.parse(await lerArquivoTexto(arq));
      const erro = validarDecisao(d, curso);
      if (erro) return $("#decisaoResumo").innerHTML = `<div class="card pendente">${esc(erro)}</div>`;
      await db.put("triagens", {id: curso + "|" + d.diretoria, curso_id:curso, diretoria:d.diretoria, vagas:d.vagas || 0,
        titulares:d.titulares || [], reservas:d.reservas || [], decidido_em:d.decidido_em || agora(), decidido_por:d.decidido_por || "", origem:arq.name});
      await registrar("decisão de diretoria importada", {curso_id:curso, diretoria:d.diretoria, titulares:(d.titulares || []).length});
      toast(`Decisão da ${d.diretoria} importada.`); navegar();
    } catch(err){ $("#decisaoResumo").innerHTML = `<div class="card pendente">Arquivo ilegível: ${esc(err.message)}</div>`; }
  });
  $$("[data-exportar]").forEach(b=> b.addEventListener("click", ()=> exportarTriagem(b.dataset.exportar, curso)));
  $$("[data-corrigir]").forEach(b=> b.addEventListener("click", async ()=>{
    const i = await db.get("inscricoes", b.dataset.corrigir);
    if (!i) return;
    $("#editorInscricao").innerHTML = `<form class="card" id="formCorrigir"><h2 style="margin-top:0">Corrigir inscrição</h2>
      <p class="sub">${esc(i.nome)} · matrícula ${esc(i.matricula)}. A correção fica na trilha com o valor anterior.</p>
      <div class="campos">
        ${campo("corrNome", "Nome", {valor:i.nome})}
        ${campo("corrLotacao", "Lotação", {valor:i.lotacao})}
        ${campo("corrDiretoria", "Diretoria", {valor:i.diretoria})}
        ${campo("corrEmail", "E-mail", {valor:i.email})}
        ${campo("corrJustificativa", "Justificativa", {tipo:"textarea", linhas:2, obrigatorio:true})}
      </div><div id="errosCorrigir"></div>
      <div class="linha-botoes"><button class="prim" type="submit">Salvar correção</button>
        <button type="button" id="btnCancelarCorr">Cancelar</button></div></form>`;
    $("#btnCancelarCorr").addEventListener("click", ()=>{ $("#editorInscricao").innerHTML = ""; });
    $("#formCorrigir").addEventListener("submit", async ev=>{
      ev.preventDefault();
      const novo = {nome:valorDe("corrNome"), lotacao:valorDe("corrLotacao"), diretoria:valorDe("corrDiretoria"), email:valorDe("corrEmail")};
      const justificativa = valorDe("corrJustificativa");
      const erros = [];
      if (!novo.nome) erros.push("Informe o nome.");
      if (!novo.diretoria) erros.push("Informe a diretoria.");
      if (!justificativa) erros.push("Escreva a justificativa da correção.");
      if (!mostrarErros("#errosCorrigir", erros)) return;
      await db.put("inscricoes", {...i, ...novo, email:novo.email.toLowerCase(), corrigido_em:agora()});
      await registrar("inscrição corrigida pela gerência", {curso_id:i.curso_id, protocolo:i.protocolo,
        valor_anterior:{nome:i.nome, lotacao:i.lotacao, diretoria:i.diretoria, email:i.email},
        valor_novo:novo, justificativa});
      toast("Correção salva na trilha."); navegar();
    });
  }));
};

function validarDecisao(d, curso){
  if (!d || d.tipo !== "decisao") return "O arquivo não é uma decisão de diretoria.";
  if (d.curso_id !== curso) return "A decisão é de outro curso.";
  if (!d.diretoria) return "A decisão não diz a diretoria.";
  if (!Array.isArray(d.titulares)) return "A decisão não traz a lista de titulares.";
  const vagas = Number(d.vagas || 0);
  if (vagas && d.titulares.length > vagas) return `A diretoria marcou ${d.titulares.length} titulares para ${vagas} vagas (RN05).`;
  return "";
}

async function exportarTriagem(sigla, curso){
  const c = await db.get("cursos", curso);
  const insc = (await db.porIndice("inscricoes", "curso_id", curso)).filter(i=> i.diretoria === sigla);
  const dirs = await db.list("diretorias"), d = dirs.find(x=> x.sigla === sigla);
  const payload = {tipo:"triagem", versao:1, gerado_em:agora(), curso_id:curso, curso:{nome:c.nome, inicio:c.inicio, fim:c.fim,
    local:c.local, prazo_triagem:c.prazo_triagem}, diretoria:sigla, nome_diretoria:d ? d.nome : sigla,
    vagas:Number(c.vagas_por_diretoria?.[sigla] || 0), prazo:c.prazo_triagem || "",
    inscritos:insc.map(i=> ({protocolo:i.protocolo, matricula:i.matricula, nome:i.nome, lotacao:i.lotacao,
      email:i.email, telefone:i.telefone || "", enviado_em:i.enviado_em}))};
  baixar(`triagem-${sigla}.json`, JSON.stringify(payload, null, 2), "application/json");
  await registrar("arquivo de triagem exportado", {curso_id:curso, diretoria:sigla, inscritos:insc.length});
  toast(`triagem-${sigla}.json gerado com ${insc.length} inscritos.`);
}

/* ================= Sprint 6 · Triagem pelas diretorias (RN05) ================= */
TELAS["#/triagem"] = async ()=>{
  const [cursos, dirs, triagens] = await Promise.all([db.list("cursos"), db.list("diretorias"), db.list("triagens")]);
  const dir = estado.tgDir || (dirs[0] && dirs[0].sigla) || "";
  const nomeDir = dirs.find(d=> d.sigla === dir)?.nome || dir;
  const curso = estado.tgCurso || (cursos[0] && cursos[0].id) || "";
  // guarda a escolha, para que os botões de ação saibam de qual diretoria e curso falam
  estado.tgDir = dir; estado.tgCurso = curso;
  const tri = triagens.find(t=> t.curso_id === curso && t.diretoria === dir) || null;
  const c = cursos.find(x=> x.id === curso);
  const vagas = Number(c?.vagas_por_diretoria?.[dir] || 0);
  const insc = curso ? (await db.porIndice("inscricoes", "curso_id", curso)).filter(i=> i.diretoria === dir) : [];
  const carga = tri ? (await db.porIndice("inscricoes", "curso_id", curso)) : [];
  // a lista mostra todo mundo do arquivo de triagem; a situação vem de quem já foi marcado
  const ordem = tri ? [...new Set([...(tri.ordem || []), ...(tri.titulares || []), ...(tri.reservas || [])])] : [];
  const lista = tri ? ordem.map(p=> ({p, i:carga.find(x=> x.protocolo === p)})).filter(x=> x.i) : [];
  const linha = (x, idx)=> `<tr data-prot="${esc(x.p)}">
    <td class="num">${idx + 1}</td><td><b>${esc(x.i.nome)}</b><br><span class="sub mono">${esc(x.i.matricula)}</span></td>
    <td>${esc(x.i.lotacao || "—")}</td>
    <td>${tri.titulares.includes(x.p) ? '<span class="selo ok">titular</span>' : tri.reservas.includes(x.p) ? '<span class="selo info">reserva</span>' : '<span class="selo">a indicar</span>'}</td>
    <td class="nao-imprimir"><button data-sobe="${esc(x.p)}">▲</button> <button data-desce="${esc(x.p)}">▼</button>
      <button data-titular="${esc(x.p)}">Titular</button> <button data-reserva="${esc(x.p)}">Reserva</button></td></tr>`;
  return `<h1>Triagem</h1><p class="sub">A diretoria indica titulares e reserva, na ordem de prioridade. A gerência exporta o arquivo e importa a decisão.</p>
    <div class="card"><div class="campos">
      <div class="campo"><label for="tgDir">Diretoria</label><select id="tgDir">${dirs.map(d=>`<option value="${esc(d.sigla)}" ${d.sigla === dir ? "selected" : ""}>${esc(d.sigla)} · ${esc(d.nome)}</option>`).join("")}</select></div>
      <div class="campo"><label for="tgCurso">Curso</label><select id="tgCurso">${cursos.map(x=>`<option value="${esc(x.id)}" ${x.id === curso ? "selected" : ""}>${esc(x.nome)}</option>`).join("")}</select></div>
    </div></div>
    <div class="grade"><div class="card kpi"><div class="v">${vagas}</div><div class="r">vagas da diretoria</div></div>
      <div class="card kpi"><div class="v">${insc.length}</div><div class="r">inscritos</div></div>
      <div class="card kpi"><div class="v">${tri ? tri.titulares.length : 0}</div><div class="r">titulares</div></div>
      <div class="card kpi"><div class="v">${tri ? tri.reservas.length : 0}</div><div class="r">reservas</div></div></div>
    ${tri && tri.aviso ? `<div class="card pendente" id="avisoTriagem"><b>Aviso.</b> ${esc(tri.aviso)}</div>` : ""}
    <div class="card"><h2 style="margin-top:0">Arquivo da gerência</h2>
      <p class="sub">A Gerência de Formação exporta <span class="mono">triagem-${esc(dir)}.json</span> e envia para a diretoria. A diretoria devolve <span class="mono">decisao-${esc(dir)}.json</span>.</p>
      <div class="linha-botoes nao-imprimir"><label class="botao">Importar o arquivo de triagem (JSON)<input type="file" accept=".json,application/json" id="arqTriagem" hidden></label>
        ${tri ? `<button class="prim" id="btnExportarDecisao">Exportar a decisão (decisao-${esc(dir)}.json)</button>` : ""}</div>
      <div id="triagemResumo"></div></div>
    <div class="card tabela-wrap"><h2>${esc(nomeDir)} · ${esc(c ? c.nome : "")}</h2>
      <table id="tabelaTriagemDecisao"><tr><th class="num">Ordem</th><th>Servidor</th><th>Lotação</th><th>Situação</th><th class="nao-imprimir">Ações</th></tr>
        ${lista.map(linha).join("") || `<tr><td colspan="5" class="vazio">Nenhuma decisão registrada para esta diretoria.</td></tr>`}</table></div>`;
};
TELAS_DEPOIS["#/triagem"] = async ()=>{
  $("#tgDir")?.addEventListener("change", e=>{ estado.tgDir = e.target.value; navegar(); });
  $("#tgCurso")?.addEventListener("change", e=>{ estado.tgCurso = e.target.value; navegar(); });
  $("#arqTriagem")?.addEventListener("change", async e=>{
    const arq = e.target.files[0]; if (!arq) return;
    try {
      const d = JSON.parse(await lerArquivoTexto(arq));
      if (d.tipo !== "triagem") return $("#triagemResumo").innerHTML = `<div class="card pendente">O arquivo não é um arquivo de triagem.</div>`;
      const curso = d.curso_id, dir = d.diretoria;
      const existentes = (await db.porIndice("inscricoes", "curso_id", curso)).filter(i=> i.protocolo !== "CSV");
      const linhas = d.inscritos.map(i=> existentes.find(x=> x.protocolo === i.protocolo) || {protocolo:i.protocolo, matricula:i.matricula,
        nome:i.nome, lotacao:i.lotacao, email:i.email, telefone:i.telefone || "", curso_id:curso, diretoria:dir, status:"triado"});
      for (const l of linhas) await db.put("inscricoes", l);
      await db.put("triagens", {id: curso + "|" + dir, curso_id:curso, diretoria:dir, vagas:d.vagas || 0,
        titulares:[], reservas:[], ordem:linhas.map(l=> l.protocolo), decidido_em:"", decidido_por:"", origem:arq.name, em_aberto:true});
      await registrar("arquivo de triagem importado", {curso_id:curso, diretoria:dir, inscritos:linhas.length});
      toast(`Arquivo de triagem importado: ${linhas.length} inscritos.`); navegar();
    } catch(err){ $("#triagemResumo").innerHTML = `<div class="card pendente">Arquivo ilegível: ${esc(err.message)}</div>`; }
  });
  $("#btnExportarDecisao")?.addEventListener("click", async ()=>{
    const curso = estado.tgCurso, dir = estado.tgDir;
    const tri = (await db.list("triagens")).find(t=> t.curso_id === curso && t.diretoria === dir);
    if (!tri) return;
    const payload = {tipo:"decisao", versao:1, gerado_em:agora(), curso_id:curso, diretoria:dir, vagas:tri.vagas || 0,
      titulares:tri.titulares || [], reservas:tri.reservas || [], decidido_em:agora(), decidido_por:estado.perfil || "Diretoria"};
    baixar(`decisao-${dir}.json`, JSON.stringify(payload, null, 2), "application/json");
    await registrar("decisão exportada", {curso_id:curso, diretoria:dir, titulares:(tri.titulares || []).length});
    toast(`decisao-${dir}.json gerado.`);
  });
  const salvar = async (mut)=>{
    const curso = estado.tgCurso, dir = estado.tgDir;
    const tri = (await db.list("triagens")).find(t=> t.curso_id === curso && t.diretoria === dir);
    if (!tri) return toast("Importe o arquivo de triagem antes.");
    const novo = mut(tri);
    await db.put("triagens", {...tri, ...novo});
    navegar();
  };
  $$("[data-titular]").forEach(b=> b.addEventListener("click", ()=> salvar(tri=>{
    const p = b.dataset.titular;
    const jaTitular = (tri.titulares || []).includes(p);
    const nTitulares = (tri.titulares || []).length + (jaTitular ? 0 : 1);
    // RN05: a diretoria não marca mais titulares que as vagas dela
    if (!jaTitular && (tri.vagas || 0) && nTitulares > tri.vagas)
      return {...tri, aviso:`A diretoria tem ${tri.vagas} vagas; marcar mais titular excede o limite (RN05).`};
    const titulares = (tri.titulares || []).filter(x=> x !== p);
    const reservas = (tri.reservas || []).filter(x=> x !== p);
    return {...tri, titulares: titulares.concat([p]), reservas, aviso:""};
  })));
  $$("[data-reserva]").forEach(b=> b.addEventListener("click", ()=> salvar(tri=>{
    const p = b.dataset.reserva;
    return {...tri, titulares:(tri.titulares || []).filter(x=> x !== p), reservas:(tri.reservas || []).filter(x=> x !== p).concat([p]), aviso:""};
  })));
  $$("[data-sobe]").forEach(b=> b.addEventListener("click", ()=> salvar(tri=> mover(tri, b.dataset.sobe, -1))));
  $$("[data-desce]").forEach(b=> b.addEventListener("click", ()=> salvar(tri=> mover(tri, b.dataset.desce, 1))));
};

function mover(tri, protocolo, passo){
  const ordem = [...(tri.ordem || []), ...(tri.titulares || []), ...(tri.reservas || [])];
  const i = ordem.indexOf(protocolo);
  if (i < 0) return tri;
  const j = i + passo;
  if (j < 0 || j >= ordem.length) return tri;
  [ordem[i], ordem[j]] = [ordem[j], ordem[i]];
  return {...tri, ordem, titulares:ordem.filter(p=> (tri.titulares || []).includes(p)),
    reservas:ordem.filter(p=> (tri.reservas || []).includes(p))};
}
