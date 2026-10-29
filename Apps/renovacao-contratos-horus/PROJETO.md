# PROJETO.md — Fluxo de Renovação de Contratos- apoiado pelo HORUS

**Aluno ou equipe:** Rodrigo Neves Ribeiro
**Unidade:** coordenadoria de aquisições e contratos
**Contato:** rodrigoribeiro@politec.mt.gov.br
**Projeto:** Fluxo de Renovação de Contratos- apoiado pelo HORUS
**Tipo de projeto:** Mapeamento de processo (fluxo, BPMN ou Mermaid)
**Data:** 2026-10-29
**Resumo:** Módulo de gestão, acompanhamento e controle de contratos do Hórus que centraliza a renovação, desde o monitoramento do vencimento até a atualização da vigência e o registro em trilha de auditoria.

## 1. Problema (a dor)

**Problema:** O fluxo não apresenta dificuldade de acompanhamento dos fiscais de contrato devido as atividades que cada fiscal exerce durante as rotinas diarias, muitas vezes esquecendo dos deveres de fiscalização de contrato, necessitando de ferramento de aviso aos fiscais e gestores.
**Impacto:** todo o valor gasto na instrução processual, empenho do contrato, e horas trabalhadas do servidor, nao se concretiza com a chegada dos materia
**Quem sofre:** Equipe interna, Unidade parceira, Servidor da unidade, Chefia
**Como é feito hoje:** O fiscal recebe um e-mail inicial, e depois fica responsável pela fiscalização dos itens, o fiscal não requisita o item e o contrato pode vencer sem execução no periodo vigente do contrato; confirmar contrato Vigente e permissão de prorrogação; avaliar vantajosidade e enquadramento legal; instruir e anexar documentos; registrar termo aditivo; registrar reajuste/repactuação/reequilíbrio, se houver; após publicação, atualizar a vigência do contrato e manter o status Vigente; recalcular alertas e registrar em auditoria.
**Evidências:** -
**Detalhe da evidência:** Fonte única: Fluxo de Renovação de Contratos — Sistema Hórus (PlaniTec), versão 1.0, de 29/10/2026. Documento de uso interno, elaborado a partir do comportamento real do módulo de Gestão de Contratos.
**O que não pode ser automatizado:** O fluxo prevê avaliação de vantajosidade e enquadramento legal, decisão pela renovação e formalização por termo aditivo assinado e publicado. Não atribui essas decisões ao sistema; as automações descritas são cálculo de término, semáforo, alertas e trilha de auditoria.

## 2. Objetivo do MVP (o que faz e o que NÃO faz)

**Objetivo do MVP:** Não informado no fluxo anexado.
**O que o MVP não faz:** O fluxo não define MVP nem recorte de funcionalidades.
**Entregável do projeto:** Fluxo documentado de renovação de contratos no módulo de Gestão, Acompanhamento e Controle de Contratos do Hórus (PlaniTec). O documento não define um novo entregável ou MVP.
**Dentro do escopo:** Monitoramento de vencimento; decisão e instrução da renovação; documentos; termo aditivo de prorrogação; reajuste/repactuação/reequilíbrio quando aplicável; atualização da vigência; semáforo, alertas, auditoria e caminhos alternativos de não renovação.
**Fora do escopo:** O documento delimita a descrição à renovação de contratos; não especifica exclusões de um projeto ou MVP.
**Plataforma alvo:** -
**Primeira tela:** Painel de Contratos: indicador Vencendo (90d) e lista Próximos do vencimento.
**Simulado no MVP:** Não informado no fluxo anexado.
**Critério de aceite:** Critério de aceite de MVP não informado. Resultado final descrito no fluxo: aditivo publicado, vigência atualizada, status Vigente, semáforo recalculado, documentos anexados e trilha de auditoria.
**Dados de exemplo:** O documento não fornece registros de contratos nem conjunto de dados de exemplo.
**O que já existe pronto e pode ser reaproveitado:** O documento descreve o módulo existente do Hórus (PlaniTec), com painel de Contratos, Documentos, Termos aditivos / apostilamentos, Reajustes / repactuações / reequilíbrio e auditoria.
**Dependências:** O fluxo identifica perfis de gestão e responsáveis designados pela fiscalização. Não informa dependências de implantação de projeto.

## 3. Usuários e papéis

