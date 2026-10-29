/**
 * Agendamento CIN · servidor (Google Apps Script)
 *
 * Serve o index.html (HtmlService) e lê e grava na planilha. As funções públicas
 * aqui são as mesmas que o index.html imita no modo local (const api = ... em
 * src/app.js). Ao criar uma função nova, crie as duas.
 *
 * Abas da planilha: postos, horarios, agendamentos, usuarios, log
 * (modelo em planilha-modelo/*.csv).
 *
 * Sprint 1: doGet, listarPostos, listarHorarios, quemSou.
 * Sprint 2: listarTodosPostos, salvarPosto, listarHorariosPosto, gerarHorarios, bloquear.
 * Testes sem a conta Google: node testes/testar_code_gs.js
 */

function doGet() {
  return HtmlService.createHtmlOutputFromFile('index')
    .setTitle('Agendamento CIN')
    .addMetaTag('viewport', 'width=device-width, initial-scale=1');
}

/* ---------------- planilha ---------------- */

/** A planilha vem da propriedade PLANILHA_ID (os dois projetos usam a mesma). Sem ela, a planilha ligada ao script. */
function planilha_() {
  const id = PropertiesService.getScriptProperties().getProperty('PLANILHA_ID');
  return id ? SpreadsheetApp.openById(id) : SpreadsheetApp.getActive();
}

function aba_(nome) {
  const aba = planilha_().getSheetByName(nome);
  if (!aba) throw new Error('Aba não encontrada: ' + nome);
  return aba;
}

/** Lê uma aba como lista de objetos, usando a primeira linha como cabeçalho. */
function lerAba_(nome) {
  const valores = aba_(nome).getDataRange().getValues();
  const cab = valores.shift();
  return valores
    .filter(function (l) { return l.join('') !== ''; })
    .map(function (l) {
      const o = {};
      cab.forEach(function (c, i) { o[c] = l[i] instanceof Date ? formatarData_(l[i], c) : l[i]; });
      return o;
    });
}

/** Acrescenta objetos no fim da aba, na ordem do cabeçalho. */
function acrescentar_(nome, objs) {
  if (!objs.length) return;
  const aba = aba_(nome);
  const cab = aba.getDataRange().getValues()[0];
  const linhas = objs.map(function (o) { return cab.map(function (c) { return o[c] === undefined || o[c] === null ? '' : o[c]; }); });
  aba.getRange(aba.getLastRow() + 1, 1, linhas.length, cab.length).setValues(linhas);
}

/** Muda campos da linha cuja coluna `chave` vale `id`. Devolve se achou. */
function atualizar_(nome, chave, id, mudancas) {
  const aba = aba_(nome);
  const v = aba.getDataRange().getValues(), cab = v[0], k = cab.indexOf(chave);
  for (var i = 1; i < v.length; i++) {
    if (String(v[i][k]) === String(id)) {
      Object.keys(mudancas).forEach(function (c) {
        const j = cab.indexOf(c);
        if (j >= 0) aba.getRange(i + 1, j + 1).setValue(mudancas[c]);
      });
      return true;
    }
  }
  return false;
}

function formatarData_(d, coluna) {
  const fuso = Session.getScriptTimeZone();
  if (coluna === 'data') return Utilities.formatDate(d, fuso, 'yyyy-MM-dd');
  if (coluna === 'hora') return Utilities.formatDate(d, fuso, 'HH:mm');
  return Utilities.formatDate(d, fuso, "yyyy-MM-dd'T'HH:mm:ssXXX");
}

function ativo_(v) { return v === true || String(v).toUpperCase() === 'TRUE'; }

function registrarLog_(acao, detalhe) {
  acrescentar_('log', [{ id: Utilities.getUuid(), data_hora: new Date().toISOString(), usuario: quemSou().email, acao: acao, protocolo: '', detalhe: detalhe }]);
}

/* ---------------- quem está usando ---------------- */

/**
 * Compara o e-mail da conta Google com a aba usuarios.
 * Devolve perfil null para o cidadão (sem login) e para quem não está cadastrado.
 * Só funciona na implantação interna (executar como o usuário que acessa); na
 * implantação pública o e-mail vem vazio. Ver DEPLOY.md.
 */
