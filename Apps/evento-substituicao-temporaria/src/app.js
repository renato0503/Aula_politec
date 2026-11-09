/* Evento de Substituição Temporária · regras, telas e ações.
   O processo vem do documento da Simone Alem: ofício no SIGADOC, autorização
   hierárquica, Gabinete, análise de RH com a ficha, assinatura do Diretor Geral
   Adjunto, envio à SESP até o dia 05 e encerramento com a publicação no DO. */
"use strict";

const EST_MOTIVOS = [
  "Férias",
  "Licença Prêmio",
  "Licença para tratamento da própria saúde",
  "Licença para acompanhar pessoa da família",
];
const EST_FINAL = ["publicado", "indeferido"];
const EST_ETAPAS = [
  ["Abertura do ofício", "Unidade do gestor afastado"],
  ["Autorização hierárquica", "Chefias da linha hierárquica"],
  ["Gabinete de Direção", "Recebe e encaminha ao RH"],
  ["Análise de RH e ficha", "Gerência de Suporte à Gestão de Pessoas"],
  ["Assinatura", "Diretor Geral Adjunto"],
  ["Envio à SESP", "Gerência de Suporte à Gestão de Pessoas"],
  ["Publicação no Diário Oficial", "Encerra o evento"],
];
const EST_STATUS = {
  autorizacao: { rotulo: "Em autorização hierárquica", selo: "info", etapa: 2 },
  devolvido: { rotulo: "Devolvido à unidade", selo: "erro", etapa: 2 },
  gabinete: { rotulo: "No Gabinete de Direção", selo: "info", etapa: 3 },
  analise_rh: { rotulo: "Em análise de RH", selo: "info", etapa: 4 },
  aguardando_assinatura: { rotulo: "Aguardando assinatura", selo: "alerta", etapa: 5 },
  assinado: { rotulo: "Assinado · aguardando envio à SESP", selo: "info", etapa: 6 },
  encaminhado_sesp: { rotulo: "Encaminhado à SESP", selo: "info", etapa: 6 },
  publicado: { rotulo: "Publicado no Diário Oficial", selo: "ok", etapa: 7 },
  indeferido: { rotulo: "Indeferido", selo: "erro", etapa: 7 },
};

const estISO = d => `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, "0")}-${String(d.getDate()).padStart(2, "0")}`;
const estDias = (de, para) => Math.round((new Date(para + "T12:00:00") - new Date(de + "T12:00:00")) / 86400000);
const estSomar = (iso, n) => { const d = new Date(iso + "T12:00:00"); d.setDate(d.getDate() + n); return estISO(d); };
const estLimite = periodo => periodo ? periodo.slice(0, 7) + "-05" : "";
const estEncerra = e => e.status === "publicado";
const estEnvioNoPrazo = (e, data = hojeISO()) => !!e.periodo_inicio && data <= estLimite(e.periodo_inicio);

function estPrazo(e, hoje = hojeISO()){
  if (!e.periodo_inicio) return { limite: "", dias: null, situacao: "sem período" };
  const limite = estLimite(e.periodo_inicio), dias = estDias(hoje, limite);
  let situacao;
  if (e.status === "publicado") situacao = "publicado";
  else if (e.status === "indeferido") situacao = "indeferido";
  else if (e.envio_sesp_em) situacao = "enviado";
  else if (dias < 0) situacao = "atrasado";
  else if (dias === 0) situacao = "vence hoje";
  else situacao = "no prazo";
  return { limite, dias, situacao };
}
const EST_PRAZO_SELO = { "no prazo": "ok", "vence hoje": "alerta", atrasado: "erro", enviado: "info", publicado: "ok", indeferido: "erro", "sem período": "" };
const estStatusSelo = s => (EST_STATUS[s] || {}).selo || "";
const estStatusNome = s => (EST_STATUS[s] || {}).rotulo || s;
const estPrazoNome = s => ({ "no prazo": "No prazo", "vence hoje": "Vence hoje", atrasado: "Fora do prazo", enviado: "Enviado à SESP", publicado: "Publicado", indeferido: "Indeferido", "sem período": "Sem período" }[s] || s);

function estValidar(d, eventos){
  const erros = [];
  if (!d.numero_sigadoc) erros.push("Informe o número do processo no SIGADOC.");
  if (!d.unidade) erros.push("Escolha a unidade do gestor afastado.");
  if (!d.substituido) erros.push("Informe o gestor substituído.");
  if (!d.substituto) erros.push("Informe o substituto (RN02).");
  if (d.substituido && d.substituto && normalizar(d.substituido) === normalizar(d.substituto)) erros.push("O substituto não pode ser o próprio gestor substituído (RN02).");
  if (!EST_MOTIVOS.includes(d.motivo)) erros.push("Escolha um motivo válido: férias, licença prêmio, licença para tratamento da própria saúde ou licença para acompanhar pessoa da família (RN01).");
  if (!d.data_oficio || d.data_oficio > hojeISO()) erros.push("Informe a data do ofício (não pode ser futura).");
  if (!d.periodo_inicio || !d.periodo_fim) erros.push("Informe o início e o fim do período da substituição.");
  if (d.periodo_inicio && d.periodo_fim && d.periodo_fim < d.periodo_inicio) erros.push("O fim do período não pode ser anterior ao início.");
  if (d.periodo_inicio && d.data_oficio && d.periodo_inicio < d.data_oficio) erros.push("O período da substituição não pode começar antes da data do ofício.");
  if (eventos.some(e => normalizar(e.numero_sigadoc) === normalizar(d.numero_sigadoc))) erros.push("Este processo do SIGADOC já está cadastrado.");
  return erros;
}

