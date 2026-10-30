# Regras do RNC, categorias e gravidades (fictício)

> **Premissa assumida em 30/10/2026.** As categorias, as gravidades e o cabeçalho
> do formulário do Google não foram confirmados com a CQUAL. Ver
> [PREMISSAS.md](../../PREMISSAS.md).

## 1. Setores

6 setores da Diretoria de Laboratório Forense:

| Sigla | Nome |
|---|---|
| LQF | Laboratório de Química Forense |
| LGF | Laboratório de Genética Forense |
| LTX | Laboratório de Toxicologia |
| REC | Recepção de vestígios |
| ALM | Almoxarifado |
| CUS | Central de Custódia |

## 2. Categorias

As 6 categorias do formulário do Google:

1. Cadeia de custódia
2. Registro incompleto
3. Equipamento sem calibração
4. Prazo de laudo
5. Armazenamento de amostra
6. Biossegurança

## 3. Gravidades

**3 gravidades: leve, moderada e grave.** A RNC grave é encaminhada à
corregedoria e não fecha na unidade.

## 4. Etapas e prazos

| Etapa | Prazo assumido |
|---|---|
| Validação | 2 dias úteis |
| Plano | 5 dias úteis |
| Avaliação | 3 dias úteis |
| Encerramento | 1 dia útil |

A RNC que passa do prazo da etapa entra na cobrança da CQUAL.

## 5. O cabeçalho do formulário do Google

O cabeçalho que o app importa é:

```
Carimbo de data/hora;Setor relator;Setor notificado;Categoria;Descrição da ocorrência;Gravidade;Número
```

A planilha de exemplo fica em `exemplos/respostas-forms-ficticio.csv`. A
importação recusa linha sem categoria, sem setor relator ou com gravidade fora
das 3 (RN01, RN07).

## 6. Linha de base

20 RNCs de exemplo, com as 4 etapas preenchidas e as datas de início e fim de
cada uma.

## Como confirmar

1. Listar com a CQUAL as categorias e as gravidades reais.
2. Copiar o cabeçalho real da planilha de respostas do Forms.
3. Medir o tempo de cada etapa e as cobranças da CQUAL no primeiro mês.
