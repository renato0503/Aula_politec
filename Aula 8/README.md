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
(`Aula 8/firebase-config.js`). Para a fase funcionar, são três passos no console
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
| `formulario-ideacao.html` | O formulário da equipe, em 14 blocos, com tabelas dinâmicas, checklist que se atualiza em tempo real, upload de arquivos e envio ao Firestore. Continua funcionando offline: salva no navegador e exporta o `.json` e o `PROJETO.md` |
| `index.html` | O **hub**: um cartão por projeto, com busca, filtro por tipo e por situação, e indicadores de completude |
| `app.html` | A página de cada projeto: 14 seções com tudo que chegou, e a lista de arquivos para download |
| `firebase-config.js` | Configuração e inicialização do Firebase, compartilhada pelas três páginas, com fallback de versão do SDK |
| `firestore.rules` | As regras de leitura e escrita do Firestore, para publicar no console |
| `prompt-bpmn-mermaid.md` | O **papel (role)** que gera os diagramas AS-IS, TO-BE e TO-BE com automação em Mermaid, no padrão BPMN, com as convenções e os três comandos |
| `formulario-ideacao.md` | As mesmas perguntas em texto, para Google Forms, Moodle ou papel |
| `template-metricas.md` | Conjunto mínimo de métricas, fórmulas de ganho, frase de defesa, exemplo preenchido e checklist do professor |
| `README.md` | Este roteiro da fase |

---

## Publicação

```powershell
git add "Aula 8" index.html AGENTS.md README.md
git commit -m "Aula 8: fase de ideacao com upload de documentos, hub no Firestore e formato PROJETO.md"
git push origin main
firebase deploy --only hosting
```

Links: `https://aulapolitec.web.app/Aula%208/` (hub),
`https://aulapolitec.web.app/Aula%208/formulario-ideacao.html` (formulário) e
`https://renato0503.github.io/Aula_politec/Aula%208/` (GitHub Pages).

> O GitHub Pages serve as páginas, mas o **envio ao Firestore** só funciona por
> `https`, com a origem permitida no console do Firebase (em *Authentication >
> Authorized domains*). Para uso em sala, use o endereço do Firebase Hosting.

---

## Ligação com as aulas anteriores e seguintes

| Aula | O que entra |
|---|---|
| **Aula 6** | O workflow já foi mapeado em Mermaid. Aqui ele é reescrito com a equipe, na linguagem de quem trabalha na etapa |
| **Aula 7** | O padrão do painel de gargalo: 11 medidas, Pareto, matriz e a hipótese em uma frase |
| **Aula 8** | A fase de ideação: problema, AS-IS, papéis, TO-BE, MVP, dados, regras, fontes, métricas, hospedagem, pesquisa e defesa |
| **Aula 9** | O MVP construído com o Antigravity a partir do PROJETO.md, e o piloto medindo a hipótese no mesmo painel |
