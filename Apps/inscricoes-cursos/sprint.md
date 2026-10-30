# Gestão Dinâmica de Inscrições em Cursos · sprints até o MVP

> Arquitetura: HTML monolítico, offline first (ver `contexto.md`).
> Cada sprint dura **1 semana** e termina com o `index.html` funcionando no Edge
> com os dados fictícios.

## Andamento

| Sprint | Situação |
|---|---|
| 0 | Parte técnica feita em 29/10/2026 (dados fictícios, bibliotecas, modelos). Itens que dependem de pessoas continuam abertos. |
| 1 | Feito em 29/10/2026. `python Apps/_base/testar.py inscricoes-cursos` passa. |
| 2 | Feito em 29/10/2026. `python Apps/_base/testar_sprints.py inscricoes-cursos` passa (cenário do "Pronto quando"). |
| 3 | Feito em 29/10/2026. `python Apps/_base/testar_sprints.py inscricoes-cursos` passa (cenário do Sprint 3 em `Apps/_base/cenarios/sprint3.py`; código em `src/sprint3.js`). Falta o teste com 3 pessoas no Outlook desktop, no Outlook Web e no celular (depende da equipe). |

Formato do bloco `INSCRICAO-v1` definido e testado (ida e volta, acento, bloco alterado). 60 e-mails fictícios com 5 reenvios e 5 inválidos.

## Visão geral

| Sprint | Tema | Entrega verificável |
|---|---|---|
| 0 | Escopo, dados e linha de base | Escopo validado, sem CPF, dados fictícios, linha de base medida |
| 1 | Esqueleto e perfis | `index.html` com rotas, perfis, IndexedDB e backup |
| 2 | Cadastro e divulgação do curso | Curso criado, link e QR Code gerados |
| 3 | Formulário de inscrição | Servidor se inscreve, recebe comprovante e envia o e-mail |
| 4 | Importação das inscrições | Blocos colados viram inscrições, sem redigitação |
| 5 | Conferência com o SEAP | Matrículas conferidas com o relatório |
| 6 | Triagem pelas diretorias | Arquivo por diretoria, ordenação e retorno da decisão |
| 7 | Convocação e reserva | Mensagens de titular e reserva, desistência e chamada da reserva |
| 8 | Turma, indicadores e LGPD | Lista final, KPIs, retenção de 30 dias |
| 9 | Publicação, aceite e piloto | Link no GitHub Pages, roteiro de aceite e piloto com uma turma |

**MVP 100% pronto = Sprints 0 a 9.**

---

## Sprint 0 · Escopo, dados e linha de base

- [ ] Ler o `contexto.md` com a aluna e decidir cada **[validar]**. _(premissa em [PREMISSAS.md](../PREMISSAS.md))_
- [ ] Decidir com a chefia: **o CPF sai do formulário**? (proposta: sim, a matrícula basta). _(premissa em [PREMISSAS.md](../PREMISSAS.md))_
- [ ] Confirmar com a TI se a caixa `capacitacao@politec.mt.gov.br` aceita uma
      regra de resposta automática por assunto `[INSCRICAO]`. _(premissa em [PREMISSAS.md](../PREMISSAS.md))_
- [ ] Listar as diretorias que recebem vagas (nome e sigla). _(premissa em [PREMISSAS.md](../PREMISSAS.md))_
- [x] Escrever em `modelos/mensagens.md` os textos: divulgação, comprovante,
      resposta automática, convocação de titular, aviso de reserva, chamada da reserva.
- [x] Gerar `exemplos/curso-ficticio.json`, `emails-ficticios.txt` (60
      inscrições, com 5 duplicadas e 5 inválidas) e `seap-ficticio.csv`.
- [ ] Medir a linha de base em 2 cursos recentes: tempo da divulgação à lista
      final, espera pelas diretorias, erros corrigidos na planilha, vagas ociosas. _(premissa em [PREMISSAS.md](../PREMISSAS.md))_
- [ ] Corrigir no formulário (importando o `projeto.json`) as métricas, a
      hospedagem e a defesa que vieram de outro projeto. _(premissa em [PREMISSAS.md](../PREMISSAS.md))_

**Pronto quando**: a decisão sobre o CPF e a regra do Outlook estão registradas,
e a linha de base dos 2 cursos está na planilha.

## Sprint 1 · Esqueleto e perfis

- [x] `index.html` com `<style>` e `<script>` internos e meta CSP sem `connect-src`.
- [x] Roteador por hash com as 9 rotas do `contexto.md`.
- [x] Escolha do perfil na primeira abertura (Gerência ou Diretoria). A rota
      `#/inscricao` abre sempre no perfil Servidor, sem perguntar.
- [x] Camada `db` sobre IndexedDB (`inscricoes_politec_v1`) com os 6 stores.
- [x] Backup e restauração `.json`, `navigator.storage.persist()`.
- [x] Tema claro e escuro, layout que funciona no celular (o servidor pode se
      inscrever pelo telefone).

**Pronto quando**: o app abre nos dois perfis, guarda um registro de teste e
continua com ele depois de fechar o navegador.

## Sprint 2 · Cadastro e divulgação do curso

- [x] `#/cursos`: criar e editar curso (datas, carga horária, local,
      pré-requisitos, vagas por diretoria, link do grupo, prazo de triagem).
- [x] Soma das vagas por diretoria = total de vagas do curso.
- [x] `#/divulgar/:curso`: gerar o link `index.html#/inscricao?c=<curso codificado>`.
- [x] Embutir o gerador de QR Code e mostrar o QR do link.
- [x] Texto de divulgação pronto para copiar (e-mail às diretorias).

