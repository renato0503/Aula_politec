# Agiliza + · sprints até o MVP

> Arquitetura: HTML monolítico, offline first (ver `contexto.md`).
> Cada sprint dura **1 semana** e termina com o `index.html` abrindo e
> funcionando no Edge, com o caso fictício.
> Ordem: primeiro o dado e o Word (o que prova a ideia), depois o PDF e o OCR,
> como o grupo pediu no campo "aprendizado".

## Andamento

| Sprint | Situação |
|---|---|
| 0 | Parte técnica feita em 29/10/2026 (dados fictícios, bibliotecas, modelos). Itens que dependem de pessoas continuam abertos. |
| 1 | Feito em 29/10/2026. `python Apps/_base/testar.py agiliza-mais` passa. |
| 2 | Feito em 29/10/2026. `python Apps/_base/testar_sprints.py agiliza-mais` passa (cenário do "Pronto quando"). |
| 3 | Feito em 29/10/2026. `python Apps/_base/testar_sprints.py agiliza-mais` passa (cenário do Sprint 3 em `Apps/_base/cenarios/sprint3.py`; código em `src/sprint3.js`). Os testes dos extratores ficaram na tela `#/testes` do próprio app (padrão dos apps), e não num `testes/testes.html` separado; o cenário confere a extração dos 3 casos contra o `GABARITO.json`. |
| 4 a 11 | Feito em 03/11/2026 (`src/sprint4.js`). Word pelo modelo embutido ou carregado em `#/config`, com a lista de marcadores sem dado e o arquivo `laudo_<protocolo>_v<N>.docx` gravado em `LAUDO_GERADO` (ou baixado); conferência com selo por campo (extraído, corrigido, digitado, confirmado), validação ao digitar, SIM incluído ou removido à mão e "Confirmar todos" preso ao IMEI 1 e ao hash; requisição em PDF lida pelo pdf.js (protocolo, ofício, processo, autoridade, data e quesitos), PDF ao lado e aviso de PDF digitalizado; biblioteca com versão, desativação, importação e exportação; marcadores dentro dos textos e prévia; quesitos da requisição com sugestão de resposta por palavra-chave, que só entra no laudo depois de aprovada; validador com bloqueia, alerta e informa; revisão com as correções feitas no Word; histórico com taxa de correção, `historico.csv` e limpeza do caso; privacidade em `#/config`; caso de exemplo embutido (`exemplos/caso-exemplo.json`). Cenários `s4_a_s11_laudo_completo` (14/14) e `s5_caso_de_exemplo_e_modelo` (4/4) passam. **OCR (S10)**: simulado, como o formulário autoriza; decisão registrada no `PROJETO.md` em 03/11/2026. |
| 12 | Aceite e piloto: dependem do grupo. |
| Início e gestão | Feito em 03/11/2026. Botão **Carregar a pasta do caso** em `#/inicio`, com criação do caso e abertura da conferência; lista de laudos em preenchimento com continuar, renomear, mover para pasta e excluir. Cenário `s12_inicio_pasta_e_gestao` (9/9). |
| 14 | Feito em 03/11/2026: outras informações do perito, foto com sugestão de cor, ajuda dos arquivos, histórico com Abrir e correção do teste. Modelo institucional, IA externa e caso real seguem humanos. |

Modelo `.docx` **fictício** com os marcadores pronto e testado no navegador (`modelos/`); falta pôr os marcadores no modelo institucional. Formatos dos TXT e HTML **supostos** (`exemplos/FORMATOS.md`). `textos.json` fictício.

## Visão geral

