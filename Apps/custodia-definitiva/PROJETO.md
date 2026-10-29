# PROJETO.md — Adequação da custódia definitiva de vestígios periciais às exigências legais

**Aluno ou equipe:** Edjane Ávila 
**Unidade:** Gerência de Custódia Definitiva
**Contato:** edjanegasparini@politec.mt.gov.br
**Projeto:** Adequação da custódia definitiva de vestígios periciais às exigências legais
**Tipo de projeto:** Mapeamento de processo (fluxo, BPMN ou Mermaid)
**Data:** 2026-10-27
**Resumo:** A proposta consiste na estruturação de uma Unidade de Custódia Definitiva (UCD), com armazenamento organizado por categorias e requisitos específicos de conservação, associado a um sistema de gestão inteligente. 

## 1. Problema (a dor)

**Problema:** Desafio administrativo e logístico, especialmente diante da necessidade de absorver prospectivamente vestígios pós-processamento, contraprovas e materiais destinados a eventuais contra perícias.
**Impacto:** O principal impacto a fragmentação da responsabilidade pela custódia dos vestígios após o processamento pericial, com consequências para a rastreabilidade, a logística, a segurança e a gestão do acervo.
**Quem sofre:** Unidade parceira
**Como é feito hoje:** Os vestígios vem para Diretoria de Laboratório Forense através das autoridades policiais, com requisições periciais de exames específicos realizados pela pasta. Lá dentro, após o processamento, eles retornam para as autoridades que fazem a custódia desse material (no caso do laboratório: armas brancas, roupas, balanças, tabletes de droga) nas delegacias respectivas. Nas cidades do interior, tudo o que é processado em definitivo pelas unidades, vem para capital como contraperícia. Por exemplo: em 2025, 12 mil alíquotas de contraprova, proveniente da perícia de entorpecentes, foram encaminhadas ao Laboratório Forense onde ficam hoje armazenadas em uma sala de custódia de contraprovas. Nesta mesma sala é armazenado também as contraprovas produzidas pela região metropolitana em Cuiabá. Ainda existe também todo quantitativo de contraprovas gerado por materiais biológicos da Toxicologia e da Biologia Molecular e que são custodiados em contêiner refrigerado. Esses materiais todos estão hoje sob responsabilidade do Núcleo de Custódia. 
**Evidências:** Entrevista com a equipe, Pesquisa externa, Documento ou norma oficial, Medida feita pela equipe
**Detalhe da evidência:** -
**O que não pode ser automatizado:** Não devem ser integralmente automatizadas a conferência física, a validação da integridade, a transferência de responsabilidade e a autorização de descarte dos vestígios, pois exigem avaliação humana, responsabilidade legal e garantia da cadeia de custódia.

## 2. Objetivo do MVP (o que faz e o que NÃO faz)

