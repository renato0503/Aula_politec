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
| 4 | Feito em 03/11/2026: tela de contratos com vigência, alerta de 60 dias (RN05) e a ficha do equipamento com histórico, MTTR (RN06) e custo. Cenário `s4_contratos` passa. |
| 5 | Feito em 03/11/2026: paradas com abertura e fechamento, equipamento parado enquanto a parada está aberta, custo diário (RN02) e custo acumulado (RN03). Cenário `s5_paradas` passa. |
| 6 | Feito em 03/11/2026: mapa com zoom (roda e botões), arrasto, filtros por contrato, parada, ponto único, diretoria e tipo, pinos coloridos por risco, painel lateral no pino e tabela equivalente. Cenário `s6_mapa_e_municipio` passa. |
| 7 | Feito em 03/11/2026: painel com os 7 indicadores, período selecionável, ranking por custo de parada e a lista de pontos únicos de falha sem contrato. Cenário `s7_painel` passa. |
| 8 | Feito em 03/11/2026: KML com pastas por diretoria e unidade, `.kmz` com JSZip, opção de exportar só os sem contrato, JSON da base e CSV. Cenário `s8_exportar` passa. |
| 10 | Feito em 03/11/2026 (`src/sprint6.js` e `src/sprint4.js`): parâmetros de custo com data da alteração, unidade dona da cópia, `.json` com ou sem fotos, gráficos de barras e de linha em SVG, fórmula no hover dos KPIs, KPI que abre o mapa filtrado, aviso de CPF antes de salvar (RN09), texto de privacidade, foto no balão do `.kmz` e tela de conflitos campo a campo na mesclagem. Acessibilidade conferida por varredura no Playwright (rótulos, nome dos botões e contraste AA nos dois temas) e pelo Lighthouse (100 em 03/11/2026). O `.kmz` é validado no esquema OGC KML 2.2 pelo cenário `s8_kml_valido`. Cenários `s10_config_e_graficos` (7/7) e `s9_conflitos` (4/4) passam. Falta abrir o `.kmz` no Google Earth Pro e Web (manual) e o Sprint 11 (aceite e piloto). |
| 9 | Feito em 03/11/2026: importação da planilha em CSV com relatório de aceitas e recusadas, e mesclagem do `.json` de uma unidade com escolha de versão (RN10). Cenário `s9_importar` passa. |
| 12 | Aberto em 03/11/2026 (feedback dos alunos). Ver Sprint 12 abaixo. |

Malha do IBGE: 141 polígonos para 142 municípios (Boa Esperança do Norte, criado em 2023, ainda sem polígono). Coordenada da unidade = centroide do município.

### Divisão por distritos (03/11/2026)

A divisão por bairros veio do IBGE (`dados-base/mt-distritos.json`, gerado por
`dados-base/gerar_distritos.py`): 258 distritos em 141 dos 142 municípios. Clicar
no município no mapa abre `#/municipio/<código>`, com a lista de distritos, as
unidades do app naquele município e a busca de equipamento por bairro (campo
"bairro" da ficha do equipamento).

O IBGE publica **distritos**, e não bairros: Cuiabá aparece com 7 distritos, e não
com os bairros da cidade. Bairro de verdade vem de lei municipal, sem base
estadual aberta, por isso o campo se chama "Bairro (distrito)".

**Decisão pendente (para 04/11/2026)**: colocar um mapa de fundo real (ruas e
satélite) dentro do app. Hoje o mapa real chega por fora: `.kmz` (Google Earth),
GeoJSON (QGIS, ArcGIS, Google Earth Engine) e o link "Abrir no Google Maps". O
Google Earth Engine analisa imagem de satélite e não serve de base do app. A
opção indicada é Leaflet em `vendor/` com tiles do OpenStreetMap, como camada
opcional ligada só com internet, porque o app é offline first e o `testar.py`
cobra zero requisição de rede.

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
| Identidade e usabilidade | Feito em 02/11/2026. Casca de ferramenta, cabeçalho compacto, fonte do sistema, densidade compacta, cantos suaves, superfícies planas e KPI em número; mapa de MT em SVG com os 142 municípios do arquivo embutido e os pinos das unidades (o número é a quantidade de equipamentos), e o perfil Unidade com o contexto de unidade. `python testes/testar.py` e `python testes/cenarios.py` passam. |