| Sprint | Tema | Entrega verificável | Regras |
|---|---|---|---|
| 0 | Preparação e linha de base | Caso fictício, modelo `.docx` com marcadores, planilha de tempo rodando | RN16 |
| 1 | Esqueleto do app | `index.html` com rotas, IndexedDB e backup `.json` | RN15 |
| 2 | Pasta do caso | Selecionar a pasta e ver o inventário de arquivos | RN01, RN02 |
| 3 | Extratores TXT e HTML | Aparelho, hash e SIMs extraídos do caso fictício | RN03, RN06, RN07 |
| 4 | Geração do Word | `.docx` gerado com os dados do Sprint 3 | RN12, RN13 |
| 5 | Tela de conferência | Perito confere e corrige cada dado com a origem ao lado | RN04 |
| 6 | Requisição em PDF | Dados do caso lidos do PDF com camada de texto | RN04 |
| 7 | Textos padronizados | Biblioteca e seleção de textos no laudo | RN08 |
| 8 | Quesitos e respostas | Quesitos numerados e respondidos no laudo | RN09, RN10 |
| 9 | Conferência automática e revisão | Bloqueios, alertas, revisão final e log | RN11, RN14 |
| 10 | OCR do PDF digitalizado | Texto extraído de PDF sem camada de texto | RN04 |
| 11 | Histórico, métricas e LGPD | CSV de tempos e correções, limpeza do caso | LGPD |
| 12 | Aceite e entrega | Roteiro de aceite cumprido, piloto iniciado | todas |
| 13 | (opcional) Laudo anterior como modelo | Converter um `.docx` antigo em modelo com marcadores | RN12 |
| Identidade e usabilidade | Feito em 02/11/2026. Casca de ferramenta, cabeçalho compacto, fonte condensada, densidade compacta, cantos suaves, superfícies planas e KPI em faixa; bancada do caso com os 6 passos à esquerda e o trabalho à direita, menu sem os passos do caso e cartões de caso na tela inicial. `python testes/testar.py` e `python testes/cenarios.py` passam. |

**MVP 100% pronto = Sprints 0 a 12.** O Sprint 10 (OCR) pode ser entregue como
"simulado", que é o que o formulário autoriza. Nesse caso, o perito digita os
dados com o PDF aberto ao lado.

---

## Sprint 0 · Preparação e linha de base

**Objetivo**: ter tudo o que o app precisa ler antes de escrever código.

- [x] Montar `exemplos/caso-ficticio-001/` com a mesma estrutura de uma pasta real:
      requisição em PDF (uma com texto e uma digitalizada), `DEVICE INFO.txt`,
      `HASHDOHASH.txt`, `OBJ 01-A/` e `OBJ 01-B/` com os HTML dos SIMs.
- [x] Montar `caso-ficticio-002/` **sem SIM** e `caso-ficticio-003/` com um
      arquivo faltando (para testar RN02 e RN06).
- [ ] Conferir com o perito o formato real dos TXT e HTML (amostra anonimizada)
      e anotar os rótulos exatos em `exemplos/FORMATOS.md`. _(premissa em [PREMISSAS.md](../PREMISSAS.md))_
- [ ] Copiar o modelo institucional para `modelos/modelo-laudo-celular.docx` e
      inserir os marcadores (`{numero_protocolo}`, `{imei_1}`, `{#sims}`...).
      Lista dos marcadores em `modelos/MARCADORES.md`. _(premissa em [PREMISSAS.md](../PREMISSAS.md))_
- [ ] Reunir os textos padronizados da Gerência em `exemplos/textos.json`
      (categoria, título, conteúdo), sem dados pessoais. _(premissa em [PREMISSAS.md](../PREMISSAS.md))_
- [x] Baixar pdf.js (build legada), PizZip e docxtemplater para `vendor/` e
      registrar versão e origem em `vendor/VERSOES.md`.
- [ ] Criar a planilha da linha de base (protocolo, início, fim, correções) e
      começar a medir os laudos manuais: **2 semanas**, que correm em paralelo
      aos Sprints 1 e 2. _(premissa em [PREMISSAS.md](../PREMISSAS.md))_

**Pronto quando**: o modelo `.docx` abre no Word com os marcadores visíveis e a
formatação oficial intacta, e a planilha já tem os primeiros laudos medidos.

## Sprint 1 · Esqueleto do app

**Objetivo**: o arquivo único abre, navega e guarda estado.

- [x] `index.html` com `<style>` e `<script>` internos, sem nenhum recurso externo.
- [x] Meta CSP: `default-src 'self' 'unsafe-inline' data: blob:; connect-src 'none'`.
- [x] Roteador por hash com as 10 rotas do `contexto.md` (telas vazias com título).
- [x] Camada `db` sobre IndexedDB (`agiliza_mais_v1`) com os 9 stores e funções
      `get`, `put`, `list`, `del`.
- [x] `navigator.storage.persist()` na primeira abertura.
- [x] Exportar e importar backup `.json` (`#/config`).
- [x] `embutir_libs.py` funcionando com marcadores `<!-- LIB:nome -->`.
- [x] Faixa fixa no topo: "Apoio à elaboração. A revisão e a aprovação são do perito."

