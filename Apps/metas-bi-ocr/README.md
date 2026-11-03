# Monitoramento de Metas pelo BI

Lê o relatório mensal do Power BI 1 (laudos pendentes), confere os números e
gera a planilha que alimenta o Power BI de monitoramento, no lugar da digitação
manual.

| Campo | Valor |
|---|---|
| Aluna | Karine Assunção |
| Contato | karineassuncao@politec.mt.gov.br |
| Unidade | CQUAL (Núcleo de Informações, NIINS) |
| Tipo | Automação de script ou rotina |
| Stack pedida | Power BI + Google Planilhas, com OCR do PDF |
| Fonte | `Aula 8/Entregas/Automao-do-monitoramento-de-metas-pelo-BI-2026-10-27.json` (29/10/2026 10:14, horário de Cuiabá) |

## Arquivos

- `envio-original.json`: o envio, sem alteração.
- `projeto.json` e `PROJETO.md`: o envio completado (ver abaixo).
- `contexto.md` e `sprint.md`: arquitetura e plano de construção.

## Pendências

- O formato do PDF do Power BI 1 não veio com o envio. Sem uma amostra (com
  números fictícios), o leitor é escrito sobre um formato suposto.
- Confirmar se o Power BI 1 permite **Exportar dados** (CSV ou Excel) nos
  visuais. Se permitir, o OCR deixa de ser necessário e o risco principal da
  defesa (erro de reconhecimento) some.

## Completado pelo professor (29/10/2026)

O `projeto.json` e o `PROJETO.md` desta pasta foram completados com propostas próximas do
que o aluno escreveu. O envio original está em `envio-original.json`.
Tudo o que foi completado precisa ser confirmado com o aluno no Sprint 0.

**Campos preenchidos (estavam vazios):** `mvp_plataforma`, `doc_descricao`.

**Campos substituídos:**

- `aluno`: o nome e o e-mail estavam em maiúsculas; o escopo, a tela inicial e o critério estavam curtos; completados a partir da visão TO-BE da aluna.
- `contato`: o nome e o e-mail estavam em maiúsculas; o escopo, a tela inicial e o critério estavam curtos; completados a partir da visão TO-BE da aluna.
- `dentro`: o nome e o e-mail estavam em maiúsculas; o escopo, a tela inicial e o critério estavam curtos; completados a partir da visão TO-BE da aluna.
- `entrega`: o nome e o e-mail estavam em maiúsculas; o escopo, a tela inicial e o critério estavam curtos; completados a partir da visão TO-BE da aluna.
- `mvp_tela_inicial`: o nome e o e-mail estavam em maiúsculas; o escopo, a tela inicial e o critério estavam curtos; completados a partir da visão TO-BE da aluna.
- `mvp_criterio`: o nome e o e-mail estavam em maiúsculas; o escopo, a tela inicial e o critério estavam curtos; completados a partir da visão TO-BE da aluna.
- `mvp_dados`: o nome e o e-mail estavam em maiúsculas; o escopo, a tela inicial e o critério estavam curtos; completados a partir da visão TO-BE da aluna.
- `mvp_mock`: o nome e o e-mail estavam em maiúsculas; o escopo, a tela inicial e o critério estavam curtos; completados a partir da visão TO-BE da aluna.
- `hospedagem_escolhida`: o nome e o e-mail estavam em maiúsculas; o escopo, a tela inicial e o critério estavam curtos; completados a partir da visão TO-BE da aluna.
- `lgpd_dados`: o nome e o e-mail estavam em maiúsculas; o escopo, a tela inicial e o critério estavam curtos; completados a partir da visão TO-BE da aluna.
- `stack_detalhe`: a stack marcada era Power BI; o Power BI continua como fonte e destino, e o app faz a ponte entre os dois.

**Tabelas:**

- AS-IS (`tAsIs`): refeita. A aluna informou 8 h no total; dividido pelas etapas descritas (consulta, digitação, conferência). Os tempos por etapa são estimativa.
- TO-BE (`tToBe`): refeita. A linha única foi dividida nas etapas da visão TO-BE.
- papéis (`tPapeis`): refeita. A tabela trazia um papel genérico.
- telas e artefatos (`tArtefatos`): refeita. A tabela veio com uma linha deslocada.
- entidades (`tEntidades`): refeita. A entidade enviada só tinha a coluna data.
- regras de negócio (`tRegras`): linhas acrescentadas. Acrescentadas as conferências citadas no AS-IS.
- fontes de dados (`tFontes`): refeita. Detalhada a fonte e acrescentada a planilha de destino.
- métricas (`tMetricas`): refeita. A métrica enviada só tinha a pergunta.
- hospedagem (`tHospedagem`): refeita. A linha enviada só tinha o tipo; acrescentada a opção que a aluna citou nas lacunas.
- marcos (`tMarcos`): refeita. O marco enviado era um risco; movido para a tabela de riscos.
- riscos (`tRiscos`): refeita. A tabela veio vazia.
- referências (`tRefs`): linhas acrescentadas. Acrescentada a alternativa ao OCR.

**Marcações:**

- `stack`: era Power BI; o Power BI continua como fonte e destino.
- `req`: acrescentados Trilha de auditoria (correções) e Funcionar offline.

## Como construir e testar

Este app é autônomo. `nucleo/`, `construir.py` e `testes/` são só dele e não
importam nada de `Apps/_base/`, porque esta pasta vai virar um repositório
próprio no GitHub. O `index.html` é **gerado**: edite as fontes (`app.json`,
`src/`, `nucleo/`, `exemplos/seed.json`) e rode a construção.

```powershell
cd "Apps/metas-bi-ocr"
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

A identidade é de monitoramento: cabeçalho claro, densidade ampla, cantos suaves
e KPI em anel. A tela-assinatura é o **ano em 12 meses**, cada mês com a situação
(sem relatório, importado, conferido ou gerado) e o atalho para a tela certa. O
fluxo ganhou os **passos 1 Importar · 2 Conferir · 3 Gerar planilha** no topo das
três telas. Código em `src/identidade.js` e `src/app.css`.

## Mapa do processo

O `processo.html` mostra o **AS-IS** (como o processo funciona antes do MVP) e o
**TO-BE** (como fica com o MVP), com as métricas, regras e papéis do projeto.
Abra ao lado do `index.html`.
