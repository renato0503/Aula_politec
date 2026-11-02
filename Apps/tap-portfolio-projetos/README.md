# TAP Digital e Portfólio de Projetos

Termo de Abertura de Projeto (TAP) guiado, com campos obrigatórios e checklist
de documentos, para a proposta chegar completa à equipe de projetos, que faz a
triagem, acompanha as pendências e mantém o Portfólio de Projetos Estratégicos.

| Campo | Valor |
|---|---|
| Aluna | Danielle Marques de Almeida Trevizan |
| Contato | daniellealmeida@politec.mt.gov.br |
| Unidade | Gestão de Projetos Estratégicos (a confirmar; o campo veio vazio) |
| Tipo | Formulário ou modelo de coleta |
| Stack pedida | HTML único, GitHub Pages (a plataforma final depende da TI) |
| Fonte | `Aula 8/Entregas/Danielle-Marques-de-Almeida-Trevizan-2026-10-27 (1).json` (29/10/2026 10:49, horário de Cuiabá) |

## Arquivos

- `envio-original.json`: o envio, sem alteração.
- `projeto.json` e `PROJETO.md`: o envio completado (ver abaixo).
- `contexto.md` e `sprint.md`: arquitetura e plano de construção.

## Pendências

- Vieram vazios o nome do projeto, a unidade e o tipo, e 10 das 12 tabelas.
- O modelo vigente do TAP e a lista oficial de documentos não vieram. Os
  campos do formulário são uma proposta até chegarem.
- A aluna pede para não escolher hospedagem pública antes da TI. O app
  funciona como arquivo, sem servidor; publicar no GitHub Pages fica para
  depois da avaliação da TI.

## Completado pelo professor (29/10/2026)

O `projeto.json` e o `PROJETO.md` desta pasta foram completados com propostas próximas do
que o aluno escreveu. O envio original está em `envio-original.json`.
Tudo o que foi completado precisa ser confirmado com o aluno no Sprint 0.

**Campos preenchidos (estavam vazios):** `nome_projeto`, `unidade`, `tipo_projeto`, `evid_detalhe`, `stack_detalhe`, `campos_data`, `base_periodo`, `lgpd_acesso`, `doc_descricao`, `doc_faltando`.

**Campos substituídos:**

- `hospedagem_escolhida`: estavam como A DEFINIR; preenchido com a solução do MVP, mantendo a decisão final com a TI.
- `conta_quem`: estavam como A DEFINIR; preenchido com a solução do MVP, mantendo a decisão final com a TI.
- `orcamento`: estavam como A DEFINIR; preenchido com a solução do MVP, mantendo a decisão final com a TI.

**Tabelas:**

- AS-IS (`tAsIs`): refeita. As colunas o que entra, o que sai, sistema e tempo estavam vazias; preenchidas a partir das entradas e saídas descritas. Tempo: não mensurado (informado).
- TO-BE (`tToBe`): refeita. A tabela veio vazia; montada a partir da visão TO-BE e da mudança principal descritas pela aluna.
- papéis (`tPapeis`): refeita. A coluna do que o sistema registra estava vazia.
- telas e artefatos (`tArtefatos`): refeita. A tabela veio vazia; as telas seguem o escopo descrito.
- entidades (`tEntidades`): refeita. A tabela veio vazia.
- regras de negócio (`tRegras`): refeita. A tabela veio vazia; as regras seguem o escopo e as restrições descritas (a automação não decide).
- fontes de dados (`tFontes`): refeita. A tabela veio vazia; fontes citadas nas lacunas.
- métricas (`tMetricas`): refeita. As três métricas estavam no campo de provas; movidas para a tabela com fórmula.
- hospedagem (`tHospedagem`): refeita. A tabela veio vazia.
- marcos (`tMarcos`): refeita. A tabela veio vazia.
- riscos (`tRiscos`): refeita. A tabela veio vazia; o primeiro risco é o da defesa da aluna.
- referências (`tRefs`): refeita. A tabela veio vazia.

**Marcações:**

- `req`: acrescentado Funcionar offline.

## Como construir e testar

Este app é autônomo. `nucleo/`, `construir.py` e `testes/` são só dele e não
importam nada de `Apps/_base/`, porque esta pasta vai virar um repositório
próprio no GitHub. O `index.html` é **gerado**: edite as fontes (`app.json`,
`src/`, `nucleo/`, `exemplos/seed.json`) e rode a construção.

```powershell
cd "Apps/tap-portfolio-projetos"
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
