# PROJETO.md — Fluxo elaboração de Registro de não conformidade

**Aluno ou equipe:** Sabrina Ellen
**Unidade:** CQUAL
**Contato:** sabrinasilva@politec.mt.gov.br
**Projeto:** Fluxo elaboração de Registro de não conformidade
**Tipo de projeto:** Formulário ou modelo de coleta
**Data:** 2026-10-27
**Resumo:** Resumo do fluxo de emissão e acompanhamento de RNCs — POLITEC/MT

O processo de Registro de Não Conformidade (RNC) tem como objetivo registrar, tratar e acompanhar ocorrências que apresentem divergências em relação aos requisitos e procedimentos institucionais, promovendo a melhoria contínua dos processos da POLITEC/MT.

1\. Abertura da RNC: o setor relator registra a ocorrência por meio de formulário eletrônico acessado via QR Code. As informações são integradas automaticamente à planilha de controle e ao Trello, com geração do documento em PDF.

2\. Análise do registro: a CQUAL analisa as informações recebidas. Caso a RNC não seja aprovada ou necessite de complementação, o setor relator será comunicado para as providências necessárias.

3\. Notificação do setor responsável: após a aprovação, o setor notificado recebe a comunicação formal e as orientações para elaboração do plano de ação.

4\. Elaboração e execução do plano de ação: o setor notificado deverá preencher o modelo institucional e encaminhá-lo no prazo de até 30 dias, tendo elaborado o plano e iniciado a execução das ações nesse período. A conclusão integral das ações não é obrigatória dentro desse prazo. Caso necessário, poderá ser solicitada prorrogação mediante justificativa.

5\. Análise e encaminhamentos: o plano de ação é submetido à análise e aprovação, com posterior encaminhamento às áreas responsáveis pelo tratamento ou apoio, conforme a necessidade identificada.

6\. Avaliação dos resultados: o setor relator avalia os resultados das ações implementadas, contribuindo para a verificação de sua efetividade e para a prevenção de recorrências.

7\. Acompanhamento e encerramento: a CQUAL auxilia os setores envolvidos, monitora o andamento das RNCs e acompanha o cumprimento das etapas previstas até a conclusão do processo.

8\. Melhoria contínua: os dados das RNCs são analisados para identificar recorrências, oportunidades de melhoria e necessidades de capacitação, subsidiando o planejamento de ações educativas e preventivas.

Responsabilidades: o setor relator registra a ocorrência e avalia os resultados; o setor notificado elabora e executa o plano de ação; e a CQUAL atua no apoio, na orientação e no monitoramento do processo, promovendo a participação e a corresponsabilidade dos setores envolvidos.

## 1. Problema (a dor)

**Problema:** Muita responsabilidade para o setor de Coordenadoria de Qualidade, todas as demandas voltam para o setor.
**Impacto:** Embora o fluxo de emissão e acompanhamento das RNCs seja automatizado, a condução do processo ainda está concentrada na Coordenadoria da Qualidade (CQUAL), que atua nas análises, nos encaminhamentos e no monitoramento das etapas.

Essa centralização gera dependência da CQUAL para o andamento dos registros, aumenta a demanda de acompanhamento das pendências e pode dificultar a agilidade no tratamento das não conformidades. Além disso, a participação dos setores envolvidos no acompanhamento das próprias responsabilidades pode ser ampliada.

Dessa forma, identifica-se a oportunidade de fortalecer a corresponsabilidade dos setores relatores e notificados, mantendo a CQUAL como unidade de apoio, orientação e monitoramento. Espera-se, com isso, otimizar o fluxo, dar maior autonomia aos setores e utilizar os dados das RNCs de forma estratégica para identificar recorrências, direcionar capacitações e promover a melhoria contínua dos processos institucionais.
**Quem sofre:** Equipe interna
**Como é feito hoje:** O processo de emissão e acompanhamento das Não Conformidades (RNCs) é realizado por meio de um fluxo automatizado, integrado ao Google Forms, Google Sheets, Trello e Autocrat.

O setor relator registra a ocorrência por meio de formulário eletrônico acessado via QR Code. Após o envio, as informações são integradas à planilha de controle e ao Trello, com geração automática do documento em PDF. assim é criada o FOR 1

