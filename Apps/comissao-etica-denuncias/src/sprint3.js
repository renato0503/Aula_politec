/* ================= Sprint 3 · Classificação assistida (RN02) ================= */
// Sem internet e sem enviar o relato para fora: as categorias têm palavras (raízes) e o app pontua o relato.
const CATEGORIAS_PADRAO = dadosEmbutidos("seed")?.categorias || [];
async function categoriasAtivas(){ const c = await db.list("categorias"); return c.length ? c : CATEGORIAS_PADRAO; }

// [{id, nome, pontos, palavras: [encontradas]}], da maior para a menor pontuação
function pontuar(relato, categorias){
  const txt = normalizar(relato);
  return categorias.map(c=>{
    const achadas = c.palavras.filter(p=>txt.includes(normalizar(p)));
    const pontos = achadas.reduce((a, p)=>a + txt.split(normalizar(p)).length - 1, 0);
    return {id: c.id, nome: c.nome, artigos: c.artigos, pontos, palavras: achadas};
  }).filter(x=>x.pontos > 0).sort((a, b)=>b.pontos - a.pontos || a.nome.localeCompare(b.nome));
}
teste("os 10 casos do exemplo têm a categoria esperada entre as 3 sugestões", ()=>{
  const s = dadosEmbutidos("seed"), erros = s.denuncias.filter(d=>!pontuar(d.relato, s.categorias).slice(0, 3).some(x=>x.id === d.categoria_esperada)).map(d=>d.id);
  return !erros.length || "fora do top 3: " + erros.join(", ");
});
// o prompt sai sem os nomes das partes
function semNomes(texto, d){
  let t = texto;
  for (const [nome, rot] of [[d.denunciante, "[DENUNCIANTE]"], [d.denunciado, "[DENUNCIADO]"]]){
    if (!nome) continue;
    t = t.split(nome).join(rot);
    nome.split(/\s+/).filter(p=>p.length > 3).forEach(p=>{ t = t.replace(new RegExp(`\\b${p.replace(/[.*+?^${}()|[\]\\]/g, "\\$&")}\\b`, "gi"), rot); });
  }
  return t;
}
teste("prompt sem os nomes das partes", ()=> !semNomes("Fulano Silva gritou com Beltrana", {denunciante: "Beltrana Souza", denunciado: "Fulano Silva"}).match(/Fulano|Beltrana|Silva/));
function montarPrompt(d, categorias){
  return `Você apoia a triagem da Comissão de Ética da POLITEC/MT. Não decida a admissibilidade: só sugira.
Classifique o relato abaixo em até 3 categorias da lista, da mais para a menos provável, e para cada uma cite o trecho do relato que a justifica.

Categorias (Código de Ética Funcional do Servidor Público Civil de MT, LC nº 112/2002):
${categorias.map((c, i)=>`${i + 1}. ${c.nome} (${c.artigos})`).join("\n")}

Relato (nomes substituídos):
"""${semNomes(d.relato, d)}"""

Responda em tópicos: categoria · trecho · grau de confiança (baixo, médio, alto).`;
}

