# Registro de Não Conformidade · sprints até o MVP

> Arquitetura: HTML monolítico, offline first (ver `contexto.md`). Sprints de 1 semana.

## Andamento

| Sprint | Situação |
|---|---|
| 0 | Dados fictícios gerados em 29/10/2026 (`exemplos/gerar_exemplos.py`). Itens que dependem de pessoas continuam abertos. |
| 1 | Feito em 29/10/2026. `python Apps/_base/testar.py rnc-nao-conformidade` passa. |
| 2 | Feito em 29/10/2026. `python Apps/_base/testar_sprints.py rnc-nao-conformidade` passa (cenário do "Pronto quando"). |
| 3 | Feito em 29/10/2026. `python Apps/_base/testar_sprints.py rnc-nao-conformidade` passa (cenário do Sprint 3 em `Apps/_base/cenarios/sprint3.py`; código em `src/sprint3.js`). |

A planilha `respostas-forms-ficticio.csv` tem colunas **supostas**; trocar pelo cabeçalho real do Forms no Sprint 0.

## Visão geral

| Sprint | Tema | Entrega verificável |
|---|---|---|
| 0 | Categorias, colunas e dados | Categorias validadas, colunas do Forms, 20 RNCs fictícias |
| 1 | Esqueleto | `index.html` com rotas, perfis, IndexedDB e backup |
| 2 | Importar a planilha | CSV do Forms vira RNCs, sem duplicar |
| 3 | Etapas e prazos | Etapas com datas, prazos de 5 e 30 dias, anulação |
| 4 | Cópia do setor | Arquivo por setor, plano e avaliação de volta |
| 5 | Painel | Setores, categorias, recorrência, vencidas |
| 6 | Aceite e piloto | 30 dias no Laboratório Forense |

**MVP 100% pronto = Sprints 0 a 6.**

---

## Sprint 0 · Categorias, colunas e dados

- [ ] Listar com a CQUAL as categorias de não conformidade e as gravidades.
- [ ] Copiar o cabeçalho da planilha de respostas do Forms (sem dados) e anotar cada coluna.
- [x] Gerar 20 RNCs fictícias com setores fictícios, incluindo anulada, prorrogada, recorrente e grave.
- [ ] Linha de base: tempo de cada etapa e cobranças da CQUAL nas RNCs do primeiro mês.

## Sprint 1 · Esqueleto

- [x] `index.html` gerado pela base comum, perfis CQUAL e Setor, 6 rotas, 6 stores.
- [x] Backup, dados fictícios e `#/testes`.

**Pronto quando**: `python Apps/_base/testar.py rnc-nao-conformidade` passa.

## Sprint 2 · Importar a planilha

- [x] Ler o CSV (vírgula ou ponto e vírgula, UTF-8) e associar as colunas uma vez (fica salvo).
- [x] Gerar ou ler o número DIRETORIA/ANO-SEQ (RN01) e recusar duplicado.
- [x] Relatório da importação: novas, já existentes, recusadas.
- [x] Descartar qualquer coluna de nome de servidor (RN07).

## Sprint 3 · Etapas e prazos

- [x] `#/rnc/:id`: etapas (validação, plano, avaliação, encerramento) com início, fim e prazo.
- [x] RN02: pedido de complemento com 5 dias; vencido sem resposta, marca anulada.
- [x] RN03: plano em 30 dias, com prorrogação registrada.
- [x] RN04: marcar "grave, encaminhada à corregedoria".

## Sprint 4 · Cópia do setor

- [ ] Exportar `rnc-<setor>.json` só com as RNCs do setor (RN06).
- [ ] Perfil Setor: `#/minhas`, registrar envio do plano (FOR 2) e avaliação (FOR 3).
- [ ] Devolver o arquivo; a CQUAL importa e mescla.

## Sprint 5 · Painel

- [ ] Gráficos em SVG: RNCs por setor notificado, por categoria, por etapa.
- [ ] Recorrência (RN05) e lista de vencidas.
- [ ] Tempo médio por etapa e cobranças da CQUAL.

## Sprint 6 · Aceite e piloto

- [ ] Roteiro: importar, validar, exportar para o setor, receber o plano, ver o painel.
- [ ] Piloto de 30 dias na Diretoria de Laboratório Forense.
- [ ] Comparar com a linha de base e atualizar `PROJETO.md` e `README.md`.
