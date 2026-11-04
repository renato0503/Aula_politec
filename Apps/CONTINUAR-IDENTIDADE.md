# Continuar: apps independentes, com identidade própria e usabilidade revisada

Registro de 02/11/2026 para outra IA continuar o trabalho. Leia este arquivo
inteiro antes de mexer em qualquer app. Depois leia
`Apps/PLANO-USABILIDADE.md` (o diagnóstico e o plano de cada app) e
`AGENTS.md` (seção 3.8).

> **Estado global de 03/11/2026:** `ANALISE-GLOBAL-PENDENCIAS.md` traz a matriz
> dos 21 apps, o que pode ser feito agora, o que depende de pessoas e o que
> depende de serviço externo. Ele exclui `horus-banco-demandas` (Iohan) e
> `agendamento-cin` (Elthon), pausados por decisão do professor.

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
  `anel`). Todos os apps receberam os valores da Parte D no bloco `visual` do `app.json`
  e a tela-assinatura em `src/identidade.js` (ver 2.7).
- `src/identidade.js` (se existir) entra **por último** no build, depois de
  todos os sprints. É o lugar da tela-assinatura de cada app.

### 2.4 Estado dos testes (03/11/2026)

- `Apps/_base/testar.py`: **21 de 21 apps OK**.
- `Apps/_base/testar_sprints.py`: **92 de 92 cenários OK**.
- Jornada do cliente: **21 apps, 158 passos no Chromium**, 0 erros.
- Lightpanda 1.0.2: **19 de 21 apps**; as 2 falhas são limitações do navegador
  (redução de imagem no `cin-segunda-via` e upload de pasta no `agiliza-mais`).
- O TEIA passa no Chromium e no Lightpanda (10/10 passos).
- As três causas históricas dos cenários que falhavam em 02/11 estão resolvidas:
  datas do seed do agendamento, esperas fixas nos testes e o botão de pendência
  do adiantamento que disparava submit.

### 2.5 O que **não** foi feito ainda

- **P2/P3 do `JORNADA-BACKLOG.md`**: matriz do TAP com escala, funil x barra da
  Comissão, perfis e “Minha fila” do Adiantamento, conferência do
  DOCUMENTAPOLITEC sem redesenhar a ficha, ficha do contêiner na Custódia,
  kanban no celular em Aquisições, contexto do Hórus em chip, menu do Metas,
  Biblioteca/Histórico do Agiliza e nome do fiscal na renovação.
- **TEIA**: a extração é simulada; faltam parsing real de e-mail/PDF, OCR,
  renomeação de arquivos e integração com a caixa institucional.
- **GitHub Pages**: os 21 repositórios são públicos, mas o Pages ainda não foi
  ligado na raiz de cada um.
- **Acessos**: 2 logins não existem na API (`Linickeraraujo-sd` e
  `Vitoriadias-droide`); 5 alunos sem login; o convite do Nelson para o TEIA e
  para o DNA está pendente de aceite.
- **Documentação**: `Apps/IDENTIDADE-VISUAL.md` e `Apps/CONTINUAR.md` ainda
  precisam refletir os 21 apps, os hubs e os diagramas; `AGENTS.md` e
  `Apps/README.md` já foram atualizados em parte.
- Os `.xlsx` e `.pbix` da `Aula 4/` continuam fora dos commits deste trabalho.

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

Os 20 apps foram feitos na ordem da seção 3, com um commit próprio por app, e o
TEIA entrou depois como o 21º. O que foi feito em cada um está resumido aqui e no
`README.md` e no `sprint.md` do app. Todos os `testar.py` e `cenarios.py` passam,
e a captura de tela foi conferida no desktop (1366 px) e no celular (390 px).

