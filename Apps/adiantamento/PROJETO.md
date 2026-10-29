# PROJETO.md — FLUXO DE ADIANTAMENTO

**Aluno ou equipe:** Jaqueline e Linicker
**Unidade:** POLITEC-DAS E SESP-GABINETE
**Contato:** jaquelineaguiar@politec.mt.gov.br
**Projeto:** FLUXO DE ADIANTAMENTO
**Tipo de projeto:** Aplicativo web / portal
**Data:** 2026-10-27
**Resumo:** Protótipo para a DAS/POLITEC acompanhar cada adiantamento, do pedido com 3 orçamentos à prestação de contas aprovada, com as etapas, os prazos do Decreto nº 1.487/2022 e as pendências. Não substitui o SICAD.

## 1. Problema (a dor)

**Problema:** Inicial na solicitação e no final prestação de contas
**Impacto:** ERROS NA SOLICITAÇÃO E PRESTAÇÃO DE CONTAS E DEMORA NA EXECUÇÃO DE SERVIÇO OU COMPRA EMERGENCIAL.
**Quem sofre:** Equipe interna, Chefia, Autoridade, Servidor da unidade, Cidadão externo
**Como é feito hoje:** SISTEMA SEM FLUXO, AS VEZES O SERVIDOR LANÇA SEM PASSAR PELO SETOR ADMINISTRATIVO DA POLITEC, E O PROCESSO VAI DIRETO PARA A SESP.
**Evidências:** Planilha ou controle local, Medida feita pela equipe
**Detalhe da evidência:** CONTROLE DE PEDIDOS DE ADIANTAMENTOS E INFORMAÇÕA DA PRÓPRIA SESP QUANDO O ADIANTAMENTO CHEGA SEM INFORMAÇÃO PRÉVIA.
**O que não pode ser automatizado:** A autorização, a aprovação e o pagamento continuam no SICAD, com as autoridades competentes. O app registra e alerta.

## 2. Objetivo do MVP (o que faz e o que NÃO faz)

**Objetivo do MVP:** Provar que a DAS consegue ver, num só lugar, em que etapa está cada adiantamento, quanto tempo ele está parado e quais prazos estão perto de vencer.
**O que o MVP não faz:** O MVP não realiza pagamentos, não autoriza despesas, não concede adiantamentos e não substitui o lançamento oficial no SICAD. Também não valida automaticamente a autenticidade das notas fiscais nem realiza a aprovação formal da prestação de contas.
**Entregável do projeto:** Desenvolver um protótipo funcional para auxiliar no controle e acompanhamento do processo de concessão, utilização e prestação de contas de adiantamentos da POLITEC e SESP/MT, desde a solicitação inicial até a análise final pela contabilidade e aprovação do ordenador de despesas.
**Dentro do escopo:** Cadastro da solicitação de adiantamento, com identificação do servidor, unidade solicitante, finalidade e valor.
Registro dos três orçamentos e da justificativa da necessidade.
Acompanhamento das etapas de autorização e aprovação.
Controle do status do processo: em análise, aprovado, pendente de correção ou concluído.
Registro das notas fiscais e dos comprovantes necessários à prestação de contas.
Controle das pendências identificadas pela contabilidade da SESP.
Acompanhamento do encaminhamento para aprovação do ordenador de despesas.
Visualização de um painel com os processos em andamento, concluídos e pendentes.
**Fora do escopo:** Transferência financeira direto na conta do servidor.
**Plataforma alvo:** Site web (abre no navegador)
**Primeira tela:** Pedido de solicitação
**Simulado no MVP:** Solicitação de pedido de adiantamento quanto ao problema gerado
**Critério de aceite:** Com 10 pedidos fictícios, a DAS registra um pedido completo, avança as etapas, registra uma devolução da contabilidade e vê no painel os processos vencidos e o tempo por etapa.
**Dados de exemplo:** Número do processo ou da solicitação;
Nome fictício do servidor solicitante;
Unidade administrativa;
Finalidade do adiantamento;
Valor solicitado;
Situação do processo;
Documentação apresentada;
Pendências identificadas;
Responsável pela etapa atual.
Exemplos de situações de exceção:
1. Documentação incompleta: ausência de um dos três orçamentos ou da justificativa da necessidade.
2. Prestação de contas com inconsistência: nota fiscal ou comprovante que necessita de correção ou complementação.
3. Processo pendente de aprovação: documentação encaminhada, mas aguardando análise ou decisão da autoridade competente.
**O que já existe pronto e pode ser reaproveitado:** Podem ser reaproveitados os procedimentos internos já utilizados pela POLITEC  e pela SESP/MT para solicitação, concessão e prestação de contas de adiantamentos, bem como os modelos de documentos, formulários, planilhas de controle e orientações administrativas existentes.
Também poderão ser utilizados:
- O fluxo de trabalho já definido para solicitação e prestação de contas;
- Os modelos de justificativa da necessidade e de levantamento de orçamentos;
- Os checklists de documentos exigidos;
- As planilhas de acompanhamento de processos e pendências;
- O template de aplicativo disponibilizado pelo professor no GitHub Pages, para desenvolver a interface do protótipo.
**Dependências:** O desenvolvimento e a validação do MVP dependem da colaboração das seguintes áreas:
- Diretoria de Administração Sistêmica (DAS/POLITEC): responsável por fornecer informações sobre o fluxo de solicitação e acompanhamento dos adiantamentos, além de validar as necessidades da área administrativa.
- SESP/MT – Setor de Contabilidade: responsável por orientar sobre a documentação exigida, os procedimentos de análise da prestação de contas e o tratamento de inconsistências.
- Chefias e gestores das unidades: responsáveis por validar as etapas de solicitação, justificativa e aprovação interna.
- Tecnologia da Informação (TI): poderá apoiar a evolução do protótipo, especialmente em futuras integrações com sistemas institucionais.
- Professor responsável pelo projeto: responsável por orientar o desenvolvimento técnico do MVP .

