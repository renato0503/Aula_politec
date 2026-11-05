# TCIN · sprints até o MVP

> Arquitetura: HTML monolítico, offline first (ver `contexto.md`). Sprints de 1 semana.

## Andamento

| Sprint | Situação |
|---|---|
| 0 | Dois envios parciais e um protótipo recebidos em 29/10/2026. Dados fictícios gerados em `exemplos/gerar_exemplos.py`. Itens que dependem de pessoas continuam abertos. |
| 1 | Feito em 29/10/2026. `python Apps/_base/testar.py trilha-custodia-necropsia` passa. |
| 2 | Feito em 29/10/2026. `python Apps/_base/testar_sprints.py trilha-custodia-necropsia` passa (cenário em `Apps/_base/cenarios/sprint2.py`). |
| 3 | Feito em 30/10/2026. `python Apps/_base/testar_sprints.py trilha-custodia-necropsia` passa (cenário do Sprint 3 em `Apps/_base/cenarios/sprint3.py`; código em `src/sprint3.js`). |
| 4 | Feito em 30/10/2026. Auto de entrega com responsável, documento e data, bloqueio sem identificação (RN02) e trilha da liberação; código em `src/sprint4.js`. |
| 5 | Feito em 30/10/2026. Tempo médio de remoção, identificação e liberação, permanência por corpo e alerta de passagem de plantão (12 h sem movimentação). |
| 6 | Feito em 30/10/2026. CSV e impressão em A4, botão de apagar caso liberado com contagem e texto de privacidade em `modelos/privacidade.md`. |
| 7 | Feito em 30/10/2026. Roteiro de aceite em `modelos/roteiro-aceite.md`. |
| 8 | Feito em 03/11/2026, a partir da versão de 02/11/2026 em `entregas/2026-11-02/`. Sete etapas no caso, resultado da identificação, busca de familiares, liberação com assinatura no canvas, sepultamento pelo Estado com justificativa, entrega e recebimento do laudo, confirmação de lacre só pelo Gestor ADM, leitura auditada, perfil Médico Legista (leitura até a etapa 5) e `#/resumo` por agente causal. |
| 9 | Feito em 05/11/2026. Três perfis (Técnico, Médico Legista e Gestor ADM), exame complementar (RN11), sepultamento pelo Estado só pelo Gestor ADM (RN09), laudo em paralelo, encerramento com três condições (RN10) e retificação (RN12). |
| 10 | Feito em 05/11/2026. O app passa a ser o **espelho do protótipo** "Sistema de Controle de Necropsia — DMML / POLITEC" (`Ncropsis/` na raiz do repositório): faixa de cabeçalho navy, painel de dez indicadores, lista de corpos com filtros e gaveta lateral, resumo por agente causal e ficha do caso com as sete etapas, assinatura no canvas e janela de justificativa. Os dados fictícios são os dez corpos do protótipo. |

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
| Identidade e usabilidade | Feito em 02/11/2026. Casca de trilho, cabeçalho sólido, fonte condensada, densidade ampla, cantos suaves, superfícies planas e KPI em número; painel por perfil (4 perfis), quadro de plantão em colunas por situação com cartões de corpo e dias no IML, e ficha em abas. `python testes/testar.py` e `python testes/cenarios.py` passam. |

**MVP 100% pronto = Sprints 0 a 8.**

---

## Sprint 0 · Processo e dados

- [ ] Confirmar com a aluna e o IML o nome do projeto (CNC ou TCIN). _(premissa em [PREMISSAS.md](../PREMISSAS.md))_
- [ ] Validar os quatro marcos e os livros que o app substitui. _(premissa em [PREMISSAS.md](../PREMISSAS.md))_
- [ ] Medir a linha de base de remoção, identificação e liberação. _(premissa em [PREMISSAS.md](../PREMISSAS.md))_
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

- [x] Mudança de situação (em custódia, aguardando, não identificado, não reclamado).
- [x] `#/busca` por protocolo, nome ou documento (RN04).
- [x] Lista do painel sem nome completo (RN05).

**Pronto quando**: `python Apps/_base/testar_sprints.py trilha-custodia-necropsia` passa (cenário do Sprint 3).

---

## Sprint 4 · Liberação

- [x] Auto de entrega com responsável, data e documento.
- [x] Bloqueio de liberação sem identificação e sem auto (RN02).
- [x] Trilha da liberação.

## Sprint 5 · Painel do gestor

- [x] Tempo de remoção, de identificação e de liberação.
- [x] Corpos não reclamados por tempo de permanência.
- [x] Alertas de passagem de plantão.

## Sprint 6 · Relatório e retirada

- [x] Relatório em CSV e impressão em A4.
- [x] Botão para apagar os dados de um caso encerrado.
- [x] Texto de privacidade e retenção.

## Sprint 7 · Aceite e piloto

- [x] Roteiro de aceite com o IML.
- [x] Piloto de 30 dias com casos fictícios.
- [x] Atualizar `PROJETO.md` e `README.md`.

## Sprint 8 · Controle de necropsia (versão de 02/11/2026)

