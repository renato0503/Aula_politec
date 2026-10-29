# Gestão de Documentos · contexto e arquitetura

> Equipe: Vitória Araújo Dias (Gabinete de Direção)
> Fonte: `PROJETO.md` e a arquitetura do curso: **HTML monolítico, offline first**.

---

## 1. O problema

O Gabinete usa um app de gestão, mas o acompanhamento de prazos e a cobrança de
retorno dos processos continuam manuais, processo a processo. São cerca de 200
processos por mês e 1 h por dia só de conferência, com risco de
extemporaneidade.

| Dado informado | Valor |
|---|---|
| Processos por mês | 200 |
| Tempo diário de acompanhamento | 1 h |
| Tempo parado na triagem | 48 h (lead time de 15 dias) |
| Requerimentos com anexo faltante | 60% |
| Despachos redigidos do zero | 100% |
| Piloto | 30 dias no Gabinete de Direção |

## 2. O que o MVP faz e o que não faz

| Faz | Não faz |
|---|---|
| Autua o processo com número `AAAA.NNNN-SD` (RN02) | Integra com o Siga-Doc |
| Exige os três anexos obrigatórios (RN01) | Envia e-mail de verdade |
| Calcula o prazo e o sinal verde, amarelo e vermelho (RN06, RN07) | Decide o mérito ou assina |
| Atribui o responsável e mostra a mesa virtual | Aplica decurso de prazo |
| Registra a trilha de auditoria | Guarda documentos reais |

## 3. Regras

- **RN01**: sem todos os anexos obrigatórios, o cadastro é recusado.
- **RN02**: o número de autuação segue `AAAA.NNNN-SD` e é único.
- **RN05**: o requerente não pode ser o responsável pela instrução.
- **RN06**: a partir de 70% do prazo, o sinal vira amarelo.
- **RN07**: ao atingir 100%, o sinal vira vermelho (vencido).
- **RN09/RN10**: a conclusão exige a assinatura da autoridade decisora e gera a
  notificação ao requerente.

## 4. Telas

| Rota | Perfil | O que faz |
|---|---|---|
| `#/painel` | todos | Vencidos, em atenção, no prazo e concluídos |
| `#/processos` | todos | Lista com filtros de sinal, situação e busca |
| `#/processo/novo` | servidor e chefia | Autuação com anexos e número gerado |
| `#/processo/:id` | todos | Ficha, prazo, documentos e histórico |
| `#/config` | todos | Perfil da cópia, backup e dados fictícios |

## 5. Modelo de dados (IndexedDB `gestao_documentos_v1`)

| Store | Campos |
|---|---|
| `processos` | id_processo, numero_processo, assunto, requerente, lotacao, data_autuacao, dias_prazo, responsavel, anexos, status |
| `documentos` | id_documento, processo_id, tipo_documento, data_criacao, assinado |
| `usuarios` | id_usuario, nome, perfil |
| `log` | id, processo_id, tipo_evento, descricao, perfil, data_hora |

O prazo é sempre calculado a partir de `data_autuacao` e `dias_prazo`; não existe
campo de "dias restantes" digitado.

## 6. LGPD e acesso

O protótipo usa nomes e números fictícios. A versão institucional precisa de
login e senha para os servidores do setor, segregação de funções (RN05), trilha
inalterável e observância da LGPD e da tabela de temporalidade documental.
