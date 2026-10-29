# PROJETO.md — Automação do monitoramento de metas pelo BI

**Aluno ou equipe:** Karine Assunção
**Unidade:** CQUAL
**Contato:** karineassuncao@politec.mt.gov.br
**Projeto:** Automação do monitoramento de metas pelo BI
**Tipo de projeto:** Automação de script ou rotina
**Data:** 2026-10-27
**Resumo:** Desenvolver uma automação mensal de extração por OCR, validação dos dados e atualização controlada da planilha.

## 1. Problema (a dor)

**Problema:** Extração manual dos dados.
**Impacto:** O fluxo atual exige a transferência manual dos dados extraídos do Power BI 1 para o Google Planilhas, tornando o processo de monitoramento das metas mais demorado e operacionalmente dependente da intervenção humana. Essa atividade aumenta o risco de erros de digitação, inconsistências nos indicadores e divergências nos resultados apresentados no Power BI de monitoramento, além de dificultar a rastreabilidade e a padronização das atualizações mensais.
**Quem sofre:** Autoridade
**Como é feito hoje:** o fluxo atual é realizado através da consulta dos dados no Power BI 1, transferência manual para o Google planilhas e esse google planilhas alimenta um novo Power BI de monitoramento, teria como automatizar essa função de alimentar manualmente o Google Planilhas.
**Evidências:** Medida feita pela equipe
**Detalhe da evidência:** Tempo gasto com a conferência dos dados
**O que não pode ser automatizado:** O acesso ao API do Power BI 1

## 2. Objetivo do MVP (o que faz e o que NÃO faz)

**Objetivo do MVP:** Validar a viabilidade da extração automatizada de dados do PDF do Power BI 1 por OCR e sua transferência para o Google Planilhas, reduzindo o trabalho manual e garantindo a confiabilidade dos indicadores no Power BI de Monitoramento.
**O que o MVP não faz:** O MVP não integra com a base de dados original do Power BI 1.
**Entregável do projeto:** App em um único HTML que lê o relatório do Power BI 1, confere os números e gera o arquivo para atualizar a planilha do Google, com manual de uso em PDF.
**Dentro do escopo:** Ler o relatório mensal do Power BI 1 (PDF ou, se permitido, exportação em CSV/Excel); extrair os laudos pendentes por unidade e mês; validar (mês de referência, totais, unidades conhecidas, variação brusca); mostrar a conferência lado a lado; gerar o arquivo no layout da planilha do Google; guardar o histórico dos meses.
**Fora do escopo:** A base dados original (API)
**Plataforma alvo:** Site web (abre no navegador)
**Primeira tela:** Tela de importação: escolher o arquivo do mês (PDF ou CSV exportado do Power BI 1) e ver o mês de referência e o resumo do que foi lido.
**Simulado no MVP:** Se o PDF for só imagem, o OCR roda no navegador (Tesseract.js); o MVP aceita digitação assistida nos campos que o OCR não ler.
**Critério de aceite:** Nos 3 meses do piloto, os números gerados pelo app são iguais aos digitados à mão (diferença zero), e as divergências plantadas no teste são apontadas.
**Dados de exemplo:** Quantitativo de laudos pendentes (passivo) por unidade e mês; 3 relatórios mensais com números fictícios para o teste.
**O que já existe pronto e pode ser reaproveitado:** o PDF que será inserido na pasta de entrada no Google DriveSS
**Dependências:** Acesso ao Power BI 1

## 3. Usuários e papéis

| Papel | Quem é | O que enxerga | O que faz | O que não pode fazer | Registro |
|---|---|---|---|---|---|
| NIINS (operador) | Servidor do núcleo | Relatório do mês e conferência | Importa o relatório e gera a planilha | Alterar número sem registro | Importação e correções |
| Chefe de núcleo | Chefia | Conferência e histórico | Aprova o mês | Aprovar mês com divergência aberta | Aprovação do mês |

**Observações sobre os papéis:** Extração e conferência dos dados

## 4. Dados (entidades e colunas; tudo SINTÉTICO)

