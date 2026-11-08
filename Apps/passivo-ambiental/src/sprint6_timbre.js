/* ================= Sprint 10 · Timbre da POLITEC no laudo (provisório) =================
   Mesmo cabeçalho e mesma faixa da missão do laudo do Agiliza+, com o setor deste
   laudo. Vale até a unidade enviar o layout oficial do laudo ambiental. */
function paTimbreEnderecos(){ return ["Avenida Gonçalo Antunes de Barros, 3245", "Novo Mato Grosso", "CEP 78058-743", "Cuiabá-MT"]; }
function paSetorTimbre(l){ return (l && l.setor) || "Diretoria de Interiorização"; }

/* ---------- Word ---------- */
const PA_NS_DOCX = 'xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main" xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships" xmlns:wp="http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing" xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" xmlns:pic="http://schemas.openxmlformats.org/drawingml/2006/picture"';
function paImagemDocx(rid, cx, cy, n, nome){
  return `<w:r><w:drawing><wp:inline distT="0" distB="0" distL="0" distR="0"><wp:extent cx="${cx}" cy="${cy}"/><wp:docPr id="${n}" name="${nome}" descr="${nome}"/><a:graphic><a:graphicData uri="http://schemas.openxmlformats.org/drawingml/2006/picture"><pic:pic><pic:nvPicPr><pic:cNvPr id="${n}" name="${nome}"/><pic:cNvPicPr/></pic:nvPicPr><pic:blipFill><a:blip r:embed="${rid}"/><a:stretch><a:fillRect/></a:stretch></pic:blipFill><pic:spPr><a:xfrm><a:off x="0" y="0"/><a:ext cx="${cx}" cy="${cy}"/></a:xfrm><a:prstGeom prst="rect"><a:avLst/></a:prstGeom></pic:spPr></pic:pic></a:graphicData></a:graphic></wp:inline></w:drawing></w:r>`;
}
function paLinhaDocx(txt, jc, negrito){
  return `<w:p><w:pPr><w:spacing w:after="0" w:line="240" w:lineRule="auto"/><w:jc w:val="${jc}"/></w:pPr><w:r><w:rPr>${negrito ? "<w:b/>" : ""}<w:sz w:val="18"/></w:rPr><w:t xml:space="preserve">${paXml(txt)}</w:t></w:r></w:p>`;
}
function paCelulaDocx(w, conteudo, borda){
  return `<w:tc><w:tcPr><w:tcW w:w="${w}" w:type="dxa"/>${borda ? '<w:tcBorders><w:right w:val="single" w:sz="12" w:space="0" w:color="1F3A7A"/></w:tcBorders>' : ""}<w:vAlign w:val="center"/></w:tcPr>${conteudo}</w:tc>`;
}
function paCabecalhoDocx(l){
  const brasao = `<w:p><w:pPr><w:spacing w:after="0"/></w:pPr>${paImagemDocx("rId1", 718185, 899160, 101, "Brasão da POLITEC")}</w:p>`;
  const unidade = paLinhaDocx("PERÍCIA OFICIAL E IDENTIFICAÇÃO TÉCNICA - POLITEC", "right", true) + paLinhaDocx(paSetorTimbre(l), "right");
  const endereco = paTimbreEnderecos().map(t=> paLinhaDocx(t, "left")).join("");
  return `<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:hdr ${PA_NS_DOCX}><w:tbl><w:tblPr><w:tblW w:w="9638" w:type="dxa"/><w:tblLayout w:type="fixed"/><w:tblCellMar><w:left w:w="100" w:type="dxa"/><w:right w:w="100" w:type="dxa"/></w:tblCellMar></w:tblPr><w:tblGrid><w:gridCol w:w="1400"/><w:gridCol w:w="5038"/><w:gridCol w:w="3200"/></w:tblGrid><w:tr>${paCelulaDocx(1400, brasao)}${paCelulaDocx(5038, unidade, true)}${paCelulaDocx(3200, endereco)}</w:tr></w:tbl>
<w:p><w:pPr><w:spacing w:before="120" w:after="120"/><w:jc w:val="center"/></w:pPr><w:r><w:rPr><w:b/><w:sz w:val="20"/></w:rPr><w:t xml:space="preserve">LAUDO PERICIAL AMBIENTAL Nº ${paXml(l.id_laudo || "")}</w:t></w:r></w:p></w:hdr>`;
}
function paCampoDocx(cod){ return `<w:fldSimple w:instr=" ${cod} "><w:r><w:rPr><w:sz w:val="18"/></w:rPr><w:t>1</w:t></w:r></w:fldSimple>`; }
function paRodapeDocx(){
  const t = x=> `<w:r><w:rPr><w:sz w:val="18"/></w:rPr><w:t xml:space="preserve">${x}</w:t></w:r>`;
  return `<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:ftr ${PA_NS_DOCX}><w:p><w:pPr><w:spacing w:after="40"/><w:jc w:val="right"/></w:pPr>${t("Página ")}${paCampoDocx("PAGE")}${t(" de ")}${paCampoDocx("NUMPAGES")}</w:p><w:p><w:pPr><w:spacing w:after="0"/><w:jc w:val="center"/></w:pPr>${paImagemDocx("rId1", 6120130, 424813, 102, "Missão da POLITEC")}</w:p></w:ftr>`;
}
function paRelsImagem(alvo){
  return `<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships"><Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/image" Target="${alvo}"/></Relationships>`;
}
function paEstilosDocx(){
  return `<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:styles xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main"><w:docDefaults><w:rPrDefault><w:rPr><w:rFonts w:ascii="Arial" w:hAnsi="Arial" w:cs="Arial"/><w:sz w:val="24"/><w:lang w:val="pt-BR"/></w:rPr></w:rPrDefault><w:pPrDefault><w:pPr><w:spacing w:after="120" w:line="300" w:lineRule="auto"/><w:jc w:val="both"/></w:pPr></w:pPrDefault></w:docDefaults></w:styles>`;
}
function paAplicarTimbreDocx(zip, l){
  const t = dadosEmbutidos("timbre");
  if (!t) throw new Error("timbre não embutido");
  zip.file("word/media/brasao.png", t.brasao, {base64: true});
  zip.file("word/media/faixa.jpg", t.faixa, {base64: true});
  zip.file("word/styles.xml", paEstilosDocx());
  zip.file("word/header1.xml", paCabecalhoDocx(l));
  zip.file("word/footer1.xml", paRodapeDocx());
  zip.file("word/_rels/header1.xml.rels", paRelsImagem("media/brasao.png"));
  zip.file("word/_rels/footer1.xml.rels", paRelsImagem("media/faixa.jpg"));
  const R = "http://schemas.openxmlformats.org/officeDocument/2006/relationships";
  zip.file("word/_rels/document.xml.rels", `<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships"><Relationship Id="rId1" Type="${R}/styles" Target="styles.xml"/><Relationship Id="rId2" Type="${R}/header" Target="header1.xml"/><Relationship Id="rId3" Type="${R}/footer" Target="footer1.xml"/></Relationships>`);
}
function paSecaoDocx(){
  return '<w:sectPr><w:headerReference w:type="default" r:id="rId2"/><w:footerReference w:type="default" r:id="rId3"/><w:pgSz w:w="11906" w:h="16838"/><w:pgMar w:top="1134" w:right="1134" w:bottom="1134" w:left="1134" w:header="567" w:footer="340" w:gutter="0"/></w:sectPr>';
}

