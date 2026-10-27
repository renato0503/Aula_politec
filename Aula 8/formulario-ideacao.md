# Formulário da fase de ideação e prototipação (versão para Google Forms, Moodle ou papel)

Mesmo conteúdo do formulário em HTML (`formulario-ideacao.html`), em texto, para
quem precisar aplicar em outra ferramenta. A ordem das perguntas é a mesma.

> Os blocos 2 (AS-IS), 3 (papéis), 4 (TO-BE), 6 (dados e regras), 7 (fontes),
> 8 (KPIs) e 9 (hospedagem) são os que o professor usa para montar os três
> diagramas e o MVP. São eles que precisam de resposta completa.

**Recursos da versão em HTML** (`formulario-ideacao.html`), que não existem em
uma versão de texto:

| Recurso | Para que serve |
|---|---|
| Salvamento automático no navegador | Fechar e voltar depois sem perder nada |
| **Importar PROJETO.md ou .json** | Continuar de onde parou, inclusive em outro computador |
| **Copiar modelo / Copiar tabela / Colar tudo de uma vez** | Preencher as tabelas no Excel e colar o bloco inteiro de uma vez |
| **Enviar projeto e arquivos ao professor** | Grava a resposta no Firestore e os arquivos na coleção `ideacao_arquivos` |
| **Enviar por e-mail** | Contingência quando o Firebase está bloqueado na máquina |
| Checklist em tempo real | Mostra o que ainda falta antes de enviar |

---

## Bloco 0 — Identificação

| # | Pergunta | Tipo |
|---|---|---|
| 0.1 | Aluno ou equipe | texto curto |
| 0.2 | Unidade, área ou setor | texto curto |
| 0.3 | E-mail de contato | texto |
| 0.4 | Nome do projeto | texto curto |
| 0.5 | Tipo de projeto | lista: app, app web, painel de BI, sistema, mapeamento de processo, automação de script, relatório, norma ou manual, formulário, protótipo de papel, outro |
| 0.6 | Data | data |
| 0.7 | Resumo do projeto em uma frase | texto longo |

## Bloco 1 — Problema e estado atual

**1.1. Qual é o problema, em uma frase?**
**1.2. Quem é afetado?** (cidadão externo, servidor, equipe interna, unidade parceira, chefia, autoridade)
**1.3. Como é feito hoje, na prática?**
**1.4. Qual é o impacto hoje?** (tempo, custo, qualidade, risco, retrabalho, com a evidência)
**1.5. De onde vem a evidência?** (planilha, relatório de sistema, entrevista, medida da equipe, documento oficial, pesquisa externa) + detalhe
**1.6. O que não pode ser automatizado, e por quê?**

## Bloco 2 — AS-IS: o processo como ele é hoje

**2.1.** Evento de início · **2.2.** Evento de fim · **2.3.** O que entra · **2.4.** O que sai
**2.5.** Volume · **2.6.** Duração total · **2.7.** Frequência

**2.8. Tabela de etapas** (uma linha por etapa)

| # | Etapa | Quem faz (papel/unidade) | O que entra | Ação realizada | O que sai | Sistema ou papel | Regra ou decisão | Onde espera | Tempo (h) | Automatizável? |
|---|---|---|---|---|---|---|---|---|---|---|

**2.9.** Decisões e aprovações · **2.10.** Caminhos alternativos e exceções · **2.11.** O que já é digitalizado

## Bloco 3 — Papéis

**3.1. Tabela de papéis**

| Papel | Quem é na prática | O que enxerga | O que faz | O que não pode fazer | O que o sistema registra |
|---|---|---|---|---|---|

**3.2.** Observações sobre os papéis

## Bloco 4 — TO-BE: como o processo deve ficar depois da mudança

**4.1.** A visão do futuro, em uma frase · **4.2.** A mudança principal · **4.3.** O que fica igual · **4.4.** O que não pode mudar

**4.5. Etapas do processo depois da mudança**

| # | Etapa depois da mudança | O que muda | Quem executa (máquina, pessoa assistida ou pessoa) | Benefício esperado | Esforço |
|---|---|---|---|---|---|

**4.6.** Onde e como testar o TO-BE

## Bloco 5 — Escopo, artefatos e o MVP mínimo

**5.1.** Entregável final · **5.2.** O que entra no escopo · **5.3.** O que fica de fora · **5.4.** O que o MVP **não** faz

**5.5. Telas, artefatos ou etapas do entregável**

| # | Artefato | Rota (#/painel) | Objetivo | Quem usa | Dados | Ação | Regra | Tipo | Verificável como | MVP mínimo |
|---|---|---|---|---|---|---|---|---|---|---|

