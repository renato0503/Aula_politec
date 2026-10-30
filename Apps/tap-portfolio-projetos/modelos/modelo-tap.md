# Modelo do TAP (fictício)

> **Premissa assumida em 30/10/2026.** O modelo vigente do TAP e a lista oficial
> de documentos não chegaram ao grupo. A estrutura abaixo é a que o app valida
> (RN01 e RN02). Ver [PREMISSAS.md](../../PREMISSAS.md).

## Identificação

| Campo | Regra do app | Observação |
|---|---|---|
| Título | 10 a 120 caracteres | obrigatório |
| Unidade | da lista de unidades | obrigatório |
| Responsável | nome e contato | obrigatório |
| Objetivo | 30 a 600 caracteres | obrigatório |
| Justificativa | 30 a 600 caracteres | obrigatório |
| Objetivo estratégico | texto livre | obrigatório |
| Valor estimado | número positivo, em R$ | obrigatório |
| Prazo | 1 a 60 meses | obrigatório |

## Documentos (RN01)

| Documento | Obrigatório | Observação |
|---|---|---|
| Pesquisa de preços | sim | com 3 cotações e a memória de cálculo |
| Estudo técnico | sim | com a memória de cálculo |
| Anuência da chefia | sim | assinatura eletrônica ou física |
| Cronograma | não | entra depois, na análise |
| Fotos | não | material de apoio |

O app recusa o envio enquanto faltar qualquer documento obrigatório.

## Fluxo

1. **Submetido** — a proposta entra com o pacote de documentos.
2. **Em triagem** — o gestor classifica, pede complementação ou recusa com
   motivo (RN05, RN06).
3. **Decidido** — a autoridade decide: aprovar, aprovar com condição ou recusar.
4. **No portfólio** — a proposta aprovada entra no portfólio com prioridade,
   fonte de recurso e situação de captação.

## Linha de base

8 propostas de exemplo, com prazo de captação de 4 meses e priorização em 3
faixas. A medição de 4 semanas de registro fica pendente de conferência.

## Como confirmar

1. Trocar este arquivo pelo modelo oficial.
2. Ajustar os limites de tamanho em `src/app.js` (RN01, RN02).
3. Ajustar a lista de documentos no store `documentos`.
