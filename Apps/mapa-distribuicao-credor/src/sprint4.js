/* ================= Sprints 4 a 7 · resultado, empresas, conferência, orçamento, exportação e auditoria ================= */
"use strict";

const SIT_ROTULO = {homologado:"Homologado", fracassado:"Fracassado", deserto:"Deserto", "sem resultado":"Sem resultado"};
const SEV_ROTULO = {bloqueia:"Bloqueia", alerta:"Alerta", informa:"Informa"};
const SEV_SELO = {bloqueia:"erro", alerta:"alerta", informa:"info"};
const chaveGI = (g, i)=> g + "|" + i;

/* ---------- os dados do processo em memória ---------- */
async function dadosDoProcesso(proc){
  const [itens, dist, res, dot, gab] = await Promise.all([
    db.porIndice("itens", "id_processo", proc),
    db.porIndice("distribuicao", "id_processo", proc),
    db.porIndice("resultado", "id_processo", proc),
    db.porIndice("dotacao", "id_processo", proc),
    db.list("gabarito")
  ]);
  return {itens, dist, res, dot, gab};
}

/* ---------- o motor: resultado por item, por órgão e por grupo ---------- */
function engine(dados){
  const resPor = new Map(dados.res.map(r=>[chaveGI(r.grupo, r.item), r]));
  const distPor = new Map();
  for (const d of dados.dist){
    const k = chaveGI(d.grupo, d.item), m = distPor.get(k) || {};
    m[d.orgao] = d.quantidade; distPor.set(k, m);
  }
  const orgaos = [...new Set(dados.dist.map(d=>d.orgao))].sort();
  const linhas = [...dados.itens]
    .sort((a, b)=> (a.grupo + a.item).localeCompare(b.grupo + b.item))
    .map(i=>{
      const k = chaveGI(i.grupo, i.item), r = resPor.get(k) || null;
      const situacao = r ? r.situacao : "sem resultado";
      const homologado = situacao === "homologado" && Number(r.valor_unitario_homologado_c) > 0;
      const totalEstimado = dinheiro.vezes(i.quantidade_total, i.valor_unitario_estimado_c);
      const vuHomologado = homologado ? r.valor_unitario_homologado_c : null;
      const totalHomologado = homologado ? dinheiro.vezes(i.quantidade_total, vuHomologado) : null;
      const qts = orgaos.map(o=> (distPor.get(k) || {})[o] || 0);
      const partes = homologado ? dinheiro.ratear(totalHomologado, qts) : orgaos.map(()=>0);
      const porOrgao = {};
      orgaos.forEach((o, idx)=> porOrgao[o] = {q: qts[idx], v: partes[idx]});
      return {
        grupo: i.grupo, item: i.item, codigo: i.codigo, descricao: i.descricao, unidade: i.unidade,
        tipo: i.tipo_despesa, qtd: i.quantidade_total, vuEstimado: i.valor_unitario_estimado_c, totalEstimado,
        situacao, empresa: r ? (r.empresa || "") : "", cnpj: r ? (r.cnpj || "") : "",
        vuHomologado, totalHomologado, economia: homologado ? totalEstimado - totalHomologado : null,
        porOrgao, somaQtd: qts.reduce((a, b)=>a + b, 0), origem: i.origem
      };
    });
  const grupos = [...new Set(linhas.map(l=>l.grupo))].map(g=>{
    const ls = linhas.filter(l=>l.grupo === g);
    const situacao = ls.some(l=>l.situacao === "homologado") ? "homologado"
      : ls.some(l=>l.situacao === "fracassado") ? "fracassado"
      : ls.some(l=>l.situacao === "deserto") ? "deserto" : "sem resultado";
    const comEmpresa = ls.find(l=>l.empresa) || {};
    return {
      grupo: g, tipo: ls[0].tipo, situacao, empresa: comEmpresa.empresa || "", cnpj: comEmpresa.cnpj || "", linhas: ls,
      totalEstimado: ls.reduce((a, l)=>a + l.totalEstimado, 0),
      totalHomologado: ls.reduce((a, l)=>a + (l.totalHomologado || 0), 0),
      qtdItens: ls.reduce((a, l)=>a + l.qtd, 0),
      qtdOrgaos: ls.reduce((a, l)=>a + l.somaQtd, 0)
    };
  });
  const totais = {
    estimado: linhas.reduce((a, l)=>a + l.totalEstimado, 0),
    homologado: linhas.reduce((a, l)=>a + (l.totalHomologado || 0), 0),
    economia: linhas.reduce((a, l)=>a + (l.economia || 0), 0)
  };
  const porOrgao = {};
  for (const o of orgaos) porOrgao[o] = {estimado:0, homologado:0, qtd:0};
  for (const l of linhas) for (const o of orgaos){
    porOrgao[o].qtd += l.porOrgao[o].q;
    porOrgao[o].estimado += dinheiro.vezes(l.porOrgao[o].q, l.vuEstimado);
    porOrgao[o].homologado += l.porOrgao[o].v;
  }
  const gab = (dados.gab || []).find(g=>g.id === "totais") || null;
  return {orgaos, linhas, grupos, totais, porOrgao, dotacao: dados.dot, gabarito: gab};
}

