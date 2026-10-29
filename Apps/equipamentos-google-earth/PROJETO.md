# PROJETO.md — Visão geral dos equipamentos no estado com Google Earth

**Aluno ou equipe:** João Lucas Nogueira Ponce
**Unidade:** Coordenadoria de qualidade  
**Contato:** joaoponce@politec.mt.gov.br
**Projeto:** Visão geral dos equipamentos no estado com Google Earth
**Tipo de projeto:** Aplicativo web / portal
**Data:** 2026-10-28
**Resumo:** O projeto armazena fotos e dados de equipamentos — incluindo custos e históricos de manutenção —, além de calcular o impacto e o custo de parada por defeito na filial e na diretoria para apoiar a tomada de decisão. A visualização é feita via Google Earth, mapeando o estado e exibindo a localização exata de cada ativo.

## 1. Problema (a dor)

**Problema:** Nem todos equipamentos possuem contrato de manutenção o intuito dessa solução e mensurar qual e o impacto se esse equipamento que parar precisar de uma manutenção.
**Impacto:** Tem equipamentos se parar para o setor inteiro.
**Quem sofre:** Cidadão externo, Servidor da unidade, Equipe interna, Unidade parceira, Chefia, Autoridade
**Como é feito hoje:** acredito que não e feito um acompanhamento via alguma ferramenta.
**Evidências:** Entrevista com a equipe, Planilha ou controle local
**Detalhe da evidência:** Entrevista com a equipe da Coordenadoria de qualidade: não há ferramenta de acompanhamento, e parte dos equipamentos está sem contrato de manutenção. A planilha que existe hoje é parcial e será reunida no Sprint 0.
**O que não pode ser automatizado:** Acredito que não temos esse impedimento para automações 

## 2. Objetivo do MVP (o que faz e o que NÃO faz)

**Objetivo do MVP:** Provar que a coordenadoria consegue ver, no mapa, os equipamentos sem contrato e o custo estimado de parada por unidade e por diretoria, a partir de um cadastro único.
**O que o MVP não faz:** Não abre chamado, não controla patrimônio contábil, não integra com sistema oficial, não exige internet (exceto para abrir o Google Earth).
**Entregável do projeto:** App em um único arquivo HTML com mapa de MT, cadastro de equipamentos com fotos, contratos, manutenções e paradas, painel de KPIs e exportação .kmz para o Google Earth.
**Dentro do escopo:** Cadastro de unidades, equipamentos (com fotos), contratos, manutenções (com comprovante) e paradas; cálculo de risco e custo de parada; mapa offline de MT; painel por unidade e diretoria; exportação .kmz, .json, .csv e relatório impresso; consolidação dos arquivos das unidades.
**Fora do escopo:** Abertura de chamado com fornecedor; controle patrimonial contábil e de estoque; integração com o sistema de patrimônio ou o SEI; login por usuário.
**Plataforma alvo:** Site web (abre no navegador)
**Primeira tela:** Mapa de Mato Grosso com os pinos das unidades coloridos pelo risco e, ao lado, os 4 KPIs principais (sem contrato, pontos únicos de falha, exposição diária, custo de parada no período).
**Simulado no MVP:** Unidades fictícias em municípios reais de MT, 150 equipamentos fictícios, contratos, manutenções e paradas sintéticos. O valor de referência do atendimento perdido é um parâmetro de teste.
**Critério de aceite:** A coordenadoria importa os equipamentos de 3 unidades, registra uma parada, vê o custo no painel, filtra os sem contrato no mapa e abre o .kmz no Google Earth com as fotos.
**Dados de exemplo:** 3 diretorias, 12 unidades, 150 equipamentos, 20 contratos, 200 manutenções e 40 paradas, todos fictícios.
**O que já existe pronto e pode ser reaproveitado:** A planilha parcial de equipamentos que a coordenadoria já tem (importada por CSV) e os comprovantes de manutenção em PDF.
**Dependências:** Coordenadoria de qualidade (parâmetros de custo e validação do escopo); lista oficial de unidades e diretorias; planilha atual de equipamentos; chefias das 3 unidades do piloto.

