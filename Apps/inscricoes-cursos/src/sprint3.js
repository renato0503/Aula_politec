/* ================= Sprint 3 · Formulário de inscrição (RN01, RN02, RN04) ================= */
const DOMINIO = "@politec.mt.gov.br";
// mensagem ao lado do campo
function erroCampo(id, msg){
  const el = $("#" + id); if (!el) return;
  let s = $("#erro-" + id);
  if (!s){ s = document.createElement("small"); s.id = "erro-" + id; s.className = "erro-txt"; s.setAttribute("role", "alert"); el.after(s); }
  s.textContent = msg || ""; el.setAttribute("aria-invalid", msg ? "true" : "false");
  return !msg;
}
// RN04: só dentro do período de inscrição do curso
function periodoAberto(c, hoje = hojeISO()){ return (!c.ii || hoje >= c.ii) && (!c.if || hoje <= c.if); }
teste("RN04: fora do período fecha a inscrição", ()=> periodoAberto({ii: "2026-11-01", if: "2026-11-10"}, "2026-11-05") && !periodoAberto({ii: "2026-11-01", if: "2026-11-10"}, "2026-11-11"));
// mesmo cálculo do gerador Python: protocolo = fnv1a(curso|matrícula|quando), 8 caracteres
const protocoloInscricao = (curso, matricula, quando)=> fnv1a(`${curso}|${matricula}|${quando}`).slice(0, 8).toUpperCase();
teste("protocolo igual ao do gerador Python", ()=> protocoloInscricao("CURSO-2026-11", "200000", "2026-10-29T08:00:00-04:00") === "1FEF59EC");

