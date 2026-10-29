# PROJETO.md — Classificação da denúncia

**Aluno ou equipe:** Letícia e Thiago
**Unidade:** Comissão de Ética
**Contato:** leticiamesquita@politec.mt.gov.br
**Projeto:** Classificação da denúncia
**Tipo de projeto:** Automação de script ou rotina
**Data:** 2026-10-27
**Resumo:** Uso de IA para agilizar a classificação da denúncia recebida, seguindo o Código de Ética Funcional do Servidor Público Civil do Estado de Mato Grosso

## 1. Problema (a dor)

**Problema:** Morosidade na análise da denúncia e recomendações, que é feita em reunião com a comissão
**Impacto:** A dificuldade de conciliar agenda dos membros, e tempo de duração da reunião em média 1 hora por denúncia com a comissão e 1 hora por oitiva. O tempo demandado é o principal gargalo, uma vez que existe acúmulo de funções, pois os membros todos desenvolvem outras atividades. 
**Quem sofre:** Equipe interna, Servidor da unidade
**Como é feito hoje:** Após o recebimento de denúncia, é realizado agendamento de reunião com a comissão, que depende da disponibilidade dos membros, quando realizada reunião é feita a análise do teor da denúncia para verificação se a mesma será acatada, caso infrinja o código de ética. O processo de classificação é feito nessa reunião, após a classificação são realizadas oitivas para averiguação dos fatos. Após ouvir as partes envolvidas, as recomendações são elaboradas e enviadas aos envolvidos, encerrando o processo.  
**Evidências:** Planilha ou controle local, Documento ou norma oficial
**Detalhe da evidência:** Planilha de denúncias recebidas, atas das reuniões e oitivas e ofícios de recomendações
**O que não pode ser automatizado:** A conferência da classificação, o aceite da denúncia, a oitiva com os envolvidos e conferência das recomendações. 

## 2. Objetivo do MVP (o que faz e o que NÃO faz)

**Objetivo do MVP:** Validar a viabilidade de um sistema para automatizar etapas dos processos da Comissão de Ética da POLITEC/MT, utilizando IA para auxiliar na classificação inicial das denúncias e na elaboração de roteiros de oitivas, mantendo as decisões sob responsabilidade humana.
**O que o MVP não faz:** O MVP não recebe denúncias reais, não acessa sistemas institucionais, não envia notificações oficiais, não realiza autenticação institucional, não mantém histórico oficial de processos e não armazena documentos sigilosos em ambiente de produção. A IA não decide sobre admissibilidade, não determina responsabilidade ética e não substitui as deliberações da Comissão. As funcionalidades serão demonstradas com dados fictícios, para validar o fluxo e a viabilidade da solução.
**Entregável do projeto:** Protótipo funcional de um sistema web para gerenciamento dos processos da Comissão de Ética da POLITEC/MT, contemplando registro de denúncias, classificação inicial assistida por inteligência artificial, acompanhamento das etapas e dos prazos, geração de roteiros de oitivas e modelos padronizados de documentos, com demonstração do fluxo desde o recebimento até o encerramento do processo.
**Dentro do escopo:** Registro e organização das denúncias; classificação inicial assistida por IA; fluxo de análise de admissibilidade; controle das etapas, dos responsáveis e dos prazos; geração assistida de roteiros de oitivas; modelos de comunicações e documentos; registro das deliberações humanas; acompanhamento da tramitação; e demonstração do encerramento do processo. O protótipo utilizará casos fictícios e permitirá validar as funcionalidades e o fluxo proposto.
**Fora do escopo:** A integração com sistemas institucionais, o uso de denúncias reais, a implantação oficial, o envio automático de comunicações, a autenticação institucional e o armazenamento de documentos sigilosos em ambiente de produção ficam fora do MVP. Essas funcionalidades dependem de avaliação técnica, autorização institucional, definição dos requisitos de segurança e proteção de dados e, quando necessário, integração com sistemas existentes. A classificação por IA e a elaboração de roteiros serão testadas em ambiente controlado, sem substituir a análise e as decisões da Comissão.
**Plataforma alvo:** Site web (abre no navegador)
**Primeira tela:** Escolha do perfil (Presidente, Membro, Secretário-executivo) e, em seguida, o painel dos casos por etapa, com prazos.
**Simulado no MVP:** Será simulado desde o registro e a organização inicial das denúncias, a classificação automatizada assistida por inteligência artificial para apoio à triagem e o fluxo de análise de admissibilidade. Além disso, o protótipo apresentará o controle de etapas, responsáveis e prazos, a geração assistida de roteiros para as oitivas, a emissão de modelos padronizados de comunicações e documentos, o registro das deliberações humanas dos membros da comissão, o acompanhamento visual da tramitação do processo e a demonstração final do encerramento com a emissão de relatórios. O envio oficial de e-mails, a autenticação institucional e o armazenamento de documentos sigilosos em ambiente de produção não funcionam de verdade e serão apenas simulados em ambiente controlado com dados de exemplo.
**Critério de aceite:** O usuário consegue registrar uma denúncia fictícia, obter a sugestão de classificação assistida por IA, registrar a deliberação de admissibilidade e gerar um roteiro de oitiva com minutas de documentos, demonstrando o fluxo completo do recebimento ao encerramento do processo sem erros.
**Dados de exemplo:** No mínimo 10 casos fictícios de denúncias contendo relatos, partes envolvidas simuladas, categorização da infração ética, ata de reunião simulada, roteiro de oitiva gerado e minuta do parecer final de recomendação.
**O que já existe pronto e pode ser reaproveitado:** O Código de Ética Funcional do Servidor Público Civil do Estado de Mato Grosso (como base legislativa), os modelos de atas de reuniões, oitivas e ofícios de recomendações em uso pela comissão.
**Dependências:** Depende dos membros da Comissão de Ética para revisão e validação das regras do fluxo e das minutas.

