/* Identidade das Inscrições em Cursos.
   Entra por último no build. A tela-assinatura são os cartões de curso com a
   esteira Divulgar → Turma; o curso ganha uma tela central com os passos. */

const INC_PASSOS = [["Divulgar", "#/divulgar/"], ["Importar", "#/importar"], ["Inscritos", "#/inscritos/"],
  ["Triagem", "#/triagem"], ["Convocação", "#/convocacao/"], ["Turma", "#/turma/"]];
function incEsteira(id){
  return `<div class="inc-esteira">${INC_PASSOS.map(([nome, rota], i)=>{
    const href = rota.endsWith("/") ? rota + encodeURIComponent(id) : rota;
    return `<a href="${href}" title="Abrir ${nome}"><span class="n">${i + 1}</span>${nome}</a>`;
  }).join("")}</div>`;
}
const incCursosAntes = TELAS["#/cursos"];
TELAS["#/cursos"] = async ()=>{
  const html = await incCursosAntes();
  const [cursos, dirs] = await Promise.all([db.list("cursos"), db.list("diretorias")]);
  const doc = new DOMParser().parseFromString(`<div id="incRaiz">${html}</div>`, "text/html");
  const raiz = doc.getElementById("incRaiz");
  if (!raiz) return html;
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
