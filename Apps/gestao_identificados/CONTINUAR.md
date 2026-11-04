# NIHDE · continuidade do trabalho

Atualizado em **03/11/2026**. Este é o ponto de entrada para quem continuar. O
MVP do NIHDE já existia nesta pasta (feito por outra IA); o trabalho descrito
aqui **acrescentou um módulo de desaparecidos** sem reescrever as telas do MVP.

## 1. Resumo

| Item | Estado |
|---|---|
| MVP do NIHDE | Intacto: `#/painel`, `#/corpos`, `#/corpo/novo`, `#/corpo/:id`, `#/relatorio`, `#/config` |
| Módulo novo | `#/desaparecidos`: CNPD (Brasil), NamUs (EUA), mapa Leaflet e catálogo de fontes |
| Dados | CNPD: **381** registros; NamUs: **300 de 26.607** (amostra); catálogo: **18 fontes** |
| Mapa | Leaflet 1.9.4 embutido, sem tiles, fundo com malha do IBGE/EUA; clique no círculo abre a lista **abaixo** do mapa |
| Testes | `testar.py` **OK**; `cenarios.py` **4/4** (20 verificações); `#/testes` **12/12**; zero requisição de rede |
| Build | `index.html` com **736 KB**, 7 rotas |

## 2. O que foi feito

### 2.1 Análise da API do CNPD

- Descoberta a API do painel público do CNPD/MJ:
  - `POST https://cnpd.mj.gov.br/api/api/painel-publico/desaparecidos/filtrar?ordenacao=...&pagina=N`
  - `GET  https://cnpd.mj.gov.br/api/api/painel-publico/desaparecidos/{id}`
  - `GET  https://cnpd.mj.gov.br/api/desaparecimentos/{id}/arquivos-imagem/main`
- Sem autenticação, com `Access-Control-Allow-Origin: *`.
- Filtros mapeados: `nome`, `sexo`, `racaCor`, `estado`, `municipio`,
  `idadeAtual`, `idadeDesaparecimento`, `faixaEtariaAtualDe/Ate`,
  `faixaEtariaDesaparecimentoDe/Ate`, `anoRegistro`, `mesRegistro`.
- Ordenações: `MAIS_RECENTE`, `MAIS_ANTIGO`, `NOME_ASC`, `NOME_DESC`.
- Paginação fixa de 30; o painel devolveu 381 registros em 13 páginas, 16 UFs.
- O site `desaparecidosbr.org` é um front que usa a mesma API do CNPD.
- A análise completa está em `ANALISE-API-CNPD.md`.

### 2.2 Cliente e coleta do CNPD

- `api_cnpd.py`: cliente Python tipado (`CnpdClient`, `Pessoa`, `Pagina`) com
  `filtrar`, `obter`, `imagem`, `todas`, além de CLI.
- `coletar_dados.py`: percorre as páginas e grava `dados/cnpd-snapshot.json`.
- Snapshot de 03/11/2026: **381 registros**, 13 páginas, 16 UFs; cobertura de
  coordenadas 381/381 nos municípios do mapa.

### 2.3 Guia Rede PCI Conecta (PDF)

- O modelo não lê PDF como entrada; o texto foi extraído com PyMuPDF para
  `RedePCIConecta.txt` (454 páginas, ~1,4 MB).
- Foram levantados os sistemas e fontes do guia: CNPD, SINALID, CADÊ, SINESP,
  SIM, RIBPG/CODIS, SINAB/BNPB, Atena, Cad-PCIConecta, INTERPOL, PLIDs e a
  própria Rede PCI Conecta.
- O catálogo virou `FONTES.md` e `dados/fontes.json`.

### 2.4 NamUs (EUA) com Scrapling

- `coletar_namus.py` usa **Scrapling** (`Fetcher`) para chamar a API que o site
  do NamUs usa:
  - `POST /api/CaseSets/NamUs/MissingPersons/Search`
  - `GET  /api/CaseSets/NamUs/MissingPersons/Cases/{id}`
