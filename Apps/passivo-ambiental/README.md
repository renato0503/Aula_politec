# Passivo Ambiental · laudos por sensoriamento remoto

Controle das requisições periciais ambientais atrasadas e dos laudos, com o
cabeçalho preenchido a partir da requisição. O perito segue dando a conclusão
técnica e assinando o laudo.

| Campo | Valor |
|---|---|
| Equipe | Fábio |
| Contato | fabioconceicao@politec.mt.gov.br |
| Unidade | Diretoria de Interiorização |
| Tipo | Mapeamento de processo (fluxo, BPMN ou Mermaid) |
| Stack | HTML único (CSS/JS inline), IndexedDB, GitHub Pages |
| Fonte | `Aula 8/Entregas/Passivo-Ambiental-2026-10-27 (1).json` (29/10/2026 11:22) |
| GitHub | `fabioconceicao-fxc` (Fábio) |

## Arquivos

- `envio-original.json`: o envio, sem alteração.
- `projeto.json` e `PROJETO.md`: o envio completado (sem campos vazios).
- `contexto.md` e `sprint.md`: arquitetura e plano de construção.
- `app.json`, `src/app.js`, `exemplos/`, `index.html`.

## Pendências

- Confirmar o formato real da requisição, do modelo de laudo e dos mapas
  (a base é o envio e o manual da unidade).
- O editor de mapas com Leaflet, o gerador de PDF e a assinatura ficam para os
  Sprints 3 e 4; dependem das amostras e das bibliotecas escolhidas.
- A linha de base de 16 h por laudo precisa ser medida em 5 laudos reais.

## Como construir e testar

Este app é autônomo. `nucleo/`, `construir.py` e `testes/` são só dele e não
importam nada de `Apps/_base/`, porque esta pasta vai virar um repositório
próprio no GitHub. O `index.html` é **gerado**: edite as fontes (`app.json`,
`src/`, `nucleo/`, `exemplos/seed.json`) e rode a construção.

```powershell
cd "Apps/passivo-ambiental"
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

A identidade é de perícia de campo: casca de topo, cabeçalho em degradê, cantos
suaves e KPI em faixa. A tela-assinatura é a **fila de laudos do perito**, com o
prazo em dias e a **miniatura do mapa** de cada requisição; o painel do gestor
(produtividade) não aparece para o perito. O laudo virou abas: Cabeçalho, Mapas,
Conclusão e Assinatura. O seed passou a usar datas relativas a hoje, com duas
requisições atrasadas e as demais dentro do prazo. Código em `src/identidade.js`
e `src/app.css`.