| Papel | Quem é | O que enxerga | O que faz | O que não pode fazer | Registro |
|---|---|---|---|---|---|
| Perfis de gestão | Administrador, Diretor, Coordenador e Gerente | Módulo de gestão de contratos; recorte por perfil não detalhado | Gestão de contratos, incluindo renovação | Restrições específicas por perfil não detalhadas | Criação de aditivos e mudanças de situação/vigência em auditoria |
| Autor do registro | Usuário autor do registro | Visibilidade não detalhada no fluxo | Escrita permitida no próprio registro | Escrita em registros de terceiros não é autorizada por essa regra | Trilha de auditoria do módulo |
| Responsáveis pela fiscalização | Gestor, fiscais titular/substituto, técnico/administrativo e preposto da contratada | Documentos anexados para consulta e fiscalização; visibilidade por papel não detalhada | Fiscalização pelos responsáveis designados | Permissão de escrita não é concedida apenas pela designação de fiscal no texto | Histórico de substituições |

**Observações sobre os papéis:** Gestão de contratos disponível a Administrador, Diretor, Coordenador e Gerente. Escrita permitida ao autor do registro e às chefias. Fiscalização pelos responsáveis designados: gestor, fiscais titular/substituto, técnico/administrativo e preposto da contratada, com histórico de substituições. O documento não detalha a visibilidade individual de cada perfil.

## 4. Dados (entidades e colunas; tudo SINTÉTICO)

| Entidade | O que representa | Colunas | Chave | Volume | Origem | Sintético |
|---|---|---|---|---|---|---|
| Contrato | Contrato administrativo | data_inicio; vigencia_meses; data_fim; permite_prorrogacao; alerta_dias; status. Tipos técnicos não especificados. | Não informado no fluxo anexado. | Não informado no fluxo anexado. | Cadastro de contratos do Hórus |  |
| Termo aditivo | Alteração contratual de prorrogação | Tipo; assinatura; nova vigência (fim); fundamento legal; número do aditivo; descrição; status. Tipos técnicos não especificados. | Não informado no fluxo anexado. | Não informado no fluxo anexado. | Termos aditivos / apostilamentos |  |
| Alteração financeira | Reajuste, repactuação, reequilíbrio, revisão ou atualização | Tipo; índice; percentual; data de aplicação; valor anterior; novo valor; memória de cálculo; status. Tipos técnicos não especificados. | Não informado no fluxo anexado. | Não informado no fluxo anexado. | Reajustes / repactuações / reequilíbrio |  |

**O que precisa ser coletado:** O documento não apresenta levantamento de dados faltantes ou plano de coleta.
**Quem libera o acesso:** O documento informa permissões dos perfis, mas não identifica quem libera acesso nem prazo.

### Fontes de dados do processo real


## 5. Regras de negócio (RN01, RN02...)

| ID | Regra | Quando se aplica | Exceção | Quem valida | Tipo |
|---|---|---|---|---|---|
| R1 | Renovação aplicável apenas a contratos com vigência ativa; confirmar permite_prorrogacao | Avaliação da renovação | Sem permissão: avaliar nova contratação | Não informado no fluxo anexado. | Negócio |
| R2 | data_fim calculada por data_inicio + vigencia_meses; admite ajuste manual | Cadastro e atualização de vigência | Ajuste manual previsto | Não informado no fluxo anexado. | Cálculo |
| R3 | Semáforo: >120 normal; 91–120 acompanhamento; 61–90 atenção; 31–60 providências; 0–30 urgente; vencido ação imediata | Monitoramento diário | Encerrado, Rescindido e Expirado saem da contagem regressiva | Sistema Hórus | Cálculo |
| R4 | Após publicação do aditivo, editar a vigência e manter Vigente | Prorrogação formalizada | Aditivo e atualização do contrato são etapas distintas | Não informado no fluxo anexado. | Negócio |
| R5 | Escrita permitida ao autor e às chefias; gestão para Administrador, Diretor, Coordenador e Gerente | Gestão e alteração de registros | Não informado no fluxo anexado. | Não informado no fluxo anexado. | Acesso |
| R6 | Auditoria append-only da criação do aditivo e mudanças de situação/vigência | Registro e alteração contratual | Não informado no fluxo anexado. | Sistema Hórus | Negócio |


## 6. Telas (#/painel, #/lista...)

