/* ================= Sprint 9 · Organograma (Decreto nº 2.180, de 26/06/2026) =================
   Fonte: https://www.politec.mt.gov.br/documents/d/politec/politec-decreto-n-2-180-de-26-06-2026-pdf
   As cinco diretorias pedidas pela CQUAL, cada uma com as coordenadorias e as gerências/núcleos.
   "Vinculadas à diretoria" agrupa as gerências e os núcleos ligados direto à diretoria. */
const VINCULADAS = "Vinculadas à diretoria";
const ORGANOGRAMA = [
  {diretoria: "Diretoria de Criminalística", chaves: ["criminalistica"], coordenadorias: [
    {nome: "Coordenadoria de Perícias Internas", gerencias: [
      "Gerência de Perícias de Balística", "Gerência de Perícias de Documentoscopia", "Gerência de Perícias de Identificação Veicular",
      "Gerência de Perícias de Computação Forense", "Gerência de Perícias em Vestígios de Impressões de Pele",
      "Gerência de Perícias em Áudio e Vídeo", "Gerência de Perícias Contábeis e Financeiras"]},
    {nome: "Coordenadoria de Perícias Externas", gerencias: [
      "Gerência de Perícias em Crimes de Trânsito", "Gerência de Perícias em Mortes Violentas", "Gerência de Perícias em Crimes contra o Patrimônio",
      "Gerência de Perícias de Meio Ambiente", "Gerência de Perícias de Engenharia Legal", "Gerência de Perícias de Medicina Veterinária"]},
    {nome: VINCULADAS, gerencias: ["Núcleo de Apoio Operacional de Criminalística", "Núcleo de Custódia e Logística de Criminalística"]}]},
  {diretoria: "Diretoria de Medicina Legal", chaves: ["medicina legal", "iml"], coordenadorias: [
    {nome: "Coordenadoria de Perícias em Vivos", gerencias: [
      "Gerência de Perícias em Vítimas de Violência Sexual e de Gênero", "Gerência de Perícias em Psiquiatria Forense"]},
    {nome: "Coordenadoria de Perícias em Mortos", gerencias: ["Gerência de Necropsia", "Gerência de Antropologia", "Gerência de Histopatologia"]},
    {nome: VINCULADAS, gerencias: ["Gerência de Atendimento de Processamento de Documentos", "Núcleo de Apoio Operacional de Medicina Legal",
      "Núcleo de Custódia e Logística de Medicina Legal"]}]},
  {diretoria: "Diretoria de Laboratório Forense", chaves: ["laboratorio"], siglas: ["DMLF", "DLF"], coordenadorias: [
    {nome: "Coordenadoria de Perícias em Biologia Molecular", gerencias: ["Gerência Técnica", "Gerência de Qualidade em Biologia Molecular"]},
    {nome: "Coordenadoria do Laboratório de Materiais", gerencias: [
      "Gerência de Perícias em Química Forense", "Gerência de Perícias em Toxicologia Forense", "Gerência de Perícias em Entorpecentes"]},
    {nome: VINCULADAS, gerencias: ["Núcleo de Apoio Operacional do Laboratório Forense", "Núcleo de Custódia e Logística do Laboratório Forense"]}]},
  {diretoria: "Diretoria de Identificação Técnica", chaves: ["identificacao"], coordenadorias: [
    {nome: "Coordenadoria de Identificação Criminal", gerencias: ["Gerência de Informação Criminal", "Gerência de Banco de Dados de Padrões"]},
    {nome: "Coordenadoria de Identificação Civil", gerencias: [
      "Gerência de Processamento Civil", "Gerência de Atendimento Volante", "Gerência de Postos de Identificação"]},
    {nome: VINCULADAS, gerencias: ["Gerência de Identificação Integrado", "Núcleo de Apoio Operacional de Identificação Técnica"]}]},
  {diretoria: "Diretoria de Interiorização", chaves: ["regional", "interior"], coordenadorias: [
    ["Coordenadoria Regional 1 - Rondonópolis", "Rondonópolis", ["Primavera do Leste", "Alto Araguaia"]],
    ["Coordenadoria Regional 2 - Barra do Garças", "Barra do Garças", ["Água Boa", "Confresa"]],
    ["Coordenadoria Regional 3 - Cáceres", "Cáceres", ["Pontes e Lacerda"]],
    ["Coordenadoria Regional 4 - Sinop", "Sinop", ["Alta Floresta", "Guarantã do Norte", "Sorriso"]],
    ["Coordenadoria Regional 5 - Tangará da Serra", "Tangará da Serra", ["Juína", "Juara"]],
    ["Coordenadoria Regional 6 - Nova Mutum", "Nova Mutum", ["Diamantino", "Lucas do Rio Verde"]],
  ].map(([nome, sede, regionais])=>({nome, sede, cidades: [sede, ...regionais], gerencias: [
    `Gerência de Criminalística de ${sede}`, `Gerência de Medicina Legal de ${sede}`, `Gerência de Identificação Técnica de ${sede}`,
    ...regionais.map(c=>`Gerência Regional de ${c}`)]}))},
];
const DIRETORIAS = ORGANOGRAMA.map(d=>d.diretoria);

