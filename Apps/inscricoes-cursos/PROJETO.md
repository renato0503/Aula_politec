# PROJETO.md — Gestão Dinâmica de Inscrições em Cursos

**Aluno ou equipe:** Edilaura Rondon 
**Unidade:** Gerência de Formação Inicial e Continuada 
**Contato:** capacitacao@politec.mt.gov.br
**Projeto:** Gestão Dinâmica de Inscrições em Cursos
**Tipo de projeto:** Aplicativo (app) para cidadão, servidor ou equipe
**Data:** 2026-10-27
**Resumo:** O projeto Gestão Dinâmica de Inscrições em Cursos consiste na padronização e automação de todo o ciclo de ingresso em capacitações da POLITEC, centralizando a coleta dos dados funcionais do servidor, como matrícula, lotação e e-mail institucional, em um fluxo contínuo e transparente. A iniciativa elimina gargalos operacionais ao fornecer confirmação imediata de recebimento ao candidato com status "em análise", automatizar a comunicação por e-mail e estruturar uma triagem eficiente para validação de requisitos e controle de vagas pela equipe responsável.

## 1. Problema (a dor)

**Problema:** O principal gargalo identificado é a ausência de um fluxo padronizado para a coleta de dados cadastrais dos servidores e a gestão das inscrições em cursos.
**Impacto:** O impacto negativo central decorre da distribuição ineficiente das vagas e de falhas no processo de coleta de dados, causadas pela falta de retorno tempestivo dos servidores e pela ausência de um cadastro atualizado e padronizado."
**Quem sofre:** Servidor da unidade, Chefia
**Como é feito hoje:** Atualmente, a divulgação das capacitações e a distribuição de vagas ocorrem diretamente às diretorias, que ficam responsáveis pela seleção dos servidores — definindo os candidatos para as vagas efetivas e para o cadastro de reserva
**Evidências:** Planilha ou controle local
**Detalhe da evidência:** Planilha de excel
**O que não pode ser automatizado:** Decidir quem fica com a vaga titular ou no cadastro de reserva quando a demanda é maior que o número de vagas.

## 2. Objetivo do MVP (o que faz e o que NÃO faz)

**Objetivo do MVP:** O objetivo do MVP é validar, em ambiente controlado, a automação da coleta de dados e do envio de notificações mantendo a triagem manual das diretorias, garantindo maior agilidade e redução de erros operacionais antes da expansão definitiva na POLITEC.
**O que o MVP não faz:** O MVP (Produto Mínimo Viável) NÃO faz a integração em tempo real com o banco de dados corporativo do RH, a emissão e o envio automatizado de certificados, a geração de painéis e dashboards gerenciais de BI, o reescalonamento automático do cadastro de reserva em caso de desistências e a autenticação centralizada por login corporativo (SSO), mantendo essas funcionalidades avançadas para fases futuras do projeto e focando, nesta etapa, exclusivamente na validação da coleta de dados, automação de avisos e apoio à triagem das diretorias.
**Entregável do projeto:** App de inscrição em um único arquivo HTML (inscrição, triagem pelas diretorias e convocação), com a documentação do novo fluxo (AS-IS e TO-BE), a matriz de governança e o relatório do piloto.
**Dentro do escopo:** O escopo do projeto abrange o mapeamento e a padronização integral do fluxo de inscrição (AS-IS e TO-BE), a criação dos formulários digitais padronizados, a automação das notificações e comunicações com os servidores, a organização da base de dados para otimizar a triagem pelas diretorias, o estabelecimento da matriz de governança, além da realização do projeto-piloto de testes e a entrega da documentação final para a implantação definitiva na POLITEC.
**Fora do escopo:** Automação da decisão de seleção das vagas; gestão das aulas práticas; integração em tempo real com o RH; emissão de certificados. A autonomia das diretorias na escolha dos servidores continua.
**Plataforma alvo:** Site web (abre no navegador)
**Primeira tela:** O primeiro artefato que o usuário vê depende do seu papel no fluxo:  * **Para o Servidor (Candidato):** É a **Tela/Formulário de Inscrição Online**, onde ele visualiza as informações do curso e preenche seus dados cadastrais. * **Para o Gestor/Diretoria:** É a **Planilha/Painel de Triagem**, onde ele visualiza a lista consolidada dos inscritos para realizar a seleção das vagas.
**Simulado no MVP:** A conferência da matrícula usa um relatório do SEAP exportado (fictício no teste). A resposta automática por e-mail usa uma regra do Outlook, se a TI liberar; sem ela, vale o comprovante na tela. A chamada da reserva é feita pela gerência com um botão, sem reescalonamento automático.
**Critério de aceite:** O critério de aceite que comprova o funcionamento do MVP é a validação de quatro condições fundamentais de ponta a ponta:

