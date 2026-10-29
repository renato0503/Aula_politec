# PROJETO.md — Agiliza +

**Aluno ou equipe:** Diego Costa, Francineide da Silva e Andreia Cristina
**Unidade:** POLITEC no geral
**Contato:** diego.n.costa@aluno.senai.br
**Projeto:** Agiliza +
**Tipo de projeto:** Automação de script ou rotina
**Data:** 2026-10-27
**Resumo:** Desenvolver um gerador em Python que automatize a criação de laudos periciais em Word, aproveitando dados e textos padronizados, com revisão final pelo perito.

## 1. Problema (a dor)

**Problema:** A elaboração manual de laudos de exames periciais menos complexos consome tempo com tarefas repetitivas, preenchimento de dados e adaptação de textos padronizados, aumentando o risco de erros e retrabalho.
**Impacto:** O processo manual consome tempo e aumenta a probabilidade de erros humanos, como falhas no preenchimento de dados, omissões de informações e inconsistências nos textos, gerando retrabalho na elaboração dos laudos de exames periciais menos complexos.
**Quem sofre:** Servidor da unidade
**Como é feito hoje:** Atualmente, o perito reúne os dados da requisição e dos arquivos gerados durante o exame, utiliza um laudo anterior como base e preenche ou adapta manualmente as informações e os textos padronizados no Word, revisando o documento antes de finalizá-lo.
**Evidências:** Entrevista com a equipe
**Detalhe da evidência:** Entrevista com os peritos da Gerência sobre a elaboração de laudos de celular; o grupo descreveu as 14 etapas atuais com base no próprio trabalho.
**O que não pode ser automatizado:** A análise técnica dos vestígios, a interpretação dos resultados, a avaliação das evidências e a elaboração das conclusões periciais devem permanecer sob responsabilidade do perito, pois exigem conhecimento especializado, julgamento técnico e validação humana. A automação deve atuar como ferramenta de apoio, cabendo ao perito conferir os dados, revisar os textos e aprovar o laudo final.

## 2. Objetivo do MVP (o que faz e o que NÃO faz)

**Objetivo do MVP:** Validar a viabilidade de gerar automaticamente laudos Word de exames periciais menos complexos, reduzindo o preenchimento manual e os erros humanos, com revisão final pelo perito.
**O que o MVP não faz:** O MVP não realizará conexão automática com o ATENA, não atenderá exames periciais complexos, não analisará tecnicamente os vestígios, não elaborará conclusões periciais automaticamente, não gerenciará múltiplos usuários nem substituirá a revisão e a validação final do perito. O foco inicial será gerar laudos de exames menos complexos em Word, utilizando arquivos fornecidos pelo perito e textos padronizados.
**Entregável do projeto:** Um gerador de laudos periciais em Python, capaz de automatizar o preenchimento e a formatação de documentos Word a partir de dados e textos padronizados, com conferência e validação final pelo perito.
**Dentro do escopo:** Desenvolvimento de um sistema local em Python para leitura de requisições em PDF por OCR, extração de dados de arquivos TXT e HTML, reutilização de textos padronizados, organização de quesitos e respostas, preenchimento e formatação de laudos Word, conferência automática de campos e revisão final pelo perito.
**Fora do escopo:** Ficam fora do escopo inicial a conexão automática com o ATENA, a realização de exames periciais, a análise técnica dos vestígios, a elaboração automática de conclusões periciais e o atendimento a exames complexos, pois o projeto prioriza a automatização documental de exames menos complexos, mantendo a responsabilidade técnica com o perito.
**Plataforma alvo:** Site web (abre no navegador)
**Primeira tela:** A tela principal do gerador de laudos, com a opção de selecionar a pasta do caso criada pelo perito, localizar automaticamente os arquivos necessários e escolher o modelo institucional ou um laudo anterior em Word para gerar o novo documento.
**Simulado no MVP:** No MVP, a análise automática por OCR de PDFs, a identificação inteligente de quesitos e a sugestão automática de respostas poderão ser simuladas com dados fictícios, caso ainda não estejam implementadas. A geração do Word, a leitura dos arquivos TXT e HTML e a seleção da pasta do caso deverão funcionar de verdade, permitindo validar o fluxo básico do sistema.
**Critério de aceite:** O MVP será considerado funcional quando o perito conseguir selecionar a pasta do caso, importar e conferir os dados, gerar um laudo Word com a estrutura e os textos esperados, corrigir informações manualmente e salvar o documento sem alterar os arquivos originais, mantendo a revisão e a aprovação final sob sua responsabilidade.
**Dados de exemplo:** O MVP deverá conter uma pasta de caso fictícia, com requisição em PDF (preferencialmente digitalizada), arquivos DEVICE INFO.txt e HASHDOHASH.txt, arquivos HTML com dados de um ou mais cartões SIM, modelo Word institucional, laudo anterior de exemplo, textos padronizados para os exames e exemplos de quesitos e respostas. Todos os dados deverão ser fictícios ou anonimizados, permitindo testar a extração, o preenchimento, a geração do Word e a conferência de erros sem expor informações reais.
**O que já existe pronto e pode ser reaproveitado:** Já existem o modelo Word do laudo pericial, arquivos TXT e HTML utilizados para obter dados dos exames, textos padronizados da Gerência e exemplos de quesitos e respostas. Esses materiais poderão ser reaproveitados no MVP, após organização e validação, sem necessidade de criar tudo do zero. O código Python do gerador ainda precisará ser desenvolvido.
**Dependências:** Modelo Word institucional do laudo; textos padronizados da Gerência; amostras anonimizadas de DEVICE INFO.txt, HASHDOHASH.txt e dos HTML dos SIMs; autorização da chefia para o piloto no computador da Gerência.

