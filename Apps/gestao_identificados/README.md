# NIHDE · Gestão de Identificados

Registro único dos corpos **não identificados** e dos **identificados não
reclamados**: entrada, características físicas, quatro exames de identificação
(necropapiloscopia, DNA, odontologia e antropologia), família, sepultamento pelo
município, identificação depois do sepultamento e relatório.

Além do MVP, a pasta tem o módulo **`#/desaparecidos`**, que lê os dados
públicos do CNPD/MJ e do NamUs (EUA), plota no mapa e cataloga as fontes de
busca e identificação. A rota é restrita aos perfis **`nihde`** e **`gestor`**
(ver `docs/CONTRATO-DESAPARECIDOS.md`). O estado do trabalho e o que falta estão
em `CONTINUAR.md`; o catálogo de fontes, em `FONTES.md`; a parte técnica, em
`MODULO-DESAPARECIDOS.md`.

| Campo | Valor |
|---|---|
| Aluna | Kesia Melo |
| Contato | nih@politec.mt.gov.br |
| Unidade | NIHDE · Núcleo de Identificação Humana e Desaparecidos |
| Tipo | Aplicativo web / portal |
| Stack | HTML único, IndexedDB, GitHub Pages |
| Fonte | `envio-original.json` e cinco áudios de 03/11/2026 |

## Arquivos

- `envio-original.json`: o envio da aluna, sem alteração.
- `TRANSCRICAO.md` e `TRANSCRICAO-GEMINI.md`: os áudios.
- `CONTEXTO-AUDIOS.md`: o que os áudios acrescentam ao envio.
- `PROJETO.md`, `contexto.md` e `sprint.md`: o projeto completado, a arquitetura
  e o plano.
- `app.json`, `src/app.js`, `exemplos/seed.json`, `index.html`: o app.
- `modelos/roteiro-aceite.md`: o roteiro do piloto.
- `src/desaparecidos.js`, `src/app.css`, `vendor/leaflet.js`: o módulo de
  desaparecidos e o mapa Leaflet.
- `dados/`: snapshots do CNPD e do NamUs, catálogo de fontes, malhas e
  municípios (ver `dados/README.md`).
- `coletar_dados.py`, `api_cnpd.py`, `coletar_namus.py`, `preparar_mapa.py`: a
  coleta e a preparação dos dados do módulo.
- `ANALISE-API-CNPD.md`, `FONTES.md`, `MODULO-DESAPARECIDOS.md`, `CONTINUAR.md`:
  a análise da API, as fontes, a documentação técnica e a continuidade.

## O que o MVP responde

**Quantos corpos não identificados a POLITEC tem, sepultados ou não?** O painel
mostra o total, por unidade e por situação; a ficha mostra os exames, a
identificação, a família, o sepultamento e a auditoria.

**O que já se sabe sobre os desaparecidos?** O módulo `#/desaparecidos` mostra
381 registros do CNPD, 300 do NamUs e 18 fontes catalogadas, com mapa, filtros,
CSV e link para o cadastro oficial.

## Como construir e testar

```powershell
cd "Apps/gestao_identificados"
python exemplos/gerar_exemplos.py   # 24 corpos fictícios, semente fixa
python construir.py                 # gera o index.html
python testes/testar.py             # estrutura, zero rede, #/testes, rotas e tema
python testes/cenarios.py           # 4 cenários: painel, entrada, relatório e desaparecidos
```

Para atualizar os dados do módulo de desaparecidos:

```powershell
python coletar_dados.py               # CNPD: 381 registros
python coletar_namus.py --limite 300  # NamUs: amostra com Scrapling
python preparar_mapa.py               # malhas e municípios do mapa
python construir.py                   # reembute os dados no index.html
```

O `index.html` é gerado; não edite. O `gerar_painel.py` gera um painel
standalone (`desaparecidos.html`) a partir de `painel/template.html` e não
sobrescreve o MVP.

## Pendências

O plano completo, com prioridades e comandos, está em **`CONTINUAR.md`**.

- Confirmar com a Kesia e a direção da POLITEC o nome oficial (NIHDE), o escopo
  dos dados físicos no MVP e a integração com o Atena.
- O login por matrícula é simulado; a autenticação real depende da TI.
- O piloto de 90 dias no IML de Cuiabá depende do aceite da chefia.
- A lista mostra iniciais; nome da família e local do sepultamento exigem acesso
  restrito na versão institucional (LGPD).
- No módulo de desaparecidos: integrar INTERPOL, NCMEC e portais estaduais;
  pedir acesso a SINALID/CADÊ/SINESP/RIBPG/SINAB/Atena; e fazer o cruzamento
  CNPD ↔ corpos do NIHDE (fase 2) com revisão humana.
- Confirmar os termos de uso dos dados do CNPD e do NamUs antes de publicar.
- Coordenar o `app.json` com a outra IA que mantém o MVP para não perder a rota
  `#/desaparecidos`.
