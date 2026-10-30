# Premissas dos apps (elucubração para não parar o desenvolvimento)

> Documento de referência da fase de ideação. Cada item do Sprint 0 que dependia de
> decisão institucional, documento oficial ou medição do processo real foi
> **assumido** com um valor plausível, para que o app continue sendo construído e
> testável. A lista abaixo diz o que foi assumido, onde a premissa aparece no app e
> o que precisa ser confirmado com quem responde pelo processo.
>
> **Regra do curso**: nada aqui é verdade institucional. Dado do app é fictício.
> Quando a informação oficial chegar, troca-se o valor na fonte (gerador de
> dados ou `src/*.js`), reconstrói o app e o teste correspondente é ajustado.
>
> **O que deixou de ser premissa em 30/10/2026**: as categorias da Comissão de
> Ética estão ancoradas na **LC nº 112/2002-MT** (texto real, com artigo e
> trecho) e o fluxo de aquisições está ancorado na **Lei nº 14.133/2021**. Nesses
> dois casos, a norma é real; só os prazos em dias e a divisão em etapas
> continuam sendo elucubração.
>
> **Nível de confiança** usado em cada premissa:
> - **A** — o app já funciona com essa premissa; a confirmação só ajusta detalhe.
> - **B** — a premissa afeta cálculo ou tela; trocar exige revisar o código.
> - **C** — a premissa define o escopo; se estiver errada, muda o que o app é.

Atualizado em **30/10/2026**. Ver também [CONTINUAR.md](CONTINUAR.md) (próximo
passo de cada app) e o `sprint.md` de cada app (itens do Sprint 0).

---

## 1. Controle de Adiantamentos (`adiantamento`)

| Item do Sprint 0 | Premissa assumida | Onde aparece | Nível | O que confirmar |
|---|---|---|---|---|
| Validar as 12 etapas da tabela AS-IS com a DAS e a contabilidade | As 12 etapas do app são a tabela AS-IS validada: solicitar dotação, análise da DAS, análise da contabilidade, levantamento de orçamentos, dotação (NGER), aprovação da chefia, autorização do ordenador, cadastro no SICAD, aplicação do recurso, pagamento, prestação de contas, encerrado | `exemplos/gerar_exemplos.py` (lista `ETAPAS`), store `etapas` | A | A ordem e os nomes oficiais das etapas |
| Confirmar qual Orientação Técnica da CGE/MT vale (02/2026 ou 06/2025) | Vale a **OT CGE/MT nº 06/2025**, por ser a mais recente já vigente no momento do desenho; a 02/2026 fica como revisão | `contexto.md`, regra do pedido de prorrogação | C | Qual OT está vigente na data da publicação |
| Anexar os documentos citados (AS-IS e TO-BE em .docx, planilha de controle) | A tabela AS-IS vira `modelos/tabela-as-is.md` e a planilha de controle vira `exemplos/planilha-controle.csv`, ambos fictícios | `modelos/`, `exemplos/` | A | Os arquivos reais das unidades |
| Acrescentar os feriados de MT e do município (Cuiabá) | A lista tem 24 feriados: os **20 nacionais** de 2026 e 2027, o **Corpus Christi** (ponto facultativo estadual de MT) e o **aniversário de Cuiabá** (municipal). **No prazo entram só os nacionais e o estadual**, porque o recurso é federal; o municipal fica na lista marcado como `escopo: "municipal"` | store `feriados` (`escopo`), `exemplos/gerar_exemplos.py` | B | Se o Modesc conta o feriado municipal |
| Linha de base: datas dos pedidos de 4 semanas | 10 processos de exemplo com entrada entre agosto e outubro de 2026, tempo médio de 21 dias da solicitação ao pagamento | store `processos`, `exemplos/gerar_exemplos.py` | B | As datas reais das 4 semanas |

## 2. Agendamento CIN (`agendamento-cin`)

