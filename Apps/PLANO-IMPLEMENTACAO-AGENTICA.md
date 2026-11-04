# Plano de implementação agêntica · o que falta nos apps

Atualizado em **03/11/2026**. Este é o runbook para uma IA agêntica continuar o
trabalho nos 21 apps de `D:\Dev\Aula Politec\Apps` com o mínimo de intervenção
humana. Leia inteiro antes de mexer em qualquer app.

> **Fora do escopo:** `agendamento-cin` (Elthon) e `horus-banco-demandas`
> (Iohan) estão pausados por decisão do professor. Não altere esses dois apps.

---

## 0. Estado de partida

| Indicador | Valor |
|---|---|
| Apps ativos | 21 |
| Telas no painel | 160/160, 0 pendentes (`painel.py`) |
| Estrutura | `testar.py` 21/21 |
| Cenários | 133 documentados (130 anteriores + 3 desta rodada) |
| Feedback de código fechado | TEIA, Controle de Aquisições, Adiantamento, Gestão de Documentos, CIN, RNC, Agiliza, Custódia, Passivo, Renovação, Metas, TAP, Comissão, Inscrições, Mapa e Gestão de Identificados |
| Feedback ainda aberto | só o teste manual de Equipamentos no Google Earth |
| Sem resposta de feedback | Documentapolitec, Trilha de Custódia e Gestão de Identificados |
| Pausados | Agendamento CIN e Hórus |

**Importante:** “0 telas pendentes” não significa produto pronto. O que falta é
refinamento de feedback, decisões do setor, integrações externas e aceite/piloto.

---

## 1. Contrato de trabalho do agente

### 1.1 Regras de ouro

1. **Nunca edite `index.html`.** Edite `app.json`, `src/*.js`, `src/app.css`,
   `nucleo/*`, `exemplos/*`, `modelos/*` e rode `python construir.py`.
2. **Um app por vez.** Não misture mudanças de dois apps no mesmo commit.
3. **Cada app é autônomo.** Não importe código de outro app; bibliotecas ficam
   em `<app>/vendor/`.
4. **Offline first.** O app não pode fazer requisição de rede em tempo de
   execução. Integrações externas viram fila local/instrução em
   `AJUDA_TECNICA`.
5. **Dados fictícios.** Nada de PII real. Sementes fixas em
   `exemplos/seed.json`/`gerar_exemplos.py`.
6. **Testes são portão.** Nenhum item é “feito” se `testar.py` ou `cenarios.py`
   falharem. Rode também os testes globais do app.
7. **Documente.** Atualize `sprint.md` (marcações), `PREMISSAS.md` (o que foi
   assumido), `README.md`/`PROJETO.md` (quando mudar escopo) e o painel/hub.
8. **Não commite sem autorização.** O padrão é deixar na árvore de trabalho e
   reportar o diff. Se o operador autorizar, um commit por app.
9. **Não toque** nos apps pausados, nos `.xlsx`/`.pbix` da `Aula 4/`, nem em
   arquivos globais enquanto outro agente estiver rodando.
10. **Parada segura.** Se um item depender de decisão externa, registre em
    `PREMISSAS.md` com nível de confiança e siga; se depender de serviço
    externo, implemente a parte local e o passo a passo em `AJUDA_TECNICA`.

### 1.2 Arquivos compartilhados (serializar)

Estes arquivos são globais. Só o **agente integrador** deve editá-los, ao fim de
cada onda:

- `Apps/PREMISSAS.md`
- `Apps/CONTINUAR.md`
- `Apps/ANALISE-GLOBAL-PENDENCIAS.md`
- `Apps/README.md`
- `Apps/painel.html` (gerado por `python Apps/_base/painel.py`)
- `Apps/index.html` (hub, gerado por `hub_apps.py`)
- `Apps/LINKS-ALUNOS.md` (gerado por `gerar_links_alunos.py`)
- hubs `processo.html` (gerado por `gerar_hubs.py`)
- diagramas (gerados por `gerar_diagramas.py`)

Os demais arquivos (`<app>/app.json`, `<app>/src/*`, `<app>/testes/*`,
`<app>/index.html`) são exclusivos do agente daquele app.

