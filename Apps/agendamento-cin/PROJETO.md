# PROJETO.md — Agendamento CIN

**Aluno ou equipe:** Elthon Teixeira
**Unidade:** Identificação Civil
**Contato:** elthonteixeira@politec.mt.gov.br
**Projeto:** Agendamento CIN
**Tipo de projeto:** Aplicativo web / portal
**Data:** 2026-10-27
**Resumo:** Sistema de agendamento aos postos de identificação ( postos próprios) por meio do google script.

## 1. Problema (a dor)

**Problema:** Hoje o sistema de agendamento existente é fragmentado e não padronizado, cada unidade utiliza o google agendas.
**Impacto:** o processo demora varios minutos alem de nao entregar muito informação para equipe, como a taxa de cancelamento ou comparecimento 
**Quem sofre:** Cidadão externo, Servidor da unidade, Chefia
**Como é feito hoje:** O cidadão liga para a unidade e a enviado a pessoa um link que dá acesso ao google agendas, e a equipe não tem acesso fácil ao sistema de informações do agendamento e o cidadão não um sistema intuito e moderno. 
**Evidências:** Entrevista com a equipe
**Detalhe da evidência:** Informação retirada de conversa com a equipe de uma unidade do interior do estado
**O que não pode ser automatizado:** a parte de analise documental e solicitação, devido a complexidade, porem a parte de agendamento pode ser melhorada.

## 2. Objetivo do MVP (o que faz e o que NÃO faz)

**Objetivo do MVP:** Comprovar que o cidadão consegue agendar a CIN e que o posto consegue gerenciar a agenda de forma simples e segura.
**O que o MVP não faz:** Não integra automaticamente com o SIC ou outros sistemas oficiais.
Não valida documentos nem emite a CIN
Não oferece análises avançadas ou relatórios gerenciais complexos.

**Entregável do projeto:** Protótipo funcional de agendamento da CIN, desenvolvido com Google Apps Script e Google Planilhas, para um ou dois postos, expansível para até 10
**Dentro do escopo:** Cadastro de postos, horários e vagas.
Calendário público para agendamento.
Formulário com CPF e e-mail opcionais.
Geração de protocolo e confirmação por e-mail.
Painel do posto para gerenciar reservas e registrar comparecimento.
Painel da Gestão com indicadores básicos
**Fora do escopo:** Integração com sistemas oficiais da Politec, por depender de autorização e acesso técnico.
Envio de SMS ou WhatsApp, para reduzir custos.
Implantação simultânea nos 10 postos, pois o piloto será gradual.
Aplicativo móvel próprio (site), porque o acesso será pelo navegador
**Plataforma alvo:** Site web (abre no navegador)
**Primeira tela:** Página pública para selecionar posto, data e horário disponíveis.
**Simulado no MVP:** Dados fictícios de cidadãos e postos
**Critério de aceite:** O cidadão conclui um agendamento e recebe o protocolo; o posto visualiza a reserva, cancela e registra o comparecimento; duas pessoas tentando a última vaga ao mesmo tempo não geram reserva duplicada.
**Dados de exemplo:** Pelo menos 10 agendamentos fictícios, incluindo casos de cancelamento, ausência e comparecimento.
**O que já existe pronto e pode ser reaproveitado:** Apenas o google agenda, será feito do zero o sistema sem reaproveitamento
**Dependências:** das diretorias de identificação e interiorização

## 3. Usuários e papéis

| Papel | Quem é | O que enxerga | O que faz | O que não pode fazer | Registro |
|---|---|---|---|---|---|
| cidadao  | pessoa que solicita o atendimento | postos, horarios | agendar e consultar a sua reserva | acessar dados de terceiros | agendamento e protocolo |
| posto | servidor | agenda e agendamentos  | configurar os horarios e administrar | acessar dados de outros postos sem o perfil | alteracoes e cancelmentos |
| gestao | responsavel pela administracao do sistema | dados operacionais | gerenciar postos | alterar registros | alterar administracoes |

**Observações sobre os papéis:** O cidadão não tem login: consulta a reserva pelo protocolo e pelo telefone ou pelos 4 últimos dígitos do CPF. Posto e gestão entram com a conta Google institucional.

## 4. Dados (entidades e colunas; tudo SINTÉTICO)

