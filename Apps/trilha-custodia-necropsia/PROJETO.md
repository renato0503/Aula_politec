# PROJETO.md — CNC

**Aluno ou equipe:** Silmara Bueno
**Unidade:** IML — Coordenadoria de Perícias em Mortos
**Contato:** silmarabueno@politec.mt.gov.br
**Projeto:** CNC
**Tipo de projeto:** Aplicativo (app) para cidadão, servidor ou equipe
**Data:** 2026-10-29
**Resumo:** CCN -  Controle de Necropsia Centralizado . Um aplicativo que controla todo Procedimento com registro digital único que acompanha cada corpo da remoção à liberação, para as equipes do IML, no lugar do controle manual disperso e sem rastreabilidade.

## 1. Problema (a dor)

**Problema:** Ausência centralizada de informações sobre os cadáveres.
**Impacto:** O impacto de hoje é retrabalho para o técnico, que repete o mesmo registro em quatro livros diferentes e ainda avisa os marcos de deslocamento de forma verbal; custódia sem rastro, com lacres e autos de entrega fora do sistema; corpos não identificados e não reclamados sem controle centralizado, com informação que se perde na passagem de plantão; espera maior para a família; e aviso tardio à autoridade policial, que segue buscando uma vítima já identificada. Nada disso é medido hoje.
**Quem sofre:** Cidadão externo, Servidor da unidade, Equipe interna, Chefia, Autoridade
**Como é feito hoje:** Hoje o registro é feito em paralelo por vários setores e em suportes diferentes. O CIOP recebe o acionamento, abre o protocolo no Atena e repassa a ocorrência ao técnico, que se desloca sem registrar os marcos de saída da base, chegada ao local, saída do local e retorno ao IML, porque esse aviso é informal e frequentemente esquecido. No local, o técnico preenche o registro de ocorrência em papel, recolhe a requisição pericial de necropsia emitida pela autoridade policial e, quando existe, o documento da vítima. Na chegada ao IML, preenche o livro de registro de necropsia, o livro de câmara fria, o livro de PAF e o controle de tornozeleira, com dados que se repetem em cada um deles, e entrega ao gestor. A necropsia e os lacres das amostras biológicas são lançados no Atena, mas não há forma de registrar a entrega dessas amostras pelo sistema. A identificação é buscada de forma manual: quando um familiar ou uma autoridade policial procura uma pessoa desaparecida, o plantonista consulta os registros um a um. Os corpos não identificados e os identificados não reclamados ficam sem controle centralizado, e a situação de cada corpo depende de quem está de plantão, o que se perde na passagem de plantão. Como consequência, a família e a autoridade policial muitas vezes só sabem da identificação dias depois, enquanto a busca por uma vítima já identificada continua.
**Evidências:** Relatório de sistema, Medida feita pela equipe, Documento ou norma oficial
**Detalhe da evidência:** O impacto de hoje é retrabalho para o técnico, que repete o mesmo registro em quatro livros diferentes e ainda avisa os marcos de deslocamento de forma verbal; custódia sem rastro, com lacres e autos de entrega fora do sistema; corpos não identificados e não reclamados sem controle centralizado, com informação que se perde na passagem de plantão; espera maior para a família; e aviso tardio à autoridade policial, que segue buscando uma vítima já identificada. Nada disso é medido hoje.
**O que não pode ser automatizado:** Não são automatizáveis a necropsia, o laudo, os exames de identificação, as decisões técnicas, a custódia física e a liberação do corpo, porque dependem de julgamento profissional, assinatura de responsabilidade e ato presencial. O sistema automatiza o registro, a geração de documentos, as notificações e o controle de prazos, não o trabalho pericial em si.

## 2. Objetivo do MVP (o que faz e o que NÃO faz)

