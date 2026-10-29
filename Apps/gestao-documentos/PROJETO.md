# PROJETO.md — Gestão de Documentos

**Aluno ou equipe:** Vitória Araújo Dias
**Unidade:** Gabinete de Direção
**Contato:** vitoriadias@politec.mt.gov.br
**Projeto:** Gestão de Documentos
**Tipo de projeto:** -
**Data:** 2026-10-27
**Resumo:** Aplicativo para automatizar e gerenciar eficientemente o ciclo de vida dos processos no setor, o fluxo foi divido nas 5 etapas descritas, com especial destaque para o controle e a cobrança automática de prazos: Cadastro e Entrada; triagem e atribuição; tramitação e instrução; acompanhamento, monitoramento de prazos e automação de cobrança; Notificação de Cobrança (Disparo Automático no Vencimento) alerta e conclusão.
Aplicativo para uso dos servidores lotados no Gabinete de Direção.
Substituir o processo manual de acompanhamento nas planilhas do Excel.

## 1. Problema (a dor)

**Problema:** Fase de acompanhamento, a conferencia diária por processo e cobranças de retorno dos processos.
**Impacto:** Tempo: 1h diária para acompanhamento dos processo em tramitações;
Risco: extemporaneidade de processos;
**Quem sofre:** Servidor da unidade, Chefia
**Como é feito hoje:** Utilizamos um apps de Gestão, porém ainda existe gargalos em acompanhamentos dos prazo e cobranças de retornos nos processos.
**Evidências:** Medida feita pela equipe
**Detalhe da evidência:** As conferencias são feitas manualmente e individualmente pelos servidores.
**O que não pode ser automatizado:** Tramitações diretas sem analise e conferencia  por parte do servidor. 

## 2. Objetivo do MVP (o que faz e o que NÃO faz)

**Objetivo do MVP:** O objetivo do MVP é validar a transformação da mesa virtual do Siga-Doc em um painel ativo, demonstrando a automatização do cálculo de prazos, os alertas visuais preditivos e o disparo automático de cobranças sem intervenção manual dos servidores.
**O que o MVP não faz:** O MVP não integra com o Siga Doc, não envia e-mail, fica apenas para lançamentos e consultas dos processos em andamentos.
**Entregável do projeto:** Componente,( que integram desde a entrada a conclusão), Tipo de Artefato (pessoal ou sistema) e Descrição Funcional no MVP (manual de utilização).
**Dentro do escopo:** Funcionalidades e Telas por Etapa do Processo
•	Etapa 1 — Cadastro e Entrada: Interface de preenchimento estruturado de dados pelo requerente, validação de anexos obrigatórios e gerador automático do número de autuação do expediente no Siga-Doc.

•	Etapa 2 — Atribuição: Painel de controle da mesa virtual da lotação para visualização da carga de trabalho e destinação do processo ao servidor responsável com base em competência ou especialidade.

•	Etapa 3 — Tramitação e Instrução: Módulo de redação e instrução com minutas padronizadas para confecção de despachos, pareceres e emissão de ofícios.

•	Etapa 4 — Acompanhamento e Monitoramento de Prazos (Core da Automação): Cronômetro sistêmico com cálculo automático do tempo de permanência no setor, alertas visuais preditivos e geração/disparo automatizado de mensagens de cobrança para documentos pendentes de resposta de terceiros.

•	Etapa 5 — Conclusão: Interface para deliberação final da autoridade decisora, assinatura digital, tramitação de saída com notificação automática ao solicitante e arquivamento do feito.

2. Governança, Regras e Automações Transversais
•	Controle de Acesso e Papéis: Matriz de permissões segregando funções por papel (Requerente, Servidor da Lotação, Analista e Autoridade Decisora).

•	Alertas e Notificações Predityivas: Motor de eventos configurado para avisar sobre proximidade de vencimento e estouro de prazos regimentais.

