# Custódia Definitiva · contexto e arquitetura

> Equipe: Edjane Ávila (Gerência de Custódia Definitiva)
> Fonte: `PROJETO.md` e a arquitetura do curso: **HTML monolítico, offline first**.

---

## 1. O problema

Depois do processamento pericial, os vestígios remanescentes voltam às delegacias
de origem e as contraprovas ficam no Laboratório Forense. A responsabilidade
fragmentada entre unidades dificulta a rastreabilidade, a logística e a gestão do
acervo. Em 2025 foram cerca de 12.000 alíquotas de contraprova vindas do interior,
além da produção da capital.

| Dado informado | Valor |
|---|---|
| Laudos por mês | 1.233 |
| Horas mensais de processamento | 616,5 (estimadas) |
| Contraprovas de entorpecentes (2025) | ~12.000 |
| Laudos laboratoriais (jan a nov/2025) | 13.558 |
| Meta da defesa | reduzir em 60% o tempo de localização dos vestígios |

## 2. O que o MVP faz e o que não faz

| Faz | Não faz |
|---|---|
| Cadastra o vestígio com protocolo, lacre, categoria e volume | Integra com o Atena |
| Sugere o contêiner compatível com a categoria e a capacidade (RN02/RN03) | Move fisicamente os contêineres |
| Mostra o endereço digital (contêiner e posição) | Lê RFID |
| Registra a movimentação com perfil, data e hora (RN04) | Autoriza transferência ou descarte |
| Mostra a ocupação e a folga de cada contêiner | Monitora a temperatura do refrigerado |
| Mantém a trilha de movimentações | Usa dados reais ou sigilosos |

## 3. Regras

- **RN01**: o lacre é obrigatório e único entre os vestígios não descartados.
- **RN02**: só entra em contêiner compatível com a categoria.
- **RN03**: não aloca volume acima da folga do contêiner.
- **RN04**: toda movimentação registra perfil, data, hora, origem e destino.

## 4. Telas

| Rota | Perfil | O que faz |
|---|---|---|
| `#/painel` | todos | Total de vestígios, ocupação, contêineres cheios e pendências |
| `#/vestigios` | todos | Lista com filtros de categoria, contêiner, situação e busca |
| `#/vestigio/novo` | custódia e perito | Cadastro com endereçamento sugerido |
| `#/vestigio/:id` | todos | Ficha, endereço digital e movimentações |
| `#/conteineres` | todos | Capacidade, ocupação e condição de conservação |
| `#/config` | todos | Perfil da cópia, backup e dados fictícios |

## 5. Modelo de dados (IndexedDB `custodia_definitiva_v1`)

| Store | Campos |
|---|---|
| `categorias` | id_categoria, nome, tipo_conservacao, restricao |
| `conteineres` | id_conteiner, categoria_permitida, capacidade, tipo_conservacao, localizacao_fisica, status |
| `vestigios` | id_vestigio, protocolo, lacre, categoria_id, volume_ocupado, data_entrada, status, descricao, conteiner_id, posicao |
| `movimentacoes` | id_movimentacao, vestigio_id, tipo, data_hora, responsavel, origem, destino |
| `historico_mensal` | id_periodo, mes, entradas, saidas, ocupacao_final |

A ocupação nunca é um número digitado: é sempre calculada pela soma do
`volume_ocupado` dos vestígios armazenados em cada contêiner.

## 6. LGPD e cadeia de custódia

O protótipo usa apenas dados fictícios. A versão institucional precisa de
autenticação individual, controle de permissões, trilha de auditoria e observância
dos artigos 158-A a 158-F do Código de Processo Penal. A IA não substitui a
conferência física, a decisão técnica nem a autorização legal.
