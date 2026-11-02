/* Identidade da Comissão de Ética.
   Entra por último no build. A tela-assinatura é o funil do processo ético, com
   o dossiê marcado “Reservado” e a barra de etapas em todas as telas do caso. */

const CE_FUNIL = ["registro", "classificação", "admissibilidade", "oitivas", "deliberação", "recomendações", "encerrado"];
TELAS["#/painel"] = async ()=>{
  const ds = await db.list("denuncias");
  const filtro = estado.ceEtapa || "";
  const vis = (filtro ? ds.filter(d=>d.etapa === filtro) : ds).sort((a, b)=>String(b.data_recebimento).localeCompare(String(a.data_recebimento)));
  const total = ds.length || 1;
  return `<h1>Funil do processo ético</h1>
    <p class="sub">${ds.length} casos. Cada etapa é clicável e filtra a lista. <a href="#/denuncia/nova">Registrar denúncia</a></p>
    <div class="card ce-funil"><div class="ce-funil-trilho">${CE_FUNIL.map((e, i)=>{
      const n = ds.filter(d=>d.etapa === e).length, pct = Math.round(n / total * 100);
      return `<button type="button" class="ce-etapa ${filtro === e ? "escolhida" : ""} ${n ? "" : "zero"}" data-ce-etapa="${e}">
        <span class="ce-etapa-nome">${i + 1}. ${esc(e)}</span>
        <span class="ce-etapa-num" data-etapa-qtd="${e}">${n}</span>
        <span class="ce-etapa-barra"><i style="width:${pct}%"></i></span></button>`;
    }).join("")}</div>
    ${filtro ? `<p class="sub">Filtrando por <b>${esc(filtro)}</b>. <button type="button" class="ce-limpar" id="btnCeLimpar">Ver o funil inteiro</button></p>` : ""}</div>
    <div class="card tabela-wrap"><table><tr><th>Protocolo</th><th>Recebida em</th><th>Canal</th><th>Etapa</th><th>Situação</th></tr>
      ${vis.map(d=>`<tr><td><a href="#/caso/${encodeURIComponent(d.id)}">${esc(d.protocolo)}</a></td>
        <td>${dataCurtaBR(d.data_recebimento)}</td><td>${esc(d.canal)}</td><td><span class="selo info">${esc(d.etapa)}</span></td><td>${esc(d.situacao)}</td></tr>`).join("") || '<tr><td colspan="5" class="vazio">Nenhum caso nesta etapa.</td></tr>'}</table></div>`;
};
TELAS_DEPOIS["#/painel"] = ()=>{
  $$("[data-ce-etapa]").forEach(b=>b.addEventListener("click", ()=>{ estado.ceEtapa = estado.ceEtapa === b.dataset.ceEtapa ? "" : b.dataset.ceEtapa; navegar(); }));
  $("#btnCeLimpar")?.addEventListener("click", ()=>{ estado.ceEtapa = ""; navegar(); });
};

/* ---------- dossiê com a barra de etapas em todas as telas do caso ---------- */
const CE_TELAS = {caso: 0, classificacao: 1, admissibilidade: 2, oitivas: 3, documentos: 4, encerramento: 5};
const CE_ROTAS = {caso: "", classificacao: "/classificacao", admissibilidade: "/admissibilidade", oitivas: "/oitivas", documentos: "/documentos", encerramento: "/encerramento"};
const CE_NOMES = ["Registro", "Classificação", "Admissibilidade", "Oitivas", "Documentos", "Encerramento"];
async function ceDossie(id, atual){
  const d = await db.get("denuncias", id);
  if (!d) return "";
  const idx = CE_TELAS[atual] ?? 0;
  const base = "#/caso/" + encodeURIComponent(id);
  return `<div class="card ce-dossie"><div class="ce-selo" aria-label="Conteúdo reservado">Reservado</div>
    <div class="ce-dossie-info"><span class="sub">Dossiê do processo ético</span><h2>${esc(d.protocolo)}</h2>
      <p class="sub">Conteúdo restrito à Comissão de Ética. ${esc(d.categoria ? "Categoria: " + d.categoria : "")}</p></div>
    <div class="etapas ce-etapas">${CE_NOMES.map((nome, i)=>{
      const suf = Object.keys(CE_ROTAS).find(k=>CE_TELAS[k] === i);
      const cls = i < idx ? "feita" : i === idx ? "atual" : "";
      return `<span class="${cls}"><a href="${base}${suf ? CE_ROTAS[suf] : ""}">${nome}</a></span>`;
    }).join("")}</div></div>`;
}
for (const [chave, atual] of Object.entries(CE_TELAS)){
  const rota = chave === "caso" ? "#/caso/:id" : "#/caso/:id/" + chave;
  const antes = TELAS[rota];
  if (typeof antes !== "function") continue;
  TELAS[rota] = async (p)=>{
    const html = await antes(p);
    return (await ceDossie(p.id, chave)) + html;
  };
}