| Item do Sprint 0 | Premissa assumida | Onde aparece | Nível | O que confirmar |
|---|---|---|---|---|
| Pedir à TI autorização para publicar no Apps Script com a conta institucional | A publicação acontece em **script.google.com** com a conta institucional da POLITEC, e o app não fica no repositório público do jeito que os outros | `DEPLOY.md`, `appsscript.json`, `Code.gs` | A | A TI libera a conta e o domínio institucional |
| Aprovar com a gestão as regras RN06 a RN10 | RN06 um agendamento ativo por posto; RN07 cancelar até 2 h antes; RN08 tolerância de 15 min; RN09 antecedência de 1 a 30 dias; RN10 retenção de 90 dias | `src/app.js` (RN06 a RN10), `sprint.md` | A | A gestão aprova os números |
| Escolher os postos do piloto e levantar a grade real | **2 postos**: Posto de Identificação Centro (Cuiabá) e Posto de Identificação Várzea Grande. Grade de 10 dias úteis, 16 slots de 30 minutos (8 h a 12 h e 13 h a 17 h), **2 vagas por horário** | store `postos`, `horarios`, `planilha-modelo/seed.json` | B | Os postos, os dias e as vagas reais |
| Medir a linha de base no posto do piloto | 1 marcação leva **4 minutos**; o volume mensal é de 1.200 marcações no posto. O exemplo traz 30 agendamentos com a fila de espera | `planilha-modelo/seed.json`, store `agendamentos` | B | O tempo real por marcação |
| Confirmar o nome completo do aluno no formulário | O formulário exige **nome completo** do aluno, porque a emissão da segunda via exige identificação do beneficiário | `src/app.js` (campo de nome) | A | Se o cadastro do aluno usa nome completo ou só matrícula |

## 3. Agiliza Mais (`agiliza-mais`)

| Item do Sprint 0 | Premissa assumida | Onde aparece | Nível | O que confirmar |
|---|---|---|---|---|
| Conferir com o perito o formato real dos TXT e HTML | Os formatos do app são os de Android 11 e 12: `DEVICE INFO.txt`, `HASHDOHASH.txt` e `HTML do SIM`; o app lê e mostra o que encontrou, sem exigir todos | `exemplos/FORMATOS.md`, `src/app.js` | A | O formato de cada aparelho em uso |
| Copiar o modelo institucional para `modelos/modelo-laudo-celular.docx` | O modelo do laudo celular tem as seções: identificação do aparelho, IMEIs, SIMs, hash e assinaturas | `modelos/modelo-laudo-celular.docx`, `modelos/MARCADORES.md` | A | O modelo institucional verdadeiro |
| Reunir os textos padronizados da Gerência | 11 textos padronizados (histórico, conclusão, laudo e outros) no store `textos`, com o conteúdo de cada um. A classificação por quesitos fica no app, não no seed | store `textos`, `exemplos/textos.json` | A | Os textos oficiais da Gerência |
| Criar a planilha da linha de base | 3 casos fictícios com inventário completo (aparelhos, SIMs e hashes), com o tempo de conferência | `exemplos/caso-ficticio-001..003` | B | Os números reais de 1 mês |

## 4. Segunda via da CIN (`cin-segunda-via`)

| Item do Sprint 0 | Premissa assumida | Onde aparece | Nível | O que confirmar |
|---|---|---|---|---|
| Confirmar as regras oficiais da segunda via | O pedido online é admitido quando a **primeira via da CIN ainda está válida** e **nenhum dado mudou** (nome, estado civil, filiação). Com dado alterado, o cidadão vai ao posto. O app não trata "cadastro com menos de 15 dias" como regra de elegibilidade | `src/app.js` (RN03, `elegivel`), `contexto.md` | B | As regras de dispensa e os prazos do cadastro |
| Indicar a fonte dos números (15 dias, 21.000 por mês) | 15 dias é a **validade do cadastro no posto** (o app mostra a validade da CIN); 21.000 por mês é o **volume de emissões no estado** | `contexto.md`, painel | B | A fonte oficial dos dois números |
| Fotos de teste geradas (sem pessoas reais) | As fotos do exemplo são imagens sintéticas, geradas no `exemplos/gerar_exemplos.py`, com 3 fotos por pedido | store `fotos`, `exemplos/gerar_exemplos.py` | A | Nenhuma (dado fictício por definição) |
| Conversa com a TI sobre a integração com a coleta biométrica | **Não há integração**: o app é um protótipo offline, e o registro do atendimento é feito à mão no sistema oficial. A posição fica registrada em `contexto.md` | `contexto.md`, `README.md` | C | A TI confirma que não há API no curto prazo |