**5.6.** Objetivo do MVP, em uma frase · **5.7.** Plataforma alvo · **5.8.** Primeira tela
**5.9.** O que vai ser simulado · **5.10.** Critério de aceite · **5.11.** Dados de exemplo
**5.12.** O que já existe pronto e pode ser reaproveitado · **5.13.** De quem o projeto depende

## Bloco 6 — Dados, regras de negócio e conformidade

**6.1. Entidades e colunas (tudo sintético)**

| Entidade | O que representa | Colunas (nome: tipo) | Chave | Volume | Origem | Sintético? |
|---|---|---|---|---|---|---|

**6.2. Regras de negócio**

| ID | Regra | Quando se aplica | Exceção | Quem valida | Tipo |
|---|---|---|---|---|---|

**6.3.** Dados pessoais tratados pelo MVP · **6.4.** Base legal e finalidade · **6.5.** Prazo de retenção · **6.6.** Quem acessa e como é registrado
**6.7.** Stack e ambiente de execução (padrão da aula: HTML único, CSS/JS inline, dados em JSON embutido, GitHub Pages) + detalhe

## Bloco 7 — Fontes de dados

**7.1. Tabela de fontes**

| Fonte | Tipo | Onde fica | Existe? | Acesso | Uma linha é | Volume | Histórico | Campos de data e tempo | Atualiza | Dado sensível (LGPD) | Observação |
|---|---|---|---|---|---|---|---|---|---|---|---|

**7.2.** O que não existe hoje e precisa ser coletado · **7.3.** Quem libera o acesso, e quando

## Bloco 8 — KPIs: linha de base e melhoria hipotética

**8.1. Tabela de métricas**

| # | Nome | Pergunta que responde | Fórmula | Fonte | Granularidade | Linha de base | Valor esperado | Como medir na semana 1 | Quem mede |
|---|---|---|---|---|---|---|---|---|---|

**8.2.** Período e volume da linha de base · **8.3.** Quais campos de data e tempo existem de fato

## Bloco 9 — Hospedagem e implantação da plataforma

**9.1. Opções de hospedagem consideradas**

| Opção | Tipo | Onde roda | Custo | Quem mantém | Acesso | Banco de dados | Escala | Limitação |
|---|---|---|---|---|---|---|---|---|

**9.2.** Opção escolhida e por quê · **9.3.** Quem cria a conta, o domínio e o acesso · **9.4.** Orçamento, licenças e custos

## Bloco 10 — Requisitos, restrições e pesquisa

**10.1.** Requisitos e restrições já definidos (múltipla escolha) · **10.2.** As restrições que você já sabe
**10.3.** Sua hipótese de campo, em uma frase

**10.4. Pesquisa de apoio**

| # | Referência | Tipo | Fonte ou link | Ano | Dado que extrai | Como usar na defesa | Link conferido |
|---|---|---|---|---|---|---|---|

**10.5.** Lacunas e limites da sua pesquisa

## Bloco 11 — Marcos, riscos e apoio

**11.1. Marcos**

| Marco | Data | Responsável | Depende de | Situação |
|---|---|---|---|---|

**11.2. Riscos**

| Risco | Probabilidade | Impacto | Mitigação |
|---|---|---|---|

**11.3.** De que apoio você precisa, e de quem · **11.4.** O que você precisa aprender para executar

## Bloco 12 — A defesa

**12.1.** A frase de defesa, em uma linha · **12.2.** As três evidências · **12.3.** Como você vai testar se a proposta funciona · **12.4.** O maior risco da proposta e como tratar

## Bloco 13 — Documentos e envio

**13.1.** Arquivos do projeto (até 600 KB por arquivo, pelo formulário) · **13.2.** O que é cada arquivo, em uma linha · **13.3.** O que ainda falta

---

## Como o professor usa o que chega

1. Cada equipe entrega o **`.json`** e o **`PROJETO.md`** (o formulário gera os dois).
2. O professor importa os `.json` no hub, que consolida tudo e mostra a pendência
   de cada equipe.
3. Na página do projeto, os botões **Copiar prompt do AS-IS**, **do TO-BE** e
   **do TO-BE com automação** montam o prompt do Mermaid já preenchido com os
   dados do aluno (papel em `prompt-bpmn-mermaid.md`).
4. O prompt vai para o Antigravity, e o diagrama volta revisado.
5. O MVP sai do Bloco 5 e do `PROJETO.md`: cada linha da tabela de artefatos vira
   uma tela do protótipo.
6. O painel do problema real sai do Bloco 7 e do Bloco 8: a linha de base medida
   nas fontes declaradas, ao lado do valor esperado.