TELAS["#/caso/:id/classificacao"] = async ({id})=>{
  const d = await db.get("denuncias", id);
  if (!d) return `<div class="card vazio">Caso não encontrado.</div>`;
  const cats = await categoriasAtivas(), sug = pontuar(d.relato, cats).slice(0, 3);
  const feita = (await db.porIndice("classificacoes", "denuncia_id", id)).filter(c=>c.confirmada).pop();
  if (d.etapa === "registro") await db.put("denuncias", {...d, etapa: "classificação"});
  let rel = esc(d.relato);
  sug.flatMap(s=>s.palavras).forEach(p=>{ rel = rel.replace(new RegExp(`(${p.replace(/[.*+?^${}()|[\]\\]/g, "\\$&")}[\\wÀ-ú]*)`, "gi"), "<mark>$1</mark>"); });
  return `<h1>Classificação · ${esc(d.protocolo)}</h1><p class="sub">Sugestão por regras, sem enviar o relato para fora. A classificação só vale depois da confirmação de um membro (RN02).</p>
    <div class="card"><h2 style="margin-top:0">Relato</h2><p style="white-space:pre-wrap">${rel}</p></div>
    <div class="card"><h2 style="margin-top:0">Sugestões</h2>${sug.length ? `<ol id="sugestoes">${sug.map(s=>`<li data-cat="${esc(s.id)}"><b>${esc(s.nome)}</b> · ${s.pontos} ocorrência(s)
      <br><small class="sub">Palavras: ${s.palavras.map(esc).join(", ")} · ${esc(s.artigos)}</small></li>`).join("")}</ol>` : '<p class="sub" id="sugestoes">Nenhuma palavra das categorias aparece no relato. Classifique manualmente.</p>'}</div>
    <details class="card"><summary><b>Usar uma ferramenta de IA autorizada (opcional)</b></summary>
      <p class="sub">O prompt sai sem os nomes das partes. Cole a resposta abaixo; ela fica registrada como apoio à decisão.</p>
      <textarea id="promptIA" rows="10" readonly>${esc(montarPrompt(d, cats))}</textarea>
      <div class="linha-botoes"><button id="btnCopiarPrompt">Copiar prompt</button></div>
      ${campo("respostaIA", "Resposta da ferramenta de IA", {tipo: "textarea", linhas: 4})}</details>
    ${feita ? `<div class="card" id="classificacaoFeita"><b>Classificação confirmada:</b> ${esc(cats.find(c=>c.id === feita.categoria_final)?.nome || feita.categoria_final)}
      por ${esc(feita.membro)} em ${dataBR(feita.data)}<br><small>${esc(feita.justificativa)}</small></div>` : ""}
    ${["presidente", "membro"].includes(estado.perfil) ? `<form class="card" id="formClassif"><h2 style="margin-top:0">${feita ? "Reclassificar" : "Confirmar"}</h2>
      ${campo("cCategoria", "Categoria", {tipo: "select", opcoes: [["", "Escolha"], ...cats.map(c=>[c.id, c.nome])], valor: sug[0]?.id || ""})}
      ${campo("cJustificativa", "Justificativa (mínimo de 20 caracteres)", {tipo: "textarea", linhas: 3})}
      <div id="errosClassif"></div><div class="linha-botoes"><button class="prim" type="submit">Confirmar classificação</button></div></form>` : ""}`;
};
TELAS_DEPOIS["#/caso/:id/classificacao"] = ({id})=>{
  $("#btnCopiarPrompt")?.addEventListener("click", async ()=>{ try { await navigator.clipboard.writeText($("#promptIA").value); toast("Prompt copiado."); } catch(e){ $("#promptIA").select(); toast("Use Ctrl+C."); } });
  $("#formClassif")?.addEventListener("submit", async e=>{
    e.preventDefault();
    const cat = valorDe("cCategoria"), just = valorDe("cJustificativa");
    const erros = [!cat && "Escolha a categoria.", just.length < 20 && "Escreva a justificativa da classificação (RN02)."].filter(Boolean);
    if (!mostrarErros("#errosClassif", erros)) return;
    const d = await db.get("denuncias", id), sug = pontuar(d.relato, await categoriasAtivas()).slice(0, 3), resposta = valorDe("respostaIA");
    await db.put("classificacoes", {id: uuid(), denuncia_id: id, sugeridas: sug.map(s=>s.id), palavras: Object.fromEntries(sug.map(s=>[s.id, s.palavras])),
      origem: resposta ? "regras + IA externa" : "regras", resposta_ia: resposta, confirmada: true, categoria_final: cat, justificativa: just, membro: estado.perfil, data: agora(),
      acertou_sugestao: sug[0]?.id === cat});
    await db.put("denuncias", {...d, etapa: d.etapa === "classificação" || d.etapa === "registro" ? "admissibilidade" : d.etapa, categoria: cat});
    await trilha("classificação confirmada", id, just); toast("Classificação confirmada."); location.hash = "#/caso/" + encodeURIComponent(id);
  });
};

/* ---- categorias editáveis (a Comissão confere com o Código de Ética) ---- */
async function configExtra(){
  const cats = await categoriasAtivas();
  return `<div class="card"><h2 style="margin-top:0">Categorias e palavras da classificação</h2>
    <p class="sub">Proposta inicial para a Comissão conferir com o Código de Ética. Palavras separadas por vírgula; vale o começo da palavra (ex.: "humilh" acha humilhou e humilhação).</p>
    ${cats.map(c=>`<div class="campos" style="align-items:end">${campo("catNome-" + c.id, "Categoria", {valor: c.nome})}${campo("catArt-" + c.id, "Artigos", {valor: c.artigos})}
      ${campo("catPal-" + c.id, "Palavras", {valor: c.palavras.join(", ")})}</div>`).join("")}
    <div class="linha-botoes"><button id="btnSalvarCats">Salvar categorias</button></div></div>`;
}
async function ligarConfigExtra(){
  $("#btnSalvarCats")?.addEventListener("click", async ()=>{
    for (const c of await categoriasAtivas())
      await db.put("categorias", {...c, nome: valorDe("catNome-" + c.id), artigos: valorDe("catArt-" + c.id), palavras: valorDe("catPal-" + c.id).split(",").map(s=>s.trim()).filter(Boolean)});
    await trilha("categorias alteradas", null); toast("Categorias salvas.");
  });
}