// o seed do exemplo vem com outros nomes de chave; o motor usa os do banco
function engineDeSeed(s){
  return engine({itens:s.itens || [], dist:s.distribuicao || [], res:s.resultado || [], dot:s.dotacao || [], gab:s.gabarito || []});
}

/* ---------- conferência: as divergências D01 a D09 ---------- */
function conferir(e){
  const F = dinheiro.fmt, div = [];
  const add = (codigo, onde, mensagem, regra, severidade)=> div.push({codigo, onde, mensagem, regra, severidade});
  for (const l of e.linhas){
    if (l.somaQtd !== l.qtd)
      add("D01", `Grupo ${l.grupo} · item ${l.item}`, `A soma por órgão (${l.somaQtd}) difere da quantidade total (${l.qtd}).`, "RN04", "bloqueia");
    if (l.situacao === "sem resultado")
      add("D02", `Grupo ${l.grupo} · item ${l.item}`, "Item da distribuição sem resultado no relatório do pregoeiro.", "RN02", "bloqueia");
    if (l.vuHomologado && l.vuHomologado > l.vuEstimado)
      add("D03", `Grupo ${l.grupo} · item ${l.item}`, `Homologado (${F(l.vuHomologado)}) maior que o estimado (${F(l.vuEstimado)}).`, "RN03", "alerta");
    if (l.situacao === "homologado" && (!l.empresa || !l.cnpj))
      add("D04", `Grupo ${l.grupo} · item ${l.item}`, "Grupo homologado sem empresa ou sem CNPJ.", "RN07", "bloqueia");
    if (l.cnpj && !cnpjValido(l.cnpj))
      add("D05", `Grupo ${l.grupo} · item ${l.item}`, `CNPJ ${l.cnpj} com dígito verificador inválido.`, "RN07", "bloqueia");
  }
  for (const g of e.grupos)
    if (g.qtdItens !== g.qtdOrgaos)
      add("D06", `Grupo ${g.grupo}`, `A soma por órgão (${g.qtdOrgaos}) não iguala o total do grupo (${g.qtdItens}).`, "RN04", "bloqueia");
  const dotSet = new Set(e.dotacao.map(d=> d.orgao + "|" + d.tipo));
  for (const g of e.grupos) for (const o of e.orgaos){
    if (g.linhas.some(l=>l.porOrgao[o].q > 0) && !dotSet.has(o + "|" + g.tipo))
      add("D07", `Grupo ${g.grupo} · ${o}`, `Órgão sem dotação do tipo ${g.tipo} (${g.tipo === 3 ? "custeio" : "investimento"}).`, "RN06", "alerta");
  }
  const o = orcamento(e);
  if (o.totais.proximo > 0)
    add("D08", "Distribuição orçamentária", `${F(o.totais.proximo)} vai para o ano seguinte (RN05).`, "RN05", "informa");
  if (e.gabarito){
    if (e.totais.estimado !== e.gabarito.total_estimado_c)
      add("D09", "Total do mapa", `Estimado ${F(e.totais.estimado)} difere do gabarito ${F(e.gabarito.total_estimado_c)}.`, "RN09", "bloqueia");
    if (e.totais.homologado !== e.gabarito.total_homologado_c)
      add("D09", "Total do mapa", `Homologado ${F(e.totais.homologado)} difere do gabarito ${F(e.gabarito.total_homologado_c)}.`, "RN09", "bloqueia");
  }
  return div;
}

/* ---------- orçamento: RN05, RN06 e RN10 ---------- */
function orcamento(e){
  const rem = new Map(e.dotacao.map(d=>[d.orgao + "|" + d.tipo, d.valor_c]));
  const dotInfo = new Map(e.dotacao.map(d=>[d.orgao + "|" + d.tipo, d]));
  const credores = [], resumos = new Map();
  // a dotação é consumida na ordem dos grupos do processo (RN10)
  for (const l of e.linhas){
    if (l.totalHomologado === null) continue;
    for (const o of e.orgaos){
      const valor = l.porOrgao[o].v;
      if (!valor) continue;
      const k = o + "|" + l.tipo;
      if (!resumos.has(k)) resumos.set(k, {orgao:o, tipo:l.tipo, dotacao: dotInfo.get(k) ? dotInfo.get(k).valor_c : 0, total:0, ano:0, proximo:0});
      const r = resumos.get(k);
      r.total += valor;
      const usa = Math.min(rem.get(k) || 0, valor);
      rem.set(k, (rem.get(k) || 0) - usa);
      r.ano += usa; r.proximo += valor - usa;
      credores.push({grupo:l.grupo, item:l.item, orgao:o, tipo:l.tipo, descricao:l.descricao, valor, ano:usa, proximo:valor - usa});
    }
  }
  const linhas = [...resumos.values()].sort((a, b)=> (a.orgao + String(a.tipo)).localeCompare(b.orgao + String(b.tipo)));
  const totais = {
    dotacao: linhas.reduce((a, l)=>a + l.dotacao, 0),
    total: linhas.reduce((a, l)=>a + l.total, 0),
    ano: linhas.reduce((a, l)=>a + l.ano, 0),
    proximo: linhas.reduce((a, l)=>a + l.proximo, 0)
  };
  return {linhas, credores, totais, semDotacao: linhas.filter(l=>!l.dotacao).length};
}