•	Rastreabilidade e Logs: Registro inalterável de todas as ações, envios de cobrança e alterações de status no Siga-Doc.
**Fora do escopo:** Análise e Decisão Automatizada de Mérito (Julgamento I.A.)
Por que fica de fora: Impedimento legal e regimental. A análise técnica de pareceres e o deferimento/indeferimento de processos são atribuições exclusivas do servidor, a automação é apenas para o controle de prazos e gestão dos documentos.
**Plataforma alvo:** Site web (abre no navegador)
**Primeira tela:** Tela do Longin, depois o painel de controle.
**Simulado no MVP:** O Envio de Notificações ao Solicitante / Terceiros: A comunicação e as cobranças de prazos (dunning) serão simuladas utilizando disparos para e-mails de teste 
**Critério de aceite:** O Servidor registra os dados em um curto período de tempo e o registro aparece no painel de controle.
**Dados de exemplo:** Templates de Pareceres e Despachos do Órgão: numero do processo, descrição, responsável por doc, data de cadastro e saída;

Estrutura de Banco de Dados e Scripts
Tabelas e Esquemas do Siga-Doc Atual: Modelo de dados relacional existente para cadastro de usuários, perfis de acesso, lotações e numeração única de autuação de processos;

Bibliotecas e Componentes de Software (Open Source / Padrão)
Motor de Regras de Tempo e Datas: Bibliotecas padrão de manipulação de datas e cronômetros

Template e Disparador de E-mails: Biblioteca/serviço de envio de e-mails -apenas para teste ou temporário;

Componentes de Interface (UI Kit / Design System): Bibliotecas de componentes de telas prontas (ex: Bootstrap, Tailwind UI ou Angular Material) para montar os cartões, cores do sinalizador (verde/amarelo/vermelho) e tabelas da Mesa Virtual sem necessidade de design do zero.

emplates de Agente / Regras de Negócio
Gatillhos de Automação de Alertas: Regras lógicas e cronjobs (agendadores de tarefas) configurados para rodar a cada intervalo fixo e verificar a tabela de prazos pendentes, acionando o envio das cobranças automatizadas.
**O que já existe pronto e pode ser reaproveitado:** Existe um aplicativo com todos os lançamentos de cadastro para entrada e saída dos  processos e expedientes.
**Dependências:** TI para a integração de sistema, chefia imediata  e os servidores que vão monitorar.

## 3. Usuários e papéis

**Observações sobre os papéis:** Flexibilização da Atribuição (Papel do Servidor da Lotação):

A função de triagem e atribuição de processos não fica restrita exclusivamente à Chefia/Gestor.

Os Servidores da Lotação passam a ter permissão para conferir o teor do documento, definir o analista/servidor responsável pela instrução e acompanhar o andamento global da fila da unidade.

Visão de Acompanhamento Abrangente:

Todos os servidores vinculados àquela lotação visualizam a caixa do setor (painel coletivo), acompanhando o status das tramitações, prazos e pendências de terceiros, mesmo de processos atribuídos a outros colegas.

## 4. Dados (entidades e colunas; tudo SINTÉTICO)

| Entidade | O que representa | Colunas | Chave | Volume | Origem | Sintético |
|---|---|---|---|---|---|---|
| **Usuario** | Atores do sistema (requerentes, servidores, autoridades e terceiros). | `id_usuario: integer`, `nome: text`, `email: text`, `perfil: string`, `lotacao: string` | `id_usuario` (PK) | 5 registros | Mock Data / Carga inicial | Sim |
| **Processo** | O expediente ou requisição autuada que tramita no Siga-Doc. | `id_processo: integer`, `numero_processo: string (YYYY.NNNN-SD)`, `assunto: text`, `data_autuacao: datetime`, `status_processo: string`, `id_requerente: integer (FK)`, `id_responsavel: integer (FK)` | `id_processo` (PK), `numero_processo` (UK) | 4 registros | Form de Entrada / Mock Data | Sim |
| **PrazosProcesso** | O cronômetro e as regras de tempo associadas a cada processo. | `id_prazo: integer`, `id_processo: integer (FK)`, `dias_concedidos: integer`, `data_limite: datetime`, `percentual_decorrido: float`, `sinalizador_visual: string (VERDE/AMARELO/VERMELHO)`, `cobranca_disparada: boolean` | `id_prazo` (PK) | 4 registros | Motor de Prazos | Sim |
| **Documento** | As minutas, pareceres, anexos e despachos vinculados ao processo. | `id_documento: integer`, `id_processo: integer (FK)`, `tipo_documento: string`, `conteudo_texto: text`, `data_criacao: datetime`, `id_autor: integer (FK)`, `assinado: boolean` | `id_documento` (PK) | ~8 registros | Módulo de Instrução | Sim |
| **LogAuditoria** | O registro inalterável de eventos, notificações e envios de cobrança (*dunning*). | `id_log: integer`, `id_processo: integer (FK)`, `tipo_evento: string`, `descricao_acao: text`, `data_hora: datetime`, `disparado_por_maquina: boolean` | `id_log` (PK) | ~15 registros | Automação / Eventos do sistema | Sim |

