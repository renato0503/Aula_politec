# Aula 7 — Gargalo medido, automação e Antigravity

**Módulo 9** — a aula que fecha o ciclo do novo formato do curso: a manhã é
sempre de **painéis, BI e análise de dados**; a tarde é de **hands-on em gestão
de projetos**, automação e digitalização, com **Antigravity** (Google) e
**GitHub** como ferramentas de construção.

Os cinco processos desta aula são **novos**. A turma não redesenha o workflow:
ela mede o gargalo no painel, propõe a intervenção com número e constrói o app
do cenário no GitHub, com o agente do Antigravity.

Curso de Capacitação POLITEC/MT · Professor Renato Rosa · Dia 7.

---

## O que foi feito nesta entrega

| Item | O que foi feito |
|---|---|
| **Cenários** | 5 processos novos da POLITEC/MT: apreensão e perícia de armas, sinistro de trânsito, credenciamento de peritos, operação de etilometria, atendimento e ouvidoria |
| **Datasets** | 5 datasets em modelo estrela, com **58.408 execuções de etapa** no total, gerados por `gerar_datasets_aula7.py` (semente fixa `20261027`) |
| **Workbooks** | 5 arquivos `.xlsx`, um por cenário, com 9 abas (`LEIA-ME` + fato + 7 dimensões), guia de uso, dicionário e tabela-resumo medida |
| **Receitas** | 5 receitas de painel em **8 blocos e 96 passos**, do Excel ao Power BI, com caminho de menu, o que esperar na tela e o que fazer quando dá erro |
| **Medidas** | 11 medidas por cenário: 8 base, 3 do Pareto e 1 específica do processo, todas com o DAX pronto para copiar |
| **Tarde** | Leitura comparada dos 5 gargalos, catálogo de 10 intervenções, matriz gargalo x intervenção, cálculo de ganho, business case, roadmap em 4 fases e proposta de solução para cada cenário |
| **Antigravity** | Aulão de 10 seções, botão por botão: instalação, janela, painel do agente, Agent Manager, modelos, terminal e painel de versão, artefatos, permissões, comandos de barra e Remote Control |
| **GitHub** | Seção com os comandos para conectar a conta pelo navegador, publicar o projeto e o fluxo diário de versionamento |
| **PDF** | `Caderno Dia 7 - POLITEC.pdf` com **135 páginas** e 68 seções no sumário paginado, em 2 passadas |

---

## Onde baixar

| Arquivo | Caminho no site |
|---|---|
| Caderno (HTML) | `Aula 7/caderno-dia7.html` |
| Workbook do Cenário 1 | `Aula 7/datasets/cenario1_apreensao_armas/Cenario1_Apreensao_Armas.xlsx` |
| Workbook do Cenário 2 | `Aula 7/datasets/cenario2_sinistro_transito/Cenario2_Sinistro_Transito.xlsx` |
| Workbook do Cenário 3 | `Aula 7/datasets/cenario3_credenciamento_peritos/Cenario3_Credenciamento_Peritos.xlsx` |
| Workbook do Cenário 4 | `Aula 7/datasets/cenario4_etilometria/Cenario4_Etilometria.xlsx` |
| Workbook do Cenário 5 | `Aula 7/datasets/cenario5_atendimento_ouvidoria/Cenario5_Atendimento_Ouvidoria.xlsx` |

---

## O dia em dois turnos

| Turno | Foco | Entregável |
|---|---|---|
| **Manhã (08h–12h)** | Painéis, BI e análise de dados | **Um painel de processo** por cenário, com 11 medidas, 9 visuais, 4 segmentações e a hipótese do gargalo em uma frase |
| **Tarde (13h–17h)** | Gargalo, automação, Antigravity e GitHub | **TO-BE em Mermaid**, cálculo do ganho, **app no GitHub** e primeira versão publicada |

---

## Estrutura do caderno (12 partes, 68 seções)

| Parte | Conteúdo | Seções |
|---|---|---|
| Abertura | Como usar o dia, mapa e pré-requisitos | 3 |
| Parte 1 | Cenário 1: apreensão e perícia de armas | 4 |
| Parte 2 | Cenário 2: sinistro de trânsito | 4 |
| Parte 3 | Cenário 3: credenciamento de peritos | 4 |
| Parte 4 | Cenário 4: operação de etilometria | 4 |
| Parte 5 | Cenário 5: atendimento e ouvidoria | 4 |
| Parte 6 | Do painel ao gargalo: os cinco na mesma régua | 5 |
| Parte 7 | Gargalo, automação e digitalização | 7 |
| Parte 8 | A solução proposta para cada cenário | 5 |
| Parte 9 | Aulão de Antigravity | 11 |
| Parte 10 | O GitHub conectado ao Antigravity | 3 |
| Parte 11 | Prática guiada: 8 labs | 9 |
| Parte 12 | Fechamento: método, erros, quiz, glossário, referências | 5 |

