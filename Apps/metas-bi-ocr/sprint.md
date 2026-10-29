# Monitoramento de Metas pelo BI · sprints até o MVP

> Arquitetura: HTML monolítico, offline first (ver `contexto.md`). Sprints de 1 semana.

## Andamento

| Sprint | Situação |
|---|---|
| 0 | Dados fictícios gerados em 29/10/2026 (`exemplos/gerar_exemplos.py`). Itens que dependem de pessoas continuam abertos. |
| 1 | Feito em 29/10/2026. `python Apps/_base/testar.py metas-bi-ocr` passa. |
| 2 | Feito em 29/10/2026. `python Apps/_base/testar_sprints.py metas-bi-ocr` passa (cenário do "Pronto quando"). |
| 3 | Feito em 29/10/2026. `python Apps/_base/testar_sprints.py metas-bi-ocr` passa (cenário do Sprint 3 em `Apps/_base/cenarios/sprint3.py`; código em `src/sprint3.js`). |

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

**MVP 100% pronto = Sprints 0 a 6.** Se a TI liberar a exportação, o Sprint 5
fica só com o PDF de texto e o OCR passa a ser opcional.

---

## Sprint 0 · Amostras e decisão do caminho

- [ ] Perguntar à TI se o Power BI 1 permite **Exportar dados** (CSV/Excel) no visual de pendências.
- [ ] Conseguir uma amostra do PDF mensal com números fictícios (ou com os números tapados).
- [ ] Copiar o cabeçalho da planilha do Google (colunas e uma linha de exemplo).
- [ ] Listar as unidades e os nomes como aparecem no relatório.
- [x] Gerar 3 meses fictícios no formato do relatório, com uma divergência plantada em cada.
- [ ] Linha de base: cronometrar a atualização do mês atual.

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

- [ ] Gerar `.xlsx` e `.csv` no layout da planilha do Google.
- [ ] Botão copiar (para colar direto na planilha).
- [ ] Teste: o arquivo dos 3 meses fictícios importa na planilha sem ajuste.

## Sprint 5 · PDF com texto e OCR

- [ ] pdf.js: extrair o texto e montar a tabela por posição (linhas e colunas).
- [ ] PDF sem texto: renderizar a página e rodar o Tesseract.js (português), página a página.
- [ ] Cada número do OCR traz a confiança; abaixo de 90%, vira alerta na conferência.
- [ ] Se o arquivo passar de 15 MB, mover o OCR para `ocr.html`.

## Sprint 6 · Aceite e piloto

- [ ] Roteiro: importar o mês, conferir, aprovar, gerar o arquivo, importar na planilha.
- [ ] Piloto de 3 meses: os números do app têm que ser iguais aos digitados (diferença zero).
- [ ] Comparar o tempo com a linha de base e atualizar `PROJETO.md` e `README.md`.
