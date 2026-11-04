# Pacote de continuidade · Agiliza+

**Equipe:** Diego, Francineide, Andreia e Eric  
**Tipo:** Automação de laudos  
**Repositório:** https://github.com/renato0503/agiliza-mais  
**App publicado:** https://renato0503.github.io/Aula_politec/Apps/agiliza-mais/index.html  
**ZIP:** https://github.com/renato0503/agiliza-mais/archive/refs/heads/main.zip

## 1. O que este app faz

Gera o laudo de exame em celular a partir da pasta do caso e do modelo Word.

## 2. O que já está pronto

- Pasta do caso, extração e conferência
- Textos, quesitos e biblioteca
- Laudo `.docx` pelo modelo embutido
- Revisão, histórico e limpeza por LGPD

## 3. O que falta

- Ler a requisição em PDF com pdf.js e o OCR de imagem
- Receber o modelo institucional timbrado e os formatos reais dos TXT/HTML
- Fechar o Sprint 12 de aceite e o piloto

## 4. Baixar e abrir no Antigravity

1. Abra https://github.com/renato0503/agiliza-mais e aceite o convite de colaborador.
2. Baixe o ZIP em https://github.com/renato0503/agiliza-mais/archive/refs/heads/main.zip ou clone com `git clone https://github.com/renato0503/agiliza-mais.git`.
3. Extraia em `C:\POLITEC\agiliza-mais`.
4. No Antigravity, use **File > Open Folder** e escolha a pasta que tem `app.json`, `src`, `nucleo` e `construir.py`.
5. Abra o terminal e confira `python --version`.
6. Rode `python construir.py`.
7. Abra `index.html` no Edge ou no Chrome e clique em **Configuração > Carregar dados fictícios**.

## 5. Integração que falta, passo a passo

### PDF e OCR

1. Ative o pdf.js já presente em `vendor/` e leia a requisição em `#/conferencia`.
2. Se o PDF não tiver texto, mostre a mensagem e permita digitar ou usar um OCR externo.
3. Registre a origem de cada campo lido.
4. Teste com uma requisição fictícia e confira o laudo.

### Modelo institucional

1. Coloque o `.docx` em `modelos/` e os marcadores em `modelos/MARCADORES.md`.
2. Confira cada marcador no `docxtemplater`.
3. Gere um laudo de teste e abra no Word.
4. Peça a validação do perito antes do piloto.

## 6. Como testar

```powershell
python construir.py
python testes/testar.py
python testes/cenarios.py
#/inicio, #/caso/:id e #/revisao
```

Se o teste falhar, leia a primeira mensagem, corrija uma coisa por vez e rode de novo.

## 7. Enviar para o GitHub

1. Entre em https://github.com/renato0503/agiliza-mais e aceite o convite de colaborador. Se ainda não recebeu, peça ao professor para enviar de novo.
2. Clique em **Code > Download ZIP** ou clone: `git clone https://github.com/renato0503/agiliza-mais.git`. O ZIP serve para abrir e estudar; para enviar alterações, use o clone ou um fork.
3. Extraia em uma pasta curta, por exemplo `C:\POLITEC\agiliza-mais`. Evite OneDrive e caminhos com muitos espaços.
4. Abra o **Antigravity**, escolha **File > Open Folder** e selecione a pasta que contém `app.json`, `src`, `nucleo`, `construir.py` e `testes`.
5. No terminal do Antigravity, rode `git checkout -b melhoria/agiliza-mais` para criar uma branch de trabalho.
6. Leia `README.md`, `PREMISSAS.md` e `sprint.md`. Não edite `index.html`: ele é gerado pelo `construir.py`.
7. Edite as fontes, rode `python construir.py`, abra o `index.html` e rode os testes do app.
8. Faça `git add .`, `git commit -m "..."`, `git push origin melhoria/<tema>` e abra um Pull Request no GitHub. Peça revisão antes do merge.

## 8. Prompt para o Antigravity

```text
Você está no projeto Agiliza+ (agiliza-mais). Leia README.md, PREMISSAS.md e sprint.md.
Não edite index.html. Trabalhe apenas em: Ler a requisição em PDF com pdf.js e o OCR de imagem.
Antes de alterar, rode python construir.py e os testes. Depois de alterar, explique o que mudou,
rode os testes de novo e mostre o diff. Não use dados reais nem peça token.
```

**Commit sugerido:** `Agiliza+: liga PDF, OCR e modelo institucional`

## 9. Onde pedir ajuda

- Leia `PREMISSAS.md` para saber o que ainda é decisão do setor.
- Leia `sprint.md` para ver o que já foi feito e o que está aberto.
- Abra uma issue no repositório com o print, o passo e a mensagem de erro.
