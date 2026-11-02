/* Identidade do Metas pelo BI.
   Entra por último no build. A tela-assinatura é o ano em 12 meses com a
   situação de cada mês; as três telas do fluxo ganham os passos 1-2-3. */

const METAS_MESES = ["janeiro", "fevereiro", "março", "abril", "maio", "junho", "julho", "agosto", "setembro", "outubro", "novembro", "dezembro"];
function metasPassos(atual){
  const itens = [["1", "Importar o mês"], ["2", "Conferir"], ["3", "Gerar planilha"]];
  return `<ol class="metas-passos">${itens.map(([n, t], i)=>{
    const num = i + 1, cls = num < atual ? "feito" : num === atual ? "atual" : "";
    return `<li class="${cls}"><span class="n">${num < atual ? "✓" : n}</span><span>${t}</span></li>`;
  }).join("")}</ol>`;
}
async function metasAno(){
  const rels = await db.list("relatorios");
  const porMes = Object.fromEntries(rels.map(r=>[r.id || r.mes, r]));
  const ano = new Date().getFullYear();
  return `<div class="card metas-ano"><div class="metas-ano-topo"><div><span class="sub">Ano de ${ano}</span>
      <h2>Situação de cada mês</h2></div><p class="sub" style="margin:0">Verde: gerado · azul: conferido · âmbar: importado e a conferir.</p></div>
    <div class="metas-meses">${METAS_MESES.map((nome, i)=>{
      const mes = `${ano}-${String(i + 1).padStart(2, "0")}`, r = porMes[mes];
      const estado = !r ? "vazio" : r.gerado_em ? "gerado" : r.aprovado_em ? "conferido" : "importado";
      const rot = !r ? "sem relatório" : r.gerado_em ? "gerado" : r.aprovado_em ? "conferido" : "importado";
      const href = !r ? "#/importar" : r.gerado_em ? "#/exportar/" + mes : r.aprovado_em ? "#/exportar/" + mes : "#/conferencia/" + mes;
      return `<a class="metas-mes ${estado}" href="${href}" title="${nome} de ${ano} · ${rot}">
        <b>${nome.slice(0, 3)}</b><span>${rot}</span></a>`;
    }).join("")}</div></div>`;
}

const metasImportarAntes = TELAS["#/importar"];
TELAS["#/importar"] = async (p)=>{
  const html = await metasImportarAntes(p);
  return `<h1>Importar o mês</h1>${metasPassos(1)}` + (await metasAno()) + html.replace(/<h1>[^<]*<\/h1>/, "");
};
const metasImportarDepoisAntes = TELAS_DEPOIS["#/importar"];
TELAS_DEPOIS["#/importar"] = async (p)=>{
  await metasImportarDepoisAntes?.(p);
  const alvo = $("#resMes");
  if (!alvo) return;
  let t = null;
  new MutationObserver(()=>{
    clearTimeout(t);
    t = setTimeout(async ()=>{
      const novo = await metasAno(), atual = document.querySelector(".metas-ano");
      if (atual) atual.outerHTML = novo;
    }, 100);
  }).observe(alvo, {childList: true, subtree: true});
};

const metasConfAntes = TELAS["#/conferencia/:mes"];
TELAS["#/conferencia/:mes"] = async (p)=>{
  const html = await metasConfAntes(p);
  return html.replace(/(<h1>)/, metasPassos(2) + "$1");
};
const metasExportAntes = TELAS["#/exportar/:mes"];
TELAS["#/exportar/:mes"] = async (p)=>{
  const html = await metasExportAntes(p);
  return html.replace(/(<h1>)/, metasPassos(3) + "$1");
};
const metasExportDepoisAntes = TELAS_DEPOIS["#/exportar/:mes"];
TELAS_DEPOIS["#/exportar/:mes"] = async (p)=>{
  await metasExportDepoisAntes?.(p);
  const marcar = async ()=>{
    const r = await db.get("relatorios", p.mes);
    if (r && !r.gerado_em){ await db.put("relatorios", {...r, gerado_em: agora()}); }
  };
  $("#btnCsv")?.addEventListener("click", ()=>setTimeout(marcar, 200));
  $("#btnXlsx")?.addEventListener("click", ()=>setTimeout(marcar, 200));
};