teste("RN01: os quatro motivos válidos", () => EST_MOTIVOS.length === 4 && EST_MOTIVOS.includes("Férias"));
teste("RN02: substituto não pode ser o substituído", () => estValidar({ numero_sigadoc: "X", unidade: "U", substituido: "Ana", substituto: "Ana", motivo: "Férias", periodo_inicio: "2026-12-01", periodo_fim: "2026-12-10", data_oficio: "2026-11-01" }, []).some(e => e.includes("RN02")));
teste("RN06: o limite é o dia 05 do mês da substituição", () => estLimite("2026-12-15") === "2026-12-05");
teste("RN06: envio depois do dia 05 fica fora do prazo", () => estEnvioNoPrazo({ periodo_inicio: "2026-11-10" }, "2026-11-06") === false && estEnvioNoPrazo({ periodo_inicio: "2026-11-10" }, "2026-11-05") === true);
teste("RN07: só a publicação no DO encerra", () => estEncerra({ status: "encaminhado_sesp" }) === false && estEncerra({ status: "publicado" }) === true);
teste("Exemplo com 15 eventos", () => dadosEmbutidos("seed").eventos.length === 15);
teste("Todas as unidades do exemplo têm chefia e diretor", () => dadosEmbutidos("seed").unidades.every(u => u.chefia && u.diretor));
teste("Cada evento do exemplo tem autorização", () => dadosEmbutidos("seed").autorizacoes.length >= dadosEmbutidos("seed").eventos.length);

async function estUnidades(){ return Object.fromEntries((await db.list("unidades")).map(u => [u.id_unidade, u])); }
const estNomeUnidade = (e, us) => e.unidade_nome || (us[e.unidade] && us[e.unidade].nome) || e.unidade || "—";
const estPeriodo = e => e.periodo_inicio && e.periodo_fim ? `${dataCurtaBR(e.periodo_inicio)} a ${dataCurtaBR(e.periodo_fim)}` : "—";

async function estLog(evento_id, tipo, descricao, extra = {}){
  await db.put("log", { id: uuid(), evento_id, tipo_evento: tipo, descricao, perfil: estado.perfil || "", data_hora: agora(), ...extra });
}
async function estMudarStatus(e, status, extra = {}){
  await db.put("eventos", { ...e, status, ...extra });
}
function estProximoMes(){
  const d = new Date(); d.setDate(1); d.setMonth(d.getMonth() + 1); return estISO(d);
}

/* ---------- a trilha das sete etapas ---------- */
function estTrilho(e){
  const atual = (EST_STATUS[e.status] || {}).etapa || 1;
  return `<ol class="est-trilho" aria-label="Etapas do evento">${EST_ETAPAS.map(([nome, quem], i) => {
    const n = i + 1;
    const cls = e.status === "indeferido" && n === atual ? "erro" : n < atual ? "feito" : n === atual ? "atual" : "";
    return `<li class="${cls}"><span class="est-ponto" aria-hidden="true">${n < atual ? "✓" : n}</span>
      <div><b>${esc(nome)}</b><small>${esc(quem)}</small></div></li>`;
  }).join("")}</ol>`;
}

/* ---------- painel ---------- */
TELAS["#/painel"] = async () => {
  const es = await db.list("eventos"), us = await estUnidades(), hoje = hojeISO();
  const infos = es.map(e => ({ e, pr: estPrazo(e, hoje) }));
  const conta = s => es.filter(e => e.status === s).length;
  const emTramite = es.filter(e => !EST_FINAL.includes(e.status)).length;
  const atrasados = infos.filter(x => !EST_FINAL.includes(x.e.status) && !x.e.envio_sesp_em && x.pr.dias < 0).length;
  const proximos = infos.filter(x => !EST_FINAL.includes(x.e.status)).sort((a, b) => String(a.pr.limite).localeCompare(String(b.pr.limite))).slice(0, 8);
  return `<h1>Painel do evento</h1>
    <p class="sub">${es.length} eventos cadastrados. O envio à SESP precisa acontecer até o dia 05 do mês em que a substituição ocorre (RN06).</p>
    <div class="grade">
      <div class="card kpi"><div class="v" data-est-kpi="tramite">${emTramite}</div><div class="r">em tramitação</div></div>
      <div class="card kpi"><div class="v" data-est-kpi="assinatura">${conta("aguardando_assinatura")}</div><div class="r">aguardando assinatura</div></div>
      <div class="card kpi"><div class="v" data-est-kpi="sesp">${conta("encaminhado_sesp")}</div><div class="r">encaminhados à SESP</div></div>
      <div class="card kpi"><div class="v" data-est-kpi="publicados">${conta("publicado")}</div><div class="r">publicados no DO</div></div>
      <div class="card kpi ${atrasados ? "alerta" : ""}"><div class="v" data-est-kpi="atrasados">${atrasados}</div><div class="r">fora do prazo do dia 05</div></div>
    </div>
    <div class="card tabela-wrap"><h2 style="margin-top:0">Próximos do dia 05</h2>
      <table><tr><th>Processo</th><th>Unidade</th><th>Substituição</th><th>Período</th><th>Limite</th><th>Prazo</th><th>Situação</th></tr>
      ${proximos.map(x => `<tr><td><a href="#/evento/${encodeURIComponent(x.e.id_evento)}">${esc(x.e.numero_sigadoc)}</a></td>
        <td>${esc(estNomeUnidade(x.e, us))}</td><td>${esc(x.e.substituido)} → ${esc(x.e.substituto)}</td><td>${estPeriodo(x.e)}</td>
        <td>${dataCurtaBR(x.pr.limite)}</td><td><span class="selo ${EST_PRAZO_SELO[x.pr.situacao]}">${esc(estPrazoNome(x.pr.situacao))}</span></td>
        <td><span class="selo ${estStatusSelo(x.e.status)}">${esc(estStatusNome(x.e.status))}</span></td></tr>`).join("")
        || '<tr><td colspan="7" class="vazio">Nenhum evento em tramitação.</td></tr>'}</table></div>`;
};

