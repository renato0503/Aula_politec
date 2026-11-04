# Dados do módulo de desaparecidos

Os JSON desta pasta são **retratos** de coleta, não faixas em tempo real. O
`index.html` embute esses arquivos; o app não faz requisição de rede.

| Arquivo | Fonte | Conteúdo | Tamanho | Quando usar |
|---|---|---|---|---|
| `cnpd-snapshot.json` | CNPD/MJ | 381 registros do painel público, 03/11/2026 | ~110 KB | Aba CNPD |
| `namus-snapshot.json` | NamUs/NIJ | 300 de 26.607 casos (amostra recente), 03/11/2026 | ~130 KB | Aba NamUs |
| `fontes.json` | pesquisa + guia Rede PCI Conecta | 18 fontes, status e acesso | ~7 KB | Aba Fontes |
| `brasil-ufs.geojson` | IBGE (malha mínima) | 27 UFs | ~97 KB | Fundo do mapa do Brasil |
| `eua-ufs.geojson` | PublicaMundi/US Census | 51 estados | ~72 KB | Fundo do mapa dos EUA |
| `municipios-cnpd.json` | kelvins/Municipios-Brasileiros (MIT) | 90 municípios do snapshot, com lat/lon | ~3 KB | Pontos do CNPD |
| `municipios-br.json` | kelvins/Municipios-Brasileiros (MIT) | 5.571 municípios (fonte completa) | ~180 KB | Painel/preview e futuro |
| `ufs-centroides.json` | derivado do CSV | centroides por UF | ~1 KB | Painel/preview |

## Como regerar

```powershell
cd "Apps/gestao_identificados"
python coletar_dados.py              # CNPD
python coletar_namus.py --limite 300 # NamUs (Scrapling)
python preparar_mapa.py              # malhas + municípios
python construir.py                  # reembute no index.html
```

## Fontes brutas (`dados/fontes/`)

| Arquivo | Origem |
|---|---|
| `municipios.csv` | <https://github.com/kelvins/Municipios-Brasileiros> (MIT) |
| `brasil-ufs-ibge.geojson` | <https://servicodados.ibge.gov.br/api/v3/malhas/paises/BR?formato=application/vnd.geo+json&qualidade=minima&intrarregiao=UF> |
| `us-states.geojson` | <https://github.com/PublicaMundi/MappingAPI/blob/master/data/geojson/us-states.json> |

## Cuidados

- **CNPD**: o painel devolve um recorte (381 registros, 16 UFs), não o total
  nacional; raça/cor vem vazia em 380 de 381; todos estavam `NAO_CONFIRMADO`.
- **NamUs**: amostra dos 300 mais recentes; Florida concentra 165; não representa
  os EUA. `racaCor` guarda a etnia do NamUs.
- Datas: CNPD em `dd/mm/aaaa`; NamUs em ISO (`aaaa-mm-dd`).
- Ao trocar o snapshot do CNPD, rode `preparar_mapa.py` para atualizar
  `municipios-cnpd.json`; se aparecer um município novo sem coordenada, o teste
  embutido "todo registro do CNPD tem coordenada" falha (é o aviso).
- Dados pessoais públicos: use apenas para busca e identificação (LGPD).
