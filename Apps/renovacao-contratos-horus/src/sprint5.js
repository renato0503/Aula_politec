/* ================= Sprint 5 · Fiscais, avisos, edição e importação ================= */
const RC_ALERTA_FAIXAS = ["atencao", "providencias", "urgente", "vencido"];

async function rcAvisarContrato(id){
  const c = await db.get("contratos", id);
  if (!c) return toast("Contrato não encontrado.");
  const fiscais = await rcFiscais(id);
  const f = fiscais.find(x=> !x.ate && (x.papel || "fiscal") === "fiscal") || fiscais.find(x=> !x.ate);
  if (!f) return toast("Cadastre o fiscal do contrato antes de avisar.");
  const dias = rcDias(c.data_fim), faixa = rcFaixa(c);
  const texto = `Contrato ${c.numero} (${c.fornecedor}) vence em ${dias} dia(s), em ${dataCurtaBR(c.data_fim)}. ${faixa?.rotulo || ""}. Providencie a renovação.`;
  await db.put("avisos", {id: uuid(), contrato_id: id, para: f.nome, email: f.email || "", telefone: f.telefone || "", texto,
    canal: "fila local", criado_em: agora(), lido_em: null});
  await rcAuditar(id, "aviso de vencimento", `${f.nome} · ${faixa?.rotulo || "sem faixa"}`);
  await registrar("aviso de vencimento registrado", {detalhe: `${c.numero} · ${f.nome}`});
  toast("Aviso registrado na fila local. O envio real usa MailApp/Apps Script (Ajuda Técnica).");
  navegar();
}

function rcAvisoBtn(c){
  const f = rcFaixa(c);
  return f && RC_ALERTA_FAIXAS.includes(f.id) ? `<button type="button" class="sec" data-rc-aviso="${esc(c.id_contrato)}">Avisar o fiscal</button>` : "";
}

/* ---------- ficha: edição e avisos ---------- */
const rcFichaS4 = TELAS["#/contrato/:id"];
TELAS["#/contrato/:id"] = async (p)=>{
  const html = await rcFichaS4(p);
  const c = await db.get("contratos", p.id);
  if (!c) return html;
  const podeEditar = ["admin", "gestor"].includes(estado.perfil);
  const fiscais = await rcFiscais(p.id), avisos = (await db.porIndice("avisos", "contrato_id", p.id)).sort((a, b)=>String(b.criado_em).localeCompare(String(a.criado_em)));
  const fAtual = fiscais.find(x=> !x.ate && (x.papel || "fiscal") === "fiscal") || fiscais.find(x=> !x.ate);
  const edit = podeEditar ? `<div class="card" id="rcEditar"><h2 style="margin-top:0">Editar contrato</h2>
    <p class="sub">Somente ADM e gestor. A alteração fica na auditoria.</p>
    <div class="campos">${campo("rcEdFornecedor", "Fornecedor", {valor: c.fornecedor})}${campo("rcEdCnpj", "CNPJ", {valor: c.cnpj})}
      ${campo("rcEdValor", "Valor (R$)", {tipo: "number", valor: (Number(c.valor_c || 0) / 100).toFixed(2), attrs: 'min="0" step="0.01"'})}
      ${campo("rcEdFim", "Término", {tipo: "date", valor: c.data_fim})}${campo("rcEdStatus", "Situação", {tipo: "select", opcoes: [["Vigente", "Vigente"], ["Encerrado", "Encerrado"], ["Rescindido", "Rescindido"], ["Expirado", "Expirado"]], valor: c.status})}
      ${campo("rcEdAlerta", "Alerta (dias)", {tipo: "number", valor: c.alerta_dias || 90, attrs: 'min="1" step="1"'})}</div>
    ${campo("rcEdObjeto", "Objeto", {tipo: "textarea", linhas: 2, valor: c.objeto || ""})}
    <div id="rcEdErros"></div><div class="linha-botoes"><button type="button" class="prim" id="btnRcEditar">Salvar alterações</button></div></div>` : "";
  const aviso = `<div class="card" id="rcAvisos"><h2 style="margin-top:0">Avisos de vencimento</h2>
    <p class="sub">Fila local; nada sai do navegador. O passo a passo de MailApp/Apps Script fica na Ajuda Técnica (três cliques no nome do app no rodapé).</p>
    ${fAtual ? `<p>Fiscal atual: <b>${esc(fAtual.nome)}</b>${fAtual.email ? ` · ${esc(fAtual.email)}` : ""}${fAtual.telefone ? ` · ${esc(fAtual.telefone)}` : ""}</p>` : '<p class="alerta-txt">Nenhum fiscal atual cadastrado.</p>'}
    ${rcAvisoBtn(c)}
    <ul class="check-lista">${avisos.map(a=>`<li class="${a.lido_em ? "feito" : "falta"}">${icone(a.lido_em ? "check" : "alerta")}
      <span><b>${esc(a.para)}</b> · ${dataBR(a.criado_em)} · ${esc(a.texto)}${a.lido_em ? ` · <span class="selo ok">lido</span>` : ` · <button type="button" data-rc-lido="${esc(a.id)}">Marcar como lido</button>`}</span></li>`).join("") || '<li class="vazio">Nenhum aviso registrado.</li>'}</ul></div>`;
  return html + edit + aviso;
};

