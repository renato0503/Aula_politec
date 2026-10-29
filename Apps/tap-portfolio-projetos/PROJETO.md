# PROJETO.md — TAP Digital e Portfólio de Projetos Estratégicos

**Aluno ou equipe:** Danielle Marques de Almeida Trevizan
**Unidade:** Gestão de Projetos Estratégicos (a confirmar)
**Contato:** daniellealmeida@politec.mt.gov.br
**Projeto:** TAP Digital e Portfólio de Projetos Estratégicos
**Tipo de projeto:** Formulário ou modelo de coleta
**Data:** 2026-10-27
**Resumo:** O projeto visa estruturar e padronizar o fluxo de recebimento, análise técnica, validação estratégica, priorização e captação de recursos para os projetos da POLITEC, consolidando o Portfólio de Projetos Estratégicos e garantindo alinhamento institucional, viabilidade técnica e financeira, governança e direcionamento eficiente dos recursos para a execução das iniciativas prioritárias.

## 1. Problema (a dor)

**Problema:** Necessidade de padronizar e simplificar o preenchimento do Termo de Abertura de Projeto (TAP), devido à falta de uniformidade nas informações recebidas, gera retrabalho dificultando a automatização de etapas e a manutenção atualizada do Portfólio de Projetos Estratégicos. Torna-se essencial simplificar e automatizar etapas do processo e manter o Portfólio de Projetos Estratégicos atualizado e confiável.
**Impacto:** Retrabalho.
**Quem sofre:** Servidor da unidade, Equipe interna, Chefia
**Como é feito hoje:** Atualmente, o servidor encaminha a proposta de projeto por meio de formulários preenchidos fora do padrão estabelecido, frequentemente com informações incompletas e documentos pendentes, exigindo solicitações de ajustes e complementações pela equipe antes de iniciar as etapas de análise e validação.
**Evidências:** Entrevista com a equipe
**Detalhe da evidência:** Entrevista com a equipe: propostas chegam fora do padrão, incompletas e sem documentos, e voltam ao demandante antes da análise.
**O que não pode ser automatizado:** A conferência do texto do projeto.

## 2. Objetivo do MVP (o que faz e o que NÃO faz)

**Objetivo do MVP:** Demonstrar que o TAP padronizado e a validação automática conseguem reduzir o envio de propostas incompletas e o retrabalho documental, sem substituir a análise humana.
**O que o MVP não faz:** Não aprova nem rejeita projetos; não substitui parecer técnico; não define prioridade institucional sozinho; não submete automaticamente projetos a financiadores. O MVP valida apenas campos e documentos conforme regras previamente definidas.
**Entregável do projeto:** Formulário digital padronizado para o TAP, com checklist de documentos, validação de campos obrigatórios, registro de status e pendências e estrutura de dados para apoiar a atualização do Portfólio de Projetos Estratégicos. Definir com a TI a plataforma institucional adequada.
**Dentro do escopo:** Modelo único de TAP com instruções de preenchimento.

Campos obrigatórios e validação de formatos/regras objetivas.

Checklist de anexos e sinalização de documentos ausentes.

Registro de envio, status, pendências e histórico de ajustes.

Visão da equipe para triagem e acompanhamento das propostas.

Exportação/relatório dos dados para apoiar a atualização do portfólio.
**Fora do escopo:** Automatizar decisões técnicas, estratégicas ou de aprovação; integração com sistemas ainda não autorizados ou não definidos; cálculo automático de prioridade antes da validação formal dos critérios pela governança.
**Plataforma alvo:** Site web (abre no navegador)
**Primeira tela:**  formulário guiado de cadastro do projeto/TAP
**Simulado no MVP:** usar projetos e documentos fictícios, sem dados sigilosos. 
**Critério de aceite:** validação correta dos campos e checklist, com registro claro das pendências. 
**Dados de exemplo:** propostas fictícias completas e incompletas.
**O que já existe pronto e pode ser reaproveitado:** modelo atual do TAP, lista oficial de documentos exigidos e critérios institucionais existentes. 
**Dependências:** validação do TAP e dos documentos obrigatórios pela área responsável, aprovação da chefia e apoio da TI.

