# Continuar o desenvolvimento dos apps (passagem para outro agente)

Atualizado em **30/10/2026**. Este arquivo registra o que já foi feito nos 20 apps
de `Apps/` e o que falta em cada um, para que outro agente de IA continue de onde
paramos. Leia também `AGENTS.md` (seção 3.8), `Apps/README.md` e
`Apps/IDENTIDADE-VISUAL.md`.

## 1. Como o projeto funciona (o mínimo para começar)

- Cada app é **um único `index.html` gerado**, offline, com IndexedDB, backup
  `.json`, perfis, dados fictícios e a tela `#/testes`.
- **Nunca edite o `index.html`.** As fontes são:
  - comuns: `Apps/_base/base.html`, `visual.css`, `icones.js`, `js_comum.js`;
  - por app: `app.json` (título, `visual`, banco, perfis, rotas), `src/app.js`
    (Sprints 1 e 2), `src/sprint3.js`, `src/sprint4.js`... (um arquivo por sprint,
    juntados em ordem depois do `app.js`), `src/app.css` (opcional),
    `exemplos/seed.json` (gerado por `exemplos/gerar_exemplos.py`).
- Uma tela é `TELAS["#/rota"] = async params => "html"` e os eventos ficam em
  `TELAS_DEPOIS["#/rota"] = params => {...}`. Um sprint novo pode **redefinir**
  uma tela antiga no seu arquivo (ex.: `custodia-definitiva/src/sprint3.js`) ou
  **embrulhar** a tela anterior guardando a função original (ex.:
  `trilha-custodia-necropsia/src/sprint3.js`).
- Regras de negócio viram funções puras com `teste("nome", ()=>...)`; elas rodam
  em `#/testes` e no `testar.py`.
- Cada sprint tem um **cenário de interface** em
  `Apps/_base/cenarios/sprintN.py` (`@cenario("<app>")`), que usa a tela como uma
  pessoa e confere o "Pronto quando" do `sprint.md`.
- Store novo no banco: acrescente em `app.json → db.stores` **e suba
  `db.versao`** (senão o IndexedDB não cria o store).
- Ao concluir um sprint: marque `[x]` nos itens do `sprint.md`, acrescente a
  linha na tabela **Andamento**, atualize `sprint` e `descricao` das rotas no
  `app.json` e a tabela de andamento do `Apps/README.md`.

### Comandos

```powershell
python Apps/_base/construir.py [<app>]          # gera o index.html (todos ou um)
python Apps/_base/testar.py [<app>]             # estrutura: zero rede, #/testes 100%, rotas, tema
python Apps/_base/testar_sprints.py [<app>]     # cenários de cada sprint
python Apps/_base/painel.py; python Apps/_base/hub_apps.py   # painel e hub
node Apps/agendamento-cin/testes/testar_code_gs.js            # só o agendamento
```

No Git Bash, rotas como `#/corpo/C-0001` passadas como argumento viram caminho de
arquivo; use `MSYS_NO_PATHCONV=1` ou rode pelo PowerShell.

## 2. O que foi feito nesta etapa (30/10/2026)

### 2.1 Identidade visual SESP/MT e POLITEC/MT (todos os 20 apps)

- Nova base visual em `Apps/_base/visual.css` (separada do `base.html`): faixa do
  Governo de Mato Grosso, SESP e POLITEC; cabeçalho com degradê azul
  institucional, textura e filete acento/dourado/verde; emblema do app; menu com
  ícones; cartões, KPIs, tabelas, selos, formulários, rodapé institucional e
  cabeçalho de impressão.
- `Apps/_base/icones.js` com 48 ícones e a escolha automática do ícone de cada
  tela.
- Bloco `visual` em cada `app.json` (acento, emblema, layout `lateral`/`topo`,
  padrão do cabeçalho, estilo `institucional`/`claro`, setor). Detalhes e tabela
  dos 20 apps em `Apps/IDENTIDADE-VISUAL.md`.
- **Tema claro como padrão** em todos os apps; o escuro só entra pelo botão Tema.
- **Tamanho da fonte**: A−, 100% e A+ no cabeçalho (80% a 150%), guardado por app.
- **Faixa de aviso removida** de todos os apps (chave `aviso` tirada dos `app.json`).
- Componentes novos reutilizáveis: `.busca-grande`, `.duas-colunas`,
  `.linha-do-tempo`, `.etapas`, `.barra`, `.chips`, `.check-lista`,
  `.documento-a4`.

