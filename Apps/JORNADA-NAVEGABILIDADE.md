# Avaliação crítica de navegabilidade · 20 apps

Registro de 02/11/2026, depois da jornada do cliente no Chromium e no
Lightpanda 1.0.2 (via WSL, CDP em `127.0.0.1:9222`, com os apps servidos por
HTTP em `127.0.0.1:8000`).

## Como foi avaliado

- **Chromium (Playwright)**: 20/20 apps, 149 passos, 0 erros.
- **Lightpanda 1.0.2**: 18/20 apps concluídos; 2 bloqueios de compatibilidade do
  navegador, não do app:
  - `cin-segunda-via`: o Lightpanda não reduz a imagem de teste
    (`createImageBitmap`/canvas), então o pedido não chega ao protocolo.
  - `agiliza-mais`: o Lightpanda não aceita upload de pasta
    (`webkitdirectory`); o app funciona no Chromium.
- Em cada app: entrada sem hash, troca de perfil pelo menu, seed, tarefa
  principal, tema/fonte, recarga, celular 390 px, console e rede.
- A avaliação abaixo é de **navegabilidade**, não de regra de negócio. O
  `JORNADA-BACKLOG.md` registra o que é defeito e o que é limitação do navegador.

## Placar

| Dimensão | O que foi observado |
|---|---|
| Entrada | 20/20 abrem sem tela de perfil; 18/20 mantêm a tarefa no Lightpanda |
| Menu e perfil | O seletor suspenso funciona; em apps de 6 perfis o contexto de unidade fica escondido no menu |
| Tarefa principal | 18/20 concluem no Lightpanda; 20/20 no Chromium |
| Feedback | Toasts, selos e estados vazios presentes; alguns passos pendentes ainda aceitam clique |
| Celular | 20/20 sem rolagem horizontal da página; tabelas largas rolam dentro do cartão |
| Identidade | 20/20 com casca, tipografia e tela-assinatura distintas |

## Achados críticos

### P1 · `inscricoes-cursos`: a Diretoria abre numa tela em construção

O perfil `diretoria` tem `inicio: "#/triagem"`, mas `#/triagem` não tem `TELAS`.
Ao trocar para Diretoria, o app abre a tela "Triagem · Esta tela ainda está em
construção". O perfil fica sem nenhuma tela de trabalho.

**Recomendação:** construir a Triagem ou trocar o `inicio` para uma tela pronta
e incluir a Triagem quando ela existir. Enquanto não existir, esconder o perfil
ou deixar claro no menu que a tela está pendente.

### P2 · `agiliza-mais`: a bancada oferece passos que não existem

A barra lateral mostra seis passos, mas só Pasta e Conferência têm `TELAS`.
Textos, Quesitos, Gerar laudo e Revisão final abrem "em construção". O menu
também só mostra Casos e Configuração, porque Biblioteca e Histórico não foram
construídos.

**Recomendação:** renderizar os passos sem `TELAS` como "em breve", sem link;
incluir Biblioteca e Histórico no menu apenas quando existirem.

### P2 · `renovacao-contratos-horus`: "Meus contratos" nasce vazio

O seed não traz fiscais. O fiscal informa o nome, mas nenhum contrato tem esse
fiscal ativo, então a caixa fica sempre vazia até alguém substituir o fiscal em
uma ficha.

**Recomendação:** incluir 2 ou 3 fiscais no seed, distribuídos entre contratos,
para a tela mostrar o fluxo.

### P2 · `distribuicao-casos-dna`: a placa é só visual

A placa de 96 poços é a tela-assinatura, mas os poços são `<span>`; clicar não
abre o caso. A única ação é ler a legenda.

**Recomendação:** cada poço com caso vira link para a ficha/rodada; o poço vazio
continua sem ação.

### P2 · `metas-bi-ocr`: conferência e geração fora do menu

O menu tem Importar, Histórico e Configuração. Conferência e geração só são
alcançadas pelo cartão do mês no ano em 12 meses. Quem não entende o cartão não
acha o caminho.

**Recomendação:** manter o ano como centro, mas incluir "Conferir" e "Gerar" no
menu quando houver mês importado, ou uma ação explícita no cartão do mês.

### P2 · `equipamentos-google-earth`: mapa estático e pinos sobrepostos

O mapa de MT é um SVG sem zoom, sem arrastar e sem seleção de pino; 12 unidades
em Cuiabá e região se sobrepõem. A lista tem 150 itens e não tem paginação.

**Recomendação:** zoom e arrastar no SVG, agrupamento de pinos próximos e
paginação/rolagem infinita na lista.

### P2 · `horus-banco-demandas`: contexto de unidade escondido

O Gerente e o Usuário setorial têm o seletor de unidade dentro do menu de
perfil. Quem abre o app não vê que a vitrine está filtrada por unidade.

**Recomendação:** mostrar a unidade como chip na barra de filtros, com "trocar"
no próprio chip.