A Coordenadoria da Qualidade (CQUAL) analisa o registro e, após sua aprovação, dá prosseguimento ao fluxo de notificação do setor responsável pelo tratamento. 

O setor notificado deve elaborar e encaminhar o plano de ação preenchido no modelo institucional, no prazo de até 30 dias, tendo iniciado a execução das ações propostas dentro desse período. Quando necessário, pode solicitar prorrogação mediante justificativa. enviado o FOR 2

Após a análise e aprovação do plano, são realizados os encaminhamentos pertinentes para tratamento ou apoio. Posteriormente, 

o setor relator avalia os resultados das ações implementadas FOR 3, enquanto a CQUAL auxilia os envolvidos e monitora o andamento do processo até sua conclusão.

As informações registradas também são utilizadas para identificar recorrências, oportunidades de melhoria e necessidades de capacitação, subsidiando ações preventivas e o aperfeiçoamento contínuo dos processos institucionais.
**Evidências:** Planilha ou controle local
**Detalhe da evidência:** Planilha do forms 
**O que não pode ser automatizado:** Nada.

## 2. Objetivo do MVP (o que faz e o que NÃO faz)

**Objetivo do MVP:** Mostrar onde estão as RNCs, quem está com cada uma e quais setores e tipos de não conformidade se repetem, sem a CQUAL precisar cobrar cada etapa.
**O que o MVP não faz:** Não substitui o Sigadoc, que continua sendo o meio oficial e auditável. Não envia notificação oficial. Não identifica o servidor que causou a não conformidade, só o setor.
**Entregável do projeto:** App em um único HTML com a lista de RNCs por setor, os prazos de cada etapa e o painel de indicadores (setores com mais RNCs, recorrências, prazos vencidos), a partir da planilha que o Forms já alimenta.
**Dentro do escopo:** Importar a planilha do Forms; mostrar a cada setor as RNCs em que ele é relator ou notificado; prazos (5 dias para complemento, 30 dias para o plano); painel de indicadores e recorrência; exportar CSV.
**Fora do escopo:** Integração com o Sigadoc; envio automático de e-mail; avaliação de responsabilidade individual; encaminhamento à corregedoria (continua manual).
**Plataforma alvo:** Site web (abre no navegador)
**Primeira tela:** Tela das métricas 
**Simulado no MVP:** As RNCs do teste são anonimizadas (só setores). A notificação ao setor continua pelo Sigadoc; o app só mostra a pendência.
**Critério de aceite:** Com as 20 RNCs do primeiro mês (anonimizadas), o painel mostra os 3 setores e as 3 categorias com mais RNCs, os prazos vencidos e a etapa de cada RNC, e cada setor vê só as suas.
**Dados de exemplo:** Número de não conformidade atualmente o projeto piloto esta sendo feito apenas dentro de uma diretoria porém a nomenclatura sera : DIRETORIA/ANO-NÚMERO SEQUENCIAL
**O que já existe pronto e pode ser reaproveitado:** O processo de emissão e acompanhamento das Não Conformidades (RNCs) é realizado por meio de um fluxo automatizado, integrado ao Google Forms, Google Sheets, Trello e Autocrat.

O setor relator registra a ocorrência por meio de formulário eletrônico acessado via QR Code. Após o envio, as informações são integradas à planilha de controle e ao Trello, com geração automática do documento em PDF. assim é criada o FOR 1

A Coordenadoria da Qualidade (CQUAL) analisa o registro e, após sua aprovação, dá prosseguimento ao fluxo de notificação do setor responsável pelo tratamento. 

O setor notificado deve elaborar e encaminhar o plano de ação preenchido no modelo institucional, no prazo de até 30 dias, tendo iniciado a execução das ações propostas dentro desse período. Quando necessário, pode solicitar prorrogação mediante justificativa. enviado o FOR 2

Após a análise e aprovação do plano, são realizados os encaminhamentos pertinentes para tratamento ou apoio. Posteriormente, 

o setor relator avalia os resultados das ações implementadas FOR 3, enquanto a CQUAL auxilia os envolvidos e monitora o andamento do processo até sua conclusão.