### 1.3 Definição de pronto (por item)

- [ ] O item do `sprint.md` está `[x]` **ou** foi movido para `PREMISSAS.md`/
      `AJUDA_TECNICA` com justificativa.
- [ ] `python construir.py` gera o `index.html` sem erro.
- [ ] `python testes/testar.py` passa (zero rede, `#/testes` 100%, rotas, tema).
- [ ] `python testes/cenarios.py` passa; **novo cenário** cobre o item.
- [ ] `python Apps/_base/testar.py <app>` e `...testar_sprints.py <app>` passam.
- [ ] Desktop (1366 px) e celular (390 px) sem rolagem horizontal, sem erro no
      console, sem requisição de rede.
- [ ] `sprint.md`, `README.md`/`PROJETO.md` e `PREMISSAS.md` atualizados.
- [ ] Se criou rota/store: `app.json` atualizado, `painel.py`/`gerar_hubs.py`
      rodados pelo integrador.
- [ ] Diff revisado; sem segredo, sem dado real, sem `index.html` editado à mão.

---

## 2. Classificação do trabalho

| Tipo | O que é | Como a IA trata |
|---|---|---|
| **A · Código** | Tela, campo, regra, CSV, importação, gráfico, teste | Implementa e testa sozinha |
| **B · Decisão** | Lista oficial, prazo, permissão, critério, modelo | Implementa uma premissa plausível, registra em `PREMISSAS.md` e segue |
| **C · Serviço externo** | E-mail, Google Sheets, Apps Script, OCR, Google Earth, base biométrica, Atena | Implementa a fila/arquivo local e o passo a passo em `AJUDA_TECNICA`; não tenta burlar acesso |
| **D · Aceite/piloto** | Homologação com a chefia, teste com caso real, piloto | Prepara roteiro/checklist/evidências; a execução é humana |
| **E · Operação** | GitHub Pages, logins, convites, publicação | Humano; a IA prepara o relatório e os comandos |

---

## 3. Ondas de execução

A ordem abaixo é por impacto e dependência. Cada onda termina com regressão
global e atualização do painel/hub.

### Onda 0 · Preparação (0,5 dia)

1. Ler este plano, `AGENTS.md` (3.8), `CONTINUAR.md`, `PREMISSAS.md` e o
   `sprint.md` do app alvo.
2. Rodar `python Apps/_base/testar.py` e `...testar_sprints.py` para confirmar a
   linha de base.
3. Criar/atualizar o **livro de estado** (seção 8) com `status = todo`.
4. Fotografar o estado atual: `git status`, `git diff --stat` e o painel.
5. Confirmar que os apps pausados não serão tocados.

### Onda 1 · Apps grandes (3 a 5 dias de agente)

| App | Foco | Paralelizável? |
|---|---|---|
| Agiliza Mais | Modelo Word, revisão, histórico, foto/cor, biblioteca | Sim, isolado |
| Custódia Definitiva | Endereço hierárquico, confirmação física, ocupação | Sim, isolado |
| Passivo Ambiental | Editor de mapas, 3 mapas, abas, `.docx` | Sim, isolado |

### Onda 2 · Apps médios (3 a 4 dias) · **concluída em 03/11/2026**

| App | Foco | Paralelizável? |
|---|---|---|
| Renovação de Contratos | Fiscais/gestores, aviso, edição, objeto, planilha | Sim |
| Metas BI | Filtro por gerência, Pendentes, aprovar/gerar | Sim |
| TAP | Objetivos, fluxo, 5 dias, e-mail, matriz | Sim |
| Comissão de Ética | Artigo, membros, oitivas, minutas, e-mail | Sim |

### Onda 3 · Fechamento (3 a 4 dias) · **concluída em 03/11/2026**

| App | Foco | Paralelizável? |
|---|---|---|
| Inscrições em Cursos | Perfis, instrutores, termo, Divulgar/Triagem | Sim |
| Mapa de Distribuição | PDF do pregoeiro, mapa SESP, dotação, empresa | Sim (parte bloqueada por gabarito) |
| Gestão de Identificados | Cruzamento CNPD ↔ corpos, confirmação humana | Sim |
| Equipamentos | Teste manual no Google Earth + aceite | Não (humano) |
| Documentapolitec / Trilha | Só Sprint 0/aceite | Não (humano) |