### 2.2 Sprint 3 em dois apps novos

- **custodia-definitiva**: acervo com busca por lacre, protocolo, categoria e
  contêiner (todas as palavras), filtros combinados (categoria, contêiner,
  situação, onde está, período), exportação CSV do filtro; ficha com
  movimentação (transferência com RN02/RN03, saída para perícia, retorno), linha
  do tempo e CSV do histórico. Cenário `s3_busca_csv_e_historico` (8/8).
- **trilha-custodia-necropsia**: transições de situação com regras e motivo,
  identificação com método, histórico da situação, painel e lista só com
  iniciais (RN05), filtros rápidos e dias no IML, busca por protocolo, nome,
  documento ou lacre (RN04). Cenário `s3_situacao_identificacao_e_busca` (11/11).

### 2.3 Verificação

`python Apps/_base/testar.py` passa nos 20 apps e `python Apps/_base/testar_sprints.py`
passa nos cenários de todos os sprints (ver o resultado no fim da seção 4).

## 3. Pendências gerais

1. **Sprint 3 dos 6 apps novos**: concluído em 30/10/2026. `passivo-ambiental`,
   `renovacao-contratos-horus`, `documentapolitec`, `gestao-documentos`,
   `controle-aquisicoes` e `distribuicao-casos-dna` têm o Sprint 3 feito.
2. **Manual de marca oficial**: as cores institucionais foram definidas por
   aproximação. Pedir o manual à ASCOM da SESP/POLITEC e trocar `--mt-*` em
   `visual.css`. Se houver brasão ou logotipo autorizado, entra no `.emblema` ou na
   `.faixa-gov` (hoje há só os quadrados da bandeira e o ícone do app).
3. **Dado fictício do TCIN**: corrigido em 30/10/2026. A lista `CASOS` de
   `trilha-custodia-necropsia/exemplos/gerar_exemplos.py` agora traz situação e
   nome juntos, e corpo "aguardando identificação" ou "não identificado" nasce
   sem nome e sem documento. O seed foi regerado e o `index.html` reconstruído;
   os testes do app e do Sprint 3 passam.
4. **KPI com texto longo** (ex.: nome da categoria na ficha do vestígio) fica com
   fonte grande; se incomodar, use um valor curto ou uma classe menor.
5. Telas antigas que ainda usam `<ol class="linha-tempo">` (adiantamento) podem
   migrar para `.linha-do-tempo`.
6. **Sprint 0**: os 77 itens que dependiam de decisão institucional, documento
   oficial ou medição do processo real foram **elucubrados** em 30/10/2026 e
   estão em [PREMISSAS.md](PREMISSAS.md), com o valor assumido, onde ele aparece
   no app e o que precisa ser confirmado. Nenhum item bloqueia o
   desenvolvimento. As referências que faltavam (modelos de DFD, ETP, TR, TAP,
   ata, laudo, caixa, marcos, plano de trabalho, esquema do Hórus) foram criadas
   nas pastas `modelos/` e `horus/` dos apps. **O que ainda depende de pessoas
   está na coluna "O que confirmar" de cada premissa**.
7. Publicação: esta etapa foi enviada ao GitHub em 30/10/2026 (identidade
   visual dos 20 apps, Sprint 3 da custódia definitiva e da TCIN, kit visual e
   este registro). Os arquivos da Aula 4 que já estavam modificados ficaram de
   fora do commit.

## 4. Estado e próximo passo de cada app

### Controle de Adiantamentos (`adiantamento`)

- **Visual**: acento `#0b6e4f`, emblema `moeda`, layout `lateral`, padrão `linhas`, cabeçalho `institucional`.
- **Sprints concluídos**: 1, 2, 3, 4, 5, 6, 7.
- **Situação**: MVP completo até o Sprint 7. O roteiro de aceite está em `modelos/roteiro-aceite.md`; o que falta depende de pessoas (ver `PREMISSAS.md`).
- **Sprint 0**: premissas assumidas em 30/10/2026. Cada item abaixo tem o valor
  adotado em [PREMISSAS.md](PREMISSAS.md), que é o que falta confirmar:
  - [ ] Validar as 12 etapas da tabela AS-IS com a DAS e com a contabilidade da SESP.
  - [ ] Confirmar qual Orientação Técnica da CGE/MT vale (02/2026 ou 06/2025).
  - [ ] Anexar os documentos citados (AS-IS e TO-BE em .docx, planilha de controle).
  - [ ] Acrescentar os feriados de MT e do município (Cuiabá) à lista.
  - [ ] Linha de base: anotar as datas dos pedidos de 4 semanas (proposta dos alunos).

