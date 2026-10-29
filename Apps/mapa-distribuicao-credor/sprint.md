# Mapa de Distribuição por Credor · sprints até o MVP

> Arquitetura: HTML monolítico, offline first (ver `contexto.md`).
> Cada sprint dura **1 semana** e termina com o `index.html` funcionando no
> Edge, sem internet, com os dados sintéticos.
> A ordem segue as 8 etapas do AS-IS: cada sprint substitui uma ou mais
> planilhas manuais.

## Andamento

| Sprint | Situação |
|---|---|
| 0 | Parte técnica feita em 29/10/2026 (dados fictícios, bibliotecas, modelos). Itens que dependem de pessoas continuam abertos. |
| 1 | Feito em 29/10/2026. `python Apps/_base/testar.py mapa-distribuicao-credor` passa. |
| 2 | Feito em 29/10/2026. `python Apps/_base/testar_sprints.py mapa-distribuicao-credor` passa (cenário do "Pronto quando"). |
| 3 | Feito em 29/10/2026. `python Apps/_base/testar_sprints.py mapa-distribuicao-credor` passa (cenário do Sprint 3 em `Apps/_base/cenarios/sprint3.py`; código em `src/sprint3.js`). |

O `mapa-manual-referencia.xlsx` é calculado por um script independente (Decimal), não à mão; o gabarito manual da equipe continua pendente. Dinheiro em centavos testado (9 testes).

## Visão geral

| Sprint | Tema | Etapas do AS-IS | Entrega verificável |
|---|---|---|---|
| 0 | Regras, gabarito e linha de base | todas | Regras [validar] decididas, dados sintéticos e gabarito manual prontos |
| 1 | Esqueleto do app | | `index.html` com rotas, IndexedDB, SheetJS e backup |
| 2 | Importação das fontes | 1 | As 3 planilhas lidas, com mapeamento de colunas e resumo |
| 3 | Mapa por grupo e item | 2 | Mapa com estimado por órgão igual ao gabarito |
| 4 | Resultado do pregoeiro | 3, 4, 5 | Situação dos grupos e homologado por órgão |
| 5 | Empresas e conferência | 6, 7 | Tabela por empresa e órgão e lista de divergências |
| 6 | Distribuição orçamentária | 8 | Tabela por credor e órgão com ano seguinte |
| 7 | Exportação e auditoria | | `.xlsx` de 8 abas, relatório de divergências, trilha |
| 8 | Aceite e piloto | todas | Diferença zero contra o gabarito e piloto com processo encerrado |

**MVP 100% pronto = Sprints 0 a 8.**

---

## Sprint 0 · Regras, gabarito e linha de base

- [ ] Anexar o `WorkFlow.docx` (exemplos 1 a 8) à pasta e conferir as colunas
      de cada exemplo com o `contexto.md`.
- [ ] Decidir com a equipe e o orçamento os 4 pontos **[validar]** do
      `contexto.md`, seção 6 (homologado por grupo ou item, arredondamento,
      ordem da dotação, grupo misto), e escrever cada regra com um exemplo numérico.
- [ ] Conseguir um relatório do pregoeiro de amostra (sem dado pessoal) e
      anotar o formato (colunas, cabeçalho, linhas de total).
- [x] Montar os dados sintéticos: 3 órgãos, 6 grupos (2 com empresa, 1
      fracassado, 1 deserto, 2 mistos), 30 itens, 4 empresas com CNPJ fictício
      válido e dotações de custeio e investimento.
- [x] Plantar divergências (uma de cada tipo D01 a D08) e listar em `DIVERGENCIAS.md`.
- [ ] Montar à mão, no Excel, o `mapa-manual-referencia.xlsx` (o gabarito).
- [ ] Medir a linha de base em 3 a 6 processos encerrados: horas por etapa,
      divergências achadas e número de planilhas.
- [x] Baixar o SheetJS para `vendor/` e registrar a versão em `VERSOES.md`.

**Pronto quando**: as 4 regras estão escritas e aprovadas, e o gabarito
manual está fechado.

## Sprint 1 · Esqueleto do app

- [x] `index.html` com `<style>` e `<script>` internos e meta CSP sem `connect-src`.
- [x] Roteador por hash com as 9 rotas do `contexto.md`.
- [x] IndexedDB `mapa_distribuicao_v1` com os 7 stores.
- [x] `embutir_libs.py` e SheetJS embutido.
- [x] Funções de dinheiro em centavos: `paraCentavos("1.234,56")`,
      `formatarReais(123456)`, multiplicação e rateio sem perda.
- [x] Botão "Carregar exemplo" com os dados sintéticos embutidos.
- [x] Backup `.json` e `navigator.storage.persist()`.

**Pronto quando**: o exemplo carrega sem internet, e os testes das funções de
dinheiro passam (incluindo `0,1 + 0,2` e números com milhar).

## Sprint 2 · Importação das fontes (etapa 1)