### P2 · `controle-aquisicoes`: kanban largo no celular

As 9 etapas ocupam uma faixa horizontal. No celular, a pessoa precisa rolar
dentro do quadro e perde a noção de etapa.

**Recomendação:** no celular, agrupar por etapa em uma lista com seletor de
etapa, ou reduzir para 3 colunas com "mais".

### P2 · `documentapolitec`: conferência por leitura esconde o restante

O campo de leitura fica acima das abas e funciona; mas depois de cada Enter a
página inteira é redesenhada e o foco volta ao campo. Em caixas de 850
prontuários, isso custa tempo.

**Recomendação:** atualizar só a linha do prontuário e manter a posição da
lista, sem redesenhar a ficha.

### P2 · `comissao-etica-denuncias`: funil de 7 etapas e barra de 6

O funil tem sete etapas (inclui deliberação e recomendações); a barra do caso
tem seis (Documentos e Encerramento). Os nomes não coincidem e a pessoa não sabe
onde está "deliberação".

**Recomendação:** usar a mesma lista de etapas no funil e na barra do caso.

### P2 · `tap-portfolio-projetos`: matriz sem eixos legíveis

Os pontos mostram o TAP, mas não há marcação numérica de prioridade nem escala
de valor; pontos próximos se sobrepõem.

**Recomendação:** marcar os eixos (1..N e faixas de valor), destacar o ponto sob
o mouse e listar o valor no título.

### P2 · `passivo-ambiental`: fila longa sem paginação

A fila do perito mostra todos os laudos; a miniatura ajuda, mas a lista cresce
sem busca por número ou filtro de atraso.

**Recomendação:** busca por número/local e filtro "atrasados" no topo da fila.

### P2 · `adiantamento`: sem perfil, sem "minha fila"

O app não tem perfis; todo mundo vê tudo. A tela `#/processos` resolve a lista,
mas não existe a fila por papel (servidor, DAS, contabilidade, ordenador).

**Recomendação:** criar os quatro perfis e a tela "Minha fila" com o que espera
cada papel, como previsto na Parte B.

### P2 · `gestao-documentos`: a nota da autoridade fica na aba

Para o servidor e a chefia, a aba Conclusão mostra o aviso "a assinatura é da
autoridade decisora". O aviso só aparece depois de clicar na aba; na primeira
tela, o botão de assinatura simplesmente não existe.

**Recomendação:** mostrar o aviso no topo da ficha ou desabilitar a aba com o
motivo, em vez de esconder.

### P2 · `custodia-definitiva`: mapa das prateleiras leva ao acervo

O mapa é claro, mas clicar numa prateleira leva ao acervo filtrado, não à ficha
do contêiner; a movimentação ainda exige abrir o vestígio.

**Recomendação:** abrir a ficha do contêiner com a lista de vestígios e a ação
"mover" na linha.

## O que melhorou e deve ser mantido

- **Agendamento CIN**: calendário do mês com vagas e horários grandes; passos
  1-2-3; a área do servidor fica discreta.
- **Segunda via**: caixa de entrada com fila à esquerda e pedido à direita;
  "Aceitar e próximo" evita voltar à lista.
- **Hórus**: facetas com contagem, filtros em uma linha e alternância
  cartões/tabela.
- **TCIN**: quadro de plantão por situação, com dias no IML e botões grandes.
- **Aquisições**: kanban das 9 etapas e ficha em abas, com ações por perfil.
- **Custódia**: balcão de leitura do lacre e mapa das prateleiras.
- **DOCUMENTAPOLITEC**: estante de lombadas, menu de 5 itens e conferência por
  leitura com Enter.
- **Gestão de documentos**: caixa por perfil e checklist com caixa de seleção.
- **Renovação**: régua de 0 a 180 dias e semáforo em barra clicável.
- **DNA**: placa de 96 poços e "Meus casos" do perito.
- **Comissão**: funil do processo ético e dossiê "Reservado" em todas as telas.
- **Passivo**: fila com miniatura do mapa e separação perito/gestor.
- **RNC**: quadro por etapa do ciclo e setor como contexto.
- **TAP**: matriz valor × prioridade e início por perfil.
- **Adiantamento**: régua de prazos e prazo no topo da ficha.
- **Metas**: ano em 12 meses com situação e passos 1-2-3.
- **Inscrições**: cartões de curso com a esteira Divulgar → Turma.
- **Mapa**: esteira das 8 etapas e grade em planilha.
- **Equipamentos**: mapa de MT com os 142 municípios e pinos das unidades.
- **Agiliza**: bancada com passos à esquerda e trabalho à direita.

## Próximo passo

1. Corrigir o P1 da Diretoria em `inscricoes-cursos`.
2. Desabilitar os passos sem `TELAS` no Agiliza.
3. Incluir fiscais no seed da renovação e tornar os poços da placa clicáveis.
4. Reexecutar `python Apps/<app>/testes/jornada.py` e a matriz Lightpanda.
