# Plano de navegabilidade, layout e usabilidade dos 20 apps

> **Depois desta análise o professor pediu apps sem base comum.** Onde este plano diz "base" ou `Apps/_base/`, leia "o `nucleo/` de cada app". O estado do trabalho e o prompt de continuação estão em `Apps/CONTINUAR-IDENTIDADE.md`.

Análise de 02/11/2026. Este plano registra o que cada MVP faz hoje na tela, o que
atrapalha quem usa e o que mudar, em ordem de prioridade. A Parte A trata da
**base comum** (`Apps/_base/`), porque uma correção ali chega aos 20 apps de uma
vez. A Parte B traz o **plano individual de cada app**. A Parte C organiza tudo
em ondas de entrega.

## Como a análise foi feita

- Os 20 `index.html` foram abertos no Chromium (Playwright), com os dados
  fictícios carregados e cada perfil ativo.
- Foram capturadas **102 telas de menu** (1366 px), **17 fichas de detalhe**,
  **20 telas de entrada** (primeira abertura, sem perfil) e **20 telas no
  celular** (390 px).
- Em cada tela foram medidos: altura da página, rolagem horizontal, número de
  botões, campos, tabelas, linhas, cartões e KPIs. As medidas citadas abaixo
  vêm dessa coleta.
- O código de `base.html`, `visual.css` e dos `src/*.js` foi lido para achar a
  causa de cada problema.

Legenda de prioridade: **P1** atrapalha o uso ou passa informação errada;
**P2** custa tempo em toda sessão; **P3** acabamento.

---

# Parte A · Diagnóstico da base comum (vale para os 20 apps)

## A1. O seletor de perfil é uma tela que bloqueia o app (P1)

**Hoje.** Em 16 apps com perfis, a primeira abertura mostra só a tela "Escolha o
perfil desta cópia" (`telaEscolherPerfil()` em `base.html`, linha 364). O menu
some, nenhuma tela do app aparece e a pessoa precisa escolher antes de ver
qualquer coisa. Para trocar depois, o caminho é Configuração → "Trocar perfil",
que **apaga o perfil** e volta à tela de bloqueio. No Hórus são 6 cartões
(ADM, Diretor, Coordenador, Gerente, Usuário setorial, Inventariante) antes de
qualquer conteúdo.

**Por que é ruim.** O perfil, nestes apps, é uma lente de demonstração e não
controle de acesso (o próprio código diz isso). Em sala e na validação com o
setor, a pessoa quer comparar o que cada papel vê, e cada troca custa 4 cliques
e uma tela vazia no meio.

**Proposta: perfil em menu suspenso no cabeçalho, trocável a qualquer momento.**

1. **Nada de tela de bloqueio.** Sem perfil gravado, o app entra no perfil
   padrão (`APP.perfilPadrao`, ou o primeiro da lista) e mostra um aviso uma
   única vez: "Você está como Coordenador. Troque o perfil no alto da tela."
2. **Botão no cabeçalho**, no lugar do selo `#perfilAtual`:
   `[ícone pessoa] Coordenador ▾`. Mostra o **nome** do perfil (hoje o selo
   mostra o id: "ADM", "posto", "coordenadoria", "USUARIO_SETORIAL").
3. **Menu suspenso** com um item por perfil: nome em negrito, descrição curta
   embaixo e marca no perfil atual. Itens com `role="menuitemradio"` e
   `aria-checked`, setas para navegar, Enter para escolher, Esc ou clique fora
   para fechar. Atalho `Alt+P` abre o menu.
4. **Ao trocar:** grava em `meta.perfil`, registra no log
   (`perfil trocado: de X para Y`), refaz o menu e **fica na mesma tela** se o
   novo perfil puder vê-la. Se não puder, vai para a tela inicial do novo
   perfil e avisa: "Coordenador não usa Nova demanda. Você foi para Banco."
5. **Tela inicial por perfil.** Novo campo opcional `perfis[].inicio` no
   `app.json` (ex.: no TAP, `equipe` abre em `#/triagem`, e não no formulário de
   Novo TAP, que é a primeira rota permitida hoje).
6. **Contexto do perfil (opcional).** Alguns perfis dependem de uma lotação: o
   perfil "Setor" da RNC escolhe o setor dentro da tela "Minhas RNCs" a cada
   visita; o "Gerente de unidade" do Hórus e a "Unidade" dos Equipamentos
   precisam de uma unidade. Novo campo `perfis[].contexto =
   {store, campo, rotulo}` faz o menu suspenso mostrar um segundo seletor
   ("Setor: LQF ▾") logo abaixo do perfil.
7. **Rotas públicas** (cidadão e candidato): o seletor some e o cabeçalho mostra
   só um link discreto "Área do servidor".
8. **Configuração** continua com o cartão "Perfil desta cópia", mas como lista
   de opções (sem apagar o perfil). Os botões mantêm `data-perfil`, para o
   `testar.py` seguir funcionando. Os cenários dos sprints usam
   `db.meta('perfil', ...)` e não mudam.
9. Um rodapé no menu suspenso deixa claro: "O perfil escolhe as telas. Não é
   controle de acesso."

Esboço da mudança em `base.html`:

```js
// partida: sem tela de bloqueio
if (APP.perfis){
  estado.perfil = (await db.meta("perfil")) || APP.perfilPadrao || APP.perfis[0].id;
  if (!(await db.meta("perfil"))){ await db.meta("perfil", estado.perfil); avisoPerfilInicial = true; }
}

async function trocarPerfil(novo){
  const de = estado.perfil; if (novo === de) return fecharMenuPerfil();
  estado.perfil = novo; await db.meta("perfil", novo);
  await registrar("perfil trocado", {detalhe: `${de} -> ${novo}`});
  montarMenu(); montarSeletorPerfil();
  const atual = casarRota(location.hash || APP.rotas[0].rota);
  if (atual && rotaPermitida(atual.r)) return navegar();
  const p = APP.perfis.find(x=>x.id === novo);
  toast(`${p.nome} não usa esta tela. Você foi para a tela inicial do perfil.`);
  location.hash = p.inicio || APP.rotas.find(rotaPermitida).rota;
}
```

## A2. Apps do cidadão abrem na tela de perfil (P1, defeito)

**Hoje.** `agendamento-cin` e `cin-segunda-via` têm a tela pública como primeira
rota, mas, aberto o endereço sem `#`, o teste de `navegar()` compara o hash
vazio com `rotaSemPerfil` e mostra "Escolha o perfil desta cópia" ao
cidadão (tela de entrada capturada nos dois apps). O mesmo vale para
`inscricoes-cursos` quando o candidato abre o link sem o hash.

**Proposta.** Novo campo `APP.rotaInicialPublica`. Hash vazio vai para ela. A
área interna fica em `#/posto`, `#/fila` etc., com o seletor de perfil do item
A1. Junto com A1, o problema deixa de existir.

## A3. Contorno dourado em volta do conteúdo em todas as telas (P1, defeito visual)

**Hoje.** Toda navegação chama `alvo.focus()` no `<main>`. A regra
`:focus-visible{outline:3px solid ouro}` vence `main{outline:none}` por
especificidade, e o conteúdo aparece emoldurado por uma borda amarela nas 102
telas capturadas. Parece um erro de validação ou um item selecionado.

**Proposta.** Em `visual.css`: `main:focus,main:focus-visible{outline:none}`.
O foco continua indo para o `<main>` (leitor de tela anuncia a troca de tela),
sem o contorno.

## A4. Telas de detalhe sem lugar no menu e sem caminho de volta (P1)