## 3. Usuários e papéis

| Papel | Quem é | O que enxerga | O que faz | O que não pode fazer | Registro |
|---|---|---|---|---|---|
| Administrador do sistema | Servidor responsável pela configuração técnica da solução, se houver essa função específica. | Configurações, usuários, perfis e registros técnicos necessários à administração. | Gerencia acessos, configura perfis e mantém o funcionamento do sistema. | Alterar decisões da Comissão ou acessar o conteúdo sigiloso sem autorização funcional. | Alterações de configuração, concessões de acesso e registros técnicos. |
| Presidente da Comissão | Presidente formalmente designado. | Denúncias, documentos, tramitação, prazos e deliberações, conforme suas atribuições. | Coordena a análise de admissibilidade, convoca reuniões, distribui atividades e acompanha os processos. | Decidir isoladamente questões que dependam de deliberação colegiada ou alterar registros sem rastreabilidade. | Encaminhamentos, despachos, decisões e movimentações realizadas. |
| Membro da Comissão | Integrante formalmente designado. | Denúncias e documentos dos casos distribuídos ou submetidos à Comissão, conforme autorização. | Analisa os casos, participa das reuniões, realiza oitivas quando designado e contribui para pareceres e deliberações. | Acessar casos sem necessidade funcional, compartilhar informações sigilosas ou deliberar individualmente em matérias colegiadas. | Análises, manifestações, participação nas deliberações e atividades realizadas. |
| Secretário(a)-executivo(a) | Servidor responsável pelo apoio administrativo e documental. | Dados necessários à tramitação, documentos, prazos, agendas, atas e comunicações. | Registra denúncias, organiza documentos, agenda reuniões, elabora atas e acompanha prazos e encaminhamentos. | Alterar o conteúdo de decisões colegiadas, deliberar sobre admissibilidade ou divulgar informações sem autorização. | Protocolos, documentos inseridos, atas, notificações e movimentações processuais. |
| Denunciante | Servidor ou pessoa que apresenta uma denúncia à Comissão. | Dados da própria manifestação e informações sobre seu recebimento e andamento que possam ser disponibilizadas. | Registra a denúncia, apresenta informações e documentos e acompanha os retornos autorizados. | Acessar documentos sigilosos, dados pessoais de terceiros ou informações restritas sobre a tramitação. | Data do envio, conteúdo apresentado, documentos anexados e comunicações recebidas. |
| Denunciado(a) | Pessoa cuja conduta é objeto de análise ética. | Comunicações dirigidas a si e informações e documentos disponibilizados formalmente pela Comissão, conforme a fase e as regras aplicáveis. | Apresenta esclarecimentos, manifesta sua versão dos fatos e encaminha informações solicitadas. | Acessar irrestritamente os registros internos, dados de terceiros ou informações protegidas sem autorização. | Notificações, respostas, documentos apresentados e registros de ciência. |

