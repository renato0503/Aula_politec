# Projeto TEIA (Triagem de E-mails com Isolação Automatizada)

Projeto de **Nelson e Luciana** · Coordenadoria de Perícias em Biologia Molecular · 2026-11-03

## 1. Identificação

| Campo | Valor |
|---|---|
| Projeto | Projeto TEIA (Triagem de E-mails com Isolação Automatizada) |
| Tipo | Automação de script ou rotina |
| Alunos | Nelson e Luciana |
| Unidade | Coordenadoria de Perícias em Biologia Molecular |
| Contato | nelsonyoshitake@politec.mt.gov.br |
| Fonte | `envio-original.json` (Firestore, 03/11/2026) |

## 2. Problema e impacto

**Problema.** As cobranças de laudos periciais chegam à POLITEC com dados essenciais dispersos em e-mails e anexos diversos, exigindo uma triagem manual morosa e arriscada quanto ao sigilo de informações sensíveis.

**Como é hoje.** Recebimento da Requisição: O coordenador acessa a caixa de e-mails institucional da POLITEC e abre a mensagem enviada pelo Ministério Público, Delegacia ou Poder Judiciário;
Download e Abertura Manual de Anexos: O coordenador faz o download e abre individualmente cada arquivo anexado (ofícios em PDF, cópias de inquéritos, despachos e termos de apreensão);
Leitura e Varredura Visual: A pessoa lê o corpo do e-mail e navega pelas páginas dos anexos buscando manualmente os campos essenciais (número do ofício/cobrança, data, protocolo, tipo de crime, regional de destino, se há Amostra de Referência e qual é o objetivo exato da perícia);
Digitação e Consolidação na Planilha: Os dados localizados são digitados um a um nos campos correspondentes de uma planilha de controle;
Tratamento de Pendências e Encaminhamento: Se alguma informação crítica estiver ausente ou confusa no e-mail, o servidor precisa redigir uma resposta solicitando complementação; caso esteja tudo correto, realiza o direcionamento do pedido para o setor de custódia para posterior processamento.

**Impacto.** Dimensão: Tempo; Impacto Atual (Estimativa Operacional): 12 a 15 minutos dedicados por e-mail/requisição recebida; Evidência / Métrica do Número: Medição de tempo médio de ciclo: abertura do e-mail, download e varredura de 3 a 5 anexos em PDF, localização visual dos 8 campos e cópia/digitação na planilha. Em um volume de 40 e-mails/dia, representa 8 a 10 horas/dia de trabalho manual contínuo.
		
Dimensão: Custo; Impacto Atual (Estimativa Operacional): R$ 6.000 a R$ 10.000/mês por regional em horas-homem pagas para digitação; Evidência / Métrica do Número: Custo/hora médio do servidor público alocado × ~160 a 200 horas mensais consumidas exclusivamente com triagem administrativa em vez de atividades periciais de ponta.
		
Dimensão: Qualidade; Impacto Atual (Estimativa Operacional): 8% a 15% de erro de transcrição ou omissão de dados; Evidência / Métrica do Número: Taxa padrão de erro humano em entrada manual de dados não estruturados (troca de dígitos em protocolos, erro no tipo de crime ou não marcação da existência de Amostra de Referência - AR).
		
Dimensão: Risco; Impacto Atual (Estimativa Operacional): Alto risco legal e de conformidade (LGPD/Sigilo); Evidência / Métrica do Número: 1. Atravancamento processual: Perda de prazos judiciais por erro na identificação do nível de urgência ou regional incorreta; 2. Vazamento de dados: Manuseio manual recorrente de arquivos contendo dados sensíveis de inquéritos e segredos de justiça.
		
Dimensão: Retrabalho; Impacto Atual (Estimativa Operacional):	15% a 20% do volume precisa ser reanalisado ou corrigido posteriormente; Evidência / Métrica do Número: Amostra de chamados e e-mails de acompanhamento enviados pelo MP/Delegacias para corrigir dados cadastrados errados, solicitar reenvio de laudos ou reencaminhar peças para a regional correta.

