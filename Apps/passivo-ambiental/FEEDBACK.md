# Feedback dos alunos · Passivo Ambiental

Gerado por `python Apps/_base/baixar_feedback.py` em 08/11/2026, a partir da coleção `feedback_apps` do Firestore.
2 resposta(s) · nota média 3,0 de 5

Use este arquivo para abrir o próximo sprint: cada item vira uma linha do `sprint.md`. Os números com fonte são da própria resposta.

## Resumo

- Usaria no trabalho: sim, com ajustes (2)
- Piloto: talvez (2)

## Prioridades (na ordem de cada pessoa)

- [ ] Acrescentar as abas adicionais _(FABIO XAVIER DA CONCEICAO, 1ª)_
- [ ] Fazer o app ler os pdfs escaneados e imagens dentro de uma pasta e transformá-los em metadados. _(Fábio Xavier da Conceição, 1ª)_
- [ ] Corrigir a aba MAPAS _(FABIO XAVIER DA CONCEICAO, 2ª)_
- [ ] acrescentar as seções (BAS?) que o laudo deverá conter _(Fábio Xavier da Conceição, 2ª)_
- [ ] Melhorar cabeçalho _(FABIO XAVIER DA CONCEICAO, 3ª)_
- [ ] acrescentar o layout padrão dos laudos da POLITEC _(Fábio Xavier da Conceição, 3ª)_

## Tela por tela

### Laudo (`#/laudo/:id`)

Situação: precisa de ajuste (2)

- [ ] Precisa de ajustes. Necessário acrescentar as informações: n. Da requisição. Nome da autoridade requisitante. Natureza do exame. Data de elaboração. Horário de início e fim. _(FABIO XAVIER DA CONCEICAO)_
- [ ] Alterar os campos obrigatórios para:
Protocolo nº: Exemplo "019639/2025"
Órgão Solicitante: Exemplo "Delegacia Especializada de Meio Ambiente"
Autoridade Requisitante: Exemplo "Delegado (a) Alexandre Vicente"
Requisição nº: Exemplo "Ofício N° 2021.5.37146/DEMA"
Data da Requisição: Exemplo "25/11/2021"
Data de Atribuição: Exemplo "20/10/2026"
Natureza dos Exames: Engenharia Legal e Meio Ambiente
Local dos Exames: Exemplo "Município de Aripuanã"
Coordenada Geográfica de Referência: -9.8953275, -60.4301475
Data e Horário dos Exames: Exemplo "iniciado em 21/10/2026 às 8h00"
Destino do Laudo: Exemplo "Delegacia Especializada de Meio Ambiente" _(Fábio Xavier da Conceição)_

### Mapa (`#/mapa/:id`)

Situação: não funciona ou deu erro (2)

- [ ] Não abriu o editor de mapas. Além disso, acrescentaria 3 mapas obrigatórios no laudo: mapa de localização, mapa anterior ao dano, mapa posterior ao dano ambiental. Além disso, acrescentaria a opção de subir os mapas em PDF _(FABIO XAVIER DA CONCEICAO)_
- [ ] Esta aba pode ser um importador de mapas salvos em uma pasta como imagem ou pdf. Os mapas serão elaborados no Qgis, pois algumas etapas podem ser automatizadas nele. _(Fábio Xavier da Conceição)_

### Painel (`#/painel`)

Situação: funciona como esperado (1); precisa de ajuste (1)

- [ ] Acrescentar um card com o tempo médio de elaboração dos laudos dentro do app. Acrescentar um mapa com a localização (coordenada) das requisições periciais, status dos laudos e preço da valoração do dano para o status "finalizado". Criar um gráfico que demonstre o preço médio da valoração por requisição, a quantidade total de requisições, tempo médio de resposta por requisição, soma das valorações do dano por status do laudo e total. _(Fábio Xavier da Conceição)_

### Requisições (`#/requisicoes`)

Situação: funciona como esperado (1); precisa de ajuste (1)

