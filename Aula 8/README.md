# Aula 8 — Fase de ideação e prototipação (formulário, hub e MVP)

Material da fase que vem depois da Aula 7. A ideia é uma só: **cada aluno traz o
problema, o fluxo como ele é hoje, a intervenção que imagina e as fontes de dados
que existem para medir**. Com essas respostas, o professor monta, para cada
aluno: o **AS-IS**, o **TO-BE** normal, o **TO-BE com automação** e o **MVP
funcional**.

A entrega acontece pelo formulário, que grava **tudo no Firestore** do projeto
Firebase `aulapolitec`: a resposta do projeto e cada arquivo enviado (um
documento por arquivo, com o conteúdo em base64). O **hub**
(`Aula 8/index.html`) lista um cartão por projeto, e cada cartão abre a página do
projeto com tudo o que chegou.

> **Plano Spark:** o projeto usa apenas o Firestore. O Cloud Storage exige o plano
> Blaze, então os arquivos vão como documento do Firestore. O limite do Firestore é
> de 1 MiB por documento, e o base64 pesa 33%: por isso, cada arquivo aceito tem
> no máximo **600 KB**. Arquivo maior vai por e-mail ou WhatsApp, com o
> identificador do projeto.

Curso de Capacitação POLITEC/MT · Professor Renato Rosa.

---

## O que o aluno entrega

| Bloco | O que o aluno traz | Para que serve |
|---|---|---|
| 0 | Identificação, tipo de projeto e resumo em uma frase | Classificar a proposta: app, painel, sistema, mapeamento, automação, relatório, norma ou formulário |
| 1 | O problema, quem sofre, o impacto e a evidência | O diagnóstico |
| 2 | **AS-IS**: início, fim, entradas, saídas, volume e a tabela de etapas | O diagrama do processo atual, com a etapa que mais espera marcada |
| 3 | **Papéis**: quem usa, o que enxerga, o que faz, o que não pode fazer | As swimlanes do diagrama e as permissões do app |
| 4 | **TO-BE**: a visão do futuro, o que muda, o que fica igual e o que não pode mudar | Os dois diagramas futuros: o normal e o com automação |
| 5 | Escopo, artefatos, MVP mínimo, plataforma, critério de aceite e dados de exemplo | O MVP funcional |
| 6 | **Entidades e colunas**, **regras de negócio** e conformidade (LGPD, stack) | A especificação técnica que o agente do Antigravity consome |
| 7 | **Fontes de dados**: sistema, planilha, base, com acesso, volume, campos de data e dado sensível | O painel do problema real |
| 8 | **KPIs**: linha de base, valor esperado, fórmula e como medir | A defesa, com número dos dois lados |
| 9 | **Hospedagem** da plataforma: opções, custo, quem mantém, limitação | A checagem de viabilidade |
| 10 | Requisitos, restrições, hipótese de campo e **pesquisa de apoio** | A defesa com fonte |
| 11 | Marcos, riscos e apoio necessário | O plano |
| 12 | A defesa: frase, provas, piloto e risco | O pitch de 3 minutos |
| 13 | **Os documentos do projeto** (upload, até 600 KB por arquivo) e o envio | O contexto para o professor montar AS-IS, TO-BE e MVP |

---

## O formato PROJETO.md

O botão **Baixar PROJETO.md** gera o dossiê no formato usado na aula de
prototipação, e é esse arquivo que o agente do Antigravity consome na hora de
construir o app:

```markdown
# PROJETO.md — NOME DO PROJETO
## 1. Problema (a dor)
## 2. Objetivo do MVP (o que faz e o que NÃO faz)
## 3. Usuários e papéis
## 4. Dados (entidades e colunas; tudo SINTÉTICO)
## 5. Regras de negócio (RN01, RN02...)
## 6. Telas (#/painel, #/lista...)
## 7. KPIs (nome = fórmula em uma linha)
## 8. Stack: HTML único (CSS/JS inline), dados em JSON embutido, GitHub Pages.
## 9. Restrições e LGPD
```

Mais os anexos: **Anexo A** com o AS-IS, **Anexo B** com o TO-BE, **Anexo C** com
pesquisa, riscos e plano, **Anexo D** com a defesa e **Anexo E** com a lista de
documentos enviados.

---

## Firebase: o que o professor precisa habilitar

O projeto Firebase `aulapolitec` já tem a configuração web
(`Aula 8/firebase-config.js`). Para a fase funcionar, são dois passos no console
do Firebase:

| Passo | Onde | O que fazer |
|---|---|---|
| 1 | **Authentication &gt; Sign-in method** | Ativar **Anônimo** (Anonymous). É o que permite gravar sem senha. Sem isso, o envio continua funcionando, porque as regras aceitam a escrita sem sessão |
| 2 | **Firestore Database &gt; Rules** | Colar o conteúdo de `Aula 8/firestore.rules` e publicar |