## 3. Usuários e papéis

| Papel | Quem é | O que enxerga | O que faz | O que não pode fazer | Registro |
|---|---|---|---|---|---|
| Demandante / Servidor | Servidor ou unidade que propõe o projeto | Seus projetos, formulário TAP, documentos e pendências | Cadastra a proposta, preenche o TAP, anexa documentos e realiza ajustes solicitados | Aprovar o próprio projeto ou alterar análises e decisões da equipe responsável | Envio, ajustes e respostas às pendências |
| Equipe de Projetos Estratégicos | Equipe responsável pela gestão e análise das propostas | Todas as propostas recebidas, TAPs, documentos, pendências e portfólio | Confere o preenchimento, solicita ajustes, realiza análises técnicas e estratégicas, atualiza o portfólio e acompanha a captação | Registrar aprovação de competência exclusiva de outra instância ou alterar decisões já formalizadas sem justificativa | Triagem, pendências, parecer e atualização do portfólio |
| Gestor / Autoridade aprovadora | Gestor ou instância com competência para aprovar projetos | Propostas analisadas, pareceres, prioridades e informações necessárias à decisão | Aprova, rejeita ou solicita readequações conforme sua competência | Alterar documentos ou pareceres técnicos sem manter o histórico das modificações | Decisão, data e justificativa |
| Responsável pela captação de recursos | Servidor ou equipe responsável por identificar fontes de financiamento | Projetos aprovados e priorizados, informações orçamentárias e oportunidades de captação | Identifica fontes de recursos, prepara submissões e acompanha os resultados | Submeter propostas sem os requisitos exigidos ou alterar informações validadas sem registro | Fontes, submissões e resultados |
| Administrador do sistema | Responsável pela configuração e manutenção da solução | Cadastros, perfis de acesso, parâmetros e registros técnicos | Gerencia usuários, permissões, formulários e regras de validação | Aprovar projetos apenas por possuir acesso administrativo, sem competência formal | Mudanças de configuração |

**Observações sobre os papéis:** O acesso ao sistema deve ser definido conforme as atribuições de cada perfil, garantindo que o demandante consiga cadastrar e acompanhar suas propostas, a equipe responsável possa analisar e manter atualizado o Portfólio de Projetos Estratégicos e as autoridades competentes formalizem as decisões de aprovação. O sistema deve manter histórico das alterações, documentos, pendências e decisões, assegurando rastreabilidade, segurança das informações e segregação de responsabilidades.

## 4. Dados (entidades e colunas; tudo SINTÉTICO)

| Entidade | O que representa | Colunas | Chave | Volume | Origem | Sintético |
|---|---|---|---|---|---|---|
| Proposta | Um TAP enviado | id: texto, titulo: texto, unidade: texto, responsavel: texto, contato: texto, objetivo: texto, justificativa: texto, objetivo_estrategico: texto, valor_estimado: número, prazo_meses: inteiro, status: texto, enviado_em: data | id | A medir | Demandante | Sim |
| Anexo | Documento da proposta | id: texto, proposta_id: texto, tipo: texto, nome: texto, conteudo: binário | id | Vários por proposta | Demandante | Sim |
| Pendencia | Devolução para ajuste | id: texto, proposta_id: texto, motivo: texto, aberta_em: data, resolvida_em: data | id | A medir | Equipe | Sim |
| Decisao | Parecer e aprovação | id: texto, proposta_id: texto, tipo: texto (parecer, aprovação, rejeição, readequação), texto: texto, autor: texto, data: data | id | Poucas por proposta | Equipe e autoridade | Sim |
| ItemPortfolio | Projeto no portfólio | proposta_id: texto, prioridade: inteiro, justificativa_prioridade: texto, fonte_recurso: texto, situacao_captacao: texto | proposta_id | Projetos aprovados | Equipe | Sim |