/* ---------- versão impressa ---------- */
function paTimbreHtml(l){
  const t = dadosEmbutidos("timbre");
  return `<div class="pa-timbre">${t ? `<img alt="Brasão da POLITEC" src="data:image/png;base64,${t.brasao}">` : ""}
    <div class="unid"><div class="forte">PERÍCIA OFICIAL E IDENTIFICAÇÃO TÉCNICA - POLITEC</div><div>${esc(paSetorTimbre(l))}</div></div>
    <div class="ender">${paTimbreEnderecos().map(x=> `<div>${esc(x)}</div>`).join("")}</div></div>`;
}
function paEstiloImpressao(){
  const t = dadosEmbutidos("timbre");
  return `<style>
    .pa-timbre{display:flex;align-items:center;gap:10pt;font:9pt/1.3 Arial,sans-serif;color:#000}
    .pa-timbre img{height:25mm;width:auto}
    .pa-timbre .unid{flex:1;text-align:right;padding-right:10pt;border-right:2pt solid #1f3a7a}
    .pa-timbre .unid .forte{font-weight:700}
    .pa-timbre .ender{flex:none;min-width:48mm}
    table.pa-paginas{width:100%;border-collapse:collapse;margin:0;border:0}
    table.pa-paginas>thead>tr>td,table.pa-paginas>tbody>tr>td{padding:0;border:0;background:none}
    table.pa-paginas>thead>tr>td{padding-bottom:12pt}
    .pa-faixa-tela{display:block;width:100%;margin-top:18px}
    @media print{
      html{print-color-adjust:exact;-webkit-print-color-adjust:exact}
      .pa-faixa-tela{display:none}
      *:has(#paDocumento)>*:not(:has(#paDocumento)):not(#paDocumento):not(style){display:none!important}
      *:has(#paDocumento){display:block!important;margin:0!important;padding:0!important;border:0!important;max-width:none!important;width:auto!important;background:#fff!important;box-shadow:none!important}
      @page{size:A4;margin:12mm 18mm 25mm 20mm;
        @bottom-center{content:"Página " counter(page) " de " counter(pages);font:9pt Arial,sans-serif;vertical-align:top;padding-top:2mm;
          print-color-adjust:exact;-webkit-print-color-adjust:exact;
          ${t ? `background:url("data:image/jpeg;base64,${t.faixa}") center 7mm/100% auto no-repeat;` : ""}}}
    }</style>`;
}
function paFaixaTela(){
  const t = dadosEmbutidos("timbre");
  return t ? `<img class="pa-faixa-tela" alt="Missão da POLITEC" src="data:image/jpeg;base64,${t.faixa}">` : "";
}
teste("PA: o timbre da POLITEC está embutido", ()=> { const t = dadosEmbutidos("timbre"); return !!t && t.brasao.length > 1000 && t.faixa.length > 1000; });
