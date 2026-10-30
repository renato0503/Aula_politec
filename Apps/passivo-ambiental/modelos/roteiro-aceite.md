# Roteiro de aceite e piloto do Passivo Ambiental (fictício)

> **Premissa assumida em 30/10/2026.** O piloto com 5 laudos reais não foi
> executado. Ver [PREMISSAS.md](../../PREMISSAS.md) e
> [modelo-laudo.md](modelo-laudo.md).

## Roteiro do aceite (com o perito)

1. Abrir `#/config` e carregar os dados fictícios (12 requisições, 2 laudos
   concluídos).
2. Em `#/requisicao/nova`, registrar a requisição com número único: repetir o
   número tem que recusar. O laudo abre com o cabeçalho preenchido (RN01).
3. Em `#/laudo/<id>`, anexar pelo menos 1 **mapa temático** com os 5 elementos
   obrigatórios (RN02) e tentar concluir sem mapa: tem que bloquear (RN03).
4. Preencher a **assinatura** (nome e cargo/matrícula) e concluir. A requisição
   passa para concluída e a assinatura fica registrada.
5. Abrir `#/pdf/<id>`: a versão para impressão só abre com cabeçalho completo e
   mapa anexado (RN03).
6. Em `#/painel`, conferir a **fila priorizada** (atraso e depois complexidade),
   o alerta de prazo, o tempo médio do laudo e as horas médias contra a meta de
   12 h.
7. Exportar o CSV de produtividade e imprimir em A4.

**Critério de aceite**: nenhum laudo conclui sem mapa, sem cabeçalho ou sem
assinatura; a fila começa pelo atrasado de maior complexidade.

## Piloto com 5 laudos

| Medida | Linha de base | Meta |
|---|---|---|
| Horas por laudo | 16 h (premissa) | 12 h |
| Tempo da requisição à conclusão | não medido | 10 dias |
| Laudos com mapa completo | não medido | 100% |
| Laudos fora do prazo | não medido | zero |

## Como confirmar

1. Rodar o roteiro com o perito da unidade.
2. Cronometrar 5 laudos e corrigir a linha de base de 16 h.
3. Confirmar o modelo de mapa (norte, escala, área) com o perito.
