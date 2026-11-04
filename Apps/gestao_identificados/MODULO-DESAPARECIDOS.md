# Módulo Desaparecidos · documentação técnica

Rota: **`#/desaparecidos`** · arquivo principal: **`src/desaparecidos.js`**
Entrou no MVP como módulo extra (sprint 5) em **03/11/2026**. Acesso restrito aos
perfis **`nihde`** e **`gestor`** (o perfil `iml` não vê no menu), conforme
`docs/CONTRATO-DESAPARECIDOS.md`.

## 1. Visão geral

O módulo lê dois retratos de dados públicos coletados fora do app e os apresenta
em três abas:

| Aba | Fonte | Registros | O que mostra |
|---|---|---|---|
| CNPD · Brasil | CNPD/MJ | 381 (recorte de 03/11/2026) | KPIs, filtros, mapa por município, tabela, CSV |
| NamUs · EUA | NamUs/NIJ | 300 de 26.607 (amostra) | KPIs, filtros, mapa por coordenada, tabela, CSV |
| Fontes | catálogo | 18 fontes | status, acesso, link e o que falta |

O app é offline e a CSP do MVP é `connect-src 'none'`. Nada é buscado em tempo
de execução: os JSON são embutidos no `index.html` pelo `construir.py`. O mapa
não usa tiles; o fundo é a malha das UFs embutida.

## 2. Arquivos

| Arquivo | Papel |
|---|---|
| `app.json` | rota `#/desaparecidos`, `libs: ["leaflet.js"]` e a lista `dados` |
| `src/desaparecidos.js` | tela, filtros, KPIs, mapa, CSV, catálogo e testes embutidos |
| `src/app.css` | CSS do Leaflet (copiado de `vendor/leaflet.css`) + estilos do módulo |
| `vendor/leaflet.js` | Leaflet 1.9.4 (embutido no HTML pelo `construir.py`) |
| `vendor/leaflet.css` | fonte do CSS do Leaflet |
| `vendor/VERSOES.md` | versões, licenças e SHA-256 |
| `coletar_namus.py` | coleta o NamUs com Scrapling |
| `coletar_dados.py` / `api_cnpd.py` | coleta e cliente do CNPD |
| `preparar_mapa.py` | gera malhas, centroides e municípios do mapa |
| `dados/cnpd-snapshot.json` | retrato do CNPD |
| `dados/namus-snapshot.json` | retrato do NamUs |
| `dados/fontes.json` | catálogo de fontes |
| `dados/brasil-ufs.geojson` | malha das 27 UFs do Brasil (IBGE) |
| `dados/eua-ufs.geojson` | malha dos 51 estados dos EUA |
| `dados/municipios-cnpd.json` | coordenadas dos 90 municípios do snapshot |
| `testes/cenarios.py` | cenário `s4_desaparecidos_e_fontes` |

## 3. Fluxo dos dados

```
coletar_dados.py  ──► dados/cnpd-snapshot.json  ─┐
coletar_namus.py  ──► dados/namus-snapshot.json ─┤
preparar_mapa.py  ──► malhas + municípios      ─┼─► construir.py ──► index.html
dados/fontes.json ──────────────────────────────┘        (embute JSON e Leaflet)
```

O `construir.py` lê a lista `dados` do `app.json` e grava cada JSON em um
`<script type="application/json" id="...">`. O módulo lê com
`dadosEmbutidos("cnpd")`, `dadosEmbutidos("namus")` etc. **Não edite o
`index.html`**: ele é gerado.

Ao atualizar um snapshot, rode `preparar_mapa.py` antes do `construir.py` para
recalcular os municípios do CNPD (a malha dos EUA e a do Brasil não mudam).

## 4. Schema dos dados

### 4.1 CNPD (`dados/cnpd-snapshot.json`)

```json
{
  "fonte": "CNPD/MJ - Painel Publico de Pessoas Desaparecidas",
  "coletado_em": "2026-11-03T...",
  "total_registros_informado": 381,
  "total_registros_coletado": 381,
  "registros": [
    {
      "id": 229101,
      "nome": "Sara Santos de Santana",
      "idadeAtual": 39,
      "idadeDesaparecimento": 39,
      "sexo": "Feminino",
      "racaCor": null,
      "localRegistro": "Salvador/BA",
      "ufRegistro": "BA",
      "dataDesaparecimento": "13/10/2026",
      "dataRegistroDesaparecimento": "27/10/2026",
      "flLocalizacaoConfirmada": "NAO_CONFIRMADO"
    }
  ]
}
```