Captura e Validação de Dados: 100% das submissões no formulário online geram registros corretos na base de dados, bloqueando envios com campos obrigatórios em branco ou inválidos.

Disparo das Notificações Automáticas: Todos os e-mails/mensagens de confirmação de inscrição ("Em Análise") chegam às caixas de entrada dos servidores de teste imediatamente após o envio do formulário.

Fluidez na Triagem pelas Diretorias: Os gestores conseguem acessar a planilha/painel consolidado, aplicar filtros por diretoria e indicar os candidatos (Titulares e Reserva) sem retrabalho ou ambiguidades.

Encaminhamento Efetivo: Os servidores aprovados recebem a notificação final de convocação contendo o link funcional para o grupo oficial da turma, concluindo o ciclo do teste sem falhas de comunicação.
**Dados de exemplo:** Para realizar os testes e homologação do MVP no ambiente de teste, a base de dados deve ser populada com os seguintes dados de exemplo (dados fictícios/dummy data):1. Dados de Entradas/Inscrições (Formulário)CPFNome CompletoMatrículaDiretoria / UnidadeE-mail Funcional
**O que já existe pronto e pode ser reaproveitado:** O que pode ser reaproveitado como fonte de validação manual/semi-automatizada (Sistemas de RH / SESP)
Cadastro Base do Servidor (SEAP / Portal do Servidor SEPLAG-MT): Os dados oficiais de identificação (Matrícula, CPF, Cargo, Nome Completo, Vínculo Ativo) já existem na base legada de recursos humanos do Estado.

Como reaproveitar no MVP: Em vez de criar um banco de dados novo, a equipe usa relatórios exportados em Excel/CSV do SEAP/Portal do Servidor para cruzar e validar rapidamente os dados informados pelos candidatos nos formulários.
**Dependências:** Para garantir o funcionamento do novo fluxo e a validação do MVP, o projeto depende diretamente do alinhamento e das parcerias entre três níveis essenciais da estrutura governamental:

1. Parcerias Internas da POLITEC (Diretoria Executiva e Áreas Finalísticas)
Diretorias Finalísticas e Regionais da POLITEC: Responsáveis por validar os pré-requisitos técnicos dos inscritos, realizar a triagem/seleção de vagas (Titulares e Reserva) e definir o limite de capacidade das turmas.

Coordenadoria de Ensino/Capacitação da POLITEC: Responsável por operacionalizar o formulário, acompanhar os disparos de notificações e intermediar a comunicação com instrutores e alunos.

Equipe de Tecnologia da Informação (TI Local): Apoia no fornecimento e suporte ao ecossistema institucional (contas corporativas, licenças e ferramentas no-code para as automações).

2. Parcerias Estratégicas com a SESP-MT (Secretaria de Estado de Segurança Pública)
Coordenadoria de Tecnologia da Informação e Comunicação (COTIC/SESP): Dependência essencial para liberação de acessos, garantia da estabilidade das ferramentas corporativas e validação das regras de segurança de dados na rede estadual.

Gestão de Pessoas / RH Central da SESP (SEAP/SEPLAG): Dependência necessária para o fornecimento pontual das bases/relatórios de servidores ativos (matrícula, vínculo e cargo) utilizados na conferência cadastral do MVP.

