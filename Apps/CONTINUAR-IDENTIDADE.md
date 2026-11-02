# Continuar: apps independentes, com identidade própria e usabilidade revisada

Registro de 02/11/2026 para outra IA continuar o trabalho. Leia este arquivo
inteiro antes de mexer em qualquer app. Depois leia
`Apps/PLANO-USABILIDADE.md` (o diagnóstico e o plano de cada app) e
`AGENTS.md` (seção 3.8).

---

## 1. O que o professor pediu (as quatro solicitações, nesta ordem)

1. **Análise crítica** do layout e das funcionalidades de cada MVP em `Apps/` e
   um **plano individual** de navegabilidade, layout e usabilidade para cada um.
   Exemplo dado: o seletor de perfil não pode ser uma tela antes do app abrir;
   ele deve ficar num **menu suspenso**, para trocar **a qualquer momento**.
2. **Cada app deve ser único.** Os apps estão muito parecidos uns com os outros.
   Corrigir e **entregar app por app**, com um plano de melhorias de tudo isso.
3. **Sem base comum.** Cada app precisa ter **individualidade e construção
   independente**, porque cada um vai subir **para o próprio repositório no
   GitHub**.
4. **Registrar tudo em `.md`** para continuar em outra IA, com o que foi feito, o
   que falta e um prompt de continuação (este arquivo).

---

## 2. O que já foi feito

### 2.1 Análise e plano (`Apps/PLANO-USABILIDADE.md`)

- Os 20 apps foram abertos no Chromium com os dados fictícios e cada perfil:
  102 telas de menu, 17 fichas de detalhe, 20 telas de entrada e 20 telas no
  celular (390 px), com medidas de altura, rolagem horizontal, botões, campos,
  tabelas e KPIs.
- **Parte A**: 17 problemas que apareciam em todos os apps (A1 a A17), com a
  evidência e a proposta.
- **Parte B**: plano individual dos 20 apps (retrato, o que funciona, problemas,
  plano em navegabilidade / layout / usabilidade com prioridade P1 a P3, e
  critério de pronto).
- **Parte C**: ordem de entrega em ondas e placar por app.
- **Parte D**: **identidade própria de cada app** (casca, cabeçalho, fonte,
  densidade, cantos, superfície, KPI e **tela-assinatura**). É a referência
  para deixar cada app único.

> Atenção: as Partes A e C foram escritas quando ainda havia base comum. A
> partir da solicitação 3, onde o texto diz "base" ou `Apps/_base/`, leia
> **"o `nucleo/` de cada app"**. O conteúdo das propostas continua valendo.

### 2.2 Cada app agora é autônomo (solicitação 3)

Ferramenta usada uma vez: `Apps/_base/separar.py`. Cada `Apps/<app>/` tem agora:

| Arquivo | O que é |
|---|---|
| `nucleo/casca.html` | A casca do app: cabeçalho, menu, roteador, IndexedDB, perfis, backup, abas, `#/testes`. **É do app** e pode divergir dos outros. |
| `nucleo/visual.css` | A identidade visual do app (paleta, componentes e os tokens de identidade). |
| `nucleo/icones.js` | Ícones do app. |
| `nucleo/comum.js` | Tela de configuração e testes comuns. |
| `construir.py` | Gera o `index.html` e embute `vendor/` e os JSON de dados. Não importa nada de fora da pasta. |
| `testes/testar.py` | Teste de estrutura: zero rede, `#/testes` 100%, todas as rotas com cada perfil, dados fictícios persistem, **nenhuma tela de escolha de perfil na abertura**, troca de perfil pelo menu do cabeçalho, tema e **celular sem rolagem horizontal**. |
| `testes/cenarios.py` | Os cenários de interface **só deste app** (extraídos dos antigos `_base/testar_sprints.py` e `_base/cenarios/*.py`). Nos cenários as abas das fichas ficam todas abertas (`localStorage abas:todas = 1`). |
| `.gitignore` | `__pycache__`, `.venv`. |

O `Apps/_base/` virou **molde**: nenhum app depende dele. Os scripts
`_base/construir.py`, `_base/testar.py` e `_base/testar_sprints.py` só chamam o
`construir.py`, o `testes/testar.py` e o `testes/cenarios.py` de cada app (um
atalho para rodar os 20 de uma vez). O `separar.py` recusa sobrescrever um app
já separado (só com `--forcar`, que **apaga as personalizações do núcleo**: não
use).

