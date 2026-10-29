# PROJETO.md — Automação do Mapa de Distribuição por Credor e da Distribuição Orçamentária

**Aluno ou equipe:** Igor Henrique de Menezes Costa
**Unidade:** Setor de Licitações – POLITEC/MT
**Contato:** izgdreyar@gmail.com
**Projeto:** Automação do Mapa de Distribuição por Credor e da Distribuição Orçamentária
**Tipo de projeto:** Automação de script ou rotina
**Data:** 2026-10-29
**Resumo:** Rotina automatizada que lê os relatórios do pregoeiro e o anexo de distribuição do TR e gera o Mapa de Distribuição por credor e a tabela de distribuição orçamentária por órgão, no lugar das planilhas Excel preenchidas e conferidas manualmente.

## 1. Problema (a dor)

**Problema:** A equipe de licitações monta à mão, em várias planilhas Excel, o mapa de distribuição por órgão e por credor, redigitando os mesmos dados a cada etapa, o que causa retrabalho, erros de cálculo e atraso na distribuição da dotação orçamentária.
**Impacto:** Retrabalho e digitação duplicada em cada etapa; risco de divergência entre planilhas e entre valores estimados e homologados; demora na distribuição orçamentária. 
**Quem sofre:** Servidor da unidade, Equipe interna, Chefia
**Como é feito hoje:** 1) Cada unidade demandante preenche no Excel a distribuição de itens por órgão. 2) A equipe compõe por grupo, item, código, descrição, unidade, quantidade, valor unitário e total, e passa para uma planilha à parte de controle. 3) Aguarda os relatórios do pregoeiro e preenche empresa vencedora e valor homologado. 4) Separa os grupos homologados, fracassados e desertos. 5) Cria colunas de resultado geral e por órgão. 6) Monta tabela por empresa e por órgão participante. 7) Monta outra tabela com valor total, para conferência. 8) Monta a tabela de distribuição orçamentária por credor e órgão (processo, dotação, custeio 3 / investimento 4, CNPJ, valores, ano seguinte quando a dotação não comporta). Tudo é copiado e digitado entre planilhas.
**Evidências:** Planilha ou controle local, Relatório de sistema, Medida feita pela equipe
**Detalhe da evidência:** Descrição do fluxo atual feita pela equipe na Aula 7 (27/10/2026), com exemplos das planilhas de cada etapa (exemplos 1 a 8).
**O que não pode ser automatizado:** Não se automatiza: a assinatura e a responsabilidade legal e a conferência final dos valores continua com a equipe.

## 2. Objetivo do MVP (o que faz e o que NÃO faz)

**Objetivo do MVP:** Provar que, a partir de uma planilha de distribuição e de um relatório do pregoeiro de exemplo, é possível gerar o mapa por credor e a tabela orçamentária sem redigitação.
**O que o MVP não faz:** Não busca dados em sistema oficial; não valida a dotação; não gera documento oficial; não grava no sistema de orçamento.
**Entregável do projeto:** Protótipo (HTML único) que importa planilhas de exemplo, gera o mapa de distribuição por credor, a tabela de conferência e a distribuição orçamentária, e aponta divergências.
**Dentro do escopo:** Leitura de planilha de distribuição por órgão e de relatório do pregoeiro (exemplo); cálculo de totais por grupo, órgão e empresa; separação em homologado, fracassado e deserto; tabela de distribuição orçamentária por credor; alerta de divergência.
**Fora do escopo:** Integração direta com o sistema oficial de licitação e de orçamento; assinatura eletrônica; decisão sobre dotação. Ficam fora por dependerem de autorização.
**Plataforma alvo:** Site web (abre no navegador)
**Primeira tela:** Tela de importação dos arquivos (distribuição por órgão e relatório do pregoeiro) com resumo do que foi lido.
**Simulado no MVP:** Planilhas, relatório do pregoeiro, CNPJs e valores de dotação serão dados sintéticos de exemplo.
**Critério de aceite:** Os totais gerados batem com a planilha manual de referência (diferença zero) e as divergências propositalmente inseridas são apontadas.
**Dados de exemplo:** 3 órgãos, 6 grupos (2 com empresa, 1 fracassado, 1 deserto, 2 mistos), 4 empresas fictícias com CNPJ fictício e dotações de custeio e investimento.
**O que já existe pronto e pode ser reaproveitado:** Planilhas de exemplo 1 a 8 do documento do workflow e as fórmulas Excel já usadas pela equipe.
**Dependências:** Equipe de licitações (regras e planilhas); pregoeiro (relatórios) e; setor de orçamento (dotação).

