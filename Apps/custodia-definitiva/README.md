# Custódia Definitiva · Central de Custódia de vestígios

Cadastro, classificação, endereçamento e localização de vestígios e contraprovas,
com painel de ocupação dos contêineres. As conferências físicas, a transferência
de responsabilidade e o descarte continuam com as pessoas.

| Campo | Valor |
|---|---|
| Equipe | Edjane Ávila |
| Contato | edjanegasparini@politec.mt.gov.br |
| Unidade | Gerência de Custódia Definitiva |
| Tipo | Mapeamento de processo (fluxo, BPMN ou Mermaid) |
| Stack | HTML único (CSS/JS inline), IndexedDB, GitHub Pages |
| Fonte | `Aula 8/Entregas/Adequao-da-custdia-definitiva-...-2026-10-27 (1).json` (29/10/2026 11:39) |
| GitHub | `edjaneavila-cyber` (Edjane) |

## Arquivos

- `envio-original.json`: o envio, sem alteração.
- `projeto.json` e `PROJETO.md`: o envio completado (sem campos vazios no envio original).
- `contexto.md` e `sprint.md`: arquitetura e plano de construção.
- `app.json`, `src/app.js`, `exemplos/`, `index.html`.

## Pendências

- Conferir as categorias, as condições de conservação e as capacidades dos
  contêineres com a equipe da custódia (o exemplo é uma proposta).
- Medir a linha de base real (volume mensal, tempo de recebimento, localização e
  movimentação); depende de autorização e de dados do Atena.
- O gerador de mapas, a projeção de ocupação e o descarte assistido ficam para os
  Sprints 3 a 5.

## Como construir e testar

Este app é autônomo. `nucleo/`, `construir.py` e `testes/` são só dele e não
importam nada de `Apps/_base/`, porque esta pasta vai virar um repositório
próprio no GitHub. O `index.html` é **gerado**: edite as fontes (`app.json`,
`src/`, `nucleo/`, `exemplos/seed.json`) e rode a construção.

```powershell
cd "Apps/custodia-definitiva"
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
