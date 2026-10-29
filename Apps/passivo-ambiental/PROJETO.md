# PROJETO.md — Passivo Ambiental

**Aluno ou equipe:** Fábio
**Unidade:** Diretoria de Interiorização
**Contato:** fabioconceicao@politec.mt.gov.br
**Projeto:** Passivo Ambiental
**Tipo de projeto:** Mapeamento de processo (fluxo, BPMN ou Mermaid)
**Data:** 2026-10-27
**Resumo:** O projeto "Passivo Ambiental" tem o objetivo de semi-automatizar a produção de laudos periciais ambientais atrasados e melhorar o tempo de resposta à autoridade requisitante.

## 1. Problema (a dor)

**Problema:** Existem cerca de 300 requisições periciais atrasadas desde 2020 e somente um perito disponível para a realização do trabalho. Atualmente, o tempo médio de elaboração de um laudo pericial ambiental, exclusivamente por sensoriamento remoto, é cerca de 16 horas. A ideia é mapear o fluxo processual e aprimorá-lo para otimizar o tempo gasto na elaboração dos laudos.
**Impacto:** Tempo: 16 horas e um total de 8 a 10 laudos por mês.
**Quem sofre:** Autoridade
**Como é feito hoje:** as requisições são protocoladas no sistema Atena e atribuídas ao perito responsável pela perícia; o perito lê a requisição e, com base nos quesitos elaborados pela autoridade requisitante decide qual a metodologia a ser utilizada; Após, abre um modelo de laudo pericial no google docs, e começa a substituir as informações do modelo pelas informações da requisição. Faz consulta a sites externos e cola uma captura da página do site no laudo. Esta primeira etapa demora cerca de 2 horas. Na sequencia abre o Qgis e elabora uma sequencia de mapas que identificam e quantificam o dano ambiental, insere imagens dos mapas nos laudo, interpreta-os e faz considerações sobre eles; À partir da quantificação do dano calcula-se o valor do dano ambiental (R$), após se elabora a resposta aos quesitos específicos e, por fim, a conclusão do laudo pericial. Esta segunda etapa dura cerca de 14 horas.
**Evidências:** Entrevista com a equipe
**Detalhe da evidência:** Entrevista com o perito responsável.
**O que não pode ser automatizado:** A elaboração do mapa, pois o dano ambiental varia de caso a caso.

## 2. Objetivo do MVP (o que faz e o que NÃO faz)

**Objetivo do MVP:** Demonstrar que o perito consegue extrair dados de uma requisição pericial para o cabeçalho e gerar um laudo ambiental em PDF com mapa de sensoriamento remoto integrado em uma única plataforma.
**O que o MVP não faz:** A elaboração e assinatura dentro do Atena fica para a etapa 2.
**Entregável do projeto:** Aplicativo que auxilia na elaboração do laudo pericial ambiental.
**Dentro do escopo:** Preenchimento de informações redundantes; Elaboração de mapas com modelos pré-definidos; Exportação do laudo em PDF; 
**Fora do escopo:** A  tradução dos mapas em palavras (texto), a elaboração e assinatura dentro do Atena fica para a etapa 2.
**Plataforma alvo:** Programa de desktop
**Primeira tela:** Tela de login do perito e, em seguida, a tela de importação/seleção da requisição pericial com visualização do cabeçalho preenchido.
**Simulado no MVP:** A integração automática com os sistemas legados de tramitação de processos e a captura de imagens de satélite em tempo real via API serão simuladas: o sistema utilizará um arquivo de requisição de exemplo e imagens de satélite pré-carregadas localmente para demonstrar o fluxo de geração do laudo e exportação em PDF.
**Critério de aceite:** O perito consegue carregar um ficheiro de requisição pericial de teste, visualizar o preenchimento automático do cabeçalho, aplicar um modelo pré-definido de mapa de sensoriamento remoto e exportar o laudo pericial completo em formato PDF com o texto e o mapa integrados.
**Dados de exemplo:** No mínimo 3 ficheiros de requisição pericial fictícios (com dados sobre desflorestação, queimada e ocupação irregular em área protegida), 3 imagens de satélite de exemplo com vetores de delimitação de dano e 1 modelo pré-definido de mapa e documento.
**O que já existe pronto e pode ser reaproveitado:** O modelo/template de laudo pericial em docx, bibliotecas open-source para visualização de mapas e geração de PDF (ex.: Leaflet, ReportLab, PyPDF), template de mapas no Qgis.
**Dependências:** O direto da DI aprova o projeto, a equipa de suporte/TI disponibiliza as imagens de satélite de amostra. A chefia da unidade pericial valida a lista de campos obrigatórios do cabeçalho e o padrão visual do mapa.

