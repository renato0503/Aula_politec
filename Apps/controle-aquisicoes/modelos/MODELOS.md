# Modelos de referência do processo de aquisição (fictícios)

> **Premissa assumida em 30/10/2026.** O modelo oficial ainda não chegou ao
> grupo. Os textos abaixo descrevem a estrutura mínima que o app exige em cada
> etapa, com base na Lei nº 14.133/2021 e no fluxo de 9 etapas desenhado no
> `contexto.md`. Servem para testar o app e para conferir com a Coordenadoria de
> Aquisições o que precisa mudar. Ver [PREMISSAS.md](../../PREMISSAS.md).

## 1. Documento de Formalização da Demanda (DFP)

O app exige o DFD na etapa **DFD** (RN02). Estrutura:

| Seção | Conteúdo | Obrigatório |
|---|---|---|
| Identificação | Órgão requisitante, responsável, data e número do processo | sim |
| Objeto | Descrição do bem ou serviço a adquirir, com quantidade | sim |
| Justificativa | Necessidade, Alignment to strategic objective | sim |
| Estimativa | Valor estimado e método usado (média de 3 cotações ou referência de preço) | sim |
| Dotação | Fonte e natureza da dotação (ordinária, convolvida ou suplementar) | sim |
| Assinatura | Responsável pela demanda | sim |

## 2. Estudo Técnico Preliminar (ETP)

Exigido na etapa **ETP** (RN02).

1. Descrição do objeto e dos requisitos.
2. Quantidade estimada e memorial descritivo.
3. Previsão de valor e memória de cálculo.
4. Possibilidades de participação de empresas de pequeno porte.
5. Procedimentos de fiscalização.
6. Responsável pela emissão.

## 3. Termo de Referência (TR)

Exigido na etapa **TR** (RN02).

1. Descrição sucinta do objeto.
2. Justificativa da necessidade.
3. Quantidade e prazo de entrega.
4. Critérios de julgamento e de habilitação.
5. Requisitos de qualidade, segurança e condições de entrega.
6. Forma de apresentação das propostas.

## 4. Análise de riscos

Exigida na etapa **Análise de riscos** (RN02).

| Risco | Probabilidade | Impacto | Tratamento |
|---|---|---|---|
| Impugnação do processo | média | alto | Sanear falhas na minuta de referência |
| Preço não compatível com o mercado | alta | médio | Pesquisa com 3 cotações e memória de cálculo |
| Atraso na entrega | média | médio | Cláusula de prazo e penalidade |
| Dirigibilidade de recurso | baixa | alto | Comissão de acompanhamento designada |

## 5. Pesquisa de preços (RN04)

O app exige **três cotações** com fornecedor, valor e data, e o valor estimado.
A memória de cálculo fica registrada com média e mediana, e o app alerta quando
a média se afasta mais de 30% do estimado.

## Como confirmar

Substituir cada arquivo pela versão oficial e conferir, no app:

1. Os nomes das etapas do fluxo (`CA_ETAPAS` em `src/app.js`).
2. Os documentos exigidos por etapa (`CA_DOCS`).
3. Os prazos reais de cada etapa.