- [x] `#/importar/:proc`: três áreas de arquivo (distribuição, pregoeiro, dotação).
- [x] Ler `.xlsx` e `.csv`, escolher a aba e a linha do cabeçalho.
- [x] Mapeamento de colunas (coluna do arquivo → campo do app), salvo como
      modelo para o próximo processo.
- [x] Validar colunas obrigatórias, tipos e CNPJ (RN07) com a lista de linhas recusadas.
- [x] Resumo do que foi lido: órgãos, grupos, itens, empresas, dotações.
- [x] Gravar a origem (arquivo, aba, linha) de cada registro e a importação na `auditoria`.

**Pronto quando**: as 3 planilhas sintéticas são lidas, e uma planilha sem a
coluna "quantidade" é recusada com a mensagem certa.

## Sprint 3 · Mapa por grupo e item (etapa 2)

- [x] `#/mapa/:proc`: tabela grupo, item, código, descrição, unidade,
      quantidade, valor unitário estimado e total (RN01), com uma coluna de
      quantidade e uma de valor por órgão.
- [x] Subtotais por grupo e total geral.
- [x] Clicar num valor mostra de onde ele veio (arquivo, aba, linha).
- [x] Teste automático: o mapa gerado bate com a aba correspondente do gabarito.

**Pronto quando**: o estimado por órgão e o total geral batem com o gabarito,
centavo a centavo.

## Sprint 4 · Resultado do pregoeiro (etapas 3, 4 e 5)

- [ ] Aplicar a situação de cada grupo (RN02): homologado, fracassado, deserto,
      com a observação padrão.
- [ ] Substituir o estimado pelo homologado (RN03), pela regra decidida no
      Sprint 0 (por item, ou desconto do grupo aplicado aos itens).
- [ ] Grupos fracassados e desertos mantêm as colunas e recebem a observação.
- [ ] `#/resultado/:proc`: resultado geral e por órgão, estimado x homologado e economia.
- [ ] Teste contra o gabarito.

**Pronto quando**: os 6 grupos sintéticos aparecem com a situação certa, e o
resultado por órgão bate com o gabarito.

## Sprint 5 · Empresas e conferência (etapas 6 e 7)

- [ ] `#/empresas/:proc`: tabela por empresa vencedora e órgão participante
      (grupos ganhos, itens, valor).
- [ ] `#/conferencia/:proc`: rodar as divergências D01 a D07 e mostrar por
      nível (bloqueia, alerta, informa), com link para a linha de origem.
- [ ] Bloqueio: a distribuição orçamentária só abre sem divergência que bloqueia,
      ou com a justificativa registrada pelo analista.
- [ ] Teste: todas as divergências de `DIVERGENCIAS.md` são apontadas, e
      nenhuma outra aparece.

**Pronto quando**: as divergências plantadas aparecem, uma a uma, e a tabela
por empresa bate com o gabarito.

## Sprint 6 · Distribuição orçamentária (etapa 8)

- [ ] `#/orcamento/:proc`: tabela por credor e órgão com processo, dotação,
      tipo (3 ou 4), CNPJ e valor.
- [ ] Consumir a dotação de cada órgão e tipo pela ordem decidida no Sprint 0.
- [ ] Excedente vai para a coluna "ano seguinte" (RN05) e gera o aviso D08.
- [ ] Marcar a dotação como validada (nome e data), sem o app decidir nada.
- [ ] Teste contra o gabarito, incluindo um caso de dotação insuficiente.

**Pronto quando**: a tabela orçamentária bate com o gabarito, inclusive a coluna
do ano seguinte.

## Sprint 7 · Exportação e auditoria

- [ ] Exportar `Mapa_Distribuicao_<processo>.xlsx` com as 8 abas, no layout dos
      exemplos 1 a 8, com valores numéricos e formato de moeda.
- [ ] Relatório de divergências para impressão e PDF (`@media print`, A4).
- [ ] `#/auditoria/:proc`: importações, edições (valor anterior e novo) e
      validações, com filtro e exportação CSV.
- [ ] Edição manual de um valor homologado exige justificativa e fica na trilha.

**Pronto quando**: o `.xlsx` abre no Excel com as 8 abas, e uma edição manual
aparece na auditoria com o valor anterior.

## Sprint 8 · Aceite e piloto

- [ ] **Teste de aceite** (critério do aluno): gerar o mapa com os dados
      sintéticos e comparar com o gabarito. A diferença tem que ser **zero**
      (D09), e todas as divergências plantadas, apontadas.
- [ ] Publicar no GitHub Pages só o app e os dados sintéticos.
- [ ] **Piloto**: rodar um processo encerrado (com autorização) e comparar
      totais e tempo com o mapa manual, cronometrando as duas versões.
- [ ] Comparar com a linha de base do Sprint 0 (tempo, divergências, número de planilhas).
- [ ] `LEIA-ME` de uso e atualização de `PROJETO.md` e `README.md`.

**Pronto quando**: diferença zero contra o gabarito e piloto medido.
