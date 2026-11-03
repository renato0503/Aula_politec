/* NIHDE · gestão de corpos não identificados e não reclamados */
"use strict";
const NI_SIT = ["não identificado", "identificado", "não reclamado", "sepultado", "identificado após sepultamento", "entregue"];
const NI_VIAS = ["necropapiloscopia", "DNA", "odontologia", "antropologia"];
const NI_STATUS_EXAME = ["não solicitado", "solicitado", "em andamento", "positivo", "negativo"];
const NI_UNIDADES = ["IML Cuiabá", "IML Sinop", "IML Rondonópolis", "IML Cáceres", "IML Barra do Garças"];
const NI_DIAS_SEPULTAMENTO = 30;

const niData = iso => iso ? dataCurtaBR(iso) : "—";
const niIniciais = n => String(n || "").trim().split(/\s+/).filter(Boolean).map(p=>p[0].toUpperCase()).join(". ");
const niDias = c => c?.data_entrada ? Math.max(0, Math.floor((Date.now() - new Date(c.data_entrada + "T12:00:00")) / 86400000)) : 0;
const niExames = c => c?.exames || {};
const niTemExame = (c, via) => (niExames(c)[via]?.status || "") === "positivo";
const niPodeEntregar = c => !!c?.identificado && !!c?.familia?.localizada && !c?.entrega_em;
const niPodeSepultar = c => !!c && !c.identificado && niDias(c) >= NI_DIAS_SEPULTAMENTO && !c.sepultamento;
const niSelo = s => s === "entregue" || s === "identificado" ? "ok" : s === "não identificado" ? "alerta" : s === "sepultado" || s === "não reclamado" ? "erro" : "info";
const niRotulo = c => c.identificado && c.nome ? niIniciais(c.nome) : "sem identificação";

teste("NIHDE: entrega exige identificação e família localizada", ()=>
  !niPodeEntregar({identificado: false, familia: {localizada: true}}) && !niPodeEntregar({identificado: true, familia: {}}) && niPodeEntregar({identificado: true, familia: {localizada: true}}));
teste("NIHDE: sepultamento só depois de 30 dias e sem identificação", ()=>{
  const c = {identificado: false, data_entrada: "2026-10-01"}; return niDias(c) >= 30 ? niPodeSepultar(c) : !niPodeSepultar(c);
});
teste("NIHDE: o seed tem não identificados e sepultados", ()=>{
  const cs = dadosEmbutidos("seed")?.corpos || []; return cs.length >= 20 && cs.some(c=>!c.identificado) && cs.some(c=>c.sepultamento);
});

async function niLog(corpo_id, acao, detalhe=""){
  await db.put("log", {id: uuid(), corpo_id, acao, detalhe, data_hora: agora(), perfil: estado.perfil || ""});
}
function niFiltro(){ return estado.niFiltro || (estado.niFiltro = {situacao: "", unidade: "", busca: ""}); }