function quemSou() {
  const email = (Session.getActiveUser().getEmail() || '').toLowerCase();
  if (!email) return { email: '', perfil: null, posto_id: null };
  const u = lerAba_('usuarios').filter(function (x) { return String(x.email).toLowerCase() === email && ativo_(x.ativo); })[0];
  return u ? { email: email, perfil: u.perfil, posto_id: u.posto_id || null } : { email: email, perfil: null, posto_id: null };
}

/** RN05: o posto só mexe na própria agenda; a gestão mexe em todas. */
function exigirPosto_(postoId) {
  const eu = quemSou();
  if (eu.perfil === 'gestao') return eu;
  if (eu.perfil !== 'posto' || eu.posto_id !== postoId) throw new Error('Sem permissão para o posto ' + postoId + ' (RN05).');
  return eu;
}

function exigirGestao_() {
  const eu = quemSou();
  if (eu.perfil !== 'gestao') throw new Error('Só a gestão cadastra postos.');
  return eu;
}

/* ---------------- público ---------------- */

/** RN01: só postos ativos. */
function listarPostos() {
  return lerAba_('postos').filter(function (p) { return ativo_(p.ativo); });
}

/** RN02 (parcial): horários abertos do posto. A conferência de vaga entra no Sprint 3. */
function listarHorarios(postoId) {
  return lerAba_('horarios').filter(function (h) { return h.posto_id === postoId && h.situacao === 'aberto'; });
}

/* ---------------- Sprint 2: postos e horários ---------------- */

function listarTodosPostos() {
  exigirGestao_();
  return lerAba_('postos');
}

function salvarPosto(p) {
  exigirGestao_();
  if (!p.posto_id || !p.nome || !p.municipio) throw new Error('Informe código, nome e município do posto.');
  const campos = { nome: p.nome, municipio: p.municipio, endereco: p.endereco || '', email: p.email || '', ativo: !!p.ativo, documentos_orientacao: p.documentos_orientacao || '' };
  if (!atualizar_('postos', 'posto_id', p.posto_id, campos)) acrescentar_('postos', [Object.assign({ posto_id: p.posto_id }, campos)]);
  registrarLog_('posto salvo', p.posto_id);
  return true;
}

function listarHorariosPosto(postoId, de, ate) {
  exigirPosto_(postoId);
  return lerAba_('horarios')
    .filter(function (h) { return h.posto_id === postoId && h.data >= de && h.data <= ate; })
    .sort(function (a, b) { return (a.data + a.hora) < (b.data + b.hora) ? -1 : 1; });
}

/** A mesma regra de horariosDaGrade() do index.html. */
function horariosDaGrade_(postoId, g) {
  const out = [], i = g.inicio.split(':').map(Number), f = g.fim.split(':').map(Number);
  const p = g.de.split('-').map(Number);
  for (var t = Date.UTC(p[0], p[1] - 1, p[2]); ; t += 86400000) {
    const d = new Date(t), data = d.toISOString().slice(0, 10);
    if (data > g.ate) break;
    if (g.dias.indexOf(d.getUTCDay()) < 0) continue;
    for (var m = i[0] * 60 + i[1]; m < f[0] * 60 + f[1]; m += g.intervalo) {
      const hora = ('0' + Math.floor(m / 60)).slice(-2) + ':' + ('0' + (m % 60)).slice(-2);
      out.push({ horario_id: postoId + '-' + data + '-' + hora.replace(':', ''), posto_id: postoId, data: data, hora: hora, capacidade: g.vagas, ocupadas: 0, situacao: 'aberto' });
    }
  }
  return out;
}

/** Gera os horários do período sem duplicar os que já existem. */
function gerarHorarios(postoId, grade) {
  exigirPosto_(postoId);
  const trava = LockService.getScriptLock();
  trava.waitLock(20000);
  try {
    const existentes = {};
    lerAba_('horarios').forEach(function (h) { existentes[h.horario_id] = true; });
    const novos = horariosDaGrade_(postoId, grade).filter(function (h) { return !existentes[h.horario_id]; });
    acrescentar_('horarios', novos);
    registrarLog_('horários gerados', postoId + ': ' + novos.length + ' novos');
    return { criados: novos.length, existentes: horariosDaGrade_(postoId, grade).length - novos.length };
  } finally {
    trava.releaseLock();
  }
}

