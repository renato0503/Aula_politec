/* Sistema de Controle de Necropsia · núcleo do app.
   Espelho do protótipo "Sistema de Controle de Necropsia — DMML / POLITEC"
   (entregue pela aluna em 02/11/2026 e revisado em 05/11/2026).

   Aqui ficam: o modelo do caso, as regras de negócio (RN01 a RN12), a busca, o
   acionamento de um novo corpo e os testes embutidos. A interface do espelho
   (painel, corpos, resumo, ficha do caso, gaveta e janelas) está em
   src/identidade.js, que entra por último no build. */

"use strict";

/* ================= vocabulário do processo ================= */

// as sete etapas do caso, na ordem do fluxograma
const TC_ETAPAS = [
  {n: 1, nome: "Acionamento"},
  {n: 2, nome: "Ocorrência e possível vítima"},
  {n: 3, nome: "Aguardando necropsia"},
  {n: 4, nome: "Necropsia em andamento"},
  {n: 5, nome: "Identificação"},
  {n: 6, nome: "Família e liberação"},
  {n: 7, nome: "Entrega de laudo para ADM"},
];

// os agentes causais do painel de resumo
const TC_AGENTES = ["Homicídio", "Suicídio", "Acidente de trânsito", "Afogamento", "Queda de altura", "Indeterminada"];

// os quatro materiais da necropsia
const TC_MATERIAIS = [
  {id: "sangue", nome: "Sangue"},
  {id: "bio", nome: "Material biológico"},
  {id: "projetil", nome: "Projétil"},
  {id: "pertences", nome: "Pertences"},
];

// os métodos de identificação
const TC_METODOS = ["Necropapiloscopia", "Odontologia legal", "DNA", "Antropologia forense", "Reconhecimento familiar"];

// os exames complementares: os métodos só se esgotam depois de um deles (RN11)
const TC_EXAMES_COMPL = ["DNA", "Odontologia legal", "Antropologia forense"];

// as situações mostradas no filtro da lista
const TC_STATUS = [
  "Ocorrência em andamento", "Aguardando necropsia", "Necropsia em andamento",
  "Aguardando identificação", "Identificado", "Não identificado",
  "Aguardando família", "Não reclamado", "Aguardando funerária", "Entregue à funerária",
  "Sepultado pelo Estado", "Entrega de laudo para ADM", "Custódia finalizada",
];

const TC_JUSTIFICATIVA_MIN = 20;
const TC_RETIFICACOES = ["Familiar localizado após o sepultamento", "Correção de dado do corpo",
  "Correção da identificação", "Correção de lacre ou laudo", "Outra correção"];
const TC_RETIFICACAO_MIN = 20;

/* ================= modelo do caso ================= */

// "2026-11-05T14:35"
const tcAgora = ()=>{ const d = new Date(), z = n => String(n).padStart(2, "0"); return `${d.getFullYear()}-${z(d.getMonth() + 1)}-${z(d.getDate())}T${z(d.getHours())}:${z(d.getMinutes())}`; };

// o nome do perfil ativo, como aparece na trilha e no histórico
const TC_NOMES_PERFIL = {tecnico: "Técnico", medico: "Médico Legista", gestor: "Gestor ADM"};
const tcNomePerfil = p => TC_NOMES_PERFIL[p] || p || "";

function tcEtapa(c){
  const n = Number(c?.etapa);
  if (Number.isFinite(n) && n >= 1) return Math.min(7, Math.max(1, Math.round(n)));
  if (c?.laudo?.recebido_em || c?.custodia_finalizada) return 7;
  if (c?.sepultamento || c?.familia?.liberado_em) return 6;
  if (c?.identificacao?.resultado === "nao_identificado" || c?.familia?.busca_iniciada_em) return 6;
  return 5;
}

