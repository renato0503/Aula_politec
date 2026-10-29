# DOCUMENTAPOLITEC · prontuários civis ao arquivo central

Conferência da relação de prontuários de cada caixa com o arquivo digital, lacre
da caixa e busca do prontuário. O papiloscopista continua atestando a veracidade e
assinando o lacre.

| Campo | Valor |
|---|---|
| Equipe | Aline Xavier dos Passos |
| Contato | alinepassos@politec.mt.gov.br |
| Unidade | Coordenadoria de Patrimônio e Serviços |
| Tipo | Aplicativo (app) para cidadão, servidor ou equipe |
| Stack | HTML único (CSS/JS inline), IndexedDB, GitHub Pages |
| Fonte | `Aula 8/Entregas/DOCUMENTAPOLITEC-2026-10-27 (1).json` (29/10/2026 11:47) |
| GitHub | `alinepassos-source` (Aline) |

## Arquivos

- `envio-original.json`: o envio, sem alteração.
- `projeto.json` e `PROJETO.md`: o envio completado. O envio tinha campos vazios
  (AS-IS, artefatos, entidades, regras, fontes, métricas, hospedagem e riscos);
  a proposta está em `contexto.md` e precisa ser confirmada no Sprint 0.
- `contexto.md` e `sprint.md`: arquitetura e plano de construção.
- `app.json`, `src/app.js`, `exemplos/`, `index.html`.

## Pendências

- Confirmar o formato do número do prontuário e o modelo das caixas (a equipe
  ainda vai definir os dígitos).
- Receber a planilha de teste com a relação de 850 prontuários para calibrar a
  importação (hoje a relação é colada como texto).
- A leitura do PDF digitalizado e a conferência automática por OCR ficam para o
  Sprint 3; a integração com o SIC está fora do MVP.
- A linha de base de 1.000 caixas e 2,5 milhões de prontuários precisa ser medida.

## Completado pelo professor (29/10/2026)

O `projeto.json` e o `PROJETO.md` desta pasta foram completados com propostas próximas do
que o aluno escreveu. O envio original está em `envio-original.json`.
Tudo o que foi completado precisa ser confirmado com o aluno no Sprint 0.

**Campos preenchidos (estavam vazios):** `asis_excecoes`, `doc_faltando`.

**Campos substituídos:**

- `mvp_plataforma`: O envio dizia apenas 'aplicativo' e não definia o objetivo do MVP; alinhado à arquitetura do curso (HTML único, offline first).
- `stack_detalhe`: O envio dizia apenas 'aplicativo' e não definia o objetivo do MVP; alinhado à arquitetura do curso (HTML único, offline first).
- `mvp_objetivo`: O envio dizia apenas 'aplicativo' e não definia o objetivo do MVP; alinhado à arquitetura do curso (HTML único, offline first).

**Tabelas:**

- AS-IS (`tAsIs`): refeita. O AS-IS estava vazio; descrito a partir do relato do envio.
- TO-BE (`tToBe`): linhas acrescentadas. O envio trazia uma linha; acrescentadas a busca e o lacre.
- papéis (`tPapeis`): refeita. Os papéis estavam vazios; descritos a partir do relato.
- telas e artefatos (`tArtefatos`): refeita. Os artefatos estavam vazios; acrescentadas as telas do protótipo, com rotas.
- entidades (`tEntidades`): refeita. As entidades estavam vazias; criadas a partir do modelo do app.
- regras de negócio (`tRegras`): refeita. As regras estavam vazias; criadas as três regras do protótipo.
- fontes de dados (`tFontes`): refeita. As fontes estavam vazias; descritas a partir do envio.
- métricas (`tMetricas`): refeita. As métricas estavam vazias; definidas as duas da defesa.
- hospedagem (`tHospedagem`): refeita. A hospedagem estava vazia; alinhada à arquitetura do curso.
- marcos (`tMarcos`): linhas acrescentadas. O envio trazia só o marco inicial.
- riscos (`tRiscos`): refeita. O risco único estava sem mitigação; acrescentados os riscos da conferência e do volume.
- referências (`tRefs`): refeita. As referências estavam vazias.
