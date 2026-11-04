# Pacote de continuidade · Segunda via da CIN

**Equipe:** André, Flávia e Glauce  
**Tipo:** Aplicativo para cidadão  
**Repositório:** https://github.com/renato0503/cin-segunda-via  
**App publicado:** https://renato0503.github.io/Aula_politec/Apps/cin-segunda-via/index.html  
**ZIP:** https://github.com/renato0503/cin-segunda-via/archive/refs/heads/main.zip

## 1. O que este app faz

Pedido de segunda via da Carteira de Identidade Nacional a distância, com conferência e fila.

## 2. O que já está pronto

- Pedido com elegibilidade e fotos de teste
- Quatro fotos de impressões digitais quando o documento foi extraviado
- Fila do servidor e protocolo
- Resumo para o sistema e troca de perfil

## 3. O que falta

- Integrar a base biométrica e o sistema de identificação
- Confirmar as regras oficiais da segunda via
- Validar a qualidade mínima das fotos e o fluxo de recusa

## 4. Baixar e abrir no Antigravity

1. Abra https://github.com/renato0503/cin-segunda-via e aceite o convite de colaborador.
2. Baixe o ZIP em https://github.com/renato0503/cin-segunda-via/archive/refs/heads/main.zip ou clone com `git clone https://github.com/renato0503/cin-segunda-via.git`.
3. Extraia em `C:\POLITEC\cin-segunda-via`.
4. No Antigravity, use **File > Open Folder** e escolha a pasta que tem `app.json`, `src`, `nucleo` e `construir.py`.
5. Abra o terminal e confira `python --version`.
6. Rode `python construir.py`.
7. Abra `index.html` no Edge ou no Chrome e clique em **Configuração > Carregar dados fictícios**.

## 5. Integração que falta, passo a passo

### Base biométrica

1. Peça à TI o contrato da API ou o caminho de exportação da base.
2. Crie uma fila local com o protocolo e o status da consulta.
3. Nunca grave a biometria no navegador; guarde só o resultado e o protocolo.
4. Teste com uma resposta simulada e registre no log.

### Regras e aceite

1. Confirme quando a segunda via dispensa nova coleta.
2. Ajuste a mensagem de recusa e o prazo.
3. Rode o roteiro com a equipe de identificação.
4. Atualize `PREMISSAS.md` com as respostas.

## 6. Como testar

```powershell
python construir.py
python testes/testar.py
python testes/cenarios.py
#/pedido e #/fila
```

Se o teste falhar, leia a primeira mensagem, corrija uma coisa por vez e rode de novo.

## 7. Enviar para o GitHub

1. Entre em https://github.com/renato0503/cin-segunda-via e aceite o convite de colaborador. Se ainda não recebeu, peça ao professor para enviar de novo.
2. Clique em **Code > Download ZIP** ou clone: `git clone https://github.com/renato0503/cin-segunda-via.git`. O ZIP serve para abrir e estudar; para enviar alterações, use o clone ou um fork.
3. Extraia em uma pasta curta, por exemplo `C:\POLITEC\cin-segunda-via`. Evite OneDrive e caminhos com muitos espaços.
4. Abra o **Antigravity**, escolha **File > Open Folder** e selecione a pasta que contém `app.json`, `src`, `nucleo`, `construir.py` e `testes`.
5. No terminal do Antigravity, rode `git checkout -b melhoria/cin-segunda-via` para criar uma branch de trabalho.
6. Leia `README.md`, `PREMISSAS.md` e `sprint.md`. Não edite `index.html`: ele é gerado pelo `construir.py`.
7. Edite as fontes, rode `python construir.py`, abra o `index.html` e rode os testes do app.
8. Faça `git add .`, `git commit -m "..."`, `git push origin melhoria/<tema>` e abra um Pull Request no GitHub. Peça revisão antes do merge.

## 8. Prompt para o Antigravity

```text
Você está no projeto Segunda via da CIN (cin-segunda-via). Leia README.md, PREMISSAS.md e sprint.md.
Não edite index.html. Trabalhe apenas em: Integrar a base biométrica e o sistema de identificação.
Antes de alterar, rode python construir.py e os testes. Depois de alterar, explique o que mudou,
rode os testes de novo e mostre o diff. Não use dados reais nem peça token.
```

**Commit sugerido:** `CIN 2ª via: prepara a integração biométrica`

## 9. Onde pedir ajuda

- Leia `PREMISSAS.md` para saber o que ainda é decisão do setor.
- Leia `sprint.md` para ver o que já foi feito e o que está aberto.
- Abra uma issue no repositório com o print, o passo e a mensagem de erro.
