/* Mapa de Distribuição · código do app (o construir.py junta com a base comum) */
"use strict";

teste("dinheiro.de('1.234,56') = 123456", ()=> dinheiro.de("1.234,56") === 123456);
teste("dinheiro.de('R$ 1.234,5') = 123450", ()=> dinheiro.de("R$ 1.234,5") === 123450);
teste("dinheiro.de('1234.56') = 123456", ()=> dinheiro.de("1234.56") === 123456);
teste("dinheiro.de('1.234') = 123400 (milhar)", ()=> dinheiro.de("1.234") === 123400);
teste("0,1 + 0,2 = 0,30 em centavos", ()=> dinheiro.de(0.1) + dinheiro.de(0.2) === 30);
teste("dinheiro.fmt(123456) = R$ 1.234,56", ()=> dinheiro.fmt(123456) === "R$ 1.234,56");
teste("dinheiro.vezes(3, 3333) = 9999", ()=> dinheiro.vezes(3, 3333) === 9999);
teste("dinheiro.vezes(2.5, 101) = 253 (meio para cima)", ()=> dinheiro.vezes(2.5, 101) === 253);
teste("dinheiro.ratear(100, [1,1,1]) soma 100", ()=> dinheiro.ratear(100, [1, 1, 1]).reduce((a, b)=>a + b) === 100);
teste("SheetJS embutido", ()=> typeof XLSX !== "undefined" && typeof XLSX.read === "function");

/* ================= Sprint 1 · Processos ================= */
TELAS["#/processos"] = async ()=>{
  const procs = await db.list("processos");
  const linhas = [];
  for (const p of procs){
    const itens = (await db.porIndice("itens", "id_processo", p.id)).length;
    linhas.push(`<tr><td><b>${esc(p.numero)}</b><br><span class="sub">${esc(p.nome)}</span></td><td class="num">${itens}</td><td>${esc(p.status || "")}</td>
      <td><a href="#/importar/${encodeURIComponent(p.id)}">Importar</a> · <a href="#/mapa/${encodeURIComponent(p.id)}">Mapa</a></td></tr>`);
  }
  return `<h1>Processos</h1><p class="sub">Cada processo reúne a distribuição por órgão, o relatório do pregoeiro e a dotação.</p>
    ${procs.length ? `<div class="card tabela-wrap"><table><tr><th>Processo</th><th class="num">Itens</th><th>Situação</th><th></th></tr>${linhas.join("")}</table></div>`
      : `<div class="card vazio">Nenhum processo. Crie um abaixo ou use <b>Carregar exemplo</b> para testar com os dados sintéticos.</div>`}
    <form class="card" id="formProcesso"><h2 style="margin-top:0">Novo processo</h2><div class="campos">
      ${campo("procNumero", "Número", {obrigatorio: true, attrs: 'placeholder="001/2026"'})}
      ${campo("procNome", "Objeto", {obrigatorio: true})}
      ${campo("procAno", "Ano da dotação", {tipo: "number", valor: new Date().getFullYear(), obrigatorio: true})}</div>
      <div id="errosProcesso"></div><div class="linha-botoes"><button class="prim" type="submit">Criar processo</button></div></form>
    <div class="linha-botoes"><button id="btnExemplo">Carregar exemplo</button></div>`;
};
TELAS_DEPOIS["#/processos"] = ()=>{
  $("#btnExemplo").addEventListener("click", async ()=>{
    await db.importar({app: APP.id, dados: dadosEmbutidos("seed")}); await registrar("exemplo carregado");
    toast("Exemplo carregado: 30 itens, 3 órgãos, 6 grupos."); navegar();
  });
  $("#formProcesso").addEventListener("submit", async e=>{
    e.preventDefault();
    const numero = valorDe("procNumero"), nome = valorDe("procNome"), ano = Number(valorDe("procAno"));
    if (!mostrarErros("#errosProcesso", [!numero && "Informe o número.", !nome && "Informe o objeto.", !(ano > 2000) && "Ano inválido."].filter(Boolean))) return;
    const id = "PROC-" + numero.replace(/\W+/g, "-");
    if (await db.get("processos", id)) return mostrarErros("#errosProcesso", ["Já existe um processo com esse número."]);
    await db.put("processos", {id, numero, nome, ano, status: "em andamento", criado_em: agora()});
    await registrar("processo criado", {id_processo: id});
    location.hash = "#/importar/" + encodeURIComponent(id);
  });
};

