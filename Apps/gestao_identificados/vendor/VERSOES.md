# Bibliotecas e dados de terceiros

| Arquivo | Versão | Licença | SHA-256 | Origem |
|---|---|---|---|---|
| `vendor/leaflet.js` | 1.9.4 | BSD-2-Clause | `DB49D009C841F5CA34A888C96511AE936FD9F5533E90D8B2C4D57596F4E5641A` | <https://unpkg.com/leaflet@1.9.4/dist/leaflet.js> |
| `vendor/leaflet.css` | 1.9.4 | BSD-2-Clause | `A7837102824184820DFA198D1EBCD109FF6D0FF9A2672A074B9A1B4D147D04C6` | <https://unpkg.com/leaflet@1.9.4/dist/leaflet.css> |
| `dados/brasil-ufs.geojson` | malha mínima, 2026 | dados públicos do IBGE | `0D3CBB61DBAA2D44A26FAF84418EC9ADB272BA3CCFDC69CC24E8EF9F400078CC` | <https://servicodados.ibge.gov.br/api/v3/malhas/paises/BR?formato=application/vnd.geo+json&qualidade=minima&intrarregiao=UF> |
| `dados/eua-ufs.geojson` | 2016 (PublicaMundi) | dados públicos (US Census) | `748503A5469E521033C2351FF944325CBE8CEBAEFC379E434D435BDDE0D7BEE2` | <https://github.com/PublicaMundi/MappingAPI/blob/master/data/geojson/us-states.json> |
| `dados/municipios-cnpd.json` | derivado de `municipios.csv` | MIT (kelvins/Municipios-Brasileiros) | `EAF93CDAAB568EB3EB7A5DC745DB16C6B5A137437E58D3CF01EC62F1EA5F4F5B` | <https://github.com/kelvins/Municipios-Brasileiros> |

## Como é usado

- `vendor/leaflet.js` é embutido no `index.html` pelo `construir.py` (lista `libs` do `app.json`).
- `vendor/leaflet.css` é a fonte; o conteúdo foi colado no começo de `src/app.css` e é embutido no `<style>`.
- As malhas e os municípios são embutidos como `<script type="application/json">` (lista `dados` do `app.json`).
- O mapa não usa tiles de rua: o app é offline e a CSP bloqueia requisições de rede. O fundo é a malha das UFs; os pontos usam as coordenadas dos registros (NamUs) ou o centroide do município (CNPD).

## Dados que não entram no repositório

- `dados/fontes/municipios.csv` e `dados/fontes/*.geojson` são as fontes brutas usadas por `preparar_mapa.py`.
- `RedePCIConecta.pdf` e `RedePCIConecta.txt` são o guia público do CONDPCI/MJSP; o texto serve de referência para `FONTES.md`.
- As imagens de `vendor/leaflet/images/` não são usadas (o app só desenha círculos e não usa o controle de camadas padrão).
