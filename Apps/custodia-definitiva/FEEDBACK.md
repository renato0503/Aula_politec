# Feedback dos alunos · Custódia Definitiva

Gerado por `python Apps/_base/baixar_feedback.py` em 03/11/2026, a partir da coleção `feedback_apps` do Firestore.
1 resposta(s) · nota média 3,0 de 5

Use este arquivo para abrir o próximo sprint: cada item vira uma linha do `sprint.md`. Os números com fonte são da própria resposta.

## Resumo

- Usaria no trabalho: sim, com ajustes (1)
- Piloto: talvez (1)

## Prioridades (na ordem de cada pessoa)

- [ ] Implementar o endereçamento físico completo dos vestígios, identificando contêiner, estante, prateleira, nível e posição. O sistema deve sugerir endereços compatíveis, exigir a confirmação do acondicionamento pelo servidor e registrar responsável, data, horário e histórico das movimentações. _(Edjane, 1ª)_
- [ ] Ampliar o cadastro para contemplar procedência, identificação dos responsáveis, integridade dos lacres, conferência documental, características físicas e requisitos de conservação. Organizar o recebimento em etapas, impedindo que o material seja considerado armazenado antes da confirmação física e documental. _(Edjane, 2ª)_
- [ ] Aprimorar o painel gerencial com indicadores de entradas e saídas, ocupação por categoria, capacidade disponível por contêiner e prateleira, pendências, alertas de saturação e projeções de crescimento. Padronizar as unidades de medida e esclarecer eventuais divergências entre os indicadores apresentados nos diferentes perfis. _(Edjane, 3ª)_

## Tela por tela

### Painel (`#/painel`)

Situação: precisa de ajuste (1)

- [ ] O painel apresenta bons indicadores operacionais e gerenciais, com ocupação, distribuição por categoria, entradas mensais e projeções. Sugiro esclarecer a diferença entre os quantitativos apresentados no painel geral e no painel do gestor, melhorar a visualização dos gráficos e tornar os alertas interativos, permitindo acessar diretamente os registros ou contêineres que exigem atenção. Também seria importante apresentar a previsão de saturação individual por contêiner ou categoria, facilitando o planejamento da capacidade de armazenamento. _(Edjane)_

### Acervo (`#/vestigios`)

Situação: precisa de ajuste (1)

- [ ] A tela Acervo apresenta boa organização, com pesquisa por identificadores, filtros combinados, consulta de situação e exportação CSV. Sugiro aprimorar a coluna de localização, detalhando o endereço físico completo do vestígio (contêiner, estante, prateleira e posição), pois a identificação atual não permite compreender com precisão sua localização interna. Também recomendo especificar os motivos das pendências e destacar os materiais sem endereçamento ou que necessitam de conferência, facilitando sua identificação e priorização pela equipe de custódia. _(Edjane)_

### Novo vestígio (`#/vestigio/novo`)

Situação: precisa de ajuste (1)

- [ ] Considero a tela de cadastro excessivamente simplificada para a complexidade da custódia de vestígios periciais. Sugiro reorganizá-la em etapas: identificação do vestígio, origem e procedência, conferência física e documental, condições de conservação, endereçamento e confirmação do armazenamento.

Devem ser incluídos campos para unidade de origem, responsáveis pela entrega e recebimento, integridade do lacre, tipo de embalagem, quantidade, dimensões e requisitos específicos de conservação, com campos condicionais conforme a natureza do material.

O endereçamento deve contemplar contêiner, estante, prateleira e posição, considerando compatibilidade e capacidade disponível. É fundamental distinguir o endereço sugerido automaticamente daquele efetivamente utilizado. Após o acondicionamento físico, o servidor deverá confirmar ou corrigir a localização, registrando obrigatoriamente o endereço definitivo, sua identificação funcional e a data e hora da operação.

A situação do vestígio somente deverá ser alterada para “Armazenado” após essa confirmação. O sistema também deverá manter o histórico de alterações de endereço, com identificação dos responsáveis, datas, horários e justificativas, assegurando rastreabilidade das movimentações.

