# Segunda via da CIN a distância

Pedido da segunda via da Carteira de Identidade Nacional sem ir ao posto,
quando a primeira via ainda está válida e os dados não mudaram. O pedido chega
pronto ao servidor, que confere e lança no sistema de identificação civil.

| Campo | Valor |
|---|---|
| Equipe | André, Flávia e Glauce (sobrenomes a confirmar) |
| Contato | glaucesilva@politec.mt.gov.br |
| Unidade | POLITEC, Identificação Civil |
| Tipo | Aplicativo para cidadão |
| Stack pedida | HTML único, GitHub Pages; app de celular com coleta biométrica por foto |
| Fonte | `Aula 8/Entregas/Emisso-2via-da-CIN-remoto-2026-10-27 (1).json` (29/10/2026 10:00, horário de Cuiabá) |

## Arquivos

- `envio-original.json`: o envio, sem alteração.
- `projeto.json` e `PROJETO.md`: o envio completado (ver abaixo).
- `contexto.md` e `sprint.md`: arquitetura e plano de construção.

## Pendências

- **Biometria é dado pessoal sensível** (LGPD, art. 11). O MVP não coleta
  biometria real: a foto do teste é fictícia e fica no navegador. A coleta
  remota em produção depende da empresa contratada, da TI e do encarregado de dados.
- O MVP sugeria "biometria de servidores do setor" como dado de teste. O
  `contexto.md` troca por fotos fictícias, sem pessoas reais.
- Mesmo domínio do **agendamento-cin** (Elthon). Os dois projetos podem se
  conectar: o pedido recusado vira um agendamento no posto.

## Completado pelo professor (29/10/2026)

O `projeto.json` e o `PROJETO.md` desta pasta foram completados com propostas próximas do
que o aluno escreveu. O envio original está em `envio-original.json`.
Tudo o que foi completado precisa ser confirmado com o aluno no Sprint 0.

**Campos preenchidos (estavam vazios):** `evid_detalhe`, `doc_descricao`, `doc_faltando`.

**Campos substituídos:**

- `mvp_objetivo`: o MVP previa app nativo e biometria de servidores; ajustado para protótipo web com dados fictícios, por ser dado sensível. Os demais campos foram detalhados a partir do envio.
- `mvp_plataforma`: o MVP previa app nativo e biometria de servidores; ajustado para protótipo web com dados fictícios, por ser dado sensível. Os demais campos foram detalhados a partir do envio.
- `mvp_criterio`: o MVP previa app nativo e biometria de servidores; ajustado para protótipo web com dados fictícios, por ser dado sensível. Os demais campos foram detalhados a partir do envio.
- `mvp_dados`: o MVP previa app nativo e biometria de servidores; ajustado para protótipo web com dados fictícios, por ser dado sensível. Os demais campos foram detalhados a partir do envio.
- `mvp_mock`: o MVP previa app nativo e biometria de servidores; ajustado para protótipo web com dados fictícios, por ser dado sensível. Os demais campos foram detalhados a partir do envio.
- `mvp_naofaz`: o MVP previa app nativo e biometria de servidores; ajustado para protótipo web com dados fictícios, por ser dado sensível. Os demais campos foram detalhados a partir do envio.
- `hospedagem_escolhida`: o MVP previa app nativo e biometria de servidores; ajustado para protótipo web com dados fictícios, por ser dado sensível. Os demais campos foram detalhados a partir do envio.
- `lgpd_dados`: o MVP previa app nativo e biometria de servidores; ajustado para protótipo web com dados fictícios, por ser dado sensível. Os demais campos foram detalhados a partir do envio.
- `lgpd_retencao`: o MVP previa app nativo e biometria de servidores; ajustado para protótipo web com dados fictícios, por ser dado sensível. Os demais campos foram detalhados a partir do envio.
- `stack_detalhe`: o MVP previa app nativo e biometria de servidores; ajustado para protótipo web com dados fictícios, por ser dado sensível. Os demais campos foram detalhados a partir do envio.
- `lacunas`: o MVP previa app nativo e biometria de servidores; ajustado para protótipo web com dados fictícios, por ser dado sensível. Os demais campos foram detalhados a partir do envio.

**Tabelas:**

- AS-IS (`tAsIs`): refeita. A coluna regra estava com "Regra" em todas as linhas; preenchida a partir das decisões do AS-IS.
- telas e artefatos (`tArtefatos`): refeita. As colunas vieram deslocadas; realinhadas e com as telas do critério de aceite.
- entidades (`tEntidades`): refeita. As colunas vieram em texto livre; organizadas no formato nome: tipo.
- regras de negócio (`tRegras`): linhas acrescentadas. Acrescentadas a elegibilidade (o público do app) e a retenção.
- métricas (`tMetricas`): linhas acrescentadas. Acrescentada a métrica que mede o público do app.
- riscos (`tRiscos`): linhas acrescentadas. Acrescentados os riscos de biometria.
- referências (`tRefs`): refeita. A referência enviada não tinha fonte.

**Marcações:**

- `req`: acrescentado Funcionar offline (o pedido pode ser preenchido sem sinal e enviado depois).

## Como construir e testar

Este app é autônomo. `nucleo/`, `construir.py` e `testes/` são só dele e não
importam nada de `Apps/_base/`, porque esta pasta vai virar um repositório
próprio no GitHub. O `index.html` é **gerado**: edite as fontes (`app.json`,
`src/`, `nucleo/`, `exemplos/seed.json`) e rode a construção.

```powershell
cd "Apps/cin-segunda-via"
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

A área do cidadão é uma coluna única, com cabeçalho claro, fonte arredondada e
cantos redondos. A tela-assinatura do servidor é a **caixa de entrada**: a fila
fica à esquerda, o pedido aberto à direita, e a decisão não obriga a voltar à
lista, porque os botões são “Aceitar e próximo” e “Recusar e próximo”. A busca
cobre protocolo, nome e CPF; cada item mostra a espera em horas ou dias, a
elegibilidade e a situação em selo. Atalhos: J e K percorrem, A aceita e R leva
ao motivo da recusa. Código em `src/identidade.js` e `src/app.css`.

## Mapa do processo

O `processo.html` mostra o **AS-IS** (como o processo funciona antes do MVP) e o
**TO-BE** (como fica com o MVP), com as métricas, regras e papéis do projeto.
Abra ao lado do `index.html`.
