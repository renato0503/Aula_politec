/* Banco de Demandas · código do app (o construir.py junta com a base comum) */
"use strict";
/* ================= Catálogo: unidades (setores) e unidades de medida ================= */
/* A nova demanda exige unidade e unidade de medida; sem catálogo ela não salva. */
function validarUnidade(u, todas = []){
  const e = [], nome = String(u.nome || "").trim(), sigla = String(u.sigla || "").trim();
  if (!nome) e.push("Informe o nome da unidade (setor).");
  if (!sigla) e.push("Informe a sigla da unidade.");
  const repetida = sigla && todas.find(o => o.id !== u.id && String(o.sigla || "").trim().toUpperCase() === sigla.toUpperCase());
  if (repetida) e.push(`A sigla ${sigla} já é da unidade "${repetida.nome}".`);
  return e;
}
function validarMedida(m, todas = []){
  const e = [], sigla = String(m.sigla || "").trim(), nome = String(m.nome || "").trim();
  if (!sigla) e.push("Informe a sigla da unidade de medida (un, kg, L...).");
  if (!nome) e.push("Informe o nome da unidade de medida.");
  const repetida = sigla && todas.find(o => o.id !== m.id && String(o.sigla || "").trim().toUpperCase() === sigla.toUpperCase());
  if (repetida) e.push(`A sigla ${sigla} já é da unidade de medida "${repetida.nome}".`);
  return e;
}
// Quantos registros usam o item do catálogo: impede excluir o que está em uso.
async function usoNoCatalogo(store, id){
  if (store === "unidades"){
    const [ds, ms, is] = await Promise.all([db.list("banco_demandas"), db.list("banco_demanda_manifestacoes"), db.list("banco_demanda_inclusoes")]);
    return ds.filter(x=>x.unidade_id === id).length + ms.filter(x=>x.unidade_id === id).length + is.filter(x=>x.unidade_id === id).length;
  }
  return (await db.list("banco_demandas")).filter(x=>x.unidade_medida_id === id).length;
}
teste("Catálogo: unidade exige nome e sigla", ()=> validarUnidade({nome: "", sigla: ""}, []).length === 2);
teste("Catálogo: sigla de unidade repetida é recusada", ()=> validarUnidade({id: "b", nome: "Setor B", sigla: "lqf"}, [{id: "a", nome: "Setor A", sigla: "LQF"}]).length === 1);
teste("Catálogo: unidade de medida exige sigla e nome", ()=> validarMedida({sigla: "", nome: ""}, []).length === 2);
teste("Catálogo: não exclui unidade em uso", async ()=>{
  await db.put("unidades", {id: "uCat", nome: "Unidade de teste", sigla: "TST"});
  await db.put("banco_demandas", {id: "dCat", unidade_id: "uCat", unidade_medida_id: "mCat", grupo: "CUSTEIO", especificacao_tecnica: "teste"});
  const uso = await usoNoCatalogo("unidades", "uCat");
  await db.del("banco_demandas", "dCat"); await db.del("unidades", "uCat");
  return uso === 1;
});

async function blocoUnidades(){
  const [unidades, diretorias, orgaos] = await Promise.all([db.list("unidades"), db.list("diretorias"), db.list("orgaos")]);
  const dir = Object.fromEntries(diretorias.map(d=>[d.id, d])), org = Object.fromEntries(orgaos.map(o=>[o.id, o]));
  const lista = [...unidades].sort((a, b)=>String(a.nome).localeCompare(String(b.nome), "pt-BR"));
  return `<div class="card" id="blocoUnidades"><h2 style="margin-top:0">Unidades (setores)</h2>
    <p class="sub">O setor a que a demanda pertence. É obrigatório na nova demanda: sem ao menos uma unidade cadastrada, não é possível salvar.</p>
    ${lista.length ? `<div class="tabela-wrap"><table>
      <tr><th>Sigla</th><th>Nome</th><th>Diretoria</th><th>Órgão</th><th>Ações</th></tr>
      ${lista.map(u=>`<tr><td class="mono">${esc(u.sigla || "—")}</td><td>${esc(u.nome)}</td>
        <td>${esc(dir[u.diretoria_id]?.nome || "—")}</td><td>${esc(org[u.orgao_id]?.nome || "—")}</td>
        <td><button type="button" data-editar-unidade="${esc(u.id)}">Editar</button>
        <button type="button" class="perigo" data-excluir-unidade="${esc(u.id)}">Excluir</button></td></tr>`).join("")}</table></div>`
      : `<p class="sub"><b>Nenhuma unidade cadastrada ainda.</b> Cadastre a primeira no formulário abaixo.</p>`}
    <form id="formUnidade" style="margin-top:14px"><input type="hidden" id="uId" value="">
      <div class="campos">
        ${campo("uNome", "Nome da unidade (setor)", {obrigatorio: true, attrs: 'placeholder="Ex.: Laboratório de Química Forense"'})}
        ${campo("uSigla", "Sigla", {obrigatorio: true, attrs: 'placeholder="Ex.: LQF" maxlength="12"'})}
        ${campo("uDiretoria", "Diretoria (opcional)", {tipo: "select", opcoes: [["", "Sem diretoria"], ...diretorias.map(d=>[d.id, `${d.sigla ? d.sigla + " · " : ""}${d.nome}`])]})}
        ${campo("uOrgao", "Órgão (opcional)", {tipo: "select", opcoes: [["", "Sem órgão"], ...orgaos.map(o=>[o.id, o.nome])]})}
      </div>
      <div id="errosUnidade"></div>
      <div class="linha-botoes"><button class="prim" type="submit" id="btnUnidade">Cadastrar unidade</button>
        <button type="button" id="btnCancelarUnidade" hidden>Cancelar edição</button></div>
    </form></div>`;
}

