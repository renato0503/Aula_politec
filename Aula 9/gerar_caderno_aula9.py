# -*- coding: utf-8 -*-
"""Gera o Caderno 9 e os pacotes de continuidade dos 21 MVPs.

Rode:  python "Aula 9/gerar_caderno_aula9.py"
PDF:   python exportar_pdf.py 9
"""
import pathlib
import sys

PASTA = pathlib.Path(__file__).resolve().parent
RAIZ = PASTA.parent
sys.path.insert(0, str(RAIZ))
sys.path.insert(0, str(PASTA))

from caderno_lib import (Caderno, p, h3, h4, ul, ol, checklist, ficha, callout,
                         tbl, code, step, q, aplicab, grid2, flow_h, kpi,
                         antesdepois, legenda, glossary)
from dados_apps import APPS, BASE, SITE


def repo(a):
    return f"{BASE}/{a['slug']}"


def zip_url(a):
    return f"{BASE}/{a['slug']}/archive/refs/heads/main.zip"


def git_steps(a):
    return [
        f"Entre em {repo(a)} e aceite o convite de colaborador. Se ainda não recebeu, peça ao professor para enviar de novo.",
        f"Clique em **Code > Download ZIP** ou clone: `git clone {repo(a)}.git`. O ZIP serve para abrir e estudar; para enviar alterações, use o clone ou um fork.",
        f"Extraia em uma pasta curta, por exemplo `C:\\POLITEC\\{a['slug']}`. Evite OneDrive e caminhos com muitos espaços.",
        "Abra o **Antigravity**, escolha **File > Open Folder** e selecione a pasta que contém `app.json`, `src`, `nucleo`, `construir.py` e `testes`.",
        f"No terminal do Antigravity, rode `git checkout -b melhoria/{a['slug']}` para criar uma branch de trabalho.",
        "Leia `README.md`, `PREMISSAS.md` e `sprint.md`. Não edite `index.html`: ele é gerado pelo `construir.py`.",
        "Edite as fontes, rode `python construir.py`, abra o `index.html` e rode os testes do app.",
        "Faça `git add .`, `git commit -m \"...\"`, `git push origin melhoria/<tema>` e abra um Pull Request no GitHub. Peça revisão antes do merge.",
    ]


def html_app(a):
    body = p(f"<b>Equipe:</b> {a['equipe']} · <b>Tipo:</b> {a['tipo']} · "
             f"<b>Repositório:</b> <a href=\"{repo(a)}\">{repo(a)}</a>")
    body += p(a["resumo"])
    body += ficha("g", "O que já está pronto", ul(a["pronto"]))
    body += ficha("a", "O que falta", ul(a["falta"]))
    body += h3("Roteiro no GitHub, do zero ao pull request")
    body += step(git_steps(a))
    body += h3("Integração que falta, passo a passo")
    for titulo, passos in a["etapas"]:
        body += h4(titulo) + step(passos)
    body += h3("Como testar")
    body += code("\n".join(a["teste"]), "powershell")
    body += h3("Prompt para colar no Antigravity")
    body += code(
        f"Você está no projeto {a['nome']} ({a['slug']}). Leia README.md, PREMISSAS.md e sprint.md.\n"
        f"Não edite index.html. Trabalhe apenas em: {a['falta'][0]}.\n"
        "Antes de alterar, rode python construir.py e os testes. Depois de alterar, explique o que mudou, "
        "rode os testes de novo e mostre o diff. Não use dados reais nem peça token.",
        "texto")
    body += callout("tip", "Mensagem de commit sugerida", code(a["commit"], "texto"))
    body += p(f"Pacote individual: <code>Aula 9/pacotes/{a['slug']}.md</code>. "
              f"App publicado: <a href=\"{SITE}/{a['slug']}/index.html\">{SITE}/{a['slug']}/index.html</a>.")
    return body


def md_app(a):
    linhas = [
        f"# Pacote de continuidade · {a['nome']}",
        "",
        f"**Equipe:** {a['equipe']}  ",
        f"**Tipo:** {a['tipo']}  ",
        f"**Repositório:** {repo(a)}  ",
        f"**App publicado:** {SITE}/{a['slug']}/index.html  ",
        f"**ZIP:** {zip_url(a)}",
        "",
        "## 1. O que este app faz",
        "",
        a["resumo"],
        "",
        "## 2. O que já está pronto",
        "",
    ]
    linhas += [f"- {x}" for x in a["pronto"]]
    linhas += ["", "## 3. O que falta", ""]
    linhas += [f"- {x}" for x in a["falta"]]
    linhas += ["", "## 4. Baixar e abrir no Antigravity", ""]
    linhas += [
        f"1. Abra {repo(a)} e aceite o convite de colaborador.",
        f"2. Baixe o ZIP em {zip_url(a)} ou clone com `git clone {repo(a)}.git`.",
        f"3. Extraia em `C:\\POLITEC\\{a['slug']}`.",
        "4. No Antigravity, use **File > Open Folder** e escolha a pasta que tem `app.json`, `src`, `nucleo` e `construir.py`.",
        "5. Abra o terminal e confira `python --version`.",
        "6. Rode `python construir.py`.",
        "7. Abra `index.html` no Edge ou no Chrome e clique em **Configuração > Carregar dados fictícios**.",
        "",
        "## 5. Integração que falta, passo a passo",
        "",
    ]
    for titulo, passos in a["etapas"]:
        linhas += [f"### {titulo}", ""]
        linhas += [f"{i}. {x}" for i, x in enumerate(passos, 1)]
        linhas += [""]
    linhas += ["## 6. Como testar", "", "```powershell"]
    linhas += a["teste"]
    linhas += ["```", "", "Se o teste falhar, leia a primeira mensagem, corrija uma coisa por vez e rode de novo.", ""]
    linhas += ["## 7. Enviar para o GitHub", ""]
    linhas += [f"{i}. {x}" for i, x in enumerate(git_steps(a), 1)]
    linhas += ["", "## 8. Prompt para o Antigravity", "", "```text",
               f"Você está no projeto {a['nome']} ({a['slug']}). Leia README.md, PREMISSAS.md e sprint.md.",
               f"Não edite index.html. Trabalhe apenas em: {a['falta'][0]}.",
               "Antes de alterar, rode python construir.py e os testes. Depois de alterar, explique o que mudou,",
               "rode os testes de novo e mostre o diff. Não use dados reais nem peça token.", "```", "",
               f"**Commit sugerido:** `{a['commit']}`", "",
               "## 9. Onde pedir ajuda", "",
               "- Leia `PREMISSAS.md` para saber o que ainda é decisão do setor.",
               "- Leia `sprint.md` para ver o que já foi feito e o que está aberto.",
               "- Abra uma issue no repositório com o print, o passo e a mensagem de erro.",
               ""]
    return "\n".join(linhas)


