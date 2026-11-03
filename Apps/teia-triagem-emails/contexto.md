# Contexto técnico do TEIA

## Fluxo

1. A pessoa abre a bancada e escolhe um e-mail da fila.
2. O painel mostra a mensagem, os anexos, os 8 campos, a confiança e os alertas.
3. O triador corrige o que faltar e salva.
4. Se houver divergência ou PDF imagem, trata o alerta.
5. A validação é humana, com perfil e data/hora na trilha.
6. A planilha consolidada exporta CSV com BOM e ponto e vírgula.

## Banco (IndexedDB)

| Store | Chave | Uso |
|---|---|---|
| `emails` | `id` | mensagens, anexos, campos, status e alerta |
| `anexos` | `id` | reservado para metadados de anexos |
| `extracao` | `id` | resultado da extração por e-mail |
| `lotes` | `id` | rodadas de extração |
| `log` | `id` | auditoria de cada ação |

## Rotas

`#/painel`, `#/email/:id`, `#/lote`, `#/planilha`, `#/config`, `#/testes`.

## Regras no código

- 8 campos: DATA COBRANÇA, Nº COBRANÇAS, NÍVEL, TIPO DE CRIME, PROTOCOLO, AR PARA CONFRONTO, OBJETIVO CLARO e NOME DA REGIONAL.
- Campo vazio deixa o e-mail `pendente` e bloqueia a validação.
- `divergencia` e `ocr` viram alerta e exigem "Tratar alerta".
- A validação só acontece com os 8 campos e sem alerta.
- O status `validado` grava `validado_por` e `validado_em`.
- O CSV sai em `;` com BOM; nenhuma requisição de rede é feita.

## Extração simulada

O seed traz `campos`, `confianca` e `alerta` por e-mail. O botão "Extrair" copia
esses valores para `extracao` e deriva a situação. O script local faria o
parsing, o OCR e a renomeação; o protótipo mostra o resultado e o ponto de
validação humana.
