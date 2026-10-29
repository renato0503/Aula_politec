# PROJETO.md — Emissão 2via da CIN remoto

**Aluno ou equipe:** Equipe - CIN (André, Flávia e Glauce)
**Unidade:** Politec
**Contato:** glaucesilva@politec.mt.gov.br
**Projeto:** Emissão 2via da CIN remoto
**Tipo de projeto:** Aplicativo (app) para cidadão, servidor ou equipe
**Data:** 2026-10-27
**Resumo:** Aplicativo que possibilita a solicitação da segunda via da CIN de maneira remota

## 1. Problema (a dor)

**Problema:** A solicitação de 2 via da emissão da CIN traz burocracia para o requerente, ainda que a primeira via esteja em data de validade aceita
**Impacto:** O tempo  médio para a entrega do documento são 15 dias, acontece retrabalho para os servidores e o requerente pode ter custos com a solicitação
**Quem sofre:** Cidadão externo, Servidor da unidade, Equipe interna, Unidade parceira
**Como é feito hoje:** O requerente (ainda que exista a CIN digital válida e a extraviada com data de validade dentro do prazo) precisa se dirigir a um posto de identificação e realizar nova coleta biométrica bem como apresentar documentação para a solicitação da segunda via
**Evidências:** Entrevista com a equipe
**Detalhe da evidência:** Entrevista com a equipe de identificação: tempo médio de 15 dias e reclamações dos usuários.
**O que não pode ser automatizado:** Análise e confronto realizado pelo papiloscopista

## 2. Objetivo do MVP (o que faz e o que NÃO faz)

**Objetivo do MVP:** Provar que o cidadão consegue pedir a segunda via pelo celular, que o pedido chega ao servidor completo e que a regra de elegibilidade (primeira via válida, sem mudança de dados) separa o que pode seguir sem ir ao posto.
**O que o MVP não faz:** Não coleta biometria real, não faz confronto papiloscópico, não envia ao sistema de identificação civil nem à Receita Federal e não emite a CIN.
**Entregável do projeto:** Aplicativo de solicitação de emissão/ reimpressão de 2via
**Dentro do escopo:** Lançamento da solicitação de emissão de 2via sem novo cadastro no posto de identificação
**Fora do escopo:** Envio do registro civil, análise e confronto
**Plataforma alvo:** Site web (abre no navegador)
**Primeira tela:** Cadastro
**Simulado no MVP:** O envio ao sistema de identificação civil é simulado (o servidor copia o resumo). A foto do teste é fictícia e não é biometria; a coleta biométrica real depende da empresa contratada.
**Critério de aceite:** Com 30 pedidos fictícios, o cidadão envia o pedido pelo celular e recebe o protocolo; o servidor vê a fila, confere a elegibilidade, aceita ou recusa com motivo e gera o resumo para lançar no sistema de identificação civil.
**Dados de exemplo:** 30 pedidos fictícios (nomes inventados, CPF de teste com dígito válido, fotos geradas sem pessoas reais), com casos elegíveis, CIN vencida, mudança de dados e foto ilegível.
**O que já existe pronto e pode ser reaproveitado:** Já existe o sistema de identificação civil
**Dependências:** TI, empresa parceira, chefia. 

## 3. Usuários e papéis

| Papel | Quem é | O que enxerga | O que faz | O que não pode fazer | Registro |
|---|---|---|---|---|---|
| Cadastro | Atendente do posto de identificação | Página de cadastro biográfico e biométrico | Cadastro e Coleta Biométrica | Preencher incorretamente, não coletar a biometia, não enviar, via sistema, o prontuário | Prontuário |
| Análise e Confronto | Papiloscopistas | Página do sistema com os dados e a biometria | Analisa os documentos e confronta as impressões digitais, se necessário | Demorar para o atendimento, não realizar o confronto, não enviar para o sistema | Prontuário/Impressão |
| Impressão | Parque gráfico - empresa licitada | Sistema de impressão | Impressão das cédulas/cartões | Não imprimir, imprimir duplicado | Cédulas/cartões da CIN |
| Envio ao postos | Setor de expediente | Documento físico e sistema para dar baixa | Recebe os documentos, dá baixa no sistema e encaminha para o posto de identificação | Extraviar documentos, Envio para posto incorreto, atrasar no envio | Baixa "enviado ao posto" |
| Entrega ao requerente | Atendente do Posto de Identificação  | Sistema e documento físico | Entrega ao requerente o documento | Extraviar, entregar incorretamente | Baixa no sistema |