Comandos de um app (rodar dentro da pasta do app):

```powershell
cd "Apps/<app>"
python construir.py           # gera o index.html
python testes/testar.py       # estrutura
python testes/cenarios.py     # cenários dos sprints
```

Os 20 de uma vez (a partir da raiz do repositório):

```powershell
python Apps/_base/construir.py
python Apps/_base/testar.py
python Apps/_base/testar_sprints.py
```

### 2.3 Correções já aplicadas no núcleo dos 20 apps

Feitas no molde antes da separação, por isso todos os 20 núcleos já têm:

- **Seletor de perfil em menu suspenso no cabeçalho** (`#btnPerfil`,
  `#perfilLista`), trocável a qualquer momento, com nome e descrição de cada
  perfil, marca no atual, `Alt+P`, setas, `Esc` e clique fora para fechar.
  **Não existe mais a tela "Escolha o perfil desta cópia"**: sem perfil gravado,
  o app entra no `perfilPadrao` (ou no primeiro perfil) e avisa uma vez.
  - Ao trocar, fica na mesma tela se o perfil puder vê-la; senão vai para a tela
    inicial do perfil (`perfis[].inicio`, campo novo e opcional no `app.json`).
  - Contexto do perfil (opcional): `perfis[].contexto = {rotulo, store, valor,
    texto}` ou `{rotulo, opcoes}` mostra um segundo seletor (setor, unidade) e
    grava em `estado.contexto`. **Ainda não configurado em nenhum app.**
  - Os itens do menu suspenso usam `data-escolher-perfil`; os botões da tela
    Configuração continuam com `data-perfil` (o `testar.py` usa).
- **Rotas públicas** (cidadão): o seletor some e aparece o link "Área do
  servidor". Campo novo `rotaInicial` no `app.json` define a tela do endereço
  sem `#`. **Ainda não configurado** em `agendamento-cin` e `cin-segunda-via`
  (hoje o endereço sem `#` abre a primeira tela pronta do menu interno; o certo
  é abrir `#/agendar` e `#/pedido`).
- **Contorno dourado em volta do conteúdo removido** (`main:focus{outline:none}`).
- **Trilha "você está em"** (`#trilha`) nas telas de detalhe, e o item pai fica
  marcado no menu. O pai é deduzido pelo radical da rota (`processo/:id` →
  `processos`) ou definido em `rotas[].pai`.
- **Telas não construídas saem do menu** (aparecem com `?dev=1` no endereço).
  A mensagem de tela pendente não cita mais "Sprint N".
- **Cabeçalho**: botão "Exibição" (Aa) com A−, 100%, A+ num menu suspenso; botão
  Tema; no celular os rótulos somem e ficam só os ícones.
- **Celular**: faixa do governo em uma linha, botão "Telas" que abre e fecha o
  menu, KPIs em 2 colunas, tabelas com rolagem dentro delas (a página não rola
  mais na horizontal).
- **Componentes novos, prontos mas ainda não usados nas telas**:
  - `abas(nome, [{id, titulo, conta, alerta, html}])` com `?aba=` no endereço,
    setas do teclado e `abrirAba(id)`;
  - `pode(acao)`, `quemPode(acao)` e `botaoSe(acao, html)`, lidos de
    `APP.permissoes` (campo novo do `app.json`);
  - `numBR(v, casas)` e `plural(n, um, varios)`;
  - classes `.acao-principal`, `a.kpi`, `.kpi.alerta`, `.kpi.zero`.
- **Tokens de identidade** lidos do bloco `visual` do `app.json` (viram
  `data-*` no `<body>`): `casca` (`lateral`, `topo`, `trilho`, `cidadao`,
  `ferramenta`), `cabecalho` (`degrade`, `solido`, `claro`, `compacto`), `fonte`
  (`sistema`, `serifa`, `condensada`, `mono`, `arredondada`), `densidade`
  (`compacta`, `normal`, `ampla`), `cantos` (`retos`, `suaves`, `redondos`),
  `superficie` (`cartoes`, `planas`, `papel`), `kpi` (`barra`, `numero`, `faixa`,
  `anel`). **Nenhum app recebeu ainda os valores da Parte D**: todos estão nos
  valores padrão.