## 3. Usuários e papéis

| Papel | Quem é | O que enxerga | O que faz | O que não pode fazer | Registro |
|---|---|---|---|---|---|
| Cadastro de protocolo no Atena | administrativo | natureza da requisição | aceita a requisição no sistema, cria um protocolo e distribui o protocolo via Atena para o perito | arquivar o protocolo sem justificativa | muda o status do protocolo para atibuído e contabiliza o prazo de 10 dias |
| Triagem | perito | complexidade da requisição | decide se é possível confeccionar o laudo por SR | arquivar o protocolo sem justificativa; Extrapolar o prazo sem solicitar prorrogação | prazo expirado |
| Confecção de Mapas | perito | tipo e extensão do dano ambiental | caracteriza através de mapas os vstígios encontrados | deixar de comprovar os vestígios | nada |
| Confecção do laudo | perito | tipo e extensão do dano ambiental | traduz em palavras os achados evidenciados nos mapas | deixar o laudo incompleto | nada |
| Assinatura do laudo | perito | laudo em pdf | assina o laudo através de chave token | deixar de assinar o laudo | nada |
| Upload do laudo | perito | laudo assinado | preenche informações complementares no sistema Atena e faz o upload do laudo assinado | deixar de preencher informações complementares | status do protocolo muda para "finalizado" |

**Observações sobre os papéis:** o acesso do perito ao sistema Atena exige autenticação via login e senha, mas a assinatura do laudo é realizada via token em sistema paralelo. o perito não tem autonomia para redistribuir o protocolo ou saber se determinado protocolo foi distribuído para outro perito.

## 4. Dados (entidades e colunas; tudo SINTÉTICO)

| Entidade | O que representa | Colunas | Chave | Volume | Origem | Sintético |
|---|---|---|---|---|---|---|
| Requisicao Pericial | Dados da requisição oficial importada para início do laudo | id: string, numero_processo: string | id | 3 registos | Ficheiro JSON / Mock | Sim |
| LaudoAmbiental | Registo do laudo pericial gerado pela aplicação | id: string, requisicao_id: string | id | 3 registos | Formulário da aplicação | Sim |
| MapaTematico | Elemento cartográfico com vestígios/evidências do dano | id: string, laudo_id: string, modelo_template: string | id | 3 registos | Módulo de mapeamento | Sim |

**O que precisa ser coletado:** Hoje não existe o registo estruturado do tempo despendido pelo perito entre a leitura da requisição, a elaboração do mapa e a emissão final do laudo. Proposta: capturar automaticamente os carimbos de data e hora (timestamps) no momento da importação da requisição, da geração do mapa e da exportação do PDF durante a fase de testes do MVP.
**Quem libera o acesso:** A chefia do setor pericial valida a estrutura dos modelos pré-definidos de laudo e mapa até ao dia [Data]. A equipa de TI / Docente disponibiliza a pasta com os ficheiros de exemplo das requisições e as imagens de satélite sintéticas até ao dia [Data].

### Fontes de dados do processo real

| Fonte | Tipo | Onde | Existe | Uma linha é | Volume | Campos de data | Atualiza | LGPD |
|---|---|---|---|---|---|---|---|---|
| Requisições periciais | Sistema oficial | Atena | Sim | Um pedido/requisição oficial de perícia ambiental | 10 | data_requisicao, data_recebimento | A cada nova requisição | Sim |
| Imagens de Satélite e Geodados | Não existe ainda | Servidor de mapas | Não | Uma cena de satélite ou camada vetorial do dano | ~50 MB por caso | data_imagem, data_captura | Conforme disponibilização de novos satélites | Não |
| Modelos e Gabaritos de Laudo | Relatório | Repositório do App / Código-fonte | Não | Um modelo estruturado de laudo e leiaute de mapa | 3 a 5 modelos | data_atualizacao | Sempre que houver alteração na norma pericial | Sim |