| App | Commit | O que mudou |
|---|---|---|
| agendamento-cin | `9620680` | Casca de cidadão, cabeçalho claro, Trebuchet, densidade ampla, cantos redondos. Calendário do mês com vagas por dia e horários em botões grandes; passos 1-2-3; grade semanal de ocupação com cor por situação; busca por protocolo, nome ou CPF na agenda do posto. |
| cin-segunda-via | `5d7dc14` | Casca de cidadão, Trebuchet, cantos redondos, KPI em número. Caixa de entrada com a fila à esquerda e o pedido à direita; busca por protocolo, nome ou CPF; espera em horas; atalhos J/K/A/R; “Aceitar e próximo” e “Recusar e próximo”. |
| horus-banco-demandas | `7d66872` | Casca lateral, degradê, fonte do sistema, cantos redondos, KPI em número. Vitrine com facetas e contagem, filtros em uma linha, ordenação, alternância cartões/tabela e contexto de unidade em Gerente e Usuário setorial. |
| trilha-custodia-necropsia | `27ede63` | Casca de trilho, cabeçalho sólido, condensada, ampla, cantos suaves, planas, KPI em número. Painel por perfil, quadro de plantão em colunas e ficha em abas. |
| controle-aquisicoes | `cdd53af` | Casca de ferramenta, degradê, condensada, compacta, cantos suaves, planas, KPI em faixa. Kanban das 9 etapas, ficha em abas com `.etapas` e ações por perfil. |
| custodia-definitiva | `94c52ee` | Casca de trilho, cabeçalho sólido, condensada, cantos retos, planas, KPI em número. Balcão de leitura do lacre, mapa das prateleiras com barra e painel do gestor só para o gestor. |
| documentapolitec | `381dbb3` | Casca lateral, sólido, serifa, cantos retos, papel, KPI em barra. Menu de 8 para 5, estante de lombadas, conferência por leitura e ficha em abas. |
| gestao-documentos | `f6a185f` | Casca lateral, sólido, serifa, cantos suaves, papel, KPI em barra. Caixa por perfil com prazo em barra, ficha em abas, checklist com caixa e assinatura só da autoridade. |
| renovacao-contratos-horus | `024ccc0` | Casca lateral, sólido, condensada, compacta, cantos retos, planas, KPI em número. Régua de 0 a 180 dias, semáforo em barra clicável, “Meus contratos” e ficha em abas. |
| distribuicao-casos-dna | `09611ca` | Casca de topo, degradê, sistema, redondos, cartões, KPI em anel. Placa de 96 poços, “Meus casos” do perito e rodada em abas. |
| comissao-etica-denuncias | `df06711` | Casca lateral, sólido, serifa, ampla, cantos retos, papel, KPI em faixa. Funil de 7 etapas, dossiê “Reservado” com barra de etapas e seed distribuído. |
| passivo-ambiental | `c878f27` | Casca de topo, degradê, sistema, cantos suaves, cartões, KPI em faixa. Fila de laudos com prazo e miniatura, painel do perito separado, laudo em abas e seed relativo a hoje. |
| rnc-nao-conformidade | `dd87047` | Casca lateral, sólido, sistema, cantos suaves, cartões, KPI em faixa. Quadro por etapa do ciclo e setor como contexto do perfil. |
| tap-portfolio-projetos | `3764f41` | Casca de topo, degradê, serifa, ampla, redondos, cartões, KPI em anel. Matriz valor × prioridade e início por perfil (Equipe → Triagem; Autoridade → Portfólio). |
| ~~adiantamento~~ ✅ | `21dab84` | Casca lateral, sólido, mono, compacta, cantos retos, planas, KPI em número. Tela `#/processos` com régua de prazos e prazo em destaque no topo da ficha. |
| ~~metas-bi-ocr~~ ✅ | `88339a3` | Casca de topo, claro, sistema, ampla, cantos suaves, cartões, KPI em anel. Ano em 12 meses com situação e passos 1-2-3. |
| ~~inscricoes-cursos~~ ✅ | `a5b7dad` | Casca de topo, degradê, arredondada, ampla, redondos, cartões, KPI em faixa. Cartões de curso com esteira e tela central do curso. |
| mapa-distribuicao-credor | `73bcfe2` | Casca de ferramenta, compacto, mono, compacta, cantos retos, planas, KPI em número. Esteira das 8 etapas e grade em planilha. |
| equipamentos-google-earth | `7962463` | Casca de ferramenta, compacto, sistema, compacta, cantos suaves, planas, KPI em número. Mapa de MT em SVG com 142 municípios e pinos das unidades; contexto de unidade. |
| agiliza-mais | `59a1109` | Casca de ferramenta, compacto, condensada, compacta, cantos suaves, planas, KPI em faixa. Bancada do caso com 6 passos à esquerda e menu sem os passos. |
| ~~teia-triagem-emails~~ ✅ | `9c05d21` | Casca de ferramenta, compacto, mono, compacta, retos, planas, número. Bancada de triagem (fila + 8 campos), validação humana, alertas, lotes, planilha e CSV; hub com figuras Mermaid. |


### 2.8 TEIA · o 21º app (03/11/2026)

