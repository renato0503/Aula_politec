# PROJETO.md — Sistema de Controle de Necropsia

**Aluno ou equipe:** Silmara Bueno
**Unidade:** IML — Coordenadoria de Perícias em Mortos
**Contato:** silmarabueno@politec.mt.gov.br
**Projeto:** Sistema de Controle de Necropsia
**Tipo de projeto:** Aplicativo (app) para cidadão, servidor ou equipe
**Data:** 2026-11-02
**Resumo:** sistema web que registra e rastreia todo o ciclo do corpo no IML, do acionamento à entrega do laudo à ADM, para técnicos, médicos legistas e gestores da Gerência de Necropsia, no lugar de planilhas e controles manuais dispersos.

## 1. Problema (a dor)

**Problema:** dificuldade em acompanhar e comprovar a custódia do corpo e dos materiais ao longo das sete etapas do processo, porque os registros ficam dispersos em planilhas e controles manuais, e isso causa perda de rastreabilidade, risco de extravio de lacres.
**Impacto:** O impacto de hoje é retrabalho para o técnico, que repete o mesmo registro em quatro livros diferentes e ainda avisa os marcos de deslocamento de forma verbal; custódia sem rastro, com lacres e autos de entrega fora do sistema; corpos não identificados e não reclamados sem controle centralizado, com informação que se perde na passagem de plantão; espera maior para a família; e aviso tardio à autoridade policial, que segue buscando uma vítima já identificada. Nada disso é medido hoje.
**Quem sofre:** Cidadão externo, Servidor da unidade, Equipe interna, Chefia, Autoridade
**Como é feito hoje:** Hoje o processo roda em planilhas, papel e livros de protocolo, e o tempo se perde nas transições entre etapas
**Evidências:** Relatório de sistema, Medida feita pela equipe, Documento ou norma oficial
**Detalhe da evidência:** O impacto de hoje é retrabalho para o técnico, que repete o mesmo registro em quatro livros diferentes e ainda avisa os marcos de deslocamento de forma verbal; custódia sem rastro, com lacres e autos de entrega fora do sistema; corpos não identificados e não reclamados sem controle centralizado, com informação que se perde na passagem de plantão; espera maior para a família; e aviso tardio à autoridade policial, que segue buscando uma vítima já identificada. Nada disso é medido hoje.
**O que não pode ser automatizado:** Não são automatizáveis a necropsia, o laudo, os exames de identificação, as decisões técnicas, a custódia física e a liberação do corpo, porque dependem de julgamento profissional, assinatura de responsabilidade e ato presencial. O sistema automatiza o registro, a geração de documentos, as notificações e o controle de prazos, não o trabalho pericial em si.

## 2. Objetivo do MVP (o que faz e o que NÃO faz)

**Objetivo do MVP:** Provar que o técnico consegue registrar um caso completo de necropsia, da etapa 1 à 7, em um único sistema, com rastreabilidade de lacres e visibilidade de pendências, sem depender de planilha ou papel.
**O que o MVP não faz:** O MVP não integra com laboratórios nem com o CIOP. Não emite laudo. Não faz assinatura com certificado digital. Não gera relatórios gerenciais exportáveis. Não tem aplicativo móvel offline para uso no local da ocorrência. Não controla estoque de insumos. Não faz notificação automática por e-mail ou WhatsApp. Não tem portal de consulta para a família ou para a autoridade policial.

O MVP prova uma coisa só: que é possível registrar o caso inteiro em um único sistema, com rastreabilidade de lacres e visibilidade de pendências, sem perder nenhuma informação que hoje está em papel.

**Entregável do projeto:** Um sistema web de controle de necropsia que registra e rastreia todo o ciclo do corpo em um único registro, da etapa 1 à 7, com trilha de auditoria, controle de recebimento de lacres e visibilidade de pendências.
**Dentro do escopo:** Cadastro do caso com as sete etapas: acionamento, ocorrência e possível vítima, entrada na base, necropsia, identificação, família e liberação, e entrega do laudo à ADM. Controle de materiais coletados com número de lacre e confirmação de recebimento pela ADM. Registro de identificação, incluindo o caminho de corpo não identificado. Registro de liberação a familiar com assinatura digital e de liberação sem familiar com sepultamento pelo Estado. Bloco de funerária com Auto de Entrega. Entrega do laudo à ADM com assinatura de quem recebe. Painel com indicadores e filtros por status. Histórico de mudanças com data, hora e usuário. Três perfis de acesso: Técnico, Médico Legista e Gestor ADM.