## 5. Regras de negócio (RN01, RN02...)

| ID | Regra | Quando se aplica | Exceção | Quem valida | Tipo |
|---|---|---|---|---|---|
| RN01 | O cabeçalho deve extrair e preencher automaticamente o número do processo, órgão e localização a partir da requisição. | Na seleção/importação da requisição pericial. | Permite edição manual se houver divergência nos dados. | Sistema / Perito | Validação |
| RN02 | Todo mapa temático gerado deve incluir obrigatoriamente a rosa dos ventos (norte), escala gráfica e a área delimitada do dano. | Durante a composição do mapa no modelo pré-definido. | Nenhuma. | Sistema | Negócio |
| RN03 | A exportação em PDF só é liberada se o cabeçalho estiver completo e pelo menos 1 mapa de evidência estiver anexado. | No momento de acionar o botão de exportar PDF. | Nenhuma. | Sistema | Negócio |


## 6. Telas (#/painel, #/lista...)

| Rota | Tela | Objetivo | Quem usa | Dados | Ação | Regra | Tipo | Verificável como | MVP |
|---|---|---|---|---|---|---|---|---|---|
| Preencher automaticamente as informações redundantes da requisição pericial no cabeçalho | Módulo de Importação e Cabeçalho | perito | Nº do processo/requisição, órgão solicitante, data, endereço/coordenadas, tipo de infração | Importar requisição pericial e validar preenchimento automático | Mapear os campos da requisição para o formulário do laudo via IA/OCR; permitir ajuste manual dos dados extraídos | Tela de Formulário / Entrada | Tela | sim | Sim |
| Auxiliar a confecção de mapas temáticos com evidências do dano ambiental usando modelos pré-definidos | Editor de Mapas de Sensoriamento Remoto | perito | Imagens de satélite, camada de delimitação do dano, legenda, escala e indicação de norte | Selecionar modelo pré-definido e destacar vestígios do dano na imagem | Aplicar gabaritos e elementos cartográficos padrão do sistema sem necessidade de softwares externos | Tela de Edição / Mapeamento | Tela | sim | Sim |
| Unir o cabeçalho, os textos descritivos e os mapas em um único laudo consolidado | Gerador e Exportador de Laudo em PDF | perito | Prévia do laudo estruturado (cabeçalho, corpo de texto e mapas integrados) | Exportar documento final em PDF | O documento exportado deve respeitar a estrutura normativa de laudos ambientais e integrar os mapas no corpo do relatório | Artefato / Documento PDF | Documento | sim |  |


## 7. KPIs (nome = fórmula em uma linha)

| KPI | Pergunta | Fórmula | Fonte | Linha de base | Valor esperado | Como medir |
|---|---|---|---|---|---|---|
| Tempo de elaboração do laudo | Quanto tempo o perito gasta para preencher o cabeçalho, gerar o mapa e exportar o laudo completo? | Soma(Tempo de exportação - Tempo de início) / Total de laudos | Formulário de Controlo Pericial / Registos | 16 horas | 12 horas | Cronometrar a elaboração de 5 laudos no modelo tradicional |
| Taxa de erro no cabeçalho | Qual a percentagem de laudos que apresentam erros de digitação nos dados extraídos da requisição? | (Laudos com erro no cabeçalho / Total de laudos) * 100 | Fichas de Revisão e Devolução de Laudos | 15% | 0 | Analisar amostra de 20 laudos emitidos e contar correções manuais de cabeçalho |

**Período da linha de base:** Todos os registos de janeiro a dezembro de 2025: 120 laudos periciais ambientais elaborados e emitidos pela unidade pericial.
**Campos de data e tempo que existem:** O sistema atual possui apenas a data de recebimento da requisição e a data de assinatura/emissão do laudo, sem registo de hora/minuto. Por isso, a linha de base histórica mede o tempo total em dias. Para o MVP, serão capturados timestamps exatos (com hora, minuto e segundo) no navegador para medir a execução por minutos.

