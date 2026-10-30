# Roteiro de aceite e piloto da TCIN (fictício)

> **Premissa assumida em 30/10/2026.** O piloto de 30 dias não foi executado.
> Ver [PREMISSAS.md](../../PREMISSAS.md), [marcos-e-livros.md](marcos-e-livros.md)
> e [privacidade.md](privacidade.md).

## Roteiro do aceite (com o IML)

1. Abrir `#/config` e carregar os dados fictícios (12 corpos e as 5 situações).
2. Em `#/corpo/novo`, registrar um acionamento. Repetir o protocolo: tem que
   recusar (RN01).
3. Registrar os **quatro marcos** na ordem, com data e perfil (RN03).
4. Mudar a situação: para "não identificado" e "não reclamado" o motivo é
   obrigatório; "em custódia" exige identificação; a identificação exige o
   método (papiloscopia, DNA, odontologia, familiar ou documento).
5. Em `#/busca`, buscar por protocolo, nome, documento e lacre (RN04).
6. No corpo identificado, preencher o **auto de entrega** (responsável,
   documento e data) e registrar a liberação. Sem identificação, o botão fica
   bloqueado (RN02).
7. Abrir `#/painel`: tempo médio de remoção, identificação e liberação,
   permanência por corpo e alerta de passagem de plantão.
8. Exportar o CSV e imprimir em A4.
9. Em um caso liberado, usar **Apagar os dados deste caso** e conferir que a
   contagem ficou.

**Critério de aceite**: o painel não mostra nome completo (RN05); a liberação
exige identificação e auto; o caso em andamento não pode ser apagado.

## Piloto de 30 dias

| Medida | Linha de base | Meta |
|---|---|---|
| Remoção | 4 h (premissa) | 4 h |
| Identificação | 48 h (premissa) | 48 h |
| Liberação | 72 h (premissa) | 72 h |
| Corpos sem movimentação em 12 h | não medido | alerts tratados no plantão |

## Como confirmar

1. Rodar o roteiro com o IML e com a equipe do plantão.
2. Confirmar o nome do projeto (TCIN ou CNC) e os 4 marcos.
3. Medir as três medidas e o prazo de retenção.