## 3. Usuários e papéis

| Papel | Quem é | O que enxerga | O que faz | O que não pode fazer | Registro |
|---|---|---|---|---|---|
| Servidor solicitante | Coordenador, gerente ou servidor da unidade | Os próprios pedidos e pendências | Registra o pedido e anexa a lista dos orçamentos | Enviar à SESP sem passar pela DAS | Pedido, datas e anexos informados |
| DAS/POLITEC | Diretoria de Administração Sistêmica | Todos os pedidos da POLITEC | Analisa a viabilidade, acompanha etapas e prazos | Aprovar no lugar do ordenador | Parecer, etapas e pendências |
| Contabilidade da SESP | Setor de contabilidade | Prestações de contas enviadas | Registra devoluções e motivos (quando usar o app) | Alterar o pedido | Devoluções e ressalvas |
| Ordenador de despesas | Autoridade da SESP | Painel (consulta) | Consulta o andamento | Nenhuma ação no app | Nenhum |

**Observações sobre os papéis:** O MVP é usado pela DAS. O servidor solicitante e a contabilidade aparecem como responsáveis das etapas; o ordenador só consulta o painel.

## 4. Dados (entidades e colunas; tudo SINTÉTICO)

| Entidade | O que representa | Colunas | Chave | Volume | Origem | Sintético |
|---|---|---|---|---|---|---|
| Processo | Um pedido de adiantamento | id: texto, numero_sicad: texto, unidade: texto, finalidade: texto, tipo: texto (compra, serviço, predial), valor_solicitado: número, situacao: texto, etapa_atual: texto, criado_em: data | id | 60 por ano (5 POLITEC + 55 SESP informados) | DAS | Sim |
| Orcamento | Um dos 3 orçamentos | id: texto, processo_id: texto, fornecedor: texto, cnpj: texto, valor: número | id | 3 por processo | Servidor | Sim |
| Etapa | Passagem do processo por uma etapa | id: texto, processo_id: texto, etapa: texto, entrada_em: data, saida_em: data, responsavel: texto | id | Até 12 por processo | DAS | Sim |
| Pendencia | Devolução para correção | id: texto, processo_id: texto, motivo: texto, aberta_em: data, prazo: data, resolvida_em: data | id | Poucas por processo | Contabilidade e DAS | Sim |
| NotaFiscal | Comprovante da prestação de contas | id: texto, processo_id: texto, numero: texto, cnpj: texto, valor: número, data: data | id | Variável | Servidor | Sim |

