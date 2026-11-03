# PROJETO.md — NIHDE

**Aluna:** Kesia Melo
**Unidade:** Núcleo de Identificação Humana e Desaparecidos — NIHDE
**Contato:** nih@politec.mt.gov.br
**Projeto:** NIHDE — Gestão de dados de corpos não identificados e corpos não reclamados
**Tipo:** aplicativo web / portal
**Data:** 2026-11-03

## 1. Problema

O IML registra a entrada do corpo no Atena, mas os setores que fazem a
identificação (necropapiloscopia, DNA, odontologia e antropologia) não sabem
quando outro setor identificou o corpo. O resultado é retrabalho, amostra
processada sem necessidade, custo de reagente e tempo do perito. A direção da
POLITEC não consegue responder quantos corpos não identificados deram entrada
nos IMLs no ano.

Hoje cada unidade mantém uma planilha de Excel. O protocolo do corpo e os
protocolos dos exames complementares divergem, e os dados ficam dentro de laudos
em PDF.

## 2. Objetivo do MVP

Responder, com dados estruturados, **quantos corpos não identificados a POLITEC
possui, sepultados ou não**, e o que já foi feito em cada caso.

**Dentro do escopo:** entrada do corpo, características físicas, quatro exames
de identificação (necropapiloscopia, DNA, odontologia e antropologia), via e data
da identificação, busca e localização da família, entrega, sepultamento pelo
município, identificação depois do sepultamento, filtros por unidade e situação,
relatório e CSV, auditoria.

**Fora do escopo:** integrar com o Atena, integrar com outros estados, emitir
laudo e autenticar com a base funcional. O **módulo de desaparecidos** está sendo
construído por outra IA, com dados públicos, dentro do MVP; o contrato está em
docs/CONTRATO-DESAPARECIDOS.md. A integração com outros estados fica para a
fase 2 e depende da direção da POLITEC.

## 3. Papéis

| Papel | O que vê | O que faz |
|---|---|---|
| Equipe do NIHDE | Todos os corpos e o relatório | Mantém o registro, identifica, busca família e registra sepultamento |
| Servidor do IML | Corpos da sua unidade | Registra a entrada e os exames |
| Gestão POLITEC | Painel e relatório | Acompanha os números; não altera o caso |

No MVP o perfil é uma lente de demonstração; a autenticação real depende da TI.

## 4. Dados

Uma linha por corpo:

`id, protocolo (Atena), unidade do IML, data_entrada, data_localizacao, municipio,
local, sexo, idade, altura, peso, olhos, cabelo, pele, sinais, nome, documento,
identificado, situacao, via_identificacao, data_identificacao, exames,
familia, sepultamento, entrega_em, observacoes, criado_em`.

`exames` tem as quatro vias, cada uma com `status` (não solicitado, solicitado,
em andamento, positivo, negativo), `protocolo` e `data`.

`familia` guarda nome, parentesco, contato, busca iniciada, localizada, data da
localização e entrega. `sepultamento` guarda data, município, local e certidão.

O `log` guarda cada ação com data, hora e perfil.

## 5. Regras de negócio

- **RN01** — o protocolo do Atena é único.
- **RN02** — cada exame tem status, protocolo e data; o positivo é o que autoriza
  a identificação pela via.
- **RN03** — a identificação registra a via, a data e muda a situação para
  identificado; se o corpo já foi sepultado, para identificado após sepultamento.
- **RN04** — o sepultamento pelo município só é registrado depois de 30 dias e
  com corpo sem identificação, com data, local e certidão.
- **RN05** — a entrega à família exige identificação e família localizada.
- **RN06** — corpo identificado sem família localizada pode ser marcado como não
  reclamado.
- **RN07** — a lista mostra iniciais; o nome completo, o contato da família e o
  local do sepultamento ficam na ficha e exigem acesso restrito na versão
  institucional (LGPD).
- **RN08** — toda ação fica na auditoria, inclusive a identificação depois do
  sepultamento.

## 6. Telas

`#/painel` (pergunta do MVP, KPIs e filtros), `#/corpos` (lista), `#/corpo/novo`
(cadastro), `#/corpo/:id` (exames, identificação, família, sepultamento e
auditoria), `#/relatorio` (por unidade, por via e CSV) e `#/config`.

## 7. KPIs

- Corpos não identificados (total e por unidade).
- Identificados não reclamados.
- Taxa de identificação.
- Sepultados pelo município.
- Entregues à família.
- Corpos por via de identificação.

## 8. Stack

HTML único, CSS e JS embutidos, IndexedDB e backup `.json`, publicado no GitHub
Pages. Offline first, sem requisição de rede. Dados fictícios com semente fixa.

## 9. Restrições e LGPD

Dados de corpo, família e servidor são sensíveis. No MVP, todos fictícios. A
versão institucional exige autenticação, acesso por papel, criptografia e
observância da LGPD. A retenção e a exclusão dependem da direção da POLITEC.

## AS-IS e TO-BE

**AS-IS:** entrada no Atena, planilha por IML, protocolos paralelos, exames em
PDF, busca manual da família e sepultamento sem controle central.

**TO-BE:** um registro por corpo, com exames, via de identificação, família,
sepultamento e auditoria; painel e relatório que respondem a pergunta do MVP. O
cadastro continua no Atena; a integração com desaparecidos e outros estados fica
para a fase 2.

**Piloto:** 90 dias, em todos os corpos que entrarem no IML de Cuiabá.
