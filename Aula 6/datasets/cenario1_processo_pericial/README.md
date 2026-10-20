# Cenario 1 - Processo de Requisicao Pericial (AS-IS)

O fluxo mais iconico da POLITEC: da delegacia ate a assinatura do
laudo. O gargalo classico e a **fila do perito** (etapa 4).

Numeros **medidos** no dataset gerado (media por execucao de etapa):

| Etapa | Espera media | Execucao media | Retrabalho |
|---|---|---|---|
| 1. Entrada da requisicao | 0 h | 0 h | 11,2% |
| 2. Triagem e classificacao | 10 h | 1 h | 12,7% |
| 3. Distribuicao ao setor | 13 h | 1 h | 11,4% |
| **4. Fila de espera do perito** | **44 h** | 0 h | 12,1% |
| 5. Analise do exame | 9 h | 5 h | 11,5% |
| 6. Revisao tecnica | 13 h | 2 h | 10,4% |
| 7. Assinatura e release | 10 h | 0 h | 11,7% |
| 8. Envio e arquivamento | 7 h | 0 h | 11,7% |

**Achado principal**: a etapa 4 concentra **41,5% de toda a espera** do
processo, e o processo inteiro e **92,4% espera** contra 7,6% de trabalho
efetivo. A analise (etapa 5) tem mais execucao (5 h) que qualquer outra, mas
apenas 9 h de espera - a **fila**, nao o trabalho, e o gargalo.

**Para onde aponta a intervencao**: a etapa 4. A TO-BE combina uma fila
priorizada por prazo legal (nao por ordem de chegada) com um painel de carga
por perito, reduzindo a espera sem aumentar a capacidade.

**Sugestao de Mermaid**: desenhe as 8 etapas como retangulos, com os sistemas
como swimlanes (SIGT, papel, e-mail).
