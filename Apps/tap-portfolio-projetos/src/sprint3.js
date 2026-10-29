/* ================= Sprint 3 · Pacote e triagem (RN05, RN06) ================= */
function fnvTap(txt){ let h = 0x811c9dc5; for (const b of new TextEncoder().encode(txt)){ h ^= b; h = Math.imul(h, 0x01000193) >>> 0; } return h.toString(16).padStart(8, "0"); }
const blobParaB64 = b => new Promise((ok, erro)=>{ const r = new FileReader(); r.onload = ()=>ok(String(r.result).split(",")[1]); r.onerror = erro; r.readAsDataURL(b); });
const b64ParaBlob = (b64, mime)=> new Blob([Uint8Array.from(atob(b64), c=>c.charCodeAt(0))], {type: mime || "application/octet-stream"});
// pacote = {formato, conteudo, verificacao}; verificacao = fnv1a do conteúdo em JSON (detecta arquivo alterado ou cortado)
const embalar = (formato, conteudo)=>{ const s = JSON.stringify(conteudo); return JSON.stringify({formato, conteudo, verificacao: fnvTap(s)}); };
function desembalar(texto, formato){
  let p; try { p = JSON.parse(texto); } catch(e){ throw new Error("O arquivo não é um pacote do TAP Digital."); }
  if (p.formato !== formato) throw new Error(`Este arquivo não é ${formato === "TAP-v1" ? "um pacote de proposta" : "uma devolução"}.`);
  if (fnvTap(JSON.stringify(p.conteudo)) !== p.verificacao) throw new Error("O código de verificação não confere: o arquivo foi alterado ou está incompleto.");
  return p.conteudo;
}
teste("pacote alterado é recusado", ()=>{ const t = embalar("TAP-v1", {a: 1}); try { desembalar(t.replace('"a":1', '"a":2'), "TAP-v1"); return false; } catch(e){ return true; } });

async function gerarPacote(id){
  const p = await db.get("propostas", id), anexos = await db.porIndice("anexos", "proposta_id", id);
  const conteudo = {proposta: {...p, status: "enviado"}, anexos: await Promise.all(anexos.map(async a=>({tipo: a.tipo, nome: a.nome, mime: a.mime, tamanho: a.tamanho, base64: await blobParaB64(a.conteudo)})))};
  await db.put("propostas", {...p, status: "enviado", enviado_em: agora()}); await registrar("pacote gerado", {proposta_id: id});
  baixar(`proposta-${id}.json`, embalar("TAP-v1", conteudo), "application/json");
}