Superintendência de Formação e Capacitação da SESP: Para alinhamento das diretrizes pedagógicas institucionais e validação de regras para aproveitamento de cursos no histórico funcional do servidor.

3. Parcerias com as demais Forças de Segurança de Mato Grosso (PMMT, CBMMT, PJC-MT)
Comandos e Diretorias de Ensino da Polícia Militar (PMMT), Polícia Judiciária Civil (PJC-MT) e Corpo de Bombeiros (CBMMT):

Em cursos integrados ou vagas interinstitucionais: Para validação e indicação de servidores externos que participarão dos treinamentos oferecidos pela POLITEC.

Alinhamento de Liberação e Escala: Dependência no envio formal da autorização de afastamento/liberação dos servidores inscritos para realizarem a capacitação presencial e prática sem prejuízo à escala operacional.

## 3. Usuários e papéis

| Papel | Quem é | O que enxerga | O que faz | O que não pode fazer | Registro |
|---|---|---|---|---|---|
| gerente  | quem organiza os cursos e o numero de vagas  | atender máximos de servidores e diferentes setores  | planilha dos interessados e divulga os inscritos  | mudar a ordem de indicação | servidores com inscrição efetivada  |
| chefia  | divulga as vagas aos servidores do setor  | possibilidades e perfis para as vagas  | respostas de indicação via email | mandar mais servidores do que vagas  | e-mail com as indicações  |
| Servidor (candidato) | Servidor da POLITEC interessado no curso | Dados do curso e o próprio comprovante | Inscreve-se e confirma presença | Ver outros inscritos | Inscrição com protocolo e data |

**Observações sobre os papéis:** O gerente verifica os dados e planilha as informações e compartilha aos gestores do curso

## 4. Dados (entidades e colunas; tudo SINTÉTICO)

| Entidade | O que representa | Colunas | Chave | Volume | Origem | Sintético |
|---|---|---|---|---|---|---|
| Curso | Capacitação oferecida | id: texto, nome: texto, inicio: data, fim: data, vagas_por_diretoria: lista, prerequisitos: lista, link_grupo: texto, prazo_triagem: data | id | 2 a 5 por mês | Gerência | Sim |
| Inscricao | Pedido de vaga do servidor | protocolo: texto, curso_id: texto, matricula: texto, nome: texto, lotacao: texto, diretoria: texto, email: texto, telefone: texto, status: texto, enviado_em: data_hora | protocolo | 50 por mês | Formulário | Sim |
| Triagem | Decisão da diretoria | id: texto, curso_id: texto, protocolo: texto, decisao: texto, ordem: inteiro, decidido_em: data_hora | id | 1 por inscrição | Diretoria | Sim |
| Convocacao | Mensagem enviada ao selecionado | id: texto, protocolo: texto, tipo: texto, enviada_em: data_hora, confirmou: lógico | id | 1 por selecionado | Gerência | Sim |
| ServidorSEAP | Servidor ativo no RH | matricula: texto, nome: texto, cargo: texto, lotacao: texto, vinculo_ativo: lógico | matricula | Relatório do SEAP | Relatório exportado | Sim |

**O que precisa ser coletado:** o material não fica disponível 
**Quem libera o acesso:** o gerente de formação e quando o curso abre 

### Fontes de dados do processo real

| Fonte | Tipo | Onde | Existe | Uma linha é | Volume | Campos de data | Atualiza | LGPD |
|---|---|---|---|---|---|---|---|---|
| Planilha de inscritos | Planilha local | Drive da Gerência de Formação | Parcialmente | Um servidor indicado | 50 por mês | Data do e-mail de indicação | A cada curso | Sim |
| E-mails das diretorias | Documento em papel | Caixa capacitacao@ | Sim | Uma resposta de diretoria | Uma por diretoria e curso | Data de envio e de resposta | A cada curso | Sim |
| Relatório de servidores ativos (SEAP) | Sistema oficial | SEAP / Portal do Servidor | Sim | Um servidor | Servidores da POLITEC | Não se aplica | Mensal | Sim |


