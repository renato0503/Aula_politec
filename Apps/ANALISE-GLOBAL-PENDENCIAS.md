# Análise global dos apps · 03/11/2026

> **Escopo:** `D:\Dev\Aula Politec\Apps`, 21 apps ativos.
> **Fora do escopo por decisão do professor:** `horus-banco-demandas` (Iohan) e
> `agendamento-cin` (Elthon) — pausados porque os alunos já desenvolveram nos
> próprios computadores. Os testes deles passam, mas não entram no plano abaixo.
>
> Base: execução de `python Apps/_base/testar.py`,
> `python Apps/_base/testar_sprints.py` e `python Apps/_base/painel.py`, leitura
> dos `sprint.md`, `FEEDBACK.md`, `CONTINUAR.md`, `CONTINUAR-IDENTIDADE.md`,
> `ENTREGA-03-11-2026.md` e `PREMISSAS.md`.
>
> **Plano de execução:** o runbook para a IA agêntica está em [`PLANO-IMPLEMENTACAO-AGENTICA.md`](PLANO-IMPLEMENTACAO-AGENTICA.md).
>
> **Rodada de implementação de 03/11/2026 (feita):** os itens de código do
> feedback de **TEIA**, **Controle de Aquisições**, **Adiantamento**,
> **Gestão de Documentos**, **Segunda via da CIN**, **Custódia definitiva**,
> **Passivo ambiental**, **Renovação de contratos**, **Metas BI**, **TAP** e
> **Comissão de Ética** foram implementados e testados. O restante de código
> está apenas em **Equipamentos** (teste manual no Google Earth) e nos aceites
> com o setor. **Inscrições**, **Mapa**, **Gestão de Identificados**, **RNC** e
> **Agiliza** foram concluídos no código.

## 0. Rodada de implementação (03/11/2026)