**Pronto quando**: abrir por duplo clique, navegar pelas 10 rotas, criar um caso
de teste, fechar o navegador, reabrir e o caso continuar lá. O DevTools mostra
zero requisições de rede.

## Sprint 2 · Pasta do caso (RN01, RN02)

- [x] Botão "Selecionar pasta do caso" com `showDirectoryPicker({mode: "read"})`.
- [x] Alternativa com `<input type="file" webkitdirectory>` quando a API não existir.
- [x] Varredura recursiva e inventário: requisição PDF, `DEVICE INFO.txt`,
      `HASHDOHASH.txt`, pastas `OBJ xx-X` com HTML.
- [x] Tabela de inventário com status **presente**, **ausente**, **duplicado**.
- [x] Bloquear o avanço se faltar arquivo obrigatório, com a opção "informar
      manualmente" (exceção da RN02).
- [x] Criar o registro em `casos` e iniciar o cronômetro (`inicio_em`).

**Pronto quando**: os casos 001, 002 e 003 mostram o inventário certo, e o 003
acusa o arquivo ausente.

## Sprint 3 · Extratores TXT e HTML (RN03, RN06, RN07)

- [x] Leitor de texto que detecta UTF-8, UTF-16 e Windows-1252.
- [x] `extrairAparelho(txt)`: marca, modelo, IMEI 1, IMEI 2, cada um com `origem` e `linha`.
- [x] `extrairHash(txt)`: SHA-256 (64 hexadecimais) e nome do arquivo de referência.
- [x] `extrairSim(html, nomePasta)`: ICCID, operadora e identificador do objeto (`01-A`).
- [x] Todos os identificadores guardados como **texto** (sem perder zero à esquerda).
- [x] Validadores: Luhn para IMEI e ICCID, regex para SHA-256.
- [x] `testes/testes.html` com os casos fictícios: cada extrator tem pelo menos
      3 testes (valor certo, valor ausente, valor malformado).

**Pronto quando**: `testes.html` mostra todos os testes verdes, e o caso 002
retorna lista de SIMs vazia, sem erro.

## Sprint 4 · Geração do Word (RN12, RN13)

> Vem antes da conferência para provar cedo a parte mais arriscada: preservar o
> modelo oficial.

- [x] Embutir PizZip e docxtemplater.
- [x] Carregar o modelo em `#/config` e guardar como Blob no store `modelos`.
- [x] Listar os marcadores encontrados no modelo e acusar os que não têm dado.
- [x] Gerar o `.docx` com os dados do Sprint 3, com laço de SIMs e o bloco "sem SIM".
- [x] Gravar em `LAUDO_GERADO/laudo_<protocolo>_v<N>.docx`. Pedir permissão de
      escrita só nessa subpasta e nunca sobrescrever (incrementa `v<N>`).
- [x] Sem permissão de escrita: oferecer o download do arquivo.
- [x] Registrar em `laudos` (versão, data, nome).

**Pronto quando**: o laudo gerado abre no Word com a mesma formatação do modelo,
os 3 casos fictícios geram arquivos e a pasta original não muda (conferir a data
de modificação dos arquivos).

## Sprint 5 · Tela de conferência (RN04)

- [x] `#/dados` em duas colunas: campo editável e trecho de origem (arquivo + linha).
- [x] Selo por campo: **extraído**, **corrigido**, **digitado**, **confirmado**.
- [x] Validação em tempo real (Luhn, tamanho, obrigatório) com a mensagem ao lado do campo.
- [x] Adicionar e remover SIM à mão (RN06), com confirmação de "aparelho sem SIM".
- [x] Botão "Confirmar todos" só habilita quando os identificadores essenciais
      foram vistos um a um.
- [x] Cada alteração gera um registro em `conferencias`.
- [x] A geração (Sprint 4) passa a usar só dados confirmados.

**Pronto quando**: alterar um IMEI para um valor inválido bloqueia a confirmação,
e o log registra a alteração com data e hora.

## Sprint 6 · Requisição em PDF (texto)

- [x] Embutir pdf.js e o worker (via Blob URL, que funciona em `file://`).
- [x] Visualizar o PDF dentro de `#/dados`, ao lado dos campos do caso.
- [x] Extrair a camada de texto e aplicar as regex de protocolo, ofício,
      processo, autoridade e data da solicitação.
- [x] Detectar PDF **sem** camada de texto e avisar: "PDF digitalizado. Digite os
      dados olhando o documento ao lado" (o OCR chega no Sprint 10).