## 3. Usuários e papéis

| Papel | Quem é | O que enxerga | O que faz | O que não pode fazer | Registro |
|---|---|---|---|---|---|
| Perito | Profissional responsável pelo exame e pelo laudo | Dados do caso, arquivos importados, textos padronizados e documento gerado | mporta arquivos, confere dados, seleciona e edita textos, responde aos quesitos, revisa e salva o laudo | Aprovar automaticamente conclusões técnicas ou dispensar a própria revisão | Arquivos utilizados, alterações realizadas e data de geração do documento |
| Gerência (chefia) | Gerente responsável pelos textos padronizados | Biblioteca de textos e respostas-modelo | Aprova e versiona os textos padronizados e as respostas-modelo | Alterar laudo de outro perito | Versão e data de aprovação de cada texto |
| Responsável pelos testes | Integrante do grupo que conduz o piloto | Casos fictícios, tempos e correções | Roda os casos de teste e registra tempo e correções | Usar dados reais sem autorização | Planilha de testes do MVP |

**Observações sobre os papéis:** O perito é o único usuário do MVP. A Gerência entra só na aprovação dos textos padronizados, e o responsável pelos testes, só no piloto.

## 4. Dados (entidades e colunas; tudo SINTÉTICO)

| Entidade | O que representa | Colunas | Chave | Volume | Origem | Sintético |
|---|---|---|---|---|---|---|
| CasoPericial | Identificação do caso em elaboração | id_caso: texto, numero_protocolo: texto, data_solicitacao: data, numero_oficio: texto, autoridade_solicitante: texto, numero_processo: texto | id_caso | 1 por laudo | Pasta do caso e PDF | Parcialmente |
| DadosAparelho | Informações do celular examinado | id_aparelho: texto, marca: texto, modelo: texto, imei_1: texto, imei_2: texto, cor: texto | id_aparelho | 1 por laudo no MVP | DEVICE INFO.txt e conferência do perito | Parcialmente |
| CartaoSIM | Informações de cada cartão SIM | id_sim: texto, identificador_objeto: texto, iccid: texto, operadora: texto | id_sim | 0 a vários por laudo | Arquivos HTML das pastas dos objetos | Parcialmente |
| ArquivoHash | Hash do material digital | id_hash: texto, algoritmo: texto, valor_hash: texto | id_hash | 1 ou mais por caso, conforme a regra definida | HASHDOHASH.txt | Parcialmente |
| TextoPadronizado | Textos aprovados para reutilização | id_texto: texto, categoria: texto, titulo: texto, conteudo: texto, versao: texto, ativo: lógico | id_texto | Vários | Biblioteca de textos da Gerência | Parcialmente |
| Quesito | Perguntas apresentadas pela autoridade | id_quesito: texto, id_caso: texto, numero_quesito: inteiro, enunciado: texto, resposta: texto, status_conferencia: texto | id_quesito | 0 a vários por caso | PDF da requisição e revisão do perito | Parcialmente |
| ModeloWord | Modelo usado para gerar o documento | id_modelo: texto, nome: texto, caminho_arquivo: texto, tipo_modelo: texto | id_modelo | 1 ou mais | Template institucional ou Word escolhido pelo perito | Não |
| LaudoGerado | Documento produzido pelo sistema | id_laudo: texto, id_caso: texto, caminho_saida: texto, data_geracao: data_hora, status_revisao: texto | id_laudo | 1 ou mais por caso | Gerador Python | Sim |
| RegistroConferencia | Resultado das conferências automáticas e humanas | id_registro: texto, id_caso: texto, campo_verificado: texto, resultado: texto, observacao: texto, data_hora: data_hora | id_registro | Vários por caso | Sistema e perito | Sim |

**O que precisa ser coletado:** Atualmente, não há registros sistemáticos sobre o tempo gasto na elaboração dos laudos, os erros e retrabalhos. Para avaliar os resultados do MVP, será criada uma planilha para registrar o tempo de elaboração, as correções necessárias, o sucesso da geração e a satisfação dos peritos, utilizando dados fictícios ou anonimizados nos testes iniciais.
**Quem libera o acesso:** O acesso a documentos reais e sistemas institucionais dependerá de autorização da chefia responsável e das áreas competentes, antes do início dos testes com esses dados. O desenvolvimento inicial poderá ocorrer com arquivos fictícios ou anonimizados, sem acesso ao ATENA.

### Fontes de dados do processo real

