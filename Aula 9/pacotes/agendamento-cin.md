# Pacote de continuidade · Agendamento CIN

**Equipe:** Elthon  
**Tipo:** Aplicativo web e Apps Script  
**Repositório:** https://github.com/renato0503/agendamento-cin  
**App publicado:** https://renato0503.github.io/Aula_politec/Apps/agendamento-cin/index.html  
**ZIP:** https://github.com/renato0503/agendamento-cin/archive/refs/heads/main.zip

## 1. O que este app faz

Agenda pública dos postos de identificação civil, com vaga única e protocolo.

## 2. O que já está pronto

- Grade de horários e cadastro de postos
- Agendamento do cidadão com protocolo
- Painel do posto e comprovante
- Versão de demonstração offline

## 3. O que falta

- Publicar a agenda no Google Apps Script com a conta institucional
- Ligar `LockService`, `MailApp` e gatilho de lembrete
- Definir os postos do piloto, a grade real e as regras RN06 a RN10

## 4. Baixar e abrir no Antigravity

1. Abra https://github.com/renato0503/agendamento-cin e aceite o convite de colaborador.
2. Baixe o ZIP em https://github.com/renato0503/agendamento-cin/archive/refs/heads/main.zip ou clone com `git clone https://github.com/renato0503/agendamento-cin.git`.
3. Extraia em `C:\POLITEC\agendamento-cin`.
4. No Antigravity, use **File > Open Folder** e escolha a pasta que tem `app.json`, `src`, `nucleo` e `construir.py`.
5. Abra o terminal e confira `python --version`.
6. Rode `python construir.py`.
7. Abra `index.html` no Edge ou no Chrome e clique em **Configuração > Carregar dados fictícios**.

## 5. Integração que falta, passo a passo

### Publicar o Apps Script

1. Crie um projeto novo em script.google.com com a conta institucional.
2. Copie `Code.gs` e `index.html` do repositório para o projeto.
3. Em Implantar, escolha Aplicativo da Web, executar como você e acesso para qualquer pessoa com o link.
4. Autorize as permissões e copie a URL publicada.

### Vaga única e e-mail

1. Use `LockService.getScriptLock()` em volta da gravação da reserva.
2. Grave cada vaga em uma linha da planilha, com chave posto, dia e hora.
3. Envie o comprovante com `MailApp.sendEmail`.
4. Crie um gatilho diário para lembrar o cidadão.

### Teste com dois navegadores

1. Abra a agenda em duas janelas e tente reservar o mesmo horário.
2. Confirme que a segunda reserva recebe mensagem de vaga ocupada.
3. Confira o protocolo e o e-mail de teste.
4. Registre o resultado em `modelos/roteiro-aceite.md`.

## 6. Como testar

```powershell
node testes/testar_code_gs.js
python testes/testar.py
publique e abra a URL do Apps Script
```

Se o teste falhar, leia a primeira mensagem, corrija uma coisa por vez e rode de novo.

## 7. Enviar para o GitHub

1. Entre em https://github.com/renato0503/agendamento-cin e aceite o convite de colaborador. Se ainda não recebeu, peça ao professor para enviar de novo.
2. Clique em **Code > Download ZIP** ou clone: `git clone https://github.com/renato0503/agendamento-cin.git`. O ZIP serve para abrir e estudar; para enviar alterações, use o clone ou um fork.
3. Extraia em uma pasta curta, por exemplo `C:\POLITEC\agendamento-cin`. Evite OneDrive e caminhos com muitos espaços.
4. Abra o **Antigravity**, escolha **File > Open Folder** e selecione a pasta que contém `app.json`, `src`, `nucleo`, `construir.py` e `testes`.
5. No terminal do Antigravity, rode `git checkout -b melhoria/agendamento-cin` para criar uma branch de trabalho.
6. Leia `README.md`, `PREMISSAS.md` e `sprint.md`. Não edite `index.html`: ele é gerado pelo `construir.py`.
7. Edite as fontes, rode `python construir.py`, abra o `index.html` e rode os testes do app.
8. Faça `git add .`, `git commit -m "..."`, `git push origin melhoria/<tema>` e abra um Pull Request no GitHub. Peça revisão antes do merge.

## 8. Prompt para o Antigravity

```text
Você está no projeto Agendamento CIN (agendamento-cin). Leia README.md, PREMISSAS.md e sprint.md.
Não edite index.html. Trabalhe apenas em: Publicar a agenda no Google Apps Script com a conta institucional.
Antes de alterar, rode python construir.py e os testes. Depois de alterar, explique o que mudou,
rode os testes de novo e mostre o diff. Não use dados reais nem peça token.
```

**Commit sugerido:** `Agendamento CIN: publica a agenda no Apps Script`

## 9. Onde pedir ajuda

- Leia `PREMISSAS.md` para saber o que ainda é decisão do setor.
- Leia `sprint.md` para ver o que já foi feito e o que está aberto.
- Abra uma issue no repositório com o print, o passo e a mensagem de erro.