**Limite.** Homologação e Validação dos Dados (Fé Pública)
O que é: A confirmação de que os dados extraídos pelo script para a planilha correspondem exatamente ao documento original.
Por que não automatizar: O script atua como um assistente de leitura e pré-preenchimento, mas a fé pública e a responsabilidade legal sobre a exatidão das informações registradas no sistema institucional permanecem integralmente com o servidor público.

Deferimento, Triagem Crítica e Recusa de Requisições
O que é: A decisão de aceitar o pedido, devolvê-lo por falta de requisitos formais ou priorizar o trâmite devido à urgência da diligência.
Por que não automatizar: Avaliar se um ofício atende aos requisitos jurídicos/técnicos para instauração do laudo envolve juízo discricionário e interpretação do contexto processual, prerrogativas indelegáveis a códigos ou algoritmos.

Resolução de Conflitos e Inconsistências Contextuais
O que é: A deliberação quando há divergências entre o corpo do e-mail e o anexo (ex: corpo do e-mail cita crime de homicídio, mas o PDF do inquérito refere-se a furto).
Por que não automatizar: Identificar a intenção real da autoridade requisitante (MP/Polícia Civil) e decidir se o e-mail deve ser retificado exige contato humano, bom senso e alinhamento institucional.

Validação da Cadeia de Custódia da Amostra de Referência (AR)
O que é: A confirmação de que o material físico para confronto (sangue, DNA, projétil) efetivamente chegou à regional e está devidamente lacrado.
Por que não automatizar: O script identifica no texto a menção à existência de AR, mas a conferência física do invólucro, verificação do lacre e recepção do material biológico/físico são atos estritamente presenciais e periciais.

Ao delimitar esses pontos na proposta, o projeto se posiciona claramente como uma ferramenta de copiloto administrativo (automação da digitação repetitiva), mantendo a autoridade, a segurança jurídica e a tomada de decisão 100% sob o controle do servidor público.

## 3. AS-IS · o processo antes do MVP

| etapa | papel | entra | acao | sai | sistema | regra | espera | tempo | auto |
|---|---|---|---|---|---|---|---|---|---|
| Chegada do e-mail de requisição | Autoridade Requisitante (MP/PC/Poder Judiciário) | Minuta do e-mail + Ofício/Anexos em PDF | Envio de e-mail institucional com solicitação de laudo pericial para a POLITEC | E-mail recebido na caixa de entrada institucional | Servidor de E-mail | N/A (Ato externo da autoridade) | Fila de e-mails não lidos na caixa de entrada | 0,00 | Não |
| Triagem inicial e abertura do e-mail | Servidor / Triador da POLITEC | E-mail na caixa de entrada | Servidor identifica o e-mail não lido, abre a mensagem e faz a leitura preliminar do assunto e corpo | E-mail aberto no monitor | Webmail / Leitor de E-mail | Priorização visual por ordem de chegada ou urgência indicada | Caixa de entrada (aguardando tempo do servidor para abrir) | 0,50 a 4,00 | Sim, com regra clara |
| Download e leitura dos anexos | Servidor / Triador da POLITEC | Anexos em PDF / Imagens (Ofícios, Inquéritos, BOs) | Baixar todos os anexos, abrir arquivo por arquivo e realizar varredura visual em busca dos dados chaves | Anexos abertos e dados localizados na tela | Leitor de PDF / Sistema de Arquivos local | Verificar se os anexos estão legíveis, completos e se pertencem ao processo | Pasta de downloads / Leitura manual de múltiplas páginas em PDF | 0,10 a 0,25 | Sim, com regra clara |
| Mapeamento dos 8 campos essenciais | Servidor / Triador da POLITEC | Texto do e-mail e conteúdo dos PDFs abertos | Localizar e conferir visualmente: Data, Nº Cobrança, Nível, Crime, Protocolo, AR, Objetivo e Regional | 8 variáveis identificadas mentalmente pelo servidor | Anotação manual / Memória | Regra de negócio: confirmar se a requisição tem todos os dados obrigatórios para autuação | Navegação visual entre corpo do e-mail e múltiplos PDFs | 0,10 a 0,15 | Sim, com regra clara |
| Digitação e consolidação na planilha | Servidor / Triador da POLITEC | 8 campos mapeados + Planilha de controle aberta | Copiar/digitar os dados identificados no e-mail/PDFs para a linha correspondente na planilha | Linha da planilha preenchida manualmente | Excel / Google Sheets / LibreOffice | Padronização dos nomes de regional, tipos de crime e formatos de data | Mão de obra / Digitação manual campo a campo (risco de erro humano) | 0,05 a 0,10 | Sim, com regra clara |
| Download, renomeação e organização dos PDFs | Servidor / Triador da POLITEC | PDFs baixados sem padrão de nome | Renomear o arquivo PDF no padrão da instituição (ex: Protocolo + Regional) e mover para a pasta correta | Arquivo PDF renomeado e salvo na pasta institucional | Gerenciador de Arquivos do S.O. | Padronização da nomenclatura dos arquivos | Operação manual de "Salvar Como", renomear e mover arquivos | 0,05 a 0,10 | Sim, com regra clara |
| Validação, aceite e encaminhamento legal | Servidor / Triador da POLITEC | Linha da planilha preenchida + Anexos salvos | Conferir os dados inseridos, validar aceite da requisição e assinar/encaminhar para a regional responsável | Requisição oficializada e atribuída ao setor pericial | Planilha + Sistema Interno de Tramitação | Fé pública: confirmar validade do ofício, cadeia de custódia e ausência de impedimento legal | Mesa do servidor (Aguardando análise e decisão humana) | 0,20 a 1,00 | Não |

