# Feedback dos alunos · Agiliza +

Gerado por `python Apps/_base/baixar_feedback.py` em 08/11/2026, a partir da coleção `feedback_apps` do Firestore.
2 resposta(s) · nota média 3,0 de 5

Use este arquivo para abrir o próximo sprint: cada item vira uma linha do `sprint.md`. Os números com fonte são da própria resposta.

## Resumo

- Usaria no trabalho: sim, com ajustes (2)
- Piloto: talvez (2)

## Prioridades (na ordem de cada pessoa)

- [ ] Texto timbrado e Formatação do texto do word sem necessidade de muitos ajustes pelo perito _(Diego Costa, 1ª)_

## Tela por tela

### Gerar laudo (`#/gerar`)

Situação: precisa de ajuste (2)

- [ ] Gerar um arquivo word com o texto timbrado da Politec. O texto do word tem que vir formatado, sem necessidade de grandes mudanças pelo perito. _(Diego Costa)_
- [ ] 8. Padronização da seção Gerar o laudo – Descrição dos objetos

Na seção Gerar o laudo, durante a geração do documento Word, o item 2. DESCRIÇÃO DOS OBJETOS deverá ser preenchido automaticamente, obedecendo rigorosamente à sequência e à estrutura textual estabelecidas abaixo.

8.1. Estrutura e sequência das informações

O texto deverá ser apresentado na seguinte ordem:

1. Parágrafo introdutório:

"Foram encaminhados para esta gerência acondicionado(s) em envelope de segurança lacrado 00004400, os seguintes objetos:"

2. Identificação do aparelho – Objeto 01:

"Objeto 01: 01 (um) celular na(s) cor(es) verde, marca Xiaomi, modelo xxxxxxx (Redmi 13c), com capa protetora de cor vermelha. O objeto apresentava o(s) seguinte(s) número(s) de IMEI: YYYYYYYYYYYYY e ZZZZZZZZZZ, e continha o(s) seguinte(s) item(ns):"

3. Identificação do cartão SIM – Objeto 01-A:

"• Objeto 01-A: um cartão SIM da operadora Vivo, com número de série ICCID RRRRRRRRRRRRRRRRRRRR;"

8.2. Preenchimento automático dos dados

As informações dos textos exemplificativos deverão ser substituídas automaticamente pelos dados correspondentes cadastrados nas etapas anteriores do aplicativo.

A correspondência deverá obedecer à seguinte lógica:

Informação no laudo

Origem dos dados

Número do lacre do envelope

Dados de entrada do exame

Quantidade e tipo de aparelho

Cadastro do objeto

Cor do aparelho

Cadastro do objeto ou informação confirmada pelo perito

Marca

Campo Vendor: do arquivo DEVICE INFO

Modelo

Campo Device Model: do arquivo DEVICE INFO

IMEI 1 e IMEI 2

Arquivo DEVICE INFO

Cor da capa protetora

Informação cadastrada pelo perito

Operadora do SIM

Campo SPN: do arquivo Report

ICCID do SIM

Campo ICCID: do arquivo Report

8.3. Tratamento dos cartões SIM

A descrição dos cartões SIM deverá ser dinâmica, conforme a quantidade identificada e cadastrada no aplicativo:

Objeto 01-A: primeiro cartão SIM.

Objeto 01-B: segundo cartão SIM, quando existente.

Caso não exista cartão SIM, o aplicativo não deverá gerar a descrição correspondente.

Caso existam dois cartões SIM, ambos deverão ser apresentados na sequência, respeitando a identificação de cada objeto.

8.4. Resultado esperado

O item 2. DESCRIÇÃO DOS OBJETOS deverá ser gerado automaticamente, mantendo a estrutura textual, a ordem de apresentação e a identificação dos objetos estabelecidas neste requisito.

O perito deverá ter a possibilidade de revisar e corrigir as informações antes da geração definitiva do laudo. _(Diego Costa)_

### Biblioteca (`#/biblioteca`)

Situação: precisa de ajuste (2)

- [ ] Criar um coluna com o tipo de dispositivo. Criar um IA para criar/adaptar um texto. _(Diego Costa)_
- [ ] 6. Identificação dos textos na Biblioteca de textos e no módulo Textos padronizados

Implementar a geração automática de um código/ID único para cada texto cadastrado na Biblioteca de textos, contemplando obrigatoriamente as seguintes categorias:

Histórico;

Descrição dos objetos;

Exames;

Anexos e mídias;

Considerações finais.

6.1. Requisitos para geração dos códigos/IDs