cad = Caderno(
    out=str(PASTA / "caderno-dia9.html"),
    dia=9,
    kicker="Aula 9 · Continuidade dos MVPs e entrega final",
    headline="Do MVP apresentado ao projeto que continua no GitHub",
    sub="O caderno final do curso. Um guia passo a passo para baixar o projeto, "
        "abrir no Antigravity, rodar, testar, corrigir e devolver pelo GitHub, "
        "com um pacote individual para cada um dos 21 MVPs.",
    meta="Curso de Capacitação POLITEC/MT · Professor Renato Rosa · Dia 9 · "
         "Módulo 10 (Continuidade, GitHub e entrega final)",
    descricao="Caderno 9 do Curso de Capacitação POLITEC/MT: guia de continuidade "
              "dos 21 MVPs, GitHub do zero, Antigravity, integração por app, "
              "testes, pull request, aceite e entrega final.",
)

# =================================================================
# ABERTURA
# =================================================================
cad.grp("Abertura", "O que é o Caderno 9, como usar e o contrato da entrega.")

cad.section("abertura-boas-vindas", "Boas-vindas à última etapa",
    p("Este é o caderno que fecha o curso. Até aqui, cada grupo construiu um MVP "
      "funcional, com telas, dados fictícios, testes e um repositório no GitHub. "
      "A partir de agora, o trabalho continua com vocês: o professor entrega o "
      "projeto, e cada equipe assume a integração com o setor, o aceite e o piloto.")
    + p("O caderno não ensina a programar do zero. Ele ensina a continuar um "
        "projeto que já funciona: baixar, abrir, entender, alterar, testar, "
        "versionar e devolver pelo GitHub.")
    + ficha("p", "A regra de ouro", p("O <code>index.html</code> é gerado. "
      "Edite <code>src/</code>, <code>app.json</code>, <code>nucleo/</code>, "
      "<code>exemplos/</code> e <code>modelos/</code>. Depois rode "
      "<code>python construir.py</code>."))
    + callout("tip", "O que você leva", "21 pacotes individuais em "
      "<code>Aula 9/pacotes/</code>, um por app, com o repositório, o que falta, "
      "o passo a passo de integração, os comandos de teste e a mensagem de commit."))

cad.section("abertura-mapa", "O mapa do caderno",
    p("O caderno tem seis partes. A Parte 1 é o GitHub. A Parte 2 é o Antigravity "
      "e a anatomia de um app. A Parte 3 é o pacote dos 21 MVPs. A Parte 4 traz "
      "as receitas de integração. A Parte 5 é o trabalho em equipe. A Parte 6 é "
      "o aceite e a entrega final.")
    + tbl(["Parte", "Pergunta que responde", "Entregável"], [
        ["1. GitHub", "Como baixar, versionar e devolver?", "Repositório atualizado e Pull Request"],
        ["2. Antigravity e app", "Onde fica cada arquivo e como rodar?", "App aberto e teste passando"],
        ["3. Os 21 MVPs", "O que falta no meu app?", "Pacote individual do app"],
        ["4. Integrações", "Como ligar e-mail, Sheets, OCR e Earth?", "Fila local e roteiro técnico"],
        ["5. Equipe", "Como trabalhar sem sobrescrever o outro?", "Branch, issue, revisão e merge"],
        ["6. Entrega", "Como provar que está pronto?", "Aceite, piloto e ata"],
    ])
    + callout("note", "Tempo sugerido", "Leia a Parte 1 e a Parte 2 na aula. "
      "Use a Parte 3 como manual do seu app. As Partes 4 a 6 ficam para as "
      "duas semanas seguintes, com encontros de acompanhamento.")
    + p("O material foi escrito para ser lido no computador, no tablet ou no "
        "celular. O HTML funciona offline. O PDF serve para imprimir e levar "
        "para a reunião com o setor."))

cad.section("abertura-contrato", "O contrato da continuidade",
    p("Cada grupo recebe um app que já funciona. O compromisso é não recomeçar "
      "do zero e não estragar o que já passa nos testes. O contrato tem cinco "
      "itens.")
    + checklist(["O app continua abrindo offline e sem requisição de rede.",
                 "O <code>index.html</code> continua sendo gerado pelo <code>construir.py</code>.",
                 "Os dados fictícios continuam separados dos dados reais.",
                 "Toda alteração entra por branch e Pull Request, com teste.",
                 "O aceite e o piloto ficam registrados no repositório."])
    + aplicab("Use este contrato na primeira reunião com o setor.",
              "Ele separa o que é demonstração do que é uso real.",
              "Um app que passa nos testes, mas usa CPF real no seed, não está pronto.")
    + callout("err", "Não faça", "Não copie o <code>index.html</code> para editar à mão, "
      "não suba o ZIP com dados de produção e não faça commit de token, senha ou "
      "planilha com nome de servidor."))