## 4. TO-BE · o processo com o MVP

**Mudança central.** A mudança principal consiste na substituição da triagem manual e fragmentada por um fluxo de extração automatizada local, alterando o papel do servidor público de "digitador/leitor de PDFs" para "validador de fé pública".
Em termos operacionais, o processo migra de uma arquitetura baseada em esforço humano repetitivo para uma arquitetura de processamento em lote orientado a eventos:
Antes (AS-IS): O servidor gastava de 12 a 15 minutos por requisição abrindo e-mails, baixando e varrendo visualmente arquivos PDF, copiando 8 campos manualmente para a planilha e renomeando arquivos um a um.
Depois (TO-BE): O script local varre a caixa de correio, lê e estrutura o conteúdo dos arquivos PDF, popula a planilha com as 8 variáveis em segundos e organiza os anexos em pastas locais. O servidor intervém apenas no final do fluxo, levando menos de 1 minuto para checar o pré-preenchimento, resolver eventuais alertas de divergência e homologar a autuação.

**Visão.** O processo de triagem da POLITEC passa a ser executado por um script local que faz a varredura automática de e-mails e anexos, extrai e organiza os 8 campos essenciais na planilha sem expor dados a IAs externas, restando ao servidor apenas a validação rápida e o aceite final das requisições periciais.

| etapa | muda | quem | beneficio | esforco |
|---|---|---|---|---|
| Monitoramento e varredura da caixa de e-mails | Substitui a checagem manual periódica por varredura automatizada continua/programada. | A máquina (automação) | Eliminação do tempo de espera na caixa de entrada e início imediato do processamento. | Baixo |
| Extração de texto e leitura dos anexos (PDF/Imagens) | A leitura visual de múltiplos anexos é substituída pela extração via código e OCR local. | A máquina (automação) | Redução drasticamente do tempo de leitura (de minutos para segundos por arquivo). | Baixo |
| Mapeamento dos 8 campos essenciais | A busca visual no texto é feita por regras de regex/parsing local, identificando as 8 variáveis. | A máquina (automação) | Padronização e eliminação de omissões ou erros de transcrição manual. | Baixo |
| Preenchimento da planilha e sinalização de alertas | Inserção automática da linha populada com dados e atribuição de flags em inconsistências. | A máquina (automação) | Fim da digitação manual ("copiar e colar") e identificação visual instantânea de erros. | Baixo |
| Salvamento, renomeação e organização dos arquivos | PDFs baixados são automaticamente renomeados (Padrão: Protocolo + Regional) e movidos. | A máquina (automação) | Organização padronizada imediata no repositório local sem intervenção manual. | Baixo |
| Validação de fé pública e decisão de aceite | Servidor apenas confere o pré-preenchimento na planilha e valida o aceite da requisição. | A pessoa, sem mudança | Manutenção da legalidade, fé pública e segurança jurídica com consumo mínimo de tempo. | Baixo |
| Autuação e encaminhamento para a Regional | A requisição validada é autuada e enviada ao setor/perito responsável pela emissão do laudo. | A pessoa, sem mudança | Tramitação rápida e segura, pronta para o início da atividade pericial de ponta. | Baixo |