## 3. Usuários e papéis

| Papel | Quem é | O que enxerga | O que faz | O que não pode fazer | Registro |
|---|---|---|---|---|---|
| Coordenadoria de qualidade | Equipe do aluno | Todas as unidades, o mapa e o painel | Consolida os arquivos, define os parâmetros de custo, exporta .kmz e relatório | Registrar CPF ou nome de pessoa | Importações, parâmetros e exportações |
| Unidade | Chefe ou responsável técnico da unidade | Os equipamentos da própria unidade | Cadastra equipamentos e fotos, registra paradas e manutenções, exporta o .json | Alterar dados de outra unidade | Cadastros e paradas com data e cargo |
| Diretoria | Diretor | O painel consolidado e o relatório impresso | Consulta a exposição e prioriza contratações | Editar cadastros | Nenhum (só leitura) |

**Observações sobre os papéis:** O app não tem login: os papéis viram perfis da cópia do arquivo (unidade ou coordenadoria). A diretoria recebe o relatório consolidado.

## 4. Dados (entidades e colunas; tudo SINTÉTICO)

| Entidade | O que representa | Colunas | Chave | Volume | Origem | Sintético |
|---|---|---|---|---|---|---|
| Unidade | Local da POLITEC | id: texto, nome: texto, tipo: texto, diretoria_id: texto, municipio_ibge: texto, latitude: número, longitude: número, atendimentos_dia: número | id | 12 no teste | Lista de unidades | Parcialmente |
| Equipamento | Ativo em uso | id: texto, patrimonio: texto, nome: texto, tipo: texto, unidade_id: texto, criticidade: inteiro 1 a 5, tem_redundancia: lógico, status: texto, contrato_id: texto, latitude: número, longitude: número | id | 150 no teste | Planilha atual + cadastro | Sim |
| Contrato | Contrato de manutenção | id: texto, numero: texto, fornecedor: texto, inicio: data, fim: data, valor_mensal: número, sla_horas: número | id | 20 no teste | Contratos vigentes | Sim |
| Manutencao | Serviço executado | id: texto, equipamento_id: texto, tipo: texto, abertura: data, conclusao: data, custo_rs: número, comprovante_id: texto | id | 200 no teste | Comprovantes | Sim |
| Parada | Período sem operar | id: texto, equipamento_id: texto, inicio: data_hora, fim: data_hora, motivo: texto, atendimentos_perdidos_dia: número | id | 40 no teste | Registro da unidade | Sim |
| Arquivo | Foto ou comprovante | id: texto, tipo: texto, mime: texto, conteudo: binário | id | Até 3 fotos por equipamento | Unidade | Sim |

**O que precisa ser coletado:** Lista de unidades com município; lista de equipamentos com patrimônio, unidade, criticidade e situação de contrato; contratos vigentes; paradas do último trimestre.
**Quem libera o acesso:** A Coordenadoria de qualidade libera a planilha atual; as chefias das unidades do piloto informam os equipamentos e as paradas.

### Fontes de dados do processo real

| Fonte | Tipo | Onde | Existe | Uma linha é | Volume | Campos de data | Atualiza | LGPD |
|---|---|---|---|---|---|---|---|---|
| Planilha de equipamentos | Planilha local | Coordenadoria de qualidade | Parcialmente | Um equipamento | A levantar | Data de aquisição, se houver | Sem rotina | Não |
| Contratos de manutenção | Documento em papel | Unidades e setor de contratos | Sim | Um contrato | A levantar | Início e fim da vigência | A cada contrato | Não |
| Comprovantes de manutenção | Documento em papel | Unidades | Sim | Uma manutenção | 200 por mês (informado) | Data do serviço | A cada manutenção | Não |
| Malha municipal de MT | Sistema oficial | IBGE | Sim | Um município | 142 municípios | Não se aplica | Anual | Não |


## 5. Regras de negócio (RN01, RN02...)