## 5. Regras de negócio (RN01, RN02...)

| ID | Regra | Quando se aplica | Exceção | Quem valida | Tipo |
|---|---|---|---|---|---|
| RN01 | Matrícula, nome, lotação, diretoria e e-mail são obrigatórios | Na inscrição | Nenhuma | Sistema | Validação |
| RN02 | E-mail institucional (@politec.mt.gov.br) | Na inscrição | Servidor de outra força em curso integrado | Sistema | Validação |
| RN03 | Uma inscrição por matrícula e curso; o reenvio substitui a anterior | Na importação | Nenhuma | Sistema | Validação |
| RN04 | Matrícula ausente do SEAP gera alerta, sem recusar | Na conferência | Nenhuma | Gerente de Formação | Validação |
| RN05 | A diretoria não marca mais titulares que as vagas dela | Na triagem | Nenhuma | Sistema | Negócio |
| RN06 | A efetivação segue a ordem de indicação da diretoria | Na convocação | Nenhuma | Gerente de Formação | Negócio |
| RN07 | Desistência de titular chama o próximo da reserva da mesma diretoria | Após a convocação | Reserva vazia: a vaga volta para a gerência | Gerente de Formação | Negócio |
| RN08 | Dados dos inscritos apagados 30 dias após o fim do curso | Ao abrir o app | Nenhuma | Gerente de Formação | LGPD |


## 6. Telas (#/painel, #/lista...)

| Rota | Tela | Objetivo | Quem usa | Dados | Ação | Regra | Tipo | Verificável como | MVP |
|---|---|---|---|---|---|---|---|---|---|
| (documento) | Mapeamento AS-IS e TO-BE | Documentar o fluxo atual e o futuro | Equipe do projeto e gestores | Etapas, gargalos, pontos de automação, papéis | Mapear e validar | O TO-BE preserva a autonomia das diretorias | Documento | Fluxograma aprovado pelos gestores | Sim |
| #/inscricao | Formulário de inscrição | Coletar dados padronizados | Servidor | Matrícula, nome, lotação, diretoria, e-mail, telefone, pré-requisitos | Preencher e enviar | Campos obrigatórios e e-mail institucional | Tela | Envio com campo vazio é bloqueado | Sim |
| #/inscricao (comprovante) | Comprovante e confirmação | Confirmar o recebimento | Servidor | Protocolo, curso, status em análise | Ver e imprimir o comprovante | Gerado no momento do envio | Automação | Comprovante aparece logo após o envio | Sim |
| #/triagem | Painel de triagem | Apoiar a decisão da diretoria | Diretorias | Inscritos da diretoria, data de envio, pré-requisitos | Ordenar titulares e reserva | Só a diretoria define a classificação | Tela | Diretoria não marca titulares acima das vagas | Sim |
| #/convocacao | Convocação e grupo oficial | Convocar e direcionar ao grupo | Gerência | Nome, status, orientações, link do grupo | Gerar e enviar a mensagem | Só selecionados recebem o link | Automação | Mensagem gerada com o link correto | Sim |
| (documento) | Matriz de governança | Formalizar papéis e limites | Gestores e instrução | Papéis, exceções, desistências | Consultar | Automação não sobrepõe decisão das diretorias | Documento | Documento aprovado | Não |
| (documento) | Relatório do piloto | Registrar os resultados do teste | Equipe e alta gestão | Erros, tempo de triagem, retorno dos usuários | Consolidar e autorizar | Avança se todas as mensagens de teste forem entregues | Relatório | Relatório apresentado à gestão | Sim |


## 7. KPIs (nome = fórmula em uma linha)