**Objetivo do MVP:** Demonstrar que é possível cadastrar, classificar e localizar vestígios periciais digitalmente, com endereçamento inteligente e previsão da capacidade de armazenamento da Central de Custódia Definitiva.
**O que o MVP não faz:** O MVP não realiza integração com o sistema Atena, leitura RFID, movimentação física de contêineres, monitoramento ambiental ou operações reais de custódia. Não utiliza dados sigilosos, não autoriza transferências ou descartes e não substitui a conferência humana. A previsão de ocupação e os alertas de elegibilidade para descarte serão demonstrados com dados simulados, sem efeitos administrativos ou jurídicos.
**Entregável do projeto:** Protótipo funcional de aplicativo web para gestão inteligente da Central de Custódia Definitiva, com cadastro e classificação de vestígios, endereçamento digital de armazenamento, consulta de localização, painel de ocupação e previsão de capacidade e descarte, com apoio de inteligência artificial. O MVP utilizará dados simulados, terá acesso por perfis de usuários e será acompanhado de manual de utilização em PDF.
**Dentro do escopo:** Desenvolvimento de protótipo web com cadastro e classificação de vestígios e contraprovas, identificação de lacres, endereçamento digital em contêineres, consulta de localização, registro de movimentações e painel de controle de ocupação. Aplicação de inteligência artificial para previsão da capacidade de armazenamento e sinalização de materiais potencialmente elegíveis para descarte, conforme critérios previamente definidos.
**Fora do escopo:** Ficam fora do MVP a integração efetiva com o sistema Atena, a implantação de RFID, a movimentação física automatizada dos contêineres, o monitoramento de equipamentos de refrigeração e a execução de descartes. Essas funcionalidades exigem infraestrutura, recursos financeiros, integração com sistemas oficiais e validações técnicas e legais. O protótipo utilizará dados fictícios, sem acesso a informações periciais sigilosas ou realização de operações reais.
**Plataforma alvo:** Site web (abre no navegador)
**Primeira tela:** Painel inicial da Central de Custódia Definitiva, apresentando indicadores de ocupação dos contêineres, quantidade de vestígios cadastrados, capacidade disponível e acesso às funções de cadastro, classificação e localização de materiais.
**Simulado no MVP:** Serão simulados o recebimento e cadastro de vestígios, a classificação por categoria, o endereçamento em contêineres, a movimentação dos materiais e a previsão de ocupação. Os dados serão fictícios, sem integração com o Atena, movimentação física real ou autorização de descarte. As recomendações de armazenamento e projeções serão demonstrativas.
**Critério de aceite:** O usuário consegue cadastrar um vestígio fictício, classificá-lo, receber uma sugestão de armazenamento compatível, localizar seu endereço digital e visualizar a atualização da ocupação no painel. O sistema também apresenta uma projeção de capacidade baseada nos dados simulados, sem permitir alocação acima do limite cadastrado.
**Dados de exemplo:** No mínimo 30 vestígios fictícios, distribuídos entre entorpecentes, armas brancas, roupas, eletrônicos e contraprovas biológicas; 5 contêineres simulados, com capacidades e condições de armazenamento distintas; registros de entrada, localização e movimentação; histórico fictício de 12 meses para projeção de ocupação; e 3 situações de exceção: capacidade esgotada, incompatibilidade de armazenamento e material com pendência documental.
**O que já existe pronto e pode ser reaproveitado:** O sistema Atena, os registros de requisições e movimentações periciais, os procedimentos operacionais do Núcleo de Custódia do Laboratório Forense, os modelos de identificação e controle de contraprovas e os dados históricos de produção pericial. Também poderão ser reaproveitados os fluxogramas e levantamentos logísticos já elaborados, além de bibliotecas gratuitas para desenvolvimento do protótipo web, utilizando exclusivamente dados fictícios.
**Dependências:** Da gestão da POLITEC/MT, para validação das diretrizes e requisitos operacionais; da Coordenadoria de Custódia de Evidências, para definição dos fluxos e regras de armazenamento; da equipe de TI, para desenvolvimento e futura integração ao Atena; da assessoria jurídica, para validação dos requisitos legais de custódia e descarte; e das equipes de infraestrutura e logística, para dimensionamento dos contêineres e das condições de conservação dos vestígios.

## 3. Usuários e papéis

| Papel | Quem é | O que enxerga | O que faz | O que não pode fazer | Registro |
|---|---|---|---|---|---|
| Autoridade requisitante | Delegado ou autoridade competente | Requisição, protocolo e laudo autorizado | Requisita exames, encaminha e retira vestígios | Alterar laudos ou registros técnicos | Requisição, identificação e movimentações |
| Recebedor / protocolo | Servidor responsável pelo recebimento | Requisições, identificação, lacres e situação do material | Confere, recebe, registra e encaminha | Alterar conclusões periciais ou autorizar descarte | Recebimento, data, responsável e protocolo |
| Perito criminal | Profissional responsável pelo exame | Requisição, vestígios, exames e registros pertinentes | Realiza exames, produz laudo e separa contraprovas | Alterar registros de custódia sem justificativa ou autorização | Exames, laudos, autoria e tramitação |
| Núcleo de Custódia | Servidores responsáveis pela guarda das contraprovas | Identificação, localização, lacres e movimentações | Recebe, confere, armazena e disponibiliza material autorizado | Retirar, transferir ou descartar sem autorização | Entradas, saídas, responsáveis e localização |
| Responsável pela devolução | Servidor designado para entrega | Protocolo, vestígios, lacres e Auto de Entrega | Confere e entrega o material, coleta assinaturas e digitaliza o auto | Entregar material sem conferência e identificação do recebedor | Auto de Entrega, lacres e documento digitalizado |
| Gestor da unidade | Chefia ou gerência responsável | Indicadores, procedimentos e registros conforme perfil | Supervisiona fluxos, acompanha pendências e organiza recursos | Alterar laudos ou suprimir registros de auditoria | Ações de gestão e alterações realizadas |

