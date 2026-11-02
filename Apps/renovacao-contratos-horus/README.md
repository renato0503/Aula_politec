# Renovação de Contratos · apoiada pelo Hórus

Painel de vencimentos com semáforo de seis faixas, cadastro de contratos e
registro do termo aditivo de prorrogação. O app avisa o fiscal; a decisão de
prorrogar continua com a gestão.

| Campo | Valor |
|---|---|
| Equipe | Rodrigo Neves Ribeiro |
| Contato | rodrigoribeiro@politec.mt.gov.br |
| Unidade | Coordenadoria de Aquisições e Contratos |
| Tipo | Mapeamento de processo (fluxo, BPMN ou Mermaid) |
| Stack | HTML único (CSS/JS inline), IndexedDB, GitHub Pages |
| Fonte | `Aula 8/Entregas/Fluxo-de-Renovao-de-Contratos--apoiado-pelo-HORUS-2026-10-29.json` (29/10/2026 11:42) |
| GitHub | `Rodrigoribeiro-cloud` (Rodrigo) |

## Arquivos

- `envio-original.json`: o envio, sem alteração.
- `projeto.json` e `PROJETO.md`: o envio completado. O documento original descreve
  o fluxo do Hórus e não define MVP; o recorte do protótipo está em `contexto.md`.
- `contexto.md` e `sprint.md`: arquitetura e plano de construção.
- `app.json`, `src/app.js`, `exemplos/`, `index.html`.

## Pendências

- Confirmar com a gestão as faixas do semáforo, o alerta padrão de 90 dias e as
  permissões de escrita (o envio não detalha a visibilidade por perfil).
- A base de dados reais de contratos não foi informada; o exemplo tem 15
  contratos fictícios.
- O envio de e-mail e a integração com o Hórus ficam fora do MVP.

## Como construir e testar

Este app é autônomo. `nucleo/`, `construir.py` e `testes/` são só dele e não
importam nada de `Apps/_base/`, porque esta pasta vai virar um repositório
próprio no GitHub. O `index.html` é **gerado**: edite as fontes (`app.json`,
`src/`, `nucleo/`, `exemplos/seed.json`) e rode a construção.

```powershell
cd "Apps/renovacao-contratos-horus"
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