**O que precisa ser coletado:** Informação imediata da solicitação
**Quem libera o acesso:** Quando solicita o cartão coorporativo.

### Fontes de dados do processo real

| Fonte | Tipo | Onde | Existe | Uma linha é | Volume | Campos de data | Atualiza | LGPD |
|---|---|---|---|---|---|---|---|---|
| Controle de pedidos da DAS | Planilha local | DAS/POLITEC | Parcialmente | Um pedido | 5 por ano na POLITEC | Data de entrada | Manual | Duvidaso |
| SICAD | Sistema oficial | Governo de MT | Sim | Um processo | 60 por ano | Datas de cada tramitação | A cada tramitação | Sim |


## 5. Regras de negócio (RN01, RN02...)

| ID | Regra | Quando se aplica | Exceção | Quem valida | Tipo |
|---|---|---|---|---|---|
| RN01 | O pedido exige 3 orçamentos e a justificativa | Ao registrar o pedido | Nenhuma | Sistema | Validação |
| RN02 | Todo pedido passa pela DAS antes do cadastro no SICAD | Início do processo | Nenhuma | DAS | Negócio |
| RN03 | Aplicação do recurso em até 90 dias (180 para intervenção predial simplificada) | Após o pagamento | Nenhuma | Sistema (alerta) | Cálculo |
| RN04 | Prestação de contas em até 30 dias corridos após o fim da aplicação | Após a aplicação | Nenhuma | Sistema (alerta) | Cálculo |
| RN05 | Correção de pendência em até 10 dias úteis após a notificação | Ao registrar a devolução | Nenhuma | Sistema (alerta) | Cálculo |
| RN06 | A soma das notas fiscais não pode passar do valor concedido | Na prestação de contas | Diferença vira alerta para a DAS | Sistema | Validação |
| RN07 | O app não aprova nem autoriza: registra o que aconteceu no SICAD | Em todas as etapas | Nenhuma | DAS | Negócio |


## 6. Telas (#/painel, #/lista...)

| Rota | Tela | Objetivo | Quem usa | Dados | Ação | Regra | Tipo | Verificável como | MVP |
|---|---|---|---|---|---|---|---|---|---|
| #/painel | Painel | Ver processos por situação e prazos | DAS | Situação, etapa, dias na etapa, prazos | Filtrar e abrir o processo | RN05 | Tela | Painel mostra o processo vencido em vermelho | Sim |
| #/pedido/novo | Novo pedido | Registrar o pedido na DAS | Servidor e DAS | Unidade, finalidade, valor, 3 orçamentos, justificativa | Salvar | RN01 e RN02 | Tela | Pedido sem 3 orçamentos é recusado | Sim |
| #/processo/:id | Processo | Acompanhar etapas e pendências | DAS e servidor | Linha do tempo, pendências, prazos | Avançar etapa, registrar pendência | RN03 e RN04 | Tela | A etapa nova fica com data e responsável | Sim |
| #/processo/:id/prestacao | Prestação de contas | Registrar notas e comprovantes | Servidor | Notas fiscais, valores, fotos | Salvar | RN06 | Tela | Soma das notas comparada ao valor concedido | Sim |
| #/relatorio | Relatório | Tempo por etapa e devoluções | DAS | Médias e contagens do período | Imprimir ou exportar CSV |  | Relatório | Relatório confere com a contagem manual | Sim |


## 7. KPIs (nome = fórmula em uma linha)

