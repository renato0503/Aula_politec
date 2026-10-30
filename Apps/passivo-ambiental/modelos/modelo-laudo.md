# Modelo do laudo pericial ambiental (fictício)

> **Premissa assumida em 30/10/2026.** A requisição real anonimizada e o modelo
> de laudo da unidade não chegaram ao grupo. A estrutura abaixo é a que o app
> monta na versão para impressão (`#/pdf/:id`). Ver
> [PREMISSAS.md](../../PREMISSAS.md).

## 1. Requisição pericial (o que o órgão pede)

| Campo | Regra |
|---|---|
| Número do processo/requisição | obrigatório, único (o app recusa repetido) |
| Órgão requisitante | obrigatório |
| Data da requisição | obrigatória, não pode ser futura |
| Tipo de infração ambiental | obrigatório (desmatamento, queimada, extração irregular, ocupação irregular, poluição de curso d'água, mineração irregular) |
| Prazo | 10 dias, no mínimo 1 |
| Local do dano | obrigatório |
| Coordenadas | latitude e longitude, usadas no mapa |

## 2. Cabeçalho do laudo (RN01)

O app preenche o cabeçalho a partir da requisição e deixa dois campos
ajustáveis: **local do dano** e **coordenadas**. São 6 linhas:

1. Número do processo
2. Órgão requisitante
3. Data da requisição
4. Tipo de infração ambiental
5. Local do dano
6. Coordenadas

A versão para impressão só abre com o cabeçalho completo (RN03).

## 3. Conclusão

Texto livre, gravado no laudo. Vai para a versão impressa.

## 4. Mapas anexados (RN02)

Cada mapa tem um **modelo pré-definido** e **5 elementos obrigatórios**:

| Elemento | Exemplo |
|---|---|
| Indicação do norte | seta para o norte no canto |
| Escala gráfica | 1:25.000 |
| Legenda | azul = área danificada; verde = vegetação preservada |
| Data do levantamento | 20/10/2026 |
| Fonte da imagem | imagem de satélite (fictícia) |

E uma medida, conforme o modelo:

| Modelo | Medida |
|---|---|
| Delimitação da área de dano | área em hectares |
| Localização do evento | distância em km |
| Ocupação irregular | área em hectares |
| Faixa de APP e nascente | área em APP, em hectares |

Sem os 6 itens, o mapa é recusado (RN02). Sem mapa, o laudo não é concluído e
não sai para impressão (RN03).

## 5. Linha de base

16 h por laudo, com prazo de 10 dias na requisição. A cronometragem de 5 laudos
reais fica pendente de conferência.

## Como confirmar

1. Trocar arequisição real e o modelo de laudo.
2. Ajustar os modelos e os elementos obrigatórios em `src/sprint3.js`
   (`PA_MODELOS`, `PA_ELEMENTOS`).
3. Cronometrar 5 laudos e corrigir as 16 h.
