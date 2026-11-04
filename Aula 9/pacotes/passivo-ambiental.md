# Pacote de continuidade · Passivo Ambiental

**Equipe:** Fábio  
**Tipo:** Mapeamento e aplicativo  
**Repositório:** https://github.com/renato0503/passivo-ambiental  
**App publicado:** https://renato0503.github.io/Aula_politec/Apps/passivo-ambiental/index.html  
**ZIP:** https://github.com/renato0503/passivo-ambiental/archive/refs/heads/main.zip

## 1. O que este app faz

Laudos ambientais atrasados, com requisição, mapas, metodologia, valoração e quesitos.

## 2. O que já está pronto

- Requisição e cabeçalho do laudo
- Editor de mapas com três mapas obrigatórios
- Metodologia, considerações e valoração
- Quesitos, PDF e `.docx`

## 3. O que falta

- Receber o modelo oficial do laudo e uma requisição anonimizada
- Confirmar o texto da metodologia e os critérios de valoração
- Validar o modelo de mapa com o perito

## 4. Baixar e abrir no Antigravity

1. Abra https://github.com/renato0503/passivo-ambiental e aceite o convite de colaborador.
2. Baixe o ZIP em https://github.com/renato0503/passivo-ambiental/archive/refs/heads/main.zip ou clone com `git clone https://github.com/renato0503/passivo-ambiental.git`.
3. Extraia em `C:\POLITEC\passivo-ambiental`.
4. No Antigravity, use **File > Open Folder** e escolha a pasta que tem `app.json`, `src`, `nucleo` e `construir.py`.
5. Abra o terminal e confira `python --version`.
6. Rode `python construir.py`.
7. Abra `index.html` no Edge ou no Chrome e clique em **Configuração > Carregar dados fictícios**.

## 5. Integração que falta, passo a passo

### Modelo oficial

1. Compare o laudo gerado com o modelo da unidade.
2. Ajuste os títulos, o cabeçalho e as seções.
3. Inclua o texto padrão de metodologia quando aprovado.
4. Teste com uma requisição fictícia.

### Valoração e mapas

1. Confirme a área, o valor de referência e a memória de cálculo.
2. Padronize norte, escala e legenda dos três mapas.
3. Gere o PDF e o `.docx` e confira as imagens.
4. Peça a revisão do perito.

## 6. Como testar

```powershell
python construir.py
python testes/testar.py
python testes/cenarios.py
#/requisicoes e #/laudo/:id
```

Se o teste falhar, leia a primeira mensagem, corrija uma coisa por vez e rode de novo.

## 7. Enviar para o GitHub

1. Entre em https://github.com/renato0503/passivo-ambiental e aceite o convite de colaborador. Se ainda não recebeu, peça ao professor para enviar de novo.
2. Clique em **Code > Download ZIP** ou clone: `git clone https://github.com/renato0503/passivo-ambiental.git`. O ZIP serve para abrir e estudar; para enviar alterações, use o clone ou um fork.
3. Extraia em uma pasta curta, por exemplo `C:\POLITEC\passivo-ambiental`. Evite OneDrive e caminhos com muitos espaços.
4. Abra o **Antigravity**, escolha **File > Open Folder** e selecione a pasta que contém `app.json`, `src`, `nucleo`, `construir.py` e `testes`.
5. No terminal do Antigravity, rode `git checkout -b melhoria/passivo-ambiental` para criar uma branch de trabalho.
6. Leia `README.md`, `PREMISSAS.md` e `sprint.md`. Não edite `index.html`: ele é gerado pelo `construir.py`.
7. Edite as fontes, rode `python construir.py`, abra o `index.html` e rode os testes do app.
8. Faça `git add .`, `git commit -m "..."`, `git push origin melhoria/<tema>` e abra um Pull Request no GitHub. Peça revisão antes do merge.

## 8. Prompt para o Antigravity

```text
Você está no projeto Passivo Ambiental (passivo-ambiental). Leia README.md, PREMISSAS.md e sprint.md.
Não edite index.html. Trabalhe apenas em: Receber o modelo oficial do laudo e uma requisição anonimizada.
Antes de alterar, rode python construir.py e os testes. Depois de alterar, explique o que mudou,
rode os testes de novo e mostre o diff. Não use dados reais nem peça token.
```

**Commit sugerido:** `Passivo: usa o modelo e a valoração oficiais`

## 9. Onde pedir ajuda

- Leia `PREMISSAS.md` para saber o que ainda é decisão do setor.
- Leia `sprint.md` para ver o que já foi feito e o que está aberto.
- Abra uma issue no repositório com o print, o passo e a mensagem de erro.