- [x] Sete etapas no caso (acionamento, ocorrência, fila da necropsia, necropsia, identificação, família e liberação, entrega do laudo à ADM).
- [x] Resultado da identificação: identificado, não identificado e óbito administrativo.
- [x] Busca de familiares com registro de início, familiar localizado ou busca sem êxito.
- [x] Liberação à família com assinatura capturada no canvas e Auto de Entrega.
- [x] Sepultamento pelo Estado com justificativa de no mínimo 20 caracteres e funerária.
- [x] Entrega do laudo à ADM e confirmação de recebimento exclusiva do Gestor ADM, com assinatura.
- [x] Confirmação de recebimento de lacre exclusiva do Gestor ADM.
- [x] Perfil Médico Legista: leitura até a etapa 5, sem edição e sem as etapas 6 e 7.
- [x] Auditoria de leitura (consulta ao caso) e `#/resumo` por agente causal.
- [x] Dados fictícios atualizados (etapa, agente causal, família, laudo, sepultamento e lacres recebidos).
- [x] Cenário `s8_sete_etapas_assinatura_e_recebimento` (14/14).
- [ ] Confirmar com o IML as regras de recebimento e de sepultamento (ver `Apps/PREMISSAS.md`).

## Sprint 9 · Fluxograma da Silmara e três perfis (05/11/2026)

Entrada: `entregas/2026-11-05/` (fluxograma, protótipo e `PROJETO.md` da aluna).

- [x] Só três perfis: Técnico, Médico Legista e Gestor ADM (saem o Operador do CIOP e o Plantonista).
- [x] Nome do app: Sistema de Controle de Necropsia.
- [x] Identificação com laço de exame complementar (DNA, odontologia legal, antropologia forense) e tentativas registradas (RN11).
- [x] Sepultamento pelo Estado só por decisão do Gestor ADM, com justificativa, número da autorização e funerária (RN09).
- [x] Funerária e Auto de Entrega também na liberação à família.
- [x] Laudo em paralelo a partir da etapa 5 e encerramento com destino, laudo e lacres confirmados (RN10).
- [x] Caso encerrado travado e retificação com tipo, texto e motivo (RN12).
- [x] Atalhos antigos de liberação (situação manual e auto do Sprint 4) fechados.
- [x] Painéis: quadro das sete etapas (Técnico), sala de necropsia (Médico Legista) e fila da ADM (Gestor ADM).
- [x] TO-BE em `docs/diagramas/to-be.manual.mmd`, com SVG e `processo.html` regerados.
- [x] Cenário `s9_fluxograma_da_silmara` (21/21) e cenários antigos ajustados.
- [ ] Confirmar com a Silmara e o IML os exames complementares, o laudo em paralelo e os tipos de retificação (ver `Apps/PREMISSAS.md`, seção 20).

**Pronto quando**: `python testes/cenarios.py` passa nos sete cenários.

## Sprint 10 · Espelho do protótipo DMML / POLITEC (05/11/2026)

Entrada: o protótipo "Sistema de Controle de Necropsia — DMML _ POLITEC.html", em
`Ncropsia/` na raiz do repositório. O app passa a ter a mesma cara e o mesmo
comportamento, campo a campo.

- [x] Faixa de cabeçalho navy com o perfil de acesso e a marca de protótipo.
- [x] Painel com os dez indicadores do protótipo (casos totais, ocorrência em
      andamento, aguardando necropsia, necropsia em andamento, aguardando
      identificação, aguardando família, aguardando funerária, sepultados pelo
      Estado, custódia finalizada e lacres pendentes de recebimento). Clicar no
      indicador filtra a lista.
- [x] Lista de corpos com busca, filtro de situação, período, contagem e cartões
      no celular. O botão "Ver detalhes" abre a **gaveta lateral** com a ficha.
- [x] Ficha do caso com o stepper das sete etapas e os blocos do protótipo:
      acionamento, ocorrência e possível vítima, alocação na base, necropsia com
      os quatro materiais lacrados, identificação, família e liberação,
      funerária e entrega do laudo à ADM. Mais encerramento, retificações e
      histórico.
- [x] Assinatura no canvas (familiar e quem recebe o laudo) e janela de
      justificativa para o sepultamento pelo Estado.
- [x] Resumo por agente causal com as seis colunas do protótipo e o total geral.
- [x] Dados fictícios: os dez corpos do protótipo (000123/2026 a 000132/2026),
      com os quatro materiais por caso e o histórico.
- [x] Regras mantidas: RN01 (protocolo único), RN02 (liberação exige
      identificação, assinatura e documento), RN03 (marcos), RN04 (busca), RN05
      (iniciais fora da ficha), RN09 (sepultamento só pelo Gestor ADM), RN10
      (encerramento com destino, laudo e lacres), RN11 (exame complementar) e
      RN12 (retificação).
- [ ] Confirmar com a Silmara e o IML os campos do protótipo que o app assume
      (chegada ao local, câmara e gaveta, estado do corpo, materiais da
      necropsia e o escopo de cada perfil).

**Pronto quando**: `python testes/cenarios.py` passa nos nove cenários e o
resumo por agente causal bate com o protótipo (10 corpos; 2 para a família, 1
sepultado pelo Estado, 6 aguardando identificação, 1 não reclamado e 1 com
custódia finalizada).

