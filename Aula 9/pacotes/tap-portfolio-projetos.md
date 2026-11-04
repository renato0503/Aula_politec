# Pacote de continuidade · TAP Digital

**Equipe:** Danielle, Cristiane e Luciana  
**Tipo:** Formulário e portfólio  
**Repositório:** https://github.com/renato0503/tap-portfolio-projetos  
**App publicado:** https://renato0503.github.io/Aula_politec/Apps/tap-portfolio-projetos/index.html  
**ZIP:** https://github.com/renato0503/tap-portfolio-projetos/archive/refs/heads/main.zip

## 1. O que este app faz

TAP guiado, triagem, parecer, decisão, portfólio e dashboard orçamentário.

## 2. O que já está pronto

- TAP guiado com checklist e pacote
- Triagem, pendência e devolução
- Parecer, decisão e portfólio
- Dashboard, objetivos editáveis e avisos

## 3. O que falta

- Confirmar os objetivos estratégicos oficiais
- Ligar o envio real dos avisos
- Validar o prazo de 5 dias e testar com a Danielle
- Ajustar a matriz do portfólio (P2)

## 4. Baixar e abrir no Antigravity

1. Abra https://github.com/renato0503/tap-portfolio-projetos e aceite o convite de colaborador.
2. Baixe o ZIP em https://github.com/renato0503/tap-portfolio-projetos/archive/refs/heads/main.zip ou clone com `git clone https://github.com/renato0503/tap-portfolio-projetos.git`.
3. Extraia em `C:\POLITEC\tap-portfolio-projetos`.
4. No Antigravity, use **File > Open Folder** e escolha a pasta que tem `app.json`, `src`, `nucleo` e `construir.py`.
5. Abra o terminal e confira `python --version`.
6. Rode `python construir.py`.
7. Abra `index.html` no Edge ou no Chrome e clique em **Configuração > Carregar dados fictícios**.

## 5. Integração que falta, passo a passo

### Objetivos e avisos

1. Cole a lista oficial em `#/config`.
2. Teste um TAP novo e confira as opções.
3. Crie uma pendência e confira a fila de avisos.
4. Para e-mail real, use Apps Script ou o canal institucional.

### Fluxo e aceite

1. Crie um TAP de teste com anexos fictícios.
2. Devolva com pendência, sane e reenvie.
3. Parecer, decisão e portfólio.
4. Peça o aceite da Danielle.

## 6. Como testar

```powershell
python construir.py
python testes/testar.py
python testes/cenarios.py
#/tap/novo, #/triagem e #/portfolio
```

Se o teste falhar, leia a primeira mensagem, corrija uma coisa por vez e rode de novo.

## 7. Enviar para o GitHub

1. Entre em https://github.com/renato0503/tap-portfolio-projetos e aceite o convite de colaborador. Se ainda não recebeu, peça ao professor para enviar de novo.
2. Clique em **Code > Download ZIP** ou clone: `git clone https://github.com/renato0503/tap-portfolio-projetos.git`. O ZIP serve para abrir e estudar; para enviar alterações, use o clone ou um fork.
3. Extraia em uma pasta curta, por exemplo `C:\POLITEC\tap-portfolio-projetos`. Evite OneDrive e caminhos com muitos espaços.
4. Abra o **Antigravity**, escolha **File > Open Folder** e selecione a pasta que contém `app.json`, `src`, `nucleo`, `construir.py` e `testes`.
5. No terminal do Antigravity, rode `git checkout -b melhoria/tap-portfolio-projetos` para criar uma branch de trabalho.
6. Leia `README.md`, `PREMISSAS.md` e `sprint.md`. Não edite `index.html`: ele é gerado pelo `construir.py`.
7. Edite as fontes, rode `python construir.py`, abra o `index.html` e rode os testes do app.
8. Faça `git add .`, `git commit -m "..."`, `git push origin melhoria/<tema>` e abra um Pull Request no GitHub. Peça revisão antes do merge.

## 8. Prompt para o Antigravity

```text
Você está no projeto TAP Digital (tap-portfolio-projetos). Leia README.md, PREMISSAS.md e sprint.md.
Não edite index.html. Trabalhe apenas em: Confirmar os objetivos estratégicos oficiais.
Antes de alterar, rode python construir.py e os testes. Depois de alterar, explique o que mudou,
rode os testes de novo e mostre o diff. Não use dados reais nem peça token.
```

**Commit sugerido:** `TAP: objetivos e avisos validados com o setor`

## 9. Onde pedir ajuda

- Leia `PREMISSAS.md` para saber o que ainda é decisão do setor.
- Leia `sprint.md` para ver o que já foi feito e o que está aberto.
- Abra uma issue no repositório com o print, o passo e a mensagem de erro.