**Observações sobre os papéis:** O acesso ao sistema Atena deve ser individualizado, mediante autenticação e identificação funcional, respeitando as competências de cada servidor. Os peritos são responsáveis pelos exames e laudos; os servidores do Núcleo de Custódia, pelo recebimento, armazenamento e movimentação autorizada das contraprovas; e as autoridades requisitantes, pela solicitação dos exames e recebimento dos vestígios devolvidos.
As movimentações devem preservar a rastreabilidade, com identificação dos responsáveis, datas, horários e lacres. Alterações, retiradas e descartes devem observar as permissões funcionais e autorizações legais, mantendo registros auditáveis para garantir a integridade da cadeia de custódia.

## 4. Dados (entidades e colunas; tudo SINTÉTICO)

| Entidade | O que representa | Colunas | Chave | Volume | Origem | Sintético |
|---|---|---|---|---|---|---|
| Vestígio | Material pericial cadastrado | id_vestigio: texto, protocolo: texto, lacre: texto, categoria_id: texto, data_entrada: data, status: texto, volume_ocupado: decimal | id_vestigio | 30 registros | Cadastro fictício | Sim |
| Categoria | Classificação e conservação | id_categoria: texto, nome: texto, tipo_conservacao: texto, restricao: texto | id_categoria | 5 categorias | Regras técnicas exemplificativas | Sim |
| Contêiner | Unidade física de armazenamento | id_conteiner: texto, categoria_permitida: texto, capacidade: decimal, ocupacao: decimal, status: texto | id_conteiner | 5 contêineres | Estrutura simulada | Sim |
| Localização | Endereço do vestígio | id_localizacao: texto, vestigio_id: texto, conteiner_id: texto, posicao: texto, data_alocacao: data | id_localizacao | 30 registros | Endereçamento simulado | Sim |
| Movimentação | Histórico de entradas e saídas | id_movimentacao: texto, vestigio_id: texto, tipo: texto, data_hora: data/hora, responsavel_id: texto, origem: texto, destino: texto | id_movimentacao | 60 registros | Movimentações fictícias | Sim |
| Usuário | Perfil de acesso ao sistema | id_usuario: texto, nome: texto, perfil: texto, matricula: texto, ativo: booleano | id_usuario | 5 usuários | Identidades fictícias | Sim |
| Histórico mensal | Base para previsão de ocupação | id_periodo: texto, mes: data, entradas: inteiro, saidas: inteiro, ocupacao_final: decimal | id_periodo | 12 meses | Série histórica simulada | Sim |

**O que precisa ser coletado:** É necessário levantar o volume mensal de vestígios processados e devolvidos às delegacias, a quantidade de contraprovas armazenadas por categoria, o tempo gasto com recebimento, conferência, registro, movimentação e localização dos materiais, além da capacidade física disponível e das condições de armazenamento. Também deverão ser coletados dados sobre o crescimento do acervo, a frequência de solicitações de contraperícia e os critérios legais de destinação e descarte, para subsidiar o dimensionamento da futura Central de Custódia Definitiva.
**Quem libera o acesso:** A gestão da POLITEC/MT e a chefia do Laboratório Forense deverão autorizar o acesso aos dados institucionais, com apoio da Coordenadoria de Custódia de Evidências e da equipe de TI, conforme as competências de cada unidade. O levantamento poderá ser realizado após autorização formal, em período inicial de 30 dias. Para o MVP acadêmico, não será necessário acesso aos sistemas oficiais, pois serão utilizados exclusivamente dados fictícios.

### Fontes de dados do processo real


## 5. Regras de negócio (RN01, RN02...)


## 6. Telas (#/painel, #/lista...)


## 7. KPIs (nome = fórmula em uma linha)

**Período da linha de base:** Período de janeiro a dezembro de 2025, utilizando como referência 12.000 alíquotas de contraprovas de entorpecentes provenientes do interior (média de 1.000/mês), além da produção da capital, estimada em 500 alíquotas mensais por perito. Como indicador complementar, foram registrados 13.558 laudos laboratoriais entre janeiro e novembro de 2025. Os tempos operacionais de custódia ainda precisam ser mensurados.
**Campos de data e tempo que existem:** O sistema Atena registra informações de tramitação dos procedimentos periciais e permite a emissão dos Autos de Entrega da Devolução, posteriormente assinados e digitalizados. Existem registros de recebimento, encaminhamento e devolução dos materiais, porém é necessário verificar quais possuem data e horário efetivamente disponíveis. Ainda não há confirmação de registros suficientes para calcular o tempo de espera, conferência, localização e armazenamento das contraprovas em horas. Esses tempos deverão ser medidos durante o diagnóstico operacional.

## 8. Stack: HTML único (CSS/JS inline), dados em JSON embutido, GitHub Pages.

