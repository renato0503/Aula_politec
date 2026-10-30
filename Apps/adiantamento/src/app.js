/* Controle de Adiantamentos · código do app (o construir.py junta com a base comum) */
"use strict";
TELAS["#/painel"] = async ()=> `<h1>Painel</h1><p class="sub">O painel com prazos chega no Sprint 6. Resumo da base:</p>
  ${await resumoBase(["processos", "etapas", "pendencias", "notas", "feriados"])}
  <p class="sub"><a href="#/pedido/novo">Novo pedido</a> · Para testar, carregue os dados fictícios em <a href="#/config">Configuração</a>.</p>`;
teste("Exemplo traz 20 feriados nacionais, 2 estaduais e 2 municipais", ()=>{
  const f = dadosEmbutidos("seed")?.feriados || [];
  return f.length === 24 && f.filter(x=>x.escopo === "nacional").length === 20
    && f.filter(x=>x.escopo === "estadual").length === 2 && f.filter(x=>x.escopo === "municipal").length === 2;
});
teste("Só os feriados nacionais e estaduais entram no prazo (recurso federal)", ()=>{
  const f = dadosEmbutidos("seed").feriados;
  const contam = f.filter(x=>x.escopo !== "municipal").map(x=>x.data);
  return !contam.includes("2026-04-08") && contam.includes("2026-04-02");
});
teste("Exemplo sem CPF", ()=> !JSON.stringify(dadosEmbutidos("seed")).toLowerCase().includes('"cpf"'));

/* ================= Sprint 2 · Novo pedido (RN01, RN02) ================= */
// As 12 etapas do AS-IS (PROJETO.md). O pedido entra na DAS (RN02).
const ETAPAS = ["Levantar orçamentos", "Análise da DAS", "Cadastro no SICAD", "Aprovação da chefia", "Conferência SESP",
  "Dotação (NGER)", "Autorização do ordenador", "Pagamento", "Aplicação do recurso", "Prestação de contas", "Análise da contabilidade", "Encerrado"];
const TIPOS = [["compra", "Compra de material"], ["serviço", "Serviço"], ["predial", "Intervenção predial simplificada (180 dias)"]];

// RN01: 3 orçamentos completos (fornecedor, CNPJ válido, valor) e a justificativa
function validarPedido(p, orcs){
  const e = [];
  if (!p.unidade) e.push("Informe a unidade solicitante.");
  if (!p.solicitante) e.push("Informe o nome do solicitante.");
  if (!/^\d{3,}$/.test(p.matricula || "")) e.push("A matrícula só aceita números.");
  if (!p.finalidade) e.push("Informe a finalidade.");
  if (!(p.valor_solicitado > 0)) e.push("Informe o valor solicitado.");
  const completos = orcs.filter(o=>o.fornecedor && o.valor > 0 && cnpjValido(o.cnpj));
  orcs.forEach((o, i)=>{
    if ((o.fornecedor || o.cnpj || o.valor) && !cnpjValido(o.cnpj)) e.push(`Orçamento ${i + 1}: CNPJ inválido.`);
  });
  if (completos.length < 3) e.push(`O pedido exige 3 orçamentos completos (RN01); há ${completos.length}.`);
  if ((p.justificativa || "").trim().length < 30) e.push("Escreva a justificativa da necessidade (RN01), com pelo menos 30 caracteres.");
  return e;
}
teste("RN01: 2 orçamentos são recusados", ()=> validarPedido({unidade: "x", solicitante: "x", matricula: "123", finalidade: "x", valor_solicitado: 10, justificativa: "x".repeat(30)},
  [{fornecedor: "A", cnpj: "11222333000181", valor: 1}, {fornecedor: "B", cnpj: "11222333000181", valor: 1}]).some(x=>x.includes("RN01")));