| App | O que foi implementado | Testes |
|---|---|---|
| **teia-triagem-emails** | Nova ficha: vítima, investigado, réu preso, tipo de crime, AR, protocolo `nnnnnn/aaaa`, data da cobrança = data do e-mail, 36 regionais, alerta de reiteração (2ª em 30 dias) e retirada de Nível/Nº da cobrança | `testar.py` OK; cenários 5 (s2 5/5, s3 4/4, s4 3/3, s5 8/8) |
| **controle-aquisicoes** | Painel compacto: KPI/tabelas menores, gráficos em 640 px e conferência no celular | `testar.py` OK; cenários 5 |
| **adiantamento** | Afastamento (férias/licença) bloqueia o pedido com motivo/data; pedido urgente com justificativa e trilha; recurso de 24 h na ficha/painel após a aprovação da chefia; Configuração de afastamentos | `testar.py` OK; cenários 6 (inclui s8 11/11) |
| **gestao-documentos** | Anexo opcional no processo de acompanhamento; data de entrada na lista; cobrança em 70% (amarelo) e no vencimento (vermelho); botão Cobrar na lista; tipo de processo na ficha | `testar.py` OK; cenários 6 (inclui s8 6/6) |
| **cin-segunda-via** | Documento extraviado pede 4 fotos de impressões digitais (não a do documento); fotos no protocolo/fila; texto do confronto papiloscópico; troca de perfil pelo menu | `testar.py` OK; cenários 5 (inclui s7 5/5) |
| **rnc-nao-conformidade** | Relação do setor para impressão com botão de imprimir; registro de quem importou; responsável pelo plano e pela avaliação; "Minhas RNCs" pelo setor | `testar.py` OK; cenários 10 (inclui s10 5/5) |
| **agiliza-mais** | Outras informações do perito, foto com sugestão de cor, ajuda dos arquivos e histórico com "Abrir"; o modelo institucional, a IA externa e o caso real seguem humanos | `testar.py` OK; cenários 6 (inclui s14 7/7) |
| **custodia-definitiva** | Endereço hierárquico, endereço sugerido x efetivo, cadastro em etapas, confirmação física, acervo com endereço/pendência, entradas/saídas e alertas clicáveis | `testar.py` OK; cenários 6 (inclui s8 7/7) |
| **passivo-ambiental** | Cabeçalho completo, editor de mapas, 3 mapas obrigatórios, abas de metodologia/considerações/valoração/quesitos e .docx | `testar.py` OK; cenários 6 (inclui s8 5/5) |
| **renovacao-contratos-horus** | Fiscais/gestores com contato, edição pelo ADM/gestor, aviso no painel e na ficha, fila local, objeto e busca na Instrução e importação de planilha | `testar.py` OK; cenários 6 (inclui s8 9/9) |
| **metas-bi-ocr** | Filtro de gerência, recorte de unidades monitoradas, cartão Pendentes, total ajustado e aprovação que abre a planilha | `testar.py` OK; cenários 6 (inclui s8 6/6) |
| **tap-portfolio-projetos** | Objetivos editáveis, sanar pendências, prazo de 5 dias, fila de avisos e cartão de prazos na Triagem | `testar.py` OK; cenários 7 (inclui s8 6/6) |
| **comissao-etica-denuncias** | Texto do artigo e enquadramento padrão, membros em lista, exclusão/encerramento de oitivas, ata com admissão, curso no relatório, encerramento e envio por e-mail | `testar.py` OK; cenários 6 (inclui s8 9/9) |
| **inscricoes-cursos** | Perfis diretoria/coordenação/gerência/chefe, instrutores e monitores, termo de convocação com as duas datas e checklist de divulgação | `testar.py` OK; cenários 9 (inclui s10 5/5) |
| **mapa-distribuicao-credor** | Leitura de PDF do pregoeiro e mapa orçamentário SESP no Exportar | `testar.py` OK; cenários 8 (inclui s10 3/3) |
| **gestao_identificados** | Cruzamento CNPD ↔ corpos com até 10 candidatos, motivo, confirmação/descarte/exame e justificativa na auditoria | `testar.py` OK; cenários 5 (inclui s5 4/4) |

**Regressão global:** `python Apps/_base/testar.py` **21/21** e
`python Apps/_base/testar_sprints.py` **todos os cenários OK** (133 no total
documentado: 130 anteriores + 3 novos). A árvore de trabalho continua sem
commit; os `sprint.md` e `PREMISSAS.md` dos apps foram atualizados.

## 1. Retrato atual

| Indicador | Resultado |
|---|---|
| Apps ativos | **21** |
| Telas no painel | **160/160**, **0 pendentes** (`painel.py`) |
| Estrutura (`testar.py`) | **21/21 OK**; zero requisição de rede |
| Cenários (`testar_sprints.py`) | **todos OK** (133 no total documentado) |
| Identidade, hub e diagramas | 21/21 |
| `gestao_identificados` | 21º app, com o módulo de desaparecidos (CNPD/NamUs/mapa) |

**Conclusão:** não faltam telas. O que falta é: (a) confirmação das premissas do
Sprint 0, (b) refinamento pedido no feedback dos alunos, (c) aceite/piloto e
(d) integrações com serviços externos. O painel marcar 160/160 não significa
"produto pronto"; significa que todas as telas planejadas existem.

## 2. Como classificar o que falta

| Código | Significado |
|---|---|
| **AGORA** | Código/UI que pode ser feito sem depender de ninguém |
| **PESSOA** | Depende de documento, medição, decisão ou aceite de alguém |
| **EXT** | Depende de serviço externo (e-mail, Google Sheets, Apps Script, OCR, Google Earth, sistema institucional) |
| **P2** | Refinamento/opcional; não bloqueia o MVP |
| **PAUSADO** | Fora do escopo por decisão do professor |

## 3. Matriz por app (19 em escopo)