/* ================= Painel ================= */
TELAS["#/painel"] = async ()=>{
  const cs = await db.list("corpos"), f = niFiltro();
  const conta = s => cs.filter(c=>c.situacao === s).length;
  const naoIdent = cs.filter(c=>!c.identificado).length;
  const naoRecl = conta("não reclamado");
  const ident = cs.filter(c=>c.identificado).length;
  const sep = cs.filter(c=>c.sepultamento).length;
  const entregues = conta("entregue");
  const porUnidade = NI_UNIDADES.map(u=>({u, n: cs.filter(c=>c.unidade === u).length, ni: cs.filter(c=>c.unidade === u && !c.identificado).length}));
  const vis = cs.filter(c=>(!f.situacao || c.situacao === f.situacao) && (!f.unidade || c.unidade === f.unidade))
    .filter(c=>!f.busca || normalizar([c.protocolo, c.municipio, c.local, c.nome].join(" ")).includes(normalizar(f.busca)))
    .sort((a, b)=>String(b.data_entrada).localeCompare(String(a.data_entrada)));
  return `<h1>Painel do NIHDE</h1><p class="sub">A pergunta do MVP: quantos corpos não identificados a POLITEC tem, sepultados ou não. Resposta: <b>${naoIdent}</b>.</p>
    <div class="card"><h2 style="margin-top:0">Desaparecidos · dados públicos</h2>
      <p class="sub">O módulo de desaparecidos é construído pela outra IA com a base pública do CNPD/MJ. Ele fica em uma página separada para não misturar a base pública com o cadastro dos corpos.</p>
      <a class="botao prim" href="desaparecidos.html" target="_blank" rel="noopener">Abrir o painel de desaparecidos</a></div>
    <div class="grade"><div class="card kpi"><div class="v" data-ni="total">${cs.length}</div><div class="r">corpos no recorte</div></div>
      <div class="card kpi"><div class="v" data-ni="nao-identificados">${naoIdent}</div><div class="r">não identificados</div></div>
      <div class="card kpi"><div class="v" data-ni="nao-reclamados">${naoRecl}</div><div class="r">identificados não reclamados</div></div>
      <div class="card kpi"><div class="v" data-ni="identificados">${ident}</div><div class="r">identificados</div></div>
      <div class="card kpi"><div class="v" data-ni="sepultados">${sep}</div><div class="r">sepultados</div></div>
      <div class="card kpi"><div class="v" data-ni="entregues">${entregues}</div><div class="r">entregues à família</div></div></div>
    <div class="card tabela-wrap"><h2 style="margin-top:0">Por unidade do IML</h2><table><tr><th>Unidade</th><th class="num">Corpos</th><th class="num">Não identificados</th></tr>
      ${porUnidade.map(x=>`<tr><td>${esc(x.u)}</td><td class="num">${x.n}</td><td class="num">${x.ni}</td></tr>`).join("")}</table></div>
    <div class="card"><div class="campos">
      ${campo("niSit", "Situação", {tipo: "select", opcoes: [["", "Todas"], ...NI_SIT.map(s=>[s, s])], valor: f.situacao})}
      ${campo("niUni", "Unidade", {tipo: "select", opcoes: [["", "Todas"], ...NI_UNIDADES.map(u=>[u, u])], valor: f.unidade})}
      ${campo("niBusca", "Buscar protocolo, município ou local", {valor: f.busca})}</div></div>
    <div class="card tabela-wrap"><h2 style="margin-top:0">Corpos (${vis.length})</h2><table><tr><th>Protocolo</th><th>Unidade</th><th>Identificação</th><th>Situação</th><th class="num">Dias</th><th>Entrada</th></tr>
      ${vis.map(c=>`<tr><td><a href="#/corpo/${encodeURIComponent(c.id)}">${esc(c.protocolo)}</a></td><td>${esc(c.unidade)}</td>
        <td>${esc(niRotulo(c))}</td><td><span class="selo ${niSelo(c.situacao)}">${esc(c.situacao)}</span></td>
        <td class="num">${c.sepultamento ? "—" : niDias(c)}</td><td>${niData(c.data_entrada)}</td></tr>`).join("")
        || '<tr><td colspan="6" class="vazio">Nenhum corpo com estes filtros.</td></tr>'}</table></div>`;
};
TELAS_DEPOIS["#/painel"] = ()=>{
  const f = niFiltro();
  $("#niSit").addEventListener("change", e=>{ f.situacao = e.target.value; navegar(); });
  $("#niUni").addEventListener("change", e=>{ f.unidade = e.target.value; navegar(); });
  let t = null;
  $("#niBusca").addEventListener("input", e=>{ clearTimeout(t); const v = e.target.value; t = setTimeout(()=>{ f.busca = v; navegar(); }, 300); });
};

