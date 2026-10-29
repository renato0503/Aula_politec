# Agiliza + · contexto e arquitetura

> Grupo: Diego Costa, Francineide da Silva e Andreia Cristina
> Fonte: `PROJETO.md` (envio de 27/10/2026) e a decisão de arquitetura do professor:
> **HTML monolítico, offline first**.

---

## 1. O problema

Hoje, o perito monta o laudo de um exame de celular de forma manual. Ele baixa a
requisição em PDF no ATENA, abre um laudo anterior no Word, renomeia esse
arquivo e copia, campo a campo, os dados de quatro fontes:

| Fonte | Arquivo | O que o perito copia |
|---|---|---|
| Requisição | PDF digitalizado, baixado do ATENA | protocolo, ofício, processo, autoridade, data, quesitos |
| Aparelho | `DEVICE INFO.txt` | marca, modelo, IMEI 1, IMEI 2 |
| Hash | `HASHDOHASH.txt` | valor SHA-256 |
| Cartões SIM | HTML nas pastas `OBJ 01-A`, `OBJ 01-B`... | ICCID e operadora de cada cartão |

Em seguida, ele adapta os textos padronizados da Gerência (descrição dos
objetos, exames, anexos), transcreve e responde aos quesitos, revisa e salva.
O AS-IS tem **14 etapas**, todas executadas pelo perito. Nesse sentido, o volume
informado é de **40 laudos por mês** e cerca de **200 h de elaboração por mês**.
O grupo ainda não mediu essa linha de base, que é o primeiro passo do piloto.

**Dor**: digitação repetitiva de identificadores longos (IMEI com 15 dígitos,
ICCID com 19 a 20, SHA-256 com 64 caracteres). Por isso, um dígito trocado
compromete o laudo, e o retrabalho aparece na revisão.

**Meta da defesa**: reduzir em **30%** o tempo médio de elaboração e a taxa de
laudos que exigem correção, medidos contra a linha de base.

## 2. O que o MVP faz e o que não faz

| Faz | Não faz |
|---|---|
| Seleciona a pasta do caso e inventaria os arquivos | Conecta ao ATENA |
| Extrai dados dos TXT, HTML e do PDF | Atende exames complexos ou outros tipos de exame |
| Mostra os dados para o perito conferir e corrigir | Analisa vestígios |
| Oferece a biblioteca de textos padronizados | Elabora ou aprova conclusões técnicas (RN10) |
| Organiza quesitos e sugere respostas | Gerencia vários usuários |
| Gera o laudo `.docx` a partir do modelo institucional | Sobrescreve o modelo ou o laudo anterior (RN13) |
| Confere campos vazios e identificadores inválidos | Dispensa a revisão do perito (RN14) |
| Registra tempo, conferências e versão gerada | Envia dados para qualquer servidor |

**Critério de aceite do MVP** (texto do grupo): o perito seleciona a pasta do
caso, importa e confere os dados, gera um laudo Word com a estrutura e os textos
esperados, corrige as informações à mão e salva o documento **sem alterar os
arquivos originais**, e a aprovação final continua com ele.

## 3. Decisão de arquitetura: HTML monolítico, offline first

O grupo propôs Python com instalação no Windows. A arquitetura adotada no curso
troca a instalação por **um único arquivo `index.html`**, que abre com duplo
clique no Edge ou no Chrome do computador da Gerência. Dessa forma, o app atende
às mesmas restrições do formulário (local, sem ATENA, sem servidor, sem custo de
hospedagem) e não depende da TI para instalar Python.

| Restrição do grupo | Como o HTML monolítico atende |
|---|---|
| Funcionar no Windows, sem servidor | Abre por `file://` no Edge ou no Chrome, sem instalação |
| Não expor dados pessoais | Nenhuma chamada de rede. A política CSP bloqueia `connect-src` |
| Não alterar os originais | A pasta do caso é aberta em modo leitura. O laudo vai para uma subpasta nova |
| Preservar o modelo oficial | O `.docx` é preenchido por marcadores, sem recriar a formatação |
| Baixo custo | Bibliotecas de código aberto, embutidas no próprio arquivo |

### 3.1 Princípios

1. **Um arquivo só.** HTML, CSS, JS e bibliotecas ficam dentro do `index.html`.
   Não há CDN, `fetch` externo nem build obrigatório para rodar.
