# Evento de Substituição Temporária · contexto e arquitetura

> Responsável: Simone Alem (Gerência de Suporte à Gestão de Pessoas)
> Fonte: `PROJETO.md` e a arquitetura do curso: **HTML monolítico, offline first**.

---

## 1. O problema

O afastamento temporário de um gestor é um processo de sete etapas, com quatro
unidades e um prazo que decide o resultado: o envio à SESP precisa acontecer até
o dia 05 do mês em que a substituição ocorre. O processo vive no SIGADOC e o
controle paralelo em uma planilha de Excel. A planilha não avisa o prazo, não
mostra a etapa e não guarda a trilha das autorizações.

| Dado informado | Valor |
|---|---|
| Etapas do processo | 7 (abertura, autorização, Gabinete, RH, assinatura, SESP, publicação) |
| Motivos válidos | 4 (férias, licença prêmio, saúde, acompanhar familiar) |
| Prazo do envio à SESP | dia 05 do mês da substituição |
| Status da planilha | amarelo (aguardando assinatura), azul (encaminhado à SESP), verde (publicado) |
| Campos obrigatórios | substituído, substituto, motivo, período, publicação no DO |
| Piloto | 30 dias na Gerência de Suporte à Gestão de Pessoas |

## 2. O que o MVP faz e o que não faz

| Faz | Não faz |
|---|---|
| Abre o ofício com o substituto, o motivo e o período (RN01, RN02) | Integra com o SIGADOC |
| Cria uma autorização por nível da linha hierárquica (RN03) | Assina digitalmente |
| Encaminha ao Gabinete e ao RH | Envia e-mail |
| Inclui a ficha de solicitação (RN04) | Publica no Diário Oficial |
| Mostra a fila de assinatura do Diretor (RN05) | Decide o mérito |
| Bloqueia o envio depois do dia 05 (RN06) | Guarda documentos reais |
| Encerra só com a publicação no DO (RN07) | — |
| Mantém a planilha e exporta CSV e Excel (`.xlsx`) (RN08) | — |
| Ajusta o evento devolvido e reenvia para a autorização | — |

## 3. Regras

- **RN01**: quatro motivos válidos; outro motivo é recusado.
- **RN02**: o substituto é obrigatório e diferente do substituído.
- **RN03**: todas as autorizações antes do Gabinete.
- **RN04**: a ficha de RH antes da assinatura.
- **RN05**: a assinatura é do Diretor Geral Adjunto.
- **RN06**: envio até o dia 05 do mês da substituição; depois, indeferimento.
- **RN07**: encerramento só com a publicação no Diário Oficial.
- **RN08**: os cinco campos obrigatórios na planilha de controle.

## 4. Telas

| Rota | Perfil | O que faz |
|---|---|---|
| `#/painel` | todos | Indicadores, próximos do dia 05 e a minha fila |
| `#/eventos` | todos | Lista com filtros de situação, motivo, unidade e busca |
| `#/evento/novo` | unidade | Ofício com o substituto, o motivo e o período |
| `#/evento/:id` | todos | Trilha das sete etapas, tramitação, ficha, assinatura, envio, publicação e histórico |
| `#/fila` | todos | O que espera o perfil, em cartões com o prazo |
| `#/planilha` | todos | Os cinco campos obrigatórios e o CSV |
| `#/config` | todos | Unidades, chefias, motivos, backup e dados fictícios |

## 5. Modelo de dados (IndexedDB `evento_substituicao_v1`)

| Store | Campos |
|---|---|
| `eventos` | id_evento, numero_sigadoc, data_oficio, unidade, unidade_nome, motivo, substituido, cargo_substituido, substituto, cargo_substituto, periodo_inicio, periodo_fim, status, assinado_por, assinado_cargo, assinado_em, envio_sesp_em, publicacao_numero, publicacao_do, indeferido_motivo, criado_em |
| `autorizacoes` | id, evento_id, nivel, gestor, cargo, situacao, data, perfil |
| `fichas` | id, evento_id, numero_ficha, data, analista, observacao |
| `publicacoes` | id, evento_id, numero_do, data_publicacao |
| `unidades` | id_unidade, nome, sigla, chefia, diretor, niveis |
| `log` | id, evento_id, tipo_evento, descricao, perfil, data_hora |

O prazo é sempre calculado a partir do mês de `periodo_inicio` (dia 05). O
status é consequência das ações: cada ação grava o novo status e um registro na
trilha. Não existe campo de "dias restantes" digitado.

## 6. Fluxo de status

```
autorizacao ──(todas as autorizações)──► gabinete ──(Gabinete)──► analise_rh
     ▲                                                                  │
     │ (reenvio)                                                        ▼
 devolvido ◄──(chefia devolve)                              aguardando_assinatura
                                                                        │ (Diretor)
                                                                        ▼
                        publicado ◄──(RH publica)── encaminhado_sesp ◄── assinado
                            │                                      (RH envia, até o dia 05)
                            └── encerra
indeferido ◄── (fora do prazo ou motivo inválido)
```

## 7. Arquitetura do app

- `nucleo/casca.html`: casca do app (cabeçalho, menu, roteador, IndexedDB,
  perfis, backup e `#/testes`). É do app.
- `nucleo/visual.css`: identidade visual (tema claro padrão, escuro pelo botão).
- `app.json`: título, banco, perfis, rotas, permissões e bloco `visual`.
- `src/app.js`: regras, telas e ações.
- `src/identidade.js`: a tela-assinatura "Minha fila" e o resumo no painel.
- `src/app.css`: trilho das sete etapas e cartões da fila.
- `construir.py`: gera o `index.html` e embute `vendor/` (SheetJS para o `.xlsx`) e `exemplos/seed.json`.
- `testes/`: estrutura (`testar.py`), cenários (`cenarios.py`) e jornada
  (`jornada.py`).

## 8. LGPD e acesso

O protótipo usa nomes, unidades e processos fictícios. A versão institucional
precisa de login e senha, segregação de funções, trilha inalterável, restrição
do motivo de saúde aos perfis que analisam o evento e prazo de retenção
definido com o RH. O perfil do MVP é uma lente de demonstração, não é segurança.