/* ---------- telas ---------- */
const cardKpi = (v, r)=> `<div class="card kpi"><div class="v">${v}</div><div class="r">${esc(r)}</div></div>`;
const seloSit = s=> `<span class="selo ${s === "homologado" ? "ok" : s === "sem resultado" ? "erro" : "alerta"}">${esc(SIT_ROTULO[s] || s)}</span>`;

async function processoOuAviso(proc){
  const p = await db.get("processos", proc);
  if (!p) return {erro:`<div class="card vazio">Processo não encontrado. <a href="#/processos">Voltar</a></div>`};
  return {p};
}
const linksDoProcesso = p=> `
  <p class="linha-botoes">
    <a class="botao" href="#/mapa/${encodeURIComponent(p.id)}">Mapa estimado</a>
    <a class="botao" href="#/resultado/${encodeURIComponent(p.id)}">Resultado</a>
    <a class="botao" href="#/empresas/${encodeURIComponent(p.id)}">Empresas</a>
    <a class="botao" href="#/conferencia/${encodeURIComponent(p.id)}">Conferência</a>
    <a class="botao" href="#/orcamento/${encodeURIComponent(p.id)}">Orçamentária</a>
    <a class="botao" href="#/exportar/${encodeURIComponent(p.id)}">Exportar</a>
    <a class="botao" href="#/auditoria/${encodeURIComponent(p.id)}">Auditoria</a>
  </p>`;

/* Sprint 4 · resultado do pregoeiro */
TELAS["#/resultado/:proc"] = async ({proc})=>{
  const {p, erro} = await processoOuAviso(proc);
  if (erro) return erro;
  const dados = await dadosDoProcesso(proc), e = engine(dados), F = dinheiro.fmt;
  if (!e.linhas.length) return `<h1>Resultado · ${esc(p.numero)}</h1><div class="card vazio">Nenhum item importado. <a href="#/importar/${encodeURIComponent(proc)}">Importar as fontes</a>.</div>`;
  const div = conferir(e), bloqueia = div.filter(d=>d.severidade === "bloqueia").length;
  const cab = `<tr><th>Grupo</th><th>Item</th><th>Descrição</th><th class="num">Qtd</th><th class="num">V. unit. estimado</th>
    <th class="num">Total estimado</th><th>Situação</th><th class="num">V. unit. homologado</th><th class="num">Total homologado</th><th class="num">Economia</th></tr>`;
  const linha = l=> `<tr><td>${esc(l.grupo)}</td><td>${esc(l.item)}</td><td>${esc(l.descricao)}</td><td class="num">${l.qtd}</td>
    <td class="num">${F(l.vuEstimado)}</td><td class="num">${F(l.totalEstimado)}</td><td>${seloSit(l.situacao)}</td>
    <td class="num">${l.vuHomologado === null ? "—" : F(l.vuHomologado)}</td>
    <td class="num">${l.totalHomologado === null ? `<span class="sub">${l.situacao === "homologado" ? "sem valor homologado" : "mantém o estimado"}</span>` : F(l.totalHomologado)}</td>
    <td class="num">${l.economia === null ? "—" : F(l.economia)}</td></tr>`;
  const porOrgaoCab = `<tr><th>Órgão</th><th class="num">Quantidade</th><th class="num">Estimado</th><th class="num">Homologado</th></tr>`;
  const porOrgaoLinha = Object.entries(e.porOrgao).map(([o, v])=> `<tr><td>${esc(o)}</td><td class="num">${v.qtd}</td>
    <td class="num">${F(v.estimado)}</td><td class="num">${F(v.homologado)}</td></tr>`);
  const gruposCab = `<tr><th>Grupo</th><th class="num">Tipo</th><th>Situação</th><th>Empresa</th><th>CNPJ</th><th class="num">Total estimado</th><th class="num">Total homologado</th></tr>`;
  const gruposLinha = e.grupos.map(g=> `<tr><td>${esc(g.grupo)}</td><td class="num">${g.tipo === 3 ? "3 · custeio" : "4 · investimento"}</td><td>${seloSit(g.situacao)}</td>
    <td>${esc(g.empresa || "—")}</td><td class="mono">${esc(g.cnpj || "—")}</td><td class="num">${F(g.totalEstimado)}</td>
    <td class="num">${g.totalHomologado ? F(g.totalHomologado) : "—"}</td></tr>`);
  return `<h1>Resultado · ${esc(p.numero)}</h1><p class="sub">${esc(p.nome)}. O homologado substitui o estimado (RN03); grupo fracassado ou deserto mantém as colunas do estimado com a observação do relatório (RN02).</p>
    ${linksDoProcesso(p)}
    <div class="grade">
      ${cardKpi(F(e.totais.estimado), "total estimado")}
      ${cardKpi(F(e.totais.homologado), "total homologado")}
      ${cardKpi(F(e.totais.economia), "economia")}
      ${cardKpi(e.grupos.length, "grupos")}
    </div>
    ${bloqueia ? `<div class="card pendente"><b>${bloqueia} divergência(s) bloqueiam</b> a conferência e a distribuição orçamentária. <a href="#/conferencia/${encodeURIComponent(proc)}">Ver a conferência</a>.</div>` : ""}
    <div class="card tabela-wrap"><h2>Itens do processo</h2><table>${cab}${e.linhas.map(linha).join("")}</table></div>
    <div class="card tabela-wrap"><h2>Por órgão</h2><table>${porOrgaoCab}${porOrgaoLinha.join("")}</table></div>
    <div class="card tabela-wrap"><h2>Situação dos grupos</h2><table>${gruposCab}${gruposLinha.join("")}</table></div>
    <form class="card" id="formEdicao"><h2 style="margin-top:0">Edição manual de valor homologado</h2>
      <p class="sub">A edição pede justificativa e fica na trilha de auditoria com o valor anterior e o novo.</p>
      <div class="campos">
        ${campo("edItem", "Item", {tipo:"select", opcoes:[["", "Escolha o item"], ...e.linhas.map(l=>[l.grupo + "|" + l.item, l.grupo + " · item " + l.item])]})}
        ${campo("edValor", "Novo valor unitário homologado", {tipo:"text", attrs:'placeholder="R$ 90,00"'})}
        ${campo("edJustificativa", "Justificativa", {tipo:"textarea", linhas:2, obrigatorio:true})}
      </div><div id="errosEdicao"></div>
      <div class="linha-botoes"><button class="prim" type="submit">Salvar edição</button></div></form>`;
};
TELAS_DEPOIS["#/resultado/:proc"] = async ({proc})=>{
  const form = $("#formEdicao"); if (!form) return;
  form.addEventListener("submit", async ev=>{
    ev.preventDefault();
    const chave = valorDe("edItem"), valorTxt = valorDe("edValor"), justificativa = valorDe("edJustificativa");
    if (!chave) return mostrarErros("#errosEdicao", ["Escolha o item."]);
    if (!justificativa) return mostrarErros("#errosEdicao", ["Escreva a justificativa."]);
    const cents = dinheiro.de(valorTxt);
    if (!(cents > 0)) return mostrarErros("#errosEdicao", ["Informe um valor unitário maior que zero."]);
    const [g, i] = chave.split("|"), anterior = await db.get("resultado", `${proc}|${g}|${i}`);
    if (!anterior) return mostrarErros("#errosEdicao", ["O item não tem resultado do pregoeiro."]);
    await db.put("resultado", {...anterior, valor_unitario_homologado_c: cents, editado_em: agora(), justificativa});
    await registrar("edição de valor homologado", {id_processo: proc, item: `${g} · ${i}`,
      valor_anterior_c: anterior.valor_unitario_homologado_c, valor_novo_c: cents, justificativa});
    toast("Edição salva na trilha de auditoria.");
    navegar();
  });
};

