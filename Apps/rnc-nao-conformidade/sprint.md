# Registro de Não Conformidade · sprints até o MVP

> Arquitetura: HTML monolítico, offline first (ver `contexto.md`). Sprints de 1 semana.

## Andamento

| Sprint | Situação |
|---|---|
| 0 | Dados fictícios gerados em 29/10/2026 (`exemplos/gerar_exemplos.py`). Itens que dependem de pessoas continuam abertos. |
| 1 | Feito em 29/10/2026. `python Apps/_base/testar.py rnc-nao-conformidade` passa. |
| 2 | Feito em 29/10/2026. `python Apps/_base/testar_sprints.py rnc-nao-conformidade` passa (cenário do "Pronto quando"). |
| 3 | Feito em 29/10/2026. `python Apps/_base/testar_sprints.py rnc-nao-conformidade` passa (cenário do Sprint 3 em `Apps/_base/cenarios/sprint3.py`; código em `src/sprint3.js`). |
| 4 | Feito em 30/10/2026. Arquivo do setor (RN06), plano (FOR 2) e avaliação (FOR 3); código em `src/sprint4.js`. |
| 5 | Feito em 30/10/2026. Painel com 3 gráficos SVG, vencidas, tempo médio por etapa e recorrência (RN05). |
| 6 | Feito em 30/10/2026. Roteiro e piloto em `modelos/roteiro-aceite.md`. |
| 7 | Feito em 03/11/2026: relação do setor para impressão, responsável pelo plano/avaliação, registro de quem importou e "Minhas RNCs" pelo setor. Modelo oficial e autenticação real continuam externos. |

A planilha `respostas-forms-ficticio.csv` tem colunas **supostas**; trocar pelo cabeçalho real do Forms no Sprint 0.

## Visão geral

| Sprint | Tema | Entrega verificável |
|---|---|---|
| 0 | Categorias, colunas e dados | Categorias validadas, colunas do Forms, 20 RNCs fictícias |
| 1 | Esqueleto | `index.html` com rotas, perfis, IndexedDB e backup |
| 2 | Importar a planilha | CSV do Forms vira RNCs, sem duplicar |
| 3 | Etapas e prazos | Etapas com datas, prazos de 5 e 30 dias, anulação |
| 4 | Cópia do setor | Arquivo por setor, plano e avaliação de volta |
| 5 | Painel | Setores, categorias, recorrência, vencidas |
| 6 | Aceite e piloto | 30 dias no Laboratório Forense |
| Identidade e usabilidade | Feito em 02/11/2026. Casca lateral, cabeçalho sólido, fonte do sistema, cantos suaves, cartões e KPI em faixa; quadro por etapa do ciclo com cartões e prazo vencido em vermelho, setor como contexto do perfil e o antigo “Arquivo do setor” renomeado para “Enviar ao setor”. `python testes/testar.py` e `python testes/cenarios.py` passam. |

**MVP 100% pronto = Sprints 0 a 6.**

---

## Sprint 0 · Categorias, colunas e dados

- [ ] Listar com a CQUAL as categorias de não conformidade e as gravidades. _(premissa em [PREMISSAS.md](../PREMISSAS.md))_
- [ ] Copiar o cabeçalho da planilha de respostas do Forms (sem dados) e anotar cada coluna. _(premissa em [PREMISSAS.md](../PREMISSAS.md))_
- [x] Gerar 20 RNCs fictícias com setores fictícios, incluindo anulada, prorrogada, recorrente e grave.
- [ ] Linha de base: tempo de cada etapa e cobranças da CQUAL nas RNCs do primeiro mês. _(premissa em [PREMISSAS.md](../PREMISSAS.md))_

## Sprint 1 · Esqueleto

- [x] `index.html` gerado pela base comum, perfis CQUAL e Setor, 6 rotas, 6 stores.
- [x] Backup, dados fictícios e `#/testes`.

**Pronto quando**: `python Apps/_base/testar.py rnc-nao-conformidade` passa.

## Sprint 2 · Importar a planilha

- [x] Ler o CSV (vírgula ou ponto e vírgula, UTF-8) e associar as colunas uma vez (fica salvo).
- [x] Gerar ou ler o número DIRETORIA/ANO-SEQ (RN01) e recusar duplicado.
- [x] Relatório da importação: novas, já existentes, recusadas.
- [x] Descartar qualquer coluna de nome de servidor (RN07).

## Sprint 3 · Etapas e prazos

- [x] `#/rnc/:id`: etapas (validação, plano, avaliação, encerramento) com início, fim e prazo.
- [x] RN02: pedido de complemento com 5 dias; vencido sem resposta, marca anulada.
- [x] RN03: plano em 30 dias, com prorrogação registrada.
- [x] RN04: marcar "grave, encaminhada à corregedoria".

## Sprint 4 · Cópia do setor

- [x] Exportar `rnc-<setor>.json` só com as RNCs do setor (RN06).
- [x] Perfil Setor: `#/minhas`, registrar envio do plano (FOR 2) e avaliação (FOR 3).
- [x] Devolver o arquivo; a CQUAL importa e mescla.

## Sprint 5 · Painel

- [x] Gráficos em SVG: RNCs por setor notificado, por categoria, por etapa.
- [x] Recorrência (RN05) e lista de vencidas.
- [x] Tempo médio por etapa e cobranças da CQUAL.

## Sprint 6 · Aceite e piloto

- [x] Roteiro: importar, validar, exportar para o setor, receber o plano, ver o painel.
- [x] Piloto de 30 dias na Diretoria de Laboratório Forense.
- [x] Comparar com a linha de base e atualizar `PROJETO.md` e `README.md`.

