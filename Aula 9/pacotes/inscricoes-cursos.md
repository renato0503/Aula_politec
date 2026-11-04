# Pacote de continuidade · Inscrições em Cursos

**Equipe:** Edilaura Rondon  
**Tipo:** Aplicativo para servidor  
**Repositório:** https://github.com/renato0503/inscricoes-cursos  
**App publicado:** https://renato0503.github.io/Aula_politec/Apps/inscricoes-cursos/index.html  
**ZIP:** https://github.com/renato0503/inscricoes-cursos/archive/refs/heads/main.zip

## 1. O que este app faz

Curso, link e QR, formulário, importação de e-mails, triagem, convocação e turma.

## 2. O que já está pronto

- Curso, vagas, link e QR Code
- Formulário e comprovante
- Importação de e-mails e triagem pelas diretorias
- Convocação, desistência e reserva
- Perfis, instrutores, monitores e termo

## 3. O que falta

- Testar o formulário no Outlook desktop, Web e celular
- Decidir se o CPF sai do formulário
- Ativar a resposta automática da caixa `capacitacao@`
- Publicar no GitHub Pages e abrir o piloto

## 4. Baixar e abrir no Antigravity

1. Abra https://github.com/renato0503/inscricoes-cursos e aceite o convite de colaborador.
2. Baixe o ZIP em https://github.com/renato0503/inscricoes-cursos/archive/refs/heads/main.zip ou clone com `git clone https://github.com/renato0503/inscricoes-cursos.git`.
3. Extraia em `C:\POLITEC\inscricoes-cursos`.
4. No Antigravity, use **File > Open Folder** e escolha a pasta que tem `app.json`, `src`, `nucleo` e `construir.py`.
5. Abra o terminal e confira `python --version`.
6. Rode `python construir.py`.
7. Abra `index.html` no Edge ou no Chrome e clique em **Configuração > Carregar dados fictícios**.

## 5. Integração que falta, passo a passo

### Outlook e celular

1. Envie o link para você mesmo em três clientes.
2. Confira o formulário, o comprovante e o bloco de e-mail.
3. Corrija o que quebrar e registre a versão testada.
4. Peça o aceite da Edilaura.

### Publicação

1. Ative o GitHub Pages no repositório, branch `main`, pasta raiz.
2. Abra a URL publicada e confira o link de inscrição.
3. Teste uma inscrição fictícia de ponta a ponta.
4. Não divulgue antes do aceite.

## 6. Como testar

```powershell
python construir.py
python testes/testar.py
python testes/cenarios.py
#/divulgar/:curso e #/inscricao
```

Se o teste falhar, leia a primeira mensagem, corrija uma coisa por vez e rode de novo.

## 7. Enviar para o GitHub

1. Entre em https://github.com/renato0503/inscricoes-cursos e aceite o convite de colaborador. Se ainda não recebeu, peça ao professor para enviar de novo.
2. Clique em **Code > Download ZIP** ou clone: `git clone https://github.com/renato0503/inscricoes-cursos.git`. O ZIP serve para abrir e estudar; para enviar alterações, use o clone ou um fork.
3. Extraia em uma pasta curta, por exemplo `C:\POLITEC\inscricoes-cursos`. Evite OneDrive e caminhos com muitos espaços.
4. Abra o **Antigravity**, escolha **File > Open Folder** e selecione a pasta que contém `app.json`, `src`, `nucleo`, `construir.py` e `testes`.
5. No terminal do Antigravity, rode `git checkout -b melhoria/inscricoes-cursos` para criar uma branch de trabalho.
6. Leia `README.md`, `PREMISSAS.md` e `sprint.md`. Não edite `index.html`: ele é gerado pelo `construir.py`.
7. Edite as fontes, rode `python construir.py`, abra o `index.html` e rode os testes do app.
8. Faça `git add .`, `git commit -m "..."`, `git push origin melhoria/<tema>` e abra um Pull Request no GitHub. Peça revisão antes do merge.

## 8. Prompt para o Antigravity

```text
Você está no projeto Inscrições em Cursos (inscricoes-cursos). Leia README.md, PREMISSAS.md e sprint.md.
Não edite index.html. Trabalhe apenas em: Testar o formulário no Outlook desktop, Web e celular.
Antes de alterar, rode python construir.py e os testes. Depois de alterar, explique o que mudou,
rode os testes de novo e mostre o diff. Não use dados reais nem peça token.
```

**Commit sugerido:** `Inscrições: publica e testa no Outlook`

## 9. Onde pedir ajuda

- Leia `PREMISSAS.md` para saber o que ainda é decisão do setor.
- Leia `sprint.md` para ver o que já foi feito e o que está aberto.
- Abra uma issue no repositório com o print, o passo e a mensagem de erro.
