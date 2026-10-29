# Comissão de Ética · sprints até o MVP

> Arquitetura: HTML monolítico, offline first (ver `contexto.md`). Sprints de 1 semana.

## Andamento

| Sprint | Situação |
|---|---|
| 0 | Categorias iniciais (proposta) e 10 casos fictícios gerados em 29/10/2026. Conferência com a Comissão continua aberta. |
| 1 | Feito em 29/10/2026. `python Apps/_base/testar.py comissao-etica-denuncias` passa. |
| 2 | Feito em 29/10/2026. `python Apps/_base/testar_sprints.py comissao-etica-denuncias` passa. |
| 3 | Feito em 29/10/2026. `python Apps/_base/testar_sprints.py comissao-etica-denuncias` passa (cenário do Sprint 3 em `Apps/_base/cenarios/sprint3.py`; código em `src/sprint3.js`). A classificação é por regras (palavras ligadas às categorias), com o prompt sem nomes para uma IA autorizada; os 10 casos fictícios têm a categoria esperada entre as 3 sugestões. |

## Visão geral

| Sprint | Tema | Entrega verificável |
|---|---|---|
| 0 | Categorias e modelos | Categorias do Código conferidas, modelos de ata, 10 casos fictícios |
| 1 | Esqueleto | `index.html` com perfis, rotas, IndexedDB e backup |
| 2 | Registro da denúncia | Protocolo, partes, relato, anexos e trilha (RN05) |
| 3 | Classificação assistida | Sugestão explicada, prompt sem nomes, confirmação obrigatória (RN02) |
| 4 | Admissibilidade e tramitação | Três vias, prova pendente, etapas e prazos (RN03, RN04) |
| 5 | Oitivas | Roteiro sugerido pela categoria, revisão e termo |
| 6 | Documentos e encerramento | Minutas e encerramento com etapas conferidas |
| 7 | Relatório, aceite e piloto | Relatório sem nomes (RN06), roteiro e piloto de 30 dias |

**MVP 100% pronto = Sprints 0 a 7.**

---

## Sprint 0 · Categorias e modelos

- [ ] Conferir com a Comissão as categorias, os artigos do Código de Ética (LC nº 112/2002) e as palavras de cada categoria.
- [ ] Receber os modelos de ata de reunião, ata de oitiva e relatório de recomendações.
- [x] Gerar 10 casos fictícios (relatos, partes simuladas, categorias esperadas).
- [ ] Linha de base: tempo das reuniões de triagem e da preparação das oitivas nos últimos casos.

## Sprint 1 · Esqueleto

- [x] `index.html` gerado pela base comum, perfis Presidente, Membro e Secretário-executivo, 10 rotas, 7 stores.
- [x] Faixa do topo sobre sigilo e dados fictícios.
- [x] Backup, dados fictícios e `#/testes`.

**Pronto quando**: `python Apps/_base/testar.py comissao-etica-denuncias` passa.

## Sprint 2 · Registro da denúncia

- [x] `#/denuncia/nova`: canal, data de recebimento, denunciante e denunciado (fictícios), relato, anexos até 10 MB.
- [x] Protocolo `CE-AAAA-NNN` gerado na hora.
- [x] Toda ação registra perfil, data, hora e justificativa quando muda dado (RN05).
- [x] `#/painel`: casos por etapa.

**Pronto quando**: um caso fictício é registrado, aparece no painel e o log mostra o registro.

## Sprint 3 · Classificação assistida

- [x] Pontuação do relato pelas palavras de cada categoria; as 3 primeiras sugestões com as palavras que dispararam.
- [x] Prompt pronto, sem os nomes das partes, para ferramenta de IA autorizada; campo para colar a resposta.
- [x] Confirmar ou trocar a categoria, com justificativa (RN02); sem isso o caso não avança.
- [x] Teste: os 10 casos fictícios têm a categoria esperada entre as 3 sugestões.

## Sprint 4 · Admissibilidade e tramitação

- [ ] Três vias: acatada, não acatada (sem enquadramento), encaminhada à corregedoria, com justificativa e membros presentes.
- [ ] Prova pendente: aguardando o denunciante, com prazo (RN04).
- [ ] Oitiva e deliberação só depois da admissibilidade (RN03).
- [ ] Etapas e prazos no painel.

## Sprint 5 · Oitivas

- [ ] Roteiro sugerido pela categoria confirmada e pelos fatos do relato, para revisão do membro.
- [ ] Registro do termo de oitiva e da pessoa ouvida (fictícia).

## Sprint 6 · Documentos e encerramento

- [ ] Minutas preenchidas: comunicação de admissibilidade, ata e relatório de recomendações.
- [ ] Encerramento só com as etapas obrigatórias concluídas.
- [ ] Apagar os dados de um caso encerrado (fica a contagem).

## Sprint 7 · Relatório, aceite e piloto

- [ ] Relatório: casos por etapa, prazos e categorias, sem nomes nem relatos (RN06).
- [ ] Roteiro de aceite do critério da equipe (registrar, classificar, deliberar, roteiro, minutas, encerrar).
- [ ] Piloto de 30 dias com casos fictícios; atualizar `PROJETO.md` e `README.md`.