**O que precisa ser coletado:** Se ainda não houver controle consolidado, registrar durante pelo menos quatro semanas: data do primeiro recebimento, data em que a documentação fica completa, número de devoluções, motivo de cada pendência, data da conclusão da análise e status final.
**Quem libera o acesso:** A definir com a chefia e os responsáveis pelos sistemas/arquivos. Registrar responsável e prazo após confirmação institucional.

### Fontes de dados do processo real

| Fonte | Tipo | Onde | Existe | Uma linha é | Volume | Campos de data | Atualiza | LGPD |
|---|---|---|---|---|---|---|---|---|
| Modelo vigente do TAP | Documento em papel | Equipe de projetos | Sim | Um modelo | 1 | Não se aplica | Quando revisado | Não |
| Portfólio de Projetos Estratégicos | Planilha local | Equipe de projetos | Sim | Um projeto | A levantar | Datas de aprovação, se houver | Manual | Não |
| Registro de propostas e devoluções | Não existe ainda | A criar no piloto | Não | Uma proposta | A medir | Recebimento, pendências, conclusão | A cada proposta | Duvidaso |


## 5. Regras de negócio (RN01, RN02...)

| ID | Regra | Quando se aplica | Exceção | Quem valida | Tipo |
|---|---|---|---|---|---|
| RN01 | Campos obrigatórios do TAP preenchidos (título, unidade, responsável, objetivo, justificativa, objetivo estratégico, valor e prazo) | Antes de gerar o pacote | Nenhuma | Sistema | Validação |
| RN02 | Justificativa e objetivo com tamanho mínimo (proposta: 200 e 100 caracteres) | Antes de gerar o pacote | Nenhuma | Sistema | Validação |
| RN03 | Checklist de anexos: cada documento obrigatório anexado ou justificado | Antes de gerar o pacote | Justificativa aceita pela equipe | Sistema e equipe | Validação |
| RN04 | Anexos até 10 MB cada, em PDF, planilha ou imagem | Ao anexar | Nenhuma | Sistema | Validação |
| RN05 | Pendência sempre com motivo; a proposta volta ao demandante | Na triagem | Nenhuma | Equipe | Negócio |
| RN06 | Proposta só segue para análise com o checklist completo | Na triagem | Nenhuma | Equipe | Negócio |
| RN07 | O app não aprova nem rejeita: registra a decisão da instância competente, com autor e data | Na decisão | Nenhuma | Autoridade | Negócio |
| RN08 | Prioridade só é registrada com justificativa e critério aprovado pela governança | No portfólio | Nenhuma | Equipe | Negócio |


## 6. Telas (#/painel, #/lista...)

| Rota | Tela | Objetivo | Quem usa | Dados | Ação | Regra | Tipo | Verificável como | MVP |
|---|---|---|---|---|---|---|---|---|---|
| #/tap/novo | TAP guiado | Cadastrar a proposta | Demandante | Campos do TAP e anexos | Gerar o pacote | RN01 a RN04 | Tela | TAP incompleto não gera pacote | Sim |
| #/minhas | Minhas propostas | Acompanhar e ajustar | Demandante | Propostas, status e pendências | Abrir e corrigir | RN05 | Tela | Proposta devolvida mostra as pendências | Sim |
| #/triagem | Triagem | Conferir as propostas recebidas | Equipe | Pacotes importados, checklist | Registrar pendência ou aceitar | RN05 e RN06 | Tela | Pendência registrada com motivo | Sim |
| #/proposta/:id | Proposta | Ver tudo de uma proposta | Equipe e autoridade | TAP, anexos, pendências, parecer, decisão | Registrar parecer e decisão | RN07 | Tela | Histórico completo | Sim |
| #/portfolio | Portfólio | Manter o portfólio | Equipe | Projetos aprovados, prioridade, captação | Filtrar e exportar Excel | RN08 | Relatório | Exporta o portfólio em .xlsx | Sim |
| #/indicadores | Indicadores | Medir o piloto | Equipe | TAPs completos no 1º envio, devoluções, tempo de triagem | Consultar |  | Relatório | Bate com a contagem manual | Sim |