## 8. Stack: HTML único (CSS/JS inline), dados em JSON embutido, GitHub Pages.

**Stack escolhida:** HTML único + dados em arquivo JSON separado
**Detalhe da stack:** Um ficheiro index.html com HTML, CSS e JavaScript embutidos, utilizando dados sintéticos armazenados num array/JSON interno e bibliotecas JS open-source (como Leaflet para renderização do mapa e html2pdf/jspdf para compilação do relatório), publicado diretamente no GitHub Pages sem necessidade de servidor ou processo de build.
**Hospedagem:** Ficheiro HTML único publicado no GitHub Pages. Cabe inteiramente na conversa do agente de IA, não exige custos de infraestrutura de TI, roda diretamente no navegador sem necessidade de instalação de software externo pelo perito e permite validação imediata do MVP através de um link público.
**Custo e licenças:** Sem custo (R$ 0,00). O projeto utiliza exclusivamente a infraestrutura gratuita do GitHub Pages e bibliotecas open-source (Leaflet para visualização de mapas e html2pdf/jsPDF para geração do relatório). Caso uma API paga de extração por visão computacional ou imagens de satélite comerciais seja integrada futuramente na versão final, estima-se um custo entre R$ 50 e R$ 150 por mês.
**Contas e domínio:** O aluno cria a conta e o repositório no GitHub utilizando o e-mail institucional. O acesso é ativado via GitHub Pages gerando o subdomínio gratuito do projeto, ficando disponível para avaliação do docente e testes com os peritos.

| Opção | Tipo | Onde roda | Custo | Quem mantém | Acesso | Banco de dados | Escala | Limitação |
|---|---|---|---|---|---|---|---|---|
| GitHub Pages (Escolha Padrão) | Hospedagem Estática (PaaS) | Navegador do utilizador / CDN do GitHub | Gratuito (R$ 0) | Aluno / GitHub | Público via URL | Nenhum (JSON local / LocalStorage) | Média (Suficiente para MVP) | Não possui backend próprio; o processamento corre 100% no navegador do cliente. |
| Ficheiro HTML Local | Ficheiro Estático Local | Computador / Notebook do perito | Gratuito (R$ 0) | Perito / Aluno | Restrito ao dispositivo | Nenhum (Array JS embutido) | Individual (1 utilizador) | Dificulta a partilha e demonstração; exige envio manual do ficheiro por e-mail ou pen drive. |
| Firebase Hosting / Vercel | Hospedagem Cloud Estática | Nuvem / Servidor Web | Gratuito (Plano Free) | Aluno | Público via URL | Cloud Firestore / LocalStorage | Alta | Exige configuração de conta adicional e ferramentas de build (CLI) fora do padrão da aula. |


## 9. Restrições e LGPD

**Restrições:** A extração automática de dados depende do formato da requisição pericial (PDFs digitalizados como imagem exigem OCR, enquanto PDFs pesquisáveis facilitam a leitura). O app não possui integração direta em tempo real com sistemas de processo eletrónico ou bases de dados de satélite governamentais (ex.: INPE/PRODES), operando apenas com modelos e imagens armazenados localmente. Um opção seria integrar com o repositório de imagens do GEE.
**Dados pessoais tratados:** Nome e matrícula do perito responsável, bem como o nome do investigado/interessado constante na requisição pericial. Todos os dados utilizados no MVP são estritamente fictícios e sintéticos.
**Base legal:** Execução de procedimento administrativo/pericial e cumprimento de obrigação legal, nos termos do art. 7.º, II, da Lei 13.709/2018 (LGPD).
**Retenção:** Os dados do MVP permanecem apenas na memória do navegador (ou LocalStorage) e são apagados ao limpar a página ou reiniciar a sessão.
**Acesso e registro:** No MVP, qualquer pessoa com o link do protótipo consegue aceder. A interface simula o registo das ações do perito logado com carimbo de data e hora em cada etapa do preenchimento.
**Requisitos marcados:** LGPD e dado pessoal, Impressão em formato oficial, Nenhum (protótipo de aula)