/* Sprint 5 · empresas por órgão */
TELAS["#/empresas/:proc"] = async ({proc})=>{
  const {p, erro} = await processoOuAviso(proc);
  if (erro) return erro;
  const e = engine(await dadosDoProcesso(proc)), F = dinheiro.fmt;
  const mapa = new Map();
  for (const l of e.linhas){
    if (!l.empresa) continue;
    const chave = l.empresa + "|" + l.cnpj;
    if (!mapa.has(chave)) mapa.set(chave, {empresa:l.empresa, cnpj:l.cnpj, grupos:new Set(), itens:0, qtd:0, valor:0, orgaos:new Map()});
    const e2 = mapa.get(chave);
    e2.grupos.add(l.grupo); e2.itens++; e2.qtd += l.qtd; e2.valor += l.totalHomologado || 0;
    for (const o of e.orgaos){
      const v = l.porOrgao[o].v; if (!v) continue;
      e2.orgaos.set(o, (e2.orgaos.get(o) || 0) + v);
    }
  }
  const lista = [...mapa.values()].sort((a, b)=> b.valor - a.valor);
  const cab = `<tr><th>Empresa</th><th>CNPJ</th><th>Grupos</th><th class="num">Itens</th><th class="num">Qtd</th>
    <th class="num">Total homologado</th>${e.orgaos.map(o=>`<th class="num">${esc(o)}</th>`).join("")}</tr>`;
  const linha = x=> `<tr><td>${esc(x.empresa)}</td><td class="mono">${esc(x.cnpj)}</td><td>${[...x.grupos].sort().join(", ")}</td>
    <td class="num">${x.itens}</td><td class="num">${x.qtd}</td><td class="num">${F(x.valor)}</td>
    ${e.orgaos.map(o=>`<td class="num">${x.orgaos.get(o) ? F(x.orgaos.get(o)) : "—"}</td>`).join("")}</tr>`;
  const semEmpresa = e.linhas.filter(l=> l.situacao === "homologado" && !l.empresa).length;
  return `<h1>Empresas · ${esc(p.numero)}</h1><p class="sub">${esc(p.nome)}. Cada linha é uma empresa vencedora, com os órgãos participantes e o valor homologado (RN03).</p>
    ${linksDoProcesso(p)}
    ${semEmpresa ? `<div class="card pendente"><b>${semEmpresa} item(ns) homologado(s) sem empresa.</b> A conferência aponta isso como D04.</div>` : ""}
    <div class="card tabela-wrap"><table>${cab}${lista.map(linha).join("") || `<tr><td colspan="${6 + e.orgaos.length}">Nenhuma empresa homologada.</td></tr>`}</table></div>`;
};