## 7. KPIs (nome = fórmula em uma linha)

| KPI | Pergunta | Fórmula | Fonte | Linha de base | Valor esperado | Como medir |
|---|---|---|---|---|---|---|
| TAPs completos no primeiro envio | Quantas propostas chegam completas? | Propostas sem pendência na triagem ÷ propostas recebidas × 100 | Triagem | A medir (4 semanas) | Acima de 70% (hipótese) | Registrar cada proposta recebida |
| Devoluções por proposta | Quantas vezes a proposta volta? | Pendências ÷ propostas | Pendências | A medir | Metade da linha de base | Contar as devoluções |
| Tempo até a documentação completa | Quanto tempo leva a triagem documental? | Documentação completa em − recebido em | Propostas | A medir | Redução no piloto | Datas de cada proposta |

**Período da linha de base:** Quatro semanas de registro manual antes do piloto (proposta da aluna): data do recebimento, data da documentação completa, devoluções e motivos.
**Campos de data e tempo que existem:** Hoje não há registro. No app: enviado_em, recebido_em, cada pendência (aberta e resolvida), documentação completa em, análise concluída em, decisão em.

## 8. Stack: HTML único (CSS/JS inline), dados em JSON embutido, GitHub Pages.

**Stack escolhida:** HTML único (CSS/JS inline), dados em JSON embutido, GitHub Pages
**Detalhe da stack:** Um único index.html com três perfis. O demandante preenche o TAP guiado (campos obrigatórios, checklist de anexos) e gera um pacote .json com os anexos; envia pelo canal oficial (SEI ou e-mail). A equipe importa o pacote, faz a triagem, registra pendências e mantém o portfólio no IndexedDB, com exportação para Excel. Sem servidor.
**Hospedagem:** Para o MVP: arquivo HTML único, aberto no navegador da equipe e do demandante, sem servidor e sem dados em hospedagem pública. A plataforma institucional definitiva é decidida com a TI (como a aluna pediu).
**Custo e licenças:** MVP sem custo (arquivo HTML e bibliotecas abertas). O custo da plataforma institucional é levantado com a TI depois do piloto.
**Contas e domínio:** No MVP, nenhuma conta: o arquivo circula pelo canal oficial. A publicação ou integração institucional depende da avaliação da TI (segurança, acesso, anexos, auditoria).

| Opção | Tipo | Onde roda | Custo | Quem mantém | Acesso | Banco de dados | Escala | Limitação |
|---|---|---|---|---|---|---|---|---|
| Arquivo HTML único | Arquivo local | Navegador do computador da unidade | Zero | Equipe do projeto | Quem recebe o arquivo | IndexedDB do navegador | Uma cópia por setor; consolidação por arquivo .json | Os dados ficam no computador; backup semanal |
| Plataforma institucional | Servidor interno | Infraestrutura da POLITEC | A levantar com a TI | TI | Usuários autorizados | A definir | Média | Depende da avaliação da TI |


## 9. Restrições e LGPD

**Restrições:** O formulário deve respeitar o modelo e os documentos oficiais aprovados pela instituição, as competências das unidades e autoridades, as regras de acesso e a disponibilidade da infraestrutura tecnológica. Requisitos específicos ainda precisam ser confirmados com as áreas competentes.
**Dados pessoais tratados:** nome institucional, unidade, contato e identificação do responsável, somente na medida necessária ao processo.
**Base legal:** validar com a área jurídica
**Retenção:** encarregado de dados
**Acesso e registro:** O demandante vê só as próprias propostas (o pacote dele); a equipe tem a base completa; a autoridade recebe o relatório das propostas analisadas.
**Requisitos marcados:** Acessibilidade, Funcionar offline, Impressão em formato oficial, LGPD e dado pessoal, Segurança e controle de acesso, Trilha de auditoria