| App | Estado | AGORA (código/UI) | PESSOA (Sprint 0, aceite, piloto) | EXT |
|---|---|---|---|---|
| **teia-triagem-emails** | MVP; **11/11 itens do feedback abertos** | Retirar Nível e Nº da cobrança; incluir vítima, investigado e réu preso; alerta de reiteração; protocolo `nnnnnn/aaaa`; data da cobrança = data do e-mail; tipos de crime; AR; lista de regionais; regra de reiteração | Confirmar regionais/grafia; onde o coordenador informa o nível; regra da reiteração | Parsing real de e-mail/PDF, OCR, renomeação e caixa institucional |
| **custodia-definitiva** | MVP; feedback grande | Hierarquia contêiner > estante > prateleira > nível > posição; endereço efetivo x sugerido; cadastro em etapas; confirmação física; acervo com endereço/motivos; painel de ocupação/saturação; alertas clicáveis; bloquear espaços incompatíveis; corrigir contêineres fictícios | Estrutura física real, capacidades e unidade; compatibilidade/conservação; o que é "contêiner" na futura Central | — |
| **passivo-ambiental** | MVP; feedback automatizável concluído 03/11 | — (resta o modelo oficial, os textos/critérios e o aceite) | Texto padrão da metodologia; critérios de valoração; mapas/fontes; nome do setor | — |
| **agiliza-mais** | MVP; feedback automatizável concluído 03/11 | — (resta o modelo institucional, a IA externa e o caso real) | Modelo institucional timbrado; textos oficiais; formato real dos TXT/HTML; testar o `CASO TESTE 2` | OCR de PDF em imagem (Tesseract/página a página) |
| **renovacao-contratos-horus** | MVP; feedback automatizável concluído 03/11 | — (resta o envio real de e-mail) | Dados dos fiscais/gestores; faixas do semáforo; modelo da planilha; permissões | E-mail automático com confirmação de leitura (MailApp/Apps Script) |
| **metas-bi-ocr** | MVP; feedback automatizável concluído 03/11; OCR pendente | — (resta OCR de PDF em imagem) | Lista/grafia das gerências; o que soma "Pendentes"; regra de aprovação; rodar com um mês real | OCR de PDF em imagem |
| **tap-portfolio-projetos** | MVP; feedback automatizável concluído 03/11 | — (resta o envio real dos avisos) | Lista oficial dos objetivos; confirmar prazo/contagem; testar com a Danielle | Avisos por e-mail (equipe, demandante, autoridade) |
| **comissao-etica-denuncias** | MVP; feedback automatizável concluído 03/11 | — (resta o canal institucional de envio) | Modelos oficiais de ata, oitiva e relatório; lista nominal dos membros; confirmar categorias | Envio dos documentos por e-mail (fila local + canal institucional) |
| **inscricoes-cursos** | MVP; feedback automatizável concluído 03/11 | — (resta publicar e testar o Outlook) | Diretorias e siglas; CPF sai do formulário?; TI da caixa `capacitacao@`; linha de base; aceite/piloto | Outlook desktop/Web/celular; resposta automática; publicação |
| **adiantamento** | MVP; feedback | Bloquear pedido em férias/licença-prêmio, com motivo e data; pedido urgente com justificativa/trilha; prazo de 24 h para recurso; mostrar na ficha e no painel | De onde vem o afastamento (RH/SIGRH/planilha); quem autoriza urgência; o prazo de 24 h conta de quê; o que é "construção" para o Linicker | — |
| **cin-segunda-via** | MVP; feedback | Pedir fotos das impressões digitais (não do documento) quando extraviado; anexar/encaminhar no protocolo e na fila; troca de perfil mais rápida; deixar claro o que é conferido no confronto | Conjunto mínimo/qualidade das fotos; quem valida o confronto; regras oficiais da 2ª via; fonte dos números | Integração com a base biométrica (TI/empresa) |
| **gestao-documentos** | MVP; feedback | Anexo opcional no acompanhamento; data de entrada na lista; notificação/cobrança perto do vencimento; definir quais processos dispensam anexo | Anexos obrigatórios por tipo (RN01); matriz de papéis; canal/antecedência da notificação; linha de base | E-mail/painel de notificação |
| **rnc-nao-conformidade** | MVP; feedback de código concluído 03/11 | — (resta o modelo oficial, a autenticação real e testar a planilha real) | Modelo oficial da RNC; regras de login/permissão; planilha real | Google Planilhas (CSV público) e e-mail |
| **mapa-distribuicao-credor** | MVP; feedback automatizável concluído 03/11 | — (resta o modelo oficial da SESP e a amostra real) | `WorkFlow.docx` (exemplos 1-8); 4 pontos `[validar]`; relatório do pregoeiro; `mapa-manual-referencia.xlsx`; regras de situação/dotação/empate; linha de base | PDF do pregoeiro; publicação/aceite/piloto |
| **controle-aquisicoes** | MVP; feedback pequeno | Reduzir a fonte do painel (KPI/tabelas/gráficos) e conferir no celular; manter gráficos em 640 px | Modelos oficiais DFD/ETP/TR/risco; fluxo/prazos; permissões e base 2024/2025 | — |
| **equipamentos-google-earth** | MVP; feedback mínimo | Nenhum ajuste de código pedido; manter gráficos em 720 px; conferir o `.kmz` | Lista de diretorias/unidades; planilha atual; valor de referência/custo; 3 unidades do piloto; aceite/piloto 30 dias | Teste manual no Google Earth Pro/Web |
| **documentapolitec** | MVP; **tecnicamente completo** | — | Formato do prontuário e modelo das caixas; planilha de 850 prontuários; amostra do PDF digitalizado; aceite | — |
| **trilha-custodia-necropsia** | MVP; **tecnicamente completo** | — | Nome do projeto (CNC/TCIN); quatro marcos/livros; linha de base; regras de recebimento/sepultamento com o IML; aceite | — |
| **gestao_identificados** | MVP + módulo CNPD/NamUs; cruzamento concluído 03/11 | — (resta o aceite do NIHDE e os pesos do match) | Confirmar nome oficial do NIHDE e escopo dos dados físicos; integração com Atena; linha de base; aceite/piloto 90 dias | INTERPOL, NCMEC, portais estaduais; acesso a SINALID/CADÊ/SINESP/RIBPG/SINAB/Atena; termos/LGPD |