TELAS["#/minhas"] = async ()=>{
  const ps = (await db.list("propostas")).sort((a, b)=>(b.criado_em || "").localeCompare(a.criado_em || ""));
  const pend = await db.list("pendencias");
  return `<h1>Minhas propostas</h1><p class="sub"><a href="#/tap/novo">Novo TAP</a> · O pacote vai pelo SEI ou e-mail para a equipe de projetos.</p>
    <div class="card"><label class="botao">Importar devolução da equipe<input type="file" id="arqDevolucao" accept=".json" hidden></label><div id="errosDevolucao"></div></div>
    <div class="card tabela-wrap"><table id="tabelaMinhas"><tr><th>TAP</th><th>Título</th><th>Situação</th><th>Pendências</th><th></th></tr>
      ${ps.map(p=>{ const abertas = pend.filter(x=>x.proposta_id === p.id && !x.resolvida_em); return `<tr data-id="${esc(p.id)}"><td>${esc(p.id)}</td><td>${esc(p.titulo || "(sem título)")}</td>
        <td><span class="selo ${p.status === "devolvida" ? "erro" : "info"}">${esc(p.status)}</span></td><td>${abertas.map(x=>esc(x.motivo)).join("<br>") || "—"}</td>
        <td>${["pronto para envio", "enviado"].includes(p.status) ? `<button data-pacote="${esc(p.id)}">${p.status === "enviado" ? "Gerar de novo" : "Gerar pacote"}</button>` : ""}
          ${p.status === "devolvida" ? `<button data-corrigir="${esc(p.id)}">Corrigir</button>` : ""}</td></tr>`; }).join("") || '<tr><td colspan="5" class="vazio">Nenhuma proposta.</td></tr>'}</table></div>`;
};
TELAS_DEPOIS["#/minhas"] = ()=>{
  $$("[data-pacote]").forEach(b=>b.addEventListener("click", async ()=>{ await gerarPacote(b.dataset.pacote); toast("Pacote gerado. Envie o arquivo pelo SEI ou e-mail."); navegar(); }));
  $$("[data-corrigir]").forEach(b=>b.addEventListener("click", async ()=>{
    const p = await db.get("propostas", b.dataset.corrigir); await db.put("propostas", {...p, status: "rascunho"}); await db.meta("rascunho_atual", p.id);
    estado.etapaTap = "ident"; location.hash = "#/tap/novo";
  }));
  $("#arqDevolucao").addEventListener("change", async e=>{
    const f = e.target.files[0]; if (!f) return;
    try {
      const d = desembalar(await lerArquivoTexto(f), "TAP-DEV-v1"), p = await db.get("propostas", d.proposta_id);
      if (!p) throw new Error(`A proposta ${d.proposta_id} não está nesta cópia.`);
      for (const x of d.pendencias) await db.put("pendencias", x);
      await db.put("propostas", {...p, status: "devolvida"}); await registrar("devolução recebida", {proposta_id: p.id}); toast("Devolução importada."); navegar();
    } catch(err){ mostrarErros("#errosDevolucao", [err.message]); }
  });
};

