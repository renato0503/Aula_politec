# Mapa de Distribuição · como usar

O app monta o mapa de distribuição por credor de um processo de compra: junta a
distribuição por órgão, o resultado do pregoeiro e a dotação, confere as
divergências e gera o Excel final. É um arquivo só (`index.html`), funciona sem
internet e guarda os dados apenas no navegador deste computador.

## Abrir

1. Dê dois cliques em `index.html` (Edge ou Chrome).
2. Para conhecer o app, abra **Configuração** e carregue os dados fictícios.

## Montar o mapa de um processo

1. **Processos**: crie o processo ou abra um da lista.
2. **Importar**: carregue a distribuição por órgão, o relatório do pregoeiro e
   a dotação orçamentária.
3. **Mapa por item**: confira grupo, item, quantidade e estimado por órgão.
4. **Resultado**: veja a situação de cada grupo (homologado, fracassado ou
   deserto) e o homologado por órgão.
5. **Empresas** e **Conferência**: confira a tabela por empresa e resolva as
   divergências D01 a D07 apontadas pelo app.
6. **Orçamentária**: confira a distribuição por credor e órgão, no ano corrente
   e no seguinte.
7. **Exportar**: baixe o Excel com 8 abas e imprima o relatório de divergências.
8. **Auditoria**: cada importação, edição e validação fica registrada.

## Backup

Os dados ficam só neste navegador. Por isso, depois de cada processo, abra
**Configuração** e clique em **Exportar backup (.json)**.

## O que não fazer

- Não use dado pessoal nos arquivos de entrada. O mapa trata empresa, órgão e
  valor, e não pessoa.
- Não limpe os dados do navegador sem antes exportar o backup.
- Não edite o `index.html`: ele é gerado pelo `construir.py`.