**O que precisa ser coletado:** Os alertas de prazos e as mensagens automáticas e a mensagem de solicitação de restituição dos documentos dentro do prazo. 
**Quem libera o acesso:** O servidor com acesso ao sistema Siga Doc, e joga no app.

### Fontes de dados do processo real


## 5. Regras de negócio (RN01, RN02...)

| ID | Regra | Quando se aplica | Exceção | Quem valida | Tipo |
|---|---|---|---|---|---|
| **RN01** | Se a solicitação não contiver todos os anexos obrigatórios cadastrados para o tipo de requisição, o envio é recusado. | Cadastro e Entrada de novas solicitações pelo requerente. | Nenhuma exceção. | Sistema (Formulário) | Validação |
| **RN02** | Se a solicitação for enviada com sucesso, o sistema deve gerar automaticamente um número único de autuação no formato `YYYY.NNNN-SD`. | Confirmação da autuação do expediente no Siga-Doc. | Nenhuma exceção. | Sistema (Automação) | Cálculo |
| **RN03** | Apenas servidores ativos e vinculados à lotação de destino do processo podem alterar a atribuição do responsável técnico. | Módulo de Atribuição e Triagem da Mesa Virtual. | Administrador geral do sistema. | Sistema (Controle de Acesso) | Validação |
| **RN04** | Se o analista selecionar uma minuta padronizada, o sistema deve preencher automaticamente os campos cadastrais do processo no texto. | Tramitação e Instrução do processo (redação de pareceres/despachos). | Se o analista optar por criar um documento em texto livre sem template. | Sistema (Módulo de Instrução) | Validação |
| **RN05** | Se o usuário for o requerente do processo, ele não pode ser atribuído como analista nem assinar como autoridade decisora no mesmo feito (Segregação de Funções - SoD). | Atribuição de responsável e Assinatura/Conclusão do processo. | Nenhuma exceção. | Sistema (Regra de Governança) | Validação |
| **RN06** | Se o percentual de tempo decorrido atingir ou ultrapassar 70% do prazo limite, o indicador visual do processo na Mesa Virtual deve mudar para a cor Amarela. | Monitoramento e cálculo contínuo do cronômetro de prazos. | Processos com prazo suspenso ou já concluídos. | Sistema (Motor de Prazos) | Cálculo |
| **RN07** | Se o tempo decorrido atingir 100% do prazo limite sem a juntada da resposta exigida, o status do prazo deve ser alterado para 'Vencido' e o indicador deve mudar para a cor Vermelha. | Estouro do tempo limite do cronômetro regimental. | Processos com prazo suspenso por decisão motivada. | Sistema (Motor de Prazos) | Cálculo |
| **RN08** | Se o processo atingir o status 'Vencido' por pendência de terceiros, o sistema deve disparar automaticamente um e-mail/notificação de cobrança (*dunning*) ao destinatário registrado. | Momento exato da virada de status do prazo para 'Vencido'. | Se a opção de envio automático de cobrança for desativada manualmente pelo gestor da lotação. | Sistema (Motor de Automação) | Cálculo |
| **RN09** | Se o despacho final não possuir uma assinatura digital válida do perfil Autoridade Decisora, o encerramento do processo é bloqueado. | Etapa de Conclusão e deliberação final do feito. | Nenhuma exceção. | Sistema (Módulo de Decisão) | Cálculo |
| **RN10** | Se o processo for assinado e concluído pela Autoridade Decisora, o sistema deve disparar a notificação do resultado ao requerente e alterar o estado do feito para 'Arquivado'. | Conclusão e arquivamento final do processo. | Nenhuma exceção. | Sistema (Automação) | Cálculo |


