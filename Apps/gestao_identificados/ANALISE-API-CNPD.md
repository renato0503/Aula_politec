# Análise da API pública — CNPD/MJ e Desaparecidos BR

Data da análise: **03/11/2026**
Pasta: `Apps/gestao_identificados/`
Objetivo: transformar a consulta pública de pessoas desaparecidas em uma fonte
legível por máquina e em um painel de leitura para o NIHDE/POLITEC.

---

## 1. Resumo

O painel público do **CNPD/MJ** (`https://cnpd.mj.gov.br/painel-publico`) é uma
aplicação Angular que consome a própria API em `/api`. Três chamadas são
suficientes para reproduzir a consulta do site:

| O que | Método e caminho | Autenticação |
|---|---|---|
| Listar e filtrar | `POST /api/api/painel-publico/desaparecidos/filtrar?ordenacao=...&pagina=N` | nenhuma |
| Abrir uma pessoa | `GET /api/api/painel-publico/desaparecidos/{id}` | nenhuma |
| Foto principal | `GET /api/desaparecimentos/{id}/arquivos-imagem/main` | nenhuma |

O endpoint devolve `Access-Control-Allow-Origin: *`, então o navegador consegue
chamar a API de qualquer origem. **Não há chave, token, cookie ou CSRF.**

O site **Desaparecidos BR** (`https://www.desaparecidosbr.org/`) não tem API
própria: ele é uma página estática (`app.js`) que chama exatamente esses mesmos
endpoints do CNPD, com `API_BASE = "https://cnpd.mj.gov.br/api/api/"` e
`IMG_BASE = "https://cnpd.mj.gov.br/api/desaparecimentos"`.

Na coleta de 03/11/2026 o painel devolveu **381 registros em 13 páginas de 30**,
distribuídos em 16 UFs. O recorte não é a totalidade nacional (ver seção 6).

---

## 2. Como a análise foi feita

