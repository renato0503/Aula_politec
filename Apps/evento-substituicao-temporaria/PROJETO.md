# PROJETO · Evento de Substituição Temporária

> Especificação completada a partir do documento da Simone Alem
> (`entregas/Evento de Substituição Temporária.docx`, 09/11/2026). O texto
> original está em `envio-original.json`.

---

## 1. Identificação

| Campo | Valor |
|---|---|
| Nome do projeto | Evento de Substituição Temporária |
| Responsável | Simone Alem |
| Unidade | Gerência de Suporte à Gestão de Pessoas |
| Tipo | Aplicativo para servidor |
| Data | 09/11/2026 |
| Stack | HTML único, offline first, IndexedDB, backup `.json` |
| Piloto | 30 dias na Gerência de Suporte à Gestão de Pessoas |

---

## 2. Problema e objetivo

### 2.1 Problema

O afastamento temporário de um gestor passa por sete etapas e por quatro
unidades diferentes. O processo vive no SIGADOC e o controle paralelo vive em
uma planilha de Excel. A planilha não avisa o prazo, não mostra em que etapa o
evento está e não guarda a trilha das autorizações. O prazo do dia 05 é
conferido manualmente e, quando passa, o processo é indeferido.

### 2.2 Objetivo do MVP

Validar uma fila única por perfil, com a etapa, o responsável e o prazo do dia
05 no mesmo lugar, a ficha de RH padronizada e o encerramento amarrado à
publicação no Diário Oficial.

### 2.3 O que o MVP faz e o que não faz

| Faz | Não faz |
|---|---|
| Registra o ofício com o substituto, o motivo e o período (RN01, RN02) | Integra com o SIGADOC |
| Cria uma autorização por nível da linha hierárquica (RN03) | Assina digitalmente |
| Encaminha ao Gabinete e ao RH | Envia e-mail |
| Inclui a ficha de solicitação (RN04) | Publica no Diário Oficial |
| Mostra a fila de assinatura do Diretor Geral Adjunto (RN05) | Decide o mérito |
| Bloqueia o envio à SESP depois do dia 05 (RN06) | Substitui o processo oficial |
| Encerra só com a publicação no DO (RN07) | Guarda documentos reais |
| Mantém a planilha de controle e exporta CSV e Excel (`.xlsx`) (RN08) | — |
| Deixa a unidade ajustar e reenviar o evento devolvido | — |

---

## 3. Papéis e permissões

| Papel | Quem é | O que vê | O que faz | O que não faz |
|---|---|---|---|---|
| Unidade solicitante | Servidor da unidade do gestor afastado | Os eventos da unidade e os devolvidos | Abre o ofício, indica o substituto e o motivo, reenvia depois do ajuste | Autoriza, assina ou publica |
| Gestor hierárquico | Chefias da linha hierárquica | A fila de autorização | Autoriza ou devolve o evento | Inclui a ficha ou assina |
| Gabinete de Direção | Servidor do Gabinete | Os eventos autorizados | Encaminha o evento ao RH | Autoriza, assina ou publica |
| Gerência de Suporte à Gestão de Pessoas | Analista de RH | Análise, envio à SESP e publicação | Inclui a ficha, envia à SESP, registra a publicação e mantém a planilha | Autoriza ou assina |
| Diretor Geral Adjunto | Diretor Geral Adjunto | A fila de assinatura | Assina o evento | Abre o ofício, inclui a ficha ou publica |

> O perfil no MVP é uma **lente de demonstração**, não é controle de acesso. Na
> versão institucional, cada papel precisa de login e de trilha inalterável.

---

## 4. Fluxo AS-IS

| # | Etapa | Quem faz | Entra | Ação | Sai | Sistema | Regra | Onde espera | Tempo | Automatizável |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | Abertura do ofício | Unidade do gestor afastado | Demanda de afastamento | Abre o processo no SIGADOC por ofício, indica o substituto e o motivo | Processo autuado | SIGADOC | RN01 e RN02 | Fila da unidade | 1 dia | Parcial |
| 2 | Autorização hierárquica | Chefias da linha | Processo com o ofício | Cada gestor responsável analisa e autoriza | Autorizações registradas | SIGADOC | RN03 | Agenda de cada chefia | 3 a 10 dias | Sim |
| 3 | Envio ao Gabinete | Unidade | Processo autorizado | Encaminha o processo ao Gabinete de Direção | Processo no Gabinete | SIGADOC | RN03 | Fila do Gabinete | 1 dia | Sim |
| 4 | Análise de RH | Gerência de Suporte à Gestão de Pessoas | Processo no Gabinete | Analisa a demanda e inclui a ficha de solicitação | Ficha anexada | SIGADOC e Word | RN04 | Fila do RH | 2 a 5 dias | Parcial |
| 5 | Assinatura | Diretor Geral Adjunto | Processo com a ficha | Analisa e assina | Processo assinado | SIGADOC | RN05 | Agenda do diretor | 1 a 7 dias | Não |
| 6 | Envio à SESP | Gerência de Suporte à Gestão de Pessoas | Processo assinado | Encaminha à Superintendência de Gestão de Pessoas da SESP | Processo na SESP | SIGADOC | RN06 | Conferência do prazo | 1 dia | Sim |
| 7 | Acompanhamento na planilha | Gerência de Suporte à Gestão de Pessoas | Dados do processo | Registra os dados e acompanha o andamento | Planilha de controle | Excel | RN08 | Conferência manual | Contínuo | Sim |
| 8 | Publicação no Diário Oficial | SESP e Diário Oficial | Processo na SESP | Publica a substituição e informa o número da publicação | Evento encerrado | DO e Excel | RN07 | Fila do Diário Oficial | 5 a 30 dias | Parcial |

