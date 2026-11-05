# Sistema de Controle de Necropsia

Registro digital único de cada corpo, da remoção à liberação: acionamento,
marcos de deslocamento, lacres das amostras, situação de identificação e busca
pelo protocolo, nome ou documento. O preenchimento não estava concluído no
formulário; a proposta abaixo foi completada a partir do relato, dos dois envios
parciais e do protótipo que a aluna construiu.

| Campo | Valor |
|---|---|
| Aluna | Silmara Bueno |
| Contato | silmarabueno@politec.mt.gov.br |
| Unidade | IML · Coordenadoria de Perícias em Mortos |
| Tipo | Aplicativo para servidor |
| Stack | HTML único (CSS/JS inline), IndexedDB, GitHub Pages |
| Fonte | `Aula 8/Entregas/Silmara/` (dois JSON parciais, protótipo e link) |
| GitHub | `silmarabueno-droid` (colaboradora) |

## Arquivos

- `envio-original.json`: o envio mais recente (CNC, 29/10/2026 13:30), sem alteração.
- `envio-tcin.json`: o envio anterior (TCIN, 29/10/2026 12:37), preservado.
- `prototipo/tci.html`: o protótipo que a aluna gerou na IA, com os assets e o link original.
- `projeto.json` e `PROJETO.md`: o envio completado (o original parava no problema).
- `contexto.md` e `sprint.md`: arquitetura e plano de construção.
- `app.json`, `src/app.js`, `exemplos/`, `index.html`.

## Pendências

- Confirmar com a aluna e com o IML o nome do projeto (CNC ou TCIN), os marcos
  oficiais do deslocamento e os livros que o app substitui.
- Medir a linha de base (tempo de remoção, de identificação e de liberação);
  o envio diz que nada é medido hoje.
- Integrar com o Atena, a criptografia de dados sensíveis e o fluxo real de
  liberação ficam fora do MVP.
- O protótipo da IA é referência visual; o app do curso é a implementação
  offline, com dados fictícios e IndexedDB.

## Completado pelo professor (29/10/2026)

O `projeto.json` e o `PROJETO.md` desta pasta foram completados com propostas próximas do
que o aluno escreveu. O envio original está em `envio-original.json`.
Tudo o que foi completado precisa ser confirmado com o aluno no Sprint 0.

**Campos substituídos:**