/* ---------- lista de eventos ---------- */
function estFiltros(){ return estado.estFiltros || (estado.estFiltros = { status: "", motivo: "", unidade: "", busca: "" }); }
TELAS["#/eventos"] = async () => {
  const f = estFiltros(), es = await db.list("eventos"), us = await estUnidades(), b = normalizar(f.busca);
  const lista = es.filter(e => (!f.status || e.status === f.status) && (!f.motivo || e.motivo === f.motivo)
      && (!f.unidade || e.unidade === f.unidade)
      && (!b || normalizar(`${e.numero_sigadoc} ${e.substituido} ${e.substituto} ${e.unidade_nome || ""} ${e.motivo}`).includes(b)))
    .sort((a, c) => String(c.data_oficio).localeCompare(String(a.data_oficio)));
  return `<h1>Eventos <span class="sub">(${lista.length})</span></h1>
    <p class="sub"><a href="#/evento/novo">Abrir novo evento</a> · <a href="#/planilha">Ver a planilha de controle</a></p>
    <div class="card"><div class="campos">
      ${campo("estBusca", "Busca por processo, nome ou motivo", { valor: f.busca })}
      ${campo("estFiltroStatus", "Situação", { tipo: "select", opcoes: [["", "Todas"], ...Object.entries(EST_STATUS).map(([k, v]) => [k, v.rotulo])], valor: f.status })}
      ${campo("estFiltroMotivo", "Motivo", { tipo: "select", opcoes: [["", "Todos"], ...EST_MOTIVOS.map(m => [m, m])], valor: f.motivo })}
      ${campo("estFiltroUnidade", "Unidade", { tipo: "select", opcoes: [["", "Todas"], ...Object.values(us).map(u => [u.id_unidade, u.nome])], valor: f.unidade })}</div></div>
    <div class="card tabela-wrap"><table><tr><th>Processo</th><th>Unidade</th><th>Substituído → substituto</th><th>Motivo</th><th>Período</th><th>Limite</th><th>Situação</th></tr>
      ${lista.map(e => {
        const pr = estPrazo(e);
        return `<tr><td><a href="#/evento/${encodeURIComponent(e.id_evento)}">${esc(e.numero_sigadoc)}</a></td>
          <td>${esc(estNomeUnidade(e, us))}</td><td>${esc(e.substituido)} → ${esc(e.substituto)}</td><td>${esc(e.motivo)}</td>
          <td>${estPeriodo(e)}</td><td>${dataCurtaBR(pr.limite)} <span class="selo ${EST_PRAZO_SELO[pr.situacao]}">${esc(estPrazoNome(pr.situacao))}</span></td>
          <td><span class="selo ${estStatusSelo(e.status)}">${esc(estStatusNome(e.status))}</span></td></tr>`;
      }).join("") || '<tr><td colspan="7" class="vazio">Nenhum evento com estes filtros.</td></tr>'}</table></div>`;
};
TELAS_DEPOIS["#/eventos"] = () => {
  const f = estFiltros();
  [["estBusca", "busca", "change"], ["estFiltroStatus", "status", "input"], ["estFiltroMotivo", "motivo", "input"], ["estFiltroUnidade", "unidade", "input"]]
    .forEach(([id, k, ev]) => { const el = $("#" + id); if (el) el.addEventListener(ev, e => { f[k] = e.target.value; navegar(); }); });
};

/* ---------- novo evento ---------- */
TELAS["#/evento/novo"] = async () => {
  const us = await db.list("unidades");
  return `<h1>Abrir evento de substituição</h1>
    <p class="sub">O ofício indica o substituto e o motivo. O evento entra na autorização hierárquica e só chega ao Gabinete depois de todas as autorizações (RN03).</p>
    <form class="card" id="formEstNovo" novalidate><div class="campos">
      ${campo("estNumero", "Número do processo no SIGADOC", { obrigatorio: true, ajuda: "Ex.: 2026.0123-SIGADOC" })}
      ${campo("estDataOficio", "Data do ofício", { tipo: "date", valor: hojeISO(), obrigatorio: true })}
      ${campo("estUnidade", "Unidade do gestor afastado", { tipo: "select", opcoes: [["", "Escolha"], ...us.map(u => [u.id_unidade, u.nome])], obrigatorio: true })}
      ${campo("estMotivo", "Motivo do afastamento (RN01)", { tipo: "select", opcoes: [["", "Escolha"], ...EST_MOTIVOS.map(m => [m, m])], obrigatorio: true })}</div>
    <div class="campos">
      ${campo("estSubstituido", "Gestor substituído", { obrigatorio: true })}
      ${campo("estCargoSubstituido", "Cargo do substituído")}
      ${campo("estSubstituto", "Substituto", { obrigatorio: true, ajuda: "Não pode ser o próprio substituído (RN02)." })}
      ${campo("estCargoSubstituto", "Cargo do substituto")}</div>
    <div class="campos">
      ${campo("estInicio", "Início da substituição", { tipo: "date", valor: estProximoMes(), obrigatorio: true })}
      ${campo("estFim", "Fim da substituição", { tipo: "date", valor: estSomar(estProximoMes(), 14), obrigatorio: true })}
      ${campo("estObservacao", "Observação", { tipo: "textarea", linhas: 2 })}</div>
    <div id="estErros"></div>
    <div class="linha-botoes"><button class="prim" type="submit">Registrar ofício</button></div></form>`;
};
TELAS_DEPOIS["#/evento/novo"] = () => {
  $("#formEstNovo").addEventListener("submit", async e => {
    e.preventDefault();
    const es = await db.list("eventos"), us = await db.list("unidades");
    const u = us.find(x => x.id_unidade === valorDe("estUnidade"));
    const d = {
      numero_sigadoc: valorDe("estNumero"), data_oficio: valorDe("estDataOficio"), unidade: valorDe("estUnidade"),
      unidade_nome: u ? u.nome : valorDe("estUnidade"), motivo: valorDe("estMotivo"),
      substituido: valorDe("estSubstituido"), cargo_substituido: valorDe("estCargoSubstituido"),
      substituto: valorDe("estSubstituto"), cargo_substituto: valorDe("estCargoSubstituto"),
      periodo_inicio: valorDe("estInicio"), periodo_fim: valorDe("estFim"), observacao: valorDe("estObservacao"),
    };
    const erros = estValidar(d, es);
    if (!mostrarErros("#estErros", erros)) return;
    const seq = es.reduce((m, x) => Math.max(m, Number(String(x.id_evento).replace(/\D/g, "")) || 0), 0) + 1;
    const id = "EST-" + String(seq).padStart(4, "0");
    await db.put("eventos", { id_evento: id, ...d, status: "autorizacao", criado_em: agora() });
    const niveis = (u && u.niveis && u.niveis.length) ? u.niveis
      : [{ nivel: 1, gestor: "Chefia imediata", cargo: "Chefia da unidade" }, { nivel: 2, gestor: "Direção da unidade", cargo: "Direção" }];
    for (const nv of niveis) await db.put("autorizacoes", { id: uuid(), evento_id: id, nivel: nv.nivel, gestor: nv.gestor, cargo: nv.cargo, situacao: "pendente" });
    await estLog(id, "ofício registrado", `${d.numero_sigadoc} · ${d.substituido} → ${d.substituto} · ${d.motivo}`);
    await estLog(id, "enviado para autorização", `${niveis.length} níveis na linha hierárquica`);
    await registrar("evento aberto", { detalhe: d.numero_sigadoc });
    toast(`Evento ${d.numero_sigadoc} registrado.`);
    location.hash = "#/evento/" + encodeURIComponent(id);
  });
};

