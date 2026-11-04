# Fontes de dados · desaparecidos e corpos não identificados

Atualizado em **03/11/2026**. Este documento registra o que existe para buscar
pessoas desaparecidas e corpos não identificados, o que é público, o que exige
credencial e o que já está integrado ao módulo `#/desaparecidos` do MVP.

## 1. Como o levantamento foi feito

1. **Guia Rede PCI Conecta** (`RedePCIConecta.pdf`, 454 páginas, CONDPCI/MJSP,
   2025). O modelo não lê PDF como entrada; o texto foi extraído com PyMuPDF
   para `RedePCIConecta.txt` e as páginas citadas abaixo são do PDF.
2. **Pesquisa na internet** nas páginas oficiais (CNMP, INTERPOL, NCMEC, CNPD,
   polícias estaduais, DATASUS).
3. **Teste das APIs** com `api_cnpd.py`, `coletar_dados.py` e `coletar_namus.py`
   (Scrapling).
4. **Catálogo na tela**: `dados/fontes.json`, lido pelo módulo em `#/desaparecidos`
   → aba **Fontes**.

## 2. Situação das fontes

| Fonte | Escopo | O que oferece | Acesso | Status | Onde ver |
|---|---|---|---|---|---|
| **CNPD/MJ** | Brasil | Pessoas desaparecidas: nome, idade, sexo, raça/cor, local, datas, situação | API pública do painel, sem chave, CORS aberto | **Integrada** | <https://cnpd.mj.gov.br/painel-publico> |
| **NamUs (NIJ)** | EUA | Pessoas desaparecidas e corpos não identificados, com coordenadas públicas | API pública usada pelo site (não documentada) | **Integrada (amostra)** | <https://www.namus.gov/MissingPersons/Search> |
| **INTERPOL Yellow Notices** | Internacional | Alertas globais de desaparecidos, inclusive menores e pessoas sem identificação | API pública não documentada; até 160 por consulta; sem coordenadas | Pesquisada, pronta para integrar | <https://ws-public.interpol.int/notices/v1/yellow> |
| **NCMEC** | EUA | Crianças desaparecidas, pôsteres e casos não identificados de crianças | API com cadastro em `posterapi.ncmec.org`; busca/mapa públicos; atualização horária | Pesquisada | <https://www.missingkids.org/search> |
| **SINALID/CNMP** | Brasil | Pessoas desaparecidas e localizadas, integrando os MPs estaduais | Credenciais concedidas pelos PLIDs; sistema em `apps.mprj.mp.br/sinalid` | Restrita | <https://cnmp.mp.br/portal/institucional/comissoes/comissao-de-defesa-dos-direitos-fundamentais/sinalid/informacoes-sobre-o-sistema> |
| **CADÊ (INI/PF)** | Brasil | Cadastro biométrico de pessoas desaparecidas para confronto de digitais | Interno, Instituto Nacional de Identificação da PF | Restrita | <https://www.gov.br/pf/pt-br> |
| **SINESP** | Brasil | Ocorrências, boletins e estatísticas de segurança pública | Institucional; painel estatístico público com recortes agregados | Restrita | <https://www.gov.br/mj/pt-br/assuntos/sua-seguranca/seguranca-publica/sinesp> |
| **SIM/DATASUS** | Brasil | Mortalidade, inclusive óbitos de pessoas não identificadas, por município e causa | Dados abertos no DATASUS | Pesquisada | <https://datasus.saude.gov.br/transferencia-de-arquivos/> |
| **RIBPG/CODIS** | Brasil | Perfis genéticos de desaparecidos e familiares | Institucional; 23 bancos estaduais + banco nacional | Restrita | <https://www.gov.br/pf/pt-br> |
| **SINAB/BNPB** | Brasil | Perfis balísticos | Institucional | Restrita | <https://www.gov.br/pf/pt-br> |
| **Atena** | Mato Grosso | Entrada do corpo, necropsia e laudos do IML | Interno POLITEC/MT | Restrita | — |
| **Cad-PCIConecta** | Brasil | Cadastro nacional proposto para integrar desaparecidos, corpos e exames | Em implantação pela Rede PCI Conecta/CONDPCI | Planejada | <https://www.gov.br/mj/pt-br/acesso-a-informacao/acoes-e-programas/desaparecidos/livro-rede-pciconecta-publicado-251206.pdf> |
| **PLIDs estaduais** | Brasil | Programas de localização e identificação nos MPs estaduais | Páginas públicas por estado; os registros vão para o SINALID | Pesquisada | <https://www.mpam.mp.br/plids-das-outras-unidades-da-federacao> |
| **Portais estaduais** | Brasil | Listas mantidas por Polícias Civil/Militar e prefeituras | HTML; coleta caso a caso | Pesquisada | SC: <https://www.pm.sc.gov.br/sos-desaparecidos> · BA: <https://www.ba.gov.br/policiacivil/652/pessoas-desaparecidas> · Osasco: <https://desaparecidos.osasco.sp.gov.br/> |
| **Desaparecidos do Brasil** | Brasil | Cadastro de associação civil desde 1997 | HTML; consulta e cadastro públicos | Pesquisada | <https://desaparecidosdobrasil.org/> |
| **Doe Network** | Internacional | Casos de desaparecidos e não identificados, com fichas e reconstruções faciais | HTML público | Pesquisada | <https://www.doenetwork.org/> |
| **Desaparecidos BR** | Brasil | Interface não oficial que consulta o painel do CNPD | Usa a mesma API do CNPD | Referência | <https://www.desaparecidosbr.org/> |
| **Rede PCI Conecta (guia)** | Brasil | Guia de serviços e manual de implementação da rede nacional | PDF público do MJSP/CONDPCI | Referência | <https://www.gov.br/mj/pt-br/acesso-a-informacao/acoes-e-programas/desaparecidos/livro-rede-pciconecta-publicado-251206.pdf> |