## 5. MVP

**Objetivo.** Demonstrar, em ambiente local controlado, que a varredura e a extração automática das 8 variáveis das requisições periciais reduzem o tempo de triagem de 15 minutos para menos de 1 minuto por processo, preservando 100% o sigilo dos dados e a soberania da fé pública do servidor.

**Critério de aceite.** O MVP será considerado aprovado e pronto para a fase de homologação se atender aos seguintes 5 critérios operacionais e mensuráveis:
Redução Comprovada do Tempo de Triagem:
O tempo total gasto pelo servidor para conferir a planilha e homologar a requisição é de menos de 1 minuto por processo (comparado aos 12–15 minutos do fluxo AS-IS manual).
Acurácia na Extração dos 8 Campos (em PDFs Impressos/Pesquisáveis):
O script extrai corretamente as 8 variáveis chaves com taxa de acerto 
≥95% nos testes em massa de dados controlada, populando as colunas da planilha de forma estruturada.
Tratamento de Exceções sem Travamento do Sistema:
Em 100% dos casos de erro (PDFs corrompidos, manuscritos, anexos faltantes ou arquivos não suportados), o script não interrompe a execução do lote: isola o arquivo, aplica a flag de alerta amarela/vermelha na planilha e grava a falha no log local.
Organização e Padronização de Arquivos:
100% dos anexos processados são salvos e renomeados no padrão exato ([PROTOCOLO]_[REGIONAL]_[NOME].pdf) no diretório local, com hiperlinks válidos e funcionais na planilha.
Garantia Total de Sigilo e Isolamento (LGPD):
O processamento é concluído de forma 
100% offline, comprovado por auditoria de tráfego de rede (zero requisições de saída para APIs ou servidores externos).

**Plataforma.** Programa de desktop

**Telas do protótipo:**

- `#/painel` · bancada de triagem (fila à esquerda, 8 campos à direita);
- `#/email/:id` · mensagem, anexos, campos, validação e auditoria;
- `#/lote` · extração de um lote;
- `#/planilha` · planilha consolidada e CSV;
- `#/config` · dicionários, backup, dados fictícios e testes.

A extração neste protótipo é **simulada** com os dados fictícios de `exemplos/seed.json`. O que o script local faria (parsing, OCR e renomeação) está representado nos campos, nas confianças e nos alertas.

## 6. Dados e LGPD

- Nenhum dado sai da estação: o processamento é local e o protótipo não faz requisição de rede.
- Dados do requisitante, das partes e dados sensíveis (DNA, saúde, inquérito) ficam no navegador, com backup `.json` e trilha de auditoria.
- Base legal do projeto: art. 7º, III e art. 11, II, "s" da LGPD, conforme a especificação.
- Retenção e descarte devem seguir a orientação da POLITEC antes do piloto.

## 7. Regras de negócio