async function blocoMedidas(){
  const medidas = await db.list("unidades_medida");
  const lista = [...medidas].sort((a, b)=>String(a.sigla).localeCompare(String(b.sigla), "pt-BR"));
  return `<div class="card" id="blocoMedidas"><h2 style="margin-top:0">Unidades de medida</h2>
    <p class="sub">Como a quantidade é contada: un, lic, kg, L, m²... É obrigatória na nova demanda.</p>
    ${lista.length ? `<div class="tabela-wrap"><table><tr><th>Sigla</th><th>Nome</th><th>Ações</th></tr>
      ${lista.map(m=>`<tr><td class="mono">${esc(m.sigla)}</td><td>${esc(m.nome)}</td>
        <td><button type="button" data-editar-medida="${esc(m.id)}">Editar</button>
        <button type="button" class="perigo" data-excluir-medida="${esc(m.id)}">Excluir</button></td></tr>`).join("")}</table></div>`
      : `<p class="sub"><b>Nenhuma unidade de medida cadastrada ainda.</b> Cadastre a primeira no formulário abaixo.</p>`}
    <form id="formMedida" style="margin-top:14px"><input type="hidden" id="mId" value="">
      <div class="campos">
        ${campo("mSigla", "Sigla", {obrigatorio: true, attrs: 'placeholder="Ex.: UN" maxlength="10"'})}
        ${campo("mNome", "Nome", {obrigatorio: true, attrs: 'placeholder="Ex.: unidade"'})}
      </div>
      <div id="errosMedida"></div>
      <div class="linha-botoes"><button class="prim" type="submit" id="btnMedida">Cadastrar unidade de medida</button>
        <button type="button" id="btnCancelarMedida" hidden>Cancelar edição</button></div>
    </form></div>`;
}

async function configExtra(){
  const unidades = await db.list("unidades"); const atual = await db.meta("unidade_id");
  return `<div class="card"><h2 style="margin-top:0">Unidade e usuário desta cópia</h2>
    <p class="sub">A unidade define de quem são as demandas criadas aqui. O usuário fica registrado como autor (criado_por).</p>
    <div class="campos">
    ${unidades.length ? campo("selUnidade", "Unidade", {tipo: "select", opcoes: [["", "Escolha"], ...unidades.map(u=>[u.id, u.nome])], valor: atual || ""})
      : `<p class="sub">Cadastre uma unidade no catálogo abaixo para escolher a desta cópia.</p>`}
    ${campo("cfgUsuario", "Seu usuário", {valor: (await db.meta("usuario")) || "", ajuda: "O mesmo login do Hórus, para a exportação bater."})}
    </div></div>
    ${await blocoUnidades()}
    ${await blocoMedidas()}`;
}

function preencherUnidade(u = {}){
  $("#uId").value = u.id || ""; $("#uNome").value = u.nome || ""; $("#uSigla").value = u.sigla || "";
  $("#uDiretoria").value = u.diretoria_id || ""; $("#uOrgao").value = u.orgao_id || "";
  $("#btnUnidade").textContent = u.id ? "Salvar alterações" : "Cadastrar unidade";
  $("#btnCancelarUnidade").hidden = !u.id; $("#errosUnidade").innerHTML = "";
  if (u.id) $("#uNome").focus();
}
function preencherMedida(m = {}){
  $("#mId").value = m.id || ""; $("#mSigla").value = m.sigla || ""; $("#mNome").value = m.nome || "";
  $("#btnMedida").textContent = m.id ? "Salvar alterações" : "Cadastrar unidade de medida";
  $("#btnCancelarMedida").hidden = !m.id; $("#errosMedida").innerHTML = "";
  if (m.id) $("#mSigla").focus();
}