## 3. Usuários e papéis

| Papel | Quem é | O que enxerga | O que faz | O que não pode fazer | Registro |
|---|---|---|---|---|---|
| Analista de licitações | Servidor que monta o mapa | Planilhas, relatórios e tabelas geradas | Importa arquivos, confere e exporta o mapa | Alterar valor homologado sem registro | Importação, edições e conferência |
| Unidade demandante | Órgão que pede os itens | Sua própria distribuição de itens | Envia a planilha de distribuição | Ver dados de outros órgãos | Envio e data |
| Pregoeiro | Responsável pelo preenchimento | Resultado de grupos | Fornece relatório com vencedores e valores | Alterar o mapa | Relatório fornecido |
| Analista de licitações / Orçamento | Valida a distribuição | Tabela orçamentária e divergências | Valida dotação e aprova | Alterar dados de origem | Validação e aprovação |

**Observações sobre os papéis:** Os papéis do MVP são internos; não há acesso de cidadão.

## 4. Dados (entidades e colunas; tudo SINTÉTICO)

| Entidade | O que representa | Colunas | Chave | Volume | Origem | Sintético |
|---|---|---|---|---|---|---|
| Processo | Processo licitatório | id_processo: texto, nome: texto | id_processo | 3 por teste | Exemplo sintético | Sim |
| Grupo/Item | Item licitado por grupo | grupo, item, código: texto, descrição: texto, unidade: texto, quantidade: número, valor_unitário: número | grupo+item | 30 | Planilha de exemplo | Sim |
| Distribuição por órgão | Quantidade por órgão | órgão: texto, item: texto, quantidade: número | órgão+item | 90 | Planilha de exemplo | Sim |
| Resultado do pregoeiro | Vencedor e valor homologado | grupo, situação: texto, empresa: texto, cnpj: texto, valor_homologado: número | grupo | 6 | Relatório de exemplo | Sim |
| Dotação | Dotação por órgão e tipo | órgão, tipo (3 custeio / 4 investimento), valor: número, ano: número | órgão+tipo+ano | 6 | Exemplo sintético | Sim |

**O que precisa ser coletado:** Relatórios do pregoeiro de processos anteriores, anexo de distribuição do TR, planilhas de controle e tempos de cada etapa.
**Quem libera o acesso:** Analista de licitações libera os relatórios e planilhas; setor de orçamento libera a dotação. Prazo: A DEFINIR.

### Fontes de dados do processo real

| Fonte | Tipo | Onde | Existe | Uma linha é | Volume | Campos de data | Atualiza | LGPD |
|---|---|---|---|---|---|---|---|---|
| Planilha de distribuição por órgão | Planilha local | Máquina da unidade | Sim | Um item por órgão | A medir | Por processo | Sim | Não |
| Relatório do pregoeiro | Relatório | Sistema de licitação | Sim | Um grupo | A medir | Por processo | Sim | Não |
| Anexo de distribuição do TR | Documento em papel | Processo | Sim | Um item | A medir | Por processo | Sim | Não |
| Dotação validada por órgão | Planilha local | Setor de orçamento | Sim | Uma dotação por órgão, tipo e ano | A medir | Ano | A cada processo | Não |


## 5. Regras de negócio (RN01, RN02...)