// a situação mostrada na lista, no painel e no resumo
function tcStatus(c){
  if (!c) return "";
  if (c.custodia_finalizada || c.laudo?.recebido_em) return "Custódia finalizada";
  if (c.laudo?.entregue_em) return "Entrega de laudo para ADM";
  if (c.sepultamento?.autorizacao) return "Sepultado pelo Estado";
  if (tcEtapa(c) >= 7) return "Entrega de laudo para ADM";
  if (c.funeraria?.data_entrega) return "Entregue à funerária";
  if (c.familia?.liberado_em) return "Aguardando funerária";
  if (c.familia?.busca_iniciada_em) return c.familia.busca_sem_sucesso ? "Não reclamado" : "Aguardando família";
  const e = tcEtapa(c);
  if (e >= 5){
    if (c.identificacao?.resultado === "identificado" || c.identificado) return "Identificado";
    if (c.identificacao?.resultado === "nao_identificado") return "Não identificado";
    return "Aguardando identificação";
  }
  if (e === 4) return "Necropsia em andamento";
  if (e === 3) return "Aguardando necropsia";
  return "Ocorrência em andamento";
}

// RN05: fora da ficha, o nome aparece só pelas iniciais
const tcIniciais = n => String(n || "").trim().split(/\s+/).filter(Boolean).map(p => p[0].toUpperCase()).join(". ");
const tcRotuloLista = c => c && c.identificado && c.nome ? tcIniciais(c.nome) : "sem identificação";

function tcDias(c){
  if (!c?.criado_em) return 0;
  return Math.max(0, Math.floor((Date.now() - new Date(c.criado_em)) / 86400000));
}

// o resumo por agente causal, com as colunas do painel gerencial
function tcResumo(cs){
  const base = () => ({total: 0, familia: 0, sepultado: 0, aguardando: 0, nao_reclamado: 0, finalizada: 0});
  const mapa = new Map();
  const linha = a => { const r = base(); mapa.set(a, r); return r; };
  for (const a of TC_AGENTES) linha(a);
  for (const c of cs){
    const agente = c.agente_causal || "Indeterminada";
    const r = mapa.get(agente) || linha(agente);
    const s = tcStatus(c);
    r.total++;
    if (["Custódia finalizada", "Entregue à funerária", "Entrega de laudo para ADM", "Aguardando funerária"].includes(s)) r.familia++;
    if (s === "Sepultado pelo Estado") r.sepultado++;
    if (["Aguardando identificação", "Ocorrência em andamento", "Aguardando necropsia", "Necropsia em andamento"].includes(s)) r.aguardando++;
    if (["Aguardando família", "Identificado", "Não reclamado"].includes(s)) r.nao_reclamado++;
    if (s === "Custódia finalizada") r.finalizada++;
  }
  const linhas = [...mapa.entries()];
  const tot = base();
  for (const [, r] of linhas) for (const k of Object.keys(tot)) tot[k] += r[k];
  return {linhas, tot};
}

// RN04: protocolo, nome, documento, município ou lacre; todas as palavras precisam casar
async function tcBuscar(q){
  const n = normalizar(q).split(" ").filter(Boolean);
  if (!n.length) return [];
  const [cs, ls] = await Promise.all([db.list("corpos"), db.list("lacres")]);
  return cs.filter(c => {
    const alvo = normalizar([c.protocolo, c.numero_necropsia, c.nome, c.documento, c.municipio,
      c.ocorrencia?.delegacia, ...ls.filter(l => l.corpo_id === c.id_corpo).map(l => l.codigo)].join(" "));
    return n.every(p => alvo.includes(p));
  }).sort((a, b) => (b.criado_em || "").localeCompare(a.criado_em || ""));
}

/* ================= regras de negócio ================= */

// RN02: a liberação exige identificação e auto de entrega completo
function tcFaltaAuto(c, auto){
  const falta = [];
  if (!c.identificado) falta.push("corpo identificado");
  if (!String(auto?.responsavel || "").trim()) falta.push("responsável pela entrega");
  if (!String(auto?.documento || "").trim()) falta.push("documento do auto");
  if (!String(auto?.data || "").trim()) falta.push("data e hora da entrega");
  return falta;
}

// RN09: o sepultamento pelo Estado exige justificativa registrada
const tcJustificativaOk = t => String(t || "").trim().length >= TC_JUSTIFICATIVA_MIN;

