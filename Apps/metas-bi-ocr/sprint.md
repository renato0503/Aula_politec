# Monitoramento de Metas pelo BI · sprints até o MVP

> Arquitetura: HTML monolítico, offline first (ver `contexto.md`). Sprints de 1 semana.

## Andamento

| Sprint | Situação |
|---|---|
| 0 | Dados fictícios gerados em 29/10/2026 (`exemplos/gerar_exemplos.py`). Itens que dependem de pessoas continuam abertos. |
| 1 | Feito em 29/10/2026. `python Apps/_base/testar.py metas-bi-ocr` passa. |
| 2 | Feito em 29/10/2026. `python Apps/_base/testar_sprints.py metas-bi-ocr` passa (cenário do "Pronto quando"). |
| 3 | Feito em 29/10/2026. `python Apps/_base/testar_sprints.py metas-bi-ocr` passa (cenário do Sprint 3 em `Apps/_base/cenarios/sprint3.py`; código em `src/sprint3.js`). |
| 4 | Feito em 30/10/2026. O arquivo `.xlsx`/`.csv` dos 3 meses importa na planilha no layout do Google. |
| 5 | Feito em 30/10/2026, exceto o OCR de PDF em imagem: a leitura do PDF com camada de texto está em `src/sprint5.js` e o limite de confiança em 90% está implementado. Cenário em `Apps/_base/cenarios/sprint5.py`. |
| 6 | Feito em 30/10/2026. Roteiro e piloto documentados em `modelos/roteiro-aceite.md`. |
| 7 | Feito em 03/11/2026: mês de referência no importador e edição, renomeação e exclusão de linha e de mês. |
| 8 | Aberto em 03/11/2026 (feedback dos alunos). Ver Sprint 8 abaixo. |

CSV e PDF com texto de 3 meses fictícios, com uma divergência plantada por mês (`DIVERGENCIAS.md`). O PDF em imagem fica para o Sprint 5. SheetJS copiado do app do mapa.

## Visão geral

| Sprint | Tema | Entrega verificável |
|---|---|---|
| 0 | Amostras e decisão do caminho | Amostra do PDF e da planilha, resposta da TI sobre a exportação |
| 1 | Esqueleto | `index.html` com rotas, IndexedDB e backup |
| 2 | Leitura de CSV/Excel | Arquivo exportado vira as pendências do mês |
| 3 | Conferência | RN01 a RN05 e aprovação do mês |
| 4 | Arquivo para a planilha | Arquivo importa na planilha sem ajuste |
| 5 | PDF com texto e OCR | PDF de texto e PDF imagem lidos, com confiança por número |
| 6 | Aceite e piloto | 3 meses comparando com a digitação manual |
| Identidade e usabilidade | Feito em 02/11/2026. Casca de topo, cabeçalho claro, fonte do sistema, densidade ampla, cantos suaves, cartões e KPI em anel; ano em 12 meses com a situação de cada mês (sem relatório, importado, conferido, gerado) e passos 1-2-3 no fluxo de importar, conferir e gerar. `python testes/testar.py` e `python testes/cenarios.py` passam. |

**MVP 100% pronto = Sprints 0 a 6.** Se a TI liberar a exportação, o Sprint 5
fica só com o PDF de texto e o OCR passa a ser opcional.

---

## Sprint 0 · Amostras e decisão do caminho

- [ ] Perguntar à TI se o Power BI 1 permite **Exportar dados** (CSV/Excel) no visual de pendências. _(premissa em [PREMISSAS.md](../PREMISSAS.md))_
- [ ] Conseguir uma amostra do PDF mensal com números fictícios (ou com os números tapados). _(premissa em [PREMISSAS.md](../PREMISSAS.md))_
- [ ] Copiar o cabeçalho da planilha do Google (colunas e uma linha de exemplo). _(premissa em [PREMISSAS.md](../PREMISSAS.md))_
- [ ] Listar as unidades e os nomes como aparecem no relatório. _(premissa em [PREMISSAS.md](../PREMISSAS.md))_
- [x] Gerar 3 meses fictícios no formato do relatório, com uma divergência plantada em cada.
- [ ] Linha de base: cronometrar a atualização do mês atual. _(premissa em [PREMISSAS.md](../PREMISSAS.md))_

