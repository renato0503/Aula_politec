# Roteiro de aceite e piloto (fictício)

> **Premissa assumida em 30/10/2026.** O piloto de 3 meses não foi executado. O
> roteiro abaixo é o que o app espera do aceite. Ver
> [PREMISSAS.md](../../PREMISSAS.md).

## 1. Roteiro do aceite

1. Abrir `#/config` e carregar os dados fictícios.
2. Abrir `#/importar` e escolher o CSV do mês (ou o PDF com camada de texto).
3. Conferir a tela de importação: mês, unidades lidas e total.
4. Abrir `#/conferencia/<mês>` e percorrer as divergências:
   - total do relatório diferente da soma das unidades (RN02);
   - unidade com nome fora do cadastro (RN03);
   - variação acima de 30% de um mês para o outro (RN04).
5. Corrigir cada divergência com motivo e aprovar o mês.
6. Abrir `#/exportar/<mês>` e gerar o `.xlsx` no layout da planilha do Google.
7. Importar o arquivo na planilha e conferir que a coluna a coluna bate.
8. Repetir para os 3 meses fictícios.

**Critério de aceite**: os números do app têm que ser iguais aos digitados à mão
na planilha, com **diferença zero**.

## 2. O que o app lê

| Formato | Situação | Observação |
|---|---|---|
| CSV da exportação do visual | lê | caminho mais seguro |
| Excel (`.xlsx`) | lê | pela biblioteca `xlsx.full.min.js` em `vendor/` |
| PDF com camada de texto | lê | extrai o texto e reconstrói as linhas por posição |
| PDF em imagem (escaneado) | **não lê** | o OCR (Tesseract.js) não está embutido: pesaria mais de 10 MB no app offline |

Se o PDF não tiver camada de texto, a tela avisa e o caminho é a exportação
CSV/Excel ou digitar os números na conferência.

## 3. Confiança da leitura

O texto extraído do PDF entra com confiança 100%. O OCR, quando existir, traz a
confiança de cada número, e **abaixo de 90%** o número vira alerta na conferência
(`CONFIANCA_MINIMA` em `src/sprint5.js`).

## 4. Piloto de 3 meses

| Mês | Divergência plantada | O que o app tem que mostrar |
|---|---|---|
| 2026-07 | Criminalística Cuiabá dobrou | variação acima de 30% (RN04) |
| 2026-08 | Unidade com nome diferente | unidade fora do cadastro (RN03) |
| 2026-09 | Total 17 a mais que a soma | total diferente da soma (RN02) |

## 5. Comparação com a linha de base

| Medida | Valor assumido |
|---|---|
| Atualização do mês hoje | 1 dia útil (dia 5 do mês seguinte) |
| Atualização com o app | minutos, depois de importar e conferir |

O ganho só se mede com os 3 meses reais. A premissa está no `PREMISSAS.md`.

## Como confirmar

1. Rodar o roteiro com a TI e com quem digita a planilha.
2. Assinar o aceite e atualizar `PROJETO.md` e `README.md`.
3. Se quiser o OCR para PDF em imagem, decidir sobre embutir o Tesseract.js.
