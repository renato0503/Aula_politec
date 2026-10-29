/* Banco de Demandas · código do app (o construir.py junta com a base comum) */
"use strict";
async function configExtra(){
  const unidades = await db.list("unidades"); const atual = await db.meta("unidade_id");
  return `<div class="card"><h2 style="margin-top:0">Unidade e usuário desta cópia</h2>
    <p class="sub">A unidade define de quem são as demandas criadas aqui. O usuário fica registrado como autor (criado_por).</p>
    <div class="campos">
    ${unidades.length ? campo("selUnidade", "Unidade", {tipo: "select", opcoes: [["", "Escolha"], ...unidades.map(u=>[u.id, u.nome])], valor: atual || ""})
      : `<p class="sub">Carregue os dados fictícios para escolher uma unidade.</p>`}
    ${campo("cfgUsuario", "Seu usuário", {valor: (await db.meta("usuario")) || "", ajuda: "O mesmo login do Hórus, para a exportação bater."})}
    </div></div>`;
}
async function ligarConfigExtra(){
  $("#selUnidade")?.addEventListener("change", async e=>{ await db.meta("unidade_id", e.target.value); await registrar("unidade da cópia", {detalhe: e.target.value}); toast("Unidade salva."); });
  $("#cfgUsuario")?.addEventListener("change", async e=>{ await db.meta("usuario", e.target.value.trim()); toast("Usuário salvo."); });
}
teste("R9: segunda manifestação da mesma unidade no mesmo item é recusada", async ()=>{
  const a = {id: "t1", banco_demanda_id: "dX", unidade_id: "uX"}, b = {id: "t2", banco_demanda_id: "dX", unidade_id: "uX"};
  await db.put("banco_demanda_manifestacoes", a); let recusou = false;
  try { await db.put("banco_demanda_manifestacoes", b); } catch(e){ recusou = true; }
  await db.del("banco_demanda_manifestacoes", "t1"); await db.del("banco_demanda_manifestacoes", "t2");
  return recusou;
});

TELAS["#/banco"] = async ()=>{
  const n = (await db.list("banco_demandas")).length;
  return `<h1>Banco de Demandas · repositório (${n})</h1><p class="sub">A grade de cards chega no Sprint 3. Resumo da base:</p>
    ${await resumoBase(["unidades", "ciclos", "banco_demandas", "banco_demanda_manifestacoes", "banco_demanda_inclusoes"])}
    <p class="sub"><a href="#/demanda/nova">Nova demanda</a> · Para testar, carregue os dados fictícios em <a href="#/config">Configuração</a>.</p>`;
};