| Entidade | O que representa | Colunas | Chave | Volume | Origem | Sintético |
|---|---|---|---|---|---|---|
| postos | unidade de atendimento | posto_id: texto, nome: texto, município: texto, endereço: texto, e-mail: texto, ativo: booleano | posto_id | 2 a 10 | Cadastro de teste | Parcialmente |
| Disponibilidade | Horários e vagas | horario_id: texto, posto_id: texto, data: data, hora: hora, capacidade: inteiro, situação: texto | horario_id | 50 a 200 | Gerado para testes | Sim |
| Agendamentos | Reservas dos cidadãos | protocolo: texto, posto_id: texto, horário_id: texto, nome: texto, CPF: texto opcional, e-mail: texto opcional, status: texto | protocolo | 10 a 100 | Dados fictícios | Sim |
| Usuários | Servidores e perfis | usuario_id: texto, e-mail: texto, perfil: texto, posto_id: texto, ativo: booleano | usuario_id | 2 a 15 | Usuários de teste | Sim |

**O que precisa ser coletado:** Atualmente, o sistema de agendamento ainda não possui uma base consolidada de horários, vagas, reservas e comparecimento. Proposta: criar uma planilha central e registrar os agendamentos, cancelamentos e comparecimentos durante quatro semanas de piloto, utilizando inicialmente um ou dois postos.
**Quem libera o acesso:** A equipe de TI institucional deverá autorizar o uso das ferramentas e a publicação do sistema. A Gestão indicará os postos participantes e os servidores autorizados antes do início do piloto. O acesso será validado antes da utilização de dados reais, começando os testes com dados fictícios.

### Fontes de dados do processo real

| Fonte | Tipo | Onde | Existe | Uma linha é | Volume | Campos de data | Atualiza | LGPD |
|---|---|---|---|---|---|---|---|---|
| Agendamentos | Não existe ainda | Google Sheets (a criar) | Não | Um agendamento | A coletar | Data e horário agendados; criação e cancelamento | A cada agendamento | Sim |
| Disponibilidade | Não existe ainda | Google Sheets (a criar) | Não | Um horário por posto | A coletar | Data, hora inicial e final | Conforme configuração da agenda | Duvidaso |
| Comparecimento | Não existe ainda | Google Sheets (a criar) | Não | Um atendimento agendado | A coletar | Data agendada e data/hora do registro de presença | A cada atendimento | Sim |
| Postos e usuários | Não existe ainda | Google Sheets (a criar) | Não | Um posto ou usuário | A coletar | Criação e atualização do cadastro | Quando houver alteração | Duvidaso |


## 5. Regras de negócio (RN01, RN02...)

| ID | Regra | Quando se aplica | Exceção | Quem valida | Tipo |
|---|---|---|---|---|---|
| RN01 | Só exibir postos ativos. | Seleção de posto | Nenhuma | Sistema | Validação |
| RN02 | Exibir somente horários abertos e com vagas. | Consulta de calendário | Nenhuma | Sistema | Negócio |
| RN03 | Gerar protocolo único para cada reserva | Confirmação | Nenhuma | Sistema | Validação |
| RN04 | Impedir reservas acima da capacidade. | Confirmação da reserva | Nenhuma | Sistema | Validação |
| RN05 | O posto só gerencia sua própria agenda. | Área restrita | Gestão conforme autorização | Sistema | Acesso |
| RN06 | Um agendamento ativo por telefone (ou CPF) em cada posto | Na reserva | Nenhuma | Sistema | Validação |
| RN07 | Cancelamento pelo cidadão até 2 h antes; a vaga volta para o calendário | No cancelamento | Posto pode cancelar a qualquer momento, com motivo | Sistema | Negócio |
| RN08 | Tolerância de 15 minutos; depois o posto marca ausente | No dia do atendimento | Decisão do posto | Servidor do posto | Negócio |
| RN09 | Agendamento com 1 a 30 dias de antecedência | Na consulta de vagas | Nenhuma | Sistema | Validação |
| RN10 | Dados do cidadão apagados 90 dias após o atendimento; ficam as contagens | Rotina diária | Nenhuma | Gestão | LGPD |


## 6. Telas (#/painel, #/lista...)