| ID | Regra | Quando se aplica | Exceção | Quem valida | Tipo |
|---|---|---|---|---|---|
| RN01 | Total do item = quantidade x valor unitário | Ao importar a planilha | Nenhuma | Analista | Cálculo |
| RN02 | Grupo sem empresa é fracassado ou deserto, conforme o relatório | Ao ler o relatório do pregoeiro | Nenhuma | Analista | Negócio |
| RN03 | Valor homologado substitui o valor estimado | Após o relatório | Grupo fracassado ou deserto | Analista | Negócio |
| RN04 | Soma por órgão deve igualar o total do grupo | Na conferência | Nenhuma; diferença vira alerta | Analista | Validação |
| RN05 | Se a dotação não suporta o valor no ano corrente, o excedente vai para o ano seguinte | Na distribuição orçamentária | Valor validado pela chefia | Analista | Cálculo |
| RN06 | Dotação do tipo 3 (custeio) ou 4 (investimento) por grupo | Na distribuição | Nenhuma | Analista/Orçamento | Negócio |
| RN07 | CNPJ deve ter 14 dígitos | Ao importar o relatório | Nenhuma | Analista | Validação |
| RN08 | O valor homologado é usado por item; se o relatório trouxer só o total do grupo, aplica-se a todos os itens o mesmo desconto (homologado ÷ estimado do grupo) | Após o relatório do pregoeiro | Equipe pode informar o valor de cada item | Analista | Cálculo |
| RN09 | Valor unitário com 2 casas; total do item = quantidade × valor unitário, arredondado a 2 casas; somas feitas em centavos | Em todos os cálculos | Nenhuma | Analista | Cálculo |
| RN10 | A dotação de cada órgão e tipo é consumida na ordem dos grupos do processo; o que não couber vai para o ano seguinte | Na distribuição orçamentária | Ordem definida pelo orçamento | Orçamento | Negócio |
| RN11 | Grupo misto (itens adjudicados a empresas diferentes) é tratado item a item | Ao ler o relatório do pregoeiro | Nenhuma | Analista | Negócio |


## 6. Telas (#/painel, #/lista...)

| Rota | Tela | Objetivo | Quem usa | Dados | Ação | Regra | Tipo | Verificável como | MVP |
|---|---|---|---|---|---|---|---|---|---|
| #/importar/:proc | Tela de importação | Carregar arquivos de origem | Analista | Arquivos lidos e linhas | Importar | Arquivo com colunas obrigatórias | Tela | Importar exemplo e ver o resumo | Sim |
| #/mapa/:proc | Mapa por grupo e órgão | Consolidar valores | Analista | Grupo, item, quantidade, valores | Gerar mapa | Total = quantidade x valor unitário | Relatório | Totais batem com a planilha manual | Sim |
| #/resultado/:proc | Situação dos grupos | Separar homologado, fracassado e deserto | Analista | Grupo e situação | Classificar | Situação vem do relatório do pregoeiro | Regra | Casos de teste classificados corretamente | Sim |
| #/conferencia/:proc | Conferência e divergências | Apontar diferenças | Analista e chefia | Estimado x homologado e totais | Conferir | Totais devem bater | Automação | Divergência inserida é apontada | Sim |
| #/orcamento/:proc | Distribuição orçamentária por credor | Distribuir por dotação | Analista e orçamento | Processo, dotação, CNPJ, valores | Gerar tabela | Se a dotação não suportar, usar ano seguinte | Documento | Tabela confere com a manual | Sim |
| #/empresas/:proc | Tabela por empresa e órgão | Ver os grupos ganhos por empresa em cada órgão | Analista | Empresa, CNPJ, grupos, valores por órgão | Gerar tabela | Só grupos homologados | Relatório | Tabela confere com o exemplo 6 | Sim |
| #/exportar/:proc | Exportação para Excel | Entregar o mapa no formato da equipe | Analista | As 8 tabelas do fluxo | Baixar .xlsx | Valores como número | Documento | Arquivo abre no Excel com 8 abas | Sim |


## 7. KPIs (nome = fórmula em uma linha)

| KPI | Pergunta | Fórmula | Fonte | Linha de base | Valor esperado | Como medir |
|---|---|---|---|---|---|---|
| Tempo de montagem do mapa | Quanto tempo leva do recebimento à tabela final? | Hora final - hora inicial | Etapas 1 a 8 do AS-IS | A MEDIR | Fração do atual (hipótese) | Cronometrar um processo |
| Divergências por processo | Quantos erros são achados na conferência? | Nº de divergências / processo | Planilha de conferência | A MEDIR | Zero ao final (hipótese) | Contar nos 3 últimos processos |
| Retrabalho de digitação | Quantas vezes o mesmo dado é redigitado? | Nº de planilhas que repetem o dado | Fluxo AS-IS | Cerca de 6 (estimativa) | 1 (hipótese) | Contar as planilhas de um processo |

