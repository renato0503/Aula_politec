# Roteiro de aceite e piloto do DOCUMENTAPOLITEC (fictício)

> **Premissa assumida em 30/10/2026.** O piloto de 30 dias com 2.400 prontuários
> não foi executado. Ver [PREMISSAS.md](../../PREMISSAS.md) e
> [modelo-caixa.md](modelo-caixa.md).

## Roteiro do aceite (com a DMIT)

1. Abrir `#/config` e carregar os dados fictícios (12 caixas, 135 prontuários).
2. Em `#/caixa/nova`, cadastrar uma caixa com a relação. Repetir um prontuário:
   tem que recusar (RN01). Usar um prontuário de outra caixa: também recusa.
3. Em `#/caixa/<id>`, conferir a relação: sem divergência, a caixa é **conferida
   e lacrada**; com prontuário ausente no arquivo digital, fica **com
   divergência** e sem lacre (RN02).
4. Conferir a **etiqueta**: código de conferência e código de barras. Digitar um
   código errado (tem que recusar) e o código certo (tem que aceitar e registrar
   no histórico).
5. Em `#/busca-nome` (perfil gestor), carregar o **índice autorizado** e buscar
   pelo nome. Conferir que o app guarda só o hash e que a consulta entra na
   trilha (RN03).
6. Entrar como papiloscopista e conferir que a busca por nome fica bloqueada.
7. Em `#/importar`, importar a planilha de 850 prontuários e o índice do arquivo
   digital; conferir o relatório de aceitas, recusadas e divergentes.
8. Abrir `#/painel`: caixas conferidas e pendentes, espaço liberado, tempo médio
   de conferência e prontuários por período. Exportar CSV e imprimir em A4.
9. Imprimir em lote as etiquetas das caixas pendentes.

**Critério de aceite**: nenhuma caixa lacra com divergência; o código de
conferência muda quando a relação muda; o nome do cidadão nunca aparece em claro
no banco do app.

## O que falta implementar (depende de biblioteca)

| Item | Por quê |
|---|---|
| QR Code na etiqueta | precisa de biblioteca embutida (`qrcode.min.js`) |
| Leitura do QR pela câmera | depende da mesma biblioteca e de HTTPS |

O app já entrega o código de conferência, o código de barras Code 39 (legível por
qualquer leitor) e a leitura digitada. O passo a passo está no botão escondido
(três cliques no nome do app, no rodapé).

## Piloto de 30 dias

| Medida | Linha de base | Meta |
|---|---|---|
| Caixas conferidas no mês | não medido | 100% das recebidas |
| Tempo de conferência | não medido | medir e reduzir |
| Espaço liberado | não medido | 1 caixa a cada 12 prontuários |
| Consultas por nome com trilha | não existia | 100% |

## Como confirmar

1. Rodar o roteiro com a DMIT e com a equipe do arquivo.
2. Confirmar o formato do número do prontuário e o modelo da caixa.
3. Decidir sobre o índice autorizado de nomes (base legal e quem acessa).