### Agendamento CIN (`agendamento-cin`)

- **Visual**: acento `#1559b7`, emblema `calendario`, layout `topo`, padrão `ondas`, cabeçalho `claro`.
- **Sprints concluídos**: 2, 3.
- **Próximo**: Sprint 1 · Esqueleto (parcial: 4 item(ns) já feito(s))
  - [ ] Projeto do Apps Script ligado à planilha; `appsscript.json` com fuso `America/Cuiaba`.
  - [ ] Repositório com `clasp` configurado.
- **Sprint 0**: premissas assumidas em 30/10/2026. Cada item abaixo tem o valor
  adotado em [PREMISSAS.md](PREMISSAS.md), que é o que falta confirmar:
  - [ ] Pedir à TI a autorização para publicar um app da web do Apps Script com a conta institucional e confirmar as cotas de execução e de e-mail.
  - [ ] Aprovar com a gestão as regras completadas: RN06 (um agendamento ativo por posto), RN07 (cancelar até 2 h antes), RN08 (tolerância de 15 min), RN09 (de 1 a 30 dias de antecedência), RN10 (retenção de 90 dias).
  - [ ] Escolher os 1 ou 2 postos do piloto e levantar a grade real (dias, horários, vagas por horário).
  - [ ] Medir a linha de base no posto do piloto: tempo de uma marcação por telefone e agendamentos por dia.
  - [ ] Confirmar o nome completo do aluno no formulário.

### Agiliza + (`agiliza-mais`)

- **Visual**: acento `#4338ca`, emblema `raio`, layout `lateral`, padrão `grade`, cabeçalho `institucional`.
- **Sprints concluídos**: 1, 2, 3.
- **Próximo**: Sprint 4 · Geração do Word (RN12, RN13)
  - [ ] Embutir PizZip e docxtemplater.
  - [ ] Carregar o modelo em `#/config` e guardar como Blob no store `modelos`.
  - [ ] Listar os marcadores encontrados no modelo e acusar os que não têm dado.
  - [ ] Gerar o `.docx` com os dados do Sprint 3, com laço de SIMs e o bloco "sem SIM".
  - [ ] Gravar em `LAUDO_GERADO/laudo_<protocolo>_v<N>.docx`. Pedir permissão de escrita só nessa subpasta e nunca sobrescrever (incrementa `v<N>`).
  - [ ] Sem permissão de escrita: oferecer o download do arquivo.
  - [ ] Registrar em `laudos` (versão, data, nome).
- **Sprint 0**: premissas assumidas em 30/10/2026. Cada item abaixo tem o valor
  adotado em [PREMISSAS.md](PREMISSAS.md), que é o que falta confirmar:
  - [ ] Conferir com o perito o formato real dos TXT e HTML (amostra anonimizada) e anotar os rótulos exatos em `exemplos/FORMATOS.md`.
  - [ ] Copiar o modelo institucional para `modelos/modelo-laudo-celular.docx` e inserir os marcadores (`{numero_protocolo}`, `{imei_1}`, `{#sims}`...). Lista dos marcadores em `modelos/MARCADORES.md`.
  - [ ] Reunir os textos padronizados da Gerência em `exemplos/textos.json` (categoria, título, conteúdo), sem dados pessoais.
  - [ ] Criar a planilha da linha de base (protocolo, início, fim, correções) e começar a medir os laudos manuais: **2 semanas**, que correm em paralelo aos Sprints 1 e 2.

### Segunda via da CIN (`cin-segunda-via`)