cad.section("abertura-estado", "O estado atual dos 21 MVPs",
    p("Os 21 apps ativos estão com o MVP funcional, a identidade visual, os dados "
      "fictícios e os testes. O painel marca 160 de 160 telas. O que falta não é "
      "tela: é integração, decisão do setor, aceite e piloto.")
    + tbl(["Indicador", "Situação"], [
        ["Apps ativos", "21"],
        ["Telas planejadas", "160 de 160"],
        ["Estrutura", "21 de 21 apps OK"],
        ["Cenários de interface", "133 de 133 OK"],
        ["Feedback automatizável", "Ondas 1 a 3 concluídas"],
        ["O que falta", "Integrações, aceite, piloto e decisões do setor"],
    ])
    + callout("tip", "Como ler os pacotes", "Cada pacote tem a mesma estrutura. "
      "Comece pelo item <b>O que falta</b>. Se a sua tarefa não estiver ali, "
      "abra uma issue e combine com o professor."))

# =================================================================
# PARTE 1 · GITHUB
# =================================================================
cad.grp("Parte 1 · GitHub do zero", "Conta, repositório, ZIP, clone, branch, commit, push e Pull Request.")

cad.section("github-conta", "A conta e o convite",
    p("O GitHub é o lugar onde o projeto fica guardado e versionado. Cada app tem "
      "um repositório próprio. Para trabalhar, você precisa de uma conta e de um "
      "convite de colaborador.")
    + step(["Crie a conta em <a href=\"https://github.com\">github.com</a> com o e-mail que você usa no curso.",
            "Confirme o e-mail. Sem confirmação, o GitHub não deixa você fazer push.",
            "Envie seu login ao professor. O convite chega por e-mail e também aparece em <b>github.com/notifications</b>.",
            "Aceite o convite. O repositório passa a aparecer na sua lista.",
            "Se o convite não chegar, peça para o professor conferir a grafia do login."])
    + callout("note", "Sem convite?", "Você ainda pode baixar o ZIP e estudar. "
      "Para enviar alterações sem convite, faça um <b>fork</b> e abra um Pull Request "
      "para o repositório original.")
    + ficha("a", "Login e e-mail", p("Use o mesmo e-mail no GitHub e no computador. "
      "O Git identifica o autor do commit por <code>user.name</code> e "
      "<code>user.email</code>. Configure uma vez: <br><code>git config --global user.name \"Seu Nome\"</code><br>"
      "<code>git config --global user.email \"seu@email\"</code>")))

cad.section("github-baixar", "Baixar o projeto: ZIP ou clone",
    p("Há dois caminhos. O ZIP é mais simples para abrir e ler. O clone é o "
      "caminho certo para quem vai alterar e devolver.")
    + grid2([
        ("ZIP", p("No repositório, clique em <b>Code > Download ZIP</b>. Extraia "
                  "em uma pasta curta. O ZIP não traz o histórico do Git, então "
                  "não serve para push direto.")),
        ("Clone", p("No terminal, rode <code>git clone URL</code>. O clone traz o "
                    "histórico, a branch e a ligação com o GitHub. É o caminho "
                    "recomendado para a continuidade.")),
    ])
    + code("git clone https://github.com/renato0503/adiantamento.git\n"
           "cd adiantamento\n"
           "git status\n"
           "git branch --show-current", "powershell")
    + callout("err", "ZIP e Git", "Se você baixou o ZIP e quer enviar alterações, "
      "não rode <code>git init</code> no meio da pasta antiga. Clone o repositório "
      "em uma pasta nova e copie para lá apenas os arquivos que você alterou."))

cad.section("github-antigravity", "Abrir a pasta no Antigravity",
    p("O Antigravity trabalha com uma pasta aberta. A pasta precisa ser a raiz do "
      "app, aquela que tem o <code>app.json</code>, o <code>src</code> e o "
      "<code>construir.py</code>.")
    + step(["Abra o Antigravity.",
            "Escolha <b>File > Open Folder</b>.",
            "Selecione a pasta do app, não a pasta do curso inteiro.",
            "Confira na barra lateral se aparecem <code>README.md</code>, <code>app.json</code>, <code>src</code>, <code>nucleo</code> e <code>construir.py</code>.",
            "Abra o terminal integrado.",
            "Peça ao agente para ler os arquivos antes de alterar qualquer coisa."])
    + code("Você está no projeto <slug>. Leia README.md, PREMISSAS.md e sprint.md.\n"
           "Não edite index.html. Antes de alterar, rode python construir.py e os testes.\n"
           "Depois de alterar, mostre o diff e rode os testes de novo.", "texto")
    + callout("tip", "Pasta certa", "Se o terminal mostrar a pasta do curso, "
      "com 21 apps dentro, você abriu a pasta errada. Abra a pasta do seu app."))

cad.section("github-rodar", "Rodar o app e os testes",
    p("O app é HTML, CSS e JavaScript. Para gerar o <code>index.html</code>, o "
      "projeto usa Python. Para os testes de interface, usa Playwright.")
    + step(["Confira o Python: <code>python --version</code>. Use 3.11 ou mais novo.",
            "Rode <code>python construir.py</code> na raiz do app.",
            "Abra o <code>index.html</code> no Edge ou no Chrome.",
            "Vá em <b>Configuração</b> e clique em <b>Carregar dados fictícios</b>.",
            "Rode <code>python testes/testar.py</code>.",
            "Rode <code>python testes/cenarios.py</code>."])
    + code("python --version\npython construir.py\npython testes/testar.py\npython testes/cenarios.py", "powershell")
    + callout("note", "Playwright", "Se o teste reclamar que o Playwright não está instalado, "
      "rode <code>pip install playwright</code> e <code>playwright install chromium</code>. "
      "O app em si não precisa de internet nem de instalação."))

cad.section("github-branch", "Criar uma branch por tarefa",
    p("Nunca trabalhe direto na <code>main</code>. A branch isola a sua alteração "
      "e permite revisar antes de juntar.")
    + step(["Atualize a main: <code>git checkout main</code> e <code>git pull</code>.",
            "Crie a branch: <code>git checkout -b melhoria/nome-curto</code>.",
            "Faça uma tarefa por branch. Se misturar duas, a revisão fica difícil.",
            "Rode os testes antes de abrir o Pull Request.",
            "Envie: <code>git push origin melhoria/nome-curto</code>."])
    + code("git checkout main\ngit pull\ngit checkout -b melhoria/aviso-email\ngit status", "powershell")
    + callout("tip", "Nome da branch", "Use verbos curtos: <code>melhoria/aviso-email</code>, "
      "<code>correcao/prazo</code>, <code>integracao/sheets</code>. Evite acentos e espaços."))

