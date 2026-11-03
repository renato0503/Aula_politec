# Fluxogramas do processo · metas-bi-ocr

Gerados a partir de `projeto.json`. As setas seguem a ordem da tabela.

## AS-IS

```mermaid
%% Fluxograma ASIS · 5 etapas
flowchart TD
  IN(["Início"])
  N1["1. Receber a demanda do mês"]:::manual
  N2["2. Consultar o Power BI 1"]:::wait
  N3["3. Digitar na planilha"]:::manual
  N4["4. Conferir"]:::wait
  N5["5. Atualizar o painel e reunir"]:::wait
  FIM(["Fim"])
  IN --> N1
  N1 --> N2
  N2 --> N3
  N3 --> N4
  N4 --> N5
  N5 --> FIM
  classDef manual fill:#fff4e5,stroke:#a35f00,color:#3b2a00;
  classDef wait fill:#fff4e5,stroke:#a35f00,stroke-dasharray:5 3,color:#3b2a00;
  classDef auto fill:#eef8f2,stroke:#127a45,color:#0b3b23;
  classDef humano fill:#eef3fa,stroke:#12487f,color:#0a2f5c;
```

## TO-BE

```mermaid
%% Fluxograma TOBE · 4 etapas
flowchart TD
  IN(["Início"])
  N1["1. Exportar o relatório<br/><small>A pessoa, sem mudança</small>"]:::humano
  N2["2. Ler e extrair<br/><small>A máquina (automação)</small>"]:::auto
  N3["3. Conferir<br/><small>A pessoa assistida pela máqui…</small>"]:::auto
  N4["4. Gerar a planilha<br/><small>A máquina (automação)</small>"]:::auto
  FIM(["Fim"])
  IN --> N1
  N1 --> N2
  N2 --> N3
  N3 --> N4
  N4 --> FIM
  classDef manual fill:#fff4e5,stroke:#a35f00,color:#3b2a00;
  classDef wait fill:#fff4e5,stroke:#a35f00,stroke-dasharray:5 3,color:#3b2a00;
  classDef auto fill:#eef8f2,stroke:#127a45,color:#0b3b23;
  classDef humano fill:#eef3fa,stroke:#12487f,color:#0a2f5c;
```
