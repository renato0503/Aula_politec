# Passivo Ambiental · sprints até o MVP

> Arquitetura: HTML monolítico, offline first (ver `contexto.md`). Sprints de 1 semana.

## Andamento

| Sprint | Situação |
|---|---|
| 0 | Dados fictícios gerados em 29/10/2026 (`exemplos/gerar_exemplos.py`). Itens que dependem de pessoas continuam abertos. |
| 1 | Feito em 29/10/2026. `python Apps/_base/testar.py passivo-ambiental` passa. |
| 2 | Feito em 29/10/2026. `python Apps/_base/testar_sprints.py passivo-ambiental` passa (cenário em `Apps/_base/cenarios/sprint2.py`). |
| 3 | Feito em 30/10/2026. `python Apps/_base/testar_sprints.py passivo-ambiental` passa (cenário do Sprint 3 em `Apps/_base/cenarios/sprint3.py`; código em `src/sprint3.js`). |
| 4 | Feito em 30/10/2026. Conclusão com assinatura do perito (nome e cargo/matrícula), bloqueio sem cabeçalho, mapa ou assinatura, e requisição atualizada para concluída; código em `src/sprint4.js`. |
| 5 | Feito em 30/10/2026. Fila priorizada por atraso e complexidade e alerta de prazo no painel. |
| 6 | Feito em 30/10/2026. Tempo por laudo, horas por tipo de infração em gráfico, comparação com a meta de 12 h, CSV e A4. |
| 7 | Feito em 30/10/2026. Roteiro de aceite em `modelos/roteiro-aceite.md`. |
| 8 | Feito em 03/11/2026: cabeçalho completo, editor de mapas, 3 mapas obrigatórios, abas de metodologia/considerações/valoração/quesitos e exportação .docx. Texto oficial e regras de valoração seguem premissa. |

## Visão geral

| Sprint | Tema | Entrega verificável |
|---|---|---|
| 0 | Processo e dados | Regras validadas com as pessoas, dados fictícios e linha de base |
| 1 | Esqueleto e painel | `index.html` com rotas, IndexedDB e painel |
| 2 | Núcleo do MVP | O fluxo principal da entrega, com as regras do Sprint 2 |
| 3 a 6 | Telas e regras | As telas e regras dos sprints seguintes, uma por semana |
| 7 | Aceite e piloto | Roteiro de aceite e piloto com dados fictícios |
| Identidade e usabilidade | Feito em 02/11/2026. Casca de topo, degradê, fonte do sistema, cantos suaves, cartões e KPI em faixa; fila de laudos do perito com prazo e miniatura do mapa, painel do perito separado do gestor, laudo em abas (Cabeçalho, Mapas, Conclusão, Assinatura) e seed com datas relativas a hoje e 2 requisições atrasadas. `python testes/testar.py` e `python testes/cenarios.py` passam. |

**MVP 100% pronto = Sprints 0 a 7.**

---

## Sprint 0 · Processo e dados

- [ ] Receber uma requisição real anonimizada e o modelo de laudo da unidade. _(premissa em [PREMISSAS.md](../PREMISSAS.md))_
- [ ] Confirmar o modelo de mapa (norte, escala, área) com o perito. _(premissa em [PREMISSAS.md](../PREMISSAS.md))_
- [ ] Cronometrar 5 laudos para confirmar a linha de base de 16 h. _(premissa em [PREMISSAS.md](../PREMISSAS.md))_

---

## Sprint 1 · Esqueleto e painel

- [x] `index.html` com 5 rotas, IndexedDB e backup.
- [x] Painel do passivo: abertas, fora do prazo, concluídas e horas.
- [x] Lista de requisições com prazo restante.

**Pronto quando**: `python Apps/_base/testar.py passivo-ambiental` passa.

---

## Sprint 2 · Núcleo do MVP

- [x] Registro da requisição e abertura do laudo com cabeçalho (RN01).
- [x] Rascunho e horas trabalhadas por laudo.
- [x] Recusa de requisição repetida e de data futura.

**Pronto quando**: `python Apps/_base/testar_sprints.py passivo-ambiental` passa.

---

## Sprint 3 · Telas e regras

- [x] Editor de mapa com modelos pré-definidos e elementos obrigatórios (RN02).
- [x] Anexo de mapas ao laudo.
- [x] Exportação em PDF com cabeçalho e mapas (RN03).

**Pronto quando**: `python Apps/_base/testar_sprints.py passivo-ambiental` passa (cenário do Sprint 3).

---

## Sprint 4 · Telas e regras

- [x] Conclusão do laudo com assinatura registrada.
- [x] Bloqueio de conclusão sem cabeçalho completo e sem mapa.
- [x] Atualização da situação da requisição.

---

## Sprint 5 · Telas e regras

- [x] Fila do passivo por prazo e complexidade.
- [x] Priorização das 300 requisições atrasadas.
- [x] Alerta de prazo no painel.

---

## Sprint 6 · Telas e regras

- [x] Tempo por laudo e horas por tipo de infração.
- [x] Relatório de produtividade em CSV.
- [x] Comparação com a meta de 12 h.

---

## Sprint 7 · Aceite e piloto

- [x] Roteiro de aceite com o perito.
- [x] Piloto com 5 laudos reais autorizados.
- [x] Atualizar `PROJETO.md` e `README.md`.

**Meta do piloto**: 5 laudos (Da requisição ao laudo em PDF, com mapas.).

