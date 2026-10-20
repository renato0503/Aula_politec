# Cenario 3 - Cadeia de Custodia de Evidencias

O processo mais critico quanto a rastreabilidade: da coleta no local ate a baixa.
O gargalo nao e so tempo - e **risco de rastreabilidade** (perda de lacre,
divergencia). O TO-BE aqui prioriza **rastreio** acima de velocidade.

Numeros **medidos** no dataset gerado (media por execucao de etapa):

| Etapa | Espera media | Execucao media | Divergencia de lacre |
|---|---|---|---|
| 1. Coleta no local | 0 h | 2 h | 4,9% |
| 2. Acondicionamento e lacre | 11 h | 1 h | 5,5% |
| 3. Registro da ocorrencia | 12 h | 0 h | 3,9% |
| 4. Transporte ao destino | 16 h | 3 h | 4,2% |
| 5. Recebimento e conferencia | 14 h | 1 h | 5,5% |
| **6. Guarda / refrigeracao** | **55 h** | 0 h | 4,0% |
| 7. Pericia propriamente dita | 21 h | 6 h | 5,2% |
| 8. Baixa e destino final | 25 h | 0 h | 4,6% |

**Achado principal**: a etapa 6 concentra **35,3% da espera**, e o processo e
**92,5% espera**. A pericia (etapa 7) tem o maior trabalho (6 h) mas apenas 21 h
de espera. A divergencia de lacre aparece em **~4,8%** das execucoes — pouco em
termos absolutos, mas grave em termos de processo (um lacre aberto pode
inviabilizar a prova).

**Para onde aponta a intervencao**: a etapa 6 (guarda) e a rastreabilidade. A
TO-BE usa **QR Code por evidencia** e **app de custodia**: cada recebimento
digitaliza o lacre, cada transferencia registra responsavel e hora, e um alerta
dispara se a evidencia ficar parada alem do prazo.

**Sugestao de Mermaid**: BPMN com **mensagens** (o QR substitui o papel) e um
gateway de "lacre confere?". Este e o melhor cenario para ensinar **rastreio**
em vez de apenas velocidade.