// RN10: a custódia só se encerra com destino do corpo, laudo recebido e todos os lacres recebidos
function tcPendenciasEncerramento(c, ls){
  const p = [];
  if (!c.destino_final) p.push("destino do corpo (liberação à família ou sepultamento pelo Estado)");
  if (!c.laudo?.recebido_em) p.push("laudo recebido pela ADM");
  const sem = (ls || []).filter(l => l.coletado !== false && l.codigo && !l.recebido_em).length;
  if (sem) p.push(`${sem} lacre(s) sem recebimento confirmado pela ADM`);
  return p;
}

// RN11: os métodos só se esgotam depois de pelo menos um exame complementar sem resultado
const tcTentativas = c => c?.identificacao?.tentativas || [];
function tcPodeEsgotar(tent){
  return (tent || []).some(t => TC_EXAMES_COMPL.includes(t.metodo) && t.resultado !== "identificou");
}

// RN12: retificação exige tipo, o que muda e motivo com 20 caracteres ou mais
function tcFaltaRetificacao(r){
  const falta = [];
  if (!TC_RETIFICACOES.includes(r?.tipo)) falta.push("o tipo da retificação");
  if (!String(r?.texto || "").trim()) falta.push("o que muda");
  if (String(r?.motivo || "").trim().length < TC_RETIFICACAO_MIN) falta.push(`o motivo, com ${TC_RETIFICACAO_MIN} caracteres ou mais`);
  return falta;
}
const tcPodeRetificar = c => !!(c?.custodia_finalizada || c?.sepultamento);

// o recebimento de lacre e de laudo é exclusivo do Gestor ADM
const tcPodeReceber = perfil => perfil === "gestor";
// o Médico Legista lê até a etapa 5
const tcEtapaVisivel = (perfil, etapa) => perfil !== "medico" || etapa <= 5;

teste("RN02: liberar exige identificação e o auto completo", ()=>{
  const c = {identificado: true}, ok = {responsavel: "Familiar", documento: "AUTO-1", data: "2026-10-30T10:00"};
  return tcFaltaAuto(c, ok).length === 0 && tcFaltaAuto({identificado: false}, ok).join() === "corpo identificado"
    && tcFaltaAuto(c, {responsavel: "Familiar"}).length === 2;
});
teste("a justificativa do sepultamento exige 20 caracteres", ()=>
  !tcJustificativaOk("curta") && tcJustificativaOk("Justificativa registrada com vinte caracteres ou mais."));
teste("RN10: a custódia só se encerra com destino, laudo e lacres", ()=>{
  const ok = {destino_final: "família", laudo: {recebido_em: "x"}};
  return tcPendenciasEncerramento(ok, [{codigo: "L1", recebido_em: "y"}]).length === 0
    && tcPendenciasEncerramento(ok, [{codigo: "L1", recebido_em: "y"}, {codigo: "L2"}]).length === 1
    && tcPendenciasEncerramento({laudo: {recebido_em: "x"}}, []).length === 1
    && tcPendenciasEncerramento({destino_final: "sepultamento"}, []).length === 1;
});
teste("RN11: os métodos só se esgotam depois de exame complementar", ()=>
  !tcPodeEsgotar([]) && !tcPodeEsgotar([{metodo: "Necropapiloscopia", resultado: "sem resultado"}])
  && tcPodeEsgotar([{metodo: "Necropapiloscopia", resultado: "sem resultado"}, {metodo: "DNA", resultado: "sem resultado"}]));
teste("RN12: retificação exige tipo, texto e motivo", ()=>
  tcFaltaRetificacao({tipo: "Outra correção", texto: "x", motivo: "curto"}).length === 1
  && tcFaltaRetificacao({tipo: TC_RETIFICACOES[0], texto: "Familiar procurou o IML", motivo: "Familiar localizado depois do sepultamento."}).length === 0);
teste("só o Gestor ADM confirma recebimento", ()=> tcPodeReceber("gestor") && !tcPodeReceber("tecnico") && !tcPodeReceber("medico"));
teste("o Médico Legista não vê as etapas 6 e 7", ()=>
  tcEtapaVisivel("medico", 5) && !tcEtapaVisivel("medico", 6) && !tcEtapaVisivel("medico", 7) && tcEtapaVisivel("tecnico", 7));
teste("RN05: iniciais no lugar do nome completo", ()=>
  tcRotuloLista({identificado: true, nome: "Maria Fictícia Souza"}) === "M. F. S" && tcRotuloLista({identificado: false}) === "sem identificação");