- `src/identidade.js` (se existir) entra **por último** no build, depois de
  todos os sprints. É o lugar da tela-assinatura de cada app.

### 2.4 Estado dos testes (02/11/2026, depois da Etapa 1)

- `testes/testar.py`: **20 de 20 apps OK**.
- `testes/cenarios.py`: **89 de 89 cenários OK** (o `_base/testar_sprints.py`
  roda os 20 e termina com código 0).
- Os dois cenários que falhavam tinham **três causas**, nenhuma delas o feriado
  de 02/11:
  1. **Datas fixas no seed** (`agendamento-cin`): a grade e os agendamentos
     fictícios estavam presos a 03/11 a 13/11, então a agenda do posto não tinha
     nada "hoje". O `planilha-modelo/gerar_planilha.py` passou a gerar **datas
     relativas a hoje** (semana passada, corrente e seguinte) e a garantir
     agendamentos confirmados hoje em cada posto. O `testar_code_gs.js` deixou de
     depender de 16/11 e calcula a grade a partir do próprio seed.
  2. **Esperas fixas nos testes**: `pg.wait_for_timeout(800)` era lido antes do
     fim da importação do seed e antes do `navegar()` terminar. Todos os
     `testes/cenarios.py` ganharam o helper `semear()` (espera a importação
     terminar, recarrega a página) e `esperar()` (polling de condição
     assíncrona). **Importante:** `pg.wait_for_function("async () => ...")` não
     serve, porque a função devolve Promise (truthy) e a espera termina na hora.
  3. **Botão dentro de formulário disparava submit** (`adiantamento`): o
     `#btnPendencia` não tinha `type="button"` e recarregava a página no meio do
     salvamento. Corrigido na fonte.

### 2.5 O que **não** foi feito ainda

- Os `.xlsx` e `.pbix` da `Aula 4/` que aparecem modificados não são deste
  trabalho: **não entram no commit**.
- Nenhum repositório novo foi criado no GitHub.
- Nenhum app recebeu ainda a identidade da Parte D nem os itens P1 da Parte B
  (é a etapa 3, abaixo).
- `AGENTS.md`, `Apps/README.md`, `Apps/IDENTIDADE-VISUAL.md` e
  `Apps/CONTINUAR.md` ainda descrevem a base comum (ver a etapa 5 abaixo).

### 2.6 Etapa 1 concluída (commit `d391b38`)

- Cenários dos 20 apps passando (ver 2.4).
- `"rotaInicial": "#/agendar"` em `agendamento-cin/app.json` e
  `"rotaInicial": "#/pedido"` em `cin-segunda-via/app.json`: o endereço sem `#`
  abre a tela do cidadão, sem tela de perfil. O hash continua vazio; a rota é
  aplicada na renderização (`document.body.dataset.rota`).
- `node testes/testar_code_gs.js` do `agendamento-cin`: **17/17**, com CSP e
  `Code.gs` funcionando com a casca nova.
- Cada `Apps/<app>/README.md` ganhou a seção **"Como construir e testar"** com
  os três comandos, o `pip install playwright` e o `playwright install chromium`;
  `agendamento-cin` inclui também o teste do `Code.gs` e o gerador da planilha.
- Commit `d391b38` com `Apps/` e `AGENTS.md`, sem os arquivos da `Aula 4/`.

---

### 2.7 Etapa 3 · app por app (andamento)

Cada app abaixo foi feito na ordem da seção 3, com um commit próprio. O que foi
feito em cada um está resumido aqui e no `README.md` e no `sprint.md` do app.

