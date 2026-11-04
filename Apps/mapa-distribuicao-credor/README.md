# Mapa de Distribuição por Credor e Distribuição Orçamentária

Rotina que lê a planilha de distribuição por órgão (anexo do TR) e o relatório
do pregoeiro e gera o mapa por grupo, órgão e empresa, a tabela de conferência
e a distribuição orçamentária por credor e órgão, sem redigitação.

| Campo | Valor |
|---|---|
| Aluno | Igor Henrique de Menezes Costa |
| Contato | izgdreyar@gmail.com |
| Unidade | Setor de Licitações, POLITEC/MT |
| Tipo | Automação de script ou rotina |
| Stack pedida | HTML único (CSS/JS inline), JSON embutido, GitHub Pages (já é a arquitetura do curso) |
| Fonte | `Aula 8/Entregas/Automao-do-Mapa-...-2026-10-29 (2).json` (29/10/2026 09:04, horário de Cuiabá) |

## Arquivos

- `projeto.json`: resposta do formulário (importável).
- `PROJETO.md`: gerado pelo próprio formulário a partir do `.json`.
- `contexto.md` e `sprint.md`: arquitetura e plano de construção.

## Pendências

- O `WorkFlow.docx` (fluxo atual com os exemplos 1 a 8 das planilhas) é a base
  do AS-IS e não veio com o envio.
- Faltam planilhas de exemplo e um relatório do pregoeiro de amostra, sem dado
  pessoal. Sem eles, o leitor de arquivos é escrito sobre um formato suposto.
- Na tabela de telas, as colunas ficaram deslocadas (o objetivo está em "rota",
  o usuário em "objetivo"). O `contexto.md` usa a leitura corrigida.
- A distribuição orçamentária está marcada como "MVP: Não" na tabela de telas,
  mas aparece no escopo e no critério de aceite. O `contexto.md` a mantém no MVP.

## Completado pelo professor (29/10/2026)

O `projeto.json` e o `PROJETO.md` desta pasta foram completados com propostas próximas do
que o aluno escreveu. O envio original está em `envio-original.json`.
Tudo o que foi completado precisa ser confirmado com o aluno no Sprint 0.

**Campos substituídos:**

- `doc_faltando`: acrescentado o mapa manual de referência, que o critério de aceite exige.

**Tabelas:**

- telas e artefatos (`tArtefatos`): refeita. As colunas vieram deslocadas uma posição (o objetivo estava em rota, o usuário em objetivo); realinhadas, com as rotas do `contexto.md`. A distribuição orçamentária passou a MVP "Sim", como no escopo e no critério de aceite. Acrescentadas a tabela por empresa e a exportação.
- papéis (`tPapeis`): refeita. O terceiro papel (quem fornece o relatório com vencedores e valores) estava como "Analista de licitações"; corrigido para Pregoeiro.
- regras de negócio (`tRegras`): linhas acrescentadas. Acrescentadas as 4 regras que o formulário deixava abertas (homologado por item, arredondamento, ordem da dotação e grupo misto), com a proposta mais próxima das planilhas da equipe.
- fontes de dados (`tFontes`): linhas acrescentadas. Acrescentada a fonte da dotação, citada nas entradas do AS-IS.
- riscos (`tRiscos`): linhas acrescentadas. Acrescentados os riscos do cálculo.
- referências (`tRefs`): refeita. A Lei nº 4.320/1964 estava com o uso "justificar dados sintéticos"; ajustado para a classificação 3 e 4, que é o que o projeto usa. Acrescentada a homologação (Lei nº 14.133/2021).

## Telas prontas (03/11/2026)

| Rota | O que faz |
|---|---|
| `#/processos` | Lista de processos, criação e carga do exemplo |
| `#/importar/:proc` | Leitura das três planilhas, com associação de colunas salva por modelo |
| `#/mapa/:proc` | Mapa estimado por grupo, item e órgão, com a origem de cada número |
| `#/resultado/:proc` | Situação dos grupos, homologado por item e por órgão, economia e edição manual com justificativa |
| `#/empresas/:proc` | Tabela por empresa vencedora, com CNPJ, grupos e valor por órgão |
| `#/conferencia/:proc` | Divergências D01 a D09, com o que bloqueia e o que só avisa |
| `#/orcamento/:proc` | Dotação por órgão e tipo, ano corrente e ano seguinte, com a validação da chefia |
| `#/exportar/:proc` | Excel com 8 abas, relatório de divergências para impressão e JSON do processo |
| `#/auditoria/:proc` | Trilha de importações, edições de valor e validações, com data e perfil |

Os totais do exemplo batem com o gabarito calculado pelo script independente:
estimado R$ 2.958.629,46, homologado R$ 917.504,89, ano corrente R$ 830.286,54
e ano seguinte R$ 87.218,35. São seis testes do motor na tela `#/testes`.

## Como construir e testar

Este app é autônomo. `nucleo/`, `construir.py` e `testes/` são só dele e não
importam nada de `Apps/_base/`, porque esta pasta vai virar um repositório
próprio no GitHub. O `index.html` é **gerado**: edite as fontes (`app.json`,
`src/`, `nucleo/`, `exemplos/seed.json`) e rode a construção.

```powershell
cd "Apps/mapa-distribuicao-credor"
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

A identidade é de ferramenta de planilha: cabeçalho compacto, fonte
monoespaçada, densidade compacta e cantos retos. A tela-assinatura é a **esteira
das 8 etapas** (Importar, Mapa, Resultado, Empresas, Conferência, Orçamentária,
Exportar e Auditoria), fixa no topo de todas as telas do processo, com a etapa
atual marcada. A tela do mapa usa a **grade em formato planilha**, com cabeçalho
fixo, subtotais e total. Código em `src/identidade.js` e `src/app.css`.

## Ajustes do feedback (03/11/2026)

- A situação do processo pode ser alterada na lista: **em andamento**, **concluído** ou **cancelado**.
- O processo guarda os **dígitos da dotação orçamentária**, mostrados no Resultado, na Distribuição e no Excel.
- A tela Empresas ganhou a tabela **Grupos e empresas**, com a empresa ganhadora, CNPJ, tipo e total homologado.
- No Mapa por item, a descrição fica justificada e grupo/item/código/unidade centralizados.
- Ainda pendentes: importar o PDF do pregoeiro e o mapa orçamentário no modelo da SESP.

## Sprint 9 · Feedback

O relatório do pregoeiro entra em PDF com camada de texto (o app avisa quando é imagem); o Exportar ganhou o **Mapa orçamentário (SESP)** com processo, órgão, tipo, dotação, credor, CNPJ e valores.

## Mapa do processo

O `processo.html` mostra o **AS-IS** (como o processo funciona antes do MVP) e o
**TO-BE** (como fica com o MVP), com as métricas, regras e papéis do projeto.
Abra ao lado do `index.html`.