**Observações sobre os papéis:** O sistema deverá respeitar o sigilo das informações, a proteção de dados pessoais e as competências da Comissão de Ética. O acesso aos processos e documentos será restrito conforme o perfil do usuário e a necessidade funcional. As etapas deverão contemplar o registro da denúncia, a análise de admissibilidade, as deliberações colegiadas, as oitivas, os encaminhamentos, a elaboração de pareceres e o encerramento. Todas as movimentações e decisões deverão possuir registro de autoria, data e histórico, assegurando rastreabilidade e integridade das informações. A disponibilização de documentos às partes deverá ocorrer mediante avaliação e autorização da Comissão, observadas as normas aplicáveis e as orientações jurídicas pertinentes.

## 4. Dados (entidades e colunas; tudo SINTÉTICO)

| Entidade | O que representa | Colunas | Chave | Volume | Origem | Sintético |
|---|---|---|---|---|---|---|
| tb_denuncia | Registro e dados da denúncia recebida | id_denuncia: texto, protocolo: texto, data_recebimento: data, relato_fatos: texto, status_etapa: texto, id_denunciante: texto, id_denunciado: texto | id_denuncia | 2 casos/mês | Formulário do protótipo | Sim |
| tb_classificacao_ia | Categorizações e sugestões geradas pela IA | id_classificacao: texto, id_denuncia: texto, categorias_sugeridas: texto, artigos_codigo_etica: texto, resumo_ia: texto, data_geracao: data | id_classificacao | 24 registros/ano | Módulo de IA / Algoritmo | Sim |
| tb_deliberacao | Registros de decisões colegiadas da Comissão | id_deliberacao: texto, id_denuncia: texto, tipo_decisao: texto, justificativa: texto, data_deliberacao: data, membros_presentes: texto | id_deliberacao | 24 registros/ano | Comissão de Ética | Sim |
| tb_oitiva | Roteiros gerados por IA e atas das oitivas | id_oitiva: texto, id_denuncia: texto, pessoa_ouvida: texto, data_oitiva: data, roteiro_perguntas_ia: texto, termo_oitiva: texto | id_oitiva | 48 registros/ano | Tríade / Membros | Sim |

**O que precisa ser coletado:** Hoje não há registro automatizado do tempo exato decorrido entre o recebimento da denúncia por e-mail e a sua classificação inicial, nem métricas consolidadas sobre o tempo gasto na elaboração de roteiros para oitivas. Proposta: registrar a data/hora de entrada do e-mail e a data/hora da validação da classificação pela comissão no sistema durante o piloto de 30 dias para mensurar os ganhos de celeridade.
**Quem libera o acesso:** A Presidência da Comissão de Ética autoriza a consulta à planilha local e às atas no Sigadoc até ao início dos testes do MVP. O docente/coordenador aprova a utilização do protótipo com dados estritamente fictícios na plataforma GitHub Pages durante o período da capacitação.

### Fontes de dados do processo real

| Fonte | Tipo | Onde | Existe | Uma linha é | Volume | Campos de data | Atualiza | LGPD |
|---|---|---|---|---|---|---|---|---|
| Planilha de controle de denúncias | Planilha local | Pasta compartilhada / Controle loca | Sim | Um registro de denúncia ou ocorrência ética | ~2 casos/mês (24/ano)    | Data do recebimento e data das reuniões | Manual / Eventual | Sim |
| Atas de reuniões e oitivas | Relatório | Sigadoc / Pasta compartilhada | Sim | Uma ata de deliberação ou depoimento coletado | ~4 a 6 atas por mês | Data da reunião, data da oitiva | A cada reunião/oitiva realizada | Sim |
| Código de Ética Funcional do Servidor Civil | Relatório | Diário Oficial / Legislação Estadual | Sim | Um artigo, inciso ou dever funcional | 1 código normativo vigente | Data de publicação/vigência | Conforme atualização lega | Não |


