/* ================= Sprint 4 · Cópia do setor (RN06) ================= */
const fmtRncSetor = setor => "rnc-" + setor.toLowerCase().replace(/[^a-z0-9]+/g, "-") + ".json";

// monta o pacote só com as RNCs notificadas ao setor (RN06)
async function pacoteDoSetor(setor){
  const rncs = (await db.list("rncs")).filter(r=>normalizar(r.setor_notificado) === normalizar(setor));
  const numeros = new Set(rncs.map(r=>r.numero));
  const etapa = (await db.list("etapas")).filter(e=>numeros.has(e.rnc));
  const plano = (await db.list("planos")).filter(p=>numeros.has(p.rnc));
  const aval = (await db.list("avaliacoes")).filter(a=>numeros.has(a.rnc));
  const conteudo = {formato: "RNC-setor-v1", setor, gerado_em: agora(), rncs, etapas: etapa, planos: plano, avaliacoes: aval};
  return {conteudo, texto: JSON.stringify({...conteudo, verificacao: fnvRnc(JSON.stringify(conteudo))})};
}
teste("RN06: o pacote do setor leva só as RNCs daquele setor", async ()=>{
  return typeof pacoteDoSetor === "function" && typeof fmtRncSetor === "function";
});

TELAS["#/exportar"] = async ()=>{
  const setores = await db.list("setores"), rncs = await db.list("rncs");
  const porSetor = setores.map(s=>({s, n: rncs.filter(r=>normalizar(r.setor_notificado) === normalizar(s.sigla)).length})).sort((a, b)=>b.n - a.n);
  return `<h1>Arquivo do setor</h1><p class="sub">O arquivo leva só as RNCs notificadas ao setor (RN06). O setor devolve com o plano (FOR 2) e a avaliação (FOR 3).</p>
    <div class="card"><div class="campos">
      ${campo("expSetor", "Setor", {tipo: "select", opcoes: [["", "Escolha"], ...porSetor.map(({s, n})=>[s.sigla, `${s.sigla} · ${s.nome} (${n} RNC)`])]})}</div>
      <div class="linha-botoes"><button class="prim" id="btnExportarSetor">${icone("download")} Gerar o arquivo do setor</button></div>
      <p class="sub" id="resExportar"></p></div>
    <div class="card"><h2 style="margin-top:0">Receber o arquivo do setor</h2>
      <p class="sub">O setor devolve o mesmo arquivo, com o plano de ação e a avaliação. A CQUAL importa e mescla.</p>
      <label class="botao">Importar o arquivo devolvido<input type="file" id="arqSetor" accept=".json" hidden></label>
      <div id="errosSetor"></div><div id="resSetor"></div></div>`;
};
TELAS_DEPOIS["#/exportar"] = ()=>{
  $("#btnExportarSetor")?.addEventListener("click", async ()=>{
    const setor = valorDe("expSetor"); if (!setor) return alert("Escolha o setor.");
    const {conteudo, texto} = await pacoteDoSetor(setor);
    baixar(fmtRncSetor(setor), texto, "application/json");
    await registrar("arquivo do setor gerado", {detalhe: `${setor} · ${conteudo.rncs.length} RNCs`});
    $("#resExportar").innerHTML = `${conteudo.rncs.length} RNC(s) de ${esc(setor)} no arquivo, com ${conteudo.etapas.length} etapa(s), ${conteudo.planos.length} plano(s) e ${conteudo.avaliacoes.length} avaliação(ões).`;
  });
  $("#arqSetor")?.addEventListener("change", async e=>{
    const f = e.target.files[0]; if (!f) return;
    try {
      const p = JSON.parse(await lerArquivoTexto(f));
      if (p.formato !== "RNC-setor-v1") throw new Error("Este arquivo não é um pacote de setor.");
      if (fnvRnc(JSON.stringify({formato: p.formato, setor: p.setor, gerado_em: p.gerado_em, rncs: p.rncs, etapas: p.etapas, planos: p.planos, avaliacoes: p.avaliacoes})) !== p.verificacao)
        throw new Error("O código de verificação não confere: o arquivo foi alterado ou está incompleto.");
      const existentes = new Set((await db.list("rncs")).map(r=>r.numero));
      const novas = (p.rncs || []).filter(r=>existentes.has(r.numero));
      if (!novas.length) throw new Error("Nenhuma RNC do arquivo está nesta cópia.");
      for (const x of p.etapas || []) await db.put("etapas", x);
      for (const x of p.planos || []) await db.put("planos", x);
      for (const x of p.avaliacoes || []) await db.put("avaliacoes", x);
      for (const r of p.rncs) if (existentes.has(r.numero)) await db.put("rncs", r);
      await registrar("arquivo do setor recebido", {detalhe: `${p.setor} · ${novas.length} RNCs`});
      mostrarErros("#errosSetor", []);
      $("#resSetor").innerHTML = `<p><span class="selo ok">mesclado</span> ${novas.length} RNC(s) de ${esc(p.setor)}, ${(p.planos || []).length} plano(s) e ${(p.avaliacoes || []).length} avaliação(ões).</p>`;
    } catch(err){ mostrarErros("#errosSetor", [err.message]); }
  });
};