const rcFichaDepoisS4 = TELAS_DEPOIS["#/contrato/:id"];
TELAS_DEPOIS["#/contrato/:id"] = async (p)=>{
  await rcFichaDepoisS4?.(p);
  $("#btnRcEditar")?.addEventListener("click", async ()=>{
    const c = await db.get("contratos", p.id);
    const fornecedor = valorDe("rcEdFornecedor"), cnpj = valorDe("rcEdCnpj").replace(/\D/g, ""), fim = valorDe("rcEdFim"), objeto = valorDe("rcEdObjeto");
    const erros = [];
    if (!fornecedor) erros.push("Informe o fornecedor.");
    if (!cnpjValido(cnpj)) erros.push("CNPJ inválido.");
    if (!fim) erros.push("Informe o término.");
    if (!objeto) erros.push("Informe o objeto.");
    if (!mostrarErros("#rcEdErros", erros)) return;
    await db.put("contratos", {...c, fornecedor, cnpj, valor_c: Math.round(Number(valorDe("rcEdValor") || 0) * 100), data_fim: fim,
      status: valorDe("rcEdStatus"), alerta_dias: Number(valorDe("rcEdAlerta") || 90), objeto});
    await rcAuditar(p.id, "contrato editado", `${fornecedor} · término ${fim}`);
    await registrar("contrato editado", {detalhe: c.numero});
    toast("Contrato atualizado."); navegar();
  });
  $$("[data-rc-aviso]").forEach(b=>b.addEventListener("click", ()=>rcAvisarContrato(b.dataset.rcAviso)));
  $$("[data-rc-lido]").forEach(b=>b.addEventListener("click", async ()=>{
    const a = await db.get("avisos", b.dataset.rcLido);
    await db.put("avisos", {...a, lido_em: agora()});
    await rcAuditar(a.contrato_id, "aviso marcado como lido", a.para);
    toast("Aviso marcado como lido."); navegar();
  }));
};

/* ---------- painel: avisos de vencimento ---------- */
const rcPainelS4 = TELAS["#/painel"];
TELAS["#/painel"] = async ()=>{
  const html = await rcPainelS4();
  const cs = await db.list("contratos"), avisos = await db.list("avisos");
  const alerta = cs.filter(c=> { const f = rcFaixa(c); return f && RC_ALERTA_FAIXAS.includes(f.id); }).sort((a, b)=>String(a.data_fim).localeCompare(String(b.data_fim)));
  return html + `<div class="card tabela-wrap" id="rcPainelAvisos"><h2 style="margin-top:0">Avisos de vencimento</h2>
    <p class="sub">Contratos em atenção, providências, urgente ou vencidos. O aviso entra na fila local; o envio real usa MailApp/Apps Script.</p>
    <table><thead><tr><th>Contrato</th><th>Fornecedor</th><th>Término</th><th class="num">Dias</th><th>Faixa</th><th></th></tr></thead><tbody>
    ${alerta.map(c=>{ const f = rcFaixa(c); return `<tr><td><a href="#/contrato/${encodeURIComponent(c.id_contrato)}">${esc(c.numero)}</a></td><td>${esc(c.fornecedor)}</td>
      <td>${dataCurtaBR(c.data_fim)}</td><td class="num">${rcDias(c.data_fim)}</td><td><span class="selo ${f.selo}">${esc(f.rotulo.split(" (")[0])}</span></td>
      <td>${rcAvisoBtn(c)}</td></tr>`; }).join("") || '<tr><td colspan="6" class="vazio">Nenhum contrato em alerta.</td></tr>'}
    </tbody></table><p class="sub">${avisos.length} aviso(s) na fila · ${avisos.filter(a=>!a.lido_em).length} não lido(s).</p></div>`;
};
const rcPainelDepoisS4 = TELAS_DEPOIS["#/painel"];
TELAS_DEPOIS["#/painel"] = async ()=>{
  await rcPainelDepoisS4?.();
  $$("[data-rc-aviso]").forEach(b=>b.addEventListener("click", ()=>rcAvisarContrato(b.dataset.rcAviso)));
};