## 3. O que está integrado

### 3.1 CNPD/MJ

- **Endpoint**: `POST https://cnpd.mj.gov.br/api/api/painel-publico/desaparecidos/filtrar?ordenacao=MAIS_RECENTE&pagina=0`
- **Corpo**: `{"nome":""}`; aceita os filtros descritos em `ANALISE-API-CNPD.md`.
- **Resposta**: `{desaparecidos, totalRegistros, totalPaginas, paginaAtual, tamanhoPagina}`.
- **Foto**: `GET /api/desaparecimentos/{id}/arquivos-imagem/main` (JSON com base64).
- **Coleta**: `coletar_dados.py` → `dados/cnpd-snapshot.json` → **381 registros** em
  13 páginas, 16 UFs, em 03/11/2026.
- **Cuidado**: é um recorte público, não o total nacional. Raça/cor vem vazia em
  380 de 381; todos estavam como `NAO_CONFIRMADO`.

### 3.2 NamUs (EUA)

- **Busca** (payload do próprio site):
  ```json
  {
    "predicates": [],
    "take": 100,
    "skip": 0,
    "projections": ["idFormatted","dateOfLastContact","lastName","firstName",
      "computedMissingMinAge","computedMissingMaxAge","cityOfLastContact",
      "countyDisplayNameOfLastContact","stateDisplayNameOfLastContact","gender",
      "raceEthnicity","modifiedDateTime","namus2Number"],
    "orderSpecifications": [{"field":"dateOfLastContact","direction":"Descending"}],
    "documentFragments": ["birthDate"]
  }
  ```
- **Detalhe**: `GET https://www.namus.gov/api/CaseSets/NamUs/MissingPersons/Cases/{id}`.
- **Coordenadas**: `sighting.publicGeolocation.coordinates` (lat/lon).
- **Coleta**: `coletar_namus.py --limite 300` com **Scrapling** → `dados/namus-snapshot.json`.
- **Amostra**: 300 dos 26.607 publicados, os mais recentes por data do último
  contato; todos com coordenada. Florida concentra 165; não representa os EUA.
- **Cuidado**: os campos `raceEthnicity`/`primaryEthnicity` são etnia, não raça no
  sentido do CNPD.

## 4. O que é restrito e por quê

| Fonte | Por que não foi coletada | O que fazer |
|---|---|---|
| SINALID | Exige credencial concedida pelo PLID estadual; os dados não são públicos | Pedir credencial ao MP estadual/CNMP; usar o painel BI agregado para números |
| CADÊ | Sistema interno da PF/INI | Acordo de cooperação institucional |
| SINESP | Microdados institucionais; o painel público é agregado | Usar o painel para estatísticas; pedir acesso para microdados |
| RIBPG/CODIS | Perfis genéticos sob sigilo | Integração via acordo com a PF/RIBPG |
| SINAB/BNPB | Perfis balísticos sob sigilo | Integração via acordo com a PF |
| Atena | Sistema interno da POLITEC/MT | Integração na fase 2 do NIHDE, com a direção |

## 5. Próximas integrações sugeridas

1. **INTERPOL Yellow Notices** (esforço baixo, impacto internacional)
   - API JSON pública; sem coordenadas; 160 por consulta.
   - Normalizar país, nome, idade, data e link; no mapa, agrupar por país.
2. **NCMEC** (esforço médio, depende de cadastro)
   - Solicitar credencial da Poster API; atualização horária.
   - Foco em crianças e adolescentes desaparecidos.
3. **Portais estaduais e PLIDs** (esforço médio/alto, caso a caso)
   - Começar por SC (336 registros), BA e Osasco (58).
   - Cada portal tem HTML e campos próprios; usar Scrapling e um normalizador
     por fonte.
4. **SIM/DATASUS** (esforço médio, alto valor para o NIHDE)
   - Série de óbitos não identificados por município/ano.
   - Cruzar com os corpos do NIHDE para dimensionar o sepultamento sem identificação.
5. **Fontes restritas** (esforço institucional)
   - SINALID/CADÊ/SINESP/RIBPG/SINAB/Atena somente com termo de cooperação.
   - O guia Rede PCI Conecta (p. 88-104, 158-173) descreve a governança e os
     fluxos que justificam o pedido.

## 6. Referências do guia Rede PCI Conecta

| Tema | Páginas do PDF |
|---|---|
| Papel dos sistemas, cadastros e integração | 88-104 |
| SINALID e sistemas complementares | 49 |
| CADÊ e papiloscopia | 35 |
| CNPD e Lei 13.812/2019 | 27-29, 43-48, 88-92 |
| RIBPG/CODIS e SINAB/BNPB | 29, 64 |
| Cad-PCIConecta e governança da Rede | 90, 136-141, 158-173 |
| INTERPOL, DVI e redes internacionais | 41, 62-70, 84-85 |
| Fluxos internos e exames | 195-217 |
| Busca ativa e identificação | 203-217 |

## 7. Cuidados de uso

- Dados pessoais públicos: usar apenas para busca, localização e identificação.
  Não fazer contato com famílias, não cruzar nomes fora da finalidade e não
  divulgar foto fora do contexto (LGPD).
- Respeitar os termos e o volume dos serviços: o CNPD é uma API pública sem
  autenticação; o NamUs é uma API usada pelo site. A coleta é uma amostra e
  espera entre requisições.
- Toda exportação deve citar a fonte, a data da coleta e o recorte (por exemplo,
  "CNPD/MJ, 381 registros, 03/11/2026").
- O catálogo da tela é estático (`dados/fontes.json`); ao integrar uma fonte nova,
  atualize o JSON, o `README` e este documento.
