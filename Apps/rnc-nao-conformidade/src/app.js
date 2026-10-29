/* Não Conformidades · código do app (o construir.py junta com a base comum) */
"use strict";
TELAS["#/painel"] = async ()=> `<h1>Painel</h1><p class="sub">Os indicadores chegam no Sprint 5. Resumo da base:</p>
  ${await resumoBase(["rncs", "etapas", "setores"])}
  <p class="sub">Para testar, carregue os dados fictícios em <a href="#/config">Configuração</a>.</p>`;
teste("RN07: exemplo sem nome de servidor", ()=> (dadosEmbutidos("seed")?.rncs || []).every(r=>!("nome" in r) && !("servidor" in r)));
teste("RN01: números DIRETORIA/ANO-SEQ únicos", ()=>{ const n = (dadosEmbutidos("seed")?.rncs || []).map(r=>r.numero); return n.length === 20 && new Set(n).size === 20 && n.every(x=>/^[A-Z]+\/\d{4}-\d{3}$/.test(x)); });

/* ================= Sprint 2 · Importar a planilha do Forms ================= */
const CAMPOS_RNC = {
  aberta_em: ["carimbo de data/hora", "data/hora", "data de abertura", "data"],
  setor_relator: ["setor relator", "relator"], setor_notificado: ["setor notificado", "notificado"],
  categoria: ["categoria", "tipo de nao conformidade"], descricao: ["descricao da ocorrencia", "descricao", "ocorrencia"],
  gravidade: ["gravidade"], numero: ["numero", "n da rnc", "rnc"]
};
const ROTULOS_RNC = {aberta_em: "Data de abertura", setor_relator: "Setor relator", setor_notificado: "Setor notificado", categoria: "Categoria",
  descricao: "Descrição", gravidade: "Gravidade", numero: "Número (opcional)"};
const OPCIONAIS_RNC = ["gravidade", "numero"];
const RE_PESSOAL = /\b(nome|servidor|matricula|cpf|e-?mail|telefone)\b/;  // RN07: colunas descartadas
const RE_NUMERO = /^[A-Z]+\/\d{4}-\d{3}$/;
const somarDiasRnc = (iso, n)=> new Date(Date.UTC(...iso.slice(0, 10).split("-").map((x, i)=>i === 1 ? x - 1 : +x)) + n * 86400000).toISOString().slice(0, 10);
let planilhaRnc = null;  // {nome, linhas, cabecalho, mapa}

function colunasDescartadas(cab){ return cab.map((c, i)=>({c, i})).filter(x=>RE_PESSOAL.test(normalizar(x.c)) && !/setor/.test(normalizar(x.c))); }
teste("RN07: coluna 'Nome do servidor' é descartada", ()=> colunasDescartadas(["Setor relator", "Nome do servidor", "Matrícula"]).length === 2);
teste("RN07: 'Setor relator' não é descartada", ()=> colunasDescartadas(["Setor relator", "Setor notificado"]).length === 0);

TELAS["#/importar"] = async ()=>{
  const diretoria = (await db.meta("diretoria")) || "DLF";
  return `<h1>Importar a planilha do Forms</h1><p class="sub">Exporte a planilha de respostas como CSV (Arquivo > Fazer download > CSV) e escolha o arquivo.
    O QR Code e o formulário continuam iguais.</p>
    <div class="card"><div class="campos">${campo("rncDiretoria", "Diretoria (para numerar)", {valor: diretoria, ajuda: "Usada quando a planilha não traz o número da RNC."})}</div>
      <label class="botao">Escolher CSV<input type="file" id="arqRnc" accept=".csv,text/csv" hidden></label>
      <div id="mapaRnc"></div><div id="errosRnc"></div><div id="relRnc"></div></div>`;
};
function desenharMapaRnc(){
  const P = planilhaRnc, opts = [["-1", "(não tem)"], ...P.cabecalho.map((c, i)=>[String(i), c || `coluna ${i + 1}`])];
  const desc = colunasDescartadas(P.cabecalho);
  $("#mapaRnc").innerHTML = `<p class="sub"><b>${esc(P.nome)}</b> · ${P.linhas.length - 1} linhas</p>
    <div class="campos">${Object.keys(CAMPOS_RNC).map(k=>campo("rmap-" + k, ROTULOS_RNC[k] + (OPCIONAIS_RNC.includes(k) ? "" : " *"), {tipo: "select", opcoes: opts, valor: String(P.mapa[k] ?? -1)})).join("")}</div>
    ${desc.length ? `<p><span class="selo alerta">descartadas (RN07)</span> ${desc.map(d=>esc(d.c)).join(", ")}: dado pessoal não entra no app.</p>` : ""}
    <div class="linha-botoes"><button class="prim" id="btnImportarRnc">Importar</button></div>`;
  Object.keys(CAMPOS_RNC).forEach(k=>$("#rmap-" + k).addEventListener("change", e=>{ P.mapa[k] = Number(e.target.value); }));
  $("#btnImportarRnc").addEventListener("click", importarRnc);
}
TELAS_DEPOIS["#/importar"] = ()=>{
  $("#arqRnc").addEventListener("change", async e=>{
    const f = e.target.files[0]; if (!f) return;
    const linhas = lerCSV(await lerArquivoTexto(f)), cabecalho = linhas[0] || [];
    const salvo = await db.meta("modelo:forms"), sug = sugerirColunas(cabecalho, CAMPOS_RNC), mapa = {};
    const desc = new Set(colunasDescartadas(cabecalho).map(d=>d.i));
    for (const k of Object.keys(CAMPOS_RNC)){
      const i = salvo?.[k] ? cabecalho.findIndex(c=>normalizar(c) === normalizar(salvo[k])) : -1;
      mapa[k] = i >= 0 ? i : (desc.has(sug[k]) ? -1 : sug[k]);
    }
    planilhaRnc = {nome: f.name, linhas, cabecalho, mapa};
    desenharMapaRnc(); $("#relRnc").innerHTML = "";
  });
};