| id | regra | quando | tipo | excecao |
|---|---|---|---|---|
| RN01 | As 8 variáveis essenciais são obrigatórias para a requisição ficar pronta: DATA COBRANÇA, Nº COBRANÇAS, NÍVEL, TIPO DE CRIME, PROTOCOLO, AR PARA CONFRONTO, OBJETIVO CLARO e NOME DA REGIONAL. | Na extração e na validação | Validação | Campo ausente vira pendência e destaca a linha. |
| RN02 | Divergência entre o corpo do e-mail e o anexo gera alerta DIVERGÊNCIA_DETECTADA e exige decisão humana. | Na extração | Negócio | O servidor escolhe o valor correto. |
| RN03 | PDF escaneado, manuscrito ou ilegível vai para leitura manual/OCR e não é homologado automaticamente. | Na leitura do anexo | Negócio | OCR local com confiança baixa. |
| RN04 | A validação final é ato humano do servidor triador, com identificação e data/hora. | Na validação | Controle | Nenhuma. |
| RN05 | Termos como URGENTE, PLANTÃO e HOMICÍDIO RECENTE elevam a prioridade para alta. | Na triagem | Priorização | O servidor pode ajustar a prioridade. |
| RN06 | Nenhum dado sai da estação: o processamento e a extração são locais (LGPD e segredo de justiça). | Sempre | Segurança | Nenhuma. |
| RN07 | Toda validação, correção, recusa ou pendência entra na trilha de auditoria. | Em toda ação | Auditoria | Nenhuma. |

## 8. Métricas do piloto

| nome | pergunta | base | esperado | fonte |
|---|---|---|---|---|
| Tempo Médio de Triagem por Processo | Quanto tempo o servidor leva para abrir, conferir e registrar uma requisição? | 15 min | < 1 min | Planilha Consolidada do Triador / Cronometragem |
| Taxa de Acurácia na Extração Automática | Qual o percentual de requisições cujas 8 variáveis foram extraídas corretamente sem intervenção humana? | 0% (Processamento 100% manual) | >= 95% | Log de Auditoria (execucao.log) e Planilha Consolidada |
| Taxa de Ingestão de Exceções sem Travamento | O sistema consegue isolar falhas (PDFs corrompidos/manuscritos) e aplicar as flags visuais sem parar o lote? | A MEDIR | 100% | Log de Auditoria (execucao.log) |
| Taxa de Conformidade no Renomeio de Anexos | Quantos anexos foram salvos no diretório local com a nomenclatura padronizada e link funcional? | A MEDIR | 100% | Repositório de Anexos (/anexos) e Planilha |
| Índice de Conexões Externas Não Autorizadas (Sigilo LGPD) | ouve qualquer tentativa de tráfego de dados para fora da rede local durante a execução do MVP? | 0 conexões | 0 conexões | Auditoria de Segurança / Logs de Firewall Local |

## 9. Papéis

| papel | quem | ve | faz | naofaz | registro |
|---|---|---|---|---|---|
| Servidor Triador (Operador) | Servidor administrativo ou perito responsável pela recepção e triagem das requisições na POLITEC. | Dashboard local com a planilha de requisições pré-preenchidas pelo script, alertas de inconsistência/erro, anexos renomeados e status de cada e-mail. | Revisa os dados extraídos pela IA/script, corrige divergências, valida/autentica os 8 campos, confirma a recepção física de AR e aprova/recusa a requisição. | Alterar o código-fonte do script, modificar regras de extração local, acessar dados sigilosos fora do seu escopo de atribuição ou deletar logs de auditoria. | Confirmações de validação, edições manuais de dados, aprovações, recusas de expedientes e carimbo de data/hora (timestamp) de cada ação realizada. |
| Administrador do Sistema (TI / Dev) | Desenvolvedor do script, analista de TI ou responsável técnico pela manutenção da ferramenta local. | Logs de execução do script, taxa de sucesso na leitura de anexos, métricas de desempenho/erros de OCR, telas de configuração e regras de regex/parsing. | Mantém o script atualizado, ajusta regras de extração e OCR local, monitora a integridade das pastas/planilhas e gerencia permissões de acesso local. | Validar legalmente requisições periciais, autuar processos jurídicos, alterar o conteúdo de laudos ou atuar como validador de fé pública. | Alterações de código, modificações de parâmetros de regras, execuções de manutenção, falhas do sistema e acessos a pastas de sistema |
| Script de Automação (Agente de Sistema) | O próprio script executado localmente (sem acesso à internet) para varredura e extração de dados. | Caixas de e-mail institucionais (corpo e metadados), arquivos anexos (PDFs, imagens) e tabelas locais de referência (regionais, tipificações). | Varre a caixa de e-mails, extrai os 8 campos requeridos, renomeia e salva anexos em diretório seguro e popula a planilha local com flags de inconsistência. | Tomar decisões jurídicas/administrativas, assinar certidões, autuar laudos, enviar dados para APIs externas ou apagar e-mails originais da caixa de entrada. | Início/fim de execuções, e-mails lidos, anexos processados, taxa de confiança do OCR, erros de extração e linhas adicionadas à planilha. |
| Gestor / Chefia Pericial (Consulta) | Diretor regional, chefe de equipe ou coordenador da unidade da POLITEC. | Relatórios consolidados de desempenho, volume de requisições recebidas por regional, estatísticas de tipos de crime e tempo médio de triagem. | Acompanha indicadores da unidade, monitora gargalos na recepção de requisições e toma decisões estratégicas de redistribuição de demandas periciais | Editar dados de requisições em triagem, alterar parâmetros do script local ou aprovar cadastros técnicos pendentes de validação pelo triador. | Consultas a relatórios consolidados, exportação de estatísticas e visualizações do painel gerencial. |

