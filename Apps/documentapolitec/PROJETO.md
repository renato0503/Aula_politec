# PROJETO.md — DOCUMENTAPOLITEC

**Aluno ou equipe:** Aline Xavier dos Passos
**Unidade:** Coordenadoria de Patrimônio e Serviços
**Contato:** alinepassos@politec.mt.gov.br
**Projeto:** DOCUMENTAPOLITEC
**Tipo de projeto:** Aplicativo (app) para cidadão, servidor ou equipe
**Data:** 2026-10-27
**Resumo:** Preciso criar um aplicativo para controlar os prontuários civis que serão encaminhados para o arquivo central

## 1. Problema (a dor)

**Problema:** Não há espaço físico e precisamos utilizar outra estrutura para guarda de prontuários e laudos periciais
**Impacto:** Falta de espaço de armazenamento e risco de extravio
**Quem sofre:** Servidor da unidade, Equipe interna, Chefia
**Como é feito hoje:** Hoje os prontuários são digitalizados, e são arquivados em sala cofre. Precisamos criar um app que faça a conferencia da relação dos prontuários que estão em determinada caixa para que a mesma seja alocada em novo setor, sem prejuízo de informação equivocada. estamos falando de um montante de 1000 (mil) caixas box.
**Evidências:** Entrevista com a equipe
**Detalhe da evidência:** -
**O que não pode ser automatizado:** A conferência dos dados e  quantitativo e o campo de assinatura de quem está lacrando a caixa.

## 2. Objetivo do MVP (o que faz e o que NÃO faz)

**Objetivo do MVP:** Demonstrar que a relação de prontuários de cada caixa pode ser conferida com o arquivo digital, que a caixa pode ser lacrada com responsável e que o prontuário pode ser localizado pelo número.
**O que o MVP não faz:** -
**Entregável do projeto:** aplicativo ou sistema de conferência
**Dentro do escopo:** leitura do arquivo digitalizado
**Fora do escopo:** o armazenamento de  dados sensíveis pela IA
**Plataforma alvo:** Site web (abre no navegador)
**Primeira tela:** tela de login
**Simulado no MVP:** -
**Critério de aceite:** O papiloscopista vai mostrar a integridade dos arquivos físicos com os digitalizados
**Dados de exemplo:** Histórico de busca
**O que já existe pronto e pode ser reaproveitado:** melhor reiniciar do 0
**Dependências:** Servidores e gestão documental e especificação das caixas


## 3. Usuários e papéis

| Papel | Quem é | O que enxerga | O que faz | O que não pode fazer | Registro |
|---|---|---|---|---|---|
| Papiloscopista | Servidor da DMIT designado | Relação da caixa, arquivo digital e lacre | Confere, atesta a veracidade, lacra e registra | Lacrar sem conferência ou sem assinatura | Conferência, lacre, responsável e data |
| Gestor documental | Chefia da Coordenadoria de Patrimônio | Caixas conferidas, pendentes e divergências | Acompanha o acervo e libera a transferência | Alterar a relação sem justificativa | Ações de gestão |
| Servidor da unidade | Qualquer servidor autorizado | Número do prontuário e caixa | Consulta onde está o prontuário físico | Retirar prontuário sem registro | Consultas realizadas |

**Observações sobre os papéis:** O Papiloscopista que atesta a veracidade, confere e lista os números dos prontuários, bem como é o agente que lacra a caixa para ser encaminhada para o arquivo permanente.

## 4. Dados (entidades e colunas; tudo SINTÉTICO)

| Entidade | O que representa | Colunas | Chave | Volume | Origem | Sintético |
|---|---|---|---|---|---|---|
| Caixa | Caixa box com a relação de prontuários | id_caixa; setor_origem; responsavel; data; qtd; status; lacrada_por; lacrada_em | id_caixa | 1.000 caixas | Planilha e cadastro | Sim |
| Prontuário | Prontuário civil da relação | numero; caixa_id; conferido; digital | numero | 2,5 milhões | Relação de cada caixa | Sim |
| Log | Trilha de conferência e lacre | id; caixa_id; acao; perfil; data_hora; detalhe | id | — | App | Sim |

**O que precisa ser coletado:** Digitalização
**Quem libera o acesso:** A DMIT

### Fontes de dados do processo real

| Fonte | Tipo | Onde | Existe | Uma linha é | Volume | Campos de data | Atualiza | LGPD |
|---|---|---|---|---|---|---|---|---|
| Relação de prontuários | Planilha | DMIT | Sim | Um prontuário por linha, com o número | 850 na planilha de teste; 2,5 milhões no acervo | numero | Por demanda | Sim |
| Prontuários digitalizados | Sistema oficial | SIC e repositório | Sim | Um PDF por prontuário | 2,5 milhões | numero, caixa, data | Contínua | Sim |
| Caixas físicas | Cadastro interno | Sala cofre | Parcial | Uma caixa com etiqueta | 1.000 | id_caixa, setor, lacre | Por demanda | Não |


## 5. Regras de negócio (RN01, RN02...)