## 5. Regras de negócio (RN01, RN02...)

| ID | Regra | Quando se aplica | Exceção | Quem valida | Tipo |
|---|---|---|---|---|---|
| RN01 | O acesso ao processo e documentos é restrito conforme o perfil do usuário (Secretário, Presidente, Membros). | Ao tentar visualizar qualquer processo ou documento no sistema. | Denunciante e denunciado acessam apenas minutas e comunicações formalmente liberadas pela Comissão. | Sistema / Autenticação do protótipo | Acesso |
| RN02 | As sugestões da IA (classificação e roteiros) têm caráter estritamente assistencial e exigem confirmação e revisão humana obrigatória. | Nas etapas de triagem inicial e preparação de oitivas. | Nenhuma; o sistema não permite transição de etapa sem a validação formal do membro. | Membro / Presidente da Comissão | Negócio |
| RN03 | O processo só pode avançar para as fases de oitiva ou deliberação após o registro da Análise de Admissibilidade. | Na movimentação e transição das etapas processuais. | Caso a denúncia seja rejeitada liminarmente ou encaminhada para a Corregedoria. | Presidente / Secretário-executivo | Validação |
| RN04 | Denúncia sem provas suficientes fica aguardando complemento do denunciante, com prazo | Na admissibilidade | Prazo definido pela Comissão | Presidente | Negócio |
| RN05 | Toda movimentação registra perfil, data, hora e justificativa | Em todas as etapas | Nenhuma | Sistema | Validação |
| RN06 | Relatório gerencial sem nomes nem relatos, só contagens e prazos | No relatório | Nenhuma | Sistema | LGPD |


## 6. Telas (#/painel, #/lista...)

| Rota | Tela | Objetivo | Quem usa | Dados | Ação | Regra | Tipo | Verificável como | MVP |
|---|---|---|---|---|---|---|---|---|---|
| #/denuncia/nova | Registro da denúncia | Registrar e organizar a manifestação. | Secretário(a)-executivo(a) | Identificação fictícia, relato, data e documentos simulados. | Cadastrar denúncia. | Campos obrigatórios devem ser preenchidos. | Tela | Registrar um caso fictício e visualizar seus dados. | Sim |
| #/caso/:id/classificacao | Classificação assistida por IA | Auxiliar na triagem inicial. | Comissão de Ética | Relato, categorias sugeridas e elementos relevantes. | Solicitar classificação. | A IA apenas sugere; a classificação não determina a admissibilidade. | Automação | Apresentar um caso fictício e visualizar a sugestão gerada. | Sim |
| #/caso/:id/admissibilidade | Análise de admissibilidade | Registrar a decisão da Comissão. | Presidente e membros | Denúncia, informações organizadas e classificação sugerida. | Registrar decisão e justificativa. | A decisão é humana e deve ser registrada. | Tela | Selecionar uma decisão e verificar o registro correspondente. | Sim |
| #/painel | Controle de tramitação | Visualizar o andamento do processo. | Presidente e secretário(a)-executivo(a) | Etapa atual, responsável, prazo e pendências. | Atualizar etapa e acompanhar prazos. | A movimentação deve respeitar a sequência definida no fluxo. | Tela | Avançar o processo e visualizar a nova etapa. | Sim |
| #/caso/:id/oitivas | Preparação de oitivas | Apoiar a preparação das perguntas. | Membros responsáveis | Relato fictício, fatos relevantes e objetivo da oitiva. | Gerar roteiro de perguntas. | A IA sugere perguntas que devem ser revisadas pelos membros. | Automação | Gerar um roteiro para um caso fictício e avaliar sua pertinência. | Sim |
| #/caso/:id/documentos | Documentos e comunicações | Padronizar os registros do processo. | Secretário(a)-executivo(a) e membros autorizados | Dados do caso, decisões e modelos institucionais. | Gerar minuta de documento. | O documento deve ser revisado antes de sua utilização oficial. | Documento | Gerar e conferir uma minuta com dados fictícios. | Sim |
| #/caso/:id/encerramento | Encerramento do processo | Demonstrar a conclusão do fluxo. | Presidente e secretário(a)-executivo(a) | Etapa final, decisão, encaminhamentos e pendências. | Registrar encerramento. | O encerramento depende da conclusão das etapas obrigatórias. | Tela | Concluir um caso de teste e verificar seu status final. | Sim |
| #/relatorio | Relatório gerencial | Demonstrar os ganhos potenciais da automação. | Presidente e Comissão | Quantidade de casos fictícios por etapa, prazos e status. | Consultar indicadores. | Exibir dados consolidados sem exposição indevida de informações pessoais. | Relatório | Visualizar os indicadores dos casos simulados. | Sim |