| ID | Regra | Quando se aplica | Exceção | Quem valida | Tipo |
|---|---|---|---|---|---|
| RN01 | Ponto único de falha: criticidade maior ou igual a 4 e sem equipamento igual na unidade | No cálculo do risco | Nenhuma | Coordenadoria | Cálculo |
| RN02 | Custo diário de parada = atendimentos perdidos por dia × valor de referência + custo alternativo por dia | Ao registrar a parada | Sem números da parada: usa os da unidade | Coordenadoria | Cálculo |
| RN03 | Custo da parada = custo diário × dias úteis parados; parada aberta conta até hoje | No painel e na ficha | Nenhuma | Sistema | Cálculo |
| RN04 | Risco = criticidade × 2 (se sem contrato) × 2 (se ponto único de falha) | No mapa e no painel | Nenhuma | Coordenadoria | Cálculo |
| RN05 | Contrato vigente quando início ≤ hoje ≤ fim; alerta 60 dias antes do fim | Diariamente ao abrir o app | Nenhuma | Sistema | Negócio |
| RN06 | MTTR = média de conclusão − abertura das manutenções corretivas | No painel | Nenhuma | Sistema | Cálculo |
| RN07 | Disponibilidade = 1 − horas paradas ÷ horas úteis do período | No painel | Nenhuma | Sistema | Cálculo |
| RN08 | Coordenada fora do contorno de MT é recusada | No cadastro da unidade | Nenhuma | Sistema | Validação |
| RN09 | Não registrar CPF nem nome de pessoa; o responsável é o cargo ou a matrícula | Em todos os cadastros | Nenhuma | Sistema | LGPD |
| RN10 | Na consolidação, vence o registro com a alteração mais recente; conflito no mesmo minuto vai para revisão | Na importação dos arquivos das unidades | Revisão manual | Coordenadoria | Negócio |


## 6. Telas (#/painel, #/lista...)

| Rota | Tela | Objetivo | Quem usa | Dados | Ação | Regra | Tipo | Verificável como | MVP |
|---|---|---|---|---|---|---|---|---|---|
| #/mapa | Mapa de MT | Ver os equipamentos pelo risco | Todos | Unidades, equipamentos, risco | Filtrar e abrir a ficha | RN04 e RN08 | Tela | Sem internet, o filtro "sem contrato" reduz os pinos | Sim |
| #/painel | Painel | Ver os KPIs | Coordenadoria e diretoria | Sem contrato, pontos únicos de falha, custo de parada | Escolher o período | RN01 a RN07 | Tela | KPIs batem com a conta manual de 2 unidades | Sim |
| #/equipamento/:id | Ficha do equipamento | Ver tudo de um equipamento | Todos | Fotos, contrato, manutenções, paradas, custo | Editar e registrar | RN09 | Tela | Ficha mostra fotos e histórico | Sim |
| #/paradas | Paradas e manutenções | Registrar parada e manutenção | Unidade | Início, fim, motivo, custo, comprovante | Abrir e fechar parada | RN02 e RN03 | Tela | Parada aberta muda o status para parado | Sim |
| #/contratos | Contratos | Controlar a cobertura | Coordenadoria | Fornecedor, vigência, equipamentos cobertos | Cadastrar e alertar vencimento | RN05 | Tela | Contrato vencido some da cobertura no mesmo dia | Sim |
| #/importar | Importar e consolidar | Juntar as unidades | Coordenadoria | CSV da planilha e .json das unidades | Importar e resolver conflitos | RN10 | Ação | Duas cópias mescladas sem duplicar | Sim |
| #/exportar | Exportar para o Google Earth | Ver no Google Earth | Coordenadoria | Equipamentos com foto e risco | Gerar .kmz | RN08 | Integração | .kmz abre no Google Earth Pro e Web | Sim |


## 7. KPIs (nome = fórmula em uma linha)

