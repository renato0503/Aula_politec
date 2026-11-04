# Pacote de continuidade · Mapa de Equipamentos

**Equipe:** João Lucas  
**Tipo:** Aplicativo web e mapa  
**Repositório:** https://github.com/renato0503/equipamentos-google-earth  
**App publicado:** https://renato0503.github.io/Aula_politec/Apps/equipamentos-google-earth/index.html  
**ZIP:** https://github.com/renato0503/equipamentos-google-earth/archive/refs/heads/main.zip

## 1. O que este app faz

Equipamentos da POLITEC por unidade, contratos, paradas e mapa no Google Earth.

## 2. O que já está pronto

- Unidades, equipamentos, contratos e paradas
- Mapa com filtros, zoom, distritos e painel
- KMZ, KML, GeoJSON e link do Google Maps
- Gráficos, custos e privacidade

## 3. O que falta

- Testar o `.kmz` no Google Earth Pro e no Web
- Confirmar a base de diretorias, unidades e equipamentos
- Escolher as 3 unidades do piloto e medir a linha de base

## 4. Baixar e abrir no Antigravity

1. Abra https://github.com/renato0503/equipamentos-google-earth e aceite o convite de colaborador.
2. Baixe o ZIP em https://github.com/renato0503/equipamentos-google-earth/archive/refs/heads/main.zip ou clone com `git clone https://github.com/renato0503/equipamentos-google-earth.git`.
3. Extraia em `C:\POLITEC\equipamentos-google-earth`.
4. No Antigravity, use **File > Open Folder** e escolha a pasta que tem `app.json`, `src`, `nucleo` e `construir.py`.
5. Abra o terminal e confira `python --version`.
6. Rode `python construir.py`.
7. Abra `index.html` no Edge ou no Chrome e clique em **Configuração > Carregar dados fictícios**.

## 5. Integração que falta, passo a passo

### Google Earth

1. Abra o app e exporte o `.kmz` em `#/exportar`.
2. Abra no Google Earth Pro e no Web.
3. Confira os pinos, as fotos e o balão de cada equipamento.
4. Registre o resultado em `modelos/roteiro-aceite.md` e abra issue se algo falhar.

### Base real

1. Importe a planilha das unidades do piloto.
2. Complete fotos e contratos de 10 equipamentos.
3. Registre uma parada e confira o custo no painel.
4. Não use CPF ou dado pessoal de servidor.

## 6. Como testar

```powershell
python construir.py
python testes/testar.py
python testes/cenarios.py
#/mapa, #/exportar e #/painel
```

Se o teste falhar, leia a primeira mensagem, corrija uma coisa por vez e rode de novo.

## 7. Enviar para o GitHub

1. Entre em https://github.com/renato0503/equipamentos-google-earth e aceite o convite de colaborador. Se ainda não recebeu, peça ao professor para enviar de novo.
2. Clique em **Code > Download ZIP** ou clone: `git clone https://github.com/renato0503/equipamentos-google-earth.git`. O ZIP serve para abrir e estudar; para enviar alterações, use o clone ou um fork.
3. Extraia em uma pasta curta, por exemplo `C:\POLITEC\equipamentos-google-earth`. Evite OneDrive e caminhos com muitos espaços.
4. Abra o **Antigravity**, escolha **File > Open Folder** e selecione a pasta que contém `app.json`, `src`, `nucleo`, `construir.py` e `testes`.
5. No terminal do Antigravity, rode `git checkout -b melhoria/equipamentos-google-earth` para criar uma branch de trabalho.
6. Leia `README.md`, `PREMISSAS.md` e `sprint.md`. Não edite `index.html`: ele é gerado pelo `construir.py`.
7. Edite as fontes, rode `python construir.py`, abra o `index.html` e rode os testes do app.
8. Faça `git add .`, `git commit -m "..."`, `git push origin melhoria/<tema>` e abra um Pull Request no GitHub. Peça revisão antes do merge.

## 8. Prompt para o Antigravity

```text
Você está no projeto Mapa de Equipamentos (equipamentos-google-earth). Leia README.md, PREMISSAS.md e sprint.md.
Não edite index.html. Trabalhe apenas em: Testar o `.kmz` no Google Earth Pro e no Web.
Antes de alterar, rode python construir.py e os testes. Depois de alterar, explique o que mudou,
rode os testes de novo e mostre o diff. Não use dados reais nem peça token.
```

**Commit sugerido:** `Equipamentos: registra o teste no Google Earth`

## 9. Onde pedir ajuda

- Leia `PREMISSAS.md` para saber o que ainda é decisão do setor.
- Leia `sprint.md` para ver o que já foi feito e o que está aberto.
- Abra uma issue no repositório com o print, o passo e a mensagem de erro.
