# Fluxogramas do processo · cin-segunda-via

Gerados a partir de `projeto.json`. As setas seguem a ordem da tabela.

## AS-IS

```mermaid
%% Fluxograma ASIS · 5 etapas
flowchart TD
  IN(["Início"])
  N1["1. Solicitação"]:::wait
  N2["2. Análise e Confronto"]:::wait
  N3["3. Impressão"]:::wait
  N4["4. Envio ao posto"]:::wait
  N5["5. Entrega ao Requerente"]:::wait
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
%% Fluxograma TOBE · 5 etapas
flowchart TD
  IN(["Início"])
  N1["1. Solicitação<br/><small>A máquina (automação)</small>"]:::auto
  N2["2. Confronto papiloscópico<br/><small>A pessoa, sem mudança</small>"]:::humano
  N3["3. Impressão<br/><small>A máquina (automação)</small>"]:::auto
  N4["4. Envio ao posto<br/><small>A pessoa assistida pela máqui…</small>"]:::auto
  N5["5. Entrega ao requerente<br/><small>A pessoa, sem mudança</small>"]:::humano
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