Essas melhorias permitirão que o cadastro deixe de ser apenas um registro de estoque e passe a representar adequadamente as operações de recebimento, acondicionamento e guarda na cadeia de custódia. _(Edjane)_

### Contêineres (`#/conteineres`)

Situação: precisa de ajuste (1)

- [ ] A tela apresenta adequadamente as informações gerais de capacidade, ocupação, categoria e conservação, mas precisa evoluir para representar a estrutura física interna de cada contêiner.

Sugiro permitir o cadastro individual de contêineres, estantes, prateleiras, níveis e posições, com visualização da ocupação e disponibilidade de cada endereço. Ao selecionar um contêiner, o usuário deveria visualizar sua organização interna e os vestígios armazenados em cada posição, podendo consultar os respectivos registros.

Também é necessário diferenciar a unidade de armazenamento de suas subdivisões físicas, evitando tratar contêiner, sala, armário e prateleira como estruturas equivalentes.

Recomendo incluir capacidade por posição, requisitos de conservação, bloqueio de espaços indisponíveis, alertas de saturação e indicação de endereços compatíveis para novos materiais. A localização física efetiva deverá ser confirmada pelo servidor responsável após o acondicionamento. _(Edjane)_

### Vestígio (`#/vestigio/:id`)

Situação: não testou (1)

- [ ] Campo já contemplado em novo vestígio e acervo. _(Edjane)_

## Erros encontrados

- [ ] Identifiquei inconsistência na representação das unidades de armazenamento: os registros fictícios denominados “contêineres” incluem descrições de salas, armários e prateleiras, sem uma hierarquia física definida. Isso pode dificultar a interpretação dos endereços e a localização operacional dos vestígios. Também observei que o painel geral apresenta 30 vestígios, enquanto o painel do gestor exibe 1.168 itens, sem esclarecer a diferença entre esses indicadores. Não foram identificadas falhas de execução nesta tela apenas pela inspeção visual. _(Edjane)_

## O que falta

- [ ] O aplicativo precisa permitir o gerenciamento detalhado da estrutura física de armazenamento, com cadastro hierárquico de contêineres, estantes, prateleiras e posições. Deve apresentar um mapa interno de ocupação, indicar endereços disponíveis, registrar a localização efetiva dos vestígios e permitir consultas e movimentações com rastreabilidade. Também são necessários alertas de incompatibilidade, saturação e pendências documentais, além de relatórios gerenciais e projeções de capacidade por categoria e unidade de armazenamento. _(Edjane)_

## Regras, nomes e números que não batem

- [ ] A identificação do armazenamento precisa diferenciar contêiner, estante, prateleira, nível e posição. Atualmente, o sistema utiliza o termo “contêiner” para estruturas de natureza distinta, como salas e armários. A capacidade também precisa ter unidade de medida definida, distinguindo quantidade de itens, embalagens e volume físico ocupado. Para a futura Central de Custódia Definitiva, a regra de endereçamento deverá considerar a localização interna, a compatibilidade dos materiais, as condições de conservação e a confirmação física do acondicionamento. _(Edjane)_

## Observações

- [ ] O protótipo apresenta uma boa estrutura inicial e demonstra potencial para apoiar a futura Central de Custódia Definitiva da POLITEC/MT. A diferenciação dos perfis de usuário, a consulta dos vestígios e os indicadores de ocupação são funcionalidades positivas.

Entretanto, a aplicação ainda precisa evoluir especialmente no controle da localização física, na conferência dos materiais e na rastreabilidade das operações. Também considero importante ampliar os recursos gerenciais, tornando os painéis mais completos e úteis à tomada de decisão.

Após esses ajustes, considero viável propor um piloto supervisionado, inicialmente com dados fictícios e situações simuladas, para avaliar a aderência às necessidades operacionais. A utilização institucional dependerá de validação técnica, adequação às normas de cadeia de custódia e autorização da gestão competente. _(Edjane)_

## Quem respondeu

- Edjane · equipe do app · Custódia · nota 3 · 2026-11-03