/* ================= Sprint 2 · Cadastro da demanda ================= */
const LIMITE_PDF = 10 * 1024 * 1024;  // R6
// R1 a R6: devolve a lista de erros (vazia = válida)
function validarDemanda(d){
  const e = [];
  if (!["CUSTEIO", "INVESTIMENTO"].includes(d.grupo)) e.push("Escolha o grupo (custeio ou investimento).");
  if (!d.unidade_id) e.push("Escolha a unidade.");
  if ((d.especificacao_tecnica || "").trim().length < 50) e.push(`A especificação técnica precisa de pelo menos 50 caracteres (R1); tem ${(d.especificacao_tecnica || "").trim().length}.`);
  if ((d.justificativa || "").trim().length < 100) e.push(`A justificativa precisa de pelo menos 100 caracteres (R2); tem ${(d.justificativa || "").trim().length}.`);
  if (!(d.valor_unitario > 0)) e.push("O valor unitário precisa ser maior que zero (R3).");
  if (!(d.quantidade > 0)) e.push("A quantidade precisa ser maior que zero (R3).");
  if (!d.unidade_medida_id) e.push("Escolha a unidade de medida.");
  if (!(d.links_referencia || []).some(l=>/^https?:\/\//i.test(l))) e.push("Informe ao menos um link de referência começando com http (R5).");
  if (d.arquivo_pdf && d.arquivo_pdf.size > LIMITE_PDF) e.push("O PDF do orçamento passa de 10 MB (R6).");
  return e;
}
// R4: valor_global = valor_unitario × quantidade, em centavos para não perder centavo
const valorGlobal = (vu, qtd)=> dinheiro.vezes(qtd, dinheiro.de(vu)) / 100;
const qtdDe = v => { const s = String(v ?? "").trim().replace(/\./g, "").replace(",", "."); return s === "" ? NaN : Math.round(Number(s) * 1000) / 1000; };
teste("R4: 3 × R$ 33,33 = R$ 99,99", ()=> valorGlobal(33.33, 3) === 99.99);
teste("R2: justificativa de 99 caracteres é recusada", ()=> validarDemanda({justificativa: "x".repeat(99)}).some(e=>e.includes("R2")));
teste("R5: link sem http é recusado", ()=> validarDemanda({links_referencia: ["www.site.com"]}).some(e=>e.includes("R5")));

// R8: editar só o criador, ou ADM e DIRETOR
async function podeEditar(d){ return ["ADM", "DIRETOR"].includes(estado.perfil) || (d.criado_por && d.criado_por === (await db.meta("usuario"))); }

async function telaDemanda({id}){
  const d = id ? await db.get("banco_demandas", id) : null;
  if (id && !d) return `<div class="card vazio">Demanda não encontrada. <a href="#/banco">Voltar</a></div>`;
  if (d && !(await podeEditar(d))) return `<h1>Editar demanda</h1><div class="card pendente">Só o autor (${esc(d.criado_por)}), o ADM ou o diretor editam esta demanda (R8).
    <a href="#/demanda/${encodeURIComponent(d.id)}/ver">Ver a ficha</a></div>`;
  const unidades = await db.list("unidades"), medidas = await db.list("unidades_medida");
  const usuario = await db.meta("usuario"), unidadeCopia = await db.meta("unidade_id");
  const v = d || {grupo: "CUSTEIO", unidade_id: unidadeCopia || "", links_referencia: [""]};
  const reais = x => x ? dinheiro.fmt(Math.round(x * 100)).replace("R$ ", "") : "";
  return `<h1>${d ? "Editar demanda" : "Nova demanda"}</h1>
    ${usuario ? "" : `<div class="card pendente">Informe o seu usuário em <a href="#/config">Configuração</a>; ele fica registrado como autor da demanda.</div>`}
    <form class="card" id="formDemanda"><div class="campos">
      ${campo("dGrupo", "Grupo", {tipo: "select", opcoes: [["CUSTEIO", "Custeio"], ["INVESTIMENTO", "Investimento"]], valor: v.grupo, obrigatorio: true})}
      ${campo("dUnidade", "Unidade", {tipo: "select", opcoes: [["", "Escolha"], ...unidades.map(u=>[u.id, u.nome])], valor: v.unidade_id, obrigatorio: true})}
      ${campo("dValor", "Valor unitário (R$)", {valor: reais(v.valor_unitario), obrigatorio: true, attrs: 'inputmode="decimal" placeholder="0,00"'})}
      ${campo("dQtd", "Quantidade", {valor: v.quantidade ?? "", obrigatorio: true, attrs: 'inputmode="decimal"'})}
      ${campo("dMedida", "Unidade de medida", {tipo: "select", opcoes: [["", "Escolha"], ...medidas.map(m=>[m.id, `${m.sigla} · ${m.nome}`])], valor: v.unidade_medida_id || "", obrigatorio: true})}
      <div class="campo"><label>Valor global (R4)</label><p class="kpi"><span class="v" id="dGlobal">${dinheiro.fmt(Math.round((v.valor_global || 0) * 100))}</span></p></div>
    </div>
    ${campo("dEspec", "Especificação técnica", {tipo: "textarea", valor: v.especificacao_tecnica || "", obrigatorio: true, ajuda: "Mínimo de 50 caracteres (R1)."})}
    <p class="sub" id="contEspec"></p>
    ${campo("dJust", "Justificativa", {tipo: "textarea", valor: v.justificativa || "", obrigatorio: true, ajuda: "Mínimo de 100 caracteres (R2)."})}
    <p class="sub" id="contJust"></p>
    ${campo("dLinks", "Links de referência (um por linha)", {tipo: "textarea", linhas: 3, valor: (v.links_referencia || []).join("\n"), obrigatorio: true, ajuda: "Pelo menos um, começando com http (R5)."})}
    ${campo("dTitulo", "Título do primeiro link (opcional)", {valor: v.preview_title || "", ajuda: "Sem internet, o app não busca o título da página; escreva aqui."})}
    <div class="campo"><label for="dPdf">PDF do orçamento (opcional, até 10 MB)</label><input type="file" id="dPdf" accept="application/pdf">
      ${v.arquivo_pdf ? `<small class="sub">Atual: ${esc(v.arquivo_pdf_nome || "orçamento.pdf")} <label style="display:inline"><input type="checkbox" id="dRemoverPdf" style="width:auto"> remover</label></small>` : ""}</div>
    <div id="errosDemanda"></div>
    <div class="linha-botoes"><button class="prim" type="submit">Salvar demanda</button>
      ${d ? `<button type="button" class="perigo" id="btnExcluirDemanda">Excluir</button>` : ""}<a class="botao" href="#/banco">Cancelar</a></div></form>`;
}
TELAS["#/demanda/nova"] = ()=>telaDemanda({});
TELAS["#/demanda/:id"] = telaDemanda;

function ligarDemanda({id}){
  const form = $("#formDemanda"); if (!form) return;
  const atualizar = ()=>{
    const vu = dinheiro.de(valorDe("dValor")), q = qtdDe(valorDe("dQtd"));
    $("#dGlobal").textContent = vu > 0 && q > 0 ? dinheiro.fmt(dinheiro.vezes(q, vu)) : "R$ 0,00";
    const ce = valorDe("dEspec").length, cj = valorDe("dJust").length;
    $("#contEspec").innerHTML = `<span class="${ce >= 50 ? "ok-txt" : "erro-txt"}">${ce} de 50 caracteres</span>`;
    $("#contJust").innerHTML = `<span class="${cj >= 100 ? "ok-txt" : "erro-txt"}">${cj} de 100 caracteres</span>`;
  };
  ["dValor", "dQtd", "dEspec", "dJust"].forEach(i=>$("#" + i).addEventListener("input", atualizar)); atualizar();
  form.addEventListener("submit", async e=>{
    e.preventDefault();
    const antes = id ? await db.get("banco_demandas", id) : null;
    const pdf = $("#dPdf").files[0] || null, remover = $("#dRemoverPdf")?.checked;
    const vu = dinheiro.de(valorDe("dValor")), q = qtdDe(valorDe("dQtd"));
    const d = {grupo: valorDe("dGrupo"), unidade_id: valorDe("dUnidade"), especificacao_tecnica: valorDe("dEspec"), justificativa: valorDe("dJust"),
      valor_unitario: vu > 0 ? vu / 100 : 0, quantidade: q > 0 ? q : 0, unidade_medida_id: valorDe("dMedida"),
      links_referencia: valorDe("dLinks").split("\n").map(s=>s.trim()).filter(Boolean), preview_title: valorDe("dTitulo"),
      arquivo_pdf: pdf || (remover ? null : antes?.arquivo_pdf || null), arquivo_pdf_nome: pdf ? pdf.name : (remover ? null : antes?.arquivo_pdf_nome || null)};
    if (pdf && pdf.type && pdf.type !== "application/pdf") return mostrarErros("#errosDemanda", ["O anexo precisa ser um PDF."]);
    if (!mostrarErros("#errosDemanda", validarDemanda(d))) return;
    d.valor_global = dinheiro.vezes(d.quantidade, vu) / 100;
    const unidade = await db.get("unidades", d.unidade_id), t = agora();
    const reg = antes ? {...antes, ...d, updated_at: t}
      : {id: uuid(), ...d, criado_por: (await db.meta("usuario")) || estado.perfil, diretoria_id: unidade?.diretoria_id || null, orgao_id: unidade?.orgao_id || null, created_at: t, updated_at: t};
    await db.put("banco_demandas", reg); await registrar(antes ? "demanda alterada" : "demanda criada", {detalhe: reg.id});
    toast("Demanda salva."); location.hash = "#/banco";
  });
  $("#btnExcluirDemanda")?.addEventListener("click", async ()=>{
    if (!confirm("Excluir esta demanda e as manifestações de interesse dela?")) return;
    for (const m of await db.porIndice("banco_demanda_manifestacoes", "banco_demanda_id", id)) await db.del("banco_demanda_manifestacoes", m.id);
    await db.del("banco_demandas", id); await registrar("demanda excluída", {detalhe: id});
    toast("Demanda excluída."); location.hash = "#/banco";
  });
}
TELAS_DEPOIS["#/demanda/nova"] = ()=>ligarDemanda({});
TELAS_DEPOIS["#/demanda/:id"] = ligarDemanda;