Gerar automaticamente um código/ID exclusivo para cada texto cadastrado, independentemente da categoria a que pertença.

Garantir que não existam códigos/IDs duplicados.

Exibir o código/ID junto ao título ou à identificação de cada texto na Biblioteca de textos.

Manter o mesmo código/ID quando o texto for editado ou atualizado.

Garantir que o identificador permaneça vinculado ao respectivo texto, mesmo após alterações de título, conteúdo ou categoria.

6.2. Exibição dos códigos/IDs no módulo Textos padronizados

No módulo Textos padronizados, apresentar o código/ID junto ao nome ou título de cada texto disponível para seleção.

Essa funcionalidade tem como objetivo permitir que o perito diferencie textos com títulos iguais ou semelhantes, evitando a seleção e a inserção equivocada de conteúdo.

A seleção deverá corresponder exatamente ao conteúdo vinculado ao código/ID escolhido na Biblioteca de textos.

6.3. Resultado esperado

Cada texto cadastrado nas cinco categorias deverá possuir um identificador único e permanente, que também será exibido no módulo Textos padronizados, facilitando sua localização, diferenciação, seleção e manutenção.

7. Inclusão e organização dos objetos no módulo Textos padronizados

No módulo Textos padronizados, incluir campos específicos para identificação dos objetos examinados, permitindo a seleção e a inserção de textos padronizados conforme a quantidade de cartões SIM identificados no aparelho.

Deverão ser disponibilizados os seguintes campos:

Objeto 01: referente ao aparelho celular.

Objeto 01-A: referente ao primeiro cartão SIM.

Objeto 01-B: referente ao segundo cartão SIM, quando existente.

A disponibilização dos campos deverá ser dinâmica, considerando a quantidade de cartões SIM identificados no aparelho.

7.1. Organização dos textos no laudo gerado

Os textos selecionados para os campos Objeto 01, Objeto 01-A e Objeto 01-B deverão ser agrupados e apresentados de forma sequencial e conjunta no laudo gerado, respeitando a estrutura e a ordem de identificação dos objetos.

Não deverá ocorrer a geração de parágrafos independentes ou seções desnecessariamente separadas para cada objeto.

Os textos deverão compor uma narrativa única, com continuidade lógica entre as informações referentes ao aparelho e aos cartões SIM.

7.2. Exemplo de resultado esperado no laudo

O resultado da composição dos textos deverá seguir uma estrutura semelhante ao exemplo abaixo:

"Durante a inspeção física do dispositivo, constatou-se o comprometimento de sua integridade estrutural, caracterizado pelo estufamento acentuado da tampa traseira. Não obstante, ao ligar o aparelho, constatou-se a presença de bloqueio de acesso, o qual foi contornado por meio de técnicas forenses para viabilizar a extração dos dados. A aquisição foi realizada pelo método de extração completa de sistema de arquivos, metodologia que, por sua natureza, não assegura a recuperação de dados previamente apagados. Por conseguinte, os dados obtidos com êxito foram gravados no anexo digital para análise da autoridade requisitante. Em relação ao objeto 01-A, os dados referentes ao(s) cartão(ões) SIM estão contidos no anexo digital."

7.3. Requisitos de composição

O aplicativo deverá permitir que o perito selecione textos padronizados individualmente para cada objeto, mas realize automaticamente a composição desses textos em uma narrativa contínua no documento Word.

A composição deverá respeitar:

A ordem dos objetos: 01, 01-A e 01-B.

A existência ou não de cartões SIM.

A continuidade textual entre os parágrafos.

A possibilidade de edição manual do texto final pelo perito antes da geração definitiva do laudo. _(Diego Costa)_

### Casos (`#/inicio`)

Situação: funciona como esperado (1); precisa de ajuste (1)


### Pasta do caso (`#/arquivos`)

Situação: funciona como esperado (1); precisa de ajuste (1)

- [ ] Dúvida se os arquivos _(Diego Costa)_
- [ ] 1. Integração dos dados do aparelho – arquivo DEVICE INFO

No campo Aparelho, o aplicativo deverá utilizar as informações extraídas do arquivo DEVICE INFO, obedecendo à seguinte correspondência:

Campo no aplicativo

Campo de origem no arquivo

Marca

Vendor:

Modelo

Device Model:

As informações deverão ser preenchidas automaticamente, mantendo a possibilidade de conferência e edição manual pelo perito.

2. Integração dos dados dos cartões SIM – arquivo Report

No item Cartões SIM, o aplicativo deverá utilizar as informações extraídas do arquivo Report, conforme a seguinte correspondência:

Campo no aplicativo

Campo de origem no arquivo

ICCID

ICCID:

Operadora

SPN:

A mesma lógica deverá ser aplicada aos demais cartões SIM, quando existentes, respeitando a identificação de cada cartão.

A identificação deverá obedecer à seguinte estrutura:

Objeto 01-A: primeiro cartão SIM.

Objeto 01-B: segundo cartão SIM, quando existente.

Os dados extraídos deverão permitir conferência e edição manual. _(Diego Costa)_

### Conferência (`#/dados`)

Situação: funciona como esperado (1); precisa de ajuste (1)

- [ ] Dar opção do perito criar outras informações, caso queira. No item "Aparelho", o campo cor deve ser editável, pois o perito quem examina o dispositivo. _(Diego Costa)_
- [ ] 3. Correção da leitura de PDFs digitalizados e inclusão do PDF da página principal do Sistema Atena

3.1. Implementação de OCR para PDFs digitalizados

Corrigir a limitação que atualmente apresenta a seguinte mensagem:

"PDF digitalizado, sem camada de texto. Digite os dados com o PDF aberto ao lado (o OCR não está embutido)."

O aplicativo deverá implementar reconhecimento óptico de caracteres (OCR), permitindo a leitura e a extração automática de informações de arquivos PDF digitalizados, mesmo quando não possuem camada de texto pesquisável.

Deverão ser observados os seguintes requisitos:

Permitir a leitura de PDFs compostos por imagens digitalizadas.

Realizar a leitura de todas as páginas do documento.

Identificar corretamente os campos e seus respectivos valores, independentemente da página em que estejam localizados.

Evitar que informações de páginas diferentes sejam associadas incorretamente aos campos do aplicativo.

Manter a possibilidade de conferência e edição manual dos dados extraídos.

3.2. Inclusão de um segundo documento PDF – página principal do Sistema Atena

Incluir a possibilidade de importar um segundo arquivo PDF, correspondente à página principal do procedimento no Sistema Atena.

O aplicativo deverá permitir o carregamento de dois documentos distintos:

Documento 1 – PDF da Requisição

Documento original encaminhado pela autoridade requisitante. Será utilizado para extrair as informações próprias da requisição, incluindo o campo Procedimento:, que alimentará o campo IP do aplicativo.

Documento 2 – PDF da página principal do Sistema Atena

Documento utilizado para extrair informações administrativas e processuais que alimentarão os campos específicos do item Conferência.

3.3. Identificação automática do PDF do Sistema Atena

O arquivo PDF correspondente à página principal do Sistema Atena poderá ser identificado por qualquer uma das seguintes denominações:

atena

Atena

ATENA

O aplicativo deverá reconhecer essas variações automaticamente, independentemente da utilização de letras maiúsculas ou minúsculas.

A identificação deverá considerar o nome do arquivo sem depender da extensão .pdf, aceitando, por exemplo:

atena.pdf

Atena.pdf

ATENA.pdf

Essa identificação deverá ser utilizada para distinguir o documento do Sistema Atena do PDF da Requisição, garantindo que cada arquivo seja processado conforme sua finalidade.

3.4. Processamento separado dos documentos

O aplicativo deverá processar separadamente os dois documentos, respeitando suas respectivas finalidades.

Deverá identificar a origem de cada informação extraída, evitando que dados de um documento sejam associados aos campos destinados ao outro.

A leitura deverá contemplar todas as páginas dos documentos, inclusive quando as informações estiverem distribuídas em páginas diferentes.

4. Inclusão e ajustes no item Conferência

Os campos deste item deverão ser preenchidos automaticamente utilizando as fontes documentais especificadas a seguir.

4.1. Inclusão de campos

IP: incluir um novo campo denominado IP no aplicativo. Seu preenchimento deverá ser realizado exclusivamente a partir do campo Procedimento: do PDF da Requisição, ou seja, do documento original encaminhado pela autoridade requisitante.

Natureza do Exame: incluir no aplicativo um campo denominado Natureza do Exame:, cujo conteúdo deverá ser extraído do campo de mesmo nome existente no PDF da página principal do Sistema Atena.

4.2. Correspondência dos campos do Sistema Atena

Os demais campos do aplicativo deverão ser preenchidos automaticamente a partir das seguintes informações do PDF da página principal do Sistema Atena:

Campo no aplicativo

Campo de origem no PDF do Sistema Atena

Autoridade requisitante

Nome do Solicitante Principal:

Destinação do Laudo

Unidade Requisitante Principal:

Data da solicitação

Data do Documento:

Ofício

Número do Documento:

Natureza do Exame

Natureza do Exame:

4.3. Edição e conferência

Todos os campos deverão permitir conferência e edição manual pelo perito antes da geração definitiva do laudo. _(Diego Costa)_

### Textos (`#/textos`)

Situação: não testou (1); precisa de ajuste (1)

- [ ] Dar opção do perito editar o texto dos campos. No word gerado, os textos dos campos 1. Histórico, 3. Exames, 6. Considerações Finais. _(Diego Costa)_

### Quesitos (`#/quesitos`)

Situação: funciona como esperado (1); precisa de ajuste (1)

- [ ] Esse campo não pode impedir a criação do laudo. Porque há casos em que a requisição não tem quesitos. _(Diego Costa)_

### Revisão final (`#/revisao`)

Situação: não funciona ou deu erro (1)

- [ ] Retirar os campos Correções feitas no Word e Quantidade de correções no Word. Permanecer os campos revisei o laudo e ele está pronto para assinatura e os botões "Concluir o caso" e "Histórico e Metas" _(Diego Costa)_

### Histórico (`#/historico`)

Situação: funciona como esperado (1)

- [ ] Sem funcionamento _(Diego Costa)_

## Erros encontrados

- [ ] Gerar um arquivo word com o texto timbrado da Politec. O texto do word tem que vir formatado, sem necessidade de grandes mudanças pelo perito. _(Diego Costa)_
- [ ] 9. Diretrizes gerais de implementação

Para todas as alterações solicitadas, deverão ser observadas as seguintes diretrizes:

Preservar as funcionalidades existentes do aplicativo que não estejam relacionadas às alterações solicitadas.

Evitar duplicidade de informações entre os documentos importados.

Garantir que os dados extraídos permaneçam vinculados à sua respectiva fonte documental.

Permitir conferência e edição manual das informações pelo perito.

Garantir que os textos padronizados sejam inseridos na ordem correta e respeitem a estrutura do modelo de laudo.

Manter a identificação única dos textos da Biblioteca de textos.

Garantir que os dados e textos selecionados sejam corretamente transportados para o documento Word gerado.

Objetivo final: tornar o aplicativo mais automatizado, confiável e padronizado, reduzindo a necessidade de preenchimento manual, evitando erros na transcrição de informações e garantindo uniformidade na elaboração dos laudos periciais. _(Diego Costa)_

## O que falta

- [ ] IA para reconhecer a cor e características do dispositivo em imagem enviada. Inserir um campo de envio de imagem do dispositivo. _(Diego Costa)_
- [ ] Resultado esperado da integração documental

Após a implementação das alterações dos itens anteriores, o aplicativo deverá:

Extrair automaticamente os dados do aparelho e dos cartões SIM a partir dos arquivos correspondentes.

Realizar OCR nos PDFs digitalizados, sem exigir que possuam camada de texto.

Processar documentos com múltiplas páginas.

Diferenciar o PDF da Requisição do PDF da página principal do Sistema Atena.

Identificar corretamente a origem de cada informação.

Preencher os campos do item Conferência conforme as correspondências definidas.

Permitir a revisão e a correção manual das informações extraídas antes da geração do laudo. _(Diego Costa)_

## Regras, nomes e números que não batem

- [ ] Dar opção do perito editar esses casos _(Diego Costa)_

## Observações

- [ ] 9. Diretrizes gerais de implementação

Para todas as alterações solicitadas, deverão ser observadas as seguintes diretrizes:

Preservar as funcionalidades existentes do aplicativo que não estejam relacionadas às alterações solicitadas.

Evitar duplicidade de informações entre os documentos importados.

Garantir que os dados extraídos permaneçam vinculados à sua respectiva fonte documental.

Permitir conferência e edição manual das informações pelo perito.

Garantir que os textos padronizados sejam inseridos na ordem correta e respeitem a estrutura do modelo de laudo.

Manter a identificação única dos textos da Biblioteca de textos.

Garantir que os dados e textos selecionados sejam corretamente transportados para o documento Word gerado.

Objetivo final: tornar o aplicativo mais automatizado, confiável e padronizado, reduzindo a necessidade de preenchimento manual, evitando erros na transcrição de informações e garantindo uniformidade na elaboração dos laudos periciais. _(Diego Costa)_

## Quem respondeu

- Diego Costa · equipe do app · Gerência de Computação · nota 3 · 2026-11-03
- Diego Costa · equipe do app · Gerência de Computação · nota 3 · 2026-11-05
