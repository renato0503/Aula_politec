# Capacitacao POLITEC/MT — Analise de Dados aplicada a Pericia Criminal

Material do curso ministrado pelo **Professor Renato Rosa** para a **POLITEC/MT**
(Pericia Oficial e Identificacao Tecnica de Mato Grosso). O repositorio organiza
**uma aula = uma pasta `Aula N/`**, cada uma com caderno vivo (HTML), PDF, slides e
materiais de pratica.

> O contrato do repositorio (padrao, convencoes e passo a passo) esta em
> **[`AGENTS.md`](./AGENTS.md)**. Este README e o indice de navegacao do curso.

---

## Aulas disponiveis

| Aula | Tema | Seções | Slides | Caderno HTML | PDF |
|---|---|---|---|---|---|
| [1](Aula%201/) | Fundamentos da Analise + Estatistica | 61 | 5,2 MB | [161 KB](Aula%201/caderno-dia1.html) | 53 pág · 4,9 MB |
| [2](Aula%202/) | Planilhas / Excel e Google Sheets | 69 | 4,4 MB | [207 KB](Aula%202/caderno-dia2.html) | 71 pág · 4,6 MB |
| [3](Aula%203/) | Organizacao, Visualizacao e ETL | 64 | 4,0 MB | [144 KB](Aula%203/caderno-dia3.html) | 48 pág · 4,2 MB |
| [4](Aula%204/) | Business Intelligence / Power BI | 107 | 6,3 MB | [227 KB](Aula%204/caderno-dia4.html) | PDF a regerar |
| [5](Aula%205/) | Dashboards de BI - 5 cenarios com datasets proprios | 80 | — | [140 KB](Aula%205/caderno-dia5.html) | PDF opcional |
| [6](Aula%206/) | Painel de Processo (manha) + Gestao de Projetos (tarde) | 80 | — | [417 KB](Aula%206/caderno-dia6.html) | [121 pág · 6,5 MB](Aula%206/Caderno%20Dia%206%20-%20POLITEC.pdf) |
| [7](Aula%207/) | Gargalo medido, Automacao e Antigravity | 68 | — | [378 KB](Aula%207/caderno-dia7.html) | [135 pág · 6,6 MB](Aula%207/Caderno%20Dia%207%20-%20POLITEC.pdf) |
| [8](Aula%208/) | Fase de ideação (formulario, metricas e defesa) | — | — | [Formulário](Aula%208/formulario-ideacao.html) | — |

Cada pasta `Aula N/` contem: `README.md` (indice da aula), `caderno-diaN.html`
(fonte viva), `Caderno Dia N - POLITEC.pdf`, `Dia-N-Politec.pdf` (slides) e
`gerar_caderno_aulaN.py` (gerador de conteudo). A Aula 6 acrescenta
`gerar_datasets_aula6.py` (5 datasets de processo), `gerar_excel_aula6.py`
(5 workbooks `.xlsx` com todas as tabelas em abas) e a pasta `datasets/` com
os 5 cenarios. A Aula 7 repete o esquema com **5 cenarios novos**
(`gerar_datasets_aula7.py` e `gerar_excel_aula7.py`, 58.408 execucoes de etapa),
acrescenta o **aulão de Antigravity** e os **comandos do GitHub**.

---

## O que e o caderno

O **caderno** e o material de **aprofundamento** do aluno — complementa, nao
substitui, os slides. Ele traz:

- **Formato em dois turnos** (a partir da Aula 6): a **manha** e de paineis, BI
  e analise de dados; a **tarde** e de hands-on em gestao de projetos e mini
  apps. O caderno se organiza em **6 a 10 partes** conforme a aula (a Aula 6
  usa 10: fundamentos do painel, 5 receitas por dataset, analise, projeto,
  BPMN/Mermaid, TO-BE, labs, cenarios e fechamento).
- **Passo a passo** de cliques/atalhos/contas (`step`) em toda secao pratica.
- **Exemplos e aplicacoes na POLITEC** (`aplicab`: QUANDO / POR QUE / EXEMPLO).
- **Labs** (6-8 por aula) e **cenarios reais** (3-4 por aula).
- **Quiz** com gabarito expansivel, glossario e referencias.
- **Recursos**: tema claro/escuro, indice lateral com busca, botao Imprimir/PDF,
  blocos de codigo com botao Copiar. Um arquivo HTML autossuficiente — abre com
  duplo clique, offline.