As informações registradas também são utilizadas para identificar recorrências, oportunidades de melhoria e necessidades de capacitação, subsidiando ações preventivas e o aperfeiçoamento contínuo dos processos institucionais.
**Dependências:** A planilha de respostas do Forms (exportada em CSV) e a definição, pela CQUAL, das categorias de não conformidade.

## 3. Usuários e papéis

| Papel | Quem é | O que enxerga | O que faz | O que não pode fazer | Registro |
|---|---|---|---|---|---|
| CQUAL | Responsável geral | Todas as informações | Monitora e audita | Perder prazos | Aprovações e encaminhamentos |
| Setor relator | Identificador  | Não conformidade e plano de ação | Relata e avalia resultado | Deixar de avaliar  | Problema enfrentado e avaliçaõ do resultado |
| Setor Notificado | Causador raiz | Relato (sem identificar o servidor e sim o setor) | Analisa a não conformidade e planeja melhorias para diminuir os registros de não conformidade | Não executar as melhorias  | Plano de ação e avaliação de melhorias |

**Observações sobre os papéis:** Sigadoc cada um possui seu perfil. 

## 4. Dados (entidades e colunas; tudo SINTÉTICO)

| Entidade | O que representa | Colunas | Chave | Volume | Origem | Sintético |
|---|---|---|---|---|---|---|
| RNC | Um registro de não conformidade | numero: texto (DIRETORIA/ANO-SEQ), aberta_em: data, setor_relator: texto, setor_notificado: texto, categoria: texto, gravidade: texto, descricao: texto, etapa: texto, situacao: texto | numero | 20 por mês no piloto | Planilha do Forms | Parcialmente |
| Etapa | Passagem da RNC por uma etapa | id: texto, rnc: texto, etapa: texto (validação, plano, avaliação, encerramento), inicio: data, fim: data, prazo: data | id | Até 5 por RNC | CQUAL | Sim |
| Plano | Plano de ação do setor notificado (FOR 2) | id: texto, rnc: texto, causa: texto, acoes: texto, enviado_em: data, prorrogado_ate: data | id | 1 por RNC | Setor notificado | Sim |
| Avaliacao | Avaliação do resultado (FOR 3) | id: texto, rnc: texto, eficaz: lógico, observacao: texto, avaliado_em: data | id | 1 por RNC | Setor relator | Sim |

**O que precisa ser coletado:** Nome de quem fez a não conformidade e sim apenas setor (isso ja esta sendo alterado)
**Quem libera o acesso:** CQUAL

### Fontes de dados do processo real

| Fonte | Tipo | Onde | Existe | Uma linha é | Volume | Campos de data | Atualiza | LGPD |
|---|---|---|---|---|---|---|---|---|
| Planilha | Planilha local | Planilhas google | Sim | perguntas no forms | atualmente 20 linhas preenchidas  | Data de entrada, data de envio, tempo anotado | Automática conforme é preenchido o forms  | Sim |


## 5. Regras de negócio (RN01, RN02...)

| ID | Regra | Quando se aplica | Exceção | Quem valida | Tipo |
|---|---|---|---|---|---|
| RN01 | Numeração DIRETORIA/ANO-SEQUENCIAL, única | Ao importar | Nenhuma | Sistema | Validação |
| RN02 | Sem resposta ao pedido de complemento em 5 dias, a RNC é anulada | Validação pela CQUAL | Nenhuma | CQUAL | Negócio |
| RN03 | O setor notificado tem 30 dias para enviar o plano (FOR 2), com prorrogação justificada | Após a validação | Prorrogação aprovada pela CQUAL | CQUAL | Negócio |
| RN04 | Ocorrência grave é encaminhada à corregedoria | Na validação | Nenhuma | CQUAL | Negócio |
| RN05 | Recorrência: mesmo setor notificado e mesma categoria em 90 dias | No painel | Nenhuma | Sistema | Cálculo |
| RN06 | Cada setor vê só as RNCs em que é relator ou notificado | Na cópia do setor | CQUAL vê todas | Sistema | Acesso |
| RN07 | Não registrar nome de servidor, só o setor | Em todos os registros | Nenhuma | Sistema | LGPD |


## 6. Telas (#/painel, #/lista...)