/* ---------- Perfil Setor: minhas RNCs, plano (FOR 2) e avaliação (FOR 3) ---------- */
TELAS["#/minhas"] = async ()=>{
  const setor = (await db.meta("setor")) || "";
  const setores = await db.list("setores");
  const rncs = (await db.list("rncs")).filter(r=>setor && normalizar(r.setor_notificado) === normalizar(setor)).sort((a, b)=>b.aberta_em.localeCompare(a.aberta_em));
  const plano = Object.fromEntries((await db.list("planos")).map(p=>[p.rnc, p]));
  const aval = Object.fromEntries((await db.list("avaliacoes")).map(a=>[a.rnc, a]));
  return `<h1>Minhas RNCs</h1><p class="sub">RNCs em que o seu setor foi notificado. Registre o plano (FOR 2) e a avaliação (FOR 3).</p>
    <div class="card"><div class="campos">${campo("rncMeuSetor", "Setor", {tipo: "select", opcoes: [["", "Escolha"], ...setores.map(s=>[s.sigla, `${s.sigla} · ${s.nome}`])], valor: setor})}</div>
      <div class="linha-botoes"><button id="btnSalvarSetor">Salvar setor</button></div></div>
    ${setor ? `<div class="card tabela-wrap"><table id="tabelaMinhasRnc"><tr><th>RNC</th><th>Categoria</th><th>Etapa</th><th>Plano (FOR 2)</th><th>Avaliação (FOR 3)</th><th></th></tr>
      ${rncs.map(r=>`<tr><td><a href="#/rnc/${encodeURIComponent(r.numero)}">${esc(r.numero)}</a></td><td>${esc(r.categoria)}</td><td>${esc(r.etapa)}</td>
        <td>${plano[r.numero]?.enviado_em ? dataCurtaBR(plano[r.numero].enviado_em) : '<span class="alerta-txt">sem plano</span>'}</td>
        <td>${aval[r.numero] ? (aval[r.numero].eficaz ? "eficaz" : "não eficaz") : "—"}</td>
        <td><button data-plano="${esc(r.numero)}">Plano</button><button data-aval="${esc(r.numero)}">Avaliação</button></td></tr>`).join("")
        || '<tr><td colspan="6" class="vazio">Nenhuma RNC para este setor.</td></tr>'}</table></div>
      <div class="card" id="formSetorBloco"></div>` : '<div class="card pendente">Escolha o setor para ver as RNCs.</div>'}`;
};
TELAS_DEPOIS["#/minhas"] = ()=>{
  $("#btnSalvarSetor")?.addEventListener("click", async ()=>{ await db.meta("setor", valorDe("rncMeuSetor")); toast("Setor salvo."); navegar(); });
  const abrir = (html)=>$("#formSetorBloco").innerHTML = html;
  $$("[data-plano]").forEach(b=>b.addEventListener("click", async ()=>{
    const n = b.dataset.plano, p = await db.get("planos", n + "-plano");
    abrir(`<h2 style="margin-top:0">Plano de ação (FOR 2) · ${esc(n)}</h2>
      <form id="formPlano"><div class="campos">${campo("plData", "Enviado em", {tipo: "date", valor: hojeISO()})}</div>
      ${campo("plAcoes", "Ações do plano", {tipo: "textarea", linhas: 4, valor: p?.acoes || "", obrigatorio: true})}
      <div id="errosPlano"></div><div class="linha-botoes"><button class="prim" type="submit">Registrar o plano</button></div></form>`);
    $("#formPlano").addEventListener("submit", async e=>{
      e.preventDefault();
      const acoes = valorDe("plAcoes"); if (acoes.length < 20) return mostrarErros("#errosPlano", ["Descreva as ações do plano (20 caracteres)."]);
      await db.put("planos", {...(p || {}), id: n + "-plano", rnc: n, enviado_em: valorDe("plData") || hojeISO(), acoes});
      await registrar("plano do setor registrado", {detalhe: n}); toast("Plano registrado."); navegar();
    });
  }));
  $$("[data-aval]").forEach(b=>b.addEventListener("click", async ()=>{
    const n = b.dataset.aval, a = await db.get("avaliacoes", n + "-aval");
    abrir(`<h2 style="margin-top:0">Avaliação da eficácia (FOR 3) · ${esc(n)}</h2>
      <form id="formAval"><div class="campos">${campo("avData", "Avaliada em", {tipo: "date", valor: hojeISO()})}
        ${campo("avEficaz", "A ação foi eficaz?", {tipo: "select", opcoes: [["sim", "Sim"], ["nao", "Não"]], valor: a?.eficaz ? "sim" : "nao"})}</div>
      ${campo("avObs", "Observação", {tipo: "textarea", linhas: 3, valor: a?.observacao || ""})}
      <div id="errosAval"></div><div class="linha-botoes"><button class="prim" type="submit">Registrar a avaliação</button></div></form>`);
    $("#formAval").addEventListener("submit", async e=>{
      e.preventDefault();
      await db.put("avaliacoes", {id: n + "-aval", rnc: n, eficaz: valorDe("avEficaz") === "sim", observacao: valorDe("avObs"), avaliado_em: valorDe("avData") || hojeISO()});
      await registrar("avaliação do setor registrada", {detalhe: n}); toast("Avaliação registrada."); navegar();
    });
  }));
};

