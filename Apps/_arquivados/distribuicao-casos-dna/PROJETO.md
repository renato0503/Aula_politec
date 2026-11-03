# PROJETO.md — Alteração do modelo de distribuição de casos envolvendo perícias de DNA, de rodada de pastas para rodada da placa de análise.

**Aluno ou equipe:** Nelson e Luciana
**Unidade:** Gerência de Perícias em Biologia Molecular
**Contato:** nelsonyoshitake@politec.mt.gov.br
**Projeto:** Alteração do modelo de distribuição de casos envolvendo perícias de DNA, de rodada de pastas para rodada da placa de análise.
**Tipo de projeto:** Mapeamento de processo (fluxo, BPMN ou Mermaid)
**Data:** 2026-10-27
**Resumo:** O projeto piloto visa reduzir o tempo entre a aliquotagem das amostras e a liberação do laudo pericial. Anteriormente, as pastas dos casos eram distribuídas após a obtenção dos perfis genéticos, e distribuído aos peritos em lotes de 5 a 8 pastas/perito. A distribuição incluía os casos ordinários e as cobranças e alguns ficavam sem distribuição durante algumas semanas. No projeto, após a aliquotagem dos casos de cobrança, as pastas são distribuídas aos peritos para iniciarem a compilação de dados e após a obtenção dos perfis genéticos, todos os casos ordinários são distribuídos para um dos peritos. Desta forma, a rodada da semana é totalmente distribuída e no próximo ciclo outro perito recebe a rodada completa dos casos ordinários.

## 1. Problema (a dor)

**Problema:** Gargalo de tempo até a distribuição de todos os casos da rodada aos peritos.
**Impacto:** Redução de tempo para liberação dos laudos após a obtenção dos perfis genéticos
**Quem sofre:** Cidadão externo, Servidor da unidade, Equipe interna, Autoridade, Unidade parceira, Chefia
**Como é feito hoje:** As pastas dos casos eram distribuídas após a obtenção dos perfis genéticos, e distribuído aos peritos em lotes de 5 a 8 pastas/perito. A distribuição incluía os casos ordinários e as cobranças e alguns ficavam sem distribuição durante algumas semanas
**Evidências:** Medida feita pela equipe, Planilha ou controle local
**Detalhe da evidência:** Planilha com o controle dos protocolos com data de entrada no setor, data de processamento das alíquotas, data de distribuição ao perito e data de liberação do laudo pericial. A redução do tempo entre a entrada no setor e o processamento está sendo feito mediante o desenvolvimento de um Power Bi que ranqueia os protocolos baseados em pesos. Neste momento, busca-se verificar a redução do tempo entre o data de processamento das alíquotas e a data de distribuição ao perito e consequentemente, a redução de tempo para a liberação do laudo pericial.
**O que não pode ser automatizado:** A análise e interpretação dos perfis genéticos depende muito da experiência do analista.

## 2. Objetivo do MVP (o que faz e o que NÃO faz)

**Objetivo do MVP:** Validar a distribuição da rodada completa de casos ordinários a um perito, antes do processamento, e a fila separada de cobranças, reduzindo o tempo entre a saída dos resultados e a distribuição das pastas.
**O que o MVP não faz:** O MVP não processa amostras, não interpreta perfis genéticos e não substitui a análise do perito. Não integra com o Atena nem com as planilhas locais; os dados são fictícios.
**Entregável do projeto:** Aplicativo web para montar a rodada da placa, separar a fila de cobranças, distribuir a rodada ordinária em rotação e medir o tempo entre o processamento e a distribuição.
**Dentro do escopo:** Cadastro das rodadas e dos casos (ordinário e cobrança), status de processamento, distribuição da rodada ordinária a um perito em rotação, fila separada de cobranças, painel dos casos sem perito e tempo entre processamento e distribuição.
**Fora do escopo:** Processamento laboratorial, análise e interpretação dos perfis genéticos, emissão e assinatura do laudo, integração com o Atena, com o Power BI de priorização e com as três planilhas locais.
**Plataforma alvo:** Site web (abre no navegador)
**Primeira tela:** Painel da rodada: casos da placa, perito responsável, fila de cobranças e tempo médio entre o processamento e a distribuição.
**Simulado no MVP:** A rodada é simulada com protocolos fictícios. O processamento é representado por uma data e um status, sem vínculo com equipamento ou amostra real.
**Critério de aceite:** O coordenador monta a rodada, distribui todos os casos ordinários a um perito e vê, no painel, que nenhum caso ordinário ficou sem perito e qual foi o tempo entre o processamento e a distribuição.
**Dados de exemplo:** 4 peritos, 6 rodadas e ao menos 40 casos fictícios, com protocolos, tipo (ordinário ou cobrança), datas de processamento e de distribuição.
**O que já existe pronto e pode ser reaproveitado:** As três planilhas locais (protocolos, custódia e alíquotas), o Power BI de priorização e os procedimentos operacionais do laboratório. No MVP, os dados são fictícios.
**Dependências:** Da coordenação do laboratório para validar a rotação e a fila de cobranças; da TI para a futura integração com o Atena; da equipe para medir a linha de base.