## 7. KPIs (nome = fórmula em uma linha)

| KPI | Pergunta | Fórmula | Fonte | Linha de base | Valor esperado | Como medir |
|---|---|---|---|---|---|---|
| Tempo de triagem e classificação | Quanto tempo a IA economiza na triagem inicial das denúncias? | (Tempo As-Is - Tempo To-Be) / Tempo As-Is | Planilha de denúncias recebidas | 1 hora | 20 minutos | Registrar data/hora do recebimento do e-mail e data/hora da validação da triagem no sistema |
| Tempo de preparação das oitivas | Qual a redução no tempo de elaboração dos roteiros para oitivas com o apoio da IA? | Tempo total de elaboração manual - Tempo de revisão do roteiro IA | Atas das oitivas | 2 horas | 20 minutos | Registrar o tempo gasto na revisão e ajuste do roteiro gerado pela IA antes da oitiva |

**Período da linha de base:** Todos os registros de denúncias recebidas no período de 12 meses: média de 24 casos por ano (2 casos por mês), com demandas estimadas em 10 horas de trabalho mensal por processo (compreendendo reuniões de classificação e oitivas).
**Campos de data e tempo que existem:** A planilha local e as atas possuem apenas a data do recebimento da denúncia e as datas de realização das reuniões e oitivas, sem o registro dos horários. Por isso, a linha de base do processo atual é estimada por duração de reuniões e oitivas, e a medição no protótipo passará a registar a data e a hora exatas das validações.

## 8. Stack: HTML único (CSS/JS inline), dados em JSON embutido, GitHub Pages.

**Stack escolhida:** HTML único (CSS/JS inline), dados em JSON embutido, GitHub Pages
**Detalhe da stack:** Um único index.html (HTML, CSS e JS embutidos), com perfis Presidente, Membro e Secretário-executivo, dados no IndexedDB do navegador e backup .json. A classificação inicial é assistida por regras (palavras-chave ligadas às categorias do Código de Ética), com a explicação de cada sugestão; um botão gera o prompt para uma ferramenta de IA autorizada pela instituição. Sem internet e sem servidor, porque os relatos são sigilosos.
**Hospedagem:** GitHub Pages com arquivo web estático, pois permite publicar o protótipo funcional sem custos de infraestrutura, roda diretamente no navegador sem depender de servidores ou orçamento inicial de TI, sendo ideal para validar o fluxo e as funcionalidades do MVP com dados fictícios.
**Custo e licenças:** Sem custo financeiro,  utilizando serviços e plataformas gratuitas.
**Contas e domínio:** Equipe responsável cria o repositório no GitHub para publicação no GitHub Pages, disponibilizando o link de acesso ao professor e à equipe para testes e avaliação.

| Opção | Tipo | Onde roda | Custo | Quem mantém | Acesso | Banco de dados | Escala | Limitação |
|---|---|---|---|---|---|---|---|---|
| GitHub Pages | Estática e gratuita | Navegador / Nuvem do GitHub | Gratuito (R$ 0) | Equipe do projeto (alunos) | Público via URL do GitHub | Sem banco (dados fictícios em JSON local) | Demonstração do MVP e testes de fluxo | Não suporta persistência de dados reais nem banco corporativo |
| Servidor Institucional (Produção futura) | Nuvem corporativa | Data Center / Cloud da POLITEC/MT | Depende da infraestrutura existente da TI | Equipe de TI da POLITEC/MT | Restrito aos servidores da Comissão via intranet | Banco relacional seguro (PostgreSQL/SQL Server) | Uso oficial da Comissão de Ética | Exige aprovação institucional, orçamento de TI e integrações |


## 9. Restrições e LGPD