| Rota | Tela | Objetivo | Quem usa | Dados | Ação | Regra | Tipo | Verificável como | MVP |
|---|---|---|---|---|---|---|---|---|---|
| #/painel | Painel de indicadores | Informar e dar transparência | Todos | RNCs por setor, categoria, etapa e prazo | Filtrar | RN05 | Relatório | Painel bate com a contagem na planilha | Sim |
| #/minhas | Minhas RNCs | Ver as RNCs do setor | Setor relator e notificado | RNCs em que o setor aparece | Abrir a RNC | RN06 | Tela | O setor vê só as suas | Sim |
| #/rnc/:id | RNC | Acompanhar uma RNC | CQUAL e setores | Etapas, prazos, FOR 1, 2 e 3 | Registrar etapa | RN02 e RN03 | Tela | Etapa nova com data | Sim |
| #/importar | Importar planilha | Trazer as respostas do Forms | CQUAL | CSV da planilha | Importar | RN01 | Ação | 20 RNCs importadas sem duplicar | Sim |
| #/exportar | Arquivo do setor | Mandar a cada setor as suas RNCs | CQUAL | RNCs por setor | Exportar | RN06 | Ação | Arquivo do setor só tem as RNCs dele | Sim |


## 7. KPIs (nome = fórmula em uma linha)

| KPI | Pergunta | Fórmula | Fonte | Linha de base | Valor esperado | Como medir |
|---|---|---|---|---|---|---|
| Tempo até o plano de ação | Quanto tempo o setor notificado leva para responder? | Envio do FOR 2 − validação da RNC | Etapas | A medir no piloto | Até 30 dias em 90% das RNCs | Datas da planilha do Forms |
| RNCs que voltam para a CQUAL | Quantas vezes a CQUAL precisa cobrar ou refazer? | Cobranças da CQUAL ÷ RNCs abertas | Registro de etapas | A medir no piloto | Metade da linha de base | Anotar cada cobrança no mês |
| Recorrência | Quais setores e categorias se repetem? | RNCs com recorrência (RN05) ÷ total | RNCs | A medir | Queda após capacitação | Painel |

**Período da linha de base:** As 20 RNCs do primeiro mês do piloto: tempo de cada etapa e quantas voltaram para a CQUAL.
**Campos de data e tempo que existem:** tem data e horário 

## 8. Stack: HTML único (CSS/JS inline), dados em JSON embutido, GitHub Pages.

**Stack escolhida:** HTML único (CSS/JS inline), dados em JSON embutido, GitHub Pages
**Detalhe da stack:** Um único index.html (HTML, CSS e JS embutidos). Lê o CSV exportado da planilha do Forms, guarda no IndexedDB e mostra o painel com gráficos em SVG próprio, sem internet. Cada setor recebe um arquivo com as suas RNCs.
**Hospedagem:** Arquivo HTML único, aberto no navegador da CQUAL e dos setores, e publicado no GitHub Pages sem dados.
**Custo e licenças:** Custo zero.
**Contas e domínio:** A CQUAL publica o arquivo; não há conta de banco de dados.

| Opção | Tipo | Onde roda | Custo | Quem mantém | Acesso | Banco de dados | Escala | Limitação |
|---|---|---|---|---|---|---|---|---|
| Arquivo HTML único | Arquivo local | Navegador do computador da unidade | Zero | Equipe do projeto | Quem recebe o arquivo | IndexedDB do navegador | Uma cópia por setor; consolidação por arquivo .json | Os dados ficam no computador; backup semanal |
| GitHub Pages | Estática e gratuita | github.io | Zero | Equipe do projeto | Link (o app; os dados ficam no navegador) | Não tem | Baixa | Publica só o app, nunca os dados |


## 9. Restrições e LGPD

**Restrições:** Sem integração com o Sigadoc; sem nome de servidor; dados sensíveis só na cópia da CQUAL.
**Dados pessoais tratados:** Setor relator, setor notificado, descrição da ocorrência e datas. O nome do servidor envolvido não entra.
**Base legal:** Execução de atribuição da CQUAL (gestão da qualidade e melhoria de processos), LGPD art. 7º, III; sem dado do servidor envolvido.
**Retenção:** As RNCs encerradas ficam pelo prazo da tabela de temporalidade da POLITEC; no MVP, dados anonimizados.
**Acesso e registro:** A cópia de cada setor recebe só as RNCs em que ele é relator ou notificado. A CQUAL tem a base completa.
**Requisitos marcados:** LGPD e dado pessoal, Segurança e controle de acesso, Funcionar offline