| Rota | Tela | Objetivo | Quem usa | Dados | Ação | Regra | Tipo | Verificável como | MVP |
|---|---|---|---|---|---|---|---|---|---|
| #/agendar | Agenda | reservar horario | cidadao | escolher posto, data e horario | selecionar vaga | exbir somente vagas disponiveis | Tela | Executar a ação com dados fictícios | Sim |
| #/agendar/dados | Confirmar | registar rserva | cidadao | nome, CPF.email como opcional | confimar vaga | gerar protocolo | Tela | Executar a ação com dados fictícios | Sim |
| #/posto | Painel do posto | administar agenda | servidor | horarios e agendamento da unidade | criar horarios, cancelar | acesso restristo | Tela | Executar a ação com dados fictícios | Sim |
| #/gestao | Painel de gestao | acompanhar unidades | gestao | postos, reservas | consultar indicadores | acesso autorizado | Tela | Executar a ação com dados fictícios | Sim |
| #/comprovante/:protocolo | Comprovante | Mostrar a reserva confirmada | Cidadão | Protocolo, posto, data, horário, documentos | Imprimir ou cancelar | RN03 | Tela | Comprovante aparece logo após reservar | Sim |
| #/consultar | Consultar reserva | Consultar ou cancelar sem login | Cidadão | Protocolo e telefone ou 4 últimos dígitos do CPF | Consultar e cancelar | RN07 | Tela | Cancelamento devolve a vaga | Sim |
| #/posto/horarios | Grade de horários | Criar horários e vagas | Servidor do posto | Dias, horários, vagas, bloqueios | Gerar e bloquear horários | RN05 | Tela | Gera 2 semanas de horários | Sim |


## 7. KPIs (nome = fórmula em uma linha)

| KPI | Pergunta | Fórmula | Fonte | Linha de base | Valor esperado | Como medir |
|---|---|---|---|---|---|---|
| Taxa de ocupação das vagas | Qual percentual das vagas disponibilizadas foi ocupado? | (Agendamentos confirmados ÷ Vagas disponibilizadas) × 100 | Planilha de disponibilidade e agendamentos | A levantar na semana 1 | ≥ 70% das vagas ocupadas | Comparar o total de vagas abertas com os agendamentos confirmados no período |
| Taxa de comparecimento | Qual percentual dos cidadãos agendados compareceu? | (Agendamentos com comparecimento registrado ÷ Agendamentos com atendimento previsto no período) × 100 | Planilha de agendamentos e registro de comparecimento | A levantar na semana 1 | ≥ 85% de comparecimento | Registrar os cidadãos que compareceram e os que não compareceram, calculando o percentual ao final da semana |
| Taxa de cancelamento | Quantas reservas são canceladas? | Cancelados ÷ agendamentos × 100 | Aba agendamentos | A levantar na semana 1 | Abaixo de 15% | Contar os cancelados na semana |
| Tempo para agendar | Quanto tempo o cidadão leva para marcar? | Hora do protocolo − hora da abertura do link | Log do app | Vários minutos por telefone (informado) | Menos de 3 minutos | Amostra de 20 agendamentos |

**Período da linha de base:** O projeto-piloto do Sistema de Agendamento da Carteira de Identidade Nacional (CIN) ainda não possui uma base histórica consolidada de agendamentos, ocupação de vagas e comparecimento dos cidadãos.

A linha de base será estabelecida a partir da coleta de dados durante a primeira semana de funcionamento do piloto, inicialmente em um ou dois postos de identificação. Serão registrados o número de vagas disponibilizadas, agendamentos realizados, cancelamentos e comparecimentos.
Os resultados das quatro semanas de teste permitirão avaliar a utilização do sistema e estabelecer parâmetros para uma possível expansão a outros postos de identificação de Mato Grosso.
**Campos de data e tempo que existem:** No projeto-piloto do Sistema de Agendamento da CIN, serão previstos campos de data e horário para registrar as etapas do agendamento. A estrutura proposta contempla a data e o horário agendados, a data e hora da criação da reserva, a data e hora de eventuais cancelamentos e o registro do comparecimento do cidadão.

Esses dados serão armazenados no Google Sheets e gerenciados pelo Google Apps Script. Como o sistema ainda será desenvolvido, esses campos precisam ser implementados e validados durante os testes.
Com esses registros, será possível medir a quantidade de agendamentos por período, a ocupação das vagas, os cancelamentos, o comparecimento e o tempo entre o agendamento e a data prevista para o atendimento. A medição do tempo efetivo de espera no posto exigirá também o registro do horário de chegada do cidadão e do início do atendimento.

## 8. Stack: HTML único (CSS/JS inline), dados em JSON embutido, GitHub Pages.