| KPI | Pergunta | Fórmula | Fonte | Linha de base | Valor esperado | Como medir |
|---|---|---|---|---|---|---|
| Tempo do pedido até o pagamento | Quanto tempo leva do pedido ao recurso na conta? | Data do pagamento − data do pedido na DAS | Etapas do app | 5 dias por pedido (informado) | 3 dias | Anotar as datas dos pedidos de 4 semanas |
| Prestações devolvidas | Quantas prestações voltam para correção? | Devolvidas ÷ prestações enviadas × 100 | Pendências do app | A medir | Metade da linha de base | Contar as devoluções do último ano |
| Pedidos sem passar pela DAS | Quantos pedidos chegam à SESP sem a DAS? | Pedidos sem registro na DAS ÷ total | Informação da SESP | A medir | Zero | Comparar a lista da SESP com o controle da DAS |

**Período da linha de base:** Todos os registro anual de janeiro a dezembro
**Campos de data e tempo que existem:** Tem data de entrada e finalida

## 8. Stack: HTML único (CSS/JS inline), dados em JSON embutido, GitHub Pages.

**Stack escolhida:** HTML único (CSS/JS inline), dados em JSON embutido, GitHub Pages
**Detalhe da stack:** Um único index.html (HTML, CSS e JS embutidos), com os processos no IndexedDB do navegador da DAS, cálculo de prazos em dias corridos e úteis, painel em SVG próprio e backup .json. Publicado no GitHub Pages sem dados.
**Hospedagem:** A escolha se justifica pela simplicidade de implantação, ausência de custos iniciais de hospedagem e compatibilidade com o padrão da aula, que prevê um arquivo HTML único com CSS, JavaScript e dados fictícios incorporados.
A plataforma permitirá acessar o protótipo pelo navegador, apresentar as telas de cadastro, acompanhamento e prestação de contas e validar o fluxo do processo de adiantamento.
**Custo e licenças:** Hospedagem no GitHub Pages	R$ 0,00
Desenvolvimento com HTML, CSS e JavaScript	R$ 0,00
Editor de código gratuito	R$ 0,00
Domínio personalizado	R$ 0,00 inicialmente
Banco de dados	R$ 0,00 no MVP
Licenças de software	R$ 0,00, utilizando ferramentas gratuitas
Custo inicial estimado: R$ 0,00.
**Contas e domínio:** Conta: o responsável pelo projeto, com orientação do professor, criará ou utilizará uma conta GitHub autorizada.
Repositório: o responsável pelo desenvolvimento criará o repositório e publicará os arquivos do protótipo.
Endereço eletrônico: será utilizado o endereço gratuito fornecido pelo GitHub Pages.
Acesso: o link será disponibilizado ao professor e aos participantes autorizados para avaliação e testes.
Implantação institucional: caso o projeto evolua para uso real na POLITEC, a criação de domínio institucional e a definição dos acessos dependerão de autorização da chefia e da TI competente.

| Opção | Tipo | Onde roda | Custo | Quem mantém | Acesso | Banco de dados | Escala | Limitação |
|---|---|---|---|---|---|---|---|---|
| Arquivo HTML único | Arquivo local | Navegador do computador da unidade | Zero | Equipe do projeto | Quem recebe o arquivo | IndexedDB do navegador | Uma cópia por setor; consolidação por arquivo .json | Os dados ficam no computador; backup semanal |
| GitHub Pages | Estática e gratuita | github.io | Zero | Equipe do projeto | Link (o app; os dados ficam no navegador) | Não tem | Baixa | Publica só o app, nunca os dados |


## 9. Restrições e LGPD