2. **Offline first.** Tudo funciona sem internet. Além disso, o estado fica no
   IndexedDB do navegador e pode ser exportado em `.json` a qualquer momento.
3. **Os originais são somente leitura.** O app lê a pasta do caso e grava apenas
   na subpasta `LAUDO_GERADO/`, com nome versionado.
4. **O perito confere tudo.** Nenhum dado extraído chega ao Word sem passar pela
   tela de conferência (RN04).
5. **Navegador alvo: Edge e Chrome** (Chromium). Eles oferecem a File System
   Access API, que permite abrir a pasta inteira e gravar o laudo nela.

### 3.2 Visão geral

```mermaid
flowchart LR
  subgraph Pasta do caso - somente leitura
    PDF[Requisição.pdf]
    TXT1[DEVICE INFO.txt]
    TXT2[HASHDOHASH.txt]
    HTML[OBJ 01-A/*.html]
  end
  subgraph index.html - navegador, offline
    UI[Telas #/rotas]
    EXT[Extratores<br/>pdf.js · regex · DOMParser]
    VAL[Validador<br/>Luhn · SHA-256 · obrigatórios]
    LIB[Biblioteca de textos]
    GEN[Gerador DOCX<br/>PizZip + docxtemplater]
    DB[(IndexedDB<br/>agiliza_mais_v1)]
  end
  MOD[Modelo .docx<br/>com marcadores]
  OUT[LAUDO_GERADO/<br/>laudo_PROTOCOLO_v1.docx]
  PDF & TXT1 & TXT2 & HTML --> EXT --> VAL --> UI
  UI <--> DB
  LIB <--> DB
  MOD --> GEN
  UI --> GEN --> OUT
```

### 3.3 Camadas dentro do `index.html`

| Camada | Responsabilidade | Tecnologia |
|---|---|---|
| Roteador | Telas por hash (`#/inicio`, `#/arquivos`...) | JS puro, `hashchange` |
| Estado | Caso aberto, dados conferidos, textos, log | objeto `estado` + IndexedDB |
| Acesso a arquivos | Abrir a pasta, ler, gravar o laudo | `showDirectoryPicker()`; alternativa: `<input webkitdirectory>` + download |
| Extratores | TXT, HTML, PDF (texto) e PDF (OCR) | regex, `DOMParser`, pdf.js, Tesseract.js (opcional) |
| Validador | Regras RN02, RN03, RN09, RN11 | JS puro (Luhn, regex, obrigatórios) |
| Gerador | Preencher o modelo `.docx` | PizZip + docxtemplater |
| Registro | Log de conferência, tempos, versões | IndexedDB, exportação CSV |

### 3.4 Estrutura de pastas do projeto

```
Apps/agiliza-mais/
├── index.html              ← o app (único arquivo entregue ao perito)
├── contexto.md             ← este arquivo
├── sprint.md               ← plano de construção
├── PROJETO.md              ← especificação enviada pelo grupo
├── vendor/                 ← bibliotecas minificadas + VERSOES.md (origem e versão)
├── modelos/
│   └── modelo-laudo-celular.docx   ← modelo institucional com marcadores {campo}
├── exemplos/
│   └── caso-ficticio-001/  ← pasta de caso 100% fictícia (PDF, TXT, HTML)
└── testes/
    └── testes.html         ← testes dos extratores e validadores (abre no navegador)
```

As bibliotecas são embutidas no `index.html` pelo `Apps/_base/embutir.py`, que troca
marcadores como `<!-- LIB:pizzip -->` pelo conteúdo minificado. Com isso, o
arquivo entregue continua sendo um só, e o código do app fica legível.

| Biblioteca | Uso | Tamanho aproximado |
|---|---|---|
| pdf.js (build legada, UMD) + worker | texto e visualização do PDF | 1,3 MB |
| PizZip | abrir e reescrever o `.docx` (que é um zip) | 100 KB |
| docxtemplater | marcadores, laços (SIMs, quesitos) e condicionais | 150 KB |
| Tesseract.js + `por.traineddata` (fast) | OCR do PDF digitalizado (sprint opcional) | 5 a 8 MB |

> As versões exatas ficam registradas em `vendor/VERSOES.md` no Sprint 0.

## 4. Telas (rotas)