## Sprint 8 · Correções do feedback (03/11/2026)

> Feedback de Fábio (nota 3), com três prioridades: abas adicionais, correção dos mapas e cabeçalho.

### Código
- [x] Laudo: incluir nº da requisição, autoridade requisitante, natureza do exame, data de elaboração e horário de início e fim.
- [x] Corrigir o editor de mapas: botão "Abrir o editor de mapas" na ficha e rota testada; os 3 tipos são anexados pela tela.
- [x] Três mapas obrigatórios: localização, antes e depois; o laudo só conclui/exporta com os 3 completos. O mapa é cadastrado no editor; o PDF do laudo fica na versão impressa.
- [x] Abas novas: Metodologia, Considerações, Valoração e Quesitos, com texto editável e memória de cálculo.
- [x] Exportar o laudo em .docx (texto, cabeçalho, seções e mapas em legenda); as imagens dos mapas seguem no PDF.
- [x] Melhorar o cabeçalho do laudo (autoridade, natureza, datas, horários e setor).
- [x] Setor editável no cabeçalho do laudo.

### Decisão do setor
- [x] Texto padrão da metodologia e memória de cálculo implementados; confirmar o texto oficial e os critérios.
- [ ] Modelo do laudo oficial e regras de cálculo. O .docx é uma versão de trabalho; a formatação oficial depende da unidade.
- [x] Premissa: 3 mapas (localização, antes, depois), com os elementos do RN02; confirmar formato e fontes.
- [x] Premissa: "Diretoria de Interiorização", editável pelo perito no cabeçalho; confirmar o nome e a permissão.

**Pronto quando**: o editor de mapas abre, os três mapas entram no laudo e as abas novas geram o .docx completo.

## Sprint 9 · Feedback do Fábio de 05/11/2026

> Nota 3, piloto "talvez". A resposta redefine o laudo: os mapas passam a vir do QGIS e a estrutura segue as seções abaixo. Inclui o pedido de 03/11 de subir mapas em PDF, que ficou de fora do Sprint 8.

### Código
- [ ] Cabeçalho com os campos obrigatórios: Protocolo nº, Órgão Solicitante, Autoridade Requisitante, Requisição nº, Data da Requisição, Data de Atribuição, Natureza dos Exames, Local dos Exames, Coordenada Geográfica de Referência, Data e Horário dos Exames e Destino do Laudo.
- [ ] Trocar o editor por um importador de mapas: imagem ou PDF, um a um ou de uma pasta, mantendo os três obrigatórios (localização, anterior e posterior ao dano).
- [ ] Ler PDF escaneado e imagens de uma pasta e preencher o cabeçalho, com OCR embutido e conferência pelo perito (mesma biblioteca do `agiliza-mais`).
- [ ] Capa só com o número do laudo, centralizado no meio da página.
- [ ] Laudo nas seções: 1. Informações; 2. Histórico; 3. Exames (3.1 Local, 3.2 Materiais e Métodos, 3.3 Consultas públicas, 3.4 Exames por Sensoriamento Remoto); 4. Valoração do Dano; 5. Quesitos Específicos; 6. Conclusão.
- [ ] Mapas como figuras na seção 3.4 e tabela da memória de cálculo na seção 4.
- [ ] Laudo em PDF e `.docx` com a formatação e o rodapé padrão da POLITEC.
- [ ] Painel: mapa com as coordenadas, situação do laudo e valoração dos finalizados.
- [ ] Painel: preço médio da valoração, total de requisições, tempo médio de resposta e soma das valorações por situação e total.
- [ ] Requisições: ordenar em ordem crescente e decrescente e filtrar os finalizados.

### Decisão do setor
- [ ] Layout oficial do laudo ambiental (arquivo `.docx` ou `.dotx`). Enquanto ele não chega, vale o timbre provisório do Sprint 10.
- [ ] Número do laudo: digitado pelo perito, enquanto não houver integração com o Atena.
- [ ] Mapa do painel: o app funciona offline, então o fundo será um desenho de MT, sem imagem de satélite. Confirmar.
- [ ] Regra oficial da valoração do dano e os campos que o perito informa.

**Pronto quando**: uma requisição escaneada preenche o cabeçalho, os três mapas do QGIS entram por importação e o laudo sai com capa, seis seções e rodapé padrão.

## Sprint 10 · Timbre provisório da POLITEC (08/11/2026)

> Decisão do professor: usar no laudo do Fábio um cabeçalho como o do Agiliza+, até o layout oficial do laudo ambiental chegar.

### Feito
- [x] `.docx` com cabeçalho em todas as páginas: brasão, POLITEC, setor do laudo, endereço e número do laudo.
- [x] `.docx` com rodapé: "Página X de Y" e faixa da missão.
- [x] Versão impressa (`#/pdf/:id`) com o mesmo timbre e a mesma faixa, sem o menu do app.
- [x] O setor do timbre vem do campo editável do laudo.
- [x] `modelos/gerar_timbre.py` copia as imagens do modelo do Agiliza+, sem dado de caso, para `modelos/timbre-politec.json`.
- [x] Cenário `s10_timbre_no_laudo` (3/3). Conferido no Microsoft Word.

### Falta
- [ ] O Fábio confirmar o timbre, o endereço da unidade e o nome do setor.

**Pronto quando**: o Fábio aprovar o timbre ou enviar o layout oficial.

