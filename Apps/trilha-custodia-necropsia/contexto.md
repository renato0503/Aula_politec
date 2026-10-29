# TCIN · contexto e arquitetura

> Aluna: Silmara Bueno (IML · Coordenadoria de Perícias em Mortos)
> Fonte: `PROJETO.md`, os dois envios parciais e o protótipo `prototipo/tci.html`.

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

## 2. O que o MVP faz e o que não faz

| Faz | Faz |
|---|---|
| Registra o acionamento com protocolo único (RN01) | Integra com o Atena |
| Registra os quatro marcos com perfil, data e hora (RN03) | Substitui os livros oficiais |
| Registra lacres e amostras biológicas | Guarda dado pessoal real |
| Controla a situação do corpo (em custódia, aguardando identificação, não identificado, não reclamado, liberado) | Decide a identificação |
| Busca por protocolo, nome ou documento (RN04) | Libera o corpo sem autorização |
| Mostra a trilha de auditoria | Emite o auto de entrega oficial |

## 3. Regras

- **RN01**: o protocolo é único e gerado no acionamento.
- **RN02**: a liberação exige identificação registrada e auto de entrega com
  responsável e data.
- **RN03**: todo marco, lacre e mudança de situação registra perfil, data e hora.
- **RN04**: a busca aceita protocolo, nome ou documento.
- **RN05**: a lista do painel não mostra nome completo; a ficha mostra.

## 4. Telas

| Rota | Perfil | O que faz |
|---|---|---|
| `#/painel` | todos | Corpos por situação, alertas e últimos marcos |
| `#/corpos` | todos | Lista com filtros de situação e busca |
| `#/corpo/novo` | técnico e operador | Acionamento e cadastro do corpo |
| `#/corpo/:id` | todos | Ficha, marcos, lacres, situação e auditoria |
| `#/busca` | todos | Busca por protocolo, nome ou documento |
| `#/config` | todos | Perfil da cópia, backup e dados fictícios |

## 5. Modelo de dados (IndexedDB `trilha_custodia_v1`)

| Store | Campos |
|---|---|
| `corpos` | id_corpo, protocolo, origem, natureza, municipio, local, nome, documento, desconhecido, sexo, idade, tecnico, situacao, criado_em |
| `marcos` | id_marco, corpo_id, tipo, data_hora, perfil, observacao |
| `lacres` | id_lacre, corpo_id, codigo, destino, data_hora, perfil |
| `log` | id, corpo_id, acao, perfil, data_hora |

## 6. LGPD e cadeia de custódia

O protótipo usa nomes, documentos e protocolos fictícios. Na versão
institucional, os dados do corpo e da vítima são sensíveis: exigem autenticação
individual, controle de acesso por perfil, criptografia, trilha append-only e
observância dos artigos 158-A a 158-F do Código de Processo Penal e da LGPD.
