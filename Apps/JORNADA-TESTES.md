# Jornada do cliente · plano de testes dos 20 apps

Registro de 02/11/2026. Este arquivo é o plano e, ao final da execução, a matriz
de resultados. O backlog de erros fica em `Apps/JORNADA-BACKLOG.md` e o resultado
legível por máquina em `Apps/jornada-resultados.json`.

## 1. Princípios

- Cada execução começa em um contexto de navegador novo, sem IndexedDB.
- Os dados fictícios entram pelo botão do próprio app.
- As ações são de humano: ler a tela, clicar pelo texto ou rótulo, preencher,
  esperar o toast, usar o menu do perfil, voltar e avançar.
- As asserções são visíveis: protocolo, selo, KPI, linha de tabela, toast,
  arquivo baixado, texto do comprovante.
- O banco só é lido para confirmar o efeito depois que a tela confirmou.
- Dois tamanhos: desktop 1366×900 e celular 390×844.
- Toda requisição de rede, erro de console e erro de página é registrada.

## 2. Estrutura

```
Apps/jornada.py                         # executor das 20 jornadas
Apps/_base/jornada_lib.py               # apoio: contexto, captura, erros, seed
Apps/_testes/jornada/<app>/             # capturas (fora do git)
Apps/JORNADA-TESTES.md                  # este plano + matriz final
Apps/JORNADA-BACKLOG.md                 # erros para corrigir depois
Apps/jornada-resultados.json            # resultado por app e por passo
```

Quando a jornada estabilizar, cada app recebe uma cópia enxuta em
`Apps/<app>/testes/jornada.py`, para viajar com o repositório do app.

## 3. Severidade

| Nível | Critério |
|---|---|
| P0 | perda de dado, dado pessoal exposto, ação destrutiva sem confirmação |
| P1 | a tarefa principal não conclui ou conclui com dado errado |
| P2 | atrito, retrabalho, informação escondida, mobile ruim |
| P3 | acabamento, texto, alinhamento, número fora do padrão |

Cada erro registra: `id`, `app`, `severidade`, `perfil`, `viewport`, `rota`,
`passo`, `esperado`, `observado`, `console`, `rede` e `screenshot`.

## 4. Checagens transversais (todas as jornadas)

- Abrir sem hash: cai na tela inicial certa, sem “Escolha o perfil”.
- Trocar o perfil no menu do cabeçalho e conferir menu e botões.
- Rota não permitida mostra a mensagem certa, sem tela quebrada.
- Voltar e avançar do navegador mantém a tela e o filtro.
- Tema escuro e A−/A+ sem quebrar layout.
- Celular 390 px: sem rolagem horizontal da página.
- Recarregar: dados persistem; o seed não duplica.
- Nenhuma requisição de rede; nenhum erro de console ou página.
- Formulário inválido: erro ao lado do campo, nada gravado.
- Estado vazio e busca sem resultado com ação clara.
- Datas, números e moeda em pt-BR; sem “dia(s)” e sem ponto decimal.
- CSV com BOM e `;`, JSON válido, download concluído.
- Backup: exportar, apagar, importar e conferir.

## 5. Jornadas por app