| ID | Regra | Quando se aplica | Exceção | Quem valida | Tipo |
|---|---|---|---|---|---|
| RN01 | O mesmo prontuário não pode estar em duas caixas nem repetido na relação | No cadastro da caixa | Nenhuma | Sistema | Validação |
| RN02 | A caixa só é conferida e lacrada quando todos os prontuários conferem com o arquivo digital e há responsável | Na conferência | Divergência fica pendente | Papiloscopista | Negócio |
| RN03 | A busca devolve a caixa onde o prontuário físico está arquivado | Na busca | Prontuário fora do acervo | Sistema | Negócio |


## 6. Telas (#/painel, #/lista...)

| Rota | Tela | Objetivo | Quem usa | Dados | Ação | Regra | Tipo | Verificável como | MVP |
|---|---|---|---|---|---|---|---|---|---|
| #/caixa/nova | Nova caixa | Registrar a caixa e a relação de prontuários | Papiloscopista | Identificação da caixa, setor, responsável e relação | Colar a relação e salvar | RN01: prontuário único | Tela | Caixa criada com a relação completa | Sim |
| #/caixa/:id | Caixa e conferência | Conferir a relação e lacrar | Papiloscopista | Prontuários, correspondência digital e lacre | Conferir e lacrar | RN02: só lacra sem divergência | Tela | Caixa conferida e lacrada com responsável | Sim |
| #/busca | Busca | Localizar a caixa do prontuário | Servidor | Número do prontuário | Buscar | RN03: devolve a caixa | Tela | Resultado com a caixa e o setor | Sim |
| #/painel | Painel | Acompanhar caixas conferidas e pendentes | Gestor | Contagens e divergências | Consultar | — | Tela | Indicadores conferem com a base | Sim |


## 7. KPIs (nome = fórmula em uma linha)

| KPI | Pergunta | Fórmula | Fonte | Linha de base | Valor esperado | Como medir |
|---|---|---|---|---|---|---|
| Tempo de conferência por caixa | Quanto tempo o papiloscopista gasta para conferir a relação de uma caixa? | Soma do tempo de conferência / número de caixas | Registro do app | 4 h por caixa (estimado) | 30 min por caixa | Cronometrar 10 caixas antes e depois |
| Tempo de busca do prontuário | Quanto tempo se leva para localizar o prontuário físico? | Soma do tempo de busca / número de buscas | Registro do app | 20 min | 2 min | Cronometrar 10 buscas |

**Período da linha de base:** todos os 2.500.000 prontuários
**Campos de data e tempo que existem:** Não se aplica

## 8. Stack: HTML único (CSS/JS inline), dados em JSON embutido, GitHub Pages.

**Stack escolhida:** Aplicativo web com framework (React, Vite, TypeScript)
**Detalhe da stack:** Um único index.html (HTML, CSS e JS embutidos), com dados no IndexedDB do navegador e backup .json, publicado no GitHub Pages. A conferência do arquivo digitalizado é simulada no MVP; a leitura do PDF e a integração com o SIC ficam fora do protótipo.
**Hospedagem:** Aplicativo, para facilitar o acesso pelo celular ou na web na rede funcional
**Custo e licenças:** -
**Contas e domínio:** -

| Opção | Tipo | Onde roda | Custo | Quem mantém | Acesso | Banco de dados | Escala | Limitação |
|---|---|---|---|---|---|---|---|---|
| Arquivo HTML local | Arquivo local | Computador da unidade | Zero | Equipe do projeto | Quem recebe o arquivo | IndexedDB do navegador | Uma cópia por setor | Backup manual em .json |
| GitHub Pages | Estática e gratuita | github.io | Zero | Equipe do projeto | Link do protótipo | Não tem | Baixa | Só o app, nunca os dados |


## 9. Restrições e LGPD

**Restrições:** -
**Dados pessoais tratados:** numero do prontuário 
**Base legal:** -
**Retenção:** -
**Acesso e registro:** versão com login e senha, para apenas servidores indicados.
**Requisitos marcados:** LGPD e dado pessoal, Segurança e controle de acesso, Funcionar offline, Trilha de auditoria

---

# Anexo A — AS-IS (o fluxo de hoje)

**Início:** Entrada do Prontuário no arquivo corrente
**Fim:** saída do arquivo corrente para a guarda permanente
**Entradas:** digitalização do prontuário, conferência, e lacramento.
**Saídas:** Guarda permanente em nova estrutura
**Volume:** 2.500.000
**Duração:** -
**Frequência:** Por demanda
| Etapa | Quem faz | O que entra | Ação | O que sai | Sistema | Regra | Onde espera | Tempo (h) | Automatizável |
|---|---|---|---|---|---|---|---|---|---|
| 1. Digitalização | Papiloscopista | Prontuário físico | Digitaliza e arquiva o PDF | PDF no repositório | SIC / repositório | Integridade do arquivo | Arquivo corrente | 2 min | Pouco |
| 2. Conferência da relação | Papiloscopista | Relação de prontuários da caixa | Confere um por um com o digital | Relação conferida | Planilha | Se os dados conferem, segue (RN02) | Sala cofre | 4 h por caixa | Não |
| 3. Lacre | Papiloscopista | Caixa conferida | Lacra e assina o lacre | Caixa lacrada | Presencial | Responsável identificado | Sala cofre | 20 min | Não |
| 4. Transferência | Equipe de patrimônio | Caixa lacrada | Transporta para o arquivo central | Caixa na guarda permanente | Presencial | Integridade do lacre | Aguarda transporte | 1 h | Não |
| 5. Busca do prontuário | Servidor da unidade | Número do prontuário | Procura na planilha e na sala | Localização do físico | Planilha | — | Sala cofre | 20 min | Não |

