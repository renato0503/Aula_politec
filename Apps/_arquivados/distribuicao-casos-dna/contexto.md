# Distribuição de casos de DNA · contexto e arquitetura

> Equipe: Nelson e Luciana (Gerência de Perícias em Biologia Molecular)
> Fonte: `PROJETO.md` e a arquitetura do curso: **HTML monolítico, offline first**.

---

## 1. O problema

As pastas dos casos eram distribuídas depois da obtenção dos perfis genéticos, em
lotes de 5 a 8 por perito. A distribuição misturava casos ordinários e cobranças,
e alguns casos ficavam semanas sem perito. O gargalo é o tempo até a distribuição
de todos os casos da rodada.

| Dado informado | Valor |
|---|---|
| Casos por mês | 300 |
| Duração informada | 84 h/caso/mês |
| Lote antigo por perito | 5 a 8 pastas |
| Piloto | 30 dias, registrado em planilha |
| Meta | reduzir o tempo entre processamento e distribuição |

## 2. O que o MVP faz e o que não faz

| Faz | Não faz |
|---|---|
| Monta a rodada da placa com os casos | Processa amostras |
| Separa a fila de cobranças (RN03) | Interpreta perfis genéticos |
| Distribui a rodada ordinária inteira a um perito (RN02) | Emite ou assina o laudo |
| Sugere o próximo perito pela rotação (RN04) | Integra com o Atena ou o Power BI |
| Mede o tempo entre processamento e distribuição | Usa amostras ou protocolos reais |

## 3. Regras

- **RN01**: a rodada só é distribuída com todos os casos ordinários processados.
- **RN02**: a rodada ordinária inteira vai para um único perito.
- **RN03**: as cobranças ficam em fila separada, distribuídas após a aliquotagem.
- **RN04**: o perito da rodada anterior não recebe a próxima (rotação).

## 4. Telas

| Rota | Perfil | O que faz |
|---|---|---|
| `#/painel` | todos | Casos sem perito, rodadas e tempo até a distribuição |
| `#/rodadas` | todos | Lista das rodadas e situação |
| `#/rodada/nova` | técnico e coordenador | Monta a placa e os casos |
| `#/rodada/:id` | coordenador | Distribui a rodada e as cobranças |
| `#/config` | todos | Perfil da cópia, backup e dados fictícios |

## 5. Modelo de dados (IndexedDB `distribuicao_casos_dna_v1`)

| Store | Campos |
|---|---|
| `rodadas` | id_rodada, placa, data, perito_id, status |
| `casos` | id_caso, rodada_id, protocolo, tipo, status, data_processamento, perito_id, distribuido_em |
| `peritos` | id_perito, nome, especialidade, ativo |
| `log` | id, rodada_id, acao, perfil, data_hora |

## 6. LGPD e cadeia de custódia

O protótipo usa protocolos e peritos fictícios. A versão institucional exige
autenticação individual, trilha de auditoria e controle de acesso por perfil. A
custódia, a análise e a interpretação dos perfis continuam com as pessoas.