---

## 5. Fluxo TO-BE

| # | Etapa | O que muda | Quem faz | Benefício | Esforço |
|---|---|---|---|---|---|
| 1 | Abertura do ofício | O app valida o motivo, o substituto e o período antes de registrar | Unidade | Menos devolução | Baixo |
| 2 | Autorização hierárquica | Cada chefia vê a sua fila e o que falta para o evento seguir | Chefias | Autorização rastreável | Baixo |
| 3 | Envio ao Gabinete | O evento avança sozinho quando todas as autorizações terminam | Chefias e app | Menos espera | Baixo |
| 4 | Análise de RH | A ficha nasce com os dados do evento e é anexada em um clique | Gerência de Suporte à Gestão de Pessoas | Ficha padronizada | Médio |
| 5 | Assinatura | O diretor vê uma fila única do que está pronto para assinar | Diretor Geral Adjunto | Fila única | Baixo |
| 6 | Envio à SESP | O app bloqueia o envio depois do dia 05 e registra a data | Gerência de Suporte à Gestão de Pessoas | Fim do indeferimento por esquecimento | Baixo |
| 7 | Acompanhamento | A planilha é uma visão do app, com CSV e os cinco campos obrigatórios | Gerência de Suporte à Gestão de Pessoas | Controle sem redigitação | Médio |
| 8 | Publicação no Diário Oficial | O evento só encerra com o número e a data da publicação | Gerência de Suporte à Gestão de Pessoas | Encerramento correto | Baixo |

---

## 6. Regras de negócio

| ID | Regra | Quando | Tipo | Exceção |
|---|---|---|---|---|
| RN01 | O motivo precisa ser férias, licença prêmio, licença para tratamento da própria saúde ou licença para acompanhar pessoa da família | Na abertura | Obrigatória | Nenhuma |
| RN02 | O substituto precisa ser informado e não pode ser o próprio gestor substituído | Na abertura | Obrigatória | Nenhuma |
| RN03 | O evento só chega ao Gabinete depois de todas as autorizações da linha hierárquica | Na tramitação | Obrigatória | Devolução para ajuste |
| RN04 | A ficha de solicitação é incluída pelo RH antes da assinatura | Na análise de RH | Obrigatória | Nenhuma |
| RN05 | A assinatura é do Diretor Geral Adjunto | Depois da ficha | Obrigatória | Nenhuma |
| RN06 | O envio à SESP precisa acontecer até o dia 05 do mês em que a substituição ocorre; depois da data, o evento é indeferido | No envio à SESP | Obrigatória | Nenhuma |
| RN07 | O evento só é encerrado com a publicação no Diário Oficial | No encerramento | Obrigatória | Indeferimento |
| RN08 | A planilha de controle tem substituído, substituto, motivo, período e publicação no Diário Oficial | No acompanhamento | Obrigatória | Nenhuma |

---

## 7. Telas e dados

### 7.1 Telas

| Rota | Título | Perfis | O que faz |
|---|---|---|---|
| `#/painel` | Painel | todos | Indicadores, próximos do dia 05 e a minha fila |
| `#/eventos` | Eventos | todos | Lista com filtros de situação, motivo, unidade e busca |
| `#/evento/novo` | Novo evento | unidade | Ofício com o substituto, o motivo e o período |
| `#/evento/:id` | Evento | todos | Trilha das sete etapas, tramitação, ficha, assinatura, envio, publicação e histórico |
| `#/fila` | Minha fila | todos | O que espera o perfil, em cartões com o prazo |
| `#/planilha` | Planilha de controle | todos | Os cinco campos obrigatórios, o CSV e o Excel (`.xlsx`) |
| `#/config` | Configuração | todos | Unidades, chefias, motivos, backup e dados fictícios |

### 7.2 Modelo de dados (IndexedDB `evento_substituicao_v1`)