## 6. Telas (#/painel, #/lista...)


## 7. KPIs (nome = fórmula em uma linha)

| KPI | Pergunta | Fórmula | Fonte | Linha de base | Valor esperado | Como medir |
|---|---|---|---|---|---|---|
| Tempo Médio de Atribuição (TMA) | Quanto tempo um processo fica parado na fila da lotação antes de ser distribuído a um analista? | (∑▒("data_atribuicao" -"data_autuacao" ) )/"Total de Processos Atribuídos"   | Mesa virtual/ atribuição | 10 dias | menor que 10 dias | Calcular a diferença média entre os timestamps de autuação e de vinculação do responsável no painel. |
| Eficiência na Sinalização Preditiva (Alertas Amarelos) | Os alertas visuais de 70% do prazo estão permitindo agir antes que o processo vença? | "Processos Concluídos no Status Amarelo" /"Total de Processos que Atingiram 70%"  x 100 | Motor de prazo | 10% das ações majoritárias  | maior igual a 75% | Filtrar processos que passaram pelo estado 'Amarelo' (RN06) e foram finalizados antes de atingir o 'Vermelho'. |
| Taxa de Sucesso da Cobrança Automática | Qual o percentual de e-mails de cobrança disparados pela máquina sem necessidade de cobrança manual? | "E-mails de Cobrança Disparados pela Máquina" /"Total de Processos Vencidos por Terceiros"  x 100 | Log de auditoria e cobrança | 0% | 100% | Consultar na tabela LogAuditoria os registros de eventos do tipo 'Cobrança Automática' (RN08) com flag de máquina ativo |

**Período da linha de base:** Todos os registros do ano por pagina
**Campos de data e tempo que existem:** A planilha possuí apenas a data, sendo contabilizados o período apenas por dias corridos.

## 8. Stack: HTML único (CSS/JS inline), dados em JSON embutido, GitHub Pages.

**Stack escolhida:** Ainda não definido
**Detalhe da stack:** -
**Hospedagem:** Acesso Multiperfil Instantâneo: Disponibiliza uma URL pública segura (HTTPS) para que os diferentes perfis de teste, custo zero, Execução Funcional do Motor de Prazos: Permite rodar o cronômetro automático, atualizar a cor dos sinalizadores (Verde/Amarelo/Vermelho) e efetuar o disparo real dos e-mails de cobrança automatizada (dunning) por serviços como SMTP/Nodemailer sem bloqueios de firewall local.
**Custo e licenças:** Sem custo, não possuímos recurso para o desenvolvimento aplicação da ferramenta.
**Contas e domínio:** O aluno cria conta e encaminha para o professor que compartilha o projeto no GitHub.

| Opção | Tipo | Onde roda | Custo | Quem mantém | Acesso | Banco de dados | Escala | Limitação |
|---|---|---|---|---|---|---|---|---|
| Sandbox Cloud Pública (PaaS - Vercel / Render / Supabase) | Nuvem corporativa | Servidores em nuvem (PaaS gratuita / Free Tier) | R$ 0 | Provedor / Time do Projeto | URL pública web (HTTPS) com controle de acesso | PostgreSQL Gerenciado em Nuvem (ex: Supabase) | Suporta dezenas de usuários simultâneos | Modo "Hibernação": Serviços no Free Tier entram em suspensão por inatividade, podendo atrasar a primeira requisição ou a execução precisa do cronjob em horários exatos. |