cad.section("github-commit", "Fazer um commit que se entende",
    p("Um commit é uma foto do projeto com uma mensagem. A mensagem precisa dizer "
      "o que mudou e por quê, não apenas “alterações”.")
    + step(["Veja o que mudou: <code>git status</code> e <code>git diff</code>.",
            "Adicione só o que pertence à tarefa: <code>git add arquivo</code>.",
            "Escreva a mensagem no imperativo: <code>Adiciona aviso de vencimento</code>.",
            "Faça o commit: <code>git commit -m \"...\"</code>.",
            "Confira: <code>git log --oneline -3</code>."])
    + code("git status\ngit diff\ngit add src/app.js app.json\ngit commit -m \"Adiciona aviso de vencimento ao fiscal\"\ngit log --oneline -3", "powershell")
    + callout("err", "Nunca commite", "Token, senha, arquivo <code>.env</code>, "
      "planilha com nome de servidor, foto de pessoa atendida ou backup real. "
      "Se commitou por engano, avise o professor antes de fazer push."))

cad.section("github-push", "Enviar e abrir o Pull Request",
    p("O push envia a branch para o GitHub. O Pull Request pede que alguém revise "
      "e junte a branch na main.")
    + step(["Envie a branch: <code>git push origin melhoria/nome-curto</code>.",
            "Abra o repositório no navegador. O GitHub mostra o botão <b>Compare & pull request</b>.",
            "Escreva o que mudou, o que testou e o que ainda falta.",
            "Marque o professor ou um colega como revisor.",
            "Depois do aceite, clique em <b>Merge pull request</b>.",
            "Apague a branch remota depois do merge."])
    + code("git push origin melhoria/aviso-email", "powershell")
    + callout("note", "Conflito", "Se o GitHub disser que há conflito, atualize a main, "
      "faça o merge dela na sua branch, resolva o arquivo, rode os testes e envie de novo."))

cad.section("github-pages", "Publicar no GitHub Pages",
    p("O GitHub Pages serve o <code>index.html</code> como site. Para o app, ative "
      "na raiz do repositório, branch <code>main</code>.")
    + step(["Abra <b>Settings > Pages</b>.",
            "Em <b>Source</b>, escolha <b>Deploy from a branch</b>.",
            "Selecione <code>main</code> e a pasta <code>/ (root)</code>.",
            "Salve e espere de 1 a 10 minutos.",
            "Abra a URL publicada e teste o app e o link de inscrição."])
    + callout("tip", "Cache", "Se a página antiga continuar aparecendo, espere ou abra "
      "em uma janela anônima. O CDN do GitHub demora alguns minutos para atualizar."))

cad.section("github-issues", "Usar issues para não perder o fio",
    p("Issue é uma tarefa ou um erro registrado. Ela guarda o print, o passo e a "
      "decisão, e evita que a informação fique só no WhatsApp.")
    + step(["Abra <b>Issues > New issue</b>.",
            "No título, diga o app e o problema: <code>Inscrições: link não abre no Outlook</code>.",
            "No corpo, coloque o passo, o esperado, o acontecido e o print.",
            "Marque uma etiqueta: <code>bug</code>, <code>melhoria</code> ou <code>duvida</code>.",
            "Feche a issue no commit ou no Pull Request que resolveu."])
    + aplicab("Use uma issue por pendência do pacote.",
              "O pacote já lista o que falta; a issue transforma a lista em trabalho acompanhável.",
              "Se a integração com o e-mail vai levar duas semanas, a issue guarda o combinado e o responsável.")
    + callout("note", "Modelo de issue", "Título: <b>App: o que falta</b>. "
      "Corpo: <b>Passo</b>, <b>Esperado</b>, <b>Aconteceu</b>, <b>Ambiente</b> e <b>Print</b>."))

# =================================================================
# PARTE 2 · ANTIGRAVITY E ANATOMIA
# =================================================================
cad.grp("Parte 2 · Antigravity e anatomia do app", "Onde mexer, o que não mexer e como pedir ajuda ao agente.")

cad.section("app-anatomia", "A anatomia de um app",
    p("Todos os apps seguem a mesma arquitetura: um único HTML gerado, CSS e "
      "JavaScript embutidos, IndexedDB e dados fictícios. A pasta é pequena e "
      "tem sempre os mesmos arquivos.")
    + tbl(["Arquivo ou pasta", "O que é", "Você edita?"], [
        ["index.html", "App gerado, com CSS, JS e dados embutidos", "Não"],
        ["app.json", "Título, banco, perfis, rotas, libs e dados", "Sim"],
        ["src/app.js", "Telas e regras das primeiras sprints", "Sim"],
        ["src/sprintN.js", "Telas e regras das sprints seguintes", "Sim"],
        ["src/app.css", "Ajustes visuais do app", "Sim"],
        ["nucleo/", "Casca, roteador, IndexedDB, ícones e CSS comum", "Com cuidado"],
        ["exemplos/", "Gerador e seed dos dados fictícios", "Sim"],
        ["modelos/", "Modelos, roteiros e documentos de referência", "Sim"],
        ["vendor/", "Bibliotecas de terceiros, com versão e SHA", "Só ao trocar a lib"],
        ["testes/", "Testes de estrutura e cenários de interface", "Sim"],
    ])
    + callout("err", "Nunca edite o index.html", "Ele é sobrescrito pelo "
      "<code>construir.py</code>. Se você editar à mão, a alteração some no próximo build.")
    + p("O <code>construir.py</code> lê o <code>app.json</code>, junta "
        "<code>src/*.js</code> em ordem e embute as bibliotecas e os dados. O "
        "resultado é um arquivo que abre com duplo clique."))

