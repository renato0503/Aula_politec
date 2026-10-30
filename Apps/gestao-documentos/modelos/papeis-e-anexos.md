# Regras de negócio e quadro de papéis (fictício)

> **Premissa assumida em 30/10/2026.** A matriz de papéis, quem pode excluir
> documentos e os anexos obrigatórios por tipo de processo não foram confirmados
> com o Gabinete. O que está abaixo é a base de trabalho do app. Ver
> [PREMISSAS.md](../../PREMISSAS.md).

## 1. Quadro de papéis

| Papel | O que faz | O que não faz |
|---|---|---|
| Servidor da lotação | cadastra o processo, instrui, anexa documento, emite minuta | não decide, não exclui |
| Chefia imediata | acompanha a fila, cobra o prazo, redistribui | não conclui |
| Autoridade decisora | decide, assina, conclui e arquiva | não cadastra |

## 2. Quem pode excluir documento

**Ninguém, pela regra do app.** A exclusão é lógica: o documento fica marcado e
continua no histórico. O pedido de exclusão é um evento na trilha, visível para
a chefia. Se a gestão decidir differently, a regra muda em `src/app.js`.

## 3. Anexos obrigatórios por tipo de processo (RN01)

A regra atual é **uma só, para todos os tipos**:

| Anexo | Obrigatório |
|---|---|
| Requerimento | sim |
| Documento de identificação | sim |
| Anexos obrigatórios | sim |

O exemplo tem **1 processo com só 2 anexos**, como exceção do caso de anexo
faltante. A matriz por tipo (pedido de informação, ofício, diligência,etc.) é o
que a premissa não resolve: depende do que o Gabinete usa de verdade.

## 4. Prazos

| Regra | Valor |
|---|---|
| Prazo padrão | 15 dias corridos |
| Prazo suspenso (diligência externa) | 30 dias |
| Sinal amarelo | a partir de 70% do prazo (RN06) |
| Sinal vermelho | a partir de 100% do prazo (RN07) |
| Segregação | o requerente não pode ser o responsável pela instrução (RN05) |

## 5. Linha de base

| Medida | Valor assumido |
|---|---|
| Instrução | 1 h por dia por servidor |
| Volume | 200 processos por mês na lotação |
| Triagem | 48 h entre a autuação e a primeira distribuição |

## 6. Minutas (Sprint 3)

Três modelos, preenchidos com os dados do processo (RN04): ofício de
encaminhamento, ofício de resposta ao requerente e despacho. Sem número,
assunto, requerente, lotação, responsável e data, a emissão é bloqueada.

## Como confirmar

1. Validar a matriz de papéis com o Gabinete.
2. Definir os anexos por tipo de processo.
3. Medir as três medidas de linha de base.