| Rota | Tela | O que o perito faz | Regras |
|---|---|---|---|
| `#/inicio` | Início | Novo laudo, retomar caso, escolher o modelo | RN15 |
| `#/arquivos` | Pasta do caso | Seleciona a pasta, vê o inventário (presente, ausente, duplicado) | RN01, RN02 |
| `#/dados` | Conferência | Vê cada dado extraído ao lado da origem, corrige e confirma | RN03, RN04, RN06, RN07 |
| `#/textos` | Textos padronizados | Escolhe e edita os textos de descrição, exames e anexos | RN08 |
| `#/quesitos` | Quesitos | Confere numeração, enunciado e resposta de cada quesito | RN09, RN10 |
| `#/gerar` | Geração | Roda a conferência automática e gera o `.docx` | RN11, RN12, RN13 |
| `#/revisao` | Revisão final | Registra correções, marca "revisado pelo perito" | RN14 |
| `#/biblioteca` | Biblioteca | Mantém os textos padronizados e as respostas-modelo | RN08 |
| `#/historico` | Histórico | Casos, versões geradas, tempos, exportação CSV | métricas |
| `#/config` | Configuração | Modelo padrão, backup `.json`, limpar dados do caso | LGPD |

## 5. Modelo de dados (IndexedDB `agiliza_mais_v1`)

Cada entidade do formulário vira um *object store*. Identificadores técnicos
(IMEI, ICCID, hash) são sempre **texto** (RN03).

| Store | Chave | Campos principais | Origem |
|---|---|---|---|
| `casos` | `id_caso` | numero_protocolo, data_solicitacao, numero_oficio, autoridade_solicitante, numero_processo, status, inicio_em, fim_em | PDF + perito |
| `aparelhos` | `id_aparelho` | id_caso, marca, modelo, imei_1, imei_2, cor | `DEVICE INFO.txt` |
| `sims` | `id_sim` | id_caso, identificador_objeto (01-A), iccid, operadora | HTML das pastas OBJ |
| `hashes` | `id_hash` | id_caso, algoritmo, valor_hash, arquivo | `HASHDOHASH.txt` |
| `textos` | `id_texto` | categoria, titulo, conteudo, versao, ativo | biblioteca da Gerência |
| `quesitos` | `id_quesito` | id_caso, numero_quesito, enunciado, resposta, status_conferencia | PDF + perito |
| `modelos` | `id_modelo` | nome, tipo_modelo, arquivo (Blob), marcadores | perito |
| `laudos` | `id_laudo` | id_caso, nome_arquivo, versao, data_geracao, status_revisao | gerador |
| `conferencias` | `id_registro` | id_caso, campo_verificado, resultado, observacao, data_hora | validador + perito |

Cada valor extraído guarda também a **origem** (`{valor, origem: "DEVICE INFO.txt", linha: 12, confirmado: false}`).
Por isso, a tela de conferência mostra de onde veio cada dado.

## 6. Extração (como cada dado é lido)

| Dado | Arquivo | Método | Validação |
|---|---|---|---|
| Marca, modelo | `DEVICE INFO.txt` | regex por rótulo (`Manufacturer`, `Model`...) | obrigatório |
| IMEI 1 e 2 | `DEVICE INFO.txt` | regex `\b\d{15}\b` próximo do rótulo IMEI | 15 dígitos + dígito de Luhn |
| SHA-256 | `HASHDOHASH.txt` | regex `\b[a-fA-F0-9]{64}\b` | 64 hexadecimais |
| ICCID, operadora | `OBJ 01-A/*.html` | `DOMParser` + busca por rótulo na tabela | 19-20 dígitos, prefixo 89, Luhn |
| Identificador do objeto | nome da pasta `OBJ 01-A` | regex `OBJ\s*(\d{2}-[A-Z])` | um SIM por pasta (RN07) |
| Protocolo, ofício, processo, autoridade, data | requisição PDF | pdf.js extrai a camada de texto e regex por rótulo | formato do número CNJ quando houver |
| Quesitos | requisição PDF | blocos após "QUESITOS", numeração `1)`, `1.`, `1 -` | sequência contínua (RN09) |
| PDF sem camada de texto | requisição digitalizada | OCR (Sprint 10) ou digitação ao lado da visualização do PDF | conferência obrigatória |

Os TXT podem vir em UTF-8, UTF-16 ou Windows-1252. Por isso, o leitor testa o
BOM e decodifica com `TextDecoder` antes de aplicar as regex.