- Amostra de **300 casos mais recentes** de **26.607** publicados, todos com
  coordenadas públicas (`sighting.publicGeolocation.coordinates`).
- Campos normalizados para o mesmo formato do CNPD: nome, idade, sexo, raça/etnia,
  local, UF/estado, datas, situação, latitude, longitude, URL.
- Snapshot em `dados/namus-snapshot.json`. A amostra é intencional: 26 mil
  detalhes seriam pesados para o HTML offline e para o serviço.

### 2.5 Módulo no MVP

- Rota nova em `app.json`: `#/desaparecidos`, título **Desaparecidos**, sprint 5
  (módulo extra, não é o piloto). A rota é restrita aos perfis **`nihde`** e
  **`gestor`**, conforme o contrato em `docs/CONTRATO-DESAPARECIDOS.md`.
- `src/desaparecidos.js`:
  - abas **CNPD · Brasil**, **NamUs · EUA** e **Fontes**;
  - KPIs (registros, mulheres, crianças/adolescentes, idosos, UFs/estados,
    últimos 30 dias);
  - filtros por nome, UF/estado, sexo, faixa etária e ordenação;
  - tabela com link para o cadastro oficial;
  - CSV do recorte com BOM;
  - catálogo das 18 fontes, com status (integrada, pesquisada, restrita,
    planejada, referência) e link.
- Mapa:
  - Leaflet 1.9.4 embutido (`vendor/leaflet.js`), CSS em `src/app.css`;
  - fundo com malha das UFs do Brasil (IBGE) e dos EUA (US Census/PublicaMundi);
  - **sem tiles de rua** e sem rede (a CSP do MVP é `connect-src 'none'`);
  - círculos por localidade (CNPD: centroide do município; NamUs: coordenada do
    caso);
  - o clique no círculo **não abre popup dentro do mapa**: abre um painel de
    detalhe abaixo do mapa. Isso corrigiu o problema do card que aparecia
    atrás do mapa/controles. O tooltip do hover continua sobre o círculo.
- `app.json` ganhou `libs: ["leaflet.js"]` e os dados embutidos:
  `cnpd`, `namus`, `fontes`, `brasil_ufs`, `municipios_cnpd`, `eua_ufs`.
- `src/app.css`: Leaflet + estilos do módulo.
- `vendor/leaflet.js` e `vendor/leaflet.css` (1.9.4), com SHA-256 em
  `vendor/VERSOES.md`.
- `coletar_namus.py`, `preparar_mapa.py` e `dados/fontes.json`.

### 2.6 Mapa: malhas e municípios

- `preparar_mapa.py` lê `dados/fontes/municipios.csv` (kelvins/Municipios-Brasileiros,
  MIT) e `dados/fontes/brasil-ufs-ibge.geojson` (IBGE), gera:
  - `dados/municipios-cnpd.json` (só os 90 municípios do snapshot);
  - `dados/brasil-ufs.geojson` (27 UFs);
  - `dados/eua-ufs.geojson` (51 estados, via PublicaMundi/US Census);
  - `dados/municipios-br.json` e `dados/ufs-centroides.json` (fontes completas,
    usadas pelo painel standalone/preview).
- Cobertura conferida: **381/381** registros do CNPD com coordenada.

### 2.7 Testes

- `python construir.py` gera `index.html` (736 KB, 7 rotas).
- `python testes/testar.py` → **OK** (zero rede, `#/testes` 100%, rotas,
  persistência, tema, celular sem rolagem horizontal).
- `python testes/cenarios.py` → **4/4**:
  - `s1_painel_e_identificacao` (7)
  - `s2_entrada_duplicada_e_sepultamento` (5)
  - `s3_relatorio_e_csv` (2)
  - `s4_desaparecidos_e_fontes` (6) — novo
