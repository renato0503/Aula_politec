# NIHDE · sprints até o MVP

> Arquitetura: HTML monolítico, offline first (ver `contexto.md`). Sprints de 1 semana.

## Andamento

| Sprint | Situação |
|---|---|
| 0 | Feito em 03/11/2026. Envio da Kesia, cinco áudios transcritos e contexto consolidado em `CONTEXTO-AUDIOS.md`; 24 corpos fictícios em `exemplos/gerar_exemplos.py`. |
| 1 | Feito em 03/11/2026. `index.html`, IndexedDB, perfis, painel com a pergunta do MVP e filtros; `python testes/testar.py` passa. |
| 2 | Feito em 03/11/2026. Lista, cadastro com protocolo único e características físicas; cenário `s2_entrada_duplicada_e_sepultamento` passa. |
| 3 | Feito em 03/11/2026. Ficha com exames, identificação, família, sepultamento, identificação após sepultamento e auditoria; cenário `s1_painel_e_identificacao` passa. |
| 4 | Feito em 03/11/2026. Relatório por unidade e por via, CSV com BOM; cenário `s3_relatorio_e_csv` passa. |
| 5 | Aceite e piloto: dependem da direção da POLITEC e do IML de Cuiabá. |

**MVP 100% pronto = Sprints 0 a 4.**

## Sprint 0 · Processo e dados

- [x] Ler o envio da Kesia e os cinco áudios.
- [x] Consolidar o fluxo, os metadados e as regras em `CONTEXTO-AUDIOS.md`.
- [x] Gerar 24 corpos fictícios em `exemplos/gerar_exemplos.py`.
- [ ] Confirmar o nome (Kesia), o nome oficial do NIHDE e o escopo dos dados físicos.
- [ ] Confirmar com a direção da POLITEC a integração com o Atena e a base de desaparecidos (fase 2).

## Sprint 1 · Painel e base

- [x] `index.html` com rotas, IndexedDB, perfis e backup.
- [x] Painel com a pergunta do MVP, KPIs, filtros e lista por unidade.
- [x] Tema claro, tamanho da fonte e celular.

## Sprint 2 · Entrada e lista

- [x] Cadastro com protocolo único (RN01), unidade, município, local e características.
- [x] Lista com filtros e iniciais (RN07).
- [x] Validação de duplicidade.

## Sprint 3 · Identificação e desfecho

- [x] Quatro exames com status, protocolo e data (RN02).
- [x] Identificação por via e data (RN03); identificação após sepultamento.
- [x] Família: busca, localização, entrega (RN05) e não reclamado (RN06).
- [x] Sepultamento pelo município depois de 30 dias (RN04).
- [x] Auditoria de cada ação (RN08).

## Sprint 4 · Relatório

- [x] Por unidade: total, não identificados, não reclamados, identificados, sepultados e entregues.
- [x] Por via de identificação e taxa de identificação.
- [x] CSV com BOM e uma linha por corpo.

## Sprint 5 · Aceite e piloto

- [ ] Roteiro de aceite com o NIHDE e o IML de Cuiabá.
- [ ] Piloto de 90 dias em todos os corpos que entrarem no IML de Cuiabá.
- [ ] Comparar com a linha de base da planilha de Excel.
- [ ] Integração com o Atena, desaparecidos e outros estados (fase 2, depende da direção).

## Sprint 6 · Módulo de desaparecidos (outra IA)

O módulo é construído por outra IA, com dados públicos. O contrato está em
`docs/CONTRATO-DESAPARECIDOS.md`; este app fornece os corpos não identificados e
não muda o build.

- [ ] Coletar a base pública com fonte e data em `dados/desaparecidos-publicos.json`.
- [ ] Criar `src/desaparecidos.js` e a rota `#/desaparecidos` (coordenar o `app.json`).
- [ ] Filtrar por sexo, idade, município, data e características; mostrar até 10 candidatos com o motivo.
- [ ] Confirmação humana com justificativa e registro no `log` do corpo.
- [ ] Aviso de que a correspondência é indício, não identificação; acesso restrito a `nihde` e `gestor`.
- [ ] Cenário próprio sem quebrar `testar.py` e os três cenários atuais.
