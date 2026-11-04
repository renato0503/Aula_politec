# Pacote de continuidade · Hórus · Banco de Demandas

**Equipe:** Iohan  
**Tipo:** Aplicativo web  
**Repositório:** https://github.com/renato0503/horus-banco-demandas  
**App publicado:** https://renato0503.github.io/Aula_politec/Apps/horus-banco-demandas/index.html  
**ZIP:** https://github.com/renato0503/horus-banco-demandas/archive/refs/heads/main.zip

## 1. O que este app faz

Banco de demandas de contratações, com cards, ficha e relatório.

## 2. O que já está pronto

- Cadastro da demanda e regras R1 a R8
- Cards, filtros e ficha
- PDF e exportação
- Dados fictícios e testes

## 3. O que falta

- Decidir o papel da versão offline, substituir, complementar ou exercício
- Copiar o esquema real do Hórus e definir o formato de importação
- Definir o relatório e o caminho de volta ao Hórus

## 4. Baixar e abrir no Antigravity

1. Abra https://github.com/renato0503/horus-banco-demandas e aceite o convite de colaborador.
2. Baixe o ZIP em https://github.com/renato0503/horus-banco-demandas/archive/refs/heads/main.zip ou clone com `git clone https://github.com/renato0503/horus-banco-demandas.git`.
3. Extraia em `C:\POLITEC\horus-banco-demandas`.
4. No Antigravity, use **File > Open Folder** e escolha a pasta que tem `app.json`, `src`, `nucleo` e `construir.py`.
5. Abra o terminal e confira `python --version`.
6. Rode `python construir.py`.
7. Abra `index.html` no Edge ou no Chrome e clique em **Configuração > Carregar dados fictícios**.

## 5. Integração que falta, passo a passo

### Esquema do Hórus

1. Copie o DDL das tabelas reais para `horus/esquema.sql`.
2. Compare com o `contexto.md` e ajuste os campos.
3. Crie um arquivo `horus-import-ciclo.json` de exemplo.
4. Teste a importação em um ambiente de teste.

### Relatório

1. Decida entre impressão do navegador e PDF embutido.
2. Inclua o ciclo, o órgão e as linhas das três tabelas.
3. Valide com a equipe do Hórus.
4. Registre o caminho de importação.

## 6. Como testar

```powershell
python construir.py
python testes/testar.py
python testes/cenarios.py
#/demandas e #/demanda/:id
```

Se o teste falhar, leia a primeira mensagem, corrija uma coisa por vez e rode de novo.

## 7. Enviar para o GitHub

1. Entre em https://github.com/renato0503/horus-banco-demandas e aceite o convite de colaborador. Se ainda não recebeu, peça ao professor para enviar de novo.
2. Clique em **Code > Download ZIP** ou clone: `git clone https://github.com/renato0503/horus-banco-demandas.git`. O ZIP serve para abrir e estudar; para enviar alterações, use o clone ou um fork.
3. Extraia em uma pasta curta, por exemplo `C:\POLITEC\horus-banco-demandas`. Evite OneDrive e caminhos com muitos espaços.
4. Abra o **Antigravity**, escolha **File > Open Folder** e selecione a pasta que contém `app.json`, `src`, `nucleo`, `construir.py` e `testes`.
5. No terminal do Antigravity, rode `git checkout -b melhoria/horus-banco-demandas` para criar uma branch de trabalho.
6. Leia `README.md`, `PREMISSAS.md` e `sprint.md`. Não edite `index.html`: ele é gerado pelo `construir.py`.
7. Edite as fontes, rode `python construir.py`, abra o `index.html` e rode os testes do app.
8. Faça `git add .`, `git commit -m "..."`, `git push origin melhoria/<tema>` e abra um Pull Request no GitHub. Peça revisão antes do merge.

## 8. Prompt para o Antigravity

```text
Você está no projeto Hórus · Banco de Demandas (horus-banco-demandas). Leia README.md, PREMISSAS.md e sprint.md.
Não edite index.html. Trabalhe apenas em: Decidir o papel da versão offline, substituir, complementar ou exercício.
Antes de alterar, rode python construir.py e os testes. Depois de alterar, explique o que mudou,
rode os testes de novo e mostre o diff. Não use dados reais nem peça token.
```

**Commit sugerido:** `Hórus: prepara importação do esquema real`

## 9. Onde pedir ajuda

- Leia `PREMISSAS.md` para saber o que ainda é decisão do setor.
- Leia `sprint.md` para ver o que já foi feito e o que está aberto.
- Abra uma issue no repositório com o print, o passo e a mensagem de erro.
