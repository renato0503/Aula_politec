/* Formulário de feedback dos apps (Aula 8).
   Cada app tem um HTML pequeno (gerado por Aula 8/gerar_feedback.py) com a
   configuração em window.FEEDBACK: o app, a equipe, os links e as telas.
   As respostas vão para a coleção `feedback_apps` do Firestore. Sem conexão,
   o rascunho fica no navegador e o aluno baixa o .json para enviar. */
import { iniciarFirebase } from "../firebase-config.js";

export const COLECAO_FEEDBACK = "feedback_apps";
const C = window.FEEDBACK || {};
const $ = s => document.querySelector(s);
const esc = s => String(s ?? "").replace(/[&<>"']/g, c => ({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;"}[c]));
const CPF = /\b\d{3}\.?\d{3}\.?\d{3}-?\d{2}\b/;
const SITUACOES = [["", "Não testei"], ["ok", "Funciona como esperado"], ["ajuste", "Funciona, mas precisa de ajuste"], ["erro", "Não funciona ou deu erro"]];

/* tema: segue o sistema, com botão para trocar */
const tema = localStorage.getItem("feedback:tema") || (matchMedia("(prefers-color-scheme: dark)").matches ? "escuro" : "claro");
document.documentElement.dataset.tema = tema;
function trocarTema(){
  const t = document.documentElement.dataset.tema === "escuro" ? "claro" : "escuro";
  document.documentElement.dataset.tema = t; localStorage.setItem("feedback:tema", t);
}

let fb = null;
async function firebase(){
  if (fb) return fb;
  fb = await iniciarFirebase();
  return fb;
}