/* Sprint 5 · conferência */
TELAS["#/conferencia/:proc"] = async ({proc})=>{
  const {p, erro} = await processoOuAviso(proc);
  if (erro) return erro;
  const e = engine(await dadosDoProcesso(proc)), div = conferir(e);
  const cont = {bloqueia:0, alerta:0, informa:0};
  for (const d of div) cont[d.severidade]++;
  const bloqueia = cont.bloqueia;
  const linha = d=> `<tr><td><b>${esc(d.codigo)}</b></td><td><span class="selo ${SEV_SELO[d.severidade]}">${esc(SEV_ROTULO[d.severidade])}</span></td>
    <td>${esc(d.onde)}</td><td>${esc(d.mensagem)}</td><td class="mono">${esc(d.regra)}</td></tr>`;
  return `<h1>Conferência · ${esc(p.numero)}</h1><p class="sub">${esc(p.nome)}. As divergências são as do checklist do projeto (D01 a D09). Divergência que bloqueia impede a distribuição orçamentária.</p>
    ${linksDoProcesso(p)}
    <div class="grade">
      ${cardKpi(cont.bloqueia, "bloqueiam")}${cardKpi(cont.alerta, "alertam")}${cardKpi(cont.informa, "informam")}
      ${cardKpi(div.length, "divergências")}
    </div>
    ${!div.length ? `<div class="card vazio"><b>Nenhuma divergência.</b> Os totais batem com o gabarito e o mapa pode seguir para a distribuição orçamentária.</div>`
      : `${!bloqueia.length ? `<div class="card"><b>Nenhuma divergência que bloqueie.</b> As linhas abaixo são avisos, que não impedem a distribuição orçamentária.</div>` : ""}
      <div class="card tabela-wrap"><table><tr><th>Código</th><th>Situação</th><th>Onde</th><th>O que aconteceu</th><th>Regra</th></tr>
      ${div.map(linha).join("")}</table></div>`}`;
};

/* Sprint 6 · distribuição orçamentária */
TELAS["#/orcamento/:proc"] = async ({proc})=>{
  const {p, erro} = await processoOuAviso(proc);
  if (erro) return erro;
  const e = engine(await dadosDoProcesso(proc)), o = orcamento(e), F = dinheiro.fmt;
  const div = conferir(e), bloqueia = div.filter(d=>d.severidade === "bloqueia");
  const validado = await db.meta("dotacao_validada:" + proc);
  const cab = `<tr><th>Órgão</th><th class="num">Tipo</th><th class="num">Dotação</th><th class="num">A distribuir</th>
    <th class="num">Ano corrente</th><th class="num">Ano seguinte</th></tr>`;
  const linha = l=> `<tr><td>${esc(l.orgao)}</td><td class="num">${l.tipo === 3 ? "3 · custeio" : "4 · investimento"}</td>
    <td class="num">${l.dotacao ? F(l.dotacao) : `<span class="selo alerta">sem dotação</span>`}</td><td class="num">${F(l.total)}</td>
    <td class="num">${F(l.ano)}</td><td class="num">${F(l.proximo)}</td></tr>`;
  const credCab = `<tr><th>Grupo</th><th class="num">Item</th><th>Órgão</th><th>Descrição</th><th class="num">Valor</th>
    <th class="num">Ano corrente</th><th class="num">Ano seguinte</th></tr>`;
  const credLinha = c=> `<tr><td>${esc(c.grupo)}</td><td class="num">${esc(c.item)}</td><td>${esc(c.orgao)}</td><td>${esc(c.descricao)}</td>
    <td class="num">${F(c.valor)}</td><td class="num">${F(c.ano)}</td><td class="num">${F(c.proximo)}</td></tr>`;
  const prox = o.totais.proximo;
  return `<h1>Distribuição orçamentária · ${esc(p.numero)}</h1><p class="sub">${esc(p.nome)}. A dotação é consumida na ordem dos grupos do processo (RN10); o que não cabe no ano corrente vai para o ano seguinte (RN05).</p>
    ${linksDoProcesso(p)}
    ${bloqueia.length ? `<div class="card pendente"><b>${bloqueia.length} divergência(s) bloqueiam</b> a distribuição orçamentária. <a href="#/conferencia/${encodeURIComponent(proc)}">Ver a conferência</a>.</div>` : ""}
    ${prox ? `<div class="card pendente"><b>${F(prox)}</b> vai para o ano seguinte (D08). O app informa o valor; a decisão é da chefia.</div>` : ""}
    <div class="grade">
      ${cardKpi(F(o.totais.dotacao), "dotação do processo")}
      ${cardKpi(F(o.totais.total), "a distribuir")}
      ${cardKpi(F(o.totais.ano), "ano corrente")}
      ${cardKpi(F(o.totais.proximo), "ano seguinte")}
    </div>
    <div class="card tabela-wrap"><h2>Por órgão e tipo</h2><table>${cab}${o.linhas.map(linha).join("")}</table></div>
    <div class="card tabela-wrap"><h2>Por credor (grupo) e órgão</h2><table>${credCab}${o.credores.map(credLinha).join("")}</table></div>
    <form class="card" id="formDotacao"><h2 style="margin-top:0">Validação da dotação</h2>
      <p class="sub">O app não decide: a chefia informa o nome de quem validou e a data, e a validação fica na trilha.</p>
      <div class="campos">
        ${campo("dotNome", "Validado por", {obrigatorio:true, attrs:'placeholder="Nome de quem validou"'})}
        ${campo("dotData", "Data", {tipo:"date", valor:hojeISO(), obrigatorio:true})}
      </div><div id="errosDotacao"></div>
      <div class="linha-botoes"><button class="prim" type="submit">Registrar validação</button></div>
      ${validado ? `<p class="sub" style="margin-top:12px">Validado por <b>${esc(validado.nome)}</b> em ${esc(dataCurtaBR(validado.data))}.</p>` : ""}</form>`;
};
TELAS_DEPOIS["#/orcamento/:proc"] = async ({proc})=>{
  const form = $("#formDotacao"); if (!form) return;
  form.addEventListener("submit", async ev=>{
    ev.preventDefault();
    const nome = valorDe("dotNome"), data = valorDe("dotData");
    if (!mostrarErros("#errosDotacao", [!nome && "Informe quem validou.", !data && "Informe a data."].filter(Boolean))) return;
    await db.meta("dotacao_validada:" + proc, {nome, data});
    await registrar("dotação validada", {id_processo: proc, nome, data});
    toast("Validação registrada.");
    navegar();
  });
};