**Objetivo do MVP:** Demonstrar um registro digital único por corpo, da remoção à liberação, com os marcos do deslocamento, os lacres das amostras e a situação de identificação visíveis para toda a equipe.
**O que o MVP não faz:** O MVP não integra com o Atena, não substitui os livros oficiais, não decide a identificação e não libera o corpo sem autorização humana. Usa apenas dados fictícios.
**Entregável do projeto:** Aplicativo web para registrar o acionamento, os marcos de deslocamento, os lacres e a situação de cada corpo, com painel e busca.
**Dentro do escopo:** Acionamento com protocolo, quatro marcos de deslocamento, lacres e amostras, situação do corpo, busca por protocolo/nome/documento, trilha de auditoria e painel por situação.
**Fora do escopo:** Integração com o Atena, substituição dos livros de necropsia, câmara fria, PAF e tornozeleira, decisão de identificação, auto de entrega oficial e qualquer dado real.
**Plataforma alvo:** Site web (abre no navegador)
**Primeira tela:** Painel com os corpos por situação, alertas e os últimos marcos registrados.
**Simulado no MVP:** Protocolos, nomes, documentos, locais e lacres fictícios. O deslocamento é representado pelos quatro marcos com data e hora.
**Critério de aceite:** A equipe registra um corpo, os quatro marcos e os lacres, e o painel mostra a situação correta; a busca encontra o corpo pelo protocolo, nome ou documento.
**Dados de exemplo:** 12 corpos fictícios em todas as situações, com marcos, lacres e um caso sem identificação.
**O que já existe pronto e pode ser reaproveitado:** O protótipo da aluna, o fluxo do CIOP, os quatro livros e os procedimentos do IML. No MVP, os dados são fictícios.
**Dependências:** Do IML para validar marcos, situações e livros substituídos; da TI para a futura integração com o Atena; da chefia para o piloto.

## 3. Usuários e papéis

| Papel | Quem é | O que enxerga | O que faz | O que não pode fazer | Registro |
|---|---|---|---|---|---|
| Operador do CIOP | Servidor que recebe o acionamento | Chamado, protocolo e ocorrência | Abre o protocolo e registra o acionamento | Decidir a identificação | Protocolo e acionamento |
| Técnico de necropsia | Técnico que vai ao local | Local, requisição e corpo | Registra os quatro marcos e recolhe a requisição | Liberar o corpo | Marcos e requisição |
| Plantonista | Servidor do plantão do IML | Situação, identificação e guarda | Registra identificação, não reclamado e liberação | Alterar laudo | Situação e auto de entrega |
| Gestor | Chefia da coordenadoria | Painel, prazos e auditoria | Acompanha prazos e passagem de plantão | Suprimir registros | Trilha de auditoria |

**Observações sobre os papéis:** O operador do CIOP registra o acionamento; o técnico de necropsia registra o local e os marcos; o plantonista acompanha a identificação e a guarda; o gestor acompanha prazos e passagem de plantão. A identificação e a liberação continuam com as pessoas.

## 4. Dados (entidades e colunas; tudo SINTÉTICO)

| Entidade | O que representa | Colunas | Chave | Volume | Origem | Sintético |
|---|---|---|---|---|---|---|
| Corpo | Registro único de um corpo | id_corpo; protocolo; origem; natureza; municipio; local; nome; documento; desconhecido; tecnico; situacao; criado_em | id_corpo | 12 no exemplo | App | Sim |
| Marco | Marco do deslocamento | id_marco; corpo_id; tipo; data_hora; perfil; observacao | id_marco | 48 no exemplo | App | Sim |
| Lacre | Amostra lacrada | id_lacre; corpo_id; codigo; destino; data_hora; perfil | id_lacre | 24 no exemplo | App | Sim |
| Log | Trilha de auditoria | id; corpo_id; acao; perfil; data_hora | id | — | App | Sim |

**O que precisa ser coletado:** Tempo de remoção, de chegada ao IML, de identificação e de liberação; volume de corpos não identificados e não reclamados.
**Quem libera o acesso:** A chefia do IML libera o acesso; no MVP, só dados fictícios.

### Fontes de dados do processo real