- `mvp_objetivo`: O envio parou no problema; MVP, arquitetura e tabelas completados a partir do relato e do protótipo.
- `mvp_naofaz`: O envio parou no problema; MVP, arquitetura e tabelas completados a partir do relato e do protótipo.
- `entrega`: O envio parou no problema; MVP, arquitetura e tabelas completados a partir do relato e do protótipo.
- `dentro`: O envio parou no problema; MVP, arquitetura e tabelas completados a partir do relato e do protótipo.
- `fora`: O envio parou no problema; MVP, arquitetura e tabelas completados a partir do relato e do protótipo.
- `mvp_plataforma`: O envio parou no problema; MVP, arquitetura e tabelas completados a partir do relato e do protótipo.
- `mvp_tela_inicial`: O envio parou no problema; MVP, arquitetura e tabelas completados a partir do relato e do protótipo.
- `mvp_mock`: O envio parou no problema; MVP, arquitetura e tabelas completados a partir do relato e do protótipo.
- `mvp_criterio`: O envio parou no problema; MVP, arquitetura e tabelas completados a partir do relato e do protótipo.
- `mvp_dados`: O envio parou no problema; MVP, arquitetura e tabelas completados a partir do relato e do protótipo.
- `mvp_reuso`: O envio parou no problema; MVP, arquitetura e tabelas completados a partir do relato e do protótipo.
- `dependencias`: O envio parou no problema; MVP, arquitetura e tabelas completados a partir do relato e do protótipo.
- `papeis_obs`: O envio parou no problema; MVP, arquitetura e tabelas completados a partir do relato e do protótipo.
- `lgpd_dados`: O envio parou no problema; MVP, arquitetura e tabelas completados a partir do relato e do protótipo.
- `lgpd_base`: O envio parou no problema; MVP, arquitetura e tabelas completados a partir do relato e do protótipo.
- `lgpd_retencao`: O envio parou no problema; MVP, arquitetura e tabelas completados a partir do relato e do protótipo.
- `lgpd_acesso`: O envio parou no problema; MVP, arquitetura e tabelas completados a partir do relato e do protótipo.
- `stack_detalhe`: O envio parou no problema; MVP, arquitetura e tabelas completados a partir do relato e do protótipo.
- `hospedagem_escolhida`: O envio parou no problema; MVP, arquitetura e tabelas completados a partir do relato e do protótipo.
- `conta_quem`: O envio parou no problema; MVP, arquitetura e tabelas completados a partir do relato e do protótipo.
- `orcamento`: O envio parou no problema; MVP, arquitetura e tabelas completados a partir do relato e do protótipo.
- `restricoes`: O envio parou no problema; MVP, arquitetura e tabelas completados a partir do relato e do protótipo.
- `campos_data`: O envio parou no problema; MVP, arquitetura e tabelas completados a partir do relato e do protótipo.
- `base_periodo`: O envio parou no problema; MVP, arquitetura e tabelas completados a partir do relato e do protótipo.
- `coletar`: O envio parou no problema; MVP, arquitetura e tabelas completados a partir do relato e do protótipo.
- `acesso`: O envio parou no problema; MVP, arquitetura e tabelas completados a partir do relato e do protótipo.
- `hipotese_campo`: O envio parou no problema; MVP, arquitetura e tabelas completados a partir do relato e do protótipo.
- `lacunas`: O envio parou no problema; MVP, arquitetura e tabelas completados a partir do relato e do protótipo.
- `apoio`: O envio parou no problema; MVP, arquitetura e tabelas completados a partir do relato e do protótipo.
- `aprendizado`: O envio parou no problema; MVP, arquitetura e tabelas completados a partir do relato e do protótipo.
- `frase`: O envio parou no problema; MVP, arquitetura e tabelas completados a partir do relato e do protótipo.
- `provas`: O envio parou no problema; MVP, arquitetura e tabelas completados a partir do relato e do protótipo.
- `piloto`: O envio parou no problema; MVP, arquitetura e tabelas completados a partir do relato e do protótipo.
- `risco_defesa`: O envio parou no problema; MVP, arquitetura e tabelas completados a partir do relato e do protótipo.
- `doc_descricao`: O envio parou no problema; MVP, arquitetura e tabelas completados a partir do relato e do protótipo.
- `doc_faltando`: O envio parou no problema; MVP, arquitetura e tabelas completados a partir do relato e do protótipo.

**Tabelas:**

- AS-IS (`tAsIs`): refeita. O AS-IS estava vazio; descrito a partir do relato do envio.
- TO-BE (`tToBe`): refeita. O TO-BE estava vazio; descritas as cinco mudanças do protótipo.
- papéis (`tPapeis`): refeita. Os papéis estavam incompletos; descritos os quatro do fluxo.
- telas e artefatos (`tArtefatos`): refeita. Os artefatos estavam vazios; criadas as telas do protótipo.
- entidades (`tEntidades`): refeita. A entidade única estava vazia; refeito o modelo.
- regras de negócio (`tRegras`): refeita. A regra única estava vazia; criadas as cinco do protótipo.
- fontes de dados (`tFontes`): refeita. As fontes estavam vazias; descritas a partir do relato.
- métricas (`tMetricas`): refeita. As métricas estavam vazias; definidas as três do relato.
- hospedagem (`tHospedagem`): refeita. A hospedagem estava vazia; alinhada à arquitetura do curso.
- marcos (`tMarcos`): refeita. O marco único estava vazio.
- riscos (`tRiscos`): refeita. O risco estava vazio; acrescentados os riscos do fluxo.
- referências (`tRefs`): refeita. As referências estavam vazias.

