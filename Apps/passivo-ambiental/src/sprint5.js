/* ================= Sprint 5 · Abas de metodologia, considerações, valoração e quesitos + .docx ================= */
const PA_METODOLOGIA_PADRAO = "A perícia ambiental foi realizada com interpretação de imagens de satélite, conferência em campo quando possível e delimitação da área afetada. As coordenadas e a base cartográfica constam dos mapas anexos. A metodologia e os critérios de valoração devem ser confirmados pelo perito responsável.";
const PA_CONSIDERACOES_PADRAO = "O sensoriamento remoto permitiu comparar a situação anterior e posterior ao dano, com apoio de imagens históricas. A interpretação considerou a cobertura vegetal, o uso do solo e as feições visíveis na cena.";
const PA_VALORACAO_PADRAO = "Memória de cálculo: área afetada (ha) x valor de referência por hectare. O valor de referência e os critérios de valoração precisam ser confirmados pela unidade.";

const paLaudoS4 = TELAS["#/laudo/:id"];
TELAS["#/laudo/:id"] = async (p)=>{
  const html = await paLaudoS4(p);
  const {r, l, mapas} = await paLaudoDe(p.id);
  if (!r) return html;
  const valorTotal = Number(l.valor_total || (Number(l.area_ha || 0) * Number(l.valor_ha || 0)));
  const cards = `<div class="card" id="paCardMetodologia"><h2 style="margin-top:0">Metodologia</h2>
      <p class="sub">Texto padrão editável; entra no laudo e no .docx.</p>
      <textarea id="paMetodologia" rows="4">${esc(l.metodologia || PA_METODOLOGIA_PADRAO)}</textarea></div>
    <div class="card" id="paCardConsideracoes"><h2 style="margin-top:0">Considerações</h2>
      <p class="sub">Sensoriamento remoto e leitura das imagens.</p>
      <textarea id="paConsideracoes" rows="4">${esc(l.consideracoes || PA_CONSIDERACOES_PADRAO)}</textarea></div>
    <div class="card" id="paCardValoracao"><h2 style="margin-top:0">Valoração do dano</h2>
      <p class="sub">Memória de cálculo: área x valor de referência. Os critérios precisam ser confirmados pela unidade.</p>
      <div class="campos">
        ${campo("paAreaHa", "Área afetada (ha)", {tipo: "number", valor: l.area_ha || "", attrs: 'min="0" step="0.01"'})}
        ${campo("paValorHa", "Valor de referência por ha (R$)", {tipo: "number", valor: l.valor_ha || "", attrs: 'min="0" step="0.01"'})}
        ${campo("paValorTotal", "Valor total (R$)", {tipo: "number", valor: valorTotal || "", attrs: 'readonly'})}</div>
      <textarea id="paValoracao" rows="4">${esc(l.valoracao || PA_VALORACAO_PADRAO)}</textarea></div>
    <div class="card" id="paCardQuesitos"><h2 style="margin-top:0">Quesitos</h2>
      <p class="sub">Respostas da requisição; se não houver quesitos, deixe em branco.</p>
      <textarea id="paQuesitos" rows="4">${esc(l.quesitos_texto || "")}</textarea></div>
    <div class="card" id="paCardDocx"><h2 style="margin-top:0">Seções e exportação</h2>
      <p class="sub">O .docx leva o texto e a memória de cálculo; os mapas seguem no PDF.</p>
      <div class="linha-botoes"><button type="button" class="prim" data-pa-salvar>Salvar as seções</button>
        <button type="button" id="btnPaDocx">Baixar .docx</button></div></div>`;
  return html + cards;
};