cad.section("app-fluxo", "O fluxo de uma alteração",
    p("Toda alteração segue o mesmo caminho. Se você pular uma etapa, o erro "
      "aparece mais tarde e fica mais caro.")
    + flow_h([("1", "Entender"), ("2", "Editar"), ("3", "Construir"), ("4", "Testar"), ("5", "Revisar"), ("6", "Commitar")])
    + step(["Leia a issue e o trecho do <code>sprint.md</code>.",
            "Localize a tela e a regra em <code>src/</code>.",
            "Altere uma coisa pequena.",
            "Rode <code>python construir.py</code>.",
            "Abra o app e reproduza o caso.",
            "Rode os testes e confira o console.",
            "Faça o commit e o pull request."])
    + antesdepois("Editar o index.html e mandar o print.", "Editar a fonte, construir e rodar o teste.",
                  "Errado", "Certo")
    + callout("tip", "Uma coisa por vez", "Se você mudar a tela, a regra e o seed no "
      "mesmo commit, fica impossível saber o que causou o erro."))

cad.section("app-agente", "Como pedir ao agente do Antigravity",
    p("O agente é útil quando recebe contexto e um limite. Pedido vago gera "
      "alteração grande e difícil de revisar.")
    + grid2([("Pedido ruim", p("“Melhore o app”. O agente não sabe o que falta, "
                              "mexe em tudo e você não consegue revisar.")),
             ("Pedido bom", p("“Leia o sprint.md. Na tela #/painel, adicione o "
                              "botão Avisar. Não altere o index.html. Rode os testes e "
                              "mostre o diff.”"))])
    + code("Leia README.md, PREMISSAS.md e sprint.md.\n"
           "Não edite index.html.\n"
           "Trabalhe apenas nesta tarefa: <descreva uma tarefa>.\n"
           "Antes de alterar, rode python construir.py e os testes.\n"
           "Depois de alterar, rode os testes de novo, mostre o diff e explique o que mudou.", "texto")
    + callout("note", "Arquivos de contexto", "Sempre peça para o agente ler "
      "<code>README.md</code>, <code>PREMISSAS.md</code>, <code>sprint.md</code> e "
      "o arquivo de <code>src/</code> que será alterado."))

cad.section("app-testes", "O que cada teste verifica",
    p("O projeto tem dois níveis de teste. O primeiro confere a estrutura. O "
      "segundo usa a tela como uma pessoa usaria.")
    + tbl(["Comando", "O que verifica", "Quando rodar"], [
        ["python testes/testar.py", "Zero rede, rotas, tema, dados fictícios, #/testes", "Sempre"],
        ["python testes/cenarios.py", "Um cenário por sprint, com o “Pronto quando”", "Antes do PR"],
        ["python Apps/_base/testar.py", "Todos os apps, no repositório do curso", "Só no computador do professor"],
        ["node testes/testar_code_gs.js", "Servidor do agendamento CIN", "Só no agendamento"],
    ])
    + callout("err", "Teste que passou não é desculpa", "O teste cobre o que foi "
      "escrito. Se você mudou uma regra, acrescente ou ajuste um cenário. Teste "
      "sem cenário novo não prova a regra nova.")
    + p("Se o teste falhar, leia a primeira linha do erro. Corrija uma coisa, rode "
        "de novo. Não tente “consertar” o teste para ele passar se a regra está errada."))

cad.section("app-dados", "Dados fictícios, backup e LGPD",
    p("Os apps usam dados fictícios. O uso real exige cuidado com dado pessoal, "
      "retenção e acesso.")
    + checklist(["O seed não tem nome, CPF, foto ou endereço de pessoa real.",
                 "O backup é feito em Configuração e guardado em local controlado.",
                 "O app avisa a finalidade e o prazo de retenção.",
                 "O perfil vê só o que precisa.",
                 "A exclusão de um caso mantém apenas a contagem, quando a regra pede."])
    + callout("err", "Nunca", "Não suba planilha real, print de tela com nome, "
      "backup de produção ou token para o repositório público. Se precisar testar, "
      "use o seed ou anonimize antes.")
    + aplicab("Use o botão de backup antes de cada reunião.",
              "Se o navegador limpar os dados, o backup é a única cópia.",
              "O backup é um .json que pode ser restaurado em Configuração."))

cad.section("app-pendencias", "Onde estão as pendências",
    p("Cada app tem três lugares para consultar o que falta. Leia nessa ordem.")
    + tbl(["Arquivo", "O que traz", "Como usar"], [
        ["README.md", "Visão do projeto, time e links", "Primeiro contato"],
        ["sprint.md", "Sprints, itens feitos e abertos", "Lista de trabalho"],
        ["PREMISSAS.md", "O que foi assumido e o que confirmar", "Reunião com o setor"],
        ["modelos/roteiro-aceite.md", "Roteiro de aceite e piloto", "Antes da entrega"],
        ["Ajuda Técnica no app", "Passo a passo de integração externa", "Quando for ligar serviço"],
    ])
    + callout("tip", "Ajuda Técnica", "No rodapé do app, clique três vezes no nome "
      "do app. O painel de ajuda abre com o passo a passo do que depende de "
      "serviço externo. Ele não aparece no menu.")
    + p("Se a pendência for uma decisão do setor, leve a pergunta escrita. Se for "
        "técnica, abra uma issue com o passo e o erro."))

# =================================================================
# PARTE 3 · OS 21 MVPS
# =================================================================
cad.grp("Parte 3 · Os 21 MVPs", "Um pacote por app: o que está pronto, o que falta, como integrar e como devolver.")

cad.section("apps-visao", "Como usar os pacotes",
    p("Cada seção desta parte é um pacote. Ela traz o repositório, o que já está "
      "pronto, o que falta, o roteiro de integração, os comandos de teste e a "
      "mensagem de commit. O mesmo conteúdo está em "
      "<code>Aula 9/pacotes/&lt;slug&gt;.md</code>.")
    + callout("tip", "Comece pelo seu", "Localize o app na lista, leia o pacote e "
      "abra a issue da primeira pendência. Não tente fazer todas de uma vez.")
    + p("A ordem abaixo é a mesma do painel e do hub. Os links de repositório e de "
        "app publicado estão em cada seção."))