**Hoje.** Em rotas com `:id` (processo, caso, contrato, corpo, vestígio...),
nenhum item do menu fica marcado, porque `navegar()` procura um link com
`data-rota="#/processo/:id"`, que não existe. Só `custodia-definitiva` e o
Hórus têm um link "← voltar". A pessoa perde a referência de onde está.

**Proposta.**
- Campo `rotas[].pai` no `app.json` (`"#/processo/:id"` → pai `"#/processos"`).
  O item pai fica marcado no menu.
- **Trilha (breadcrumb)** acima do `h1`, gerada pela base:
  `Processos › 2026.1000-SD › Pesquisa de preços`.
- `Esc` ou o atalho `Alt+←` volta ao pai.

## A5. Fichas de detalhe longas, com os blocos de cada sprint empilhados (P1)

**Hoje.** Cada sprint acrescentou um cartão no fim da ficha. Resultado medido:
aquisições 4.332 px (21 cartões, 20 campos), renovação de contratos 3.191 px,
TCIN 2.497 px, gestão de documentos 2.481 px, DNA 2.271 px, documentapolitec
2.129 px. Para registrar uma análise jurídica no processo de aquisição, a
pessoa rola 3 telas e meia.

**Proposta: componente de abas na base** (`abas([{id, titulo, conta, html}])`):
- Cabeçalho fixo da ficha com: identificador, selo de situação, 3 ou 4 KPIs e
  a **ação principal** do momento (ex.: "Concluir etapa DFD").
- Abas com contador ("Pendências 2", "Documentos 5"). A aba fica no hash
  (`#/processo/AQ-0001?aba=precos`), para o link poder ser compartilhado e para
  o voltar do navegador funcionar.
- Etapas do processo no componente `.etapas` (já existe em `visual.css` e quase
  não é usado) em vez de lista numerada em texto.

## A6. Ações aparecem para perfis que não podem executá-las (P1)

**Hoje.** O perfil filtra o **menu**, mas não os **botões** dentro das fichas.
Exemplos capturados: o perfil "requisitante" vê "Registrar análise" e
"Concluir etapa DFD" no processo de aquisição; o "servidor" vê "Assinar e
concluir", que é ato da autoridade, na gestão de documentos; o "operador" do
TCIN vê o "Painel do gestor". Seis apps nem consultam `estado.perfil` nas telas
(`adiantamento`, `agiliza-mais`, `inscricoes-cursos`, `mapa-distribuicao-credor`,
`metas-bi-ocr`, e `rnc` só uma vez).

**Proposta.** Helper na base `pode(acao)`, lido de `APP.permissoes =
{"assinar": ["autoridade"], ...}`. A ação sem permissão aparece **desabilitada,
com o motivo** ("Só a autoridade decisora assina"), para o perfil entender o
fluxo, ou fica escondida quando não faz sentido para aquele papel.

## A7. Jargão de desenvolvimento na interface (P2)

**Hoje.** 42 títulos de cartão citam o sprint ou a regra de negócio:
"Painel do gestor (Sprint 5)", "Descarte (Sprint 5)", "Etiqueta da caixa
(Sprint 5)", "Fila e produtividade (Sprint 5 e 6)", "Semáforo (R3)",
"Pesquisa de preços (RN04)", "Cabeçalho (RN01)". Além disso, telas pendentes
dizem "O mapa de MT com os pinos chega no Sprint 6".

**Proposta.**
- Tirar "(Sprint N)" de todo título visível.
- O código da regra (RN04) sai do título e vai para um ícone "ⓘ" ao lado, com
  o texto da regra no `title`/popover. Quem valida o app ainda encontra a
  regra; quem usa lê "Pesquisa de preços".
- Telas não construídas saem do menu (ver A10).

## A8. Celular: o cabeçalho ocupa um quarto da tela (P2)

**Hoje (390 px).** A faixa do governo quebra em 3 linhas; o cabeçalho com
emblema, título, selo de perfil, A−/100%/A+ e Tema quebra em 2; o menu quebra
em 2 ou 3 linhas. O conteúdo começa perto de 330 px. Os KPIs ficam um por
linha (4 KPIs = uma tela inteira de rolagem). Em `distribuicao-casos-dna` e
`renovacao-contratos-horus` a **página inteira** rola na horizontal por causa
das tabelas.

**Proposta.**
- Faixa do governo em uma linha no celular ("Governo de MT · POLITEC").
- **Botão "Exibição"** (ícone Aa) com A−, A+, 100% e Tema dentro de um menu
  suspenso, no celular e no desktop. Libera espaço para o seletor de perfil.
- **Menu compacto** abaixo de 900 px: botão "☰ Telas" que abre uma gaveta, ou
  barra inferior com até 4 itens nos apps de campo (TCIN, custódia).
- KPIs em grade de 2 colunas no celular.
- Tabela larga vira **lista de cartões** abaixo de 640 px (classe
  `.tabela-responsiva` com `data-rotulo` em cada `td`), ou fica com rolagem
  apenas dentro do cartão, nunca da página.

## A9. Listas sem paginação, ordenação nem busca padrão (P2)

**Hoje.** A lista de equipamentos tem 151 linhas e 10.371 px de altura. A fila
da segunda via tem 23 linhas sem busca e sem ordenação. Cada app escreveu seu
próprio filtro, com aparência diferente.

**Proposta.** Componente de lista na base (`listaTabela({colunas, linhas,
busca, filtros, porPagina})`): busca com `.busca-grande`, chips de filtro,
ordenação ao clicar no cabeçalho, 25 linhas por página, contador "25 de 151",
exportação CSV do filtro e estado vazio com ação ("Nenhum equipamento.
Cadastrar equipamento").

## A10. Telas pendentes aparecem no menu (P2)

**Hoje.** `agiliza-mais` mostra 10 itens no menu e 8 levam a "Esta tela é
construída no Sprint N". Em `equipamentos-google-earth` são 5 de 9 (incluindo a
tela inicial, o Mapa). Em `inscricoes-cursos`, Importar e Triagem.

**Proposta.** `montarMenu()` esconde rotas cuja tela não existe em `TELAS`,
exceto com `?dev=1` no endereço (para o professor mostrar o roteiro). A tela
inicial passa a ser a primeira rota **construída**.

## A11. KPIs que não levam a lugar nenhum (P2)

**Hoje.** Os painéis têm de 4 a 9 KPIs ("4 vencidos", "12 com etapa vencida",
"10 fora do prazo"), mas nenhum é clicável. Para ver quais são os 4 vencidos, a
pessoa procura na tabela.

**Proposta.** `kpi(valor, rotulo, link)` na base. O KPI vira link para a lista já
filtrada (`#/processos?situacao=vencido`). KPI com zero fica em cinza, e KPI de
alerta (vencido, atrasado) fica com a borda vermelha.

## A12. Números e rótulos fora do padrão brasileiro (P3)

**Hoje.** "46.8" dias (adiantamento), "1.2 dia(s)" (DNA), rótulos cortados no
painel do adiantamento ("Análise da contabilida", "Autorização do ordenad"),
"manutencoes" sem acento (equipamentos), "repositório ( 15 )" e "todos ( 30 )"
com espaços dentro do parêntese.

**Proposta.** Helper `numBR(v, casas)` com `toLocaleString("pt-BR")`, plural
correto ("1 dia", "2 dias"), e rótulo completo com reticências por CSS
(`text-overflow`) e `title` com o texto inteiro.

## A13. Confirmações com `confirm()` do navegador e mensagens que somem (P3)

