# Categorias, conservação e capacidade dos contêineres (fictício)

> **Premissa assumida em 30/10/2026.** A conferência com a equipe da custódia não
> aconteceu. As categorias, as condições de conservação e as capacidades abaixo
> são a base de trabalho do app. Ver [PREMISSAS.md](../../PREMISSAS.md).

## 1. Categorias de vestígio

| Categoria | Condição de conservação | Restrição |
|---|---|---|
| Roupas e têxteis | ambiente seco e arejado | sem contato com líquido |
| Material biológico | geladeira de 2 a 8 °C | não congela |
| Armas e munição | armaria com controle de acesso | dupla custódia na entrada e na saída |
| Material perigoso | recipiente próprio, sinalizado | descarte por empresa licenciada |
| Papéis e documentos | sala cofre, com controle de umidade | acesso registrado |

## 2. Contêineres

| Contêiner | Categoria que aceita | Capacidade | Localização física |
|---|---|---|---|
| C-01 | todas | 300 L | Sala cofre A |
| C-02 | roupas e têxteis | 200 L | Depósito seco B |
| C-03 | material biológico | 120 L | Geladeira G-1 |
| C-04 | armas e munição | 80 L | Armaria |
| C-05 | material perigoso | 60 L | Depósito de reagentes |

O app recusa a transferência para um contêiner que não aceite a categoria
(RN02) e para um contêiner sem folga de volume (RN03).

## 3. Medição

| Medida | Valor assumido |
|---|---|
| Unidade de volume | litro (2 L por item típico) |
| Tempo de recebimento | 40 min |
| Tempo de localização no acervo | 15 min |

O histórico mensal (`historico_mensal`) guarda entradas, saídas e a ocupação
final de cada mês.

## Como confirmar

1. Conferir as categorias, a condição de conservação e as restrições.
2. Medir o volume real de um contêiner e de um vestígio.
3. Cronometrar o recebimento e a localização.