---

## Novidades da Aula 6 (formato novo do curso)

A partir da Aula 6, o curso opera em **dois turnos** e o caderno da aula foi
reescrito do zero em **portugues do Brasil**:

- **Manha (08h-12h)**: paineis, BI e analise de dados. O aluno abre o workbook
  do dataset, importa no Power BI, modela o relaciomanto, cria as medidas e
  monta o painel (cartoes, graficos, Pareto, linha do tempo, matriz, filtros,
  segmentacoes e tabela resumo).
- **Tarde (13h-17h)**: hands-on de gestao de projetos, BPMN/Mermaid, AS-IS,
  TO-BE, calculo do ganho e canvas do mini app. Nas aulas seguintes, a tarde
  vira ideacao e prototipacao de mini apps com IA agentica.

Entregas da Aula 6:

- **5 datasets de processo** (57.293 execucoes medidas), cada um em um
  **workbook `.xlsx` com 9 abas** (`LEIA-ME` + `fato_execucao` + 7 `dim_*`).
- **5 receitas de painel** no caderno, uma por dataset, com **72 passos em 8
  blocos** cada (antes eram 19).
- **8 labs** (4 de painel pela manha + 4 de processo e mini app pela tarde).
- **80 secoes em 10 partes**, com quiz, glossario e referencias.
- Novo padrao de idioma: acentuacao completa, sem adjetivacoes, sem
  travessoes e com conectivos depois do ponto final (aplicado por `ptbr.py`).

### O que foi feito nesta entrega (Aula 6)

| Item | Detalhe |
|---|---|
| **Formato do curso** | Passa a ter manha de paineis/BI/analise e tarde de gestao de projetos e mini apps. O caderno foi reestruturado em **10 partes**: fundamentos do painel, 5 receitas, analise do processo, fundamentos de projeto, BPMN/Mermaid, do texto ao diagrama, TO-BE, 8 labs, 3 cenarios e fechamento |
| **5 datasets** | 3 existentes (requisicao pericial, empenho e contrato, cadeia de custodia) + 2 novos (**atendimento de local de crime** e **analise laboratorial**). Total de **57.293 execucoes** medidas, com tempos de espera e execucao separados |
| **Workbooks Excel** | Novo gerador `Aula 6/gerar_excel_aula6.py`: um `.xlsx` por dataset, com 9 abas (LEIA-ME + fato + 7 dims), cabecalho formatado, filtro, painel congelado e tabela-resumo medida |
| **Receitas detalhadas** | A funcao `receita()` passou de 19 para **72 passos em 8 blocos** (Excel, importacao, Power Query, modelo, medidas, painel, filtros e tabela resumo, formatacao e publicacao), com o DAX do Pareto (`Rank da Etapa`, `% Acumulado da Espera`, `Espera por Etapa`) e as instrucoes de eixo secundario, escala, interacoes entre visuais, formatacao condicional da matriz e publicacao no Service |
| **Reescrita em pt-BR** | Abertura e as 10 partes reescritas em portugues do Brasil: acentuacao completa, sem adjetivacoes, sem travessoes e com conectivos depois do ponto final. Nova ferramenta `ptbr.py` + `ptbr_dict.json` (403 entradas), chamada no fim do build |
| **Correcoes nos datasets** | (1) `dim_etapa.etapa_key` alinhado com a chave usada pela fato, que estava quebrando o join do Pareto; (2) cabecalhos de `dim_unidade` (`tipo`) e `dim_projeto` (`escopo`); (3) `tempo_total_min` &rarr; `tempo_total_h` e `custo_minuto` &rarr; `custo_execucao_rs`; (4) `unidade_padrao` passou a trazer o nome da unidade |
| **Quiz** | Corrigida a pergunta sobre o grao da tabela fato, que estava com as alternativas da pergunta de stateDiagram |
| **PDF** | `Caderno Dia 6 - POLITEC.pdf` gerado com **121 paginas** e 80 secoes no sumario paginado (2 passadas), publicado junto com o site |
| **Publicacao** | Commit `3516501` na branch `main`: site `https://renato0503.github.io/Aula_politec/` com o card novo da Aula 6, o caderno com 80 secoes, o PDF e os workbooks para download |

