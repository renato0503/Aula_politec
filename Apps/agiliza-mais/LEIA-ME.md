# Agiliza + · como usar

O Agiliza + monta o laudo de exame em aparelho celular a partir da pasta da
extração. É um arquivo só (`index.html`), funciona sem internet e guarda os
dados apenas no navegador deste computador.

## Abrir

1. Dê dois cliques em `index.html`. Use o Edge ou o Chrome, porque eles
   permitem escolher a pasta e gravar o laudo dentro dela.
2. Para conhecer o app sem um caso real, clique em **Carregar caso de exemplo**
   na tela **Casos**.

## Fazer um laudo (seis passos, à esquerda da tela)

1. **Pasta do caso**: selecione a pasta com a requisição em PDF, o
   `DEVICE INFO.txt`, o `HASHDOHASH.txt` e as pastas `OBJ 01-A`. O app só lê a
   pasta e não altera os originais.
2. **Conferência**: clique em **Ler os dados da requisição em PDF**. Em seguida,
   confira cada campo com a origem ao lado e corrija o que precisar. O botão
   **Confirmar todos os campos** só libera com o IMEI 1 e o hash válidos. Se o
   PDF for digitalizado, o app avisa, e você digita os campos com o PDF aberto
   ao lado.
3. **Textos**: escolha o texto de cada seção. A prévia já traz os dados do caso.
4. **Quesitos**: use os quesitos lidos da requisição ou cole a lista. O app
   sugere a resposta, mas a sugestão só entra no laudo depois que você marca
   **resposta aprovada pelo perito**.
5. **Gerar laudo**: informe o número do laudo e o seu nome. Se não houver
   bloqueio, clique em **Gerar o .docx**. O arquivo vai para a pasta
   `LAUDO_GERADO` do caso, quando o navegador permite, ou para Downloads.
6. **Revisão final**: depois de revisar no Word, anote as correções e marque a
   revisão. Só essa marcação conclui o caso e para o cronômetro.

## Backup

Os dados ficam só neste navegador. Por isso, toda semana, abra
**Configuração** e clique em **Exportar backup (.json)**. Para voltar os dados,
use **Importar backup** na mesma tela.

## O que não fazer

- Não limpe os dados do navegador sem antes exportar o backup.
- Não edite o `index.html`: ele é gerado pelo `construir.py`.
- Não use o modelo fictício em laudo real. Carregue o modelo institucional com
  os marcadores em **Configuração** (lista em `modelos/MARCADORES.md`).
- Depois de entregue o laudo, use **Histórico › Limpar os dados do caso**. As
  métricas ficam, e os dados do aparelho saem (LGPD).