**Restrições:** O sistema deve respeitar rigorosamente o sigilo das informações e a proteção de dados pessoais (LGPD). Não é permitido tomar decisões automáticas de admissibilidade ou responsabilidade ética via IA. Toda alteração e movimentação deve manter registro de autoria e histórico.
**Dados pessoais tratados:** Nomes, e-mails, matrículas e relatos de partes envolvidas (denunciante e denunciado).
**Base legal:** Código de Ética do Servidor Público de MT LC 112 de 2002
**Retenção:** Os dados ficam no IndexedDB do computador da Comissão (não no LocalStorage), com backup .json. No MVP, só casos fictícios; um botão apaga os dados de um caso encerrado.
**Acesso e registro:** O acesso é feito por meio de perfis simulados (Presidente, Membro, Secretário-executivo), onde o sistema registra perfil, data, hora, alteração realizada e justificativa em um histórico simulado no navegador.
**Requisitos marcados:** LGPD e dado pessoal, Segurança e controle de acesso, Trilha de auditoria, Funcionar offline

---

# Anexo A — AS-IS (o fluxo de hoje)

**Início:** Recebimento de denúncia
**Fim:** Documento de recebimento das recomendações por parte do denunciado
**Entradas:** E-mail, relato, provas como prints de WhatsApp, escala de plantão  
**Saídas:** Ata de reunião, ata de oitiva, recomendações
**Volume:** 2 casos mês
**Duração:** 10 horas
**Frequência:** Mensal
| Etapa | Quem faz | O que entra | Ação | O que sai | Sistema | Regra | Onde espera | Tempo (h) | Automatizável |
|---|---|---|---|---|---|---|---|---|---|
| Recebimento denúncia | Presidente | Denúncia | leitura e-mail | registro da ocorrência | E-mail |  agendamento de reunião | e-mail | 2 | Sim, com apoio humano |
| Reunião | Todos membros | Denúncia (s) | Deliberação, formação de tríade | Ata de reunião | Reunião presencial e Sigadoc | Classificação | pasta compartilhada | 2 | Sim, com apoio humano |
| Oitivas | Tríade | Ata de reunião | Escuta | Ata da oitiva | Presencial e Sigadoc | Consolidação | pasta compartilhada | 4 | Sim, com apoio humano |
| Reunião Tríade | Tríade | Relatório de consolidação | Deliberação | Relatório de Recomendações | Reunião e Sigadoc | Recomendações | pasta compartilhada | 2 | Não |

**Decisões e aprovações:** Três vias: se a denúncia for acatada vai para reunião, pode não ser acatada por não enquadramento no código de ética ou ser encaminhada para outra instância, caso necessite de correição (corregedoria).
**Exceções:** Caso falte provas para analisar a denúncia, as mesmas são solicitadas ao denunciante e fica aguardando sua resposta
**Já digitalizado:** A denúncia é recebida via e-mail, as atas são registradas no Sigadoc, assim como os relatórios de recomendação.

# Anexo B — TO-BE (o fluxo depois da mudança)