TELAS["#/pedido/novo"] = async ()=>{
  const unidades = [...new Set((await db.list("processos")).map(p=>p.unidade))].sort();
  return `<h1>Novo pedido de adiantamento</h1><p class="sub">Registro na DAS antes do cadastro no SICAD (RN02). O SICAD continua sendo o sistema oficial.</p>
    <form id="formPedido"><div class="card"><h2 style="margin-top:0">Pedido</h2><div class="campos">
      ${campo("pUnidade", "Unidade solicitante", {obrigatorio: true, attrs: 'list="listaUnidades"'})}
      ${campo("pSolicitante", "Solicitante (nome)", {obrigatorio: true})}
      ${campo("pMatricula", "Matrícula", {obrigatorio: true, attrs: 'inputmode="numeric"'})}
      ${campo("pTipo", "Tipo", {tipo: "select", opcoes: TIPOS})}
      ${campo("pValor", "Valor solicitado (R$)", {obrigatorio: true, attrs: 'inputmode="decimal" placeholder="0,00"'})}
      </div><datalist id="listaUnidades">${unidades.map(u=>`<option value="${esc(u)}">`).join("")}</datalist>
      ${campo("pFinalidade", "Finalidade", {obrigatorio: true})}
      ${campo("pJust", "Justificativa da necessidade", {tipo: "textarea", obrigatorio: true})}</div>
    <div class="card"><h2 style="margin-top:0">Três orçamentos (RN01)</h2>
      ${[1, 2, 3].map(i=>`<div class="campos">${campo(`oForn${i}`, `Fornecedor ${i}`)}${campo(`oCnpj${i}`, "CNPJ", {attrs: 'inputmode="numeric" placeholder="00.000.000/0000-00"'})}
        ${campo(`oValor${i}`, "Valor (R$)", {attrs: 'inputmode="decimal"'})}</div>`).join("")}
      <p class="sub" id="menorOrc"></p></div>
    <div id="errosPedido"></div>
    <div class="linha-botoes"><button class="prim" type="submit">Registrar pedido</button><a class="botao" href="#/painel">Cancelar</a></div></form>`;
};
TELAS_DEPOIS["#/pedido/novo"] = ()=>{
  const orcs = ()=>[1, 2, 3].map(i=>({fornecedor: valorDe(`oForn${i}`), cnpj: valorDe(`oCnpj${i}`).replace(/\D/g, ""), valor: (dinheiro.de(valorDe(`oValor${i}`)) || 0) / 100}));
  const menor = ()=>{ const v = orcs().filter(o=>o.valor > 0).map(o=>o.valor); $("#menorOrc").textContent = v.length ? `Menor orçamento: ${dinheiro.fmt(Math.round(Math.min(...v) * 100))}` : ""; };
  [1, 2, 3].forEach(i=>{
    $(`#oValor${i}`).addEventListener("input", menor);
    $(`#oCnpj${i}`).addEventListener("blur", e=>{ const d = e.target.value.replace(/\D/g, ""); e.target.style.borderColor = d && !cnpjValido(d) ? "var(--vermelho)" : ""; });
  });
  $("#formPedido").addEventListener("submit", async e=>{
    e.preventDefault();
    const p = {unidade: valorDe("pUnidade"), solicitante: valorDe("pSolicitante"), matricula: valorDe("pMatricula"), tipo: valorDe("pTipo"),
               valor_solicitado: (dinheiro.de(valorDe("pValor")) || 0) / 100, finalidade: valorDe("pFinalidade"), justificativa: valorDe("pJust")};
    const os = orcs();
    if (!mostrarErros("#errosPedido", validarPedido(p, os))) return;
    const ano = new Date().getFullYear(), seq = (await db.list("processos")).filter(x=>x.id.startsWith(`AD-${ano}-`)).length + 1;
    const id = `AD-${ano}-${String(seq).padStart(3, "0")}`, hoje = hojeISO();
    await db.put("processos", {id, numero_sicad: "", ...p, valor_concedido: null, situacao: "em andamento", etapa_atual: ETAPAS[1], pago_em: null, criado_em: hoje});
    for (const [i, o] of os.entries()) await db.put("orcamentos", {id: `${id}-O${i + 1}`, processo_id: id, ...o});
    await db.put("etapas", {id: `${id}-E00`, processo_id: id, etapa: ETAPAS[0], entrada_em: hoje, saida_em: hoje, responsavel: p.unidade});
    await db.put("etapas", {id: `${id}-E01`, processo_id: id, etapa: ETAPAS[1], entrada_em: hoje, saida_em: null, responsavel: "DAS"});
    await registrar("pedido registrado", {processo_id: id, detalhe: p.finalidade});
    toast(`Pedido ${id} registrado na DAS.`); location.hash = "#/painel";
  });
};