### 4.2 NamUs (`dados/namus-snapshot.json`)

```json
{
  "fonte": "NamUs - National Missing and Unidentified Persons System (EUA)",
  "coletado_em": "2026-11-03T...",
  "total_registros_informado": 26607,
  "total_registros_coletado": 300,
  "amostra": 300,
  "registros": [
    {
      "id": 163474,
      "idFormatado": "MP163474",
      "nome": "PHEDRAIRA YARIE DELBOIS-CRUZ",
      "idadeAtual": 21,
      "idadeDesaparecimento": 21,
      "sexo": "Feminino",
      "racaCor": "Hispanic / Latino",
      "localRegistro": "Davenport/FL",
      "ufRegistro": "FL",
      "dataDesaparecimento": "2026-10-07",
      "dataRegistroDesaparecimento": "2026-10-07",
      "flLocalizacaoConfirmada": "NAO_CONFIRMADO",
      "lat": 28.1614046,
      "lon": -81.6017417,
      "url": "https://www.namus.gov/MissingPersons/Case#/163474",
      "fonte": "NamUs"
    }
  ]
}
```

O módulo normaliza as duas fontes para o mesmo conjunto de campos. Datas do CNPD
vêm em `dd/mm/aaaa` e do NamUs em ISO; `desData()` aceita as duas.

## 5. Tela e comportamento

### 5.1 Estado

```js
const DES = {
  fonte: "cnpd",   // cnpd | namus | fontes
  q: "",           // busca por nome
  uf: "",          // UF/estado
  sexo: "",
  faixa: "",       // 0-11 | 12-17 | 18-29 | 30-44 | 45-59 | 60+ | sem
  ordem: "recente",
  visiveis: 80
};
```

O estado é de memória; ao trocar de aba, os filtros são limpos. A tela é
re-renderizada a cada mudança (`navegar()`), o que recria o mapa.

### 5.2 KPIs

- Registros no recorte;
- Mulheres;
- Crianças e adolescentes (0 a 17);
- Idosos (60+);
- UFs/estados com registro;
- Últimos 30 dias (pela data do desaparecimento).

### 5.3 Filtros

- **Nome** (debounce de 260 ms; normaliza acentos);
- **UF/estado** (opções vêm da fonte ativa);
- **Sexo**;
- **Faixa etária**;
- **Ordenação**: desaparecimento mais recente/antigo, nome A-Z, mais tempo
  desaparecido.

### 5.4 Tabela e CSV

- A tabela mostra até `DES.visiveis` (80) registros e um botão "Mostrar mais".
- O nome aponta para o cadastro oficial (CNPD card ou NamUs case).
- O CSV usa `;`, BOM (`\ufeff`), uma linha por registro, e inclui a fonte, a URL
  e a data da coleta (`coletado_em`).
- A foto não é baixada: a CSP bloqueia imagem externa e o volume seria grande.

### 5.5 Catálogo de fontes

- Lê `dados/fontes.json` (18 entradas).
- Status: `integrada`, `pesquisada`, `restrita`, `planejada`, `referencia`.
- Mostra acesso, o que oferece, link e a referência (página do guia ou site).

## 6. Mapa

### 6.1 Por que sem tiles

A CSP do MVP (`connect-src 'none'`, `img-src 'self' data: blob:`) impede tiles
externos. O mapa usa Leaflet com:

- GeoJSON das UFs do Brasil (`dados/brasil-ufs.geojson`, IBGE) ou dos EUA
  (`dados/eua-ufs.geojson`, US Census/PublicaMundi);
- `L.circleMarker` para as localidades;
- `map.fitBounds` na malha;
- `attributionControl` com "Malha: IBGE" ou "Malha: US Census";
- **nenhuma requisição de rede**.

### 6.2 Coordenadas

- **CNPD**: `localRegistro` (`Cidade/UF`) → `dados/municipios-cnpd.json`
  (`{UF: {chave_normalizada: [lat, lon]}}`). Cobertura 381/381.