const paLaudoDepoisS4 = TELAS_DEPOIS["#/laudo/:id"];
TELAS_DEPOIS["#/laudo/:id"] = async (p)=>{
  await paLaudoDepoisS4?.(p);
  const total = ()=>{ const v = (Number(valorDe("paAreaHa") || 0) * Number(valorDe("paValorHa") || 0)); const el = $("#paValorTotal"); if (el) el.value = v ? v.toFixed(2) : ""; };
  $("#paAreaHa")?.addEventListener("input", total); $("#paValorHa")?.addEventListener("input", total); total();
  $$("[data-pa-salvar]").forEach(b=>b.addEventListener("click", async ()=>{
    const {l} = await paLaudoDe(p.id);
    const area = Number(valorDe("paAreaHa") || 0), valor = Number(valorDe("paValorHa") || 0);
    await db.put("laudos", {...l, metodologia: valorDe("paMetodologia"), consideracoes: valorDe("paConsideracoes"),
      valoracao: valorDe("paValoracao"), quesitos_texto: valorDe("paQuesitos"), area_ha: area, valor_ha: valor,
      valor_total: Number((area * valor).toFixed(2))});
    await registrar("seções do laudo salvas", {detalhe: l.id_laudo});
    toast("Seções do laudo salvas."); navegar();
  }));
  $("#btnPaDocx")?.addEventListener("click", async ()=>{
    try {
      const {r, l, mapas} = await paLaudoDe(p.id);
      const blob = paGerarDocx(r, l, mapas);
      baixar(`laudo-${l.id_laudo}.docx`, blob, "application/vnd.openxmlformats-officedocument.wordprocessingml.document");
      await registrar("laudo exportado em .docx", {detalhe: l.id_laudo});
      toast("Arquivo .docx gerado. Os mapas seguem no PDF.");
    } catch(err){ toast("Não consegui gerar o .docx: " + err.message); }
  });
};

function paXml(txt){ return String(txt ?? "").replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;").replace(/"/g, "&quot;"); }
function paParagrafo(txt, negrito){
  return `<w:p><w:r><w:rPr>${negrito ? "<w:b/>" : ""}</w:rPr><w:t xml:space="preserve">${paXml(txt)}</w:t></w:r></w:p>`;
}
function paGerarDocx(r, l, mapas){
  if (typeof PizZip === "undefined") throw new Error("biblioteca do .docx não embarcada");
  const linhas = [];
  linhas.push(paParagrafo("LAUDO PERICIAL AMBIENTAL", true));
  for (const [k, v] of paCabecalho(r, l)) linhas.push(paParagrafo(`${k}: ${v}`));
  linhas.push(paParagrafo("Metodologia", true), paParagrafo(l.metodologia || PA_METODOLOGIA_PADRAO));
  linhas.push(paParagrafo("Considerações", true), paParagrafo(l.consideracoes || PA_CONSIDERACOES_PADRAO));
  linhas.push(paParagrafo("Valoração do dano", true));
  linhas.push(paParagrafo(`Área afetada: ${l.area_ha || "—"} ha · Valor de referência: R$ ${l.valor_ha || "—"} · Valor total: R$ ${l.valor_total || "—"}`));
  linhas.push(paParagrafo(l.valoracao || PA_VALORACAO_PADRAO));
  linhas.push(paParagrafo("Quesitos", true), paParagrafo(l.quesitos_texto || "Sem quesitos."));
  linhas.push(paParagrafo("Conclusão", true), paParagrafo(l.conclusao || "Conclusão não registrada."));
  linhas.push(paParagrafo("Mapas anexados", true));
  for (const m of mapas) linhas.push(paParagrafo(`${PA_TIPOS_MAPA.find(t=>t[0] === paTipoMapa(m))?.[1] || "Mapa"} · ${paModelo(m.modelo_id).rotulo} · ${m.valor_extra || ""}`));
  const document = `<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:document ${PA_NS_DOCX}><w:body>${linhas.join("")}${paSecaoDocx()}</w:body></w:document>`;
  const zip = new PizZip();
  zip.file("[Content_Types].xml", `<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">
<Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>
<Default Extension="xml" ContentType="application/xml"/>
<Default Extension="png" ContentType="image/png"/>
<Default Extension="jpg" ContentType="image/jpeg"/>
<Override PartName="/word/document.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml"/>
<Override PartName="/word/styles.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.styles+xml"/>
<Override PartName="/word/header1.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.header+xml"/>
<Override PartName="/word/footer1.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.footer+xml"/>
</Types>`);
  zip.file("_rels/.rels", `<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="word/document.xml"/>
</Relationships>`);
  zip.file("word/document.xml", document);
  paAplicarTimbreDocx(zip, l);
  return zip.generate({type: "blob", mimeType: "application/vnd.openxmlformats-officedocument.wordprocessingml.document"});
}
teste("PA: o .docx tem o conteúdo do laudo", ()=>{
  const r = {numero_processo: "2026.1", orgao: "MP", data_requisicao: "2026-01-01"};
  const l = {id_laudo: "L-1", conclusao: "Dano confirmado", area_ha: 2, valor_ha: 100, valor_total: 200};
  const blob = paGerarDocx(r, l, []);
  return blob && blob.size > 1000;
});
