// ============================================================
// GOOGLE APPS SCRIPT — Prova de Nivelamento POLITEC/MT
// ============================================================

var PLANILHA_ID = '1jkRd70Ph0K4fbR_59yw0IqlfvAOaqvlsn_fQmUEgzhk';
var NOME_ABA = 'Respostas';

function doPost(e) {
  return salvarResposta(JSON.parse(e.postData.contents));
}

function doGet() {
  return ContentService
    .createTextOutput(JSON.stringify({ status: 'ok', msg: 'API ativa' }))
    .setMimeType(ContentService.MimeType.JSON);
}

function salvarResposta(dados) {
  var ss = SpreadsheetApp.openById(PLANILHA_ID);
  var aba = ss.getSheetByName(NOME_ABA);

  if (!aba) {
    aba = ss.insertSheet(NOME_ABA);
    criarCabecalho(aba);
  }

  var linha = [];
  linha.push(dados.data || new Date().toLocaleString('pt-BR'));
  linha.push(dados.nome || '');
  linha.push(dados.email || '');
  linha.push(dados.pontuacao || 0);

  for (var i = 1; i <= 50; i++) {
    linha.push(dados.respostas['p' + i] || '-');
  }

  linha.push(calcularNivel(dados.pontuacao || 0));

  aba.appendRow(linha);

  return ContentService
    .createTextOutput(JSON.stringify({ status: 'ok' }))
    .setMimeType(ContentService.MimeType.JSON);
}

function criarCabecalho(aba) {
  var cabecalho = [
    'Data/Hora',
    'Nome',
    'E-mail',
    'Pontuacao'
  ];
  for (var i = 1; i <= 50; i++) {
    cabecalho.push('P' + i);
  }
  cabecalho.push('Nivel');
  aba.appendRow(cabecalho);

  var range = aba.getRange(1, 1, 1, cabecalho.length);
  range.setFontWeight('bold');
  range.setBackground('#12507f');
  range.setFontColor('#ffffff');
  aba.setFrozenRows(1);
}

function calcularNivel(pontos) {
  if (pontos <= 12) return 'INICIANTE';
  if (pontos <= 18) return 'BASICO';
  if (pontos <= 24) return 'INTERMEDIARIO';
  if (pontos <= 38) return 'AVANCADO';
  return 'EXPERT';
}

function testar() {
  var dadosExemplo = {
    nome: 'Teste Servidor',
    email: 'teste@politec.mt.gov.br',
    pontuacao: 38,
    data: new Date().toLocaleString('pt-BR'),
    respostas: {}
  };
  for (var i = 1; i <= 50; i++) {
    dadosExemplo.respostas['p' + i] = 'C';
  }
  salvarResposta(dadosExemplo);
  Logger.log('Teste concluido! Verifique sua planilha.');
}