## 9. Restrições e LGPD

**Restrições:** Os usuários não autorizados, não podem excluir documentos já cadastrados.
**Dados pessoais tratados:** Dados do servidor que cadastra e é responsável pelo tramite da documentação e a lotação que é enviada.
**Base legal:** Atendimento ao Interesse Público: O tratamento decorre do exercício do poder de dever da administração pública de instruir e decidir processos sob sua custódia, conforme o Art. 7º, III da LGPD.  Atendimento aos Princípios do Art. 6º da LGPD:  Finalidade e Adequação: Limitação estrita dos dados coletados às 5 etapas do ciclo de vida processual.  Necessidade (Minimização): Coleta restrita ao mínimo indispensável para autuar, tramitar, notificar e deliberar, sem o uso de dados sensíveis no MVP.
**Retenção:** Dados permanecem do app mesmo após fechar o navegador.
**Acesso e registro:** Somente os usuários do setor, registrando os dados de acesso dos usuários.
**Requisitos marcados:** LGPD e dado pessoal, Segurança e controle de acesso, Funcionar offline, Integração com sistema oficial

---

# Anexo A — AS-IS (o fluxo de hoje)

**Início:** Cadastro de processo 
**Fim:** Tramitação para o destinatário final ou arquivamento de processo, (conclusão do processo).
**Entradas:** -
**Saídas:** -
**Volume:** 200
**Duração:** -
**Frequência:** Mensal
| Etapa | Quem faz | O que entra | Ação | O que sai | Sistema | Regra | Onde espera | Tempo (h) | Automatizável |
|---|---|---|---|---|---|---|---|---|---|
| Cadastro | Servidor que recebe o documento no sistema | Processo ou expediente eletronico | Lançamento no app | Processo formalizado e autuado | sistema app | Verificar se documentação mínima está completa para autuação | no app |  | Sim, com apoio humano |
| Atribuição | Servidor que faz o cadastro | Processo sem andamento | Analisar o documento, elaborar despacho ou ofício  para validação para autuação | Parecer, despacho ou ofício elaborado | Sistema app | Regra de distribuição por competência | no app |  | Sim, com apoio humano |
| Tramitação e Instrução | Servidor responsável | Processo atribuído para análise | Analisar o feito, confeccionar despacho ou ofício | Despacho ou ofício validado | Sistema SIGA DOC | Verificar se o conteúdo do documento é administrativo ou jurídico | no app |  | Sim, com apoio humano |
| Acompanhamento e Prazos | Sistema / Controle de Prazos | Processo aguardando resposta de ou lotação ou a validação da chefia imediata | Monitorar permanência, controlar prazos vigentes e cobrar pendências | Alertas de prazo e notificações de cobrança | Sistema app | Validação do transcurso do prazo regimental ou recebimento de resposta externa | no app, Aguardando resposta de órgãos externos/internos ou término do prazo |  | Sim, com apoio humano |
| Conclusão | Servidor | Processo instruído e analisado | Tomar decisão final, assinar, tramitar para saída ou arquivar | Processo concluído, decisão emitida e feito arquivado | Sistema | alidação da instrução para deferimento/indeferimento e assinatura final | Fila da autoridade aguardando assinatura final ou processamento do arquivo |  | Sim, com apoio humano |

**Decisões e aprovações:** Validação na Entrada
Documentação Completa? 
Presença dos requisitos e documentos mínimos no cadastro.
• Sim: Autua e segue para Atribuição.
• Não: Devolve ao solicitante para correção.

 Instrução do Processo
Exige Parecer Externo/Terceiros?
Necessidade técnica ou legal de consultar outros órgãos/unidades.
• Sim: Emite ofício e vai para Acompanhamento de Prazos.
• Não: Elabora parecer/despacho final.

Controle de Prazos
Resposta Recebida no Prazo?
Retorno de terceiros dentro do limite do prazo regimental.
• Sim: Anexa resposta e retorna para análise.
• Não: Dispara cobrança/alerta e/ou aplica decurso de prazo.