**Stack escolhida:** Planilha com automação
**Detalhe da stack:** Um único index.html (CSS e JS embutidos) servido pelo Google Apps Script (HtmlService), com as áreas do cidadão, do posto e da gestão. Dados no Google Planilhas. A reserva passa por LockService para não ultrapassar a capacidade. O painel do posto guarda a agenda do dia no IndexedDB e envia os registros quando a conexão volta.
**Hospedagem:** opção escolhida é Google Apps Script integrado ao Google Sheets, por permitir desenvolver e disponibilizar o Sistema de Agendamento da CIN como uma aplicação web acessível por link, sem necessidade de contratar inicialmente um servidor ou banco de dados externo.
**Custo e licenças:** O projeto-piloto utilizará o Google Apps Script e o Google Sheets, ferramentas que podem ser utilizadas sem custo adicional de licenciamento, desde que a instituição disponha de contas compatíveis e o uso permaneça dentro das cotas e dos limites aplicáveis.
**Contas e domínio:** A criação ou disponibilização da conta institucional, a autorização para uso do Google Apps Script e do Google Sheets e a definição das permissões de publicação deverão ser realizadas ou autorizadas pela equipe institucional de TI da Politec/MT, conforme as políticas de segurança vigentes.

| Opção | Tipo | Onde roda | Custo | Quem mantém | Acesso | Banco de dados | Escala | Limitação |
|---|---|---|---|---|---|---|---|---|
| Google Apps Script + Google Sheets | Plataforma como serviço | Infraestrutura em nuvem do Google | Sem custo adicional inicial, sujeito a cotas e limites | Desenvolvedor e equipe institucional de TI | Link público para cidadãos e acesso restrito para servidores | Google Sheets | Adequada para piloto de 1 a 2 postos, expansível para até 10 após testes | Limites de execução, cotas, concorrência e dependência das permissões institucionais |
| Firebase + aplicação web | Plataforma como serviço | Infraestrutura Firebase/Google Cloud | Plano gratuito limitado; custos podem surgir conforme o uso | Desenvolvedor e equipe de TI | Acesso público e autenticação de servidores | Cloud Firestore | Maior potencial de expansão | Exige autorização institucional para criação do projeto, configuração de segurança e possível cobrança |
| Hospedagem web tradicional | Servidor interno | Servidor contratado ou institucional | Variável, conforme infraestrutura | Equipe de TI ou fornecedor | Link público e área restrita | Banco de dados contratado ou institucional | Depende dos recursos contratados | Exige configuração, manutenção, segurança e administração do servidor |
| GitHub Pages | Estática e gratuita | Infraestrutura do GitHub | Gratuito para uso compatível com o serviço | Desenvolvedor | Link público | Não possui banco de dados próprio | Adequada para páginas estáticas | Não executa diretamente a lógica de reservas nem protege operações administrativas sem um backend externo |


## 9. Restrições e LGPD

**Restrições:** Limites do Google: cotas de execução, envio de e-mails e acessos simultâneos.
Internet: necessária para cidadãos e servidores acessarem o sistema.
Segurança e LGPD: controle de acesso e proteção dos dados pessoais.
Escopo: início em um ou dois postos, com expansão condicionada aos testes.
Regras oficiais: validação dos procedimentos de agendamento pela Gestão
**Dados pessoais tratados:** Nome completo e, opcionalmente, CPF, e-mail e telefone do cidadão. Também serão tratados e-mails institucionais e registros de ações dos servidores.
**Base legal:** organizar o agendamento de atendimentos da CIN. A base legal aplicável deverá ser validada pela instituição e pelo encarregado de proteção de dados antes do uso real.
**Retenção:** Durante o piloto, utilizar dados fictícios. Para produção, estabelecer prazo de retenção e descarte conforme as normas institucionais, obrigações legais e orientações do encarregado de dados.
**Acesso e registro:** Cidadão: realiza o agendamento e acessa apenas informações autorizadas sobre sua reserva.
Posto: consulta e gerencia os agendamentos de sua unidade.
Gestão: administra os postos e consulta indicadores consolidados.
Sistema: registra operações relevantes, data, hora e usuário responsável.
**Requisitos marcados:** Acessibilidade, Funcionar offline, LGPD e dado pessoal, Segurança e controle de acesso, Trilha de auditoria

---

# Anexo A — AS-IS (o fluxo de hoje)