/* ================= Sprint 2 · Importação das fontes ================= */
// Cada fonte: campos obrigatórios, sinônimos para sugerir a coluna e como vira registro.
const FONTES = {
  distribuicao: {
    titulo: "Distribuição por órgão (anexo do TR)", store: ["itens", "distribuicao"],
    campos: {grupo: ["grupo", "lote"], item: ["item"], codigo: ["codigo", "catmat", "catser"], descricao: ["descricao", "especificacao"],
             unidade: ["unidade", "unid"], tipo_despesa: ["tipo de despesa", "natureza", "elemento"],
             valor_unitario_estimado: ["valor unitario estimado", "valor estimado", "valor unitario"], quantidade_total: ["quantidade total", "qtd total", "quantidade"]},
    opcionais: ["codigo"], orgaos: true
  },
  pregoeiro: {
    titulo: "Relatório do pregoeiro", store: ["resultado"],
    campos: {grupo: ["grupo", "lote"], item: ["item"], situacao: ["situacao", "status"], empresa: ["empresa", "fornecedor", "razao social"],
             cnpj: ["cnpj"], valor_unitario_homologado: ["valor unitario homologado", "valor homologado", "homologado"]},
    opcionais: ["empresa", "cnpj", "valor_unitario_homologado"]
  },
  dotacao: {
    titulo: "Dotação por órgão", store: ["dotacao"],
    campos: {orgao: ["orgao", "unidade orcamentaria"], tipo: ["tipo", "elemento", "categoria"], ano: ["ano", "exercicio"], valor: ["valor", "dotacao"]},
    opcionais: []
  }
};
const ROTULO = {grupo: "Grupo", item: "Item", codigo: "Código", descricao: "Descrição", unidade: "Unidade", tipo_despesa: "Tipo de despesa (3 ou 4)",
  valor_unitario_estimado: "Valor unitário estimado", quantidade_total: "Quantidade total", situacao: "Situação", empresa: "Empresa", cnpj: "CNPJ",
  valor_unitario_homologado: "Valor unitário homologado", orgao: "Órgão", tipo: "Tipo (3 ou 4)", ano: "Ano", valor: "Valor"};
const leitura = {};  // fonte -> {arquivo, livro, aba, linhaCab, linhas, cabecalho}

function lerPlanilha(arquivo, buffer){
  const livro = /\.csv$/i.test(arquivo.name)
    ? {SheetNames: ["CSV"], Sheets: {CSV: XLSX.utils.aoa_to_sheet(lerCSV(new TextDecoder("utf-8").decode(buffer)))}}
    : XLSX.read(buffer, {type: "array"});
  return livro;
}
function linhasDaAba(livro, aba){ return XLSX.utils.sheet_to_json(livro.Sheets[aba], {header: 1, raw: true, defval: ""}); }
// primeira linha com 3 ou mais células preenchidas
const linhaDoCabecalho = linhas => Math.max(0, linhas.findIndex(l=>l.filter(c=>String(c).trim() !== "").length >= 3));

async function modeloSalvo(fonte){ return (await db.meta("modelo:" + fonte)) || null; }