**Fora do escopo:** Integração com os laboratórios de toxicologia, genética e balística: depende de sistemas externos que não fazem parte desta gerência. Integração com o CIOP: o acionamento continua chegando por telefone ou rádio. Assinatura digital certificada com validade jurídica: a captura do traço é suficiente para o controle interno nesta fase. Emissão do laudo dentro do sistema: o laudo é produzido pelo médico legista em sistema próprio. Gestão de estoque de materiais e insumos: é outro processo, de outra área.
**Plataforma alvo:** Aplicativo de celular
**Primeira tela:** Tela de login com matrícula funcional e seleção de perfil. Depois do login, o painel de indicadores com os cards de status e a lista de corpos.
**Simulado no MVP:** A autenticação por matrícula é simulada: o sistema valida o formato do número, mas não consulta a base funcional da POLITEC. A assinatura digital é capturada como traço no canvas, sem certificado digital e sem validade jurídica. A integração com os laboratórios de toxicologia, genética e balística não existe: o recebimento é registrado manualmente pela ADM. A integração com o CIOP é simulada: o acionamento é digitado pelo técnico, não recebido automaticamente. Os dados são fictícios, com nomes e protocolos de exemplo.
**Critério de aceite:** O técnico consegue registrar um caso completo, da etapa 1 à 7, sem usar papel ou planilha em paralelo. O gestor da ADM consegue confirmar o recebimento de um lacre e do laudo, e o registro aparece no histórico com data, hora e usuário. Os três caminhos de desfecho funcionam sem travar: liberação a familiar, liberação sem familiar e corpo não identificado. O perfil Médico Legista não consegue editar nada nem ver as etapas 6 e 7. O painel mostra os lacres pendentes corretamente após recarregar a página.
**Dados de exemplo:** No mínimo 100 casos 
**O que já existe pronto e pode ser reaproveitado:** Planilhas com informações de casos que já passaram
**Dependências:** TI da POLITEC: hospedagem, rede, autenticação e backup. Chefia da Gerência de Necropsia: validação do processo e liberação da equipe para os testes. Gestor da ADM: definição das regras de recebimento e autorização de sepultamento. 

## 3. Usuários e papéis

**Observações sobre os papéis:** 1. O papel não é o cargo.
O papel define o que a pessoa vê e faz dentro do sistema, não a posição funcional dela. Um mesmo servidor pode ter mais de um papel atribuído, desde que a acumulação seja autorizada pela chefia. O sistema deve registrar qual papel estava ativo em cada ação, não apenas quem era o usuário.

2. O Médico Legista é o único papel com restrição de escopo por etapa.
Enquanto Técnico e Gestor ADM enxergam o caso inteiro, o Médico Legista vê apenas até a etapa 5. Essa restrição não é técnica, é de finalidade: o médico precisa dos dados clínicos e de identificação para fundamentar o laudo, mas não precisa de dados de família, funerária ou entrega administrativa. Restringir reduz exposição de informação sensível de terceiros sem prejudicar o trabalho pericial.

3. A confirmação de recebimento é exclusiva do Gestor ADM.
Nenhum outro papel pode confirmar recebimento de lacre ou de laudo. Essa exclusividade é o que dá valor probatório ao registro: se qualquer pessoa pudesse confirmar, a confirmação perderia o sentido de controle. O sistema deve registrar data, hora e usuário em cada confirmação, sem possibilidade de edição posterior.

4. A decisão de sepultamento pelo Estado exige justificativa registrada.
É a única ação do sistema que encerra um caminho sem confirmação técnica prévia. Por isso exige justificativa com mínimo de caracteres e registro do responsável. A justificativa não é formalidade: é o que permite reconstruir, meses depois, por que aquele corpo foi sepultado sem identificação ou sem familiar reclamante.

5. O Técnico não pode alterar caso concluído.
Após a entrega do laudo à ADM, o caso é encerrado e nenhum papel pode editar os dados. Correções posteriores devem ser feitas por registro de retificação, que cria uma nova entrada no histórico sem apagar a anterior. Isso preserva a integridade da cadeia de custódia.

