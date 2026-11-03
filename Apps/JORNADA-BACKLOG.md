# Backlog da jornada do cliente

Erros encontrados na execução de `Apps/jornada.py`, para corrigir depois. Um
item por erro, com o ID, a severidade, a evidência e a sugestão.

O plano e a matriz estão em `Apps/JORNADA-TESTES.md`. A execução de 02/11/2026
(com o TEIA em 03/11/2026) está registrada lá; este arquivo lista o que ficou
em aberto e o que foi corrigido.

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

| ID | App | Sev | Achado |
|---|---|---|---|
| tap-portfolio-projetos-01 | tap-portfolio-projetos | P2 | A matriz não tem escala numérica nos eixos; pontos próximos se sobrepõem. |
| comissao-etica-denuncias-01 | comissao-etica-denuncias | P2 | O funil tem 7 etapas e a barra do caso tem 6; os nomes não coincidem. |
| adiantamento-01 | adiantamento | P2 | Sem perfis e sem “Minha fila” por papel. |
| documentapolitec-01 | documentapolitec | P2 | Cada Enter da conferência redesenha a ficha inteira. |
| custodia-definitiva-01 | custodia-definitiva | P2 | A prateleira leva ao acervo filtrado, não à ficha do contêiner. |
| controle-aquisicoes-01 | controle-aquisicoes | P2 | O kanban de 9 colunas exige rolagem horizontal no celular. |
| horus-banco-demandas-01 | horus-banco-demandas | P2 | O contexto de unidade aparece no subtítulo, mas o seletor continua dentro do menu de perfil. |
| metas-bi-ocr-01 | metas-bi-ocr | P2 | Conferência e geração ainda ficam no cartão do mês, fora do menu. |
| agiliza-mais-01 | agiliza-mais | P2 | O menu mostra Casos e Configuração; Biblioteca e Histórico ainda não existem. |
| renovacao-contratos-horus-01 | renovacao-contratos-horus | P2 | “Meus contratos” depende de digitar o nome do fiscal (agora com lista de sugestões). |

## Corrigidos nesta rodada

- `rnc-nao-conformidade-01` (P1): contexto de setor passa a preencher Minhas RNCs.
- `inscricoes-cursos-01` (P1): a Diretoria abre na Triagem, com vagas e inscrições por diretoria.
- `inscricoes-cursos-02` (P1/A14): “＋ Novo curso” abre o formulário; a esteira marca “em breve” nos passos sem tela.
- `mapa-distribuicao-credor-01` (P1): a importação ganhou a tabela de 3 linhas, com arquivo, situação e linhas lidas.
- `equipamentos-google-earth-01` (P1): a lista pagina de 25 em 25.
- `metas-bi-ocr-01` (P1): botão “Usar arquivo de exemplo” com o CSV de julho/2026.
- `agiliza-mais-01` (P1): os passos sem `TELAS` aparecem como “em breve”, sem link; botão de caso de exemplo.
- `renovacao-contratos-horus-01` (P2): o seed agora tem três fiscais; o botão “Substituir o fiscal” deixou de disparar submit.
- `distribuicao-casos-dna-01` (P2): clicar no poço mostra protocolo, perito e tipo.
- `gestao-documentos-01` (P2): o aviso da autoridade aparece no topo da ficha e na aba.
- `passivo-ambiental-01` (P2): a fila do perito ganhou busca e filtro “só atrasados”.
- `controle-aquisicoes-02` (P2): o botão “Abrir pendência” deixou de disparar submit.


## TEIA e operação (03/11/2026)

| ID | App | Sev | Achado |
|---|---|---|---|
| teia-triagem-emails-01 | teia-triagem-emails | P2 | A extração é simulada; faltam parsing real de e-mail/PDF, OCR e renomeação de arquivos. |
| teia-triagem-emails-02 | teia-triagem-emails | P3 | O botão de integração com a caixa institucional ainda é local; o passo a passo está em `AJUDA_TECNICA`. |
| operacao-01 | todos | P1 | Dois logins não existem na API (`Linickeraraujo-sd`, `Vitoriadias-droide`) e cinco alunos não têm login. |
| operacao-02 | todos | P2 | O GitHub Pages não foi ligado nos 21 repositórios públicos. |
| operacao-03 | teia-triagem-emails, distribuicao-casos-dna | P2 | O convite de push do Nelson está pendente de aceite. |

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