TELAS["#/inscricao"] = async ()=>{
  const r = lerCursoDoLink(location.hash);
  if (r.erro) return `<div class="card pendente"><h1>Inscrição</h1><p>${esc(r.erro)}</p></div>`;
  const c = r.curso; estado.cursoLink = c;
  const topo = `<h1>Inscrição · ${esc(c.nome)}</h1>
    <div class="card"><p><b>Período:</b> ${dataCurtaBR(c.ini)} a ${dataCurtaBR(c.fim)} · <b>Carga horária:</b> ${esc(c.ch)} h · <b>Local:</b> ${esc(c.local)}</p>
      <p><b>Inscrições:</b> ${dataCurtaBR(c.ii)} a ${dataCurtaBR(c.if)}</p></div>`;
  if (!periodoAberto(c)) return topo + `<div class="card pendente" id="foraPeriodo"><b>Inscrições fechadas.</b> O período é de ${dataCurtaBR(c.ii)} a ${dataCurtaBR(c.if)} (RN04).</div>`;
  return topo + `<form class="card" id="formInscricao" novalidate><h2 style="margin-top:0">Seus dados</h2><div class="campos">
      ${campo("iMatricula", "Matrícula", {obrigatorio: true, attrs: 'inputmode="numeric" autocomplete="off"'})}
      ${campo("iNome", "Nome completo", {obrigatorio: true, attrs: 'autocomplete="name"'})}
      ${campo("iLotacao", "Lotação", {obrigatorio: true})}
      ${campo("iDiretoria", "Diretoria", {tipo: "select", opcoes: [["", "Escolha"], ...c.dirs], obrigatorio: true})}
      ${campo("iEmail", "E-mail institucional", {tipo: "email", obrigatorio: true, attrs: `placeholder="nome${DOMINIO}" autocomplete="email"`})}
      ${campo("iTelefone", "Telefone (opcional)", {tipo: "tel", attrs: 'autocomplete="tel"'})}</div>
    ${c.pre.length ? `<h2>Pré-requisitos</h2>${c.pre.map((p, i)=>`<fieldset style="border:0;padding:0;margin:8px 0"><legend>${esc(p)}</legend>
      <label style="display:inline-flex;gap:6px;margin-right:16px"><input type="radio" name="pre${i}" value="sim" style="width:auto"> Atendo</label>
      <label style="display:inline-flex;gap:6px"><input type="radio" name="pre${i}" value="nao" style="width:auto"> Não atendo</label></fieldset>`).join("")}` : ""}
    <p class="sub">Seus dados vão só para a Gerência de Formação e para a sua diretoria, para a seleção. Eles são apagados 30 dias depois do fim do curso.</p>
    <div class="linha-botoes"><button class="prim" type="submit">Enviar inscrição</button></div></form><div id="comprovante"></div>`;
};
TELAS_DEPOIS["#/inscricao"] = ()=>{
  const form = $("#formInscricao"); if (!form) return;
  const c = estado.cursoLink;
  const validar = ()=>{
    const ok = [
      erroCampo("iMatricula", /^\d{4,}$/.test(valorDe("iMatricula")) ? "" : "Matrícula só com números (RN01)."),
      erroCampo("iNome", valorDe("iNome").split(/\s+/).length >= 2 ? "" : "Informe o nome completo (RN01)."),
      erroCampo("iLotacao", valorDe("iLotacao") ? "" : "Informe a lotação (RN01)."),
      erroCampo("iDiretoria", valorDe("iDiretoria") ? "" : "Escolha a diretoria (RN01)."),
      erroCampo("iEmail", valorDe("iEmail").toLowerCase().endsWith(DOMINIO) && /^\S+@\S+$/.test(valorDe("iEmail")) ? "" : `Use o e-mail institucional (${DOMINIO}) (RN02).`),
      erroCampo("iTelefone", !valorDe("iTelefone") || valorDe("iTelefone").replace(/\D/g, "").length >= 10 ? "" : "Telefone com DDD.")
    ];
    const semResposta = c.pre.filter((_, i)=>!$(`input[name=pre${i}]:checked`));
    if (semResposta.length) toast("Responda a todos os pré-requisitos.");
    return ok.every(Boolean) && !semResposta.length;
  };
  ["iMatricula", "iNome", "iLotacao", "iDiretoria", "iEmail", "iTelefone"].forEach(id=>$("#" + id).addEventListener("blur", e=>{
    // indo para o botão de envio, o submit já valida; validar aqui move o botão e o clique se perde
    if (e.relatedTarget && e.relatedTarget.type === "submit") return;
    if ($("#erro-" + id)) validar(); }));
  form.addEventListener("submit", e=>{
    e.preventDefault();
    if (!validar()) return;
    const quando = new Date().toISOString(), matricula = valorDe("iMatricula");
    const dados = {p: protocoloInscricao(c.id, matricula, quando), c: c.id, m: matricula, n: valorDe("iNome"), l: valorDe("iLotacao"),
      d: valorDe("iDiretoria"), e: valorDe("iEmail").toLowerCase(), t: valorDe("iTelefone"),
      r: c.pre.filter((_, i)=>$(`input[name=pre${i}]:checked`).value === "sim"), s: quando};
    const bloco = blocoInscricao.gerar(dados);
    const assunto = `[INSCRICAO] ${c.nome} ${dados.p}`;
    const corpo = `Inscrição no curso ${c.nome}\nNome: ${dados.n}\nMatrícula: ${dados.m}\nDiretoria: ${dados.d}\nProtocolo: ${dados.p}\n\nNão altere o bloco abaixo; ele é lido pela Gerência de Formação.\n\n${bloco}\n`;
    form.remove();
    $("#comprovante").innerHTML = `<div class="card" id="cardComprovante"><h2 style="margin-top:0">Inscrição registrada</h2>
      <p>Protocolo: <b class="mono" id="protInscricao">${dados.p}</b> · Situação: <span class="selo info">em análise</span></p>
      <p>Curso: <b>${esc(c.nome)}</b> (${dataCurtaBR(c.ini)} a ${dataCurtaBR(c.fim)})</p>
      <p><b>Falta um passo:</b> envie o e-mail de inscrição para a Gerência de Formação. Sem o e-mail, a inscrição não chega.</p>
      <ol><li>Clique em "Enviar e-mail de inscrição" e confirme o envio no seu e-mail.</li>
        <li>A sua diretoria faz a seleção até o prazo da triagem.</li><li>O resultado chega no seu e-mail institucional.</li></ol>
      <div class="linha-botoes nao-imprimir"><a class="botao prim" id="lnkEmail" href="mailto:${encodeURIComponent(c.email)}?subject=${encodeURIComponent(assunto)}&body=${encodeURIComponent(corpo)}">Enviar e-mail de inscrição</a>
        <button id="btnCopiarBloco">Copiar o texto do e-mail</button><button onclick="window.print()">Imprimir comprovante</button></div>
      <details class="nao-imprimir"><summary>Se o e-mail não abrir</summary><p>Copie o texto, cole num e-mail novo para <b>${esc(c.email)}</b> com o assunto <span class="mono">${esc(assunto)}</span>.</p>
        <textarea id="textoEmail" rows="6" readonly>${esc(corpo)}</textarea></details></div>`;
    $("#btnCopiarBloco").addEventListener("click", async ()=>{ try { await navigator.clipboard.writeText(corpo); toast("Texto copiado."); } catch(err){ $("#textoEmail").select(); toast("Use Ctrl+C."); } });
  });
};
