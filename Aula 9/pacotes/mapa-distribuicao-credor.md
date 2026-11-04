# Pacote de continuidade · Mapa de Distribuição

**Equipe:** Igor Henrique  
**Tipo:** Automação de planilhas  
**Repositório:** https://github.com/renato0503/mapa-distribuicao-credor  
**App publicado:** https://renato0503.github.io/Aula_politec/Apps/mapa-distribuicao-credor/index.html  
**ZIP:** https://github.com/renato0503/mapa-distribuicao-credor/archive/refs/heads/main.zip

## 1. O que este app faz

Importa as planilhas e o PDF do pregoeiro, monta o mapa por item e a distribuição orçamentária.

## 2. O que já está pronto

- Importação de `.xlsx`, `.csv` e PDF com camada de texto
- Mapa por item e por órgão
- Resultado, empresas e conferência
- Distribuição orçamentária e mapa SESP

## 3. O que falta

- Receber o `WorkFlow.docx` e o `mapa-manual-referencia.xlsx`
- Confirmar o modelo oficial do mapa SESP
- Conseguir uma amostra real do PDF do pregoeiro
- Fechar os testes contra o gabarito

## 4. Baixar e abrir no Antigravity

1. Abra https://github.com/renato0503/mapa-distribuicao-credor e aceite o convite de colaborador.
2. Baixe o ZIP em https://github.com/renato0503/mapa-distribuicao-credor/archive/refs/heads/main.zip ou clone com `git clone https://github.com/renato0503/mapa-distribuicao-credor.git`.
3. Extraia em `C:\POLITEC\mapa-distribuicao-credor`.
4. No Antigravity, use **File > Open Folder** e escolha a pasta que tem `app.json`, `src`, `nucleo` e `construir.py`.
5. Abra o terminal e confira `python --version`.
6. Rode `python construir.py`.
7. Abra `index.html` no Edge ou no Chrome e clique em **Configuração > Carregar dados fictícios**.

## 5. Integração que falta, passo a passo

### Gabarito e modelo

1. Coloque o gabarito em `modelos/` e compare item a item.
2. Ajuste o mapa orçamentário ao modelo da SESP.
3. Teste um caso de dotação insuficiente.
4. Registre as diferenças encontradas.

### PDF real

1. Peça uma amostra sem dado pessoal.
2. Confira o cabeçalho, as colunas e as linhas de total.
3. Ajuste a associação de colunas se necessário.
4. Rode a conferência e compare com o gabarito.

## 6. Como testar

```powershell
python construir.py
python testes/testar.py
python testes/cenarios.py
#/importar/:proc e #/exportar/:proc
```

Se o teste falhar, leia a primeira mensagem, corrija uma coisa por vez e rode de novo.

## 7. Enviar para o GitHub

1. Entre em https://github.com/renato0503/mapa-distribuicao-credor e aceite o convite de colaborador. Se ainda não recebeu, peça ao professor para enviar de novo.
2. Clique em **Code > Download ZIP** ou clone: `git clone https://github.com/renato0503/mapa-distribuicao-credor.git`. O ZIP serve para abrir e estudar; para enviar alterações, use o clone ou um fork.
3. Extraia em uma pasta curta, por exemplo `C:\POLITEC\mapa-distribuicao-credor`. Evite OneDrive e caminhos com muitos espaços.
4. Abra o **Antigravity**, escolha **File > Open Folder** e selecione a pasta que contém `app.json`, `src`, `nucleo`, `construir.py` e `testes`.
5. No terminal do Antigravity, rode `git checkout -b melhoria/mapa-distribuicao-credor` para criar uma branch de trabalho.
6. Leia `README.md`, `PREMISSAS.md` e `sprint.md`. Não edite `index.html`: ele é gerado pelo `construir.py`.
7. Edite as fontes, rode `python construir.py`, abra o `index.html` e rode os testes do app.
8. Faça `git add .`, `git commit -m "..."`, `git push origin melhoria/<tema>` e abra um Pull Request no GitHub. Peça revisão antes do merge.

## 8. Prompt para o Antigravity

```text
Você está no projeto Mapa de Distribuição (mapa-distribuicao-credor). Leia README.md, PREMISSAS.md e sprint.md.
Não edite index.html. Trabalhe apenas em: Receber o `WorkFlow.docx` e o `mapa-manual-referencia.xlsx`.
Antes de alterar, rode python construir.py e os testes. Depois de alterar, explique o que mudou,
rode os testes de novo e mostre o diff. Não use dados reais nem peça token.
```

**Commit sugerido:** `Mapa: valida o gabarito e o modelo SESP`

## 9. Onde pedir ajuda

- Leia `PREMISSAS.md` para saber o que ainda é decisão do setor.
- Leia `sprint.md` para ver o que já foi feito e o que está aberto.
- Abra uma issue no repositório com o print, o passo e a mensagem de erro.
