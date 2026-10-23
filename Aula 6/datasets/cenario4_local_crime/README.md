# Cenario 4 - Atendimento de Local de Crime

O processo que comeca no acionamento da equipe e termina no relatorio de
atendimento. O gargalo classico nao esta na coleta (o trabalho visivel), mas no
**deslocamento** e na **liberacao do local** - as duas filas que dependem de
equipe, veiculo e autoridade.

Numeros **medidos** no dataset gerado (media por execucao de etapa):

| Etapa | Espera media | Execucao media | Retrabalho |
|---|---|---|---|
| 1. Acionamento da equipe | 0 h | 0 h | 8,5% |
| **2. Deslocamento ao local** | **22,9 h** | 2,6 h | 7,5% |
| 3. Isolamento e preservacao | 3,9 h | 0,8 h | 8,0% |
| 4. Coleta de vestigios | 7,5 h | 3,7 h | 8,3% |
| 5. Registro fotografico | 5,1 h | 0 h | 8,1% |
| 6. Acondicionamento e lacre | 6,2 h | 0,8 h | 8,6% |
| 7. Liberacao do local | 10,8 h | 0,6 h | 8,8% |
| 8. Relatorio de atendimento | 8,6 h | 1,7 h | 9,0% |

**Achado principal**: o deslocamento concentra **35,2% da espera**, e o processo
e **86,5% espera**. A coleta tem o maior trabalho manual (3,7 h), mas nao e o
gargalo. O retrabalho e sistemico (8,4%, parecido em todas as etapas), sinal de
problema de checklist/padrao, nao de uma equipe especifica.

**Para onde aponta a intervencao**: roteirizacao de equipes + checklist digital
de vestigios. A TO-BE reduz o deslocamento com fila por proximidade e elimina a
redigitacao do relatorio.

**Sugestao de Mermaid**: swimlanes por unidade (ATO, ATV - Campo, IML, CTRL) e
um gateway "local preservado?" antes da coleta.