| Fonte | Tipo | Onde | Existe | Uma linha é | Volume | Campos de data | Atualiza | LGPD |
|---|---|---|---|---|---|---|---|---|
| Requisição pericial | Sistema oficial | Pasta do caso, baixada do ATENA | Sim | Uma requisição | Variável | Data da solicitação; prazo, se disponível | A cada caso | Sim |
| Dados do aparelho | Relatório | Pasta do caso | Sim | Um aparelho | Um por laudo no MVP | Não identificado | A cada exame | Sim |
| Dados dos cartões SIM | Relatório | Subpastas OBJ 01-A, OBJ 01-B etc. | Sim | Um cartão SIM | Zero ou vários por caso | Não identificado | A cada exame | Sim |
| Hash dos arquivos | Relatório | Pasta do caso | Sim | Um registro de hash | Variável | Não identificado | A cada exame | Duvidaso |
| Modelo de laudo | Documento em papel | Arquivo institucional ou pasta local | Sim | Um modelo | Um ou mais | Não se aplica | Quando houver alteração | Duvidaso |
| Textos padronizados | Documento em papel | Arquivo local da Gerência | Sim | Um texto padronizado | Variável | Não se aplica | Quando houver revisão | Duvidaso |
| Controle de tempo de elaboração | Não existe ainda | A definir | Não | Um laudo acompanhado | Ainda não levantado | Início, fim e duração da elaboração | A cada laudo acompanhado | Duvidaso |
| Registro de testes do MVP | Não existe ainda | A criar no projeto | Não | Um teste de geração | A definir | Data, duração e resultado do teste | A cada teste | Não |


## 5. Regras de negócio (RN01, RN02...)

| ID | Regra | Quando se aplica | Exceção | Quem valida | Tipo |
|---|---|---|---|---|---|
| RN01 | O sistema deve permitir selecionar a pasta do caso criada pelo perito. | Início do processo | Nenhuma | Sistema | Validação |
| RN02 | O sistema deve verificar a existência dos arquivos necessários antes de iniciar a geração. | Importação dos arquivos | Arquivo ausente pode ser informado manualmente, quando possível | Sistema e perito | Validação |
| RN03 | Os IMEIs e ICCIDs devem ser tratados como texto, preservando todos os dígitos. | Leitura e preenchimento dos dados | Nenhuma | Sistema | Validação |
| RN04 | Os dados extraídos automaticamente devem ser apresentados ao perito para conferência antes da geração do laudo. | Após a extração | Dados não extraídos podem ser preenchidos manualmente | Perito | Negócio |
| RN05 | Cada laudo do MVP deve corresponder a um único aparelho celular. | Montagem do documento | Outros tipos de exame ficam fora do MVP | Perito | Negócio |
| RN06 | O sistema deve permitir nenhum, um ou vários cartões SIM, conforme os arquivos disponíveis. | Descrição dos objetos | Na ausência de SIM, a descrição deve refletir essa condição após confirmação do perito | Perito | Negócio |
| RN07 | Cada cartão SIM deve ser associado ao identificador correto do objeto, como 01-A ou 01-B. | Leitura dos arquivos HTML | Dados ambíguos exigem conferência manual | Perito | Validação |
| RN08 | O sistema deve inserir somente textos padronizados compatíveis com as opções selecionadas e os dados confirmados. | Montagem do laudo | O perito pode editar ou redigir o texto manualmente | Perito | Negócio |
| RN09 | Os quesitos devem ser numerados sequencialmente e associados às respectivas respostas. | Montagem da seção de quesitos | Quesitos não identificados automaticamente devem ser inseridos ou corrigidos manualmente | Perito | Validação |
| RN10 | O sistema não deve elaborar nem aprovar conclusões técnicas de forma autônoma. | Elaboração e revisão do laudo | Nenhuma | Perito | Negócio |
| RN11 | O sistema deve alertar sobre campos obrigatórios vazios ou inconsistentes antes de gerar a versão final. | Conferência automática | O perito pode corrigir os dados e repetir a conferência | Sistema e perito | Validação |
| RN12 | O documento gerado deve preservar a estrutura e a formatação do modelo escolhido, dentro das limitações técnicas identificadas. | Geração do Word | Ajustes de formatação podem exigir intervenção manual | Perito | Validação |
| RN13 | O sistema deve salvar o novo laudo em arquivo separado, sem sobrescrever o modelo ou laudo anterior. | Salvamento | Sobrescrita somente mediante ação explícita e controlada, se futuramente permitida | Perito | Negócio |
| RN14 | O laudo somente será considerado finalizado após a revisão e validação do perito. | Encerramento do processo | Nenhuma | Perito | Negócio |
| RN15 | O MVP deve funcionar localmente, sem conexão automática com o ATENA. | Em todas as etapas | Integrações futuras dependem de avaliação e autorização específicas | Responsável pelo projeto | Acesso |
| RN16 | Os testes iniciais devem utilizar dados fictícios ou documentos devidamente anonimizados. | Desenvolvimento e testes | Uso de dados reais depende das autorizações e regras institucionais aplicáveis | Responsável pelos testes | LGPD |


## 6. Telas (#/painel, #/lista...)