### Onda 4 · Integração global (1 a 2 dias)

- Regressão completa: `testar.py` e `testar_sprints.py`.
- `painel.py`, `gerar_hubs.py`, `hub_apps.py`, `gerar_links_alunos.py`,
  `gerar_diagramas.py`.
- Reconciliar `CONTINUAR.md`, `CONTINUAR-IDENTIDADE.md`, `ENTREGA-*`,
  `PREMISSAS.md` e `README.md`.
- Relatório final e, se autorizado, commits por app.

---

## 4. Cartões por app

Cada cartão é uma unidade de trabalho. O agente deve abrir o app, ler o
`FEEDBACK.md`/`sprint.md` e seguir os passos. Os itens marcados **H** dependem de
humano/serviço externo e não bloqueiam os demais.

### 4.1 Agiliza Mais (`agiliza-mais`)

**Objetivo:** fechar o feedback do laudo de celular e o histórico.

**Arquivos:** `src/app.js`, `src/sprint4.js`, `src/app.css`,
`modelos/modelo-laudo-celular.docx`, `modelos/MARCADORES.md`,
`exemplos/caso-ficticio-*`, `README.md`, `sprint.md`.

**Passos:**

1. Inserir marcadores no modelo timbrado (ou no `.dotx` de `CASO TESTE 2`) e
   validar a geração com o `docxtemplater` já embutido. **H:** modelo oficial.
2. Revisão simplificada: trocar o fluxo por “Revisei” + “Concluir”, mantendo a
   trilha de quem revisou.
3. Corrigir o histórico: reproduzir o caso “sem funcionamento” do Diego, abrir
   `#/historico` com um caso real e registrar o defeito/correção.
4. Foto do aparelho: upload com `reduzirImagem`, sugestão de cor e
   características; a sugestão é assistida, não automática.
5. Lista de tipos de dispositivo e IA local opcional; sem chamada de rede.
6. Textos/quesitos: permitir editar, marcar como opcional e reordenar.
7. Biblioteca e histórico: lista de modelos, busca e reuso.
8. Testar com `CASO TESTE 2`; atualizar o README da pasta.

**Aceite:** gera `.docx` com marcadores; histórico abre; foto/cor funciona;
testes passam; novo cenário cobre o fluxo.

**Depende de:** modelo Word oficial, textos da Gerência, caso real. **H**

### 4.2 Custódia Definitiva (`custodia-definitiva`)

**Objetivo:** endereço físico real e ocupação.

**Arquivos:** `src/sprint3.js`, `src/sprint4.js`, `src/app.css`, `app.json`,
`exemplos/gerar_exemplos.py`, `PREMISSAS.md`.

**Passos:**

1. Modelo de endereço: `{container, estante, prateleira, nivel, posicao}` +
   `endereco_sugerido` e `endereco_efetivo`.
2. Regras de compatibilidade por categoria/conservação; bloquear espaços
   incompatíveis e sugerir apenas endereços válidos.
3. Cadastro em etapas: identificação, procedência, conferência documental,
   integridade do lacre, embalagem, quantidade, dimensões e conservação.
4. Só mudar para “Armazenado” após confirmação física (responsável, data, hora,
   histórico).
5. Acervo: endereço completo, motivos de pendência e destaque do que está sem
   endereço.
6. Painel: entradas/saídas, ocupação/capacidade por contêiner/prateleira,
   saturação, projeções e unidade de medida.
7. Alertas clicáveis abrem o contêiner/vestígio.
8. Corrigir o seed que mistura sala/armário/prateleira.

**Aceite:** cadastro hierárquico, confirmação, ocupação e alertas funcionam;
testes passam.

**Depende de:** estrutura física, capacidades e unidade de medida. **H**

### 4.3 Passivo Ambiental (`passivo-ambiental`)

**Objetivo:** laudo completo com mapas e `.docx`.

**Arquivos:** `src/app.js`, `src/sprint3.js`, `src/sprint4.js`, `src/app.css`,
`modelos/`, `sprint.md`.