| KPI | Pergunta | Fórmula | Fonte | Linha de base | Valor esperado | Como medir |
|---|---|---|---|---|---|---|
| Equipamentos sem contrato | Quantos equipamentos estão sem cobertura? | Sem contrato vigente ÷ total × 100 | Equipamentos e contratos | A medir no Sprint 0 | Todos identificados no piloto | Cruzar a planilha atual com os contratos |
| Exposição diária | Quanto a POLITEC perde por dia se os críticos sem contrato pararem? | Soma do custo diário (RN02) dos pontos únicos de falha sem contrato | Equipamentos, contratos e parâmetros | Não existe hoje | Calculada para as 3 unidades | Painel do app |
| Custo de parada no período | Quanto custaram as paradas? | Soma de RN03 nas paradas do período | Paradas | Não existe hoje | Registrado em 100% das paradas do piloto | Painel do app |
| Tempo para responder o custo de uma parada | Quanto tempo leva para saber quanto custa uma parada? | Hora da resposta − hora da pergunta | Cronômetro | A medir no Sprint 0 | Menos de 5 minutos | Cronometrar 3 perguntas antes e depois |

**Período da linha de base:** Último trimestre antes do piloto, nas 3 unidades: equipamentos sem contrato, paradas registradas e tempo para responder "quanto custa essa parada?".
**Campos de data e tempo que existem:** Hoje: datas dos comprovantes de manutenção e de vigência dos contratos (em PDF). No app: início e fim de cada parada, abertura e conclusão de cada manutenção, início e fim de cada contrato.

## 8. Stack: HTML único (CSS/JS inline), dados em JSON embutido, GitHub Pages.

**Stack escolhida:** HTML único (CSS/JS inline), dados em JSON embutido, GitHub Pages
**Detalhe da stack:** Um único arquivo index.html (HTML, CSS e JS embutidos), com a malha dos 142 municípios de MT embutida para o mapa offline e a biblioteca JSZip para gerar o .kmz do Google Earth. Dados no IndexedDB do navegador; cada unidade exporta um .json, e a coordenadoria importa e consolida. O aluno propôs Python/Flask na máquina local.
**Hospedagem:** Arquivo HTML único, aberto por duplo clique e publicado também no GitHub Pages (o mesmo arquivo). O mapa funciona sem internet, e o Google Earth recebe o arquivo .kmz exportado.
**Custo e licenças:** Custo zero: arquivo HTML, bibliotecas de código aberto e GitHub Pages.
**Contas e domínio:** O aluno publica o arquivo no GitHub Pages; não há conta de banco de dados nem de servidor.

| Opção | Tipo | Onde roda | Custo | Quem mantém | Acesso | Banco de dados | Escala | Limitação |
|---|---|---|---|---|---|---|---|---|
| Arquivo HTML único | Arquivo local | Computador da coordenadoria e das unidades | Zero | O aluno | Quem recebe o arquivo | IndexedDB do navegador | Uma cópia por unidade | Consolidação por arquivo .json |
| GitHub Pages | Estática e gratuita | GitHub | Zero | O aluno | Link público (sem dados) | Não tem; os dados ficam no navegador | Baixa | Publica só o app, nunca os dados |


## 9. Restrições e LGPD

**Restrições:** Sem dado pessoal; sem servidor; navegadores Edge ou Chrome; o custo de parada depende de parâmetros aprovados pela coordenadoria; requisito de acessibilidade.
**Dados pessoais tratados:** Nenhum dado pessoal. O app guarda equipamentos, unidades, contratos, manutenções, paradas e fotos dos equipamentos. O responsável é registrado por cargo ou matrícula, nunca por CPF.
**Base legal:** Execução de atribuição da Coordenadoria de qualidade (gestão dos equipamentos do órgão). Não há tratamento de dado pessoal.
**Retenção:** Os dados de equipamentos acompanham a vida útil do equipamento; paradas e manutenções ficam por 5 anos para comparação.
**Acesso e registro:** A cópia da unidade guarda só os equipamentos da unidade; a cópia da coordenadoria consolida todas. Toda alteração registra data, cópia de origem e cargo de quem alterou.
**Requisitos marcados:** Acessibilidade, Funcionar offline, Impressão em formato oficial

---

# Anexo A — AS-IS (o fluxo de hoje)