/* ================= Sprint 5 · Painel ================= */
const rncDias = (a, b)=> a && b ? Math.max(0, Math.round((new Date(b) - new Date(a)) / 86400000)) : null;

// barras horizontais em SVG, com rótulo e número
function graficoBarras(titulo, pares, cor = "var(--accent)"){
  const max = Math.max(1, ...pares.map(([, n])=>n)), altura = 26, largura = 420;
  return `<div class="card"><h2 style="margin-top:0">${esc(titulo)}</h2>
    <svg viewBox="0 0 ${largura} ${Math.max(60, pares.length * altura + 10)}" role="img" aria-label="${esc(titulo)}" style="width:100%;height:auto">
      ${pares.map(([rot, n], i)=>{
        const w = Math.round(n / max * (largura - 170)), y = i * altura + 6;
        return `<text x="0" y="${y + 13}" font-size="12" fill="var(--ink2)">${esc(String(rot).slice(0, 22))}</text>
          <rect x="150" y="${y + 2}" width="${w}" height="14" rx="3" fill="${cor}"></rect>
          <text x="${156 + w}" y="${y + 13}" font-size="12" fill="var(--ink)">${n}</text>`;
      }).join("")}
    </svg></div>`;
}

TELAS["#/painel"] = async ()=>{
  const [rncs, etapas] = await Promise.all([db.list("rncs"), db.list("etapas")]);
  const hoje = hojeISO(), ativas = rncs.filter(r=>r.situacao === "aberta" || r.situacao === "aguardando complemento");
  const conta = (campo)=> Object.entries(rncs.reduce((a, r)=>{ const k = r[campo] || "—"; a[k] = (a[k] || 0) + 1; return a; }, {})).sort((a, b)=>b[1] - a[1]);
  // RN05: mesma categoria no mesmo setor notificado mais de uma vez
  const recorrencia = conta("categoria").map(([cat, n])=>{
    const setores = new Set(rncs.filter(r=>r.categoria === cat).map(r=>r.setor_notificado));
    return {cat, n, setores: [...setores]};
  }).filter(x=>x.n > 1 && x.setores.some(s=>rncs.filter(r=>r.categoria === x.cat && r.setor_notificado === s).length > 1));
  // vencidas: etapa aberta com prazo vencido
  const vencidas = etapas.filter(e=>!e.fim && e.prazo && e.prazo < hoje).map(e=>{
    const r = rncs.find(x=>x.numero === e.rnc); return {e, r, dias: rncDias(e.prazo, hoje)};
  }).filter(x=>x.r).sort((a, b)=>b.dias - a.dias);
  // tempo médio por etapa (só etapas fechadas)
  const tempos = {};
  for (const e of etapas.filter(x=>x.fim)){
    const d = rncDias(x_inicio(e), e.fim); if (d !== null){ (tempos[e.etapa] ||= []).push(d); }
  }
  function x_inicio(e){ return e.inicio; }
  const medias = Object.fromEntries(Object.entries(tempos).map(([k, v])=>[k, Math.round(v.reduce((a, b)=>a + b, 0) / v.length * 10) / 10]));
  return `<h1>Painel da CQUAL</h1><p class="sub">${rncs.length} RNCs no recorte · ${ativas.length} em andamento · ${vencidas.length} com etapa vencida.</p>
    <div class="grade">
      <div class="card kpi"><div class="v" data-rnc-ind="total">${rncs.length}</div><div class="r">RNCs no recorte</div></div>
      <div class="card kpi"><div class="v" data-rnc-ind="ativas">${ativas.length}</div><div class="r">em andamento</div></div>
      <div class="card kpi"><div class="v" data-rnc-ind="vencidas">${vencidas.length}</div><div class="r">com etapa vencida</div></div>
      <div class="card kpi"><div class="v" data-rnc-ind="recorrencia">${recorrencia.length}</div><div class="r">categorias recorrentes (RN05)</div></div></div>
    ${graficoBarras("RNCs por setor notificado", conta("setor_notificado"))}
    ${graficoBarras("RNCs por categoria", conta("categoria"), "var(--verde)")}
    ${graficoBarras("RNCs por etapa", conta("etapa"), "var(--ambar)")}
    <div class="card tabela-wrap"><h2 style="margin-top:0">Etapas vencidas</h2><table id="tabelaVencidas"><tr><th>RNC</th><th>Setor</th><th>Etapa</th><th>Prazo</th><th class="num">Dias</th></tr>
      ${vencidas.map(({e, r, dias})=>`<tr><td><a href="#/rnc/${encodeURIComponent(e.rnc)}">${esc(e.rnc)}</a></td><td>${esc(r.setor_notificado)}</td>
        <td>${esc(e.etapa)}</td><td>${dataCurtaBR(e.prazo)}</td><td class="num"><span class="erro-txt">${dias}</span></td></tr>`).join("")
        || '<tr><td colspan="5" class="vazio">Nenhuma etapa vencida.</td></tr>'}</table></div>
    <div class="card tabela-wrap"><h2 style="margin-top:0">Tempo médio por etapa</h2><table id="tabelaTempo"><tr><th>Etapa</th><th class="num">Dias (média)</th></tr>
      ${ETAPAS_RNC.map(e=>`<tr><td>${esc(e)}</td><td class="num">${medias[e] ?? "—"}</td></tr>`).join("")}</table></div>
    <div class="card"><h2 style="margin-top:0">Recorrência (RN05)</h2>
      ${recorrencia.length ? `<ul>${recorrencia.map(x=>`<li><b>${esc(x.cat)}</b>: ${x.n} ocorrências, em ${x.setores.map(esc).join(", ")}</li>`).join("")}</ul>`
        : '<p class="sub">Nenhuma categoria recorrente no mesmo setor.</p>'}</div>`;
};
