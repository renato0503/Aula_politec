# Mapa de Distribuição · como usar

O app monta o mapa de distribuição por credor a partir da planilha do processo:
lê grupos, itens e órgãos, aplica o resultado do pregoeiro, distribui a
dotação e gera o Excel final. É um arquivo só (`index.html`), funciona sem
internet e guarda os dados apenas no navegador deste computador.

## Abrir

1. Dê dois cliques em `index.html` (Edge ou Chrome).
2. Para testar, importe `exemplos/mapa-exemplo.xlsx` (dados fictícios).

## Montar o mapa de um processo

1. **Importar**: escolha a planilha (.xlsx ou .xls) ou baixe o modelo em
   branco, preencha e importe. Confira a prévia e salve.
2. **Relatório do pregoeiro**: carregue o PDF para preencher vencedor,
   fracassado e deserto de cada grupo.
3. **Mapa por item**: confira grupo, item, quantidade e valor por órgão.
4. **Apuração por empresa**: veja o total de cada empresa por órgão.
5. **Dotação orçamentária**: informe a dotação por grupo ou por item e os
   lançamentos por exercício.
6. **Conferência**: resolva o que aparece em vermelho.
7. **Exportar**: baixe o Excel completo ou a planilha de entrada.
8. **Backup**: exporte o `.json` do processo ou de todos.

## O que não fazer

- Não use dado pessoal nos arquivos de entrada. O mapa trata empresa, órgão e
  valor, e não pessoa.
- Não limpe os dados do navegador sem antes exportar o backup.
- Não edite o `index.html`: ele é gerado pelo `construir.py` a partir de
  `src/mapa.html`.
