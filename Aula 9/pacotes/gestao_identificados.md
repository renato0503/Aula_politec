# Pacote de continuidade · NIHDE · Gestão de Identificados

**Equipe:** Kesia Melo  
**Tipo:** Aplicativo web e portal  
**Repositório:** https://github.com/renato0503/gestao_identificados  
**App publicado:** https://renato0503.github.io/Aula_politec/Apps/gestao_identificados/index.html  
**ZIP:** https://github.com/renato0503/gestao_identificados/archive/refs/heads/main.zip

## 1. O que este app faz

Corpos não identificados e não reclamados, exames, família, sepultamento e relatório.

## 2. O que já está pronto

- Cadastro, exames, identificação e família
- Sepultamento, entrega e auditoria
- Relatório e CSV
- Módulo CNPD/NamUs e cruzamento com os corpos

## 3. O que falta

- Confirmar o nome oficial do NIHDE e o escopo dos dados físicos
- Integrar com o Atena e a base de desaparecidos
- Validar os pesos do cruzamento e o fluxo de exames complementares

## 4. Baixar e abrir no Antigravity

1. Abra https://github.com/renato0503/gestao_identificados e aceite o convite de colaborador.
2. Baixe o ZIP em https://github.com/renato0503/gestao_identificados/archive/refs/heads/main.zip ou clone com `git clone https://github.com/renato0503/gestao_identificados.git`.
3. Extraia em `C:\POLITEC\gestao_identificados`.
4. No Antigravity, use **File > Open Folder** e escolha a pasta que tem `app.json`, `src`, `nucleo` e `construir.py`.
5. Abra o terminal e confira `python --version`.
6. Rode `python construir.py`.
7. Abra `index.html` no Edge ou no Chrome e clique em **Configuração > Carregar dados fictícios**.

## 5. Integração que falta, passo a passo

### Atena

1. Peça à TI o dicionário de dados e o caminho de integração.
2. Crie um importador/exportador em JSON e registre a origem.
3. Nunca misture dado público com o cadastro do corpo.
4. Teste com um caso fictício e registre no log.

### Cruzamento

1. Escolha um desaparecido e clique em **Ver corpos**.
2. Confira os motivos e a lista de até 10 candidatos.
3. Confirme, descarte ou peça exame com justificativa.
4. Valide o resultado com o NIHDE antes do piloto.

## 6. Como testar

```powershell
python construir.py
python testes/testar.py
python testes/cenarios.py
#/desaparecidos e #/corpo/:id
```

Se o teste falhar, leia a primeira mensagem, corrija uma coisa por vez e rode de novo.

## 7. Enviar para o GitHub

1. Entre em https://github.com/renato0503/gestao_identificados e aceite o convite de colaborador. Se ainda não recebeu, peça ao professor para enviar de novo.
2. Clique em **Code > Download ZIP** ou clone: `git clone https://github.com/renato0503/gestao_identificados.git`. O ZIP serve para abrir e estudar; para enviar alterações, use o clone ou um fork.
3. Extraia em uma pasta curta, por exemplo `C:\POLITEC\gestao_identificados`. Evite OneDrive e caminhos com muitos espaços.
4. Abra o **Antigravity**, escolha **File > Open Folder** e selecione a pasta que contém `app.json`, `src`, `nucleo`, `construir.py` e `testes`.
5. No terminal do Antigravity, rode `git checkout -b melhoria/gestao_identificados` para criar uma branch de trabalho.
6. Leia `README.md`, `PREMISSAS.md` e `sprint.md`. Não edite `index.html`: ele é gerado pelo `construir.py`.
7. Edite as fontes, rode `python construir.py`, abra o `index.html` e rode os testes do app.
8. Faça `git add .`, `git commit -m "..."`, `git push origin melhoria/<tema>` e abra um Pull Request no GitHub. Peça revisão antes do merge.

## 8. Prompt para o Antigravity

```text
Você está no projeto NIHDE · Gestão de Identificados (gestao_identificados). Leia README.md, PREMISSAS.md e sprint.md.
Não edite index.html. Trabalhe apenas em: Confirmar o nome oficial do NIHDE e o escopo dos dados físicos.
Antes de alterar, rode python construir.py e os testes. Depois de alterar, explique o que mudou,
rode os testes de novo e mostre o diff. Não use dados reais nem peça token.
```

**Commit sugerido:** `NIHDE: valida o cruzamento com o setor`

## 9. Onde pedir ajuda

- Leia `PREMISSAS.md` para saber o que ainda é decisão do setor.
- Leia `sprint.md` para ver o que já foi feito e o que está aberto.
- Abra uma issue no repositório com o print, o passo e a mensagem de erro.