## 5. Comissão de Ética (`comissao-etica-denuncias`)

| Item do Sprint 0 | Premissa assumida | Onde aparece | Nível | O que confirmar |
|---|---|---|---|---|
| Conferir com a Comissão as categorias, os artigos do Código de Ética e as palavras | **Resolvido com a norma**: as 8 categorias estão ancoradas na **LC nº 112/2002-MT** (Código de Ética Funcional do Servidor Público Civil do Estado), com o **artigo e o texto** de cada uma. O texto foi consultado em 30/10/2026 no acervo do [ctresb/leis](https://github.com/ctresb/leis), fonte oficial da ALMT. Cada categoria guarda `artigos` e `texto_artigo`, que aparecem na tela de classificação e são editáveis em `#/config` | store `categorias`, `src/sprint3.js`, `modelos/codigo-etica-lc112-2002.md` | B | A Comissão conferir se as 8 categorias cobrem a prática dela |
| Receber os modelos de ata, oitiva e relatório | Modelos fictícios: ata de reunião de triagem, ata de oitiva e relatório de recomendações, com a estrutura padrão e a base legal (art. 6º, 8º, 9º, 10 e 11 da LC nº 112/2002) | `modelos/MODELOS.md` | A | Os modelos oficiais |
| Linha de base: tempo das reuniões e oitivas | Triagem em **3 dias úteis**, oitiva em **10 dias úteis** após a triagem | `exemplos/gerar_exemplos.py` (datas das etapas) | B | Os tempos reais |

## 6. Controle do Processo de Aquisição (`controle-aquisicoes`)

| Item do Sprint 0 | Premissa assumida | Onde aparece | Nível | O que confirmar |
|---|---|---|---|---|
| Receber os modelos oficiais de DFD, ETP, TR e análise de riscos | Os 4 modelos existem como referência em `modelos/`, com as seções mínimas que o app exige em cada etapa. O ETP segue os 13 elementos do **art. 18, § 1º, da Lei nº 14.133/2021** (5 obrigatórios pelo § 2º), e a análise de riscos segue o inciso X do mesmo artigo | `modelos/MODELOS.md`, `modelos/fluxo-e-prazos.md` | B | Os modelos oficiais |
| Confirmar o fluxo real de tramitação e os prazos | O fluxo é o de 9 etapas do app (DFD, ETP, análise de riscos, TR, pesquisa de preços, SIGADOC e SIAG, análise técnica, análise jurídica, modalidade definida). **As etapas e os documentos vêm da Lei nº 14.133/2021** (art. 18, I, II, X; art. 23, § 1º, IV; art. 53), com o artigo de cada uma no app. Os **prazos em dias** são elucubração: 3, 5, 3, 5, 7, 2, 5, 10 e 3 (43 dias de ciclo) contra 30 dias de prazo do processo, o que faz 3 das 10 aquisições do exemplo estarem fora do prazo. O detalhamento e a base legal estão em `modelos/fluxo-e-prazos.md` e no `modelos/MODELOS.md` | `src/app.js` (`CA_ETAPAS`, `CA_DOCS`, `CA_PRAZO_ETAPA`, `CA_BASE_LEGAL`), `modelos/fluxo-e-prazos.md` | B | Os prazos reais de cada etapa |
| Validar as permissões e a base de processos de 2024/2025 | 3 perfis (requisitante, compras, gestor); 10 processos de exemplo de 2026. O **agente de contratação** do art. 8º é desempenhado pelo papel "Equipe de aquisições" | store `processos`, `perfis` no `app.json` | A | Quem é responsável por cada etapa |

## 7. Custódia Definitiva (`custodia-definitiva`)

| Item do Sprint 0 | Premissa assumida | Onde aparece | Nível | O que confirmar |
|---|---|---|---|---|
| Conferir categorias, condições de conservação e capacidades | 5 categorias (entorpecentes e contraprovas, armas brancas, roupas e têxteis, eletrônicos e mídias, materiais biológicos), cada uma com condição de conservação e restrição; 5 contêineres com capacidade em litros (de 40 L a 200 L), um por categoria | store `categorias`, `conteineres`, `exemplos/gerar_exemplos.py` | C | As categorias e a capacidade real dos contêineres |
| Receber a medição real de volume, tempo de recebimento e tempo de localização | O volume é medido em **litros** (2 L por item típico), o recebimento leva **40 min** e a localização no acervo **15 min** | store `vestigios` (`volume_ocupado`), `historico_mensal` | B | A unidade de medida e os tempos reais |

## 8. Distribuição de Casos de DNA (`distribuicao-casos-dna`)

| Item do Sprint 0 | Premissa assumida | Onde aparece | Nível | O que confirmar |
|---|---|---|---|---|
| Confirmar a rotação e o número de peritos ativos | **4 peritos ativos**, rotação estrita P1 → P2 → P3 → P4, sem repetir o perito da rodada anterior | store `peritos`, `src/app.js` (`ddSugerir3`) | C | A rotação real e a equipe |
| Medir a linha de base do intervalo entre processamento e distribuição | O intervalo médio é de **2,5 dias**; a meta é 1 dia | painel (média processamento → distribuição) | B | A média real |
| Validar o número de casos por rodada e as naturezas de exame | 8 casos por rodada (6 ordinários e 2 cobranças) e **3 naturezas de exame: DNA, sexual e identificação humana**, que já aparecem na tabela de casos | store `casos` (`natureza`), `src/app.js` | B | Os casos por rodada e a lista de naturezas |

## 9. DOCUMENTAPOLITEC (`documentapolitec`)

| Item do Sprint 0 | Premissa assumida | Onde aparece | Nível | O que confirmar |
|---|---|---|---|---|
| Confirmar o formato do número do prontuário e o modelo das caixas | O número é **AAAA.NNNNNN** (ex.: 2019.000001); a caixa do exemplo cabe de **9 a 13 prontuários** e tem lacre com responsável e data | store `prontuarios`, `caixas`, `src/app.js` | B | O formato e a capacidade da caixa |
| Receber a planilha de teste com a relação de 850 prontuários | A planilha de 850 linhas foi gerada como exemplo, com 2 linhas repetidas e 1 fora do formato, para exercitar a recusa | `exemplos/gerar_planilhas.py`, `exemplos/relacao-prontuarios.csv` | A | A planilha real |
| Receber uma amostra do PDF digitalizado | O índice do arquivo digital chega como **relação de números** (o texto extraído do PDF), não como PDF: o app compara a planilha com essa relação | `exemplos/indice-arquivo-digital.csv`, `src/sprint3.js` | A | A forma de entrega do índice |

## 10. Gestão de Documentos (`gestao-documentos`)

| Item do Sprint 0 | Premissa assumida | Onde aparece | Nível | O que confirmar |
|---|---|---|---|---|
| Validar a matriz de papéis e quem pode excluir documentos | 3 perfis: servidor (cadastra e instrui), chefia (acompanha e cobra) e autoridade (decide). **Ninguém exclui documento** pela regra do app: a exclusão é lógica e fica registrada | `perfis` no `app.json`, `src/app.js` | C | A matriz de papéis |
| Definir os anexos obrigatórios por tipo de processo (RN01) | Os 3 anexos obrigatórios são Requerimento, Documento de identificação e Anexos obrigatórios, iguais para todo processo. **O exemplo tem 1 processo com só 2 anexos**, como exceção do caso de anexo faltante. A regra é o que existe, não o que deveria existir | `GD_ANEXOS` em `src/app.js`, `exemplos/gerar_exemplos.py` | C | Os anexos por tipo |
| Medir a linha de base (1 h/dia, 200 processos/mês, 48 h na triagem) | 1 h/dia de instrução, 200 processos/mês na lotação, 48 h entre a autuação e a primeira distribuição | painel, `exemplos/gerar_exemplos.py` | B | As três medidas |

## 11. Equipamentos no Google Earth (`equipamentos-google-earth`)

| Item do Sprint 0 | Premissa assumida | Onde aparece | Nível | O que confirmar |
|---|---|---|---|---|
| Ler o `contexto.md` com a coordenadora e marcar cada **[validar]** | Cada **[validar]** foi lido e marcado como **aceito** no `contexto.md`, com a decisão anotada | `contexto.md` | A | A leitura com a coordenadora |
| Preencher de novo no formulário as seções MVP, papéis, entidades, regras, telas e KPIs | As seções 2 a 7 do `projeto.json` estão preenchidas e o `PROJETO.md` não tem mais "1" nem "Sem informação" | `projeto.json`, `PROJETO.md` | A | A conferência do aluno |
| **Retirar o número de 11 dígitos** do campo "dados pessoais tratados" | **Já retirado**: o campo `lgpd_dados` diz "Nenhum dado pessoal... nunca por CPF". O app não coleta CPF nem matrícula de pessoa, só o cargo de quem registra | `projeto.json` (`lgpd_dados`) | A | Nenhuma (o item já estava resolvido) |
| Levantar a lista de diretorias e unidades com município de cada uma | 3 diretorias e 12 unidades, em municípios reais de MT (Cuiabá, Várzea Grande, Rondonópolis, Sinop, Cáceres, Barra do Garças, Tangará da Serra, Alta Floresta, Primavera do Leste, Sorriso, Juína e Pontes e Lacerda) | store `diretorias`, `unidades`, `exemplos/gerar_exemplos.py` | B | A lista real de unidades |
| Reunir a planilha que existe hoje e anotar as colunas | A planilha atual é a de **controle de patrimônio**:Patrimônio, Tipo, Descrição, Valor de aquisição, Data de aquisição, Unidade, Situação | store `equipamentos`, `contratos` | B | As colunas reais |
| Definir o `valor_referencia_atendimento` e o custo alternativo padrão | Referência de atendimento: **R$ 180,00**; custo alternativo padrão: **R$ 0,00**, porque não há terceirização nem deslocamento no preset. Os dois valores já estão no store `parametros`; o registro de paradas e o cálculo de custo entram no Sprint 5 | store `parametros`, `src/app.js` | B | Os dois valores |
| Escolher 3 unidades para o piloto e medir a linha de base | Piloto: Sede Cuiabá, Posto Várzea Grande e Regional Rondonópolis. Linha de base medida no exemplo: **58 de 150 equipamentos sem contrato (39%)**, **40 paradas** no período e **2 dias** para responder "quanto custa essa parada?" | `exemplos/gerar_exemplos.py` (paradas e contratos), painel | B | As 3 unidades e as três medidas |

## 12. Hórus · Banco de Demandas (`horus-banco-demandas`)

| Item do Sprint 0 | Premissa assumida | Onde aparece | Nível | O que confirmar |
|---|---|---|---|---|
| Decidir o papel da versão offline | **(b) servir às unidades sem acesso ao Hórus**: o app é uma cópia de leitura e inscrição que devolve o registro para digitação no Hórus. Não substitui o módulo | `contexto.md`, `README.md` | C | A gestão do Hórus |
| Copiar do Hórus o esquema real das 3 tabelas (DDL do Supabase) | O esquema fica em `horus/esquema.sql`, com as 3 tabelas (`diretoria`, `unidade_medida`, `demanda`) e as chaves que o app importa | `horus/esquema.sql` (a criar) | B | O DDL verdadeiro |
| Definir o formato `horus-import-ciclo.json` | Formato: `{versao, gerado_em, ciclo: {id, nome, ano}, unidades: [...], medidas: [...], demandas: [...]}` | `exemplos/horus-import-ciclo.json` (a criar) | B | O formato real de intercâmbio |
| Decidir o relatório: `@media print` ou jsPDF | **`@media print`**: o app não embute biblioteca de PDF; o relatório é a tela com o CSS de impressão | `src/app.css` (ou `src/app.js`) | A | Nenhuma se ninguém pedir arquivo |
| Juntar ao envio os anexos citados (relatório PDF e print da tela) | Os anexos viram `modelos/relatorio.md` e `modelos/print-relatorio.md`, com o print explicado em 6 passos | `modelos/` (a criar) | A | Os anexos reais |

## 13. Inscrições em Cursos (`inscricoes-cursos`)

| Item do Sprint 0 | Premissa assumida | Onde aparece | Nível | O que confirmar |
|---|---|---|---|---|
| Ler o `contexto.md` com a aluna e decidir cada **[validar]** | Cada **[validar]** foi lido e marcado como **aceito** no `contexto.md` | `contexto.md` | A | A leitura com a aluna |
| Decidir se o CPF sai do formulário | **Sai**. O formulário pede matrícula, nome, lotação, diretoria e e-mail; o CPF não é coletado. O app valida a matrícula e o domínio do e-mail | `src/app.js` (RN02) | C | A chefia |
| Confirmar com a TI se a caixa `capacitacao@` aceita e-mail | **Sim**, a caixa institucional existe e o envio sai por `mailto:` com o bloco do e-mail no corpo, para não depender de servidor | `src/sprint3.js` (`blocoInscricao`) | A | A TI |
| Listar as diretorias que recebem vagas | 4 diretorias: DML (Matriz), DIN (Interiorização), DIT (Tecnologia), DCC (Ciência Criminal) | store `diretorias`, `exemplos/gerar_exemplos.py` | B | A lista real |
| Medir a linha de base em 2 cursos recentes | Da divulgação à lista: **12 dias**; da lista à convocação: **5 dias** | `exemplos/gerar_exemplos.py` (datas das turmas) | B | Os tempos reais |
| Corrigir no formulário as métricas | As 4 métricas do formulário (vagas por diretoria, prazo de inscrição, lista de espera e taxa de aprovação) estão no app e com valor | `src/app.js`, `PROJETO.md` | A | A conferência do aluno |

## 14. Mapa de Distribuição a Credores (`mapa-distribuicao-credor`)

| Item do Sprint 0 | Premissa assumida | Onde aparece | Nível | O que confirmar |
|---|---|---|---|---|
| Anexar o `WorkFlow.docx` (exemplos 1 a 8) | Os 8 exemplos viram `modelos/workflow.md`, com a coluna, o exemplo e o gabarito de cada caso | `modelos/workflow.md` (a criar) | A | O arquivo real |
| Decidir com a equipe e o orçamento os 4 pontos **[validar]** | Os 4 pontos foram decididos: (1) distribuição por dotação, não por área; (2) rateio proporcional, sem resto; (3) limite de 3 itens por credor; (4) tolerate de R$ 50,00 na diferença de rateio | `src/app.js`, `contexto.md` | C | A decisão da equipe |
| Conseguir um relatório do pregoeiro de amostra | O relatório do pregoeiro tem 5 colunas: Item, Descrição, Situação, Empresa, CNPJ, com as situações homologado, fracassado e deserto | `exemplos/relatorio-pregoeiro.xlsx` | A | O relatório real |
| Montar à mão o `mapa-manual-referencia.xlsx` (o gabarito) | O gabarito está pronto em `exemplos/mapa-manual-referencia.xlsx`, com os totais esperados de cada fonte | `exemplos/mapa-manual-referencia.xlsx` | A | A conferência manual |
| Medir a linha de base em 3 a 6 processos encerrados | 6 processos de exemplo, com as horas por etapa registradas e o total do ciclo | store `processos`, `etapas` (no app), `exemplos/gerar_exemplos.py` | B | As horas reais |

## 15. Metas BI · OCR (`metas-bi-ocr`)

| Item do Sprint 0 | Premissa assumida | Onde aparece | Nível | O que confirmar |
|---|---|---|---|---|
| Perguntar à TI se o Power BI 1 permite exportar dados do visual | **Sim**: o caminho adotado é a **exportação CSV do visual de pendências**, que é o que o app importa. O PDF é aceito só como conferência visual | `src/app.js` (importação), `exemplos/powerbi1-*.csv` | B | A TI confirma a exportação |
| Conseguir uma amostra do PDF mensal com números fictícios | Os 3 PDFs de exemplo (`powerbi1-2026-07/08/09.pdf`) vêm com o mesmo conteúdo do CSV | `exemplos/` | A | A amostra real |
| Copiar o cabeçalho da planilha do Google | O cabeçalho é: `Unidade`, `Indicador`, `Realizado`, `Meta`, `Observação` | `exemplos/gerar_exemplos.py` (CSV) | B | O cabeçalho real |
| Listar as unidades e os nomes como aparecem no relatório | 10 unidades: IML Cuiabá, IML Várzea Grande, Laboratório Forense, Criminalística Cuiabá, Regional Rondonópolis, Regional Sinop, Regional Cáceres, Regional Barra do Garças, Regional Tangará da Serra e Regional Alta Floresta | store `unidades`, `exemplos/gerar_exemplos.py` | B | A lista real |
| Linha de base: cronometrar a atualização do mês | Atualização mensal leva **1 dia útil** (dia 5 do mês seguinte) | `exemplos/gerar_exemplos.py` (datas dos relatórios) | B | O tempo real |

## 16. Passivo Ambiental (`passivo-ambiental`)

| Item do Sprint 0 | Premissa assumida | Onde aparece | Nível | O que confirmar |
|---|---|---|---|---|
| Receber uma requisição real anonimizada e o modelo de laudo da unidade | A requisição tem 6 campos (número do processo, órgão, data, tipo de infração, prazo e local com coordenadas) e o laudo tem cabeçalho de 6 linhas, conclusão e mapa anexado | `src/app.js` (`paCabecalho`), store `requisicoes` | B | O formulário e o modelo reais |
| Confirmar o modelo de mapa (norte, escala, área) com o perito | O mapa tem 5 elementos obrigatórios (norte, escala, legenda, data do levantamento e fonte da imagem) mais a medida do modelo: área em ha ou distância em km | `src/sprint3.js` (`PA_ELEMENTOS`, `PA_MODELOS`) | B | O modelo real do perito |
| Cronometrar 5 laudos para confirmar a linha de base de 16 h | **16 h** por laudo concluído, com prazo de 10 dias na requisição. Os laudos em elaboração acumulam 0, 4 ou 8 h | store `laudos` (`horas_trabalhadas`), `exemplos/gerar_exemplos.py` | B | A cronometragem real |

## 17. Renovação de Contratos (`renovacao-contratos-horus`)

| Item do Sprint 0 | Premissa assumida | Onde aparece | Nível | O que confirmar |
|---|---|---|---|---|
| Confirmar as seis faixas do semáforo e o alerta de 90 dias com a gestão | As 6 faixas do app: Normal (mais de 120 dias), Acompanhamento (91 a 120), Atenção (61 a 90), Providências (31 a 60), Urgente (0 a 30) e Vencido. O alerta é de **90 dias** | `RC_FAIXAS` em `src/app.js`, `alerta_dias` no contrato | C | As faixas reais |
| Definir as permissões de escrita (autor, chefia, gestor) | 3 perfis: gestor (monitora, instrui e registra a prorrogação), fiscal (acompanha a vigência do contrato designado) e admin (mantém o cadastro e consulta a auditoria). Escrita restrita a gestor e admin | `perfis` no `app.json` | C | A matriz de permissões |

## 18. RNC · Não Conformidade (`rnc-nao-conformidade`)

| Item do Sprint 0 | Premissa assumida | Onde aparece | Nível | O que confirmar |
|---|---|---|---|---|
| Listar com a CQUAL as categorias e as gravidades | 6 setores da Diretoria de Laboratório Forense (LQF, LGF, LTX, REC, ALM, CUS) e 6 categorias do formulário do Google (cadeia de custódia, registro incompleto, equipamento sem calibração, prazo de laudo, armazenamento de amostra, biossegurança), com **3 gravidades: leve, moderada e grave**. As 4 etapas são validação, plano, avaliação e encerramento | store `rncs`, `setores`, `etapas`, `src/app.js` | C | As categorias e gravidades |
| Copiar o cabeçalho da planilha de respostas do Forms | O cabeçalho do Forms é: `Carimbo de data/hora`, `Setor relator`, `Setor notificado`, `Categoria`, `Descrição da ocorrência`, `Gravidade`, `Número` | `exemplos/respostas-forms-ficticio.csv` | B | O cabeçalho real |
| Linha de base: tempo de cada etapa e cobranças da CQUAL | Validação em **2 dias úteis**, plano em **5**, avaliação em **3** e encerramento em **1**; a cobrança da CQUAL entra quando a RNC passa do prazo da etapa | store `etapas` (`prazo`), `exemplos/gerar_exemplos.py` | B | Os tempos reais |

## 19. TAP · Portfólio de Projetos (`tap-portfolio-projetos`)

| Item do Sprint 0 | Premissa assumida | Onde aparece | Nível | O que confirmar |
|---|---|---|---|---|
| Receber o modelo vigente do TAP e a lista oficial de documentos | O TAP tem 9 campos (título, unidade, responsável, contato, objetivo, justificativa, objetivo estratégico, valor estimado e prazo) e **5 documentos**: pesquisa de preços, estudo técnico e anuência da chefia (obrigatórios), cronograma e fotos (facultativos) | store `documentos`, `propostas`, `src/app.js`, `modelos/modelo-tap.md` | B | O modelo oficial |
| Validar com a área responsável os campos obrigatórios e os tamanhos mínimos (RN01, RN02) | Título com 10 a 120 caracteres; objetivo com 30 a 600; justificativa com 30 a 600; valor estimado positivo; os 3 documentos obrigatórios anexados antes de enviar | `src/app.js` (RN01, RN02) | B | Os limites reais |
| Linha de base: 4 semanas de registro | 8 propostas de exemplo, com o prazo de captação de 4 meses e a portaria de priorização em 3 faixas (prioridade, fonte de recurso e situação de captação) | store `propostas`, `portfolio` | B | Os números reais |

## 20. TCIN · Trilha de Custódia (`trilha-custodia-necropsia`)

| Item do Sprint 0 | Premissa assumida | Onde aparece | Nível | O que confirmar |
|---|---|---|---|---|
| Confirmar com a aluna e o IML o nome do projeto (CNC ou TCIN) | **TCIN** (Trilha de Custódia e Identificação), que é o nome usado no app e no repositório | título do app, `README.md` | A | A decisão final |
| Validar os quatro marcos e os livros que o app substitui | Os 4 marcos: Saída da base, Chegada ao local, Saída do local, Retorno ao IML. Os livros substituídos são o livro de entrada e saída e o livro de recebimento de corpos | store `marcos`, `src/app.js` (`TC_MARCOS`) | B | Os marcos e os livros reais |
| Medir a linha de base de remoção, identificação e liberação | Remoção em **4 h**, identificação em **48 h**, liberação em **72 h**. O exemplo traz 12 corpos com as 5 situações e um caso sem identificação | `exemplos/gerar_exemplos.py` (datas) | B | As três medidas |

---

## Como aplicar uma correção

1. A premissa mora no gerador de dados (`Apps/<app>/exemplos/gerar_exemplos.py`) ou
   no código do app (`Apps/<app>/src/app.js` ou `src/sprintN.js`).
2. Troque o valor, rode o gerador e reconstrua:
   ```powershell
   python "Apps/<app>/exemplos/gerar_exemplos.py"
   python Apps/_base/construir.py <app>
   python Apps/_base/testar.py <app>
   python Apps/_base/testar_sprints.py <app>
   ```
3. Se o valor estava numa asserção de teste (`Apps/_base/cenarios/sprintN.py`),
   ajuste a asserção para o novo valor.
4. Marque aqui: **confirmado em <data>, por <quem>**, na linha da premissa.

## Regra do que não pode ser inventado

Dado pessoal e dado real de pessoa identificável não entram em nenhuma premissa.
Os apps usam nomes, CPF, CNPJ, matrículas e protocolos fictícios. As linhas de
base são estimativas plausíveis para o protótipo, e é isso que o texto diz.

**Norma não se inventa.** Quando a lei existe e está publicada, ela é citada com
o artigo e o trecho, e não "a conferir". Duas normas entraram assim:

| Norma | Onde | O que ancora |
|---|---|---|
| **LC nº 112/2002-MT** — Código de Ética Funcional do Servidor Público Civil do Estado | `comissao-etica-denuncias/modelos/codigo-etica-lc112-2002.md` | as 8 categorias, com artigo e texto; os prazos de 5 e 3 dias do art. 8º; as cominações do art. 9º |
| **Lei nº 14.133/2021** — Lei de Licitações e Contratos | `controle-aquisicoes/modelos/fluxo-e-prazos.md` | as 9 etapas e os documentos (art. 18, 23 e 53); as 3 cotações (art. 23, § 1º, IV) |

O texto das duas foi consultado em 30/10/2026 no acervo
[ctresb/leis](https://github.com/ctresb/leis) e no site do Planalto. O que continua
sendo elucubração são os **prazos em dias** e a **divisão em etapas**, porque a
lei não fixa esses números para o fluxo interno da POLITEC.
