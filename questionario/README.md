# Questionario de Nivelamento

Pagina HTML com as 50 perguntas da prova de nivelamento do curso de Analise de Dados, BI e IA da POLITEC/MT. As respostas sao salvas em uma planilha Google Sheets via Google Apps Script.

## Estrutura

```
questionario/
├── index.html        <- Pagina do questionario (publicada no GitHub Pages)
├── apps-script.gs   <- Codigo do Google Apps Script
└── README.md        <- Este arquivo
```

---

## Setup passo a passo

### Parte 1 — Criar a planilha Google Sheets

1. Abra o Google Drive >Novo >Google Sheets
2. Dê um nome: `Prova Nivelamento POLITEC`
3. Copie o **ID da planilha** da URL:
   `https://docs.google.com/spreadsheets/d/`**`A1B2C3...`**`/edit`
4. Anote esse ID — usaremos no Apps Script

### Parte 2 — Configurar o Google Apps Script

1. Na planilha criada, vá em **Extensões > Apps Script**
2. Apague qualquer código padrão e cole o conteúdo de `apps-script.gs`
3. Substitua `SEU_PLANILHA_ID_AQUI` pelo ID da sua planilha (etapa 3 acima)
4. Salve (Ctrl+S), dê um nome ao projeto: `Prova Nivelamento`
5. Para testar, clique em **Selecionar função** > `testar` > Executar (▶)
   - Na primeira vez, será pedido autorização — autorize
   - Verifique se uma linha de teste apareceu na aba `Respostas`

### Parte 3 — Publicar o Apps Script como Web App

1. No Apps Script, clique em **Implantar > Nova implantação**
2. Em "Tipo", selecione **App da Web**
3. Configure:
   - Descrição: `Prova Nivelamento POLITEC`
   - Quem pode acessar: **Qualquer pessoa**
4. Clique em **Implantar**
5. Copie a **URL do Web App** (algo como `https://script.google.com/macros/s/AKfycb.../exec`)

### Parte 4 — Atualizar o HTML

1. Abra `questionario/index.html`
2. Encontre a linha:
   ```js
   var GScriptUrl = 'https://script.google.com/macros/s/.../exec';
   ```
3. Substitua pela URL do Web App que você copiou na parte 3

### Parte 5 — Publicar no GitHub Pages

1. Commit e push da pasta `questionario/`
2. Acesse: `https://renato0503.github.io/Aula_politec/questionario/`
   (ou o endereço do seu GitHub Pages)

---

## Colunas geradas na planilha

| Coluna | Conteúdo |
|---|---|
| A | Data/Hora da submissão |
| B | Nome do servidor |
| C | E-mail institucional |
| D | Pontuação (0 a 50) |
| E a BA | Resposta de cada questão (P1 a P50) |
| BB | Nível calculado |

## Níveis de pontuação

| Pontos | Nível |
|---|---|
| 0-12 | INICIANTE |
| 13-18 | BASICO |
| 19-24 | INTERMEDIARIO |
| 25-38 | AVANCADO |
| 39-50 | EXPERT |