for a in APPS:
    cad.section(f"app-{a['slug']}", f"{a['nome']} · {a['equipe']}", html_app(a))

# =================================================================
# PARTE 4 · INTEGRAÇÕES
# =================================================================
cad.grp("Parte 4 · Receitas de integração", "E-mail, Google Sheets, OCR, Earth, QR, Firestore e aceite.")

cad.section("int-email", "E-mail e Apps Script",
    p("Quase todo app precisa avisar alguém. No MVP, a fila é local. No uso real, "
      "o envio passa por Apps Script, Gmail institucional ou SMTP.")
    + step(["Crie um projeto em <a href=\"https://script.google.com\">script.google.com</a> com a conta institucional.",
            "Cole a função abaixo e autorize.",
            "Chame a função a partir do app por uma fila local ou por um botão.",
            "Teste primeiro com o seu próprio e-mail.",
            "Registre quem recebeu, quando e qual foi a resposta."])
    + code("function enviarAviso(para, assunto, corpo) {\n"
           "  MailApp.sendEmail({to: para, subject: assunto, body: corpo});\n"
           "  return {ok: true, enviado_em: new Date().toISOString()};\n"
           "}", "javascript")
    + callout("err", "Não coloque token no app", "O Apps Script usa a permissão da "
      "conta. Não embuta senha, token ou chave no <code>index.html</code>.")
    + p("Para vaga única e concorrência, use <code>LockService.getScriptLock()</code> "
        "e grave em uma planilha. Para lembrete, crie um gatilho diário."))

cad.section("int-sheets", "Google Sheets e CSV",
    p("O Sheets é útil para uma fila compartilhada e para o setor conferir os "
      "dados sem abrir o app. O app continua offline e importa ou exporta CSV.")
    + step(["Defina a planilha e as colunas, com uma linha de exemplo.",
            "No app, exporte CSV com BOM e ponto e vírgula.",
            "No Sheets, use <b>Arquivo > Importar</b> e confira a acentuação.",
            "Para leitura, publique a aba como CSV ou use Apps Script.",
            "Nunca publique uma aba com nome, CPF ou dado de saúde."])
    + code("Unidade;Laudos pendentes\nIML Cuiabá;570\nIML Várzea Grande;511\n", "texto")
    + callout("note", "CSP", "O app não pode buscar CSV em tempo de execução se a "
      "política for <code>connect-src 'none'</code>. A sincronização precisa ser "
      "por importação manual ou por Apps Script com a permissão do setor."))

cad.section("int-ocr", "OCR e PDF",
    p("PDF com camada de texto é fácil. PDF em imagem precisa de OCR. O OCR "
      "consome memória e não é 100% confiável.")
    + step(["Tente ler o texto com pdf.js. Se vier texto, use a tabela.",
            "Se não vier, avise e permita digitar ou importar CSV.",
            "Se o OCR for inevitável, coloque em uma página separada para não pesar o app.",
            "Mostre a confiança de cada número e exija conferência humana.",
            "Nunca aprove um mês ou um laudo sem revisão."])
    + callout("err", "OCR não é verdade", "Um número lido com 80% de confiança não "
      "pode entrar na planilha sem alerta. O app deve marcar e pedir confirmação.")
    + aplicab("Use OCR só quando o setor não consegue exportar CSV ou Excel.",
              "A exportação nativa é mais rápida e mais confiável.",
              "No Metas BI, o CSV do Power BI é o caminho preferido."))

cad.section("int-earth", "Google Earth, KMZ e GeoJSON",
    p("O mapa do app é offline. Para o mapa real, exporte KMZ ou GeoJSON e abra "
      "no Google Earth, QGIS ou ArcGIS.")
    + step(["Gere o `.kmz` em Exportar.",
            "Abra no Google Earth Pro e no Web.",
            "Confira pinos, fotos, balões e cores.",
            "Se o balão não abrir, verifique o tamanho da foto e o nome do arquivo.",
            "Registre o teste no roteiro de aceite."])
    + callout("note", "Earth Engine", "O Earth Engine é para análise de imagem de "
      "satélite, não para cadastro de equipamentos. Para o cadastro, use KMZ, "
      "GeoJSON ou a Google Maps API."))

cad.section("int-qr", "QR Code e link de inscrição",
    p("O QR Code serve para o cidadão abrir o formulário sem digitar. O código "
      "precisa ser gerado offline e apontar para a URL publicada.")
    + step(["Publique o app no GitHub Pages.",
            "Gere o link de inscrição com os dados do curso.",
            "Gere o QR a partir do link e baixe o SVG.",
            "Imprima e teste com dois celulares.",
            "Se o link mudar, gere o QR de novo."])
    + callout("err", "Link local", "Um link <code>file:///C:/...</code> não funciona "
      "no celular do cidadão. Publique antes de divulgar."))

cad.section("int-firestore", "Firestore e formulário público",
    p("O formulário da Aula 8 usa Firestore no plano Spark. Os arquivos vão como "
      "documentos em base64, com limite de 600 KB por arquivo.")
    + step(["Confira as regras em <code>Aula 8/firestore.rules</code>.",
            "Ative a autenticação anônima, se o projeto exigir.",
            "Teste o envio com um projeto fictício.",
            "Confira a coleção e o documento.",
            "Nunca envie dado pessoal de caso real."])
    + callout("note", "Plano Spark", "O Cloud Storage exige o plano Blaze. Por isso "
      "os arquivos vão no Firestore. Arquivo maior vai por e-mail ou WhatsApp, com "
      "o identificador do projeto."))

cad.section("int-biometria", "Biometria e sistemas institucionais",
    p("A integração com base biométrica, Atena, SINALID, CADÊ, SINESP, RIBPG e "
      "SINAB depende de credencial e termo. O app faz a parte local e deixa o "
      "passo a passo.")
    + step(["Peça à TI o contrato da API, o dicionário de dados e o ambiente de teste.",
            "Crie uma fila local com protocolo, status e data.",
            "Nunca grave a biometria ou o dado sensível no navegador.",
            "Registre cada consulta no log, com finalidade.",
            "Teste com resposta simulada antes de ligar a produção."])
    + callout("err", "Sem credencial, não invente", "Não simule uma integração "
      "como se fosse real. O app deve dizer que a etapa está pendente e por quê."))