| Entidade | O que representa | Colunas | Chave | Volume | Origem | Sintético |
|---|---|---|---|---|---|---|
| RelatorioMensal | Arquivo do Power BI 1 de um mês | id: texto, mes_ref: texto (AAAA-MM), arquivo: texto, tipo: texto (pdf, csv), importado_em: data, aprovado_por: texto | id | 1 por mês | Power BI 1 | Parcialmente |
| Pendencia | Laudos pendentes de uma unidade no mês | id: texto, mes_ref: texto, unidade: texto, pendentes: inteiro, origem: texto (pdf, ocr, digitado), confianca: número | id | Uma por unidade e mês | Extração | Sim |
| Correcao | Número alterado na conferência | id: texto, pendencia_id: texto, valor_lido: inteiro, valor_final: inteiro, motivo: texto, data: data | id | Poucas por mês | Conferência | Sim |

**O que precisa ser coletado:** Os dados já estão disponíveis
**Quem libera o acesso:** O acesso é permitido através de link e liberado pelo chefe de núcleo

### Fontes de dados do processo real

| Fonte | Tipo | Onde | Existe | Uma linha é | Volume | Campos de data | Atualiza | LGPD |
|---|---|---|---|---|---|---|---|---|
| Relatório do Power BI 1 | Relatório | Power BI 1 (TI) | Sim | Uma unidade no mês | 1 relatório por mês | Mês e ano | Mensal | Não |
| Planilha de monitoramento | Planilha local | Google Drive | Sim | Uma unidade no mês | Unidades × meses | Mês e ano | Mensal | Não |


## 5. Regras de negócio (RN01, RN02...)

| ID | Regra | Quando se aplica | Exceção | Quem valida | Tipo |
|---|---|---|---|---|---|
| RN01 | O relatório deve possuir um mês de referência válido. | Toda importação | Relatório sem período identificável é rejeitado. | Automação | Validação |
| RN02 | A soma das unidades tem que bater com o total do relatório | Na conferência | Diferença vira bloqueio | Sistema | Validação |
| RN03 | Unidade não cadastrada vira alerta | Na extração | A pessoa associa ou cadastra | NIINS | Validação |
| RN04 | Variação acima de 30% em relação ao mês anterior vira alerta | Na conferência | Confirmada pela pessoa | NIINS | Validação |
| RN05 | Mês aprovado não muda; correção gera nova versão com motivo | Depois da aprovação | Nenhuma | Chefe de núcleo | Negócio |


## 6. Telas (#/painel, #/lista...)

| Rota | Tela | Objetivo | Quem usa | Dados | Ação | Regra | Tipo | Verificável como | MVP |
|---|---|---|---|---|---|---|---|---|---|
| #/importar | Importar o mês | Ler o relatório do Power BI 1 | NIINS | Arquivo, mês, unidades lidas | Importar | RN01 | Tela | Mês lido e 100% das unidades | Sim |
| #/conferencia/:mes | Conferência | Comparar e corrigir | NIINS e chefe | Número lido, número anterior, variação, alerta | Confirmar ou corrigir | RN02 a RN04 | Tela | Divergência plantada é apontada | Sim |
| #/exportar/:mes | Gerar planilha | Atualizar o Google Planilhas | NIINS | Linhas no layout da planilha | Baixar .xlsx/.csv ou copiar | RN05 | Ação | Arquivo importa sem ajuste | Sim |
| #/historico | Histórico | Ver os meses | Chefe | Meses, totais, quem aprovou | Consultar |  | Relatório | Mostra os 3 meses do piloto | Sim |


## 7. KPIs (nome = fórmula em uma linha)

| KPI | Pergunta | Fórmula | Fonte | Linha de base | Valor esperado | Como medir |
|---|---|---|---|---|---|---|
| Tempo mensal de atualização | Quanto tempo leva para atualizar o mês? | Hora da aprovação − hora do início | Cronômetro | 8 h (informado) | Menos de 1 h | Cronometrar o mês atual |
| Divergências na conferência | Os dados estão corretos? | Números corrigidos ÷ números do mês | Correções do app | A medir no mês atual | Zero após a conferência | Comparar a planilha digitada com o Power BI 1 |

**Período da linha de base:** Período disponível para análise comparativa
**Campos de data e tempo que existem:** mês e ano

## 8. Stack: HTML único (CSS/JS inline), dados em JSON embutido, GitHub Pages.

