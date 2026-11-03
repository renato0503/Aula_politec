# Visão geral dos equipamentos no estado (Google Earth)

Cadastro de equipamentos com fotos, custos e histórico de manutenção, com
cálculo do impacto e do custo de parada por defeito, e com a localização de
cada equipamento no mapa do estado, no Google Earth.

| Campo | Valor |
|---|---|
| Aluno | João Lucas Nogueira Ponce |
| Contato | joaoponce@politec.mt.gov.br |
| Unidade | Coordenadoria de qualidade |
| Tipo | Outro |
| Plataforma | Site web (abre no navegador) |
| Fonte | `Aula 8/Entregas/...-2026-10-28 (1).json` (28/10/2026 08:44, horário de Cuiabá) |

## Arquivos

- `projeto.json`: a versão mais recente da resposta (62 campos e 12 tabelas).
  Pode ser importada no formulário para continuar a edição.
- `PROJETO.md`: o export do formulário, atualizado com os 2 campos da versão
  das 08:44 (plataforma alvo e detalhe da evidência).

## Histórico

No Firestore há 3 envios do mesmo projeto (08:24, 08:27 e 08:33). Os dois
primeiros não têm MVP, papéis nem TO-BE. Esta pasta usa a versão local das
08:44, que é posterior a todos eles.

## Pendências

- O nome do projeto foi enviado como "google heart". O resumo diz Google Earth.
- Nenhum arquivo anexado.
- O campo "dados pessoais tratados" traz um número de 11 dígitos que parece
  um CPF. Retirar no próximo envio.
- MVP, papéis, entidades, regras, telas e KPIs vieram em branco ou com "1".
  O `contexto.md` propõe o escopo, e o Sprint 0 valida com o aluno.

## Completado pelo professor (29/10/2026)

O `projeto.json` e o `PROJETO.md` desta pasta foram completados com propostas próximas do
que o aluno escreveu. O envio original está em `envio-original.json`.
Tudo o que foi completado precisa ser confirmado com o aluno no Sprint 0.

**Campos preenchidos (estavam vazios):** `evid_detalhe`, `asis_inicio`, `asis_fim`, `asis_decisoes`, `asis_excecoes`, `asis_digital`, `papeis_obs`, `tobe_visao`, `tobe_mudanca`, `tobe_inalterado`, `tobe_restricao`, `tobe_piloto`, `entrega`, `dentro`, `fora`, `dependencias`, `mvp_objetivo`, `mvp_tela_inicial`, `mvp_mock`, `mvp_criterio`, `mvp_dados`, `mvp_reuso`, `mvp_naofaz`, `coletar`, `acesso`, `base_periodo`, `campos_data`, `conta_quem`, `orcamento`, `lgpd_base`, `lgpd_retencao`, `lgpd_acesso`, `restricoes`, `hipotese_campo`, `lacunas`, `frase`, `provas`, `risco_defesa`, `doc_descricao`, `doc_faltando`.

**Campos substituídos:**

- `nome_projeto`: o texto anterior estava vazio, com erro de digitação ("google heart"), com um CPF no lugar da descrição dos dados, ou com a stack Python; alinhado ao resumo do aluno e à arquitetura do curso.
- `tipo_projeto`: o texto anterior estava vazio, com erro de digitação ("google heart"), com um CPF no lugar da descrição dos dados, ou com a stack Python; alinhado ao resumo do aluno e à arquitetura do curso.
- `stack_detalhe`: o texto anterior estava vazio, com erro de digitação ("google heart"), com um CPF no lugar da descrição dos dados, ou com a stack Python; alinhado ao resumo do aluno e à arquitetura do curso.
- `hospedagem_escolhida`: o texto anterior estava vazio, com erro de digitação ("google heart"), com um CPF no lugar da descrição dos dados, ou com a stack Python; alinhado ao resumo do aluno e à arquitetura do curso.
- `lgpd_dados`: o texto anterior estava vazio, com erro de digitação ("google heart"), com um CPF no lugar da descrição dos dados, ou com a stack Python; alinhado ao resumo do aluno e à arquitetura do curso.
- `mvp_plataforma`: o texto anterior estava vazio, com erro de digitação ("google heart"), com um CPF no lugar da descrição dos dados, ou com a stack Python; alinhado ao resumo do aluno e à arquitetura do curso.

