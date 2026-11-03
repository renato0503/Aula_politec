# NIHDE · Gestão de Identificados

Registro único dos corpos **não identificados** e dos **identificados não
reclamados**: entrada, características físicas, quatro exames de identificação
(necropapiloscopia, DNA, odontologia e antropologia), família, sepultamento pelo
município, identificação depois do sepultamento e relatório.

| Campo | Valor |
|---|---|
| Aluna | Kesia Melo |
| Contato | nih@politec.mt.gov.br |
| Unidade | NIHDE · Núcleo de Identificação Humana e Desaparecidos |
| Tipo | Aplicativo web / portal |
| Stack | HTML único, IndexedDB, GitHub Pages |
| Fonte | `envio-original.json` e cinco áudios de 03/11/2026 |

## Arquivos

- `envio-original.json`: o envio da aluna, sem alteração.
- `TRANSCRICAO.md` e `TRANSCRICAO-GEMINI.md`: os áudios.
- `CONTEXTO-AUDIOS.md`: o que os áudios acrescentam ao envio.
- `PROJETO.md`, `contexto.md` e `sprint.md`: o projeto completado, a arquitetura
  e o plano.
- `app.json`, `src/app.js`, `exemplos/seed.json`, `index.html`: o app.
- `modelos/roteiro-aceite.md`: o roteiro do piloto.

## O que o MVP responde

**Quantos corpos não identificados a POLITEC tem, sepultados ou não?** O painel
mostra o total, por unidade e por situação; a ficha mostra os exames, a
identificação, a família, o sepultamento e a auditoria.

## Como construir e testar

```powershell
cd "Apps/gestao_identificados"
python exemplos/gerar_exemplos.py   # 24 corpos fictícios, semente fixa
python construir.py                 # gera o index.html
python testes/testar.py             # estrutura, zero rede, #/testes, rotas e tema
python testes/cenarios.py           # painel, identificação, família, sepultamento, CSV
```

## Pendências

- Confirmar com a Kesia e a direção da POLITEC o nome oficial (NIHDE), o escopo
  dos dados físicos no MVP e a integração com o Atena.
- O **módulo de desaparecidos** está em `desaparecidos.html` (painel do CNPD/MJ com 381 registros), ligado pelo painel do app. O contrato está em `docs/CONTRATO-DESAPARECIDOS.md`; a base pública fica separada do cadastro dos corpos. A integração com outros estados é fase 2.
- O login por matrícula é simulado; a autenticação real depende da TI.
- O piloto de 90 dias no IML de Cuiabá depende do aceite da chefia.
- A lista mostra iniciais; nome da família e local do sepultamento exigem acesso
  restrito na versão institucional (LGPD).