- **Visual**: acento `#0e7490`, emblema `identidade`, layout `topo`, padrão `ondas`, cabeçalho `claro`.
- **Sprints concluídos**: 1, 2, 3, 4, 5, 6.
- **Situação**: MVP completo até o Sprint 6. O roteiro de aceite está em `modelos/roteiro-aceite.md`; o que falta depende de pessoas (ver `PREMISSAS.md`).
- **Sprint 0**: premissas assumidas em 30/10/2026. Cada item abaixo tem o valor
  adotado em [PREMISSAS.md](PREMISSAS.md), que é o que falta confirmar:
  - [ ] Confirmar as regras oficiais da segunda via (quando dispensa nova coleta).
  - [ ] Indicar a fonte dos números (15 dias, 21.000 por mês).
  - [ ] Fotos de teste geradas (sem pessoas reais).
  - [ ] Conversa com a TI e com a empresa da coleta biométrica sobre a integração (registrar a posição).

### Comissão de Ética (`comissao-etica-denuncias`)

- **Visual**: acento `#8a1c3a`, emblema `balanca`, layout `lateral`, padrão `pontos`, cabeçalho `institucional`.
- **Sprints concluídos**: 1, 2, 3, 4, 5, 6, 7.
- **Situação**: MVP completo até o Sprint 7. O roteiro de aceite está em `modelos/roteiro-aceite.md`; o que falta depende de pessoas (ver `PREMISSAS.md`).
- **Sprint 0**: premissas assumidas em 30/10/2026. Cada item abaixo tem o valor
  adotado em [PREMISSAS.md](PREMISSAS.md), que é o que falta confirmar:
  - [ ] Conferir com a Comissão as categorias e as palavras. **Os artigos da LC nº 112/2002-MT já estão na norma real**, com o texto em `modelos/codigo-etica-lc112-2002.md`.
  - [ ] Receber os modelos de ata de reunião, ata de oitiva e relatório de recomendações.
  - [ ] Linha de base: tempo das reuniões de triagem e da preparação das oitivas nos últimos casos.

### Controle do Processo de Aquisição (`controle-aquisicoes`)

- **Visual**: acento `#b23c17`, emblema `carrinho`, layout `lateral`, padrão `grade`, cabeçalho `institucional`.
- **Sprints concluídos**: 1, 2, 3.
- **Próximo**: Sprint 4 · Trilha de aprovação
  - [ ] Trilha de aprovação por setor, com perfil e data.
  - [ ] Análise técnica, orçamentária e jurídica.
  - [ ] Definição da modalidade registrada.
  - Feito no Sprint 3: pesquisa de preços com três cotações (RN04), alerta de inconsistência entre estimado e cotado (tolerância de 30%) e histórico de preços por objeto em `#/precos`.
- **Sprint 0**: premissas assumidas em 30/10/2026. Cada item abaixo tem o valor
  adotado em [PREMISSAS.md](PREMISSAS.md), que é o que falta confirmar:
  - [ ] Receber os modelos oficiais de DFD, ETP, TR e análise de riscos (a estrutura já segue a Lei nº 14.133/2021 em `modelos/MODELOS.md`).
  - [ ] Confirmar os prazos de cada etapa. **As 9 etapas e os documentos já estão ancorados na Lei nº 14.133/2021**, com 43 dias de ciclo em `modelos/fluxo-e-prazos.md`.
  - [ ] Validar as permissões e a base de processos de 2024/2025.

### Custódia Definitiva (`custodia-definitiva`)

- **Visual**: acento `#3f4a5a`, emblema `caixa`, layout `lateral`, padrão `hexagonos`, cabeçalho `institucional`.
- **Sprints concluídos**: 1, 2, 3.
- **Próximo**: Sprint 4 · Telas e regras
  - [ ] Projeção de ocupação a partir da série de 12 meses.
  - [ ] Tendência e alerta de saturação por contêiner.
  - [ ] Cenário de crescimento com entradas e saídas.
- **Sprint 0**: premissas assumidas em 30/10/2026. Cada item abaixo tem o valor
  adotado em [PREMISSAS.md](PREMISSAS.md), que é o que falta confirmar:
  - [ ] Conferir categorias, condições de conservação e capacidades com a equipe da custódia.
  - [ ] Receber a medição real de volume, tempo de recebimento e tempo de localização.

### Distribuição de Casos de DNA (`distribuicao-casos-dna`)