---

## Os cinco cenários e os gargalos medidos

| # | Cenário | Execuções | Gargalo | Share | 2ª etapa | Top 2 |
|---|---|---|---|---|---|---|
| 1 | Apreensão e perícia de armas | 11.312 | Prova de fogo | 40,3% | Registro no SINARM (21,3%) | 61,6% |
| 2 | Sinistro de trânsito | 11.336 | Conferência de documentos | 35,7% | Parecer com a seguradora (19,3%) | 55,0% |
| 3 | Credenciamento de peritos | 10.152 | Análise de currículo | 31,3% | Parecer da comissão (18,2%) | 49,5% |
| 4 | Operação de etilometria | 12.176 | Emissão do auto de infração | 28,9% | Conferência do aparelho (28,1%) | 57,0% |
| 5 | Atendimento e ouvidoria | 13.432 | Instrução | 35,5% | Resposta formal (18,7%) | 54,2% |

Padrão dos cinco: a espera representa de 92,1% a 97,2% do tempo do processo, e
duas etapas concentram de 49,5% a 61,6% de toda a espera.

---

## Os labs

| Lab | Turno | Entregável | Tempo |
|---|---|---|---|
| 1. Montar o painel do seu cenário | Manhã | Arquivo `.pbix` com cartões, barras, Pareto, matriz e linha do tempo | 90 min |
| 2. Revisar modelo e medidas | Manhã | Números do painel batendo com a aba LEIA-ME | 45 min |
| 3. Escrever a hipótese do gargalo | Manhã | Uma frase com número e fonte | 20 min |
| 4. Escrever a proposta de solução | Tarde | TO-BE em Mermaid e cálculo do ganho | 45 min |
| 5. Instalar o Antigravity e abrir o projeto | Tarde | Projeto criado e agente respondendo | 40 min |
| 6. Conectar o GitHub pelo navegador | Tarde | Conta conectada e repositório criado | 30 min |
| 7. Pedir o app ao agente e revisar o diff | Tarde | App gerado, diff lido e primeira versão | 60 min |
| 8. Publicar a primeira versão | Tarde | Push no GitHub e pull request aberto | 40 min |

---

## Os comandos do GitHub, em um lugar só

```bash
# 1. instalar a ferramenta oficial do GitHub (Windows, PowerShell)
winget install --id GitHub.cli

# 2. entrar com a conta pelo navegador (abre a pagina de autorizacao)
gh auth login --hostname github.com --git-protocol https --web

# 3. conferir e ligar o Git a essa conta
gh auth status
gh auth setup-git

# 4. criar o repositorio privado e publicar de uma vez
gh repo create politec-mini-app --private --source=. --remote=origin --push

# 5. fluxo do dia a dia
git status
git add .
git commit -m "Aula 7: formulario de abertura de protocolo"
git push
```

O caminho pela interface também está no caderno: botão de conta no canto
inferior direito do Antigravity, provedor GitHub, autorização no navegador.

---

## Como reproduzir

```powershell
python "Aula 7\gerar_datasets_aula7.py"   # gera os 5 datasets (CSV)
python "Aula 7\gerar_excel_aula7.py"      # empacota os 5 workbooks
python "Aula 7\gerar_caderno_aula7.py"    # gera o HTML do caderno
python validar.py 7                       # precisa imprimir OK
python exportar_pdf.py 7                  # gera o PDF
```

---

## Onde a aula se liga à Aula 6

| Aula 6 | Aula 7 |
|---|---|
| Mapeou o workflow em Mermaid | O workflow já existe: hoje é entrada do diagnóstico |
| Ensnou AS-IS e TO-BE | O TO-BE é desenhado a partir do gargalo medido, e não de opinião |
| Introduziu o painel de processo | Monta 5 painéis novos, com passo a passo de 96 pontos cada |
| Terminou no canvas do mini app | Constrói o app de verdade, no Antigravity, com código no GitHub |