/* ================= formulário de um app ================= */
function radios(nome, opcoes, obrigatorio){
  return `<div class="opcoes" role="radiogroup" aria-label="${esc(nome)}">${opcoes.map(([v, t]) =>
    `<label><input type="radio" name="${nome}" value="${esc(v)}" ${obrigatorio ? "required" : ""}> ${esc(t)}</label>`).join("")}</div>`;
}
function montarFormulario(){
  document.title = `Feedback · ${C.titulo} | POLITEC/MT`;
  $("#topo").innerHTML = `<div class="wrap"><div class="kicker">Curso POLITEC/MT · Feedback dos apps</div>
    <h1>${esc(C.titulo)}</h1><p>${esc(C.subtitulo || "")}</p>
    <p style="margin-top:8px">Equipe: <b>${esc(C.equipe)}</b></p>
    <div class="barra"><a href="${esc(C.link_app)}" target="_blank" rel="noopener">Abrir o app</a>
      <a href="${esc(C.link_hub)}" target="_blank" rel="noopener">Abrir o hub do app</a>
      <button type="button" id="btnTema">Tema claro ou escuro</button></div></div>`;
  $("#btnTema").addEventListener("click", trocarTema);
  $("#conteudo").innerHTML = `
    <div class="aviso info">Abra o app, use cada tela com os dados fictícios (<b>Configuração › Carregar dados fictícios</b>) e responda.
      O que você escrever aqui vira a lista do próximo ciclo de desenvolvimento do app. Não escreva CPF, nome de pessoa atendida ou dado real de caso.</div>
    <div id="avisoEnvio"></div>
    <form id="formFeedback" novalidate>
      <section class="bloco"><h2>1. Quem responde</h2>
        <div class="grade2"><div class="campo"><label for="nome">Seu nome *</label><input type="text" id="nome" autocomplete="name" required></div>
          <div class="campo"><label for="setor">Setor</label><input type="text" id="setor" autocomplete="organization"></div></div>
        <div class="campo"><span class="rotulo" id="rotPapel">Você é *</span>
          ${radios("papel", [["equipe", "Integrante da equipe do app"], ["usuario", "Servidor do setor que vai usar"], ["outro", "Outro"]], true)}</div>
      </section>
      <section class="bloco"><h2>2. Visão geral</h2>
        <div class="campo"><span class="rotulo">O app resolve o problema do processo? *</span>
          ${radios("nota", [["1", "1 · não resolve"], ["2", "2"], ["3", "3 · em parte"], ["4", "4"], ["5", "5 · resolve"]], true)}</div>
        <div class="campo"><span class="rotulo">Você usaria no trabalho? *</span>
          ${radios("usaria", [["sim", "Sim, como está"], ["ajustes", "Sim, com ajustes"], ["nao", "Não"]], true)}</div>
      </section>
      <section class="bloco"><h2>3. Tela por tela</h2>
        <p class="ajuda">Para cada tela que você abriu, diga se funciona e o que mudaria. Deixe "Não testei" nas que não abriu.</p>
        ${C.telas.map((t, i) => `<div class="tela"><div class="nome">${esc(t.titulo)} <span class="rota">${esc(t.rota)}</span></div>
          ${t.descricao ? `<div class="desc">${esc(t.descricao)}</div>` : ""}
          <label class="rotulo" for="tela_sit_${i}" style="font-weight:500">Situação</label>
          <select id="tela_sit_${i}">${SITUACOES.map(([v, txt]) => `<option value="${v}">${esc(txt)}</option>`).join("")}</select>
          <textarea id="tela_com_${i}" aria-label="O que mudaria na tela ${esc(t.titulo)}" placeholder="O que mudaria nesta tela? (campo, botão, texto, ordem, regra)"></textarea></div>`).join("")}
      </section>
      <section class="bloco"><h2>4. O que falta e o que está errado</h2>
        <div class="campo"><label for="falta">O que o app ainda não faz e precisa fazer</label>
          <textarea id="falta" placeholder="Ex.: gerar o relatório mensal em PDF; avisar por e-mail quando o prazo vencer"></textarea></div>
        <div class="campo"><label for="erros">Erros que você encontrou</label>
          <textarea id="erros" placeholder="O que você fez, o que esperava e o que aconteceu"></textarea></div>
        <div class="campo"><label for="regras">Campo, regra, nome ou número que não bate com o processo real</label>
          <textarea id="regras" placeholder="Ex.: o prazo é de 10 dias úteis, e não de 15; o setor se chama..."></textarea></div>
      </section>
      <section class="bloco"><h2>5. Prioridades</h2>
        <p class="ajuda">As três mudanças mais importantes, da mais para a menos importante.</p>
        ${[1, 2, 3].map(n => `<div class="campo"><label for="prio${n}">${n}ª prioridade</label><input type="text" id="prio${n}"></div>`).join("")}
      </section>
      <section class="bloco"><h2>6. Próximo passo</h2>
        <div class="campo"><span class="rotulo">O setor topa um piloto com o app?</span>
          ${radios("piloto", [["sim", "Sim"], ["talvez", "Talvez, depois dos ajustes"], ["nao", "Não"]], false)}</div>
        <div class="campo"><label for="obs">Observações</label><textarea id="obs"></textarea></div>
      </section>
      <div id="errosForm"></div>
      <div class="acoes"><button class="prim" type="submit" id="btnEnviar">Enviar o feedback</button>
        <button class="sec" type="button" id="btnBaixar">Baixar as respostas (.json)</button>
        <small id="estadoRascunho" style="color:var(--ink-faint)"></small></div>
    </form>`;
  restaurarRascunho();
  $("#formFeedback").addEventListener("input", salvarRascunho);
  $("#formFeedback").addEventListener("change", salvarRascunho);
  $("#formFeedback").addEventListener("submit", enviar);
  $("#btnBaixar").addEventListener("click", () => baixar(`feedback-${C.app}.json`, JSON.stringify(coletar(), null, 2)));
  firebase().then(() => {}).catch(e => avisoEnvio("info", `Sem conexão com o Firestore (${esc(e.message)}). Você pode responder: o rascunho fica salvo neste navegador e, no fim, o botão "Baixar as respostas" gera o arquivo para enviar ao professor.`));
}