O Nelson e a Luciana enviaram uma **nova entrada** no formulário da Aula 8
(`Projeto TEIA · Triagem de E-mails com Isolação Automatizada`). Ela é a nova etapa do projeto do Nelson e Luciana. Por isso o TEIA virou o
**21º app**, em
`Apps/teia-triagem-emails/`, e o `distribuicao-casos-dna` continua como a fase
anterior.

- Entrada original: `Aula 8/Entregas/TEIA - Nelson e Luciana - 2026-11-03.json`.
- `projeto.json`, `PROJETO.md`, `contexto.md` e `sprint.md` próprios.
- MVP com bancada de triagem (fila + 8 campos), validação humana, alertas de
  divergência/OCR, lotes, planilha e CSV.
- `testes/testar.py`, `testes/cenarios.py` (3 cenários) e `testes/jornada.py`
  (Chromium e Lightpanda).
- `docs/diagramas/` com as fontes `.mmd`, os SVG e o `processo.md`.
- `processo.html` com AS-IS/TO-BE, figuras Mermaid (`docs/diagramas/as-is.svg`
  e `to-be.svg`) e as tabelas do projeto.
- Repositório público `renato0503/teia-triagem-emails`, com convite de push
  para `nelsonyoshitake` (pendente de aceite).
- `python Apps/_base/testar.py`: 21/21; `testar_sprints.py`: 92/92;
  jornada do cliente 21/21 (158 passos); Lightpanda 19/21 (2 limitações).

### 2.9 Fechamento do MVP e diagramas (03/11/2026)

O registro completo da entrega está em [`ENTREGA-03-11-2026.md`](ENTREGA-03-11-2026.md).

- **21 apps** com identidade, testes, jornada, repositório e hub.
- **Hubs `processo.html`** em todos os apps, com AS-IS/TO-BE, KPIs, regras,
  papéis, métricas, como testar e **duas figuras Mermaid** (AS-IS e TO-BE)
  renderizadas em SVG em `docs/diagramas/`.
- **Repositórios públicos** em `github.com/renato0503`, um por app, com
  convite de colaborador (18 aceitos/convites enviados; 2 logins 404; 5 sem
  login; 1 convite pendente no TEIA e no DNA).
- **Correções de MVP** feitas: Triagem da Diretoria e “Novo curso” em Inscrições,
  tabela de importação no Mapa, paginação em Equipamentos, arquivo de exemplo no
  Metas, passos “em breve” e caso de exemplo no Agiliza, fiscais no seed e botão
  do fiscal na Renovação, poços clicáveis no DNA, aviso da autoridade no topo da
  Gestão, busca na fila do Passivo e `type="button"` nos botões de formulário.
- **Testes**: 21/21 estrutura, 92/92 cenários, 158 passos de jornada no Chromium,
  19/21 no Lightpanda (2 limitações de navegador).
- **Git**: monorepo em `ae7f9fd` (e commits seguintes de docs); repositórios dos
  apps atualizados.