## 3. Usuários e papéis

| Papel | Quem é | O que enxerga | O que faz | O que não pode fazer | Registro |
|---|---|---|---|---|---|
| coordenador | Responsável pela gestão operacional do laboratório e pela supervisão das equipes e dos processos. | Painel geral, fila de exames, status das amostras, prazos, pendências, indicadores, relatórios e histórico de atividades conforme sua autorização. | Distribui demandas, acompanha prazos, supervisiona o fluxo de trabalho, trata pendências, autoriza ações administrativas previstas e acompanha indicadores de desempenho. | Alterar resultados periciais sem autorização e justificativa formal; apagar registros de auditoria; acessar dados restritos sem necessidade funcional; aprovar o próprio trabalho quando houver segregação obrigatória de funções. | Login e acessos, distribuição de exames, alterações de prioridade, decisões administrativas, autorizações, justificativas, consultas e exportações de dados. |
| técnico administrativo | Profissional responsável pelo recebimento, cadastro, organização documental e controle administrativo dos exames e das amostras. | Cadastros, solicitações, identificação e situação administrativa das amostras, documentos, protocolos, pendências e prazos necessários à sua função. | Cadastra solicitações, confere documentos, registra recebimentos e movimentações autorizadas, organiza processos, atualiza dados administrativos e encaminha demandas aos responsáveis. | Validar ou alterar resultados de DNA; emitir conclusões periciais; modificar dados técnicos sem autorização; liberar laudos restritos; excluir registros definitivos ou contornar controles de acesso. | Cadastros e alterações, recebimento e encaminhamento de materiais, conferências documentais, usuário responsável, data e hora das ações e justificativas de correção. |
| perito | Profissional habilitado responsável pela análise técnico-científica das amostras e pela elaboração ou validação das conclusões periciais, conforme sua competência. | Dados técnicos autorizados, identificação codificada das amostras, cadeia de custódia, protocolos analíticos, resultados laboratoriais, controles de qualidade, histórico de processamento e documentos pertinentes ao exame. | Analisa amostras, registra procedimentos, interpreta resultados, documenta inconformidades, elabora conclusões e assina ou valida laudos conforme suas atribuições e os procedimentos do laboratório. | Alterar ou apagar resultados sem trilha de auditoria; modificar a cadeia de custódia retroativamente; acessar casos sem autorização; validar análises fora de sua competência; liberar resultados sem cumprir os critérios de revisão aplicáveis. | Acesso ao caso, identificação das amostras, etapas analíticas, métodos utilizados, equipamentos e reagentes quando aplicável, resultados, controles, revisões, alterações justificadas, assinatura e emissão de laudos. |

**Observações sobre os papéis:** O coordenador distribui as pastas e acompanha os prazos; o perito analisa, interpreta e elabora o laudo; o técnico administrativo cadastra e organiza a documentação. A distribuição é uma decisão do coordenador, apoiada pelo cálculo de rotação.

## 4. Dados (entidades e colunas; tudo SINTÉTICO)

| Entidade | O que representa | Colunas | Chave | Volume | Origem | Sintético |
|---|---|---|---|---|---|---|
| Rodada | Rodada da placa de análise | id_rodada; placa; data; perito_id; status | id_rodada | 6 no exemplo | Cadastro do app | Sim |
| Caso | Pasta de um protocolo na rodada | id_caso; rodada_id; protocolo; tipo; status; data_processamento; perito_id; distribuido_em | id_caso | ~50 no exemplo | Cadastro do app | Sim |
| Perito | Profissional que recebe a rodada | id_perito; nome; especialidade; ativo | id_perito | 4 no exemplo | Cadastro fictício | Sim |
| Log | Histórico das distribuições | id; rodada_id; acao; perfil; data_hora | id | — | App | Sim |

**O que precisa ser coletado:** Atualmente existe um delay entre a saída dos resultados do processamento e a entrega da pasta ao perito
**Quem libera o acesso:** o coordenador no momento da distribuição dos casos

### Fontes de dados do processo real

