# Evento de Substituição Temporária · afastamento de gestor

Abertura e acompanhamento do afastamento temporário de um gestor da POLITEC:
ofício no SIGADOC, autorização da linha hierárquica, Gabinete de Direção, ficha
de RH, assinatura do Diretor Geral Adjunto, envio à SESP e publicação no Diário
Oficial. O app controla o prazo do dia 05 e mantém a planilha de controle.

| Campo | Valor |
|---|---|
| Equipe | Simone Alem |
| Contato | a informar |
| Unidade | Gerência de Suporte à Gestão de Pessoas |
| Tipo | Aplicativo para servidor |
| Stack | HTML único (CSS/JS inline), IndexedDB, GitHub Pages |
| Fonte | `entregas/Evento de Substituição Temporária.docx` (09/11/2026) |
| GitHub | [renato0503/evento-substituicao-temporaria](https://github.com/renato0503/evento-substituicao-temporaria) |

## Arquivos

- `entregas/Evento de Substituição Temporária.docx`: o documento original, sem alteração.
- `envio-original.json`: o texto extraído do documento, bloco a bloco.
- `projeto.json` e `PROJETO.md`: a especificação completada.
- `contexto.md` e `sprint.md`: arquitetura e plano de construção.
- `app.json`, `src/app.js`, `src/identidade.js`, `src/app.css`, `exemplos/`, `index.html`.
- `vendor/xlsx.full.min.js` (SheetJS 0.18.5), embutido no `index.html` para gerar a planilha Excel.
- `processo.html` e `docs/diagramas/`: o AS-IS, o TO-BE e as figuras Mermaid.

## O que o app faz

- Abre o evento com o número do SIGADOC, a unidade, o gestor substituído, o
  substituto, o motivo e o período (RN01 e RN02).
- Cria uma autorização por nível da linha hierárquica e só leva o evento ao
  Gabinete quando todas forem concedidas (RN03).
- Deixa o Gabinete encaminhar ao RH e o RH incluir a ficha de solicitação (RN04).
- Mostra a fila de assinatura do Diretor Geral Adjunto (RN05).
- Bloqueia o envio à SESP depois do dia 05 do mês da substituição e permite o
  indeferimento com motivo (RN06).
- Só encerra o evento com o número e a data da publicação no Diário Oficial
  (RN07).
- Mantém a planilha de controle com os cinco campos obrigatórios e exporta CSV
  e Excel (`.xlsx`, abas Controle e Resumo) (RN08).
- Deixa a unidade ajustar os dados do evento devolvido antes de reenviar para a
  autorização.

## Pendências

- Confirmar com a Simone as unidades, as chefias e os níveis de cada linha
  hierárquica. As premissas estão em [`Apps/PREMISSAS.md`](../PREMISSAS.md).
- Receber o desenho oficial da ficha de solicitação de substituição temporária.
- Medir o volume mensal e o tempo de cada etapa no piloto de 30 dias.
- O SIGADOC, a assinatura digital e a publicação no Diário Oficial ficam fora do
  MVP: o app registra o evento, a etapa, o prazo e a trilha.
- O repositório público está criado; o convite de push para a Simone ainda
  depende do login do GitHub dela, e o contato precisa ser informado.

## Como construir e testar

Este app é autônomo. `nucleo/`, `construir.py` e `testes/` são só dele e não
importam nada de `Apps/_base/`, porque esta pasta vai virar um repositório
próprio no GitHub. O `index.html` é **gerado**: edite as fontes (`app.json`,
`src/`, `nucleo/`, `exemplos/seed.json`) e rode a construção.

```powershell
cd "Apps/evento-substituicao-temporaria"
python construir.py           # gera o index.html a partir de app.json, src/, nucleo/ e os dados
python testes/testar.py       # estrutura: zero rede, #/testes 100%, rotas por perfil, tema e celular
python testes/cenarios.py     # cenários dos sprints: usa a tela como uma pessoa usaria
python testes/jornada.py      # jornada do cliente no desktop e no celular
```

Antes da primeira execução: `pip install playwright` e
`playwright install chromium`.

Os dados fictícios são gerados por `exemplos/gerar_exemplos.py`; rode-o quando
mudar o esquema e confira o novo `exemplos/seed.json` no navegador.

Regras: não edite `index.html` direto; nenhum arquivo de fora da pasta do app é
importado; o tema claro é o padrão e o escuro só entra pelo botão; os textos
seguem o português do Brasil com acentuação, sem travessões.

## Identidade e usabilidade

A identidade é de gestão de pessoas: casca de trilho, cabeçalho em degradê,
fonte do sistema, densidade ampla, cantos redondos, cartões e KPI em anel, no
acento verde-petróleo. A tela-assinatura é a **Minha fila**: o que espera cada
perfil, em cartões com a etapa, o prazo do dia 05 e o link para a ficha. A ficha
do evento tem a trilha das sete etapas no alto e abas (Resumo, Tramitação, Ficha
de RH, Assinatura, Publicação e Histórico). Código em `src/identidade.js` e
`src/app.css`.

## Mapa do processo

O `processo.html` mostra o **AS-IS** (como o evento funciona antes do MVP) e o
**TO-BE** (como fica com o MVP), com as métricas, regras e papéis do projeto.
Abra ao lado do `index.html`.