/* ---------- ficha do evento ---------- */
TELAS["#/evento/:id"] = async ({ id }) => {
  const e = await db.get("eventos", id);
  if (!e) return `<div class="card vazio">Evento não encontrado. <a href="#/eventos">Voltar</a></div>`;
  const us = await estUnidades();
  const auths = (await db.porIndice("autorizacoes", "evento_id", id)).sort((a, b) => a.nivel - b.nivel);
  const ficha = (await db.porIndice("fichas", "evento_id", id))[0];
  const pub = (await db.porIndice("publicacoes", "evento_id", id))[0];
  const logs = (await db.porIndice("log", "evento_id", id)).sort((a, b) => String(b.data_hora).localeCompare(String(a.data_hora)));
  const pr = estPrazo(e);
  const st = EST_STATUS[e.status] || { rotulo: e.status, selo: "", etapa: 1 };

  const resumo = `<div class="card"><h2 style="margin-top:0">Dados do evento</h2>
      <div class="est-dados">
        <div><span class="sub">Processo SIGADOC</span><b>${esc(e.numero_sigadoc)}</b></div>
        <div><span class="sub">Unidade</span><b>${esc(estNomeUnidade(e, us))}</b></div>
        <div><span class="sub">Gestor substituído</span><b>${esc(e.substituido)}</b><small>${esc(e.cargo_substituido || "")}</small></div>
        <div><span class="sub">Substituto</span><b>${esc(e.substituto)}</b><small>${esc(e.cargo_substituto || "")}</small></div>
        <div><span class="sub">Motivo</span><b>${esc(e.motivo)}</b></div>
        <div><span class="sub">Período</span><b>${estPeriodo(e)}</b></div>
        <div><span class="sub">Data do ofício</span><b>${dataCurtaBR(e.data_oficio)}</b></div>
        <div><span class="sub">Limite do dia 05</span><b>${dataCurtaBR(pr.limite)}</b><small>${esc(estPrazoNome(pr.situacao))}</small></div>
      </div>
      ${e.observacao ? `<p class="sub">${esc(e.observacao)}</p>` : ""}</div>`;

  const tramitacao = `<div class="card"><h2 style="margin-top:0">Autorizações da linha hierárquica (RN03)</h2>
      <div class="tabela-wrap"><table><tr><th>Nível</th><th>Gestor</th><th>Cargo</th><th>Situação</th><th>Data</th><th></th></tr>
      ${auths.map(a => `<tr><td>${a.nivel}</td><td>${esc(a.gestor)}</td><td>${esc(a.cargo || "")}</td>
        <td><span class="selo ${a.situacao === "autorizado" ? "ok" : a.situacao === "devolvido" ? "erro" : "alerta"}">${esc(a.situacao)}</span></td>
        <td>${a.data ? dataCurtaBR(a.data) : "—"}</td>
        <td>${e.status === "autorizacao" && a.situacao === "pendente"
          ? `${botaoSe("autorizar", `<button type="button" class="prim" data-est-autorizar="${esc(a.id)}">Autorizar</button>`)}
             ${botaoSe("devolver", `<button type="button" class="sec" data-est-devolver="${esc(a.id)}">Devolver</button>`)}` : ""}</td></tr>`).join("")}</table></div>
      ${e.status === "devolvido" ? `<div class="card pendente" style="margin:12px 0"><b>Evento devolvido à unidade.</b> Ajuste os dados e reenvie para a autorização.</div>
        <form id="formEstAjuste" novalidate><div class="campos">
          ${campo("estAjusteNumero", "Número do processo no SIGADOC", { valor: e.numero_sigadoc, obrigatorio: true })}
          ${campo("estAjusteData", "Data do ofício", { tipo: "date", valor: e.data_oficio, obrigatorio: true })}
          ${campo("estAjusteUnidade", "Unidade", { tipo: "select", opcoes: Object.values(us).map(u => [u.id_unidade, u.nome]), valor: e.unidade, obrigatorio: true })}
          ${campo("estAjusteMotivo", "Motivo", { tipo: "select", opcoes: EST_MOTIVOS.map(m => [m, m]), valor: e.motivo, obrigatorio: true })}</div>
        <div class="campos">
          ${campo("estAjusteSubstituido", "Gestor substituído", { valor: e.substituido, obrigatorio: true })}
          ${campo("estAjusteCargoSubstituido", "Cargo do substituído", { valor: e.cargo_substituido })}
          ${campo("estAjusteSubstituto", "Substituto", { valor: e.substituto, obrigatorio: true })}
          ${campo("estAjusteCargoSubstituto", "Cargo do substituto", { valor: e.cargo_substituto })}</div>
        <div class="campos">
          ${campo("estAjusteInicio", "Início", { tipo: "date", valor: e.periodo_inicio, obrigatorio: true })}
          ${campo("estAjusteFim", "Fim", { tipo: "date", valor: e.periodo_fim, obrigatorio: true })}
          ${campo("estAjusteObservacao", "Observação", { tipo: "textarea", linhas: 2, valor: e.observacao || "" })}</div>
        <div id="estErrosAjuste"></div>
        <div class="linha-botoes">${botaoSe("reenviar", '<button type="submit" class="prim">Salvar ajuste e reenviar</button>')}
          ${botaoSe("reenviar", '<button type="button" class="sec" id="btnEstReenviar">Reenviar sem alterar</button>')}</div></form>` : ""}</div>
    <div class="card"><h2 style="margin-top:0">Gabinete de Direção</h2>
      ${e.status === "gabinete"
        ? `<p class="sub">O evento está autorizado. O Gabinete encaminha o caso à Gerência de Suporte à Gestão de Pessoas (RN04).</p>
           <div class="linha-botoes">${botaoSe("enviar_gabinete", '<button type="button" class="prim" id="btnEstEnviarRh">Encaminhar ao RH</button>')}</div>`
        : `<p class="sub">${["analise_rh", "aguardando_assinatura", "assinado", "encaminhado_sesp", "publicado"].includes(e.status) ? "Etapa cumprida: o evento já está com o RH." : "O Gabinete recebe o evento depois de todas as autorizações."}</p>`}</div>
    <div class="card"><h2 style="margin-top:0">Envio à SESP e prazo (RN06)</h2>
      ${estCardEnvio(e, pr)}</div>`;

  const cardFicha = `<div class="card" id="estCardFicha"><h2 style="margin-top:0">Ficha de solicitação de substituição temporária</h2>
      ${ficha ? `<div class="est-dados">
          <div><span class="sub">Número da ficha</span><b>${esc(ficha.numero_ficha)}</b></div>
          <div><span class="sub">Data</span><b>${dataCurtaBR(ficha.data)}</b></div>
          <div><span class="sub">Analista</span><b>${esc(ficha.analista || "—")}</b></div>
          <div><span class="sub">Situação</span><b>Anexada ao processo</b></div></div>
        ${ficha.observacao ? `<p class="sub">${esc(ficha.observacao)}</p>` : ""}`
        : e.status === "analise_rh"
          ? `<p class="sub">A Gerência de Suporte à Gestão de Pessoas analisa a demanda e inclui a ficha no processo (RN04).</p>
             <form id="formEstFicha"><div class="campos">
               ${campo("estFichaNumero", "Número da ficha", { valor: "FS-" + (e.numero_sigadoc || "").replace(/\D/g, "").slice(-4), obrigatorio: true })}
               ${campo("estFichaData", "Data", { tipo: "date", valor: hojeISO(), obrigatorio: true })}
               ${campo("estFichaAnalista", "Analista responsável", { obrigatorio: true })}</div>
               ${campo("estFichaObs", "Observação", { tipo: "textarea", linhas: 2 })}
               <div id="estErrosFicha"></div>
               <div class="linha-botoes">${botaoSe("incluir_ficha", '<button type="submit" class="prim">Incluir a ficha e enviar para assinatura</button>')}</div></form>`
          : `<p class="sub">A ficha é incluída na análise de RH, antes da assinatura.</p>`}</div>`;

  const cardAssinatura = `<div class="card" id="estCardAssinatura"><h2 style="margin-top:0">Assinatura do Diretor Geral Adjunto (RN05)</h2>
      ${e.assinado_em ? `<div class="est-dados">
          <div><span class="sub">Assinado por</span><b>${esc(e.assinado_por)}</b></div>
          <div><span class="sub">Cargo</span><b>${esc(e.assinado_cargo || "")}</b></div>
          <div><span class="sub">Data</span><b>${dataCurtaBR(e.assinado_em)}</b></div></div>`
        : e.status === "aguardando_assinatura"
          ? `<p class="sub">A ficha está anexada. A assinatura é do Diretor Geral Adjunto; depois dela, o evento volta ao RH para o envio à SESP.</p>
             <form id="formEstAssinar"><div class="campos">
               ${campo("estAssNome", "Nome do signatário", { obrigatorio: true })}
               ${campo("estAssCargo", "Cargo", { valor: "Diretor Geral Adjunto", obrigatorio: true })}</div>
               <div id="estErrosAssinar"></div>
               <div class="linha-botoes">${botaoSe("assinar", '<button type="submit" class="prim">Assinar o evento</button>')}</div></form>`
          : `<p class="sub">A assinatura acontece depois da ficha de RH e antes do envio à SESP.</p>`}</div>`;

  const cardPublicacao = `<div class="card" id="estCardPublicacao"><h2 style="margin-top:0">Publicação no Diário Oficial (RN07)</h2>
      ${pub ? `<div class="est-dados">
          <div><span class="sub">Publicação</span><b>${esc(pub.numero_do)}</b></div>
          <div><span class="sub">Data</span><b>${dataCurtaBR(pub.data_publicacao)}</b></div>
          <div><span class="sub">Situação</span><b>Evento encerrado</b></div></div>`
        : e.status === "encaminhado_sesp"
          ? `<p class="sub">O evento está na SESP. O encerramento só acontece com a publicação no Diário Oficial (RN07).</p>
             <form id="formEstPublicar"><div class="campos">
               ${campo("estPubNumero", "Número da publicação no DO", { obrigatorio: true })}
               ${campo("estPubData", "Data da publicação", { tipo: "date", valor: hojeISO(), obrigatorio: true })}</div>
               <div id="estErrosPublicar"></div>
               <div class="linha-botoes">${botaoSe("publicar", '<button type="submit" class="prim">Registrar publicação e encerrar</button>')}</div></form>`
          : `<p class="sub">${e.status === "publicado" ? "Publicado no Diário Oficial." : "A publicação é registrada depois do envio à SESP."}</p>`}
      ${!EST_FINAL.includes(e.status) ? `<hr class="est-divisor"><h3>Indeferimento</h3>
        <form id="formEstIndeferir"><div class="campos">
          ${campo("estIndMotivo", "Motivo do indeferimento", { tipo: "select", opcoes: [["", "Escolha"], ["Enviado depois do dia 05 (RN06)", "Enviado depois do dia 05 (RN06)"], ["Motivo do afastamento não se enquadra (RN01)", "Motivo do afastamento não se enquadra (RN01)"], ["Documentação incompleta", "Documentação incompleta"], ["Outro", "Outro"]], obrigatorio: true })}</div>
          <div id="estErrosIndeferir"></div>
          <div class="linha-botoes">${botaoSe("indeferir", '<button type="submit" class="perigo">Indeferir o evento</button>')}</div></form>` : ""}</div>`;

  const historico = `<div class="card tabela-wrap"><h2 style="margin-top:0">Histórico</h2>
      <table><tr><th>Data e hora</th><th>Evento</th><th>Descrição</th><th>Perfil</th></tr>
      ${logs.map(l => `<tr><td>${dataBR(l.data_hora)}</td><td>${esc(l.tipo_evento)}</td><td>${esc(l.descricao)}</td><td>${esc(l.perfil || "—")}</td></tr>`).join("")
        || '<tr><td colspan="4" class="vazio">Sem movimentação.</td></tr>'}</table></div>`;

  return `<h1>${esc(e.numero_sigadoc)} <span class="selo ${st.selo}" id="estStatusAtual">${esc(st.rotulo)}</span></h1>
    <p class="sub">${esc(e.substituido)} → ${esc(e.substituto)} · ${esc(e.motivo)} · ${estPeriodo(e)} · ${esc(estNomeUnidade(e, us))}</p>
    ${estTrilho(e)}
    <div class="grade">
      <div class="card kpi est-kpi-data"><div class="v">${dataCurtaBR(pr.limite)}</div><div class="r">limite do dia 05</div></div>
      <div class="card kpi ${pr.situacao === "atrasado" ? "alerta" : ""}"><div class="v" id="estDias">${pr.dias === null ? "—" : numBR(pr.dias)}</div><div class="r">dias até o limite</div></div>
      <div class="card kpi"><div class="v">${auths.filter(a => a.situacao === "autorizado").length}/${auths.length}</div><div class="r">autorizações</div></div>
    </div>
    ${abas("evento", [
      { id: "resumo", titulo: "Resumo", html: resumo },
      { id: "tramitacao", titulo: "Tramitação", html: tramitacao },
      { id: "ficha", titulo: "Ficha de RH", html: cardFicha },
      { id: "assinatura", titulo: "Assinatura", html: cardAssinatura },
      { id: "publicacao", titulo: "Publicação", html: cardPublicacao },
      { id: "historico", titulo: "Histórico", html: historico },
    ])}`;
};