**Stack escolhida:** HTML único (CSS/JS inline), dados em JSON embutido, GitHub Pages
**Detalhe da stack:** Um único index.html com pdf.js (texto do PDF), Tesseract.js (OCR, só se o PDF for imagem) e SheetJS (gerar o .xlsx/.csv), tudo embutido. Dados no IndexedDB. A atualização da planilha do Google é feita importando o arquivo gerado (ou colando), sem credencial no app.
**Hospedagem:** Arquivo HTML único, aberto no navegador do núcleo, sem servidor e sem enviar o relatório para fora; o arquivo gerado é importado na planilha do Google.
**Custo e licenças:** R$0
**Contas e domínio:** Chefe de núcleo

| Opção | Tipo | Onde roda | Custo | Quem mantém | Acesso | Banco de dados | Escala | Limitação |
|---|---|---|---|---|---|---|---|---|
| Arquivo HTML único | Arquivo local | Navegador do computador da unidade | Zero | Equipe do projeto | Quem recebe o arquivo | IndexedDB do navegador | Uma cópia por setor; consolidação por arquivo .json | Os dados ficam no computador; backup semanal |
| Google Apps Script + Drive | Nuvem corporativa | Conta institucional Google | Zero | NIINS | Conta institucional | Google Planilhas | Mensal | Depende da autorização da TI e das cotas de OCR |


## 9. Restrições e LGPD

**Restrições:** PDF predominantemente em imagem e Permissões e segurança institucional:
**Dados pessoais tratados:** Nenhum dado pessoal: quantitativos de laudos por unidade e mês.
**Base legal:** Tratamento de dados destinado ao monitoramento das metas institucionais da POLITEC, com a finalidade de automatizar a extração
**Retenção:** Os arquivos e dados utilizados no MVP serão mantidos durante o período de testes, pelo tempo estritamente necessário à validação da solução
**Acesso e registro:** O acesso ao MVP será restrito aos servidores e colaboradores autorizados envolvidos no desenvolvimento, teste e validação da solução. 
**Requisitos marcados:** Segurança e controle de acesso, Trilha de auditoria, Funcionar offline

---

# Anexo A — AS-IS (o fluxo de hoje)

**Início:** Solicitação de demanda 
**Fim:** Reunião mensal
**Entradas:** Consulta dos dados do Power BI 1
**Saídas:** Visualização e monitoramento das metas
**Volume:** 2
**Duração:** 8h
**Frequência:** Mensal
| Etapa | Quem faz | O que entra | Ação | O que sai | Sistema | Regra | Onde espera | Tempo (h) | Automatizável |
|---|---|---|---|---|---|---|---|---|---|
| Receber a demanda do mês | NIINS | Calendário da reunião mensal | Inicia a coleta | Demanda aberta | E-mail | Mensal | Não identificado | 0,5 | Sim, com regra clara |
| Consultar o Power BI 1 | NIINS | Painel do Power BI 1 | Consulta os laudos pendentes por unidade | Números do mês | Power BI 1 | Mês de referência | Acesso ao painel | 1 | Sim, com regra clara |
| Digitar na planilha | NIINS | Números do mês | Digita no Google Planilhas | Planilha atualizada | Google Planilhas | Uma linha por unidade e mês | Não identificado | 4 | Sim, com regra clara |
| Conferir | Chefe de núcleo | Planilha e Power BI 1 | Compara os números e corrige | Planilha conferida | Google Planilhas | Números iguais aos do Power BI 1 | Correções | 2 | Sim, com apoio humano |
| Atualizar o painel e reunir | NIINS | Planilha conferida | Atualiza o Power BI de monitoramento | Indicadores do mês | Power BI de monitoramento | Atualização antes da reunião | Reunião mensal | 0,5 | Sim, com regra clara |

**Decisões e aprovações:** A principal bifurcação do fluxo ocorre após a conferência dos dados extraídos do Power BI 1 e inseridos manualmente no Google Planilhas.
**Exceções:** Sim: prosseguir com a atualização da base de dados e disponibilização dos indicadores no Power BI de monitoramento.
Não: revisar e corrigir os dados na planilha, confrontando-os com o relatório original do Power BI 1, antes de prosseguir.
**Já digitalizado:** Os dados iniciais são todos digitalizados.

# Anexo B — TO-BE (o fluxo depois da mudança)

