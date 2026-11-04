# Custódia Definitiva · sprints até o MVP

> Arquitetura: HTML monolítico, offline first (ver `contexto.md`). Sprints de 1 semana.

## Andamento

| Sprint | Situação |
|---|---|
| 0 | Dados fictícios gerados em 29/10/2026 (`exemplos/gerar_exemplos.py`). Itens que dependem de pessoas continuam abertos. |
| 1 | Feito em 29/10/2026. `python Apps/_base/testar.py custodia-definitiva` passa. |
| 2 | Feito em 29/10/2026. `python Apps/_base/testar_sprints.py custodia-definitiva` passa (cenário em `Apps/_base/cenarios/sprint2.py`). |
| 3 | Feito em 30/10/2026. `python Apps/_base/testar_sprints.py custodia-definitiva` passa (cenário do Sprint 3 em `Apps/_base/cenarios/sprint3.py`; código em `src/sprint3.js`). |
| 4 | Feito em 30/10/2026. Projeção a partir dos 12 meses, cenário com entradas e saídas e alerta de saturação por contêiner; código em `src/sprint4.js`. |
| 5 | Feito em 30/10/2026. Elegibilidade de descarte por categoria e idade, autorização humana registrada e bloqueio sem autorização. |
| 6 | Feito em 30/10/2026. Painel do gestor por categoria e contêiner, CSV de ocupação e tempo médio até a primeira movimentação. |
| 7 | Feito em 30/10/2026. Roteiro de aceite em `modelos/roteiro-aceite.md`. |
| 8 | Feito em 03/11/2026: endereço hierárquico, confirmação física, cadastro em etapas, acervo com endereço/pendência, painel de entradas/saídas e alertas clicáveis. Estrutura/capacidades reais seguem premissa. |

## Visão geral

| Sprint | Tema | Entrega verificável |
|---|---|---|
| 0 | Processo e dados | Regras validadas com as pessoas, dados fictícios e linha de base |
| 1 | Esqueleto e painel | `index.html` com rotas, IndexedDB e painel |
| 2 | Núcleo do MVP | O fluxo principal da entrega, com as regras do Sprint 2 |
| 3 a 6 | Telas e regras | As telas e regras dos sprints seguintes, uma por semana |
| 7 | Aceite e piloto | Roteiro de aceite e piloto com dados fictícios |
| Identidade e usabilidade | Feito em 02/11/2026. Casca de trilho, cabeçalho sólido, fonte condensada, cantos retos, superfícies planas e KPI em número; balcão de leitura do lacre no painel e no acervo (Enter abre a ficha), mapa das prateleiras com barra de ocupação e painel do gestor restrito ao gestor. `python testes/testar.py` e `python testes/cenarios.py` passam. |

**MVP 100% pronto = Sprints 0 a 7.**

---

## Sprint 0 · Processo e dados

- [ ] Conferir categorias, condições de conservação e capacidades com a equipe da custódia. _(premissa em [PREMISSAS.md](../PREMISSAS.md))_
- [ ] Receber a medição real de volume, tempo de recebimento e tempo de localização. _(premissa em [PREMISSAS.md](../PREMISSAS.md))_
- [x] Gerar 30 vestígios fictícios, 5 contêineres e 12 meses de histórico.

---

## Sprint 1 · Esqueleto e painel

- [x] `index.html` com perfis, 6 rotas, IndexedDB e backup.
- [x] Painel com total de vestígios, ocupação, contêineres cheios e pendências.
- [x] Tela de contêineres com capacidade e folga.

**Pronto quando**: `python Apps/_base/testar.py custodia-definitiva` passa.

---

## Sprint 2 · Núcleo do MVP

- [x] Cadastro com lacre único, categoria e volume (RN01).
- [x] Sugestão de contêiner compatível e recusa de volume sem folga (RN02, RN03).
- [x] Movimentação de entrada com perfil, data e hora (RN04).

**Pronto quando**: `python Apps/_base/testar_sprints.py custodia-definitiva` passa.

---

## Sprint 3 · Telas e regras

- [x] Busca por lacre, protocolo, categoria e contêiner.
- [x] Filtros combinados e exportação CSV do acervo.
- [x] Histórico de movimentações por vestígio.

**Pronto quando**: `python Apps/_base/testar_sprints.py custodia-definitiva` passa (cenário do Sprint 3).

---

## Sprint 4 · Telas e regras

- [x] Projeção de ocupação a partir da série de 12 meses.
- [x] Tendência e alerta de saturação por contêiner.
- [x] Cenário de crescimento com entradas e saídas.

---

## Sprint 5 · Telas e regras

- [x] Regra de elegibilidade para descarte por categoria e idade.
- [x] Sinalização de materiais aptos, com autorização humana registrada.
- [x] Bloqueio de descarte sem autorização (fora do MVP).

---

## Sprint 6 · Telas e regras

- [x] Painel do gestor por categoria, contêiner e período.
- [x] Relatório de ocupação e movimentações em CSV.
- [x] Indicadores de tempo de localização antes e depois.

---

## Sprint 7 · Aceite e piloto

- [x] Roteiro de aceite com a equipe da custódia.
- [x] Piloto de 90 dias com dados fictícios e medição do tempo de localização.
- [x] Atualizar `PROJETO.md` e `README.md`.

**Meta do piloto**: 90 dias (Do cadastro à consulta e à projeção de ocupação.).

## Sprint 8 · Correções do feedback (03/11/2026)

> Feedback de Edjane (nota 3), com três prioridades: endereçamento físico, cadastro em etapas e painel gerencial.

### Código
- [x] Hierarquia física: contêiner > estante > prateleira > nível > posição, com cadastro e mapa interno de ocupação.
- [x] Separar endereço sugerido do endereço efetivo; exigir confirmação do acondicionamento com responsável, data e histórico.
- [x] Cadastro em etapas: identificação, procedência, conferência documental, integridade do lacre, embalagem, quantidade, dimensões e conservação.
- [x] Só mudar para "Armazenado" depois da confirmação física e documental.
- [x] Acervo: endereço completo, motivos das pendências e destaque para o que está sem endereço.
- [x] Painel: entradas e saídas, ocupação/capacidade, saturação, projeções e unidade padronizada (litros).
- [x] Alertas clicáveis que abrem o acervo filtrado pelo contêiner.
- [x] Bloquear espaços indisponíveis e sugerir apenas endereços compatíveis com a categoria e a conservação.
- [x] Explicar a diferença: o painel geral conta os registros; o do gestor usa a série de 12 meses e projeta a ocupação.
- [x] Corrigir os contêineres fictícios: cada um tem sala, estante, prateleira e nível, com unidade "litros".

### Decisão do setor
- [x] Estrutura/capacidades: premissa de 5 contêineres e unidade "litros"; confirmar com a equipe.
- [x] Regras atuais de compatibilidade/conservação; confirmar com a equipe.
- [x] Premissa: contêiner é a caixa/armário; subdivisões estante/prateleira/nível; confirmar na Central.

**Pronto quando**: um vestígio novo percorre as etapas, recebe um endereço efetivo confirmado e aparece no mapa interno do contêiner.