function blocoFonte(fonte){
  const f = FONTES[fonte], L = leitura[fonte];
  if (!L) return `<div class="card" id="fonte-${fonte}"><h2 style="margin-top:0">${esc(f.titulo)}</h2>
    <label class="botao">Escolher arquivo (.xlsx ou .csv)<input type="file" accept=".xlsx,.xls,.csv" data-fonte="${fonte}" hidden></label></div>`;
  const cab = L.cabecalho, opts = [["-1", "(não tem)"], ...cab.map((c, i)=>[String(i), String(c || `coluna ${i + 1}`)])];
  const usadas = new Set(Object.values(L.mapa).filter(i=>i >= 0));
  const orgaos = f.orgaos ? cab.map((c, i)=>({c, i})).filter(x=>!usadas.has(x.i) && String(x.c).trim()) : [];
  return `<div class="card" id="fonte-${fonte}"><h2 style="margin-top:0">${esc(f.titulo)}</h2>
    <p class="sub"><b>${esc(L.arquivo)}</b> · ${L.linhas.length - L.linhaCab - 1} linhas de dados
      <label class="botao" style="margin-left:8px">Trocar arquivo<input type="file" accept=".xlsx,.xls,.csv" data-fonte="${fonte}" hidden></label></p>
    <div class="campos">
      ${campo(`aba-${fonte}`, "Aba", {tipo: "select", opcoes: L.livro.SheetNames, valor: L.aba})}
      ${campo(`cab-${fonte}`, "Linha do cabeçalho", {tipo: "number", valor: L.linhaCab + 1, attrs: 'min="1"'})}
    </div>
    <h3>Associação das colunas</h3><div class="campos">
      ${Object.keys(f.campos).map(k=>campo(`map-${fonte}-${k}`, ROTULO[k] + (f.opcionais.includes(k) ? "" : " *"), {tipo: "select", opcoes: opts, valor: String(L.mapa[k] ?? -1)})).join("")}
    </div>
    ${f.orgaos ? `<h3>Colunas de órgãos (quantidade por órgão)</h3><p class="sub">${orgaos.length ? orgaos.map(o=>`<label style="display:inline-block;margin-right:12px">
      <input type="checkbox" data-orgao="${o.i}" ${L.orgaosDesmarcados?.includes(o.i) ? "" : "checked"} style="width:auto"> ${esc(o.c)}</label>`).join("") : "Nenhuma coluna sobrando."}</p>` : ""}
    <div id="erros-${fonte}"></div><div id="rel-${fonte}"></div></div>`;
}

TELAS["#/importar/:proc"] = async ({proc})=>{
  const p = await db.get("processos", proc);
  if (!p) return `<div class="card vazio">Processo não encontrado. <a href="#/processos">Voltar</a></div>`;
  estado.proc = p;
  return `<h1>Importar · ${esc(p.numero)}</h1><p class="sub">${esc(p.nome)}. Escolha os três arquivos, confira a associação das colunas e importe.
    A associação fica salva como modelo para o próximo processo.</p>
    <div id="fontes">${Object.keys(FONTES).map(blocoFonte).join("")}</div>
    <div class="linha-botoes"><button class="prim" id="btnImportar">Validar e importar</button></div>
    <div id="resumoImport">${await resumoProcesso(proc)}</div>`;
};
TELAS_DEPOIS["#/importar/:proc"] = ()=>ligarImportacao();

// liga os eventos só uma vez por elemento (o bloco é redesenhado a cada mudança)
const umaVez = el => el && !el.dataset.ligado && (el.dataset.ligado = "1");
function ligarImportacao(){
  if (!$("#btnImportar")) return;  // processo não encontrado
  $$("input[type=file][data-fonte]").filter(umaVez).forEach(inp=>inp.addEventListener("change", async e=>{
    const arq = e.target.files[0], fonte = e.target.dataset.fonte; if (!arq) return;
    try {
      const livro = lerPlanilha(arq, await lerArrayBuffer(arq));
      const aba = livro.SheetNames[0], linhas = linhasDaAba(livro, aba), linhaCab = linhaDoCabecalho(linhas);
      leitura[fonte] = {arquivo: arq.name, livro, aba, linhas, linhaCab, cabecalho: linhas[linhaCab] || [], mapa: {}};
      await aplicarMapa(fonte);
    } catch(err){ toast("Não consegui ler o arquivo: " + err.message, 5000); }
    redesenharFonte(fonte);
  }));
  for (const fonte of Object.keys(FONTES)){
    const el = $(`#fonte-${fonte}`); if (!el || !leitura[fonte] || !umaVez($(`#aba-${fonte}`))) continue;
    $(`#aba-${fonte}`).addEventListener("change", async e=>{
      const L = leitura[fonte]; L.aba = e.target.value; L.linhas = linhasDaAba(L.livro, L.aba); L.linhaCab = linhaDoCabecalho(L.linhas);
      L.cabecalho = L.linhas[L.linhaCab] || []; await aplicarMapa(fonte); redesenharFonte(fonte);
    });
    $(`#cab-${fonte}`).addEventListener("change", async e=>{
      const L = leitura[fonte]; L.linhaCab = Math.max(0, Number(e.target.value) - 1); L.cabecalho = L.linhas[L.linhaCab] || [];
      await aplicarMapa(fonte); redesenharFonte(fonte);
    });
    Object.keys(FONTES[fonte].campos).forEach(k=>$(`#map-${fonte}-${k}`).addEventListener("change", e=>{
      leitura[fonte].mapa[k] = Number(e.target.value); redesenharFonte(fonte);
    }));
    $$(`#fonte-${fonte} [data-orgao]`).forEach(cb=>cb.addEventListener("change", ()=>{
      leitura[fonte].orgaosDesmarcados = $$(`#fonte-${fonte} [data-orgao]`).filter(x=>!x.checked).map(x=>Number(x.dataset.orgao));
    }));
  }
  $("#btnImportar").onclick = importarTudo;
}
function redesenharFonte(fonte){ $(`#fonte-${fonte}`).outerHTML = blocoFonte(fonte); ligarImportacao(); }