---

## Novidades da Aula 7 (gargalo medido, automacao e Antigravity)

A Aula 7 mantem o formato de dois turnos e acrescenta a construcao do app.

| Item | Detalhe |
|---|---|
| **5 cenarios novos** | Apreensao e pericia de armas, sinistro de transito, credenciamento de peritos, operacao de etilometria e atendimento/ouvidoria. **58.408 execucoes de etapa** medidas, com o gargalo de cada processo saindo do dado |
| **Workbooks Excel** | `Aula 7/gerar_excel_aula7.py`: um `.xlsx` por cenario, com 9 abas (LEIA-ME + fato + 7 dims) e a tabela-resumo medida |
| **Receitas detalhadas** | 5 receitas em **8 blocos e 96 passos**, do Excel ao Power BI, com caminho de menu, o que esperar na tela e o que fazer quando da erro |
| **11 medidas por cenario** | 8 medidas base, 3 do Pareto e 1 especifica do processo, com o DAX pronto para copiar |
| **Tarde de projeto** | Leitura comparada dos 5 gargalos, catalogo de 10 intervencoes, matriz gargalo x intervencao, calculo de ganho, business case, roadmap em 4 fases e proposta de solucao (TO-BE em Mermaid) para cada cenario |
| **Aulao de Antigravity** | 11 secoes, botao por botao: instalacao, janela, painel do agente, Agent Manager, modelos, terminal e painel de versao, artefatos, permissoes, comandos de barra e Remote Control |
| **GitHub** | Secao com os comandos para conectar a conta pelo navegador (`gh auth login --hostname github.com --git-protocol https --web`), publicar o projeto e o fluxo diario de versionamento |
| **PDF** | `Caderno Dia 7 - POLITEC.pdf` gerado com **135 paginas** e 68 secoes no sumario paginado (2 passadas) |

---

## Fase de ideação (Aula 8)

Material da fase que vem depois da Aula 7, em `Aula 8/`:

| Arquivo | O que é |
|---|---|
| `formulario-ideacao.html` | Formulário do projeto, em 14 blocos: identificação, problema, **AS-IS** (tabela de etapas), **papéis**, **TO-BE**, escopo e **MVP mínimo**, **entidades, regras de negócio e LGPD**, **fontes de dados**, **KPIs** com linha de base, **hospedagem**, pesquisa de apoio, marcos e riscos, defesa e **upload dos documentos**. Exporta o `PROJETO.md`, **importa o `.md` e o `.json`** para continuar depois, e em todas as tabelas oferece **copiar modelo, copiar tabela e colar tudo de uma vez** (TAB do Excel, ponto e vírgula ou Markdown). Não envia formulário vazio e avisa as pendências antes do envio |
| `index.html` | O **hub**: um cartão por projeto, com busca, filtros e indicadores de completude |
| `app.html` | A página de cada projeto, com os 15 blocos recebidos, os arquivos para download e os prompts de Mermaid (AS-IS, TO-BE e TO-BE com automação) prontos para colar no Antigravity |
| `prompt-bpmn-mermaid.md` | O **papel (role)** de Mermaid/BPMN, com as convenções e os três comandos de mapeamento |
| `firestore.rules` | As regras do Firestore: leitura pública, criação livre, sem alteração nem remoção |
| `formulario-ideacao.md` | As mesmas perguntas em texto, para Google Forms, Moodle ou papel |
| `template-metricas.md` | Conjunto mínimo de métricas, fórmulas de ganho, frase de defesa, exemplo preenchido e checklist do professor |
| `README.md` | Roteiro da fase: as duas semanas, a rotina do professor e os critérios de avaliação |

A lógica da fase: a equipe declara **problema, AS-IS, papéis, TO-BE, MVP, dados,
regras, fontes e hospedagem**; o professor mede a **linha de base** nas fontes
declaradas, monta os **três diagramas** (AS-IS, TO-BE e TO-BE com automação) em
Mermaid e constrói o **MVP funcional**; a equipe defende a proposta com a
**mesma métrica**, comparando o valor medido com o valor esperado, que vira
hipótese testada no piloto.