**Restrições:** Não poderá substituir o SICAD, sistema oficial de concessão e prestação de contas de adiantamentos em Mato Grosso. 
IMAD
Não terá integração com os sistemas oficiais da POLITEC/SESP.
Utilizará somente dados fictícios durante os testes.
Não realizará concessões, pagamentos, aprovações ou validações contábeis oficiais.
Dependerá da validação dos procedimentos administrativos pela DAS/POLITEC e pela área contábil da SESP.
A publicação em plataforma externa dependerá da avaliação das regras institucionais de segurança da informação.
Os prazos e documentos exigidos deverão seguir a legislação vigente e as orientações dos setores competentes.
**Dados pessoais tratados:** Nome e matrícula do servidor solicitante, valores e dados de fornecedores (pessoa jurídica). Sem CPF: o SICAD já identifica o servidor.
**Base legal:** Decreto Estadual nº 1.487/2022, Instrução Normativa nº 010/2023/SEPLAG, Lei Estadual nº 11.648/2021, Orientação Técnica nº 02/2026 da CGE/MT
**Retenção:** No Decreto Estadual nº 1.487/2022, de Mato Grosso, os prazos principais são: - Utilização do recurso: até 90 dias para compras e serviços em geral, ou até 180 dias para intervenções prediais simplificadas (art. 10). - Prestação de contas: até 30 dias corridos após o término do período de aplicação (art. 14). - Correção de inconsistências: até 10 dias úteis após a notificação (art. 14, § 3º).
**Acesso e registro:** Servidor solicitante, chefia imediato, servidores que analisam e autorizam o andamento da solicitação.
**Requisitos marcados:** LGPD e dado pessoal, Segurança e controle de acesso, Trilha de auditoria, Funcionar offline

---

# Anexo A — AS-IS (o fluxo de hoje)

**Início:** E-MAIL AO SETOR ADMINISTRATIVO
**Fim:** PROCESSO ARQUIVADO
**Entradas:** FOTOS E ORÇAMENTOS
**Saídas:** NOTA FISCAL E FOTOS
**Volume:** 5 POLITEC E 55 SESP
**Duração:** 5 DIAS POR PROCESSO PARA PEDIDO INICIAL
**Frequência:** Diário
| Etapa | Quem faz | O que entra | Ação | O que sai | Sistema | Regra | Onde espera | Tempo (h) | Automatizável |
|---|---|---|---|---|---|---|---|---|---|
| Levantar orçamentos | Coordenador ou gerente da unidade | Necessidade de compra ou serviço | Reúne 3 orçamentos | 3 orçamentos | E-mail | 3 orçamentos obrigatórios | Fornecedores | A medir | Não |
| Encaminhar à DAS | Coordenador ou gerente | Orçamentos | Envia por e-mail para análise | Pedido na DAS | E-mail | Passar pela DAS antes do SICAD | Caixa da DAS | A medir | Sim, com regra clara |
| Cadastrar no SICAD | Servidor solicitante | Manifestação favorável da DAS | Registra o pedido com orçamentos e justificativa | Pedido no SICAD | SICAD | Anexar 3 orçamentos e justificativa | Não identificado | A medir | Pouco |
| Aprovar (chefia imediata) | Chefia imediata | Pedido no SICAD | Aprova ou devolve | Pedido aprovado | SICAD | Aprovação da chefia | Caixa da chefia | A medir | Não |
| Conferir documentos (SESP) | Setor financeiro da SESP | Pedido aprovado | Confere pelo checklist | Pedido conferido | SICAD | Checklist da SESP | Fila do financeiro | A medir | Sim, com apoio humano |
| Confirmar dotação (NGER) | NGER, a pedido do ordenador | Pedido conferido | Verifica disponibilidade orçamentária | Dotação confirmada | SICAD | Disponibilidade orçamentária | Fila do NGER | A medir | Não |
| Autorizar | Ordenador de despesas | Dotação confirmada | Autoriza o adiantamento | Adiantamento autorizado | SICAD | Requisitos atendidos | Caixa do ordenador | A medir | Não |
| Pagar | Setor orçamentário e financeiro | Autorização | Empenha e paga | Recurso na conta | SICAD | Procedimentos orçamentários | Fila do financeiro | A medir | Não |
| Aplicar o recurso | Servidor solicitante | Recurso | Compra ou contrata | Notas fiscais e fotos | Externo | Até 90 dias (180 para intervenção predial) | Fornecedor | A medir | Não |
| Prestar contas | Servidor solicitante | Notas fiscais e fotos | Lança no SICAD e envia à contabilidade | Prestação de contas | SICAD | Até 30 dias após o fim da aplicação | Fila da contabilidade | A medir | Pouco |
| Analisar a prestação | Contabilidade da SESP | Prestação de contas | Confere e devolve se houver pendência | Prestação conferida ou devolvida | SICAD | Correção em até 10 dias úteis | Correção do servidor | A medir | Sim, com apoio humano |
| Aprovar e encerrar | Ordenador de despesas e contabilidade | Prestação conferida (ou com ressalvas) | Aprova e encerra | Processo arquivado | SICAD | Ressalvas: decisão do ordenador | Caixa do ordenador | A medir | Não |