| KPI | Pergunta | Fórmula | Fonte | Linha de base | Valor esperado | Como medir |
|---|---|---|---|---|---|---|
| Tempo até a lista final | Quanto tempo leva da divulgação à lista final? | Data da lista final − data da divulgação | E-mails e app | A medir em 2 cursos | Metade do tempo atual | Datas dos e-mails dos 2 últimos cursos |
| Espera pela indicação | Quanto as diretorias demoram a responder? | Retorno da triagem − envio do arquivo | App | 36 h (AS-IS) | Até 24 h | Datas de exportação e retorno |
| Inscrições com erro de dado | Quantas inscrições a gerência precisou corrigir? | Inscrições corrigidas ÷ total × 100 | Log do app | A medir na planilha atual | Abaixo de 5% | Contar correções na planilha de 2 cursos |
| Vagas ociosas | Quantas vagas ficaram sem servidor? | Vagas − confirmados | App | A medir em 2 cursos | Zero com o cadastro de reserva | Comparar vagas e presentes |

**Período da linha de base:** Os 2 últimos cursos com inscrição encerrada: data da divulgação, data de retorno de cada diretoria, data da lista final, inscrições corrigidas pela gerência e vagas não ocupadas.
**Campos de data e tempo que existem:** Hoje: data dos e-mails de divulgação e de resposta das diretorias, e a data da planilha final. No app: enviado_em e recebido_em da inscrição, data da exportação e do retorno da triagem, data da convocação e da confirmação de presença.

## 8. Stack: HTML único (CSS/JS inline), dados em JSON embutido, GitHub Pages.

**Stack escolhida:** HTML único (CSS/JS inline), dados em JSON embutido, GitHub Pages
**Detalhe da stack:** Um único arquivo index.html (HTML, CSS e JS embutidos) com três perfis: servidor (inscrição), diretoria (triagem) e gerência. A inscrição gera um bloco de dados enviado por e-mail à caixa capacitacao@; a gerência cola os e-mails no app. Dados no IndexedDB da gerência; troca com as diretorias por arquivo .json. Biblioteca embutida: gerador de QR Code.
**Hospedagem:** Arquivo HTML único, publicado no GitHub Pages para o servidor abrir o link de inscrição, e aberto por duplo clique no computador da gerência. Sem servidor e sem banco de dados externo.
**Custo e licenças:** Custo zero: arquivo HTML, biblioteca de QR Code de código aberto e GitHub Pages.
**Contas e domínio:** A Gerência de Formação publica o arquivo no GitHub Pages (ou no site institucional, se a TI preferir). A caixa capacitacao@politec.mt.gov.br já existe.

| Opção | Tipo | Onde roda | Custo | Quem mantém | Acesso | Banco de dados | Escala | Limitação |
|---|---|---|---|---|---|---|---|---|
| Arquivo HTML único + GitHub Pages | Estática e gratuita | GitHub Pages (link) e computador da gerência | Zero | Gerência de Formação | Link público de inscrição; base só na gerência | IndexedDB da gerência | Dezenas de inscrições por curso | Inscrições chegam por e-mail |
| Forms + planilha + Power Automate | Nuvem corporativa | Microsoft 365 ou Google Workspace | Licença institucional | Gerência e TI | Conta institucional | Planilha | Média | Depende de licença e de configuração pela TI |


## 9. Restrições e LGPD

**Restrições:** Sem servidor: as inscrições chegam por e-mail à caixa da gerência. Sem CPF. A decisão de quem fica com a vaga é da diretoria. Dados dos inscritos apagados 30 dias após o fim do curso.
**Dados pessoais tratados:** Matrícula, nome, lotação, diretoria, e-mail institucional e telefone opcional dos servidores inscritos. Sem CPF: a matrícula identifica o servidor no SEAP.
**Base legal:** Cadastro de servidores nos cursos de fromação
**Retenção:** 30 dias 
**Acesso e registro:** O gerente de formação
**Requisitos marcados:** Funcionar offline, LGPD e dado pessoal, Segurança e controle de acesso, Trilha de auditoria

---

# Anexo A — AS-IS (o fluxo de hoje)