Tudo é gravado no **Firestore** do projeto Firebase `aulapolitec` (plano Spark:
só Firestore, sem Storage). Cada arquivo enviado vira um documento na coleção
`ideacao_arquivos`, com limite de 600 KB por arquivo.

**Links da sala:** o aluno abre
`https://renato0503.github.io/Aula_politec/Aula%208/formulario-ideacao.html` e o
professor acompanha em `https://renato0503.github.io/Aula_politec/Aula%208/`
(espelho em `https://aulapolitec.web.app/Aula%208/`).

**O que foi feito nesta fase**, em ordem: (1) formulário inicial, com métricas e
painel do professor; (2) formulário genérico, com AS-IS, papéis, TO-BE, MVP,
entidades, regras, LGPD, stack e hospedagem; (3) Firebase só Firestore, com os
arquivos em base64 e limite de 600 KB; (4) hub com cartões, filtros e CSV, e
página do projeto com 15 seções; (5) `PROJETO.md` em 9 seções e o papel de
Mermaid/BPMN com os três comandos; (6) importação do `.md` e do `.json` e
copiar/colar tabelas; (7) validação do envio e contingência por e-mail;
(8) publicação no GitHub Pages e no Firebase Hosting.

---

## Apps dos grupos (Aula 8, fase 2)

Cada entrega do formulário vira uma pasta em `Apps/<slug>/` com a ficha do grupo,
a especificação completada (`PROJETO.md`), o contexto e o plano de sprints. O app
em si é **um único `index.html`** (CSS, JS, bibliotecas e dados embutidos), que
abre com duplo clique, guarda os dados no IndexedDB e funciona sem internet. A
exceção é o `agendamento-cin`, servido pelo Google Apps Script.

| Situação (29/10/2026) | Apps |
|---|---|
| Sprints 1, 2 e 3 | adiantamento, agendamento-cin, agiliza-mais, cin-segunda-via, comissao-etica-denuncias, equipamentos-google-earth, horus-banco-demandas, inscricoes-cursos, mapa-distribuicao-credor, metas-bi-ocr, rnc-nao-conformidade, tap-portfolio-projetos |
| Sprints 1 e 2 | custodia-definitiva, passivo-ambiental, renovacao-contratos-horus, documentapolitec, gestao-documentos, controle-aquisicoes, distribuicao-casos-dna |

A base comum fica em `Apps/_base/`: `base.html` (tema, rotas, IndexedDB, perfis,
backup e `#/testes`), `construir.py` (gera o `index.html`), `embutir.py`,
`testar.py`, `testar_sprints.py` e `equipes.py` (logins do GitHub). O índice
completo, com contatos e pendências, está em [`Apps/README.md`](./Apps/README.md).

```powershell
python Apps/_base/construir.py <app>          # gera o index.html
python Apps/_base/testar.py <app>             # estrutura e testes embutidos
python Apps/_base/testar_sprints.py <app>     # cenário de cada sprint
```

---

## Estrutura do repositorio

```
Aula Politec/
├── README.md              ← este indice
├── AGENTS.md              ← contrato do repositorio (padrao dos cadernos)
├── caderno_lib.py         ← motor compartilhado (CSS + helpers + classe Caderno)
├── caderno_svg.py         ← biblioteca SVG (icones BPMN 2.0 e diagramas de processo)
├── ptbr.py                ← acentuacao pt-BR do HTML gerado
├── ptbr_dict.json         ← dicionario de acentuacao (403 entradas)
├── exportar_pdf.py        ← exporta caderno-diaN.html -> "Caderno Dia N - POLITEC.pdf"
├── validar.py             ← checa secoes x TOC x h2, tema, erros de console
├── gerar_datasets_estrela.py ← monta o modelo estrela (fato_*/dim_*) nas Aulas 2, 3 e 4
├── Aula 1/ … Aula 8/      ← uma pasta por aula
├── Apps/                  ← mini apps dos grupos (19 projetos, HTML único)
```

---

## Como usar