/* ================= Lista e cadastro ================= */
TELAS["#/corpos"] = async ()=>{
  const cs = (await db.list("corpos")).sort((a, b)=>String(b.data_entrada).localeCompare(String(a.data_entrada)));
  return `<h1>Corpos</h1><p class="sub">Todos os corpos do NIHDE. A lista mostra as iniciais; o nome completo fica na ficha (LGPD).</p>
    <div class="linha-botoes" style="margin-top:0"><a class="botao prim" href="#/corpo/novo">Nova entrada</a>
      <a class="botao" href="#/relatorio">Relatório</a></div>
    <div class="card tabela-wrap"><table><tr><th>Protocolo</th><th>Unidade</th><th>Identificação</th><th>Situação</th><th>Entrada</th><th>Exames</th></tr>
      ${cs.map(c=>`<tr><td><a href="#/corpo/${encodeURIComponent(c.id)}">${esc(c.protocolo)}</a></td><td>${esc(c.unidade)}</td>
        <td>${esc(niRotulo(c))}</td><td><span class="selo ${niSelo(c.situacao)}">${esc(c.situacao)}</span></td><td>${niData(c.data_entrada)}</td>
        <td>${NI_VIAS.filter(v=>niExames(c)[v]?.status && niExames(c)[v].status !== "não solicitado").length}/4</td></tr>`).join("")
        || '<tr><td colspan="6" class="vazio">Nenhum corpo.</td></tr>'}</table></div>`;
};

TELAS["#/corpo/novo"] = async ()=>{
  return `<h1>Nova entrada</h1><p class="sub">Use apenas dados fictícios. O protocolo do Atena é único.</p>
    <form class="card" id="formNiNovo"><div class="campos">
      ${campo("niProt", "Protocolo do Atena", {obrigatorio: true, attrs: 'placeholder="2026.0001"'})}
      ${campo("niUnidade", "Unidade do IML", {tipo: "select", opcoes: NI_UNIDADES.map(u=>[u, u]), valor: "IML Cuiabá"})}
      ${campo("niEntrada", "Data de entrada", {tipo: "date", valor: hojeISO(), obrigatorio: true})}
      ${campo("niMun", "Município", {obrigatorio: true, valor: "Cuiabá"})}</div>
      ${campo("niLocal", "Local de localização", {obrigatorio: true})}
      <div class="campos">${campo("niSexo", "Sexo", {tipo: "select", opcoes: [["", "Não informado"], ["Feminino", "Feminino"], ["Masculino", "Masculino"]]})}
        ${campo("niIdade", "Idade aparente", {tipo: "number", attrs: 'min="0" max="120"'})}
        ${campo("niAltura", "Altura (m)", {attrs: 'placeholder="1,65"'})}
        ${campo("niPeso", "Peso (kg)", {attrs: 'placeholder="70"'})}
        ${campo("niOlhos", "Cor dos olhos")}${campo("niCabelo", "Cor do cabelo")}
        ${campo("niPele", "Pele / raça")}${campo("niSinais", "Sinais particulares")}</div>
      <label style="display:flex;gap:8px;align-items:center;margin:8px 0"><input type="checkbox" id="niIdent" style="width:auto">
        <span>O corpo já entrou identificado</span></label>
      <div class="campos" id="niBlocoNome" hidden>${campo("niNome", "Nome (fictício)")}${campo("niDoc", "Documento (fictício)")}</div>
      ${campo("niObs", "Observações", {tipo: "textarea", linhas: 2})}
      <div id="niErrosNovo"></div><div class="linha-botoes"><button class="prim" type="submit">Registrar a entrada</button></div></form>`;
};
TELAS_DEPOIS["#/corpo/novo"] = ()=>{
  $("#niIdent").addEventListener("change", e=>{ $("#niBlocoNome").hidden = !e.target.checked; });
  $("#formNiNovo").addEventListener("submit", async e=>{
    e.preventDefault();
    const protocolo = valorDe("niProt").trim(), unidade = valorDe("niUnidade"), entrada = valorDe("niEntrada");
    const identificado = $("#niIdent").checked, nome = valorDe("niNome");
    const erros = [];
    if (!protocolo) erros.push("Informe o protocolo do Atena.");
    if (!entrada) erros.push("Informe a data de entrada.");
    if (!valorDe("niMun")) erros.push("Informe o município.");
    if (!valorDe("niLocal")) erros.push("Informe o local de localização.");
    if (identificado && !nome) erros.push("Informe o nome fictício ou desmarque a identificação.");
    if (await db.list("corpos").then(cs=>cs.some(c=>normalizar(c.protocolo) === normalizar(protocolo)))) erros.push("Este protocolo já está registrado.");
    if (!mostrarErros("#niErrosNovo", erros)) return;
    const id = "C-" + String((await db.list("corpos")).length + 1).padStart(4, "0");
    const exames = Object.fromEntries(NI_VIAS.map(v=>[v, {status: "não solicitado", protocolo: "", data: ""}]));
    const c = {id, protocolo, unidade, data_entrada: entrada, municipio: valorDe("niMun"), local: valorDe("niLocal"),
      data_localizacao: entrada, sexo: valorDe("niSexo"), idade: valorDe("niIdade"), altura: valorDe("niAltura"), peso: valorDe("niPeso"),
      olhos: valorDe("niOlhos"), cabelo: valorDe("niCabelo"), pele: valorDe("niPele"), sinais: valorDe("niSinais"),
      nome: identificado ? nome : "", documento: identificado ? valorDe("niDoc") : "", identificado,
      situacao: identificado ? "identificado" : "não identificado", via_identificacao: identificado ? "manual" : "", data_identificacao: identificado ? entrada : "",
      exames, familia: {}, sepultamento: null, entrega_em: null, observacoes: valorDe("niObs"), criado_em: agora()};
    await db.put("corpos", c); await niLog(id, "entrada registrada", protocolo);
    toast(`Corpo ${protocolo} registrado.`); location.hash = "#/corpo/" + encodeURIComponent(id);
  });
};

