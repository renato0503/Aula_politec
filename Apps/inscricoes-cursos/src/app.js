/* Inscrições em Cursos · código do app (o construir.py junta com a base comum) */
"use strict";
/* ---------- bloco de inscrição (formato definido no Sprint 0, ver exemplos/gerar_exemplos.py) ---------- */
function fnv1a(txt){
  let h = 0x811c9dc5;
  for (const b of new TextEncoder().encode(txt)){ h ^= b; h = Math.imul(h, 0x01000193) >>> 0; }
  return h.toString(16).padStart(8, "0");
}
function b64url(txt){ return btoa(String.fromCharCode(...new TextEncoder().encode(txt))).replace(/\+/g, "-").replace(/\//g, "_").replace(/=+$/, ""); }
function deB64url(s){ const b = atob(s.replace(/-/g, "+").replace(/_/g, "/")); return new TextDecoder().decode(Uint8Array.from(b, c=>c.charCodeAt(0))); }
const blocoInscricao = {
  gerar(dados){ const b = b64url(JSON.stringify(dados)); return `INSCRICAO-v1:${b}.${fnv1a(b)}`; },
  // Acha todos os blocos num texto colado. Devolve {dados} ou {erro} por bloco.
  ler(texto){
    return Array.from(texto.matchAll(/INSCRICAO-v1:([A-Za-z0-9_-]+)(?:\.([0-9a-f]{8}))?/g)).map(m=>{
      if (!m[2]) return {erro: "bloco incompleto (cortado)", trecho: m[0].slice(0, 40)};
      if (fnv1a(m[1]) !== m[2]) return {erro: "código de verificação não confere (bloco alterado)", trecho: m[0].slice(0, 40)};
      try { return {dados: JSON.parse(deB64url(m[1]))}; } catch(e){ return {erro: "bloco ilegível", trecho: m[0].slice(0, 40)}; }
    });
  }
};
teste("fnv1a('abc') = 1a47e90b (igual ao gerador Python)", ()=> fnv1a("abc") === "1a47e90b");
teste("bloco ida e volta com acento", ()=>{ const d = {n: "João Ávila", m: "123"}; const r = blocoInscricao.ler("x " + blocoInscricao.gerar(d) + " y"); return r[0].dados.n === "João Ávila"; });
teste("bloco alterado é recusado", ()=>{ const b = blocoInscricao.gerar({m: "1"}); return !!blocoInscricao.ler(b.slice(0, -1) + (b.endsWith("0") ? "1" : "0"))[0].erro; });
teste("biblioteca de QR Code embutida", ()=> typeof qrcode === "function");

const EMAIL_GERENCIA = "capacitacao@politec.mt.gov.br";

/* ---------- diretorias (configuração) ---------- */
async function configExtra(){
  const dirs = await db.list("diretorias");
  return `<div class="card"><h2 style="margin-top:0">Diretorias que recebem vagas</h2>
    <p>${dirs.map(d=>`<span class="selo info">${esc(d.sigla)} · ${esc(d.nome)}</span>`).join(" ") || '<span class="sub">Nenhuma.</span>'}</p>
    <form id="formDir" class="campos">${campo("dirSigla", "Sigla")}${campo("dirNome", "Nome")}
      <div class="campo"><label>&nbsp;</label><button type="submit">Acrescentar</button></div></form></div>`;
}
async function ligarConfigExtra(){
  $("#formDir")?.addEventListener("submit", async e=>{
    e.preventDefault(); const sigla = valorDe("dirSigla").toUpperCase(), nome = valorDe("dirNome");
    if (!sigla || !nome) return toast("Informe sigla e nome.");
    await db.put("diretorias", {sigla, nome}); await registrar("diretoria cadastrada", {detalhe: sigla}); navegar();
  });
}

/* ================= Sprint 2 · Cadastro e divulgação do curso ================= */
const totalVagas = c => Object.values(c.vagas_por_diretoria || {}).reduce((a, b)=>a + Number(b || 0), 0);
const periodo = c => `${dataCurtaBR(c.inicio)} a ${dataCurtaBR(c.fim)}`;

TELAS["#/cursos"] = async ()=>{
  const cursos = (await db.list("cursos")).sort((a, b)=>(b.inicio || "").localeCompare(a.inicio || ""));
  const dirs = await db.list("diretorias");
  return `<h1>Cursos</h1><p class="sub">Cadastre o curso, distribua as vagas por diretoria e gere o link de inscrição.</p>
    <div class="card tabela-wrap">${cursos.length ? `<table><tr><th>Curso</th><th>Período</th><th>Inscrições até</th><th class="num">Vagas</th><th>Situação</th><th></th></tr>
      ${cursos.map(c=>`<tr><td><b>${esc(c.nome)}</b><br><span class="sub">${esc(c.local || "")}</span></td><td>${periodo(c)}</td><td>${dataCurtaBR(c.inscricao_fim)}</td>
      <td class="num">${totalVagas(c)}</td><td>${esc(c.status || "")}</td>
      <td><a href="#/divulgar/${encodeURIComponent(c.id)}">Divulgar</a> · <button data-editar="${esc(c.id)}">Editar</button></td></tr>`).join("")}</table>`
      : `<p class="sub">Nenhum curso. Cadastre abaixo.</p>`}</div>
    <form class="card" id="formCurso"><h2 style="margin-top:0" id="tituloCurso">Novo curso</h2><input type="hidden" id="cursoId">
      <div class="campos">
        ${campo("cNome", "Nome do curso", {obrigatorio: true})}
        ${campo("cCarga", "Carga horária (h)", {tipo: "number", obrigatorio: true, attrs: 'min="1"'})}
        ${campo("cLocal", "Local", {obrigatorio: true})}
        ${campo("cInicio", "Início do curso", {tipo: "date", obrigatorio: true})}
        ${campo("cFim", "Fim do curso", {tipo: "date", obrigatorio: true})}
        ${campo("cInscIni", "Inscrições a partir de", {tipo: "date", obrigatorio: true})}
        ${campo("cInscFim", "Inscrições até", {tipo: "date", obrigatorio: true})}
        ${campo("cTriagem", "Prazo da triagem pelas diretorias", {tipo: "date", obrigatorio: true})}
        ${campo("cGrupo", "Link do grupo oficial da turma", {tipo: "url", ajuda: "Enviado só aos selecionados (RN08)."})}
      </div>
      ${campo("cPre", "Pré-requisitos (um por linha)", {tipo: "textarea", linhas: 3})}
      <h3>Vagas por diretoria</h3>
      ${dirs.length ? `<div class="campos">${dirs.map(d=>campo("vaga-" + d.sigla, `${d.sigla} · ${d.nome}`, {tipo: "number", valor: 0, attrs: 'min="0" data-vaga="' + esc(d.sigla) + '"'})).join("")}</div>
        <p>Total de vagas: <b id="totalVagas">0</b></p>`
        : `<p class="sub">Nenhuma diretoria cadastrada. Cadastre em <a href="#/config">Configuração</a> ou carregue os dados fictícios.</p>`}
      <div id="errosCurso"></div>
      <div class="linha-botoes"><button class="prim" type="submit">Salvar curso</button></div></form>`;
};
TELAS_DEPOIS["#/cursos"] = ()=>{
  const soma = ()=>{ const t = $$("[data-vaga]").reduce((a, i)=>a + (Number(i.value) || 0), 0); if ($("#totalVagas")) $("#totalVagas").textContent = t; };
  $$("[data-vaga]").forEach(i=>i.addEventListener("input", soma));
  $$("[data-editar]").forEach(b=>b.addEventListener("click", async ()=>{
    const c = await db.get("cursos", b.dataset.editar);
    $("#cursoId").value = c.id; $("#cNome").value = c.nome; $("#cCarga").value = c.carga_horaria; $("#cLocal").value = c.local || "";
    $("#cInicio").value = c.inicio; $("#cFim").value = c.fim; $("#cInscIni").value = c.inscricao_inicio || ""; $("#cInscFim").value = c.inscricao_fim || "";
    $("#cTriagem").value = c.prazo_triagem || ""; $("#cGrupo").value = c.link_grupo || ""; $("#cPre").value = (c.prerequisitos || []).join("\n");
    $$("[data-vaga]").forEach(i=>i.value = c.vagas_por_diretoria?.[i.dataset.vaga] || 0); soma();
    $("#tituloCurso").textContent = "Editar " + c.nome; $("#formCurso").scrollIntoView();
  }));
  $("#formCurso").addEventListener("submit", async e=>{
    e.preventDefault();
    const vagas = {}; $$("[data-vaga]").forEach(i=>{ const v = Number(i.value) || 0; if (v > 0) vagas[i.dataset.vaga] = v; });
    const c = {nome: valorDe("cNome"), carga_horaria: Number(valorDe("cCarga")), local: valorDe("cLocal"), inicio: valorDe("cInicio"), fim: valorDe("cFim"),
      inscricao_inicio: valorDe("cInscIni"), inscricao_fim: valorDe("cInscFim"), prazo_triagem: valorDe("cTriagem"), link_grupo: valorDe("cGrupo"),
      prerequisitos: valorDe("cPre").split("\n").map(s=>s.trim()).filter(Boolean), vagas_por_diretoria: vagas};
    const erros = [];
    if (!c.nome) erros.push("Informe o nome do curso.");
    if (!(c.carga_horaria > 0)) erros.push("Informe a carga horária.");
    if (!c.local) erros.push("Informe o local.");
    if (!c.inicio || !c.fim || c.fim < c.inicio) erros.push("O fim do curso deve ser igual ou depois do início.");
    if (!c.inscricao_inicio || !c.inscricao_fim || c.inscricao_fim < c.inscricao_inicio) erros.push("O fim das inscrições deve ser depois do início das inscrições.");
    if (c.inscricao_fim && c.inicio && c.inscricao_fim > c.inicio) erros.push("As inscrições terminam antes de o curso começar.");
    if (!c.prazo_triagem || (c.inscricao_fim && c.prazo_triagem < c.inscricao_fim) || (c.inicio && c.prazo_triagem > c.inicio)) erros.push("O prazo da triagem fica entre o fim das inscrições e o início do curso.");
    if (c.link_grupo && !/^https?:\/\//.test(c.link_grupo)) erros.push("O link do grupo começa com http:// ou https://.");
    if (!totalVagas(c)) erros.push("Distribua ao menos uma vaga.");
    if (!mostrarErros("#errosCurso", erros)) return;
    const id = valorDe("cursoId"), antes = id ? await db.get("cursos", id) : null;
    const reg = {...(antes || {id: "CURSO-" + Date.now().toString(36).toUpperCase(), status: "inscrições abertas", criado_em: agora()}), ...c, atualizado_em: agora()};
    await db.put("cursos", reg); await registrar(antes ? "curso alterado" : "curso criado", {curso_id: reg.id});
    toast("Curso salvo."); location.hash = "#/divulgar/" + encodeURIComponent(reg.id);
  });
};

// O link leva o curso dentro do endereço, para abrir a inscrição sem dado prévio.
function cursoPublico(c){
  return {v: 1, id: c.id, nome: c.nome, ch: c.carga_horaria, ini: c.inicio, fim: c.fim, local: c.local, pre: c.prerequisitos || [],
          ii: c.inscricao_inicio, if: c.inscricao_fim, dirs: Object.keys(c.vagas_por_diretoria || {}), email: EMAIL_GERENCIA};
}
function linkInscricao(c){
  const b = b64url(JSON.stringify(cursoPublico(c)));
  return location.href.split("#")[0] + "#/inscricao?c=" + b + "." + fnv1a(b);
}
function lerCursoDoLink(hash){
  const m = String(hash).match(/[?&]c=([A-Za-z0-9_-]+)\.([0-9a-f]{8})/);
  if (!m) return {erro: "O link não traz os dados do curso."};
  if (fnv1a(m[1]) !== m[2]) return {erro: "O link foi alterado ou cortado. Peça o link de novo à Gerência de Formação."};
  try { return {curso: JSON.parse(deB64url(m[1]))}; } catch(e){ return {erro: "O link está ilegível."}; }
}
function textoDivulgacao(c, link, dirs){
  const nomeDir = s => dirs.find(d=>d.sigla === s)?.nome || s;
  return `Assunto: Inscrições abertas: ${c.nome} (${periodo(c)})

Prezados,

Estão abertas as inscrições para o curso ${c.nome}, com carga horária de ${c.carga_horaria} h, de ${periodo(c)}, em ${c.local}.

Vagas por diretoria:
${Object.entries(c.vagas_por_diretoria).map(([s, v])=>`- ${nomeDir(s)}: ${v} vagas`).join("\n")}

Os servidores interessados se inscrevem pelo link abaixo até ${dataCurtaBR(c.inscricao_fim)}:
${link}
${c.prerequisitos?.length ? `\nPré-requisitos: ${c.prerequisitos.join("; ")}.\n` : ""}
Até ${dataCurtaBR(c.prazo_triagem)}, cada diretoria recebe o arquivo com os inscritos para indicar titulares e cadastro de reserva.

Gerência de Formação Inicial e Continuada`;
}
function qrSvg(texto){
  const qr = qrcode(0, "M"); qr.addData(texto); qr.make();
  return qr.createSvgTag({cellSize: 3, margin: 2, scalable: true, alt: "QR Code do link de inscrição"});
}
teste("link do curso ida e volta", ()=>{
  const c = {id: "C1", nome: "Curso Ávila", carga_horaria: 8, inicio: "2026-12-01", fim: "2026-12-02", local: "X", vagas_por_diretoria: {DMC: 2}};
  const r = lerCursoDoLink(linkInscricao(c).split("#")[1]); return r.curso && r.curso.nome === "Curso Ávila";
});
teste("link alterado é recusado", ()=>{ const l = linkInscricao({id: "C1", nome: "A", vagas_por_diretoria: {}}); return !!lerCursoDoLink(l.replace(/.$/, l.endsWith("0") ? "1" : "0")).erro; });

TELAS["#/divulgar/:curso"] = async ({curso})=>{
  const c = await db.get("cursos", curso);
  if (!c) return `<div class="card vazio">Curso não encontrado. <a href="#/cursos">Voltar</a></div>`;
  const dirs = await db.list("diretorias"), link = linkInscricao(c);
  return `<h1>Divulgar · ${esc(c.nome)}</h1><p class="sub">${periodo(c)} · ${totalVagas(c)} vagas · inscrições até ${dataCurtaBR(c.inscricao_fim)}</p>
    <div class="card"><h2 style="margin-top:0">Link de inscrição</h2>
      <p class="mono" id="linkInscricao" style="word-break:break-all">${esc(link)}</p>
      <div class="linha-botoes"><button class="prim" id="btnCopiarLink">Copiar link</button><a class="botao" href="${esc(link)}" target="_blank" rel="noopener">Abrir a inscrição</a></div></div>
    <div class="card"><h2 style="margin-top:0">QR Code</h2><div id="qr" style="max-width:260px">${qrSvg(link)}</div>
      <div class="linha-botoes"><button id="btnBaixarQr">Baixar QR Code (.svg)</button></div></div>
    <div class="card"><h2 style="margin-top:0">Texto para as diretorias</h2>
      <textarea id="textoDivulgacao" rows="16">${esc(textoDivulgacao(c, link, dirs))}</textarea>
      <div class="linha-botoes"><button id="btnCopiarTexto">Copiar texto</button></div></div>`;
};
TELAS_DEPOIS["#/divulgar/:curso"] = ({curso})=>{
  if (!$("#btnCopiarLink")) return;  // curso não encontrado
  const copiar = async (t, msg)=>{ try { await navigator.clipboard.writeText(t); toast(msg); } catch(e){ toast("Selecione e copie com Ctrl+C."); } };
  $("#btnCopiarLink").addEventListener("click", ()=>copiar($("#linkInscricao").textContent, "Link copiado."));
  $("#btnCopiarTexto").addEventListener("click", ()=>copiar($("#textoDivulgacao").value, "Texto copiado."));
  $("#btnBaixarQr").addEventListener("click", ()=>baixar(`qr-${curso}.svg`, $("#qr").innerHTML, "image/svg+xml"));
};

// Sprint 2: a inscrição já mostra o curso do link. O formulário chega no Sprint 3.
TELAS["#/inscricao"] = async ()=>{
  const r = lerCursoDoLink(location.hash);
  if (r.erro) return `<div class="card pendente"><h1>Inscrição</h1><p>${esc(r.erro)}</p></div>`;
  const c = r.curso;
  return `<h1>Inscrição · ${esc(c.nome)}</h1>
    <div class="card"><p><b>Período:</b> ${dataCurtaBR(c.ini)} a ${dataCurtaBR(c.fim)} · <b>Carga horária:</b> ${esc(c.ch)} h</p>
      <p><b>Local:</b> ${esc(c.local)}</p><p><b>Inscrições:</b> ${dataCurtaBR(c.ii)} a ${dataCurtaBR(c.if)}</p>
      ${c.pre.length ? `<p><b>Pré-requisitos:</b></p><ul>${c.pre.map(p=>`<li>${esc(p)}</li>`).join("")}</ul>` : ""}</div>
    <div class="card pendente">O formulário de inscrição chega no Sprint 3.</div>`;
};