**MVP 100% pronto = Sprints 0 a 11.**

---

## Sprint 0 · Descoberta e escopo

**Objetivo**: completar o que o formulário deixou em branco, com o João e a
coordenadora.

- [ ] Ler o `contexto.md` com a coordenadora e marcar cada **[validar]** como
      aceito, alterado ou recusado. _(premissa em [PREMISSAS.md](../PREMISSAS.md))_
- [ ] Preencher de novo no formulário (importando o `projeto.json`) as seções
      MVP, papéis, entidades, regras, telas e KPIs, com o escopo validado. _(premissa em [PREMISSAS.md](../PREMISSAS.md))_
- [ ] **Retirar o número de 11 dígitos** do campo "dados pessoais tratados". _(premissa em [PREMISSAS.md](../PREMISSAS.md))_
- [ ] Levantar a lista de diretorias e unidades da POLITEC com município de cada uma. _(premissa em [PREMISSAS.md](../PREMISSAS.md))_
- [ ] Reunir a planilha que existe hoje ("parcialmente", segundo o formulário)
      e anotar as colunas. _(premissa em [PREMISSAS.md](../PREMISSAS.md))_
- [ ] Definir com a coordenadoria o `valor_referencia_atendimento` e o custo
      alternativo padrão (terceirização, deslocamento para outra unidade). _(premissa em [PREMISSAS.md](../PREMISSAS.md))_
- [ ] Escolher 3 unidades para o piloto e medir a linha de base: quantos
      equipamentos estão sem contrato, quantas paradas houve no último trimestre
      e quanto tempo levou para responder "quanto custa essa parada?". _(premissa em [PREMISSAS.md](../PREMISSAS.md))_
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

- [x] `#/contratos`: cadastro com fornecedor, vigência, valor mensal, SLA e
      seleção dos equipamentos cobertos.
- [x] Cálculo de contrato vigente (RN05) e alerta de 60 dias para o vencimento.
- [x] Registro de manutenção (preventiva ou corretiva) na ficha, com custo,
      fornecedor e **comprovante** anexado (PDF ou imagem, até 2 MB).
- [x] Histórico em linha do tempo na ficha.
- [x] MTTR por equipamento (RN06).

**Pronto quando**: um contrato vencido some da cobertura no mesmo dia, e a ficha
mostra o histórico com o comprovante abrindo em nova aba.

## Sprint 5 · Paradas, custo e risco

- [x] `#/paradas`: abrir parada (equipamento, início, motivo) e fechar (fim).
- [x] Status do equipamento muda para **parado** enquanto a parada está aberta.
- [x] Funções de cálculo isoladas e testadas em `testes/testes.html`:
      `custoDiarioParada` (RN02), `custoParada` (RN03), `risco` (RN04),
      `pontoUnicoDeFalha` (RN01), `disponibilidade` (RN07).
- [x] `#/config`: parâmetros de custo editáveis, com data da última alteração.
- [x] Na ficha: custo diário estimado, custo acumulado das paradas e a fórmula
      com os valores usados.

**Pronto quando**: os testes de cálculo estão verdes, e abrir uma parada em um
ponto único de falha sem contrato muda o risco para **alto** na ficha.

## Sprint 6 · Mapa offline de MT

- [x] Desenhar o contorno de MT e os municípios em SVG a partir do GeoJSON embutido.
- [x] Pinos agrupados por unidade, na cor do maior risco, com o número de equipamentos.
- [x] Zoom (roda do mouse e botões) e arrasto via `viewBox`.
- [x] Filtros: sem contrato, parados, ponto único de falha, diretoria, tipo.
- [x] Clique no pino: painel lateral com os equipamentos da unidade e o link para a ficha.
- [x] Legenda das cores e do tamanho dos pinos.
- [x] Tabela equivalente abaixo do mapa (acessibilidade).

