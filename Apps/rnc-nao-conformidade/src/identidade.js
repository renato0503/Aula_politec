/* Identidade das Não Conformidades.
   Entra por último no build. A tela-assinatura é o quadro por etapa do ciclo,
   com o setor como contexto do perfil. */

const RNC_COLUNAS = [["validação", "Validação", "5 dias"], ["plano", "Plano de ação", "30 dias"],
  ["avaliação", "Avaliação", "15 dias"], ["encerramento", "Encerramento", "—"]];
function rncEtapaAtual(r, etapas){
  const e = etapas.filter(x=>x.rnc === r.numero).sort((a, b)=>(a.inicio + a.id).localeCompare(b.inicio + b.id)).filter(x=>!x.fim).pop();
  return e ? e.etapa : r.etapa;
}
async function rncQuadro(){
  const [rs, es, setores] = await Promise.all([db.list("rncs"), db.list("etapas"), db.list("setores")]);
  const nomeSetor = Object.fromEntries(setores.map(s=>[s.sigla, s.nome || s.sigla]));
  const hoje = hojeISO();
  const por = Object.fromEntries(RNC_COLUNAS.map(([id])=>[id, []]));
  rs.filter(r=>!["anulada", "encerrada", "encaminhada à corregedoria"].includes(r.situacao)).forEach(r=>{
    const et = rncEtapaAtual(r, es);
    (por[et] || por["validação"]).push(r);
  });
  const card = r=>{
    const e = es.filter(x=>x.rnc === r.numero && !x.fim).pop();
    const atrasada = e && e.prazo && e.prazo < hoje;
    return `<a class="rnc-card ${atrasada ? "atrasada" : ""}" href="#/rnc/${encodeURIComponent(r.numero)}">
      <span class="rnc-card-topo"><b class="mono">${esc(r.numero)}</b>${atrasada ? '<span class="selo erro">vencida</span>' : ""}</span>
      <span class="rnc-card-desc" title="${esc(r.descricao || "")}">${esc(r.descricao || "Sem descrição")}</span>
      <span class="sub">${esc(nomeSetor[r.setor_notificado] || r.setor_notificado || "")}</span>
      <span class="sub">${esc(r.categoria || "")}${e?.prazo ? " · prazo " + dataCurtaBR(e.prazo) : ""}</span></a>`;
  };
  return `<div class="card rnc-quadro-card"><div class="rnc-quadro-topo"><div><span class="sub">Ciclo da RNC</span>
      <h2>Quadro por etapa <span class="conta">${rs.length}</span></h2></div>
      <p class="sub" style="margin:0">Cada coluna é uma etapa; o cartão vermelho está com o prazo vencido.</p></div>
    <div class="rnc-quadro">${RNC_COLUNAS.map(([id, titulo, prazo])=>`<section class="rnc-col">
      <h3>${titulo} <span class="conta">${por[id].length}</span></h3>
      <p class="sub rnc-prazo">${prazo === "—" ? "sem prazo próprio" : "prazo de " + prazo}</p>
      <div class="rnc-col-lista">${por[id].map(card).join("") || '<p class="sub">Nenhuma RNC.</p>'}</div></section>`).join("")}</div></div>`;
}

const rncPainelAntes = TELAS["#/painel"];
TELAS["#/painel"] = async ()=>{
  const html = await rncPainelAntes();
  const quadro = await rncQuadro();
  const doc = new DOMParser().parseFromString(`<div id="rncRaiz">${html}</div>`, "text/html");
  const raiz = doc.getElementById("rncRaiz");
  if (!raiz) return html;
  const bloco = doc.createElement("div"); bloco.innerHTML = quadro;
  const h1 = raiz.querySelector("h1");
  if (h1 && h1.nextElementSibling) h1.nextElementSibling.after(bloco.firstElementChild);
  else raiz.insertBefore(bloco.firstElementChild, raiz.firstChild);
  return raiz.innerHTML;
};

/* o setor escolhido no menu do perfil vira o setor da tela “Minhas RNCs” */
const rncMinhasAntes = TELAS["#/minhas"];
if (typeof rncMinhasAntes === "function"){
  TELAS["#/minhas"] = async (p)=>{
    if (estado.contexto){ await db.meta("setor", estado.contexto); await db.meta("meu_setor", estado.contexto); }
    return rncMinhasAntes(p);
  };
}
