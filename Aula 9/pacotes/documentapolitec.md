# Pacote de continuidade · DOCUMENTAPOLITEC

**Equipe:** Aline Xavier  
**Tipo:** Aplicativo para servidor  
**Repositório:** https://github.com/renato0503/documentapolitec  
**App publicado:** https://renato0503.github.io/Aula_politec/Apps/documentapolitec/index.html  
**ZIP:** https://github.com/renato0503/documentapolitec/archive/refs/heads/main.zip

## 1. O que este app faz

Controle de prontuários civis enviados ao arquivo central, com caixas, lacres e conferência.

## 2. O que já está pronto

- Caixa com relação e lacre
- Importação da planilha de 850 prontuários com associação de colunas
- Comparação com o índice digital
- Relatório de aceitas, recusadas e divergentes

## 3. O que falta

- Receber a planilha real de 850 prontuários
- Receber uma amostra do PDF digitalizado
- Confirmar o formato do prontuário e o modelo das caixas
- Implementar o QR Code se o setor mantiver o pedido

## 4. Baixar e abrir no Antigravity

1. Abra https://github.com/renato0503/documentapolitec e aceite o convite de colaborador.
2. Baixe o ZIP em https://github.com/renato0503/documentapolitec/archive/refs/heads/main.zip ou clone com `git clone https://github.com/renato0503/documentapolitec.git`.
3. Extraia em `C:\POLITEC\documentapolitec`.
4. No Antigravity, use **File > Open Folder** e escolha a pasta que tem `app.json`, `src`, `nucleo` e `construir.py`.
5. Abra o terminal e confira `python --version`.
6. Rode `python construir.py`.
7. Abra `index.html` no Edge ou no Chrome e clique em **Configuração > Carregar dados fictícios**.

## 5. Integração que falta, passo a passo

### Planilha e PDF

1. Coloque a planilha real em `exemplos/` ou importe em `#/importar`.
2. Confira o mapeamento das colunas e o relatório.
3. Teste uma amostra do PDF digitalizado, sem dado pessoal.
4. Ajuste as regras de aceite e recusa.

### QR Code

1. Decida se o QR Code será impresso na caixa ou no prontuário.
2. Gere o código offline com uma biblioteca embutida em `vendor/`.
3. Inclua o código no PDF de conferência.
4. Teste a leitura com um celular.

## 6. Como testar

```powershell
python construir.py
python testes/testar.py
python testes/cenarios.py
#/importar e #/relatorio-importacao
```

Se o teste falhar, leia a primeira mensagem, corrija uma coisa por vez e rode de novo.

## 7. Enviar para o GitHub

1. Entre em https://github.com/renato0503/documentapolitec e aceite o convite de colaborador. Se ainda não recebeu, peça ao professor para enviar de novo.
2. Clique em **Code > Download ZIP** ou clone: `git clone https://github.com/renato0503/documentapolitec.git`. O ZIP serve para abrir e estudar; para enviar alterações, use o clone ou um fork.
3. Extraia em uma pasta curta, por exemplo `C:\POLITEC\documentapolitec`. Evite OneDrive e caminhos com muitos espaços.
4. Abra o **Antigravity**, escolha **File > Open Folder** e selecione a pasta que contém `app.json`, `src`, `nucleo`, `construir.py` e `testes`.
5. No terminal do Antigravity, rode `git checkout -b melhoria/documentapolitec` para criar uma branch de trabalho.
6. Leia `README.md`, `PREMISSAS.md` e `sprint.md`. Não edite `index.html`: ele é gerado pelo `construir.py`.
7. Edite as fontes, rode `python construir.py`, abra o `index.html` e rode os testes do app.
8. Faça `git add .`, `git commit -m "..."`, `git push origin melhoria/<tema>` e abra um Pull Request no GitHub. Peça revisão antes do merge.

## 8. Prompt para o Antigravity

```text
Você está no projeto DOCUMENTAPOLITEC (documentapolitec). Leia README.md, PREMISSAS.md e sprint.md.
Não edite index.html. Trabalhe apenas em: Receber a planilha real de 850 prontuários.
Antes de alterar, rode python construir.py e os testes. Depois de alterar, explique o que mudou,
rode os testes de novo e mostre o diff. Não use dados reais nem peça token.
```

**Commit sugerido:** `DOCUMENTAPOLITEC: valida planilha e QR Code`

## 9. Onde pedir ajuda

- Leia `PREMISSAS.md` para saber o que ainda é decisão do setor.
- Leia `sprint.md` para ver o que já foi feito e o que está aberto.
- Abra uma issue no repositório com o print, o passo e a mensagem de erro.
