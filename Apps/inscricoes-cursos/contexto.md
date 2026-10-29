# Gestão Dinâmica de Inscrições em Cursos · contexto e arquitetura

> Aluna: Edilaura Rondon (Gerência de Formação Inicial e Continuada)
> Fonte: `PROJETO.md` (versão de 29/10/2026 08:56) e a decisão de arquitetura do
> professor: **HTML monolítico, offline first**.
>
> Os trechos do formulário que tratam de "transações financeiras", "clientes",
> CNPJ, Render e Supabase não descrevem este processo e ficaram de fora. Os
> itens marcados com **[proposta]** precisam da confirmação da aluna no Sprint 0.

---

## 1. O problema

Hoje a Gerência de Formação divulga o curso e distribui as vagas por e-mail às
diretorias. Cada diretoria escolhe os servidores (titulares e reserva) e
responde também por e-mail. Em seguida, a gerência copia os dados para uma
planilha Excel (nome, lotação, matrícula, CPF, telefone e e-mail) e envia a
planilha ao responsável pelo curso.

| Dado do AS-IS | Valor informado |
|---|---|
| Volume | 50 inscrições por mês |
| Espera na etapa de retorno das indicações | 36 h |
| Esforço da gerência | 40 h por semana |
| Regra de efetivação | ordem de indicação da diretoria |
| Exceção | desistência do titular chama o cadastro de reserva |

**Dor**: as vagas são mal distribuídas porque as diretorias e os servidores
demoram a responder, e não existe cadastro padronizado. Por isso, a gerência
redigita dados que chegam em formatos diferentes, e erros de matrícula ou de
e-mail aparecem só na hora de convocar.

## 2. O que o MVP faz e o que não faz

| Faz | Não faz (texto da aluna) |
|---|---|
| Formulário de inscrição padronizado, com validação | Integração em tempo real com o RH (SEAP) |
| Comprovante imediato "em análise" para o servidor | Emissão e envio de certificados |
| Painel de triagem por diretoria (titular, reserva, não selecionado) | Painéis de BI |
| Mensagens padronizadas de confirmação e convocação | Reescalonamento automático do cadastro de reserva |
| Conferência da matrícula contra o relatório exportado do SEAP | Login corporativo (SSO) |
| Lista final do curso em CSV | Decidir quem fica com a vaga (é da diretoria) |

**Critério de aceite** (adaptado das 4 condições da aluna):

1. Toda inscrição enviada entra na base da gerência sem redigitação, e o envio
   com campo obrigatório vazio ou inválido é bloqueado.
2. O servidor recebe o comprovante "em análise" no momento do envio.
3. Cada diretoria vê só os inscritos dela, ordena titulares e reserva e devolve
   a decisão sem ambiguidade.
4. Os selecionados recebem a convocação com o link do grupo oficial da turma.

## 3. Decisão de arquitetura: HTML monolítico, offline first

A aluna propôs Forms + planilha + Power Automate. A arquitetura do curso troca
isso por **um único arquivo `index.html`**, que serve aos três papéis. O
arquivo pode ficar no GitHub Pages (para o servidor abrir pelo link) e também
abre por duplo clique. Depois de carregado, ele funciona sem internet.

O ponto difícil é que um app offline **não tem servidor para receber as
inscrições**. A solução usa o canal que a POLITEC já tem, o **e-mail
institucional**, e um bloco de dados que o app lê de volta:

```mermaid
flowchart LR
  G1[Gerência<br/>cria o curso] -->|link com o curso no endereço| S[Servidor<br/>abre #/inscricao]
  S -->|valida e mostra<br/>comprovante| C[Comprovante<br/>em análise]
  S -->|mailto: com bloco<br/>INSCRICAO-v1| M[(Caixa<br/>capacitacao@)]
  M -->|regra do Outlook<br/>responde na hora| S
  M -->|gerência cola os blocos| G2[Gerência<br/>#/inscritos]
  G2 -->|exporta arquivo<br/>da diretoria| D[Diretoria<br/>#/triagem]
  D -->|devolve arquivo<br/>com a decisão| G3[Gerência<br/>#/convocacao]
  G3 -->|mailto: titular e reserva<br/>com link do grupo| S
```