/* ================= Ficha ================= */
TELAS["#/corpo/:id"] = async ({id})=>{
  const c = await db.get("corpos", id);
  if (!c) return `<div class="card vazio">Corpo não encontrado. <a href="#/corpos">Voltar</a></div>`;
  const logs = (await db.porIndice("log", "corpo_id", id)).sort((a, b)=>String(b.data_hora).localeCompare(String(a.data_hora)));
  const ex = niExames(c), fam = c.familia || {};
  return `<h1>${esc(c.protocolo)} <span class="selo ${niSelo(c.situacao)}" id="niSitAtual">${esc(c.situacao)}</span></h1>
    <p class="sub">${esc(c.unidade)} · entrada ${niData(c.data_entrada)} · ${c.sepultamento ? "sepultado" : niDias(c) + " dias no IML"} · ${esc(c.municipio)}</p>
    <div class="card"><h2 style="margin-top:0">Dados do corpo</h2><p>Local: ${esc(c.local)}<br>
      Nome: <b>${c.nome ? esc(c.nome) : "não identificado"}</b> · documento ${esc(c.documento || "—")} · ${esc(c.sexo || "sexo não informado")} · ${c.idade ? esc(c.idade) + " anos" : "idade não informada"}<br>
      Altura ${esc(c.altura || "—")} · peso ${esc(c.peso || "—")} · olhos ${esc(c.olhos || "—")} · cabelo ${esc(c.cabelo || "—")} · pele ${esc(c.pele || "—")}<br>
      Sinais: ${esc(c.sinais || "—")} · observações: ${esc(c.observacoes || "—")}</p>
      ${c.identificado ? `<p class="ok-txt"><b>Identificado</b> por ${esc(c.via_identificacao || "—")} em ${niData(c.data_identificacao)}.</p>` : '<p class="alerta-txt">Corpo sem identificação registrada.</p>'}</div>
    <div class="card tabela-wrap"><h2 style="margin-top:0">Exames de identificação</h2>
      <table><tr><th>Via</th><th>Status</th><th>Protocolo do exame</th><th>Data</th></tr>
        ${NI_VIAS.map(v=>`<tr><td>${esc(v)}</td><td><select id="niEx_${v}" aria-label="Status do exame ${esc(v)}">${NI_STATUS_EXAME.map(s=>`<option value="${s}" ${s === (ex[v]?.status || "não solicitado") ? "selected" : ""}>${s}</option>`).join("")}</select></td>
          <td><input id="niProto_${v}" value="${esc(ex[v]?.protocolo || "")}" placeholder="protocolo"></td>
          <td><input id="niData_${v}" type="date" value="${esc(ex[v]?.data || "")}"></td></tr>`).join("")}</table>
      <div id="niErrosExames"></div><div class="linha-botoes"><button class="prim" type="button" id="btnNiExames">Salvar exames</button></div></div>
    <div class="card"><h2 style="margin-top:0">Identificação</h2>
      <div class="campos">${campo("niViaIdent", "Via que identificou", {tipo: "select", opcoes: [["", "Escolha"], ...NI_VIAS.map(v=>[v, v]), ["manual", "registro manual"]]})}
        ${campo("niDataIdent", "Data da identificação", {tipo: "date", valor: hojeISO()})}</div>
      <div id="niErrosIdent"></div><div class="linha-botoes"><button class="prim" type="button" id="btnNiIdent">Registrar identificação</button></div></div>
    <div class="card"><h2 style="margin-top:0">Família e entrega</h2>
      <p class="sub">${fam.busca_iniciada_em ? "Busca iniciada em " + niData(fam.busca_iniciada_em) + ". " : "Busca de familiares ainda não iniciada. "}${fam.localizada ? "Família localizada." : "Família não localizada."}${c.entrega_em ? ` Corpo entregue em ${niData(c.entrega_em)}.` : ""}</p>
      <div class="campos">${campo("niFamNome", "Familiar (fictício)", {valor: fam.nome || ""})}${campo("niFamParentesco", "Parentesco", {valor: fam.parentesco || ""})}${campo("niFamContato", "Contato", {valor: fam.contato || ""})}</div>
      <div id="niErrosFam"></div><div class="linha-botoes"><button type="button" id="btnNiBusca">Busca iniciada</button>
        <button type="button" id="btnNiFam">Família localizada</button>
        <button class="prim" type="button" id="btnNiEntregar" ${niPodeEntregar(c) ? "" : "disabled"}>Entregar à família</button>
        <button type="button" id="btnNiNaoRecl" ${c.identificado && c.situacao !== "entregue" && c.situacao !== "não reclamado" ? "" : "disabled"}>Marcar como não reclamado</button></div></div>
    ${!c.identificado ? `<div class="card"><h2 style="margin-top:0">Sepultamento pelo município</h2>
      <p class="sub">${c.sepultamento ? `Sepultado em ${niData(c.sepultamento.data)} · ${esc(c.sepultamento.local || "")} · certidão ${esc(c.sepultamento.certidao || "—")}.` : `O sepultamento pode ser registrado depois de ${NI_DIAS_SEPULTAMENTO} dias. Hoje: ${niDias(c)} dias.`}</p>
      ${c.sepultamento ? "" : `<div class="campos">${campo("niSepData", "Data do sepultamento", {tipo: "date", valor: hojeISO()})}${campo("niSepMun", "Município", {valor: c.municipio})}
        ${campo("niSepLocal", "Local do sepultamento")}${campo("niSepCert", "Certidão de óbito de não identificado")}</div>
        <div id="niErrosSep"></div><div class="linha-botoes"><button class="prim" type="button" id="btnNiSepultar" ${niPodeSepultar(c) ? "" : "disabled"}>Registrar sepultamento</button></div>`}</div>` : ""}
    <div class="card tabela-wrap"><h2 style="margin-top:0">Auditoria</h2><table><tr><th>Data e hora</th><th>Perfil</th><th>Ação</th><th>Detalhe</th></tr>
      ${logs.map(l=>`<tr><td>${dataBR(l.data_hora)}</td><td>${esc(l.perfil)}</td><td>${esc(l.acao)}</td><td>${esc(l.detalhe || "")}</td></tr>`).join("") || '<tr><td colspan="4" class="vazio">Sem ações registradas.</td></tr>'}</table></div>`;
};
TELAS_DEPOIS["#/corpo/:id"] = ({id})=>{
  const atual = async ()=> db.get("corpos", id);
  const salvar = async (novo, acao, detalhe)=>{ await db.put("corpos", novo); await niLog(id, acao, detalhe); toast(acao + "."); navegar(); };
  $("#btnNiExames")?.addEventListener("click", async ()=>{
    const c = await atual(), exames = {};
    for (const v of NI_VIAS) exames[v] = {status: valorDe("niEx_" + v), protocolo: valorDe("niProto_" + v), data: valorDe("niData_" + v)};
    await salvar({...c, exames}, "exames atualizados");
  });
  $("#btnNiIdent")?.addEventListener("click", async ()=>{
    const c = await atual(), via = valorDe("niViaIdent"), data = valorDe("niDataIdent");
    if (!via || !data) return mostrarErros("#niErrosIdent", ["Informe a via e a data da identificação."]);
    const situacao = c.sepultamento ? "identificado após sepultamento" : "identificado";
    await salvar({...c, identificado: true, situacao, via_identificacao: via, data_identificacao: data, nome: c.nome || "Pessoa Fictícia Identificada"},
      "identificação registrada", `${via} em ${data}`);
  });
  $("#btnNiBusca")?.addEventListener("click", async ()=>{
    const c = await atual(); await salvar({...c, familia: {...(c.familia || {}), busca_iniciada_em: hojeISO()}}, "busca de familiares iniciada");
  });
  $("#btnNiFam")?.addEventListener("click", async ()=>{
    const c = await atual(), nome = valorDe("niFamNome"), parentesco = valorDe("niFamParentesco"), contato = valorDe("niFamContato");
    if (!nome) return mostrarErros("#niErrosFam", ["Informe o familiar localizado."]);
    await salvar({...c, familia: {...(c.familia || {}), nome, parentesco, contato, localizada: true, localizada_em: hojeISO()}}, "família localizada", nome);
  });
  $("#btnNiEntregar")?.addEventListener("click", async ()=>{
    const c = await atual();
    if (!niPodeEntregar(c)) return mostrarErros("#niErrosFam", ["A entrega exige identificação e família localizada."]);
    await salvar({...c, situacao: "entregue", entrega_em: hojeISO(), familia: {...c.familia, entrega_em: hojeISO()}}, "corpo entregue à família");
  });
  $("#btnNiNaoRecl")?.addEventListener("click", async ()=>{
    const c = await atual();
    if (!c.identificado) return mostrarErros("#niErrosFam", ["Só corpo identificado pode ficar não reclamado."]);
    await salvar({...c, situacao: "não reclamado", familia: {...(c.familia || {}), busca_sem_sucesso: true}}, "corpo marcado como não reclamado");
  });
  $("#btnNiSepultar")?.addEventListener("click", async ()=>{
    const c = await atual();
    if (!niPodeSepultar(c)) return mostrarErros("#niErrosSep", [`O sepultamento exige ${NI_DIAS_SEPULTAMENTO} dias e corpo sem identificação.`]);
    const data = valorDe("niSepData"), local = valorDe("niSepLocal"), certidao = valorDe("niSepCert");
    if (!data || !local || !certidao) return mostrarErros("#niErrosSep", ["Informe a data, o local e a certidão."]);
    await salvar({...c, situacao: "sepultado", sepultamento: {data, municipio: valorDe("niSepMun"), local, certidao}}, "sepultamento registrado", `${data} · ${local}`);
  });
};

