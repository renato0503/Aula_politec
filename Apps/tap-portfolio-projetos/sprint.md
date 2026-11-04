# TAP Digital e Portfólio de Projetos · sprints até o MVP

> Arquitetura: HTML monolítico, offline first (ver `contexto.md`). Sprints de 1 semana.

## Andamento

| Sprint | Situação |
|---|---|
| 0 | Dados fictícios gerados em 29/10/2026. Itens que dependem de pessoas continuam abertos. |
| 1 | Feito em 29/10/2026. `python Apps/_base/testar.py tap-portfolio-projetos` passa. |
| 2 | Feito em 29/10/2026. `python Apps/_base/testar_sprints.py tap-portfolio-projetos` passa (cenário do "Pronto quando"). |
| 3 | Feito em 29/10/2026. `python Apps/_base/testar_sprints.py tap-portfolio-projetos` passa (cenário do Sprint 3 em `Apps/_base/cenarios/sprint3.py`; código em `src/sprint3.js`). |
| 4 | Feito em 30/10/2026. Ficha da proposta, parecer da equipe e decisão da autoridade (RN07); código em `src/sprint4.js`. |
| 5 | Feito em 30/10/2026. Portfólio com prioridade justificada (RN08), fonte de recurso, captação e exportação `.xlsx` (SheetJS em `vendor/`). |
| 6 | Feito em 30/10/2026. Indicadores e roteiro de aceite em `modelos/roteiro-aceite.md`. |
| 8 | Aberto em 03/11/2026 (feedback dos alunos). Ver Sprint 8 abaixo. |

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
| Identidade e usabilidade | Feito em 02/11/2026. Casca de topo, degradê, fonte serifada, densidade ampla, cantos redondos, cartões e KPI em anel; matriz do portfólio (valor × prioridade) com ponto tracejado para a aprovada sem prioridade e tela inicial por perfil (Equipe → Triagem; Autoridade → Portfólio). `python testes/testar.py` e `python testes/cenarios.py` passam. |

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

- [x] `#/proposta/:id`: TAP, anexos, pendências, histórico.
- [x] Parecer da equipe e decisão da autoridade (aprovação, rejeição, readequação) com autor e data (RN07).

## Sprint 5 · Portfólio

- [x] Aprovados entram no portfólio; prioridade só com justificativa (RN08).
- [x] Fonte de recurso e situação da captação.
- [x] Exportar o portfólio em `.xlsx`.

## Sprint 6 · Indicadores, aceite e piloto

- [x] Indicadores do `contexto.md`.
- [x] Roteiro: TAP incompleto bloqueado, pacote importado, pendência devolvida, aprovação, portfólio exportado.
- [x] Piloto de 60 a 90 dias; comparar com a linha de base e atualizar `PROJETO.md` e `README.md`.

## Sprint 7 · Dashboard orçamentário (03/11/2026)

- [x] Loja `orcamentos` (ano, eixo, projeto, empenhado, liquidado) e 15 lançamentos fictícios no seed.
- [x] `#/dashboard` com filtros de ano e eixo, KPIs de empenhado, liquidado, saldo, percentual e lançamentos.
- [x] Barras de empenhado e liquidado por ano e por eixo, e resumo por ano e eixo.
- [x] Formulário para adicionar e editar; cada linha da tabela tem Editar e Excluir.
- [x] Importação de `.xlsx` ou `.csv` com as colunas ano, eixo, empenhado e liquidado; o que já existe (ano + eixo + projeto) é atualizado.
- [x] Exportação CSV do recorte e cenário `s7_dashboard_orcamentario` (8/8).

## Sprint 8 · Correções do feedback (03/11/2026)

> Feedback de Danielle (nota 5).

### Código
- [x] Atualizar os objetivos estratégicos com os objetivos reais do plano estratégico da POLITEC.
- [x] Corrigir o fluxo depois de sanada a pendência: voltar a analisar e enviar para aprovação da autoridade.
- [x] Avisos por e-mail: equipe quando o prazo vencer; demandante quando a pendência for incluída; autoridade quando houver projeto para aprovar.
- [x] Prazo padrão de **5 dias** para todos os casos.

### Decisão do setor
- [ ] Lista oficial dos objetivos estratégicos.
- [ ] Canal de e-mail e textos dos avisos.
- [ ] Confirmar o prazo de 5 dias e a contagem.
- [ ] Testar o fluxo pendência → análise → aprovação com a Danielle.

**Pronto quando**: uma proposta com pendência resolvida volta para a análise e chega à autoridade, e os três avisos disparam.


**Implementado em 03/11/2026**: objetivos editáveis em `#/config` (lista oficial ainda a confirmar); botão de sanar pendências que devolve o TAP à análise; prazo de 5 dias úteis na pendência; fila local de avisos para demandante, equipe e autoridade; cartão de prazos na Triagem. O envio real de e-mail continua como passo a passo de MailApp/Apps Script.
