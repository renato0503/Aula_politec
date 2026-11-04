# Feedback dos alunos · Metas pelo BI

Gerado por `python Apps/_base/baixar_feedback.py` em 04/11/2026, a partir da coleção `feedback_apps` do Firestore.
2 resposta(s) · nota média 3,0 de 5

Use este arquivo para abrir o próximo sprint: cada item vira uma linha do `sprint.md`. Os números com fonte são da própria resposta.

## Resumo

- Usaria no trabalho: sim, com ajustes (2)
- Piloto: talvez (1); sim (1)

## Prioridades (na ordem de cada pessoa)

- [ ] Selecionar o mês _(Karine Assunção, 1ª)_
- [ ] Fazer a leitura correta dos dados do PDF _(Karine Assunção, 1ª)_
- [ ] Filtro da Gerência _(Karine Assunção, 2ª)_
- [ ] Inserir os filtros conforme o organograma _(Karine Assunção, 2ª)_
- [ ] Extração dos dados na aba conferir _(Karine Assunção, 3ª)_

## Tela por tela

### Importar o mês (`#/importar`)

Situação: não funciona ou deu erro (2)

- [ ] Não é possível selecionar o mês antes de exportar o arquivo.
Inserir a um filtro suspenso para identificar a gerência que o arquivo pertence, _(Karine Assunção)_
- [ ] 1. Seria possível inserir os filtros Diretoria (DIRETORIA DE CRIMINALÍSTICA, DIRETORIA DE MEDICINA LEGAL, DIRETORIA DE LABORATÓRIO FORENSE, DIRETORIA DE IDENTIFICAÇÃO TÉCNICA e DIRETORIA DE INTERIORIZAÇÃO) e suas respectivas Coordenadoria e Gerências conforme organograma disponibilizado no link https://www.politec.mt.gov.br/documents/d/politec/politec-decreto-n-2-180-de-26-06-2026-pdf
2. Não está sendo possível a leitura da imagem inserida no PDF
Corrija antes de salvar:
O PDF não tem camada de texto (é imagem ou não traz a tabela de unidades). O OCR automático não está embutido nesta versão: use a exportação CSV/Excel ou digite os números na conferência.
2. Aba meses importados: Soma e Total de Relatório com quantitativo errado. _(Karine Assunção)_

### Conferência (`#/conferencia/:mes`)

Situação: não funciona ou deu erro (2)

- [ ] Extrair os dados da cartão "Pendentes"
Unidade e informações inexistentes
O botão "Aprovar o mês" não funciona e não gera a planilha _(Karine Assunção)_
- [ ] 1. Não está sendo realizado a leitura do PDF, o dado informado em "lido" está errado;
2. Mesmo após as correções, o botão "Aprovar o mês" não funciona, impedindo prosseguir para a próxima etapa "Gerar planilha" _(Karine Assunção)_

### Gerar planilha (`#/exportar/:mes`)

Situação: não funciona ou deu erro (2)

- [ ] O botão "Aprovar o mês" não funciona e não gera a planilha _(Karine Assunção)_
- [ ] 2. Mesmo após as correções, o botão "Aprovar o mês" não funciona, impedindo prosseguir para a próxima etapa "Gerar planilha" _(Karine Assunção)_

### Histórico (`#/historico`)

Situação: funciona como esperado (2)


## Erros encontrados

- [ ] Em conferir sobe dados fictícios e unidades não monitoras _(Karine Assunção)_

## O que falta

- [ ] Extrair os dados da cartão "Pendentes" _(Karine Assunção)_

## Quem respondeu

- Karine Assunção · equipe do app · CQUAL · nota 3 · 2026-11-03
- Karine Assunção · equipe do app · CQUAL · nota 3 · 2026-11-04