---

# Anexo A — AS-IS (o fluxo de hoje)

**Início:** Preenchimento do formulário de Registro de não conformidade
**Fim:** Finalização da RNC, encaminhamento para corregedoria ou finalização das recorrências das não conformidades 
**Entradas:** Formulário de RNC - Planilha com as respostas do FORMS
Geração autocrat - Formulário 1 (Com as respostas do formulário pelo setor relator)
Formulário 2 - Modelo preenchido pelo setor notificado 
Formulário 3- Avaliação do resultado preenchido pelo setor relator
**Saídas:** Plano de ação e evidencias de melhoria 
**Volume:** 20 no primeiro mês
**Duração:** Sem média (provavelmente longa duranção)
**Frequência:** Diário
| Etapa | Quem faz | O que entra | Ação | O que sai | Sistema | Regra | Onde espera | Tempo (h) | Automatizável |
|---|---|---|---|---|---|---|---|---|---|
| Identificação da não conformidade | Setor Relator | RNC | Preenchimento do forms | Relato da Não conformidade | FORMS |  | sem espera | 0 | Sim, com regra clara |
| Encaminhamento de validação | CQUAL | Formulário 1 | Confirmação da RNC | Formulário 1 aprovado/encmainhado | Aprovação é visualizando/lendo e aprovando tanto enviando email para o setor relator quanto aprovando no trello para maior visualização dos protocolos.  | Aprovado ou não  | Trello | 24 | Sim, com regra clara |
| Encaminha para o setor notificado | CQUAL | Formulário 1 | Encaminha a notificação e anexa um modelo de formulário com as informações | Formulário 2 com plano de ação e evidencias de melhora | Sigadoc (aberto para ideias) | período de 30 dias para responder | Trello (para acompanhamento da CQUAL) Sigadoc com prazo | 24 | Sim, com regra clara |
| Elaboração e execução  | Setor notificado | modelo de Formulário 2 | Elabora o plano de ação, executa e anexa o FOR 2 no sigadoc | Formulário 2 preenchido | Sigadoc | período de 30 dias para responder | Sigadoc | 720 | Pouco |
| Avaliação | Setor Relator | Formulário 2 | Avaliar se a execução do plano de ação foi adequado e gerou os resultados esperados | Formulário 3 | Sigadoc | Avaliação | Sigadoc | 48 | Pouco |
| Finalização/encaminhamento | CQUAL | Formulário 3 | Verifica o processo inteiro e da conclusão ou encaminha para os setores responsáveis  | Métrica dos erros e não conformidades da POLITEC | Sigadoc | Decide se vai ser finalizado ou não | Sigadoc | 48 | Sim, com apoio humano |

**Decisões e aprovações:** RNC - formulário 1 - Aprovado ou não 
Avaliação do plano de ação e seus resultados
Decide se vai ser finalizado ou não
**Exceções:** Se não houver resposta sobre informações complementares em até 5 dias a RNC é anulada.
Em casos de ocorrências graves são encaminhadas a corregedoria 
**Já digitalizado:** QR code para entrar no formulário 
Automatização do planilhas/forms para o trello (acompanhamento da CQUAL) e geração por autocrat dos formulários


# Anexo B — TO-BE (o fluxo depois da mudança)