**Início:** Um equipamento apresenta defeito ou para em uma unidade.
**Fim:** O equipamento volta a operar (ou é baixado) e o comprovante da manutenção é arquivado.
**Entradas:** Documentos comprovantes de manutenções 
**Saídas:** Laudo e a carteira de identidade 
**Volume:** 200
**Duração:** 500
**Frequência:** Mensal
| Etapa | Quem faz | O que entra | Ação | O que sai | Sistema | Regra | Onde espera | Tempo (h) | Automatizável |
|---|---|---|---|---|---|---|---|---|---|
| Identificar o defeito | Servidor da unidade | Equipamento com defeito | Percebe a falha e avisa a chefia | Aviso por e-mail ou telefone | E-mail e telefone | Equipamento parado ou com falha | Até a chefia ver o aviso | A medir | Pouco |
| Verificar o contrato | Chefia da unidade | Aviso do defeito | Procura se o equipamento tem contrato de manutenção vigente | Com ou sem contrato | Pastas e PDFs de contratos | Contrato vigente aciona o fornecedor | Busca de documentos | A medir | Sim, com regra clara |
| Providenciar a manutenção | Chefia da unidade | Situação do contrato | Aciona o fornecedor ou pede orçamento e abre a contratação | Manutenção solicitada | E-mail e processo de contratação | Sem contrato: orçamento e contratação | Orçamento e contratação | A medir | Pouco |
| Executar a manutenção | Fornecedor | Solicitação | Conserta ou substitui o equipamento | Equipamento operando e comprovante | Externo | Prazo do contrato, quando houver | Agenda do fornecedor | A medir | Não |
| Arquivar o comprovante | Chefia da unidade | Comprovante de manutenção | Guarda o comprovante em papel ou PDF | Comprovante arquivado | Pasta física ou digital | Guardar o comprovante | Não identificado | A medir | Sim, com apoio humano |
| Consolidar o impacto | Coordenadoria de qualidade | Informações das unidades | Tenta reunir equipamentos, paradas e custos numa planilha | Planilha parcial | Planilha | Sem regra definida | Retorno das unidades | A medir | Sim, com regra clara |

**Decisões e aprovações:** O equipamento tem contrato de manutenção vigente? Se sim, aciona o fornecedor do contrato; se não, a chefia pede orçamento ou abre a contratação. O setor tem outro equipamento igual para continuar o trabalho?
**Exceções:** Equipamento sem contrato e sem substituto na unidade: o setor para até a manutenção. Contrato vencido sem que a unidade saiba. Comprovante de manutenção perdido.
**Já digitalizado:** Em parte: e-mails, PDFs de comprovantes e uma planilha parcial. Não há base única dos equipamentos nem do histórico de manutenção.

# Anexo B — TO-BE (o fluxo depois da mudança)

**Visão do futuro:** Quando o app existir, a coordenadoria vê no mapa de MT cada equipamento da POLITEC, sabe quais estão sem contrato e quanto custa, por dia, a parada de cada um, por unidade e por diretoria.
**Mudança principal:** O cadastro dos equipamentos, contratos, manutenções e paradas passa a ficar numa base única, e o app calcula o risco e o custo de parada. Por isso, a decisão de contratar manutenção passa a ter número.
**O que fica igual:** A manutenção continua com os fornecedores; a contratação segue o rito da Lei nº 14.133/2021; a decisão de contratar continua com a chefia e a diretoria.
**O que não pode mudar:** Não registrar dado pessoal; o custo de parada usa parâmetros definidos pela coordenadoria; o app não substitui o controle patrimonial oficial.
| Etapa | O que muda | Quem executa | Benefício | Esforço |
|---|---|---|---|---|
| Cadastrar equipamentos e contratos | Base única com fotos, contrato e criticidade | A pessoa assistida pela máquina | Saber o que existe e onde | Médio |
| Registrar a parada | A unidade abre e fecha a parada no app | A pessoa assistida pela máquina | Histórico de paradas | Baixo |
| Calcular risco e custo de parada | O app calcula por equipamento, unidade e diretoria | A máquina (automação) | Decisão com número | Médio |
| Alertar contratos a vencer | Aviso 60 dias antes do fim | A máquina (automação) | Nenhum contrato vence sem aviso | Baixo |
| Consolidar as unidades | A coordenadoria importa os arquivos e o app mescla | A pessoa assistida pela máquina | Visão do estado | Médio |
| Ver no mapa e no Google Earth | Mapa offline e exportação .kmz | A máquina (automação) | Localização de cada equipamento | Médio |
| Decidir a contratação | A chefia decide com o relatório de exposição | A pessoa, sem mudança | Prioridade pelo custo | Baixo |