**Visão do futuro:** Quando o processo da Comissão de Ética for automatizado, os integrantes deixarão de depender de controles manuais, documentos dispersos e acompanhamento individual de prazos e passarão a utilizar um sistema centralizado para gerenciar as denúncias, acompanhar as etapas e registrar as deliberações com segurança e rastreabilidade.
**Mudança principal:** O controle manual das denúncias, dos documentos, dos prazos e dos encaminhamentos será substituído por um sistema que organize o fluxo processual, automatize tarefas administrativas repetitivas, emita notificações e gere registros e documentos padronizados. A inteligência artificial (IA) poderá auxiliar na classificação inicial das denúncias, na identificação de elementos relevantes e na elaboração de roteiros personalizados para as oitivas, com base nos fatos relatados e nos objetivos da apuração ética. A análise de admissibilidade, a avaliação dos fatos e as deliberações permanecerão sob responsabilidade da Comissão de Ética, cabendo aos seus membros revisar e validar os conteúdos gerados pela IA, de modo a assegurar a imparcialidade, o sigilo e a observância das normas aplicáveis.
**O que fica igual:** A competência da Comissão de Ética, a análise de admissibilidade, a avaliação dos fatos, a realização das oitivas, as deliberações colegiadas e a elaboração e validação dos pareceres e das orientações permanecem sob responsabilidade dos membros da Comissão. A inteligência artificial poderá atuar como ferramenta de apoio à classificação das denúncias, à organização das informações e à elaboração de roteiros de oitivas, cabendo aos membros revisar e validar os conteúdos gerados, sem transferir à tecnologia o poder de decisão.
**O que não pode mudar:** A automação e o uso da inteligência artificial não poderão substituir as competências legais e regimentais da Comissão de Ética, tomar decisões sobre admissibilidade ou responsabilidade ética, nem comprometer a imparcialidade, o sigilo, a proteção de dados pessoais e a rastreabilidade dos atos. As classificações, sugestões e os roteiros gerados pela IA deverão ser tratados como subsídios sujeitos à revisão humana, observando-se o Código de Ética, as normas institucionais e as orientações jurídicas aplicáveis.
| Etapa | O que muda | Quem executa | Benefício | Esforço |
|---|---|---|---|---|
| Recebimento e registro da denúncia | O sistema registra a manifestação, gera protocolo e organiza os documentos anexados. | A máquina (automação) | Padronização e redução de registros manuais. | Médio |
| Classificação inicial da denúncia | A IA analisa as informações apresentadas e sugere categorias, temas e elementos relevantes para subsidiar a triagem. | A pessoa assistida pela máquina | Agilidade na triagem e melhor organização das informações. | Alto |
| Análise de admissibilidade | A Comissão avalia a denúncia e delibera sobre seu acolhimento ou não, registrando a decisão no sistema. | A pessoa, sem mudança | Decisão fundamentada e preservação da competência institucional. | Médio |
| Comunicação da decisão de admissibilidade | O sistema gera a minuta da comunicação com base na decisão registrada, para revisão e envio conforme as permissões estabelecidas. | A pessoa assistida pela máquina | Padronização e agilidade nas comunicações. | Baixo |
| Distribuição e acompanhamento do caso | O sistema registra os responsáveis, controla as etapas e os prazos e emite alertas de pendências. | A máquina (automação) | Melhor controle dos prazos e das responsabilidades. | Médio |
| Preparação das oitivas | A IA utiliza as informações do caso para sugerir roteiros de perguntas individualizados, sujeitos à revisão e ao ajuste pelos membros responsáveis. | A pessoa assistida pela máquina | Redução do tempo de preparação e maior direcionamento das oitivas. | Alto |
| Realização e registro das oitivas | Os membros conduzem as oitivas, registram as declarações e organizam os documentos correspondentes no sistema. | A pessoa, sem mudança | Organização dos registros e facilidade de consulta autorizada. | Médio |
| Análise dos fatos e deliberação | Os membros analisam as informações e os documentos, discutem o caso e registram as deliberações colegiadas. | A pessoa, sem mudança | Maior rastreabilidade e segurança dos registros decisórios. | Alto |
| Elaboração de parecer ou orientação | O sistema disponibiliza modelos padronizados e poderá utilizar IA para auxiliar na elaboração de minutas, sujeitas à revisão e validação dos membros. | A pessoa assistida pela máquina | Redução do tempo de elaboração e padronização documental. | Alto |
| Comunicação dos encaminhamentos | O sistema prepara as comunicações decorrentes das deliberações e registra seu envio aos destinatários autorizados. | A pessoa assistida pela máquina | Agilidade e comprovação dos encaminhamentos. | Médio |
| Encerramento e arquivamento | O sistema verifica os campos obrigatórios, registra o encerramento e organiza os documentos e o histórico do caso. | A máquina (automação) | Integridade documental e rastreabilidade. | Médio |
| Geração de relatórios gerenciais | O sistema consolida dados sobre denúncias recebidas, classificação, etapas, prazos e encerramentos, preservando as informações pessoais. | A máquina (automação) | Apoio à gestão e identificação de gargalos. | Médio |

**Piloto do TO-BE:** Piloto de 30 dias

# Anexo C — Pesquisa, riscos e plano