**Início:** divulgação de vagas de cursos/treinamentos para a Diretorias da POLITEC
**Fim:** Cadastro do servidor no curso/treinamento
**Entradas:** Planilha com os dados do servidor(nome completo, unidade/lotação, matricula, CPF, telefone e email funcional)
**Saídas:** Servidor capacitado e certificação/declaração de conclusão de cursos/treinamentos
**Volume:** 50
**Duração:** 40 horas semanais
**Frequência:** Mensal
| Etapa | Quem faz | O que entra | Ação | O que sai | Sistema | Regra | Onde espera | Tempo (h) | Automatizável |
|---|---|---|---|---|---|---|---|---|---|
| Divulgar o curso e as vagas | Gerente de Formação | Curso, vagas e pré-requisitos | Envia e-mail às diretorias com as vagas de cada uma | E-mail de divulgação | E-mail | Vagas distribuídas por diretoria | Não identificado | 1 | Sim, com regra clara |
| Indicar os servidores | Chefia da diretoria | E-mail de divulgação | Escolhe titulares e reserva e responde por e-mail | E-mail com as indicações | E-mail | Não indicar mais servidores que vagas | Retorno das diretorias | 36 | Sim, com apoio humano |
| Coletar os dados dos servidores | Gerente de Formação | Indicações | Pede e recebe nome, lotação, matrícula, e-mail e telefone | Dados dos indicados | E-mail | Dados completos | Retorno dos servidores | A medir | Sim, com regra clara |
| Montar a planilha | Gerente de Formação | Dados dos indicados | Digita os dados no Excel | Planilha de inscritos | Excel | Ordem de indicação | Não identificado | A medir | Sim, com regra clara |
| Enviar ao responsável pelo curso | Gerente de Formação | Planilha | Compartilha a planilha com o gestor do curso | Lista de inscritos | E-mail | Efetivação pela ordem de indicação | Não identificado | A medir | Sim, com regra clara |
| Tratar desistências | Gerente de Formação | Desistência do titular | Chama o próximo do cadastro de reserva | Reserva convocada | E-mail e telefone | Próximo da reserva da mesma diretoria | Resposta da reserva | A medir | Sim, com apoio humano |

**Decisões e aprovações:**  A efetivação da inscrição é pela ordem de indicação 
**Exceções:** Caso haja desistência de primeiro indicado temos o cadastro reserva 
**Já digitalizado:** Digitação em planilha de Excel e disponibilizado ao setor ou órgão responsável pelo o curso 

# Anexo B — TO-BE (o fluxo depois da mudança)

**Visão do futuro:** Transformar a gestão de capacitações em um processo totalmente fluido, onde a tecnologia automatiza a coleta de dados e a comunicação, permitindo que a liderança foque na decisão estratégica e no desenvolvimento continuo dos servidores.
**Mudança principal:** A mudança principal é a transição de um processo manual, descentralizado e lento para um fluxo automatizado, padronizado e transparente.
**O que fica igual:** A prerrogativa das diretorias na seleção dos servidores, a validação humana dos pré-requisitos e a execução presencial das instruções práticas permanecem exatamente as mesmas.
**O que não pode mudar:** A autonomia das diretorias na indicação dos participantes, o cumprimento rigoroso dos pré-requisitos regulamentares e a avaliação presencial da aptidão técnica do servidor permanecem intocados
| Etapa | O que muda | Quem executa | Benefício | Esforço |
|---|---|---|---|---|
| Criar e divulgar o curso | Link e QR Code de inscrição gerados pelo app | A pessoa assistida pela máquina | Divulgação padronizada | Baixo |
| Inscrever-se | Formulário validado e comprovante na hora | A pessoa assistida pela máquina | Dados completos na primeira vez | Médio |
| Importar as inscrições | A gerência cola os e-mails e o app lê os blocos | A máquina (automação) | Fim da redigitação | Médio |
| Triagem pela diretoria | Arquivo com os inscritos da diretoria e limite de vagas | A pessoa assistida pela máquina | Decisão sem ambiguidade | Médio |
| Convocar e chamar a reserva | Mensagens geradas com o link do grupo oficial | A pessoa assistida pela máquina | Convocação no mesmo dia | Baixo |

