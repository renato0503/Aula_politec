# Como publicar o Agendamento CIN

## Testar sem publicar

Abra `index.html` com duplo clique. Sem o Apps Script, o app entra no **modo de
teste local**: usa os dados fictícios da `planilha-modelo/` guardados no
navegador, e o perfil (posto ou gestão) é escolhido na tela. Os testes
automáticos ficam em `index.html#/testes`.

## Publicar (precisa da autorização da TI, Sprint 0)

Um app da web do Apps Script tem **uma** configuração de acesso por projeto
(`appsscript.json`). O cidadão precisa de acesso anônimo, e o posto precisa ser
identificado pela conta institucional. Por isso, são **dois projetos** com o
mesmo `index.html` e o mesmo `Code.gs`, ligados à mesma planilha:

| Projeto | `executeAs` | `access` | Quem usa | `quemSou()` |
|---|---|---|---|---|
| Público | `USER_DEPLOYING` | `ANYONE_ANONYMOUS` | cidadão | sempre sem perfil (só telas públicas) |
| Interno | `USER_ACCESSING` | `DOMAIN` | posto e gestão | perfil pela aba `usuarios` |

O `appsscript.json` desta pasta é o do projeto público. No projeto interno,
troque o bloco `webapp` por `{"executeAs": "USER_ACCESSING", "access": "DOMAIN"}`.

Passo a passo (com o [clasp](https://github.com/google/clasp)):

1. Crie a planilha e importe cada CSV de `planilha-modelo/` como uma aba com o mesmo nome. Copie o ID da planilha (o trecho da URL entre `/d/` e `/edit`).
2. Crie um projeto em script.google.com (ou `clasp create --type standalone`).
3. Copie `index.html`, `Code.gs` e `appsscript.json` para a pasta do projeto e rode `clasp push`.
4. No editor: Configurações do projeto > Propriedades do script > `PLANILHA_ID` = o ID do passo 1.
5. Implantar > Nova implantação > App da Web. Anote a URL.
6. Repita os passos 2 a 5 para o projeto interno, com o `webapp` interno.

A regra de "o posto só vê o próprio posto" (RN05) é conferida no `Code.gs`, pela
aba `usuarios`, e não só na tela.
