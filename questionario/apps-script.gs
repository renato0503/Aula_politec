// ============================================================
// GOOGLE APPS SCRIPT — Prova de Nivelamento POLITEC/MT
// ============================================================
// INSTRUCOES DE SETUP (veja o README.md da pasta questionario)
// ============================================================

// CONFIGURACAO: Cole aqui o ID da sua planilha Google
// Para obter: abra a planilha > o ID esta na URL entre /d/ e /edit
// Exemplo: https://docs.google.com/spreadsheets/d/1A2B3C4D5E6F.../edit
// O ID e: 1A2B3C4D5E6F...
var PLANILHA_ID = 'SEU_PLANILHA_ID_AQUI';

// Nome da aba onde os dados serao salvos (criada automaticamente se nao existir)
var NOME_ABA = 'Respostas';

function doPost(e) {
  return salvarResposta(JSON.parse(e.postData.contents));
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

  // Colunas das 50 respostas (D a BA)
  for (var i = 1; i <= 50; i++) {
    linha.push(dados.respostas['p' + i] || '-');
  }

  // Coluna extra: nivel
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

  // Formatacao do cabecalho
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

// Funcao de teste — rode esta funao manualmente para verificar se tudo funciona
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

// ============================================================
// PASSO A PASSO DE DEPLOY (para referencia)
// ============================================================
// 1. Abra a planilha Google Sheets > menu Extensoes > Apps Script
// 2. Cole este codigo (substitua PLANILHA_ID pelo ID da sua planilha)
// 3. Salve o projeto (Ctrl+S)
// 4. Clique em + ao lado de "Arquivos" > "Modulo" para adicionar,
//    ou simplemente substitua o codigo do arquivo Code.gs padrao
// 5. Clique em "Implantar" > "Nova implantacao"
// 6. Em "Tipo", escolha "App da Web"
// 7. Descricao: "Prova de Nivelamento POLITEC"
// 8. "Quem pode acessar": "Anyone" (qualquer pessoa)
// 9. Clique em "Implantar"
// 10. Copie a URL gerada (comeca com https://script.google.com/macros/s/...)
// 11. Cole essa URL no arquivo questionario/index.html
//     na variavel GScriptUrl (linha ~290 do JS)