| Rota | Tela | Objetivo | Quem usa | Dados | Ação | Regra | Tipo | Verificável como | MVP |
|---|---|---|---|---|---|---|---|---|---|
| #/inicio | Tela principal | Iniciar a elaboração do laudo | Perito | Opções de arquivo e modelo | Iniciar novo laudo | Permitir selecionar modelo institucional ou laudo anterior | Tela | Abrir a tela e iniciar um caso | Sim |
| #/arquivos | Seleção de arquivos | Reunir os dados do exame | Perito | PDF, TXT e HTML | Selecionar arquivos | Não avançar sem os arquivos obrigatórios | Tela | Importar arquivos de teste | Sim |
| (automação) | Extração de dados | Identificar informações nos arquivos | Sistema | Dados da requisição, aparelho, IMEIs, hash e cartões SIM | Extrair dados | Permitir correção manual quando a extração falhar | Automação | Comparar dados extraídos com os originais | Sim |
| #/dados | Conferência dos dados | Evitar erros de preenchimento | Perito | Dados extraídos e campos editáveis | Confirmar ou corrigir | Exigir conferência dos identificadores essenciais | Tela | Corrigir um dado e confirmar o resultado | Sim |
| #/textos | Seleção de textos padronizados | Padronizar a redação | Perito | Textos para descrição dos objetos e exames | Selecionar e adaptar textos | Permitir edição e redação manual quando necessário | Tela | Selecionar um texto e verificar sua inserção | Sim |
| #/quesitos | Quesitos e respostas | Organizar perguntas e respostas | Perito, com apoio do sistema | Quesitos identificados e respostas sugeridas | Conferir e editar respostas | Não aprovar respostas técnicas automaticamente | Tela | Conferir numeração e edição dos quesitos | Sim |
| #/gerar | Geração do laudo Word | Montar o documento completo | Sistema | Dados confirmados e textos selecionados | Gerar documento | Preservar a estrutura e a formatação do modelo escolhido | Automação | Abrir o Word gerado e conferir as seis seções | Sim |
| #/gerar | Conferência automática | Identificar omissões e inconsistências | Sistema | Campos obrigatórios e dados do documento | Executar validação | Alertar sobre campos vazios ou divergentes | Automação | Testar com dados faltantes e inconsistentes | Sim |
| #/revisao | Revisão final | Garantir a validação humana | Perito | Laudo completo | Revisar e corrigir | A aprovação técnica é responsabilidade do perito | Documento | Conferir o laudo e registrar as correções necessárias | Sim |
| #/revisao | Salvamento do laudo | Armazenar a versão final | Perito | Documento revisado | Salvar arquivo | Não sobrescrever automaticamente o laudo anterior | Ação | Salvar e conferir que o laudo anterior não foi sobrescrito | Sim |


## 7. KPIs (nome = fórmula em uma linha)

| KPI | Pergunta | Fórmula | Fonte | Linha de base | Valor esperado | Como medir |
|---|---|---|---|---|---|---|
| Tempo de elaboração do laudo | O sistema reduz o tempo de elaboração? | Tempo final − tempo inicial | Registro de testes e controle de tempo | A MEDIR | Redução de 30% | Cronometrar a elaboração manual de laudos comparáveis |
| Taxa de correções após geração | O sistema reduz erros e retrabalho? | (Laudos que exigiram correção ÷ total de laudos) × 100 | Registro de testes e conferência dos laudos | A MEDIR | Redução de 30% | Registrar correções necessárias em laudos manuais e gerados pelo MVP |

**Período da linha de base:** Período da linha de base: duas semanas, com coleta do tempo de elaboração e das correções necessárias nos laudos produzidos manualmente.

Volume: a definir conforme a quantidade de casos disponíveis no período. Se possível, utilizar os mesmos casos ou casos fictícios equivalentes na comparação com o MVP, garantindo condições semelhantes de avaliação.
**Campos de data e tempo que existem:** Nos arquivos atuais, existe a possibilidade de identificar a data da solicitação na requisição pericial, mas não foram confirmados campos que registrem o início e o término da elaboração do laudo.

Para medir o tempo de execução, será necessário registrar manualmente a data e hora de início e de conclusão de cada laudo em uma planilha de controle. Assim, será possível comparar o tempo de elaboração antes e depois do uso do MVP.

## 8. Stack: HTML único (CSS/JS inline), dados em JSON embutido, GitHub Pages.

**Stack escolhida:** HTML único (CSS/JS inline), dados em JSON embutido, GitHub Pages
**Detalhe da stack:** Um único arquivo index.html (HTML, CSS e JS embutidos) aberto no Edge ou no Chrome, sem instalação. Bibliotecas embutidas: pdf.js (ler o PDF), PizZip e docxtemplater (preencher o modelo .docx). Dados no IndexedDB do navegador e backup em .json. O grupo propôs Python; a troca evita a instalação no computador institucional.
**Hospedagem:** Arquivo HTML único, aberto no Edge ou no Chrome do computador da Gerência, sem servidor e sem instalação. A opção do grupo era aplicativo instalado no Windows.
**Custo e licenças:** Orçamento previsto: baixo ou sem custo adicional no MVP, utilizando Python e bibliotecas gratuitas ou de código aberto. Poderá haver custos com licença do Microsoft Word, caso não exista licença institucional disponível, e com suporte técnico, instalação ou implantação futura. O desenvolvimento e os testes iniciais serão realizados localmente, sem custos de hospedagem ou domínio.
**Contas e domínio:** Conta e acesso: no MVP, não será necessária conta em plataforma externa, domínio ou hospedagem. O aplicativo será executado localmente no Windows, pelo perito responsável.