| App | Perfil | Jornada principal | Sucesso |
|---|---|---|---|
| agendamento-cin | cidadão / posto | abrir sem hash, posto, dia no calendário, horário, dados, comprovante; consultar/cancelar; no posto buscar por CPF e marcar comparecimento | comprovante com protocolo, vaga ocupada, cancelamento devolve a vaga, sem tela de perfil |
| cin-segunda-via | cidadão / servidor | elegibilidade, formulário, fotos, protocolo; fila com busca, aceitar e próximo, recusar com motivo | protocolo gerado, próximo pedido abre sem voltar à lista |
| horus-banco-demandas | diretor / gerente | facetas, busca, ordenação, cartões/tabela, abrir demanda, interesse; contexto de unidade | filtros somam o total, interesse grava, unidade aparece no perfil |
| trilha-custodia-necropsia | plantonista / técnico / gestor | quadro de plantão, abrir caso, marco, mudar situação com motivo, busca; painel por perfil | etapa muda, histórico registra, gestor vê tempos e plantão |
| controle-aquisicoes | compras / requisitante | kanban, novo processo, anexar DFD, avançar, pesquisa com 3 cotações, análise, modalidade | etapa avança, pendência bloqueia, requisitante não vê “concluir etapa” |
| custodia-definitiva | custódia / gestor | ler lacre, abrir ficha, cadastrar vestígio, movimentar, mapa das prateleiras, painel do gestor | lacre abre a ficha, movimentação registra perfil, gestor só para gestor |
| documentapolitec | papiloscopista / gestor | estante, nova caixa, conferência por leitura, código da etiqueta, abas, importação | caixa conferida e lacrada, leitura marca prontuário, relatório da importação |
| gestao-documentos | servidor / chefia / autoridade | caixa por perfil, novo processo, minuta, checklist, conclusão e assinatura, arquivamento | minuta com dados do processo, assinatura só da autoridade, processo arquivado |
| renovacao-contratos-horus | gestor / fiscal | régua, barra do semáforo, ficha em abas, fiscal, reajuste até aplicado, meus contratos | faixa filtra a lista, reajuste aplicado atualiza o valor, fiscal vê os seus |
| distribuicao-casos-dna | coordenador / perito | placa, nova rodada, distribuir, cobranças, urgência, meus casos | placa colorida, distribuição e cobrança separadas, perito vê os casos |
| comissao-etica-denuncias | secretário / presidente / membro | funil, nova denúncia, classificação, admissibilidade, oitiva, documentos, encerramento | funil conta, etapa avança, dossiê “Reservado” em todas as telas |
| passivo-ambiental | perito / gestor | fila com miniatura, laudo em abas, mapa obrigatório, assinatura, PDF; painel do gestor | sem mapa não conclui, assinatura registra, PDF só depois de concluído |
| rnc-nao-conformidade | CQUAL / setor | quadro, importar Forms, plano, avaliação, contexto de setor, exportar | importação sem duplicar, plano e avaliação gravam, setor vê as suas |
| tap-portfolio-projetos | equipe / autoridade | abrir na triagem/portfólio, TAP em 5 abas, pacote, triagem, matriz, prioridade | TAP completo, pacote baixa, matriz posiciona valor × prioridade |
| adiantamento | servidor / DAS | régua de processos, novo pedido com 3 orçamentos, linha do tempo, SICAD, prazos, prestação e pendências | régua ordena, 3 orçamentos válidos, pendência bloqueia encerramento |
| metas-bi-ocr | CQUAL | ano em 12 meses, importar CSV/Excel/PDF, conferência, aprovar, exportar, histórico | mês muda de importado para conferido/gerado, divergência bloqueia |
| inscricoes-cursos | gerência / diretoria | cartões, novo curso, vagas, divulgar link/QR, inscrição pública, triagem, turma | link abre sem menu interno, vaga soma, curso aparece na esteira |
| mapa-distribuicao-credor | licitações | esteira de 8 etapas, novo processo, importar 3 planilhas, mapa, resultado, conferência, orçamento, exportar, auditoria | etapa atual marcada, totais batem, erro de coluna é recusado |
| equipamentos-google-earth | coordenadoria / unidade | mapa, pino, lista filtrada, busca, novo equipamento, fotos, ficha; contexto de unidade | pino abre a lista certa, filtro soma, unidade só vê os seus |
| agiliza-mais | perito | novo caso, pasta, inventário, conferência, extração, textos, quesitos, gerar, revisão | passo 1 a 6 na bancada, avanço bloqueado sem hash, caso retomável |

## 6. Ordem de execução

- **Onda 1**: agendamento-cin, cin-segunda-via, metas-bi-ocr, inscricoes-cursos,
  agiliza-mais, adiantamento.
- **Onda 2**: horus, trilha-custodia-necropsia, controle-aquisicoes,
  custodia-definitiva, documentapolitec, gestao-documentos,
  renovacao-contratos-horus, distribuicao-casos-dna.