| Fonte | Tipo | Onde | Existe | Uma linha é | Volume | Campos de data | Atualiza | LGPD |
|---|---|---|---|---|---|---|---|---|
| Atena | Sistema oficial | POLITEC | Sim | Um protocolo | não informado | protocolo, necropsia, lacres | Contínua | Sim |
| Livros de necropsia, câmara fria, PAF e tornozeleira | Caderno | IML | Sim | Um corpo por linha | não informado | nome, protocolo, câmara, lacre | Diária | Sim |
| Requisição pericial de necropsia | Documento | Autoridade policial | Sim | Uma requisição por corpo | não informado | número, autoridade, data | Por caso | Sim |


## 5. Regras de negócio (RN01, RN02...)

| ID | Regra | Quando se aplica | Exceção | Quem valida | Tipo |
|---|---|---|---|---|---|
| RN01 | O protocolo é único e gerado no acionamento | No cadastro | Nenhuma | Sistema | Validação |
| RN02 | A liberação exige identificação registrada e auto de entrega com responsável e data | Na liberação | Nenhuma | Plantonista | Negócio |
| RN03 | Todo marco, lacre e mudança de situação registra perfil, data e hora | Em toda ação | Nenhuma | Sistema | Validação |
| RN04 | A busca aceita protocolo, nome ou documento | Na busca | Caso sem nome | Sistema | Negócio |
| RN05 | A lista do painel não mostra nome completo | No painel | Ficha do caso | Sistema | LGPD |


## 6. Telas (#/painel, #/lista...)

| Rota | Tela | Objetivo | Quem usa | Dados | Ação | Regra | Tipo | Verificável como | MVP |
|---|---|---|---|---|---|---|---|---|---|
| #/painel | Painel | Ver a situação de todos os corpos | Equipe do IML | Corpos, situações e marcos | Filtrar e abrir o caso | RN05 | Tela | Contagens conferem com a base | Sim |
| #/corpo/novo | Acionamento | Registrar um corpo | Operador e técnico | Protocolo, origem, local e vítima | Salvar | RN01 | Tela | Corpo criado com protocolo único | Sim |
| #/corpo/:id | Ficha e marcos | Registrar marcos, lacres e situação | Técnico e plantonista | Marcos, lacres e situação | Registrar | RN02, RN03 | Tela | Marcos e lacres na trilha | Sim |
| #/busca | Busca | Localizar o corpo | Equipe e autoridade | Protocolo, nome ou documento | Buscar | RN04 | Tela | Resultado com a situação | Sim |


## 7. KPIs (nome = fórmula em uma linha)

| KPI | Pergunta | Fórmula | Fonte | Linha de base | Valor esperado | Como medir |
|---|---|---|---|---|---|---|
| Tempo de remoção | Quanto tempo entre o acionamento e a chegada ao IML? | Média(chegada - acionamento) | Marcos do app | não medida | medir no piloto | Comparar as datas dos marcos |
| Tempo até a identificação | Quanto tempo a família espera para saber da identificação? | Média(identificação - entrada) | App | dias | menos de 1 dia | Comparar antes e depois |
| Corpos não reclamados | Quantos corpos ficam sem retirada? | Não reclamados / total | App | não medido | acompanhar | Contar por situação |

**Período da linha de base:** Não informada no envio; medir no piloto.
**Campos de data e tempo que existem:** Data e hora do acionamento, dos quatro marcos, dos lacres e da liberação.

## 8. Stack: HTML único (CSS/JS inline), dados em JSON embutido, GitHub Pages.

**Stack escolhida:** Aplicativo web com framework (React, Vite, TypeScript)
**Detalhe da stack:** Um único index.html (HTML, CSS e JS embutidos), com dados no IndexedDB do navegador e backup .json, publicado no GitHub Pages. O protótipo da IA fica preservado em `prototipo/` como referência visual.
**Hospedagem:** GitHub Pages, com um arquivo HTML único, para demonstração com dados fictícios.
**Custo e licenças:** R$ 0,00 no MVP acadêmico.
**Contas e domínio:** O professor publica o protótipo no GitHub; a versão institucional depende da TI e da chefia do IML.

