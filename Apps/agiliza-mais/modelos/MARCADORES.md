# Marcadores do modelo

Sintaxe do docxtemplater: `{campo}` troca pelo valor; `{#lista}...{/lista}` repete para cada item; `{^lista}...{/lista}` aparece quando a lista está vazia.

O `modelo-laudo-celular.docx` é **fictício**. No Sprint 0, os mesmos marcadores entram no modelo institucional, escritos de uma vez (sem formatação no meio do marcador, para o Word não dividir o texto em vários trechos).

O layout institucional enviado em 03/11/2026 está em `../CASO TESTE 2/MODELO DE LAUDO - Projeto.dotx`. Ele **ainda não tem marcadores**: para usá-lo, copie para `.docx`, insira os marcadores desta tabela e carregue em `#/config`. O passo a passo e o inventário do caso de teste estão em `../CASO TESTE 2/README.md`.

| Marcador | Origem |
|---|---|
| `autoridade_solicitante` | requisição em PDF |
| `cor` | DEVICE INFO.txt |
| `data_laudo` | perito |
| `data_solicitacao` | requisição em PDF |
| `enunciado` | requisição + resposta conferida pelo perito |
| `hash_algoritmo` | HASHDOHASH.txt |
| `hash_arquivo` | HASHDOHASH.txt |
| `iccid` | HTML das pastas OBJ |
| `identificador_objeto` | HTML das pastas OBJ |
| `imei_1` | DEVICE INFO.txt |
| `imei_2` | DEVICE INFO.txt |
| `marca` | DEVICE INFO.txt |
| `modelo` | DEVICE INFO.txt |
| `nome_perito` | perito |
| `numero_laudo` | perito |
| `numero_oficio` | requisição em PDF |
| `numero_processo` | requisição em PDF |
| `numero_protocolo` | requisição em PDF |
| `numero_quesito` | requisição + resposta conferida pelo perito |
| `operadora` | HTML das pastas OBJ |
| `quesitos` | requisição + resposta conferida pelo perito |
| `resposta` | requisição + resposta conferida pelo perito |
| `sims` | HTML das pastas OBJ |
| `texto_anexos` | biblioteca de textos padronizados |
| `texto_consideracoes` | biblioteca de textos padronizados |
| `texto_descricao_objetos` | biblioteca de textos padronizados |
| `texto_exames` | biblioteca de textos padronizados |
| `texto_historico` | biblioteca de textos padronizados |
| `texto_sem_sim` | biblioteca de textos padronizados |
| `valor_hash` | HASHDOHASH.txt |
| `numero_requisicao` | requisição em PDF (REQUISIÇÃO DE PERÍCIA Nº) |
| `natureza_exame` | requisição em PDF |
| `procedimento` | requisição em PDF (I.P.) |
| `boletim_ocorrencia` | requisição em PDF |
| `enquadramento` | requisição em PDF |
| `destinacao_laudo` | requisição em PDF |
| `data_fato` | requisição em PDF |
| `local_fato` | requisição em PDF |
| `itens_requisicao` | lista dos itens a periciar: `{#itens_requisicao}{numero_item}. {descricao} · lacre {lacre}{/itens_requisicao}`; também `identificador`, `imei` e `codigo_apreensao` |
| `qtd_itens` | quantidade de itens a periciar |