**Início:** solicitação de agendamento
**Fim:** Requerente compareceu
**Entradas:** entra informações do cidadão básica: nome, telefone, e-mail ( se houver)
**Saídas:** Data e horário do agendamento
**Volume:** 100 por dia
**Duração:** Vários minutos por agendamento (ligação + envio do link). Informado: "2,5 por hora"; medir no Sprint 0.
**Frequência:** Diário
| Etapa | Quem faz | O que entra | Ação | O que sai | Sistema | Regra | Onde espera | Tempo (h) | Automatizável |
|---|---|---|---|---|---|---|---|---|---|
| Consulta de vagas | Cidadão | Posto desejado | Consulta datas e horários disponíveis | Opção de agendamento | Site ou atendimento presencial | Deve haver vaga disponível | Até encontrar horário disponível | A medir | Sim, com regra clara |
| Solicitação de agendamento | Cidadão | Dados pessoais e horário | Preenche e envia formulário | Solicitação registrada | Formulário ou papel | Campos obrigatórios preenchidos | Durante o preenchimento | A medir | Pouco |
| Verificação da vaga | Sistema ou servidor | Solicitação recebida | Confere disponibilidade | Agendamento validado | Planilha ou conferência manual | Não exceder a capacidade | Até a conferência | A medir | Sim, com regra clara |
| Confirmação | Servidor ou sistema | Solicitação validada | Confirma data e horário | Protocolo de agendamento | E-mail ou comunicação manual | Vaga confirmada | Até o envio da confirmação | A medir | Sim, com regra clara |
| Comparecimento | Cidadão | Confirmação do agendamento | Comparece ao posto na data marcada | Cidadão presente ou ausência | Atendimento presencial | Data e horário agendados | Na chegada ao posto | A medir | Não |
| Registro do atendimento | Servidor do posto | Agendamento e cidadão presente | Registra comparecimento e atendimento | Situação atualizada | Planilha ou sistema | Registrar presença ou ausência | Até o registro pelo servidor | A medir | Pouco |

**Decisões e aprovações:** disponibilidade de agenda/data
**Exceções:** caso a data esteja ocupado, a pessoa poderá escolher outra data
**Já digitalizado:** o processo é digital

# Anexo B — TO-BE (o fluxo depois da mudança)

**Visão do futuro:** Implantar um sistema centralizado de agendamento da CIN
**Mudança principal:** O agendamento passa a ser digital, permitindo ao cidadão escolher o posto, a data e o horário disponíveis por meio de um link, enquanto o sistema automatiza o controle de vagas e confirmações.
**O que fica igual:** As regras oficiais para emissão da CIN e o atendimento presencial permanecem inalterados, assim como as responsabilidades dos servidores dos postos.
**O que não pode mudar:** As exigências legais para emissão da CIN, as normas institucionais, a proteção dos dados pessoais e as atribuições oficiais dos servidores devem ser respeitadas.
| Etapa | O que muda | Quem executa | Benefício | Esforço |
|---|---|---|---|---|
| configurar agenda | definir postos, horarios e vagas | A pessoa assistida pela máquina | padronização | Médio |
| consultar horario | exibir vagas disponiveis | A máquina (automação) | agilidade | Baixo |
| agendar atendimento | cidadao escolhe | A pessoa assistida pela máquina | faciidade  | Baixo |
| gerar indicadores | consolidar dados | A pessoa assistida pela máquina | melhor gestao | Médio |
| Confirmar por e-mail | E-mail com protocolo enviado na hora | A máquina (automação) | Cidadão recebe a confirmação sem ligar | Baixo |
| Cancelar ou remarcar | Cidadão cancela pelo protocolo e a vaga volta | A pessoa assistida pela máquina | Menos vaga perdida | Baixo |
| Registrar comparecimento | Posto marca presença ou ausência no painel, mesmo sem internet | A pessoa assistida pela máquina | Taxa de comparecimento medida | Médio |

**Piloto do TO-BE:** Realizar um piloto de 30 dias em um ou dois postos

# Anexo C — Pesquisa, riscos e plano

**Hipótese de campo:** A implantação do sistema de agendamento da CIN em um ou dois postos deverá reduzir o trabalho manual, facilitar o acesso dos cidadãos às vagas e melhorar o controle dos agendamentos e comparecimentos.
| Referência | Tipo | Fonte ou link | Ano | Dado que extrai | Como usar na defesa | Link conferido |
|---|---|---|---|---|---|---|
| Lei Geral de Proteção de Dados — Lei nº 13.709 | Norma ou lei | Planalto | 2018 | Regras para tratamento de dados pessoais | Fundamentar a proteção dos dados dos cidadãos | Não |
| Lei do Governo Digital — Lei nº 14.129 | Norma ou lei | Planalto | 2021 | Digitalização e eficiência dos serviços públicos | Justificar a proposta de agendamento digital | Não |
| Agendamento nos postos de identificação | Documento interno | Politec-MT | A consultar | Existem diferentes orientações e formas de agendamento por posto | Demonstrar a relevância de avaliar uma solução centralizada | Não |
| Mais de 420 mil CIN emitidas em Mato Grosso em 2025 | Notícia | Politec-MT | 2026 | 429.378 CIN emitidas em 2025 | Contextualizar o volume de atendimento e a importância do serviço | Não |