## 4. O que pode ser feito agora (sem depender de ninguém)

### P0 · desbloqueia demonstração ou corrige risco

1. ~~**TEIA**~~: feito em 03/11/2026 (campos, região, reiteração). Resta o
   parsing real/OCR.
2. ~~**Agiliza**~~: feito na parte automatizável (outras informações, foto/cor,
   ajuda dos arquivos e histórico). Restam o modelo institucional, a IA externa
   e o caso real.
3. ~~**Custódia definitiva**~~: feito em 03/11/2026 (hierarquia, confirmação,
   acervo, painel e alertas). Resta a estrutura física real e o aceite.
4. ~~**Passivo ambiental**~~: feito em 03/11/2026 (cabeçalho, mapas, abas e .docx).
   Resta o modelo oficial/textos e o aceite.
5. **Renovação**: fiscais/gestores por contrato, edição, objeto e importação da
   planilha (o e-mail pode ficar em fila local).
6. **Gestão de Identificados**: tela de candidatos + confirmação humana no
   `log`; link do módulo no painel/hub; atualizar o `sprint.md`.
7. **Global**: reconciliar a documentação (ver seção 6) e regenerar painel/hub/
   links; a árvore de trabalho está com muitas mudanças não commitadas.

### P1 · feedback do aluno, código/UI

