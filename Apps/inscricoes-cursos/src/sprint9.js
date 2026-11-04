/* ================= Sprint 10 · Perfis, instrutores e termo de convocação ================= */
function termoConvocacao(c){
  const lista = (x)=> (x && x.length ? x.join("; ") : "a informar");
  return `TERMO DE CONVOCAÇÃO

Curso: ${c.nome}
Carga horária: ${c.carga_horaria} h
Período do curso: ${periodo(c)}
Local: ${c.local || "a informar"}

Instrutores: ${lista(c.instrutores)}
Monitores: ${lista(c.monitores)}

Convocação: ${c.convocacao_data ? dataCurtaBR(c.convocacao_data) : "a informar"}
Compensação: ${c.compensacao_inicio ? dataCurtaBR(c.compensacao_inicio) : "a informar"} a ${c.compensacao_fim ? dataCurtaBR(c.compensacao_fim) : "a informar"}

A convocação e a compensação seguem as datas acima, conforme a carga horária e a disponibilidade da unidade.

Gerência de Formação Inicial e Continuada · POLITEC/MT`;
}

const inscConvocacaoAntes = TELAS["#/convocacao/:curso"];
TELAS["#/convocacao/:curso"] = async (p)=>{
  const html = await inscConvocacaoAntes(p);
  const c = await db.get("cursos", p.curso); if (!c) return html;
  const texto = termoConvocacao(c);
  return html + `<div class="card" id="cardTermoConvocacao"><h2 style="margin-top:0">Termo de convocação</h2>
    <p class="sub">Documento do curso com instrutores, monitores, convocação e compensação. A impressão e o e-mail usam o texto abaixo.</p>
    <pre id="textoTermo" style="white-space:pre-wrap;font-family:Georgia,serif;font-size:15px;line-height:1.6">${esc(texto)}</pre>
    <div class="linha-botoes nao-imprimir"><button type="button" id="btnTermoImprimir">Imprimir</button>
      <button type="button" id="btnTermoCopiar">Copiar o termo</button>
      <button type="button" id="btnTermoEmail">Enviar por e-mail</button></div>
    <p class="sub">Faltando algum dado? Preencha instrutores, monitores e as datas em <a href="#/cursos">Cursos → Editar</a>.</p></div>`;
};
const inscConvocacaoDepois = TELAS_DEPOIS["#/convocacao/:curso"];
TELAS_DEPOIS["#/convocacao/:curso"] = async (p)=>{
  await inscConvocacaoDepois?.(p);
  const texto = $("#textoTermo")?.textContent || "";
  $("#btnTermoImprimir")?.addEventListener("click", ()=>window.print());
  $("#btnTermoCopiar")?.addEventListener("click", async ()=>{ try { await navigator.clipboard.writeText(texto); toast("Termo copiado."); } catch(e){ toast("Use Ctrl+C no texto do termo."); } });
  $("#btnTermoEmail")?.addEventListener("click", ()=>{
    const c = estado.cursoTermo;
    location.href = `mailto:?subject=${encodeURIComponent("Termo de convocação")}&body=${encodeURIComponent(texto)}`;
  });
};