**Pronto quando**: o PDF fictício com texto preenche os 5 campos do caso, e o
digitalizado mostra o aviso com a visualização.

## Sprint 7 · Textos padronizados (RN08)

- [x] `#/biblioteca`: criar, editar, versionar e desativar textos por categoria
      (descrição dos objetos, exames, anexos, considerações).
- [x] Importar `textos.json` do Sprint 0 e exportar a biblioteca.
- [x] Marcadores dentro dos textos (`{marca}`, `{qtd_sims}`) preenchidos com os dados confirmados.
- [x] `#/textos`: para cada seção do laudo, escolher um texto, ver a prévia
      preenchida e editar só para este caso.
- [x] Sugestão de texto por condição (ex.: "sem SIM" quando a lista está vazia).

**Pronto quando**: escolher um texto de exame mostra a prévia com os dados do
caso e o texto aparece na seção certa do Word gerado.

## Sprint 8 · Quesitos e respostas (RN09, RN10)

- [x] Recortar o bloco de quesitos do texto do PDF e separar por numeração.
- [x] `#/quesitos`: lista editável (inserir, excluir, reordenar, renumerar).
- [x] Biblioteca de respostas-modelo, com sugestão por palavras-chave do enunciado
      (correspondência simples, que pode ficar simulada no MVP).
- [x] Toda resposta sugerida nasce como **"sugestão, não aprovada"** e só vai
      para o laudo depois que o perito marca "conferida" (RN10).
- [x] Laço `{#quesitos}` no modelo.

**Pronto quando**: os quesitos do PDF fictício aparecem numerados de 1 a N, e o
laudo não é gerado com resposta não conferida.

## Sprint 9 · Conferência automática e revisão final (RN11, RN14)

- [x] Validador geral com três níveis: **bloqueia**, **alerta**, **informa**
      (tabela no `contexto.md`, seção 8).
- [x] `#/gerar` mostra o relatório da conferência antes do botão "Gerar".
- [x] `#/revisao`: o perito abre o `.docx`, anota as correções feitas no Word,
      responde "exigiu correção após gerar?" e marca **revisado pelo perito**.
- [x] Só a marcação de revisão encerra o caso e para o cronômetro (`fim_em`).

**Pronto quando**: o caso 003 (arquivo faltando) gera alertas, e um caso com IMEI
inválido não chega à versão final.

## Sprint 10 · OCR do PDF digitalizado

- [ ] Avaliar o tamanho de Tesseract.js + `por.traineddata` (versão *fast*).
- [ ] Se o arquivo ficar acima de 15 MB, criar `ocr.html` separado, que
      devolve o texto para o app principal por copiar e colar ou por arquivo `.txt`.
- [ ] Rodar o OCR página a página, com barra de progresso.
- [ ] Usar o texto do OCR nas mesmas regex do Sprint 6. Todo campo vindo do OCR
      nasce com selo **"OCR, conferir"**.
- [x] Se o grupo decidir simular: registrar a decisão em `PROJETO.md` e manter o
      fluxo de digitação ao lado do PDF.

**Pronto quando**: o PDF digitalizado fictício preenche ao menos protocolo e
ofício, ou a decisão de simular está registrada.

## Sprint 11 · Histórico, métricas e LGPD

- [x] `#/historico`: casos, versões geradas, tempo de elaboração, correções.
- [x] Exportar `historico.csv` (UTF-8 com BOM, separador `;`).
- [x] Indicadores no topo: tempo médio, taxa de correção, campos corrigidos por caso.
- [x] Botão "Limpar dados do caso": apaga aparelho, SIMs, hash e quesitos e
      mantém só o registro de métricas.
- [x] Texto de privacidade em `#/config` (finalidade, retenção, base legal a validar).

**Pronto quando**: depois de 3 casos fictícios, o CSV abre no Excel com os tempos,
e a limpeza remove os dados pessoais do IndexedDB (conferir no DevTools).

## Sprint 12 · Aceite e entrega

- [ ] Rodar o **roteiro de aceite** com um perito, no computador da Gerência:
  1. Abrir `index.html` por duplo clique, sem internet.
  2. Selecionar a pasta do caso fictício.
  3. Conferir e corrigir um dado.
  4. Escolher textos e responder os quesitos.
  5. Gerar o `.docx`, abrir no Word e conferir as seis seções.
  6. Corrigir à mão e salvar.
  7. Confirmar que os arquivos originais não mudaram.
  8. Marcar como revisado.