**Passos:**

1. Cabeçalho do laudo: nº da requisição, autoridade, natureza, data de
   elaboração, hora de início/fim.
2. Corrigir o editor de mapas (não abriu no teste).
3. Três mapas obrigatórios: localização, antes e depois; aceitar PDF.
4. Abas Metodologia, Considerações, Valoração do Dano e Quesitos.
5. Exportar `.docx` além do PDF; melhorar o cabeçalho.
6. Setor editável (hoje fixo em “Diretoria de Interiorização”).

**Aceite:** laudo com 3 mapas, abas, `.docx` e cabeçalho; testes passam.

**Depende de:** texto padrão da metodologia, critérios de valoração, modelo
oficial e mapas. **H**

### 4.4 Renovação de Contratos (`renovacao-contratos-horus`)

**Objetivo:** fiscais/gestores, aviso e edição.

**Arquivos:** `src/app.js`, `src/sprint3.js`, `src/sprint4.js`, `app.json`
(store `fiscais` se necessário), `modelos/`, `sprint.md`.

**Passos:**

1. Cadastro de fiscais/gestores por contrato (nome, e-mail, telefone,
   vigência).
2. Botão de aviso no painel/semáforo para laranja/vermelho; fila local de
   e-mails com texto e destinatário.
3. “Meus contratos” sem digitar o nome do fiscal (usar o perfil/contexto).
4. Edição de contrato pelo ADM/gestor.
5. Campo objeto do contrato na Instrução, com busca/filtro.
6. Importar a planilha de controle do setor (Excel/CSV) com prévia.
7. `AJUDA_TECNICA`: passo a passo de MailApp/Apps Script e confirmação de
   leitura.

**Aceite:** fiscais por contrato, aviso em fila, edição, objeto e importação;
testes passam.

**Depende de:** dados dos fiscais, planilha, faixas/antecedência, canal de
e-mail. **H/C**

### 4.5 Metas BI (`metas-bi-ocr`)

**Objetivo:** gerência, Pendentes e aprovação.

**Arquivos:** `src/app.js`, `src/sprint3.js`, `src/sprint4.js`, `app.json`,
`exemplos/gerar_exemplos.py`, `sprint.md`.

**Passos:**

1. Acrescentar `gerencia` às unidades (store `unidades` e seed) e exibir/filtrar
   no importador e na conferência.
2. Definir o cartão “Pendentes” como soma das unidades ativas (ou do campo
   próprio do PDF); extrair do PDF/CSV e mostrar separado.
3. Revisar “Aprovar o mês”: explicar o bloqueio RN02 (soma ≠ total), oferecer
   “Aceitar a soma” e, depois, liberar a aprovação e a geração.
4. Não misturar unidades fictícias com não monitoradas: marcar `desconhecida`,
   exigir associação e manter fora do total até associar.
5. Testar com o mês real da Karine. **H**

**Aceite:** filtro por gerência, Pendentes, aprovação/geração e unidades
desconhecidas; testes passam.

**Depende de:** lista/grafia das gerências, definição de Pendentes, regra de
aprovação e mês real. **H**

### 4.6 TAP (`tap-portfolio-projetos`)

**Objetivo:** objetivos reais, fluxo e prazo.

**Arquivos:** `src/app.js`, `src/sprint3.js`, `src/sprint4.js`, `src/app.css`,
`app.json`, `sprint.md`.

**Passos:**

1. Lista de objetivos estratégicos: usar a lista oficial (quando chegar) ou
   tornar configurável em `#/config`; registrar a premissa.
2. Fluxo: ao sanar a pendência, voltar a “em análise” e permitir “Enviar à
   autoridade”; a autoridade aprova/rejeita e o histórico registra.
3. Prazo de 5 dias: campo no TAP/pendência, contagem e destaque.
4. Avisos por e-mail: fila local (equipe no vencimento, demandante na pendência,
   autoridade na aprovação) + `AJUDA_TECNICA`.
5. Matriz: escala numérica nos eixos e deslocamento dos pontos sobrepostos.

**Aceite:** fluxo pendência → análise → autoridade, 5 dias, fila de avisos e
matriz legível; testes passam.