Implantação futura: caso seja disponibilizado para outros usuários, a criação de contas, a definição de acessos e eventual hospedagem em servidor deverão ser avaliadas e autorizadas pela instituição, com apoio da equipe de TI.

| Opção | Tipo | Onde roda | Custo | Quem mantém | Acesso | Banco de dados | Escala | Limitação |
|---|---|---|---|---|---|---|---|---|
| Arquivo HTML único (offline first) | Arquivo local | Edge ou Chrome do computador da Gerência | Zero | Grupo do projeto | Perito que abre o arquivo | IndexedDB do navegador | Um perito por computador | Os dados ficam no computador; backup por arquivo .json |
| Arquivo local | Arquivo local | Pasta do computador | Baixo | Desenvolvedor | Um usuário por vez | Não necessário no MVP | Baixa | Depende do computador e da instalação local |
| Aplicativo instalado | Aplicativo instalado | Computador Windows | Baixo a moderado | Desenvolvedor e suporte de TI | Usuários autorizados por instalação | Não necessário no MVP | Média | Atualizações e instalações precisam ser gerenciadas |
| Servidor interno | Servidor interno | Infraestrutura da instituição | A definir | Equipe de TI institucional | Conforme permissões | Opcional | Alta | Depende de aprovação, infraestrutura e manutenção institucional |


## 9. Restrições e LGPD

**Restrições:** O MVP deverá funcionar localmente em computadores Windows, sem conexão automática com o ATENA. O desenvolvimento está limitado ao tempo disponível e à necessidade de manter a estrutura e a formatação do modelo oficial de laudo. O uso de dados reais depende das autorizações e normas institucionais aplicáveis. A extração de informações de PDFs digitalizados por OCR poderá exigir correção manual, e todo laudo gerado deverá passar pela conferência e aprovação final do perito.
**Dados pessoais tratados:** O MVP poderá tratar dados pessoais presentes na requisição pericial e no laudo, como nomes de autoridades e peritos, além de números de processos e outras informações de identificação eventualmente presentes nos documentos. Também poderá processar identificadores técnicos dos aparelhos, como IMEIs e ICCIDs. Os testes iniciais utilizarão dados fictícios ou anonimizados. O sistema deverá limitar o acesso aos arquivos, evitar armazenamento desnecessário e observar a LGPD e as normas institucionais aplicáveis.
**Base legal:** Finalidade: auxiliar na elaboração e conferência de laudos periciais, reduzindo o tempo de produção e os erros humanos, contribuindo para o cumprimento dos prazos.  Base legal: deverá ser validada pela instituição conforme a LGPD (arts. 7º e 23). Como referência, o art. 465 do CPC prevê que o juiz fixe o prazo para entrega do laudo pericial.  Os testes utilizarão dados fictícios ou anonimizados. O uso de dados reais seguirá as normas institucionais aplicáveis.
**Retenção:** Prazo de retenção: os arquivos utilizados pelo MVP serão mantidos apenas pelo tempo necessário à geração e conferência do laudo. Após isso, eventuais cópias temporárias deverão ser eliminadas, respeitando as normas institucionais e os prazos oficiais de guarda documental, conforme os arts. 15 e 16 da LGPD
**Acesso e registro:** Quem acessa: inicialmente, apenas o perito responsável, em ambiente local. O acesso por outros usuários dependerá de autorização institucional.

Registro: o sistema poderá registrar a data e hora de geração do laudo, os arquivos utilizados, as conferências realizadas e o status da revisão final, sem armazenar dados desnecessários. O acesso aos arquivos deverá seguir as normas institucionais de segurança e a LGPD, especialmente os arts. 37 e 46
**Requisitos marcados:** Funcionar offline, Impressão em formato oficial, LGPD e dado pessoal, Trilha de auditoria

---

# Anexo A — AS-IS (o fluxo de hoje)