| Rota | Tela | Objetivo | Quem usa | Dados | Ação | Regra | Tipo | Verificável como | MVP |
|---|---|---|---|---|---|---|---|---|---|
|  | Painel de Contratos | Monitorar vencimento | Perfis de gestão | Indicador Vencendo (90d), próximos do vencimento e semáforo | Consultar lista e filtrar faixas | Seis faixas; recálculo diário; alerta padrão 90 dias | Tela | Conferir faixa conforme dias restantes; resultado descrito no fluxo |  |
|  | Documentos | Reunir documentação do processo | Perfis autorizados do módulo | Documentos anexados ao contrato | Anexar documentação como Termo aditivo | Repositório privado | Tela | Consultar documento anexado ao contrato |  |
|  | Termos aditivos / apostilamentos | Registrar prorrogação | Autor do registro e chefias | Tipo, assinatura, nova vigência, fundamento, número, descrição e status | Registrar e tramitar aditivo | Rascunho → Em tramitação → Assinado → Publicado; ou Cancelado | Tela | Conferir registro do aditivo e situação |  |
|  | Reajustes / repactuações / reequilíbrio | Registrar alteração financeira quando aplicável | Autor do registro e chefias | Tipo, índice, percentual, data, valores e memória de cálculo | Registrar alteração financeira | Solicitado → Em análise → Aprovado → Aplicado; ou Indeferido | Tela | Conferir campos e situação do registro |  |
|  | Edição da vigência | Refletir a nova vigência no contrato | Autor do registro e chefias | Data de término ou meses de vigência; status | Atualizar término após publicação do aditivo | Manter Vigente; edição distinta do registro do aditivo | Ação | Conferir nova data e semáforo recalculado |  |
|  | Trilha de auditoria | Registrar alterações do contrato | Sistema Hórus | Criação do aditivo e mudanças de situação/vigência | Registrar eventos | Append-only | Automação | Conferir eventos registrados; procedimento de teste não especificado |  |


## 7. KPIs (nome = fórmula em uma linha)

| KPI | Pergunta | Fórmula | Fonte | Linha de base | Valor esperado | Como medir |
|---|---|---|---|---|---|---|
| Dias restantes até o fim da vigência | Em qual faixa do semáforo está o contrato? | Quantidade de dias restantes até data_fim | Contrato: data_fim; semáforo do Hórus | Não informada no fluxo | Não informado; o documento não fixa meta de melhoria | Plano de medição não informado no fluxo |
| Vencendo (90d) | Quais contratos estão próximos do vencimento em até 90 dias? | Indicador do painel relativo aos contratos próximos do vencimento (até 90 dias) | Painel de Contratos do Hórus | Não informada no fluxo | Não informado; 90 dias é janela de alerta, não meta de melhoria | Plano de medição não informado no fluxo |

**Período da linha de base:** Não há período, volume ou valores de linha de base no fluxo anexado.
**Campos de data e tempo que existem:** Contrato: data_inicio, vigencia_meses, data_fim e alerta_dias (padrão 90). Aditivo: data de assinatura e nova vigência (fim). Alteração financeira: data de aplicação. O documento não especifica horários ou datas de entrada/saída por etapa.

## 8. Stack: HTML único (CSS/JS inline), dados em JSON embutido, GitHub Pages.

**Stack escolhida:** HTML único (CSS/JS inline), dados em JSON embutido, GitHub Pages
**Detalhe da stack:** Tecnologias, linguagem, framework e infraestrutura não informados no fluxo.
**Hospedagem:** Hospedagem não informada no fluxo anexado.
**Custo e licenças:** Não informado no fluxo anexado.
**Contas e domínio:** Não informado no fluxo anexado.


## 9. Restrições e LGPD

**Restrições:** Renovação apenas para contrato em vigência ativa, com permissão de prorrogação. Aditivo e atualização da vigência são registros distintos. Documentos em repositório privado; escrita restrita ao autor e chefias; auditoria append-only. O documento cita os arts. 105, 107 e 125 da Lei nº 14.133/2021 e diferencia prorrogação pura de prazo de acréscimo de valor.
**Dados pessoais tratados:** O fluxo identifica papéis de responsáveis e preposto, mas não especifica dados pessoais ou tratamento em MVP.
**Base legal:** Base legal de tratamento de dados pessoais não informada no fluxo.
**Retenção:** Não informado no fluxo anexado.
**Acesso e registro:** Gestão: Administrador, Diretor, Coordenador e Gerente. Escrita: autor do registro e chefias. Documentos em repositório privado. Trilha append-only registra criação do aditivo e mudanças de situação/vigência.
**Requisitos marcados:** Segurança e controle de acesso, Trilha de auditoria