| App | Commit | O que mudou |
|---|---|---|
| agendamento-cin | (este commit) | Casca de cidadão, cabeçalho claro, Trebuchet, densidade ampla, cantos redondos. Calendário do mês com vagas por dia e horários em botões grandes; passos 1-2-3; grade semanal de ocupação com cor por situação; busca por protocolo, nome ou CPF na agenda do posto. |
| cin-segunda-via | (este commit) | Casca de cidadão, Trebuchet, cantos redondos, KPI em número. Caixa de entrada com a fila à esquerda e o pedido à direita; busca por protocolo, nome ou CPF; espera em horas; atalhos J/K/A/R; “Aceitar e próximo” e “Recusar e próximo”. |
| horus-banco-demandas | (este commit) | Casca lateral, degradê, fonte do sistema, cantos redondos, KPI em número. Vitrine com facetas e contagem, filtros em uma linha, ordenação, alternância cartões/tabela e contexto de unidade em Gerente e Usuário setorial. |
| trilha-custodia-necropsia | (este commit) | Casca de trilho, cabeçalho sólido, condensada, ampla, cantos suaves, planas, KPI em número. Painel por perfil, quadro de plantão em colunas e ficha em abas. |
| controle-aquisicoes | (este commit) | Casca de ferramenta, degradê, condensada, compacta, cantos suaves, planas, KPI em faixa. Kanban das 9 etapas, ficha em abas com `.etapas` e ações por perfil. |
| custodia-definitiva | (este commit) | Casca de trilho, cabeçalho sólido, condensada, cantos retos, planas, KPI em número. Balcão de leitura do lacre, mapa das prateleiras com barra e painel do gestor só para o gestor. |

---

## 3. O que falta fazer, em detalhe

### Etapa 1 · Fechar a separação (antes de individualizar)

1. Resolver os 2 cenários da seção 2.4.
2. Em `agendamento-cin/app.json` e `cin-segunda-via/app.json`, acrescentar
   `"rotaInicial": "#/agendar"` e `"rotaInicial": "#/pedido"`. Conferir que o
   endereço sem `#` abre a tela do cidadão. Em `inscricoes-cursos`, a inscrição
   pública já abre pelo link com hash.
3. Conferir se a `CSP` e o `Code.gs` de `agendamento-cin` (servido pelo Apps
   Script) continuam funcionando com a casca nova
   (`node testes/testar_code_gs.js` dentro da pasta).
4. Em cada app, criar ou atualizar o `README.md` com a seção **"Como construir e
   testar"** (os 3 comandos da seção 2.2, `pip install playwright` e
   `playwright install chromium`), porque cada pasta vai virar repositório.
5. Commit: `Apps: cada app autônomo (núcleo, construir.py e testes próprios), perfil em menu suspenso`.

### Etapa 2 · Itens comuns que agora são feitos **em cada núcleo**

Estes itens da Parte A ainda não estão nos apps. Como não há mais base comum,
cada um é feito dentro do app, junto da etapa 3, e pode ter forma diferente em
cada app:

| Item | O que fazer em cada app |
|---|---|
| A5 abas | Usar `abas()` nas fichas longas (aquisições 4.332 px, renovação 3.191, TCIN 2.497, gestão de documentos 2.481, DNA 2.271, documentapolitec 2.129). Ver os nomes das abas na Parte B. Depois de salvar algo dentro de uma aba, chamar `abrirAba(id)` para continuar nela. |
| A6 permissões | Preencher `permissoes` no `app.json` e trocar os botões por `botaoSe("acao", html)`. Casos já vistos: aquisições (requisitante não registra análise nem conclui etapa), gestão de documentos (só a autoridade assina), TCIN e custódia (painel do gestor só para o gestor). |
| A7 jargão | Tirar "(Sprint N)" de 42 títulos e passar o código RN para um ícone ⓘ com o texto da regra no `title`. Lista: `grep -nE '<h[1-4][^>]*>[^<]*(Sprint|RN[0-9]|\(R[0-9])' */src/*.js`. |
| A9 listas | Paginação, ordenação e busca nas listas grandes (equipamentos com 151 linhas e 10.371 px; fila da segunda via sem busca). |
| A11 KPIs | KPI como link para a lista filtrada (`<a class="card kpi" href="#/processos?situacao=vencido">`), `.alerta` e `.zero`. |
| A12 números | Trocar `toFixed`/ponto por `numBR` e `plural` ("46.8" no adiantamento, "1.2 dia(s)" no DNA). |
| A14 formulários | "＋ Novo" em vez de formulário sempre aberto (inscrições, mapa de distribuição). |
| A15 configuração | Separar Cadastros / Dados / Sobre (comissão de ética com 3.236 px, feriados do adiantamento). |
| A16 dados fictícios | Registros em **todas** as etapas, datas relativas a hoje, cerca de 20% atrasados (comissão: 10 casos em "registro"; passivo: 10 de 10 atrasados com datas de 2023; metas: histórico vazio; agiliza: sem caso). Regerar com `exemplos/gerar_exemplos.py` de cada app. |

