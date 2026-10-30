# Identidade visual dos apps (mídia kit)

Todos os 20 apps usam a mesma base visual, com as cores do **Governo de Mato
Grosso, da SESP/MT e da POLITEC/MT**. Além disso, cada app tem a sua
personalização: cor de acento, emblema, layout, padrão do cabeçalho e estilo.

> **Atenção**: as cores institucionais abaixo foram definidas por aproximação
> (azul institucional, dourado e verde da bandeira de MT). Não há manual de marca
> oficial no repositório. Por isso, quando o manual da SESP ou da POLITEC chegar,
> troque os valores de `--mt-*` em `Apps/_base/visual.css` e reconstrua os apps.

## 1. Onde fica cada coisa

| Arquivo | O que define |
|---|---|
| `Apps/_base/visual.css` | Paleta institucional, tema claro e escuro, cabeçalho, menu, cartões, KPIs, tabelas, selos, formulários, rodapé, impressão e os componentes dos sprints. |
| `Apps/_base/icones.js` | Os 48 ícones (traço 24x24, herdam a cor) e a regra que escolhe o ícone de cada tela pelo título. |
| `Apps/_base/base.html` | Faixa do governo, cabeçalho com emblema, botões de fonte (A−, 100%, A+) e de tema, menu, rodapé. |
| `Apps/_base/construir.py` | Lê o bloco `visual` do `app.json`, calcula as variações do acento e embute o padrão do cabeçalho. |
| `Apps/<app>/app.json` → `visual` | A personalização do app. |
| `Apps/<app>/src/app.css` | CSS próprio do app (opcional, use pouco). |

## 2. Paleta institucional (fixa)

| Variável | Cor | Uso |
|---|---|---|
| `--mt-azul-9` | `#061f3d` | Faixa do governo, fundo mais escuro do cabeçalho |
| `--mt-azul-8` | `#0a2f5c` | Cabeçalho, toast, títulos no estilo claro |
| `--mt-azul-7` | `#12487f` | Fim do degradê do cabeçalho; acento padrão |
| `--mt-azul-5` | `#1e63ae` | Quarto KPI, bandeira |
| `--mt-ouro` | `#c99a2e` | Filete da faixa, anel do emblema, segundo KPI |
| `--mt-ouro-claro` | `#e8b931` | Foco do teclado, aviso |
| `--mt-verde` | `#0b7a3e` | Terceiro KPI, fim do filete do cabeçalho |

Estados: `--verde` (ok), `--ambar` (alerta), `--vermelho` (erro). Superfícies:
`--bg`, `--painel`, `--painel-2`, `--ink`, `--ink2`, `--linha`.

O filete de 3 px no pé do cabeçalho junta as três cores: o acento do app (62%),
o dourado (24%) e o verde de MT (14%).

## 3. Tema e fonte

- **Tema claro é o padrão** em todos os apps, mesmo quando o sistema
  operacional está no escuro. O botão **Tema** troca para o escuro, e a escolha
  fica guardada por app (`localStorage`, chave `<app>:tema`).
- **Tamanho da fonte**: os botões **A−** e **A+** mudam a escala de 80% a 150%,
  em passos de 10%. O botão do meio mostra o valor e volta a 100%. A escolha fica
  guardada por app (`<app>:fonte`). A escala usa `zoom` na área `.corpo` (menu e
  conteúdo), e o cabeçalho fica no tamanho original.

## 4. Personalização por app (bloco `visual` do `app.json`)

```json
"visual": {
  "acento": "#0a5c64",
  "icone": "etiqueta",
  "layout": "lateral",
  "padrao": "pontos",
  "estilo": "institucional",
  "setor": "IML · Perícias em Mortos"
}
```

| Campo | Valores | Efeito |
|---|---|---|
| `acento` | cor hex com contraste >= 4,5:1 com o branco | Botões, menu ativo, links, barra dos títulos, emblema. O `construir.py` calcula o tom claro (emblema), o forte (hover) e o do tema escuro. Opcional: `acento_claro`, `acento_escuro`. |
| `icone` | nome de `ICONES` em `icones.js` | Emblema do cabeçalho. |
| `layout` | `lateral` ou `topo` | Menu na coluna da esquerda (apps de trabalho interno com muitas telas) ou em abas abaixo do cabeçalho. Abaixo de 900 px o lateral vira abas. |
| `padrao` | `linhas`, `pontos`, `grade`, `hexagonos`, `ondas`, `topografico` | Textura do cabeçalho. |
| `estilo` | `institucional` ou `claro` | Cabeçalho azul (servidor) ou branco (apps voltados ao cidadão). |
| `setor` | texto | Aparece à direita da faixa do governo. |

Cada tela do menu ganha ícone pelo título. Para forçar um ícone, acrescente
`"icone": "<nome>"` na rota do `app.json`.

### Tabela dos 20 apps

