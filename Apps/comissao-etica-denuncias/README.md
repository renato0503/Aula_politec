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

## Como construir e testar

Este app é autônomo. `nucleo/`, `construir.py` e `testes/` são só dele e não
importam nada de `Apps/_base/`, porque esta pasta vai virar um repositório
próprio no GitHub. O `index.html` é **gerado**: edite as fontes (`app.json`,
`src/`, `nucleo/`, `exemplos/seed.json`) e rode a construção.

```powershell
cd "Apps/comissao-etica-denuncias"
python construir.py           # gera o index.html a partir de app.json, src/, nucleo/ e os dados
python testes/testar.py       # estrutura: zero rede, #/testes 100%, rotas por perfil, tema e celular
python testes/cenarios.py     # cenários dos sprints: usa a tela como uma pessoa usaria
```

Antes da primeira execução: `pip install playwright` e
`playwright install chromium`.

Os dados fictícios são gerados por `exemplos/gerar_exemplos.py`; rode-o quando
mudar o esquema e confira o novo `exemplos/seed.json` no navegador.


Regras: não edite `index.html` direto; nenhum arquivo de fora da pasta do app é
importado; o tema claro é o padrão e o escuro só entra pelo botão; os textos
seguem o português do Brasil com acentuação, sem travessões.

## Identidade e usabilidade (02/11/2026)

A identidade é de comissão: fonte serifada, densidade ampla, cantos retos,
superfície de papel e KPI em faixa. A tela-assinatura é o **funil do processo
ético** em sete etapas clicáveis, que filtram a lista de casos. Toda tela do caso
abre com o **dossiê “Reservado”** e a barra de etapas (Registro, Classificação,
Admissibilidade, Oitivas, Documentos, Encerramento), com a etapa atual marcada.
O seed passou a distribuir os casos pelas etapas. Código em `src/identidade.js` e
`src/app.css`.

## Sprint 8 · Feedback

A classificação mostra o texto do artigo e preenche o enquadramento padrão; a admissibilidade usa a lista de membros e o fundamento padrão; as oitivas podem ser excluídas e encerradas; a ata usa **admissão** e o enquadramento; o relatório indica o curso; o encerramento usa o texto das recomendações; e os documentos podem ser enviados por `mailto:`.

## Mapa do processo

O `processo.html` mostra o **AS-IS** (como o processo funciona antes do MVP) e o
**TO-BE** (como fica com o MVP), com as métricas, regras e papéis do projeto.
Abra ao lado do `index.html`.