**Início:** Envio do Ofício Requisitório pela autoridade requisitante
**Fim:** Entrega do Laudo
**Entradas:** Informações do cadastro, da Requisição de Perícia, os relatórios da extração dos dispositivos
**Saídas:** Laudo Pericial assinado
**Volume:** 40
**Duração:** 200
**Frequência:** Mensal
| Etapa | Quem faz | O que entra | Ação | O que sai | Sistema | Regra | Onde espera | Tempo (h) | Automatizável |
|---|---|---|---|---|---|---|---|---|---|
| Obter a requisição | Perito | Requisição do exame | Baixa a requisição em PDF no ATENA e salva na pasta do protocolo | PDF da requisição organizado | ATENA e computador | Identificar o protocolo correto | Não identificado | A medir | Pouco |
| Organizar os arquivos | Perito | Pastas do exame, arquivos TXT, HTML e PDF | Confere e organiza os arquivos necessários à elaboração do laudo | Arquivos disponíveis para consulta | Explorador de arquivos | Verificar se os arquivos necessários estão disponíveis | Possível, se houver arquivos faltantes | A medir | Sim, com apoio humano |
| Consultar os dados do aparelho | Perito | DEVICE INFO.txt | Consulta marca, modelo e IMEIs do celular | Dados do aparelho identificados | Arquivo TXT | Conferir e corrigir dados, se necessário | Possível, se houver divergências | A medir | Sim, com apoio humano |
| Consultar o hash | Perito | HASHDOHASH.txt | Localiza e confere o valor SHA-256 | Hash identificado | Arquivo TXT | Conferir se o valor corresponde ao arquivo do exame | Possível, se houver inconsistência | A medir | Sim, com apoio humano |
| Consultar dados dos cartões SIM | Perito | Arquivos HTML das pastas OBJ 01-A, OBJ 01-B etc. | Consulta ICCID e operadora de cada cartão SIM | Dados dos cartões SIM identificados | Arquivos HTML | Verificar quantos cartões SIM existem | Possível, se houver arquivos faltantes | A medir | Sim, com apoio humano |
| Reutilizar um laudo anterior | Perito | Laudo anterior em Word ou modelo institucional | Abre, renomeia e utiliza o documento como base | Documento inicial para o novo laudo | Microsoft Word | Escolher um documento adequado e preservar o modelo | Não identificado | A medir | Sim, com apoio humano |
| Preencher os dados iniciais | Perito | Requisição e dados dos arquivos | Transfere manualmente os dados para o Word | Laudo com dados iniciais preenchidos | Microsoft Word | Conferir números, datas, nomes e demais identificadores | Não identificado | A medir | Sim, com apoio humano |
| Elaborar a descrição dos objetos | Perito | Dados do celular, envelope de segurança e cartões SIM | Redige ou adapta a descrição dos objetos examinados | Seção de descrição dos objetos | Microsoft Word e textos de referência | Adequar a descrição aos objetos efetivamente recebidos | Não identificado | A medir | Sim, com apoio humano |
| Elaborar a seção dos exames | Perito | Informações do exame e textos padronizados | Seleciona e adapta os textos relativos aos procedimentos realizados | Seção dos exames preenchida | Microsoft Word e arquivo de textos padronizados | Selecionar o texto compatível com a situação real | Não identificado | A medir | Sim, com apoio humano |
| Elaborar a seção de anexos | Perito | Hash e informações dos arquivos digitais | Preenche a seção e as tabelas de anexos | Seção de mídias e anexos preenchida | Microsoft Word | Conferir os dados dos arquivos apresentados | Não identificado | A medir | Sim, com apoio humano |
| Responder aos quesitos | Perito | Quesitos da autoridade e textos de respostas padronizadas | Transcreve os quesitos e elabora ou adapta as respostas | Quesitos numerados e respondidos | PDF da requisição, eventualmente ATENA, e Word de referência | A resposta deve corresponder ao quesito e aos resultados do exame | Não identificado | A medir | Sim, com apoio humano |
| Elaborar as considerações | Perito | Informações específicas do caso | Redige ou adapta as considerações finais | Seção de considerações preenchida | Microsoft Word | Manter conclusões compatíveis com os resultados periciais | Não identificado | A medir | Sim, com apoio humano |
| Revisar o laudo | Perito | Documento Word preenchido | Confere dados, textos, quesitos, formatação e possíveis omissões | Laudo revisado | Microsoft Word | Corrigir erros antes da finalização | Se houver necessidade de correções | A medir | Sim, com apoio humano |
| Salvar a versão final | Perito | Laudo revisado | Salva o documento final na pasta correspondente | Laudo pericial em Word finalizado | Computador e Microsoft Word | Confirmar nome e local de salvamento | Não identificado | A medir | Sim, com apoio humano |

**Decisões e aprovações:** Durante a elaboração do laudo, o perito verifica se todos os arquivos necessários estão disponíveis e se os dados extraídos estão corretos, realizando correções manuais quando necessário. Em seguida, seleciona os textos padronizados adequados à situação do exame e confere se os quesitos foram respondidos de acordo com os resultados periciais. Ao final, revisa o laudo completo. Se identificar erros ou informações faltantes, realiza as correções e revisa novamente. Se estiver correto e completo, aprova o documento e salva a versão final.
**Exceções:** Se houver falhas na leitura do PDF, arquivos ausentes ou dados inconsistentes, o perito deverá corrigir ou inserir as informações manualmente. Na ausência de cartão SIM ou de texto padronizado adequado, o sistema adaptará o documento ou permitirá o preenchimento manual. Erros identificados na revisão deverão ser corrigidos antes da aprovação final.
**Já digitalizado:** A digitação é no sistema/computador

# Anexo B — TO-BE (o fluxo depois da mudança)