- [ ] Acrescentar na lista de requisições a possibilidade de ordenar em ordem crescente ou decrescente; Na situação do laudo acrescentar filtro para seleção de processos "finalizados" _(Fábio Xavier da Conceição)_

### Laudo em PDF (`#/pdf/:id`)

Situação: funciona como esperado (1); precisa de ajuste (1)

- [ ] Acrescentaria a opção de exportação em .docx _(FABIO XAVIER DA CONCEICAO)_
- [ ] A versão em PDF está sendo gerada, contudo, o texto está sem formatação. Será necessário acrescentar rodapé padrão da Politec. _(Fábio Xavier da Conceição)_

### Nova requisição (`#/requisicao/nova`)

Situação: não testou (1); funciona como esperado (1)

- [ ] Não foi testado _(FABIO XAVIER DA CONCEICAO)_

## Erros encontrados

- [ ] Erro na elaboração de mapas. _(FABIO XAVIER DA CONCEICAO)_

## O que falta

- [ ] Adicionar abas: Metodologia - aba em que um texto padrão sobre a metologia de elaboração do laudo é adicionado; Considerações: local em que os vestígios encontrados por Sensoriamento Remoto, são explicados; Valoração do Dano Ambiental - O sistema calcula o valor do dano ambiental a partir de informações lançadas pelo perito e apresenta uma tabela com a memória do cálculo no laudo; Quesitos - campo onde as perguntas apresentadas na requisição pericial são respondidas pelo perito. _(FABIO XAVIER DA CONCEICAO)_
- [ ] O app será alterado para rodar offline, na máquina do perito, ler imagens e PDF escaneado para gerar as informações do cabeçalho.
A primeira página será a capa do laudo e deverá conter somente o número do laudo (obtido no sistema Atena);
Seções que o laudo deverá conter:
CAPA DO LAUDO: inserir n. do laudo centralizado no meio da página
1. INFORMAÇÕES
Inserir dados do cabeçalho
2. HISTÓRICO
Descrever breve histórico do laudo, quando foi demandado, os documentos anexados à requisição, etc.
3. EXAMES 
3.1. Local
Descrição da localização do local de perícia (Município, se inserido em Unidade de Conservação, Zona de Amortecimento, Terra Indígena, Área de Abrangência, tipo de vegetação, Amazônia Legal ?).
3.2. Materiais e Métodos
Descrição da metodologia utilizada na elaboração do laudo.
3.3. Consultas públicas
Resultado das consultas realizadas a sites públicos para saber sobre a legalidade do dano ambiental e sobre eventual titularidade.
3.4. Exames por Sensoriamento Remoto
Local destinado à apresentação de tabelas e resumo dos achados encontrados no exame por sensoriamento remoto. Os mapas podem ser apresentados aqui como figuras.
4. VALORAÇÃO DO DANO
Local destinado à apresentação de tabelas resumo do cálculo realizado e valor final da valoração.
5. QUESITOS ESPECÍFICOS
Lista de perguntas apresentadas na requisição pericial e respectivas respostas.
6. CONCLUSÃO
Conclusão do aludo pericial em formato texto. _(Fábio Xavier da Conceição)_

## Regras, nomes e números que não batem

- [ ] O setor se chama Diretoria de Interiorização, mas no app pode ser editável, haja vista que o nome do setor pode ser alterado ao longo do tempo. _(FABIO XAVIER DA CONCEICAO)_

## Observações

- [ ] Gostaria muito de ver o app funcionando. Acredito que a elaboração de laudos ambientais ficaria mais acessível aos demais peritos e que o passivo processual seria colocado reduzido nos próximos 6 meses. Se o app ficar dentro das expectativas, talvez possa ser compartilhado com outras coordenadorias e gerências da Politec. _(FABIO XAVIER DA CONCEICAO)_

## Quem respondeu

- FABIO XAVIER DA CONCEICAO · equipe do app · DI/Politec · nota 3 · 2026-11-03
- Fábio Xavier da Conceição · equipe do app · DI · nota 3 · 2026-11-05