**Depende de:** lista oficial, textos/canal de e-mail, teste com a Danielle.
**H/C**

### 4.7 Comissão de Ética (`comissao-etica-denuncias`)

**Objetivo:** fechar o fluxo de classificação, oitivas e minutas.

**Arquivos:** `src/sprint3.js`, `src/sprint4.js`, `modelos/`, `sprint.md`.

**Passos:**

1. Classificação: mostrar o texto do artigo (já existe) e um texto padrão de
   confirmação do descumprimento.
2. Admissibilidade: lista suspensa de membros e fundamento padrão com data do
   relato, data da reunião e artigo.
3. Oitivas: apagar uma oitiva e encerrar as oitivas.
4. Minutas: “admissão” (não “admitida”), enquadramento na fundamentação,
   indicação no relatório e encerramento conforme modelo.
5. Envio por e-mail: fila local + instrução.

**Aceite:** classificação, membros, oitivas, minutas e fila; testes passam.

**Depende de:** modelos oficiais, lista de membros e canal de e-mail. **H/C**

### 4.8 Inscrições em Cursos (`inscricoes-cursos`)

**Objetivo:** perfis, instrutores e termo.

**Arquivos:** `app.json` (perfis), `src/app.js`, `src/sprint3.js`,
`src/sprint4.js`, `modelos/`, `sprint.md`.

**Passos:**

1. Perfis: diretoria, coordenação, gerência e chefe; definir o que cada um vê e
   faz; aplicar `perfis` nas rotas.
2. Instrutores e monitores no curso.
3. Termo de convocação: nome, data, carga horária, convocação e compensação
   (ambas com datas).
4. Revisar a tela Divulgar (feedback sem detalhe).
5. Investigar a Triagem (feedback marcou erro sem detalhe; pedir o caso à
   Edilaura). **H**
6. Testar no Outlook desktop/Web e no celular. **H**

**Aceite:** perfis, instrutores, termo e Divulgar/Triagem; testes passam.

**Depende de:** diretorias/siglas, decisão do CPF, TI da caixa, modelo do termo.
**H**

### 4.9 Mapa de Distribuição (`mapa-distribuicao-credor`)

**Objetivo:** PDF do pregoeiro e mapa orçamentário.

**Arquivos:** `src/sprint4.js`, `src/app.js`, `exemplos/`,
`modelos/`, `sprint.md`.

**Passos:**

1. Importar o relatório do pregoeiro em PDF (além de `.xlsx`/`.csv`); avisar
   quando for imagem. Usar pdf.js já embutido.
2. Novo mapa orçamentário no modelo da SESP (exportação), com os dígitos da
   dotação, situação do processo e empresa ganhadora por grupo.
3. Alinhamento do mapa/grade e conferência com o `mapa-manual-referencia.xlsx`.
4. Testes contra o gabarito (depende do Sprint 0). **H**
5. Exportar e publicar; aceite/piloto. **H**

**Aceite:** PDF importado, mapa SESP e conferência; testes passam.

**Depende de:** `WorkFlow.docx`, 4 pontos `[validar]`, relatório do pregoeiro,
gabarito e regras de dotação/empate. **H**

### 4.10 Gestão de Identificados (`gestao_identificados`)

**Objetivo:** cruzar o CNPD com os corpos não identificados, com revisão humana.

**Arquivos:** `src/desaparecidos.js` (ou novo `src/correspondencias.js`),
`app.json`, `src/app.css`, `docs/CONTRATO-DESAPARECIDOS.md`, `sprint.md`,
`testes/cenarios.py`.

**Passos:**

1. Criar a tela/rota `#/correspondencias` (restrita a `nihde` e `gestor`) ou
   uma seção dentro de `#/desaparecidos`.
2. Para cada corpo não identificado, gerar até 10 candidatos do CNPD/NamUs:
   sexo (30), idade ±5 (25) / ±10 (15), mesma UF (15) / mesmo município (25),
   janela de datas (20) e características quando existirem (10).
3. Mostrar o motivo de cada ponto e o total; não mostrar candidato sem fonte.
4. Confirmação humana: “confirmar”, “descartar” ou “pedir exame”, com
   justificativa; gravar em store `correspondencias` (nova, com
   `db.versao++`) e no `log` do corpo.
