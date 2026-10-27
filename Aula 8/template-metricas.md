# Template de métricas — da linha de base à defesa da intervenção

Material de apoio da fase de ideação. O aluno usa o formulário para propor as
métricas; o professor usa este template para conferir se a métrica sustenta a
defesa e para montar o painel de gargalo de cada equipe.

---

## 1. O conjunto mínimo de métricas de um processo

Toda proposta de melhoria começa com estas cinco métricas, calculadas nas fontes
que a equipe declarou. As duas primeiras são de contexto, a terceira é o
diagnóstico, e as duas últimas são a defesa.

| # | Métrica | Pergunta que responde | Fórmula típica | Unidade |
|---|---|---|---|---|
| M1 | **Volume** | Quantos casos passam pelo processo? | contagem de casos no período | casos/mês |
| M2 | **TAT médio** | Quanto tempo o caso leva do início ao fim? | soma do tempo total / quantidade de casos | horas |
| M3 | **% de espera** | Quanto do tempo é fila, e quanto é trabalho? | tempo de espera / tempo total | % |
| M4 | **Espera na etapa crítica** | Onde o caso fica parado por mais tempo? | soma da espera na etapa X / casos | horas/caso |
| M5 | **Taxa de retrabalho** | Quanto do trabalho é refeito? | execuções devolvidas / execuções totais | % |

> **Por que M3 importa.** Sem a separação entre espera e execução, a métrica M4
> não tem sentido: a etapa que mais trabalha não é a etapa que mais espera. É
> essa separação que transforma a proposta em diagnóstico.

---

## 2. Como escrever a hipótese de melhoria

A hipótese é um número com LASTRO, não um palpite. Ela precisa de quatro peças:

| Peça | O que é | Exemplo |
|---|---|---|
| **Linha de base** | Valor medido no processo de hoje | 54,4 h de espera por caso na conferência de documentos |
| **Origem** | Onde esse número foi medido (fonte + período + volume) | sistema de sinistros, 2025, 1.113 casos |
| **Hipótese** | Valor esperado depois da intervenção, com a taxa de redução | 18 h por caso, com redução de 67% |
| **Teste** | Como a hipótese é verificada | piloto de 90 dias em uma central, medido no painel |

### Fórmulas de ganho

```text
Ganho anual (horas) = espera da etapa crítica no período
                     x taxa de redução da fila
                     / número de anos do período

Ganho em capacidade = horas liberadas por ano
                     x valor da hora de fila (R$ 42,00 no exercício do curso)

Retorno em 2 anos  = ganho em capacidade x 2 - investimento
```

> **Três cuidados.** (1) O valor por hora é uma hipótese assumida, e precisa
> estar escrito no painel. (2) Capacidade liberada não é economia: é o que a
> área vai fazer com ela. (3) A taxa de redução é hipótese até o piloto, e o
> painel do piloto é quem a confirma ou corrige.

---

## 3. A frase de defesa

O modelo é fixo, e ele força a coerência entre métrica, problema e intervenção:

```text
Se a equipe [M4: espera na etapa crítica] passar de [linha de base] para
[valor esperado], o [processo] deixa de [problema descrito no Bloco 1].
```

Exemplo preenchido:

> Se a espera na conferência de documentos cair de 54,4 horas para 18 horas por
> caso, o sinistro de trânsito deixa de ficar mais de dois dias parado sem que
> o segurado receba nenhuma notícia.

A frase só vale se: a métrica tem fonte, a linha de base foi medida, o valor
esperado tem a mesma unidade e a intervenção mexe na etapa da métrica. Se uma
dessas quatro peças falta, a defesa é opinião.

---

## 4. Exemplo completo (cenário 2, sinistro de trânsito)

| Métrica | Linha de base | Origem | Hipótese | Teste |
|---|---|---|---|---|
| M1 Volume | 1.113 casos/ano | sistema de sinistros, 2025 | 1.200 casos/ano | acompanhamento mensal |
| M2 TAT médio | 696,7 h | soma do tempo total / casos | 520 h | painel pós-piloto |
| M3 % de espera | 93,9% | espera / total | 90% | idem |
| M4 Espera na conferência de documentos | 54,4 h por caso | 35,7% da espera total (77.035 h em 3 anos) | 18 h por caso (redução de 67%) | piloto de 90 dias em uma central |
| M5 Retrabalho | 17,0% das execuções | flag de devolução no sistema | 8% | idem |

**Ganho calculado:** 77.035 h x 67% / 3 anos = 17.205 h de fila liberadas por
ano, o que equivale a R$ 722.600 de capacidade liberada ao ano, a R$ 42,00 por
hora de fila.

**Intervenção que produz o número:** abertura do sinistro pelo celular com
upload de foto e documento, alerta automático de pendência com prazo de 48 horas
e emissão assistida do laudo de vistoria.

**Limite declarado:** o segurado sem smartphone continua no fluxo em papel, com
digitação feita pela central. O canal digital não substitui o papel: ele
reduz o volume que chega à etapa de conferência.

---

## 5. Checklist do professor antes de montar o painel

- [ ] A métrica responde a **uma** pergunta, e a pergunta está escrita.
- [ ] A fórmula é executável por outra pessoa, com os campos que a fonte tem.
- [ ] A fonte existe, tem volume, e o acesso está liberado.
- [ ] A linha de base está medida, com período e volume declarados.
- [ ] O valor esperado tem a mesma unidade da linha de base.
- [ ] A intervenção mexe na etapa da métrica. Métrica que não muda com a intervenção é enfeite.
- [ ] A hipótese tem piloto, prazo e critério de sucesso.
- [ ] O limite da automação está escrito, e alguém da área concorda com ele.

---

## 6. Como o painel da defesa fica

O painel tem duas camadas, e o valor esperado entra na segunda.

| Camada | Visuais | Para que serve |
|---|---|---|
| **Diagnóstico** (hoje) | cartões de volume, TAT, % de espera, espera na etapa crítica; Pareto de espera por etapa; matriz etapa por unidade | mostrar onde a fila está |
| **Proposta** (depois) | cartão com o valor esperado ao lado do valor atual; barra de comparação antes e depois; cartão de ganho em horas por ano | defender a intervenção com a mesma métrica |

A leitura do painel na apresentação, em três frases:

1. "Hoje, [M4] responde por [X]% da espera do processo, e são [Y] horas por caso."
2. "A proposta mexe nessa etapa, e a hipótese é [Z] horas, medida com [fonte] no [período]."
3. "O piloto de [prazo] em [unidade] testa essa hipótese, e este mesmo painel mostra o valor real quando acabar."
