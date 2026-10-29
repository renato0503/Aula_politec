# Mapa de Equipamentos POLITEC · sprints até o MVP

> Arquitetura: HTML monolítico, offline first (ver `contexto.md`).
> Cada sprint dura **1 semana** e termina com o `index.html` abrindo e
> funcionando no Edge, com os dados fictícios.
> O Sprint 0 é maior que os outros porque o formulário chegou incompleto: sem
> ele, o resto do plano constrói em cima de suposições.

## Andamento

| Sprint | Situação |
|---|---|
| 0 | Parte técnica feita em 29/10/2026 (dados fictícios, bibliotecas, modelos). Itens que dependem de pessoas continuam abertos. |
| 1 | Feito em 29/10/2026. `python Apps/_base/testar.py equipamentos-google-earth` passa. |
| 2 | Feito em 29/10/2026. `python Apps/_base/testar_sprints.py equipamentos-google-earth` passa (cenário do "Pronto quando"). |
| 3 | Feito em 29/10/2026. `python Apps/_base/testar_sprints.py equipamentos-google-earth` passa (cenário do Sprint 3 em `Apps/_base/cenarios/sprint3.py`; código em `src/sprint3.js`). |

Malha do IBGE: 141 polígonos para 142 municípios (Boa Esperança do Norte, criado em 2023, ainda sem polígono). Coordenada da unidade = centroide do município.

## Visão geral

| Sprint | Tema | Entrega verificável |
|---|---|---|
| 0 | Descoberta e escopo | `PROJETO.md` completo, escopo validado, lista de unidades e planilha atual em mãos |
| 1 | Esqueleto do app | `index.html` com rotas, IndexedDB, backup `.json` |
| 2 | Unidades e base de MT | Unidades cadastradas com município e coordenadas validadas |
| 3 | Equipamentos e fotos | Cadastro com fotos comprimidas e ficha do equipamento |
| 4 | Contratos e manutenções | Contratos vigentes, alertas e histórico com comprovantes |
| 5 | Paradas e custo | Paradas registradas, custo de parada e risco calculados |
| 6 | Mapa offline de MT | Pinos por risco e filtros no mapa, sem internet |
| 7 | Painel de KPIs | Indicadores por unidade e diretoria |
| 8 | Exportação para o Google Earth | `.kmz` abrindo no Google Earth com fotos e balões |
| 9 | Importação e consolidação | Planilha atual importada e arquivos das unidades mesclados |
| 10 | Acessibilidade, LGPD e relatório | Navegação por teclado, contraste AA, relatório impresso |
| 11 | Aceite e piloto de 30 dias | Roteiro de aceite cumprido e piloto aberto |

**MVP 100% pronto = Sprints 0 a 11.**

---

## Sprint 0 · Descoberta e escopo

**Objetivo**: completar o que o formulário deixou em branco, com o João e a
coordenadora.

- [ ] Ler o `contexto.md` com a coordenadora e marcar cada **[validar]** como
      aceito, alterado ou recusado.
- [ ] Preencher de novo no formulário (importando o `projeto.json`) as seções
      MVP, papéis, entidades, regras, telas e KPIs, com o escopo validado.
- [ ] **Retirar o número de 11 dígitos** do campo "dados pessoais tratados".
- [ ] Levantar a lista de diretorias e unidades da POLITEC com município de cada uma.
- [ ] Reunir a planilha que existe hoje ("parcialmente", segundo o formulário)
      e anotar as colunas.
- [ ] Definir com a coordenadoria o `valor_referencia_atendimento` e o custo
      alternativo padrão (terceirização, deslocamento para outra unidade).
- [ ] Escolher 3 unidades para o piloto e medir a linha de base: quantos
      equipamentos estão sem contrato, quantas paradas houve no último trimestre
      e quanto tempo levou para responder "quanto custa essa parada?".
- [x] Baixar a malha municipal de MT do IBGE, simplificar no mapshaper e salvar
      em `dados-base/`. Montar `mt-municipios.csv` (código, nome, lat, long).
- [x] Baixar o JSZip para `vendor/` e registrar a versão em `VERSOES.md`.
- [x] Escrever `exemplos/seed-ficticio.json`: 3 diretorias, 12 unidades
      fictícias em municípios reais, 150 equipamentos, 20 contratos, 200
      manutenções e 40 paradas.

**Pronto quando**: a coordenadora assinou o escopo (pode ser por e-mail) e o
`PROJETO.md` não tem mais campos com "1" nem "Sem informação" nas seções 2 a 7.

## Sprint 1 · Esqueleto do app