/* ---------- importação da planilha do setor ---------- */
const rcContratosAntes = TELAS["#/contratos"];
TELAS["#/contratos"] = async (p)=> (await rcContratosAntes(p)) + `<div class="card" id="rcImportar"><h2 style="margin-top:0">Importar a planilha do setor</h2>
  <p class="sub">Aceita .xlsx, .xls ou .csv. Colunas esperadas: numero, fornecedor, cnpj, valor, data_inicio, data_fim, objeto, status (as demais são opcionais). Contratos com o mesmo número são atualizados.</p>
  <label class="botao">Escolher a planilha<input type="file" id="rcArquivoPlanilha" accept=".xlsx,.xls,.csv" hidden></label>
  <div id="rcImportRes"></div></div>`;
const rcContratosDepois = TELAS_DEPOIS["#/contratos"];
TELAS_DEPOIS["#/contratos"] = (p)=>{
  rcContratosDepois?.(p);
  $("#rcArquivoPlanilha")?.addEventListener("change", async e=>{
    const f = e.target.files[0]; if (!f) return;
    try {
      const buf = new Uint8Array(await lerArrayBuffer(f));
      const texto = new TextDecoder().decode(buf);
      const wb = /\.csv$/i.test(f.name) ? XLSX.read(texto, {type: "string", FS: texto.includes(";") ? ";" : ","}) : XLSX.read(buf, {type: "array"});
      const linhas = XLSX.utils.sheet_to_json(wb.Sheets[wb.SheetNames[0]], {defval: ""});
      if (!linhas.length) throw new Error("A planilha está vazia.");
      const cs = await db.list("contratos"); let criados = 0, atualizados = 0, ignorados = 0;
      for (const l of linhas) {
        const get = (nomes)=> { for (const n of nomes) { const k = Object.keys(l).find(k=>normalizar(k) === normalizar(n)); if (k) return String(l[k]).trim(); } return ""; };
        const numero = get(["numero", "contrato", "numero_contrato"]);
        if (!numero) { ignorados++; continue; }
        const inicio = get(["data_inicio", "inicio"]) || hojeISO();
        const fim = get(["data_fim", "termino", "fim"]) || rcFim(inicio, 12);
        const existente = cs.find(c=>normalizar(c.numero) === normalizar(numero));
        const id = existente?.id_contrato || "CT-" + String(cs.length + criados + 1).padStart(3, "0");
        const d = {numero, fornecedor: get(["fornecedor", "empresa"]), cnpj: get(["cnpj"]).replace(/\D/g, ""), valor_c: Math.round(Number(get(["valor", "valor_contrato"]).replace(/[^\d,.]/g, "").replace(".", "").replace(",", ".")) * 100) || 0,
          data_inicio: inicio, data_fim: fim, objeto: get(["objeto", "descricao"]), status: get(["status", "situacao"]) || "Vigente",
          permite_prorrogacao: /sim|true|1/i.test(get(["permite_prorrogacao", "prorrogacao"]) || "sim"), alerta_dias: Number(get(["alerta_dias", "alerta"])) || 90};
        await db.put("contratos", {...(existente || {}), id_contrato: id, ...d, atualizado_em: agora()});
        existente ? atualizados++ : criados++;
      }
      $("#rcImportRes").innerHTML = `<p class="ok-txt">Importação concluída: ${criados} criado(s), ${atualizados} atualizado(s), ${ignorados} sem número.</p>`;
      await registrar("planilha de contratos importada", {detalhe: `${f.name}: ${criados} criados, ${atualizados} atualizados`});
      toast("Planilha importada.");
    } catch(err){ $("#rcImportRes").innerHTML = `<p class="erro-txt">Não consegui importar: ${esc(err.message)}</p>`; }
  });
};