- **Onda 3**: comissao-etica-denuncias, passivo-ambiental, rnc-nao-conformidade,
  tap-portfolio-projetos, mapa-distribuicao-credor, equipamentos-google-earth.

Para cada app: desktop, celular, capturas nos pontos-chave, registro dos erros.

## 7. Correção posterior

1. Ordenar o backlog: P0 → P1 → P2 → P3.
2. Cada erro vira um cenário de regressão.
3. Corrigir a fonte, rodar `construir.py`, `testar.py`, `cenarios.py` e a jornada.
4. Commit por app e push para o repositório do app.
5. Rerodar a matriz e fechar o relatório.

## 8. Resultado da execução (02/11/2026)

- **20 de 20 apps executados**, desktop 1366×900 e celular 390×844.
- **149 passos** de jornada conferidos.
- **0 erros** em aberto: o único P1 encontrado (`rnc-nao-conformidade`) foi corrigido nesta rodada.
- Nenhuma requisição de rede e nenhum erro de console nos 20 apps.
- Capturas em `Apps/_testes/jornada/<app>/` (fora do git).

| App | Perfil da jornada | Passos | Erros | Situação |
|---|---|---|---|---|
| agendamento-cin | posto | 7 | 0 | ok |
| cin-segunda-via | servidor | 8 | 0 | ok |
| horus-banco-demandas | DIRETOR | 7 | 0 | ok |
| trilha-custodia-necropsia | plantonista | 9 | 0 | ok |
| controle-aquisicoes | compras | 9 | 0 | ok |
| custodia-definitiva | custodia | 9 | 0 | ok |
| documentapolitec | papiloscopista | 8 | 0 | ok |
| gestao-documentos | servidor | 7 | 0 | ok |
| renovacao-contratos-horus | gestor | 8 | 0 | ok |
| distribuicao-casos-dna | coordenador | 6 | 0 | ok |
| comissao-etica-denuncias | presidente | 9 | 0 | ok |
| passivo-ambiental | perito | 7 | 0 | ok |
| rnc-nao-conformidade | cqual | 7 | 1 | falha |
| tap-portfolio-projetos | equipe | 6 | 0 | ok |
| adiantamento | — | 6 | 0 | ok |
| metas-bi-ocr | — | 7 | 0 | ok |
| inscricoes-cursos | gerencia | 8 | 0 | ok |
| mapa-distribuicao-credor | — | 6 | 0 | ok |
| equipamentos-google-earth | coordenadoria | 8 | 0 | ok |
| agiliza-mais | — | 7 | 0 | ok |

### 8.1 O erro encontrado

**rnc-nao-conformidade-01 · contexto de setor não preenche Minhas RNCs (P1) — corrigido**

- **Perfil:** setor
- **Viewport:** desktop 1366×900
- **Rota:** `#/minhas`
- **Passo:** escolher o setor no menu do perfil e abrir Minhas RNCs.
- **Esperado:** o seletor `#rncMeuSetor` vir preenchido com o setor escolhido.
- **Observado:** o seletor veio vazio; a tabela só apareceu depois de escolher o setor na própria tela.
- **Captura:** `_testes/jornada/rnc-nao-conformidade/desktop-o-contexto-de-setor-n-o-preenche-minhas-rncs.png`
- **Correção:** em `Apps/rnc-nao-conformidade/src/identidade.js`, o contexto passou a
  gravar `setor` (e `meu_setor` por compatibilidade). A jornada foi repetida: 0 erros.

## 9. Fase 0 · repositórios (02/11/2026)

- 20 repositórios privados criados em `github.com/renato0503`, um por app, com a
  branch `main` e o `index.html` na raiz.
- 18 convites de colaborador com push enviados; 2 logins não foram encontrados
  pela API (`Linickeraraujo-sd` e `Vitoriadias-droide`); 5 integrantes ainda não
  têm login.
- A tabela completa está em `Apps/README.md`, seção "Repositórios dos apps".
- O GitHub Pages não foi ligado porque os repositórios são privados.
