# Pacote de continuidade · Controle do Processo de Aquisição

**Equipe:** Kasteline  
**Tipo:** Painel de BI  
**Repositório:** https://github.com/renato0503/controle-aquisicoes  
**App publicado:** https://renato0503.github.io/Aula_politec/Apps/controle-aquisicoes/index.html  
**ZIP:** https://github.com/renato0503/controle-aquisicoes/archive/refs/heads/main.zip

## 1. O que este app faz

Nove etapas da contratação, documentos, três cotações, alerta de preço e base legal.

## 2. O que já está pronto

- Fluxo de 9 etapas ancorado na Lei 14.133/2021
- Pesquisa de preços com três cotações e memória de cálculo
- Alerta de estimado x cotado e histórico por objeto
- Painel compacto e conferência no celular

## 3. O que falta

- Receber os modelos oficiais de DFD, ETP, TR e análise de riscos
- Confirmar prazos, permissões e a base de 2024/2025
- Validar o alerta de 30% com o setor

## 4. Baixar e abrir no Antigravity

1. Abra https://github.com/renato0503/controle-aquisicoes e aceite o convite de colaborador.
2. Baixe o ZIP em https://github.com/renato0503/controle-aquisicoes/archive/refs/heads/main.zip ou clone com `git clone https://github.com/renato0503/controle-aquisicoes.git`.
3. Extraia em `C:\POLITEC\controle-aquisicoes`.
4. No Antigravity, use **File > Open Folder** e escolha a pasta que tem `app.json`, `src`, `nucleo` e `construir.py`.
5. Abra o terminal e confira `python --version`.
6. Rode `python construir.py`.
7. Abra `index.html` no Edge ou no Chrome e clique em **Configuração > Carregar dados fictícios**.

## 5. Integração que falta, passo a passo

### Modelos oficiais

1. Salve os modelos em `modelos/` sem dado real.
2. Ajuste os campos e os anexos obrigatórios em `src/app.js`.
3. Faça um processo de teste do DFD ao parecer.
4. Confira a base legal exibida na ficha.

### Base e permissões

1. Importe a base histórica em CSV e confira as colunas.
2. Defina quem cria, quem aprova e quem só consulta.
3. Teste cada perfil e registre no roteiro de aceite.
4. Meça o tempo do processo antes e depois.

## 6. Como testar

```powershell
python construir.py
python testes/testar.py
python testes/cenarios.py
#/processos e #/precos
```

Se o teste falhar, leia a primeira mensagem, corrija uma coisa por vez e rode de novo.

## 7. Enviar para o GitHub

1. Entre em https://github.com/renato0503/controle-aquisicoes e aceite o convite de colaborador. Se ainda não recebeu, peça ao professor para enviar de novo.
2. Clique em **Code > Download ZIP** ou clone: `git clone https://github.com/renato0503/controle-aquisicoes.git`. O ZIP serve para abrir e estudar; para enviar alterações, use o clone ou um fork.
3. Extraia em uma pasta curta, por exemplo `C:\POLITEC\controle-aquisicoes`. Evite OneDrive e caminhos com muitos espaços.
4. Abra o **Antigravity**, escolha **File > Open Folder** e selecione a pasta que contém `app.json`, `src`, `nucleo`, `construir.py` e `testes`.
5. No terminal do Antigravity, rode `git checkout -b melhoria/controle-aquisicoes` para criar uma branch de trabalho.
6. Leia `README.md`, `PREMISSAS.md` e `sprint.md`. Não edite `index.html`: ele é gerado pelo `construir.py`.
7. Edite as fontes, rode `python construir.py`, abra o `index.html` e rode os testes do app.
8. Faça `git add .`, `git commit -m "..."`, `git push origin melhoria/<tema>` e abra um Pull Request no GitHub. Peça revisão antes do merge.

## 8. Prompt para o Antigravity

```text
Você está no projeto Controle do Processo de Aquisição (controle-aquisicoes). Leia README.md, PREMISSAS.md e sprint.md.
Não edite index.html. Trabalhe apenas em: Receber os modelos oficiais de DFD, ETP, TR e análise de riscos.
Antes de alterar, rode python construir.py e os testes. Depois de alterar, explique o que mudou,
rode os testes de novo e mostre o diff. Não use dados reais nem peça token.
```

**Commit sugerido:** `Aquisições: integra modelos e base histórica`

## 9. Onde pedir ajuda

- Leia `PREMISSAS.md` para saber o que ainda é decisão do setor.
- Leia `sprint.md` para ver o que já foi feito e o que está aberto.
- Abra uma issue no repositório com o print, o passo e a mensagem de erro.
