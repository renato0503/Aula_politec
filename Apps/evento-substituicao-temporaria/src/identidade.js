/* Identidade do Evento de Substituição Temporária.
   Entra por último no build. A tela-assinatura é a "Minha fila" em trilho: o
   que espera cada perfil, com a etapa do processo e o prazo do dia 05. O painel
   recebe a mesma fila em resumo. */

function estRegraFila(perfil){
  return {
    unidade: { titulo: "Devolvidos para ajuste", texto: "Eventos que a linha hierárquica devolveu e esperam o ajuste da unidade.", filtra: e => e.status === "devolvido" },
    hierarquia: { titulo: "Aguardando autorização", texto: "Eventos que precisam da autorização de cada nível da linha hierárquica (RN03).", filtra: e => e.status === "autorizacao" },
    gabinete: { titulo: "No Gabinete de Direção", texto: "Eventos já autorizados que o Gabinete encaminha à Gerência de Suporte à Gestão de Pessoas.", filtra: e => e.status === "gabinete" },
    rh: { titulo: "Com a Gerência de Suporte à Gestão de Pessoas", texto: "Eventos para analisar e incluir a ficha, enviar à SESP ou registrar a publicação no DO.", filtra: e => ["analise_rh", "assinado", "encaminhado_sesp"].includes(e.status) },
    diretor: { titulo: "Aguardando assinatura", texto: "Eventos com a ficha de RH pronta que esperam a assinatura do Diretor Geral Adjunto.", filtra: e => e.status === "aguardando_assinatura" },
  }[perfil] || { titulo: "Minha fila", texto: "Eventos que esperam uma ação.", filtra: () => false };
}

async function estDadosFila(){
  const es = await db.list("eventos"), us = await estUnidades(), hoje = hojeISO();
  const regra = estRegraFila(estado.perfil);
  const lista = es.filter(regra.filtra).map(e => ({ e, pr: estPrazo(e, hoje) }))
    .sort((a, b) => String(a.pr.limite).localeCompare(String(b.pr.limite)));
  return { regra, lista, us };
}

function estCartaoFila(x){
  const e = x.e, pr = x.pr;
  return `<a class="est-fila-card" href="#/evento/${encodeURIComponent(e.id_evento)}">
    <span class="est-fila-topo"><span class="mono">${esc(e.numero_sigadoc)}</span>
      <span class="selo ${estStatusSelo(e.status)}">${esc(estStatusNome(e.status))}</span></span>
    <b>${esc(e.substituido)} → ${esc(e.substituto)}</b>
    <span class="sub">${esc(e.motivo)} · ${estPeriodo(e)} · ${esc(e.unidade_nome || e.unidade || "")}</span>
    <span class="est-fila-rodape"><span class="selo ${EST_PRAZO_SELO[pr.situacao]}">${esc(estPrazoNome(pr.situacao))}</span>
      <small class="sub">limite ${dataCurtaBR(pr.limite)}</small></span></a>`;
}

async function estFilaResumo(){
  const { regra, lista } = await estDadosFila();
  const primeiros = lista.slice(0, 4);
  return `<div class="card est-fila-resumo">
    <div class="est-fila-cabeca"><div><span class="sub">Minha fila</span><h2>${esc(regra.titulo)} <span class="conta">${lista.length}</span></h2></div>
      <a class="botao" href="#/fila">Abrir a fila</a></div>
    <p class="sub">${esc(regra.texto)}</p>
    ${primeiros.length ? `<div class="est-fila-grade">${primeiros.map(estCartaoFila).join("")}</div>` : '<p class="sub">Nada esperando este perfil agora.</p>'}
  </div>`;
}

TELAS["#/fila"] = async () => {
  const { regra, lista } = await estDadosFila();
  const p = (APP.perfis || []).find(x => x.id === estado.perfil);
  return `<h1>Minha fila <span class="est-role">${esc(p ? p.nome : "")}</span></h1>
    <p class="sub"><b>${esc(regra.titulo)}.</b> ${esc(regra.texto)}</p>
    ${estTrilho({ status: lista[0] ? lista[0].e.status : "autorizacao" })}
    ${lista.length ? `<div class="est-fila-grade">${lista.map(estCartaoFila).join("")}</div>`
      : '<div class="card vazio">Nada esperando este perfil agora. <a href="#/eventos">Ver todos os eventos</a></div>'}
    <div class="card"><h2 style="margin-top:0">O caminho do evento</h2>
      <ol class="est-caminho">${EST_ETAPAS.map(([nome, quem], i) => `<li><b>${i + 1}. ${esc(nome)}</b><span class="sub">${esc(quem)}</span></li>`).join("")}</ol>
      <p class="sub">O envio à SESP precisa acontecer até o dia 05 do mês em que a substituição ocorre. Depois dessa data, o evento é indeferido (RN06). O encerramento só acontece com a publicação no Diário Oficial (RN07).</p></div>`;
};

/* painel: a fila do perfil entra no alto, antes dos indicadores */
const estPainelAntes = TELAS["#/painel"];
TELAS["#/painel"] = async () => {
  const html = await estPainelAntes();
  const doc = new DOMParser().parseFromString(`<div id="estRaiz">${html}</div>`, "text/html");
  const raiz = doc.getElementById("estRaiz");
  if (!raiz) return html;
  const caixa = doc.createElement("div");
  caixa.innerHTML = await estFilaResumo();
  const h1 = raiz.querySelector("h1");
  if (h1) h1.after(caixa.firstElementChild);
  return raiz.innerHTML;
};
