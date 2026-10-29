/* Segunda via da CIN · código do app (o construir.py junta com a base comum) */
"use strict";
teste("RN01: CPF de teste válido", ()=> cpfValido(dadosEmbutidos("seed").pedidos[0].cpf));
teste("RN01: CPF com dígito errado é recusado", ()=> !cpfValido("00000001029") && !cpfValido("11111111111"));
teste("Todos os CPFs do exemplo são válidos", ()=> dadosEmbutidos("seed").pedidos.every(p=>cpfValido(p.cpf)));

/* ================= Sprint 2 · Pedido do cidadão ================= */
const LINK_AGENDAMENTO = "../agendamento-cin/index.html#/agendar";
const fotosDoPedido = {rosto: null, documento: null};  // Blob reduzido (até 800 px)

// Foto de teste gerada no navegador: o MVP não usa foto de pessoa real (LGPD, art. 11).
function fotoDeTeste(tipo){
  return new Promise(ok=>{
    const cv = document.createElement("canvas"); cv.width = 600; cv.height = tipo === "rosto" ? 800 : 400;
    const g = cv.getContext("2d");
    g.fillStyle = tipo === "rosto" ? "#c9d6e8" : "#e8e2c9"; g.fillRect(0, 0, cv.width, cv.height);
    g.fillStyle = "#1c2430"; g.font = "bold 36px sans-serif"; g.textAlign = "center";
    g.fillText("FOTO DE TESTE", cv.width / 2, cv.height / 2 - 20);
    g.font = "24px sans-serif"; g.fillText(tipo === "rosto" ? "rosto (fictício)" : "documento (fictício)", cv.width / 2, cv.height / 2 + 24);
    cv.toBlob(ok, "image/jpeg", 0.8);
  });
}
// RN03: só segue a distância com a CIN válida e sem mudança de dados
const elegivel = (valida, mudou)=> valida === "sim" && mudou === "nao";
teste("RN03: CIN vencida não é elegível", ()=> !elegivel("nao", "nao") && !elegivel("sim", "sim") && elegivel("sim", "nao"));
function validarPedido(p, fotos){
  const e = [];
  if (p.nome.split(/\s+/).length < 2) e.push("Informe o nome completo.");
  if (!cpfValido(p.cpf)) e.push("CPF inválido (RN01).");
  if (!p.nascimento || p.nascimento > hojeISO()) e.push("Informe a data de nascimento.");
  if (!p.validade_cin) e.push("Informe a validade da CIN.");
  else if (p.validade_cin < hojeISO()) e.push("A CIN está vencida: o pedido é feito no posto (RN03).");
  if (!/^\S+@\S+\.\S+$/.test(p.contato) && p.contato.replace(/\D/g, "").length < 10) e.push("Informe um e-mail ou um telefone com DDD para contato.");
  if (!fotos.rosto) e.push("Falta a foto do rosto (RN02).");
  if (!fotos.documento) e.push("Falta a foto do documento (RN02).");
  return e;
}
const novoProtocolo = ()=> "2V-" + hojeISO().replace(/-/g, "") + "-" + Math.random().toString(16).slice(2, 6).toUpperCase();

TELAS["#/pedido"] = async ()=> `<h1>Pedir a segunda via da Carteira de Identidade</h1>
  <p class="sub">Sem ir ao posto, quando a primeira via ainda está válida e nenhum dado mudou.</p>
  <form class="card" id="formElegivel"><h2 style="margin-top:0">1. Antes de começar</h2>
    <fieldset style="border:0;padding:0"><legend>Sua Carteira de Identidade (primeira via) está dentro da validade?</legend>
      <label style="display:inline-flex;gap:6px;margin-right:16px"><input type="radio" name="valida" value="sim" style="width:auto"> Sim</label>
      <label style="display:inline-flex;gap:6px"><input type="radio" name="valida" value="nao" style="width:auto"> Não</label></fieldset>
    <fieldset style="border:0;padding:0;margin-top:10px"><legend>Algum dado mudou desde a emissão (nome, estado civil, filiação)?</legend>
      <label style="display:inline-flex;gap:6px;margin-right:16px"><input type="radio" name="mudou" value="sim" style="width:auto"> Sim</label>
      <label style="display:inline-flex;gap:6px"><input type="radio" name="mudou" value="nao" style="width:auto"> Não</label></fieldset>
    <div class="linha-botoes"><button class="prim" type="submit">Continuar</button></div></form>
  <div id="naoElegivel"></div><div id="etapaDados"></div>`;