Publicar as regras pela linha de comando, na raiz do repositório:

```powershell
firebase deploy --only firestore:rules
firebase deploy --only hosting
```

### O que fica gravado onde

| Dado | Onde | Nome |
|---|---|---|
| Resposta completa do projeto (JSON) | Firestore | coleção `ideacao` |
| Arquivos enviados (diagramas, planilhas, modelos, prints) | Firestore | coleção `ideacao_arquivos`, um documento por arquivo, com o conteúdo em base64 |
| Rascunho enquanto o aluno preenche | Navegador | `localStorage` |

As regras bloqueiam a remoção de tudo e a alteração do conteúdo de um projeto de
outra pessoa. A única alteração permitida é a lista de arquivos do próprio
projeto, no momento do envio.

---

## Arquivos desta pasta

| Arquivo | O que é |
|---|---|
| `formulario-ideacao.html` | O formulário da equipe, em 14 blocos, com tabelas dinâmicas, checklist que se atualiza em tempo real, upload de arquivos e envio ao Firestore. Continua funcionando offline: salva no navegador, exporta o `PROJETO.md` e o `.json`, e **importa os dois de volta** para continuar de onde parou |
| `index.html` | O **hub**: um cartão por projeto, com busca, filtro por tipo e por situação, e indicadores de completude |
| `app.html` | A página de cada projeto: 15 seções com tudo que chegou, a lista de arquivos para download e os botões que montam o prompt de Mermaid (AS-IS, TO-BE e TO-BE com automação) já preenchido |
| `firebase-config.js` | Configuração e inicialização do Firebase, compartilhada pelas três páginas, com fallback de versão do SDK |
| `firestore.rules` | As regras de leitura e escrita do Firestore, para publicar no console |
| `prompt-bpmn-mermaid.md` | O **papel (role)** que gera os diagramas AS-IS, TO-BE e TO-BE com automação em Mermaid, no padrão BPMN, com as convenções e os três comandos |
| `formulario-ideacao.md` | As mesmas perguntas em texto, para Google Forms, Moodle ou papel |
| `template-metricas.md` | Conjunto mínimo de métricas, fórmulas de ganho, frase de defesa, exemplo preenchido e checklist do professor |
| `README.md` | Este roteiro da fase |

---

## Trabalhar no Excel, copiar e colar

Todas as 12 tabelas do formulário têm, logo abaixo, três botões e uma área de
colagem. O objetivo é deixar o preenchimento mais simples para quem prefere
trabalhar na planilha.

| Recurso | O que faz |
|---|---|
| **Copiar modelo** | Copia a linha de cabeçalho da tabela, para colar no Excel e preencher lá |
| **Copiar tabela** | Copia a tabela inteira (cabeçalho + linhas) em TSV, para levar ao Excel ou para outra pessoa |
| **Colar tudo de uma vez** | Abre um campo único onde o aluno cola o bloco inteiro. Aceita **TAB** (cópia do Excel), ponto e vírgula, dois espaços e tabela **Markdown** (`\|`) |

Regras da colagem:

- a primeira linha com os **nomes das colunas** vira cabeçalho, e as linhas são
  distribuídas **pelo nome**, então o aluno pode reordenar as colunas no Excel;
- sem cabeçalho, a distribuição é pela **posição**;
- se a tabela já tiver linhas, o formulário pede confirmação antes de substituir;
- linha com menos colunas que o modelo gera aviso, com a quantidade de linhas
  incompletas;
- as colunas de seleção (`Automatizável?`, `Situação`, `Granularidade`, `Tipo`,
  `MVP mínimo`) recebem o valor colado, desde que o texto seja igual a uma das
  opções.

## Continuar depois: importar o que já foi baixado

No topo do formulário existe o botão **Importar PROJETO.md ou .json**:

| Arquivo | O que volta |
|---|---|
| `.json` | Tudo: campos, listas marcadas, tabelas e a opção de stack |
| `PROJETO.md` | Tudo o que estava escrito, lido pelos rótulos e pelas tabelas do dossiê |

A importação **substitui** o que está na tela, então o aluno deve baixar antes se
tiver algo em andamento. Depois de importar, o formulário mostra quantas etapas
de AS-IS, métricas e papéis foram recuperados.

## Antes de enviar

O botão **Enviar projeto e arquivos ao professor** passou a validar:

- formulário **vazio** não é enviado, e o aluno recebe a orientação de preencher
  ao menos a identificação, o problema e a tabela de etapas do AS-IS;
- formulário **incompleto** mostra a lista de pendências e pede confirmação,
  explicando que o professor vai ver as pendências no hub;
- se o Firebase estiver bloqueado na máquina, aparece um aviso no topo do bloco
  de envio, com o motivo, e o botão **Enviar por e-mail** abre a mensagem pronta
  para o aluno anexar o `PROJETO.md` e o `.json`.

