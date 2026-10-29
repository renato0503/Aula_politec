# Controle do Processo de Aquisição · contexto e arquitetura

> Equipe: Kasteline Gonçalves (Aquisição)
> Fonte: `PROJETO.md` e a arquitetura do curso: **HTML monolítico, offline first**.

---

## 1. O problema

O processo de aquisição começa na unidade requisitante, passa pelo DFD, ETP,
análise de riscos, TR, pesquisa de preços, SIGADOC/SIAG, análises técnica e
jurídica e termina na definição da modalidade. Sem controle, o tempo se perde em
revisões, coleta de preços, assinaturas, análises e correção de pendências.

| Dado informado | Valor |
|---|---|
| Processos por semana | 10 |
| Duração informada | 8 h por processo |
| Prazo usado no protótipo | 30 dias |
| Base de referência | processos de 2024 e 2025 (DSI) |
| Decisão final | permanece com os agentes públicos |

## 2. O que o MVP faz e o que não faz

| Faz | Não faz |
|---|---|
| Registra o processo com SIGADOC e SIAG (RN01) | Integra com SIGADOC ou SIAG |
| Controla a etapa atual e os documentos exigidos (RN02) | Executa a licitação ou a contratação |
| Abre e acompanha pendências (RN03) | Decide a modalidade ou assina |
| Mostra atrasados e a fila por etapa | Fiscaliza contratos |
| Mantém o histórico das ações | Usa processos reais |

## 3. Regras

- **RN01**: números do SIGADOC e do SIAG são obrigatórios e únicos.
- **RN02**: a etapa só é concluída com os documentos que ela exige.
- **RN03**: pendência aberta impede o avanço da etapa.
- **RN04**: o processo fica atrasado quando passa o prazo em dias corridos.

## 4. Telas

| Rota | Perfil | O que faz |
|---|---|---|
| `#/painel` | todos | Em andamento, atrasados, pendências e processos por etapa |
| `#/processos` | todos | Lista com filtros de etapa, situação e busca |
| `#/processo/novo` | requisitante e compras | Registro com SIGADOC e SIAG |
| `#/processo/:id` | todos | Etapas, documentos, pendências e histórico |
| `#/config` | todos | Perfil da cópia, backup e dados fictícios |

## 5. Modelo de dados (IndexedDB `controle_aquisicoes_v1`)

| Store | Campos |
|---|---|
| `processos` | id_processo, numero_sigadoc, numero_siag, objeto, unidade, responsavel, data_abertura, prazo_dias, etapa, status |
| `documentos` | id_documento, processo_id, tipo_documento, nome, data |
| `pendencias` | id_pendencia, processo_id, motivo, aberta_em, resolvida_em |
| `log` | id, processo_id, acao, perfil, data_hora |

## 6. LGPD e acesso

O protótipo usa números e nomes fictícios. A versão institucional exige login,
matrícula funcional, permissões por setor e observância da Lei nº 14.133/2021 e
da LGPD. A automação não substitui a decisão dos agentes públicos.