---

# Anexo A — AS-IS (o fluxo de hoje)

**Início:** Recebimento de uma proposta de projeto encaminhada pelo servidor ou pela unidade demandante.
**Fim:** Captação de recursos concluída e execução do projeto liberada, ou necessidade de readequação da proposta para nova oportunidade de financiamento.
**Entradas:** Formulário TAP, descrição dos objetivos e justificativa, vínculo com os objetivos estratégicos da SESP/POLITEC, documentos obrigatórios, pesquisa de preços e demais informações necessárias à análise técnica e à captação de recursos.
**Saídas:** Projeto analisado e validado, TAP e documentação regularizados, projeto aprovado técnica e estrategicamente, Portfólio de Projetos Estratégicos atualizado e priorizado, justificativas de priorização registradas e proposta submetida à captação de recursos, quando aplicável.
**Volume:** Não mensurada atualmente.
**Duração:** Não mensurada atualmente.
**Frequência:** Por demanda
| Etapa | Quem faz | O que entra | Ação | O que sai | Sistema | Regra | Onde espera | Tempo (h) | Automatizável |
|---|---|---|---|---|---|---|---|---|---|
| Recebimento da demanda | Servidor / unidade demandante | Ideia de projeto | Encaminha a proposta de projeto | Proposta em formato livre | E-mail ou SEI |  | Recebimento de propostas em formatos diferentes | Não mensurado | Sim, com regra clara |
| Preenchimento do TAP | Servidor / unidade demandante | Modelo do TAP | Preenche o formulário com informações do projeto, objetivos e alinhamento estratégico | TAP preenchido | Documento de texto |  | Dificuldade de compreensão e preenchimento do modelo | Não mensurado | Sim, com apoio humano |
| Anexação de documentos | Servidor / unidade demandante | TAP | Anexa documentos obrigatórios e pesquisa de preços | Anexos | E-mail ou SEI |  | Documentos ausentes ou incompletos | Não mensurado | Sim, com regra clara |
| Triagem documental | Equipe responsável | TAP e anexos | Confere o preenchimento e a documentação recebida | Lista de pendências | Planilha da equipe |  | Conferência manual e identificação tardia de pendências | Não mensurado | Sim, com regra clara |
| Solicitação de ajustes | Equipe responsável e demandante | Pendências | Solicita correções e complementações no TAP e nos documentos | TAP corrigido | E-mail |  | Retorno da proposta ao demandante e retrabalho | Não mensurado | Sim, com apoio humano |
| Análise técnica e estratégica | Equipe responsável | TAP completo | Verifica requisitos, alinhamento estratégico e viabilidade técnica | Parecer técnico | Documento |  | Informações inconsistentes podem atrasar a análise | Não mensurado | Sim, com apoio humano |
| Aprovação e inclusão no portfólio | Instância responsável / equipe de projetos | Parecer | Formaliza a aprovação e registra o projeto no Portfólio de Projetos Estratégicos | Decisão e registro no portfólio | Planilha do portfólio |  | Necessidade de manter as informações atualizadas | Não mensurado | Sim, com regra clara |
| Priorização dos projetos | Equipe responsável / governança | Portfólio | Avalia critérios, classifica os projetos e registra justificativas | Prioridades justificadas | Planilha do portfólio |  | Consolidação e atualização das informações | Não mensurado | Sim, com regra clara |
| Mapeamento e submissão para captação | Equipe responsável | Projeto priorizado | Identifica fontes financeiras e submete propostas | Proposta submetida | Sistema do financiador |  | Dependência de editais e oportunidades disponíveis | Não mensurado | Sim, com apoio humano |
| Avaliação da captação e readequação | Equipe responsável / financiador | Resultado da captação | Verifica a aprovação dos recursos e readequa o plano quando necessário | Projeto financiado ou readequado | E-mail |  | Dependência do retorno do financiador e de novas oportunidades | Não mensurado | Sim, com apoio humano |