**Piloto do TO-BE:** O teste do estado futuro (TO-BE) será realizado em ambiente de homologação e por meio de um projeto-piloto em turma reduzida, validando o preenchimento dos dados, o disparo das notificações automáticas e a facilidade de triagem pelas diretorias antes do lançamento oficial.

# Anexo C — Pesquisa, riscos e plano

**Hipótese de campo:** A maior parte do tempo se perde esperando o retorno das diretorias (36 h por etapa) e redigitando dados que chegam em formatos diferentes, e não na escolha dos servidores.
| Referência | Tipo | Fonte ou link | Ano | Dado que extrai | Como usar na defesa | Link conferido |
|---|---|---|---|---|---|---|
| Lei Geral de Proteção de Dados, art. 6º (necessidade) | Norma ou lei | Lei nº 13.709/2018, Planalto | 2018 | Tratar só os dados necessários à finalidade | Justificar a retirada do CPF | Não |
| Lei do Governo Digital | Norma ou lei | Lei nº 14.129/2021, Planalto | 2021 | Digitalização de serviços públicos | Justificar a inscrição digital | Não |

**Lacunas:** Não há medição do tempo entre a divulgação e a lista final, nem contagem de erros de cadastro. A regra de resposta automática da caixa de e-mail depende da TI.
| Marco | Data | Responsável | Depende de | Situação |
|---|---|---|---|---|
| Escopo e mensagens aprovados | Semana 1 | Edilaura | Gerente de Formação | Planejado |
| Formulário de inscrição com comprovante | Semana 4 | Edilaura | Curso cadastrado | Planejado |
| Triagem pelas diretorias | Semana 7 | Edilaura | Importação das inscrições | Planejado |
| Piloto com turma reduzida | Semana 10 | Edilaura e diretorias | Aceite | Planejado |

| Risco | Probabilidade | Impacto | Mitigação |
|---|---|---|---|
| E-mail de inscrição cortado pelo cliente de e-mail | Média | Médio | Bloco curto e botão de copiar o bloco |
| Diretoria não devolve a triagem no prazo | Alta | Médio | Prazo no arquivo e lista de pendentes na gerência |
| TI não libera a resposta automática | Média | Baixo | Comprovante na tela vale como confirmação |
| Base só no computador da gerência | Baixa | Alto | Backup .json semanal |

**Apoio necessário:** Gerente de Formação: aprovar o fluxo e as mensagens. Diretorias: testar a triagem por arquivo. TI: confirmar a regra de resposta automática da caixa capacitacao@ e a publicação do link.
**Aprendizado necessário:** Estrutura de um app em um único HTML, IndexedDB, leitura de texto colado (blocos de inscrição), exportação de CSV e regras de LGPD (minimização e retenção).

# Anexo D — A defesa

**Frase de defesa:** Se a inscrição chegar padronizada e a triagem voltar por arquivo, a gerência deixa de redigitar planilhas e as vagas são distribuídas antes do curso começar.
**Provas:** 1) A gerência gasta 40 h por semana no processo (informado pela aluna). 2) A espera pelo retorno das indicações é de 36 h por etapa (AS-IS). 3) O piloto com uma turma reduzida mede a redigitação e o tempo até a lista final.
**Piloto:** Uma turma reduzida, com 10 servidores de teste e 3 diretorias, do link de inscrição à lista final, comparando com a linha de base dos 2 cursos anteriores.
**Maior risco:** O e-mail de inscrição não chegar inteiro (corpo cortado). Mitigação: bloco curto, botão de copiar o bloco e comprovante na tela com o protocolo.

# Anexo E — Documentos enviados

**Descrição dos documentos:** Tabela de definições consolidadas (7 artefatos): movida para o bloco de telas e artefatos.
**O que ainda falta:** Planilha usada hoje (sem dados pessoais); exemplo de e-mail de divulgação e de resposta das diretorias; lista das diretorias que recebem vagas.