teste("o exemplo tem os 10 corpos do protótipo", ()=> dadosEmbutidos("seed").corpos.length === 10);
teste("o resumo por agente causal soma as colunas", ()=>{
  const r = tcResumo([
    {agente_causal: "Homicídio", etapa: 5, situacao: "aguardando identificação"},
    {agente_causal: "Homicídio", etapa: 6, sepultamento: {autorizacao: "SE-1"}},
    {agente_causal: "Suicídio", etapa: 7, familia: {liberado_em: "x"}, custodia_finalizada: true},
  ]);
  const h = r.linhas.find(x => x[0] === "Homicídio")[1];
  const s = r.linhas.find(x => x[0] === "Suicídio")[1];
  return h.total === 2 && h.sepultado === 1 && h.aguardando === 1
    && s.familia === 1 && s.finalizada === 1 && r.tot.total === 3;
});

/* ================= gravação ================= */

async function tcAuditar(corpo_id, acao, motivo){
  await db.put("log", {id: uuid(), corpo_id, acao, motivo: motivo || "", perfil: estado.perfil || "", data_hora: agora()});
}

// grava os campos do caso e deixa a trilha de auditoria
async function tcGravar(id, dados, acao, motivo){
  const c = await db.get("corpos", id);
  if (!c) throw new Error("Corpo não encontrado.");
  await db.put("corpos", {...c, ...dados});
  await tcAuditar(id, acao, motivo);
  return {...c, ...dados};
}

// fecha a custódia quando as três condições do RN10 estão satisfeitas
async function tcTentarFinalizar(id){
  const c = await db.get("corpos", id);
  if (!c || c.custodia_finalizada) return false;
  const ls = await db.porIndice("lacres", "corpo_id", id);
  if (tcPendenciasEncerramento(c, ls).length) return false;
  await db.put("corpos", {...c, custodia_finalizada: true, finalizada_em: agora(), etapa: 7});
  await tcAuditar(id, "custódia finalizada", "destino, laudo e lacres confirmados");
  return true;
}

// RN01: o protocolo é único
async function tcProtocoloExistente(proposito){
  const ano = new Date().getFullYear(), usados = new Set((await db.list("corpos")).map(c => c.protocolo));
  let n = 1;
  while (usados.has(proposito) || usados.has(`NEC-${ano}-${String(n).padStart(3, "0")}`)) n++;
  return `NEC-${ano}-${String(n).padStart(3, "0")}`;
}

/* ================= telas de apoio ================= */