### Etapa 3 · Identidade própria e plano individual, app por app

Ordem sugerida (públicos primeiro, depois os de mais perfis e os de ficha
longa): agendamento-cin, cin-segunda-via, horus-banco-demandas,
trilha-custodia-necropsia, controle-aquisicoes, custodia-definitiva,
documentapolitec, gestao-documentos, renovacao-contratos-horus,
distribuicao-casos-dna, comissao-etica-denuncias, passivo-ambiental,
rnc-nao-conformidade, tap-portfolio-projetos, adiantamento, metas-bi-ocr,
inscricoes-cursos, mapa-distribuicao-credor, equipamentos-google-earth,
agiliza-mais.

Para **cada** app, nesta ordem:

1. **Bloco `visual`** no `app.json` com os valores da Parte D (casca, cabecalho,
   fonte, densidade, cantos, superficie, kpi). Rever o acento e o emblema.
2. **Divergir o núcleo**: o `nucleo/casca.html` e o `nucleo/visual.css` são do
   app. Mudar o que for preciso para a forma da tela-assinatura (por exemplo, o
   TCIN pode ter barra inferior no tablet; o agendamento pode não ter menu na
   área pública; a ferramenta de mapa pode ocupar a largura toda). Não copiar
   mudanças de um app para outro por padrão: cada app decide.
3. **Tela-assinatura** em `src/identidade.js` (redefine `TELAS["#/..."]` e
   `TELAS_DEPOIS`) e `src/app.css`.
4. **Itens P1 e P2 da Parte B** daquele app e os itens da etapa 2 que se
   aplicam.
5. `perfis[].inicio` e, quando fizer sentido, `perfis[].contexto`.
6. `python construir.py`, `python testes/testar.py` e `python testes/cenarios.py`
   passando. Ajustar os cenários quando a tela mudar de forma (eles são do app).
7. Captura de tela no desktop (1366 px) e no celular (390 px), olhada de fato.
8. Marcar no `sprint.md` do app uma linha nova na tabela **Andamento**
   ("Identidade e usabilidade") e atualizar o `README.md` do app.
9. **Um commit por app**: `Apps/<app>: identidade própria e plano de usabilidade`.

Checklist resumido por app (detalhes nas Partes B e D do plano):