function estCardEnvio(e, pr){
  if (e.envio_sesp_em) return `<div class="est-dados">
      <div><span class="sub">Enviado em</span><b>${dataCurtaBR(e.envio_sesp_em)}</b></div>
      <div><span class="sub">Limite</span><b>${dataCurtaBR(pr.limite)}</b></div>
      <div><span class="sub">Situação</span><b>${esc(estPrazoNome(pr.situacao))}</b></div></div>`;
  if (e.status === "indeferido") return `<p class="sub">Evento indeferido. ${esc(e.indeferido_motivo || "")}</p>`;
  if (e.status === "assinado" || e.status === "encaminhado_sesp"){
    const noPrazo = estEnvioNoPrazo(e);
    return `<p class="sub">A SESP recebe o evento pela Gerência de Suporte à Gestão de Pessoas. O prazo é o dia 05 do mês da substituição.</p>
      <p><b>Limite:</b> ${dataCurtaBR(pr.limite)} · <span class="selo ${EST_PRAZO_SELO[pr.situacao]}">${esc(estPrazoNome(pr.situacao))}</span></p>
      ${noPrazo ? `<div class="linha-botoes">${botaoSe("enviar_sesp", '<button type="button" class="prim" id="btnEstEnviarSesp">Encaminhar à SESP</button>')}</div>`
        : `<div class="card pendente"><b>Fora do prazo (RN06).</b> O envio depois do dia 05 implica indeferimento. Registre o indeferimento na aba Publicação.</div>`}`;
  }
  return `<p class="sub">O envio à SESP acontece depois da assinatura do Diretor Geral Adjunto.</p>`;
}