Decisão Final
Pedido Deferido / Aprovado?
Cumprimento das regras de negócio e mérito do processo.
• Sim: Emite aprovação, tramita ou arquiva.
• Não: Emite analisa, despacha novamente e acomapanha.


**Exceções:** Descrição Geral de Caminhos Alternativos e Exceções
O fluxo principal do processo assume a tramitação contínua e sem pendências desde a entrada até o arquivamento. Contudo, para garantir o tratamento adequado de desvios operacionais e eventos de exceção, preveem-se as seguintes rotas condicionais:

1. Caminhos Alternativos
Pendência de Documentação (Entrada): Caso o expediente seja autuado com dados incompletos ou falta de anexos obrigatórios, o fluxo principal é pausado e gera-se uma notificação de exigência ao requerente, aguardando a complementação para prosseguir à fase de atribuição.

Redistribuição por Indisponibilidade (Atribuição): Se o servidor designado estiver ausente (férias, licenças) ou com excesso de carga de trabalho, o processo é retrabalhado para atribuição secundária ou remanejado automaticamente para um substituto.

Consultas Técnicas Intermediárias (Instrução): Quando a análise exigir validação técnica ou parecer jurídico complementar de outra unidade interna, o processo é temporariamente encaminhado para instrução concorrente antes do despacho decisório.

Prorrogação de Prazo (Acompanhamento): Havendo solicitação motivada do interessado ou de órgãos externos, o tempo de permanência é suspenso e um novo prazo limite é repactuado no sistema.

2. Exceções e Tratamento de Erros
Incompetência do Setor: Processos protocolados indevidamente no setor são sumariamente declinados e redirecionados ao órgão competente ou cancelados por falta de amparo regimental.

Decurso de Prazo sem Resposta: Findo o prazo regimental sem manifestação de terceiros e após alertas automáticos de cobrança, o feito retorna ao analista para decisão no estado em que se encontra ou arquivamento por abandono.

Fase Recursal: Caso haja contestação do requerente após a decisão de indeferimento na fase de conclusão, o feito é reaberto e retorna à etapa de instrução para análise em instância superior.
**Já digitalizado:** A entrada da documentação, ofícios, requerimentos, pedidos, convites via Siga Doc, e  e-mails e Ofícios Eletrônicos, fazemos um controle de gestão de documentos em um app que funciona basicamente como uma automação de planilha de Excel.

# Anexo B — TO-BE (o fluxo depois da mudança)

**Visão do futuro:** Quando este processo existir, os servidores da lotação deixam de conferir manualmente os prazos na mesa virtual do Siga-Doc e passam a contar com a gestão de documentos integrada, monitoramento automatizado, alertas de prazos, notificações preditivas e geração automática de cobranças para processos pendentes de resposta.
**Mudança principal:** A mesa virtual do Siga-Doc deixa de ser um mero repositório passivo de documentos e passa a controlar os prazos de forma ativa e automática.

Em termos práticos: a gestão do tempo e a cobrança de documentos pendentes saem da memória e do controle manual dos servidores da lotação e passam a ser executadas diretamente pela inteligência do sistema.
**O que fica igual:** A responsabilidade técnica e o julgamento humano: Os servidores da lotação e a autoridade decisora continuam sendo os únicos responsáveis por analisar o mérito dos documentos, elaborar os pareceres e tomar as decisões finais (o sistema não decide nem assina pelo servidor).

O uso do Siga-Doc como sistema oficial: O Siga-Doc permanece como a plataforma principal de gestão documental e tramitação do órgão.

A estrutura de papéis e alçadas: A hierarquia de aprovação, as competências regimentais de cada servidor e a exigência de assinatura legal não mudam.

A necessidade de prazos regimentais e normas: As regras de negócio, legislações aplicáveis e os prazos limite estabelecidos por norma continuam válidos.
**O que não pode mudar:** O Livre Convencimento e a Análise Técnica (Atribuição Legal do Servidor): A automação não pode substituir a interpretação humana, a discricionariedade administrativa ou a valoração de mérito na confecção de pareceres, despachos e relatórios.

