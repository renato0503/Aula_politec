# Hórus · Banco de Demandas · sprints até o MVP

> Arquitetura: HTML monolítico, offline first (ver `contexto.md`).
> Cada sprint dura **1 semana**. O aluno já tem o modelo de dados e as regras
> prontos no Hórus, e por isso o plano é mais curto que o dos outros apps.

## Andamento

| Sprint | Situação |
|---|---|
| 0 | Parte técnica feita em 29/10/2026 (dados fictícios, bibliotecas, modelos). Itens que dependem de pessoas continuam abertos. |
| 1 | Feito em 29/10/2026. `python Apps/_base/testar.py horus-banco-demandas` passa. |
| 2 | Feito em 29/10/2026. `python Apps/_base/testar_sprints.py horus-banco-demandas` passa (cenário do "Pronto quando"). |
| 3 | Feito em 29/10/2026. `python Apps/_base/testar_sprints.py horus-banco-demandas` passa (cenário do Sprint 3 em `Apps/_base/cenarios/sprint3.py`; código em `src/sprint3.js`). |

Seed fictício pronto (1 diretoria, 4 unidades, 15 demandas, 3 manifestações, ciclo 2027 ATIVO). Índices únicos de R9 e das inclusões testados.

## Visão geral

| Sprint | Tema | Entrega verificável |
|---|---|---|
| 0 | Decisão e contrato com o Hórus | Papel da versão offline decidido e formato de troca fechado |
| 1 | Esqueleto, perfis e seed | `index.html` com rotas, IndexedDB e dados fictícios |
| 2 | Cadastro da demanda | Formulário com R1 a R6 e anexo do PDF |
| 3 | Grade e ficha | Repositório em cards com filtros e ficha completa |
| 4 | Troca entre unidade e diretoria | Demandas e catálogo circulando por arquivo |
| 5 | Manifestação de interesse | Outra unidade adere ao item (R9) |
| 6 | Ciclo e aprovação | Aprovação com ciclo ATIVO (R7), reabrir item |
| 7 | Relatórios e exportação para o Hórus | Relatórios Geral e Aprovadas, arquivo importado no Hórus |
| 8 | Aceite | Roteiro de aceite cumprido |

**MVP 100% pronto = Sprints 0 a 8.**

---

## Sprint 0 · Decisão e contrato com o Hórus

- [ ] Decidir com o aluno o papel da versão offline: (a) substituir o módulo,
      (b) servir às unidades sem acesso ao Hórus e entregar no formato dele, ou
      (c) ficar como exercício. Proposta: **(b)**. _(premissa em [PREMISSAS.md](../PREMISSAS.md))_
- [ ] Copiar do Hórus o esquema real das 3 tabelas (DDL do Supabase) para
      `horus/esquema.sql` e conferir com o `contexto.md`, seção 5. _(premissa em [PREMISSAS.md](../PREMISSAS.md))_
- [ ] Definir o formato `horus-import-ciclo.json` (versão do esquema, órgão,
      diretoria, ciclo, linhas das 3 tabelas) e o caminho de importação no
      Hórus (tela de importação ou SQL). _(premissa em [PREMISSAS.md](../PREMISSAS.md))_
- [ ] Decidir o relatório: `@media print` ou jsPDF embutido. _(premissa em [PREMISSAS.md](../PREMISSAS.md))_
- [ ] Juntar ao envio os anexos citados (relatório PDF e print da tela). _(premissa em [PREMISSAS.md](../PREMISSAS.md))_

**Pronto quando**: o formato de troca está escrito e o aluno confirmou que o
Hórus consegue importá-lo.

## Sprint 1 · Esqueleto, perfis e seed

- [x] `index.html` com `<style>` e `<script>` internos e meta CSP sem `connect-src`.
- [x] Roteador por hash com as 9 rotas do `contexto.md`.
- [x] IndexedDB `banco_demandas_v1` com os stores e índices únicos (R9 e inclusões).
- [x] Perfil da cópia (6 papéis do aluno), unidade e diretoria em `#/config`.
- [x] Seed fictício: 1 órgão, 1 diretoria, 4 unidades, unidades de medida,
      1 ciclo ATIVO e 15 demandas (reagentes, EPIs, equipamentos de laboratório).
- [x] Backup `.json` e `navigator.storage.persist()`.

**Pronto quando**: o seed carrega, e cada perfil vê o menu certo.

## Sprint 2 · Cadastro da demanda

- [x] Formulário "Nova demanda" com grupo, unidade, especificação, valor,
      quantidade, unidade de medida, links, justificativa e PDF.