/* Sprint 7 · exportação */
function abasDoExcel(e, o, div, auditoria, p){
  const reais = c=> c === null || c === undefined ? null : Math.round(c) / 100;
  const abas = [];
  abas.push(["Mapa por item", e.linhas.map(l=>({
    Grupo:l.grupo, Item:l.item, Codigo:l.codigo, Descricao:l.descricao, Unidade:l.unidade, "Tipo despesa":l.tipo,
    Quantidade:l.qtd, "Valor unitário estimado":reais(l.vuEstimado), "Total estimado":reais(l.totalEstimado),
    Situação:SIT_ROTULO[l.situacao], "Valor unitário homologado":reais(l.vuHomologado),
    "Total homologado":reais(l.totalHomologado), Economia:reais(l.economia),
    "Arquivo de origem":l.origem ? l.origem.arquivo : "", "Linha de origem":l.origem ? l.origem.linha : ""
  }))]);
  const linhasOrgao = [];
  for (const l of e.linhas) for (const o2 of e.orgaos) if (l.porOrgao[o2].q)
    linhasOrgao.push({Grupo:l.grupo, Item:l.item, "Órgão":o2, Quantidade:l.porOrgao[o2].q,
      "Valor estimado":reais(dinheiro.vezes(l.porOrgao[o2].q, l.vuEstimado)), "Valor homologado":reais(l.porOrgao[o2].v)});
  abas.push(["Mapa por órgão", linhasOrgao]);
  abas.push(["Resultado", e.linhas.map(l=>({
    Grupo:l.grupo, Item:l.item, Descricao:l.descricao, Situação:SIT_ROTULO[l.situacao], Empresa:l.empresa, CNPJ:l.cnpj,
    "Valor unitário estimado":reais(l.vuEstimado), "Valor unitário homologado":reais(l.vuHomologado),
    "Total estimado":reais(l.totalEstimado), "Total homologado":reais(l.totalHomologado), Economia:reais(l.economia)
  }))]);
  abas.push(["Situação dos grupos", e.grupos.map(g=>({
    Grupo:g.grupo, "Tipo (3 custeio / 4 investimento)":g.tipo, Situação:SIT_ROTULO[g.situacao], Empresa:g.empresa, CNPJ:g.cnpj,
    "Total estimado":reais(g.totalEstimado), "Total homologado":reais(g.totalHomologado)
  }))]);
  const linhasEmp = [];
  for (const l of e.linhas){
    if (!l.empresa) continue;
    for (const o2 of e.orgaos) if (l.porOrgao[o2].v)
      linhasEmp.push({Empresa:l.empresa, CNPJ:l.cnpj, Grupo:l.grupo, Item:l.item, "Órgão":o2,
        Descricao:l.descricao, Quantidade:l.porOrgao[o2].q, "Valor homologado":reais(l.porOrgao[o2].v)});
  }
  abas.push(["Empresas e órgãos", linhasEmp]);
  abas.push(["Conferência", div.map(d=>({Código:d.codigo, Situação:SEV_ROTULO[d.severidade], Onde:d.onde,
    "O que aconteceu":d.mensagem, Regra:d.regra}))]);
  abas.push(["Distribuição orçamentária", [
    ...o.linhas.map(l=>({Órgão:l.orgao, Tipo:l.tipo, Dotação:reais(l.dotacao), "A distribuir":reais(l.total),
      "Ano corrente":reais(l.ano), "Ano seguinte":reais(l.proximo)})),
    ...o.credores.map(c=>({Órgão:c.orgao, Tipo:c.tipo, Grupo:c.grupo, Item:c.item, Descricao:c.descricao,
      Valor:reais(c.valor), "Ano corrente":reais(c.ano), "Ano seguinte":reais(c.proximo)}))
  ]]);
  abas.push(["Auditoria", auditoria.map(a=>({Quando:a.data_hora, Perfil:a.perfil, Ação:a.acao,
    Detalhe:JSON.stringify(a.detalhe || {}), Item:a.item || "", Justificativa:a.justificativa || ""}))]);
  return abas;
}