// tira o que é comum aos nomes ("gerência de perícias de", "núcleo de"...) para comparar o miolo
const miolo = s => normalizar(s).replace(/^(gerencia|nucleo|coordenadoria)( regional)?( de| do| da| em)?( pericias?)?( de| do| da| em)?\s+/, "").trim();

/* De onde é a unidade lida no relatório: {diretoria, coordenadoria, gerencia}.
   1) nome igual (ou contido) ao de uma gerência/núcleo do organograma;
   2) cidade do interior -> coordenadoria regional (e a gerência pelo tipo: criminalística, IML, identificação);
   3) palavra-chave da diretoria (IML, laboratório, criminalística, identificação).
   Sem nada disso, devolve diretoria vazia ("Outras"). */
function lotacaoDe(nome){
  const n = normalizar(nome), m = miolo(nome), vazio = {diretoria: "", coordenadoria: "", gerencia: ""};
  if (!n) return vazio;
  let melhor = null, nota = 0;
  for (const d of ORGANOGRAMA) for (const c of d.coordenadorias) for (const g of c.gerencias){
    const gn = normalizar(g), gm = miolo(g);
    // exato vale mais; depois o trecho contido mais longo
    const s = (n === gn || m === gm) ? 1000 : (gm.length > 6 && n.includes(gm)) ? gm.length : (m.length > 6 && gm.includes(m)) ? m.length - 1 : 0;
    if (s > nota){ nota = s; melhor = {diretoria: d.diretoria, coordenadoria: c.nome, gerencia: g}; }
  }
  if (melhor) return melhor;
  // coordenadoria pelo nome ("PERÍCIAS EM LABORATÓRIOS DE MATERIAIS" = Coordenadoria do Laboratório de Materiais):
  // todas as palavras do miolo da coordenadoria aparecem no nome lido (plural e singular contam igual)
  const palavrasDe = s => normalizar(s).split(/[^a-z0-9]+/).filter(w=>w.length > 3).map(w=>w.replace(/s$/, ""));
  const lidas = new Set(palavrasDe(nome));
  let coord = null, tam = 0;
  for (const d of ORGANOGRAMA) for (const c of d.coordenadorias){
    if (c.nome === VINCULADAS || c.sede) continue;   // as regionais têm a regra da cidade, abaixo
    const ws = palavrasDe(miolo(c.nome));
    if (ws.length && ws.every(w=>lidas.has(w)) && ws.length > tam){ tam = ws.length; coord = {diretoria: d.diretoria, coordenadoria: c.nome, gerencia: ""}; }
  }
  if (coord) return coord;
  const interior = ORGANOGRAMA.find(d=>d.diretoria === "Diretoria de Interiorização");
  for (const c of interior.coordenadorias) for (const cidade of c.cidades){
    if (!n.includes(normalizar(cidade))) continue;
    const tipo = /iml|medicina legal/.test(n) ? "Medicina Legal" : /criminalistica/.test(n) ? "Criminalística" : /identificacao/.test(n) ? "Identificação Técnica" : "";
    const g = cidade === c.sede ? (tipo ? `Gerência de ${tipo} de ${cidade}` : "") : `Gerência Regional de ${cidade}`;
    return {diretoria: interior.diretoria, coordenadoria: c.nome, gerencia: g};
  }
  const d = ORGANOGRAMA.find(o=>o.chaves.some(k=>new RegExp(`\\b${k}\\b`).test(n)) || (o.siglas || []).some(k=>normalizar(k) === n));
  return d ? {diretoria: d.diretoria, coordenadoria: "", gerencia: ""} : vazio;
}
teste("Organograma: gerência pelo nome", ()=> lotacaoDe("GERÊNCIA DE PERÍCIAS DE BALÍSTICA").coordenadoria === "Coordenadoria de Perícias Internas"
  && lotacaoDe("Balística").diretoria === "Diretoria de Criminalística" && lotacaoDe("Necropsia").coordenadoria === "Coordenadoria de Perícias em Mortos");
teste("Organograma: cidade do interior vai para a regional", ()=> lotacaoDe("Regional Alta Floresta").gerencia === "Gerência Regional de Alta Floresta"
  && lotacaoDe("IML Sinop").gerencia === "Gerência de Medicina Legal de Sinop"
  && lotacaoDe("Gerência de Identificação Técnica de Sinop").coordenadoria === "Coordenadoria Regional 4 - Sinop" && lotacaoDe("Regional Sinop").coordenadoria === "Coordenadoria Regional 4 - Sinop");
teste("Organograma: coordenadoria e sigla como aparecem no painel do Power BI", ()=>
  lotacaoDe("PERÍCIAS EM LABORATÓRIOS DE MATERIAIS").coordenadoria === "Coordenadoria do Laboratório de Materiais"
  && lotacaoDe("PERÍCIAS EM BIOLOGIA MOLECULAR").coordenadoria === "Coordenadoria de Perícias em Biologia Molecular"
  && lotacaoDe("DMLF").diretoria === "Diretoria de Laboratório Forense" && lotacaoDe("Outro").diretoria === "");
