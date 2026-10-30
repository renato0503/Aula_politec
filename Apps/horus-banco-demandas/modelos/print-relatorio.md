# Print do relatório do banco de demandas (fictício)

> **Premissa assumida em 30/10/2026.** O print de tela que acompanha o envio não
> chegou ao grupo. O passo a passo abaixo é o que o app espera que o servidor
> faca. Ver [relatorio.md](relatorio.md).

## Passo a passo

1. Abrir o app em `#/banco` e escolher o ciclo ativo (PCA 2027).
2. Abrir a tela de relatório do ciclo.
3. No navegador, usar **Ctrl + P** (ou Cmd + P no macOS).
4. Em "Destino", escolher **Salvar como PDF**.
5. Em "Mais configurações":
   - **Destino**: Salvar como PDF
   - **Margens**: Mínimo
   - **Gráficos**: Ativos
   - **Cabeçalhos e rodapés**: desmarcar
   - **Escala**: 100%
6. Confirmar em "Salvar" e anexar o arquivo ao envio.

## O que sai no papel

- A faixa do governo e o menu do app **não** saem (o CSS de impressão esconde).
- O cabeçalho institucional (`POLITEC/MT · SESP/MT · Governo de Mato Grosso`)
  sai no topo de cada página.
- Os quadros de dados saem com a borda, sem sombra.
- A quebra de página é evitada dentro de cada cartão.

## Se o servidor preferir

Se a impressão pelo navegador ficar ruim na impressora da unidade, o app aceita
a troca por **jsPDF embutido** (RN de relatório). A decisão fica registrada em
[PREMISSAS.md](../../PREMISSAS.md).