const valor = id => ($("#" + id)?.value || "").trim();
const marcado = nome => document.querySelector(`input[name="${nome}"]:checked`)?.value || "";
function coletar(){
  return {
    app: C.app, projeto: C.titulo, equipe: C.equipe,
    aluno: valor("nome"), setor: valor("setor"), papel: marcado("papel"),
    nota: Number(marcado("nota")) || null, usaria: marcado("usaria"),
    telas: C.telas.map((t, i) => ({rota: t.rota, titulo: t.titulo, situacao: valor("tela_sit_" + i), comentario: valor("tela_com_" + i)}))
      .filter(t => t.situacao || t.comentario),
    falta: valor("falta"), erros: valor("erros"), regras: valor("regras"),
    prioridades: [valor("prio1"), valor("prio2"), valor("prio3")].filter(Boolean),
    piloto: marcado("piloto"), observacoes: valor("obs"),
    versao_formulario: 1, navegador: navigator.userAgent.slice(0, 160)
  };
}
const CHAVE = () => "feedback:rascunho:" + C.app;
function salvarRascunho(){
  localStorage.setItem(CHAVE(), JSON.stringify(coletar()));
  $("#estadoRascunho").textContent = "Rascunho salvo neste navegador.";
}
function restaurarRascunho(){
  let d; try { d = JSON.parse(localStorage.getItem(CHAVE()) || "null"); } catch (e) { d = null; }
  if (!d) return;
  for (const [id, k] of [["nome", "aluno"], ["setor", "setor"], ["falta", "falta"], ["erros", "erros"], ["regras", "regras"], ["obs", "observacoes"]]) if ($("#" + id)) $("#" + id).value = d[k] || "";
  (d.prioridades || []).forEach((p, i) => { if ($("#prio" + (i + 1))) $("#prio" + (i + 1)).value = p; });
  for (const nome of ["papel", "nota", "usaria", "piloto"]){
    const v = nome === "nota" ? String(d.nota || "") : d[nome];
    const el = document.querySelector(`input[name="${nome}"][value="${CSS.escape(v || "")}"]`); if (el) el.checked = true;
  }
  for (const t of d.telas || []){
    const i = C.telas.findIndex(x => x.rota === t.rota); if (i < 0) continue;
    $("#tela_sit_" + i).value = t.situacao || ""; $("#tela_com_" + i).value = t.comentario || "";
  }
  $("#estadoRascunho").textContent = "Rascunho recuperado deste navegador.";
}
function avisoEnvio(tipo, html){ $("#avisoEnvio").innerHTML = `<div class="aviso ${tipo}" role="${tipo === "erro" ? "alert" : "status"}">${html}</div>`; }
function baixar(nome, texto){
  const a = document.createElement("a"); a.href = URL.createObjectURL(new Blob([texto], {type: "application/json"})); a.download = nome; a.click();
  setTimeout(() => URL.revokeObjectURL(a.href), 2000);
}
async function enviar(ev){
  ev.preventDefault();
  const d = coletar(), erros = [];
  if (!d.aluno) erros.push("Informe o seu nome.");
  if (!d.papel) erros.push("Diga se você é da equipe, usuário do setor ou outro.");
  if (!d.nota) erros.push("Dê a nota de 1 a 5.");
  if (!d.usaria) erros.push("Diga se usaria o app no trabalho.");
  if (!d.telas.length && !d.falta && !d.erros && !d.prioridades.length) erros.push("Avalie pelo menos uma tela ou escreva o que falta.");
  const textos = [d.falta, d.erros, d.regras, d.observacoes, ...d.prioridades, ...d.telas.map(t => t.comentario)].join(" ");
  if (CPF.test(textos)) erros.push("Algum campo tem um número com formato de CPF. Apague antes de enviar.");
  $("#errosForm").innerHTML = erros.length ? `<div class="aviso erro" role="alert"><b>Antes de enviar:</b><ul>${erros.map(e => `<li>${esc(e)}</li>`).join("")}</ul></div>` : "";
  if (erros.length) return $("#errosForm").scrollIntoView({block: "center"});
  const btn = $("#btnEnviar"); btn.disabled = true; btn.textContent = "Enviando…";
  try {
    const {fs, db} = await firebase();
    const ref = await fs.addDoc(fs.collection(db, COLECAO_FEEDBACK), {...d, criadoEm: fs.serverTimestamp()});
    localStorage.removeItem(CHAVE());
    avisoEnvio("ok", `<b>Feedback enviado.</b> Obrigado! Protocolo <span style="font-family:monospace">${esc(ref.id)}</span>. Se quiser, responda de novo depois de testar mais telas.`);
    $("#formFeedback").reset(); window.scrollTo({top: 0, behavior: "smooth"});
  } catch (e){
    avisoEnvio("erro", `Não consegui enviar ao Firestore (${esc(e.message)}). As respostas continuam salvas neste navegador. Clique em <b>Baixar as respostas (.json)</b> e envie o arquivo ao professor.`);
  } finally { btn.disabled = false; btn.textContent = "Enviar o feedback"; }
}

