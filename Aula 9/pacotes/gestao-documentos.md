# Pacote de continuidade · Gestão de Documentos

**Equipe:** Vitória Araújo  
**Tipo:** Aplicativo para servidor  
**Repositório:** https://github.com/renato0503/gestao-documentos  
**App publicado:** https://renato0503.github.io/Aula_politec/Apps/gestao-documentos/index.html  
**ZIP:** https://github.com/renato0503/gestao-documentos/archive/refs/heads/main.zip

## 1. O que este app faz

Processos e prazos do Gabinete de Direção, com minutas, ofícios e checklist.

## 2. O que já está pronto

- Autuação com anexos e número AAAA.NNNN-SD
- Sinal de prazo e cobrança em 70% e no vencimento
- Minutas, ofício e despacho
- Checklist por etapa e anexo opcional

## 3. O que falta

- Validar a matriz de papéis e quem pode excluir
- Definir os anexos obrigatórios por tipo
- Ligar o canal de cobrança e medir a linha de base

## 4. Baixar e abrir no Antigravity

1. Abra https://github.com/renato0503/gestao-documentos e aceite o convite de colaborador.
2. Baixe o ZIP em https://github.com/renato0503/gestao-documentos/archive/refs/heads/main.zip ou clone com `git clone https://github.com/renato0503/gestao-documentos.git`.
3. Extraia em `C:\POLITEC\gestao-documentos`.
4. No Antigravity, use **File > Open Folder** e escolha a pasta que tem `app.json`, `src`, `nucleo` e `construir.py`.
5. Abra o terminal e confira `python --version`.
6. Rode `python construir.py`.
7. Abra `index.html` no Edge ou no Chrome e clique em **Configuração > Carregar dados fictícios**.

## 5. Integração que falta, passo a passo

### Papéis e anexos

1. Liste quem cria, tramita, aprova e exclui.
2. Ajuste as permissões no `app.json` e nos botões.
3. Defina os anexos obrigatórios por tipo de processo.
4. Teste cada perfil.

### Cobrança

1. Decida entre painel local e e-mail institucional.
2. Mantenha a fila local com data, destinatário e texto.
3. Teste o aviso em 70% e no vencimento.
4. Registre quem recebeu e quando.

## 6. Como testar

```powershell
python construir.py
python testes/testar.py
python testes/cenarios.py
#/processos, #/processo/:id e #/painel
```

Se o teste falhar, leia a primeira mensagem, corrija uma coisa por vez e rode de novo.

## 7. Enviar para o GitHub

1. Entre em https://github.com/renato0503/gestao-documentos e aceite o convite de colaborador. Se ainda não recebeu, peça ao professor para enviar de novo.
2. Clique em **Code > Download ZIP** ou clone: `git clone https://github.com/renato0503/gestao-documentos.git`. O ZIP serve para abrir e estudar; para enviar alterações, use o clone ou um fork.
3. Extraia em uma pasta curta, por exemplo `C:\POLITEC\gestao-documentos`. Evite OneDrive e caminhos com muitos espaços.
4. Abra o **Antigravity**, escolha **File > Open Folder** e selecione a pasta que contém `app.json`, `src`, `nucleo`, `construir.py` e `testes`.
5. No terminal do Antigravity, rode `git checkout -b melhoria/gestao-documentos` para criar uma branch de trabalho.
6. Leia `README.md`, `PREMISSAS.md` e `sprint.md`. Não edite `index.html`: ele é gerado pelo `construir.py`.
7. Edite as fontes, rode `python construir.py`, abra o `index.html` e rode os testes do app.
8. Faça `git add .`, `git commit -m "..."`, `git push origin melhoria/<tema>` e abra um Pull Request no GitHub. Peça revisão antes do merge.

## 8. Prompt para o Antigravity

```text
Você está no projeto Gestão de Documentos (gestao-documentos). Leia README.md, PREMISSAS.md e sprint.md.
Não edite index.html. Trabalhe apenas em: Validar a matriz de papéis e quem pode excluir.
Antes de alterar, rode python construir.py e os testes. Depois de alterar, explique o que mudou,
rode os testes de novo e mostre o diff. Não use dados reais nem peça token.
```

**Commit sugerido:** `Gestão de Documentos: fecha papéis e cobrança`

## 9. Onde pedir ajuda

- Leia `PREMISSAS.md` para saber o que ainda é decisão do setor.
- Leia `sprint.md` para ver o que já foi feito e o que está aberto.
- Abra uma issue no repositório com o print, o passo e a mensagem de erro.