// Usa o modelo salvo quando as colunas dele existem; senão, sugere pelos sinônimos.
async function aplicarMapa(fonte){
  const L = leitura[fonte], f = FONTES[fonte], cab = L.cabecalho.map(c=>normalizar(c));
  const salvo = await modeloSalvo(fonte), sug = sugerirColunas(L.cabecalho, f.campos), mapa = {};
  for (const k of Object.keys(f.campos)){
    const nome = salvo?.[k];
    mapa[k] = nome && cab.includes(normalizar(nome)) ? cab.indexOf(normalizar(nome)) : sug[k];
  }
  L.mapa = mapa; L.orgaosDesmarcados = [];
}

const texto = v => String(v ?? "").trim();
const codigoItem = v => { const s = texto(v); return /^\d+$/.test(s) ? s.padStart(2, "0") : s; };
function numero(v){ if (typeof v === "number") return v; const s = texto(v).replace(/\./g, "").replace(",", "."); return s === "" ? NaN : Number(s); }
function centavos(v){ const c = dinheiro.de(typeof v === "number" ? v : texto(v)); return c === null ? null : c; }

// Lê as linhas da fonte com o mapa atual. Devolve {registros, recusadas, alertas} ou {erroColunas}.
function lerFonte(fonte, proc){
  const L = leitura[fonte], f = FONTES[fonte];
  const faltando = Object.keys(f.campos).filter(k=>!f.opcionais.includes(k) && !(L.mapa[k] >= 0));
  if (faltando.length) return {erroColunas: faltando.map(k=>ROTULO[k])};
  const col = (l, k)=> L.mapa[k] >= 0 ? l[L.mapa[k]] : "";
  const origem = n => ({arquivo: L.arquivo, aba: L.aba, linha: n + 1});
  const out = {registros: {}, recusadas: [], alertas: []};
  f.store.forEach(s=>out.registros[s] = []);
  L.linhas.slice(L.linhaCab + 1).forEach((l, i)=>{
    const n = L.linhaCab + 1 + i;
    if (l.every(c=>texto(c) === "")) return;
    const motivo = m => out.recusadas.push({linha: n + 1, motivo: m});
    if (fonte === "distribuicao"){
      const grupo = texto(col(l, "grupo")), item = codigoItem(col(l, "item")), vu = centavos(col(l, "valor_unitario_estimado"));
      const qtd = numero(col(l, "quantidade_total")), tipo = Number(texto(col(l, "tipo_despesa")));
      if (!grupo || !item) return motivo("grupo ou item vazio");
      if (!(vu > 0)) return motivo("valor unitário estimado inválido");
      if (!(qtd >= 0)) return motivo("quantidade total inválida");
      if (![3, 4].includes(tipo)) return motivo("tipo de despesa deve ser 3 ou 4");
      out.registros.itens.push({id: `${proc}|${grupo}|${item}`, id_processo: proc, grupo, item, codigo: texto(col(l, "codigo")),
        descricao: texto(col(l, "descricao")), unidade: texto(col(l, "unidade")), tipo_despesa: tipo, valor_unitario_estimado_c: vu, quantidade_total: qtd, origem: origem(n)});
      L.cabecalho.forEach((nomeOrgao, j)=>{
        if (Object.values(L.mapa).includes(j) || !texto(nomeOrgao) || L.orgaosDesmarcados?.includes(j)) return;
        const q = numero(l[j]);
        if (Number.isNaN(q)) return out.alertas.push({linha: n + 1, motivo: `quantidade de ${nomeOrgao} ilegível`});
        out.registros.distribuicao.push({id: `${proc}|${texto(nomeOrgao)}|${grupo}|${item}`, id_processo: proc, orgao: texto(nomeOrgao), grupo, item, quantidade: q, origem: origem(n)});
      });
    }
    if (fonte === "pregoeiro"){
      const grupo = texto(col(l, "grupo")), item = codigoItem(col(l, "item")), sit = normalizar(col(l, "situacao"));
      if (!grupo || !item) return motivo("grupo ou item vazio");
      if (!["homologado", "fracassado", "deserto"].includes(sit)) return motivo(`situação "${texto(col(l, "situacao"))}" não é homologado, fracassado ou deserto`);
      const cnpj = texto(col(l, "cnpj")).replace(/\D/g, ""), vh = centavos(col(l, "valor_unitario_homologado"));
      if (sit === "homologado"){
        if (!(vh > 0)) return motivo("homologado sem valor unitário");
        if (!cnpj) out.alertas.push({linha: n + 1, motivo: "homologado sem CNPJ"});
        else if (!cnpjValido(cnpj)) out.alertas.push({linha: n + 1, motivo: `CNPJ ${cnpj} inválido (RN07)`});
      }
      out.registros.resultado.push({id: `${proc}|${grupo}|${item}`, id_processo: proc, grupo, item, situacao: sit, empresa: texto(col(l, "empresa")),
        cnpj, valor_unitario_homologado_c: sit === "homologado" ? vh : null, origem: origem(n)});
    }
    if (fonte === "dotacao"){
      const orgao = texto(col(l, "orgao")), tipo = Number(texto(col(l, "tipo"))), ano = Number(texto(col(l, "ano"))), valor = centavos(col(l, "valor"));
      if (!orgao) return motivo("órgão vazio");
      if (![3, 4].includes(tipo)) return motivo("tipo deve ser 3 ou 4");
      if (!(ano > 2000)) return motivo("ano inválido");
      if (!(valor >= 0)) return motivo("valor inválido");
      out.registros.dotacao.push({id: `${proc}|${orgao}|${tipo}|${ano}`, id_processo: proc, orgao, tipo, ano, valor_c: valor, origem: origem(n)});
    }
  });
  return out;
}