---

# Anexo A — AS-IS (o fluxo de hoje)

**Início:** Envio da Requisição Pericial
**Fim:** Upload do laudo no Atena
**Entradas:** Requisição pericial
**Saídas:** laudo pericial assinado
**Volume:** 10 casos por mês
**Duração:** 16 horas por caso, em média
**Frequência:** Mensal
| Etapa | Quem faz | O que entra | Ação | O que sai | Sistema | Regra | Onde espera | Tempo (h) | Automatizável |
|---|---|---|---|---|---|---|---|---|---|
| 1 | protocolo Atena | Requisição | cadastro no sistema | numero de protocolo | sistema | não | adm | 0,2 | Sim, com apoio humano |
| 2 | Perito | requisição | Triagem | Requisicao | planilha | Realizável por Sensoriamento Remoto? Se sim, fazer laudo por SR; Se não, ir no local | Sistema Atena | 1 | Não |
| 3 | Perito | Requisição | Confecção de Mapas | Mapas | QGis | Caracterização e delimitação do Dano Ambiental | Sistema Atena | 12 | Sim, com apoio humano |
| 4 | Perito | Mapa | Confecção do Laudo | Laudo | GDocs | Explicar os mapas, unir informações e concluir o laudo | Sistema Atena | 4 | Pouco |

**Decisões e aprovações:** Se for possível a confecção dos mapas por Sensoriamento Remoto o laudo será elaborado em Cuiabá; Caso não seja possível fazê-lo por SR, um perito do interior deverá se deslocar até o local do crime para a realização de exame in loco.
**Exceções:** Requisições sem caracterização do local de crime com coordenada geográfica necessita de complementação por parte da delegacia. A complementação é feita via e-mail.
**Já digitalizado:** O envio da requisição da delegacia para a Politec é realizada via sistema Atena.

# Anexo B — TO-BE (o fluxo depois da mudança)

**Visão do futuro:** Quando o laudo for elaborado via aplicativo compatível com o sistema Atena, à partir de um modelo pré-definido, não será necessário utilizar softwares complementares para elaboração e assinatura dos laudos. As informações que correlacionam o laudo ao protocolo, requisição e quesitos já virão preenchidas.
**Mudança principal:** Preenchimento automático de informações redundantes; Confecção de mapas pré-definidos; Resposta dos quesitos por IA; Assinatura do laudo via sistema, sem necessidade de token externo.
**O que fica igual:** Cadastro do protocolo e triagem das requisições.
**O que não pode mudar:** O prazo legal de confecção do laudo, pois é estabelecido por legislação.
| Etapa | O que muda | Quem executa | Benefício | Esforço |
|---|---|---|---|---|
| Confecção de Mapas | Elaborado dentro do sistema, à partir de modelo pré-definido | A pessoa assistida pela máquina | padronização e redução do esforço | Médio |
| Confecção do laudo | Elaborado dentro do sistema, à partir de modelo pré-definido | A pessoa assistida pela máquina | padronização e redução do esforço | Médio |
| Assinatura do laudo | Assinado dentro do sistema, sem necessidade de aplicativo externo e de upload do laudo | A pessoa assistida pela máquina | redução do esforço | Baixo |

**Piloto do TO-BE:** Dentro da diretoria de Interiorização, por um único perito. Caso atenda as expectativas difundir para outros setores do interior.

# Anexo C — Pesquisa, riscos e plano