**Observações sobre os papéis:** A impressão depende da validação da Receita Federal (com um sistema diferente do nosso e que não temos acesso)

## 4. Dados (entidades e colunas; tudo SINTÉTICO)

| Entidade | O que representa | Colunas | Chave | Volume | Origem | Sintético |
|---|---|---|---|---|---|---|
| Pedido | Pedido de segunda via | protocolo: texto, nome: texto, cpf: texto, nascimento: data, numero_cin: texto, validade_cin: data, mudou_dados: lógico, contato: texto, criado_em: data, situacao: texto, motivo: texto | protocolo | 30 no teste | Cidadão (fictício) | Sim |
| Foto | Foto enviada pelo cidadão | id: texto, protocolo: texto, tipo: texto (rosto, documento), conteudo: binário | id | 2 por pedido | Cidadão (fictício) | Sim |
| Decisao | Conferência do servidor | id: texto, protocolo: texto, resultado: texto, motivo: texto, servidor: texto, data: data | id | 1 por pedido | Servidor | Sim |

**O que precisa ser coletado:** Hoje não existe uma planilha/sistema com a solicitação de reimpressão/emissão de 2via
**Quem libera o acesso:** A gestão libera a planilha para os servidores que fazem o atendimento

### Fontes de dados do processo real

| Fonte | Tipo | Onde | Existe | Uma linha é | Volume | Campos de data | Atualiza | LGPD |
|---|---|---|---|---|---|---|---|---|
| Cadastro | Planilha local | Planilha da unidade | Não | Uma solicitação | 30 solicitações | Data de entrada da solicitação | Conforme solicitado | Sim |
| Prontuário | Banco de dados | Sistema de Identificação Civil | Sim | Um prontuário | 30 Solicitações | Data de entrada | Conforme solicitação | Sim |


## 5. Regras de negócio (RN01, RN02...)

| ID | Regra | Quando se aplica | Exceção | Quem valida | Tipo |
|---|---|---|---|---|---|
| RN01 | Precisa de CPF válido | Todos os casos | Não tem | Sistema | Validação |
| RN02 | Precisa da Biometria coletada | Todos os cados | Não tem  | Sistema/Papiloscopista | Validação |
| RN03 | Só segue a distância se a primeira via estiver válida e não houver mudança de dados | No pedido | Os demais casos são orientados a ir ao posto | Sistema | Negócio |
| RN04 | Foto obrigatória de rosto e de documento, legível | No pedido | Nenhuma | Sistema e servidor | Validação |
| RN05 | Recusa sempre com motivo, que o cidadão vê no protocolo | Na conferência | Nenhuma | Servidor | Negócio |
| RN06 | Pedido e foto apagados após o lançamento ou a recusa | Após a decisão | Nenhuma | Sistema | LGPD |


## 6. Telas (#/painel, #/lista...)

| Rota | Tela | Objetivo | Quem usa | Dados | Ação | Regra | Tipo | Verificável como | MVP |
|---|---|---|---|---|---|---|---|---|---|
| #/pedido | Pedido da segunda via | Pedir sem ir ao posto | Cidadão | Nome, CPF, nascimento, número da CIN, contato, foto | Enviar | RN01 a RN04 | Tela | Pedido completo gera protocolo | Sim |
| #/protocolo/:id | Protocolo | Acompanhar o pedido | Cidadão | Protocolo, situação, próximo passo | Consultar |  | Tela | Situação muda quando o servidor decide | Sim |
| #/fila | Fila do servidor | Conferir os pedidos | Servidor | Pedidos, elegibilidade, foto | Aceitar ou recusar com motivo | RN05 | Tela | Recusado sai com o motivo | Sim |
| #/pedido/:id/resumo | Resumo para o sistema | Lançar no sistema de identificação civil | Servidor | Dados do pedido no formato do sistema | Copiar ou imprimir |  | Ação | Resumo tem todos os campos do cadastro | Sim |
| #/indicadores | Indicadores | Medir o piloto | Gestão | Pedidos, aceitos, recusados, tempo | Consultar |  | Relatório | Bate com a contagem da fila | Sim |