| Fonte | Tipo | Onde | Existe | Uma linha é | Volume | Campos de data | Atualiza | LGPD |
|---|---|---|---|---|---|---|---|---|
| sistema Atena | Sistema oficial | rede | Sim | protocolo |  | sim | sim | Sim |
| sistema | Planilha local | rede local | Sim | protocolo |  | sim | sim | Sim |
| sistema | Planilha local | rede local | Sim | protocolo |  | sim | sim | Sim |
| sistema | Planilha local | rede local | Sim | alíquota |  | sim | sim | Sim |


## 5. Regras de negócio (RN01, RN02...)

| ID | Regra | Quando se aplica | Exceção | Quem valida | Tipo |
|---|---|---|---|---|---|
| RN01 | A rodada só é distribuída quando todos os casos ordinários estão processados | Na distribuição | Cobranças seguem a fila própria | Coordenador | Negócio |
| RN02 | Todos os casos ordinários da rodada vão para o mesmo perito | Na distribuição | Nenhuma | Sistema | Negócio |
| RN03 | As cobranças ficam em fila separada e são distribuídas depois da aliquotagem | No cadastro e na distribuição | Nenhuma | Técnico | Negócio |
| RN04 | O perito da rodada anterior não recebe a rodada seguinte (rotação) | Na sugestão de perito | Menos de 3 peritos ativos | Sistema | Cálculo |


## 6. Telas (#/painel, #/lista...)

| Rota | Tela | Objetivo | Quem usa | Dados | Ação | Regra | Tipo | Verificável como | MVP |
|---|---|---|---|---|---|---|---|---|---|
| #/painel | Painel | Ver casos sem perito, rodadas e o tempo até a distribuição | Coordenador | Rodadas, casos e tempos | Abrir a rodada | RN01 a RN04 | Tela | Nenhum caso ordinário sem perito | Sim |
| #/rodada/nova | Nova rodada | Montar a placa e os casos | Técnico e coordenador | Placa, data e casos (ordinário ou cobrança) | Salvar | RN01 | Tela | Rodada criada com os casos | Sim |
| #/rodada/:id | Rodada e distribuição | Distribuir a rodada ordinária e as cobranças | Coordenador | Casos, peritos e datas | Distribuir | RN02 a RN04 | Tela | Rodada inteira para um perito, em rotação | Sim |


## 7. KPIs (nome = fórmula em uma linha)

| KPI | Pergunta | Fórmula | Fonte | Linha de base | Valor esperado | Como medir |
|---|---|---|---|---|---|---|
| Tempo entre processamento e distribuição | Quantos dias o caso espera entre o processamento e a pasta do perito? | Média(distribuido_em - data_processamento) | Registro do app | não medida no envio | 1 dia | Medir os casos do piloto de 30 dias |
| Tempo até a liberação do laudo | O laudo sai mais cedo depois da mudança? | Média(data_laudo - data_processamento) | Planilha e app | 84 h/caso/mês | reduzir | Comparar antes e depois no piloto |

**Período da linha de base:** Registro
**Campos de data e tempo que existem:** Data de entrada no setor, data de processamento da alíquota, data de distribuição ao perito e data de liberação do laudo.

## 8. Stack: HTML único (CSS/JS inline), dados em JSON embutido, GitHub Pages.

**Stack escolhida:** HTML único (CSS/JS inline), dados em JSON embutido, GitHub Pages
**Detalhe da stack:** Um único index.html (HTML, CSS e JS embutidos), com dados no IndexedDB do navegador e backup .json, publicado no GitHub Pages, sem servidor.
**Hospedagem:** GitHub Pages, com um arquivo HTML único. É suficiente para demonstrar a montagem da rodada e a distribuição, sem integrar com sistemas oficiais.
**Custo e licenças:** R$ 0,00 no MVP acadêmico (HTML, CSS, JavaScript e GitHub Pages).
**Contas e domínio:** O professor publica o protótipo em uma conta do GitHub; a versão institucional depende da TI e da coordenação.

| Opção | Tipo | Onde roda | Custo | Quem mantém | Acesso | Banco de dados | Escala | Limitação |
|---|---|---|---|---|---|---|---|---|
| GitHub Pages | Estática e gratuita | github.io | Zero | Equipe do projeto | Link (o app; os dados ficam no navegador) | Não tem | Baixa | Publica só o app, nunca os dados |


## 9. Restrições e LGPD