- **NamUs**: `lat`/`lon` do detalhe do caso (`sighting.publicGeolocation`).
- Se faltar coordenada, o registro não é plotado e entra na nota "sem coordenada".

### 6.3 Agregação e tamanho

- Agrupa por `localRegistro` (e UF); calcula a média das coordenadas do grupo.
- Raio: `6 + sqrt(n) * 3`; cor da fonte (CNPD `#5b4b8a`, NamUs `#b7791f`).
- Tooltip no hover: `Local · N`.
- Clique: abre o painel de detalhe **abaixo do mapa** (não usa popup do Leaflet).

### 6.4 O problema do card atrás do mapa

A primeira versão usava `bindPopup` com `autoPan`. O popup podia:

1. ficar atrás do controle de zoom (o controle tem `z-index: 1000` e o popup,
   700);
2. ser cortado pela borda do contêiner;
3. em um caso, o `autoPan` deslocou o mapa para o Ártico e a malha saiu da tela.

A correção:

- o clique abre `#desDetalhe`, um painel fora do contêiner do mapa, logo abaixo
  dele (sempre visível e à frente);
- o tooltip do hover continua no mapa, com `direction: "auto"`;
- o mapa ganhou `position: relative; z-index: 2` e o painel do Leaflet
  `z-index: 1100` (caso algum popup/tooltip seja usado no futuro);
- `.des-mapa-card` passou de `overflow: hidden` para `visible`.

O painel lista todos os nomes da localidade, com link para o cadastro oficial e
o tempo desde o desaparecimento.

## 7. Como adicionar uma fonte

1. Crie um coletor que grave `dados/<fonte>-snapshot.json` no mesmo formato
   (campos normalizados; `lat`/`lon` quando houver).
2. Adicione a entrada no `app.json`:
   ```json
   ["minhafonte", "dados/minhafonte-snapshot.json"]
   ```
3. Em `src/desaparecidos.js`:
   - carregue com `dadosEmbutidos("minhafonte")`;
   - acrescente a fonte em `DES_INFO` (nome, cor, malha, geo);
   - ajuste `desDados()` para devolver os registros da fonte;
   - inclua a aba em `desAbas()`;
   - ajuste `desIniciarMapa()` se as coordenadas vierem de outro campo;
   - inclua o status no catálogo `dados/fontes.json`.
4. Adicione um teste em `teste(...)` e, se quiser, um cenário em
   `testes/cenarios.py`.
5. Rode `python construir.py` e `python testes/testar.py`.

## 8. Testes

- Embutidos (`#/testes`): 12 testes, incluindo:
  - CNPD carregado;
  - NamUs com coordenadas;
  - malha do Brasil com 27 UFs;
  - todo registro do CNPD com coordenada.
- `testes/cenarios.py` → `s4_desaparecidos_e_fontes`:
  - CNPD 381 e mapa com círculos;
  - filtro UF AL → 151;
  - NamUs 300 e mapa com círculos;
  - catálogo com 18 fontes;
  - CSV com BOM e cabeçalho.
- `testar.py`: zero rede, todas as 7 rotas, `#/testes` 100%, celular 390 px sem
  rolagem horizontal.

## 9. Comandos

```powershell
cd "Apps/gestao_identificados"
python coletar_dados.py
python coletar_namus.py --limite 300
python preparar_mapa.py
python construir.py
python testes/testar.py
python testes/cenarios.py
```

## 10. Pendências técnicas do módulo

- [ ] Focar os círculos do mapa por teclado (hoje a tabela é a alternativa).
- [ ] Avaliar miniaturas/fotos em modo online (hoje não há imagem).
- [ ] Integrar INTERPOL/NCMEC/portais estaduais (ver `FONTES.md`).
- [ ] Recalcular `municipios-cnpd.json` sempre que o CNPD mudar de município.
- [x] Cruzar CNPD com os corpos do NIHDE, com candidatos e confirmação humana (03/11/2026).
- [ ] Revisar os termos de uso do NamUs e do CNPD antes de publicar os dados.
- [ ] Coordenar o `app.json` com a outra IA que mantém o MVP (o contrato já foi
      atualizado com a rota `#/desaparecidos` e os arquivos reais).