**Visão do futuro:** Quando esse processo existir, os peritos deixarão de elaborar manualmente laudos de exames periciais menos complexos e passarão a gerar documentos padronizados com mais agilidade, reduzindo erros humanos e retrabalho, mantendo a revisão e a validação técnica sob sua responsabilidade.
**Mudança principal:** Substituir o preenchimento manual e repetitivo dos laudos por uma geração automatizada de documentos Word a partir de dados e textos padronizados, com conferência e validação final pelo perito.
**O que fica igual:** A responsabilidade técnica do perito, a análise dos vestígios, a interpretação dos resultados, a elaboração das conclusões e a revisão e validação final do laudo permanecem inalteradas, assim como os procedimentos e padrões institucionais vigentes.
**O que não pode mudar:** Devem ser preservadas as normas legais e institucionais aplicáveis à atividade pericial, os procedimentos oficiais, a integridade e a rastreabilidade das informações e a responsabilidade exclusiva do perito pela análise técnica, pelas conclusões e pela validação final do laudo. A automação deverá apenas auxiliar na elaboração documental, sem substituir o julgamento técnico ou alterar atribuições legais.
| Etapa | O que muda | Quem executa | Benefício | Esforço |
|---|---|---|---|---|
| Selecionar os arquivos do caso | O perito seleciona a requisição e os arquivos já produzidos durante o exame. | A pessoa assistida pela máquina | Centralização das informações | Baixo |
| Extrair dados dos arquivos | O sistema lê o PDF por OCR e identifica dados nos arquivos TXT e HTML. | A máquina (automação) | Redução de digitação manual | Alto |
| Conferir os dados extraídos | O perito verifica e corrige os dados identificados pelo sistema. | A pessoa assistida pela máquina | Prevenção de erros humanos | Médio |
| Selecionar o documento-base | O perito escolhe o modelo institucional ou um laudo anterior em Word. | A pessoa assistida pela máquina | Aproveitamento de documentos existentes | Baixo |
| Montar a descrição dos objetos | O sistema organiza os dados do celular e dos cartões SIM conforme as informações disponíveis. | A pessoa assistida pela máquina | Padronização e agilidade | Médio |
| Inserir textos dos exames | O sistema sugere ou insere textos padronizados conforme as opções selecionadas pelo perito. | A pessoa assistida pela máquina | Menos retrabalho na redação | Médio |
| Organizar quesitos e respostas | O sistema identifica e numera os quesitos e auxilia na seleção das respostas padronizadas. | A pessoa assistida pela máquina | Melhor organização e menor esforço repetitivo | Alto |
| Gerar o documento Word | O sistema preenche e formata o laudo, preservando o documento-base escolhido quando aplicável. | A máquina (automação) | Redução do tempo de elaboração | Médio |
| Executar conferência automática | O sistema verifica campos vazios, dados inconsistentes e itens obrigatórios ausentes. | A máquina (automação) | Identificação antecipada de falhas | Médio |
| Revisar e validar o laudo | O perito confere o conteúdo, os resultados técnicos, as respostas e a formatação. | A pessoa, sem mudança | Manutenção da responsabilidade técnica | Médio |
| Corrigir e gerar a versão final | O perito solicita ou realiza ajustes e salva a versão final aprovada. | A pessoa assistida pela máquina | Menos erros e maior eficiência | Baixo |

**Piloto do TO-BE:** Testar em computador da Gerência, com autorização, utilizando cópias de laudos e arquivos de exames concluídos, preferencialmente anonimizados, para avaliar a precisão dos dados, a formatação do Word, a redução do tempo de elaboração e a necessidade de correções, sem conexão automática com o ATENA.

# Anexo C — Pesquisa, riscos e plano

**Hipótese de campo:** A elaboração manual de laudos periciais menos complexos consome tempo com tarefas repetitivas e aumenta o risco de erros e retrabalho, podendo ser reduzida com a geração automatizada de documentos e a revisão final pelo perito.
| Referência | Tipo | Fonte ou link | Ano | Dado que extrai | Como usar na defesa | Link conferido |
|---|---|---|---|---|---|---|
| Código de Processo Civil, art. 465 | Norma ou lei | Lei nº 13.105/2015, Planalto | 2015 | O juiz fixa o prazo para entrega do laudo pericial | Justificar a organização da elaboração dos laudos e o cumprimento dos prazos | Sim |
| Lei Geral de Proteção de Dados | Norma ou lei | Lei nº 13.709/2018, Planalto | 2018 | Princípios e regras para o tratamento de dados pessoais | Fundamentar os cuidados com documentos, identificadores e informações tratados pelo app | Sim |
| Código de Processo Penal, arts. 158-A a 158-F (cadeia de custódia) | Norma ou lei | Decreto-Lei nº 3.689/1941, com a redação da Lei nº 13.964/2019, Planalto | 2019 | Registro e rastreabilidade do vestígio, incluindo o material digital | Justificar a conferência obrigatória do hash e dos identificadores no laudo | Não |