TELAS["#/triagem"] = async ()=>{
  const ps = (await db.list("propostas")).filter(p=>["em triagem", "devolvida", "em análise"].includes(p.status)).sort((a, b)=>(a.recebido_em || "").localeCompare(b.recebido_em || ""));
  const sel = estado.tapSel && await db.get("propostas", estado.tapSel), docs = await documentosChecklist();
  let ficha = "";
  if (sel){
    const anexos = await db.porIndice("anexos", "proposta_id", sel.id), pends = (await db.porIndice("pendencias", "proposta_id", sel.id));
    const falta = pendenciasTap(sel, anexos, docs);
    ficha = `<div class="card" id="fichaTriagem"><h2 style="margin-top:0">${esc(sel.id)} · ${esc(sel.titulo)} <span class="selo info" id="sitTap">${esc(sel.status)}</span></h2>
      <p>${esc(sel.unidade)} · ${esc(sel.responsavel)} · ${dinheiro.fmt(Math.round((sel.valor_estimado || 0) * 100))} · ${sel.prazo_meses} meses · ${esc(sel.objetivo_estrategico)}</p>
      <h3>Checklist de documentos</h3><ul>${docs.map(d=>{ const a = anexos.find(x=>x.tipo === d.tipo);
        return `<li>${esc(d.nome)}${d.obrigatorio ? " *" : ""}: ${a ? `<span class="ok-txt">anexado</span> (${esc(a.nome)})` : sel.ausencias?.[d.tipo] ? `<span class="alerta-txt">ausência justificada</span>: ${esc(sel.ausencias[d.tipo])}` : '<span class="erro-txt">falta</span>'}</li>`; }).join("")}</ul>
      ${falta.length ? `<p class="erro-txt">O app aponta: ${falta.map(esc).join(" · ")}</p>` : ""}
      ${pends.length ? `<h3>Pendências</h3><ul>${pends.map(x=>`<li>${esc(x.motivo)} · ${dataCurtaBR(x.aberta_em)}${x.resolvida_em ? " · resolvida" : ""}</li>`).join("")}</ul>` : ""}
      ${sel.status === "em triagem" ? `${campo("tMotivo", "Pendência (motivo)", {tipo: "textarea", linhas: 2})}<div id="errosTriagem"></div>
        <div class="linha-botoes"><button id="btnPendencia">Registrar pendência e devolver</button><button class="prim" id="btnAceitarTap">Aceitar para análise</button></div>` : ""}</div>`;
  }
  return `<h1>Triagem</h1><div class="card"><label class="botao prim">Importar pacote de proposta<input type="file" id="arqPacote" accept=".json" hidden></label><div id="errosPacote"></div></div>
    ${ficha}<div class="card tabela-wrap"><table><tr><th>TAP</th><th>Título</th><th>Unidade</th><th>Recebido</th><th>Situação</th></tr>
      ${ps.map(p=>`<tr><td><a href="#" data-tap="${esc(p.id)}">${esc(p.id)}</a></td><td>${esc(p.titulo)}</td><td>${esc(p.unidade)}</td><td>${dataBR(p.recebido_em)}</td><td>${esc(p.status)}</td></tr>`).join("")
        || '<tr><td colspan="5" class="vazio">Nenhuma proposta em triagem.</td></tr>'}</table></div>`;
};
TELAS_DEPOIS["#/triagem"] = ()=>{
  $$("[data-tap]").forEach(a=>a.addEventListener("click", e=>{ e.preventDefault(); estado.tapSel = a.dataset.tap; navegar(); }));
  $("#arqPacote").addEventListener("change", async e=>{
    const f = e.target.files[0]; if (!f) return;
    try {
      const c = desembalar(await lerArquivoTexto(f), "TAP-v1"), id = c.proposta.id;
      for (const a of await db.porIndice("anexos", "proposta_id", id)) await db.del("anexos", a.id);
      for (const a of c.anexos) await db.put("anexos", {id: `${id}-${a.tipo}`, proposta_id: id, tipo: a.tipo, nome: a.nome, mime: a.mime, tamanho: a.tamanho, conteudo: b64ParaBlob(a.base64, a.mime)});
      await db.put("propostas", {...c.proposta, status: "em triagem", recebido_em: agora()});
      await registrar("pacote recebido", {proposta_id: id, detalhe: f.name}); estado.tapSel = id; toast(`Proposta ${id} recebida.`); navegar();
    } catch(err){ mostrarErros("#errosPacote", [err.message]); }
  });
  $("#btnPendencia")?.addEventListener("click", async ()=>{
    const motivo = valorDe("tMotivo"); if (!motivo) return mostrarErros("#errosTriagem", ["Escreva o motivo da pendência (RN05)."]);
    const p = await db.get("propostas", estado.tapSel), pend = {id: uuid(), proposta_id: p.id, motivo, aberta_em: hojeISO(), resolvida_em: null};
    await db.put("pendencias", pend); await db.put("propostas", {...p, status: "devolvida"}); await registrar("pendência registrada", {proposta_id: p.id, detalhe: motivo});
    const abertas = (await db.porIndice("pendencias", "proposta_id", p.id)).filter(x=>!x.resolvida_em);
    baixar(`devolucao-${p.id}.json`, embalar("TAP-DEV-v1", {proposta_id: p.id, pendencias: abertas}), "application/json");
    toast("Pendência registrada. Envie o arquivo de devolução ao demandante."); navegar();
  });
  $("#btnAceitarTap")?.addEventListener("click", async ()=>{
    const p = await db.get("propostas", estado.tapSel), falta = pendenciasTap(p, await db.porIndice("anexos", "proposta_id", p.id), await documentosChecklist());
    if (falta.length) return mostrarErros("#errosTriagem", ["Checklist incompleto (RN06): " + falta.join(" · ")]);
    for (const x of (await db.porIndice("pendencias", "proposta_id", p.id)).filter(x=>!x.resolvida_em)) await db.put("pendencias", {...x, resolvida_em: hojeISO()});
    await db.put("propostas", {...p, status: "em análise", completa_em: agora()}); await registrar("aceita para análise", {proposta_id: p.id}); toast("Proposta aceita para análise."); navegar();
  });
};
