# Roteiro de aceite e piloto da RNC (fictício)

> **Premissa assumida em 30/10/2026.** O piloto de 30 dias na Diretoria de
> Laboratório Forense não foi executado. Ver [PREMISSAS.md](../../PREMISSAS.md).

## Roteiro do aceite

1. Abrir `#/config` e carregar os dados fictícios.
2. Abrir `#/importar`, escolher a planilha do Forms e conferir a associação das
   colunas. As colunas de dado pessoal (nome, matrícula, CPF) aparecem como
   **descartadas** (RN07) e não podem ser associadas.
3. Importar e conferir o relatório: novas, existentes, recusadas e alertas.
4. Abrir uma RNC em `#/rnc/<número>` e aprovar; pedir complemento em outra e
   verificar que, sem resposta em 5 dias, ela é anulada (RN02).
5. Registrar o plano de ação (prorrogação só com justificativa, RN03) e a
   avaliação de eficácia.
6. Abrir `#/exportar`, gerar o arquivo do setor e conferir que ele traz **só**
   as RNCs daquele setor (RN06).
7. Entrar como perfil Setor, em `#/minhas`, registrar o plano (FOR 2) e a
   avaliação (FOR 3).
8. Importar o arquivo devolvido em `#/exportar` e conferir a mesclagem.
9. Abrir `#/painel` e conferir os três gráficos, as vencidas, o tempo por etapa
   e a recorrência (RN05).

**Critério de aceite**: nenhuma etapa gera erro no console; o arquivo do setor
não leva RNC de outro setor; a RNC grave é encaminhada à corregedoria.

## Piloto de 30 dias

| Medida | Linha de base | Meta |
|---|---|---|
| RNCs registradas no mês | pelo formulário do Google | as mesmas, importadas pelo app |
| Tempo de validação | 2 dias úteis (premissa) | 2 dias úteis |
| Plano de ação enviado no prazo | não medido | 100% dentro de 30 dias |
| Etapas vencidas | não medido | abaixo de 10% |

## Como confirmar

1. Rodar o roteiro com a CQUAL e com os setores da DLF.
2. Assinar o aceite e atualizar `PROJETO.md` e `README.md`.
3. Medir 30 dias e comparar com a linha de base.