**Stack escolhida:** HTML único (CSS/JS inline), dados em JSON embutido, GitHub Pages
**Detalhe da stack:** O MVP será desenvolvido em arquivo HTML único (index.html), com CSS e JavaScript incorporados e dados fictícios armazenados em JSON no próprio arquivo, publicado no GitHub Pages. A aplicação permitirá simular o cadastro, a classificação, o endereçamento e a localização dos vestígios, além de apresentar indicadores e projeções de ocupação dos contêineres, utilizando regras automatizadas e cálculos demonstrativos, sem integração com sistemas oficiais.
**Hospedagem:** GitHub Pages, com aplicação em arquivo HTML único, contendo CSS, JavaScript e dados fictícios em JSON. A escolha permite acesso ao protótipo por navegador, sem custos de hospedagem ou necessidade de servidor próprio. É suficiente para demonstrar cadastro, classificação, endereçamento e previsão de ocupação, sem integração com sistemas oficiais. A solução institucional futura exigirá ambiente seguro e infraestrutura própria ou corporativa autorizada.
**Custo e licenças:** Custo estimado de R$ 0,00 para o MVP acadêmico, utilizando HTML, CSS, JavaScript e hospedagem gratuita no GitHub Pages, sem contratação de licenças, servidores ou APIs pagas. O desenvolvimento utilizará ferramentas gratuitas e dados fictícios. A implantação institucional futura exigirá orçamento específico para infraestrutura tecnológica, integração com o Atena, equipamentos, segurança da informação e manutenção.
**Contas e domínio:** A responsável pelo projeto acadêmico criará ou utilizará uma conta pessoal no GitHub para publicar o protótipo no GitHub Pages, utilizando o endereço gratuito fornecido pela plataforma. O acesso será por link, exclusivamente para demonstração com dados fictícios. A futura implantação institucional dependerá da equipe de TI e das autorizações da gestão da POLITEC/MT, com autenticação individual e controle de permissões.


## 9. Restrições e LGPD

**Restrições:** A solução deve respeitar os artigos 158-A a 158-F do Código de Processo Penal, os procedimentos institucionais de cadeia de custódia e as exigências específicas de conservação dos vestígios. O acesso a dados e sistemas oficiais depende de autorização institucional. A IA não poderá substituir a conferência física, as decisões técnicas ou as autorizações legais para movimentação e descarte. O MVP utilizará exclusivamente dados fictícios, sem integração com o Atena ou operações reais de custódia. A implantação definitiva dependerá de infraestrutura, orçamento, validação jurídica e segurança da informação.
**Dados pessoais tratados:** O MVP utilizará exclusivamente dados sintéticos, incluindo identificadores fictícios de servidores, vestígios, protocolos e movimentações. Não serão utilizados nomes reais, matrículas funcionais, dados pessoais de investigados ou informações sigilosas de procedimentos periciais.
**Base legal:** O protótipo possui finalidade acadêmica, voltada à demonstração de uma solução tecnológica para gestão da custódia de vestígios. Utilizará dados fictícios, sem tratamento intencional de dados pessoais reais. O projeto institucional futuro deverá observar os artigos 158-A a 158-F do Código de Processo Penal, a legislação aplicável à proteção de dados e as normas de segurança da informação da POLITEC/MT.
**Retenção:** Os dados fictícios serão mantidos apenas durante a demonstração e avaliação acadêmica do MVP, podendo ser excluídos ou reinicializados ao término dos testes. A versão institucional deverá estabelecer prazos de retenção conforme a legislação aplicável e as políticas de gestão documental e segurança da informação.
**Acesso e registro:** No MVP, o acesso será demonstrativo, com perfis fictícios de servidor da custódia, gestor e administrador. As operações simuladas de cadastro e movimentação poderão registrar identificador do usuário, data, hora e ação realizada. Na versão institucional, o acesso deverá exigir autenticação individual, controle de permissões e trilha de auditoria, impedindo alterações não autorizadas.
**Requisitos marcados:** LGPD e dado pessoal, Segurança e controle de acesso, Acessibilidade, Funcionar offline, Integração com sistema oficial, Trilha de auditoria

---

# Anexo A — AS-IS (o fluxo de hoje)

