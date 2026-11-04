# Pacote de continuidade · TCIN · Trilha de Custódia

**Equipe:** Silmara Bueno  
**Tipo:** Aplicativo para servidor  
**Repositório:** https://github.com/renato0503/trilha-custodia-necropsia  
**App publicado:** https://renato0503.github.io/Aula_politec/Apps/trilha-custodia-necropsia/index.html  
**ZIP:** https://github.com/renato0503/trilha-custodia-necropsia/archive/refs/heads/main.zip

## 1. O que este app faz

Trilha de custódia e identificação de necropsia, com sete etapas, perfis e assinatura.

## 2. O que já está pronto

- Sete etapas e três perfis
- Assinatura no canvas e sepultamento
- Recebimento de lacre e laudo
- Auditoria e resumo

## 3. O que falta

- Confirmar o nome CNC ou TCIN
- Validar os quatro marcos e os livros substituídos
- Medir a linha de base e alinhar com o IML
- Fazer o aceite e o piloto

## 4. Baixar e abrir no Antigravity

1. Abra https://github.com/renato0503/trilha-custodia-necropsia e aceite o convite de colaborador.
2. Baixe o ZIP em https://github.com/renato0503/trilha-custodia-necropsia/archive/refs/heads/main.zip ou clone com `git clone https://github.com/renato0503/trilha-custodia-necropsia.git`.
3. Extraia em `C:\POLITEC\trilha-custodia-necropsia`.
4. No Antigravity, use **File > Open Folder** e escolha a pasta que tem `app.json`, `src`, `nucleo` e `construir.py`.
5. Abra o terminal e confira `python --version`.
6. Rode `python construir.py`.
7. Abra `index.html` no Edge ou no Chrome e clique em **Configuração > Carregar dados fictícios**.

## 5. Integração que falta, passo a passo

### Marcos e livros

1. Reúna os quatro livros e os marcos com o IML.
2. Ajuste os campos e as etapas no `app.json`.
3. Teste um caso fictício do acolhimento à liberação.
4. Registre as diferenças.

### Aceite

1. Rode o roteiro com a Silmara e o IML.
2. Confira as permissões dos três perfis.
3. Teste a assinatura e o recebimento.
4. Abra o piloto de 90 dias.

## 6. Como testar

```powershell
python construir.py
python testes/testar.py
python testes/cenarios.py
#/painel e #/caso/:id
```

Se o teste falhar, leia a primeira mensagem, corrija uma coisa por vez e rode de novo.

## 7. Enviar para o GitHub

1. Entre em https://github.com/renato0503/trilha-custodia-necropsia e aceite o convite de colaborador. Se ainda não recebeu, peça ao professor para enviar de novo.
2. Clique em **Code > Download ZIP** ou clone: `git clone https://github.com/renato0503/trilha-custodia-necropsia.git`. O ZIP serve para abrir e estudar; para enviar alterações, use o clone ou um fork.
3. Extraia em uma pasta curta, por exemplo `C:\POLITEC\trilha-custodia-necropsia`. Evite OneDrive e caminhos com muitos espaços.
4. Abra o **Antigravity**, escolha **File > Open Folder** e selecione a pasta que contém `app.json`, `src`, `nucleo`, `construir.py` e `testes`.
5. No terminal do Antigravity, rode `git checkout -b melhoria/trilha-custodia-necropsia` para criar uma branch de trabalho.
6. Leia `README.md`, `PREMISSAS.md` e `sprint.md`. Não edite `index.html`: ele é gerado pelo `construir.py`.
7. Edite as fontes, rode `python construir.py`, abra o `index.html` e rode os testes do app.
8. Faça `git add .`, `git commit -m "..."`, `git push origin melhoria/<tema>` e abra um Pull Request no GitHub. Peça revisão antes do merge.

## 8. Prompt para o Antigravity

```text
Você está no projeto TCIN · Trilha de Custódia (trilha-custodia-necropsia). Leia README.md, PREMISSAS.md e sprint.md.
Não edite index.html. Trabalhe apenas em: Confirmar o nome CNC ou TCIN.
Antes de alterar, rode python construir.py e os testes. Depois de alterar, explique o que mudou,
rode os testes de novo e mostre o diff. Não use dados reais nem peça token.
```

**Commit sugerido:** `TCIN: valida marcos e aceite com o IML`

## 9. Onde pedir ajuda

- Leia `PREMISSAS.md` para saber o que ainda é decisão do setor.
- Leia `sprint.md` para ver o que já foi feito e o que está aberto.
- Abra uma issue no repositório com o print, o passo e a mensagem de erro.
