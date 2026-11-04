# Pacote de continuidade · Controle de Adiantamentos

**Equipe:** Jaqueline e Linicker  
**Tipo:** Aplicativo para servidor  
**Repositório:** https://github.com/renato0503/adiantamento  
**App publicado:** https://renato0503.github.io/Aula_politec/Apps/adiantamento/index.html  
**ZIP:** https://github.com/renato0503/adiantamento/archive/refs/heads/main.zip

## 1. O que este app faz

Pedido de suprimento de fundos, três orçamentos, 12 etapas, urgência e recurso.

## 2. O que já está pronto

- Pedido com três orçamentos e CNPJ conferido
- Linha do tempo de 12 etapas, com devolução motivada
- Afastamento, urgência e recurso de 24 h
- Painel, checklist e dados fictícios

## 3. O que falta

- Validar as 12 etapas com a DAS e a contabilidade da SESP
- Confirmar a Orientação Técnica da CGE e os feriados
- Definir a origem dos afastamentos e a integração com o SICAD

## 4. Baixar e abrir no Antigravity

1. Abra https://github.com/renato0503/adiantamento e aceite o convite de colaborador.
2. Baixe o ZIP em https://github.com/renato0503/adiantamento/archive/refs/heads/main.zip ou clone com `git clone https://github.com/renato0503/adiantamento.git`.
3. Extraia em `C:\POLITEC\adiantamento`.
4. No Antigravity, use **File > Open Folder** e escolha a pasta que tem `app.json`, `src`, `nucleo` e `construir.py`.
5. Abra o terminal e confira `python --version`.
6. Rode `python construir.py`.
7. Abra `index.html` no Edge ou no Chrome e clique em **Configuração > Carregar dados fictícios**.

## 5. Integração que falta, passo a passo

### Afastamentos

1. Combine com o RH se a lista vem do SIGRH, de planilha ou de exportação manual.
2. Crie um importador de CSV em `#/config` e grave na loja `afastamentos`.
3. No pedido, bloqueie o servidor afastado e mostre a data de retorno.
4. Teste com um afastamento fictício e confira o bloqueio.

### Aprovação e SICAD

1. Defina o canal de aprovação, e-mail ou fila local.
2. Registre o número SICAD no fechamento da etapa.
3. Inclua o número no CSV e na ficha do pedido.
4. Valide o fluxo com um pedido de teste, sem dado real.

## 6. Como testar

```powershell
python construir.py
python testes/testar.py
python testes/cenarios.py
#/pedido/novo e #/pedido/:id
```

Se o teste falhar, leia a primeira mensagem, corrija uma coisa por vez e rode de novo.

## 7. Enviar para o GitHub

1. Entre em https://github.com/renato0503/adiantamento e aceite o convite de colaborador. Se ainda não recebeu, peça ao professor para enviar de novo.
2. Clique em **Code > Download ZIP** ou clone: `git clone https://github.com/renato0503/adiantamento.git`. O ZIP serve para abrir e estudar; para enviar alterações, use o clone ou um fork.
3. Extraia em uma pasta curta, por exemplo `C:\POLITEC\adiantamento`. Evite OneDrive e caminhos com muitos espaços.
4. Abra o **Antigravity**, escolha **File > Open Folder** e selecione a pasta que contém `app.json`, `src`, `nucleo`, `construir.py` e `testes`.
5. No terminal do Antigravity, rode `git checkout -b melhoria/adiantamento` para criar uma branch de trabalho.
6. Leia `README.md`, `PREMISSAS.md` e `sprint.md`. Não edite `index.html`: ele é gerado pelo `construir.py`.
7. Edite as fontes, rode `python construir.py`, abra o `index.html` e rode os testes do app.
8. Faça `git add .`, `git commit -m "..."`, `git push origin melhoria/<tema>` e abra um Pull Request no GitHub. Peça revisão antes do merge.

## 8. Prompt para o Antigravity

```text
Você está no projeto Controle de Adiantamentos (adiantamento). Leia README.md, PREMISSAS.md e sprint.md.
Não edite index.html. Trabalhe apenas em: Validar as 12 etapas com a DAS e a contabilidade da SESP.
Antes de alterar, rode python construir.py e os testes. Depois de alterar, explique o que mudou,
rode os testes de novo e mostre o diff. Não use dados reais nem peça token.
```

**Commit sugerido:** `Adiantamento: integra afastamentos e SICAD`

## 9. Onde pedir ajuda

- Leia `PREMISSAS.md` para saber o que ainda é decisão do setor.
- Leia `sprint.md` para ver o que já foi feito e o que está aberto.
- Abra uma issue no repositório com o print, o passo e a mensagem de erro.
