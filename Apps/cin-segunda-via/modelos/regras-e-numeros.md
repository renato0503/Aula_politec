# Regras da CIN, elegibilidade e volume (fictício)

> **Premissa assumida em 30/10/2026.** As regras oficiais da segunda via e a
> fonte dos números não foram confirmados pelo regional. Ver
> [PREMISSAS.md](../../PREMISSAS.md).

## 1. Quem pode pedir a segunda via online

O pedido é admitido quando **as 3 condições**-valem:

| Condição | Regra |
|---|---|
| Primeira via válida | a validade da CIN ainda não passou |
| Nenhum dado mudou | nome, estado civil e filiação iguais aos do cadastro |
| CPF válido | com dígito verificador (RN01) |

Com dado alterado, o cidadão **vai ao posto**. Com a CIN vencida, o pedido é
feito no posto (RN03).

## 2. A validade do cadastro

**15 dias** é a validade do cadastro no posto. O app mostra a validade da CIN
informada pelo cidadão e recusa o pedido quando ela já passou.

## 3. O volume

**21.000 por mês** é o volume de emissões de CIN no estado. Serve de
referência para o dimensionamento do piloto, não de meta do app.

## 4. O que o app não faz

**Não há integração com a coleta biométrica.** O app é um protótipo offline:
o atendimento é registrado à mão no sistema oficial e o app serve para
organizar a fila e o prazo. A posição está registrada em `contexto.md`.

## 5. Fotos

As fotos do exemplo são **geradas no navegador**, com o texto "FOTO DE TESTE"
desenhado, sem nenhuma pessoa real (LGPD, art. 11). O app reduz a imagem para
800 px antes de guardar.

## 6. Fila do servidor

O Sprint 3 traz a fila: o servidor aceita (com conferência da foto) ou recusa
**com motivo**. Os motivos de recusa do exemplo: foto ilegível, divergência de
dados e documento incorreto.

## Como confirmar

1. Confirmar as regras oficiais de dispensa de nova coleta.
2. Indicar a fonte oficial dos números (15 dias e 21.000 por mês).
3. Registrar a posição da TI sobre a integração com a coleta biométrica.
