# Roteiro de aceite e piloto do Controle de Adiantamentos (fictício)

> **Premissa assumida em 30/10/2026.** O piloto de 4 semanas não foi executado.
> Ver [PREMISSAS.md](../../PREMISSAS.md).

## Roteiro do aceite (com a DAS)

1. Abrir `#/config` e carregar os dados fictícios. Conferir a lista de feriados:
   só os **nacionais e estaduais** entram no prazo; o municipal fica na lista
   marcado como "não conta".
2. Em `#/pedido/novo`, registrar um pedido com 3 orçamentos completos, CNPJ
   válido e justificativa com 30 caracteres. Testar um CNPJ inválido: tem que
   recusar (RN01).
3. Em `#/processo/<id>`, avançar as 12 etapas. Antes do "Cadastro no SICAD", o
   app exige o número (RN02). Devolver uma etapa sem motivo: tem que recusar.
4. Conferir o bloco **Prazo**: base de contagem, limite e o selo (no prazo,
   vence em até 7 dias, vencido), com a regra do tipo do processo (RN03).
5. Em `#/processo/<id>/prestacao`, registrar as notas fiscais e comparar a soma
   com o valor concedido (RN06). Abrir uma pendência e conferir o prazo de 10
   dias úteis (RN05). Encerrar com pendência aberta: tem que recusar.
6. Encerrar como "aprovado sem ressalvas" ou "com ressalvas".
7. Abrir `#/painel`: contagens, vencidos, a vencer, gráficos de etapa e tempo.
8. Abrir `#/relatorio`: devoluções por motivo, tempo do pedido ao pagamento,
   exportar o CSV e imprimir em A4.

**Critério de aceite**: 10 dias úteis com feriado no meio dão o limite certo; o
app nunca encerra com pendência aberta nem com nota acima do concedido.

## Piloto de 4 semanas

| Medida | Linha de base | Meta |
|---|---|---|
| Tempo do pedido ao pagamento | 21 dias corridos | 15 dias |
| Devoluções por documento | não medido | reduzir |
| Processos vencidos | não medido | zero |

## Como confirmar

1. Rodar o roteiro com a DAS e com a contabilidade.
2. Confirmar a Orientação Técnica vigente da CGE/MT (premissa: 06/2025).
3. Anotar as datas dos pedidos de 4 semanas e refazer a linha de base.