- **Visual**: acento `#86198f`, emblema `dna`, layout `topo`, padrão `hexagonos`, cabeçalho `institucional`.
- **Sprints concluídos**: 1, 2, 3.
- **Próximo**: Sprint 4 · Painel do coordenador
  - [ ] Painel do coordenador com tempo entre processamento e distribuição.
  - [ ] Comparação por rodada, perito e natureza de exame.
  - [ ] Meta de 1 dia e acompanhamento.
  - Feito no Sprint 3: sugestão do próximo perito pelo histórico de rotação, fila de urgência com justificativa (RN05) e alerta de rodada parada.
- **Sprint 0**: premissas assumidas em 30/10/2026. Cada item abaixo tem o valor
  adotado em [PREMISSAS.md](PREMISSAS.md), que é o que falta confirmar:
  - [ ] Confirmar a rotação e o número de peritos ativos com a coordenação.
  - [ ] Medir a linha de base do intervalo entre processamento e distribuição.
  - [ ] Validar o número de casos por rodada e as naturezas de exame.

### DOCUMENTAPOLITEC (`documentapolitec`)

- **Visual**: acento `#7c5a16`, emblema `pasta`, layout `lateral`, padrão `linhas`, cabeçalho `institucional`.
- **Sprints concluídos**: 1, 2, 3.
- **Próximo**: Sprint 4 · Busca autorizada
  - [ ] Busca por nome do cidadão, com índice autorizado e controle de acesso (RN03).
  - [ ] Resultado com caixa, setor e situação.
  - [ ] Trilha de consultas.
  - Feito no Sprint 3: importação da planilha de 850 prontuários com associação de colunas em `#/importar`, comparação com o índice do arquivo digital e relatório de aceitas, recusadas e divergentes em `#/relatorio-importacao`. Os arquivos de exemplo ficam em `exemplos/gerar_planilhas.py`.
- **Sprint 0**: premissas assumidas em 30/10/2026. Cada item abaixo tem o valor
  adotado em [PREMISSAS.md](PREMISSAS.md), que é o que falta confirmar:
  - [ ] Confirmar o formato do número do prontuário e o modelo das caixas.
  - [ ] Receber a planilha de teste com a relação de 850 prontuários.
  - [ ] Receber uma amostra do PDF digitalizado, sem dado pessoal.

### Mapa de Equipamentos (`equipamentos-google-earth`)

- **Visual**: acento `#2f7d32`, emblema `globo`, layout `topo`, padrão `topografico`, cabeçalho `institucional`.
- **Sprints concluídos**: 1, 2, 3.
- **Próximo**: Sprint 4 · Contratos e manutenções
  - [ ] `#/contratos`: cadastro com fornecedor, vigência, valor mensal, SLA e seleção dos equipamentos cobertos.
  - [ ] Cálculo de contrato vigente (RN05) e alerta de 60 dias para o vencimento.
  - [ ] Registro de manutenção (preventiva ou corretiva) na ficha, com custo, fornecedor e **comprovante** anexado (PDF ou imagem, até 2 MB).
  - [ ] Histórico em linha do tempo na ficha.
  - [ ] MTTR por equipamento (RN06).
- **Sprint 0**: premissas assumidas em 30/10/2026. Cada item abaixo tem o valor
  adotado em [PREMISSAS.md](PREMISSAS.md), que é o que falta confirmar:
  - [ ] Ler o `contexto.md` com a coordenadora e marcar cada **[validar]** como aceito, alterado ou recusado.
  - [ ] Preencher de novo no formulário (importando o `projeto.json`) as seções MVP, papéis, entidades, regras, telas e KPIs, com o escopo validado.
  - [ ] **Retirar o número de 11 dígitos** do campo "dados pessoais tratados".
  - [ ] Levantar a lista de diretorias e unidades da POLITEC com município de cada uma.
  - [ ] Reunir a planilha que existe hoje ("parcialmente", segundo o formulário) e anotar as colunas.
  - [ ] Definir com a coordenadoria o `valor_referencia_atendimento` e o custo alternativo padrão (terceirização, deslocamento para outra unidade).
  - [ ] Escolher 3 unidades para o piloto e medir a linha de base: quantos equipamentos estão sem contrato, quantas paradas houve no último trimestre e quanto tempo levou para responder "quanto custa essa parada?".

### Gestão de Documentos (`gestao-documentos`)