TELAS_DEPOIS["#/evento/:id"] = async ({ id }) => {
  const recarregar = async (msg) => { if (msg) toast(msg); await navegar(); };
  $$("[data-est-autorizar]").forEach(b => b.addEventListener("click", async () => {
    const a = await db.get("autorizacoes", b.dataset.estAutorizar);
    if (!a || a.situacao !== "pendente") return;
    await db.put("autorizacoes", { ...a, situacao: "autorizado", data: hojeISO(), perfil: estado.perfil || "" });
    const e = await db.get("eventos", id);
    const todas = await db.porIndice("autorizacoes", "evento_id", id);
    await estLog(id, "autorização concedida", `${a.cargo || "Nível " + a.nivel} · ${a.gestor}`);
    if (todas.every(x => x.situacao === "autorizado")){
      await estMudarStatus(e, "gabinete", { autorizado_em: hojeISO() });
      await estLog(id, "enviado ao Gabinete", "todas as autorizações da linha hierárquica foram concedidas");
      await recarregar("Autorizações completas. O evento seguiu para o Gabinete.");
    } else await recarregar("Autorização registrada.");
  }));
  $$("[data-est-devolver]").forEach(b => b.addEventListener("click", async () => {
    const a = await db.get("autorizacoes", b.dataset.estDevolver);
    if (!a || a.situacao !== "pendente") return;
    const e = await db.get("eventos", id);
    await db.put("autorizacoes", { ...a, situacao: "devolvido", data: hojeISO(), perfil: estado.perfil || "" });
    await estMudarStatus(e, "devolvido");
    await estLog(id, "devolvido à unidade", `${a.cargo || "Nível " + a.nivel} · ${a.gestor}`);
    await recarregar("Evento devolvido à unidade.");
  }));
  $("#formEstAjuste")?.addEventListener("submit", async ev => {
    ev.preventDefault();
    const e = await db.get("eventos", id), us = await db.list("unidades");
    const u = us.find(x => x.id_unidade === valorDe("estAjusteUnidade"));
    const d = {
      numero_sigadoc: valorDe("estAjusteNumero"), data_oficio: valorDe("estAjusteData"), unidade: valorDe("estAjusteUnidade"),
      unidade_nome: u ? u.nome : valorDe("estAjusteUnidade"), motivo: valorDe("estAjusteMotivo"),
      substituido: valorDe("estAjusteSubstituido"), cargo_substituido: valorDe("estAjusteCargoSubstituido"),
      substituto: valorDe("estAjusteSubstituto"), cargo_substituto: valorDe("estAjusteCargoSubstituto"),
      periodo_inicio: valorDe("estAjusteInicio"), periodo_fim: valorDe("estAjusteFim"), observacao: valorDe("estAjusteObservacao"),
    };
    const eventos = (await db.list("eventos")).filter(x => x.id_evento !== id);
    if (!mostrarErros("#estErrosAjuste", estValidar(d, eventos))) return;
    const auths = await db.porIndice("autorizacoes", "evento_id", id);
    for (const a of auths) await db.put("autorizacoes", { ...a, situacao: "pendente", data: null });
    await db.put("eventos", { ...e, ...d, status: "autorizacao" });
    await estLog(id, "evento ajustado pela unidade", `${d.substituto} · ${d.motivo} · ${d.periodo_inicio} a ${d.periodo_fim}`);
    await estLog(id, "reenviado para autorização", "a unidade ajustou o evento");
    await recarregar("Ajuste salvo. Evento reenviado para a autorização.");
  });
  $("#btnEstReenviar")?.addEventListener("click", async () => {
    const e = await db.get("eventos", id);
    const auths = await db.porIndice("autorizacoes", "evento_id", id);
    for (const a of auths) await db.put("autorizacoes", { ...a, situacao: "pendente", data: null });
    await estMudarStatus(e, "autorizacao");
    await estLog(id, "reenviado para autorização", "a unidade ajustou o evento");
    await recarregar("Evento reenviado para a autorização.");
  });
  $("#btnEstEnviarRh")?.addEventListener("click", async () => {
    const e = await db.get("eventos", id);
    await estMudarStatus(e, "analise_rh");
    await estLog(id, "encaminhado ao RH", "Gabinete de Direção → Gerência de Suporte à Gestão de Pessoas");
    await recarregar("Evento encaminhado ao RH.");
  });
  $("#formEstFicha")?.addEventListener("submit", async ev => {
    ev.preventDefault();
    const e = await db.get("eventos", id);
    const d = { numero_ficha: valorDe("estFichaNumero"), data: valorDe("estFichaData"), analista: valorDe("estFichaAnalista"), observacao: valorDe("estFichaObs") };
    const erros = [];
    if (!d.numero_ficha) erros.push("Informe o número da ficha.");
    if (!d.data) erros.push("Informe a data da ficha.");
    if (!d.analista) erros.push("Informe o analista responsável.");
    if (!mostrarErros("#estErrosFicha", erros)) return;
    await db.put("fichas", { id: uuid(), evento_id: id, ...d, criado_em: agora() });
    await estMudarStatus(e, "aguardando_assinatura", { ficha_em: d.data });
    await estLog(id, "ficha de solicitação incluída", `${d.numero_ficha} · ${d.analista}`);
    await estLog(id, "enviado para assinatura", "Diretor Geral Adjunto");
    await recarregar("Ficha incluída. O evento seguiu para assinatura.");
  });
  $("#formEstAssinar")?.addEventListener("submit", async ev => {
    ev.preventDefault();
    const e = await db.get("eventos", id);
    const ficha = (await db.porIndice("fichas", "evento_id", id))[0];
    const nome = valorDe("estAssNome"), cargo = valorDe("estAssCargo");
    const erros = [];
    if (!ficha) erros.push("A ficha de solicitação precisa estar incluída antes da assinatura (RN04).");
    if (!nome) erros.push("Informe o nome do signatário.");
    if (!cargo) erros.push("Informe o cargo do signatário.");
    if (!mostrarErros("#estErrosAssinar", erros)) return;
    await estMudarStatus(e, "assinado", { assinado_por: nome, assinado_cargo: cargo, assinado_em: hojeISO() });
    await estLog(id, "assinatura registrada", `${nome} · ${cargo}`);
    await recarregar("Assinatura registrada. O evento voltou ao RH para o envio à SESP.");
  });
  $("#btnEstEnviarSesp")?.addEventListener("click", async () => {
    const e = await db.get("eventos", id);
    if (!estEnvioNoPrazo(e)){ toast("Fora do prazo do dia 05 (RN06): registre o indeferimento.", 5000); return; }
    await estMudarStatus(e, "encaminhado_sesp", { envio_sesp_em: hojeISO() });
    await estLog(id, "encaminhado à SESP", `enviado em ${dataCurtaBR(hojeISO())}, dentro do prazo do dia 05`);
    await recarregar("Evento encaminhado à Superintendência de Gestão de Pessoas da SESP.");
  });
  $("#formEstPublicar")?.addEventListener("submit", async ev => {
    ev.preventDefault();
    const e = await db.get("eventos", id);
    const numero = valorDe("estPubNumero"), data = valorDe("estPubData");
    const erros = [];
    if (!numero) erros.push("Informe o número da publicação no Diário Oficial.");
    if (!data) erros.push("Informe a data da publicação.");
    if (!mostrarErros("#estErrosPublicar", erros)) return;
    await db.put("publicacoes", { id: uuid(), evento_id: id, numero_do: numero, data_publicacao: data, criado_em: agora() });
    await estMudarStatus(e, "publicado", { publicacao_numero: numero, publicacao_do: data, encerrado_em: data });
    await estLog(id, "publicação no Diário Oficial", `${numero} · ${dataCurtaBR(data)}`);
    await estLog(id, "evento encerrado", "encerrado com a publicação no Diário Oficial (RN07)");
    await recarregar("Publicação registrada. Evento encerrado.");
  });
  $("#formEstIndeferir")?.addEventListener("submit", async ev => {
    ev.preventDefault();
    const e = await db.get("eventos", id);
    const motivo = valorDe("estIndMotivo");
    if (!motivo){ mostrarErros("#estErrosIndeferir", ["Escolha o motivo do indeferimento."]); return; }
    await estMudarStatus(e, "indeferido", { indeferido_motivo: motivo, indeferido_em: hojeISO() });
    await estLog(id, "evento indeferido", motivo);
    await recarregar("Evento indeferido.");
  });
};

