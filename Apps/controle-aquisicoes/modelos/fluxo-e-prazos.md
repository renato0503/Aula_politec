# Fluxo de aquisição e prazos (elucubração com base legal)

> **Premissa assumida em 30/10/2026.** O fluxo real de tramitação e os prazos de
> cada etapa não foram confirmados com a Coordenadoria de Aquisições. O fluxo
> abaixo foi **elucubrado a partir da Lei nº 14.133/2021** (Lei de Licitações e
> Contratos Administrativos), com o artigo que fundamenta cada etapa. O texto da
> lei foi consultado em 30/10/2026 no acervo
> [ctresb/leis](https://github.com/ctresb/leis) e no site do Planalto.
>
> **O que é premissa e o que é lei**: a **lei** diz o que precisa existir
> (fase preparatória, estudo técnico preliminar, análise de riscos, pesquisa de
> preços com 3 fornecedores, parecer jurídico, modalidade). Os **prazos em dias e
> a divisão em 9 etapas** são elucubração, para o app ter algo testável.

---

## 1. As 9 etapas do app

O app de Controle do Processo de Aquisição (`controle-aquisicoes`) tem 9 etapas.
Cada uma com o documento que ela exige e o artigo que a fundamenta:

| # | Etapa do app | Documento exigido | Base legal | Prazo assumido |
|---|---|---|---|---|
| 1 | DFD | Documento de Formalização de Demanda | art. 18, I e § 1º, I e VI | 3 dias |
| 2 | ETP | Estudo Técnico Preliminar | art. 18, § 1º (13 elementos) | 5 dias |
| 3 | Análise de riscos | Análise dos riscos | art. 18, X | 3 dias |
| 4 | TR | Termo de Referência | art. 18, II | 5 dias |
| 5 | Pesquisa de preços | Pesquisa de preços com 3 cotações | art. 23, § 1º, IV | 7 dias |
| 6 | SIGADOC e SIAG | SIGADOC (número) e SIAG (número) | art. 12, caput e § 3º | 2 dias |
| 7 | Análise técnica | Análise técnica pela área demandante | art. 11, I | 5 dias |
| 8 | Análise jurídica | Parecer do órgão de assessoramento jurídico | art. 53 | 10 dias |
| 9 | Modalidade definida | Definição da modalidade e do critério de julgamento | art. 18, VIII | 3 dias |

**Total do ciclo: 43 dias**, contra o prazo de 30 dias corridos do processo no
app. A diferença é o que o painel mostra como atraso: na prática, 3 das 10
aquisições do exemplo estão fora do prazo.

## 2. Por que a pesquisa de preços exige 3 cotações

O **art. 23, § 1º, IV** da Lei nº 14.133/2021 diz:

> *"pesquisa direta com no mínimo 3 (três) fornecedores, mediante solicitação
> formal de cotação, desde que seja apresentada justificativa da escolha desses
> fornecedores e que não tenham sido obtidos os orçamentos com mais de 6 (seis)
> meses de antecedência da data de divulgação do edital."*

Por isso o app exige 3 cotações (RN04) e o alerta de inconsistência entre o
estimado e o cotado. A margem de 30% usada no alerta é elucubração: a lei não
fixa percentual, ela manda o estimado ser compatível com o mercado.

## 3. O que a lei exige em cada etapa

### Fase preparatória (art. 18)

> *"A fase preparatória do processo licitatório é caracterizada pelo planejamento
> e deve compatibilizar-se com o plano de contratações anual [...] e com as leis
> orçamentárias, bem como abordar todas as considerações técnicas, mercadológicas
> e de gestão que podem interferir na contratação."*

O art. 18 traz 11 incisos que o app cobre assim:

| Inciso do art. 18 | Onde entra no app |
|---|---|
| I - descrição da necessidade fundamentada em ETP | etapa DFD e etapa ETP |
| II - definição do objeto por termo de referência, anteprojeto ou projeto | etapa TR |
| III - condições de execução, pagamento, garantias e recebimento | etapa TR |
| IV - orçamento estimado com as composições dos preços | etapa Pesquisa de preços |
| V - elaboração do edital | etapa Modalidade definida |
| VI - minuta de contrato, quando necessária | etapa Modalidade definida |
| VII - regime de fornecimento, prestação de serviços ou execução de obras | etapa TR |
| VIII - modalidade, critério de julgamento, modo de disputa | etapa Modalidade definida |
| IX - motivação circunstanciada das condições do edital | etapa Análise técnica |
| X - análise dos riscos | etapa Análise de riscos |
| XI - motivação sobre o momento da divulgação do orçamento | etapa Análise técnica |

### Os 13 elementos do ETP (art. 18, § 1º)

O § 1º do art. 18 lista os elementos que o estudo técnico preliminar deve
conter. O § 2º diz que **pelo menos os incisos I, IV, VI, VIII e XIII** são
obrigatórios, e os demais precisam de justificativa.

| Item | Elemento | Obrigatório pelo § 2º |
|---|---|---|
| I | descrição da necessidade, sob a perspectiva do interesse público | sim |
| II | previsão no plano de contratações anual | não |
| III | requisitos da contratação | não |
| IV | estimativas das quantidades, com memórias de cálculo | sim |
| V | levantamento de mercado e justificativa da solução | não |
| VI | estimativa do valor, com preços unitários referenciais | sim |
| VII | descrição da solução como um todo, com manutenção e assistência | não |
| VIII | justificativas para o parcelamento da contratação | sim |
| IX | demonstrativo dos resultados pretendidos | não |
| X | providências para a fiscalização e a gestão contratual | não |
| XI | contratações correlatas e interdependentes | não |
| XII | impactos ambientais e medidas mitigadoras | não |
| XIII | posicionamento conclusivo sobre a adequação da contratação | sim |

### A pesquisa de preços (art. 23)

O valor estimado pode vir de 4 parâmetros, **combinados ou não**:

| § 1º | Parâmetro |
|---|---|
| I | composição de custos unitários até a mediana do painel de preços ou do PNCP |
| II | contratações similares da Administração no período de 1 ano anterior |
| III | dados de pesquisa publicada em mídia especializada, tabela de referência ou sítios especializados, com data e hora de acesso |
| IV | **pesquisa direta com no mínimo 3 fornecedores**, com justificativa da escolha e orçamentos de no máximo 6 meses |

### O parecer jurídico (art. 53)

> *"Ao final da fase preparatória, o processo licitatório seguirá para o órgão
> de assessoramento jurídico da Administração, que realizará controle prévio de
> legalidade mediante análise jurídica da contratação."*

O § 1º do art. 53 exige que o parecer seja redigido em linguagem simples e
compreensível, de forma clara e objetiva, apreciando todos os elementos
indispensáveis à contratação. O § 3º diz que, encerrada a instrução do processo
sob os aspectos técnico e jurídico, a autoridade determinará a divulgação do
edital.

**Por isso a etapa de análise jurídica é a mais longa do fluxo (10 dias)** e vem
logo antes da definição da modalidade.

### Os prazos de divulgação (art. 55)

O art. 55 fixa os prazos **mínimos para apresentação de propostas e lances**,
contados da divulgação do edital. É o prazo do mercado, não o prazo interno do
app, mas serve de referência para o planejamento:

| Objeto | Prazo mínimo |
|---|---|
| Aquisição de bens (menor preço ou maior desconto) | 8 dias úteis |
| Aquisição de bens (melhor técnica) | 15 dias úteis |
| Serviços e obras (menor preço) | 8 dias úteis |
| Serviços e obras (melhor técnica) | 15 dias úteis |

O app não implementa a etapa de divulgação, porque ela depende do edital. A
etapa 9 (Modalidade definida) é o ponto em que o processo fica pronto para o
agente de contratação publicar o edital, nos prazos do art. 55.

## 4. As permissões

| Perfil | O que faz |
|---|---|
| Unidade requisitante | registra a demanda, responde a diligências |
| Equipe de aquisições | instrui, anexa documentos, conclui etapas, responde pela pesquisa de preços |
| Chefia | acompanha prazos, pendências e aprova |

O **agente de contratação** (art. 8º) é pessoa designada pela autoridade
competente, entre servidores efetivos ou empregados públicos dos quadros
permanentes, para tomar decisões, acompanhar o trâmite, dar impulso ao
procedimento e executar outras atividades até a homologação. Quando o processo
envolver bens ou serviços especiais, pode ser substituído por comissão com no
mínimo 3 membros (art. 8º, § 2º). No app, o papel "Equipe de aquisições"
desempenha essa função.

## 5. Os documentos do exemplo

| Etapa | Documento no seed |
|---|---|
| DFD | DFD |
| ETP | ETP |
| Análise de riscos | Análise de riscos |
| TR | TR |
| Pesquisa de preços | Pesquisa de preços |

As 5 últimas etapas (SIGADOC e SIAG, Análise técnica, Análise jurídica,
Modalidade definida) não exigem documento no app: são registros de decisão.

## 6. A linha de base

| Medida | Valor assumido |
|---|---|
| Prazo do processo | 30 dias corridos |
| Ciclo pelas 9 etapas | 43 dias |
| Processos fora do prazo no exemplo | 3 de 10 |

## Como confirmar

1. Ler o fluxo real com a Coordenadoria de Aquisições e comparar com as 9 etapas.
2. Ajustar os prazos de cada etapa na lista do app (`CA_ETAPAS` e a tabela de
   prazos em `src/app.js`).
3. Confirmar se a pesquisa de preços usa o inciso IV (3 fornecedores) ou outro
   parâmetro do art. 23.
4. Confirmar quem é o agente de contratação e quem responde por cada etapa.