**Hipótese de campo:** A maior perda de tempo na elaboração do laudo ambiental não é a  a transcrição manual de dados redundantes da requisição e o manuseio de softwares externos de SIG para montar os mapas de evidência.
| Referência | Tipo | Fonte ou link | Ano | Dado que extrai | Como usar na defesa | Link conferido |
|---|---|---|---|---|---|---|
| Norma Técnica de Laudos Periciais Ambientais | Norma ou lei | Órgão Oficial de Perícia / Manual da Unidade | 2023 | Padrões de cabeçalho, estrutura do laudo e elementos obrigatórios no mapa (norte, escala e legenda) | Justifica a escolha das regras de negócio e o modelo de documento gerado em PDF | Sim |
| Relatório Anual de Produtividade Pericial | Dado oficial | Unidade Pericial Ambiental | 2024 | O tempo médio total de emissão de um laudo ambiental é de vários dias, com grande fatia gasta na formatação | Sustenta a necessidade de automação de processos repetitivos para aumentar a produtividade | Sim |

**Lacunas:** Não foi encontrada uma série temporal pública com o tempo exato despendido apenas no preenchimento de cabeçalhos e montagem de mapas. O tempo estimado de linha de base (180 minutos) baseia-se na observação direta de um número reduzido de casos e necessita de uma medição padronizada ao longo de 4 semanas para validação estatística.
| Marco | Data | Responsável | Depende de | Situação |
|---|---|---|---|---|
| M1: Definição do escopo e dados sintéticos | [Data 1] | Aluno | Validação dos modelos de requisição e mapa com o docente | Planejado |
| M2: Protótipo da interface (Cabeçalho + Editor de Mapa) | [Data 2] | Aluno | Estruturação do ficheiro HTML/JS único | Planejado |
| M3: Integração do gerador de PDF e publicação no GitHub Pages | [Data 3] | Aluno | Testes de exportação do relatório e upload do repositório | Planejado |
| M4: Teste de usabilidade e entrega final | [Data 4] | Aluno | Validação do fluxo completo de emissão do laudo pelo docente/perito | Planejado |

| Risco | Probabilidade | Impacto | Mitigação |
|---|---|---|---|
| Dificuldade na formatação do PDF final via biblioteca JavaScript | Média | Alto | Utilizar bibliotecas consolidadas (ex.: html2pdf.js ou jsPDF) e modelos HTML simples com estilos CSS bem definidos. |
| Incompatibilidade ou complexidade na manipulação do mapa no navegador | Média | Médio | Recorrer a bibliotecas leves como Leaflet.js com dados GeoJSON locais estáticos para simular as camadas do dano ambiental. |
| Atraso na validação dos campos obrigatórios do laudo | Baixa | Médio | Adotar como base os modelos padrão de laudos periciais já existentes no manual da unidade pericial. |

**Apoio necessário:** Preciso de uma validação de 30 minutos com a chefia pericial para aprovar os campos essenciais do cabeçalho e a disposição visual do mapa, além do acesso às imagens de satélite de exemplo.
**Aprendizado necessário:** Manipulação de bibliotecas de mapeamento web (ex.: Leaflet.js), conversão/renderização de documentos HTML para PDF no cliente (jsPDF / html2pdf), estruturação de dados sintéticos em JSON e publicação estática via GitHub Pages.

# Anexo D — A defesa

**Frase de defesa:** Se o tempo médio de elaboração do laudo passar de 16 horas para 10 horas, o perito deixa de perder tempo com transcrição de dados e softwares externos de SIG.
**Provas:** 15% dos laudos apresentam inconformidades ou erros de digitação no cabeçalho em relação à requisição. 2. São gastos 180 minutos por laudo para transcrever dados e compilar mapas de sensoriamento remoto em softwares externos. 3. Não existe integração nem padronização entre as requisições periciais e o formato final de exportação em PDF.
**Piloto:** Teste de uso do MVP durante 30 dias com a equipa de perícia ambiental, medindo o tempo total de elaboração dos laudos e a taxa de eliminação de erros no cabeçalho.
**Maior risco:** A chefia ou a norma pericial alterar a estrutura dos campos obrigatórios do laudo ou do formato do mapa. Mitigação: manter os modelos de layout desacoplados do código principal através de arquivos de configuração JSON, permitindo atualizações de versão sem reconstruir a aplicação.

# Anexo E — Documentos enviados

**Descrição dos documentos:** 551.2.22.9185.2026.067565-A01 - modelo de laudo ambiental
**O que ainda falta:** Falta o modelo em PDF das requisições periciais e captura das informações no sistema Atena.
