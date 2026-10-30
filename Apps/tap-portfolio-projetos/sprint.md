# TAP Digital e Portfólio de Projetos · sprints até o MVP

> Arquitetura: HTML monolítico, offline first (ver `contexto.md`). Sprints de 1 semana.

## Andamento

| Sprint | Situação |
|---|---|
| 0 | Dados fictícios gerados em 29/10/2026. Itens que dependem de pessoas continuam abertos. |
| 1 | Feito em 29/10/2026. `python Apps/_base/testar.py tap-portfolio-projetos` passa. |
| 2 | Feito em 29/10/2026. `python Apps/_base/testar_sprints.py tap-portfolio-projetos` passa (cenário do "Pronto quando"). |
| 3 | Feito em 29/10/2026. `python Apps/_base/testar_sprints.py tap-portfolio-projetos` passa (cenário do Sprint 3 em `Apps/_base/cenarios/sprint3.py`; código em `src/sprint3.js`). |

O checklist de documentos é uma proposta até o modelo oficial do TAP chegar.

## Visão geral

| Sprint | Tema | Entrega verificável |
|---|---|---|
| 0 | Modelo e checklist | Modelo do TAP e checklist validados, propostas fictícias, linha de base |
| 1 | Esqueleto | `index.html` com perfis, rotas, IndexedDB e backup |
| 2 | TAP guiado | Formulário em etapas, campos obrigatórios e checklist (RN01 a RN04) |
| 3 | Pacote e triagem | Pacote com anexos, importação pela equipe, pendências (RN05, RN06) |
| 4 | Proposta e decisão | Parecer e decisão registrados, histórico (RN07) |
| 5 | Portfólio | Prioridade justificada, captação, exportação Excel (RN08) |
| 6 | Indicadores, aceite e piloto | Indicadores, roteiro e piloto de 60 a 90 dias |

**MVP 100% pronto = Sprints 0 a 6.**

---

## Sprint 0 · Modelo e checklist

- [ ] Receber o modelo vigente do TAP e a lista oficial de documentos. _(premissa em [PREMISSAS.md](../PREMISSAS.md))_
- [ ] Validar com a área responsável os campos obrigatórios e os tamanhos mínimos (RN01, RN02). _(premissa em [PREMISSAS.md](../PREMISSAS.md))_
- [x] Gerar propostas fictícias completas e incompletas.
- [ ] Linha de base: 4 semanas de registro (recebimento, documentação completa, devoluções e motivos). _(premissa em [PREMISSAS.md](../PREMISSAS.md))_

## Sprint 1 · Esqueleto

- [x] `index.html` gerado pela base comum, perfis Demandante, Equipe e Autoridade, 7 rotas, 7 stores.
- [x] Backup, dados fictícios e `#/testes`.

**Pronto quando**: `python Apps/_base/testar.py tap-portfolio-projetos` passa.

## Sprint 2 · TAP guiado

- [x] Formulário em etapas (identificação, objetivo, alinhamento, custo e prazo, anexos), com instruções em cada campo.
- [x] Campos obrigatórios e tamanhos mínimos (RN01, RN02), com contador.
- [x] Checklist de anexos a partir do store `documentos`; documento ausente exige justificativa (RN03).
- [x] Anexos até 10 MB (RN04), guardados no IndexedDB.
- [x] Lista de pendências antes do envio; rascunho salvo a cada campo.

## Sprint 3 · Pacote e triagem

- [x] Gerar `proposta-<id>.json` com os anexos e o código de verificação.
- [x] Equipe importa o pacote em `#/triagem`, vê o checklist e registra pendência com motivo (RN05) ou aceita (RN06).
- [x] Devolução gera o arquivo de volta para o demandante.

## Sprint 4 · Proposta e decisão

- [ ] `#/proposta/:id`: TAP, anexos, pendências, histórico.
- [ ] Parecer da equipe e decisão da autoridade (aprovação, rejeição, readequação) com autor e data (RN07).

## Sprint 5 · Portfólio

- [ ] Aprovados entram no portfólio; prioridade só com justificativa (RN08).
- [ ] Fonte de recurso e situação da captação.
- [ ] Exportar o portfólio em `.xlsx`.

## Sprint 6 · Indicadores, aceite e piloto

- [ ] Indicadores do `contexto.md`.
- [ ] Roteiro: TAP incompleto bloqueado, pacote importado, pendência devolvida, aprovação, portfólio exportado.
- [ ] Piloto de 60 a 90 dias; comparar com a linha de base e atualizar `PROJETO.md` e `README.md`.
