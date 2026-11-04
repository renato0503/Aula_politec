# Aula 9 — Continuidade dos MVPs e entrega final

**Módulo 10** — o caderno que fecha o curso. Ele não ensina a construir o app
do zero: ensina a **continuar** um MVP que já funciona, com GitHub, Antigravity,
testes, aceite e piloto.

Curso de Capacitação POLITEC/MT · Professor Renato Rosa · Dia 9.

---

## O que foi entregue

| Item | O que é |
|---|---|
| **Caderno** | `caderno-dia9.html`, com **58 seções** em 6 partes e tema claro/escuro |
| **Pacotes** | 21 arquivos em `pacotes/`, um por MVP, com repositório, pendências, integração passo a passo, testes e commit sugerido. Versão compactada: `Pacote-Continuidade.zip` |
| **PDF** | `Caderno Dia 9 - POLITEC.pdf`, com **88 páginas** e 58 seções no sumário paginado |
| **Público** | Alunos que vão baixar o ZIP do repositório, abrir a pasta no Antigravity e continuar a integração |

---

## Estrutura do caderno

| Parte | Conteúdo | Seções |
|---|---|---|
| Abertura | Boas-vindas, mapa, contrato e estado dos 21 MVPs | 4 |
| Parte 1 | GitHub do zero: conta, ZIP, clone, branch, commit, push, Pull Request, Pages e issues | 10 |
| Parte 2 | Antigravity e anatomia do app: arquivos, fluxo, agente, testes, dados e pendências | 8 |
| Parte 3 | Os 21 MVPs, um pacote por app | 21 |
| Parte 4 | Receitas de integração: e-mail, Sheets, OCR, Earth, QR, Firestore e biometria | 7 |
| Parte 5 | Equipe: papéis, revisão, aceite, piloto e entrega | 5 |
| Parte 6 | Fechamento: checklist, erros, quiz, glossário e referências | 5 |

**Total:** 58 seções.

---

## Os 21 pacotes

Cada pacote tem a mesma estrutura:

1. O que o app faz.
2. O que já está pronto.
3. O que falta.
4. Baixar e abrir no Antigravity.
5. Integração que falta, passo a passo.
6. Como testar.
7. Enviar para o GitHub.
8. Prompt para o Antigravity.
9. Onde pedir ajuda.

Índice completo: [`pacotes/README.md`](pacotes/README.md). Pacote compactado: [`Pacote-Continuidade.zip`](Pacote-Continuidade.zip).

| App | Equipe | Repositório |
|---|---|---|
| Controle de Adiantamentos | Jaqueline e Linicker | [adiantamento](https://github.com/renato0503/adiantamento) |
| Agendamento CIN | Elthon | [agendamento-cin](https://github.com/renato0503/agendamento-cin) |
| Agiliza+ | Diego, Francineide, Andreia e Eric | [agiliza-mais](https://github.com/renato0503/agiliza-mais) |
| Segunda via da CIN | André, Flávia e Glauce | [cin-segunda-via](https://github.com/renato0503/cin-segunda-via) |
| Comissão de Ética | Letícia e Thiago | [comissao-etica-denuncias](https://github.com/renato0503/comissao-etica-denuncias) |
| Controle do Processo de Aquisição | Kasteline | [controle-aquisicoes](https://github.com/renato0503/controle-aquisicoes) |
| Custódia Definitiva | Edjane Ávila | [custodia-definitiva](https://github.com/renato0503/custodia-definitiva) |
| DOCUMENTAPOLITEC | Aline Xavier | [documentapolitec](https://github.com/renato0503/documentapolitec) |
| Mapa de Equipamentos | João Lucas | [equipamentos-google-earth](https://github.com/renato0503/equipamentos-google-earth) |
| Gestão de Documentos | Vitória Araújo | [gestao-documentos](https://github.com/renato0503/gestao-documentos) |
| NIHDE · Gestão de Identificados | Kesia Melo | [gestao_identificados](https://github.com/renato0503/gestao_identificados) |
| Hórus · Banco de Demandas | Iohan | [horus-banco-demandas](https://github.com/renato0503/horus-banco-demandas) |
| Inscrições em Cursos | Edilaura Rondon | [inscricoes-cursos](https://github.com/renato0503/inscricoes-cursos) |
| Mapa de Distribuição | Igor Henrique | [mapa-distribuicao-credor](https://github.com/renato0503/mapa-distribuicao-credor) |
| Metas pelo BI | Karine Assunção | [metas-bi-ocr](https://github.com/renato0503/metas-bi-ocr) |
| Passivo Ambiental | Fábio | [passivo-ambiental](https://github.com/renato0503/passivo-ambiental) |
| Renovação de Contratos | Rodrigo Neves | [renovacao-contratos-horus](https://github.com/renato0503/renovacao-contratos-horus) |
| Registro de Não Conformidade | Sabrina Ellen | [rnc-nao-conformidade](https://github.com/renato0503/rnc-nao-conformidade) |
| TAP Digital | Danielle, Cristiane e Luciana | [tap-portfolio-projetos](https://github.com/renato0503/tap-portfolio-projetos) |
| TEIA · Triagem de E-mails | Nelson e Helen | [teia-triagem-emails](https://github.com/renato0503/teia-triagem-emails) |
| TCIN · Trilha de Custódia | Silmara Bueno | [trilha-custodia-necropsia](https://github.com/renato0503/trilha-custodia-necropsia) |

---

## Como gerar

```powershell
python "Aula 9/gerar_caderno_aula9.py"   # HTML e os 21 pacotes
python validar.py 9                        # precisa imprimir OK
python exportar_pdf.py 9                   # PDF em 2 passadas
```

O gerador lê os dados de `Aula 9/dados_apps.py`. Para corrigir um nome, uma
pendência ou um link, edite esse arquivo e rode o gerador de novo. Não edite o
`caderno-dia9.html` à mão.

---

## Regra de ouro para os alunos

- O `index.html` é gerado. Edite `src/`, `app.json`, `nucleo/`, `exemplos/` e
  `modelos/`.
- Depois de alterar, rode `python construir.py` e os testes.
- Uma branch por tarefa, um Pull Request por tarefa.
- Nunca suba token, senha, backup real ou dado pessoal.
- O aceite e o piloto ficam registrados no repositório.