- [x] Validações R1, R2, R3, R5 e R6 na tela, com contador de caracteres.
- [x] `valor_global` calculado na hora (R4), em reais.
- [x] PDF guardado como Blob, com abertura em nova aba.
- [x] Editar e excluir respeitando R8 (criador, ADM ou Diretor), com `log`.

**Pronto quando**: uma demanda com justificativa de 99 caracteres é recusada, e
com 100 é salva com o valor global certo.

## Sprint 3 · Grade e ficha

- [x] `#/banco`: grade de cards "Banco de Demandas · repositório (N)".
- [x] Filtros por grupo, unidade, situação (livre, com interesse, aprovada no ciclo) e busca.
- [x] Ficha da demanda com anexo, links (título informado), manifestações e
      ciclos em que entrou.
- [x] Selo "Aprovada no ciclo <ano>" no card.

**Pronto quando**: os 15 itens do seed aparecem, e os filtros somam o total certo.

## Sprint 4 · Troca entre unidade e diretoria

- [ ] Unidade: exportar `demandas-<unidade>.json` (com ou sem PDFs).
- [ ] Diretoria: importar e mesclar por `id` e `updated_at`, com relatório de
      novos, atualizados e conflitos.
- [ ] Diretoria: exportar `catalogo-<diretoria>.json` para as unidades.
- [ ] Recusar arquivo de outra diretoria ou de outro órgão.
- [ ] Revalidar R1 a R6 em toda importação.

**Pronto quando**: duas cópias de unidade, alteradas em paralelo, são
consolidadas sem duplicar item, e o catálogo volta para elas.

## Sprint 5 · Manifestação de interesse

- [ ] Botão "Manifestar interesse" no card de outra unidade (some no da própria).
- [ ] Quantidade > 0 e justificativa ≥ 50 caracteres.
- [ ] Uma manifestação por unidade e item (R9). Uma segunda edita a primeira.
- [ ] Exportar `manifestacao-<unidade>.json` e importar na diretoria.
- [ ] Quantidade total do item (própria + manifestações) visível no card.

**Pronto quando**: a unidade B adere ao item da unidade A, e a diretoria vê a
manifestação depois de importar o arquivo.

## Sprint 6 · Ciclo e aprovação

- [ ] `#/ciclos`: cadastrar ciclos e marcar um como ATIVO (só um por vez).
- [ ] `#/aprovar`: selecionar demandas e aprovar, só com ciclo ATIVO (R7).
- [ ] Coordenador aprova só itens das unidades que gerencia.
- [ ] Registrar a inclusão (`banco_demanda_inclusoes`) com aprovador e data.
- [ ] Reabrir item: desfaz a inclusão no ciclo ativo, com motivo no `log`.
- [ ] Item aprovado ganha o selo "Aprovada no ciclo".

**Pronto quando**: sem ciclo ativo o botão de aprovar fica bloqueado, e com
ciclo ativo a aprovação gera a inclusão.

## Sprint 7 · Relatórios e exportação para o Hórus

- [ ] Relatório **Geral**: KPIs (total, valor global, por grupo, unidades,
      reuso) e uma ficha por demanda.
- [ ] Relatório **Aprovadas**: só as inclusões do ciclo ativo.
- [ ] Gerar em PDF (impressão ou jsPDF, conforme o Sprint 0), em A4.
- [ ] Exportar `horus-import-ciclo.json` (e CSV por tabela) no formato do Sprint 0.
- [ ] Importar o arquivo no Hórus de teste e conferir a demanda APROVADO no Kanban.

**Pronto quando**: a demanda aprovada offline aparece como APROVADO no Kanban
do Hórus e no relatório "Aprovadas".

## Sprint 8 · Aceite

- [ ] **Roteiro de aceite** (do piloto do aluno):
  1. Abrir o `index.html` sem internet, perfil Usuário setorial.
  2. Cadastrar uma demanda válida com PDF.
  3. Exportar e consolidar na diretoria.
  4. Outra unidade manifesta interesse.
  5. O diretor aprova para o ciclo ATIVO.
  6. O relatório "Aprovadas" mostra o item.
  7. O arquivo exportado entra no Hórus e o item aparece no Kanban.
- [ ] Acessibilidade básica (rótulos, teclado, contraste).
- [ ] `LEIA-ME` de uso e atualização de `PROJETO.md` e `README.md`.

**Pronto quando**: os 7 passos passam, sem ajuda, com os dados fictícios.