**Decisões e aprovações:** A proposta é avaliada quanto ao preenchimento do TAP, à documentação obrigatória, ao alinhamento com os objetivos estratégicos e à viabilidade técnica. Caso existam pendências ou inconsistências, retorna ao demandante para ajustes e complementações; se estiver adequada, segue para análise técnica e validação. Após a aprovação, o projeto é incluído no Portfólio de Projetos Estratégicos e encaminhado para priorização e captação de recursos.
**Exceções:** Propostas com TAP preenchido fora do padrão, informações incompletas ou documentos pendentes retornam ao demandante para regularização, podendo gerar retrabalho e atrasos. Projetos sem alinhamento estratégico ou sem viabilidade técnica precisam ser readequados ou não prosseguem para aprovação. Caso não haja aprovação da captação de recursos, o plano pode ser ajustado para nova oportunidade de financiamento.
**Já digitalizado:** O recebimento das propostas e o encaminhamento de documentos podem ocorrer por meios digitais, porém o preenchimento do TAP, a conferência das informações, a verificação documental e o controle das pendências ainda dependem de atividades manuais. A atualização e o acompanhamento do Portfólio de Projetos Estratégicos também exigem intervenção da equipe, evidenciando oportunidades de padronização, validação automática e integração das informações.

# Anexo B — TO-BE (o fluxo depois da mudança)

**Visão do futuro:** Quando o fluxo digital estiver implantado, o demandante deixará de encaminhar propostas em formatos variados e passará a preencher um TAP padronizado, orientado e validado, enquanto a equipe receberá propostas mais completas e poderá concentrar seu trabalho na análise técnica e estratégica.
**Mudança principal:** Implantar um formulário único e guiado para o TAP, com campos obrigatórios, orientações de preenchimento, checklist documental e sinalização automática de pendências antes do envio.
**O que fica igual:** A equipe continuará realizando a análise de alinhamento estratégico, a avaliação técnica e de viabilidade. As aprovações e a priorização continuarão sob responsabilidade das instâncias competentes.
**O que não pode mudar:** As competências institucionais, os critérios e documentos oficiais exigidos, as responsabilidades decisórias e as regras de governança. A automação não deve aprovar ou rejeitar projetos de forma autônoma.
| Etapa | O que muda | Quem executa | Benefício | Esforço |
|---|---|---|---|---|
| Preencher o TAP guiado | Formulário único com instruções, campos obrigatórios e checklist | A pessoa assistida pela máquina | TAP completo no primeiro envio | Médio |
| Conferir antes do envio | O app aponta campos e anexos faltando antes de gerar o pacote | A máquina (automação) | Menos devolução | Baixo |
| Triagem | A equipe importa o pacote e confere pelo checklist, registrando pendências | A pessoa assistida pela máquina | Pendência registrada com motivo e data | Baixo |
| Análise técnica e estratégica | Sem mudança; o app guarda o parecer | A pessoa, sem mudança | Histórico em um só lugar | Baixo |
| Portfólio | Aprovados entram no portfólio com status e exportação para Excel | A pessoa assistida pela máquina | Portfólio atualizado | Médio |

**Piloto do TO-BE:** Realizar piloto com um conjunto definido de propostas por 60 a 90 dias (prazo a validar), comparando com o processo anterior: proporção de TAPs completos no primeiro envio, número médio de devoluções e tempo entre recebimento e documentação completa.

# Anexo C — Pesquisa, riscos e plano