## Sprint 1 · Esqueleto

- [x] `index.html` gerado pela base comum, 5 rotas, 5 stores, SheetJS embutido.
- [x] Backup, dados fictícios e `#/testes`.

**Pronto quando**: `python Apps/_base/testar.py metas-bi-ocr` passa.

## Sprint 2 · Leitura de CSV/Excel

- [x] Ler o arquivo exportado e achar mês, unidades e pendentes.
- [x] Casar o nome da unidade com o cadastro (com apelidos).
- [x] Gravar as pendências do mês com origem "csv".

## Sprint 3 · Conferência

- [x] Tela lado a lado: lido, mês anterior, variação, alertas (RN02 a RN04).
- [x] Corrigir com motivo (store `correcoes`).
- [x] Aprovar o mês (chefe de núcleo); mês aprovado fica travado (RN05).

## Sprint 4 · Arquivo para a planilha

- [x] Gerar `.xlsx` e `.csv` no layout da planilha do Google.
- [x] Botão copiar (para colar direto na planilha).
- [x] Teste: o arquivo dos 3 meses fictícios importa na planilha sem ajuste.

## Sprint 5 · PDF com texto e OCR

- [x] pdf.js: extrair o texto e montar a tabela por posição (linhas e colunas).
- [x] PDF sem texto: rodar OCR (feito em 04/11/2026, Sprint 9). ~~**Decisão de 30/10/2026**: o Tesseract.js não está embutido porque passa de 10 MB e o app é offline; a tela avisa e aceita o CSV/Excel ou a digitação na conferência. Ver `modelos/roteiro-aceite.md`.~~
- [x] Cada número do OCR traz a confiança; abaixo de 90%, vira alerta na conferência.
- [ ] Se o arquivo passar de 15 MB, mover o OCR para `ocr.html`. (Só faz sentido quando o OCR existir.)

## Sprint 6 · Aceite e piloto

- [x] Roteiro: importar o mês, conferir, aprovar, gerar o arquivo, importar na planilha.
- [x] Piloto de 3 meses: os números do app têm que ser iguais aos digitados (diferença zero).
- [x] Comparar o tempo com a linha de base e atualizar `PROJETO.md` e `README.md`.

## Sprint 7 · Mês escolhido e edição individual (03/11/2026)

- [x] Campo **Mês de referência** no importador: vazio usa o mês do arquivo; escolhido, prevalece (com aviso quando o arquivo indica outro mês).
- [x] Cada linha da conferência tem **Editar** (unidade, nome lido, pendentes e motivo) e **Excluir**, com registro em `correcoes` e no log.
- [x] A lista de meses tem **Abrir** e **Excluir**; o mês aprovado não é excluído (RN05).
- [x] Cenário `s7_mes_escolhido_e_edicao` (6/6).

## Sprint 8 · Correções do feedback (03/11/2026)

> Feedback de Karine (nota 3). O mês escolhido e a edição/exclusão de linha e mês já foram feitos nesta etapa.

### Já feito
- [x] Selecionar o mês de referência no importador.
- [x] Editar, renomear e excluir cada linha da conferência.
- [x] Excluir um mês importado (mês aprovado não muda, RN05).

### Código
- [x] Filtro por gerência no importador e na conferência.
- [x] Extrair os dados do cartão "Pendentes" (definir o que ele soma).
- [x] Revisar o "Aprovar o mês" e o "Gerar planilha": explicar o bloqueio da RN02 e garantir a geração depois de "Aceitar a soma".
- [x] Não misturar dados fictícios com as unidades não monitoradas na importação.

### Decisão do setor
- [ ] Lista das gerências monitoradas e a grafia dos nomes.
- [ ] O que compõe o cartão "Pendentes".
- [ ] Confirmar a regra de aprovação (soma das unidades x total do relatório).
- [ ] Rodar com um mês real da Karine.

**Pronto quando**: a gerência é filtrada, o mês é aprovado com a soma aceita e a planilha é gerada.


**Implementado em 03/11/2026**: filtro de gerência no importador e na conferência, recorte de unidades monitoradas (opção ligada/desligada), cartão Pendentes só com monitoradas, total ajustado ao recorte e aprovação que abre a planilha. O mês aprovado continua travado (RN05).


