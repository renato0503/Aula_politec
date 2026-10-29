# Comissão de Ética · Classificação da denúncia

Controle dos processos da Comissão de Ética, do recebimento da denúncia ao
encerramento, com classificação inicial assistida, roteiro de oitiva e minutas
padronizadas. As decisões continuam com a Comissão.

| Campo | Valor |
|---|---|
| Equipe | Letícia e Thiago (sobrenomes a confirmar) |
| Contato | leticiamesquita@politec.mt.gov.br |
| Unidade | Comissão de Ética |
| Tipo | Automação de script ou rotina |
| Stack pedida | Ainda não definida (GitHub Pages para o protótipo) |
| Fonte | `Aula 8/Entregas/Classificao-da-denncia-2026-10-27.json` (29/10/2026 11:19, horário de Cuiabá) |

## Arquivos

- `envio-original.json`: o envio, sem alteração.
- `projeto.json` e `PROJETO.md`: o envio completado (ver abaixo).
- `contexto.md` e `sprint.md`: arquitetura e plano de construção.

## Pendências

- **IA sem internet**: o app offline não chama serviço de IA externo, e os
  relatos são dados sensíveis. A classificação é assistida por regras
  (palavras-chave ligadas às categorias do Código de Ética), com a explicação
  da sugestão; um botão gera o prompt para uma ferramenta de IA autorizada. Ver
  `contexto.md`, seção 3.
- As categorias e os artigos do Código de Ética (LC nº 112/2002) precisam ser
  conferidos pela Comissão. O app traz uma lista inicial editável.
- Faltam os modelos de ata e de relatório de recomendações (citado pela equipe).

## Completado pelo professor (29/10/2026)

O `projeto.json` e o `PROJETO.md` desta pasta foram completados com propostas próximas do
que o aluno escreveu. O envio original está em `envio-original.json`.
Tudo o que foi completado precisa ser confirmado com o aluno no Sprint 0.

**Campos substituídos:**

- `mvp_plataforma`: a plataforma era desktop, a stack não estava definida, o armazenamento citava LocalStorage e a tela inicial era de login; alinhado à arquitetura do curso (HTML monolítico, offline first).
- `stack_detalhe`: a plataforma era desktop, a stack não estava definida, o armazenamento citava LocalStorage e a tela inicial era de login; alinhado à arquitetura do curso (HTML monolítico, offline first).
- `lgpd_retencao`: a plataforma era desktop, a stack não estava definida, o armazenamento citava LocalStorage e a tela inicial era de login; alinhado à arquitetura do curso (HTML monolítico, offline first).
- `mvp_tela_inicial`: a plataforma era desktop, a stack não estava definida, o armazenamento citava LocalStorage e a tela inicial era de login; alinhado à arquitetura do curso (HTML monolítico, offline first).

**Tabelas:**

- telas e artefatos (`tArtefatos`): refeita. As colunas vieram deslocadas uma posição e o tipo trazia texto livre; realinhadas, com rotas e tipos do formulário.
- regras de negócio (`tRegras`): refeita. O tipo trazia valores fora das opções do formulário; acrescentadas as regras da exceção (prova pendente), da trilha e do relatório sem dado pessoal.
- métricas (`tMetricas`): refeita. A granularidade estava como "por denúncia" e "por oitiva"; ajustada à opção Caso.
- riscos (`tRiscos`): refeita. O impacto "Altíssimo" não é opção do formulário (virou Alto); acrescentado o risco da classificação por regra.
- AS-IS (`tAsIs`): refeita. A coluna sistema trazia "Sistema"; preenchida com os meios citados (e-mail, Sigadoc, reuniões).

**Marcações:**

- `stack`: estava como Ainda não definido.