function formDados(){
  return `<form class="card" id="formPedido"><h2 style="margin-top:0">2. Seus dados</h2><div class="campos">
      ${campo("cNome", "Nome completo", {obrigatorio: true, attrs: 'autocomplete="name"'})}
      ${campo("cCpf", "CPF (é o número da CIN)", {obrigatorio: true, attrs: 'inputmode="numeric" autocomplete="off" placeholder="000.000.000-00"'})}
      ${campo("cNasc", "Data de nascimento", {tipo: "date", obrigatorio: true})}
      ${campo("cValidade", "Validade da CIN", {tipo: "date", obrigatorio: true})}
      ${campo("cContato", "E-mail ou telefone para contato", {obrigatorio: true})}</div>
    <h2>3. Fotos</h2><p class="sub">Protótipo: use as fotos de teste. Não envie fotos reais.</p>
    <div class="grade">${["rosto", "documento"].map(t=>`<div class="card"><b>${t === "rosto" ? "Foto do rosto" : "Foto do documento"}</b>
      <div id="prev-${t}" style="margin:8px 0;min-height:60px" class="sub">Sem foto.</div>
      <label class="botao">Tirar ou escolher foto<input type="file" accept="image/*" capture="${t === "rosto" ? "user" : "environment"}" data-foto="${t}" hidden></label>
      <button type="button" data-teste="${t}">Usar foto de teste</button></div>`).join("")}</div>
    <div id="errosPedido"></div>
    <div class="linha-botoes"><button class="prim" type="submit">Enviar pedido</button></div></form>`;
}
async function definirFoto(tipo, blob){
  fotosDoPedido[tipo] = await reduzirImagem(blob, 800, 0.8);
  $(`#prev-${tipo}`).innerHTML = `<img src="${URL.createObjectURL(fotosDoPedido[tipo])}" alt="Foto do ${tipo}" style="max-width:120px;border-radius:6px">
    <br><small>${(fotosDoPedido[tipo].size / 1024).toFixed(0)} KB</small>`;
}
TELAS_DEPOIS["#/pedido"] = ()=>{
  fotosDoPedido.rosto = fotosDoPedido.documento = null;
  $("#formElegivel").addEventListener("submit", e=>{
    e.preventDefault();
    const valida = $("input[name=valida]:checked")?.value, mudou = $("input[name=mudou]:checked")?.value;
    if (!valida || !mudou) return toast("Responda às duas perguntas.");
    if (!elegivel(valida, mudou)){
      $("#etapaDados").innerHTML = "";
      $("#naoElegivel").innerHTML = `<div class="card pendente" id="avisoPosto"><h2 style="margin-top:0">Este pedido é feito no posto</h2>
        <p>${valida === "nao" ? "Com a CIN vencida" : "Com mudança de dados"}, a segunda via precisa de nova coleta no posto de identificação.</p>
        <a class="botao prim" href="${LINK_AGENDAMENTO}">Agendar atendimento no posto</a></div>`;
      return;
    }
    $("#naoElegivel").innerHTML = ""; $("#etapaDados").innerHTML = formDados(); ligarPedido();
  });
};
function ligarPedido(){
  $$("[data-foto]").forEach(inp=>inp.addEventListener("change", async e=>{
    const f = e.target.files[0]; if (!f) return;
    try { await definirFoto(e.target.dataset.foto, f); } catch(err){ toast(err.message); }
  }));
  $$("[data-teste]").forEach(b=>b.addEventListener("click", async ()=>definirFoto(b.dataset.teste, await fotoDeTeste(b.dataset.teste))));
  $("#formPedido").addEventListener("submit", async e=>{
    e.preventDefault();
    const p = {nome: valorDe("cNome"), cpf: valorDe("cCpf").replace(/\D/g, ""), nascimento: valorDe("cNasc"), validade_cin: valorDe("cValidade"), contato: valorDe("cContato")};
    if (!mostrarErros("#errosPedido", validarPedido(p, fotosDoPedido))) return;
    const protocolo = novoProtocolo();
    await db.put("pedidos", {protocolo, ...p, numero_cin: p.cpf, mudou_dados: false, criado_em: agora(), situacao: "recebido", motivo: ""});
    for (const t of ["rosto", "documento"]) await db.put("fotos", {id: `${protocolo}-${t}`, protocolo, tipo: t, conteudo: fotosDoPedido[t]});
    await registrar("pedido enviado", {protocolo});
    $("#etapaDados").innerHTML = `<div class="card" id="protocoloGerado"><h2 style="margin-top:0">Pedido recebido</h2>
      <p>Protocolo: <b class="mono" id="numProtocolo">${protocolo}</b></p><p>Guarde o número. O servidor confere o pedido e a situação aparece no protocolo.</p>
      <a class="botao" href="#/protocolo/${encodeURIComponent(protocolo)}">Acompanhar o pedido</a></div>`;
    $("#formElegivel").remove();
  });
}