async function importarTudo(){
  const proc = estado.proc.id, relatorio = [];
  const fontes = Object.keys(FONTES).filter(f=>leitura[f]);
  if (!fontes.length) return toast("Escolha ao menos um arquivo.");
  for (const fonte of fontes){
    const r = lerFonte(fonte, proc);
    if (r.erroColunas){
      mostrarErros(`#erros-${fonte}`, [`Falta associar a coluna obrigatória: ${r.erroColunas.join(", ")}. A planilha não foi importada.`]);
      continue;
    }
    mostrarErros(`#erros-${fonte}`, []);
    // substitui a importação anterior desta fonte neste processo
    for (const store of FONTES[fonte].store){
      for (const antigo of await db.porIndice(store, "id_processo", proc)) await db.del(store, antigo.id);
      for (const reg of r.registros[store]) await db.put(store, reg);
    }
    const L = leitura[fonte], nomes = {};
    Object.entries(L.mapa).forEach(([k, i])=>{ if (i >= 0) nomes[k] = L.cabecalho[i]; });
    await db.meta("modelo:" + fonte, nomes);
    const qtd = Object.values(r.registros).reduce((a, x)=>a + x.length, 0);
    await registrar("importação", {id_processo: proc, fonte, arquivo: L.arquivo, aceitas: qtd, recusadas: r.recusadas.length, alertas: r.alertas.length});
    $(`#rel-${fonte}`).innerHTML = `<p><span class="selo ok">${qtd} registros importados</span>
      ${r.recusadas.length ? `<span class="selo erro">${r.recusadas.length} linhas recusadas</span>` : ""}
      ${r.alertas.length ? `<span class="selo alerta">${r.alertas.length} alertas</span>` : ""}</p>
      ${[...r.recusadas.map(x=>({...x, t: "recusada"})), ...r.alertas.map(x=>({...x, t: "alerta"}))].length ? `<div class="tabela-wrap"><table>
        <tr><th>Linha</th><th>Tipo</th><th>Motivo</th></tr>${[...r.recusadas.map(x=>({...x, t: "recusada"})), ...r.alertas.map(x=>({...x, t: "alerta"}))]
        .map(x=>`<tr><td class="num">${x.linha}</td><td>${x.t}</td><td>${esc(x.motivo)}</td></tr>`).join("")}</table></div>` : ""}`;
    relatorio.push(fonte);
  }
  $("#resumoImport").innerHTML = await resumoProcesso(proc);
  if (relatorio.length) toast("Importação concluída: " + relatorio.map(f=>FONTES[f].titulo).join(", "));
}

