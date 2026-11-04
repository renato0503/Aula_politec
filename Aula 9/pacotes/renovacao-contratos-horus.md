# Pacote de continuidade · Renovação de Contratos

**Equipe:** Rodrigo Neves  
**Tipo:** Mapeamento de processo  
**Repositório:** https://github.com/renato0503/renovacao-contratos-horus  
**App publicado:** https://renato0503.github.io/Aula_politec/Apps/renovacao-contratos-horus/index.html  
**ZIP:** https://github.com/renato0503/renovacao-contratos-horus/archive/refs/heads/main.zip

## 1. O que este app faz

Semáforo de vencimento, instrução, aditivos, fiscais e avisos de contrato.

## 2. O que já está pronto

- Cadastro e semáforo de seis faixas
- Aditivos, reajustes e instrução
- Fiscais e gestores com contato
- Edição, avisos e importação da planilha

## 3. O que falta

- Confirmar os contatos reais dos fiscais e gestores
- Definir o canal de e-mail e a confirmação de leitura
- Confirmar as faixas e o modelo da planilha do setor
- Validar as permissões de edição

## 4. Baixar e abrir no Antigravity

1. Abra https://github.com/renato0503/renovacao-contratos-horus e aceite o convite de colaborador.
2. Baixe o ZIP em https://github.com/renato0503/renovacao-contratos-horus/archive/refs/heads/main.zip ou clone com `git clone https://github.com/renato0503/renovacao-contratos-horus.git`.
3. Extraia em `C:\POLITEC\renovacao-contratos-horus`.
4. No Antigravity, use **File > Open Folder** e escolha a pasta que tem `app.json`, `src`, `nucleo` e `construir.py`.
5. Abra o terminal e confira `python --version`.
6. Rode `python construir.py`.
7. Abra `index.html` no Edge ou no Chrome e clique em **Configuração > Carregar dados fictícios**.

## 5. Integração que falta, passo a passo

### Contatos e planilha

1. Preencha os fiscais e gestores no cadastro do contrato.
2. Importe a planilha do setor em `#/contratos`.
3. Confira os contratos atualizados e o semáforo.
4. Corrija a planilha modelo se necessário.

### Avisos

1. Mantenha a fila local com destinatário, texto e data.
2. Para envio real, crie um Apps Script com `MailApp`.
3. Teste laranja e vermelho com contratos fictícios.
4. Registre leitura e resposta no app.

## 6. Como testar

```powershell
python construir.py
python testes/testar.py
python testes/cenarios.py
#/painel, #/instrucao e #/contrato/:id
```

Se o teste falhar, leia a primeira mensagem, corrija uma coisa por vez e rode de novo.

## 7. Enviar para o GitHub

1. Entre em https://github.com/renato0503/renovacao-contratos-horus e aceite o convite de colaborador. Se ainda não recebeu, peça ao professor para enviar de novo.
2. Clique em **Code > Download ZIP** ou clone: `git clone https://github.com/renato0503/renovacao-contratos-horus.git`. O ZIP serve para abrir e estudar; para enviar alterações, use o clone ou um fork.
3. Extraia em uma pasta curta, por exemplo `C:\POLITEC\renovacao-contratos-horus`. Evite OneDrive e caminhos com muitos espaços.
4. Abra o **Antigravity**, escolha **File > Open Folder** e selecione a pasta que contém `app.json`, `src`, `nucleo`, `construir.py` e `testes`.
5. No terminal do Antigravity, rode `git checkout -b melhoria/renovacao-contratos-horus` para criar uma branch de trabalho.
6. Leia `README.md`, `PREMISSAS.md` e `sprint.md`. Não edite `index.html`: ele é gerado pelo `construir.py`.
7. Edite as fontes, rode `python construir.py`, abra o `index.html` e rode os testes do app.
8. Faça `git add .`, `git commit -m "..."`, `git push origin melhoria/<tema>` e abra um Pull Request no GitHub. Peça revisão antes do merge.

## 8. Prompt para o Antigravity

```text
Você está no projeto Renovação de Contratos (renovacao-contratos-horus). Leia README.md, PREMISSAS.md e sprint.md.
Não edite index.html. Trabalhe apenas em: Confirmar os contatos reais dos fiscais e gestores.
Antes de alterar, rode python construir.py e os testes. Depois de alterar, explique o que mudou,
rode os testes de novo e mostre o diff. Não use dados reais nem peça token.
```

**Commit sugerido:** `Renovação: liga contatos e avisos reais`

## 9. Onde pedir ajuda

- Leia `PREMISSAS.md` para saber o que ainda é decisão do setor.
- Leia `sprint.md` para ver o que já foi feito e o que está aberto.
- Abra uma issue no repositório com o print, o passo e a mensagem de erro.