**Hipótese de campo:** O maior gargalo na apuração ética não é a análise humana em si, mas o tempo gasto em reuniões presenciais para triagem manual, controle disperso de prazos e elaboração do zero dos roteiros de oitivas.
| Referência | Tipo | Fonte ou link | Ano | Dado que extrai | Como usar na defesa | Link conferido |
|---|---|---|---|---|---|---|
| Código de Ética Funcional do Servidor Público Civil do Estado de Mato Grosso | Norma ou lei | Site da POLITEC | 2002 | Regras de conduta, infrações éticas e trâmite processual das comissões | Definir as categorias de classificação e parâmetros legais utilizados no prompt de IA | Sim |
| Mapeamento de Processos As-Is da Comissão de Ética | Documento interno | POLITEC/MT | 2026 | Gargalo de 1h por reunião de classificação e 4h por oitiva, além de fluxo 100% manual | Justificar a necessidade de automação e estabelecer a linha de base de tempo das métricas | Sim |

**Lacunas:** Não foi possível acessar dados históricos consolidados e estruturados sobre o tempo exato gasto individualmente em cada oitiva e na elaboração das minutas finais, uma vez que tais registros atualmente ocorrem de forma descentralizada em atas e arquivos locais.
| Marco | Data | Responsável | Depende de | Situação |
|---|---|---|---|---|
| Mapeamento de Requisitos e Protótipo de Telas | 29/10/2026 | Letícia e Thiago | Definição do fluxo To-Be da Comissão | Feito |
| Desenvolvimento do Módulo de Registro e Classificação por IA | 10/11/2026 | Equipe de Dev / Alunos | Validação dos prompts de IA com o Código de Ética | Planejado |
| Módulo de Admissibilidade, Oitivas e Emissão de Minutas | 17/11/2026 | Equipe de Dev / Alunos | Testes dos modelos de ata e roteiros | Planejado |
| Testes com Casos Fictícios e Homologação do Piloto | 24/11/2026 | Comissão de Ética / Alunos | Finalização das telas no GitHub Pages | Planejado |

| Risco | Probabilidade | Impacto | Mitigação |
|---|---|---|---|
| IA gerar classificações imprecisas ou inadequadas das denúncias | Média | Alto | Revisão e validação humana obrigatória pelos membros da Comissão antes de qualquer deliberação |
| Exposição de dados sensíveis ou informações de envolvidos | Baixa | Alto | Utilização exclusiva de dados 100% fictícios durante a prototipagem e simulação |
| Resistência dos membros à utilização da ferramenta automatizada | Média | Médio | Desenvolvimento de interface simples e intuitiva focada na redução de carga de trabalho manual |
| Sugestão de classificação errada por regra de palavra-chave | Média | Médio | A sugestão mostra as palavras que a dispararam; a Comissão confirma ou troca a categoria (RN02) |

**Apoio necessário:** Preciso da validação da Presidência da Comissão de Ética sobre a estrutura das minutas e regras do fluxo, além da orientação do professor/orientador para ajuste dos prompts de IA e publicação no GitHub Pages.
**Aprendizado necessário:** Engenharia de prompt para classificação de textos jurídicos/normativos, manipulação de arrays JSON em JavaScript no navegador e publicação/gestão de repositórios no GitHub Pages.

# Anexo D — A defesa

**Frase de defesa:** Se o tempo de triagem e preparação passar de 1 hora para 20 minutos por processo, a Comissão de Ética deixa de depender de reuniões presenciais demoradas e controles manuais.
**Provas:** Reuniões manuais para análise de denúncias e oitivas demandam em média 1 hora cada e causam gargalos por acúmulo de funções dos membros. 2. O processo atual depende de planilhas locais e documentos dispersos sem controle automatizado de prazos. 3. Existe previsão de cerca de 24 casos por ano gerando aproximadamente 10 horas mensais de trabalho manual reprimido.
**Piloto:** Piloto de 30 dias com casos e dados fictícios, medindo o tempo gasto na validação da triagem com IA e o tempo de preparação de roteiros para oitivas.
**Maior risco:** A IA gerar classificações ou roteiros de oitivas imprecisos. Mitigação: manter a revisão e validação humana obrigatória pelos membros da Comissão antes de qualquer deliberação ou avanço de etapa no sistema.

# Anexo E — Documentos enviados

**Descrição dos documentos:** Resolução tramite do processo; LC do Código de Ética; Código em linguagem simples; Lei de carreira da POLITEC.
**O que ainda falta:** Falta modelo de ata e relatórios.