/** Bloqueia (ou libera) um horário ({horario_id}) ou um dia inteiro ({data}). */
function bloquear(postoId, alvo, bloquearSim) {
  exigirPosto_(postoId);
  const situacao = bloquearSim ? 'bloqueado' : 'aberto';
  const alvos = lerAba_('horarios').filter(function (h) {
    return h.posto_id === postoId && (alvo.horario_id ? h.horario_id === alvo.horario_id : h.data === alvo.data);
  });
  alvos.forEach(function (h) { atualizar_('horarios', 'horario_id', h.horario_id, { situacao: situacao }); });
  registrarLog_(bloquearSim ? 'bloqueio' : 'desbloqueio', alvo.horario_id || (postoId + ' ' + alvo.data));
  return alvos.length;
}

/* ---------------- Sprint 3: agendamento do cidadão ---------------- */

function hoje_() { return Utilities.formatDate(new Date(), Session.getScriptTimeZone(), 'yyyy-MM-dd'); }
function somarDias_(iso, n) { const p = iso.split('-').map(Number); return new Date(Date.UTC(p[0], p[1] - 1, p[2]) + n * 86400000).toISOString().slice(0, 10); }
/** RN09: de 1 a 30 dias de antecedência. */
function dentroDaJanela_(data) { const h = hoje_(); return data >= somarDias_(h, 1) && data <= somarDias_(h, 30); }

/** RN02: horários abertos, com vaga e dentro da janela. */
function listarVagas(postoId) {
  return lerAba_('horarios')
    .filter(function (h) { return h.posto_id === postoId && h.situacao === 'aberto' && Number(h.ocupadas) < Number(h.capacidade) && dentroDaJanela_(h.data); })
    .sort(function (a, b) { return (a.data + a.hora) < (b.data + b.hora) ? -1 : 1; });
}

function novoProtocolo_() {
  const letras = 'ABCDEFGHJKLMNPQRSTUVWXYZ23456789';
  var s = 'CIN-';
  for (var i = 0; i < 6; i++) s += letras.charAt(Math.floor(Math.random() * letras.length));
  return s;
}

/** RN03 e RN04. O cidadão só manda nome, contato e o horário; o CPF fica com os 4 últimos dígitos. */
function reservar(d) {
  const h = lerAba_('horarios').filter(function (x) { return x.horario_id === d.horario_id; })[0];
  if (!h || h.situacao !== 'aberto' || !dentroDaJanela_(h.data)) throw new Error('Este horário não está disponível.');
  if (Number(h.ocupadas) >= Number(h.capacidade)) throw new Error('Este horário acabou de ser preenchido. Escolha outro.');
  const usados = {};
  lerAba_('agendamentos').forEach(function (a) { usados[a.protocolo] = true; });
  var protocolo; do { protocolo = novoProtocolo_(); } while (usados[protocolo]);
  atualizar_('horarios', 'horario_id', h.horario_id, { ocupadas: Number(h.ocupadas) + 1 });
  acrescentar_('agendamentos', [{ protocolo: protocolo, posto_id: h.posto_id, horario_id: h.horario_id, nome: d.nome, telefone: d.telefone || '', email: d.email || '',
    cpf_final4: d.cpf ? String(d.cpf).slice(-4) : '', status: 'confirmado', criado_em: new Date().toISOString(), cancelado_em: '', compareceu_em: '' }]);
  return { protocolo: protocolo };
}

/** Só o necessário para o comprovante (sem telefone, e-mail ou CPF). */
function comprovante(protocolo) {
  const a = lerAba_('agendamentos').filter(function (x) { return x.protocolo === protocolo; })[0];
  if (!a) return null;
  const h = lerAba_('horarios').filter(function (x) { return x.horario_id === a.horario_id; })[0] || {};
  const p = lerAba_('postos').filter(function (x) { return x.posto_id === a.posto_id; })[0] || {};
  return { protocolo: protocolo, primeiro_nome: String(a.nome).split(' ')[0], data: h.data, hora: h.hora, status: a.status, posto: p.nome, endereco: p.endereco, documentos: p.documentos_orientacao };
}
