/* Identidade do TAP Digital.
   Entra por último no build. A tela-assinatura é a matriz do portfólio, com o
   valor estimado no eixo vertical e a prioridade no horizontal. */

const tapReais = v => Number(v || 0).toLocaleString("pt-BR", {style: "currency", currency: "BRL"});
async function tapMatriz(){
  const [ps, pri] = await Promise.all([db.list("propostas"), db.list("portfolio")]);
  const aprovadas = ps.filter(p=>p.status === "aprovada");
  const priDe = Object.fromEntries(pri.map(x=>[x.proposta_id, Number(x.prioridade) || 0]));
  const comPrioridade = aprovadas.filter(p=>priDe[p.id]);
  const sem = aprovadas.filter(p=>!priDe[p.id]);
  const maxPri = Math.max(1, ...comPrioridade.map(p=>priDe[p.id]));
  const maxValor = Math.max(1, ...aprovadas.map(p=>Number(p.valor_estimado) || 0));
  const ponto = (p, i, semPrioridade)=>{
    const x = semPrioridade ? 100 : Math.max(4, Math.min(96, (priDe[p.id] / maxPri) * 88 + 6));
    const y = Math.max(4, Math.min(92, (Number(p.valor_estimado) || 0) / maxValor * 84 + 6));
    return `<a class="tap-ponto ${semPrioridade ? "sem" : ""}" style="left:${x}%;bottom:${y}%"
      href="#/proposta/${encodeURIComponent(p.id)}" title="${esc(p.titulo)} · ${tapReais(p.valor_estimado)}${semPrioridade ? " · sem prioridade" : " · prioridade " + priDe[p.id]}">
      <span>${esc(p.id.replace("TAP-2026-", ""))}</span></a>`;
  };
  return `<div class="card tap-matriz-card"><div class="tap-matriz-topo"><div><span class="sub">Portfólio aprovado</span>
      <h2>Matriz do portfólio <span class="conta">${aprovadas.length}</span></h2></div>
      <p class="sub" style="margin:0">Valor estimado no eixo vertical; prioridade no horizontal. Ponto tracejado é proposta aprovada sem prioridade.</p></div>
    <div class="tap-matriz"><span class="tap-eixo-y">valor estimado</span>
      <div class="tap-area">${comPrioridade.map((p, i)=>ponto(p, i, false)).join("")}${sem.map((p, i)=>ponto(p, i, true)).join("")}
        ${sem.length ? '<span class="tap-sem-linha" title="sem prioridade"></span>' : ""}</div>
      <span class="tap-eixo-x">prioridade →</span></div>
    <div class="tap-legenda"><span><i class="ok"></i>com prioridade ${comPrioridade.length}</span><span><i class="sem"></i>sem prioridade ${sem.length}</span>
      <span>maior valor: ${tapReais(maxValor)}</span></div></div>`;
}

const tapPortfolioAntes = TELAS["#/portfolio"];
TELAS["#/portfolio"] = async (p)=>{
  const html = await tapPortfolioAntes(p);
  const doc = new DOMParser().parseFromString(`<div id="tapRaiz">${html}</div>`, "text/html");
  const raiz = doc.getElementById("tapRaiz");
  if (!raiz) return html;
  const bloco = doc.createElement("div"); bloco.innerHTML = await tapMatriz();
  const h1 = raiz.querySelector("h1");
  const alvo = h1 && h1.nextElementSibling ? h1.nextElementSibling : null;
  if (alvo) alvo.after(bloco.firstElementChild); else raiz.insertBefore(bloco.firstElementChild, raiz.firstChild);
  return raiz.innerHTML;
};