- **Visual**: acento `#2b5a8a`, emblema `carimbo`, layout `lateral`, padrão `linhas`, cabeçalho `institucional`.
- **Sprints concluídos**: 1, 2, 3.
- **Próximo**: Sprint 4 · Cobrança automática
  - [ ] Cobrança automática registrada no vencimento (RN08).
  - [ ] Opção de desligar a cobrança por lotação.
  - [ ] Histórico de cobranças.
  - Feito no Sprint 3: minutas padronizadas com os dados do processo (RN04), emissão de ofício e despacho e checklist de instrução por etapa.
- **Sprint 0**: premissas assumidas em 30/10/2026. Cada item abaixo tem o valor
  adotado em [PREMISSAS.md](PREMISSAS.md), que é o que falta confirmar:
  - [ ] Validar a matriz de papéis e quem pode excluir documentos.
  - [ ] Definir os anexos obrigatórios por tipo de processo (RN01).
  - [ ] Medir a linha de base (1 h/dia, 200 processos/mês, 48 h na triagem).

### Banco de Demandas (`horus-banco-demandas`)

- **Visual**: acento `#8f6b00`, emblema `olho`, layout `lateral`, padrão `pontos`, cabeçalho `institucional`.
- **Sprints concluídos**: 1, 2, 3.
- **Próximo**: Sprint 4 · Troca entre unidade e diretoria
  - [ ] Unidade: exportar `demandas-<unidade>.json` (com ou sem PDFs).
  - [ ] Diretoria: importar e mesclar por `id` e `updated_at`, com relatório de novos, atualizados e conflitos.
  - [ ] Diretoria: exportar `catalogo-<diretoria>.json` para as unidades.
  - [ ] Recusar arquivo de outra diretoria ou de outro órgão.
  - [ ] Revalidar R1 a R6 em toda importação.
- **Sprint 0**: premissas assumidas em 30/10/2026. Cada item abaixo tem o valor
  adotado em [PREMISSAS.md](PREMISSAS.md), que é o que falta confirmar:
  - [ ] Decidir com o aluno o papel da versão offline: (a) substituir o módulo, (b) servir às unidades sem acesso ao Hórus e entregar no formato dele, ou (c) ficar como exercício. Proposta: **(b)**.
  - [ ] Copiar do Hórus o esquema real das 3 tabelas (DDL do Supabase) para `horus/esquema.sql` e conferir com o `contexto.md`, seção 5.
  - [ ] Definir o formato `horus-import-ciclo.json` (versão do esquema, órgão, diretoria, ciclo, linhas das 3 tabelas) e o caminho de importação no Hórus (tela de importação ou SQL).
  - [ ] Decidir o relatório: `@media print` ou jsPDF embutido.
  - [ ] Juntar ao envio os anexos citados (relatório PDF e print da tela).

### Inscrições em Cursos (`inscricoes-cursos`)

- **Visual**: acento `#0369a1`, emblema `capelo`, layout `topo`, padrão `ondas`, cabeçalho `institucional`.
- **Sprints concluídos**: 1, 2.
- **Próximo**: Sprint 3 · Formulário de inscrição (parcial: 6 item(ns) já feito(s))
  - [ ] Testar no Outlook desktop, no Outlook Web e no celular.
- **Sprint 0**: premissas assumidas em 30/10/2026. Cada item abaixo tem o valor
  adotado em [PREMISSAS.md](PREMISSAS.md), que é o que falta confirmar:
  - [ ] Ler o `contexto.md` com a aluna e decidir cada **[validar]**.
  - [ ] Decidir com a chefia: **o CPF sai do formulário**? (proposta: sim, a matrícula basta).
  - [ ] Confirmar com a TI se a caixa `capacitacao@politec.mt.gov.br` aceita uma regra de resposta automática por assunto `[INSCRICAO]`.
  - [ ] Listar as diretorias que recebem vagas (nome e sigla).
  - [ ] Medir a linha de base em 2 cursos recentes: tempo da divulgação à lista final, espera pelas diretorias, erros corrigidos na planilha, vagas ociosas.
  - [ ] Corrigir no formulário (importando o `projeto.json`) as métricas, a hospedagem e a defesa que vieram de outro projeto.

### Mapa de Distribuição (`mapa-distribuicao-credor`)

