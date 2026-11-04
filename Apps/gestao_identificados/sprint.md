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
| Extra | Feito em 03/11/2026. Módulo `#/desaparecidos` com CNPD (381), NamUs (300 de 26.607), mapa Leaflet offline e catálogo de 18 fontes. |

**MVP 100% pronto = Sprints 0 a 4.**

## Extra · módulo de desaparecidos

Feito:

- [x] Rota `#/desaparecidos` no `app.json`, restrita a `nihde`/`gestor`, sem
      alterar as telas do MVP.
- [x] Abas CNPD, NamUs e Fontes; KPIs, filtros, tabela e CSV.
- [x] Mapa Leaflet 1.9.4 embutido, sem tiles, com malha do IBGE/EUA.
- [x] Clique no círculo abre a lista em painel abaixo do mapa (corrige o card
      que aparecia atrás do mapa).
- [x] Coleta do CNPD (`coletar_dados.py`) e do NamUs com Scrapling
      (`coletar_namus.py`).
- [x] Catálogo de fontes (`FONTES.md` e `dados/fontes.json`).
- [x] Testes: `testar.py` OK; `cenarios.py` 4/4; `#/testes` 12/12.

Falta:

- [ ] Revisar o recorte do CNPD e a amostra do NamUs com a Kesia/NIHDE.
- [ ] Integrar INTERPOL, NCMEC e portais estaduais; pedir acesso a
      SINALID/CADÊ/SINESP/RIBPG/SINAB/Atena.
- [ ] Cruzar CNPD com os corpos do NIHDE (fase 2), com revisão humana.
- [ ] Confirmar termos de uso e LGPD; coordenar o `app.json` com a outra IA.
- [ ] Ver `CONTINUAR.md` para a lista priorizada.

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

O módulo foi construído com dados públicos. O contrato está em
`docs/CONTRATO-DESAPARECIDOS.md`; este app fornece os corpos não identificados e
não muda o build. A leitura das fontes e o mapa estão prontos; o cruzamento com
os corpos (candidatos + confirmação humana) continua aberto.

- [x] Coletar a base pública com fonte e data em `dados/cnpd-snapshot.json` e
      `dados/namus-snapshot.json` (o antigo `desaparecidos-publicos.json` não foi usado).
- [x] Criar `src/desaparecidos.js` e a rota `#/desaparecidos` (restrita a `nihde` e
      `gestor`; contrato atualizado).
- [x] Filtrar por sexo, idade, município, data e características; mostrar até 10
      candidatos com o motivo.
- [x] Confirmação humana com justificativa e registro no `log` do corpo.
- [x] Aviso de que a correspondência é indício, não identificação; acesso restrito
      a `nihde` e `gestor`.
- [x] Cenário próprio (`s4_desaparecidos_e_fontes`) sem quebrar `testar.py` e os
      três cenários anteriores.


**Implementado em 03/11/2026**: o botão **Ver corpos** cruza o desaparecido com os corpos não identificados (sexo, idade ±5, altura ±10 cm, município, janela de datas e características), mostra até 10 candidatos com o motivo e registra **confirmado**, **descartado** ou **exame complementar**, com justificativa na loja `correspondencias` e no `log` do corpo. O aceite com o NIHDE continua humano.
