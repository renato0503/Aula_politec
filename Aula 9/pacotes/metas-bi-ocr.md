# Pacote de continuidade · Metas pelo BI

**Equipe:** Karine Assunção  
**Tipo:** Automação de rotina  
**Repositório:** https://github.com/renato0503/metas-bi-ocr  
**App publicado:** https://renato0503.github.io/Aula_politec/Apps/metas-bi-ocr/index.html  
**ZIP:** https://github.com/renato0503/metas-bi-ocr/archive/refs/heads/main.zip

## 1. O que este app faz

Importa o mês do Power BI, confere, aprova e gera a planilha.

## 2. O que já está pronto

- Leitura de CSV, Excel e PDF com texto
- Filtro de gerência e recorte de unidades monitoradas
- Conferência, correção e aprovação
- Geração da planilha

## 3. O que falta

- Confirmar se o Power BI permite exportar o visual
- Receber uma amostra do PDF mensal
- Confirmar o cabeçalho da planilha e as unidades
- Avaliar OCR de PDF em imagem

## 4. Baixar e abrir no Antigravity

1. Abra https://github.com/renato0503/metas-bi-ocr e aceite o convite de colaborador.
2. Baixe o ZIP em https://github.com/renato0503/metas-bi-ocr/archive/refs/heads/main.zip ou clone com `git clone https://github.com/renato0503/metas-bi-ocr.git`.
3. Extraia em `C:\POLITEC\metas-bi-ocr`.
4. No Antigravity, use **File > Open Folder** e escolha a pasta que tem `app.json`, `src`, `nucleo` e `construir.py`.
5. Abra o terminal e confira `python --version`.
6. Rode `python construir.py`.
7. Abra `index.html` no Edge ou no Chrome e clique em **Configuração > Carregar dados fictícios**.

## 5. Integração que falta, passo a passo

### Exportação do Power BI

1. Peça à TI a opção Exportar dados do visual.
2. Teste CSV e Excel com o mês real.
3. Ajuste o mapeamento de colunas se o cabeçalho mudar.
4. Registre a versão do Power BI usada.

### OCR

1. Só implemente se o PDF em imagem for inevitável.
2. Prefira uma página `ocr.html` separada para não pesar o app.
3. Valide o número lido com confiança e correção humana.
4. Nunca aprove sem conferência.

## 6. Como testar

```powershell
python construir.py
python testes/testar.py
python testes/cenarios.py
#/importar, #/conferencia/:mes e #/exportar/:mes
```

Se o teste falhar, leia a primeira mensagem, corrija uma coisa por vez e rode de novo.

## 7. Enviar para o GitHub

1. Entre em https://github.com/renato0503/metas-bi-ocr e aceite o convite de colaborador. Se ainda não recebeu, peça ao professor para enviar de novo.
2. Clique em **Code > Download ZIP** ou clone: `git clone https://github.com/renato0503/metas-bi-ocr.git`. O ZIP serve para abrir e estudar; para enviar alterações, use o clone ou um fork.
3. Extraia em uma pasta curta, por exemplo `C:\POLITEC\metas-bi-ocr`. Evite OneDrive e caminhos com muitos espaços.
4. Abra o **Antigravity**, escolha **File > Open Folder** e selecione a pasta que contém `app.json`, `src`, `nucleo`, `construir.py` e `testes`.
5. No terminal do Antigravity, rode `git checkout -b melhoria/metas-bi-ocr` para criar uma branch de trabalho.
6. Leia `README.md`, `PREMISSAS.md` e `sprint.md`. Não edite `index.html`: ele é gerado pelo `construir.py`.
7. Edite as fontes, rode `python construir.py`, abra o `index.html` e rode os testes do app.
8. Faça `git add .`, `git commit -m "..."`, `git push origin melhoria/<tema>` e abra um Pull Request no GitHub. Peça revisão antes do merge.

## 8. Prompt para o Antigravity

```text
Você está no projeto Metas pelo BI (metas-bi-ocr). Leia README.md, PREMISSAS.md e sprint.md.
Não edite index.html. Trabalhe apenas em: Confirmar se o Power BI permite exportar o visual.
Antes de alterar, rode python construir.py e os testes. Depois de alterar, explique o que mudou,
rode os testes de novo e mostre o diff. Não use dados reais nem peça token.
```

**Commit sugerido:** `Metas: integra a exportação real do Power BI`

## 9. Onde pedir ajuda

- Leia `PREMISSAS.md` para saber o que ainda é decisão do setor.
- Leia `sprint.md` para ver o que já foi feito e o que está aberto.
- Abra uma issue no repositório com o print, o passo e a mensagem de erro.
