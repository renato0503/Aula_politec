# Backlog da jornada do cliente

Erros encontrados na execução de `Apps/jornada.py`, para corrigir depois. Um
item por erro, com o ID, a severidade, a evidência e a sugestão.

O plano e a matriz estão em `Apps/JORNADA-TESTES.md`. A execução ainda não
começou; este arquivo é preenchido ao final de cada rodada.

## Formato

```markdown
### <APP>-<NN> · <título curto>

- **Severidade:** P0, P1, P2 ou P3
- **Perfil:** <perfil>
- **Viewport:** desktop 1366×900 ou celular 390×844
- **Rota:** `#/...`
- **Passo:** <o que a pessoa fazia>
- **Esperado:** <o que deveria acontecer>
- **Observado:** <o que aconteceu>
- **Console/rede:** <erros>
- **Captura:** `_testes/jornada/<app>/...png`
- **Sugestão:** <onde corrigir>
```

## Em aberto

### inscricoes-cursos-01 · a Diretoria abre em tela em construção (P1)

- **Severidade:** P1
- **Perfil:** diretoria
- **Rota:** `#/triagem`
- **Passo:** trocar para o perfil Diretoria e abrir o app.
- **Esperado:** uma tela de trabalho (Triagem).
- **Observado:** "Triagem · Esta tela ainda está em construção"; o perfil não tem tela pronta.
- **Sugestão:** construir a Triagem ou trocar o `inicio` do perfil para uma tela pronta; enquanto isso, esconder o perfil.

## Encontrados na avaliação crítica (abertos)

| ID | App | Sev | Achado |
|---|---|---|---|
| agiliza-mais-01 | agiliza-mais | P2 | A barra mostra 6 passos, mas Textos, Quesitos, Gerar e Revisão não têm tela; o clique leva a "em construção". |
| renovacao-contratos-horus-01 | renovacao-contratos-horus | P2 | O seed não tem fiscais; "Meus contratos" fica vazio até alguém substituir o fiscal. |
| distribuicao-casos-dna-01 | distribuicao-casos-dna | P2 | A placa de 96 poços é visual; os poços não abrem o caso. |
| metas-bi-ocr-01 | metas-bi-ocr | P2 | Conferência e geração só são alcançadas pelo cartão do mês, fora do menu. |
| equipamentos-google-earth-01 | equipamentos-google-earth | P2 | Mapa estático, sem zoom/arrastar; pinos se sobrepõem e a lista não pagina. |
| horus-banco-demandas-01 | horus-banco-demandas | P2 | O contexto de unidade fica escondido dentro do menu de perfil. |
| controle-aquisicoes-01 | controle-aquisicoes | P2 | O kanban de 9 colunas exige rolagem horizontal no celular. |
| documentapolitec-01 | documentapolitec | P2 | Cada Enter da conferência redesenha a ficha inteira e devolve o foco ao campo. |
| comissao-etica-denuncias-01 | comissao-etica-denuncias | P2 | O funil tem 7 etapas e a barra do caso tem 6; os nomes não coincidem. |
| tap-portfolio-projetos-01 | tap-portfolio-projetos | P2 | A matriz não tem escala nos eixos; pontos próximos se sobrepõem. |
| passivo-ambiental-01 | passivo-ambiental | P2 | A fila do perito não tem busca nem filtro de atrasados. |
| adiantamento-01 | adiantamento | P2 | Sem perfis e sem "Minha fila" por papel. |
| gestao-documentos-01 | gestao-documentos | P2 | O aviso de que a assinatura é da autoridade só aparece na aba Conclusão. |
| custodia-definitiva-01 | custodia-definitiva | P2 | A prateleira leva ao acervo filtrado, não à ficha do contêiner. |

## Limitações do navegador (não são bugs do app)

- **cin-segunda-via**: o Lightpanda não reduz a imagem de teste
  (`createImageBitmap`/canvas), então o pedido não chega ao protocolo.
- **agiliza-mais**: o Lightpanda não aceita upload de pasta (`webkitdirectory`).
- Nos dois casos, o Chromium conclui a jornada.

## Corrigidos nesta rodada

### rnc-nao-conformidade-01 · contexto de setor não preenche Minhas RNCs

- **Severidade:** P1
- **Perfil:** setor
- **Viewport:** desktop 1366×900
- **Rota:** `#/minhas`
- **Passo:** escolher o setor no menu do perfil e abrir Minhas RNCs.
- **Esperado:** o seletor `#rncMeuSetor` vir preenchido com o setor escolhido.
- **Observado:** o seletor veio vazio e a tabela só apareceu depois de escolher o setor na tela.
- **Console/rede:** nenhum.
- **Captura:** `_testes/jornada/rnc-nao-conformidade/desktop-o-contexto-de-setor-n-o-preenche-minhas-rncs.png`
- **Correção:** o contexto passou a gravar `setor` (e `meu_setor`); jornada repetida com 0 erros.
- **Sugestão original:** em `Apps/rnc-nao-conformidade/src/identidade.js`, o contexto grava `meu_setor`, mas a tela lê `setor`. Gravar em `setor` (ou ler os dois) e regerar o `index.html`.