TELAS["#/corpo/novo"] = async ()=>{
  const nec = await tcProtocoloExistente();
  const agoraLocal = tcAgora();
  return `<div class="esp">
    <h1 class="esp-titulo-escuro">Novo acionamento</h1>
    <p class="esp-sub">Etapas 1 e 2 do caso. Use apenas dados fictícios. O protocolo é único (RN01).</p>
    <div class="esp-card">
      <h2 class="esp-titulo">Etapa 1 — Acionamento</h2>
      <p class="esp-sub">Número da necropsia e horário do acionamento.</p>
      <div class="esp-grid-2">
        <div class="esp-field"><label for="tcNec">Número da necropsia *</label>
          <input class="esp-input" id="tcNec" type="text" value="${esc(nec)}" data-esp-campo="numero_necropsia"></div>
        <div class="esp-field"><label for="tcAcionamento">Horário do acionamento *</label>
          <input class="esp-input" id="tcAcionamento" type="time" value="${esc(agoraLocal.slice(11, 16))}" data-esp-campo="acionamento_horario"></div>
      </div>
      <h2 class="esp-titulo esp-mt">Etapa 2 — Ocorrência e possível vítima</h2>
      <div class="esp-grid-2">
        <div class="esp-field"><label for="tcChegada">Data e hora da chegada ao local *</label>
          <input class="esp-input" id="tcChegada" type="datetime-local" value="${esc(agoraLocal)}" data-esp-campo="chegada"></div>
        <div class="esp-field"><label for="tcAgente">Agente causal *</label>
          <select class="esp-input" id="tcAgente" data-esp-campo="agente">${TC_AGENTES.map(a => `<option value="${esc(a)}">${esc(a)}</option>`).join("")}</select></div>
        <div class="esp-field"><label for="tcDelegacia">Delegacia *</label>
          <input class="esp-input" id="tcDelegacia" type="text" data-esp-campo="delegacia"></div>
        <div class="esp-field"><label for="tcAutoridade">Autoridade policial</label>
          <input class="esp-input" id="tcAutoridade" type="text" data-esp-campo="autoridade"></div>
        <div class="esp-field"><label for="tcEndereco">Endereço *</label>
          <input class="esp-input" id="tcEndereco" type="text" data-esp-campo="endereco"></div>
        <div class="esp-field"><label for="tcMunicipio">Município *</label>
          <input class="esp-input" id="tcMunicipio" type="text" data-esp-campo="municipio"></div>
        <div class="esp-field"><label for="tcUf">UF</label>
          <input class="esp-input" id="tcUf" type="text" value="MT" maxlength="2" data-esp-campo="uf"></div>
        <div class="esp-field"><label for="tcPossivel">Possível nome</label>
          <input class="esp-input" id="tcPossivel" type="text" data-esp-campo="possivel_nome"></div>
        <div class="esp-field"><label for="tcFiliacao">Filiação</label>
          <input class="esp-input" id="tcFiliacao" type="text" data-esp-campo="filiacao"></div>
        <div class="esp-field"><label for="tcNascimento">Data de nascimento</label>
          <input class="esp-input" id="tcNascimento" type="date" data-esp-campo="nascimento"></div>
        <div class="esp-field"><label for="tcIdade">Idade</label>
          <input class="esp-input" id="tcIdade" type="text" data-esp-campo="idade"></div>
        <div class="esp-field"><label for="tcSexo">Sexo</label>
          <select class="esp-input" id="tcSexo" data-esp-campo="sexo">
            <option value="M">M</option><option value="F">F</option><option value="Indeterminado">Indeterminado</option></select></div>
        <div class="esp-field"><label for="tcFonte">Fonte da informação</label>
          <input class="esp-input" id="tcFonte" type="text" data-esp-campo="fonte"></div>
        <div class="esp-field"><label for="tcDocumento">Documento encontrado</label>
          <input class="esp-input" id="tcDocumento" type="text" data-esp-campo="documento"></div>
        <div class="esp-field"><label for="tcTelefone">Telefone de familiar</label>
          <input class="esp-input" id="tcTelefone" type="text" data-esp-campo="telefone"></div>
      </div>
      <div class="esp-field esp-mt"><label for="tcObservacoes">Observações</label>
        <textarea class="esp-input" id="tcObservacoes" rows="4" data-esp-campo="observacoes"></textarea></div>
      <div class="esp-field esp-mt"><label for="tcTecnico">Técnico responsável *</label>
        <input class="esp-input" id="tcTecnico" type="text" data-esp-campo="tecnico"></div>
      <div id="tcErros"></div>
      <div class="esp-acoes"><button class="esp-btn" id="btnTcNovo" type="button">Registrar o acionamento</button></div>
    </div></div>`;
};