| Necessidade | Como o HTML monolítico atende |
|---|---|
| O servidor se inscrever sem instalar nada | Abre o link `index.html#/inscricao?c=...`. O curso vem codificado no endereço |
| Confirmação imediata | O comprovante aparece na tela, com protocolo. A regra de resposta automática do Outlook da caixa `capacitacao@` responde ao e-mail **[validar com a TI]** |
| A gerência receber os dados sem redigitar | O e-mail leva o bloco `INSCRICAO-v1:<dados>`. A gerência cola vários e-mails de uma vez em `#/importar` |
| Triagem pela diretoria | A gerência exporta `triagem-<DIRETORIA>.json`. A diretoria abre no mesmo `index.html`, ordena e devolve |
| Convocação | O app gera a mensagem de cada selecionado (titular ou reserva) com o link do grupo, via `mailto:` ou cópia |
| Sem custo, sem servidor | Nenhum backend. Os dados ficam no IndexedDB da gerência |

### 3.1 Princípios

1. **Um arquivo só**, com CSS, JS e a biblioteca de QR Code embutidos.
2. **Offline first**: o IndexedDB da gerência é a base. Cada troca entre
   papéis acontece por arquivo `.json` ou por e-mail.
3. **Perfis da cópia**: o mesmo arquivo abre como *Inscrição*, *Diretoria* ou
   *Gerência*. O perfil escolhe as telas, mas não é controle de segurança.
4. **Dado mínimo**: matrícula, nome, lotação, e-mail institucional e telefone
   opcional. Sem CPF **[proposta]**.
5. **A decisão é da diretoria**: o app ordena e comunica, mas não escolhe.

### 3.2 Estrutura de pastas

```
Apps/inscricoes-cursos/
├── index.html          ← o app (servidor, diretoria e gerência)
├── contexto.md
├── sprint.md
├── PROJETO.md
├── projeto.json
├── vendor/             ← qrcode-generator minificado + VERSOES.md
├── modelos/
│   └── mensagens.md    ← textos das mensagens (comprovante, convocação, reserva)
├── exemplos/
│   ├── curso-ficticio.json
│   ├── emails-ficticios.txt     ← 60 e-mails com o bloco INSCRICAO-v1
│   └── seap-ficticio.csv        ← relatório de servidores ativos (fictício)
└── testes/testes.html
```

## 4. Telas (rotas)

| Rota | Perfil | O que faz |
|---|---|---|
| `#/inscricao?c=...` | Servidor | Vê o curso, preenche, declara os pré-requisitos, envia, recebe o comprovante |
| `#/cursos` | Gerência | Cria o curso: datas, vagas por diretoria, pré-requisitos, link do grupo oficial, prazo de triagem |
| `#/divulgar/:curso` | Gerência | Gera o link e o QR Code da inscrição e o texto de divulgação |
| `#/importar` | Gerência | Cola os blocos dos e-mails ou importa CSV. Mostra novos, duplicados e inválidos |
| `#/inscritos/:curso` | Gerência | Lista, confere a matrícula com o SEAP, exporta o arquivo de cada diretoria |
| `#/triagem` | Diretoria | Importa o arquivo, ordena titulares e reserva até o limite de vagas, devolve o arquivo |
| `#/convocacao/:curso` | Gerência | Importa as decisões, gera as mensagens de convocação e reserva, marca enviada |
| `#/turma/:curso` | Gerência | Lista final (CSV), desistências e chamada manual da reserva |
| `#/config` | Gerência | Perfil, endereço da caixa, retenção, backup `.json`, limpar dados |

## 5. Modelo de dados (IndexedDB `inscricoes_politec_v1`)