- [x] `index.html` com `<style>` e `<script>` internos, sem recurso externo.
- [x] Meta CSP: `default-src 'self' 'unsafe-inline' data: blob:; connect-src 'none'`.
- [x] Roteador por hash com as 10 rotas do `contexto.md` (telas vazias).
- [x] Camada `db` sobre IndexedDB (`equipamentos_politec_v1`) com os 8 stores.
- [x] Todo registro ganha `id`, `criadoEm`, `atualizadoEm`, `origem`, `excluido`.
- [x] `navigator.storage.persist()` e indicador de espaço usado.
- [x] Exportar e importar backup `.json` completo.
- [x] Botão "Carregar dados fictícios" que lê o seed embutido.
- [x] Tema claro e escuro com variáveis CSS.
- [x] `embutir.py` funcionando para `vendor/` e `dados-base/`.

**Pronto quando**: o seed carrega, o navegador fecha e reabre com os dados, e o
DevTools mostra zero requisições de rede.

## Sprint 2 · Unidades e base de MT

- [x] `#/unidades`: cadastro de diretorias e unidades.
- [x] Município escolhido numa lista com busca (os 142 municípios embutidos).
      A coordenada da sede do município entra como padrão.
- [x] Ajuste manual de latitude e longitude, recusando ponto fora de MT (RN08):
      teste de ponto dentro do polígono do contorno do estado.
- [x] Campos de referência da unidade: horas úteis por dia e atendimentos por dia.
- [x] Exclusão lógica (não apaga, marca `excluido`).

**Pronto quando**: as 12 unidades do seed aparecem com coordenadas, e uma
coordenada de Goiânia é recusada.

## Sprint 3 · Equipamentos e fotos

- [x] `#/equipamentos`: lista com busca, filtros (unidade, tipo, status,
      criticidade) e ordenação.
- [x] Formulário do equipamento com os campos do `contexto.md`, seção 5.
- [x] Fotos: escolher arquivo ou câmera (`<input accept="image/*" capture>`),
      reduzir para 1280 px, JPEG 0,75, gerar miniatura de 240 px, guardar em `arquivos`.
- [x] `#/equipamento/:id`: ficha com galeria, dados e blocos vazios de contrato,
      manutenções e paradas (preenchidos nos próximos sprints).
- [x] Patrimônio único: alerta de duplicado.
- [x] Exportar a lista em CSV (UTF-8 com BOM, `;`).

**Pronto quando**: cadastrar um equipamento com 3 fotos de celular (cerca de 4 MB
cada) ocupa menos de 1 MB no IndexedDB, e a ficha mostra as fotos.

## Sprint 4 · Contratos e manutenções

- [ ] `#/contratos`: cadastro com fornecedor, vigência, valor mensal, SLA e
      seleção dos equipamentos cobertos.
- [ ] Cálculo de contrato vigente (RN05) e alerta de 60 dias para o vencimento.
- [ ] Registro de manutenção (preventiva ou corretiva) na ficha, com custo,
      fornecedor e **comprovante** anexado (PDF ou imagem, até 2 MB).
- [ ] Histórico em linha do tempo na ficha.
- [ ] MTTR por equipamento (RN06).

**Pronto quando**: um contrato vencido some da cobertura no mesmo dia, e a ficha
mostra o histórico com o comprovante abrindo em nova aba.

## Sprint 5 · Paradas, custo e risco

- [ ] `#/paradas`: abrir parada (equipamento, início, motivo) e fechar (fim).
- [ ] Status do equipamento muda para **parado** enquanto a parada está aberta.
- [ ] Funções de cálculo isoladas e testadas em `testes/testes.html`:
      `custoDiarioParada` (RN02), `custoParada` (RN03), `risco` (RN04),
      `pontoUnicoDeFalha` (RN01), `disponibilidade` (RN07).
- [ ] `#/config`: parâmetros de custo editáveis, com data da última alteração.
- [ ] Na ficha: custo diário estimado, custo acumulado das paradas e a fórmula
      com os valores usados.

**Pronto quando**: os testes de cálculo estão verdes, e abrir uma parada em um
ponto único de falha sem contrato muda o risco para **alto** na ficha.

## Sprint 6 · Mapa offline de MT

- [ ] Desenhar o contorno de MT e os municípios em SVG a partir do GeoJSON embutido.
- [ ] Pinos agrupados por unidade, na cor do maior risco, com o número de equipamentos.
- [ ] Zoom (roda do mouse e botões) e arrasto via `viewBox`.
- [ ] Filtros: sem contrato, parados, ponto único de falha, diretoria, tipo.
- [ ] Clique no pino: painel lateral com os equipamentos da unidade e o link para a ficha.
- [ ] Legenda das cores e do tamanho dos pinos.
- [ ] Tabela equivalente abaixo do mapa (acessibilidade).

