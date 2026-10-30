# Regras do semáforo e permissões de escrita (fictício)

> **Premissa assumida em 30/10/2026.** As seis faixas do semáforo, o alerta de
> 90 dias e as permissões de escrita não foram confirmados com a gestão de
> contratos. Ver [PREMISSAS.md](../../PREMISSAS.md).

## 1. As seis faixas

A contagem é regressiva, em dias, até a data de término da vigência:

| Faixa | De | Até | Sinal |
|---|---|---|---|
| Normal | 121 | — | verde |
| Acompanhamento | 91 | 120 | azul |
| Atenção | 61 | 90 | amarelo |
| Providências | 31 | 60 | amarelo |
| Urgente | 0 | 30 | vermelho |
| Vencido | — | -1 | vermelho |

**Fora da contagem**: contrato Encerrado, Rescindido ou Expirado não entra em
nenhuma faixa (R3).

## 2. O alerta de 90 dias

Todo contrato com **até 90 dias** para o fim entra no painel de "vencendo em
90 dias", que é o que a gestão pediu. O alerta também aparece na ficha, com a
contagem de dias restantes.

## 3. A regra do aditivo (R4)

O termo aditivo de prorrogação:
- só existe para contrato **Vigente**;
- só existe se o contrato **permite prorrogação** (R1);
- a nova vigência precisa ser **depois** do término atual;
- a assinatura não pode ser futura;
- ao publicar, a data de término do contrato passa a ser a nova.

## 4. Permissões de escrita

| Papel | Ler | Escrever | Observação |
|---|---|---|---|
| Gestor de contratos | sim | sim | monitora vencimentos, instrui, registra a prorrogação |
| Fiscal do contrato | sim | não | acompanha a vigência do contrato designado |
| Administrador | sim | sim | mantém o cadastro e consulta a trilha de auditoria |

O perfil **fiscal** não altera dados: ele acompanha. Quem registra é o gestor,
e o administrador cuida do cadastro.

## 5. A instrução do processo de renovação (Sprint 3)

O checklist tem 7 itens, 6 obrigatórios:

| Item | Obrigatório |
|---|---|
| Solicitação de renovação assinada | sim |
| Justificativa da necessidade | sim |
| Certidão de regularidade fiscal | sim |
| Certidão de débitos trabalhistas | sim |
| Parecer jurídico | sim |
| Minuta do termo aditivo | sim |
| Publicação do aditivo | não |

O item facultativo **não impede** a conclusão da instrução. A instrução está
completa quando os 6 obrigatórios estão marcados.

O aviso de 60 dias entra para o contrato **Vigente** que vence em até 60 dias
e ainda não tem a instrução completa.

## 6. Repositório de documentos

Os documentos ficam no navegador, no store `anexos`. Cada um tem visibilidade:
`todos` (todos os perfis) ou `gestao` (só gestor e administrador).

## Como confirmar

1. Confirmar as seis faixas e o alerta de 90 dias com a gestão.
2. Confirmar a matriz de permissões de escrita.
3. Confirmar os itens do checklist de instrução.