**Restrições:** A custódia, a análise e a interpretação dos perfis genéticos continuam com as pessoas. O sistema não decide a distribuição sozinho: sugere a rotação e o coordenador confirma.
**Dados pessoais tratados:** Número do protocolo, tipo de exame e nome do perito. No MVP, todos fictícios.
**Base legal:** Exercício de competência legal do órgão para a perícia oficial (art. 7º, III, da LGPD). O protótipo não usa dados reais.
**Retenção:** Dados fictícios mantidos só durante o piloto acadêmico; um botão apaga a rodada.
**Acesso e registro:** Acesso por perfil: coordenador, perito e técnico. A versão institucional exige autenticação individual e trilha de auditoria.
**Requisitos marcados:** -

---

# Anexo A — AS-IS (o fluxo de hoje)

**Início:** Abertura de protocolo solicitando exame complementar para o DNA
**Fim:** Liberação do laudo pericial
**Entradas:** Laudos periciais associados (laudo da medicina legal, laudo de local de crime), Requisição de laudo, pasta do caso, Formulários, planilhas, perfis genéticos, relatórios de cálculos estatísticos, laudo pericial
**Saídas:** Laudo pericial disponibilizado
**Volume:** 300
**Duração:** 84h/caso/mês
**Frequência:** Mensal
| Etapa | Quem faz | O que entra | Ação | O que sai | Sistema | Regra | Onde espera | Tempo (h) | Automatizável |
|---|---|---|---|---|---|---|---|---|---|
| Recebimento da solicitação de perícia | recepção do laboratório forense | materiais em lacre e documentos solicitantes  | encaminhamento |  | sistema | decisão | recepção do laboratório | 2 | Sim, com apoio humano |
| Busca dos envelopes de lacre e dos documentos solicitantes | Técnico do laboratório de DNA | materiais em lacre e documentos solicitantes | guarda dos materiais em lacre no container da custódia |  | sistema | regra | adm | 120 | Sim, com apoio humano |
| cadastro em planilha | Técnico do laboratório de DNA | dados de cada requisição | cadastro dos dados da requisição | planilha alimentada | sistema | decisão | adm | 120 | Sim, com apoio humano |
| Ranqueamento da prioridade dos protocolos | Coordenador, mas estamos estruturando um Power BI baseado em pesos | dados | Análise do intervalo entre a data do fato e a data da coleta do material | lista classificada | sistema | regra | automático | 0 | Sim, com regra clara |
| solicitação de amostras da custódia | Técnico do laboratório de DNA |  | busca ativa | envelopes de lacre | sistema | regra | sala de custódia | 8 | Sim, com apoio humano |
| entrega do envelope de lacre ao perito | Técnico do laboratório de DNA |  | entrega física e da custódia do material | envelopes de lacre | papel | regra | freezer | 4 | Não |
| conferência e aliquotagem dos materiais | perito com auxílio de técnico | amostra íntegra | aliquotagem | amostra aliquotada | papel | decisão | tempo de bancada | 2 | Sim, com apoio humano |
| encaminhamento para processamento até a obtenção do perfil genético | perito | amostra aliquotada | extração do dna, purificação, quantificação, normalização, amplificação, eletroforese capilar, montagem e liberação de projeto, análise dos perfis genéticos | perfil genético | sistema | regra | laboratório de processamento de amostras questionadas | 96 | Sim, com apoio humano |
| distribuição das pastas aos peritos | coordenador | pastas dos casos | repasse da custódia dos documentos | pastas dos casos | papel e sistema | decisão | até a próxima distribuição | 120 | Pouco |
| análise do caso, dos resultados e elaboração do laudo pericial | perito | dados | análise dos perfis genéticos, confronto genético, análise estatística e confecção do laudo | laudo pericial | sistema | regra | mesa do perito | 48 | Sim, com apoio humano |
| Inclusão do laudo no sistema Atena | perito | arquivo | upload | arquivo | sistema | regra | sistema | 1 | Não |

**Decisões e aprovações:** 1- recepção do laboratório confere se não há divergências entre informações do sistema e os materiais entregues, caso haja é registrada divergência;
3- Durante o cadastro das informações referentes ao protocolo na planilha, podem haver dados incompletos dificultando o cadastro e o prosseguimento das etapas analíticas;
7- Apesar de existirem POPs que norteiam a tomada de decisões para a aliquotagem, existem muitas particularidades que requerem um olhar caso a caso;
9- Existem diferentes naturezas (crime sexual, local de crime, identificação humana) de exames e peritos especializados para cada natureza. O encaminhamento das pastas aos peritos pelo coordenador depende do número de casos ainda pendentes e do número de cobranças recentes que o perito tem em andamento
**Exceções:** -
**Já digitalizado:** Atualmente existem 3 planilhas (1- contém as todas as informações de cada protocolo desde a entrada do documento até a liberação  do laudo pericial; 2- custódia dos materiais; 3- nome das alíquotas produzidas e que vão ser colocadas para processamento). Existe ainda, um app em desenvolvimento que permitirá o acompanhamento das amostras se já foram aliquotadas, qual o método de extração e o status de processamento