TELAS["#/exportar/:proc"] = async ({proc})=>{
  const {p, erro} = await processoOuAviso(proc);
  if (erro) return erro;
  const e = engine(await dadosDoProcesso(proc)), o = orcamento(e), div = conferir(e);
  const auditoria = (await db.list("auditoria")).filter(a=> a.id_processo === proc);
  const F = dinheiro.fmt;
  const linhasDiv = div.map(d=> `<tr><td><b>${esc(d.codigo)}</b></td><td>${esc(SEV_ROTULO[d.severidade])}</td><td>${esc(d.onde)}</td>
    <td>${esc(d.mensagem)}</td><td>${esc(d.regra)}</td></tr>`).join("");
  return `<h1>Exportar · ${esc(p.numero)}</h1><p class="sub">${esc(p.nome)}. O Excel sai com 8 abas, uma por etapa do processo, com os valores como número.</p>
    ${linksDoProcesso(p)}
    <div class="linha-botoes nao-imprimir"><button class="prim" id="btnExcel">Gerar Excel com 8 abas</button>
      <button id="btnImprimir">Imprimir o relatório de divergências</button>
      <button id="btnJson">Baixar o JSON do processo</button></div>
    <div class="card documento-a4" id="relatorioImpressao">
      <div class="impressao-cab"><b>Mapa de Distribuição</b><span>Relatório de divergências · ${esc(p.numero)}</span></div>
      <h2 style="margin-top:0">Relatório de divergências</h2>
      <p class="sub">Processo ${esc(p.numero)} · ${esc(p.nome)} · ${esc(dataBR(agora()))}</p>
      ${div.length ? `<div class="tabela-wrap"><table><tr><th>Código</th><th>Situação</th><th>Onde</th><th>O que aconteceu</th><th>Regra</th></tr>${linhasDiv}</table></div>`
        : `<p>Não há divergência neste processo.</p>`}
      <p class="sub">Totais: estimado ${F(e.totais.estimado)} · homologado ${F(e.totais.homologado)} · ano corrente ${F(o.totais.ano)} · ano seguinte ${F(o.totais.proximo)}.</p></div>`;
};
TELAS_DEPOIS["#/exportar/:proc"] = async ({proc})=>{
  const btnExcel = $("#btnExcel"); if (!btnExcel) return;
  const p = await db.get("processos", proc);
  const e = engine(await dadosDoProcesso(proc)), o = orcamento(e), div = conferir(e);
  const auditoria = (await db.list("auditoria")).filter(a=> a.id_processo === proc);
  btnExcel.onclick = ()=>{
    const wb = XLSX.utils.book_new();
    for (const [nome, linhas] of abasDoExcel(e, o, div, auditoria, p)){
      const ws = XLSX.utils.json_to_sheet(linhas.length ? linhas : [{Observação:"sem dados"}]);
      ws["!cols"] = Object.keys(linhas.length ? linhas[0] : {Observação:1}).map(k=>({wch: Math.max(12, k.length + 2)}));
      XLSX.utils.book_append_sheet(wb, ws, nome);
    }
    const saida = XLSX.write(wb, {bookType:"xlsx", type:"array"});
    const nome = `Mapa_Distribuicao_${String(p.numero || proc).replace(/[^\w-]+/g, "_")}.xlsx`;
    baixar(nome, saida, "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet");
    registrar("exportação do Excel", {id_processo: proc, arquivo: nome});
    toast("Excel gerado: " + nome);
  };
  $("#btnImprimir").onclick = ()=> window.print();
  const resultado = await db.porIndice("resultado", "id_processo", proc);
  const dotacao = await db.porIndice("dotacao", "id_processo", proc);
  $("#btnJson").onclick = ()=>{
    const pacote = {app: APP.id, versao: APP.db.versao, exportado_em: agora(),
      dados: {processos: [p], itens: e.linhas, resultado, dotacao}};
    baixar(`mapa_${String(p.numero || proc).replace(/[^\w-]+/g, "_")}.json`, JSON.stringify(pacote, null, 2), "application/json");
  };
};