## 10. Piloto, marcos e riscos

| marco | data | resp | dep | sit |
|---|---|---|---|---|
| M01: Aprovação da Especificação e Conformidade LGPD | Dia 1 | Líder do Piloto / Chefia da Triagem | Parecer de sigilo local e validação das 8 variáveis essenciais | Feito |
| M02: Liberação do Ambiente Técnico e Permissões Locais | Dia 3 | Gerência de TI da POLITEC | Perfilamento de instalação do Python 3.10+ / Tesseract OCR e permissões de diretório (/entrada, /painel) | Planejado |
| M03: Construção do Dicionário De/Para e Base Sintética | Dia 5 | TI / Chefia da Triagem | Coleta de nomenclaturas oficiais de regionais/crimes e geração de 30 PDFs de teste | Planejado |
| M04: Entrega dos Scripts e Painel SPA (main.py + index.html) | Dia 8 | Desenvolvedor / TI | Homologação em sandbox dos motores de parsing, regex e | Planejado |
| M05: Execução do Piloto de Campo e Coleta da Linha de Base | Dias 9 a 18 | Servidor Triador / Líder do Piloto | Execução do script com 200 a 300 requisições reais e auditoria dos logs (execucao.log) | Planejado |
| M06: Apresentação dos Resultados e Consolidação das Métricas | Dia 20 | Líder do Piloto | Apuração das métricas M01 a M05 e validação final da hi | Planejado |

## 11. Entidades do protótipo

| entidade | representa | colunas | chave | volume |
|---|---|---|---|---|
| Email | Mensagem de requisição recebida | id, assunto, remetente, corpo, recebido_em, prioridade, status | id | 100/mês |
| Anexo | Ofício, inquérito ou termo em PDF/imagem | id, email_id, nome, tipo, paginas, legivel, status | id | 3 a 5 por e-mail |
| Extracao | Os 8 campos extraídos de um e-mail | id, email_id, campos, confianca, alerta, status, validado_por, validado_em | id | 1 por e-mail |
| Lote | Conjunto de e-mails processados juntos | id, nome, email_ids, criado_em, status | id | 1 por rodada |

## 12. O que ainda não está no protótipo

- OCR real de PDF imagem e leitura de anexos reais;
- renomeação e organização de arquivos no sistema operacional;
- parsing de e-mails reais (o protótipo usa a caixa fictícia);
- integração com a caixa institucional e com o sistema de tramitação;
- assinatura/autuação oficial.

## 13. Referências

- `envio-original.json` · `projeto.json` · `processo.html`
- `README.md` · `sprint.md` · `contexto.md`
