# Modelos de referência do processo de aquisição

> **Base legal**: Lei nº 14.133/2021 (Lei de Licitações e Contratos
> Administrativos), consultada em 30/10/2026 no acervo
> [ctresb/leis](https://github.com/ctresb/leis) e no site do Planalto.
> **Premissa**: os modelos oficiais da POLITEC ainda não chegaram ao grupo; a
> estrutura abaixo é a que o app exige, ancorada nos artigos da lei. Ver
> [PREMISSAS.md](../../PREMISSAS.md) e [fluxo-e-prazos.md](fluxo-e-prazos.md).

## 1. Documento de Formalização da Demanda (DFD)

Art. 18, I e § 1º, I e VI, da Lei nº 14.133/2021.

| Seção | Conteúdo | Obrigatório |
|---|---|---|
| Identificação | órgão requisitante, responsável, data e número do processo (SIGADOC) | sim |
| Objeto | descrição do bem ou serviço, com quantidade | sim |
| Justificativa | necessidade pública e alinhamento com o plano de contratações anual | sim |
| Estimativa | valor estimado e memória de cálculo | sim |
| Dotação | fonte e natureza da dotação (ordinária, convolvida ou suplementar) | sim |
| Assinatura | responsável pela demanda | sim |

## 2. Estudo Técnico Preliminar (ETP)

Art. 18, § 1º, com os 13 elementos. O § 2º exige ao menos **I, IV, VI, VIII e
XIII**; os demais precisam de justificativa.

| # | Elemento | Obrigatório |
|---|---|---|
| I | descrição da necessidade, sob a perspectiva do interesse público | **sim** |
| II | previsão no plano de contratações anual | não |
| III | requisitos da contratação | não |
| IV | estimativas das quantidades, com memórias de cálculo | **sim** |
| V | levantamento de mercado e justificativa da solução | não |
| VI | estimativa do valor, com preços unitários referenciais | **sim** |
| VII | descrição da solução como um todo, com manutenção e assistência | não |
| VIII | justificativas para o parcelamento da contratação | **sim** |
| IX | demonstrativo dos resultados pretendidos | não |
| X | providências para a fiscalização e a gestão contratual | não |
| XI | contratações correlatas e interdependentes | não |
| XII | impactos ambientais e medidas mitigadoras | não |
| XIII | posicionamento conclusivo sobre a adequação da contratação | **sim** |

## 3. Termo de Referência (TR)

Art. 18, II e III, da Lei nº 14.133/2021.

1. Descrição sucinta do objeto.
2. Justificativa da necessidade.
3. Quantidade e prazo de entrega.
4. Critérios de julgamento e de habilitação.
5. Requisitos de qualidade, segurança e condições de entrega.
6. Condições de execução, pagamento, garantias e recebimento.
7. Forma de apresentação das propostas.

## 4. Análise de riscos

Art. 18, X, da Lei nº 14.133/2021: *"a análise dos riscos que possam comprometer
o sucesso da licitação e a boa execução contratual"*.

| Risco | Probabilidade | Impacto | Tratamento |
|---|---|---|---|
| Impugnação do processo | média | alto | sanear falhas na minuta de referência |
| Preço não compatível com o mercado | alta | médio | pesquisa com 3 cotações e memória de cálculo |
| Atraso na entrega | média | médio | cláusula de prazo e penalidade |
| Dirigibilidade de recurso | baixa | alto | comissão de acompanhamento designada |

## 5. Pesquisa de preços

Art. 23 da Lei nº 14.133/2021. O § 1º lista 4 parâmetros, adotados de forma
combinada ou não. O app usa o **inciso IV**:

> *"pesquisa direta com no mínimo 3 (três) fornecedores, mediante solicitação
> formal de cotação, desde que seja apresentada justificativa da escolha desses
> fornecedores e que não tenham sido obtidos os orçamentos com mais de 6 (seis)
> meses de antecedência da data de divulgação do edital."*

O app exige 3 cotações com fornecedor, valor e data, e o valor estimado. A
memória de cálculo registra média e mediana. O alerta de inconsistência quando a
média se afasta mais de **30%** do estimado é elucubração: a lei manda o valor
ser compatível com o mercado, sem fixar percentual.

## 6. Análise jurídica (art. 53)

> *"Ao final da fase preparatória, o processo licitatório seguirá para o órgão
> de assessoramento jurídico da Administração, que realizará controle prévio de
> legalidade mediante análise jurídica da contratação."*

O parecer é redigido em linguagem simples e compreensível, de forma clara e
objetiva, apreciando todos os elementos indispensáveis à contratação (§ 1º, II).
Encerrada a instrução, a autoridade determina a divulgação do edital (§ 3º).

## Como confirmar

1. Trocar cada arquivo pela versão oficial da POLITEC.
2. Conferir as 9 etapas e os documentos exigidos por etapa.
3. Confirmar os prazos de cada etapa e a janela de 30% do alerta de preços.