## 7. KPIs (nome = fórmula em uma linha)

| KPI | Pergunta | Fórmula | Fonte | Linha de base | Valor esperado | Como medir |
|---|---|---|---|---|---|---|
| Tempo de emissão | Tempo do processo  | soma do tempo da solicitação a emissão |  | a medir | a medir | Somar a data da entrada |
| Pedidos elegíveis | Quantos pedidos podem seguir sem ir ao posto? | Elegíveis ÷ pedidos × 100 | Fila | A medir | A medir no piloto | Contar na fila |

**Período da linha de base:** Solicitações a partir da  implementação
**Campos de data e tempo que existem:** Data da solicitação, data da entrada no sistema, data de emissão

## 8. Stack: HTML único (CSS/JS inline), dados em JSON embutido, GitHub Pages.

**Stack escolhida:** HTML único (CSS/JS inline), dados em JSON embutido, GitHub Pages
**Detalhe da stack:** Um único index.html (HTML, CSS e JS embutidos), com a câmera do celular pelo navegador (getUserMedia) e os pedidos no IndexedDB. Perfis: cidadão (pedido e protocolo) e servidor (fila e conferência). Sem servidor no MVP.
**Hospedagem:** Para o protótipo: arquivo HTML único no GitHub Pages, com os pedidos guardados no navegador. Em produção, o pedido precisa de um servidor institucional integrado ao sistema de identificação civil.
**Custo e licenças:** A princípio sem custos. Mas previsto o valor de contratação de empresa que crie o app para a coleta biométrica (por foto)
**Contas e domínio:** Servidor com conta no github

| Opção | Tipo | Onde roda | Custo | Quem mantém | Acesso | Banco de dados | Escala | Limitação |
|---|---|---|---|---|---|---|---|---|
| GitHub Pages | Estática e gratuita | github.io, a partir de um repositório | Gratuito | O aluno, com a conta institucional | Público ou privado, conforme o repositório | Não tem | Serve a página estática | Só site estático: sem servidor, sem banco de dados e sem autenticação |


## 9. Restrições e LGPD

**Restrições:** Precisa de integração com o sistema oficial de identificação civil
**Dados pessoais tratados:** Nome, CPF, data de nascimento, número da CIN, contato e foto. Foto e biometria são dados sensíveis (LGPD, art. 11); no MVP, só dados fictícios.
**Base legal:** Execução de serviço público
**Retenção:** Pedido e foto apagados após o lançamento no sistema de identificação civil ou a recusa; no MVP, dados fictícios no navegador.
**Acesso e registro:** Requerente acessa para a solicitação. Servidor acessa para o procedimento de emissão
**Requisitos marcados:** Acessibilidade, Funcionar offline, Integração com sistema oficial, LGPD e dado pessoal, Segurança e controle de acesso

---

# Anexo A — AS-IS (o fluxo de hoje)

**Início:** Requerente solicita 2 via da CIN
**Fim:** Entrega do documento
**Entradas:** Documento de Registro civil, biometria, 
**Saídas:** CIN impressa
**Volume:** 21000 solicitações
**Duração:** 15 dias em média
**Frequência:** Mensal
| Etapa | Quem faz | O que entra | Ação | O que sai | Sistema | Regra | Onde espera | Tempo (h) | Automatizável |
|---|---|---|---|---|---|---|---|---|---|
| Solicitação | Requerente | Dados biométricos e biográficos | Cadastro | Prontuário | Sistema | Dados conferem com o registro civil | Análise e Confronto | 1 | Sim, com apoio humano |
| Análise e Confronto | Papiloscopista | Prontuário | Análise e Confronto | Prontuário | Sistema | Confronto quando houver dúvida | Impressão | 72 | Sim, com apoio humano |
| Impressão | Parque gráfico | Prontuário | Impressão | Cédula/cartão | Papel/Sistema | Validação pela Receita Federal | Expediente | 168 | Sim, com regra clara |
| Envio ao posto | Setor de expediente | Cédulas/cartão | Envio dos documento | Cédulas | Sistema/Papel | Posto de destino correto | Posto de Identificação | 48 | Não |
| Entrega ao Requerente | Posto de Identificação | Cédulas/Cartões | Entrega ao requerente | Cédulas/cartões | Papel/Sistema | Documento entregue ao titular | Arquivo |  | Não |