TELAS_DEPOIS["#/corpo/novo"] = ()=>{
  espLigarHero();
  $("#btnTcNovo")?.addEventListener("click", async ()=>{
    const v = id => valorDe(id);
    const erros = [];
    if (!v("tcNec")) erros.push("Informe o número da necropsia.");
    if (!v("tcChegada")) erros.push("Informe a data e a hora da chegada ao local.");
    if (!v("tcDelegacia")) erros.push("Informe a delegacia.");
    if (!v("tcEndereco")) erros.push("Informe o endereço.");
    if (!v("tcMunicipio")) erros.push("Informe o município.");
    if (!v("tcTecnico")) erros.push("Informe o técnico responsável.");
    const cs = await db.list("corpos");
    if (cs.some(c => normalizar(c.numero_necropsia) === normalizar(v("tcNec")))) erros.push("Este número de necropsia já está registrado (RN01).");
    if (!mostrarErros("#tcErros", erros)) return;
    const cid = "C-" + String(cs.length + 1).padStart(4, "0");
    const chegada = v("tcChegada");
    const possivel = v("tcPossivel");
    const corpo = {
      id_corpo: cid, protocolo: v("tcNec"), numero_necropsia: v("tcNec"), entrada: chegada.slice(0, 10),
      criado_em: chegada + ":00", tecnico: v("tcTecnico"), origem: v("tcDelegacia"), natureza: v("tcAgente"),
      agente_causal: v("tcAgente"), municipio: v("tcMunicipio"), local: v("tcEndereco"),
      nome: "", documento: "", desconhecido: true, identificado: false, sexo: v("tcSexo"), idade: v("tcIdade"),
      situacao: "em custódia", etapa: 2, etapa_em: agora(),
      acionamento: {horario: v("tcAcionamento"), numero: v("tcNec")},
      ocorrencia: {chegada, delegacia: v("tcDelegacia"), autoridade: v("tcAutoridade"), endereco: v("tcEndereco"),
        municipio: v("tcMunicipio"), uf: v("tcUf"), possivel_nome: possivel, filiacao: v("tcFiliacao"),
        nascimento: v("tcNascimento"), idade: v("tcIdade"), sexo: v("tcSexo"), fonte: v("tcFonte"),
        documento: v("tcDocumento"), telefone: v("tcTelefone"), observacoes: v("tcObservacoes"),
        fotos_doc: [], fotos_cena: []},
      camara: "", gaveta: "", estado_corpo: "", lacre_corpo: "", confirmado_entrada: false,
      necropsia: {}, identificacao: {}, familia: {}, funeraria: {}, laudo: {}, sepultamento: null,
      entrega: null, destino_final: "", custodia_finalizada: false, finalizada_em: "", retificacoes: [],
    };
    await db.put("corpos", corpo);
    await tcAuditar(cid, "acionamento registrado", `${corpo.numero_necropsia} · ${corpo.municipio}`);
    await registrar("corpo registrado", {detalhe: corpo.numero_necropsia});
    toast("Acionamento registrado.");
    location.hash = "#/corpo/" + encodeURIComponent(cid);
  });
};

TELAS["#/busca"] = async ()=>{
  const q = estado.tcBusca || "";
  const achados = q ? await tcBuscar(q) : [];
  return `<div class="esp">
    <h1 class="esp-titulo-escuro">Buscar corpo</h1>
    <p class="esp-sub">Por protocolo, nome, documento, delegacia ou lacre (RN04). Use apenas dados fictícios.</p>
    <div class="esp-card">
      <div class="esp-field"><label for="tcBusca">Protocolo, nome, documento ou lacre</label>
        <input class="esp-input" id="tcBusca" type="search" value="${esc(q)}" placeholder="Ex.: 000125/2026, Marcelo, RG 12.998.330-1, LA-44101"></div>
      <div class="esp-acoes"><button class="esp-btn" id="btnTcBuscar" type="button">Buscar</button></div>
    </div>
    ${q ? `<div class="esp-card esp-mt" id="tcResultado"><h2 class="esp-titulo">${achados.length} resultado(s) para “${esc(q)}”</h2>
      <div class="esp-tabela-wrap"><table class="esp-tabela">
        <thead><tr><th>Protocolo</th><th>Nome</th><th>Documento</th><th>Município</th><th>Situação</th></tr></thead>
        <tbody>${achados.map(c => `<tr>
          <td><a href="#/corpo/${encodeURIComponent(c.id_corpo)}">${esc(c.protocolo)}</a></td>
          <td>${c.identificado ? esc(c.nome) : "não identificado"}</td>
          <td>${esc(c.documento || "—")}</td><td>${esc(c.municipio)}</td>
          <td>${esc(tcStatus(c))}</td></tr>`).join("") || '<tr><td colspan="5" class="esp-vazio">Nenhum corpo encontrado.</td></tr>'}</tbody>
      </table></div></div>` : ""}</div>`;
};

TELAS_DEPOIS["#/busca"] = ()=>{
  espLigarHero();
  const ir = async ()=>{ estado.tcBusca = valorDe("tcBusca"); await registrar("busca", {detalhe: estado.tcBusca}); navegar(); };
  $("#btnTcBuscar")?.addEventListener("click", ir);
  $("#tcBusca")?.addEventListener("keydown", e=>{ if (e.key === "Enter") ir(); });
};
