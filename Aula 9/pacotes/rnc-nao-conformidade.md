# Pacote de continuidade · Registro de Não Conformidade

**Equipe:** Sabrina Ellen  
**Tipo:** Formulário e painel  
**Repositório:** https://github.com/renato0503/rnc-nao-conformidade  
**App publicado:** https://renato0503.github.io/Aula_politec/Apps/rnc-nao-conformidade/index.html  
**ZIP:** https://github.com/renato0503/rnc-nao-conformidade/archive/refs/heads/main.zip

## 1. O que este app faz

RNC com importação da planilha oficial, etapas, prazos, plano de ação e documento.

## 2. O que já está pronto

- Importação do `.xlsx` oficial e do Google Planilhas
- Etapas, prazos e complemento em 5 dias úteis
- Plano de ação, avaliação e relacionamento
- Relação do setor e documento para impressão

## 3. O que falta

- Receber o modelo oficial e as categorias da CQUAL
- Definir login e permissões reais
- Validar a planilha real e o canal de e-mail

## 4. Baixar e abrir no Antigravity

1. Abra https://github.com/renato0503/rnc-nao-conformidade e aceite o convite de colaborador.
2. Baixe o ZIP em https://github.com/renato0503/rnc-nao-conformidade/archive/refs/heads/main.zip ou clone com `git clone https://github.com/renato0503/rnc-nao-conformidade.git`.
3. Extraia em `C:\POLITEC\rnc-nao-conformidade`.
4. No Antigravity, use **File > Open Folder** e escolha a pasta que tem `app.json`, `src`, `nucleo` e `construir.py`.
5. Abra o terminal e confira `python --version`.
6. Rode `python construir.py`.
7. Abra `index.html` no Edge ou no Chrome e clique em **Configuração > Carregar dados fictícios**.

## 5. Integração que falta, passo a passo

### Planilha e categorias

1. Coloque a planilha oficial em `modelos/`.
2. Ajuste as 23 colunas e as categorias em `src/app.js`.
3. Importe uma resposta fictícia e confira a ficha.
4. Valide com a CQUAL.

### Login e e-mail

1. A autenticação real não fica no navegador; use o provedor institucional.
2. Mantenha a fila local para os avisos.
3. Teste a relação do setor e o PDF.
4. Registre as permissões.

## 6. Como testar

```powershell
python construir.py
python testes/testar.py
python testes/cenarios.py
#/importar e #/rnc/:id
```

Se o teste falhar, leia a primeira mensagem, corrija uma coisa por vez e rode de novo.

## 7. Enviar para o GitHub

1. Entre em https://github.com/renato0503/rnc-nao-conformidade e aceite o convite de colaborador. Se ainda não recebeu, peça ao professor para enviar de novo.
2. Clique em **Code > Download ZIP** ou clone: `git clone https://github.com/renato0503/rnc-nao-conformidade.git`. O ZIP serve para abrir e estudar; para enviar alterações, use o clone ou um fork.
3. Extraia em uma pasta curta, por exemplo `C:\POLITEC\rnc-nao-conformidade`. Evite OneDrive e caminhos com muitos espaços.
4. Abra o **Antigravity**, escolha **File > Open Folder** e selecione a pasta que contém `app.json`, `src`, `nucleo`, `construir.py` e `testes`.
5. No terminal do Antigravity, rode `git checkout -b melhoria/rnc-nao-conformidade` para criar uma branch de trabalho.
6. Leia `README.md`, `PREMISSAS.md` e `sprint.md`. Não edite `index.html`: ele é gerado pelo `construir.py`.
7. Edite as fontes, rode `python construir.py`, abra o `index.html` e rode os testes do app.
8. Faça `git add .`, `git commit -m "..."`, `git push origin melhoria/<tema>` e abra um Pull Request no GitHub. Peça revisão antes do merge.

## 8. Prompt para o Antigravity

```text
Você está no projeto Registro de Não Conformidade (rnc-nao-conformidade). Leia README.md, PREMISSAS.md e sprint.md.
Não edite index.html. Trabalhe apenas em: Receber o modelo oficial e as categorias da CQUAL.
Antes de alterar, rode python construir.py e os testes. Depois de alterar, explique o que mudou,
rode os testes de novo e mostre o diff. Não use dados reais nem peça token.
```

**Commit sugerido:** `RNC: valida a planilha e as permissões oficiais`

## 9. Onde pedir ajuda

- Leia `PREMISSAS.md` para saber o que ainda é decisão do setor.
- Leia `sprint.md` para ver o que já foi feito e o que está aberto.
- Abra uma issue no repositório com o print, o passo e a mensagem de erro.