O trabalho seguiu o método do repositório
[`kalil0321/reverse-api-engineer`](https://github.com/kalil0321/reverse-api-engineer):
descobrir a chamada que a tela faz, capturar a requisição, tipar a resposta e
entregar um cliente executável.

Neste caso não foi necessário dirigir um navegador para gravar HAR. O painel
Angular publica a configuração e o código do módulo público:

1. `https://cnpd.mj.gov.br/assets/env.js` revela `apiUrl = "/api"`.
2. `runtime-es2015.*.js` aponta para os chunks `common` e `7`, onde está o
   `PainelPublicoModule`.
3. O chunk `7-es2015.*.js` contém a classe do serviço:

   ```js
   this.apiUrl = `${environment.apiUrl}/api/painel-publico/desaparecidos`;
   buscarDesaparecidos(filtros = {}, ordenacao = "MAIS_RECENTE", pagina = 0) { ... }
   ```

4. O `app.js` do Desaparecidos BR confirma os mesmos caminhos e mostra como a
   foto é decodificada (campo `conteudo`, em base64).

O CLI `reverse-api-engineer` 0.14.0 foi instalado e passou no preflight
(`agent --dry-run`) com o provedor Playwright. Como os endpoints estavam
expostos no bundle e a API aceita CORS aberto, a captura foi substituída por
leitura do bundle e validação por requisições diretas. O cliente tipado
equivalente está em `api_cnpd.py`.

---

## 3. Arquitetura dos dois sites

| Site | Stack | Origem dos dados | Como chama |
|---|---|---|---|
| `cnpd.mj.gov.br/painel-publico` | Angular (chunks ES2015/ES5), `env.js` | API própria em `/api` | Angular `HttpClient` |
| `www.desaparecidosbr.org` | HTML + `app.js` puro, sem build | API do CNPD | `fetch()` direto, com cache de 30 min em `sessionStorage` |

O Desaparecidos BR monta a foto com `fetch` no endpoint `/main`, extrai o
`conteudo` (base64) por expressão regular e monta um `data:` URI. Ele também
filtra **no cliente** por idade (crianças de 1 a 17 e idosos de 60+), porque a
API não é chamada com esses filtros.

---

## 4. Endpoints

### 4.1 Listar e filtrar

```
POST https://cnpd.mj.gov.br/api/api/painel-publico/desaparecidos/filtrar?ordenacao=MAIS_RECENTE&pagina=0
Content-Type: application/json

{"nome": ""}
```

Resposta (200):

```json
{
  "desaparecidos": [
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
  ],
  "totalRegistros": 381,
  "totalPaginas": 13,
  "paginaAtual": 0,
  "tamanhoPagina": 30
}
```

Regras observadas:

- `tamanhoPagina` é fixo em **30**; não há parâmetro para mudar.
- A paginação começa em **0**. Página acima do total devolve 200 com
  `desaparecidos: []` e os totais corretos.
- Campos com valor nulo ou vazio podem ser omitidos do corpo do POST; o
  servidor filtra apenas o que recebe.
- O filtro `nome` não é apenas o nome da pessoa: em teste, `{"nome":"maria"}`
  devolveu 17 registros, incluindo nomes sem "Maria". A busca do site parece
  cobrir outros campos internos que não aparecem no retorno público. A busca
  do painel deste repositório é nominal (nome do registro) e está rotulada
  assim na tela.

#### Filtros aceitos no corpo

Extraídos do formulário do painel público:

| Campo | Tipo | Exemplo | Observação |
|---|---|---|---|
| `nome` | string | `"maria"` | busca textual |
| `sexo` | string | `"Feminino"` | `Masculino`, `Feminino`, `Intersexo` |
| `racaCor` | string | `"Parda"` | `Branca`, `Preta`, `Parda`, `Amarela`, `Indígena` |
| `estado` | string | `"MT"` | sigla da UF |
| `municipio` | string | `"Cuiabá"` | usado junto com `estado`; o site ajusta `Brasília` para `Brasília` |
| `idadeAtual` | inteiro | `15` | idade exata |
| `idadeDesaparecimento` | inteiro | `15` | idade exata no desaparecimento |
| `faixaEtariaAtualDe` | inteiro | `0` | faixa de idade atual |
| `faixaEtariaAtualAte` | inteiro | `17` | faixa de idade atual |
| `faixaEtariaDesaparecimentoDe` | inteiro | `0` | faixa na data do desaparecimento |
| `faixaEtariaDesaparecimentoAte` | inteiro | `17` | faixa na data do desaparecimento |
| `anoRegistro` | string | `"2026"` | ano do registro |
| `mesRegistro` | string | `"10"` | mês do registro (1 a 12) |

#### Ordenação (`query string`)

| Valor | Efeito |
|---|---|
| `MAIS_RECENTE` | registro mais recente primeiro (padrão do site) |
| `MAIS_ANTIGO` | registro mais antigo primeiro |
| `NOME_ASC` | nome A-Z |
| `NOME_DESC` | nome Z-A |

Teste de referência: `estado=MT` devolveu 1 registro; `sexo=Feminino`, 72;
`faixaEtariaAtualDe=0&faixaEtariaAtualAte=17`, 23; `faixaEtariaAtualDe=60`, 55.

### 4.2 Detalhe de uma pessoa

```
GET https://cnpd.mj.gov.br/api/api/painel-publico/desaparecidos/229101
```

Devolve **os mesmos campos** da listagem. O painel público não expõe, nesse
endpoint, características físicas, circunstâncias, boletim de ocorrência ou
nome da mãe. O modal do site oficial é montado com o objeto que já veio da
lista.

### 4.3 Foto principal

```
GET https://cnpd.mj.gov.br/api/desaparecimentos/229101/arquivos-imagem/main
```

Resposta (200):

```json
{
  "id": 137758,
  "desaparecimentoId": null,
  "arquivoCnpd": {
    "id": 23497,
    "nome": "sara santos de santana_crop.jpg",
    "path": "cnpd/jpg/2026-10-22/...",
    "tamanho": 47993,
    "arquivoDTO": {
      "nome": "...",
      "extensao": "jpg",
      "tamanho": 47993,
      "conteudo": "/9j/4AAQSkZJRgABAQAAAQABAAD/...",
      "hash": "...",
      "path": "..."
    }
  },
  "isMain": true
}
```

O campo `conteudo` é a imagem em **base64**. A extensão vem em `extensao`
(`jpg`, `png`). Para montar a imagem:

```js
const url = `data:${ext === "png" ? "image/png" : "image/jpeg"};base64,${conteudo}`;
```

Se a pessoa não tem foto, o endpoint responde com erro ou sem `conteudo`; o
site cai para `assets/images/sem-imagem.jpeg`.

### 4.4 Demais imagens (não públicas)

O serviço do painel também chama:

```
GET /api/desaparecimentos/{id}/arquivos-imagem?pageIndex=0&pageSize=1&sortField=id&isAscSortMode=false
```

Essa listagem respondeu **401 Não Autorizado** sem sessão. Ou seja, apenas a
imagem principal é pública. O painel deste repositório usa só `/main`.

### 4.5 Limpar filtros

```
POST /api/api/painel-publico/desaparecidos/limpar-filtros
Content-Type: application/json

{}
```

Responde 200 com a primeira página completa (mesmo formato da listagem). O site
usa para resetar o formulário; o painel local não precisa desse endpoint.

### 4.6 Serviços de apoio (lado do cliente)

| Serviço | Uso no site oficial | No painel local |
|---|---|---|
| `https://servicodados.ibge.gov.br/api/v1/localidades/estados/{UF}/municipios` | preencher a lista de municípios | não usado (o município vem no registro) |
| `https://ipapi.co/{ip}/json/` | sugerir a UF pela localização do IP | não usado |
| `https://api.qrserver.com/v1/create-qr-code/` | QR Code do cartão compartilhado | não usado |

O painel local não depende de nenhum deles.

### 4.7 Contato da delegacia

O modal de compartilhamento do site chama um serviço interno
(`delegaciaService.findByUf(uf)`) para obter telefone e e-mail da delegacia da
UF. O caminho desse serviço não está no chunk público e não foi mapeado. Não é
necessário para listar, detalhar ou exibir a foto.

---

## 5. Campos do registro

| Campo na API | Tipo | Significado | Qualidade no recorte |
|---|---|---|---|
| `id` | inteiro | identificador do boletim | sempre presente |
| `nome` | string | nome da pessoa | sempre presente |
| `idadeAtual` | inteiro ou nulo | idade recalculada hoje | 372 de 381 preenchidos |
| `idadeDesaparecimento` | inteiro ou nulo | idade na data do desaparecimento | 376 de 381 |
| `sexo` | string | `Masculino`, `Feminino`, `Intersexo`, `Sem informação`, `Não identificado` | sempre presente |
| `racaCor` | string ou nulo | raça/cor autodeclarada | 380 de 381 nulos ou "Não Informada" |
| `localRegistro` | string | `Município/UF` | sempre presente |
| `ufRegistro` | string | sigla da UF | sempre presente |
| `dataDesaparecimento` | string `dd/mm/aaaa` | data do desaparecimento | 378 de 381 |
| `dataRegistroDesaparecimento` | string `dd/mm/aaaa` | data do registro no CNPD | sempre presente |
| `flLocalizacaoConfirmada` | string | `NAO_CONFIRMADO` ou indicador de localização | 381 `NAO_CONFIRMADO` na coleta |

Observações:

- Datas em `dd/mm/aaaa`; o painel converte para ISO ao exportar.
- `localRegistro` pode vir com acentuação corrompida em algumas ferramentas
  (por exemplo, `Maceió` como `MaceiÃ³` quando o cliente lê o JSON como
  Latin-1). O conteúdo é UTF-8; leia como UTF-8.
- A API pode devolver `localRegistro` genérico ou incompleto; o painel usa o
  campo como veio.

---

## 6. Recorte observado em 03/11/2026

Coleta completa (13 páginas, 381 registros):

| UF | Registros |
|---|---:|
| AL | 151 |
| BA | 73 |
| SE | 37 |
| RN | 33 |
| AM | 29 |
| TO | 10 |
| AP | 10 |
| PI | 10 |
| SC | 7 |
| RR | 7 |
| GO | 6 |
| RO | 2 |
| RS | 2 |
| MA | 2 |
| MT | 1 |
| PR | 1 |

- **Sexo:** 301 masculino, 72 feminino, 6 "Sem informação", 2 "Não identificado".
- **Faixa etária atual:** 4 de 0 a 11; 19 de 12 a 17; 106 de 18 a 29;
  113 de 30 a 44; 75 de 45 a 59; 55 de 60+; 9 sem informação.
- **Raça/cor:** 380 nulos ou "Não Informada" (o restante é 1 "Parda").
- **Localização confirmada:** 381 como `NAO_CONFIRMADO`.
- **Datas de desaparecimento:** de 01/01/1965 a 02/11/2026.
- **Datas de registro:** de 05/08/2018 a 03/11/2026.

**Leitura:** a concentração em AL, BA, SE, RN e AM e a ausência de SP indicam
que o painel público devolve um recorte, não o banco nacional completo. O
número de 381 não deve ser citado como "total de desaparecidos do Brasil".

---

## 7. Regras, limites e cuidados

| Item | Situação |
|---|---|
| Autenticação | nenhuma nos três endpoints usados |
| CORS | `Access-Control-Allow-Origin: *`; `Allow-Credentials: true` |
| Cache | respostas com `Cache-Control: no-cache`; o site do Desaparecidos BR guarda 30 min em `sessionStorage` |
| Limite de taxa | não documentado; use no máximo uma requisição por vez e espere entre páginas (o coletor usa 0,4 s) |
| Tamanho da página | 30 registros, fixo |
| Imagens | somente `/main` é pública; a listagem de outras imagens dá 401 |
| Estabilidade | API não documentada, pode mudar sem aviso; os caminhos foram confirmados em 03/11/2026 |
| LGPD | são dados pessoais públicos (nome, idade, cidade, foto), publicados pelo CNPD para localização. Use apenas para essa finalidade; não faça contato com famílias, cruzamento nominal ou divulgação fora do contexto |

---

## 8. Cliente, coleta e painel

| Arquivo | O que faz |
|---|---|
| `api_cnpd.py` | cliente Python tipado (`CnpdClient`, `Pessoa`, `Pagina`) com `filtrar`, `obter`, `imagem`, `todas` e CLI |
| `coletar_dados.py` | percorre as 13 páginas e grava `dados/cnpd-snapshot.json` |
| `gerar_painel.py` | injeta o snapshot no `painel/template.html` e grava `index.html` |
| `painel/template.html` | fonte da tela (HTML, CSS e JS, sem dependência externa) |
| `index.html` | painel pronto para abrir com duplo clique |
| `dados/cnpd-snapshot.json` | retrato da coleta: metadados + 381 registros |

Comandos:

```powershell
cd Apps\gestao_identificados
python api_cnpd.py --nome maria --uf BA
python api_cnpd.py --id 229101
python coletar_dados.py
python gerar_painel.py
```

O `index.html` abre sem servidor. Ele já traz o snapshot embutido; o botão
**Atualizar** refaz a coleta no navegador (quando há internet) e as fotos são
carregadas sob demanda do CNPD.

O painel oferece: indicadores (total, crianças e adolescentes, idosos,
mulheres, UFs, últimos 30 dias), seis gráficos (UF, sexo, faixa etária, tempo
desde o desaparecimento, série mensal e municípios), busca por nome, filtros de
UF, sexo e faixa, ordenação, cartões com foto, ficha completa, link para o
cartão oficial e exportação CSV do recorte.

---

## 9. Reprodução rápida

PowerShell:

```powershell
$body = '{"nome":""}'
Invoke-RestMethod -Method POST -ContentType 'application/json' -Body $body `
  -Uri 'https://cnpd.mj.gov.br/api/api/painel-publico/desaparecidos/filtrar?ordenacao=MAIS_RECENTE&pagina=0'
```

curl:

```bash
curl -s -X POST \
  'https://cnpd.mj.gov.br/api/api/painel-publico/desaparecidos/filtrar?ordenacao=MAIS_RECENTE&pagina=0' \
  -H 'Content-Type: application/json' -d '{"nome":""}'
```

Python (stdlib):

```python
from api_cnpd import CnpdClient

cli = CnpdClient()
pagina = cli.filtrar({"sexo": "Feminino", "estado": "MT"})
print(pagina.total_registros)
for pessoa in pagina.registros:
    print(pessoa.id, pessoa.nome, pessoa.local_registro)
```

---

## 10. O que ficou de fora

- O caminho do serviço de contato das delegacias (usado no compartilhamento do
  site oficial).
- O detalhe ampliado (características físicas, circunstâncias, documentos) não
  é público nesse painel; fica para uma integração autenticada, se houver.
- O cruzamento com os corpos não identificados do NIHDE: o formulário do
  projeto prevê essa integração para a fase 2. Este painel entrega a leitura da
  base de desaparecidos, que é a outra ponta do cruzamento.
- Uma API HTTP própria (FastAPI/Express): o cliente e o painel cobrem a leitura;
  se o NIHDE precisar de um serviço, o `api_cnpd.py` é a camada de acesso a
  reaproveitar.

---

## 11. Referências

- Painel público: <https://cnpd.mj.gov.br/painel-publico>
- Cartão individual: <https://cnpd.mj.gov.br/painel-publico/card/229101>
- Desaparecidos BR: <https://www.desaparecidosbr.org/>
- Reverse API Engineer: <https://github.com/kalil0321/reverse-api-engineer>
- Formulário do NIHDE nesta pasta:
  `NIHDE---Gesto-de-dados-de-Corpos-No-Identificados-e-Corpos-No-Reclamados-2026-11-03.json`