**Pronto quando**: o link gerado abre a tela de inscrição com os dados do curso
em outro navegador, sem nenhum dado prévio no IndexedDB.

## Sprint 3 · Formulário de inscrição

- [x] `#/inscricao`: dados do curso no topo, formulário com os campos mínimos.
- [x] Validação na tela (RN01, RN02, RN04) com a mensagem ao lado do campo.
- [x] Declaração de cada pré-requisito (sim ou não) com o texto do curso.
- [x] Gerar o protocolo e o bloco `INSCRICAO-v1:<dados>` com código de verificação.
- [x] Comprovante na tela: protocolo, curso, status **em análise**, próximos
      passos, botão de imprimir.
- [x] Botão "Enviar e-mail de inscrição" (`mailto:capacitacao@...` com assunto
      `[INSCRICAO] <curso> <protocolo>` e o bloco no corpo) e botão "Copiar".
- [ ] Testar no Outlook desktop, no Outlook Web e no celular.

**Pronto quando**: 3 pessoas da equipe se inscrevem pelo celular e pelo
computador, e os 3 e-mails chegam à caixa de teste com o bloco inteiro.

## Sprint 4 · Importação das inscrições

- [ ] `#/importar`: área para colar vários e-mails de uma vez (o app acha todos
      os blocos `INSCRICAO-v1` no texto).
- [ ] Verificar o código de cada bloco e acusar bloco alterado.
- [ ] Classificar: **novas**, **duplicadas** (RN03, a mais recente vence),
      **inválidas**, **de outro curso**.
- [ ] Importar CSV como alternativa (planilha antiga ou Forms), com associação de colunas.
- [ ] Registrar `recebido_em` e gravar no `log`.

**Pronto quando**: colar os 60 e-mails fictícios gera 50 inscrições, e o
relatório aponta as 5 duplicadas e as 5 inválidas.

## Sprint 5 · Conferência com o SEAP

- [ ] Importar o relatório exportado do SEAP (CSV) para o store `seap`.
- [ ] `#/inscritos/:curso`: lista com filtros por diretoria, status e alerta.
- [ ] Alerta quando a matrícula não existe no SEAP, o vínculo não está ativo ou
      a lotação diverge (RN05).
- [ ] Correção feita pela gerência fica no `log`, com o valor anterior.

**Pronto quando**: as matrículas inventadas do arquivo fictício aparecem com
alerta, e a correção de uma delas fica registrada.

## Sprint 6 · Triagem pelas diretorias

- [ ] Botão "Exportar para as diretorias": um `triagem-<SIGLA>.json` por
      diretoria, só com os inscritos dela e o limite de vagas.
- [ ] Mensagem pronta para enviar o arquivo a cada diretoria, com o prazo.
- [ ] Perfil Diretoria, `#/triagem`: importar o arquivo, arrastar para ordenar,
      marcar titular, reserva ou não selecionado.
- [ ] Bloquear mais titulares que vagas (RN06).
- [ ] Exportar `decisao-<SIGLA>.json` para devolver à gerência.
- [ ] Gerência importa as decisões, e o app mostra quais diretorias ainda não responderam.

**Pronto quando**: 3 diretorias fictícias devolvem as decisões, e uma diretoria
não consegue marcar titulares acima do limite.

## Sprint 7 · Convocação e reserva

- [ ] `#/convocacao/:curso`: lista de titulares e reservas com a mensagem
      preenchida (nome, curso, datas, local, link do grupo).
- [ ] Botão por pessoa: abrir `mailto:` ou copiar a mensagem. Marcar como enviada.
- [ ] Só titular e reserva chamada recebem o link do grupo (RN08).
- [ ] Registrar confirmação de presença e desistência.
- [ ] Desistência: botão "chamar o próximo da reserva" da mesma diretoria, com
      confirmação da gerência (RN09).

**Pronto quando**: no curso fictício, todas as convocações são geradas, e uma
desistência chama a reserva certa.

## Sprint 8 · Turma, indicadores e LGPD

- [ ] `#/turma/:curso`: lista final em CSV (UTF-8 com BOM, `;`) para o
      responsável pelo curso.
- [ ] Indicadores do `contexto.md`, seção 8, por curso.
- [ ] Aviso de retenção ao abrir: cursos encerrados há mais de 30 dias e botão
      de limpeza (RN10), que mantém só as contagens.
- [ ] Texto de privacidade na tela de inscrição (finalidade, dados, prazo).
- [ ] Acessibilidade do formulário de inscrição: rótulos, teclado, contraste.

**Pronto quando**: a lista final abre no Excel, e a limpeza apaga os dados dos
inscritos de um curso encerrado (conferir no DevTools).

## Sprint 9 · Publicação, aceite e piloto

- [ ] Publicar o `index.html` no GitHub Pages (ou no site institucional) para o
      link de inscrição funcionar fora da rede.
- [ ] Ativar a regra de resposta automática do Outlook, se aprovada no Sprint 0.
- [ ] **Roteiro de aceite** com a gerência e uma diretoria:
  1. Criar o curso e divulgar o link.
  2. 10 servidores de teste se inscrevem e recebem o comprovante.
  3. A gerência importa os e-mails sem digitar nada.
  4. A diretoria faz a triagem e devolve o arquivo.
  5. A gerência envia as convocações com o link do grupo.
  6. Uma desistência chama a reserva.
  7. A lista final sai em CSV.
- [ ] Piloto com **uma turma reduzida** (proposto pela aluna).
- [ ] Comparar com a linha de base do Sprint 0 e atualizar `PROJETO.md` e `README.md`.

**Pronto quando**: o roteiro é cumprido sem redigitação, e o piloto está aberto.