> **Os formatos reais dos TXT e HTML ainda não foram vistos.** O Sprint 0 recebe
> amostras anonimizadas para escrever as regex certas.

## 7. Geração do Word

O modelo institucional recebe **marcadores** uma única vez (Sprint 0), e a
formatação continua a do documento oficial:

```
Protocolo: {numero_protocolo}            Ofício: {numero_oficio}
Aparelho {marca} {modelo}, IMEI 1 {imei_1}, IMEI 2 {imei_2}.
{#sims}Objeto {identificador_objeto}: cartão SIM {operadora}, ICCID {iccid}.
{/sims}{^sims}{texto_sem_sim}{/sims}
{#quesitos}{numero_quesito}) {enunciado}
Resposta: {resposta}
{/quesitos}
```

- `{#sims}...{/sims}` repete o bloco para cada cartão. `{^sims}` cobre a
  ausência de SIM (RN06).
- O arquivo sai como `LAUDO_GERADO/laudo_<protocolo>_v<N>.docx`. Se o nome já
  existe, o app grava `v<N+1>` (RN13).
- **Laudo anterior como base** (pedido na primeira tela): o MVP usa o modelo
  com marcadores. Converter um laudo anterior em modelo fica no Sprint 11, que é
  opcional. A substituição automática de valores num laudo antigo pode deixar
  restos de outro caso (risco: "laudo com informações incorretas").

## 8. Conferência automática (RN11)

Antes de gerar a versão final, o validador lista os problemas em três níveis:

| Nível | Exemplos | Efeito |
|---|---|---|
| Bloqueia | IMEI com dígito de Luhn inválido, SHA-256 com tamanho errado, protocolo vazio, quesito sem resposta | não gera a versão final |
| Alerta | IMEI 2 ausente, nenhum SIM encontrado, texto padronizado não selecionado | gera, mas registra o alerta |
| Informa | dado corrigido à mão, dado digitado sem origem | registra no log |

## 9. LGPD e segurança

- **Nada sai do computador.** A meta tag CSP traz `connect-src 'none'`, e o app
  não chama nenhum endereço externo.
- **Retenção**: ao finalizar o caso, o botão "Limpar dados do caso" apaga
  aparelho, SIMs, hash e quesitos do IndexedDB e mantém só o registro de
  métricas (protocolo, tempos, número de correções), como o grupo previu (LGPD,
  arts. 15 e 16).
- **Testes só com dados fictícios** (RN16). A pasta `exemplos/caso-ficticio-001/`
  é o material de desenvolvimento.
- **Rastreabilidade**: o store `conferencias` registra o que foi extraído, o que
  o perito alterou e quando o laudo foi gerado.

## 10. Métricas do piloto

| KPI | Fórmula | Como o app mede |
|---|---|---|
| Tempo de elaboração | `fim_em − inicio_em` por caso | cronômetro do caso (início ao abrir a pasta, fim ao marcar "revisado") |
| Taxa de correção | laudos com correção ÷ total × 100 | campo "exigiu correção após gerar?" na revisão |
| Campos corrigidos por caso | nº de dados extraídos alterados pelo perito | store `conferencias` |

A exportação `historico.csv` (UTF-8 com BOM, `;`) alimenta a comparação com a
planilha manual da linha de base (2 semanas, antes do piloto).

## 11. Riscos de arquitetura

| Risco | Mitigação |
|---|---|
| TI bloqueia o `showDirectoryPicker` ou o Edge está em versão antiga | Alternativa com `<input webkitdirectory>` para leitura e download do `.docx` |
| Limpeza do navegador apaga o IndexedDB | `navigator.storage.persist()` e backup `.json` com um clique |
| Formato real dos TXT/HTML diferente do esperado | Sprint 0 com amostras anonimizadas e testes de cada extrator |
| OCR lento ou impreciso em PDF digitalizado | OCR opcional. O fluxo padrão mostra o PDF ao lado dos campos para digitação |
| Marcador quebrado no Word (o Word divide o texto em vários *runs*) | Escrever cada marcador de uma vez no modelo. O docxtemplater acusa marcador inválido |
| Arquivo `index.html` grande | Sem OCR, cerca de 2 MB. Com OCR, cerca de 10 MB, e por isso o OCR pode ficar num segundo arquivo `ocr.html` |