# Anexo B — TO-BE (o fluxo depois da mudança)

**Visão do futuro:** Redução do tempo de distribuição dos casos e consequente redução no tempo de liberação dos laudos periciais
**Mudança principal:** Melhora na eficiência da prestação de serviço para a sociedade
**O que fica igual:** Os procedimentos laboratoriais, controle de qualidade, rastreabilidade permanecem iguais
**O que não pode mudar:** O controle da custódia, a análise e interpretação dos perfis genéticos
| Etapa | O que muda | Quem executa | Benefício | Esforço |
|---|---|---|---|---|
| Aliquotagem e fila de cobranças | As cobranças são distribuídas logo após a aliquotagem, em fila separada | A pessoa assistida pela máquina | Antecipa a compilação de dados | Baixo |
| Rodada de casos ordinários | A rodada inteira da placa vai para um perito, em rotação | A máquina (automação) | Reduz o tempo até a distribuição | Médio |
| Registro da distribuição | O sistema grava perito, data e hora de cada pasta | A máquina (automação) | Rastreabilidade e medida do tempo | Baixo |
| Acompanhamento | Painel com o tempo entre o processamento e a distribuição | A máquina (automação) | Mostra o ganho do piloto | Baixo |

**Piloto do TO-BE:** Piloto de 30 dias registrado em planilha

# Anexo C — Pesquisa, riscos e plano

**Hipótese de campo:** Distribuir a rodada ordinária antes do processamento e separar as cobranças reduz o tempo entre a saída dos resultados e a distribuição das pastas, e por consequência o tempo até o laudo.
| Referência | Tipo | Fonte ou link | Ano | Dado que extrai | Como usar na defesa | Link conferido |
|---|---|---|---|---|---|---|
| Planilha de controle dos protocolos | Documento interno | Gerência de Perícias em Biologia Molecular | 2026 | Datas de entrada, processamento, distribuição e laudo | Sustenta a linha de base do piloto | Sim |
| POPs de aliquotagem | Documento interno | Laboratório de DNA | 2026 | Decisões de aliquotagem | Explica o que permanece humano | Sim |

**Lacunas:** O envio não traz a linha de base medida de tempo entre processamento e distribuição, nem o número de casos por rodada. O piloto de 30 dias deve medir os dois.
| Marco | Data | Responsável | Depende de | Situação |
|---|---|---|---|---|
| Rodadas e peritos modelados | 06/11/2026 | Nelson e Luciana | Reunião com a coordenação | Planejado |
| Protótipo com distribuição em rotação | 27/11/2026 | Nelson | Dados fictícios e regras | Planejado |
| Piloto de 30 dias | 18/12/2026 | Coordenação | Aceite da chefia | Planejado |
| Comparação antes e depois | 29/01/2027 | Nelson | Registros do piloto | Planejado |

| Risco | Probabilidade | Impacto | Mitigação |
|---|---|---|---|
| Resistência do coordenador à nova rotina | Média | Alto | Piloto com confirmação humana e treinamento |
| Caso urgente fora da rodada | Média | Médio | Fila de exceção registrada com justificativa |
| Menos de 3 peritos ativos | Baixa | Médio | A rotação é suspensa e o coordenador decide |

**Apoio necessário:** Apoio da coordenação para validar a rotação e da equipe para registrar as datas no piloto.
**Aprendizado necessário:** Modelagem do processo, regra de rotação, medição de espera, GitHub e Antigravity.

# Anexo D — A defesa

**Frase de defesa:** Se a rodada inteira for distribuída antes do processamento, o tempo entre o resultado e a pasta do perito cai e o laudo sai mais cedo.
**Provas:** A planilha de controle registra as quatro datas de cada protocolo; o Power BI já ranqueia a prioridade. Falta medir o intervalo entre o processamento e a distribuição.
**Piloto:** Piloto de 30 dias com a rodada registrada em planilha e no protótipo, comparando o intervalo entre o processamento e a distribuição antes e depois.
**Maior risco:** O maior risco é a resistência à mudança de rotina do coordenador e do perito; mitigar com piloto, treinamento e a confirmação humana da distribuição.

# Anexo E — Documentos enviados

**Descrição dos documentos:** Planilha de controle dos protocolos com data de entrada, de processamento, de distribuição e de liberação do laudo.
**O que ainda falta:** Número de casos por rodada, tempo medido entre processamento e distribuição e a lista de peritos por natureza de exame.