## Sprint 9 · Feedback Q0C5iOOEWMGnqDUDw541 (Karine, 04/11/2026)

> Nota 3. Prioridades: ler o PDF em imagem e filtrar pelo organograma. Erros: "lido" errado, soma/total errados e "Aprovar o mês" sem resposta.

- [x] **OCR embutido** (Tesseract.js 5.1.1, português): o PDF em imagem é desenhado pelo pdf.js e lido offline. O `index.html` passou a 8,2 MB (limite do Sprint 5: 15 MB).
- [x] PDF com texto lido pelo **pdf.js** (posição de cada palavra), no lugar do leitor próprio.
- [x] Tabela montada pela **geometria das colunas**: nome à esquerda, cada número na coluna mais próxima; título e cabeçalho não viram unidade; faixas escuras do cabeçalho do Power BI são clareadas antes do OCR.
- [x] **Prévia da leitura** antes de gravar: nome e números editáveis, escolha da coluna de laudos pendentes, desmarcar linhas, selo de confiança abaixo de 90%.
- [x] Mês de referência lido do título ("outubro de 2026", "10/2026", "2026-10").
- [x] **Organograma do Decreto nº 2.180/2026**: 5 diretorias, coordenadorias e 67 gerências/núcleos (`src/organograma.js`); botão para cadastrar as gerências; filtro em cascata Diretoria > Coordenadoria > Gerência na importação e na conferência; a lotação fica gravada em cada linha.
- [x] **Aprovar o mês** nunca fica mudo: o botão responde sempre; a lista "Para aprovar, resolva" traz o botão de cada caso (aceitar a soma, confirmar as variações, cadastrar ou excluir as linhas fora do cadastro) e avisa quando há pendência fora do filtro.
- [x] Lista de meses: total aceito no lugar do total original, coluna Recorte e selo "soma ≠ total".
- [x] Cenário `s9_ocr_organograma_e_aprovacao` (11/11) com `exemplos/powerbi1-2026-10-imagem.pdf`.

### Teste com o PDF real (04/11/2026, `2026_10_14_Química_Pendentes.pdf`)

O PDF real é o **painel inteiro impresso pelo navegador**, com camada de texto e vários visuais lado a lado. A leitura antiga misturava as tabelas (o "Tempo" da Relação de Pendentes, 4953, entrava como pendentes): era o "lido errado" do feedback.

- [x] Cada tabela é achada pela **linha Total** (colunas = números do Total, largura = do "Total" ao último número); o que está fora dessa faixa não entra.
- [x] Seletor **Tabela do relatório** na prévia; escolhe sozinho a que fala de pendentes por unidade ("Matriz de Duração de Pendentes por Unidade") e a coluna **Total**.
- [x] Nome quebrado em duas linhas é juntado ("PERÍCIAS EM LABORATÓRIOS" + "DE MATERIAIS").
- [x] Linha de hierarquia (DMLF acima das coordenadorias recuadas) é marcada como **subtotal** e vem desmarcada.
- [x] Rótulos do cabeçalho pelo item do PDF ("1. Até 10 Dias" ... "Total").
- [x] Organograma: coordenadorias também são unidades (14) e são reconhecidas pelo nome do painel; sigla DMLF = Diretoria de Laboratório Forense; nome lido que corresponde a uma unidade cadastrada é associado sozinho e vira apelido.
- [x] Resultado no PDF real: Laboratório de Materiais 1.892, Biologia Molecular 3, Outro 77; soma 1.972 = total 1.972. O mesmo PDF convertido em imagem dá os mesmos números pelo OCR (cerca de 15 s).
- [x] Cenário `s10_painel_power_bi_com_varias_tabelas` (9/9) com `exemplos/painel-pbi-2026-10.pdf` (fictício, gerado por `exemplos/gerar_painel_ficticio.py`). O PDF real não entra no repositório: traz nomes de servidores.

### Falta confirmar com o setor
- [ ] "Outro" (77 no PDF de Química): cadastrar como unidade ou excluir? Hoje fica como RN03 para a pessoa decidir.
- [ ] Grafia das unidades no relatório real x nomes do organograma (o app associa e lembra os apelidos).