| App | Visual (Parte D) | Tela-assinatura | P1 da Parte B |
|---|---|---|---|
| ~~agendamento-cin~~ ✅ | cidadao · claro · arredondada · ampla · redondos · cartoes | Calendário do mês com vagas e horários em botões grandes | `rotaInicial #/agendar`; passos 1-2-3 no fluxo público; grade semanal de horários com cor por ocupação; busca por protocolo/CPF na agenda do posto |
| cin-segunda-via | cidadao · claro · arredondada · normal · redondos · cartoes · numero | Caixa de entrada (lista à esquerda, pedido à direita) | `rotaInicial #/pedido`; "Aceitar e próximo"; busca na fila |
| ~~horus-banco-demandas~~ ✅ | lateral · degrade · sistema · normal · redondos · cartoes · numero | Vitrine com filtros em facetas e ordenação | contexto de unidade nos perfis Gerente e Usuário setorial; barra de filtros em uma linha; alternar cartões/tabela |
| ~~trilha-custodia-necropsia~~ ✅ | trilho · solido · condensada · ampla · suaves · planas · numero | Quadro de plantão (colunas por situação, cartões de corpo, botões grandes) | painel por perfil (4 perfis); uma tabela só no painel; ficha em abas |
| ~~controle-aquisicoes~~ ✅ | ferramenta · degrade · condensada · compacta · suaves · planas · faixa | Kanban das 9 etapas da Lei 14.133 | ficha em abas; etapas em `.etapas`; ações por perfil |
| ~~custodia-definitiva~~ ✅ | trilho · solido · condensada · normal · retos · planas · numero | Balcão de leitura do lacre + mapa das prateleiras | campo "Ler lacre"; painel do gestor só para o gestor |
| documentapolitec | lateral · solido · serifa · normal · retos · papel · barra | Estante de caixas (lombadas) + conferência por leitura | menu de 8 para 5 itens; conferência com campo focado e Enter |
| gestao-documentos | lateral · solido · serifa · normal · suaves · papel · barra | Caixa por perfil (a instruir, a revisar, a assinar) | ficha em abas; checklist com caixa de seleção; assinatura só da autoridade |
| renovacao-contratos-horus | lateral · solido · condensada · compacta · retos · planas · numero | Régua de vencimentos de 0 a 180 dias | ficha em abas; semáforo como barra empilhada clicável |
| distribuicao-casos-dna | topo · degrade · sistema · normal · redondos · cartoes · anel | Placa de 96 poços com a cor do perito | "Meus casos" do perito; rodada em abas |
| comissao-etica-denuncias | lateral · solido · serifa · ampla · retos · papel · faixa | Funil do processo ético + dossiê "Reservado" | barra de etapas e abas no caso; seed em todas as etapas |
| passivo-ambiental | topo · degrade · sistema · normal · suaves · cartoes · faixa | Fila de laudos com prazo e miniatura do mapa | laudo em abas; painel do perito separado do gestor; seed com datas de hoje |
| rnc-nao-conformidade | lateral · solido · sistema · normal · suaves · cartoes · faixa | Quadro por etapa do ciclo | setor como contexto do perfil |
| tap-portfolio-projetos | topo · degrade · serifa · ampla · redondos · cartoes · anel | Matriz do portfólio (valor × prioridade) | `inicio` por perfil (Equipe → Triagem, Autoridade → Portfólio) |
| adiantamento | lateral · solido · mono · compacta · retos · planas · numero | Régua de prazos por processo | tela `#/processos`; prazo da prestação de contas no topo da ficha |
| metas-bi-ocr | topo · claro · sistema · ampla · suaves · cartoes · anel | Ano em 12 meses com a situação de cada mês | assistente em 3 passos; histórico em tabela; "Usar arquivo de exemplo" |
| inscricoes-cursos | topo · degrade · arredondada · ampla · redondos · cartoes · faixa | Cartões de curso com a esteira Divulgar → Turma | curso como centro com barra de passos; "＋ Novo curso" |
| mapa-distribuicao-credor | ferramenta · compacto · mono · compacta · retos · planas · numero | Esteira das 8 etapas + grade em formato planilha | barra de etapas em todas as telas `/:proc`; importação em tabela de 3 linhas |
| equipamentos-google-earth | ferramenta · compacto · sistema · compacta · suaves · planas · numero | Mapa de MT em SVG (os 142 municípios de `dados-base/mt-municipios.json` têm `lat`, `lon` e o polígono `p`) | tela inicial = Equipamentos até o mapa existir; lista paginada; contexto de unidade |
| agiliza-mais | ferramenta · compacto · condensada · compacta · suaves · planas · faixa | Bancada do caso (passos à esquerda, trabalho à direita) | menu com 4 itens; barra de passos dentro do caso; seed com 1 caso |

### Etapa 4 · Um repositório por app no GitHub

Só depois da etapa 3 de cada app, e **com a confirmação do professor** (publicar
é ação externa):

1. Os logins dos alunos estão em `Apps/_base/equipes.json` e na tabela "Equipes
   e GitHub" do `Apps/README.md`.
2. Para cada app, a pasta `Apps/<app>/` inteira vira a raiz do repositório
   (`index.html` gerado, `app.json`, `src/`, `nucleo/`, `testes/`, `exemplos/`,
   `modelos/`, `vendor/`, documentos). Caminho sugerido, sem perder o histórico:
   `git subtree split --prefix "Apps/<app>" -b app-<app>` e depois
   `gh repo create <dono>/<app> --private --source . ` com push do ramo
   `app-<app>` para `main`.
3. Em cada repositório novo, ativar o GitHub Pages na raiz (o app é um
   `index.html` offline).
4. Decidir com o professor se `Apps/` continua no repositório do curso
   (monorrepo de origem) ou se passa a ser só um índice com links.

### Etapa 5 · Documentação

- `AGENTS.md` seção 3.8: trocar "edite as fontes ... gerado por
  `Apps/_base/construir.py` a partir de `_base/base.html`" por "cada app é
  autônomo: `nucleo/`, `construir.py` e `testes/` próprios; `_base/` é só
  molde". Atualizar a tabela de ferramentas e a sequência de comandos.
