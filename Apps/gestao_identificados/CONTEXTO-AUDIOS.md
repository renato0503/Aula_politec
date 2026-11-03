# Contexto dos áudios · NIHDE

Leitura consolidada dos cinco áudios de 03/11/2026 e do envio da Kezia
(`NIHDE---Gesto-de-dados...json`). Serve para completar o `PROJETO.md` e o
`sprint.md` quando o app for construído.

## O que o núcleo faz

O NIHDE centraliza as informações de **corpos não identificados** e de
**corpos identificados e não reclamados**. Hoje o dado fica disperso entre o
Atena, as planilhas de cada IML e os laudos em PDF.

## Fluxo real descrito

1. O corpo dá entrada no IML e é cadastrado no **Atena**, com um protocolo.
2. Na necropsia, o médico coleta material biológico para DNA.
3. O corpo vai para a **necropapiloscopia**; em paralelo, a amostra vai para o
   **laboratório de DNA** e o corpo para a **odontologia** (arcada dentária).
4. A papiloscopia cruza as digitais com bases biométricas (TSE, Polícia
   Federal). Sem correspondência, emite laudo negativo.
5. O perfil genético vai para o **CODIS** estadual.
6. A odontologia processa a arcada.
7. Corpos esqueletizados ou sem digitais vão para a **antropologia**, que traça
   o perfil biológico.
8. Sem identificação em **30 dias**, o corpo é sepultado pelo município com
   certidão de óbito de não identificado.
9. As análises continuam depois do sepultamento. Quando a identificação sai, o
   núcleo precisa localizar a família, entregar o corpo e atualizar a certidão.

## Dados que o app precisa guardar

- Protocolo do Atena; unidade do IML; data e local de entrada; município.
- Características físicas: sexo, idade aparente, altura, peso, cor dos olhos,
  cor do cabelo, pele/raça e sinais particulares, quando possível.
- Amostras coletadas: digital, material para DNA, arcada dentária.
- Exames: necropapiloscopia, DNA, odontologia e antropologia, com protocolo,
  data, resultado (positivo, negativo, em andamento) e laudo.
- Identificação: data, via que identificou e órgão responsável.
- Família: busca iniciada, família localizada, entrega e data.
- Sepultamento: data, município, local e certidão.
- Situação: não identificado, identificado, não reclamado, sepultado,
  identificado após o sepultamento, entregue à família.

## O que os áudios acrescentam ao envio

- O envio diz que o MVP **não estrutura os dados físicos**; os áudios tratam
  esses metadados como o núcleo do projeto. É preciso decidir: o MVP guarda as
  características físicas (mesmo que em campos simples) ou só o estado das
  etapas?
- O envio fala em integrar com órgãos externos; os áudios colocam a integração
  com desaparecidos e com outros estados na **fase 2**. Em 03/11/2026, outra IA
  passou a construir o **módulo de desaparecidos com dados públicos dentro do
  MVP**; a integração com outros estados continua fase 2. O contrato está em
  docs/CONTRATO-DESAPARECIDOS.md.
- O prazo de **30 dias** para o sepultamento pelo município e a identificação
  **posterior ao sepultamento** não aparecem no envio.
- A via que identificou (papiloscopia, DNA, odontologia ou antropologia) e o
  aviso aos outros setores são requisitos centrais.
- O piloto é de **90 dias**, em todos os corpos que entrarem no IML de Cuiabá.
- O relatório precisa responder: quantos corpos não identificados a POLITEC tem,
  sepultados ou não, por período e por unidade.

## Pontos para confirmar com a Kezia

- Nome: o envio traz **Kesia Melo**; a conversa fala em **Kezia**. Qual é o
  correto?
- O envio usa **NIHDE** e a transcrição às vezes escreve CIGID. O nome oficial é
  NIHDE?
- Quais campos físicos entram no MVP e quais ficam para a fase 2?
- O app substitui a planilha de cada IML ou convive com ela no piloto?
- Quem pode ver o nome da família e o local do sepultamento (LGPD)?
- O login por matrícula é simulado no MVP? A autenticação real depende da TI?