| Opção | Tipo | Onde roda | Custo | Quem mantém | Acesso | Banco de dados | Escala | Limitação |
|---|---|---|---|---|---|---|---|---|
| GitHub Pages | Estática e gratuita | github.io | Zero | Equipe do projeto | Link (o app; os dados ficam no navegador) | Não tem | Baixa | Publica só o app, nunca os dados |


## 9. Restrições e LGPD

**Restrições:** Dados do corpo e da vítima são sensíveis. A versão institucional exige criptografia, controle de acesso e observância dos arts. 158-A a 158-F do CPP e da LGPD.
**Dados pessoais tratados:** Nome, documento, idade, sexo e local do corpo. No MVP, todos fictícios.
**Base legal:** Exercício de competência legal do órgão para a perícia oficial (art. 7º, III, da LGPD), com dados sensíveis tratados apenas na versão institucional.
**Retenção:** Dados fictícios mantidos só durante o piloto; um botão apaga o caso encerrado.
**Acesso e registro:** Acesso por perfil (operador, técnico, plantonista e gestor), com autenticação individual e trilha na versão institucional.
**Requisitos marcados:** -

---

# Anexo A — AS-IS (o fluxo de hoje)

**Início:** Acionamento pelo CIOSP
**Fim:** Arquivamento do laudo
**Entradas:** Acionamento do CIOP, requisição pericial de necropsia, dados da ocorrência (local, horário, natureza da morte), documentos da vítima quando houver, informações de familiares, o corpo, amostras biológicas, guia de auto de entrega de cadáver e resultados dos exames de identificação.
**Saídas:** Registro de ocorrência, livro de necropsia, livro de câmara fria, livro de PAF e controle de tornozeleira preenchidos, laudo de necropsia assinado, declaração de identificação, auto de entrega do cadáver, relação de lacres de amostras e comunicação de identificação à autoridade policial.
**Volume:** -
**Duração:** -
**Frequência:** Diário
| Etapa | Quem faz | O que entra | Ação | O que sai | Sistema | Regra | Onde espera | Tempo (h) | Automatizável |
|---|---|---|---|---|---|---|---|---|---|
| 1. Acionamento | CIOP | Chamado da autoridade | Abre o protocolo no Atena e repassa ao técnico | Protocolo e ocorrência | Atena | — | Fila do CIOP | — | Sim, com apoio humano |
| 2. Deslocamento | Técnico de necropsia | Ocorrência | Sai da base sem registrar os marcos | Técnico no local | Aviso verbal | Aviso informal | Saída da base | — | Não |
| 3. Local | Técnico de necropsia | Local e requisição | Preenche o registro em papel e recolhe a requisição | Registro em papel | Papel | — | No local | — | Não |
| 4. Chegada ao IML | Técnico de necropsia | Corpo e documentos | Preenche o livro de necropsia, câmara fria, PAF e tornozeleira | Quatro livros preenchidos | Papel | Dados repetidos | Recepção | — | Não |
| 5. Necropsia | Perito e técnico | Corpo | Realiza a necropsia e lacra as amostras | Laudo e lacres | Atena | — | Sala de necropsia | — | Pouco |
| 6. Identificação | Plantonista | Consulta de familiar ou autoridade | Procura manualmente nos registros | Identificação registrada | Papel e Atena | — | Um a um | dias | Não |
| 7. Guarda | Plantonista | Corpo não identificado | Mantém na câmara fria sem controle central | Corpo guardado | Planilha | — | Câmara fria | — | Não |
| 8. Liberação | Gestor e plantonista | Autorização | Entrega o corpo e assina o auto em papel | Corpo liberado | Papel | Identificação e auto | Aguardando retirada | — | Não |

**Decisões e aprovações:** -
**Exceções:** -
**Já digitalizado:** -

# Anexo B — TO-BE (o fluxo depois da mudança)

