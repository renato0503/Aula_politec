# Renovação de Contratos · contexto e arquitetura

> Equipe: Rodrigo Neves Ribeiro (Coordenadoria de Aquisições e Contratos)
> Fonte: `PROJETO.md` e a arquitetura do curso: **HTML monolítico, offline first**.

---

## 1. O problema

O fiscal esquece os prazos de fiscalização porque acumula outras rotinas, e o
contrato pode vencer sem execução no período de vigência. O documento de origem
descreve o fluxo do Hórus (PlaniTec): monitorar, decidir, instruir, registrar o
aditivo, atualizar a vigência e registrar a auditoria. Ele **não** define um MVP.

| Dado do fluxo | Valor |
|---|---|
| Alerta padrão | 90 dias antes do término |
| Faixas do semáforo | 6 (normal, acompanhamento, atenção, providências, urgente, vencido) |
| Base de contratos | não informada |
| Meta de melhoria | não informada |

## 2. Recorte do protótipo

O MVP acadêmico transforma o fluxo em um painel que avisa o fiscal:

| Faz | Não faz |
|---|---|
| Cadastra o contrato e calcula o término (R2) | Integra com o Hórus |
| Mostra o semáforo de seis faixas (R3) | Decide a vantajosidade ou o enquadramento legal |
| Registra o termo aditivo e atualiza a vigência (R4) | Assina ou publica o aditivo |
| Mantém a trilha de auditoria (R6) | Envia e-mail ou notificação externa |
| Avisa o que vence em 90 dias | Trata reajuste e repactuação (Sprint 4) |

## 3. Regras

- **R1**: renovação só para contrato Vigente e com permissão de prorrogação.
- **R2**: `data_fim` = `data_inicio` + `vigencia_meses`, com ajuste manual.
- **R3**: semáforo de seis faixas; encerrado, rescindido e expirado saem da contagem.
- **R4**: depois do aditivo publicado, a vigência é atualizada e o contrato segue Vigente.
- **R6**: auditoria append-only das criações e mudanças de situação e vigência.

## 4. Telas

| Rota | Perfil | O que faz |
|---|---|---|
| `#/painel` | todos | Vencendo em 90 dias, urgentes, vencidos e as seis faixas |
| `#/contratos` | todos | Lista com filtros de faixa, situação e busca |
| `#/contrato/novo` | gestor e admin | Cadastro com término calculado |
| `#/contrato/:id` | todos | Ficha, semáforo, aditivos e auditoria |
| `#/config` | todos | Perfil da cópia, backup e dados fictícios |

## 5. Modelo de dados (IndexedDB `renovacao_contratos_v1`)

| Store | Campos |
|---|---|
| `contratos` | id_contrato, numero, fornecedor, cnpj, valor_c, data_inicio, vigencia_meses, data_fim, objeto, permite_prorrogacao, alerta_dias, status |
| `aditivos` | id_aditivo, contrato_id, numero_aditivo, data_assinatura, nova_vigencia, fundamento, status |
| `auditoria` | id_evento, contrato_id, acao, detalhe, perfil, data_hora |

## 6. LGPD e acesso

O protótipo usa dados fictícios. Na versão institucional, a escrita é restrita ao
autor do registro e às chefias, os documentos ficam em repositório privado e a
trilha de auditoria é append-only.