**Início:** Atualmente, os vestígios são coletados no local de crime, identificados, acondicionados e encaminhados pelas autoridades policiais ao Laboratório Forense, acompanhados de requisição pericial encaminhada no sistema Atena.
**Fim:** Após o recebimento e processamento técnico, os materiais remanescentes, como armas brancas, roupas, balanças e entorpecentes, são devolvidos às delegacias de origem, responsáveis por sua guarda até o descarte autorizado pelo judiciário.
**Entradas:** 1. Vestígios: materiais coletados em locais de crime ou apreendidos pelas autoridades policiais (drogas, armas brancas, roupas, balanças, materiais biológicos etc.).
2. Requisições periciais: documentos oficiais que solicitam a realização de exames específicos.
3. Registros de cadeia de custódia: identificação, origem, acondicionamento, lacres e histórico de movimentação dos vestígios.
4. Autoridades requisitantes: delegados de polícia e demais autoridades legalmente competentes.
5. Servidores envolvidos: peritos criminais, profissionais responsáveis pelo recebimento e equipe do Núcleo de Custódia.
6. Informações processuais: número do procedimento, identificação da unidade requisitante, tipo de exame solicitado e dados de referência do vestígio.
7. Contraprovas provenientes do interior: alíquotas produzidas pelas unidades periciais regionais e encaminhadas ao Laboratório para custódia.
8. Contraprovas produzidas na capital: alíquotas de entorpecentes e materiais biológicos destinados ao armazenamento.
9. Solicitações de movimentação: pedidos de retirada, disponibilização para contraprova, transferência ou destinação de materiais.
10. Registros informatizados: dados inseridos nos sistemas institucionais de controle pericial e movimentação de vestígios.
**Saídas:** 1. Laudos periciais: resultados dos exames realizados, encaminhados às autoridades requisitantes.
2. Vestígios processados: materiais remanescentes devolvidos às delegacias de origem para custódia.
3. Contraprovas de entorpecentes: alíquotas destinadas à sala de custódia do Laboratório Forense.
4. Contraprovas biológicas: materiais destinados ao armazenamento em contêiner refrigerado.
5. Registros de movimentação: documentação de recebimento, transferência, devolução e armazenamento dos vestígios.
6. Materiais disponibilizados para contraprova: vestígios retirados da guarda mediante solicitação e autorização competentes.
7. Materiais destinados ao descarte: vestígios encaminhados à destinação final, quando legalmente autorizada.
**Volume:** 1.233 laudos por mês
**Duração:** 616,5 horas mensais estimadas de processamento pericial.
**Frequência:** Mensal
| Etapa | Quem faz | O que entra | Ação | O que sai | Sistema | Regra | Onde espera | Tempo (h) | Automatizável |
|---|---|---|---|---|---|---|---|---|---|
| Coleta do vestígio | Perito / agente competente | Vestígio no local de crime | Coleta, identifica e acondiciona | Vestígio lacrado | RNC / registros | Preservação e integridade | Local de coleta / transporte | 0,50 | Pouco |
| Requisição pericial | Autoridade requisitante | Vestígio e dados do procedimento | Solicita exame específico | Requisição e material encaminhado | Requisição / Atena | Competência e tipo de exame | Unidade requisitante / transporte | 0,25 | Sim, com apoio humano |
| Recebimento | Servidor do Laboratório | Vestígio e requisição | Confere material, lacre e documentos | Material recebido ou pendência registrada | Atena / RNC | Conformidade da entrega | Área de recebimento | 0,25 | Sim, com apoio humano |
| Registro e distribuição | Equipe administrativa / técnica | Material recebido | Registra e encaminha ao setor competente | Material distribuído | Atena | Especialidade pericial | Fila do setor técnico | 0,17 | Sim, com regra clara |
| Processamento pericial | Perito criminal | Vestígio e requisição | Realiza exames e análises | Resultado técnico e material remanescente | Registros técnicos / Atena | Método e protocolo pericial | Fila de exames | 0,50 | Pouco |
| Emissão do laudo | Perito criminal | Resultados dos exames | Elabora, revisa e assina laudo | Laudo pericial | Atena / laudo | Validação técnica do perito | Fila de elaboração / revisão | 0,50 | Sim, com apoio humano |
| Separação pós-exame | Equipe técnica | Material processado | Separa vestígios remanescentes e contraprovas | Materiais para destinos distintos | RNC / registros | Natureza e destinação | Setor técnico | 0,17 | Pouco |
| Preparação da devolução | Equipe do Laboratório | Vestígios remanescentes | Confere, acondiciona e registra saída | Material para devolução | Atena / RNC | Identificação e integridade | Área de expedição | 0,25 | Sim, com apoio humano |
| Devolução à autoridade | Servidor / transportador autorizado | Vestígio e documentação | Entrega e registra transferência | Vestígio sob guarda policial | RNC / comprovante | Identificação do recebedor | Aguarda retirada / transporte | 0,25 | Pouco |
| Preparação da contraprova | Perito / equipe técnica | Alíquota ou material biológico | Identifica e acondiciona | Contraprova preparada | Registros / etiquetas | Requisitos de conservação | Setor técnico | 0,17 | Pouco |
| Recebimento na custódia | Núcleo de Custódia | Contraprova e registros | Confere, registra e recebe | Contraprova custodiada | Atena / controles internos | Integridade e identificação | Fila de recebimento | 0,25 | Sim, com apoio humano |
| Armazenamento | Núcleo de Custódia | Contraprova recebida | Organiza e armazena conforme categoria | Material localizado na custódia | Controle de localização | Conservação e segurança | Sala / contêiner refrigerado | 0,17 | Sim, com apoio humano |