---

# Anexo A — AS-IS (o fluxo de hoje)

**Início:** Identificação de contrato vigente próximo do vencimento no painel (até 90 dias) ou pelo filtro do semáforo.
**Fim:** Vigência atualizada após publicação do aditivo, status Vigente mantido, semáforo recalculado, documentos anexados e alterações registradas na trilha de auditoria.
**Entradas:** Contrato com data_inicio, vigencia_meses, data_fim, permite_prorrogacao, alerta_dias e status; avaliação de vantajosidade e enquadramento legal; documentos do processo; termo aditivo; dados de reajuste, repactuação ou reequilíbrio quando aplicável.
**Saídas:** Termo aditivo de prorrogação registrado e publicado; nova vigência no contrato; semáforo e alertas atualizados; documentos para consulta e fiscalização; trilha de auditoria. Quando aplicável, registro da alteração financeira.
**Volume:** Não informado no fluxo anexado.
**Duração:** Não informado no fluxo anexado.
**Frequência:** -
| Etapa | Quem faz | O que entra | Ação | O que sai | Sistema | Regra | Onde espera | Tempo (h) | Automatizável |
|---|---|---|---|---|---|---|---|---|---|
| Monitoramento e gatilho | Administrador, Diretor, Coordenador ou Gerente; escrita pelo autor e chefias | Contrato vigente e datas de vigência | Consultar Próximos do vencimento ou filtrar semáforo | Contrato identificado para avaliação | Hórus — painel de Contratos | Até 90 dias; confirmar Vigente e permite_prorrogacao | Não informado no fluxo anexado. | Não informado no fluxo anexado. |  |
| Decisão e instrução | Administrador, Diretor, Coordenador ou Gerente; escrita pelo autor e chefias | Contrato elegível e condições/preços de mercado | Avaliar vantajosidade e enquadramento legal; reunir e anexar documentos | Documentação anexada ao contrato | Hórus — Documentos, repositório privado | Decidir pela prorrogação ou avaliar nova contratação | Não informado no fluxo anexado. | Não informado no fluxo anexado. |  |
| Registro do termo aditivo | Administrador, Diretor, Coordenador ou Gerente; escrita pelo autor e chefias | Documentação e dados da prorrogação | Registrar tipo, assinatura, nova vigência, fundamento, número, descrição e status | Aditivo registrado e tramitado até publicação | Hórus — Termos aditivos / apostilamentos | Rascunho → Em tramitação → Assinado → Publicado; ou Cancelado | Não informado no fluxo anexado. | Não informado no fluxo anexado. |  |
| Alteração financeira, quando aplicável | Administrador, Diretor, Coordenador ou Gerente; escrita pelo autor e chefias | Índice, percentual, data, valores e memória de cálculo | Registrar reajuste, repactuação, reequilíbrio, revisão ou atualização monetária | Alteração financeira registrada | Hórus — Reajustes / repactuações / reequilíbrio | Solicitado → Em análise → Aprovado → Aplicado; ou Indeferido | Não informado no fluxo anexado. | Não informado no fluxo anexado. |  |
| Atualização da vigência | Administrador, Diretor, Coordenador ou Gerente; escrita pelo autor e chefias | Aditivo publicado com nova data de término | Editar data de término ou meses de vigência | Contrato com nova vigência e status Vigente | Hórus — edição do contrato | Registro do aditivo e edição da vigência são etapas distintas | Após publicação do aditivo; espera não medida | Não informado no fluxo anexado. |  |
| Efeitos e encerramento do fluxo | Sistema Hórus | Nova vigência e registros de alterações | Recalcular semáforo e registrar criação do aditivo e mudanças em auditoria | Alertas recalculados; documentos disponíveis; trilha de auditoria | Hórus — semáforo, alertas e auditoria | Auditoria append-only; faixa recalculada diariamente | Não informado no fluxo anexado. | Não informado no fluxo anexado. | Sim, com regra clara |