- **Visual**: acento `#047857`, emblema `tabela`, layout `lateral`, padrão `grade`, cabeçalho `institucional`.
- **Sprints concluídos**: 1, 2, 3.
- **Próximo**: Sprint 4 · Resultado do pregoeiro (etapas 3, 4 e 5)
  - [ ] Aplicar a situação de cada grupo (RN02): homologado, fracassado, deserto, com a observação padrão.
  - [ ] Substituir o estimado pelo homologado (RN03), pela regra decidida no Sprint 0 (por item, ou desconto do grupo aplicado aos itens).
  - [ ] Grupos fracassados e desertos mantêm as colunas e recebem a observação.
  - [ ] `#/resultado/:proc`: resultado geral e por órgão, estimado x homologado e economia.
  - [ ] Teste contra o gabarito.
- **Sprint 0**: premissas assumidas em 30/10/2026. Cada item abaixo tem o valor
  adotado em [PREMISSAS.md](PREMISSAS.md), que é o que falta confirmar:
  - [ ] Anexar o `WorkFlow.docx` (exemplos 1 a 8) à pasta e conferir as colunas de cada exemplo com o `contexto.md`.
  - [ ] Decidir com a equipe e o orçamento os 4 pontos **[validar]** do `contexto.md`, seção 6 (homologado por grupo ou item, arredondamento, ordem da dotação, grupo misto), e escrever cada regra com um exemplo numérico.
  - [ ] Conseguir um relatório do pregoeiro de amostra (sem dado pessoal) e anotar o formato (colunas, cabeçalho, linhas de total).
  - [ ] Montar à mão, no Excel, o `mapa-manual-referencia.xlsx` (o gabarito).
  - [ ] Medir a linha de base em 3 a 6 processos encerrados: horas por etapa, divergências achadas e número de planilhas.

### Metas pelo BI (`metas-bi-ocr`)

- **Visual**: acento `#9d174d`, emblema `alvo`, layout `topo`, padrão `grade`, cabeçalho `institucional`.
- **Sprints concluídos**: 1, 2, 3.
- **Próximo**: Sprint 4 · Arquivo para a planilha (parcial: 2 item(ns) já feito(s))
  - [ ] Teste: o arquivo dos 3 meses fictícios importa na planilha sem ajuste.
- **Sprint 0**: premissas assumidas em 30/10/2026. Cada item abaixo tem o valor
  adotado em [PREMISSAS.md](PREMISSAS.md), que é o que falta confirmar:
  - [ ] Perguntar à TI se o Power BI 1 permite **Exportar dados** (CSV/Excel) no visual de pendências.
  - [ ] Conseguir uma amostra do PDF mensal com números fictícios (ou com os números tapados).
  - [ ] Copiar o cabeçalho da planilha do Google (colunas e uma linha de exemplo).
  - [ ] Listar as unidades e os nomes como aparecem no relatório.
  - [ ] Linha de base: cronometrar a atualização do mês atual.

### Passivo Ambiental (`passivo-ambiental`)

- **Visual**: acento `#4d7c0f`, emblema `folha`, layout `topo`, padrão `topografico`, cabeçalho `institucional`.
- **Sprints concluídos**: 1, 2, 3.
- **Próximo**: Sprint 4 · Conclusão do laudo
  - [ ] Conclusão do laudo com assinatura registrada.
  - [ ] Bloqueio de conclusão sem cabeçalho completo e sem mapa.
  - [ ] Atualização da situação da requisição.
  - Feito no Sprint 3: editor de mapa com modelos pré-definidos e elementos obrigatórios (RN02) em `#/mapa/:id`, anexo do mapa ao laudo e versão para impressão em `#/pdf/:id`, bloqueada sem cabeçalho completo e sem mapa (RN03).
- **Sprint 0**: premissas assumidas em 30/10/2026. Cada item abaixo tem o valor
  adotado em [PREMISSAS.md](PREMISSAS.md), que é o que falta confirmar:
  - [ ] Receber uma requisição real anonimizada e o modelo de laudo da unidade.
  - [ ] Confirmar o modelo de mapa (norte, escala, área) com o perito.
  - [ ] Cronometrar 5 laudos para confirmar a linha de base de 16 h.

### Renovação de Contratos · Hórus (`renovacao-contratos-horus`)