**Visão do futuro:** Informações centralizadas e sem retrabalho.
**Mudança principal:** O registro deixa de ser papel em manual em papeis, além de concentrar informações sobre o cadáver em um único local. 
**O que fica igual:** As necropsias 
**O que não pode mudar:** -
| Etapa | O que muda | Quem executa | Benefício | Esforço |
|---|---|---|---|---|
| Acionamento e marcos | Os quatro marcos passam a ser registrados no app | A pessoa assistida pela máquina | Rastreabilidade do deslocamento | Baixo |
| Registro único | Um cadastro por corpo, sem repetir em quatro livros | A máquina (automação) | Menos retrabalho | Médio |
| Lacres | A entrega das amostras passa a ter registro | A pessoa assistida pela máquina | Custódia com rastro | Baixo |
| Identificação e busca | Consulta por protocolo, nome ou documento | A máquina (automação) | Resposta no mesmo dia | Médio |
| Painel | Situação de todos os corpos visível na passagem de plantão | A máquina (automação) | Nada se perde entre plantões | Baixo |

**Piloto do TO-BE:** -

# Anexo C — Pesquisa, riscos e plano

**Hipótese de campo:** Um registro único com marcos e situação visível reduz o retrabalho dos quatro livros, o tempo de identificação e o aviso tardio à família e à autoridade.
| Referência | Tipo | Fonte ou link | Ano | Dado que extrai | Como usar na defesa | Link conferido |
|---|---|---|---|---|---|---|
| Código de Processo Penal, arts. 158-A a 158-F | Norma ou lei | Planalto | 1941 | Cadeia de custódia | Sustenta o registro dos marcos, lacres e responsáveis | Sim |
| Lei nº 13.709/2018 (LGPD) | Norma ou lei | Planalto | 2018 | Dados pessoais sensíveis | Justifica o acesso restrito e o uso de dados fictícios | Sim |

**Lacunas:** O envio não traz volume, tempo médio, linha de base nem a lista de campos de cada livro. O piloto deve medir.
| Marco | Data | Responsável | Depende de | Situação |
|---|---|---|---|---|
| Fluxo e marcos validados com o IML | 06/11/2026 | Silmara e chefia | Reunião e leitura dos livros | Planejado |
| Protótipo com acionamento e marcos | 27/11/2026 | Silmara | Dados fictícios e regras | Planejado |
| Identificação, busca e liberação | 11/12/2026 | Silmara | Validação com o plantão | Planejado |
| Piloto de 30 dias | 29/01/2027 | Equipe do IML | Aceite da chefia | Planejado |

| Risco | Probabilidade | Impacto | Mitigação |
|---|---|---|---|
| Duplicidade com o Atena | Alta | Alto | Definir o que o app registra e o que fica no Atena; integração futura |
| Resistência à mudança de rotina | Média | Alto | Piloto com o plantão e treinamento |
| Dado sensível exposto | Baixa | Alto | Só dados fictícios no MVP; acesso por perfil e criptografia na versão institucional |
| Perda de informação na passagem de plantão | Média | Médio | Painel com situação e últimos marcos |

**Apoio necessário:** Apoio da chefia do IML e dos plantonistas para validar o fluxo e medir os tempos.
**Aprendizado necessário:** Modelagem do processo, marcos e custódia, GitHub e Antigravity.

# Anexo D — A defesa

**Frase de defesa:** Se o corpo tem um registro único e os marcos visíveis, a equipe deixa de procurar em quatro livros e a família sabe da identificação no dia.
**Provas:** O relato descreve quatro livros paralelos, marcos verbais e busca manual; o protótipo da aluna organiza acionamento, marcos, lacres e recepção.
**Piloto:** Piloto de 30 dias com casos fictícios, comparando o tempo de registro e de identificação antes e depois.
**Maior risco:** O maior risco é a resistência à mudança de rotina e a duplicidade com o Atena; mitigar com piloto, treinamento e integração futura.

# Anexo E — Documentos enviados

**Descrição dos documentos:** Dois envios parciais do formulário (CNC e TCIN) e um protótipo HTML gerado na IA.
**O que ainda falta:** Lista de campos dos quatro livros, marcos oficiais, volume, linha de base e o nome definitivo do projeto.