**Decisões e aprovações:** Contrato deve estar Vigente e permitir prorrogação; caso contrário, avaliar nova contratação. Avaliar vantajosidade e enquadramento legal. Aditivo: Rascunho → Em tramitação → Assinado → Publicado, ou Cancelado. Alteração financeira, se houver: Solicitado → Em análise → Aprovado → Aplicado, ou Indeferido. Atualizar a vigência após publicação do aditivo.
**Exceções:** Sem interesse/vantajosidade: deixar expirar (Expirado) ou encerrar formalmente (Encerrado). Extinção antecipada: registrar aditivo tipo Rescisão e alterar para Rescindido. Nova contratação: encerrar o contrato atual e iniciar novo instrumento. Contratos encerrados, rescindidos ou expirados saem da contagem regressiva.
**Já digitalizado:** Painel de Contratos, semáforo e alertas; cadastro e edição de vigência; aba Documentos em repositório privado; Termos aditivos / apostilamentos; Reajustes / repactuações / reequilíbrio; trilha de auditoria append-only.

# Anexo B — TO-BE (o fluxo depois da mudança)

**Visão do futuro:** O documento descreve o funcionamento atual do Hórus; não apresenta processo futuro distinto.
**Mudança principal:** Não há mudança proposta no fluxo anexado.
**O que fica igual:** O fluxo documentado é: monitorar, decidir, instruir, registrar aditivo, registrar alteração financeira se houver, atualizar vigência e registrar auditoria.
**O que não pode mudar:** Conforme o documento: observar os fundamentos legais indicados (Lei nº 14.133/2021, arts. 105, 107 e 125), formalização por termo aditivo e permissões de acesso. Registro do aditivo e atualização da vigência são etapas distintas.
**Piloto do TO-BE:** Não informado no fluxo anexado.

# Anexo C — Pesquisa, riscos e plano

**Hipótese de campo:** O fluxo não formula hipótese de campo.
| Referência | Tipo | Fonte ou link | Ano | Dado que extrai | Como usar na defesa | Link conferido |
|---|---|---|---|---|---|---|
| Fluxo de Renovação de Contratos — Hórus (PlaniTec), versão 1.0 | Documento interno | Fluxo-Renovacao-Contratos-Horus(1).docx | 2026 | Etapas, dados, status, semáforo, papéis e auditoria | Sustentar a descrição do funcionamento documentado | Não se aplica |
| Lei nº 14.133/2021, arts. 105, 107 e 125, citados no fluxo | Norma ou lei | Referência presente no documento anexado; link não fornecido | 2021 | Fundamentos de duração/prorrogação e limites de acréscimos/supressões, conforme o fluxo | Identificar os fundamentos indicados pelo documento, sem validação jurídica externa | Não |

**Lacunas:** Fonte limitada ao fluxo anexado. Não há diagnóstico anterior ao Hórus, tempos de etapas, filas medidas, volumes, linha de base, meta de melhoria, TO-BE distinto, definição de MVP, infraestrutura, custos ou cronograma de projeto. As referências legais são as citadas no documento; não houve pesquisa externa.
**Apoio necessário:** Não informado no fluxo anexado.
**Aprendizado necessário:** Não informado no fluxo anexado.

# Anexo D — A defesa

**Frase de defesa:** O Hórus centraliza o acompanhamento da renovação contratual, do alerta de vencimento ao registro do termo aditivo, à atualização da vigência e à trilha de auditoria. O fluxo não fornece base e meta para uma defesa quantitativa.
**Provas:** 1. Semáforo com seis faixas e alerta padrão de 90 dias.
**Piloto:** Plano de teste ou piloto não informado no fluxo.
**Maior risco:** O documento não hierarquiza riscos de uma proposta. Para contratos vencidos, indica ação imediata/análise jurídica; para a faixa de 0–30 dias, recomenda assinar/publicar antes do vencimento.

# Anexo E — Documentos enviados

**Descrição dos documentos:** Fluxo-Renovacao-Contratos-Horus(1).docx: documento de uso interno que descreve o fluxo de renovação de contratos do Hórus (PlaniTec), versão 1.0, 29/10/2026. Referência usada no preenchimento; arquivo não anexado ao formulário.
**O que ainda falta:** O fluxo não define os insumos necessários para um MVP.