**Visão do futuro:** Automatizar a extração, validação e transferência dos dados do Power BI 1 para o Google Planilhas, garantindo maior agilidade, confiabilidade e padronização no monitoramento mensal das metas institucionais da POLITEC, com atualização dos indicadores no Power BI de monitoramento e redução de falhas operacionais.
**Mudança principal:** Substituir o preenchimento manual do Google Planilhas por um processo automatizado de extração e validação dos dados do PDF emitido pelo Power BI 1,
**O que fica igual:** Permanecem inalterados o Power BI 1 como fonte dos dados, a emissão mensal do relatório em PDF, o Google Planilhas como base de armazenamento dos indicadores.
**O que não pode mudar:** Permanecem inalterados o Power BI 1 como fonte dos dados.
| Etapa | O que muda | Quem executa | Benefício | Esforço |
|---|---|---|---|---|
| Exportar o relatório | Baixa o PDF (ou o CSV) do Power BI 1 | A pessoa, sem mudança | Fonte única do mês | Baixo |
| Ler e extrair | O app lê o arquivo e extrai os números por unidade | A máquina (automação) | Fim da digitação | Médio |
| Conferir | O app compara totais, mês e variação, e a pessoa confirma | A pessoa assistida pela máquina | Erro achado antes do painel | Baixo |
| Gerar a planilha | O app gera o arquivo no layout da planilha do Google | A máquina (automação) | Atualização em minutos | Baixo |

**Piloto do TO-BE:** A validação deverá comparar os dados extraídos com o relatório original, verificar possíveis erros de reconhecimento, duplicidades e inconsistências.

# Anexo C — Pesquisa, riscos e plano

**Hipótese de campo:** Os dados serem transferidos erroneamente.
| Referência | Tipo | Fonte ou link | Ano | Dado que extrai | Como usar na defesa | Link conferido |
|---|---|---|---|---|---|---|
| Power BI | Documento interno | Link | 2026 | Pendentes |  | Sim |
| Power BI: exportar dados de visuais | Documento interno | Documentação da Microsoft | 2026 | Exportação em CSV/Excel quando o administrador permite | Mostrar a alternativa ao OCR | Não |

**Lacunas:** Não foram confirmadas a disponibilidade e as permissões necessárias para utilização do Google Apps Script e dos serviços de OCR no ambiente institucional da POLITEC. 
| Marco | Data | Responsável | Depende de | Situação |
|---|---|---|---|---|
| Amostra do PDF e da planilha (números fictícios) | Semana 1 | Karine | TI do Power BI 1 | Planejado |
| Leitura do PDF e conferência | Semana 3 | Karine | Amostra | Planejado |
| OCR para PDF em imagem | Semana 5 | Karine | Leitura | Planejado |
| Piloto de 3 meses | Mês 1 a 3 | Karine e chefe de núcleo | Aceite | Planejado |

| Risco | Probabilidade | Impacto | Mitigação |
|---|---|---|---|
| Erros de reconhecimento do OCR | Alta | Alto | Conferência obrigatória (RN02 a RN04) e preferência pela exportação CSV do Power BI 1 |
| Layout do relatório muda | Média | Médio | Modelo de leitura configurável por coluna |
| Sem permissão para exportar dados do Power BI 1 | Média | Médio | Seguir com o PDF e o OCR |

**Apoio necessário:** Equipe de TI da POLITEC (Responsável pelo Power BI 1)
**Aprendizado necessário:** OCR

# Anexo D — A defesa

**Frase de defesa:** Automatizar a extração e validação dos dados do Power BI 1 para reduzir o trabalho manual, aumentar a confiabilidade das informações e tornar o monitoramento das metas da POLITEC mais ágil e eficiente.
**Provas:** Existência de atividade manual recorrente, Risco de erros e inconsistências e Viabilidade técnica da automação
**Piloto:** 3 meses comparando os dados
**Maior risco:** Erros de reconhecimento do OCR na extração dos dados do PDF, comprometendo a precisão dos indicadores e o monitoramento das metas da POLITEC.

# Anexo E — Documentos enviados

**Descrição dos documentos:** Nenhum documento enviado. Falta uma amostra do PDF do Power BI 1 com números fictícios.
**O que ainda falta:** OCR