A Competência Exclusiva para Decisão (Alçada da Autoridade): O ato administrativo final (deferimento, indeferimento, homologação ou sanção) precisa obrigatoriamente ser assinado pela autoridade competente legalmente constituída. A máquina não pode tomar decisões finais de mérito.
As Normas de Temporalidade e Arquivamento Público: A tabela de temporalidade documental, as regras de classificação de sigilo/LGPD e a obrigatoriedade de conservação do histórico do processo no Siga-Doc continuam sendo imposições legais inalteráveis.
**Piloto do TO-BE:** Na unidade de lotação Gabinete de Direção, plano piloto de 30 dias comparando a gestão antiga com a atual.

# Anexo C — Pesquisa, riscos e plano

**Hipótese de campo:** A conferência manual de documentos e do cumprimento de prazos consome tempo excessivo dos servidores, gargalo que será eliminado ao automatizar a verificação visual dos prazos e a triagem das minutas padronizadas.
| Referência | Tipo | Fonte ou link | Ano | Dado que extrai | Como usar na defesa | Link conferido |
|---|---|---|---|---|---|---|
| PORTARIA Nº 07/2024/DG/POLITEC, de 24 de Julho de 2024  | Dado oficial | https://www.politec.mt.gov.br/publicacoes-oficiais | 2024 | Designação dos membros que compõem a Comissão de Ética Pública no âmbito da Perícia Oficial e Identificação Técnica - POLITEC/MT, e da outras providências.  | Alinhar o projeto às metas nacionais de eficiência, governo 100% digital e automação de serviços. | Não |

**Lacunas:** A resposta exata de comportamento;
O que precisa ser verificado: Realizar testes de estresse (load testing) na fase de sandbox simulando volume superior à linha de base (acima de 500 autuações/mês) para garantir a estabilidade do banco relacional.

| Marco | Data | Responsável | Depende de | Situação |
|---|---|---|---|---|
| Planejamento de matrizes e regras da gestão | 29/10/2026 | Vitória Araújo Dias | Renato (professor) | Planejado |

| Risco | Probabilidade | Impacto | Mitigação |
|---|---|---|---|
| Suspensão/Hibernação do serviço no ambiente PaaS gratuito (Free Tier) | Alta | Alto | Configurar uma rotina externa de ping (ex.: UptimeRobot) com requisições periódicas para manter a aplicação continuamente ativa e garantir a execução exata do cronjob de prazos. |

**Apoio necessário:** Preciso realizar os lançamentos de dados para automação do controle de prazos, alinhar com a chefia.
**Aprendizado necessário:** Modelagem do processo, medida de espera, leitura de documento por imagem, GitHub e Antigravity.

# Anexo D — A defesa

**Frase de defesa:** Modelagem do processo, medida de espera, leitura de documento por imagem, GitHub e Antigravity.
**Provas:** Três Evidências de Sustentação
Gargalo no Trâmite (Lead Time de 15 dias): O processo fica parado em média 48 horas apenas na fila de triagem aguardando distribuição manual.

Alto Refugo na Entrada (60% de erros): Seis em cada dez requerimentos chegam com anexos faltantes, e 100% dos despachos são redigidos manualmente do zero (0% de padronização).

Exigência Legal e Social (LAI / Governo Digital): O descumprimento de prazos e a falta de rastreabilidade são as principais causas de insatisfação do cidadão no serviço público.
**Piloto:** Testar o piloto em uma semana, medindo o tempo de duração e a taxa de retorno do formulário.
**Maior risco:** Inclusão de um campo novo (função), manter o formulário atual para a conferencia do novo campo.

# Anexo E — Documentos enviados

**Descrição dos documentos:** Controle de tramitação de processos e expedientes, entrada, saída e atribuição no Excel.
**O que ainda falta:** Falta o modelo To-BE.