**Pronto quando**: com o Wi-Fi desligado, o mapa mostra as 12 unidades do seed e
o filtro "sem contrato" reduz os pinos de acordo.

## Sprint 7 · Painel de KPIs

- [ ] `#/painel`: os 7 KPIs do `contexto.md`, seção 8, com o período selecionável.
- [ ] Ranking de unidades e de diretorias por custo de parada.
- [ ] Lista dos pontos únicos de falha sem contrato, ordenada pela exposição diária.
- [ ] Gráfico de barras em SVG próprio (custo de parada por unidade) e linha
      (paradas por mês). Sem biblioteca externa.
- [ ] Cada número mostra a fórmula e os parâmetros ao passar o mouse.
- [ ] Clique num KPI filtra o mapa.

**Pronto quando**: os KPIs do seed batem com a conta feita à mão numa planilha
para 2 unidades.

## Sprint 8 · Exportação para o Google Earth

- [ ] Gerar o KML: pastas por diretoria e unidade, um *Placemark* por
      equipamento, estilos por faixa de risco.
- [ ] Balão com miniatura da foto, patrimônio, status, contrato, custo diário e risco.
- [ ] Empacotar KML e miniaturas em `.kmz` com JSZip.
- [ ] Opção de exportar só o filtro atual (ex.: só os sem contrato).
- [ ] Testar no Google Earth Pro e no Google Earth Web.

**Pronto quando**: o `.kmz` do seed abre nos dois, com as pastas, as cores e as
fotos nos balões.

## Sprint 9 · Importação e consolidação

- [ ] Importar a planilha atual em CSV, com tela de associação de colunas
      (coluna da planilha → campo do app) e prévia das 10 primeiras linhas.
- [ ] Relatório da importação: linhas aceitas, recusadas e o motivo.
- [ ] Importar o `.json` de uma unidade e mesclar (RN10): novos, atualizados,
      excluídos e conflitos.
- [ ] Tela de conflitos: escolher a versão da unidade ou a da coordenadoria.
- [ ] Exportar `.json` com ou sem fotos.
- [ ] `#/config`: escolher o perfil da cópia (unidade ou coordenadoria) e a
      unidade dona.

**Pronto quando**: duas cópias do app, alteradas em paralelo, são mescladas na
coordenadoria sem duplicar nenhum equipamento.

## Sprint 10 · Acessibilidade, LGPD e relatório

- [ ] Navegação completa por teclado (tab, enter, esc) e foco visível.
- [ ] Contraste AA nos temas claro e escuro, conferido no DevTools (Lighthouse).
- [ ] `aria-label` em botões de ícone e `<label>` em todos os campos.
- [ ] Relatório impresso (`@media print`): resumo dos KPIs, pontos únicos de
      falha sem contrato e lista por unidade, em A4.
- [ ] Varredura de dados pessoais: aviso se algum campo de texto livre tiver
      padrão de CPF (RN09).
- [ ] Texto de privacidade em `#/config` e botão "limpar dados desta cópia".

**Pronto quando**: o Lighthouse marca acessibilidade 90 ou mais, e o relatório
impresso cabe em A4 sem cortar tabela.

## Sprint 11 · Aceite e piloto de 30 dias

- [ ] Rodar o **roteiro de aceite** com a coordenadora:
  1. Abrir o `index.html` por duplo clique, sem internet.
  2. Importar a planilha atual das 3 unidades do piloto.
  3. Completar fotos e contratos de 10 equipamentos.
  4. Registrar uma parada e conferir o custo no painel.
  5. Filtrar os sem contrato no mapa.
  6. Exportar o `.kmz` e abrir no Google Earth.
  7. Mesclar o `.json` de uma unidade.
  8. Imprimir o relatório.
- [ ] Corrigir o que o roteiro apontar.
- [ ] `LEIA-ME` de uso em uma página (como abrir, fazer backup e enviar o `.json`).
- [ ] Abrir o **piloto de 30 dias** (pedido no formulário) nas 3 unidades, com
      backup semanal enviado à coordenadoria.
- [ ] No fim do piloto, comparar com a linha de base do Sprint 0: equipamentos
      sem contrato identificados, paradas registradas e tempo para responder
      "quanto custa essa parada?".
- [ ] Atualizar o `PROJETO.md` (marcos, defesa) e o `README.md` da pasta.

**Pronto quando**: a coordenadora cumpre os 8 passos sem ajuda, e o piloto está aberto.
