# Relatório do banco de demandas (fictício)

> **Premissa assumida em 30/10/2026.** O relatório que acompanha o envio ainda não
> chegou ao grupo. A estrutura abaixo é a que o app monta na tela e que o
> `@media print` transforma em página A4. Ver [PREMISSAS.md](../../PREMISSAS.md).

## 1. Relatório do ciclo

| Campo | Valor |
|---|---|
| Órgão | POLITEC/MT (fictício) |
| Diretoria | Diretoria Metropolitana de Criminalística (fictícia) |
| Ciclo | PCA 2027, ativo |
| Período | 2027 |

## 2. Demandas por grupo

| Grupo | Quantidade | Valor estimado |
|---|---|---|
| Custeio | 8 | R$ 21.400,00 |
| Investimento | 7 | R$ 486.900,00 |

## 3. Demandas por unidade

| Unidade | Sigla | Custeio | Investimento |
|---|---|---|---|
| Laboratório de Química Forense | LQF | 4 | 1 |
| Laboratório de Genética Forense | LGF | 2 | 2 |
| Identificação Civil | IC | 1 | 2 |
| Custódia Definitiva | CD | 1 | 2 |

## 4. Manifestações de interesse

| Demanda | Unidade | Quantidade | Justificativa |
|---|---|---|---|
| Reagente luminol | LGF | 100 | A unidade usa o mesmo reagente nas triagens |

## 5. Regras aplicadas

- **RN01**: grupo CUSTEIO ou INVESTIMENTO, com especificação técnica obrigatória.
- **RN03**: a manifestação exige unidade, quantidade e justificativa.
- **RN04**: o ciclo fica aberto para inscrição até a data limite.
- **RN06**: PDF do orçamento até 10 MB, opcional.
- **RN08**: a estimativa é em centavos, para não perder centavo.

## 6. Decisão de projeto

O relatório é **imprimível** (`@media print`), não um PDF gerado por biblioteca.
A tela de relatório sai pelo botão "Imprimir" do navegador, que permite
"Salvar como PDF". Não há jsPDF embutido: a biblioteca pesaria mais que o app
todo e o resultado seria o mesmo.

Ver [print-relatorio.md](print-relatorio.md) com o passo a passo do print.