**Hoje.** 11 chamadas a `confirm()`/`prompt()` em 8 apps. O toast some em 3,2 s
e só mostra uma mensagem por vez.

**Proposta.** Diálogo próprio na base (`confirmar({titulo, texto, botao,
perigo})`) no visual do app, com o botão destrutivo em vermelho. Toast com
botão "Desfazer" nas ações reversíveis (marcar item, mover vestígio) e
mensagens de erro que só fecham no clique.

## A14. Formulário de criação sempre aberto embaixo da lista (P3)

**Hoje.** `inscricoes-cursos` (Novo curso, 15 campos) e
`mapa-distribuicao-credor` (Novo processo) mostram o formulário inteiro abaixo
da lista, e a lista fica pequena no topo.

**Proposta.** Botão "＋ Novo curso" no cabeçalho da tela, que abre o formulário
em painel lateral ou em rota própria (`#/curso/novo`), como já fazem custódia,
TCIN e aquisições.

## A15. Configuração mistura cadastro do negócio com manutenção técnica (P3)

**Hoje.** Configuração reúne backup, dados fictícios, apagar tudo e, em vários
apps, os cadastros do negócio: categorias e base legal da Comissão de Ética
(3.236 px, 33 campos), feriados do adiantamento (2.713 px, 29 botões), usuários
do agendamento.

**Proposta.** Configuração com abas fixas: **Cadastros** (o que é do negócio),
**Dados** (backup, importar, fictícios, apagar) e **Sobre** (versão, testes,
ajuda técnica). O cadastro grande vira tela própria no menu de quem administra.

## A16. Dados fictícios que não mostram o fluxo (P2)

**Hoje.** Na Comissão de Ética os 10 casos estão em "registro" e 6 dos 7 KPIs
mostram zero. No Passivo Ambiental 10 de 10 requisições estão fora do prazo,
com até 1.124 dias de atraso (datas de 2023). No Metas BI o histórico está
vazio. No Agiliza + não há caso de exemplo. Quem abre o app para avaliar não vê
o fluxo funcionando.

**Proposta.** Regra para todos os `gerar_exemplos.py`: distribuir os registros
por **todas as etapas** do fluxo, com pelo menos 1 caso em cada situação, cerca
de 20% atrasados e datas relativas à data de hoje (`hoje - N dias`), para o
painel não envelhecer.

## A17. Nenhuma busca global (P3)

**Proposta.** Campo de busca no cabeçalho (atalho `/`) que procura pelo
identificador principal do app (protocolo, lacre, número do processo, CPF
parcial) e abre a ficha direto. Cada app declara `APP.buscaGlobal = {store,
campos, rota}`.

---

# Parte B · Plano individual por app

Formato de cada app: **retrato** (layout, perfis, telas), **o que funciona**,
**problemas** com a evidência e o **plano** em três frentes (navegabilidade,
layout, usabilidade), com prioridade. Os itens da Parte A não são repetidos,
exceto quando o app tem um caso particular.

## 1. Controle de Adiantamentos (`adiantamento`)

**Retrato.** Layout lateral, sem perfis, 4 telas no menu (Painel, Novo pedido,
Relatório, Configuração) e 2 fichas (processo e prestação de contas).

**O que funciona.** O painel resume vencidos e a vencer na frase de abertura. A
linha do tempo do processo mostra cada etapa com datas e responsável.

**Problemas.**
- Não existe tela de **lista de processos**. A única entrada para um processo é
  a tabela do painel (2.325 px de altura).
- "Processos por etapa" corta os rótulos ("Análise da contabilida") e o tempo
  médio sai com ponto ("46.8").
- A prestação de contas só abre por link dentro do processo.
- O processo passa por servidor, DAS, contabilidade e ordenador, mas o app não
  tem perfis. Cada pessoa vê tudo e não tem "minha fila".
- Configuração com 2.713 px (lista de 24 feriados com um botão por linha).
- A ficha ainda usa a `linha-tempo` antiga.

**Plano.**
- Navegabilidade
  - P1 Criar `#/processos` com busca por número, servidor e etapa, filtros
    "vencidos" e "vencem em 7 dias" (os KPIs do painel apontam para eles).
  - P2 Ficha do processo com abas: Resumo · Orçamentos · Linha do tempo ·
    Prestação de contas · Pendências.
  - P2 Criar perfis Servidor, DAS, Contabilidade e Ordenador, com o seletor da
    A1, e uma tela "Minha fila" com o que espera aquele papel.
- Layout
  - P2 Etapas no `.etapas` horizontal; tempo por etapa em barras.
  - P3 Feriados em tabela compacta com filtro por ano e escopo, numa tela de
    Cadastros.
- Usabilidade
  - P1 Prazo de prestação de contas em destaque no topo da ficha, com contagem
    regressiva e cor.
  - P3 `numBR` nos tempos médios.

**Pronto quando:** o servidor acha o próprio processo em 2 cliques pela lista e
a DAS abre o app direto na fila dela.

## 2. Agendamento CIN (`agendamento-cin`)

**Retrato.** Layout topo, estilo claro (cidadão), 4 rotas públicas (agendar,
dados, comprovante, consultar) e área interna com perfis Posto e Gestão.

**O que funciona.** Fluxo público com comprovante e consulta. Geração de grade de
horários sem duplicar. Gestão com comparecimento por posto.

**Problemas.**
- **O cidadão abre o endereço e vê "Escolha o perfil desta cópia"** (A2).
- Horários: 6 dias × 16 horários = 96 chips verdes iguais e 103 botões na tela.
  Não dá para ver quais horários já têm reserva, quais estão lotados e quais
  foram bloqueados. "Bloquear o dia" fica colado à data, desalinhado.
- A agenda do posto não tem busca por protocolo ou CPF em destaque, que é a
  ação do balcão.
- Gestão mistura indicadores com o cadastro de usuários do app.

**Plano.**
- Navegabilidade
  - P1 Endereço sem `#` abre `#/agendar`. Área interna por "Área do servidor"
    no rodapé.
  - P1 Fluxo público com passos visíveis: 1 Posto e data · 2 Seus dados ·
    3 Comprovante, com voltar sem perder o que foi preenchido.
  - P2 Gestão em abas: Indicadores · Postos · Usuários.
- Layout
  - P1 Horários como **grade semanal** (dias em colunas, horários em linhas),
    cor por ocupação (livre, parcial, lotado, bloqueado) e número de vagas
    restantes na célula.
  - P2 Público mobile-first: botões de horário com 44 px de altura, data em
    calendário de mês com os dias sem vaga desabilitados.
- Usabilidade
  - P1 Agenda do posto abre com campo grande "Protocolo ou CPF" focado e botões
    Compareceu / Ausente na própria linha.
  - P2 Comprovante com botão "Salvar no celular" (imagem) além de imprimir.

**Pronto quando:** o cidadão agenda pelo celular sem ver nenhuma tela interna e
o servidor do posto marca o comparecimento em 1 busca e 1 clique.

## 3. Agiliza + (`agiliza-mais`)

**Retrato.** Layout lateral, sem perfis, 10 itens no menu. Só Início e Pasta do
caso estão construídos (Sprint 2 e parte do 3).

**O que funciona.** Criar caso e selecionar a pasta do exame. A ideia de
biblioteca de textos.

**Problemas.**
- 8 dos 10 itens do menu levam a "Esta tela é construída no Sprint N".
- Pasta, Conferência, Textos, Quesitos, Gerar laudo e Revisão são **passos de um
  caso**, mas estão no menu como telas soltas. Não dá para saber de qual caso
  se trata.