/* ================= página de respostas (professor) ================= */
const ROTULO_SIT = Object.fromEntries(SITUACOES);
const SELO_SIT = {ok: "ok", ajuste: "alerta", erro: "erro"};
async function montarRespostas(){
  $("#topo").innerHTML = `<div class="wrap"><div class="kicker">Curso POLITEC/MT · Feedback dos apps</div><h1>Respostas por app</h1>
    <p>Lidas da coleção <span style="font-family:monospace">${COLECAO_FEEDBACK}</span> do Firestore. Para gerar o <span style="font-family:monospace">FEEDBACK.md</span> de cada app, rode <span style="font-family:monospace">python Apps/_base/baixar_feedback.py</span>.</p>
    <div class="barra"><button type="button" id="btnTema">Tema claro ou escuro</button><button type="button" id="btnJson">Baixar tudo (.json)</button></div></div>`;
  $("#btnTema").addEventListener("click", trocarTema);
  $("#conteudo").innerHTML = `<div class="bloco">Carregando…</div>`;
  let lista = [];
  try {
    const {fs, db} = await firebase();
    const snap = await fs.getDocs(fs.collection(db, COLECAO_FEEDBACK));
    lista = snap.docs.map(d => ({id: d.id, ...d.data(), criadoEm: d.data().criadoEm?.toDate?.()?.toISOString() || ""}));
  } catch (e){ $("#conteudo").innerHTML = `<div class="aviso erro">Não consegui ler o Firestore: ${esc(e.message)}</div>`; }
  $("#btnJson").addEventListener("click", () => baixar("feedback_apps.json", JSON.stringify(lista, null, 2)));
  const porApp = {};
  for (const r of lista) (porApp[r.app] = porApp[r.app] || []).push(r);
  const media = rs => { const n = rs.filter(r => r.nota); return n.length ? (n.reduce((a, r) => a + r.nota, 0) / n.length).toFixed(1).replace(".", ",") : "—"; };
  $("#conteudo").innerHTML = `<div class="bloco"><h2>Resumo</h2><p class="ajuda">${lista.length} resposta(s) em ${Object.keys(porApp).length} de ${C.apps.length} apps.</p>
      <table><tr><th>App</th><th>Equipe</th><th class="num">Respostas</th><th class="num">Nota média</th><th>Formulário</th></tr>
      ${C.apps.map(a => `<tr><td><a href="#app-${esc(a.app)}">${esc(a.titulo)}</a></td><td>${esc(a.equipe)}</td><td class="num">${(porApp[a.app] || []).length}</td>
        <td class="num">${media(porApp[a.app] || [])}</td><td><a href="${esc(a.app)}.html">abrir</a></td></tr>`).join("")}</table></div>
    ${C.apps.filter(a => porApp[a.app]).map(a => `<section class="bloco" id="app-${esc(a.app)}"><h2>${esc(a.titulo)}</h2>
      ${porApp[a.app].sort((x, y) => y.criadoEm.localeCompare(x.criadoEm)).map(r => `<details><summary>${esc(r.aluno)} · ${esc(r.papel)} · nota ${esc(r.nota ?? "—")} · ${esc(r.criadoEm.slice(0, 16).replace("T", " "))}</summary>
        <p>Usaria: <b>${esc(r.usaria)}</b> · Piloto: <b>${esc(r.piloto || "—")}</b>${r.setor ? " · Setor: " + esc(r.setor) : ""}</p>
        ${(r.prioridades || []).length ? `<p><b>Prioridades:</b></p><ol>${r.prioridades.map(p => `<li>${esc(p)}</li>`).join("")}</ol>` : ""}
        ${(r.telas || []).length ? `<table><tr><th>Tela</th><th>Situação</th><th>Comentário</th></tr>${r.telas.map(t => `<tr><td>${esc(t.titulo)}</td>
          <td>${t.situacao ? `<span class="selo ${SELO_SIT[t.situacao] || ""}">${esc(ROTULO_SIT[t.situacao])}</span>` : ""}</td><td>${esc(t.comentario)}</td></tr>`).join("")}</table>` : ""}
        ${[["O que falta", r.falta], ["Erros", r.erros], ["Regras e nomes", r.regras], ["Observações", r.observacoes]].filter(x => x[1]).map(([t, v]) => `<p><b>${t}:</b> ${esc(v)}</p>`).join("")}
      </details>`).join("")}</section>`).join("")}`;
}

if (C.modo === "respostas") montarRespostas(); else montarFormulario();