- [ ] Corrigir o que o roteiro apontar.
- [x] `LEIA-ME` de uso em uma página (como abrir, como fazer backup, o que não fazer).
- [ ] Comparar a linha de base (Sprint 0) com os primeiros casos do app e
      registrar o resultado parcial do KPI de 30%.
- [ ] Atualizar `PROJETO.md` (marcos e situação) e o `README.md` da pasta.

**Pronto quando**: o perito cumpre os 8 passos sem ajuda, e o piloto está aberto.

## Início e gestão dos laudos (03/11/2026)

- [x] `#/inicio`: botão **Carregar a pasta do caso** (e o seletor do sistema) que inventaria os arquivos, cria o caso e abre a conferência; se faltar arquivo obrigatório, leva ao inventário.
- [x] Lista de laudos em preenchimento com **Continuar**, **Renomear**, **Pasta** e **Excluir**.
- [x] Pastas livres, com filtro por pasta e contagem por pasta; a pasta fica no caso e em `ag_pastas`.
- [x] Exclusão apaga o caso, o aparelho, os SIMs, os hashes, os quesitos, os laudos e as conferências, sem tocar nos arquivos originais.
- [x] Cenário `s12_inicio_pasta_e_gestao` (9/9) e `python testes/testar.py`.
- [ ] Testar com a pasta real do `CASO TESTE 2` (nomes de arquivo ainda fora do padrão; ver o `README.md` da pasta).

## Sprint 13 · (opcional, pós-MVP) Laudo anterior como modelo

- [ ] Abrir um laudo antigo `.docx` e listar os parágrafos.
- [ ] O perito seleciona trechos e associa cada um a um marcador.
- [ ] Salvar o resultado como novo modelo em `modelos`, sem alterar o laudo de origem.
- [ ] Verificar se sobrou algum dado do caso antigo (busca pelos IMEIs e ICCIDs antigos).

## Sprint 14 · Correções do feedback (03/11/2026)

> Feedback de Diego (nota 3). A carga da pasta e a gestão dos laudos já foram feitas; o foco aqui é o Word, a revisão e a edição dos textos.

### Código
- [x] Aceitar o modelo institucional em `.docx` e `.dotx` (o `.dotx` é convertido no carregamento).
- [ ] Inserir os marcadores no modelo timbrado da POLITEC e validar a formatação no Word.
- [x] Revisão: retirar "Correções feitas no Word" e "Quantidade de correções"; manter "Revisei o laudo e ele está pronto para assinatura", "Concluir o caso" e "Histórico e Metas".
- [x] Biblioteca: coluna e filtro de tipo de dispositivo; adaptação de texto por marcadores (local).
- [ ] IA externa para criar/adaptar texto. Premissa: a adaptação local por marcadores cobre o MVP; a IA externa fica para a versão institucional, com revisão humana e LGPD.
- [x] Conferência: a cor do aparelho é editável (já estava no formulário e o teste cobre).
- [x] Conferência: permitir outras informações do perito. (campo livre que entra nas considerações finais)
- [x] Textos: editar Histórico, Exames e Considerações por caso, sem mudar a biblioteca.
- [x] Quesitos: não impedir o laudo quando a requisição não tiver quesitos.
- [x] Corrigir o histórico. A tela ganhou o botão "Abrir" que retoma o caso; o cenário s14 cobre o caminho. A causa original não foi reproduzida; pedir o caso ao Diego se voltar.
- [x] Upload de foto do aparelho com sugestão de cor (assistida). A foto fica no navegador; o perito confirma a cor.
- [x] Esclarecer na tela o que cada arquivo da pasta alimenta.

### Decisão do setor
- [ ] Modelo institucional timbrado e os marcadores. O app aceita `.docx`/`.dotx` e avisa quando não há marcadores; falta o modelo oficial com os marcadores de `modelos/MARCADORES.md`.
- [ ] Uso de IA: local, autorizada e com LGPD; lista de tipos de dispositivo.
- [ ] Formato dos textos de Histórico, Exames e Considerações. O app permite editar por caso; o texto padrão oficial depende da Gerência.
- [ ] Testar com o caso real do `CASO TESTE 2`. Depende do perito e dos arquivos reais.

**Pronto quando**: um caso completo gera o Word timbrado sem ajuste manual de formatação, a revisão tem só os dois campos pedidos e os textos podem ser editados.