| App | Acento | Emblema | Layout | Padrão | Estilo | Setor |
|---|---|---|---|---|---|---|
| adiantamento | `#0b6e4f` verde | moeda | lateral | linhas | institucional | DAS · Suprimento de fundos |
| agendamento-cin | `#1559b7` azul | calendario | topo | ondas | claro | Identificação Civil · Atendimento ao cidadão |
| agiliza-mais | `#4338ca` índigo | raio | lateral | grade | institucional | Perícia de informática · Laudos |
| cin-segunda-via | `#0e7490` azul petróleo | identidade | topo | ondas | claro | Identificação Civil · Segunda via |
| comissao-etica-denuncias | `#8a1c3a` vinho | balanca | lateral | pontos | institucional | Comissão de Ética |
| controle-aquisicoes | `#b23c17` terracota | carrinho | lateral | grade | institucional | Coordenadoria de Aquisições |
| custodia-definitiva | `#3f4a5a` grafite | caixa | lateral | hexagonos | institucional | Central de Custódia Definitiva |
| distribuicao-casos-dna | `#86198f` fúcsia escuro | dna | topo | hexagonos | institucional | Biologia Molecular · DNA |
| documentapolitec | `#7c5a16` sépia | pasta | lateral | linhas | institucional | Patrimônio e Serviços · Arquivo central |
| equipamentos-google-earth | `#2f7d32` verde mata | globo | topo | topografico | institucional | Qualidade · Parque de equipamentos |
| gestao-documentos | `#2b5a8a` azul aço | carimbo | lateral | linhas | institucional | Gabinete de Direção · Protocolo |
| horus-banco-demandas | `#8f6b00` dourado | olho | lateral | pontos | institucional | Planejamento de Contratações · PCA |
| inscricoes-cursos | `#0369a1` azul céu | capelo | topo | ondas | institucional | Formação Inicial e Continuada |
| mapa-distribuicao-credor | `#047857` esmeralda | tabela | lateral | grade | institucional | Licitações · Distribuição orçamentária |
| metas-bi-ocr | `#9d174d` magenta | alvo | topo | grade | institucional | CQUAL · Monitoramento de metas |
| passivo-ambiental | `#4d7c0f` oliva | folha | topo | topografico | institucional | Interiorização · Perícia ambiental |
| renovacao-contratos-horus | `#3b4f7a` azul ardósia | contrato | lateral | linhas | institucional | Aquisições e Contratos · Renovação |
| rnc-nao-conformidade | `#b42318` vermelho | alerta | lateral | linhas | institucional | CQUAL · Qualidade |
| tap-portfolio-projetos | `#5b21b6` violeta | portfolio | topo | pontos | institucional | Escritório de Projetos Estratégicos |
| trilha-custodia-necropsia | `#0a5c64` verde petróleo (do protótipo da aluna) | etiqueta | lateral | pontos | institucional | IML · Perícias em Mortos |

## 5. Componentes (use estas classes nas telas novas)

| Classe | Para que serve |
|---|---|
| `.card`, `.card.kpi` (`.v` valor, `.r` rótulo), `.grade` | Cartões e indicadores. A barra lateral do KPI alterna acento, dourado, verde e azul. |
| `.card.tabela-wrap` + `<table>` | Tabela com cabeçalho em caixa alta e linha destacada no hover. |
| `.selo.ok / .alerta / .erro / .info` | Situação em pílula. |
| `button.prim`, `button.perigo`, `.botao` | Botões. |
| `campo(id, rotulo, {...})` + `.campos` | Formulário em grade. |
| `.busca-grande` (com `icone("busca")` e um `<input>`) | Caixa de busca principal da tela. |
| `.duas-colunas` | Dois cartões lado a lado (vira uma coluna abaixo de 980 px). |
| `ol.linha-do-tempo` com `li.ldt-ok / ldt-alerta / ldt-erro / ldt-futuro` e `.ldt-quando` | Histórico e marcos. |
| `.etapas` com `span.feita / span.atual` | Barra de etapas numeradas. |
| `.barra.ok/.alerta/.erro > i[style=width:NN%]` | Barra de ocupação ou progresso. |
| `.chips` | Botões de filtro rápido. |
| `ul.check-lista > li.feito/.falta` | Checklist com ícone. |
| `.documento-a4` com `.doc-cab` | Minuta, ofício ou laudo para imprimir (fundo branco, fonte serifada). |
| `icone("nome")` | Ícone em qualquer lugar do HTML. |
| `main > h1:first-child` | Ganha sozinho a barra vertical de acento e dourado. |

## 6. Regras

- Nunca use cor fixa nas telas: use `var(--accent)`, `var(--verde)`, `var(--ambar)`, `var(--vermelho)`, `var(--ink2)`.
- Não edite o `index.html` de um app. Edite `visual.css`, `icones.js`, `base.html` ou o `app.json` e rode `python Apps/_base/construir.py`.
- Faixa de aviso ("Protótipo, sem validade...") foi **removida a pedido** em 30/10/2026. O `construir.py` ainda aceita a chave `aviso`, mas nenhum app a usa.
- Confira as telas novas no tema claro, no escuro e com a fonte em 130%.
