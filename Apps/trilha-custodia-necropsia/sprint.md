# TCIN · sprints até o MVP

> Arquitetura: HTML monolítico, offline first (ver `contexto.md`). Sprints de 1 semana.

## Andamento

| Sprint | Situação |
|---|---|
| 0 | Dois envios parciais e um protótipo recebidos em 29/10/2026. Dados fictícios gerados em `exemplos/gerar_exemplos.py`. Itens que dependem de pessoas continuam abertos. |
| 1 | Feito em 29/10/2026. `python Apps/_base/testar.py trilha-custodia-necropsia` passa. |
| 2 | Feito em 29/10/2026. `python Apps/_base/testar_sprints.py trilha-custodia-necropsia` passa (cenário em `Apps/_base/cenarios/sprint2.py`). |

## Visão geral

| Sprint | Tema | Entrega verificável |
|---|---|---|
| 0 | Processo e dados | Marcos, livros substituídos e situação validados; dados fictícios; linha de base |
| 1 | Esqueleto e painel | `index.html` com rotas, IndexedDB e painel por situação |
| 2 | Acionamento e marcos | Corpo com protocolo único, quatro marcos e lacres (RN01, RN03) |
| 3 | Identificação e busca | Situação de identificação, busca por nome/documento e trilha (RN04) |
| 4 | Liberação | Auto de entrega com responsável e data, só com identificação (RN02) |
| 5 | Painel do gestor | Tempo de remoção, identificação e liberação; não reclamados |
| 6 | Relatório e retirada | Relatório em CSV e impressão; retirada de dados do caso |
| 7 | Aceite e piloto | Piloto de 30 dias com casos fictícios e roteiro de aceite |

**MVP 100% pronto = Sprints 0 a 7.**

---

## Sprint 0 · Processo e dados

- [ ] Confirmar com a aluna e o IML o nome do projeto (CNC ou TCIN).
- [ ] Validar os quatro marcos e os livros que o app substitui.
- [ ] Medir a linha de base de remoção, identificação e liberação.
- [x] Gerar os dados fictícios em `exemplos/gerar_exemplos.py`.

## Sprint 1 · Esqueleto e painel

- [x] `index.html` com 3 perfis, 6 rotas, IndexedDB e backup.
- [x] Painel com corpos por situação, alertas e últimos marcos.
- [x] Lista de corpos com filtros.

**Pronto quando**: `python Apps/_base/testar.py trilha-custodia-necropsia` passa.

## Sprint 2 · Acionamento e marcos

- [x] Cadastro com protocolo único e recusa de duplicidade (RN01).
- [x] Registro dos quatro marcos com perfil, data e hora (RN03).
- [x] Lacres e amostras com código e destino.
- [x] Trilha de auditoria na ficha.

**Pronto quando**: `python Apps/_base/testar_sprints.py trilha-custodia-necropsia` passa.

## Sprint 3 · Identificação e busca

- [ ] Mudança de situação (em custódia, aguardando, não identificado, não reclamado).
- [ ] `#/busca` por protocolo, nome ou documento (RN04).
- [ ] Lista do painel sem nome completo (RN05).

## Sprint 4 · Liberação

- [ ] Auto de entrega com responsável, data e documento.
- [ ] Bloqueio de liberação sem identificação e sem auto (RN02).
- [ ] Trilha da liberação.

## Sprint 5 · Painel do gestor

- [ ] Tempo de remoção, de identificação e de liberação.
- [ ] Corpos não reclamados por tempo de permanência.
- [ ] Alertas de passagem de plantão.

## Sprint 6 · Relatório e retirada

- [ ] Relatório em CSV e impressão em A4.
- [ ] Botão para apagar os dados de um caso encerrado.
- [ ] Texto de privacidade e retenção.

## Sprint 7 · Aceite e piloto

- [ ] Roteiro de aceite com o IML.
- [ ] Piloto de 30 dias com casos fictícios.
- [ ] Atualizar `PROJETO.md` e `README.md`.