| Store | Campos |
|---|---|
| `eventos` | id_evento, numero_sigadoc, data_oficio, unidade, unidade_nome, motivo, substituido, cargo_substituido, substituto, cargo_substituto, periodo_inicio, periodo_fim, status, assinado_por, assinado_cargo, assinado_em, envio_sesp_em, publicacao_numero, publicacao_do, indeferido_motivo, criado_em |
| `autorizacoes` | id, evento_id, nivel, gestor, cargo, situacao, data, perfil |
| `fichas` | id, evento_id, numero_ficha, data, analista, observacao |
| `publicacoes` | id, evento_id, numero_do, data_publicacao |
| `unidades` | id_unidade, nome, sigla, chefia, diretor, niveis |
| `log` | id, evento_id, tipo_evento, descricao, perfil, data_hora |

O prazo não é digitado: ele é calculado a partir do mês de `periodo_inicio`
(dia 05). O status também não é digitado: cada ação grava o novo status.

---

## 8. KPIs e piloto

| Indicador | Pergunta | Base | Esperado | Fonte |
|---|---|---|---|---|
| Eventos enviados fora do dia 05 | Quantos eventos chegaram à SESP depois do prazo? | A medir no piloto | Zero | Status e data de envio |
| Tempo entre a abertura e o envio à SESP | Quantos dias o evento leva da abertura ao envio? | A medir no piloto | Menor que o ciclo atual | Data do ofício e data do envio |
| Eventos parados na linha hierárquica | Quantos eventos esperam autorização? | A medir no piloto | Visíveis na fila do gestor | Status `autorizacao` |
| Eventos encerrados com publicação | Todo evento enviado termina com publicação no DO? | A medir no piloto | 100% | Status `publicado` e número do DO |

**Piloto**: 30 dias na Gerência de Suporte à Gestão de Pessoas, comparando a
planilha atual com a fila do app. Critério de aceite: a unidade abre o ofício,
cada chefia autoriza, o RH inclui a ficha, o Diretor assina, o RH envia à SESP e
registra a publicação, e o evento aparece na planilha com os cinco campos.

---

## 9. Stack, restrições e LGPD

### 9.1 Stack

- Um `index.html` com CSS, JS e dados embutidos; abre com duplo clique.
- IndexedDB para os dados, backup em `.json`, funciona sem internet.
- Sem CDN; a única biblioteca é a SheetJS 0.18.5, embutida em `vendor/` para gerar o `.xlsx`. Fontes do sistema.
- Publicação prevista no GitHub Pages ou no Firebase Hosting.

### 9.2 Restrições

- Não excluir um evento publicado.
- Não assinar sem a ficha.
- Não enviar à SESP depois do dia 05.
- Não encerrar sem a publicação no Diário Oficial.
- O SIGADOC continua sendo o sistema oficial do processo.

### 9.3 LGPD

- Dados tratados: nomes de gestores e substitutos, cargo, unidade, motivo do
  afastamento e período.
- O motivo de saúde é dado pessoal sensível: deve ficar restrito aos perfis que
  analisam o evento.
- Base legal: execução de políticas públicas de gestão de pessoas (art. 7º, III,
  da LGPD) e cumprimento de obrigação legal.
- No MVP os dados ficam só no navegador. A versão institucional precisa de
  login, segregação de funções, prazo de retenção e trilha inalterável.

---

## Anexo A · Dados de controle (planilha)

Campos obrigatórios: **substituído, substituto, motivo, período e publicação no
Diário Oficial**. O app acrescenta a situação, a unidade e o processo do
SIGADOC. O CSV sai com BOM e ponto e vírgula, pronto para o Excel.

## Anexo B · Status do evento

| Status | Cor | Etapa |
|---|---|---|
| Em autorização hierárquica | azul | 2 |
| Devolvido à unidade | vermelho | 2 |
| No Gabinete de Direção | azul | 3 |
| Em análise de RH | azul | 4 |
| Aguardando assinatura | amarelo | 5 |
| Assinado · aguardando envio à SESP | azul | 6 |
| Encaminhado à SESP | azul | 6 |
| Publicado no Diário Oficial | verde | 7 |
| Indeferido | vermelho | 7 |

## Anexo C · Como testar

```powershell
cd "Apps/evento-substituicao-temporaria"
python construir.py
python testes/testar.py
python testes/cenarios.py
python testes/jornada.py
```

## Anexo D · Pendências com pessoas

- Simone: confirmar unidades, chefias e níveis; enviar o desenho da ficha.
- Gerência: confirmar a regra do dia 05 e o fluxo de indeferimento.
- TI: definir a integração futura com o SIGADOC.

## Anexo E · Histórico

| Data | O que foi feito |
|---|---|
| 09/11/2026 | Documento recebido; app criado com os Sprints 0 a 7, dados fictícios, testes, diagramas e hub. |
| 09/11/2026 | Sprint 8: ajuste da unidade antes do reenvio e planilha Excel (`.xlsx`) com as abas Controle e Resumo. |