# =================================================================
# PARTE 5 · EQUIPE E ENTREGA
# =================================================================
cad.grp("Parte 5 · Equipe, revisão e entrega", "Trabalho em paralelo, revisão e o que apresentar.")

cad.section("equipe-papeis", "Papéis na continuidade",
    p("Um grupo pequeno precisa combinar quem faz o quê. O MVP já está pronto; "
      "agora o trabalho é de integração, teste e aceite.")
    + tbl(["Papel", "Responsabilidade", "Entrega"], [
        ["Coordenação", "Fala com o setor, prioriza e marca o aceite", "Ata e decisão"],
        ["Desenvolvimento", "Altera as fontes, constrói e testa", "Pull Request"],
        ["Dados", "Cuida do seed, da planilha e da LGPD", "Backup e dicionário"],
        ["Teste", "Roda os cenários e registra o que falhou", "Issue e print"],
        ["Documentação", "Atualiza README, sprint e PREMISSAS", "Commit de docs"],
    ])
    + callout("tip", "Uma pessoa por branch", "Se duas pessoas mexem no mesmo "
      "arquivo, combine antes. Uma branch por tarefa reduz o conflito.")
    + p("O grupo não precisa de todos os papéis em tempo integral. Precisa saber "
        "quem responde por cada um."))

cad.section("equipe-revisao", "Revisão de código em 10 minutos",
    p("A revisão não é para achar culpado. É para garantir que o app continua "
      "funcionando e que a mudança é compreensível.")
    + checklist(["O Pull Request tem uma tarefa só.",
                 "O commit não inclui dado real, token ou backup.",
                 "O <code>index.html</code> foi gerado, não editado à mão.",
                 "Os testes passam.",
                 "O cenário novo cobre a regra nova.",
                 "O README ou o sprint foi atualizado.",
                 "A mensagem de commit explica o porquê."])
    + callout("note", "Comentário útil", "Diga o que observar e por quê. "
      "“Aqui o prazo pode ficar negativo; teste o caso de hoje” ajuda mais do que "
      "“está errado”.")
    + p("Se a mudança for grande, peça para dividir em duas. Pull Request pequeno "
        "é revisado em minutos; grande fica parado."))

cad.section("equipe-aceite", "O aceite com o setor",
    p("Aceite é o momento em que o setor confirma que o app resolve o problema. "
      "Não é uma demonstração; é um roteiro com critério.")
    + step(["Marque uma reunião de 40 minutos.",
            "Abra o roteiro de aceite do app.",
            "Use dados fictícios ou anonimizados.",
            "Peça para o servidor do setor executar a tarefa, não você.",
            "Anote o que travou e o tempo.",
            "No fim, peça o aceite escrito, com data e responsável."])
    + callout("tip", "Critério de aceite", "O critério já está no <code>sprint.md</code>. "
      "Se ele não estiver claro, escreva antes da reunião: “o app está aceito quando "
      "o servidor consegue fazer X sem ajuda”."))

cad.section("equipe-piloto", "O piloto e a linha de base",
    p("O piloto mede o app no uso real, com um grupo pequeno e por tempo limitado. "
      "A linha de base é o tempo ou o erro antes do app.")
    + tbl(["Momento", "O que medir", "Como registrar"], [
        ["Antes", "Tempo, erros, retrabalho", "Planilha ou print"],
        ["Durante", "Uso, dúvidas, falhas", "Diário de bordo e issues"],
        ["Depois", "Ganho, custo, satisfação", "Relatório de 1 página"],
    ])
    + aplicab("Use o piloto para decidir, não para defender o app.",
              "Se o app não reduzir o tempo ou o erro, o piloto mostra e vocês ajustam.",
              "Três unidades ou uma turma reduzida são suficientes para começar.")
    + callout("err", "Piloto sem baseline", "Sem o “antes”, o “depois” não prova nada. "
      "Meça uma semana antes de ligar o app."))

cad.section("equipe-entrega", "O que entregar no fim",
    p("A entrega final tem quatro provas: o app, o repositório, o aceite e o "
      "relatório do piloto.")
    + checklist(["App publicado e abrindo no navegador.",
                 "Repositório com README, PREMISSAS, sprint e modelos atualizados.",
                 "Pull Requests revisados e mergeados.",
                 "Roteiro de aceite assinado ou registrado.",
                 "Relatório do piloto com a linha de base.",
                 "Backup dos dados fictícios e dicionário de dados.",
                 "Apresentação de 5 minutos com problema, solução, número e próximo passo."])
    + p("A apresentação não precisa mostrar código. Precisa mostrar o problema, "
        "o antes, o depois e o que o setor ganhou.")
    + callout("tip", "5 minutos", "Um slide de problema, um de solução, um de "
      "número, um de próximos passos e um de equipe. O resto é conversa."))

# =================================================================
# PARTE 6 · FECHAMENTO
# =================================================================
cad.grp("Parte 6 · Fechamento", "Checklist, erros comuns, quiz, glossário e referências.")

cad.section("fechamento-checklist", "Checklist final do curso",
    p("Use esta lista na véspera da entrega. Se algum item falhar, resolva antes "
      "de apresentar.")
    + checklist(["O app abre com duplo clique e não pede internet.",
                 "O seed carrega e o botão de backup funciona.",
                 "O teste de estrutura passa.",
                 "O cenário da última tarefa passa.",
                 "O repositório está atualizado e a branch main está limpa.",
                 "O GitHub Pages abre a URL publicada.",
                 "O README diz o que o app faz e como rodar.",
                 "O sprint.md está marcado até onde chegou.",
                 "As premissas estão registradas, não escondidas.",
                 "O aceite e o piloto têm data e responsável."])
    + callout("note", "Se algo não estiver pronto", "Diga o que falta. Um MVP "
      "honesto com pendência registrada vale mais do que uma demo que quebra."))