async function ligarConfigExtra(){
  $("#selUnidade")?.addEventListener("change", async e=>{ await db.meta("unidade_id", e.target.value); await registrar("unidade da cópia", {detalhe: e.target.value}); toast("Unidade salva."); });
  $("#cfgUsuario")?.addEventListener("change", async e=>{ await db.meta("usuario", e.target.value.trim()); toast("Usuário salvo."); });

  /* catálogo de unidades (setores) */
  $("#formUnidade")?.addEventListener("submit", async ev=>{
    ev.preventDefault();
    const todas = await db.list("unidades"), id = valorDe("uId"), antes = id ? todas.find(u=>u.id === id) : null;
    const u = {id: id || uuid(), nome: valorDe("uNome"), sigla: valorDe("uSigla").toUpperCase(),
      diretoria_id: valorDe("uDiretoria") || null, orgao_id: valorDe("uOrgao") || null,
      created_at: antes?.created_at || agora(), updated_at: agora()};
    if (!mostrarErros("#errosUnidade", validarUnidade(u, todas))) return;
    await db.put("unidades", u);
    await registrar(antes ? "unidade alterada" : "unidade cadastrada", {detalhe: `${u.sigla} · ${u.nome}`});
    toast(antes ? "Unidade alterada." : "Unidade cadastrada."); navegar();
  });
  $("#btnCancelarUnidade")?.addEventListener("click", ()=>preencherUnidade());
  $$("[data-editar-unidade]").forEach(b=>b.addEventListener("click", async ()=>{
    const u = await db.get("unidades", b.dataset.editarUnidade); if (u) preencherUnidade(u);
  }));
  $$("[data-excluir-unidade]").forEach(b=>b.addEventListener("click", async ()=>{
    const id = b.dataset.excluirUnidade, u = await db.get("unidades", id); if (!u) return;
    const uso = await usoNoCatalogo("unidades", id);
    if (uso) return toast(`Não dá para excluir: ${uso} registro(s) usam esta unidade.`, 5000);
    if (!confirm(`Excluir a unidade "${u.nome}" do catálogo?`)) return;
    await db.del("unidades", id);
    if ((await db.meta("unidade_id")) === id) await db.meta("unidade_id", "");
    await registrar("unidade excluída", {detalhe: `${u.sigla} · ${u.nome}`});
    toast("Unidade excluída."); navegar();
  }));

  /* catálogo de unidades de medida */
  $("#formMedida")?.addEventListener("submit", async ev=>{
    ev.preventDefault();
    const todas = await db.list("unidades_medida"), id = valorDe("mId"), antes = id ? todas.find(m=>m.id === id) : null;
    const m = {id: id || uuid(), sigla: valorDe("mSigla").toUpperCase(), nome: valorDe("mNome"),
      created_at: antes?.created_at || agora(), updated_at: agora()};
    if (!mostrarErros("#errosMedida", validarMedida(m, todas))) return;
    await db.put("unidades_medida", m);
    await registrar(antes ? "unidade de medida alterada" : "unidade de medida cadastrada", {detalhe: `${m.sigla} · ${m.nome}`});
    toast(antes ? "Unidade de medida alterada." : "Unidade de medida cadastrada."); navegar();
  });
  $("#btnCancelarMedida")?.addEventListener("click", ()=>preencherMedida());
  $$("[data-editar-medida]").forEach(b=>b.addEventListener("click", async ()=>{
    const m = await db.get("unidades_medida", b.dataset.editarMedida); if (m) preencherMedida(m);
  }));
  $$("[data-excluir-medida]").forEach(b=>b.addEventListener("click", async ()=>{
    const id = b.dataset.excluirMedida, m = await db.get("unidades_medida", id); if (!m) return;
    const uso = await usoNoCatalogo("unidades_medida", id);
    if (uso) return toast(`Não dá para excluir: ${uso} demanda(s) usam esta unidade de medida.`, 5000);
    if (!confirm(`Excluir a unidade de medida "${m.sigla} · ${m.nome}" do catálogo?`)) return;
    await db.del("unidades_medida", id);
    await registrar("unidade de medida excluída", {detalhe: `${m.sigla} · ${m.nome}`});
    toast("Unidade de medida excluída."); navegar();
  }));
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
  const faltaCatalogo = [
    unidades.length ? "" : "nenhuma unidade (setor)",
    medidas.length ? "" : "nenhuma unidade de medida"
  ].filter(Boolean);
  return `<h1>${d ? "Editar demanda" : "Nova demanda"}</h1>
    ${usuario ? "" : `<div class="card pendente">Informe o seu usuário em <a href="#/config">Configuração</a>; ele fica registrado como autor da demanda.</div>`}
    ${faltaCatalogo.length ? `<div class="card pendente">O catálogo está incompleto: falta ${faltaCatalogo.join(" e ")}.
      Esses campos são obrigatórios, então a demanda não salva sem eles. <a href="#/config">Cadastrar em Configuração</a>.</div>` : ""}
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