6. Todo acesso é auditável, inclusive o de leitura.
O sistema registra não apenas as alterações, mas também as consultas. Se um Médico Legista abriu um caso, isso fica registrado com data e hora. A auditoria de leitura é o que permite responder, em caso de questionamento judicial, quem teve acesso à informação e quando.

7. Papéis ainda não previstos.
Dois papéis podem ser necessários em uma segunda fase: a Autoridade Policial, que hoje só interage por requisição em papel, e a Consulta Externa, para órgãos que precisam verificar a existência de um registro sem acessar o conteúdo. Nenhum dos dois está no escopo desta versão.

8. O que o sistema não decide.
O sistema não define causa da morte, não escolhe método de identificação, não decide se um corpo deve ser sepultado pelo Estado e não valida o mérito do laudo. Ele registra a decisão tomada por quem tem competência para tomá-la, com o rastro necessário para comprovar quem decidiu e quando.

## 4. Dados (entidades e colunas; tudo SINTÉTICO)

**O que precisa ser coletado:** -
**Quem libera o acesso:** -

### Fontes de dados do processo real


## 5. Regras de negócio (RN01, RN02...)


## 6. Telas (#/painel, #/lista...)


## 7. KPIs (nome = fórmula em uma linha)

**Período da linha de base:** Não existe medição de tempo por etapa. Precisa ser coletado: data e hora de início e fim de cada uma das sete etapas, para calcular duração e gargalo.
Não existe controle de prazo de busca de familiares. Precisa ser coletado: data de início da busca e data de resultado.
Não existe trilha de auditoria. Precisa ser coletado: usuário, data e hora de cada ação
**Campos de data e tempo que existem:** TI da POLITEC libera o acesso ao sistema e à base funcional, após aprovação da chefia da Gerência de Necropsia. A chefia define quem tem qual perfil e comunica à TI. O gestor da ADM libera o acesso às informações de custódia e autorizações.

## 8. Stack: HTML único (CSS/JS inline), dados em JSON embutido, GitHub Pages.

**Stack escolhida:** HTML único (CSS/JS inline), dados em JSON embutido, GitHub Pages
**Detalhe da stack:** -
**Hospedagem:** Período proposto: 12 meses anteriores ao início do piloto. Volume: todos os casos registrados nesse período na planilha de controle.
**Custo e licenças:** -
**Contas e domínio:** -


## 9. Restrições e LGPD

**Restrições:** -
**Dados pessoais tratados:** Do corpo: nome, filiação, nascimento, idade, sexo, documentos e características físicas. De familiares: nome, parentesco, documento, telefone e assinatura. De servidores: matrícula, nome e perfil. Dados sensíveis de saúde: agente causal, estado do corpo e achados periciais.
**Base legal:** Exercício regular de atribuição legal do órgão público, previsto na LGPD.
**Retenção:** indetermidado
**Acesso e registro:** Técnico (edita as 7 etapas), Médico Legista (leitura até a etapa 5) e Gestor ADM (confirma recebimentos e autoriza sepultamento). Todo acesso é auditado, inclusive leitura, com data, hora, matrícula, perfil, ação e protocolo. O histórico não permite edição nem exclusão.
**Requisitos marcados:** -

---

# Anexo A — AS-IS (o fluxo de hoje)

**Início:** No acionamento da ocorrência
**Fim:**  custódia do laudo - entrega do laudo
**Entradas:** •Comunicação do CIOP - Dados da ocorrência: local, delegacia e autoridade policial
• Corpo da vítima - Removido do local, com ou sem documentos comprobatórios
• Documentos encontrados - RG, CNH e outros pertences localizados junto ao corpo
• Informações de possíveis familiares - Contatos ou dados preliminares, quando disponíveis
• Requisição de necropsia - Documento formal expedido pela autoridade policial
•Materiais biológicos e vestígios - Elementos a serem coletados durante o procedimento pericial
**Saídas:** Laudo necroscópico

Documento pericial conclusivo assinado pelo médico legista