**Período da linha de base:** A MEDIR: últimos 3 a 6 processos encerrados, com nº de grupos, itens e horas gastas.
**Campos de data e tempo que existem:** A verificar nos relatórios do pregoeiro (data de homologação) e nas planilhas (datas de recebimento). Sem data hoje, a espera é medida por cronômetro na semana 1.

## 8. Stack: HTML único (CSS/JS inline), dados em JSON embutido, GitHub Pages.

**Stack escolhida:** HTML único (CSS/JS inline), dados em JSON embutido, GitHub Pages
**Detalhe da stack:** HTML único com JS embutido, rodando no navegador e publicado no GitHub Pages, com dados de exemplo em JSON.
**Hospedagem:** GitHub Pages: gratuito, sem servidor e sem banco, suficiente para o protótipo com dados sintéticos.
**Custo e licenças:** Custo zero no protótipo; produção futura depende de decisão da TI.
**Contas e domínio:** O próprio aluno cria a conta no GitHub; domínio padrão github.io.

| Opção | Tipo | Onde roda | Custo | Quem mantém | Acesso | Banco de dados | Escala | Limitação |
|---|---|---|---|---|---|---|---|---|
| GitHub Pages | Estática e gratuita | Servidores do GitHub | Grátis | O aluno | Público por link | Não tem | Baixa | Sem dados sensíveis e sem banco |
| Arquivo HTML único | Arquivo local | Computador do usuário | Grátis | O aluno | Só quem recebe o arquivo | Não tem | Baixa | Difícil de atualizar |


## 9. Restrições e LGPD

**Restrições:** Não pode usar dado pessoal; depende de liberação dos relatórios; integração com sistema oficial exige TI; dotação é validada por pessoa.
**Dados pessoais tratados:** Nenhum dado pessoal de cidadão. Apenas dados de órgãos, itens, valores e empresas (razão social e CNPJ, dados de pessoa jurídica). No MVP, tudo sintético.
**Base legal:** Execução de atribuição legal de licitação e controle orçamentário (Lei 14.133/2021 e Lei nº 4.320/1964). Finalidade: distribuir e conferir a aquisição por órgão e credor.
**Retenção:** Conforme a tabela de temporalidade da unidade para processos licitatórios; no MVP, nenhum dado é guardado fora do navegador.
**Acesso e registro:** Somente servidores da licitação e do orçamento; cada importação e edição registra usuário, data e arquivo de origem.
**Requisitos marcados:** LGPD e dado pessoal, Segurança e controle de acesso, Integração com sistema oficial, Trilha de auditoria

---

# Anexo A — AS-IS (o fluxo de hoje)