- `#/testes` embutido: **12/12**.
- Playwright manual: CNPD 381; filtro AL 151; NamUs 300 com 132 localidades;
  fontes 18; mapa com 90 círculos; celular 390 px sem rolagem horizontal; zero
  requisição de rede; zero erro no console.

### 2.8 Documentação

- `docs/CONTRATO-DESAPARECIDOS.md`: fronteira entre o app do NIHDE e o módulo,
  atualizada com a rota restrita, os arquivos reais e o teste.
- `ANALISE-API-CNPD.md`: endpoints, filtros, campos, paginação, CORS, limites.
- `FONTES.md`: catálogo e pesquisa das fontes (PDF + internet).
- `MODULO-DESAPARECIDOS.md`: arquitetura do módulo, dados, mapa e como mexer.
- `dados/README.md`: o que é cada arquivo de dados e como regerar.
- `vendor/VERSOES.md`: Leaflet e malhas, versões, licenças e SHA-256.
- Este `CONTINUAR.md`.

## 3. Como abrir, construir e testar

```powershell
cd "Apps/gestao_identificados"
python construir.py                 # gera o index.html (não edite o index.html)
python testes/testar.py             # estrutura, zero rede, rotas, tema, celular
python testes/cenarios.py           # 4 cenários de interface
```

Para atualizar os dados:

```powershell
python coletar_dados.py             # CNPD: 13 páginas, 381 registros
python coletar_namus.py --limite 300  # NamUs: amostra com Scrapling
python preparar_mapa.py             # malhas e municípios do mapa
python construir.py                 # reembute os dados no index.html
```

O painel standalone (fora do MVP) é gerado por:

```powershell
python gerar_painel.py              # gera painel/desaparecidos.html
```

O `index.html` do MVP é gerado pelo `construir.py`; **não edite o `index.html`**.
O `gerar_painel.py` grava `desaparecidos.html` e não sobrescreve o MVP.

## 4. O que falta fazer

### Prioridade 0 (fechar o módulo)

- [ ] Revisar o módulo com a Kesia/NIHDE e a direção da POLITEC: o recorte do
      CNPD e a amostra do NamUs bastam para a demonstração? O mapa e o catálogo
      respondem à pergunta da fase 2?
- [ ] Confirmar os termos de uso e a licença dos dados do NamUs e do CNPD; registrar
      a fonte e a data em cada exportação.
- [ ] Coordenar com a outra IA que mantém o MVP: o `app.json` é compartilhado.
      Se ela reescrever o arquivo, a rota `#/desaparecidos`, `libs` e `dados`
      podem sumir. Preservar as entradas ao rodar o `construir.py`. O contrato
      `docs/CONTRATO-DESAPARECIDOS.md` foi atualizado em 03/11/2026 com a rota, os
      arquivos de dados reais e o cenário de teste.
- [ ] Revisar acessibilidade do mapa: os `circleMarker` do Leaflet não recebem
      foco por teclado. A tabela abaixo do mapa é a alternativa; avaliar uma
      lista de localidades focável ou um `tabindex` nos círculos.
- [ ] Adicionar ao `testes/cenarios.py` um caso de teclado/leitores de tela, se
      o aceite exigir.

### Prioridade 1 (mais fontes)

- [ ] **INTERPOL Yellow Notices**: a API pública `https://ws-public.interpol.int/notices/v1/yellow`
      devolve JSON, sem coordenadas e com limite de 160 por consulta. Integrar
      como terceira fonte (tabela; mapa por país, não por cidade).
- [ ] **NCMEC**: a `posterapi.ncmec.org` exige cadastro/credencial. Solicitar
      acesso e integrar crianças desaparecidas; a atualização é horária.
- [ ] **Portais estaduais/PLIDs**: começar por SC (SOS Desaparecidos, 336
      registros), BA (PC) e Osasco (58 registros municipais); usar Scrapling e
      normalizar para o mesmo schema. Cada estado tem campos e regras próprios.