**Lacunas:** A pesquisa ainda não dispõe de dados consolidados sobre demanda, ocupação de vagas, cancelamentos, faltas e tempo de espera nos postos. Esses indicadores serão coletados durante o piloto de quatro semanas, inicialmente em um ou dois postos. Os resultados serão limitados ao período e às unidades avaliadas, não permitindo generalização para todos os postos de Mato Grosso
| Marco | Data | Responsável | Depende de | Situação |
|---|---|---|---|---|
| Definir requisitos e regras do sistema | A definir | Responsável pelo projeto e Gestão | Validação das regras de agendamento | Em andamento |
| Criar planilha e estrutura de dados | A definir | Responsável pelo projeto | Requisitos definidos | Planejado |
| Desenvolver o sistema em Apps Script | A definir | Responsável pelo projeto | Estrutura de dados pronta | Planejado |
| Realizar testes com dados fictícios | A definir | Responsável pelo projeto | Protótipo funcional | Planejado |
| Validar com a equipe de TI | A definir | TI institucional | Análise de segurança e publicação | Planejado |
| Executar piloto em 1 ou 2 postos | A definir | Gestão e postos participantes | Autorização institucional | Planejado |
| Avaliar resultados após 4 semanas | A definir | Responsável pelo projeto e Gestão | Dados coletados no piloto | Planejado |

| Risco | Probabilidade | Impacto | Mitigação |
|---|---|---|---|
| Falta de autorização da TI | Média | Alto | Solicitar aprovação antes da publicação. |
| Acesso indevido a dados pessoais | Média | Alto | Implementar controle de acesso e validar a segurança. |
| Limites do Google Apps Script | Média | Médio | Realizar testes de desempenho e concorrência. |
| Agendamentos duplicados | Média | Alto | Validar vagas e impedir reservas simultâneas. |
| Baixa adesão dos postos | Média | Médio | Orientar servidores e acompanhar o piloto. |
| Falhas no envio de e-mails | Média | Médio | Exibir protocolo na tela e permitir consulta do agendamento. |

**Apoio necessário:** Gestão: aprovação das regras e indicação dos postos participantes.
**Aprendizado necessário:** - Google Apps Script e JavaScript: desenvolvimento das funcionalidades.
- Google Sheets: estruturação e gerenciamento dos dados.
- HTML e CSS: criação da interface para cidadãos e servidores.
- Segurança e LGPD: controle de acesso e proteção dos dados pessoais.
- Testes: validação de agendamentos simultâneos, permissões e envio de e-mails.
- Publicação: configuração do acesso e implantação com apoio da TI institucional.

# Anexo D — A defesa

**Frase de defesa:** Desenvolver um sistema digital de agendamento da CIN para modernizar o atendimento ao cidadão, otimizar a gestão de vagas e melhorar o controle dos atendimentos nos postos de identificação de Mato Grosso.
**Provas:** 1-Volume de atendimento: Mato Grosso emitiu mais de 429 mil CIN em 2025, demonstrando a relevância do serviço de identificação.

2. Necessidade de organização: o piloto permitirá centralizar horários, vagas, agendamentos, cancelamentos e comparecimentos.

3. Viabilidade técnica: Google Apps Script e Google Sheets permitem desenvolver um protótipo de baixo custo, sujeito à autorização da TI e aos testes de segurança e desempenho.
**Piloto:** Desenvolver um protótipo e testá-lo durante quatro semanas em um ou dois postos de identificação, utilizando inicialmente dados fictícios. Serão avaliados o funcionamento dos agendamentos, o controle de vagas, os cancelamentos, o comparecimento e a facilidade de uso, com análise dos resultados ao final do piloto.
**Maior risco:** O maior risco é a falta de autorização institucional para publicar o sistema e utilizar dados reais

# Anexo E — Documentos enviados

**Descrição dos documentos:** Nenhum documento enviado.
**O que ainda falta:** Grade real de horários e vagas dos postos do piloto; lista dos documentos que o cidadão deve levar; autorização da TI para publicar o app.
