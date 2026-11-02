/* Identidade do Mapa de Distribuição.
   Entra por último no build. A tela-assinatura é a esteira das 8 etapas, fixa
   em todas as telas do processo, e a grade em formato planilha. */

const MAPA_ETAPAS = [["importar", "Importar"], ["mapa", "Mapa"], ["resultado", "Resultado"], ["empresas", "Empresas"],
  ["conferencia", "Conferência"], ["orcamento", "Orçamentária"], ["exportar", "Exportar"], ["auditoria", "Auditoria"]];
function mapaEtapas(proc, atual){
  return `<nav class="mapa-passos" aria-label="Etapas do processo">
    <a class="mapa-voltar" href="#/processos">← Processos</a>
    ${MAPA_ETAPAS.map(([id, nome], i)=>`<a href="#/${id}/${encodeURIComponent(proc)}" class="${id === atual ? "atual" : ""}">
      <span class="n">${i + 1}</span>${nome}</a>`).join("")}</nav>`;
}

for (const [id, nome] of MAPA_ETAPAS){
  const rota = "#/" + id + "/:proc";
  const antes = TELAS[rota];
  if (typeof antes !== "function") continue;
  TELAS[rota] = async (p)=>{
    const html = await antes(p);
    return mapaEtapas(p.proc, id) + html;
  };
}