/* ================= Relatório ================= */
TELAS["#/relatorio"] = async ()=>{
  const cs = await db.list("corpos");
  const linhas = NI_UNIDADES.map(u=>{
    const g = cs.filter(c=>c.unidade === u);
    return {u, total: g.length, ni: g.filter(c=>!c.identificado).length, nr: g.filter(c=>c.situacao === "não reclamado").length,
      id: g.filter(c=>c.identificado).length, sep: g.filter(c=>c.sepultamento).length, ent: g.filter(c=>c.situacao === "entregue").length};
  });
  const porVia = NI_VIAS.map(v=>({v, n: cs.filter(c=>c.via_identificacao === v).length}));
  const total = cs.length, ident = cs.filter(c=>c.identificado).length;
  return `<h1>Relatório do NIHDE</h1><p class="sub">Quantos corpos a POLITEC tem, por unidade e situação. O CSV leva uma linha por corpo.</p>
    <div class="grade"><div class="card kpi"><div class="v">${total}</div><div class="r">corpos</div></div>
      <div class="card kpi"><div class="v">${cs.filter(c=>!c.identificado).length}</div><div class="r">não identificados</div></div>
      <div class="card kpi"><div class="v">${cs.filter(c=>c.situacao === "não reclamado").length}</div><div class="r">não reclamados</div></div>
      <div class="card kpi"><div class="v">${total ? (ident / total * 100).toFixed(1).replace(".", ",") : "0,0"}%</div><div class="r">taxa de identificação</div></div></div>
    <div class="card tabela-wrap"><h2 style="margin-top:0">Por unidade</h2><table id="tabelaRel"><tr><th>Unidade</th><th class="num">Total</th><th class="num">Não identificados</th><th class="num">Não reclamados</th><th class="num">Identificados</th><th class="num">Sepultados</th><th class="num">Entregues</th></tr>
      ${linhas.map(x=>`<tr><td>${esc(x.u)}</td><td class="num">${x.total}</td><td class="num">${x.ni}</td><td class="num">${x.nr}</td><td class="num">${x.id}</td><td class="num">${x.sep}</td><td class="num">${x.ent}</td></tr>`).join("")}</table></div>
    <div class="card tabela-wrap"><h2 style="margin-top:0">Por via de identificação</h2><table><tr><th>Via</th><th class="num">Corpos</th></tr>
      ${porVia.map(x=>`<tr><td>${esc(x.v)}</td><td class="num">${x.n}</td></tr>`).join("")}</table></div>
    <div class="linha-botoes"><button class="prim" id="btnNiCsv">Baixar o CSV</button></div>`;
};
TELAS_DEPOIS["#/relatorio"] = ()=>{
  $("#btnNiCsv")?.addEventListener("click", async ()=>{
    const cs = await db.list("corpos");
    const cols = ["id","protocolo","unidade","data_entrada","municipio","local","sexo","idade","situacao","identificado","via_identificacao","data_identificacao","familia_localizada","sepultado","sepultamento_data","sepultamento_local","entrega_em"];
    const linhas = cs.map(c=>[c.id,c.protocolo,c.unidade,c.data_entrada,c.municipio,c.local,c.sexo,c.idade,c.situacao,c.identificado ? "sim" : "não",
      c.via_identificacao || "", c.data_identificacao || "", c.familia?.localizada ? "sim" : "não", c.sepultamento ? "sim" : "não",
      c.sepultamento?.data || "", c.sepultamento?.local || "", c.entrega_em || ""]);
    const csv = "﻿" + [cols.join(";"), ...linhas.map(l=>l.map(x=>/[;"\n]/.test(String(x)) ? `"${String(x).replace(/"/g, '""')}"` : x).join(";"))].join("\r\n");
    baixar(`nihde-${hojeISO()}.csv`, csv, "text/csv;charset=utf-8");
    await niLog("", "relatório exportado", `${cs.length} corpos`);
  });
};

/* ================= Configuração ================= */
async function configExtra(){
  return `<div class="card"><h2 style="margin-top:0">Privacidade</h2>
    <p class="sub">O MVP usa dados fictícios. Na versão institucional, nome da família, documento e local do sepultamento exigem acesso restrito e auditoria (LGPD). O app não acessa a rede.</p></div>`;
}
async function ligarConfigExtra(){}