**Pronto quando**: com o Wi-Fi desligado, o mapa mostra as 12 unidades do seed e
o filtro "sem contrato" reduz os pinos de acordo.

## Sprint 7 · Painel de KPIs

- [x] `#/painel`: os 7 KPIs do `contexto.md`, seção 8, com o período selecionável.
- [x] Ranking de unidades e de diretorias por custo de parada.
- [x] Lista dos pontos únicos de falha sem contrato, ordenada pela exposição diária.
- [x] Gráfico de barras em SVG próprio (custo de parada por unidade) e linha
      (paradas por mês). Sem biblioteca externa.
- [x] Cada número mostra a fórmula e os parâmetros ao passar o mouse.
- [x] Clique num KPI filtra o mapa.

**Pronto quando**: os KPIs do seed batem com a conta feita à mão numa planilha
para 2 unidades.

## Sprint 8 · Exportação para o Google Earth

- [x] Gerar o KML: pastas por diretoria e unidade, um *Placemark* por
      equipamento, estilos por faixa de risco.
- [x] Balão com miniatura da foto, patrimônio, status, contrato, custo diário e risco.
- [x] Empacotar KML e miniaturas em `.kmz` com JSZip.
- [x] Opção de exportar só o filtro atual (ex.: só os sem contrato).
- [ ] Testar no Google Earth Pro e no Google Earth Web.

**Pronto quando**: o `.kmz` do seed abre nos dois, com as pastas, as cores e as
fotos nos balões.

## Sprint 9 · Importação e consolidação

- [x] Importar a planilha atual em CSV, com tela de associação de colunas
      (coluna da planilha → campo do app) e prévia das 10 primeiras linhas.
- [x] Relatório da importação: linhas aceitas, recusadas e o motivo.
- [x] Importar o `.json` de uma unidade e mesclar (RN10): novos, atualizados,
      excluídos e conflitos.
- [x] Tela de conflitos: escolher a versão da unidade ou a da coordenadoria.
- [x] Exportar `.json` com ou sem fotos.
- [x] `#/config`: escolher o perfil da cópia (unidade ou coordenadoria) e a
      unidade dona.

**Pronto quando**: duas cópias do app, alteradas em paralelo, são mescladas na
coordenadoria sem duplicar nenhum equipamento.

## Sprint 10 · Acessibilidade, LGPD e relatório

- [x] Navegação completa por teclado (tab, enter, esc) e foco visível.
- [x] Contraste AA nos temas claro e escuro, conferido no DevTools (Lighthouse).
- [x] `aria-label` em botões de ícone e `<label>` em todos os campos.
- [x] Relatório impresso (`@media print`): resumo dos KPIs, pontos únicos de
      falha sem contrato e lista por unidade, em A4.
- [x] Varredura de dados pessoais: aviso se algum campo de texto livre tiver
      padrão de CPF (RN09).
- [x] Texto de privacidade em `#/config` e botão "limpar dados desta cópia".

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
- [x] `LEIA-ME` de uso em uma página (como abrir, fazer backup e enviar o `.json`).
- [ ] Abrir o **piloto de 30 dias** (pedido no formulário) nas 3 unidades, com
      backup semanal enviado à coordenadoria.
- [ ] No fim do piloto, comparar com a linha de base do Sprint 0: equipamentos
      sem contrato identificados, paradas registradas e tempo para responder
      "quanto custa essa parada?".
- [ ] Atualizar o `PROJETO.md` (marcos, defesa) e o `README.md` da pasta.

**Pronto quando**: a coordenadora cumpre os 8 passos sem ajuda, e o piloto está aberto.

## Sprint 12 · Correções do feedback (03/11/2026)

> Feedback de João Lucas (nota 5). Não pediu ajuste de código; o que falta é o teste manual no Google Earth, que depende de internet.

### Código
- [ ] Nenhum ajuste pedido; manter os gráficos em até 720 px.

### Depende de pessoa
- [ ] Testar o `.kmz` no Google Earth Pro e no Web.
- [ ] Confirmar a base do Google Earth e o mapa de fundo escolhido.

**Pronto quando**: o teste no Google Earth estiver registrado em `modelos/roteiro-aceite.md`.