**Decisões e aprovações:** #	Decisão (gateway)	Critério	Caminho SIM	Caminho NÃO
1	Documentação e lacres estão conformes?	Conferência da requisição, identificação, integridade e registros de custódia.	Receber e registrar o vestígio.	Registrar inconsistência e encaminhar para avaliação do responsável.
2	O material está apto ao processamento?	Condições técnicas, natureza do vestígio e exame solicitado.	Encaminhar ao setor técnico competente.	Submeter à avaliação técnica para providências.
3	O exame pericial foi concluído?	Finalização das análises e validação dos resultados.	Emitir o laudo e encaminhar os materiais à destinação aplicável.	Manter o material sob controle até a conclusão.
4	O material é uma contraprova?	Identificação de alíquota ou amostra destinada a eventual contraperícia.	Encaminhar ao Núcleo de Custódia do Laboratório.	Seguir o fluxo de devolução dos vestígios remanescentes à autoridade policial, quando aplicável.
5	A contraprova exige refrigeração?	Natureza do material e requisitos de conservação.	Armazenar em contêiner refrigerado.	Armazenar em sala de custódia apropriada.
6	Existe solicitação autorizada de retirada ou destinação?	Requisição formal, competência e requisitos legais.	Registrar e executar a movimentação autorizada.	Manter o material armazenado.
**Exceções:** O fluxo atual apresenta caminhos alternativos relacionados a inconsistências documentais, violações de lacres, necessidade de exames complementares, atrasos na retirada dos vestígios, condições especiais de conservação e solicitações de contraprova.
Essas situações exigem registros, avaliações técnicas e, quando aplicável, autorizações específicas, podendo gerar espera, retrabalho e movimentações adicionais.
Destacam-se como gargalos a dependência da retirada dos vestígios pelas autoridades policiais e a necessidade de gerenciamento de contraprovas em diferentes condições de armazenamento.
**Já digitalizado:** 1. Registro das requisições periciais e identificação dos procedimentos.
2. Cadastro dos vestígios e informações relacionadas aos exames.
3. Acompanhamento das etapas periciais e movimentações registradas no sistema.
4. Elaboração, emissão e disponibilização dos laudos periciais.
5. Registros de encaminhamento e devolução dos materiais, conforme as funcionalidades utilizadas.
6. Auto de Entrega da Devolução, é emitido pelo sistema Atena e assinado pela autoridade na entrega e na retirada, com os lacres respectivos. Após a devolução o documento é digitalizado no protocolo correspondente.

# Anexo B — TO-BE (o fluxo depois da mudança)

**Visão do futuro:** Com a implantação da Central de Custódia Definitiva, a POLITEC/MT deixa de manter a guarda pós-pericial descentralizada entre delegacias e unidades técnicas e passa a centralizar o recebimento, armazenamento e gerenciamento dos vestígios processados e contraprovas, com rastreabilidade, segurança e apoio de inteligência artificial na gestão logística,  bem como no controle e na previsão de elegibilidade para descarte, conforme a natureza de cada vestígio e os requisitos legais aplicáveis, mediante autorização competente.
**Mudança principal:** A custódia pós pericial deixa de ser descentralizada e passa a ser realizada pela Central de Custódia Definitiva, com gestão integrada dos vestígios, controle de armazenamento, rastreabilidade e previsão de demanda e descarte, apoiados por inteligência artificial e respeitando as exigências legais.
**O que fica igual:** Permanecem inalterados os procedimentos técnicos de coleta, identificação, acondicionamento e processamento pericial dos vestígios, bem como a elaboração e assinatura dos laudos pelos peritos responsáveis. A conferência física, a verificação da integridade dos lacres e a transferência formal de responsabilidade continuam exigindo intervenção humana, assim como as autorizações legais para movimentação e descarte dos materiais.