async function resumoProcesso(proc){
  const itens = await db.porIndice("itens", "id_processo", proc), dist = await db.porIndice("distribuicao", "id_processo", proc);
  const res = await db.porIndice("resultado", "id_processo", proc), dot = await db.porIndice("dotacao", "id_processo", proc);
  if (!itens.length && !res.length && !dot.length) return "";
  const k = (v, r)=>`<div class="card kpi"><div class="v">${v}</div><div class="r">${r}</div></div>`;
  return `<h2>Resumo do que foi lido</h2><div class="grade">
    ${k(new Set(dist.map(d=>d.orgao)).size, "órgãos")}${k(new Set(itens.map(i=>i.grupo)).size, "grupos")}${k(itens.length, "itens")}
    ${k(new Set(res.filter(r=>r.cnpj).map(r=>r.cnpj)).size, "empresas")}${k(dot.length, "dotações")}</div>`;
}

teste("linhaDoCabecalho pula título e linhas vazias", ()=> linhaDoCabecalho([["Mapa"], [], ["Grupo", "Item", "Valor"], [1, 2, 3]]) === 2);
teste("codigoItem completa com zero", ()=> codigoItem(2) === "02" && codigoItem("A1") === "A1");

/* ================= Sprint 3 · Mapa por grupo e item (etapa 2) ================= */
// Monta o mapa estimado: total do item (RN01) e quantidade e valor por órgão, tudo em centavos.
function montarMapa(itens, dist){
  const orgaos = [...new Set(dist.map(d=>d.orgao))].sort();
  const porItem = {}; dist.forEach(d=>{ (porItem[d.grupo + "|" + d.item] = porItem[d.grupo + "|" + d.item] || {})[d.orgao] = d; });
  const linhas = [...itens].sort((a, b)=>(a.grupo + a.item).localeCompare(b.grupo + b.item)).map(i=>{
    const od = porItem[i.grupo + "|" + i.item] || {};
    const porOrgao = Object.fromEntries(orgaos.map(o=>{ const q = od[o]?.quantidade || 0; return [o, {q, v: dinheiro.vezes(q, i.valor_unitario_estimado_c), origem: od[o]?.origem}]; }));
    return {...i, total_c: dinheiro.vezes(i.quantidade_total, i.valor_unitario_estimado_c), porOrgao};
  });
  const somar = ls => ({total_c: ls.reduce((a, l)=>a + l.total_c, 0),
    porOrgao: Object.fromEntries(orgaos.map(o=>[o, {q: ls.reduce((a, l)=>a + l.porOrgao[o].q, 0), v: ls.reduce((a, l)=>a + l.porOrgao[o].v, 0)}]))});
  const grupos = [...new Set(linhas.map(l=>l.grupo))].map(g=>({grupo: g, linhas: linhas.filter(l=>l.grupo === g), ...somar(linhas.filter(l=>l.grupo === g))}));
  return {orgaos, grupos, geral: somar(linhas)};
}
teste("mapa do exemplo: total estimado igual ao gabarito, centavo a centavo", ()=>{
  const s = dadosEmbutidos("seed"), m = montarMapa(s.itens, s.distribuicao);
  return m.geral.total_c === s.gabarito[0].total_estimado_c || `${m.geral.total_c} ≠ ${s.gabarito[0].total_estimado_c}`;
});
teste("mapa do exemplo: soma por órgão = total geral (exemplo limpo)", ()=>{
  const s = dadosEmbutidos("seed"), m = montarMapa(s.itens, s.distribuicao);
  return Object.values(m.geral.porOrgao).reduce((a, x)=>a + x.v, 0) === m.geral.total_c;
});