---

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
agiliza-mais, teia-triagem-emails.

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
| ~~cin-segunda-via~~ ✅ | cidadao · claro · arredondada · normal · redondos · cartoes · numero | Caixa de entrada (lista à esquerda, pedido à direita) | `rotaInicial #/pedido`; "Aceitar e próximo"; busca na fila |
| ~~horus-banco-demandas~~ ✅ | lateral · degrade · sistema · normal · redondos · cartoes · numero | Vitrine com filtros em facetas e ordenação | contexto de unidade nos perfis Gerente e Usuário setorial; barra de filtros em uma linha; alternar cartões/tabela |
| ~~trilha-custodia-necropsia~~ ✅ | trilho · solido · condensada · ampla · suaves · planas · numero | Quadro de plantão (colunas por situação, cartões de corpo, botões grandes) | painel por perfil (4 perfis); uma tabela só no painel; ficha em abas |
| ~~controle-aquisicoes~~ ✅ | ferramenta · degrade · condensada · compacta · suaves · planas · faixa | Kanban das 9 etapas da Lei 14.133 | ficha em abas; etapas em `.etapas`; ações por perfil |
| ~~custodia-definitiva~~ ✅ | trilho · solido · condensada · normal · retos · planas · numero | Balcão de leitura do lacre + mapa das prateleiras | campo "Ler lacre"; painel do gestor só para o gestor |
| ~~documentapolitec~~ ✅ | lateral · solido · serifa · normal · retos · papel · barra | Estante de caixas (lombadas) + conferência por leitura | menu de 8 para 5 itens; conferência com campo focado e Enter |
| ~~gestao-documentos~~ ✅ | lateral · solido · serifa · normal · suaves · papel · barra | Caixa por perfil (a instruir, a revisar, a assinar) | ficha em abas; checklist com caixa de seleção; assinatura só da autoridade |
| ~~renovacao-contratos-horus~~ ✅ | lateral · solido · condensada · compacta · retos · planas · numero | Régua de vencimentos de 0 a 180 dias | ficha em abas; semáforo como barra empilhada clicável |
| ~~distribuicao-casos-dna~~ ✅ | topo · degrade · sistema · normal · redondos · cartoes · anel | Placa de 96 poços com a cor do perito | "Meus casos" do perito; rodada em abas |
| ~~comissao-etica-denuncias~~ ✅ | lateral · solido · serifa · ampla · retos · papel · faixa | Funil do processo ético + dossiê "Reservado" | barra de etapas e abas no caso; seed em todas as etapas |
| ~~passivo-ambiental~~ ✅ | topo · degrade · sistema · normal · suaves · cartoes · faixa | Fila de laudos com prazo e miniatura do mapa | laudo em abas; painel do perito separado do gestor; seed com datas de hoje |
| ~~rnc-nao-conformidade~~ ✅ | lateral · solido · sistema · normal · suaves · cartoes · faixa | Quadro por etapa do ciclo | setor como contexto do perfil |
| ~~tap-portfolio-projetos~~ ✅ | topo · degrade · serifa · ampla · redondos · cartoes · anel | Matriz do portfólio (valor × prioridade) | `inicio` por perfil (Equipe → Triagem, Autoridade → Portfólio) |
| ~~adiantamento~~ ✅ | lateral · solido · mono · compacta · retos · planas · numero | Régua de prazos por processo | tela `#/processos`; prazo da prestação de contas no topo da ficha |
| ~~metas-bi-ocr~~ ✅ | topo · claro · sistema · ampla · suaves · cartoes · anel | Ano em 12 meses com a situação de cada mês | assistente em 3 passos; histórico em tabela; "Usar arquivo de exemplo" |
| ~~inscricoes-cursos~~ ✅ | topo · degrade · arredondada · ampla · redondos · cartoes · faixa | Cartões de curso com a esteira Divulgar → Turma | curso como centro com barra de passos; "＋ Novo curso" |
| ~~mapa-distribuicao-credor~~ ✅ | ferramenta · compacto · mono · compacta · retos · planas · numero | Esteira das 8 etapas + grade em formato planilha | barra de etapas em todas as telas `/:proc`; importação em tabela de 3 linhas |
| ~~equipamentos-google-earth~~ ✅ | ferramenta · compacto · sistema · compacta · suaves · planas · numero | Mapa de MT em SVG (os 142 municípios de `dados-base/mt-municipios.json` têm `lat`, `lon` e o polígono `p`) | tela inicial = Equipamentos até o mapa existir; lista paginada; contexto de unidade |
| ~~agiliza-mais~~ ✅ | ferramenta · compacto · condensada · compacta · suaves · planas · faixa | Bancada do caso (passos à esquerda, trabalho à direita) | menu com 4 itens; barra de passos dentro do caso; seed com 1 caso |

### Etapa 4 · Um repositório por app no GitHub (concluída em 03/11/2026)

- Os **21 repositórios públicos** estão em `github.com/renato0503`, um por app.
- A pasta `Apps/<app>/` é a raiz do repositório, com `index.html`,
  `processo.html`, `docs/diagramas/`, `nucleo/`, `construir.py`, `testes/`,
  `exemplos/`, `modelos/` e os documentos.
- Os convites de colaborador com push foram enviados; 2 logins não existem na
  API (`Linickeraraujo-sd`, `Vitoriadias-droide`) e 5 alunos ainda não têm login.
- O **GitHub Pages ainda não foi ligado**; os repositórios são públicos, então
  pode ser ativado na raiz de cada um.
- A dupla Nelson e Luciana tem dois repositórios: `distribuicao-casos-dna`
  (fase anterior) e `teia-triagem-emails` (novo projeto).

### Etapa 5 · Documentação (parcial)

- `AGENTS.md` seção 3.8 e `Apps/README.md` já registram os apps autônomos, o
  TEIA, os repositórios públicos e os testes.
- Falta atualizar `Apps/IDENTIDADE-VISUAL.md` (tokens e Parte D) e
  `Apps/CONTINUAR.md` (apontar para este arquivo, para o TEIA e para os hubs).
- `Apps/painel.py` e `Apps/_base/hub_apps.py`: conferir se leem os 21 `app.json`
  e `sprint.md`; o TEIA já está na pasta.