## O que foi feito (histórico desta fase)

| Etapa | O que entrou |
|---|---|
| 1 | Formulário inicial da fase de ideação: identificação, problema, fluxo atual, intervenção, fontes de dados, métricas com linha de base e valor esperado, e defesa. Salvamento local no navegador, exportação `.md` e `.json`, painel do professor com importação e consolidação |
| 2 | Formulário **genérico**: o projeto pode ser app, painel, sistema, mapeamento, automação, relatório, norma ou formulário. Entraram os blocos de **AS-IS** (tabela de etapas com onde espera, tempo e automatizável), **papéis** (o que cada um vê, faz e não pode fazer), **TO-BE**, **MVP mínimo** (o que faz e o que não faz, telas com rota, critério de aceite), **entidades e colunas**, **regras de negócio RN01**, **LGPD**, **stack**, **hospedagem** (opções, custo, quem mantém, limitação), **pesquisa de apoio** com fontes, e marcos e riscos |
| 3 | **Firebase no plano Spark**: só Firestore. A resposta vai para a coleção `ideacao` e cada arquivo enviado vira um documento em `ideacao_arquivos`, em base64, com limite de 600 KB. Regras publicadas: leitura pública, criação livre, sem alteração nem remoção |
| 4 | **Hub** (`index.html`) com um cartão por projeto, busca, filtros, indicadores de completude e exportação em CSV; e a **página do projeto** (`app.html`) com 15 seções e download dos arquivos |
| 5 | **PROJETO.md** no formato da aula de prototipação (9 seções + anexos A a E), gerado a partir das respostas, e o **papel (role) de Mermaid/BPMN** (`prompt-bpmn-mermaid.md`), com os três comandos (AS-IS, TO-BE, TO-BE com automação). Na página do projeto, os botões montam o prompt já preenchido com os dados do aluno |
| 6 | **Importar `.md` e `.json`** para continuar de onde parou, e **copiar modelo, copiar tabela e colar tudo de uma vez** em todas as tabelas, para quem prefere trabalhar no Excel |
| 7 | **Validação do envio**: não envia formulário vazio, avisa as pendências antes de enviar e oferece o envio por e-mail quando o Firebase está bloqueado |
| 8 | **Publicação** no GitHub Pages (link dos alunos) e no Firebase Hosting (espelho), com as regras do Firestore publicadas |

---

## Publicação

```powershell
git add "Aula 8" index.html AGENTS.md README.md
git commit -m "Aula 8: fase de ideacao com upload de documentos, hub no Firestore e formato PROJETO.md"
git push origin main
firebase deploy --only hosting
```

**Links para a sala:**

| Quem | Endereço |
|---|---|
| Aluno (formulário) | `https://renato0503.github.io/Aula_politec/Aula%208/formulario-ideacao.html` |
| Professor (hub) | `https://renato0503.github.io/Aula_politec/Aula%208/` |
| Professor (hub, espelho no Firebase) | `https://aulapolitec.web.app/Aula%208/` |

O aluno abre o formulário no GitHub Pages e clica em **Enviar projeto e arquivos
ao professor**: a resposta vai para o Firestore e aparece no hub, sem e-mail e
sem planilha.

> **Domínio autorizado no Firebase:** para o envio automático funcionar a partir
> do GitHub Pages, adicione `renato0503.github.io` em **Authentication >
> Configurações > Domínios autorizados** no console do Firebase. As regras do
> Firestore já aceitam a escrita sem sessão, então o envio funciona mesmo sem
> essa autorização; o que ela garante é o login anônimo e a identificação de
> quem enviou.
>
> **Se o computador da sala bloquear o acesso:** o formulário continua
> funcionando offline (salva no navegador e exporta o `PROJETO.md` e o `.json`).
> Nesse caso, o aluno baixa os dois arquivos e envia por e-mail ou WhatsApp, e o
> professor importa o `.json` pelo botão **Importar arquivos .json** do hub.
> Para descobrir o que está bloqueado, abra o console do navegador (F12) na aba
> **Console**: o nome do domínio recusado aparece lá.

---

## Ligação com as aulas anteriores e seguintes

| Aula | O que entra |
|---|---|
| **Aula 6** | O workflow já foi mapeado em Mermaid. Aqui ele é reescrito com a equipe, na linguagem de quem trabalha na etapa |
| **Aula 7** | O padrão do painel de gargalo: 11 medidas, Pareto, matriz e a hipótese em uma frase |
| **Aula 8** | A fase de ideação: problema, AS-IS, papéis, TO-BE, MVP, dados, regras, fontes, métricas, hospedagem, pesquisa e defesa |
| **Aula 9** | O MVP construído com o Antigravity a partir do PROJETO.md, e o piloto medindo a hipótese no mesmo painel |