**O que não pode mudar:** Devem ser preservadas as exigências legais da cadeia de custódia previstas nos artigos 158-A a 158-F do Código de Processo Penal, garantindo a integridade, autenticidade, rastreabilidade e segurança dos vestígios. Permanecem obrigatórias a identificação dos responsáveis, o registro das movimentações, a observância das condições específicas de conservação e a autorização competente para destinação ou descarte. A inteligência artificial não poderá substituir decisões técnicas, atribuições legais ou a responsabilidade dos servidores e autoridades competentes.
| Etapa | O que muda | Quem executa | Benefício | Esforço |
|---|---|---|---|---|
| Coleta e requisição pericial | Mantidos os procedimentos legais e técnicos de origem. | A pessoa, sem mudança | Preservação da cadeia de custódia. | Baixo |
| Recebimento e processamento pericial | Mantidos os exames, conferências técnicas e emissão dos laudos. | A pessoa, sem mudança | Continuidade e segurança dos procedimentos periciais. | Baixo |
| Preparação pós-processamento | Vestígios remanescentes e contraprovas passam a ser destinados à Central, conforme regras aplicáveis. | A pessoa assistida pela máquina | Padronização do encaminhamento e redução de inconsistências. | Médio |
| Cadastro e classificação dos materiais | Sistema identifica categorias e sugere condições de armazenamento. | A pessoa assistida pela máquina | Melhor organização e menor retrabalho. | Médio |
| Encaminhamento à Central | Substituição do fluxo rotineiro de devolução às delegacias pelo encaminhamento à Central. | A pessoa assistida pela máquina | Concentração da custódia institucional e rastreabilidade. | Alto |
| Recebimento na Central | Conferência física e validação dos registros de transferência de custódia. | A pessoa assistida pela máquina | Maior controle de entrada e identificação dos responsáveis. | Médio |
| Endereçamento inteligente | Sistema sugere contêiner e posição conforme categoria, compatibilidade e capacidade. | A máquina (automação) | Otimização da ocupação e localização dos materiais. | Alto |
| Armazenamento físico | Materiais são acondicionados e movimentados em estruturas apropriadas. | A pessoa assistida pela máquina | Segurança, conservação e organização logística. | Alto |
| Monitoramento de ocupação | Sistema acompanha entradas, saídas, capacidade e tendências de crescimento. | A máquina (automação) | Previsão de saturação e planejamento de expansão. | Alto |
| Localização e consulta | Pesquisa digital por identificação, categoria, lacre e endereço. | A máquina (automação) | Redução do tempo de busca e recuperação de informações. | Médio |
| Controle de elegibilidade para descarte | Sistema sinaliza materiais potencialmente aptos à destinação conforme critérios legais cadastrados. | A pessoa assistida pela máquina | Apoio à gestão do acervo e planejamento da capacidade. | Alto |
| Autorização e execução do descarte | Decisão competente e execução supervisionada, com registros de custódia. | A pessoa assistida pela máquina | Destinação legalmente adequada e auditável. | Médio |

**Piloto do TO-BE:** Realizar projeto-piloto de 90 dias no Núcleo de Custódia do Laboratório Forense da POLITEC/MT, simulando o futuro fluxo da Central de Custódia Definitiva. Testar o cadastro, a classificação, o endereçamento inteligente, a rastreabilidade e a previsão de ocupação dos materiais, utilizando dados históricos e amostras de registros. Comparar os tempos de recebimento, registro e localização antes e depois da intervenção, avaliando a eficiência operacional, a segurança e a viabilidade da implantação.

# Anexo C — Pesquisa, riscos e plano