- [ ] **SIM/DATASUS**: baixar os microdados de mortalidade e montar a série de
      óbitos não identificados por município; cruzar com os corpos do NIHDE.
- [ ] **SINALID, CADÊ, SINESP, RIBPG/CODIS, SINAB/BNPB e Atena**: são restritos.
      Pedir credencial/termo de cooperação; não tentar burlar o acesso. O guia
      Rede PCI Conecta descreve o papel de cada um.

### Prioridade 2 (produto e operação)

- [ ] Cruzamento **CNPD ↔ corpos não identificados do NIHDE** (fase 2):
      candidatos por sexo, faixa etária, janela de datas e distância; fila de
      revisão humana; registro da decisão; nunca identificação automática.
- [ ] Fotos: hoje não são baixadas (a CSP bloqueia imagem externa e o volume
      seria grande). Avaliar miniaturas opcionais em modo online ou um recorte
      com consentimento.
- [ ] Coleta completa do NamUs (26.607) somente se houver necessidade e
      autorização; a amostra atual é dos 300 mais recentes e concentra FL (165).
- [ ] Atualização agendada (diária/semanal), com hash, contagem e diff; registrar
      a data da coleta na tela e no CSV.
- [ ] Relatório consolidado CNPD + NamUs + NIHDE, com totais por UF/estado e
      pendências de identificação.
- [ ] Revisão de LGPD: base legal, finalidade, retenção, acesso por perfil,
      auditoria de consulta e anonimização no que não for necessário.

## 5. Limitações conhecidas

- **CNPD**: o painel público devolve um recorte (381 registros, 16 UFs), não o
  total nacional; raça/cor vem vazia em 380 de 381; todos os registros estavam
  como `NAO_CONFIRMADO` na coleta. As fotos são externas e não entram no app.
- **NamUs**: amostra de 300 dos 26.607, ordenada pelos casos mais recentes;
  Florida concentra 165. Não representa os EUA. O campo `racaCor` guarda a
  etnia do NamUs (`Hispanic / Latino` etc.), não a raça no sentido do CNPD.
- **Mapa**: sem tiles de rua; fundo estático das UFs. CNPD usa o centroide do
  município; NamUs usa a coordenada pública do caso. Não há geocodificação de
  endereço nem busca por raio.
- **Fontes restritas**: SINALID, CADÊ, SINESP, RIBPG, SINAB e Atena não foram
  coletados; o catálogo apenas registra o acesso e o papel de cada um.
- **Outra IA no MVP**: as telas e o `app.json` podem mudar. O módulo está em
  arquivos separados (`src/desaparecidos.js`, `src/app.css`) e dados embutidos;
  a integração depende de 3 entradas no `app.json`.
- **PDF**: o modelo não lê PDF; o texto foi extraído para `RedePCIConecta.txt`.
  As referências de página no catálogo são do PDF original.

## 6. Referências rápidas

- CNPD: <https://cnpd.mj.gov.br/painel-publico>
- Endpoint: `POST https://cnpd.mj.gov.br/api/api/painel-publico/desaparecidos/filtrar`
- NamUs: <https://www.namus.gov/MissingPersons/Search>
- API do NamUs: `POST https://www.namus.gov/api/CaseSets/NamUs/MissingPersons/Search`
- INTERPOL: <https://ws-public.interpol.int/notices/v1/yellow>
- NCMEC: <https://posterapi.ncmec.org/swagger/index.html>
- SINALID/CNMP: <https://cnmp.mp.br/portal/institucional/comissoes/comissao-de-defesa-dos-direitos-fundamentais/sinalid/informacoes-sobre-o-sistema>
- Rede PCI Conecta (PDF): <https://www.gov.br/mj/pt-br/acesso-a-informacao/acoes-e-programas/desaparecidos/livro-rede-pciconecta-publicado-251206.pdf>
- Lei 13.812/2019: <http://www.planalto.gov.br/ccivil_03/_Ato2019-2022/2019/Lei/L13812.htm>