**Início:** Unidades demandantes enviam a distribuição de itens por órgão (Excel)
**Fim:** Tabela de distribuição orçamentária por credor e órgão pronta para a dotação
**Entradas:** Planilhas de distribuição de itens por órgão (unidades demandantes); anexo de distribuição do TR; relatórios do pregoeiro (empresa vencedora e valor homologado); dotação orçamentária validada por órgão.
**Saídas:** Mapa de distribuição por credor; tabelas por empresa e órgão; tabela de conferência; tabela de distribuição orçamentária por credor e órgão participante (com CNPJ e valores por dotação).
**Volume:** A MEDIR: nº de processos, grupos e itens por mês
**Duração:** A MEDIR (do recebimento das planilhas à distribuição orçamentária)
**Frequência:** Por demanda
| Etapa | Quem faz | O que entra | Ação | O que sai | Sistema | Regra | Onde espera | Tempo (h) | Automatizável |
|---|---|---|---|---|---|---|---|---|---|
| Receber distribuição de itens por órgão | Unidade demandante / Licitações | Planilha Excel da unidade | Aguardar e conferir o preenchimento | Planilha recebida | Excel / e-mail | Cada item com sua unidade de medida | Espera as unidades preencherem | A medir | Sim, com apoio humano |
| Compor mapa por grupo e item | Licitações | Planilha das unidades | Compor grupo, item, código, descrição, unidade, quantidade, valor unitário e total, e valor estimado por órgão | Planilha de controle | Excel | Valores vêm da pesquisa de preço | Digitação duplicada | A medir | Sim, com regra clara |
| Preencher valores homologados | Licitações | Relatórios do pregoeiro | Digitar empresa vencedora e valor homologado | Planilha com valores homologados | Excel / sistema de licitação | Valor homologado substitui o estimado | Espera o relatório do pregoeiro | A medir | Sim, com regra clara |
| Separar homologados, fracassados e desertos | Licitações | Planilha preenchida | Separar os grupos e registrar a observação conforme o caso | Planilha separada por situação | Excel | Situação do grupo define a observação | Retrabalho de cópia | A medir | Sim, com regra clara |
| Gerar resultado geral e por órgão | Licitações | Planilha separada | Criar colunas de resultado geral e por órgão | Planilha com resultados | Excel | Soma por órgão e total geral | Cálculo manual | A medir | Sim, com regra clara |
| Montar tabela por empresa e órgão | Licitações | Planilha com resultados | Montar tabela das empresas vencedoras por órgão participante | Tabela por empresa e órgão | Excel | Grupos ganhos por empresa | Redigitação | A medir | Sim, com regra clara |
| Montar tabela de conferência | Licitações | Tabela por empresa e órgão | Criar tabela com valor total para conferir a planilha anterior | Tabela de totais conferida | Excel | Totais devem bater com a planilha base | Divergências só são vistas no fim | A medir | Sim, com apoio humano |
| Montar distribuição orçamentária por credor e órgão | Licitações / Orçamento | Tabelas e dotação validada | Montar tabela com processo, dotação por órgão e grupo (3 custeio / 4 investimento), CNPJ e valores por credor; coluna do ano seguinte se faltar dotação | Tabela de distribuição orçamentária | Excel | Dotação não suporta o valor: nova coluna para o ano seguinte | Espera a validação da dotação | A medir | Sim, com apoio humano |

**Decisões e aprovações:** Grupo teve empresa homologada, foi fracassado ou deserto (define a observação); a dotação validada suporta todo o valor no ano corrente? Se não, cria coluna para o ano seguinte; item custeio (3) ou investimento (4).
**Exceções:** Grupos fracassados e desertos (mantêm as colunas, só muda a observação); valor homologado diferente do estimado; dotação insuficiente no ano corrente.
**Já digitalizado:** Tudo em planilhas Excel; os relatórios do pregoeiro vêm do sistema de licitação; não há integração entre os arquivos.

# Anexo B — TO-BE (o fluxo depois da mudança)

**Visão do futuro:** Quando este processo existir, a equipe de licitações deixa de redigitar e conferir planilhas à mão e passa a gerar o mapa de distribuição e a tabela orçamentária automaticamente a partir dos relatórios do pregoeiro e do anexo do TR.
**Mudança principal:** Os dados são lidos uma única vez dos relatórios do pregoeiro e do anexo de distribuição do TR, e todas as tabelas (por empresa, por órgão, conferência e distribuição orçamentária) são geradas automaticamente, com rastreabilidade até o arquivo de origem.
**O que fica igual:** As unidades demandantes continuam enviando a distribuição de itens; o pregoeiro continua homologando; a validação da dotação e a decisão final continuam com pessoas.
**O que não pode mudar:** Lei de licitações, regras de dotação orçamentária (custeio 3 / investimento 4) e procedimento oficial do processo.
| Etapa | O que muda | Quem executa | Benefício | Esforço |
|---|---|---|---|---|
| Receber planilhas das unidades | Importar para a ferramenta | A pessoa assistida pela máquina | Menos digitação | Baixo |
| Importar relatório do pregoeiro | Leitura automática de empresa e valor homologado | A máquina (automação) | Fim da redigitação | Médio |
| Gerar mapa por grupo, órgão e empresa | Cálculos padronizados automáticos | A máquina (automação) | Menos erros e tempo | Médio |
| Separar homologados, fracassados e desertos | Classificação automática com observação | A máquina (automação) | Padronização | Baixo |
| Conferir divergências | Alerta antes da distribuição orçamentária | A máquina (automação) | Erros achados cedo | Médio |
| Validar dotação e distribuir | Tabela por credor e órgão gerada; ano seguinte quando faltar dotação | A pessoa assistida pela máquina | Menos retrabalho | Alto |