- `Apps/README.md`: estrutura nova de pasta e comandos.
- `Apps/IDENTIDADE-VISUAL.md`: tokens novos e a tabela da Parte D, com a regra
  "comum só a faixa do governo, o rodapé, o foco, o tema claro padrão e o A−/A+".
- `Apps/CONTINUAR.md`: apontar para este arquivo no topo.
- `Apps/painel.py` e `Apps/_base/hub_apps.py`: conferir se ainda leem os
  arquivos certos (eles leem `app.json` e `sprint.md`, que não mudaram).

---

## 4. Regras para quem continuar

- **Nunca edite `index.html`.** Edite `app.json`, `src/`, `nucleo/` e rode
  `python construir.py` dentro da pasta do app.
- **Nenhum app importa nada de fora da própria pasta.** Se uma melhoria serve a
  vários apps, faça em cada um e adapte à identidade dele.
- **Não rode `_base/separar.py --forcar`**: ele sobrescreve o núcleo e os testes
  personalizados.
- `src/identidade.js` entra por último no build: use para redefinir telas sem
  apagar o código dos sprints.
- Store novo no banco: acrescente em `app.json → db.stores` e suba `db.versao`.
- Tema claro é o padrão; o escuro só pelo botão. Fonte de 80% a 150% (A−/A+).
- Offline: sem CDN, sem rede (o `testar.py` reprova qualquer requisição).
  Fontes só do sistema (Segoe UI, Georgia/Cambria, Bahnschrift, Consolas,
  Trebuchet MS).
- Texto em português do Brasil com acentuação, sem travessões e sem
  adjetivações (padrão do repositório, `AGENTS.md` seção 5.2).
- O perfil é uma lente de demonstração, **não é segurança**.
- No Git Bash, rotas como `#/corpo/C-0001` passadas como argumento viram
  caminho; use `MSYS_NO_PATHCONV=1` ou o PowerShell.
- Commit só do que é da entrega; os arquivos da `Aula 4/` ficam de fora.

---

## 5. Prompt para a próxima IA

Copie e cole:

```text
Você vai continuar o trabalho nos 20 mini apps do curso POLITEC/MT, no
repositório "D:\Dev\Aula Politec" (pasta Apps/).

Leia, nesta ordem, antes de qualquer alteração:
1. Apps/CONTINUAR-IDENTIDADE.md  (o que o professor pediu, o que foi feito, o que falta)
2. Apps/PLANO-USABILIDADE.md     (Parte B: plano de cada app; Parte D: identidade de cada app)
3. AGENTS.md, seção 3.8 e seção 5.2 (regras do repositório e do texto)

Contexto: o professor pediu que (1) cada app tenha um plano próprio de
navegabilidade, layout e usabilidade; (2) cada app seja único, sem parecer com os
outros; (3) não exista base comum: cada app tem construção independente, porque
cada um vai para o próprio repositório no GitHub. A separação já foi feita: cada
Apps/<app>/ tem nucleo/ (casca.html, visual.css, icones.js, comum.js),
construir.py, testes/testar.py e testes/cenarios.py. O seletor de perfil já é um
menu suspenso no cabeçalho, sem tela de bloqueio.

Comece pela Etapa 1 do CONTINUAR-IDENTIDADE.md (seção 3): resolver os 2 cenários
que falham (adiantamento s5 e agendamento-cin s6; hipótese: 02/11 é feriado),
configurar "rotaInicial" nos dois apps do cidadão, escrever "Como construir e
testar" no README de cada app e fazer o commit da separação (sem os arquivos da
Aula 4/).

Depois siga a Etapa 3, um app por vez, na ordem indicada: bloco "visual" da
Parte D, núcleo divergente quando a forma da tela pedir, tela-assinatura em
src/identidade.js, itens P1 e P2 da Parte B, testes do app passando, captura de
tela olhada no desktop e no celular, e um commit por app. Ao terminar cada app,
atualize a seção 2 do CONTINUAR-IDENTIDADE.md (o que foi feito) e risque o app
no checklist da seção 3.

Não crie repositórios no GitHub nem faça push sem a confirmação do professor.
Nunca edite index.html direto; nunca importe nada de fora da pasta do app; não
rode _base/separar.py --forcar.
```
