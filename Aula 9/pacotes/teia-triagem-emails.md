# Pacote de continuidade · TEIA · Triagem de E-mails

**Equipe:** Nelson e Helen  
**Tipo:** Automação de rotina  
**Repositório:** https://github.com/renato0503/teia-triagem-emails  
**App publicado:** https://renato0503.github.io/Aula_politec/Apps/teia-triagem-emails/index.html  
**ZIP:** https://github.com/renato0503/teia-triagem-emails/archive/refs/heads/main.zip

## 1. O que este app faz

Triagem de e-mails, extração de campos, divergências, lote e planilha.

## 2. O que já está pronto

- Fila, extração e conferência
- Divergências e OCR simulado
- Lote e planilha
- Campos do feedback, 36 regionais e reiteração

## 3. O que falta

- Ler e-mails e PDFs reais
- Integrar a caixa institucional
- Validar as regionais, os níveis e a regra de reiteração
- Definir o OCR real

## 4. Baixar e abrir no Antigravity

1. Abra https://github.com/renato0503/teia-triagem-emails e aceite o convite de colaborador.
2. Baixe o ZIP em https://github.com/renato0503/teia-triagem-emails/archive/refs/heads/main.zip ou clone com `git clone https://github.com/renato0503/teia-triagem-emails.git`.
3. Extraia em `C:\POLITEC\teia-triagem-emails`.
4. No Antigravity, use **File > Open Folder** e escolha a pasta que tem `app.json`, `src`, `nucleo` e `construir.py`.
5. Abra o terminal e confira `python --version`.
6. Rode `python construir.py`.
7. Abra `index.html` no Edge ou no Chrome e clique em **Configuração > Carregar dados fictícios**.

## 5. Integração que falta, passo a passo

### Caixa e e-mails

1. Peça à TI a caixa e o formato de exportação.
2. Implemente a leitura local de `.eml`/`.msg` ou a cola de texto.
3. Mantenha a fila e o protocolo `nnnnnn/aaaa`.
4. Teste com e-mails fictícios.

### OCR e regionais

1. Confirme as 36 regionais e a grafia.
2. Se o PDF for imagem, avalie um OCR separado.
3. Valide a reiteração em 30 dias.
4. Registre as divergências.

## 6. Como testar

```powershell
python construir.py
python testes/testar.py
python testes/cenarios.py
#/fila e #/lote
```

Se o teste falhar, leia a primeira mensagem, corrija uma coisa por vez e rode de novo.

## 7. Enviar para o GitHub

1. Entre em https://github.com/renato0503/teia-triagem-emails e aceite o convite de colaborador. Se ainda não recebeu, peça ao professor para enviar de novo.
2. Clique em **Code > Download ZIP** ou clone: `git clone https://github.com/renato0503/teia-triagem-emails.git`. O ZIP serve para abrir e estudar; para enviar alterações, use o clone ou um fork.
3. Extraia em uma pasta curta, por exemplo `C:\POLITEC\teia-triagem-emails`. Evite OneDrive e caminhos com muitos espaços.
4. Abra o **Antigravity**, escolha **File > Open Folder** e selecione a pasta que contém `app.json`, `src`, `nucleo`, `construir.py` e `testes`.
5. No terminal do Antigravity, rode `git checkout -b melhoria/teia-triagem-emails` para criar uma branch de trabalho.
6. Leia `README.md`, `PREMISSAS.md` e `sprint.md`. Não edite `index.html`: ele é gerado pelo `construir.py`.
7. Edite as fontes, rode `python construir.py`, abra o `index.html` e rode os testes do app.
8. Faça `git add .`, `git commit -m "..."`, `git push origin melhoria/<tema>` e abra um Pull Request no GitHub. Peça revisão antes do merge.

## 8. Prompt para o Antigravity

```text
Você está no projeto TEIA · Triagem de E-mails (teia-triagem-emails). Leia README.md, PREMISSAS.md e sprint.md.
Não edite index.html. Trabalhe apenas em: Ler e-mails e PDFs reais.
Antes de alterar, rode python construir.py e os testes. Depois de alterar, explique o que mudou,
rode os testes de novo e mostre o diff. Não use dados reais nem peça token.
```

**Commit sugerido:** `TEIA: prepara a caixa e o OCR reais`

## 9. Onde pedir ajuda

- Leia `PREMISSAS.md` para saber o que ainda é decisão do setor.
- Leia `sprint.md` para ver o que já foi feito e o que está aberto.
- Abra uma issue no repositório com o print, o passo e a mensagem de erro.
