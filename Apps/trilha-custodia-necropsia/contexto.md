# Sistema de Controle de Necropsia · contexto e arquitetura

> Aluna: Silmara Bueno (IML · Gerência de Necropsia — DMML)
> Fonte: `PROJETO.md`, os dois envios parciais, o protótipo `prototipo/tci.html`
> e o protótipo "Sistema de Controle de Necropsia — DMML _ POLITEC.html"
> (em `Ncropsia/`, na raiz do repositório), que o app espelha desde o Sprint 10.

---

## 1. O problema

O registro de cada corpo é feito em paralelo por vários setores e em suportes
diferentes: protocolo no Atena, livro de necropsia, livro de câmara fria, livro
de PAF e controle de tornozeleira. Os marcos do deslocamento são avisados de
forma verbal e se perdem na passagem de plantão. A identificação é buscada
manualmente, um registro por vez. Corpos não identificados e não reclamados não
têm controle centralizado, e a família e a autoridade policial sabem da
identificação dias depois.

| Dado do relato | Valor |
|---|---|
| Registros paralelos por corpo | 4 livros + Atena |
| Marcos do deslocamento | saída da base, chegada ao local, saída do local, retorno ao IML |
| Identificação | manual, por consulta aos registros |
| Medição atual | nenhuma |

## 2. As sete etapas do caso

O espelho do protótipo organiza o caso em sete etapas, na mesma ordem do
fluxograma revisado pela aluna (`entregas/2026-11-05/`):

| Etapa | Nome | O que registra |
|---|---|---|
| 1 | Acionamento | horário e número da necropsia |
| 2 | Ocorrência e possível vítima | delegacia, autoridade, local, dados da possível vítima, fotos e marcos do deslocamento |
| 3 | Aguardando necropsia | câmara fria, gaveta, estado do corpo e lacre do corpo |
| 4 | Necropsia em andamento | equipe (médico, técnico, odonto), horários e os quatro materiais lacrados |
| 5 | Identificação | resultado, método, nome confirmado, busca de familiares e exame complementar |
| 6 | Família e liberação | termo de liberação com assinatura ou sepultamento pelo Estado |
| 7 | Entrega de laudo para ADM | quem entrega, quem recebe, assinatura e confirmação da ADM |

Entre a 6 e a 7 entra o bloco da **funerária** (destino, Auto de Entrega,
autorização e local), e depois o **encerramento** (destino do corpo, laudo
recebido e lacres recebidos).

## 3. O que o MVP faz e o que não faz

| Faz | Não faz |
|---|---|
| Registra o acionamento com protocolo único (RN01) | Integra com o Atena |
| Registra os quatro marcos com perfil, data e hora (RN03) | Substitui os livros oficiais |
| Registra os quatro materiais da necropsia e o recebimento pela ADM | Guarda dado pessoal real |
| Controla a situação do corpo em todas as etapas | Decide a identificação |
| Busca por protocolo, nome, documento, delegacia ou lacre (RN04) | Libera o corpo sem autorização |
| Mostra a trilha de auditoria, inclusive a consulta (RN03) | Emite o auto de entrega oficial |

## 4. Regras

- **RN01**: o protocolo é único e gerado no acionamento.
- **RN02**: a liberação exige identificação registrada, assinatura do familiar e
  documento.
- **RN03**: todo marco, lacre e mudança registra perfil, data e hora; a
  consulta ao caso também é auditada.
- **RN04**: a busca aceita protocolo, nome, documento, delegacia ou lacre.
- **RN05**: a lista e o painel não mostram nome completo; a ficha mostra.
- **RN09**: o sepultamento pelo Estado é decisão do Gestor ADM, com
  justificativa, autorização e Auto de Entrega da funerária.
- **RN10**: a custódia só se encerra com o destino do corpo, o laudo recebido
  pela ADM e todos os lacres recebidos.
- **RN11**: os métodos de identificação só se esgotam depois de pelo menos um
  exame complementar (DNA, odontologia legal ou antropologia forense).
- **RN12**: depois do encerramento (ou do sepultamento) o caso não se edita; a
  correção entra como retificação, com tipo, o que muda e motivo.

## 5. Telas

| Rota | Perfil | O que faz |
|---|---|---|
| `#/painel` | todos | Dez indicadores do protótipo; por perfil, o quadro das sete etapas, a sala de necropsia ou a fila da ADM |
| `#/corpos` | todos | Lista com busca, filtros e gaveta lateral |
| `#/corpo/novo` | técnico e gestor | Acionamento e ocorrência (etapas 1 e 2) |
| `#/corpo/:id` | todos | Ficha do caso com as sete etapas, a funerária, o encerramento, as retificações e o histórico |
| `#/busca` | todos | Busca por protocolo, nome, documento, delegacia ou lacre |
| `#/resumo` | todos | Resumo por agente causal |
| `#/config` | todos | Perfil da cópia, backup e dados fictícios |

## 6. Modelo de dados (IndexedDB `trilha_custodia_v1`)

| Store | Campos |
|---|---|
| `corpos` | id_corpo, protocolo, numero_necropsia, acionamento{horario,numero}, ocorrencia{chegada,delegacia,autoridade,endereco,municipio,uf,possivel_nome,filiacao,nascimento,idade,sexo,fonte,documento,telefone,observacoes,fotos_doc,fotos_cena}, camara, gaveta, estado_corpo, lacre_corpo, confirmado_entrada, necropsia{medico,tecnico,odonto,inicio,termino}, identificacao{resultado,metodo,nome_confirmado,responsavel,data_confirmacao,busca,autorizacao,tentativas,pendente}, familia{tipo,nome,parentesco,documento,telefone,data_liberacao,assinatura,busca,autorizacao}, funeraria{destino,nome,auto,data_entrega,hora_entrega,autorizacao,data_autorizacao,local}, laudo{entregue_por,entregue_em,recebido_por,recebido_em,assinatura_recebimento,confirmado_perfil}, sepultamento{justificativa,autorizacao,autorizado_em,perfil}, destino_final, custodia_finalizada, retificacoes |
| `marcos` | id_marco, corpo_id, tipo, data_hora, perfil, observacao |
| `lacres` | id_lacre, corpo_id, tipo (sangue, bio, projetil, pertences), nome, coletado, codigo, destino, data_hora, perfil, recebido_em, recebido_por |
| `log` | id, corpo_id, acao, perfil, data_hora |

A situação mostrada na tela (`Ocorrência em andamento`, `Aguardando necropsia`,
`Necropsia em andamento`, `Aguardando identificação`, `Aguardando família`,
`Sepultado pelo Estado`, `Entrega de laudo para ADM`, `Custódia finalizada`, ...)
é calculada a partir da etapa e dos campos do caso, e não gravada: assim ela
nunca diverge do conteúdo do registro.

## 7. LGPD e cadeia de custódia

O app usa nomes, documentos e protocolos fictícios. Na versão institucional, os
dados do corpo e da vítima são sensíveis: exigem autenticação individual,
controle de acesso por perfil, criptografia, trilha append-only e observância
dos artigos 158-A a 158-F do Código de Processo Penal e da LGPD.
