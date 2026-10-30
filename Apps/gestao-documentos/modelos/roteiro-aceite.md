# Roteiro de aceite e piloto da Gestão de Documentos (fictício)

> **Premissa assumida em 30/10/2026.** O piloto de 30 dias não foi executado.
> Ver [PREMISSAS.md](../../PREMISSAS.md) e [papeis-e-anexos.md](papeis-e-anexos.md).

## Roteiro do aceite (com o Gabinete)

1. Abrir `#/config` e carregar os dados fictícios.
2. Em `#/processo/novo`, autuar um processo sem os 3 anexos: tem que recusar
   (RN01). Completar e autuar; conferir o número AAAA.NNNN-SD (RN02).
3. Acompanhar o prazo: verde, amarelo a 70% e vermelho a 100% (RN06, RN07).
4. Abrir `#/painel`: a **cobrança automática** aparece para cada processo vencido
   (RN08), uma vez só. Abrir de novo não duplica.
5. Desligar a cobrança de uma lotação e conferir que ela deixa de ser cobrada.
6. Em `#/processo/<id>`, usar as **minutas** (ofício e despacho) e o checklist.
7. Assinar e concluir: sem a conclusão escrita e sem nome e cargo da autoridade,
   o app recusa (RN09). Com tudo, o processo é **notificado e arquivado** (RN10).
8. Conferir a trilha de aprovação e o histórico.
9. Exportar o CSV e imprimir em A4.

**Critério de aceite**: a cobrança não duplica; a conclusão só acontece com
assinatura; o arquivamento registra a notificação ao requerente.

## Piloto de 30 dias

| Medida | Linha de base | Meta |
|---|---|---|
| Tempo da autuação à conclusão | 48 h na triagem (premissa) | 24 h |
| Processos vencidos | não medido | zero |
| Cobranças registradas | manuais | automáticas |
| Processos concluídos com assinatura | não medido | 100% |

## Como confirmar

1. Rodar o roteiro com o Gabinete de Direção.
2. Confirmar a matriz de papéis e quem assina a conclusão.
3. Medir 30 dias e comparar com a linha de base.