| Store | Chave | Campos |
|---|---|---|
| `cursos` | `id` | nome, carga_horaria, inicio, fim, local, prerequisitos[], vagas_por_diretoria{}, link_grupo, prazo_triagem, status |
| `inscricoes` | `protocolo` | curso_id, matricula, nome, lotacao, diretoria, email, telefone, prerequisitos_declarados[], enviado_em, recebido_em, status |
| `triagens` | `id` | curso_id, diretoria, protocolo, decisao (titular, reserva, não selecionado), ordem, decidido_em |
| `convocacoes` | `id` | protocolo, tipo (titular, reserva), mensagem_gerada_em, enviada_em, confirmou_presenca |
| `seap` | `matricula` | nome, cargo, lotacao, vinculo_ativo (importado do relatório) |
| `log` | `id` | data_hora, acao, protocolo, detalhe |

**Status da inscrição**: `em análise` → `titular` ou `reserva` ou `não
selecionado` → `convocado` → `confirmado` ou `desistente`.

O **protocolo** é gerado no navegador do servidor (curso + matrícula + data,
resumido em 8 caracteres). Por isso, o mesmo protocolo aparece no comprovante,
no e-mail e na base da gerência.

## 6. Regras de negócio

| ID | Regra | Tipo |
|---|---|---|
| RN01 | Campos obrigatórios: matrícula, nome, lotação, diretoria, e-mail | Validação |
| RN02 | E-mail precisa terminar em `@politec.mt.gov.br` **[proposta]** | Validação |
| RN03 | Uma inscrição por matrícula e curso. Reenvio substitui a anterior e fica no log | Validação |
| RN04 | Inscrição fora do período do curso é recusada na tela | Validação |
| RN05 | Matrícula ausente do relatório do SEAP vira alerta para a gerência, sem recusar | Validação |
| RN06 | A diretoria não marca mais titulares que as vagas dela (regra do papel "chefia") | Negócio |
| RN07 | A efetivação segue a ordem definida pela diretoria. A gerência não altera a ordem | Negócio |
| RN08 | Só recebe o link do grupo quem foi marcado como titular, ou reserva chamado | Negócio |
| RN09 | Desistência de titular: a gerência chama o próximo da reserva da mesma diretoria, com um clique e confirmação | Negócio |
| RN10 | Dados dos inscritos são apagados 30 dias após o fim do curso. Fica só a contagem | LGPD |

## 7. LGPD

- **Finalidade**: inscrição e seleção para capacitação.
- **Minimização**: sem CPF. A matrícula identifica o servidor no SEAP.
  Telefone é opcional.
- **Retenção**: 30 dias após o fim do curso (informado pela aluna). Ao abrir, o
  app avisa quais cursos passaram do prazo e oferece a limpeza (RN10).
- **O bloco do e-mail não é criptografia.** Ele só evita a redigitação. Por
  isso, o e-mail vai para a caixa institucional e não leva dado além do mínimo.
- **Acesso**: a base completa fica só no computador da gerência. A diretoria
  recebe apenas os inscritos dela.

## 8. KPIs

| KPI | Fórmula | Linha de base |
|---|---|---|
| Tempo até a lista final | data da lista final − data da divulgação | medir 2 cursos antes do piloto |
| Espera pela indicação | retorno da diretoria − envio do arquivo de triagem | 36 h (AS-IS) |
| Inscrições com erro de dado | inscrições corrigidas pela gerência ÷ total × 100 | medir na planilha atual |
| Vagas ociosas | vagas − confirmados, por curso | medir nos cursos recentes |
| Redigitação | campos digitados pela gerência por inscrição | meta: 0 |

## 9. Riscos de arquitetura

| Risco | Mitigação |
|---|---|
| O cliente de e-mail corta o corpo longo do `mailto:` | Bloco curto (só os campos mínimos) e botão "copiar o bloco" como alternativa |
| A TI não libera a regra de resposta automática | O comprovante na tela vale como confirmação, e o e-mail enviado fica na caixa do servidor |
| Servidor edita o bloco no e-mail | O bloco leva um código de verificação, e o app acusa bloco alterado |
| Diretoria perde o arquivo de triagem | A gerência reexporta a qualquer momento |
| Base só no computador da gerência | Backup `.json` semanal e `navigator.storage.persist()` |