- Os comandos de Lightpanda e de geração dos diagramas estão neste arquivo e em
  `Apps/_base/gerar_diagramas.py`.

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
Você vai testar e continuar os 21 mini apps do curso POLITEC/MT, no repositório
"D:\Dev\Aula Politec" (pasta Apps/). O trabalho anterior terminou com os apps
autônomos, com identidade própria, testes, hubs, diagramas e repositórios
públicos.

Leia, nesta ordem, antes de qualquer alteração:
1. Apps/CONTINUAR-IDENTIDADE.md
2. Apps/JORNADA-TESTES.md
3. Apps/JORNADA-NAVEGABILIDADE.md
4. Apps/JORNADA-BACKLOG.md
5. AGENTS.md, seções 3.8 e 5.2

Estado atual (03/11/2026):
- 21 apps: os 20 da turma e o TEIA (Triagem de E-mails), do Nelson e Luciana.
  O TEIA é a nova etapa do projeto do Nelson e Luciana; o app de DNA continua como a fase anterior.
- Cada app tem nucleo/ próprio, construir.py, testes/testar.py,
  testes/cenarios.py, testes/jornada.py, processo.html e docs/diagramas/
  (as-is.mmd, to-be.mmd, as-is.svg, to-be.svg e processo.md).
- Testes: python Apps/_base/testar.py = 21/21;
  python Apps/_base/testar_sprints.py = 92/92;
  jornada = 21 apps e 158 passos no Chromium.
- Lightpanda 1.0.2: 19/21; as 2 falhas são limitações do navegador
  (redução de imagem no cin-segunda-via e upload de pasta no agiliza-mais).
- Repositórios públicos em github.com/renato0503, um por app. O TEIA está em
  teia-triagem-emails. O convite de push do Nelson está pendente; 2 logins
  não existem na API e 5 alunos não têm login.
- GitHub Pages ainda não foi ligado nos repositórios.
- Os arquivos da Aula 4/ não entram nos commits.

O que falta (detalhado em JORNADA-BACKLOG.md):
1. Completar as 22 rotas em 4 apps: mapa-distribuicao-credor, inscricoes-cursos,
   equipamentos-google-earth e agiliza-mais.
2. Fechar os P2/P3: matriz do TAP com escala; unificar funil e barra da Comissão;
   perfis e "Minha fila" do Adiantamento; conferência do DOCUMENTAPOLITEC sem
   redesenhar a ficha; ficha do contêiner na Custódia; kanban no celular em
   Aquisições; contexto do Hórus em chip; menu de conferência/geração do Metas;
   Biblioteca/Histórico do Agiliza; nome do fiscal na renovação.
3. TEIA: trocar a extração simulada por parsing real de e-mail/PDF, OCR,
   renomeação e integração com a caixa institucional, mantendo o app offline e a
   validação humana.
4. Ativar GitHub Pages na raiz de cada repositório, se o professor confirmar.
5. Corrigir os 2 logins 404 e cobrar os 5 logins que faltam.
6. Conferir Apps/IDENTIDADE-VISUAL.md e Apps/CONTINUAR.md.

Como testar:
- Tudo: python Apps/_base/testar.py && python Apps/_base/testar_sprints.py
- Um app: cd Apps/<app>; python construir.py; python testes/testar.py;
  python testes/cenarios.py; python testes/jornada.py
- Lightpanda: suba o binário no WSL, o servidor CDP em 9222 e o HTTP em 8000;
  depois: python testes/jornada.py --cdp http://127.0.0.1:9222 --base http://127.0.0.1:8000
- Diagramas: python Apps/_base/gerar_diagramas.py (Mermaid local em
  C:\Users\Renato\AppData\Local\Temp\mermaid-render)
- Hubs: python Apps/_base/gerar_hubs.py

Regras:
- Nunca edite index.html direto; edite app.json, src/, nucleo/ e rode
  construir.py dentro da pasta do app.
- Nenhum app importa nada de fora da própria pasta.
- Não rode Apps/_base/separar.py --forcar.
- Commit só do que é da entrega; a Aula 4/ fica de fora.
- Tema claro é o padrão; fonte 80% a 150%; offline, sem CDN no app.
- O perfil é lente de demonstração, não segurança.

Comece rodando os testes completos e a jornada do TEIA. Depois escolha o primeiro
P2 do backlog, corrija na fonte, rode construir.py, testar.py, cenarios.py e
jornada.py, olhe as capturas no desktop e no celular e faça um commit por app.
```