**Visão do futuro:** Quando o RNC for gerado sera encaminhado para os setores responsáveis e cada uma fara seu papel sendo necessário avaliar apenas a entrada e saída da não conformidade.
**Mudança principal:** Cada setor vê e cumpre a sua etapa (o relator abre e avalia, o notificado responde com o plano), com prazo e alerta; a CQUAL só valida a entrada e a saída e acompanha pelo painel.
**O que fica igual:** QR code para formulário (precisa ser fácil para ter adesão)
**O que não pode mudar:** O Sigadoc continua como meio oficial; casos graves seguem para a corregedoria; o QR Code do formulário continua.
| Etapa | O que muda | Quem executa | Benefício | Esforço |
|---|---|---|---|---|
| Registrar a RNC | Continua pelo QR Code e Forms | A pessoa, sem mudança | Adesão mantida | Baixo |
| Validar a entrada | A CQUAL aprova ou devolve, com prazo de 5 dias para complemento | A pessoa assistida pela máquina | Prazo visível | Baixo |
| Responder com o plano | O setor notificado vê a RNC, o prazo de 30 dias e o alerta de vencimento | A pessoa assistida pela máquina | Menos cobrança da CQUAL | Médio |
| Avaliar o resultado | O setor relator vê o plano e registra a avaliação (FOR 3) | A pessoa assistida pela máquina | Avaliação no prazo | Baixo |
| Indicadores | Painel de setores, categorias, recorrência e prazos | A máquina (automação) | Uso estratégico das RNCs | Médio |

**Piloto do TO-BE:** Piloto de 30 dias na Diretoria de Laboratório Forense, com as RNCs do período.

# Anexo C — Pesquisa, riscos e plano

**Hipótese de campo:** A maior parte do tempo das RNCs é espera do setor notificado e cobrança feita pela CQUAL, e os mesmos setores e categorias se repetem.
| Referência | Tipo | Fonte ou link | Ano | Dado que extrai | Como usar na defesa | Link conferido |
|---|---|---|---|---|---|---|
| ABNT NBR ISO 9001:2015, item 10.2 (não conformidade e ação corretiva) | Norma ou lei | ABNT | 2015 | Tratar a não conformidade, avaliar a causa e a eficácia da ação | Fundamentar as etapas FOR 1, 2 e 3 | Não |
| ABNT NBR ISO/IEC 17025:2017, item 7.10 (trabalho não conforme) | Norma ou lei | ABNT | 2017 | Requisitos de trabalho não conforme em laboratórios | Relacionar ao piloto no Laboratório Forense | Não |

**Lacunas:** Não há medição do tempo de cada etapa nem do número de RNCs que voltam para a CQUAL.
| Marco | Data | Responsável | Depende de | Situação |
|---|---|---|---|---|
| Categorias e prazos validados | Semana 1 | Sabrina | CQUAL | Planejado |
| Importação e lista por setor | Semana 3 | Sabrina | Planilha anonimizada | Planejado |
| Painel de indicadores | Semana 5 | Sabrina | Importação | Planejado |
| Piloto de 30 dias no Laboratório Forense | Semana 7 | Sabrina e CQUAL | Aceite | Planejado |

| Risco | Probabilidade | Impacto | Mitigação |
|---|---|---|---|
| Vazamento de dados sensíveis | Média | Alto | Só setores, sem nomes; a cópia do setor recebe só as suas RNCs |
| Setores não usam o app | Média | Médio | Manter o QR Code e o Forms; o app só mostra a etapa e o prazo |
| Planilha do Forms muda de colunas | Média | Médio | Associação de colunas na importação |

**Apoio necessário:** Diretoria de Laboratório Forense (piloto) e chefias dos setores notificados.
**Aprendizado necessário:** Modelagem do projeto

# Anexo D — A defesa

**Frase de defesa:** Otimizar o fluxo de RNCs, fortalecendo a corresponsabilidade dos setores e posicionando a CQUAL como unidade de apoio, orientação e monitoramento para a melhoria contínua dos processos da POLITEC/MT.
**Provas:** Número de desistências por burocracia e falta de aceite dos setores notificados 
**Piloto:** Piloto com a diretoria de laboratório forense 30 dias 
**Maior risco:** Como é piloto pode haver mudanças durante o caminho

# Anexo E — Documentos enviados

**Descrição dos documentos:** Esta no titulo de cada um
**O que ainda falta:** Ainda falta:
faltam a visão do TO-BE e a tabela de etapas futuras
falta o escopo do MVP, o objetivo e as funcionalidades mínimas
faltam as entidades de dados e as regras de negócio
faltam duas métricas com fonte, base e hipótese
faltam a hospedagem escolhida e a justificativa
falta a hipótese de campo