•Destinação do corpo - Liberado à família ou sepultado pelo Estado
• Materiais encaminhados - Amostras enviadas a toxicologia, genética ou balística
•Termo de liberação - Documento comprobatório assinado pelo familiar
• Auto de Entrega - Comprovante assinado pelo responsável da funerária
• Autorização de sepultamento - Expedida nos casos de sepultamento pelo Estado
•Protocolo de entrega à ADM - Comprovante de entrega física do laudo assinado em papel
**Volume:** variavel
**Duração:** -
**Frequência:** Diário
**Decisões e aprovações:** •Requisição de necropsia - Autoridade policial decide formalmente pelo exame
•Método de identificação - Médico legista define a técnica aplicável ao caso
•Causa da morte e laudo - Médico legista define a conclusão técnica pericial
•Liberação do corpo à família - Gestor da ADM valida documentação e autoriza entrega
•Sepultamento pelo Estado - Gestor da ADM autoriza quando não há familiar reclamante
•Recebimento do laudo - Gestor da ADM confere fisicamente e chancela a entrega
**Exceções:** •Corpo sem identificação - A necropapiloscopia não retorna e o caso segue para DNA ou odontologia legal, podendo levar semanas.
•Corpo não reclamado - Após prazo de busca de familiares sem êxito, o corpo é sepultado pelo Estado com autorização administrativa.
•Corpo não identificado - Quando os métodos de identificação se esgotam, o sepultamento pelo Estado ocorre sem confirmação de identidade.
•Familiar localizado após sepultamento - O corpo já foi sepultado e o registro precisa ser recuperado manualmente em arquivos físicos.
•Material sem recebimento confirmado - O lacre saiu da necropsia mas não há comprovação formal de quem recebeu no laboratório de destino.
•Laudo não entregue - O caso fica aberto sem que ninguém perceba, até que alguma autoridade ou familiar venha procurar.
**Já digitalizado:** A digitalização é parcial e fragmentada. Existe uma planilha eletrônica que concentra o cadastro dos corpos, com abas para histórico de status e materiais coletados. Essa planilha é o único registro digital consolidado.
Todo o resto permanece em papel: formulário de necropsia, laudo de identificação, termo de liberação familiar, Auto de Entrega da funerária, autorização de sepultamento e protocolo de entrega do laudo à ADM.

# Anexo B — TO-BE (o fluxo depois da mudança)

**Visão do futuro:** Quando este processo existir, a Gerência de Necropsia deixa de depender de planilhas, papel e livros de protocolo para saber onde está cada corpo e cada lacre, e passa a ter rastreabilidade completa em um único sistema, com cada etapa registrada, cada recebimento confirmado e cada pendência visível antes de virar problema.
**Mudança principal:** A mudança principal é a unificação do registro em um único sistema com trilha de auditoria. Hoje cada etapa tem seu próprio registro — planilha, formulário de papel, livro de protocolo — e nenhum conversa com o outro. Isso resolve o problema central: a informação deixa de precisar ser procurada e passa a estar onde é necessária.
**O que fica igual:** O processo operacional. O técnico continua recebendo o acionamento, indo ao local e lacrando materiais. O médico legista continua fazendo a necropsia e definindo a causa da morte. A identificação continua pelos mesmos métodos. A liberação continua exigindo termo assinado. As sete etapas permanecem as mesmas, na mesma ordem
**O que não pode mudar:** A cadeia de custódia: nenhuma automação substitui a confirmação humana de recebimento.
A competência legal: o médico define causa da morte e identificação; o gestor autoriza liberação e sepultamento.
A assinatura presencial: o termo de liberação e o protocolo do laudo são atos de responsabilidade.
O sigilo: dados de necropsia são sensíveis e o acesso precisa ser restrito e auditado.
A autorização para sepultamento pelo Estado: exige registro com justificativa.
**Piloto do TO-BE:** Três frentes. Fluxo completo: refazer um caso real já encerrado no sistema, da etapa 1 à 7, comparando com o registro em papel. Caminhos alternativos: simular liberação a familiar, liberação sem familiar e corpo não identificado, garantindo que os três cheguem ao fim sem travar. Permissões: entrar com cada perfil e verificar o que cada um enxerga e faz.

O teste deve ser feito com quem executa o processo, não só com quem desenvolveu. Sugestão: primeiro rodar com os dados de exemplo do protótipo, depois um caso real em paralelo ao processo atual, sem substituí-lo.

# Anexo C — Pesquisa, riscos e plano

**Hipótese de campo:** -
**Lacunas:** -
**Apoio necessário:** -
**Aprendizado necessário:** -

# Anexo D — A defesa

**Frase de defesa:** -
**Provas:** -
**Piloto:** Se eu conseguir ter os dados sem precisar de papeis
**Maior risco:** -

# Anexo E — Documentos enviados

**Descrição dos documentos:** -
**O que ainda falta:** -