**Piloto do TO-BE:** Em um processo já encerrado, comparando o resultado gerado pela automação com o mapa feito manualmente, usando dados sintéticos ou sem dado pessoal.

# Anexo C — Pesquisa, riscos e plano

**Hipótese de campo:** A maior parte do tempo se perde em redigitar e conferir entre planilhas, não em decidir.
| Referência | Tipo | Fonte ou link | Ano | Dado que extrai | Como usar na defesa | Link conferido |
|---|---|---|---|---|---|---|
| Lei nº 4.320, de 17 de Março de 1964 | Norma ou lei | Planalto.gov.br | 1964 | Classificação da despesa por categoria econômica: 3 (despesas correntes) e 4 (despesas de capital) | Fundamentar a separação entre custeio (3) e investimento (4) na distribuição orçamentária | Não |
| Documento WorkFlow (Aula 7) | Documento interno | Anexo do projeto | 2026 | Descrição das 8 etapas do fluxo | Base do AS-IS | Sim |
| Lei nº 14.133/2021, art. 71 (homologação) | Norma ou lei | Planalto | 2021 | Encerrado o julgamento, a autoridade homologa o resultado | Mostrar de onde vem o valor homologado que substitui o estimado | Não |

**Lacunas:** Sem medição de tempo atual; sem levantamento de erros históricos; falta pesquisa externa sobre mapas de distribuição em outros órgãos.
| Marco | Data | Responsável | Depende de | Situação |
|---|---|---|---|---|
| Medir tempo do fluxo atual |  | Equipe | Acesso às planilhas | Planejado |
| Montar dados de exemplo |  | Aluno | Planilhas | Planejado |
| MVP funcional |  | Professor e aluno | Dados de exemplo | Planejado |
| Teste comparativo |  | Equipe | MVP | Planejado |

| Risco | Probabilidade | Impacto | Mitigação |
|---|---|---|---|
| Relatórios com formato variável | Média | Alto | Modelo padrão de importação |
| Falta de liberação dos dados | Média | Médio | Usar dados sintéticos |
| Resistência à mudança | Baixa | Médio | Envolver a equipe no piloto |
| Arredondamento diferente da planilha manual | Média | Alto | Teste de diferença zero contra o gabarito (RN09) |
| Regra da dotação não escrita | Média | Alto | Escrever a RN10 com o orçamento antes do sprint de distribuição |

**Apoio necessário:** Equipe de licitações (regras e exemplos), setor de orçamento (dotação), professor (construção do MVP).
**Aprendizado necessário:** Ler e cruzar planilhas com script, regras de dotação orçamentária e publicação no GitHub Pages.

# Anexo D — A defesa

**Frase de defesa:** Se o tempo de montagem do mapa passar de A MEDIR horas para uma fração disso, a equipe de licitações deixa de redigitar e conferir planilhas à mão.
**Provas:** 1) Descrição do fluxo atual em 8 etapas, com exemplos reais das planilhas. 2) Etapas repetitivas e com regra clara (cálculos, separação, conferência). 3) Teste com dados de exemplo comparando manual x automático.
**Piloto:** Rodar um processo já encerrado na ferramenta e comparar totais e tempo com o mapa manual, medindo as duas versões.
**Maior risco:** Relatórios do pregoeiro em formato variável; tratar com um modelo padrão de importação e validação de colunas.

# Anexo E — Documentos enviados

**Descrição dos documentos:** WorkFlow.docx: descrição do fluxo atual do Mapa de Distribuição, com exemplos 1 a 8 das planilhas.
**O que ainda falta:** WorkFlow.docx (exemplos 1 a 8), planilhas de exemplo sem dado pessoal, relatório do pregoeiro de amostra, mapa manual de um processo encerrado (gabarito) e medição de tempo das etapas.
