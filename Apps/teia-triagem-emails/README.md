# TEIA · Triagem de E-mails com Isolação Automatizada

Painel local do triador para a Coordenação de Perícias em Biologia Molecular.
Recebe a fila de e-mails de requisição, mostra os 9 campos essenciais extraídos
com confiança e alertas, e registra a validação humana. O protótipo não envia
nada para fora: a extração é simulada com os dados fictícios.

| Campo | Valor |
|---|---|
| Alunos | Nelson e Helen Coelho Gonçalves |
| Contato | nelsonyoshitake@politec.mt.gov.br |
| Unidade | Coordenação de Perícias em Biologia Molecular |
| Tipo | Automação de script ou rotina |
| Fonte | `envio-original.json` (Firestore, 03/11/2026) |
| App anterior da dupla | `distribuicao-casos-dna` (projeto de distribuição de DNA) |

## Arquivos

- `envio-original.json`: a entrada do formulário, sem alteração.
- `projeto.json` e `PROJETO.md`: o projeto completado (AS-IS, TO-BE, MVP, regras e métricas).
- `processo.html`: o hub AS-IS → TO-BE + MVP, em HTML separado.
- `contexto.md` e `sprint.md`: arquitetura e plano de construção.

## Identidade e usabilidade

A identidade é de bancada de triagem: casca de ferramenta, cabeçalho compacto,
fonte monoespaçada, densidade compacta, cantos retos e superfícies planas. A
tela-assinatura é a **bancada**: a fila de e-mails à esquerda e os 9 campos à
direita, com a confiança da extração, os alertas de divergência/OCR e a
validação humana. O app tem dois perfis: servidor triador e chefia da triagem.

## Como construir e testar

```powershell
cd "Apps/teia-triagem-emails"
python construir.py
python testes/testar.py
python testes/cenarios.py
python testes/jornada.py
```

Antes da primeira execução: `pip install playwright` e `playwright install chromium`.

Lightpanda (via WSL, CDP em 9222 e HTTP em 8000):

```powershell
python testes/jornada.py --cdp http://127.0.0.1:9222 --base http://127.0.0.1:8000
```

## Limites do protótipo

O parsing de e-mails reais, o OCR de PDF imagem, a renomeação de arquivos e a
integração com a caixa institucional ficam para o script local. O app representa
o painel do triador e usa a caixa fictícia de `exemplos/seed.json`.
