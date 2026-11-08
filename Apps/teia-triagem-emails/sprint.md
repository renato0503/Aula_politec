# Plano de sprints · TEIA

## Andamento

| Sprint | Situação |
|---|---|
| 0 | Parte técnica feita em 02/11/2026: entrada do Firestore, `projeto.json`, seed de 10 e-mails fictícios, regras e modelos. |
| 1 | Feito em 02/11/2026: bancada, ficha do e-mail, 9 campos, extração simulada, validação humana e auditoria. |
| 2 | Feito em 02/11/2026: lotes, planilha consolidada, CSV e filtros. |
| 3 | Feito em 02/11/2026: alertas de divergência e OCR, tratamento de alerta, recusa e dicionários. |
| Identidade e usabilidade | Feito em 02/11/2026: casca de ferramenta, fonte monoespaçada, bancada de triagem, perfil triador/chefia, `processo.html` e jornada do cliente no Chromium e no Lightpanda. |
| 4 | Feito em 03/11/2026: campos do feedback, protocolo `nnnnnn/aaaa`, data do e-mail, novas categorias, 36 regionais e alerta de reiteração (2ª cobrança em 30 dias, premissa). |

## Pronto quando

O triador abre a fila, confere os 9 campos, trata os alertas, valida a requisição
e exporta a planilha, sem nenhuma requisição de rede.

## Sprint 4 · Correções do feedback (03/11/2026)

> Feedback de Nelson (nota 5). O layout novo no PC e no celular já foi feito nesta etapa; agora são os campos.

### Código
- [x] Retirar "Nível" (definido pelo coordenador) e "Nº da cobrança" (vem do Atena).
- [x] Incluir Nome da vítima, Nome do investigado e Réu preso (Sim, Não, Não informado).
- [x] Alertar quando a cobrança do mesmo protocolo for reiterada. (2ª cobrança em 30 dias; premissa)
- [x] Protocolo no formato `nnnnnn/aaaa`. (6 números, barra e ano)
- [x] Data da cobrança = data do e-mail. (campo somente leitura)
- [x] Tipos de crime: Crime Sexual, Local de Crime, Identificação Humana e Biologia.
- [x] AR para confronto: Sim, Não ou Não informado.
- [x] Lista de regionais completa, com a grafia informada. (36 unidades do feedback do Nelson)

### Decisão do setor
- [x] Confirmar a lista de regionais e a grafia. (lista enviada pelo Nelson em 03/11/2026)
- [x] Onde o coordenador informa o nível. (o campo saiu do app; o nível é do coordenador/Atena)
- [x] Regra do alerta de reiteração. Premissa: 2ª cobrança do mesmo protocolo em até 30 dias; confirmar no aceite.

**Pronto quando**: a ficha mostra vítima, investigado e réu preso, e a cobrança reiterada gera alerta.

## Sprint 5 · Ficha e classificação automática do Nelson (07/11/2026)

> Pedido do Nelson pelo WhatsApp, com a foto da disposição dos campos. Asterisco: item novo. Dois asteriscos: nome alterado.

### Feito
- [x] Campos em duas colunas, na ordem da foto: Classificação e Protocolo; Data da cobrança e Tipo de crime; Origem da cobrança e Nome da vítima; Prioridade Legal e Nome do Investigado/Suspeito/Acusado; Réu preso e Nome do familiar; Regional da Politec e AR para confronto; Objetivo.
- [x] Novo: Origem da cobrança (Judicial/Ministério Público, Delegacia, Outros).
- [x] Novo: Prioridade Legal (Vítima menor de idade, Idoso, Incapaz, Doença grave), com mais de uma opção.
- [x] Novo: Classificação automática e somente leitura: 1 Judicial ou Ministério Público; 2 Delegacia com qualquer prioridade legal ou réu preso; 3 Delegacia sem prioridade legal e sem réu preso; 4 Outros.
- [x] A fila passa a sair da classificação 1 para a 4, e o selo Normal/Alta/Urgente, que não seguia essa regra, saiu da tela e do CSV.
- [x] Nomes: "Nome do Investigado/Suspeito/Acusado", "Regional da Politec" e "Objetivo".
- [x] Registros já gravados no navegador recebem a origem pelo nome do órgão, para o triador conferir.
- [x] Cenário `s6_classificacao_automatica` e testes das quatro classes.

### Confirmar com o Nelson
- [ ] "Nome do familiar" está na foto sem asterisco, mas o campo não existia. Foi incluído como opcional.
- [ ] Réu preso "Não informado" conta como não preso: Delegacia sem prioridade legal fica na classificação 3.
- [ ] Prioridade Legal é opcional, porque a classificação 3 depende de não haver nenhum item.

**Pronto quando**: o Nelson conferir a ficha e a ordem da fila com cobranças reais.

