# Contrato do módulo de desaparecidos

O módulo de desaparecidos está sendo construído por **outra IA**, com dados
públicos, dentro do MVP do NIHDE. Este documento fixa a fronteira para as duas
partes não se atropelarem.

## Quem é dono do quê

| Caminho | Dono | O que é |
|---|---|---|
| `src/app.js`, `app.json` (rotas atuais), `exemplos/seed.json` | este app | Corpos não identificados e não reclamados, exames, família, sepultamento e relatório |
| `src/desaparecidos.js` | outra IA | Tela, filtros e correspondência com os desaparecidos |
| `desaparecidos.html` | outra IA | Painel público do CNPD/MJ gerado por `gerar_painel.py` |
| `painel/template.html`, `gerar_painel.py`, `api_cnpd.py`, `coletar_dados.py` | outra IA | Template, gerador e coleta do CNPD |
| `dados/`, `RedePCIConecta.*`, `vendor/leaflet/` | outra IA | Dados públicos, análise e mapa |
| `dados/desaparecidos-publicos.json` | outra IA | Base pública coletada, com fonte e data |
| `index.html` | este app | App do NIHDE, gerado por `construir.py` |
| `docs/CONTRATO-DESAPARECIDOS.md` | as duas | Este contrato |

O `construir.py` junta `src/*.js` em ordem alfabética (depois de `app.js` e antes
de `identidade.js`). O arquivo `src/desaparecidos.js` entra sem mudar o build.

## O que este app oferece

A lista de corpos não identificados, com os campos que servem para a comparação:

| Campo | Exemplo | Uso |
|---|---|---|
| `id` | `C-0007` | Chave do corpo |
| `protocolo` | `2026.0007` | Referência do Atena |
| `sexo` | `Feminino` | Primeiro filtro |
| `idade` | `35` | Faixa de ±5 anos |
| `altura` | `1,65` | Faixa de ±10 cm |
| `olhos`, `cabelo`, `pele` | `castanhos`, `preto`, `parda` | Características |
| `sinais` | `cicatriz no braço` | Texto livre |
| `municipio`, `local` | `Cuiabá` | Onde foi encontrado |
| `data_localizacao` | `2026-09-12` | Janela de desaparecimento |
| `situacao` | `não identificado` | Só entra quem não está identificado |

A tela do módulo pode ler `db.list("corpos")` diretamente. Não é preciso exportar
nada deste app.

## O que o módulo deve trazer

Dados públicos de desaparecidos, com pelo menos:

`id_publico, nome, idade, sexo, data_desaparecimento, municipio, bairro,
caracteristicas, fonte, url, coletado_em`.

Regras:

- **Fonte e data** em cada linha; sem fonte, a linha não entra.
- **Dado público não é dado livre**: a base precisa de finalidade, acesso restrito
  e registro de consulta. O módulo deve avisar que a correspondência é indício,
  não identificação.
- **Nunca identificar automaticamente.** A sugestão passa por um servidor do
  NIHDE, que confirma ou descarta, com justificativa na auditoria.
- **Não misturar** a base pública com o cadastro do corpo. São stores separados.
- A lista de desaparecidos não deve aparecer para o perfil `iml` sem necessidade;
  a consulta fica com `nihde` e `gestor`.

## Correspondência sugerida

1. Filtrar por sexo e faixa de idade (±5 anos).
2. Filtrar por município/região e janela de datas (desaparecimento antes da
   localização do corpo).
3. Pontuar altura (±10 cm), olhos, cabelo, pele e sinais.
4. Mostrar no máximo 10 candidatos, com o motivo do match.
5. O servidor confirma, descarta ou pede exame complementar; tudo vai para o
   `log` do corpo.

## Rota e menu

- O painel público fica em `desaparecidos.html`, separado do `index.html` do app.
  O `gerar_painel.py` grava nesse arquivo; nunca no `index.html`.
- A outra IA pode publicar a rota `#/desaparecidos` ou manter a página separada.
  O `app.json` é deste app; a rota nova deve ser combinada antes de entrar.
- A tela pode abrir a ficha do corpo (`#/corpo/:id`) e a ficha do desaparecido.

## Testes

- O módulo deve ter cenário próprio em `testes/cenarios.py` (ou arquivo separado)
  e não pode quebrar `testar.py` nem os três cenários atuais.
- A base pública é fictícia nos testes; nenhum dado real de pessoa desaparecida
  entra no repositório.

## Atualização de 03/11/2026 (executada)

- A rota **`#/desaparecidos`** entrou no `app.json` a pedido do professor, com
  acesso restrito aos perfis **`nihde`** e **`gestor`** (`perfis` na rota). O
  perfil `iml` não vê a tela no menu e recebe o aviso de permissão.
- A base pública real está em **`dados/cnpd-snapshot.json`** e
  **`dados/namus-snapshot.json`**, com fonte, data e URL em cada arquivo. Não
  existe `dados/desaparecidos-publicos.json`; os nomes acima são os usados pelo
  módulo. Nenhum campo privado ou sensível foi acrescentado: só o que o painel
  público do CNPD e a API pública do NamUs já publicam.
- O painel standalone é **`desaparecidos.html`**, gerado por `gerar_painel.py`;
  ele não sobrescreve o `index.html` do app.
- O módulo tem cenário próprio em `testes/cenarios.py`
  (`s4_desaparecidos_e_fontes`) e testes embutidos em `#/testes`. Os testes
  usam os snapshots públicos apenas para conferir estrutura, cobertura e mapa;
  não criam dados novos de pessoas.
- A tela mostra a fonte e a data da coleta e avisa que a correspondência é
  indício, não identificação. O cruzamento com os corpos do NIHDE continua
  sendo fase 2 e exige revisão humana/auditoria.


## Atualização de 03/11/2026 · cruzamento executado

- O botão **Ver corpos** na tabela de desaparecidos abre até 10 corpos não
  identificados, com o motivo do match (sexo, idade ±5, altura ±10 cm,
  município, janela de datas e características).
- A decisão humana é **confirmado**, **descartado** ou **exame complementar**,
  sempre com justificativa de pelo menos 20 caracteres.
- Cada decisão entra na loja **`correspondencias`** (índices por
  `desaparecido_id` e `corpo_id`) e no array `correspondencias` do corpo, além
  do `log` global com `corpo_id` e `desaparecido_id`.
- O módulo continua lendo `db.list("corpos")`; nenhum dado público foi misturado
  ao cadastro do corpo e nenhuma identificação é automática.