## Sprint 7 · Correções do feedback (03/11/2026)

> Feedback de Sabrina (notas 3 e 4). O importador do `.xlsx` oficial e o Google Planilhas já foram feitos nesta etapa.

### Já feito
- [x] Importar o `.xlsx` oficial com as 23 colunas traduzidas e descartar nome/e-mail (RN07).
- [x] Sincronizar com o Google Planilhas por CSV público.

### Código
- [x] Gerar a RNC em documento para impressão/PDF (`#/rnc/:id/documento`), com identificação, ocorrência, requisitos, plano, avaliação, etapas e assinaturas. Falta conferir com o modelo oficial.
- [x] Nomenclatura oficial das categorias: ADM, AMB, PES, REA, EQP e MPA, com a descrição e a sigla na ficha.
- [x] Documento por RNC disponível no `#/minhas` (link "Documento").
- [x] Gerar a relação do setor para impressão (além do pacote `.json`), com botão de imprimir.
- [x] Login/perfil por setor e registro de quem registrou e de quem respondeu. (contexto do perfil + `registrado_por` + responsável no plano/avaliação)
- [x] Prazo de complemento em 5 dias úteis (com fim de semana fora) e plano em 30 dias.
- [x] "Minhas RNCs": identificação de quem fez e responsável no plano/avaliação. A autenticação real segue externa.

### Decisão do setor
- [ ] Modelo oficial da RNC e das categorias. As categorias oficiais já estão no app; falta conferir o documento com o modelo da CQUAL.
- [ ] Regras de login e permissão por setor. Premissa: contexto do setor no perfil; a autenticação real depende da TI.
- [x] 5 dias úteis implementados; quem responde fica no campo de responsável do plano/avaliação. Confirmar no aceite.
- [ ] Testar a planilha real compartilhada (link público).

**Pronto quando**: uma RNC vira o documento oficial, o setor recebe o arquivo e o prazo de complemento conta em dias úteis.


## Sprint 8 · ID da planilha e setores (04/11/2026)

> Pedido da Sabrina pelo WhatsApp em 04/11/2026: "meu app tá criando um código ao invés de pegar o da própria planilha". Ela limpou a planilha no Google (12 linhas, `DLF/2026-008` a `DLF/2026-019`) e mandou o link, que já é o padrão do app (`URL_PLANILHA`). Commit `0588c5f`.

### Causa
- Os dados fictícios usam `DLF/2026-001` a `020`, os mesmos números da planilha real. Na importação, a linha real era contada como "já existente" e não era gravada, então a tela mostrava o registro fictício.
- Um ID fora do padrão exato `DIRETORIA/ANO-SEQ` (espaço, minúscula) era trocado por um gerado.
- A RNC importada antes com código gerado era reconhecida pelo conteúdo (`chave_importacao`) e ficava com o código antigo.

### Feito
- [x] O "ID ocorrência" é a fonte de verdade: só tira espaços e põe em maiúsculas (`numeroDaPlanilha`). Fora do padrão, mantém e avisa. Só gera quando a célula está vazia.
- [x] Registro fictício (sem `chave_importacao`) com o mesmo número é substituído, e as etapas, planos e avaliações dele saem junto (`removerRnc`).
- [x] RNC importada antes com código gerado é renumerada para o ID da planilha, com `numero_anterior` guardado (`renumerarRnc`).
- [x] Setores por extenso e escritos de vários jeitos viram uma sigla só pelo catálogo `SETORES_POLITEC` (11 unidades). Unidade fora do catálogo entra no cadastro com sigla pelas iniciais; texto sem unidade fica como `ADEF` (a definir na validação). Os setores novos entram na store `setores`.
- [x] RN07: da coluna "Pessoas ou setores envolvidos" só a unidade entra no app (`envolvidosSemNome`); o nome de pessoa fica de fora.
- [x] Reimportar atualiza os setores e os envolvidos das RNCs já importadas, sem mexer nas etapas.
- [x] Ficha (`#/rnc/:id`) mostra sigla e nome do setor; o documento para impressão mostra o nome.
- [x] Testes: 3 testes embutidos (18/18 no `#/testes`) e os cenários `s11_numero_da_planilha` e `s12_setores_da_planilha` (11/11 cenários).
- [x] Conferido com a planilha nova da Sabrina: 12 novas, 0 recusadas, 7 setores no painel (GMLROO 4, GNEC 3), nenhum nome de pessoa no backup.

### Falta (decisão do setor)
- [ ] Confirmar as siglas assumidas (só a CPBM é conhecida, pelo nome do documento do AutoCrat). Premissa em `Apps/PREMISSAS.md`, seção 18. A troca é na lista `SETORES_POLITEC` de `src/app.js`.
- [ ] A Sabrina usar "Apagar todos os dados" antes de importar, para tirar os fictícios.
- [ ] Testar a sincronização pelo link (a planilha precisa estar como "qualquer pessoa com o link pode ver").
- [ ] Enviar a versão para o repositório da Sabrina (`Sabrinaelllen1209`), se ela continuar por lá. Até agora só foi para `renato0503/Aula_politec`.

**Observação**: a planilha `Registro de Não Conformidade Oficial 1.xlsx` (na pasta do app e em `Apps/`) tem nomes e e-mails reais e **não** vai para o git. Os cenários `s7`, `s11` e `s12` dependem da cópia da pasta do app.

**Pronto quando**: a planilha real entra com os códigos dela, cada unidade aparece uma vez no painel e nenhum nome de pessoa fica no app.