- **Metas**: filtro por gerência, cartão "Pendentes", fluxo aprovar/gerar.
- **TAP**: objetivos reais, fluxo pendência → análise → autoridade, prazo de 5 dias.
- **Comissão**: texto do artigo, membros, oitivas, minutas.
- **Inscrições**: perfis, instrutores/monitores, termo de convocação, Divulgar/Triagem.
- **Feitos nesta rodada:** Controle, Adiantamento, CIN, Gestão de Documentos e
  RNC. O que resta deles é decisão/aceite ou serviço externo.
- **Mapa**: PDF do pregoeiro, mapa orçamentário SESP, dígitos, situação, empresa.
- **Controle**: fonte do painel e conferência no celular.

### P2 · refinamento/opcional

- TAP: escala da matriz e sobreposição dos pontos.
- Comissão: funil de 7 etapas x barra de 6.
- Adiantamento: perfis e "Minha fila".
- Documentapolitec: cada Enter da conferência não deve redesenhar a ficha.
- Custódia: a prateleira deve abrir a ficha do contêiner, não o acervo filtrado.
- Controle: kanban de 9 colunas no celular.
- Metas: conferência e geração no menu.
- Agiliza: Biblioteca/Histórico (parte já entregue; conferir).
- Renovação: "Meus contratos" sem digitar o nome do fiscal.
- Agiliza: Sprint 13 (laudo anterior como modelo) e OCR real.
- TEIA: parsing real/OCR/caixa institucional.

## 5. O que está bloqueado e por quem

| Bloqueio | Apps afetados | Como desbloquear |
|---|---|---|
| Sprint 0: documentos, medições e decisões | praticamente todos | Reunião com cada aluno/setor; `Apps/PREMISSAS.md` diz o que confirmar e o nível de confiança |
| Aceite e piloto | todos | Roteiro em `modelos/roteiro-aceite.md`; depende da chefia de cada unidade |
| Google Earth manual | equipamentos-google-earth | Abrir o `.kmz` no Google Earth Pro e Web; confirmar base/mapa |
| Outlook e celular | inscricoes-cursos | Testar o formulário no Outlook desktop/Web e no celular |
| E-mail institucional | comissao, renovacao, tap, gestao-documentos, inscricoes, rnc | Definir canal (MailApp/Apps Script/SMTP), textos e confirmação de leitura |
| Google Planilhas | rnc-nao-conformidade | Planilha pública + teste com o link real; CSP já libera `docs.google.com` |
| OCR | agiliza-mais, metas-bi-ocr | Decidir Tesseract.js embutido x `ocr.html` separado; testar com PDF real |
| Base biométrica | cin-segunda-via | TI e empresa da coleta; LGPD |
| Atena e sistemas periciais | gestao_identificados | Direção da POLITEC; integração fase 2 |
| SINALID/CADÊ/SINESP/RIBPG/SINAB | gestao_identificados | Credencial/termo de cooperação; não são públicos |
| GitHub Pages | todos os repositórios separados | Decidir se publica em cada repo ou mantém o monorepo; ligar Pages |
| Logins/convites | 2 logins 404, 5 sem login, convites pendentes | Pedir login correto; reenviar convite; aceitar convite |

## 6. Tarefas globais

1. **Documentação divergente**: `CONTINUAR-IDENTIDADE.md` ainda fala em 21 apps
   e 92/92; `ENTREGA-03-11-2026.md` fala em 22 rotas pendentes (já resolvidas);
   `PREMISSAS.md` é de 30/10. Consolidar em um único estado atual.
2. **Painel/hub/links**: rodar `painel.py`, `gerar_hubs.py`, `hub_apps.py`,
   `gerar_links_alunos.py` e `gerar_diagramas.py` depois das mudanças. O painel
   já marca 160/160; o hub do `gestao_identificados` foi regerado e aponta para
   `desaparecidos.html`, enquanto a rota `#/desaparecidos` aparece no menu do
   app. Se o professor quiser o link direto para a rota no hub, ajustar o
   gerador.