async function importarRnc(){
  const P = planilhaRnc, diretoria = valorDe("rncDiretoria").toUpperCase() || "DLF";
  const falta = Object.keys(CAMPOS_RNC).filter(k=>!OPCIONAIS_RNC.includes(k) && !(P.mapa[k] >= 0));
  if (!mostrarErros("#errosRnc", falta.length ? [`Associe as colunas: ${falta.map(k=>ROTULOS_RNC[k]).join(", ")}.`] : [])) return;
  const desc = new Set(colunasDescartadas(P.cabecalho).map(d=>d.i));
  if (Object.values(P.mapa).some(i=>desc.has(i))) return mostrarErros("#errosRnc", ["Uma coluna de dado pessoal foi associada a um campo. Escolha outra coluna (RN07)."]);
  await db.meta("diretoria", diretoria);
  const nomes = {}; Object.entries(P.mapa).forEach(([k, i])=>{ if (i >= 0) nomes[k] = P.cabecalho[i]; }); await db.meta("modelo:forms", nomes);
  const setores = await db.list("setores");
  const acharSetor = t => setores.find(s=>normalizar(s.sigla) === normalizar(t) || normalizar(s.nome) === normalizar(t));
  const existentes = await db.list("rncs"), chaves = new Set(existentes.map(r=>r.chave_importacao).filter(Boolean)), numeros = new Set(existentes.map(r=>r.numero));
  const rel = {novas: 0, existentes: 0, recusadas: [], alertas: []};
  const col = (l, k)=> P.mapa[k] >= 0 ? String(l[P.mapa[k]] ?? "").trim() : "";
  for (const [n, l] of P.linhas.slice(1).entries()){
    const linha = n + 2, aberta = dataDeTexto(col(l, "aberta_em"));
    if (!aberta) { rel.recusadas.push({linha, motivo: "data de abertura ilegível"}); continue; }
    const relT = col(l, "setor_relator"), notT = col(l, "setor_notificado");
    if (!relT || !notT) { rel.recusadas.push({linha, motivo: "setor relator ou notificado vazio"}); continue; }
    if (!col(l, "descricao")) { rel.recusadas.push({linha, motivo: "descrição vazia"}); continue; }
    const chave = fnvRnc([aberta, normalizar(relT), normalizar(col(l, "descricao"))].join("|"));
    let numero = col(l, "numero").toUpperCase();
    if (numero && !RE_NUMERO.test(numero)) { rel.alertas.push({linha, motivo: `número "${numero}" fora do padrão DIRETORIA/ANO-SEQ; gerado outro`}); numero = ""; }
    if ((numero && numeros.has(numero)) || chaves.has(chave)) { rel.existentes++; continue; }
    if (!numero){
      const ano = aberta.slice(0, 4); let seq = 1;
      while (numeros.has(`${diretoria}/${ano}-${String(seq).padStart(3, "0")}`)) seq++;
      numero = `${diretoria}/${ano}-${String(seq).padStart(3, "0")}`;
    }
    const sRel = acharSetor(relT), sNot = acharSetor(notT);
    if (!sRel) rel.alertas.push({linha, motivo: `setor relator "${relT}" não cadastrado`});
    if (!sNot) rel.alertas.push({linha, motivo: `setor notificado "${notT}" não cadastrado`});
    await db.put("rncs", {numero, aberta_em: aberta, setor_relator: sRel?.sigla || relT, setor_notificado: sNot?.sigla || notT,
      categoria: col(l, "categoria"), gravidade: col(l, "gravidade") || "não informada", descricao: col(l, "descricao"),
      etapa: "validação", situacao: "aberta", chave_importacao: chave, origem: {arquivo: P.nome, linha}});
    await db.put("etapas", {id: `${numero}#0`, rnc: numero, etapa: "validação", inicio: aberta.slice(0, 10), fim: null, prazo: somarDiasRnc(aberta, 5)});
    numeros.add(numero); chaves.add(chave); rel.novas++;
  }
  await registrar("planilha importada", {detalhe: `${P.nome}: ${rel.novas} novas, ${rel.existentes} já existentes, ${rel.recusadas.length} recusadas`});
  const lista = [...rel.recusadas.map(x=>({...x, t: "recusada"})), ...rel.alertas.map(x=>({...x, t: "alerta"}))];
  $("#relRnc").innerHTML = `<h2>Resultado</h2><p><span class="selo ok" id="qtdNovas">${rel.novas} novas</span>
    <span class="selo info" id="qtdExistentes">${rel.existentes} já existentes</span> <span class="selo erro">${rel.recusadas.length} recusadas</span>
    <span class="selo alerta">${rel.alertas.length} alertas</span></p>
    ${lista.length ? `<div class="tabela-wrap"><table><tr><th>Linha</th><th>Tipo</th><th>Motivo</th></tr>${lista.map(x=>`<tr><td class="num">${x.linha}</td><td>${x.t}</td><td>${esc(x.motivo)}</td></tr>`).join("")}</table></div>` : ""}`;
}
function fnvRnc(txt){ let h = 0x811c9dc5; for (const b of new TextEncoder().encode(txt)){ h ^= b; h = Math.imul(h, 0x01000193) >>> 0; } return h.toString(16); }