**So ler** — abra o `caderno-diaN.html` da aula no navegador (ou o PDF).

**Editar/regerar um caderno**

```powershell
python "Aula N\gerar_caderno_aulaN.py"   # gera o HTML
python validar.py N                       # precisa imprimir OK
python exportar_pdf.py N                  # gera o PDF (opcional)
```

Requisitos das ferramentas: `pip install playwright pymupdf` e
`playwright install chromium` (so para o PDF).

**Regerar os datasets da Aula 6** (na ordem)

```powershell
python "Aula 6\gerar_datasets_aula6.py"   # 5 datasets (CSVs + READMEs)
python "Aula 6\gerar_excel_aula6.py"      # 5 workbooks .xlsx (uma aba por tabela)
python "Aula 6\gerar_caderno_aula6.py"    # caderno (ja aplica a acentuacao pt-BR)
python validar.py 6
```

**Regerar os datasets da Aula 7** (na ordem)

```powershell
python "Aula 7\gerar_datasets_aula7.py"   # 5 datasets novos (58.408 execucoes)
python "Aula 7\gerar_excel_aula7.py"      # 5 workbooks .xlsx (uma aba por tabela)
python "Aula 7\gerar_caderno_aula7.py"    # caderno (ja aplica a acentuacao pt-BR)
python validar.py 7
```

**Criar uma nova aula** — siga `AGENTS.md` > "Como criar uma nova aula".

---

## Publicacao do site

O site e publicado em **dois canais**, a partir do mesmo repositorio
`renato0503/Aula_politec` (branch `main`):

| Canal | Endereco |
|---|---|
| GitHub Pages | **https://renato0503.github.io/Aula_politec/** |
| Firebase Hosting | https://aulapolitec.web.app |

Publicar uma alteracao:

```powershell
python "Aula N\gerar_caderno_aulaN.py"     # gera o HTML
python validar.py N                        # precisa imprimir OK
git add <arquivos da aula> <docs>
git commit -m "Aula N: <resumo>"
git push origin main
```

> O cache do CDN do GitHub Pages leva de **1 a 10 minutos**. Apos o push, a
> pagina pode continuar servindo a versao anterior por alguns minutos. Para
> conferir se o commit chegou, use
> `https://raw.githubusercontent.com/renato0503/Aula_politec/main/<caminho>`.
>
> Os **workbooks `.xlsx` da Aula 6** sao publicados junto e podem ser baixados
> direto do site, em `Aula 6/datasets/cenarioN/`.

---

## Convencoes rapidas

- Nomes: `Dia-N-Politec.pdf`, `caderno-diaN.html`, `Caderno Dia N - POLITEC.pdf`,
  `gerar_caderno_aulaN.py` (sem zero a esquerda).
- Texto em portugues **sem acentos** (padrao das Aulas 1 a 5). **A partir da
  Aula 6**, o padrao e portugues do Brasil **com acentuacao completa**, sem
  adjetivacoes, sem travessoes e com conectivos ligando as frases depois do
  ponto final.
- HTML sem dependencia externa; tema claro/escuro; UTF-8.
- Numeros sempre com fonte (slide ou dataset).

---

## Pendencias / proximos passos

1. **PDF fiel ao HTML** — o `@media print` atual comprime as secoes; falta um
   layout de impressao dedicado (capa, quebras por parte). O HTML e a fonte de verdade.
2. **Datasets** — arquivos sinteticos (`datasets/`) para os labs de Excel/Power BI.
3. **PDFs das Aulas 5 e 6** — opcional; rodar `python exportar_pdf.py 5` e `python exportar_pdf.py 6`.
4. **Aula 8+** — a Aula 7 ja entrega o app construido no GitHub, com o agente do Antigravity e o diff revisado. O proximo passo e pegar esse app e transformá-lo em artefato pronto para apresentar: teste automatizado, imagem de tela, documentacao e deploy.
5. **Ampliar o dicionario pt-BR** — ao escrever palavras novas no gerador, incluir a entrada em `ptbr_dict.json` para que a acentuacao continue correta.

---

*Padrao herdado do curso SESP/MT. Motor do caderno: [`caderno_lib.py`](./caderno_lib.py).*