5. Aviso de que é indício, não identificação; nada automático.
6. Link do painel/hub para a tela.

**Aceite:** candidatos com motivo, confirmação/descarte e log; testes passam.

**Depende de:** validação da Kesia/NIHDE, integração com Atena e termos de uso.
**H**

### 4.11 Equipamentos no Google Earth (`equipamentos-google-earth`)

**Objetivo:** fechar o teste manual e o aceite.

**Passos:**

1. Gerar um checklist de teste (abrir `.kmz` no Pro e no Web, conferir foto no
   balão, camadas, zoom, filtros).
2. Validar o KML programaticamente (já há teste OGC 2.2).
3. Preparar o roteiro de aceite/piloto e as evidências.
4. **H:** abrir no Google Earth; nenhum ajuste de código pedido.

### 4.12 Documentapolitec (`documentapolitec`) e Trilha (`trilha-custodia-necropsia`)

**Objetivo:** preparar o Sprint 0 e o aceite; não há feedback de aluno.

**Passos:**

1. Documentapolitec: consolidar o formato do prontuário, o modelo das caixas, a
   planilha de 850 e a amostra do PDF; atualizar `PREMISSAS.md`.
2. Trilha: confirmar nome (CNC/TCIN), marcos/livros, linha de base e regras de
   recebimento/sepultamento com o IML.
3. Preparar roteiro de aceite.
4. **H:** documentos, medições e aceite.

### 4.13 Pausados

- `agendamento-cin`: não alterar. Quando retomar, o único passo externo é
  publicar o Apps Script e ligar `LockService`/`MailApp`.
- `horus-banco-demandas`: não alterar. Quando retomar, seguir o `sprint.md` e o
  contexto de unidade.

---

## 5. Trabalho global (integrador)

1. **Regressão:** `python Apps/_base/testar.py` e `...testar_sprints.py`.
2. **Painel/hubs:** `painel.py`, `gerar_hubs.py`, `hub_apps.py`,
   `gerar_links_alunos.py`, `gerar_diagramas.py`.
3. **Documentação:** reconciliar `CONTINUAR-IDENTIDADE.md` (ainda fala em 92/92),
   `ENTREGA-03-11-2026.md` (fala em rotas pendentes já resolvidas),
   `PREMISSAS.md`, `README.md` e `ANALISE-GLOBAL-PENDENCIAS.md`.
4. **GitHub Pages/logins:** 2 logins 404, 5 sem login, convites pendentes
   (Nelson/Helen no TEIA, Kesia no NIHDE). **H/E**
5. **Feedback:** 18 respostas em 16 apps; Agendamento aguardando; os demais sem
   resposta. Recolher mais respostas antes de fechar a próxima onda. **H**
6. **Publicação:** commit por app e push, quando autorizado; não incluir os
   `.xlsx`/`.pbix` da `Aula 4/`.

---

## 6. O que não é automatizável

| Item | Por que | Quem resolve |
|---|---|---|
| Sprint 0 (documentos, medições, decisões) | Depende do setor | Aluno/chefia; a IA registra premissa |
| Aceite e piloto | Depende da chefia e do uso real | Aluno/chefia |
| E-mail institucional | Conta, política e consentimento | TI/chefia; a IA deixa fila + instrução |
| Google Sheets | Planilha real e permissão | Setor; a IA valida o link |
| OCR real | Tamanho/Tesseract e amostra | Decisão técnica + PDF real |
| Google Earth | Teste visual humano | Coordenadora |
| Base biométrica | API, convênio e LGPD | TI/empresa |
| Atena/SINALID/CADÊ/SINESP/RIBPG/SINAB | Credencial/termo | Direção/órgão |
| Logins/convites/Pages | Contas e aceite | Alunos/professor |
| Termos de uso e LGPD | Decisão institucional | Direção/encarregado |

A IA **pode** preparar: minuta de termo, checklist, roteiro de aceite, fila
local, mensagem de erro, `AJUDA_TECNICA`, dados fictícios e testes.

---

## 7. Protocolo de execução do agente (loop)

Para cada app:

1. **Ler:** `Apps/<app>/sprint.md`, `FEEDBACK.md`, `contexto.md`,
   `PREMISSAS.md` (seção do app), `app.json`, `src/`.
2. **Baseline:** rodar `python testes/testar.py` e `python testes/cenarios.py`.
3. **Escolher 1 item** do `sprint.md` (menor dependência primeiro).
4. **Implementar** na fonte (`src/`, `app.json`, `modelos/`), em diffs pequenos.
5. **Construir e testar** após cada item:
   `python construir.py` → `testes/testar.py` → `testes/cenarios.py`.
6. **Acrescentar cenário** em `testes/cenarios.py` que usa a tela como uma
   pessoa usaria.
7. **Conferir** desktop 1366 e celular 390; console limpo; zero rede.
8. **Atualizar** `sprint.md` (`[x]`), `PREMISSAS.md` (premissa nova),
   `README`/`PROJETO` (se mudou escopo).
9. **Registrar** no livro de estado: item, status, teste, commit.
10. **Repetir** até o app fechar; então rodar os testes globais do app.
11. **Reportar** diff, evidências e pendências humanas.
12. **Commit:** só com autorização; mensagem `app: <resumo>`.

**Parada:** se um teste falhar duas vezes no mesmo item, pare, registre o erro,
o arquivo e a hipótese; não “conserte” escondendo o teste. Se faltar decisão,
assuma o valor plausível, registre em `PREMISSAS.md` (nível B/C) e siga.

---

## 8. Livro de estado (atualizar durante a execução)

Copie esta tabela para `Apps/PLANO-ESTADO.md` (ou mantenha no fim deste
arquivo) e atualize a cada item:

| App | Item | Tipo | Status | Teste | Commit |
|---|---|---|---|---|---|
| agiliza-mais | marcadores no modelo | B | blocked (modelo oficial) | — | — |
| agiliza-mais | revisão simplificada | A | done | s4 | — |
| agiliza-mais | histórico | A | done | s14 | — |
| agiliza-mais | foto/cor | A | done | s14 | — |
| custodia-definitiva | endereço hierárquico | A | done | s8 | — |
| custodia-definitiva | confirmação física | A | done | s8 | — |
| custodia-definitiva | ocupação/saturação | A | done | s8 | — |
| passivo-ambiental | mapa/3 mapas | A | done | s3/s8 | — |
| passivo-ambiental | abas/docx | A | done | s8 | — |
| renovacao-contratos-horus | fiscais/gestores | A | todo | — | — |
| renovacao-contratos-horus | aviso/edição/objeto | A | todo | — | — |
| metas-bi-ocr | gerência/Pendentes | A | todo | — | — |
| metas-bi-ocr | aprovar/gerar | A | todo | — | — |
| tap-portfolio-projetos | objetivos/fluxo/5 dias | A | todo | — | — |
| tap-portfolio-projetos | matriz | A/P2 | todo | — | — |
| comissao-etica-denuncias | artigo/membros/oitivas/minutas | A | todo | — | — |
| inscricoes-cursos | perfis/instrutores/termo | A | todo | — | — |
| inscricoes-cursos | Outlook/celular | D | todo | — | — |
| mapa-distribuicao-credor | PDF/mapa SESP | A | todo | — | — |
| mapa-distribuicao-credor | gabarito | D | bloqueado | — | — |
| gestao_identificados | correspondência | A | todo | — | — |
| equipamentos-google-earth | teste Google Earth | D | todo | — | — |
| documentapolitec | Sprint 0/aceite | D | todo | — | — |
| trilha-custodia-necropsia | Sprint 0/aceite | D | todo | — | — |

Status: `todo`, `doing`, `blocked`, `done`.

---

## 9. Prompts prontos

### 9.1 Prompt de app (copiar e executar)