cad.section("fechamento-erros", "Os erros que mais aparecem",
    p("Estes erros já apareceram no curso. Reconheça e evite.")
    + tbl(["Erro", "Sintoma", "Correção"], [
        ["Editar o index.html", "A alteração some no build", "Editar a fonte e rodar construir.py"],
        ["Misturar dado real", "Nome ou CPF no seed", "Anonimizar e refazer o seed"],
        ["Não rodar o build", "A tela nova não aparece", "Rodar construir.py"],
        ["Commit gigante", "Revisão impossível", "Dividir por tarefa"],
        ["Teste ajustado para passar", "A regra continua errada", "Corrigir a regra e o cenário"],
        ["Link local no QR", "Não abre no celular", "Publicar no Pages"],
        ["Token no código", "Vazamento", "Remover do histórico e avisar"],
        ["Sem backup", "Dados perdidos", "Exportar .json antes da reunião"],
    ])
    + callout("err", "O erro mais caro", "É acreditar que o teste cobre tudo. "
      "Teste cobre o que foi escrito. O aceite com o setor cobre o resto."))

cad.section("fechamento-quiz", "Quiz final",
    q("Qual arquivo você edita para mudar uma tela?", [
        "index.html", "src/app.js ou src/sprintN.js", "app.json apenas", "O PDF"], 1,
      "O index.html é gerado. A tela está em src/.")
    + q("Qual comando gera o index.html?", [
        "python testes/testar.py", "python construir.py", "git push", "python validar.py"], 1)
    + q("O que fazer antes de abrir um Pull Request?", [
        "Rodar os testes e revisar o diff", "Apagar a branch main", "Subir o backup real",
        "Editar o index.html"], 0)
    + q("Onde fica o passo a passo de integração externa?", [
        "No README apenas", "Na Ajuda Técnica, três cliques no nome do app",
        "No index.html", "No arquivo .pbix"], 1)
    + q("O que é a linha de base?", [
        "O tempo ou o erro antes do app", "O nome do repositório", "O backup do banco",
        "A branch principal"], 0)
    + q("Qual é o caminho correto para uma alteração?", [
        "main, editar, push", "branch, editar, construir, testar, commit, push, PR",
        "ZIP, editar, e-mail", "index.html, print, WhatsApp"], 1)
    + q("O que nunca pode entrar no repositório?", [
        "README", "Dados fictícios", "Token, senha e dado pessoal real", "Sprint.md"], 2)
    + q("O que o aceite precisa ter?", [
        "Um print bonito", "Critério, data e responsável", "Só a opinião do professor",
        "O código inteiro"], 1))

cad.section("fechamento-glossario", "Glossário",
    glossary([
        ("MVP", "Menor versão do produto que resolve o problema principal e pode ser testada."),
        ("Repositório", "Pasta versionada no GitHub, com histórico de commits."),
        ("Branch", "Linha paralela de trabalho, usada para isolar uma alteração."),
        ("Commit", "Registro de uma alteração, com autor, data e mensagem."),
        ("Pull Request", "Pedido para juntar uma branch na main, com revisão."),
        ("Issue", "Tarefa, erro ou dúvida registrada no GitHub."),
        ("Build", "Processo que gera o index.html a partir das fontes."),
        ("Seed", "Dados fictícios com semente fixa, usados nos testes e na demo."),
        ("IndexedDB", "Banco do navegador onde o app guarda os dados locais."),
        ("Offline first", "O app funciona sem internet e não faz requisição de rede."),
        ("Aceite", "Confirmação do setor de que o app atende ao critério combinado."),
        ("Piloto", "Uso real, limitado e medido, antes da implantação."),
        ("Linha de base", "Medida do processo antes do app, para comparar depois."),
        ("LGPD", "Lei de proteção de dados: finalidade, acesso, retenção e segurança."),
    ]))

cad.section("fechamento-referencias", "Referências e próximos passos",
    p("O material do curso continua no repositório. Os links principais estão "
      "abaixo.")
    + ul(["<a href=\"https://github.com/renato0503/Aula_politec\">Repositório do curso</a>",
          "<a href=\"https://renato0503.github.io/Aula_politec/\">Site do curso</a>",
          "<a href=\"https://renato0503.github.io/Aula_politec/Apps/index.html\">Hub dos 21 apps</a>",
          "<a href=\"https://github.com/renato0503/Aula_politec/blob/main/Apps/CONTINUAR.md\">CONTINUAR.md</a>",
          "<a href=\"https://github.com/renato0503/Aula_politec/blob/main/Apps/PREMISSAS.md\">PREMISSAS.md</a>",
          "<a href=\"https://docs.github.com/pt\">Documentação do GitHub</a>",
          "<a href=\"https://www.antigravity.google/\">Antigravity</a>"])
    + callout("tip", "Próximo passo", "Escolha uma pendência do seu pacote, abra uma "
      "issue, crie a branch e faça o primeiro Pull Request. A continuidade começa "
      "com uma alteração pequena e testada.")
    + p("Bom trabalho. O app já funciona; agora ele ganha o uso real, com o setor, "
        "com número e com responsabilidade."))

# =================================================================
# PACOTES INDIVIDUAIS
# =================================================================
for a in APPS:
    (PASTA / "pacotes" / f"{a['slug']}.md").write_text(md_app(a), encoding="utf-8")

indice = ["# Pacotes de continuidade · Aula 9", "",
          "Um arquivo por app. Cada pacote tem o repositório, o que falta, o passo a passo de integração, os testes e o commit sugerido.", "",
          "| App | Equipe | Repositório | Pacote |", "|---|---|---|---|"]
for a in APPS:
    indice.append(f"| {a['nome']} | {a['equipe']} | {repo(a)} | [{a['slug']}.md]({a['slug']}.md) |")
(PASTA / "pacotes" / "README.md").write_text("\n".join(indice) + "\n", encoding="utf-8")

cad.build()
print(f"Pacotes: {len(APPS)} arquivos em {PASTA / 'pacotes'}")
