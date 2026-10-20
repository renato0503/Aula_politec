# Cenario 3 - Mapa da Criminalidade em MT

Dataset sintetico de **ocorrencias criminais** nos 18 municipios-polo da
POLITEC/MT, com tipo de crime, arma, faixa etaria da vitima e periodo do dia.
Foco do dashboard: **inteligencia geografica** (mapa), perfil da vitima,
sazonalidade, arma predominante, alerta de latrocinio. Anonimizado.

---

## Arquivos

| Tabela                | Grao (1 linha =)    | Linhas |
|-----------------------|---------------------|--------|
| `fato_ocorrencias`    | 1 ocorrencia/BO     | 1500   |
| `dim_municipio`       | 1 municipio (MT)    | 18     |
| `dim_tipo_crime`      | 1 tipo              | 7      |
| `dim_arma`            | 1 tipo de arma      | 6      |
| `dim_faixa_etaria`    | 1 faixa             | 6      |
| `dim_periodo_dia`     | 1 faixa de horario  | 4      |
| `dim_calendario`      | 1 dia               | 1096   |

---

## Sugestoes de visuais para a aba de Criminalidade

- **Mapa Preenchido (Shape Map / Bing)**: ocorrencias por municipio, com densidade.
- **Linha temporal**: serie diaria ou mensal com pico de sazonalidade.
- **Colunas empilhadas**: tipo de crime x arma (%).
- **Piramide etaria (barras divergentes)**: vitimas por faixa etaria e sexo.
- **Heatmap de calendario (matrix)**: dia da semana x hora do dia.
- **Cartoes KPI**: total de vitimas, latrocinios, % flagrante.
- **Slicer**: ano, municipio (com hierarquia microrregiao se quiser), tipo, arma.

---

## Numeros de referencia

| Indicador                          | Valor aprox. |
|------------------------------------|--------------|
| Total de ocorrencias               | 1.500        |
| Vitimas envolvidas (soma)          | ~1.700       |
| % Roubo (tipo mais frequente)      | ~24%         |
| % Arma de Fogo                     | ~38%         |
| % flagrante                        | ~18%         |
| Periodo dos fatos                  | 2023-01-01 a 2025-12-31 |