/* ---------- planilha de controle ---------- */
TELAS["#/planilha"] = async () => {
  const es = await db.list("eventos"), us = await estUnidades();
  const lista = es.slice().sort((a, b) => String(a.periodo_inicio).localeCompare(String(b.periodo_inicio)));
  const publicados = es.filter(e => e.status === "publicado").length;
  return `<h1>Planilha de controle</h1>
    <p class="sub">Os cinco campos obrigatórios do controle: substituído, substituto, motivo, período e publicação no Diário Oficial. ${publicados} de ${es.length} eventos publicados.</p>
    <div class="linha-botoes"><button class="prim" id="btnEstXlsx">Baixar planilha (.xlsx)</button><button class="sec" id="btnEstCsv">Exportar CSV</button><button class="sec" id="btnEstImprimir">Imprimir</button></div>
    <div class="card tabela-wrap"><table id="tabelaEstPlanilha"><tr><th>Processo</th><th>Substituído</th><th>Substituto</th><th>Motivo</th><th>Período</th><th>Publicação no DO</th><th>Situação</th><th>Unidade</th></tr>
      ${lista.map(e => `<tr><td><a href="#/evento/${encodeURIComponent(e.id_evento)}">${esc(e.numero_sigadoc)}</a></td>
        <td>${esc(e.substituido)}</td><td>${esc(e.substituto)}</td><td>${esc(e.motivo)}</td><td>${estPeriodo(e)}</td>
        <td>${e.publicacao_do ? `${esc(e.publicacao_numero || "")} · ${dataCurtaBR(e.publicacao_do)}` : "—"}</td>
        <td><span class="selo ${estStatusSelo(e.status)}">${esc(estStatusNome(e.status))}</span></td><td>${esc(estNomeUnidade(e, us))}</td></tr>`).join("")}</table></div>`;
};
TELAS_DEPOIS["#/planilha"] = () => {
  $("#btnEstXlsx")?.addEventListener("click", async () => {
    if (typeof XLSX === "undefined"){ toast("A biblioteca da planilha não carregou."); return; }
    const es = await db.list("eventos"), us = await estUnidades();
    const linhas = [["Processo SIGADOC", "Substituído", "Substituto", "Motivo", "Período inicial", "Período final", "Publicação no DO", "Situação", "Unidade"]];
    for (const e of es) linhas.push([e.numero_sigadoc, e.substituido, e.substituto, e.motivo, e.periodo_inicio, e.periodo_fim, e.publicacao_do || "", estStatusNome(e.status), estNomeUnidade(e, us)]);
    const ws = XLSX.utils.aoa_to_sheet(linhas);
    ws["!cols"] = [{ wch: 20 }, { wch: 24 }, { wch: 24 }, { wch: 30 }, { wch: 14 }, { wch: 14 }, { wch: 22 }, { wch: 26 }, { wch: 30 }];
    const wb = XLSX.utils.book_new();
    XLSX.utils.book_append_sheet(wb, ws, "Controle");
    const resumo = [["Situação", "Quantidade"], ...Object.keys(EST_STATUS).map(s => [estStatusNome(s), es.filter(e => e.status === s).length]),
      [], ["Regra", "Valor"], ["Prazo do envio à SESP", "dia 05 do mês em que a substituição ocorre"],
      ["Encerramento", "publicação no Diário Oficial"], ["Campos obrigatórios", "substituído, substituto, motivo, período e publicação no DO"]];
    const ws2 = XLSX.utils.aoa_to_sheet(resumo);
    ws2["!cols"] = [{ wch: 34 }, { wch: 52 }];
    XLSX.utils.book_append_sheet(wb, ws2, "Resumo");
    XLSX.writeFile(wb, "eventos-substituicao-" + hojeISO() + ".xlsx");
    await registrar("planilha .xlsx exportada");
  });
  $("#btnEstCsv")?.addEventListener("click", async () => {
    const es = await db.list("eventos"), us = await estUnidades();
    const linhas = [["Processo SIGADOC", "Substituído", "Substituto", "Motivo", "Período inicial", "Período final", "Publicação no DO", "Situação", "Unidade"]];
    for (const e of es) linhas.push([e.numero_sigadoc, e.substituido, e.substituto, e.motivo, e.periodo_inicio, e.periodo_fim, e.publicacao_do || "", estStatusNome(e.status), estNomeUnidade(e, us)]);
    const csv = "\ufeff" + linhas.map(l => l.map(v => `"${String(v ?? "").replace(/"/g, '""')}"`).join(";")).join("\r\n");
    baixar("eventos-substituicao-" + hojeISO() + ".csv", csv, "text/csv");
    await registrar("CSV da planilha de controle exportado");
  });
  $("#btnEstImprimir")?.addEventListener("click", () => window.print());
};

/* ---------- configuração ---------- */
TELAS["#/config"] = async () => {
  const us = await db.list("unidades");
  return `<h1>Configuração</h1>${await blocoConfigComum()}
    <div class="card tabela-wrap"><h2 style="margin-top:0">Unidades e chefias</h2>
      <p class="sub">Cada unidade define os níveis da autorização hierárquica. O evento novo copia esses níveis.</p>
      <table><tr><th>Unidade</th><th>Sigla</th><th>Chefia</th><th>Direção</th><th>Níveis</th></tr>
      ${us.map(u => `<tr><td>${esc(u.nome)}</td><td>${esc(u.sigla)}</td><td>${esc(u.chefia)}</td><td>${esc(u.diretor)}</td><td>${(u.niveis || []).length}</td></tr>`).join("")}</table></div>
    <div class="card"><h2 style="margin-top:0">Motivos válidos (RN01)</h2><ul>${EST_MOTIVOS.map(m => `<li>${esc(m)}</li>`).join("")}</ul></div>`;
};
TELAS_DEPOIS["#/config"] = () => ligarConfigComum();
