# Evento de Substituição Temporária · sprints até o MVP

> Arquitetura: HTML monolítico, offline first (ver `contexto.md`). Sprints de 1 semana.

## Andamento

| Sprint | Situação |
|---|---|
| 0 | Dados fictícios gerados em 09/11/2026 (`exemplos/gerar_exemplos.py`), com 15 eventos, 30 autorizações, 8 fichas e 1 publicação. Itens que dependem de pessoas continuam abertos. |
| 1 | Feito em 09/11/2026. Painel, rotas, IndexedDB, perfis e backup. `python testes/testar.py` passa. |
| 2 | Feito em 09/11/2026. Abertura do ofício, motivo e substituto (RN01, RN02), autorizações por nível (RN03) e ficha do evento. Cenário `s1_abertura_e_regras` passa. |
| 3 | Feito em 09/11/2026. Autorização, devolução e reenvio; fila do gestor. Cenário `s2_autorizacao_e_devolucao` passa. |
| 4 | Feito em 09/11/2026. Gabinete, análise de RH e ficha de solicitação (RN04). Cenário `s3_gabinete_rh_e_ficha` passa. |
| 5 | Feito em 09/11/2026. Assinatura do Diretor Geral Adjunto (RN05), envio à SESP e bloqueio depois do dia 05 (RN06). Cenário `s4_assinatura_e_prazo` passa. |
| 6 | Feito em 09/11/2026. Publicação no DO (RN07), encerramento, planilha de controle (RN08), CSV e impressão. Cenário `s5_publicacao_e_planilha` passa. |
| 7 | Feito em 09/11/2026. Roteiro de aceite em `modelos/roteiro-aceite.md`; diagramas AS-IS/TO-BE e `processo.html`. |
| 8 | Feito em 09/11/2026. Ajuste da unidade antes do reenvio e planilha Excel (`.xlsx`) com as abas Controle e Resumo, além do CSV. Cenários `s7_ajuste_e_reenvio` e `s8_planilha_excel` passam. |
| Identidade e usabilidade | Feito em 09/11/2026. Casca de trilho, cabeçalho em degradê, fonte do sistema, densidade ampla, cantos redondos, cartões e KPI em anel, no acento verde-petróleo. A tela-assinatura é a "Minha fila"; a ficha tem a trilha das sete etapas e abas. `python testes/cenarios.py` e `python testes/jornada.py` passam. |

**MVP 100% pronto = Sprints 0 a 7.** O Sprint 8 é o refinamento do aceite:
ajuste da unidade e planilha Excel.

---

## Sprint 0 · Processo e dados

- [ ] Confirmar com a Simone as unidades, as chefias e os níveis de cada linha
      hierárquica. _(premissa em [PREMISSAS.md](../PREMISSAS.md))_
- [ ] Receber o desenho oficial da ficha de solicitação de substituição
      temporária. _(premissa em [PREMISSAS.md](../PREMISSAS.md))_
- [ ] Medir o volume mensal e o tempo de cada etapa no piloto.
- [x] Dados fictícios com semente fixa e datas relativas a hoje.

---

## Sprint 1 · Esqueleto e painel

- [x] `index.html` com as 7 rotas, IndexedDB e backup.
- [x] Painel com eventos em tramitação, aguardando assinatura, na SESP, publicados e fora do prazo.
- [x] Tabela dos próximos do dia 05.
- [x] Perfis em menu suspenso no cabeçalho, trocáveis a qualquer momento.

**Pronto quando**: `python testes/testar.py` passa.

---

## Sprint 2 · Abertura e núcleo do MVP

- [x] Ofício com o número do SIGADOC, a unidade, o substituído, o substituto, o motivo e o período.
- [x] Motivo válido (RN01) e substituto diferente do substituído (RN02).
- [x] Uma autorização por nível da linha hierárquica (RN03).
- [x] Lista de eventos com filtros de situação, motivo, unidade e busca.

**Pronto quando**: `python testes/cenarios.py` passa (cenário `s1_abertura_e_regras`).

---

## Sprint 3 · Autorização hierárquica

- [x] Autorizar e devolver por nível.
- [x] Avançar ao Gabinete quando todas as autorizações terminam.
- [x] Reenviar depois do ajuste da unidade.
- [x] Fila "Minha fila" do gestor hierárquico.

**Pronto quando**: `python testes/cenarios.py` passa (cenário `s2_autorizacao_e_devolucao`).

---

## Sprint 4 · Gabinete e RH

- [x] Gabinete encaminha o evento ao RH.
- [x] RH inclui a ficha de solicitação (RN04).
- [x] O evento segue para assinatura depois da ficha.
- [x] Fila do Gabinete e do RH.

**Pronto quando**: `python testes/cenarios.py` passa (cenário `s3_gabinete_rh_e_ficha`).

---

## Sprint 5 · Assinatura, SESP e prazo

- [x] Fila de assinatura do Diretor Geral Adjunto (RN05).
- [x] Registro do nome, cargo e data da assinatura.
- [x] Envio à SESP dentro do prazo.
- [x] Bloqueio do envio depois do dia 05 e indeferimento com motivo (RN06).

**Pronto quando**: `python testes/cenarios.py` passa (cenário `s4_assinatura_e_prazo`).

---

## Sprint 6 · Publicação e planilha

- [x] Registro do número e da data da publicação no DO (RN07).
- [x] Encerramento só com a publicação.
- [x] Planilha de controle com os cinco campos obrigatórios (RN08).
- [x] CSV com BOM e impressão.

**Pronto quando**: `python testes/cenarios.py` passa (cenário `s5_publicacao_e_planilha`).

---

## Sprint 7 · Aceite e piloto

- [x] Roteiro de aceite em `modelos/roteiro-aceite.md`.
- [x] Diagramas AS-IS e TO-BE em `docs/diagramas/`.
- [x] `processo.html` com o problema, as tabelas, as regras e as métricas.
- [ ] Piloto de 30 dias na Gerência de Suporte à Gestão de Pessoas.

**Pronto quando**: o roteiro de aceite é executado com dados fictícios e o piloto
começa com a linha de base medida.

---

## Sprint 8 · Ajuste da unidade e planilha Excel

- [x] Formulário de ajuste no evento devolvido, com os dados preenchidos.
- [x] Validação do ajuste (RN01, RN02 e número do SIGADOC).
- [x] Reenvio para a autorização com as autorizações zeradas.
- [x] Planilha `.xlsx` com as abas Controle e Resumo, além do CSV.

**Pronto quando**: `python testes/cenarios.py` passa (cenários `s7_ajuste_e_reenvio`
e `s8_planilha_excel`).
