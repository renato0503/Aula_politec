# Mapa de Equipamentos · como usar

O app reúne os equipamentos da POLITEC/MT, os contratos de manutenção, as
paradas e o custo de cada parada, e mostra tudo no mapa de Mato Grosso. É um
arquivo só (`index.html`), funciona sem internet e guarda os dados apenas no
navegador deste computador.

## Abrir

1. Dê dois cliques em `index.html` (Edge ou Chrome).
2. Escolha o perfil no alto da tela: **Coordenadoria**, **Unidade** ou
   **Diretoria**.
3. Para conhecer o app, abra **Configuração** e clique em
   **Carregar dados fictícios**.

## Na unidade

1. Em **Configuração**, escolha a **unidade dona** desta cópia.
2. Cadastre os equipamentos em **Equipamentos**, com a foto e o bairro (distrito).
3. Quando um equipamento parar, abra a parada em **Paradas**. Quando voltar,
   feche a parada.
4. Toda semana, em **Exportar**, clique em **Baixar o .json da base** e envie o
   arquivo à coordenadoria. Ele vai só com a sua unidade. Desmarque **com as
   fotos** se o arquivo ficar grande para o e-mail.

## Na coordenadoria

1. Em **Importar**, escolha o `.json` de cada unidade. Quando o mesmo
   equipamento mudou dos dois lados, o app mostra os campos em conflito e você
   escolhe a versão de cada um. Nenhum equipamento é duplicado.
2. Defina em **Configuração** o valor de referência por atendimento e o custo
   alternativo por dia. Eles entram no custo da parada.
3. Acompanhe o **Painel**. Clique num indicador para abrir o mapa já filtrado.
4. Para o Google Earth, em **Exportar**, baixe o `.kmz`. Para QGIS, ArcGIS ou
   Google Earth Engine, baixe o GeoJSON.

## Backup

Os dados ficam só neste navegador. Por isso, toda semana, abra
**Configuração** e clique em **Exportar backup (.json)**.

## O que não fazer

- Não escreva CPF, nome de servidor ou dado de pessoa atendida nos campos de
  texto. O app avisa quando encontra um número com formato de CPF (RN09).
- Não limpe os dados do navegador sem antes exportar o backup.
- Não edite o `index.html`: ele é gerado pelo `construir.py`.
