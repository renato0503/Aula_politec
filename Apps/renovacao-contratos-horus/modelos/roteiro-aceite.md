# Roteiro de aceite e piloto da Renovação de Contratos (fictício)

> **Premissa assumida em 30/10/2026.** O piloto de 30 dias não foi executado.
> Ver [PREMISSAS.md](../../PREMISSAS.md) e
> [semaforo-e-permissoes.md](semaforo-e-permissoes.md).

## Roteiro do aceite (com a gestão de contratos)

1. Abrir `#/config` e carregar os dados fictícios (15 contratos).
2. Em `#/contrato/novo`, cadastrar um contrato: a data de término é calculada
   pelos meses (R2) e pode ser ajustada. CNPJ inválido tem que recusar.
3. Em `#/painel`, conferir o **semáforo de seis faixas**, os vencendo em 90 dias,
   o **valor em risco** e o tempo médio até a renovação.
4. Em `#/contrato/<id>`, registrar o **checklist de instrução** (R7) e conferir o
   aviso de contrato sem instrução a 60 dias.
5. Guardar um documento em **repositório local** com visibilidade restrita (R8) e
   conferir que o perfil fiscal não o vê.
6. Registrar um **termo aditivo** de prorrogação: a vigência muda e o contrato
   continua "Vigente" (R4).
7. Registrar um **reajuste** com memória de cálculo. Testar 30%: tem que exceder
   o limite legal (art. 125 da Lei nº 14.133/2021). Com 5%, percorrer o fluxo
   solicitado → em análise → aprovado → aplicado e conferir o novo valor.
8. **Substituir o fiscal** e conferir o histórico (o anterior fica com data de
   saída) e a auditoria (R6).
9. Exportar o CSV e imprimir em A4.

**Critério de aceite**: o ajuste acima de 25% é recusado; o fiscal antigo fecha
com data; a auditoria registra autor e data de cada evento.

## Piloto de 30 dias

| Medida | Linha de base | Meta |
|---|---|---|
| Contratos monitorados no semáforo | planilha manual | 100% |
| Renovações fora da janela de 90 dias | não medido | zero |
| Ajustes com memória de cálculo | não medido | 100% |
| Instrução completa a 60 dias do fim | não medido | 100% |

## Como confirmar

1. Rodar o roteiro com a gestão de contratos.
2. Confirmar as seis faixas e o alerta de 90 dias.
3. Confirmar a matriz de escrita (autor, chefia, gestor) e a do fiscal.