- Ícones repetidos (pasta em 4 itens).
- Sem caso de exemplo: a tela inicial mostra "Nenhum caso ainda".

**Plano.**
- Navegabilidade
  - P1 Menu com 4 itens: **Casos**, **Biblioteca**, **Histórico**,
    **Configuração**.
  - P1 Dentro do caso (`#/caso/:id/...`), barra de passos fixa: 1 Pasta ·
    2 Conferência · 3 Textos · 4 Quesitos · 5 Gerar · 6 Revisão, com o estado
    de cada passo (feito, atual, bloqueado) e "Próximo passo" no rodapé.
  - P2 Passos não construídos aparecem na barra como "em breve", sem link.
- Layout
  - P2 Lista de casos em cartões com protocolo, aparelho, passo atual e data.
  - P3 Ícone próprio para cada passo.
- Usabilidade
  - P1 Seed com 1 caso de exemplo e uma pasta fictícia, para a validação com o
    perito.
  - P2 Gravar o passo em que o perito parou e reabrir nele.

**Pronto quando:** o perito abre um caso e sabe em que passo está, sem passar
pelo menu.

## 4. Segunda via da CIN (`cin-segunda-via`)

**Retrato.** Layout topo, estilo claro, pedido público e perfis Servidor e Gestão
(2 telas internas: Fila e Indicadores).

**O que funciona.** Fila com chips por situação e contagem. Indicadores com recusas
por motivo.

**Problemas.**
- **O cidadão abre o endereço e vê a tela de perfil** (A2).
- Fila (23 linhas): sem busca, sem ordenação por antiguidade, sem coluna de
  "há quanto tempo espera". "Elegível: não" sem o motivo. Situação em texto
  simples, sem selo.
- O servidor trata pedido por pedido, mas precisa voltar à fila a cada um.
- "Tempo médio do pedido à decisão" aparece como "—" com os dados fictícios.

**Plano.**
- Navegabilidade
  - P1 Endereço sem `#` abre `#/pedido` (A2).
  - P1 Na ficha do pedido, botões "Aceitar e próximo" e "Recusar e próximo",
    que abrem o próximo da fila sem voltar à lista.
- Layout
  - P2 Fila com colunas Espera (horas), Motivo de inelegibilidade e Situação em
    selo. Ordenação padrão: mais antigo primeiro.
  - P2 Pedido público em passos curtos com indicador "Passo 2 de 3".
- Usabilidade
  - P1 Busca por protocolo ou nome na fila.
  - P2 Atalhos de teclado na ficha (A aceitar, R recusar, J/K próximo e
    anterior).
  - P3 Seed com decisões datadas, para o tempo médio aparecer.

**Pronto quando:** o servidor esvazia a fila sem voltar à lista entre um pedido e
outro.

## 5. Comissão de Ética (`comissao-etica-denuncias`)

**Retrato.** Layout lateral, perfis Presidente, Membro e Secretário(a). Menu com 4
itens. O caso tem 6 subtelas (classificação, admissibilidade, oitivas,
documentos, encerramento).

**O que funciona.** Classificação com o artigo e o texto real da LC 112/2002. Etapas
do processo bem definidas.

**Problemas.**
- Os 10 casos fictícios estão em "registro": 6 dos 7 KPIs mostram zero.
- 7 KPIs, um por etapa, ocupam duas linhas e não dão a noção de funil.
- As 6 subtelas do caso só abrem por botão dentro da ficha, cada uma numa rota
  própria, sem marcar onde a pessoa está.
- Configuração com 3.236 px e 33 campos (categorias e base legal).
- O membro (relator) não tem a tela "meus casos".

**Plano.**
- Navegabilidade
  - P1 Ficha do caso com a barra `.etapas` (Registro → Classificação →
    Admissibilidade → Oitivas → Deliberação → Encerramento) e abas para as
    subtelas, marcando a atual.
  - P2 Tela "Meus casos" para o membro, com os casos em que é relator.
  - P2 Categorias e base legal viram tela própria do Presidente ("Base legal").
- Layout
  - P2 Os 7 KPIs viram uma **barra de funil** única com a contagem em cada
    etapa, clicável.
  - P3 Prazo de cada etapa na lista (dias na etapa, com cor).
- Usabilidade
  - P1 Seed com casos em todas as etapas.
  - P2 Aviso de sigilo fixo na ficha ("Conteúdo restrito à Comissão").

**Pronto quando:** o presidente vê o funil com os casos parados e entra em
qualquer etapa de um caso em 1 clique.

## 6. Controle do Processo de Aquisição (`controle-aquisicoes`)

**Retrato.** Layout lateral, perfis Requisitante, Aquisições e Chefia. Menu com 5
itens. A ficha do processo é o centro do app.

**O que funciona.** Base legal da Lei 14.133/2021 em cada etapa. Pesquisa de preços
com média, mediana e alerta de desvio. Trilha de aprovação.

**Problemas.**
- **Ficha com 4.332 px, 21 cartões e 20 campos**: objeto, etapas, anexar,
  documentos, pendência, pendências, histórico, pesquisa de preços, trilha de
  aprovação e modalidade, um embaixo do outro.
- As 9 etapas são uma lista numerada em texto pequeno.
- O aviso vermelho "O ciclo não cabe no prazo" aparece em todo processo, para
  todo perfil. É um problema da configuração dos prazos, não do processo.
- O Requisitante vê "Registrar análise" e "Concluir etapa".
- O painel tem 3 tabelas (2.174 px).

**Plano.**
- Navegabilidade
  - P1 Ficha em abas: Resumo · Documentos (n) · Pendências (n) · Preços ·
    Aprovações · Histórico.
  - P2 Painel por perfil: Requisitante vê "Meus pedidos"; Aquisições vê
    "Etapas vencendo"; Chefia vê o gargalo por etapa.
- Layout
  - P1 Etapas no `.etapas` horizontal com prazo e dias usados em cada uma.
  - P2 Cabeçalho da ficha com a ação da etapa atual ("Concluir etapa DFD")
    sempre visível.
