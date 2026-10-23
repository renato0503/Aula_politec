# Cenario 5 - Analise Laboratorial (DNA / Toxicologia)

O processo de bancada: do recebimento da amostra ao laudo assinado. O gargalo
tipico e a **fila do equipamento** (amplificacao e eletroforese), nao a
interpretacao - que e o trabalho mais visivel do perito.

Numeros **medidos** no dataset gerado (media por execucao de etapa):

| Etapa | Espera media | Execucao media | Retrabalho |
|---|---|---|---|
| 1. Recebimento e protocolo | 0 h | 0 h | 6,6% |
| 2. Triagem da amostra | 10,2 h | 0,9 h | 7,1% |
| 3. Preparo e extracao | 15,5 h | 4,2 h | 6,9% |
| 4. Quantificacao | 12,2 h | 1,3 h | 6,5% |
| **5. Amplificacao (PCR)** | **24,6 h** | 2,6 h | 7,0% |
| **6. Eletroforese** | **27,5 h** | 2,1 h | 6,2% |
| 7. Interpretacao do perfil | 11,0 h | 3,2 h | 6,8% |
| 8. Revisao e laudo | 9,7 h | 0 h | 7,7% |

**Achado principal**: as duas etapas de equipamento concentram **47,1% da
espera** (24,9% + 22,2%), e o processo e **88,6% espera**. A interpretacao tem o
maior trabalho manual (3,2 h), mas nao e o gargalo. O retrabalho e baixo e
uniforme (6,8%) - o problema e **capacidade de equipamento**, nao erro de
execucao.

**Para onde aponta a intervencao**: fila unica de amostras + painel de
capacidade do laboratorio. A TO-BE agenda a placa por prazo e prioridade, em vez
de ordem de chegada.

**Sugestao de Mermaid**: swimlanes por laboratorio (Biologia, Toxicologia,
Fisica) e um gateway "amostra conforme?" na triagem.