**Tabelas:**

- AS-IS (`tAsIs`): refeita. Montado a partir do problema ("não é feito acompanhamento via ferramenta"), das entradas (comprovantes de manutenção) e do impacto informados pelo aluno.
- TO-BE (`tToBe`): refeita. Montado a partir do resumo do aluno (fotos, custos, histórico, impacto e Google Earth).
- papéis (`tPapeis`): refeita. A tabela veio com "1" em todas as células.
- telas e artefatos (`tArtefatos`): refeita. A tabela veio com "1"; as telas seguem o `contexto.md`.
- entidades (`tEntidades`): refeita. A tabela veio com "1"; as entidades seguem o `contexto.md`, seção 5.
- regras de negócio (`tRegras`): refeita. A tabela veio com "1"; as regras seguem o `contexto.md`, seção 6.
- fontes de dados (`tFontes`): refeita. A tabela veio com "1".
- métricas (`tMetricas`): refeita. A tabela veio com "1".
- hospedagem (`tHospedagem`): refeita. A tabela veio com "1".
- marcos (`tMarcos`): refeita. A tabela veio com "1"; as datas seguem os sprints de 1 semana do `sprint.md`.
- riscos (`tRiscos`): refeita. A tabela veio com "1".
- referências (`tRefs`): refeita. A tabela veio com "1".

**Marcações:**

- `stack`: era Python/Flask; alinhado à arquitetura do curso.
- `req`: mantida Acessibilidade; acrescentados Funcionar offline e Impressão (relatório A4).
- `evid`: acrescentada a planilha parcial citada pelo aluno.

## Telas prontas (03/11/2026)

| Rota | O que faz |
|---|---|
| `#/mapa` | Mapa de MT com os 142 municípios, pinos por unidade e legenda |
| `#/unidades` | Diretorias e unidades, com município e coordenadas (RN08) |
| `#/equipamentos` | Lista com busca, filtros e paginação de 25 em 25 |
| `#/equipamento/:id` | Ficha com fotos, contrato, histórico de manutenção, paradas, MTTR e custo |
| `#/contratos` | Contratos, cobertura, vencimento e alerta de 60 dias (RN05) |
| `#/paradas` | Abertura e fechamento de paradas, com custo diário (RN02) e acumulado (RN03) |
| `#/painel` | Os 7 indicadores do projeto, ranking por custo de parada e pontos únicos de falha sem contrato |
| `#/exportar` | KML e `.kmz` para o Google Earth, JSON da base, CSV e relatório |
| `#/importar` | Planilha em CSV com relatório de aceitas e recusadas, e mesclagem do `.json` da unidade (RN10) |

Sete cenários de interface cobrem os Sprints 2 a 9.

## Como construir e testar

Este app é autônomo. `nucleo/`, `construir.py` e `testes/` são só dele e não
importam nada de `Apps/_base/`, porque esta pasta vai virar um repositório
próprio no GitHub. O `index.html` é **gerado**: edite as fontes (`app.json`,
`src/`, `nucleo/`, `exemplos/seed.json`) e rode a construção.

```powershell
cd "Apps/equipamentos-google-earth"
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

A identidade é de ferramenta de campo: cabeçalho compacto, fonte do sistema,
densidade compacta e cantos suaves. A tela-assinatura é o **mapa de MT em SVG**,
com os 142 municípios do arquivo `dados-base/mt-municipios.json` e os pinos das
unidades; o número no pino é a quantidade de equipamentos e o clique abre a lista
filtrada. O perfil Unidade ganhou o **contexto de unidade** no menu do perfil.
Código em `src/identidade.js` e `src/app.css`.

## Mapa do processo

O `processo.html` mostra o **AS-IS** (como o processo funciona antes do MVP) e o
**TO-BE** (como fica com o MVP), com as métricas, regras e papéis do projeto.
Abra ao lado do `index.html`.