**Hipótese de campo:** A maior parte do retrabalho ocorre antes da análise técnica, porque o TAP chega fora do padrão, incompleto ou sem todos os documentos necessários; um formulário guiado com validações objetivas tende a aumentar a completude no primeiro envio e reduzir as devoluções.
| Referência | Tipo | Fonte ou link | Ano | Dado que extrai | Como usar na defesa | Link conferido |
|---|---|---|---|---|---|---|
| Modelo vigente do TAP da POLITEC | Documento interno | Equipe de projetos | A confirmar | Campos e instruções | Base do formulário guiado | Não |
| PMBOK, Termo de Abertura do Projeto | Relatório | Project Management Institute | 2021 | Conteúdo mínimo de um termo de abertura | Conferir campos obrigatórios | Não |

**Lacunas:** Fontes internas prioritárias: modelo vigente do TAP, checklist oficial de documentos, normas institucionais de aprovação e priorização, registros do portfólio e histórico de propostas devolvidas. Inserir título, unidade responsável, versão/data e link ou localização documental após conferência. Lacunas: volume de propostas, tempo de triagem, quantidade de devoluções, critérios oficiais de priorização e requisitos de hospedagem ainda precisam ser levantados/confirmados.
| Marco | Data | Responsável | Depende de | Situação |
|---|---|---|---|---|
| Modelo do TAP e checklist validados | Semana 1 | Danielle | Área responsável | Planejado |
| TAP guiado e pacote | Semana 3 | Danielle | Modelo validado | Planejado |
| Triagem e pendências | Semana 5 | Danielle | TAP guiado | Planejado |
| Portfólio e indicadores | Semana 7 | Danielle | Triagem | Planejado |
| Piloto de 60 a 90 dias | Semana 9 | Danielle e equipe | Aceite | Planejado |

| Risco | Probabilidade | Impacto | Mitigação |
|---|---|---|---|
| Formulário não reflete os requisitos institucionais | Média | Alto | Validar o modelo e o checklist com a área competente e versionar (risco da aluna) |
| Formulário complexo demais | Média | Médio | Testar com demandantes e cortar campos não usados |
| Pacote com anexos grande demais para o e-mail | Média | Médio | Limite por anexo e envio pelo SEI |

**Apoio necessário:** Apoio da chefia e da área responsável para validar o TAP, os campos obrigatórios, os documentos exigidos e os critérios de priorização; apoio da TI para definir plataforma, segurança, acesso e manutenção; participação de servidores demandantes para testar a clareza do formulário.
**Aprendizado necessário:** Mapeamento e melhoria de processos; desenho de formulários; definição de regras de validação; indicadores de processo e medição de linha de base; requisitos de segurança e proteção de dados; noções da plataforma escolhida.

# Anexo D — A defesa

**Frase de defesa:** Se aumentarmos a proporção de TAPs completos no primeiro envio e reduzirmos as devoluções para ajuste, a equipe poderá dedicar menos tempo à regularização documental e mais tempo à análise técnica, à gestão do portfólio e à captação de recursos.
**Provas:** Quantidade de propostas recebidas e percentual de TAPs completos no primeiro envio.

Número médio de devoluções e principais motivos de pendência.

Tempo entre o recebimento da proposta e a conclusão da triagem documental.
**Piloto:** Executar um piloto com unidades demandantes selecionadas, comparar os indicadores antes e depois da implantação e registrar os resultados por um período previamente definido, preferencialmente de 60 a 90 dias, conforme volume de propostas e autorização institucional.
**Maior risco:** O maior risco é padronizar o formulário sem refletir todos os requisitos institucionais ou tornar o preenchimento excessivamente complexo. Mitigação: validar o modelo e o checklist com a área competente, testar com usuários, manter controle de versões e revisar as regras após o piloto.

# Anexo E — Documentos enviados

**Descrição dos documentos:** Nenhum documento enviado.
**O que ainda falta:** Modelo vigente do TAP; lista oficial de documentos obrigatórios; critérios de priorização aprovados pela governança; histórico de propostas devolvidas.