3. **GitHub Pages**: os 20/21 repositórios separados não têm Pages; os links dos
   alunos apontam para o monorepo. Decidir e documentar.
4. **Acessos**: corrigir os 2 logins 404, pedir os 5 que faltam e acompanhar os
   convites (Nelson/Helen no TEIA, Kesia no NIHDE).
5. **Feedback**: 18 respostas em 16 apps; o Agendamento aguarda; os demais não
   responderam. Cada `FEEDBACK.md` é a entrada do próximo sprint.
6. **Sprint 0**: o maior bloqueio. Revisar `PREMISSAS.md` app por app e marcar no
   `sprint.md` o que foi confirmado; trocar as premissas pelas informações reais.
7. **Qualidade**: reexecutar `testar.py`, `testar_sprints.py`, Lighthouse e a
   jornada depois de cada rodada; manter zero rede e celular sem rolagem.
8. **LGPD/segurança**: RNC (planilha pública), fotos de impressões digitais,
   e-mails, dados de desaparecidos e acesso por perfil. Registrar finalidade e
   retenção.
9. **Commit/push**: a árvore de trabalho tem muitas mudanças da segunda etapa e
   do módulo de desaparecidos. Fazer commits por app, sem os `.xlsx`/`.pbix` da
   `Aula 4/`, e publicar quando o professor confirmar.

## 7. Ordem sugerida

**Semana 1 (AGORA):**

1. TEIA (11 itens) + parsing real/OCR como projeto separado.
2. Agiliza (marcadores, revisão, histórico, foto/cor, textos/quesitos).
3. Custódia (endereço hierárquico, confirmação, painel).
4. Passivo (mapas, abas, `.docx`).
5. Renovação (fiscais/gestores, edição, objeto, planilha).
6. Gestão de Identificados (candidatos + confirmação + link no painel).
7. Documentação global + painel/hub + logins/convites.

**Semana 2 (AGORA + PESSOA):**

1. Metas, TAP, Comissão, Inscrições, Adiantamento.
2. CIN, Gestão de Documentos, RNC, Mapa, Controle.
3. Rodada de Sprint 0 com os alunos (documentos, medições, decisões).
4. Aceite/piloto dos apps que já estão tecnicamente completos
   (`documentapolitec`, `trilha-custodia-necropsia`, `equipamentos`).
5. Reexecutar todos os testes e publicar.

## 8. Apps fora do escopo (pausados)

| App | Dono | Estado | O que fazer |
|---|---|---|---|
| `horus-banco-demandas` | Iohan | MVP e testes OK | Não mexer; quando retomar, seguir o `sprint.md` e o backlog de contexto de unidade |
| `agendamento-cin` | Elthon | MVP e testes OK; Apps Script a ligar | Não mexer; quando retomar, o único passo externo é publicar o Apps Script e ligar `LockService`/`MailApp` |

Eles continuam aparecendo no painel e nos testes globais; a pausa é de
prioridade, não de qualidade.

## 9. Observações para o próximo agente

- **Não edite `index.html`**: rode `python construir.py` dentro do app.
- Rode `python testes/testar.py` e `python testes/cenarios.py` no app alterado;
  depois `python Apps/_base/testar.py <app>` e
  `python Apps/_base/testar_sprints.py <app>`.
- O `sprint.md` de vários apps tem itens já feitos **sem `[x]`** (ex.: Agiliza e
  alguns feedbacks). Ao mexer, atualize a marcação para a análise não mentir.
- O `gestao_identificados` tem um módulo novo (CNPD/NamUs/mapa) fora do ciclo
  dos grupos; o `sprint.md` foi atualizado em 03/11/2026, mas o cruzamento com
  os corpos continua aberto.
- O `painel.py` mostra 160/160 telas; use-o para conferir telas, não para medir
  produto. O que falta está nas seções 3 a 6.
