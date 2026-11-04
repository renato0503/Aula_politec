# Pacote de continuidade · Comissão de Ética

**Equipe:** Letícia e Thiago  
**Tipo:** Automação de rotina  
**Repositório:** https://github.com/renato0503/comissao-etica-denuncias  
**App publicado:** https://renato0503.github.io/Aula_politec/Apps/comissao-etica-denuncias/index.html  
**ZIP:** https://github.com/renato0503/comissao-etica-denuncias/archive/refs/heads/main.zip

## 1. O que este app faz

Registro, classificação, admissibilidade, oitivas, minutas e relatório da Comissão de Ética.

## 2. O que já está pronto

- Registro e classificação assistida com o artigo da LC 112/2002-MT
- Admissibilidade com membros e fundamento padrão
- Oitivas com exclusão e encerramento
- Minutas, relatório, encerramento e envio por e-mail

## 3. O que falta

- Receber os modelos oficiais de ata, oitiva e relatório
- Confirmar a lista nominal dos membros
- Definir o canal de e-mail institucional e as permissões de envio

## 4. Baixar e abrir no Antigravity

1. Abra https://github.com/renato0503/comissao-etica-denuncias e aceite o convite de colaborador.
2. Baixe o ZIP em https://github.com/renato0503/comissao-etica-denuncias/archive/refs/heads/main.zip ou clone com `git clone https://github.com/renato0503/comissao-etica-denuncias.git`.
3. Extraia em `C:\POLITEC\comissao-etica-denuncias`.
4. No Antigravity, use **File > Open Folder** e escolha a pasta que tem `app.json`, `src`, `nucleo` e `construir.py`.
5. Abra o terminal e confira `python --version`.
6. Rode `python construir.py`.
7. Abra `index.html` no Edge ou no Chrome e clique em **Configuração > Carregar dados fictícios**.

## 5. Integração que falta, passo a passo

### Membros e modelos

1. Troque a lista `CE_MEMBROS` em `src/sprint4.js` pelos nomes reais.
2. Coloque os modelos em `modelos/` e ajuste `CE_MINUTAS` em `src/sprint6.js`.
3. Valide a ata, o relatório e o encerramento com a Comissão.
4. Registre as diferenças em `PREMISSAS.md`.

### Envio institucional

1. Decida se o envio será `mailto:` ou Apps Script.
2. Para Apps Script, crie uma função `enviarDocumento` e uma fila local.
3. Nunca coloque token no código; use as permissões da conta.
4. Teste com um documento sem dado real.

## 6. Como testar

```powershell
python construir.py
python testes/testar.py
python testes/cenarios.py
#/caso/:id/documentos e #/relatorio
```

Se o teste falhar, leia a primeira mensagem, corrija uma coisa por vez e rode de novo.

## 7. Enviar para o GitHub

1. Entre em https://github.com/renato0503/comissao-etica-denuncias e aceite o convite de colaborador. Se ainda não recebeu, peça ao professor para enviar de novo.
2. Clique em **Code > Download ZIP** ou clone: `git clone https://github.com/renato0503/comissao-etica-denuncias.git`. O ZIP serve para abrir e estudar; para enviar alterações, use o clone ou um fork.
3. Extraia em uma pasta curta, por exemplo `C:\POLITEC\comissao-etica-denuncias`. Evite OneDrive e caminhos com muitos espaços.
4. Abra o **Antigravity**, escolha **File > Open Folder** e selecione a pasta que contém `app.json`, `src`, `nucleo`, `construir.py` e `testes`.
5. No terminal do Antigravity, rode `git checkout -b melhoria/comissao-etica-denuncias` para criar uma branch de trabalho.
6. Leia `README.md`, `PREMISSAS.md` e `sprint.md`. Não edite `index.html`: ele é gerado pelo `construir.py`.
7. Edite as fontes, rode `python construir.py`, abra o `index.html` e rode os testes do app.
8. Faça `git add .`, `git commit -m "..."`, `git push origin melhoria/<tema>` e abra um Pull Request no GitHub. Peça revisão antes do merge.

## 8. Prompt para o Antigravity

```text
Você está no projeto Comissão de Ética (comissao-etica-denuncias). Leia README.md, PREMISSAS.md e sprint.md.
Não edite index.html. Trabalhe apenas em: Receber os modelos oficiais de ata, oitiva e relatório.
Antes de alterar, rode python construir.py e os testes. Depois de alterar, explique o que mudou,
rode os testes de novo e mostre o diff. Não use dados reais nem peça token.
```

**Commit sugerido:** `Comissão de Ética: usa os modelos e o canal oficiais`

## 9. Onde pedir ajuda

- Leia `PREMISSAS.md` para saber o que ainda é decisão do setor.
- Leia `sprint.md` para ver o que já foi feito e o que está aberto.
- Abra uma issue no repositório com o print, o passo e a mensagem de erro.
