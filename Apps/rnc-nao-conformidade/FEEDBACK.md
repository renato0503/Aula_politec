# Feedback dos alunos · Não Conformidades

Gerado por `python Apps/_base/baixar_feedback.py` em 03/11/2026, a partir da coleção `feedback_apps` do Firestore.
2 resposta(s) · nota média 3,5 de 5

Use este arquivo para abrir o próximo sprint: cada item vira uma linha do `sprint.md`. Os números com fonte são da própria resposta.

## Resumo

- Usaria no trabalho: sim, com ajustes (2)
- Piloto: sem resposta (1); talvez (1)

## Prioridades (na ordem de cada pessoa)

- [ ] geração de RNC baseada no modelo oficial _(Sabrina Ellen Costa Silva, 1ª)_
- [ ] Nomenclatura correta: Categoria Sigla Descrição Administração ADM Procedimentos administrativos, tais como elaboração e tramitação de documentos. Ambiente e Segurança AMB Procedimentos relacionados ao ambiente e à segurança do trabalho. Pessoal PES Procedimentos relacionados à Gestão de pessoas e à promoção da qualidade de vida no trabalho. Reagentes REA Procedimentos de preparo, armazenamento, utilização e descarte de reagentes. Equipamentos EQP Procedimentos de operação e manutenção de equipamentos. Métodos de Procedimento e Análise MPA Procedimentos relacionados a métodos de procedimento e análise. _(Sabrina Ellen Costa Silva, 1ª)_
- [ ] Nomenclaturas corretas: _(Sabrina Ellen Costa Silva, 2ª)_

## Tela por tela

### Minhas RNCs (`#/minhas`)

Situação: precisa de ajuste (1)

- [ ] Ele cria um relatório em PDF ? Quem fez é registrado ? Qualquer um do setor pode responder ? _(Sabrina Ellen Costa Silva)_

### Painel (`#/painel`)

Situação: funciona como esperado (1)

- [ ] A tela está boa para visualizar mas apenas o login da CQUAL realmente poderia usar devido a facilidade para trocar o acesso _(Sabrina Ellen Costa Silva)_

### RNC (`#/rnc/:id`)

Situação: funciona como esperado (1)


### Importar (`#/importar`)

Situação: não testou (1)

- [ ] Minha planilha é on-line no Google planilhas devido ser automatizada com forms _(Sabrina Ellen Costa Silva)_

### Enviar ao setor (`#/exportar`)

Situação: não testou (1)

- [ ] Não gera um documento gera apenas escritas _(Sabrina Ellen Costa Silva)_

## Erros encontrados

- [ ] Não gera os arquivos para encaminhar aos outros setores _(Sabrina Ellen Costa Silva)_

## O que falta

- [ ] Precisa gerar os documentos com o modelo já existente e se der ter login e senha para cada um entrar e visualizar oque cada um precisa enxergar _(Sabrina Ellen Costa Silva)_

## Regras, nomes e números que não batem

- [ ] Prazo para lançamento de plano de ação é de 30 dias e para resposta de complementação de dados é 5 dias úteis _(Sabrina Ellen Costa Silva)_

## Observações

- [ ] Professor eu mandei sem ter terminado !! Mas em geral está bom mas acredito que será mais para acompanhar do que encaminhar para eles ! _(Sabrina Ellen Costa Silva)_

## Quem respondeu

- Sabrina Ellen Costa Silva · equipe do app · CQUAL · nota 3 · 2026-11-03
- Sabrina Ellen Costa Silva · equipe do app · Cqual · nota 4 · 2026-11-03

## Retorno pelo WhatsApp (04/11/2026)

- [x] "Meu app tá criando um código ao invés de pegar o da própria planilha" _(Sabrina)_. Resolvido no Sprint 8 do `sprint.md` (commit `0588c5f`): o ID ocorrência da planilha passou a ser usado, os setores foram padronizados e o nome de pessoa saiu da coluna de envolvidos.
- [ ] Confirmar com ela as siglas dos setores (GNEC, GMLROO, GPVV...). Premissa em `Apps/PREMISSAS.md`, seção 18.