**Lacunas:** A pesquisa ainda não identificou dados quantitativos sobre o tempo médio de elaboração de laudos na Gerência, nem estudos que comprovem a redução de tempo e erros com esta solução específica. Será necessário medir o processo atual, testar o MVP com casos fictícios ou anonimizados e verificar os requisitos institucionais de segurança, autorização e compatibilidade com o modelo oficial de laudo.
| Marco | Data | Responsável | Depende de | Situação |
|---|---|---|---|---|
| 1. Consolidar requisitos e escopo do MVP | A definir | Idealizador do projeto | Conclusão do planejamento | Em andamento |
| 2. Reunir modelo Word e textos padronizados fictícios ou autorizados | A definir | Idealizador do projeto | Disponibilidade dos arquivos | Planejado |
| 3. Desenvolver a leitura dos arquivos TXT e HTML | A definir | Desenvolvedor | Requisitos definidos | Planejado |
| 4. Implementar a geração do laudo em Word | A definir | Desenvolvedor | Modelo Word definido | Planejado |
| 5. Implementar OCR e conferência dos dados extraídos | A definir | Desenvolvedor | Amostras fictícias de PDF | Planejado |
| 6. Testar o sistema com casos fictícios ou anonimizados | A definir | Idealizador e peritos participantes | MVP funcional | Planejado |
| 7. Medir tempo, correções e resultados do piloto | A definir | Idealizador e peritos participantes | Testes concluídos | Planejado |
| 8. Documentar resultados e propor próximos passos | A definir | Idealizador do projeto | Análise dos resultados | Planejado |

| Risco | Probabilidade | Impacto | Mitigação |
|---|---|---|---|
| Falhas na extração de dados por OCR | Alta | Médio | Exigir conferência e correção manual dos dados extraídos. |
| Erros na leitura dos arquivos TXT e HTML | Média | Alto | Validar os campos e alertar sobre informações ausentes ou inconsistentes. |
| Alteração da formatação do modelo oficial Word | Média | Alto | Testar a geração e comparar o documento com o modelo institucional. |
| Inserção de texto padronizado inadequado | Média | Alto | Permitir seleção e edição pelo perito antes da finalização. |
| Exposição de dados pessoais ou periciais | Baixa | Alto | Usar dados fictícios ou anonimizados nos testes e manter os arquivos em ambiente local protegido. |
| Indisponibilidade de tempo para desenvolvimento | Média | Médio | Priorizar as funcionalidades essenciais do MVP e desenvolver por etapas. |
| Geração de laudo com informações incorretas | Média | Alto | Implementar validações obrigatórias e exigir revisão e aprovação final do perito. |
| Dificuldade de instalação ou execução em computadores institucionais | Média | Médio | Validar os requisitos com a equipe de TI antes de uma implantação institucional. |

**Apoio necessário:** Chefia da Gerência: autorizar o piloto e aprovar os textos padronizados. TI: confirmar que o Edge do computador institucional permite abrir a pasta do caso (File System Access API). Peritos participantes: medir a linha de base e testar o MVP.
**Aprendizado necessário:** Para executar o projeto, preciso aprender e praticar Python básico, leitura de arquivos PDF, TXT e HTML, extração de texto por OCR, geração e formatação de documentos Word com Python, validação de dados e criação de uma interface simples para Windows. Também preciso aprender a testar o sistema, tratar erros e aplicar boas práticas de segurança e proteção de dados. O desenvolvimento será gradual, começando pela leitura dos arquivos e geração do Word, avançando depois para OCR e funcionalidades mais complexas.

# Anexo D — A defesa

**Frase de defesa:** Se o tempo médio de elaboração dos laudos for reduzido em 30% em relação à linha de base medida, os peritos deixarão de gastar tanto tempo com preenchimentos repetitivos, reduzindo o retrabalho sem abrir mão da revisão técnica final.
**Provas:** 1. Processo atual: a elaboração manual exige reunir dados de diferentes arquivos, preencher o Word e adaptar textos padronizados, gerando tarefas repetitivas e possibilidade de erros.

2. Viabilidade técnica: já existem arquivos TXT, HTML e modelos Word que podem servir de base para automatizar parte do preenchimento e da geração dos laudos.

3. Validação por métricas: o piloto comparará o tempo de elaboração e a necessidade de correções antes e depois do MVP, verificando se a redução de 30% no tempo é alcançável.
**Piloto:** O MVP será testado com casos fictícios ou anonimizados, comparando a elaboração manual com a geração automatizada. Serão medidos o tempo gasto, a quantidade de correções necessárias e a qualidade da formatação do Word. Os resultados serão analisados para verificar se o sistema reduz o tempo em pelo menos 30%, mantendo a precisão das informações e a revisão técnica final pelo perito.
**Maior risco:** O maior risco é a geração de laudos com informações incorretas ou formatação inadequada, comprometendo a confiabilidade do documento. Para mitigá-lo, o MVP será testado com dados fictícios ou anonimizados, incluirá validações dos campos obrigatórios e exigirá a conferência e aprovação final do perito antes da utilização do laudo.

# Anexo E — Documentos enviados

**Descrição dos documentos:** Tabelas do fluxo AS-IS, do TO-BE, das telas, das entidades, das regras, das fontes, das métricas, da hospedagem, das referências e dos marcos. O conteúdo foi movido para as tabelas do formulário.
**O que ainda falta:** Modelo Word com os marcadores; amostras anonimizadas de DEVICE INFO.txt, HASHDOHASH.txt e dos HTML dos SIMs; requisição em PDF fictícia (com texto e digitalizada); textos padronizados sem dados pessoais.