**Decisões e aprovações:** ORDENADOR DE DESPESAS - SESP
**Exceções:** NÃO TEM 
**Já digitalizado:** TUDO

# Anexo B — TO-BE (o fluxo depois da mudança)

**Visão do futuro:** Quando o app existir, a DAS sabe em que etapa está cada adiantamento e quais prazos vão vencer, e nenhum pedido chega à SESP sem a análise da DAS.
**Mudança principal:** Todo pedido passa pela DAS e é acompanhado no app, com datas por etapa e alertas de prazo, enquanto a tramitação oficial segue no SICAD.
**O que fica igual:** o servidor continua sendo responsável pela solicitação
**O que não pode mudar:** normativas
| Etapa | O que muda | Quem executa | Benefício | Esforço |
|---|---|---|---|---|
| Registrar o pedido na DAS | A DAS registra o pedido no app antes do SICAD, com checklist dos 3 orçamentos | A pessoa assistida pela máquina | Nenhum pedido chega à SESP sem passar pela DAS | Baixo |
| Acompanhar as etapas | Cada mudança de etapa no SICAD é anotada no app com a data | A pessoa assistida pela máquina | Saber onde o processo está e há quanto tempo | Baixo |
| Alertar prazos | O app calcula os prazos de aplicação, prestação e correção e avisa antes do vencimento | A máquina (automação) | Prestação de contas no prazo | Médio |
| Registrar pendências | Devoluções da contabilidade viram pendências com prazo de 10 dias úteis | A pessoa assistida pela máquina | Correção no prazo e motivo registrado | Baixo |
| Painel | Processos por situação, tempo por etapa e devoluções | A máquina (automação) | Gargalo visível | Médio |

**Piloto do TO-BE:** No Órgão

# Anexo C — Pesquisa, riscos e plano

**Hipótese de campo:** A hipótese é que a ausência de um controle centralizado das etapas, datas e pendências dos processos de adiantamento dificulta o acompanhamento dos prazos pela POLITEC, aumentando o risco de atrasos, inconsistências documentais e retrabalho administrativo.
| Referência | Tipo | Fonte ou link | Ano | Dado que extrai | Como usar na defesa | Link conferido |
|---|---|---|---|---|---|---|
| Decreto Estadual nº 1.487/2022 | Norma ou lei | Consultar IOMAT | 2022 | Regulamenta a concessão, aplicação e prestação de contas do suprimento de fundos e define o SICAD como sistema oficial. | Demonstrar a necessidade de manter o MVP alinhado ao fluxo e às regras oficiais. | Sim |
| Instrução Normativa nº 010/2023/SEPLAG | Norma ou lei | Consultar PDF oficial | 2023 | Estabelece procedimentos para solicitação, concessão, aplicação e prestação de contas. | dentificar documentos, etapas e controles que devem ser considerados no protótipo. | Sim |
| Lei Federal nº 13.709/2018 — LGPD | Norma ou lei | Consultar PDF oficial | 2018 | Estabelece regras para o tratamento de dados pessoais. | Justificar o uso de dados fictícios no MVP e os cuidados necessários em uma futura implantação. | Sim |
| Orientação Técnica nº 06/2025 — CGE/MT | Documento interno | Consultar PDF oficial | 2025 | Orienta os órgãos estaduais sobre procedimentos de suprimento de fundos realizados por meio do SICAD. | Reforçar a importância da conformidade com os procedimentos oficiais. | Sim |
| Decreto Estadual nº 1.487/2022, arts. 10 e 14 | Norma ou lei | IOMAT | 2022 | Prazos de aplicação (90 e 180 dias), prestação (30 dias) e correção (10 dias úteis) | Base das regras RN03 a RN05 | Não |