**Decisões e aprovações:** Se os dados conferem, segue para arquivo permanente
**Exceções:** Prontuário sem correspondência no arquivo digital, relação repetida, caixa com lacre violado e prontuário de outra caixa. Todos exigem conferência humana e registro antes de seguir.
**Já digitalizado:** a digitalização dos prontuários

# Anexo B — TO-BE (o fluxo depois da mudança)

**Visão do futuro:** a conferência dos prontuários físicos com os arquivos digitalizados por meio de compara automatizado, e posterior busca por nome do cidadão para identificar numero da caixa que o fisico está aquivado
**Mudança principal:** automatizar essa conferência, sem a necessidade de conferir um por um, após a digitalização.
**O que fica igual:** A organização e conferência inicial permanece a cargo do servidor indicado pela DMIT
**O que não pode mudar:** os dados e informações constantes nos prontuários
| Etapa | O que muda | Quem executa | Benefício | Esforço |
|---|---|---|---|---|
| Arquivo Permanente | Conferência automatizada | A máquina (automação) | mais ganho de tempo e menos retrabalho | Médio |
| Conferência da relação | Comparação automática da relação com o arquivo digital | A máquina (automação) | Menos retrabalho e menos conferência manual | Médio |
| Busca do prontuário | Consulta pelo número devolve a caixa e o setor | A máquina (automação) | Menos tempo de busca | Baixo |
| Lacre | Registro do responsável, da data e da relação no app | A pessoa assistida pela máquina | Rastreabilidade do lacre | Baixo |

**Piloto do TO-BE:** Piloto de 30 dias, com 2400 prontuários

# Anexo C — Pesquisa, riscos e plano

**Hipótese de campo:** -
| Referência | Tipo | Fonte ou link | Ano | Dado que extrai | Como usar na defesa | Link conferido |
|---|---|---|---|---|---|---|
| Lei nº 8.159/1991 | Norma ou lei | Política nacional de arquivos públicos e privados | 1991 | Guarda, classificação e destinação de documentos | Sustenta a separação entre arquivo corrente e guarda permanente | Não |
| Lei nº 13.709/2018 (LGPD) | Norma ou lei | Planalto | 2018 | Tratamento de dados pessoais | Justifica o acesso restrito e a busca por nome só com base legal | Sim |

**Lacunas:** -
| Marco | Data | Responsável | Depende de | Situação |
|---|---|---|---|---|
| Inicial | 29/10 | Aline | execução | Planejado |
| Formato das caixas e do número do prontuário | 06/11/2026 | Aline e DMIT | Reunião com a equipe | Planejado |
| Planilha de 850 prontuários recebida | 13/11/2026 | DMIT | Autorização e exportação | Planejado |
| Conferência e lacre no protótipo | 27/11/2026 | Aline | Dados e regras definidos | Planejado |
| Leitura do PDF digitalizado | 11/12/2026 | Aline | Amostra real do PDF | Planejado |
| Piloto de 30 dias | 29/01/2027 | DMIT | Aceite da chefia | Planejado |

| Risco | Probabilidade | Impacto | Mitigação |
|---|---|---|---|
| incompatibilidade | Média | Médio | Testar o app no navegador da rede funcional e manter cópia local. |
| Prontuário sem correspondência no arquivo digital | Alta | Alto | A conferência para a caixa e mostra a divergência antes do lacre (RN02) |
| Formato do número do prontuário ambíguo | Alta | Médio | Confirmar os dígitos no Sprint 0 e validar na importação |
| Volume de 2,5 milhões de prontuários | Média | Médio | Trabalhar por caixa e paginar a lista; a busca usa índice |

**Apoio necessário:** Preciso reunir novamente com a equipe para definir modelo de dígitos dos prontuários
**Aprendizado necessário:** modelagem de processo, antigravity, leitura para tomada de decisões

# Anexo D — A defesa

**Frase de defesa:** Digitalização que abre espaço para o novo
**Provas:** Atualmente os prontuários são automaticamente gerados dentro do SIC; os prontuários fisicos são de anos anteriores há 2019 e estão ocupando espaço fisico, a digitalização controlada e íntegra, permitirá que a guarda em estrutura adequado, liberando espaço para novos serviços e setores
**Piloto:** teste por 30 dias.
**Maior risco:** A DMIT não validar

# Anexo E — Documentos enviados

**Descrição dos documentos:** planilha teste com relação de 850 prontuários
**O que ainda falta:** Planilha de teste com a relação de 850 prontuários; modelo dos dígitos do prontuário; amostra do PDF digitalizado.
