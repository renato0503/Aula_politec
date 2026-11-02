# Gestão de Documentos · processos e prazos do Gabinete

Cadastro, atribuição e acompanhamento dos processos do Gabinete de Direção, com o
prazo calculado e o sinal verde, amarelo ou vermelho. A cobrança automática é
simulada no MVP; a decisão e a assinatura continuam com as pessoas.

| Campo | Valor |
|---|---|
| Equipe | Vitória Araújo Dias |
| Contato | vitoriadias@politec.mt.gov.br |
| Unidade | Gabinete de Direção |
| Tipo | Aplicativo para servidor |
| Stack | HTML único (CSS/JS inline), IndexedDB, GitHub Pages |
| Fonte | `Aula 8/Entregas/Vitória Araújo.json` (29/10/2026) |
| GitHub | `Vitoriadias-droide` (Vitória) |

## Arquivos

- `envio-original.json`: o envio, sem alteração.
- `projeto.json` e `PROJETO.md`: o envio completado (sem campos vazios; o TO-BE
  está descrito nos campos do formulário).
- `contexto.md` e `sprint.md`: arquitetura e plano de construção.
- `app.json`, `src/app.js`, `exemplos/`, `index.html`.

## Pendências

- Confirmar com a chefia a matriz de papéis (requerente, servidor, analista e
  autoridade) e quem pode excluir documentos.
- O envio e o cronjob reais ficam fora do MVP: na versão de sala, a cobrança é
  registrada na trilha, sem SMTP.
- O TO-BE está descrito só em texto no envio; montar o diagrama em Mermaid no
  Sprint 3.
- A linha de base (1 h/dia, 200 processos/mês, 48 h na triagem) precisa ser
  medida no piloto de 30 dias.

## Como construir e testar

Este app é autônomo. `nucleo/`, `construir.py` e `testes/` são só dele e não
importam nada de `Apps/_base/`, porque esta pasta vai virar um repositório
próprio no GitHub. O `index.html` é **gerado**: edite as fontes (`app.json`,
`src/`, `nucleo/`, `exemplos/seed.json`) e rode a construção.

```powershell
cd "Apps/gestao-documentos"
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