/* Sprint 7 · auditoria */
TELAS["#/auditoria/:proc"] = async ({proc})=>{
  const {p, erro} = await processoOuAviso(proc);
  if (erro) return erro;
  const todos = await db.list("auditoria");
  const doProcesso = todos.filter(a=> a.id_processo === proc);
  const validacoes = doProcesso.filter(a=> a.acao === "dotação validada");
  const edicoes = doProcesso.filter(a=> a.acao === "edição de valor homologado");
  const importacoes = doProcesso.filter(a=> a.acao === "importação");
  const linha = a=> `<tr><td>${esc(dataBR(a.data_hora))}</td><td>${esc(a.perfil || "—")}</td><td>${esc(a.acao)}</td>
    <td>${esc(a.item || "—")}</td><td>${esc(a.arquivo || a.fonte || "—")}</td><td>${esc(a.justificativa || "")}</td></tr>`;
  const detalheEdicao = edicoes.map(a=> `<li>${esc(dataBR(a.data_hora))} · <b>${esc(a.item)}</b>: ${dinheiro.fmt(a.valor_anterior_c)} → ${dinheiro.fmt(a.valor_novo_c)} (${esc(a.justificativa || "sem justificativa")})</li>`).join("");
  const detalheValid = validacoes.map(a=> `<li>${esc(dataBR(a.data_hora))} · ${esc(a.nome)}</li>`).join("");
  return `<h1>Auditoria · ${esc(p.numero)}</h1><p class="sub">${esc(p.nome)}. Importações, edições e validações, com data, perfil e origem do arquivo.</p>
    ${linksDoProcesso(p)}
    <div class="grade">
      ${cardKpi(importacoes.length, "importações")}${cardKpi(edicoes.length, "edições")}
      ${cardKpi(validacoes.length, "validações")}${cardKpi(doProcesso.length, "registros")}
    </div>
    ${detalheEdicao ? `<div class="card"><h2 style="margin-top:0">Edições de valor</h2><ul>${detalheEdicao}</ul></div>` : ""}
    ${detalheValid ? `<div class="card"><h2 style="margin-top:0">Validações da dotação</h2><ul>${detalheValid}</ul></div>` : ""}
    <div class="card tabela-wrap"><h2>Trilha</h2><table><tr><th>Quando</th><th>Perfil</th><th>Ação</th><th>Item</th><th>Arquivo</th><th>Justificativa</th></tr>
      ${doProcesso.sort((a, b)=> String(b.data_hora).localeCompare(String(a.data_hora))).map(linha).join("") || `<tr><td colspan="6">Nenhum registro neste processo.</td></tr>`}</table></div>`;
};

/* ---------- testes do motor ---------- */
const seedDoApp = ()=> dadosEmbutidos("seed");
teste("motor: total estimado do exemplo bate com o gabarito", ()=>{
  const s = seedDoApp(), e = engineDeSeed(s);
  return e.totais.estimado === s.gabarito[0].total_estimado_c || `${e.totais.estimado} ≠ ${s.gabarito[0].total_estimado_c}`;
});
teste("motor: total homologado do exemplo bate com o gabarito", ()=>{
  const s = seedDoApp(), e = engineDeSeed(s);
  return e.totais.homologado === s.gabarito[0].total_homologado_c || `${e.totais.homologado} ≠ ${s.gabarito[0].total_homologado_c}`;
});
teste("orçamento: ano corrente e ano seguinte batem com o gabarito", ()=>{
  const s = seedDoApp(), o = orcamento(engineDeSeed(s)), g = s.gabarito[0];
  const ok = o.totais.ano === g.orcamento_ano_c && o.totais.proximo === g.orcamento_ano_seguinte_c;
  return ok || `ano ${o.totais.ano}/${g.orcamento_ano_c} · prox ${o.totais.proximo}/${g.orcamento_ano_seguinte_c}`;
});
teste("conferência: o exemplo limpo não tem divergência bloqueante", ()=>{
  const s = seedDoApp(), div = conferir(engineDeSeed(s));
  const bloqueia = div.filter(d=>d.severidade === "bloqueia");
  return bloqueia.length === 0 || bloqueia.map(d=>d.codigo + " em " + d.onde).join("; ");
});
teste("orçamento: a soma do ano corrente e do seguinte é o total a distribuir", ()=>{
  const s = seedDoApp(), o = orcamento(engineDeSeed(s));
  return o.totais.ano + o.totais.proximo === o.totais.total;
});
teste("resultado: grupo fracassado mantém o estimado e não soma no homologado", ()=>{
  const s = seedDoApp(), e = engineDeSeed(s);
  const g = e.grupos.find(x=>x.situacao === "fracassado");
  if (!g) return true;
  return g.totalHomologado === 0 || `grupo ${g.grupo} somou ${g.totalHomologado}`;
});
