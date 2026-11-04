# Pacote de continuidade · Custódia Definitiva

**Equipe:** Edjane Ávila  
**Tipo:** Mapeamento e aplicativo  
**Repositório:** https://github.com/renato0503/custodia-definitiva  
**App publicado:** https://renato0503.github.io/Aula_politec/Apps/custodia-definitiva/index.html  
**ZIP:** https://github.com/renato0503/custodia-definitiva/archive/refs/heads/main.zip

## 1. O que este app faz

Recebimento, endereçamento e localização de vestígios na custódia definitiva.

## 2. O que já está pronto

- Cadastro e endereço hierárquico
- Endereço sugerido x efetivo e confirmação física
- Acervo, movimentações e painel de ocupação
- Alertas de capacidade e compatibilidade

## 3. O que falta

- Confirmar a estrutura física real e as capacidades
- Definir a unidade de medida e a compatibilidade entre categorias
- Medir o tempo de recebimento e de localização

## 4. Baixar e abrir no Antigravity

1. Abra https://github.com/renato0503/custodia-definitiva e aceite o convite de colaborador.
2. Baixe o ZIP em https://github.com/renato0503/custodia-definitiva/archive/refs/heads/main.zip ou clone com `git clone https://github.com/renato0503/custodia-definitiva.git`.
3. Extraia em `C:\POLITEC\custodia-definitiva`.
4. No Antigravity, use **File > Open Folder** e escolha a pasta que tem `app.json`, `src`, `nucleo` e `construir.py`.
5. Abra o terminal e confira `python --version`.
6. Rode `python construir.py`.
7. Abra `index.html` no Edge ou no Chrome e clique em **Configuração > Carregar dados fictícios**.

## 5. Integração que falta, passo a passo

### Estrutura real

1. Levante contêiner, estante, prateleira, nível e posição de cada espaço.
2. Ajuste as capacidades e a unidade em `app.json` e no cadastro.
3. Recadastre os espaços fictícios com os reais.
4. Teste uma entrada e uma localização ponta a ponta.

### Aceite

1. Escolha uma amostra de vestígios.
2. Compare o endereço sugerido com o efetivo.
3. Registre as divergências e o tempo de localização.
4. Atualize o roteiro de aceite.

## 6. Como testar

```powershell
python construir.py
python testes/testar.py
python testes/cenarios.py
#/acervo, #/entrada e #/painel
```

Se o teste falhar, leia a primeira mensagem, corrija uma coisa por vez e rode de novo.

## 7. Enviar para o GitHub

1. Entre em https://github.com/renato0503/custodia-definitiva e aceite o convite de colaborador. Se ainda não recebeu, peça ao professor para enviar de novo.
2. Clique em **Code > Download ZIP** ou clone: `git clone https://github.com/renato0503/custodia-definitiva.git`. O ZIP serve para abrir e estudar; para enviar alterações, use o clone ou um fork.
3. Extraia em uma pasta curta, por exemplo `C:\POLITEC\custodia-definitiva`. Evite OneDrive e caminhos com muitos espaços.
4. Abra o **Antigravity**, escolha **File > Open Folder** e selecione a pasta que contém `app.json`, `src`, `nucleo`, `construir.py` e `testes`.
5. No terminal do Antigravity, rode `git checkout -b melhoria/custodia-definitiva` para criar uma branch de trabalho.
6. Leia `README.md`, `PREMISSAS.md` e `sprint.md`. Não edite `index.html`: ele é gerado pelo `construir.py`.
7. Edite as fontes, rode `python construir.py`, abra o `index.html` e rode os testes do app.
8. Faça `git add .`, `git commit -m "..."`, `git push origin melhoria/<tema>` e abra um Pull Request no GitHub. Peça revisão antes do merge.

## 8. Prompt para o Antigravity

```text
Você está no projeto Custódia Definitiva (custodia-definitiva). Leia README.md, PREMISSAS.md e sprint.md.
Não edite index.html. Trabalhe apenas em: Confirmar a estrutura física real e as capacidades.
Antes de alterar, rode python construir.py e os testes. Depois de alterar, explique o que mudou,
rode os testes de novo e mostre o diff. Não use dados reais nem peça token.
```

**Commit sugerido:** `Custódia: atualiza a estrutura física real`

## 9. Onde pedir ajuda

- Leia `PREMISSAS.md` para saber o que ainda é decisão do setor.
- Leia `sprint.md` para ver o que já foi feito e o que está aberto.
- Abra uma issue no repositório com o print, o passo e a mensagem de erro.
