# Aula 5 - Datasets para o Projeto Integrador

Cinco datasets sinteticos da POLITEC/MT em **modelo estrela** (cada cenario =
1 pasta, 1 tabela fato + dimensoes proprias + dim_calendario compartilhada).
Todos os fatos tem **>= 1000 linhas** para permitir pratica realista de
agregacoes, slicers, drill e DAX. Cada cenario foi desenhado para virar **uma
aba tematica** do dashboard final do projeto integrador.

| # | Cenario | Pasta | Tema | Fato (linhas) |
|---|---------|-------|------|---------------|
| 1 | Backlog de Pericias      | `cenario1_backlog/`       | Operacional - filas e TAT     | 1.200 |
| 2 | TAT do Laboratorio de DNA | `cenario2_dna/`           | Laboratorio - qualidade/TAT   | 1.100 |
| 3 | Mapa da Criminalidade em MT | `cenario3_criminalidade/` | Inteligencia geografica      | 1.500 |
| 4 | Orcamento e Contratos    | `cenario4_orcamento/`     | Gestao financeira             | 1.300 + 240 |
| 5 | Cadeia de Custodia       | `cenario5_custodia/`      | Rastreabilidade de evidencias | 1.300 |

> Cada cenario traz `README.md` proprio com o esquema estrela, numeros de
> referencia e **sugestoes de visuais** (quais visuais funcionam bem para aquela
> aba tematica).

---

## O projeto integrador exige, no minimo

- **3 abas tematicas** (pegar 3 dos 5 cenarios; cada aba = 1 cenario);
- **1 slicer por aba** (periodo + 1 atributo do cenario);
- **1 KPI com formatacao condicional** (verde / amarelo / vermelho);
- **1 visual geografico OU temporal** para cada aba;
- **RLS (Row-Level Security)** recomendada em pelo menos uma aba;
- Publicacao em **workspace segregado** + link para a App.

Detalhes no caderno: `Parte 5 - Projeto Integrador`.

---

## Como carregar no Power BI

1. Abra o Power BI Desktop e crie um arquivo novo (`Projeto_Integrador.pbix`).
2. **Obter Dados -> Pasta** e selecione **a pasta inteira** da Aula 5/datasets/.
3. O Power BI importa cada CSVs como uma tabela individual. Conecte-as com a
   `dim_calendario` propria de cada cenario por relacionamentos 1:N.
4. Para limpar e "tipar", use o Power Query (o caderno da Aula 4 tem o
   passo a passo).
5. Crie a tabela de medidas (clicar com botao direito em qualquer medida ->
   nova medida) e aplique DAX.

---

## Convencoes

- CSV UTF-8 com BOM, separador `;`, datas ISO `AAAA-MM-DD`.
- `data_key` inteiro no formato `AAAAMMDD`.
- Chaves substitutas (surrogate keys) inteiras, atribuidas por ordem alfabetica.
- `dim_calendario` compartilhada em cada pasta, comecando em
  `2023-01-01` ate `2025-12-31` (1096 dias).
- Sem dependencia externa: todos os arquivos abrem com duplo clique.
