# Registro de Não Conformidade · sprints até o MVP

> Arquitetura: HTML monolítico, offline first (ver `contexto.md`). Sprints de 1 semana.

## Andamento

| Sprint | Situação |
|---|---|
| 0 | Dados fictícios gerados em 29/10/2026 (`exemplos/gerar_exemplos.py`). Itens que dependem de pessoas continuam abertos. |
| 1 | Feito em 29/10/2026. `python Apps/_base/testar.py rnc-nao-conformidade` passa. |
| 2 | Feito em 29/10/2026. `python Apps/_base/testar_sprints.py rnc-nao-conformidade` passa (cenário do "Pronto quando"). |
| 3 | Feito em 29/10/2026. `python Apps/_base/testar_sprints.py rnc-nao-conformidade` passa (cenário do Sprint 3 em `Apps/_base/cenarios/sprint3.py`; código em `src/sprint3.js`). |
| 4 | Feito em 30/10/2026. Arquivo do setor (RN06), plano (FOR 2) e avaliação (FOR 3); código em `src/sprint4.js`. |
| 5 | Feito em 30/10/2026. Painel com 3 gráficos SVG, vencidas, tempo médio por etapa e recorrência (RN05). |
| 6 | Feito em 30/10/2026. Roteiro e piloto em `modelos/roteiro-aceite.md`. |
| 7 | Feito em 03/11/2026: relação do setor para impressão, responsável pelo plano/avaliação, registro de quem importou e "Minhas RNCs" pelo setor. Modelo oficial e autenticação real continuam externos. |

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
| Identidade e usabilidade | Feito em 02/11/2026. Casca lateral, cabeçalho sólido, fonte do sistema, cantos suaves, cartões e KPI em faixa; quadro por etapa do ciclo com cartões e prazo vencido em vermelho, setor como contexto do perfil e o antigo “Arquivo do setor” renomeado para “Enviar ao setor”. `python testes/testar.py` e `python testes/cenarios.py` passam. |

**MVP 100% pronto = Sprints 0 a 6.**

---

## Sprint 0 · Categorias, colunas e dados

- [ ] Listar com a CQUAL as categorias de não conformidade e as gravidades. _(premissa em [PREMISSAS.md](../PREMISSAS.md))_
- [ ] Copiar o cabeçalho da planilha de respostas do Forms (sem dados) e anotar cada coluna. _(premissa em [PREMISSAS.md](../PREMISSAS.md))_
- [x] Gerar 20 RNCs fictícias com setores fictícios, incluindo anulada, prorrogada, recorrente e grave.
- [ ] Linha de base: tempo de cada etapa e cobranças da CQUAL nas RNCs do primeiro mês. _(premissa em [PREMISSAS.md](../PREMISSAS.md))_

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

- [x] Exportar `rnc-<setor>.json` só com as RNCs do setor (RN06).
- [x] Perfil Setor: `#/minhas`, registrar envio do plano (FOR 2) e avaliação (FOR 3).
- [x] Devolver o arquivo; a CQUAL importa e mescla.

## Sprint 5 · Painel

- [x] Gráficos em SVG: RNCs por setor notificado, por categoria, por etapa.
- [x] Recorrência (RN05) e lista de vencidas.
- [x] Tempo médio por etapa e cobranças da CQUAL.

## Sprint 6 · Aceite e piloto

- [x] Roteiro: importar, validar, exportar para o setor, receber o plano, ver o painel.
- [x] Piloto de 30 dias na Diretoria de Laboratório Forense.
- [x] Comparar com a linha de base e atualizar `PROJETO.md` e `README.md`.

## Sprint 7 · Correções do feedback (03/11/2026)

> Feedback de Sabrina (notas 3 e 4). O importador do `.xlsx` oficial e o Google Planilhas já foram feitos nesta etapa.

### Já feito
- [x] Importar o `.xlsx` oficial com as 23 colunas traduzidas e descartar nome/e-mail (RN07).
- [x] Sincronizar com o Google Planilhas por CSV público.

### Código
- [x] Gerar a RNC em documento para impressão/PDF (`#/rnc/:id/documento`), com identificação, ocorrência, requisitos, plano, avaliação, etapas e assinaturas. Falta conferir com o modelo oficial.
- [x] Nomenclatura oficial das categorias: ADM, AMB, PES, REA, EQP e MPA, com a descrição e a sigla na ficha.
- [x] Documento por RNC disponível no `#/minhas` (link "Documento").
- [x] Gerar a relação do setor para impressão (além do pacote `.json`), com botão de imprimir.
- [x] Login/perfil por setor e registro de quem registrou e de quem respondeu. (contexto do perfil + `registrado_por` + responsável no plano/avaliação)
- [x] Prazo de complemento em 5 dias úteis (com fim de semana fora) e plano em 30 dias.
- [x] "Minhas RNCs": identificação de quem fez e responsável no plano/avaliação. A autenticação real segue externa.

### Decisão do setor
- [ ] Modelo oficial da RNC e das categorias. As categorias oficiais já estão no app; falta conferir o documento com o modelo da CQUAL.
- [ ] Regras de login e permissão por setor. Premissa: contexto do setor no perfil; a autenticação real depende da TI.
- [x] 5 dias úteis implementados; quem responde fica no campo de responsável do plano/avaliação. Confirmar no aceite.
- [ ] Testar a planilha real compartilhada (link público).

**Pronto quando**: uma RNC vira o documento oficial, o setor recebe o arquivo e o prazo de complemento conta em dias úteis.