- **Visual**: acento `#3b4f7a`, emblema `contrato`, layout `lateral`, padrão `linhas`, cabeçalho `institucional`.
- **Sprints concluídos**: 1, 2, 3.
- **Próximo**: Sprint 4 · Reajuste e fluxo
  - [ ] Reajuste, repactuação e reequilíbrio com memória de cálculo.
  - [ ] Fluxo Solicitado → Em análise → Aprovado → Aplicado.
  - [ ] Limites legais de acréscimo e supressão.
  - Feito no Sprint 3: checklist de instrução (R7) na ficha do contrato e em `#/instrucao`, repositório local de documentos com visibilidade restrita à gestão (R8) e aviso de contrato sem instrução a 60 dias do fim no painel.
- **Sprint 0**: premissas assumidas em 30/10/2026. Cada item abaixo tem o valor
  adotado em [PREMISSAS.md](PREMISSAS.md), que é o que falta confirmar:
  - [ ] Confirmar as seis faixas do semáforo e o alerta de 90 dias com a gestão.
  - [ ] Definir as permissões de escrita (autor, chefia, gestor).

### Não Conformidades (`rnc-nao-conformidade`)

- **Visual**: acento `#b42318`, emblema `alerta`, layout `lateral`, padrão `linhas`, cabeçalho `institucional`.
- **Sprints concluídos**: 1, 2, 3.
- **Próximo**: Sprint 4 · Cópia do setor
  - [ ] Exportar `rnc-<setor>.json` só com as RNCs do setor (RN06).
  - [ ] Perfil Setor: `#/minhas`, registrar envio do plano (FOR 2) e avaliação (FOR 3).
  - [ ] Devolver o arquivo; a CQUAL importa e mescla.
- **Sprint 0**: premissas assumidas em 30/10/2026. Cada item abaixo tem o valor
  adotado em [PREMISSAS.md](PREMISSAS.md), que é o que falta confirmar:
  - [ ] Listar com a CQUAL as categorias de não conformidade e as gravidades.
  - [ ] Copiar o cabeçalho da planilha de respostas do Forms (sem dados) e anotar cada coluna.
  - [ ] Linha de base: tempo de cada etapa e cobranças da CQUAL nas RNCs do primeiro mês.

### TAP Digital (`tap-portfolio-projetos`)

- **Visual**: acento `#5b21b6`, emblema `portfolio`, layout `topo`, padrão `pontos`, cabeçalho `institucional`.
- **Sprints concluídos**: 1, 2, 3.
- **Próximo**: Sprint 4 · Proposta e decisão
  - [ ] `#/proposta/:id`: TAP, anexos, pendências, histórico.
  - [ ] Parecer da equipe e decisão da autoridade (aprovação, rejeição, readequação) com autor e data (RN07).
- **Sprint 0**: premissas assumidas em 30/10/2026. Cada item abaixo tem o valor
  adotado em [PREMISSAS.md](PREMISSAS.md), que é o que falta confirmar:
  - [ ] Receber o modelo vigente do TAP e a lista oficial de documentos.
  - [ ] Validar com a área responsável os campos obrigatórios e os tamanhos mínimos (RN01, RN02).
  - [ ] Linha de base: 4 semanas de registro (recebimento, documentação completa, devoluções e motivos).

### TCIN · Trilha de Custódia e Identificação (`trilha-custodia-necropsia`)

- **Visual**: acento `#0a5c64`, emblema `etiqueta`, layout `lateral`, padrão `pontos`, cabeçalho `institucional`.
- **Sprints concluídos**: 1, 2, 3.
- **Próximo**: Sprint 4 · Liberação
  - [ ] Auto de entrega com responsável, data e documento.
  - [ ] Bloqueio de liberação sem identificação e sem auto (RN02).
  - [ ] Trilha da liberação.
- **Sprint 0**: premissas assumidas em 30/10/2026. Cada item abaixo tem o valor
  adotado em [PREMISSAS.md](PREMISSAS.md), que é o que falta confirmar:
  - [ ] Confirmar com a aluna e o IML o nome do projeto (CNC ou TCIN).
  - [ ] Validar os quatro marcos e os livros que o app substitui.
  - [ ] Medir a linha de base de remoção, identificação e liberação.

## 5. Resultado da verificação (30/10/2026)

%RESULTADO%