```text
Trabalhe APENAS em Apps/<app>. Leia Apps/<app>/sprint.md, FEEDBACK.md,
contexto.md e a seção do app em Apps/PREMISSAS.md. Rode
`python testes/testar.py` e `python testes/cenarios.py` antes de começar.
Implemente um item por vez do Sprint <N> aberto, na fonte (src/, app.json,
modelos/), nunca no index.html. Depois de cada item rode
`python construir.py`, `python testes/testar.py` e `python testes/cenarios.py`;
acrescente um cenário que use a tela como uma pessoa usaria. Confira desktop
1366 e celular 390, console limpo e zero requisição de rede. Atualize
sprint.md ([x]) e PREMISSAS.md se assumir algo. Não toque em
agendamento-cin nem horus-banco-demandas. Não commite sem autorização.
Ao terminar, reporte: itens fechados, testes, diff e pendências humanas.
```

### 9.2 Prompt do integrador (fim de onda)

```text
Rode a regressão completa (testar.py e testar_sprints.py), atualize
painel.py, gerar_hubs.py, hub_apps.py, gerar_links_alunos.py e
gerar_diagramas.py. Reconcilie CONTINUAR-IDENTIDADE.md, ENTREGA-03-11-2026.md,
PREMISSAS.md e ANALISE-GLOBAL-PENDENCIAS.md com o estado real. Não altere
código de app nesta etapa. Reporte o que passou, o que falhou e o que ficou
bloqueado por pessoa/serviço externo.
```

### 9.3 Prompt de dependências humanas

```text
Liste, por app, o que depende de pessoa/serviço externo (Sprint 0, aceite,
e-mail, Google Sheets, OCR, Google Earth, base biométrica, Atena, Pages,
logins). Para cada item, escreva o que pedir, a quem, o texto pronto e o
impacto de não ter. Não tente acessar sistemas restritos.
```

---

## 10. Estimativa e paralelismo

| Onda | Esforço de agente | Com 3 agentes |
|---|---|---|
| 0 · preparação | 0,5 dia | 0,5 dia |
| 1 · Agiliza/Custódia/Passivo | 4 a 6 dias | 2 dias |
| 2 · Renovação/Metas/TAP/Comissão | 3 a 4 dias | 1,5 dia |
| 3 · Inscrições/Mapa/Identificados/Equipamentos/Docs | 3 a 4 dias | 1,5 dia |
| 4 · integração/publicação | 1 a 2 dias | 1 dia |

**Paralelismo seguro:** um agente por app, desde que não editem os arquivos
globais da seção 1.2. O integrador é único.

---

## 11. Riscos e mitigação

| Risco | Mitigação |
|---|---|
| Dois agentes no mesmo `app.json`/`src` | Um app por agente; branch/pasta isolada; integrador único |
| `index.html` editado à mão | Regra de ouro + build no teste |
| Teste “verde” escondendo regressão | Cenário novo por item + `testar.py` global |
| Decisão do setor faltando | Premissa A/B/C em `PREMISSAS.md`; não bloquear |
| Serviço externo indisponível | Fila local + `AJUDA_TECNICA` + mensagem clara |
| Dados reais/PII | Só fichas fictícias; seed com semente fixa |
| App pausado alterado | Lista explícita de exclusão no topo |
| Documentação divergente | Integrador reconcilia no fim de cada onda |
| Commits misturados | Um commit por app, só com autorização |

---

## 12. Próxima ação imediata

1. Confirmar a linha de base: `python Apps/_base/testar.py` e
   `...testar_sprints.py` (21/21 e 133/133 nesta data).
2. Fechar o **teste manual do `.kmz` no Google Earth Pro/Web** (Equipamentos) e
   registrar em `modelos/roteiro-aceite.md`.
3. Regerar painel, hubs, links e diagramas e atualizar a documentação global.
4. Entregar ao professor sem commit até autorização expressa.

---

## 13. Referências

- `AGENTS.md` (seção 3.8) — contrato dos apps.
- `Apps/CONTINUAR.md` — histórico e backlog por app.
- `Apps/CONTINUAR-IDENTIDADE.md` — identidade e usabilidade.
- `Apps/ANALISE-GLOBAL-PENDENCIAS.md` — matriz do que falta.
- `Apps/PREMISSAS.md` — o que foi assumido e o que confirmar.
- `Apps/PLANO-USABILIDADE.md` — diagnóstico de layout/navegabilidade.
- `Apps/<app>/sprint.md` e `FEEDBACK.md` — a fonte de cada tarefa.