const origemAttr = o => o ? ` data-origem="${esc(`${o.arquivo} · aba ${o.aba} · linha ${o.linha}`)}" tabindex="0"` : "";
TELAS["#/mapa/:proc"] = async ({proc})=>{
  const p = await db.get("processos", proc);
  if (!p) return `<div class="card vazio">Processo não encontrado. <a href="#/processos">Voltar</a></div>`;
  const itens = await db.porIndice("itens", "id_processo", proc), dist = await db.porIndice("distribuicao", "id_processo", proc);
  if (!itens.length) return `<h1>Mapa · ${esc(p.numero)}</h1><div class="card vazio">Nenhum item. <a href="#/importar/${encodeURIComponent(proc)}">Importe a distribuição por órgão</a>.</div>`;
  const m = montarMapa(itens, dist), F = dinheiro.fmt;
  const cab = `<tr><th>Grupo</th><th>Item</th><th>Código</th><th>Descrição</th><th>Unid.</th><th class="num">Qtd</th><th class="num">V. unit. estimado</th><th class="num">Total estimado</th>
    ${m.orgaos.map(o=>`<th class="num">${esc(o)}<br>qtd</th><th class="num">${esc(o)}<br>valor</th>`).join("")}</tr>`;
  const linha = l => `<tr><td>${esc(l.grupo)}</td><td>${esc(l.item)}</td><td>${esc(l.codigo)}</td><td>${esc(l.descricao)}</td><td>${esc(l.unidade)}</td>
    <td class="num"${origemAttr(l.origem)}>${l.quantidade_total}</td><td class="num"${origemAttr(l.origem)}>${F(l.valor_unitario_estimado_c)}</td><td class="num">${F(l.total_c)}</td>
    ${m.orgaos.map(o=>`<td class="num"${origemAttr(l.porOrgao[o].origem)}>${l.porOrgao[o].q}</td><td class="num">${F(l.porOrgao[o].v)}</td>`).join("")}</tr>`;
  const soma = (rot, s, cls) => `<tr class="${cls}"><td colspan="7"><b>${rot}</b></td><td class="num"><b>${F(s.total_c)}</b></td>
    ${m.orgaos.map(o=>`<td class="num"><b>${s.porOrgao[o].q}</b></td><td class="num"><b>${F(s.porOrgao[o].v)}</b></td>`).join("")}</tr>`;
  return `<h1>Mapa por item · ${esc(p.numero)}</h1><p class="sub">Valores estimados (pesquisa de preço). Clique num número para ver de onde ele veio.
    <a href="#/importar/${encodeURIComponent(proc)}">Importar de novo</a></p>
    <div class="grade">${m.orgaos.map(o=>`<div class="card kpi"><div class="v" style="font-size:20px">${F(m.geral.porOrgao[o].v)}</div><div class="r">${esc(o)}</div></div>`).join("")}
      <div class="card kpi"><div class="v" style="font-size:20px" id="totalGeral">${F(m.geral.total_c)}</div><div class="r">Total geral estimado</div></div></div>
    <div id="origemValor" class="card" hidden></div>
    <div class="card tabela-wrap"><table id="tabelaMapa">${cab}${m.grupos.map(g=>g.linhas.map(linha).join("") + soma("Subtotal " + g.grupo, g, "subtotal")).join("")}
      ${soma("Total geral", m.geral, "total")}</table></div>`;
};
TELAS_DEPOIS["#/mapa/:proc"] = ()=>{
  const mostrar = el=>{ const box = $("#origemValor"); box.hidden = false; box.innerHTML = `<b>Origem:</b> ${esc(el.dataset.origem)}`; };
  $$("[data-origem]").forEach(el=>{ el.style.cursor = "pointer"; el.addEventListener("click", ()=>mostrar(el)); el.addEventListener("keydown", e=>{ if (e.key === "Enter") mostrar(el); }); });
};