**Lacunas:** Até o momento, não foram levantados dados quantitativos sobre o tempo médio de tramitação dos adiantamentos, a quantidade de processos devolvidos para correção ou os principais motivos de atraso na POLITEC.
Também é necessário confirmar com a DAS/POLITEC e a contabilidade da SESP se existe planilha ou relatório interno com essas informações, bem como verificar eventuais procedimentos complementares específicos da instituição.
Como próxima etapa, propõe-se acompanhar os processos durante quatro semanas, registrando as datas de entrada, encaminhamento, devolução para correção e conclusão. Os resultados permitirão avaliar a hipótese inicial e identificar oportunidades de melhoria.
| Marco | Data | Responsável | Depende de | Situação |
|---|---|---|---|---|
| Levantamento do fluxo atual de adiantamentos | Semana 1 | DAS/POLITEC | Identificação das etapas e documentos | Planejado |
| Definição dos requisitos e das informações a registrar | Semana 1 | Responsável pelo projeto | Levantamento do fluxo | Planejado |
| Início da coleta de dados sobre prazos e pendências | Semana 1 | DAS/POLITEC e setores envolvidos | Definição do formulário de controle | Planejado |
| Desenvolvimento das telas do MVP | Semana 2 | Responsável pelo projeto | Requisitos definidos e template da aula | Planejado |
| Inserção dos dados fictícios e testes funcionais | Semana 3 | Responsável pelo projeto | Protótipo desenvolvido | Planejado |
| Conclusão da coleta e análise dos resultados | Semana 4 | DAS/POLITEC | Registros das quatro semanas | Planejado |
| Apresentação do MVP e proposta de melhorias | Final da semana 4 | Responsável pelo projeto | Testes e análise dos resultados | Planejado |

| Risco | Probabilidade | Impacto | Mitigação |
|---|---|---|---|
| Falta de informações sobre o fluxo atual | Média | Alto | Consultar os setores envolvidos e documentar as etapas existentes. |
| Demora na disponibilização de informações pela SESP | Média | Alto | Iniciar o protótipo com dados fictícios, sem depender de acessos oficiais. |
| Desenvolvimento técnico acima do conhecimento disponível | Média | Médio | Utilizar o template HTML fornecido na aula e desenvolver funcionalidades simples. |
| Utilização indevida de dados pessoais ou institucionais | Baixa | Alto | Utilizar somente dados fictícios e evitar a publicação de documentos reais. |
| Falta de adesão dos servidores ao registro dos prazos | Média | Médio | Criar formulário simples e orientar os responsáveis sobre o preenchimento. |
| Protótipo ser confundido com sistema oficial | Baixa | Alto | Identificar claramente a aplicação como protótipo demonstrativo, sem validade administrativa. |
| Inconsistência entre o protótipo e as normas vigentes | Média | Alto | Validar o fluxo e os requisitos com a DAS/POLITEC e a contabilidade da SESP. |

**Apoio necessário:** Preciso do apoio da Diretoria de Administração Sistêmica (DAS/POLITEC) para validar o fluxo administrativo dos adiantamentos, identificar as principais dificuldades e definir quais informações devem ser acompanhadas.
Também será necessário o apoio do setor de contabilidade da SESP/MT para confirmar os documentos exigidos, os prazos aplicáveis, os motivos mais frequentes de devolução e os procedimentos de prestação de contas.
O professor responsável pelo curso deverá orientar a construção do protótipo e a publicação no GitHub Pages. Em uma etapa futura, caso haja interesse em implantar a solução institucionalmente, será necessária a participação da TI e das áreas responsáveis pela segurança da informação e pelos sistemas oficiais.
**Aprendizado necessário:** Desenvolvimento básico de HTML, CSS e JavaScript: para criar as telas e as funcionalidades do protótipo.
Organização de dados em JSON: para inserir e apresentar registros fictícios de solicitações e pendências.
Publicação no GitHub Pages: para disponibilizar o MVP por meio de um link acessível pelo navegador.
Mapeamento de processos: para representar corretamente as etapas de solicitação, autorização, aplicação dos recursos e prestação de contas.
Indicadores de acompanhamento: para calcular prazos de tramitação, identificar pendências e avaliar gargalos.
Legislação e procedimentos de adiantamento: para manter o protótipo alinhado às normas estaduais e aos procedimentos da POLITEC/SESP.
Noções de LGPD e segurança da informação: para evitar exposição de dados pessoais e institucionais.