teste("Organograma: IML da capital fica na Medicina Legal", ()=> lotacaoDe("IML Cuiabá").diretoria === "Diretoria de Medicina Legal" && lotacaoDe("Unidade Fantasma").diretoria === "");

// lotação gravada na linha (ou na unidade) vence a dedução pelo nome
const lotacaoPend = p => (p.lotacao && p.lotacao.diretoria) ? p.lotacao : lotacaoDe(p.unidade);

/* ---------- filtro em cascata: Diretoria > Coordenadoria > Gerência ---------- */
function opcoesOrg(sel = {}){
  const d = ORGANOGRAMA.find(x=>x.diretoria === sel.diretoria);
  const c = d?.coordenadorias.find(x=>x.nome === sel.coordenadoria);
  return {
    diretorias: [["", "Todas as diretorias"], ...DIRETORIAS.map(x=>[x, x]), ["Outras", "Outras (fora do organograma)"]],
    coordenadorias: [["", "Todas as coordenadorias"], ...(d ? d.coordenadorias.map(x=>[x.nome, x.nome]) : [])],
    gerencias: [["", "Todas as gerências"], ...(c ? c.gerencias.map(x=>[x, x]) : d ? d.coordenadorias.flatMap(x=>x.gerencias).map(x=>[x, x]) : [])],
  };
}
function filtroOrg(prefixo, sel = {}){
  const o = opcoesOrg(sel);
  return `<div class="campos filtro-org" data-filtro-org="${prefixo}">
    ${campo(prefixo + "Diretoria", "Diretoria", {tipo: "select", valor: sel.diretoria || "", opcoes: o.diretorias})}
    ${campo(prefixo + "Coordenadoria", "Coordenadoria", {tipo: "select", valor: sel.coordenadoria || "", opcoes: o.coordenadorias, attrs: sel.diretoria && sel.diretoria !== "Outras" ? "" : "disabled"})}
    ${campo(prefixo + "Gerencia", "Gerência ou núcleo", {tipo: "select", valor: sel.gerencia || "", opcoes: o.gerencias, attrs: sel.diretoria && sel.diretoria !== "Outras" ? "" : "disabled"})}</div>`;
}
const lerFiltroOrg = prefixo => ({diretoria: valorDe(prefixo + "Diretoria"), coordenadoria: valorDe(prefixo + "Coordenadoria"), gerencia: valorDe(prefixo + "Gerencia")});
// liga a cascata: trocar a diretoria limpa as de baixo; ao fim chama aoMudar(sel)
function ligarFiltroOrg(prefixo, aoMudar){
  const caixa = $(`[data-filtro-org="${prefixo}"]`); if (!caixa) return;
  caixa.addEventListener("change", e=>{
    const sel = lerFiltroOrg(prefixo);
    if (e.target.id === prefixo + "Diretoria"){ sel.coordenadoria = ""; sel.gerencia = ""; }
    if (e.target.id === prefixo + "Coordenadoria") sel.gerencia = "";
    caixa.outerHTML = filtroOrg(prefixo, sel);
    ligarFiltroOrg(prefixo, aoMudar);
    $("#" + e.target.id)?.focus();
    aoMudar?.(sel);
  });
}
function noRecorte(lot, sel = {}){
  if (!sel.diretoria) return true;
  if (sel.diretoria === "Outras") return !lot.diretoria;
  if (lot.diretoria !== sel.diretoria) return false;
  if (sel.coordenadoria && lot.coordenadoria !== sel.coordenadoria) return false;
  if (sel.gerencia && lot.gerencia !== sel.gerencia) return false;
  return true;
}
const textoRecorte = sel => !sel?.diretoria ? "Todas" : (sel.gerencia || sel.coordenadoria || sel.diretoria);
teste("Recorte por diretoria e coordenadoria", ()=> noRecorte(lotacaoDe("Balística"), {diretoria: "Diretoria de Criminalística", coordenadoria: "Coordenadoria de Perícias Internas"})
  && !noRecorte(lotacaoDe("IML Cuiabá"), {diretoria: "Diretoria de Criminalística"}) && noRecorte(lotacaoDe("Unidade X"), {diretoria: "Outras"}));

// cadastra as coordenadorias, as gerências e os núcleos das cinco diretorias como unidades monitoradas
async function carregarOrganograma(){
  let novas = 0;
  for (const d of ORGANOGRAMA) for (const c of d.coordenadorias){
    if (c.nome === VINCULADAS || await db.get("unidades", c.nome)) continue;
    await db.put("unidades", {nome: c.nome, apelidos: [], lotacao: {diretoria: d.diretoria, coordenadoria: c.nome, gerencia: ""}}); novas++;
  }
  for (const d of ORGANOGRAMA) for (const c of d.coordenadorias) for (const g of c.gerencias){
    if (await db.get("unidades", g)) continue;
    await db.put("unidades", {nome: g, apelidos: [], lotacao: {diretoria: d.diretoria, coordenadoria: c.nome, gerencia: g}}); novas++;
  }
  await registrar("organograma carregado", {detalhe: `${novas} unidades novas (Decreto 2.180/2026)`});
  return novas;
}