- Usabilidade
  - P1 Ações filtradas por perfil (A6).
  - P2 O aviso de prazo do ciclo sai da ficha e vai para a Configuração.
  - P2 Anexar documento direto na linha do documento exigido ("DFD: falta ·
    Anexar").

**Pronto quando:** a equipe de aquisições registra uma análise sem rolar a
página e o requisitante vê só o que pode fazer.

## 7. Custódia Definitiva (`custodia-definitiva`)

**Retrato.** Layout lateral, perfis Núcleo de Custódia, Perito e Gestor. Menu com 5
itens.

**O que funciona.** Acervo com busca por várias palavras e filtros combinados.
Ficha do vestígio com "← Acervo" (o melhor exemplo de volta entre os 20). Regras
de transferência.

**Problemas.**
- Painel com 2.687 px e 8 KPIs, que inclui "Descarte (Sprint 5)" e "Painel do
  gestor (Sprint 6)" para todos os perfis.
- Contêineres em cartões de texto ("Ocupado: 23 de 200 (folga 177)"), sem barra
  de ocupação.
- O trabalho do balcão começa pela leitura do lacre, mas não há campo de leitura
  rápida.

**Plano.**
- Navegabilidade
  - P1 Campo "Ler lacre" no topo do Acervo e do Painel, focado, aceitando leitor
    de código de barras (Enter abre a ficha ou avisa "lacre não encontrado").
  - P2 Clique no contêiner abre o acervo filtrado por ele.
- Layout
  - P1 Painel por perfil: o bloco do gestor só para o Gestor; descarte em tela
    própria.
  - P2 Contêineres com `.barra` de ocupação (verde até 70%, âmbar até 90%,
    vermelho acima) e condição de conservação em ícone.
- Usabilidade
  - P2 Movimentação em diálogo curto (destino, motivo) a partir da linha do
    acervo, sem abrir a ficha.

**Pronto quando:** o servidor da custódia lê o lacre e movimenta o vestígio em
menos de 30 segundos.

## 8. Distribuição de Casos de DNA (`distribuicao-casos-dna`)

**Retrato.** Layout topo, perfis Coordenador, Perito e Técnico administrativo.
Menu com 5 itens.

**O que funciona.** Sugestão do próximo perito pela rotação. Fila de urgência com
justificativa.

**Problemas.**
- No celular **a página rola na horizontal** (painel com 6 tabelas).
- Painel com 2.580 px; "Painel do coordenador (Sprint 4)"; "1.2 dia(s)".
- O Perito não tem tela própria: vê o painel do coordenador.
- No menu, "Importar protocolos" vem depois de "Configuração".
- Rodada com 2.271 px: distribuir, cobranças e urgências empilhados.

**Plano.**
- Navegabilidade
  - P1 Tela "Meus casos" para o Perito (casos recebidos, por rodada e prazo).
  - P2 Ordem do menu: Painel · Rodadas · Nova rodada · Importar · Configuração.
- Layout
  - P1 Tabelas responsivas (A8), sem rolagem da página.
  - P2 Rodada em abas: Distribuição · Cobranças · Urgências, e um desenho da
    placa (grade de poços) com a cor de cada perito.
- Usabilidade
  - P2 "Aceitar sugestão" em 1 clique, com o motivo da sugestão visível.

**Pronto quando:** o coordenador distribui uma rodada pela sugestão em 2 cliques
e o perito abre direto nos seus casos.

## 9. DOCUMENTAPOLITEC (`documentapolitec`)

**Retrato.** Layout lateral, perfis Papiloscopista e Gestor documental. **8 itens
no menu**, o maior entre os apps com MVP completo.

**O que funciona.** Conferência da caixa com o arquivo digital e trava do lacre
(RN02). Importação com associação de colunas.

**Problemas.**
- Menu fragmentado: Busca e Busca por nome separadas; Importar planilha e
  Relatório da importação separados (o relatório aparece vazio antes de
  importar).
- Painel com "Etiqueta da caixa (Sprint 5)" e "Painel do gestor documental
  (Sprint 6)".
- Conferência da caixa sem campo de leitura sequencial.

**Plano.**
- Navegabilidade
  - P1 Menu com 5 itens: Painel · Caixas · Busca (aba "por nome" para o gestor)
    · Importação (assistente em 3 passos: arquivo, colunas, relatório) ·
    Configuração.
  - P2 Ficha da caixa em abas: Prontuários · Conferência · Etiqueta · Histórico.
- Layout
  - P2 Progresso da caixa ("11 de 12 conferidos") como `.barra` no topo.
- Usabilidade
  - P1 Conferência com campo "Número do prontuário" focado: cada Enter marca o
    item, toca um aviso de "não está na relação" e volta o foco ao campo.
  - P2 Etiqueta com prévia em tamanho real antes de imprimir.

**Pronto quando:** o papiloscopista confere uma caixa de 12 prontuários sem usar o
mouse.

## 10. Mapa de Equipamentos (`equipamentos-google-earth`)

**Retrato.** Layout topo, perfis Coordenadoria, Unidade e Diretoria. **9 itens no
menu**, 5 deles pendentes (Painel, Contratos, Paradas, Importar, Exportar).

**O que funciona.** Base com 142 municípios de MT. Ficha do equipamento. Cadastro
de unidades.

**Problemas.**
- A tela inicial (Mapa) é um texto: "O mapa de MT com os pinos chega no Sprint
  6", mais 5 KPIs. "manutencoes" sem acento.
- **Equipamentos: 151 linhas e 10.371 px**, sem paginação.
- Unidades com 27 botões numa tela.
- 9 itens no menu topo quebram em 3 linhas no celular.
- O perfil Unidade não fixa qual unidade.

**Plano.**
- Navegabilidade
  - P1 Tela inicial = Equipamentos (até o mapa existir); itens pendentes fora do
    menu (A10).
  - P1 Perfil Unidade com contexto (A1, item 6): a lista já vem filtrada pela
    unidade escolhida.
  - P2 Ficha em abas: Dados · Manutenções · Paradas · Contratos · Fotos.
- Layout
  - P1 Lista com paginação, ordenação e filtros em chips (A9).
  - P2 Quando o mapa entrar: mapa à esquerda e lista sincronizada à direita
    (clicar no pino destaca a linha).
- Usabilidade
  - P2 KPIs da Diretoria (parados, sem contrato, em manutenção) clicáveis.

**Pronto quando:** a coordenadoria encontra um equipamento por patrimônio em 1
busca e a unidade só vê os seus.

## 11. Gestão de Documentos (`gestao-documentos`)

**Retrato.** Layout lateral, perfis Servidor, Chefia e Autoridade. Menu com 4
itens.

**O que funciona.** Minutas padronizadas com os dados do processo. Cobrança
automática de prazo. Checklist por etapa.

**Problemas.**
- Ficha com 2.481 px.
- Checklist: o botão "Marcar" fica logo depois do texto, cada um numa posição, e
  o item não tem caixa de seleção.
- O Servidor vê "Assinar e concluir".
- KPI com texto longo ("Autoridade Fictícia") em fonte de 28 px.
- "Painel da chefia (Sprint 6)".

**Plano.**
- Navegabilidade
  - P1 Ficha em abas: Resumo · Documentos e minutas · Checklist · Conclusão ·
    Histórico.
  - P2 "Minha caixa" por perfil: Servidor (a instruir), Chefia (a revisar),
    Autoridade (a assinar).
- Layout
  - P1 Checklist com caixa de seleção alinhada à esquerda e data de quem marcou
    à direita.
  - P2 Prazo como `.barra` ("160% do prazo") em vez de KPI percentual; o
    responsável sai do KPI e vai para a linha de dados.
- Usabilidade
  - P1 Assinatura só para a Autoridade (A6).
  - P2 Prévia da minuta lado a lado com o formulário.

**Pronto quando:** cada perfil abre o app na própria caixa e a autoridade assina
sem ver o checklist da instrução.

## 12. Banco de Demandas · Hórus (`horus-banco-demandas`)

**Retrato.** Layout lateral, **6 perfis** (o caso que mais sofre com a tela de
perfil), menu com 7 itens.

**O que funciona.** Cartões com tipo, unidade, valor e interesse. Filtros por grupo,
unidade e situação. Valor global do filtro.

**Problemas.**
- A primeira tela são 6 cartões de perfil.
- Cartões com o título cortado em "..." (a especificação é o que diferencia os
  itens).
- Filtros num cartão grande, com "Situação" sozinha na segunda linha.
- Sem ordenação (por valor, por data) e sem alternar para tabela.
- "repositório ( 15 )" com espaços.
- "Gerente de unidade" e "Usuário setorial" não fixam a unidade.

**Plano.**
- Navegabilidade
  - P1 Seletor de perfil suspenso com contexto de unidade (A1).
  - P2 Ficha da demanda com Editar, Manifestar interesse e Voltar no topo (já
    existe) e trilha (A4).
- Layout
  - P1 Barra de filtros em uma linha (busca, grupo, unidade, situação, ordenar)
    e botão "Cartões / Tabela".
  - P2 Título do cartão em 3 linhas com o texto inteiro no `title`; valor e
    quantidade em linha própria.
- Usabilidade
  - P2 "Minhas demandas" como filtro rápido para os perfis que criam.
  - P3 Trocar arquivos com a explicação do ciclo (exportar, enviar, importar)
    em passos.

**Pronto quando:** o professor troca entre os 6 perfis sem sair do Banco.

## 13. Inscrições em Cursos (`inscricoes-cursos`)

**Retrato.** Layout topo, perfis Gerência e Diretoria, inscrição pública. 5 das 9
telas pendentes (S4 a S9).

**O que funciona.** Cadastro do curso com vagas por diretoria e total automático.
Divulgação com link de inscrição.

**Problemas.**
- O formulário "Novo curso" (15 campos) fica sempre aberto abaixo da lista.
- "Divulgar" é link e "Editar" é botão, lado a lado.
- Importar e Triagem estão no menu e são telas pendentes.
- As telas do curso (divulgar, inscritos, convocação, turma) são rotas soltas,
  sem ligação visível entre elas.

**Plano.**
- Navegabilidade
  - P1 **Curso como centro**: `#/curso/:id` com a barra de passos Divulgar →
    Importar → Inscritos → Triagem → Convocação → Turma e o estado de cada um.
  - P1 Pendentes fora do menu (A10).
  - P2 Diretoria abre em "Triagem" com só os cursos da diretoria dela.
- Layout
  - P1 "＋ Novo curso" abre o formulário em rota própria (A14).
  - P2 Lista de cursos em cartões com a situação (inscrições abertas, em
    triagem, turma formada) e as datas-chave.
- Usabilidade
  - P2 Ações da linha com o mesmo tipo de controle (dois botões).

**Pronto quando:** a gerência acompanha um curso do cadastro à turma sem voltar à
lista.

## 14. Mapa de Distribuição (`mapa-distribuicao-credor`)

**Retrato.** Layout lateral, sem perfis, **2 itens no menu** (Processos,
Configuração) e 8 telas dentro do processo (S4 a S8 pendentes).

**O que funciona.** Importação de 3 fontes com associação de colunas guardada como
modelo. Resumo do que foi lido.

**Problemas.**
- Dentro do processo não há navegação entre as 8 etapas. A pessoa volta à lista
  e usa os links "Importar · Mapa" da linha.
- A tela de importação usa 3 cartões grandes para 3 botões de arquivo.
- "Novo processo" sempre aberto; "Carregar exemplo" solto no fim da página.

**Plano.**
- Navegabilidade
  - P1 Barra de etapas do processo, fixa no topo de todas as telas `/:proc`:
    1 Importar · 2 Mapa · 3 Resultado · 4 Empresas · 5 Conferência ·
    6 Orçamentária · 7 Exportar · 8 Auditoria, com estado (feito, atual,
    bloqueado) e "Próxima etapa".
  - P2 O processo aberto aparece no menu lateral com as etapas como subitens.
- Layout
  - P1 Importação como tabela de 3 linhas (fonte, arquivo, situação, linhas
    lidas, botão), com o resumo ao lado.
  - P2 "＋ Novo processo" e "Carregar exemplo" no cabeçalho da lista.
- Usabilidade
  - P2 Validação mostra a linha e a coluna do erro na planilha.

**Pronto quando:** o setor de licitações percorre as etapas de um processo só com
"Próxima etapa".

## 15. Metas pelo BI (`metas-bi-ocr`)

**Retrato.** Layout topo, sem perfis, 3 itens no menu, fluxo por mês
(importar → conferir → gerar planilha).

**O que funciona.** Fluxo curto. Aviso sobre PDF sem camada de texto.

**Problemas.**
- Histórico vazio, sem orientação, mesmo com 3 arquivos de exemplo embutidos.
- Conferência e geração só abrem depois de importar, sem indicação do passo.

**Plano.**
- Navegabilidade
  - P1 Assistente do mês com passos: 1 Importar · 2 Conferir · 3 Gerar
    planilha.
  - P1 Histórico em tabela (mês, origem, situação, pendências, ações "Continuar"
    e "Baixar planilha").
- Layout
  - P2 Conferência com as divergências no topo e as linhas corretas recolhidas.
- Usabilidade
  - P1 Botão "Usar arquivo de exemplo" na importação e seed com 1 mês já
    conferido.
  - P2 Arrastar e soltar o arquivo.

**Pronto quando:** quem abre o app pela primeira vez gera a planilha de exemplo em
3 passos.

## 16. Passivo Ambiental (`passivo-ambiental`)

**Retrato.** Layout topo, perfis Perito e Gestor, menu com 4 itens; o laudo tem 3
rotas (laudo, mapa, PDF).

**O que funciona.** Editor de mapa com elementos obrigatórios. Laudo em formato A4.
Assinatura.

**Problemas.**
- Painel com 2.463 px: 10 de 10 requisições "fora do prazo", com até 1.124 dias
  (datas de 2023).
- "Assinatura do laudo (Sprint 4)" e "Fila e produtividade (Sprint 5 e 6)".
- Laudo, mapa e PDF em 3 rotas, ligadas só por links.
- O Gestor não abre o laudo (a rota é só do Perito), mas vê a lista.

**Plano.**
- Navegabilidade
  - P1 Laudo em abas: Cabeçalho · Mapas · Conclusão · Assinatura · PDF.
  - P2 Gestor abre o laudo em modo leitura.
- Layout
  - P1 Painel do Perito (minha fila por prazo) separado do painel do Gestor
    (produtividade).
- Usabilidade
  - P1 Seed com datas relativas a hoje e no máximo 20% atrasados (A16).
  - P2 Pendências do laudo antes de assinar ("Falta o mapa de uso do solo").

**Pronto quando:** o perito vai do cabeçalho ao PDF assinado sem sair da ficha.

## 17. Renovação de Contratos · Hórus (`renovacao-contratos-horus`)

**Retrato.** Layout lateral, perfis Gestor, Fiscal e Administrador, menu com 5
itens.

**O que funciona.** Semáforo por faixa de vencimento. Checklist de instrução.
Aviso de contrato sem instrução a 60 dias.

**Problemas.**
- No celular **a página rola na horizontal**.
- Ficha com 3.191 px, 11 botões e 12 campos.
- O semáforo é uma tabela de faixas, sem visão de linha do tempo.
- "Semáforo (R3)", "Aviso de instrução (Sprint 3)", "Valor em risco e renovação
  (Sprint 6)".
- O Fiscal não tem "meus contratos".

**Plano.**
- Navegabilidade
  - P1 Ficha em abas: Resumo · Aditivos · Instrução · Fiscais · Auditoria.
  - P2 "Meus contratos" para o Fiscal.
- Layout
  - P1 Semáforo como barra empilhada clicável (vencido, 0-30, 31-60, 61-90,
    91-120, normal) e lista de contratos ordenada por dias restantes.
  - P1 Tabelas responsivas (A8).
- Usabilidade
  - P2 Contagem regressiva no topo da ficha com a próxima providência ("Faltam
    1 dia. Registrar aditivo").

**Pronto quando:** o gestor vê os contratos a vencer em 1 olhar e registra o
aditivo pela aba certa.

## 18. Não Conformidades (`rnc-nao-conformidade`)

**Retrato.** Layout lateral, perfis CQUAL e Setor, menu com 4 a 5 itens.

**O que funciona.** Painel com RNCs por setor, categoria e etapa. Recorrência
(RN05).

**Problemas.**
- O perfil Setor escolhe o setor **dentro** de "Minhas RNCs" (select + "Salvar
  setor") e a tela fica vazia até isso.
- Painel com 2.740 px de contagens em tabelas.
- "12 com etapa vencida" não leva às 12.
- "Arquivo do setor" não diz o que faz (é a exportação da cópia do setor).

**Plano.**
- Navegabilidade
  - P1 Setor como contexto do perfil (A1, item 6): "Perfil: Setor · LQF ▾".
  - P2 "Arquivo do setor" passa a "Enviar ao setor" com a explicação do
    caminho do arquivo.
- Layout
  - P2 Contagens em barras horizontais; KPIs clicáveis (A11).
- Usabilidade
  - P2 Ficha da RNC com os formulários FOR 2 e FOR 3 como passos.

**Pronto quando:** o setor abre o app direto nas próprias RNCs.

## 19. TAP Digital (`tap-portfolio-projetos`)

**Retrato.** Layout topo, perfis Demandante, Equipe e Autoridade, menu de 3 a 4
itens por perfil.

**O que funciona.** O melhor formulário entre os 20: TAP em 5 abas numeradas,
rascunho salvo a cada campo, botão "Próxima".

**Problemas.**
- A Equipe abre em "Novo TAP" (primeira rota permitida), e não na Triagem.
- "Pendências antes do envio (12)" aparece completa desde o primeiro campo, com
  códigos RN, e assusta.
- As abas não mostram quais estão completas.

**Plano.**
- Navegabilidade
  - P1 Tela inicial por perfil (A1, item 5): Equipe → Triagem; Autoridade →
    Portfólio.
- Layout
  - P2 Cada aba com selo de completude (✓ ou "2 pendentes").
- Usabilidade
  - P2 Pendências mostradas por aba, junto do campo, e a lista completa só no
    passo de envio.
  - P3 Prioridade do portfólio por arrastar ou por botões ↑ ↓, com a
    justificativa pedida na hora.

**Pronto quando:** o demandante vê o que falta só na aba em que está e a equipe
abre na triagem.

## 20. TCIN · Trilha de Custódia e Identificação (`trilha-custodia-necropsia`)

**Retrato.** Layout lateral, **4 perfis** (Operador do CIOP, Técnico,
Plantonista, Gestor), menu com 5 itens.

**O que funciona.** Lista só com iniciais (RN05). Chips por situação com contagem.
Dias no IML com cor. Busca por protocolo, nome, documento ou lacre.

**Problemas.**
- Painel com 2.334 px, que repete os mesmos 12 corpos três vezes: na tabela de
  situação, na tabela "Permanência por corpo" e na lista do alerta de plantão.
- O Operador vê "Painel do gestor (Sprint 5)".
- Ficha com 2.497 px e 16 campos.
- Uso provável em tablet no IML, mas os botões têm a altura padrão de desktop.

**Plano.**
- Navegabilidade
  - P1 Painel por perfil: Operador (acionamentos em deslocamento), Técnico
    (corpos na sala), Plantonista (passagem de plantão), Gestor (tempos e
    permanência).
  - P2 Ficha em abas: Marcos · Identificação · Lacres · Liberação · Auditoria.
- Layout
  - P1 Uma tabela só no painel, com a coluna "sem movimentação há" e o alerta
    como filtro rápido ("10 sem movimentação há mais de 12 h").
  - P2 Modo tablet: botões de 44 px e ações do marco em botões grandes
    ("Chegada ao local", "Saída do local", "Retorno ao IML").
- Usabilidade
  - P2 Leitura do lacre para abrir a ficha (mesmo padrão da custódia).

**Pronto quando:** cada perfil vê só a lista de que precisa e o técnico registra
um marco com 1 toque.

---

# Parte C · Ordem de entrega

## Onda 0 · Base comum (1 entrega, chega aos 20 apps)

| Item | Arquivo | Efeito |
|---|---|---|
| A1 Seletor de perfil suspenso, perfil padrão, tela inicial e contexto por perfil | `base.html`, `visual.css`, `app.json` | Fim da tela de bloqueio em 16 apps |
| A2 Rota inicial pública | `base.html`, 3 `app.json` | Cidadão não vê mais a tela de perfil |
| A3 Contorno do `<main>` | `visual.css` | Some a borda amarela das 102 telas |
| A4 `pai` da rota e trilha | `base.html`, `app.json` | Menu marcado nas fichas |
| A7 Títulos sem "(Sprint N)" e RN em ícone | `src/*.js` dos 17 apps | 42 títulos limpos |
| A8 Cabeçalho "Exibição", menu compacto, tabela responsiva | `base.html`, `visual.css` | Celular legível; fim da rolagem horizontal |
| A10 Menu sem telas pendentes | `base.html` | Agiliza, Equipamentos e Inscrições sem becos |
| A12 `numBR` | `base.html` | Decimais com vírgula |

Verificação: `python Apps/_base/construir.py`, `python Apps/_base/testar.py` e
`python Apps/_base/testar_sprints.py` nos 20 apps. Acrescentar ao `testar.py`:
(1) abrir sem hash e conferir que não aparece "Escolha o perfil";
(2) trocar o perfil pelo menu suspenso numa tela permitida e numa não permitida;
(3) celular sem `scrollWidth > clientWidth`.

## Onda 1 · Componentes e fichas (os apps de ficha longa)

A5 (abas), A6 (`pode()`), A9 (lista), A11 (KPI com link), A13 (diálogo) e A14
na base. Em seguida, aplicar nas 6 fichas mais longas: aquisições, renovação de
contratos, TCIN, gestão de documentos, DNA e documentapolitec.

## Onda 2 · Planos individuais P1 e P2

Por app, na ordem: agendamento CIN e segunda via da CIN (públicos), Hórus e TCIN
(mais perfis), custódia e documentapolitec (leitura de lacre/prontuário),
comissão, passivo, RNC, TAP, adiantamento, metas BI. Inclui os seeds com todas
as etapas (A16).

## Onda 3 · Apps com sprints pendentes

Agiliza +, mapa de distribuição, inscrições e equipamentos recebem a estrutura de
navegação nova (passos do caso, do processo e do curso) **antes** das sprints
que faltam, para que as telas novas já nasçam no lugar certo.

## Placar por app (hoje)

| App | Perfis | Itens no menu | Tela mais longa (px) | Celular rola na horizontal | P1 do plano |
|---|---|---|---|---|---|
| adiantamento | 0 | 4 | 2.713 (config) | não | 3 |
| agendamento-cin | 2 | 3 | 1.838 | não | 4 |
| agiliza-mais | 0 | 10 | 924 | não | 3 |
| cin-segunda-via | 2 | 2 | 1.462 | não | 3 |
| comissao-etica-denuncias | 3 | 4 | 3.236 (config) | não | 2 |
| controle-aquisicoes | 3 | 5 | 4.332 (ficha) | não | 3 |
| custodia-definitiva | 3 | 5 | 2.687 | não | 2 |
| distribuicao-casos-dna | 3 | 5 | 2.580 | **sim** | 2 |
| documentapolitec | 2 | 8 | 2.129 (ficha) | não | 2 |
| equipamentos-google-earth | 3 | 9 | 10.371 | não | 3 |
| gestao-documentos | 3 | 4 | 2.481 (ficha) | não | 3 |
| horus-banco-demandas | 6 | 7 | 1.702 | não | 2 |
| inscricoes-cursos | 2 | 3 | 1.599 | não | 3 |
| mapa-distribuicao-credor | 0 | 2 | 1.129 | não | 2 |
| metas-bi-ocr | 0 | 3 | 991 | não | 3 |
| passivo-ambiental | 2 | 4 | 2.463 | não | 3 |
| renovacao-contratos-horus | 3 | 5 | 3.191 (ficha) | **sim** | 3 |
| rnc-nao-conformidade | 2 | 4 | 2.740 | não | 1 |
| tap-portfolio-projetos | 3 | 3 | 1.600 | não | 1 |
| trilha-custodia-necropsia | 4 | 5 | 2.497 (ficha) | não | 2 |

---

# Parte D · Cada app com cara própria

## O problema

Os 20 apps nasceram da mesma base e hoje só se diferenciam pela cor do acento,
pelo emblema e pela textura do cabeçalho. A estrutura é a mesma em todos: faixa
do governo, cabeçalho em degradê azul, menu (lateral ou em abas), título com
filete, 4 a 9 KPIs em cartões iguais e tabelas. Quem abre dois apps seguidos não
sabe em qual está. Além disso, a forma da tela não ajuda o trabalho de cada
setor: o balcão da custódia, a placa do DNA e o calendário do agendamento usam a
mesma lista de cartões.

## A regra

1. **Fica comum** só o que identifica o governo: faixa de MT, SESP e POLITEC,
   rodapé institucional, foco do teclado, tema claro como padrão, A− / A+,
   backup e testes.
2. **Muda por app** a forma da tela: casca (como o menu se organiza), cabeçalho,
   tipografia, densidade, cantos, superfície dos cartões, estilo dos KPIs e,
   principalmente, a **tela-assinatura**: a tela inicial desenhada para o
   trabalho daquele setor.
3. A tela-assinatura nasce da tarefa principal do app (o que a pessoa faz 20
   vezes por dia), e não do dado que existe no banco.

## Novas opções do bloco `visual` (base)

| Campo | Valores | Efeito |
|---|---|---|
| `casca` | `lateral`, `topo`, `trilho`, `cidadao`, `ferramenta` | `trilho`: coluna estreita de ícones com rótulo embaixo; `cidadao`: coluna única centralizada, sem menu interno; `ferramenta`: largura total, menu compacto, para telas de trabalho (mapa, planilha, quadro). |
| `cabecalho` | `degrade`, `solido`, `claro`, `compacto` | Degradê institucional, cor sólida do acento, branco, ou barra fina de 52 px. |
| `fonte` | `sistema`, `serifa`, `condensada`, `mono`, `arredondada` | Fontes do sistema (sem rede): Segoe UI; Georgia/Cambria; Bahnschrift; Consolas nos números; Trebuchet/Segoe UI arredondada. |
| `densidade` | `compacta`, `normal`, `ampla` | Espaçamento de tabelas, cartões e botões (ampla = toque, 44 px). |
| `cantos` | `retos`, `suaves`, `redondos` | Raio de 3, 10 ou 18 px. |
| `superficie` | `cartoes`, `planas`, `papel` | Sombra; só borda; fundo creme de documento. |
| `kpi` | `barra`, `numero`, `faixa`, `anel` | Barra lateral (hoje); número grande sem caixa; faixa colorida no topo; anel de progresso. |

## A identidade de cada app

| App | Casca | Cabeçalho | Fonte | Densidade | Cantos | Superfície | KPI | Tela-assinatura |
|---|---|---|---|---|---|---|---|---|
| adiantamento | lateral | sólido | mono | compacta | retos | planas | número | **Régua de prazos**: cada processo numa linha com a barra do prazo da etapa e da prestação de contas |
| agendamento-cin | cidadão | claro | arredondada | ampla | redondos | cartões | — | **Calendário do mês** com vagas por dia e horários em botões grandes |
| agiliza-mais | ferramenta | compacto | condensada | compacta | suaves | planas | faixa | **Bancada do caso**: passos do laudo à esquerda e área de trabalho à direita |
| cin-segunda-via | cidadão (público) / topo (interno) | claro | arredondada | normal | redondos | cartões | número | **Caixa de entrada**: lista de pedidos à esquerda, pedido aberto à direita, Aceitar e próximo |
| comissao-etica-denuncias | lateral | sólido | serifa | ampla | retos | papel | faixa | **Funil do processo ético** e dossiê com a marca "Reservado" |
| controle-aquisicoes | ferramenta | degradê | condensada | compacta | suaves | planas | faixa | **Quadro (kanban) das 9 etapas** da Lei 14.133 com os processos em cartões |
| custodia-definitiva | trilho | sólido | condensada | normal | retos | planas | número | **Balcão de leitura do lacre** e o mapa das prateleiras com a ocupação de cada contêiner |
| distribuicao-casos-dna | topo | degradê | sistema | normal | redondos | cartões | anel | **Placa de 96 poços** com a cor do perito em cada caso |
| documentapolitec | lateral | sólido | serifa | normal | retos | papel | barra | **Estante de caixas** (lombadas) e conferência por leitura sequencial |
| equipamentos-google-earth | ferramenta | compacto | sistema | compacta | suaves | planas | número | **Mapa de MT** (SVG dos 142 municípios embutidos) com as unidades e os equipamentos parados |
| gestao-documentos | lateral | sólido | serifa | normal | suaves | papel | barra | **Caixa por perfil** (a instruir, a revisar, a assinar) com o prazo em barra |
| horus-banco-demandas | lateral | degradê | sistema | normal | redondos | cartões | número | **Vitrine** de demandas com filtros em facetas e ordenação |
| inscricoes-cursos | topo | degradê | arredondada | ampla | redondos | cartões | faixa | **Cartões de curso** com a esteira Divulgar → Turma |
| mapa-distribuicao-credor | ferramenta | compacto | mono | compacta | retos | planas | número | **Esteira do processo** em 8 etapas e a grade de itens no formato planilha |
| metas-bi-ocr | topo | claro | sistema | ampla | suaves | cartões | anel | **Ano em 12 meses**: cada mês com a situação (importado, conferido, gerado) |
| passivo-ambiental | topo | degradê | sistema | normal | suaves | cartões | faixa | **Fila de laudos** com prazo e o mapa do dano em miniatura |
| renovacao-contratos-horus | lateral | sólido | condensada | compacta | retos | planas | número | **Régua de vencimentos** de 0 a 180 dias com cada contrato como ponto |
| rnc-nao-conformidade | lateral | sólido | sistema | normal | suaves | cartões | faixa | **Quadro por etapa do ciclo** (registro, plano, execução, avaliação, encerramento) |
| tap-portfolio-projetos | topo | degradê | serifa | ampla | redondos | cartões | anel | **Matriz do portfólio** (valor × prioridade) e o TAP como formulário em abas |
| trilha-custodia-necropsia | trilho | sólido | condensada | ampla | suaves | planas | número | **Quadro de plantão**: colunas por situação, cartões de corpo com dias no IML e botões grandes |

## Entrega app por app

Cada app é entregue em um commit, nesta ordem de trabalho:

1. bloco `visual` novo no `app.json` e `src/app.css` com os detalhes próprios;
2. tela-assinatura (`src/identidade.js`, carregado depois dos sprints, que
   redefine a tela inicial e as telas indicadas no plano da Parte B);
3. os itens P1 da Parte B;
4. `construir.py`, `testar.py` e `testar_sprints.py` do app passando;
5. captura de tela conferida (desktop e celular).
