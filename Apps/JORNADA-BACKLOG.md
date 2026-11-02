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
- **Sugestão:** em `Apps/rnc-nao-conformidade/src/identidade.js`, o contexto grava `meu_setor`, mas a tela lê `setor`. Gravar em `setor` (ou ler os dois) e regerar o `index.html`.

## Corrigidos nesta rodada

Nenhum.
