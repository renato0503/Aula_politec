/* Identidade das Inscrições em Cursos.
   Entra por último no build. A tela-assinatura são os cartões de curso com a
   esteira Divulgar → Turma; o curso ganha uma tela central com os passos. */

const INC_PASSOS = [["Divulgar", "#/divulgar/"], ["Importar", "#/importar"], ["Inscritos", "#/inscritos/"],
  ["Triagem", "#/triagem"], ["Convocação", "#/convocacao/"], ["Turma", "#/turma/"]];
function incEsteira(id){
  return `<div class="inc-esteira">${INC_PASSOS.map(([nome, rota], i)=>{
    const href = rota.endsWith("/") ? rota + encodeURIComponent(id) : rota;
    const pronta = typeof TELAS[rota] === "function";
    return pronta ? `<a href="${href}" title="Abrir ${nome}"><span class="n">${i + 1}</span>${nome}</a>`
      : `<span class="em-breve" title="Tela ainda em construção"><span class="n">${i + 1}</span>${nome} · em breve</span>`;
  }).join("")}</div>`;
}
const incCursosAntes = TELAS["#/cursos"];
TELAS["#/cursos"] = async ()=>{
  const html = await incCursosAntes();
  const [cursos, dirs] = await Promise.all([db.list("cursos"), db.list("diretorias")]);
  const doc = new DOMParser().parseFromString(`<div id="incRaiz">${html}</div>`, "text/html");
  const raiz = doc.getElementById("incRaiz");
  if (!raiz) return html;
  const novo = doc.createElement("div"); novo.className = "linha-botoes"; novo.style.margin = "0 0 12px";
  novo.innerHTML = '<button class="prim" type="button" id="btnNovoCurso">＋ Novo curso</button>';
  const h1 = raiz.querySelector("h1"); if (h1) h1.after(novo);
  const tabela = [...raiz.querySelectorAll(".card")].find(c=>c.querySelector("table"));
  const cards = doc.createElement("div"); cards.className = "inc-cursos";
  cards.innerHTML = cursos.length ? cursos.sort((a, b)=>String(b.inicio).localeCompare(String(a.inicio))).map(c=>`
    <div class="card inc-curso">
      <a class="inc-curso-titulo" href="#/curso/${encodeURIComponent(c.id)}"><b>${esc(c.nome)}</b></a>
      <p class="sub">${esc(c.local || "")} · ${periodo(c)}</p>
      <p class="inc-curso-dados"><span class="selo ${c.status === "encerrado" ? "info" : "ok"}">${esc(c.status || "rascunho")}</span>
        <b>${totalVagas(c)}</b> vagas · inscrições até ${dataCurtaBR(c.inscricao_fim)}</p>
      ${incEsteira(c.id)}
      <div class="inc-acoes"><a class="botao prim" href="#/divulgar/${encodeURIComponent(c.id)}">Divulgar</a><button type="button" data-editar="${esc(c.id)}">Editar</button></div>
    </div>`).join("") : '<div class="card vazio">Nenhum curso. Use o formulário abaixo para cadastrar o primeiro.</div>';
  if (tabela) tabela.replaceWith(cards); else raiz.insertBefore(cards, raiz.querySelector("#formCurso"));
  return raiz.innerHTML;
};

TELAS["#/curso/:curso"] = async ({curso})=>{
  const c = await db.get("cursos", curso);
  if (!c) return `<div class="card vazio">Curso não encontrado. <a href="#/cursos">Voltar</a></div>`;
  const insc = (await db.list("inscricoes")).filter(i=>i.curso_id === curso);
  const dirs = await db.list("diretorias");
  const porDir = dirs.map(d=>({d, n: insc.filter(i=>i.diretoria === d.sigla).length}));
  return `<h1>${esc(c.nome)}</h1>
    <p class="sub">${esc(c.local || "")} · ${periodo(c)} · ${totalVagas(c)} vagas. <a href="#/cursos">Voltar aos cursos</a></p>
    <div class="card inc-centro"><h2 style="margin-top:0">Esteira do curso</h2>
      <p class="sub">Seis passos, da divulgação à turma. Clique no passo para abrir a tela.</p>
      ${incEsteira(curso)}
      <div class="inc-centro-kpis"><span><b>${insc.length}</b> inscrições</span><span><b>${totalVagas(c)}</b> vagas</span>
        <span><b>${dataCurtaBR(c.inscricao_fim)}</b> fim das inscrições</span><span><b>${dataCurtaBR(c.prazo_triagem)}</b> triagem</span></div></div>
    <div class="card"><h2 style="margin-top:0">Inscrições por diretoria</h2>
      <div class="inc-dirs">${porDir.map(({d, n})=>`<span><i>${esc(d.sigla)}</i><b>${n}</b><small>${esc(d.nome)}</small></span>`).join("")}</div></div>`;
};

