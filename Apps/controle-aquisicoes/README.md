# Controle do Processo de Aquisição

Painel das aquisições da POLITEC, do DFD à definição da modalidade, com etapas,
documentos exigidos, responsáveis, prazos e pendências. A decisão e a aprovação
continuam com os agentes públicos.

| Campo | Valor |
|---|---|
| Equipe | Kasteline Gonçalves |
| Contato | kastelinesilva@politec.mt.gov.br |
| Unidade | Aquisição |
| Tipo | Painel de Business Intelligence (dashboard) |
| Stack | HTML único (CSS/JS inline), IndexedDB, GitHub Pages |
| Fonte | `Aula 8/Entregas/Controle-do-processo-de-aquisio-2026-10-27 (4).json` (29/10/2026) |
| GitHub | `kastelinesilva-netizen` (Kasteline) |

## Arquivos

- `envio-original.json`: o envio, sem alteração.
- `projeto.json` e `PROJETO.md`: o envio completado. As tabelas do envio estavam
  em uma linha só; foram refeitas a partir dos campos e do relato.
- `contexto.md` e `sprint.md`: arquitetura e plano de construção.
- `app.json`, `src/app.js`, `exemplos/`, `index.html`.

## Pendências

- Receber os modelos oficiais de DFD, ETP, TR e análise de riscos e o fluxo real
  de tramitação (o envio lista como documento faltante).
- Confirmar os prazos de cada etapa e quem aprova cada documento.
- A integração com SIGADOC e SIAG está fora do MVP; os números são registrados
  manualmente.
- A linha de base (10 processos, 8 h por processo) precisa ser medida.

## Completado pelo professor (29/10/2026)

O `projeto.json` e o `PROJETO.md` desta pasta foram completados com propostas próximas do
que o aluno escreveu. O envio original está em `envio-original.json`.
Tudo o que foi completado precisa ser confirmado com o aluno no Sprint 0.

**Campos substituídos:**

- `mvp_plataforma`: O envio dizia 'programa de desktop' e não descrevia a stack; alinhado à arquitetura do curso (HTML único, offline first).
- `stack_detalhe`: O envio dizia 'programa de desktop' e não descrevia a stack; alinhado à arquitetura do curso (HTML único, offline first).

**Tabelas:**

- papéis (`tPapeis`): refeita. O papel único estava incompleto; descritos os cinco do relato.
- AS-IS (`tAsIs`): refeita. O AS-IS tinha uma linha; descrito o fluxo do envio.
- TO-BE (`tToBe`): refeita. O TO-BE estava vazio; proposto o recorte do MVP.
- telas e artefatos (`tArtefatos`): refeita. Os artefatos estavam vazios; criadas as telas do protótipo, com rotas.
- entidades (`tEntidades`): refeita. A entidade única ('POLITEC') não representava o processo; refeito o modelo.
- regras de negócio (`tRegras`): refeita. A regra única ('Matrícula') não descrevia o fluxo; criadas as quatro do protótipo.
- métricas (`tMetricas`): refeita. A métrica única ('Número do processo') não era um indicador; definidos tempo e retrabalho.
- fontes de dados (`tFontes`): refeita. As fontes estavam vazias; descritas a partir do envio.
- hospedagem (`tHospedagem`): refeita. A hospedagem dizia 'caixa de texto'; alinhada à arquitetura do curso.
- marcos (`tMarcos`): linhas acrescentadas. O envio trazia só o marco inicial.
- riscos (`tRiscos`): refeita. O risco único estava sem mitigação; acrescentados os riscos dos modelos e da duplicidade.
- referências (`tRefs`): refeita. As referências foram completadas.