**Hipótese de campo:** A centralização da custódia pós-pericial, associada ao endereçamento inteligente e à previsão de ocupação dos contêineres, reduzirá o tempo de localização e movimentação dos vestígios, melhorando a rastreabilidade e o planejamento da capacidade de armazenamento.
**Lacunas:** Ainda não foram identificados dados consolidados sobre o volume total de vestígios pós-processamento devolvidos às delegacias, o tempo médio de recebimento, conferência, localização e movimentação dos materiais, a capacidade atual de armazenamento e os custos logísticos da custódia descentralizada. Também precisam ser definidos os requisitos técnicos de capacidade dos contêineres e validados os critérios legais de destinação por categoria. Os ganhos estimados de automação são hipotéticos e deverão ser avaliados por meio de medições operacionais e testes do MVP.
| Marco | Data | Responsável | Depende de | Situação |
|---|---|---|---|---|
| Concluir diagnóstico e requisitos | 06/11/2026 | Responsável pelo projeto | Formulário e mapeamento AS-IS | em andamento |
| Preparar dados fictícios e regras | 13/11/2026 | Responsável pelo projeto | Definição de categorias e capacidade | planejado |
| Desenvolver MVP em HTML | 27/11/2026 | Responsável pelo projeto | Dados e regras definidos | planejado |
| Publicar protótipo no GitHub Pages | 04/12/2026 | Responsável pelo projeto | MVP funcional e testes básicos | planejado |
| Testar cadastro, localização e ocupação | 18/12/2026 | Responsável pelo projeto | Protótipo publicado | planejado |
| Levantar linha de base operacional | 15/01/2027 | Equipe da custódia, se autorizada | Autorização e disponibilidade | planejado |
| Avaliar resultados e apresentar proposta | 29/01/2027 | Responsável pelo projeto | Testes e indicadores consolidados | planejado |

| Risco | Probabilidade | Impacto | Mitigação |
|---|---|---|---|
| Dados operacionais insuficientes | Alta | Alto | Medir amostra de operações e declarar limitações |
| Regras de conservação inadequadas | Média | Alto | Validar categorias e restrições com especialistas |
| Previsão de ocupação imprecisa | Alta | Médio | Usar cenários fictícios e comparar projeções |
| Falhas de cadastro ou endereçamento | Média | Alto | Validar campos, compatibilidade e capacidade |
| Exposição de dados institucionais | Baixa | Alto | Usar exclusivamente dados fictícios |
| Dificuldade de desenvolvimento | Média | Médio | Priorizar funcionalidades essenciais em HTML |
| Atraso na autorização institucional | Média | Médio | Separar MVP acadêmico da coleta de dados reais |

**Apoio necessário:** Preciso do apoio da chefia do Laboratório Forense e da Coordenadoria de Custódia de Evidências para validar o fluxo de custódia, as categorias de vestígios e as necessidades de armazenamento. A equipe de TI poderá orientar sobre segurança, integração futura com o Atena e infraestrutura institucional. Também será necessária a participação de servidores da custódia para medir tempos operacionais, mediante autorização. O MVP acadêmico poderá ser desenvolvido independentemente dessas liberações, utilizando dados fictícios.
**Aprendizado necessário:** Preciso aprofundar conhecimentos em modelagem de processos, desenvolvimento básico com HTML, CSS e JavaScript, publicação no GitHub Pages, estruturação de dados em JSON, criação de regras de classificação e endereçamento, indicadores de ocupação e métodos simples de previsão de demanda. Também será necessário aprender a testar o protótipo, identificar erros e avaliar os resultados das métricas propostas.

# Anexo D — A defesa

**Frase de defesa:** Se o endereçamento inteligente reduzir em 60% o tempo de localização dos vestígios, a Central de Custódia Definitiva poderá agilizar a recuperação dos materiais, melhorar a rastreabilidade e tornar mais eficiente a gestão do acervo pericial.
**Provas:** 1. O Código de Processo Penal, nos artigos 158-A a 158-F, estabelece requisitos para a cadeia de custódia, incluindo armazenamento e rastreabilidade dos vestígios. 2. Em 2025, o Laboratório Forense recebeu aproximadamente 12.000 alíquotas de contraprovas provenientes do interior, evidenciando demanda expressiva de armazenamento. 3. Atualmente, parte dos materiais pós-periciais é devolvida às delegacias e as contraprovas permanecem sob guarda do Laboratório, demonstrando a descentralização da custódia e a necessidade de planejamento para sua futura centralização.
**Piloto:** Realizarei um piloto demonstrativo de 90 dias, utilizando um MVP com dados fictícios para testar cadastro, classificação, endereçamento, localização e previsão de ocupação dos contêineres. Serão comparados os tempos de localização e registro, a precisão das regras de armazenamento e a capacidade de antecipar a saturação. Havendo autorização institucional, serão coletadas medições operacionais reais para comparação com as metas hipotéticas.
**Maior risco:** O maior risco é a classificação ou o endereçamento inadequado dos vestígios, comprometendo sua conservação e rastreabilidade. Para mitigá-lo, serão estabelecidas regras de compatibilidade por categoria, capacidade e condições de armazenamento, com validação humana obrigatória. O MVP utilizará apenas dados fictícios e não realizará movimentações físicas, transferências ou descartes reais.

# Anexo E — Documentos enviados

**Descrição dos documentos:** -
**O que ainda falta:** -