/* ---------- Triagem (Diretoria): leitura das vagas e inscrições ---------- */
TELAS["#/triagem"] = async ()=>{
  const [cursos, dirs, insc, triagens] = await Promise.all([db.list("cursos"), db.list("diretorias"), db.list("inscricoes"), db.list("triagens")]);
  const dir = estado.tgDir || (dirs[0] && dirs[0].sigla) || "";
  const linhas = cursos.map(c=>{
    const doCurso = insc.filter(i=>i.curso_id === c.id);
    const daDir = doCurso.filter(i=>!dir || i.diretoria === dir);
    const vagas = Number(c.vagas_por_diretoria?.[dir] || 0);
    const tri = triagens.filter(t=>t.curso_id === c.id && (!dir || t.diretoria === dir));
    return {c, vagas, insc: daDir.length, tri: tri.length};
  }).sort((a, b)=>String(b.c.inicio).localeCompare(String(a.c.inicio)));
  const totalVagas = linhas.reduce((a, l)=>a + l.vagas, 0);
  const totalInsc = linhas.reduce((a, l)=>a + l.insc, 0);
  return `<h1>Triagem</h1><p class="sub">Vagas e inscrições por diretoria. Esta tela é de leitura: a seleção de titulares e reserva é registrada pela equipe de formação.</p>
    <div class="card"><div class="campos">${campo("tgDir", "Diretoria", {tipo: "select", opcoes: dirs.map(d=>[d.sigla, `${d.sigla} · ${d.nome}`]), valor: dir})}</div></div>
    <div class="grade"><div class="card kpi"><div class="v">${linhas.length}</div><div class="r">cursos</div></div>
      <div class="card kpi"><div class="v">${totalVagas}</div><div class="r">vagas da diretoria</div></div>
      <div class="card kpi"><div class="v">${totalInsc}</div><div class="r">inscrições da diretoria</div></div></div>
    <div class="card tabela-wrap"><table id="tabelaTriagem"><thead><tr><th>Curso</th><th>Período</th><th>Situação</th><th class="num">Vagas</th><th class="num">Inscrições</th><th class="num">Triagens</th></tr></thead>
      <tbody>${linhas.map(({c, vagas, insc, tri})=>`<tr><td><b>${esc(c.nome)}</b><br><span class="sub">${esc(c.local || "")}</span></td>
        <td>${periodo(c)}</td><td><span class="selo ${c.status === "inscrições abertas" ? "ok" : "info"}">${esc(c.status || "—")}</span></td>
        <td class="num">${vagas}</td><td class="num">${insc}</td><td class="num">${tri}</td></tr>`).join("") || '<tr><td colspan="6" class="vazio">Nenhum curso cadastrado.</td></tr>'}</tbody></table></div>`;
};
TELAS_DEPOIS["#/triagem"] = ()=>{
  $("#tgDir")?.addEventListener("change", e=>{ estado.tgDir = e.target.value; navegar(); });
};

const incCursosDepoisAntes = TELAS_DEPOIS["#/cursos"];
TELAS_DEPOIS["#/cursos"] = async ()=>{
  await incCursosDepoisAntes?.();
  $("#btnNovoCurso")?.addEventListener("click", ()=>{
    const f = $("#formCurso"); if (!f) return; f.hidden = false; f.scrollIntoView({block: "center"}); $("#cNome")?.focus();
  });
};