**Piloto do TO-BE:** Piloto de 30 dias em 3 unidades, com a coordenadoria consolidando os arquivos das unidades toda semana.

# Anexo C — Pesquisa, riscos e plano

**Hipótese de campo:** Uma parte dos equipamentos críticos não tem contrato nem substituto na unidade, e a parada de um deles custa mais por dia do que a manutenção preventiva por mês.
| Referência | Tipo | Fonte ou link | Ano | Dado que extrai | Como usar na defesa | Link conferido |
|---|---|---|---|---|---|---|
| Malha Municipal de Mato Grosso | Dado oficial | IBGE, malhas territoriais | 2024 | Contorno dos 142 municípios de MT | Base do mapa offline | Não |
| Lei nº 14.133/2021 (Nova Lei de Licitações) | Norma ou lei | Planalto | 2021 | Contratação de serviços de manutenção | Mostrar que a contratação continua no rito legal | Não |
| Formato KML | Documento interno | Google, documentação do KML | 2026 | Estrutura de Placemark, Folder e Style | Base da exportação para o Google Earth | Não |

**Lacunas:** Não há contagem atual de equipamentos sem contrato nem registro de paradas; o valor de referência do atendimento perdido ainda não foi definido.
| Marco | Data | Responsável | Depende de | Situação |
|---|---|---|---|---|
| Escopo validado com a coordenadora | Semana 1 | Aluno | Leitura do contexto.md | Planejado |
| Lista de unidades e planilha atual reunidas | Semana 1 | Aluno | Coordenadoria | Planejado |
| Cadastro de equipamentos com fotos | Semana 4 | Aluno | Esqueleto do app | Planejado |
| Custo de parada e mapa offline | Semana 7 | Aluno | Parâmetros aprovados | Planejado |
| Exportação para o Google Earth | Semana 9 | Aluno | Mapa e fotos | Planejado |
| Piloto de 30 dias em 3 unidades | Semana 12 | Aluno e coordenadora | Aceite | Planejado |

| Risco | Probabilidade | Impacto | Mitigação |
|---|---|---|---|
| Lista de unidades e equipamentos incompleta | Alta | Alto | Começar pelas 3 unidades do piloto e completar aos poucos |
| Custo de parada contestado | Média | Médio | Parâmetros aprovados pela coordenadoria e fórmula visível |
| Fotos ocupam espaço demais | Média | Baixo | Compressão para cerca de 200 KB por foto |
| Arquivos das unidades geram duplicados | Média | Médio | Identificador único e tela de conflitos |

**Apoio necessário:** Minha Coordenadora e bem acessível 
**Aprendizado necessário:** Modelagem de processo 

# Anexo D — A defesa

**Frase de defesa:** Se a POLITEC souber quanto custa, por dia, a parada de cada equipamento crítico sem contrato, a decisão de contratar manutenção passa a ter número.
**Provas:** 1) Não há ferramenta de acompanhamento hoje (entrevista com a equipe). 2) Há equipamentos cuja parada interrompe o setor inteiro (informado pelo aluno). 3) O piloto mede a exposição diária nas 3 unidades.
**Piloto:** Piloto de 30 dias 
**Maior risco:** O custo de parada ser contestado. Mitigação: parâmetros visíveis e aprovados pela coordenadoria, com a fórmula ao lado de cada número.

# Anexo E — Documentos enviados

**Descrição dos documentos:** Nenhum documento enviado.
**O que ainda falta:** Planilha atual de equipamentos; lista de unidades e diretorias; exemplo de comprovante de manutenção; contratos vigentes.