# Anexo D — A defesa

**Frase de defesa:** Se o tempo de acompanhamento dos processos de adiantamento for reduzido e as pendências forem identificadas mais rapidamente, a DAS/POLITEC poderá melhorar o controle administrativo, reduzir retrabalho e dar mais agilidade à prestação de contas.”
**Provas:** 1. Necessidade de controle dos processos: o acompanhamento das solicitações, autorizações e prestações de contas envolve diferentes etapas e responsáveis, tornando importante centralizar as informações.
2. Existência de procedimentos oficiais: o Decreto Estadual nº 1.487/2022 e a Instrução Normativa nº 010/2023/SEPLAG estabelecem regras para a concessão, aplicação e prestação de contas dos adiantamentos, que precisam ser observadas no fluxo administrativo.
3. Possibilidade de medir os resultados: o registro das datas de entrada, encaminhamento, devolução para correção e conclusão permitirá identificar o tempo de tramitação e os principais pontos de atraso.
**Piloto:** - 1ª semana: mapear o fluxo atual e iniciar o registro dos processos e das respectivas datas.
- 2ª semana: desenvolver o protótipo e cadastrar pelo menos dez solicitações fictícias, incluindo casos com documentação incompleta, inconsistências e pendências de aprovação.
- 3ª semana: testar o cadastro, a atualização de status, o registro de pendências e a visualização do painel.
- 4ª semana: analisar os dados coletados, identificar gargalos e comparar os resultados disponíveis com a situação inicial.
Os principais indicadores serão o tempo médio de tramitação, a quantidade de processos pendentes, o número de devoluções para correção e o percentual de processos com informações completas.
**Maior risco:** O maior risco é desenvolver uma ferramenta que não corresponda ao fluxo real de adiantamentos da POLITEC/MT ou que apresente informações divergentes dos procedimentos oficiais da SESP/MT.
Para reduzir esse risco, o fluxo deverá ser validado previamente com a DAS/POLITEC e o setor de contabilidade da SESP. O protótipo utilizará apenas dados fictícios e não substituirá o SICAD, as autorizações oficiais ou os procedimentos de prestação de contas.
A implantação de uma solução institucional somente será considerada após a avaliação da viabilidade técnica, da segurança da informação e da conformidade com as normas aplicáveis.

# Anexo E — Documentos enviados

**Descrição dos documentos:** - **Fluxo_Adiantamento_AS-IS.docx:** descrição do procedimento atual de solicitação, concessão e prestação de contas dos adiantamentos.
- **Fluxo_Adiantamento_TO-BE.docx:** proposta de melhoria do fluxo, com acompanhamento de etapas, prazos e pendências.
- **Controle_Adiantamentos.xlsx:** planilha para registrar solicitações, responsáveis, datas, status e inconsistências.
- **Legislacao_Adiantamento.pdf:** normas e orientações aplicáveis à concessão, aplicação e prestação de contas dos adiantamentos.
- **MVP_Adiantamento.html:** protótipo demonstrativo para cadastro e acompanhamento das solicitações, utilizando dados fictícios.
**O que ainda falta:** Ainda preciso concluir o diagrama do fluxo atual (AS-IS), detalhando o início, as etapas, os responsáveis, os pontos de espera e o encerramento do processo. Também preciso elaborar o fluxo futuro proposto (TO-BE), incluindo a possibilidade de automatizar o registro de datas, o acompanhamento dos prazos e a identificação de pendências.
Para desenvolver e validar o MVP, preciso preparar uma planilha de controle com dados fictícios, definir pelo menos duas métricas de desempenho com fonte, linha de base e resultado esperado, e construir o protótipo em HTML, CSS e JavaScript. Também será necessário validar o fluxo proposto com a DAS/POLITEC e consultar a contabilidade da SESP para confirmar os procedimentos e documentos exigidos.