**Decisões e aprovações:** Caso não passe pela análise, o processo é devolvido para o posto de identificação.
Caso exista divergência com a Receita Federal, não acontece a impressão.
**Exceções:** Processos recusados poderiam ser devolvidos automaticamente.
**Já digitalizado:** Digitação via sistema, análise e confronto via sistema, envio para impressão pelo sistema. 

# Anexo B — TO-BE (o fluxo depois da mudança)

**Visão do futuro:** Quando esse processo existir, o requerente deixa de esperar tanto tempo para a emissão da segunda via e passa a ter o documento com mais agilidade.
**Mudança principal:** Automação na solicitação do processo da segunda via, através de algum aplicativo para celular.
**O que fica igual:** A entrega para o cidadão permanece
**O que não pode mudar:** O confronto das impressões digitais
| Etapa | O que muda | Quem executa | Benefício | Esforço |
|---|---|---|---|---|
| Solicitação | Processo por app | A máquina (automação) | Agilidade no processo | Alto |
| Confronto papiloscópico | Não muda, permanece no sistema | A pessoa, sem mudança | Permanece com prazo menor | Médio |
| Impressão | Não muda | A máquina (automação) | Agilidade no processo | Baixo |
| Envio ao posto | Não muda | A pessoa assistida pela máquina | Maior agilidade | Baixo |
| Entrega ao requerente | Tempo menor | A pessoa, sem mudança | Menor prazo de entrega | Baixo |

**Piloto do TO-BE:** Piloto de 30 dias, observando o tempo médio da emissão desde a solicitação.

# Anexo C — Pesquisa, riscos e plano

**Hipótese de campo:** O processo, para o requerente, é burocrático e lento para a impressão de um documento que já havia sido oficializado e com data de validade dentro do prazo
| Referência | Tipo | Fonte ou link | Ano | Dado que extrai | Como usar na defesa | Link conferido |
|---|---|---|---|---|---|---|
| Lei Geral de Proteção de Dados, art. 11 (dados sensíveis) | Norma ou lei | Lei nº 13.709/2018, Planalto | 2018 | Biometria é dado pessoal sensível | Justificar o MVP sem biometria real | Não |
| Decreto nº 10.977/2022 (Carteira de Identidade Nacional) | Norma ou lei | Planalto | 2022 | Regras de emissão da CIN | Base das regras de elegibilidade | Não |

**Lacunas:** Não há registro de quantas segundas vias são de CIN válida sem mudança de dados (o público do app). Também falta a posição da TI e da empresa da coleta biométrica sobre a integração.
| Marco | Data | Responsável | Depende de | Situação |
|---|---|---|---|---|
| Criação | 2027 | Coordenadoria de Identificação Civil | TI | Planejado |
| Implementação | 2027 | TI e Coordenadoria de Identificação Civil | TI | Planejado |

| Risco | Probabilidade | Impacto | Mitigação |
|---|---|---|---|
| Cadastro incorreto | Alta | Alto | Interface de fácil compreensão pelo usuário |
| Falta de biometria | Baixa | Alto | Não deixar encaminhar a solicitação sem toda a coleta |
| Fraude com foto de outra pessoa | Média | Alto | Em produção, prova de vida e confronto pela empresa contratada; no MVP, só dados fictícios |
| Vazamento de dado sensível | Baixa | Alto | Sem dados reais no MVP; em produção, servidor institucional e apagamento após o lançamento |

**Apoio necessário:** Preciso alinhar com a equipe de TI
**Aprendizado necessário:** GitHub

# Anexo D — A defesa

**Frase de defesa:** Se o tempo de impressão de 2vias válidas passaram a 5 dias úteis, o índice de satisfação do cidadão aumentará
**Provas:** 1-Tempo médio de emissão de 15 dias
2-Reclamações por usuários
3-Grande demanda por emissão de 2vias no estado
**Piloto:** Piloto em 30 dias para verificar se a solicitação chega diretamente
**Maior risco:** Dificuldade de usabilidade pelo cidadão. Mitigar com interface de fácil compreensão.

# Anexo E — Documentos enviados

**Descrição dos documentos:** Nenhum documento enviado.
**O que ainda falta:** Fonte do tempo médio de 15 dias e das 21.000 solicitações; regras oficiais da segunda via; posição da TI sobre a integração.