## Como construir e testar

Este app é autônomo. `nucleo/`, `construir.py` e `testes/` são só dele e não
importam nada de `Apps/_base/`, porque esta pasta vai virar um repositório
próprio no GitHub. O `index.html` é **gerado**: edite as fontes (`app.json`,
`src/`, `nucleo/`, `exemplos/seed.json`) e rode a construção.

```powershell
cd "Apps/trilha-custodia-necropsia"
python construir.py           # gera o index.html a partir de app.json, src/, nucleo/ e os dados
python testes/testar.py       # estrutura: zero rede, #/testes 100%, rotas por perfil, tema e celular
python testes/cenarios.py     # cenários dos sprints: usa a tela como uma pessoa usaria
```

Antes da primeira execução: `pip install playwright` e
`playwright install chromium`.

Os dados fictícios são gerados por `exemplos/gerar_exemplos.py`; rode-o quando
mudar o esquema e confira o novo `exemplos/seed.json` no navegador.


Regras: não edite `index.html` direto; nenhum arquivo de fora da pasta do app é
importado; o tema claro é o padrão e o escuro só entra pelo botão; os textos
seguem o português do Brasil com acentuação, sem travessões.

## Identidade e usabilidade (02/11/2026)

O app tem casca de trilho de ícones, cabeçalho sólido, fonte condensada e
densidade ampla, para uso em tablet no IML. O painel é **por perfil** (atualizado
no Sprint 9): o Técnico vê o **quadro das sete etapas** em colunas (com cartões de
corpo, iniciais, dias no IML e último marco), o Médico Legista vê a sala de
necropsia (etapas 3 a 5) e o Gestor ADM vê a **fila da ADM**, os tempos, a
permanência e o alerta de 12 h. A ficha do corpo virou abas: Resumo, Etapas,
Marcos, Lacres, Situação, Liberação e Auditoria.
Código em `src/identidade.js` e `src/app.css`.

## Mapa do processo

O `processo.html` mostra o **AS-IS** (como o processo funciona antes do MVP) e o
**TO-BE** (como fica com o MVP), com as métricas, regras e papéis do projeto.
Abra ao lado do `index.html`.

## Sprint 9 · Fluxograma da Silmara (05/11/2026)

O fluxograma e o protótipo que a Silmara trouxe em 05/11/2026 estão em
`entregas/2026-11-05/`. A revisão do fluxograma virou o TO-BE do app
(`docs/diagramas/to-be.manual.mmd`, renderizado em `to-be.svg` e no `processo.html`).

- **Três perfis só**: Técnico, Médico Legista e Gestor ADM. O Operador do CIOP e
  o Plantonista saíram.
- **Identificação com exame complementar (RN11)**: necropapiloscopia, depois DNA,
  odontologia legal ou antropologia forense, com as tentativas registradas. Os
  métodos só se esgotam depois de pelo menos um exame complementar.
- **Sepultamento pelo Estado só por decisão do Gestor ADM (RN09)**, nos dois
  caminhos (não identificado ou identificado e não reclamado), com justificativa,
  número da autorização e Auto de Entrega da funerária.
- **Funerária nos dois destinos**: a liberação à família também exige a funerária
  e o Auto de Entrega.
- **Laudo em paralelo e encerramento com três condições (RN10)**: o laudo pode ir
  à ADM a partir da etapa 5; a custódia só se encerra com o destino do corpo, o
  laudo recebido e todos os lacres recebidos.
- **Caso encerrado não se edita (RN12)**: a correção entra como retificação, com
  tipo, o que muda e motivo, inclusive "familiar localizado após o sepultamento".
- **A liberação só acontece pela etapa 6**: os atalhos antigos (situação manual e
  auto de entrega do Sprint 4) foram fechados.

Código em `src/sprint8.js` (etapas 5 a 7), `src/sprint9.js` (retificação e
bloqueios) e `src/identidade.js` (painéis). Cenário `s9_fluxograma_da_silmara`.
