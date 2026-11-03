# Fluxogramas do processo · controle-aquisicoes

Gerados a partir de `projeto.json`. As setas seguem a ordem da tabela.

## AS-IS

```mermaid
%% Fluxograma ASIS · 6 etapas
flowchart TD
  IN(["Início"])
  N1["1. 1. Identificação da necessidade"]:::wait
  N2["2. 2. DFD"]:::wait
  N3["3. 3. ETP, riscos e TR"]:::wait
  N4["4. 4. Pesquisa de preços"]:::wait
  N5["5. 5. Formalização"]:::wait
  N6["6. 6. Análises e modalidade"]:::wait
  FIM(["Fim"])
  IN --> N1
  N1 --> N2
  N2 --> N3
  N3 --> N4
  N4 --> N5
  N5 --> N6
  N6 --> FIM
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
  N1["1. DFD a TR<br/><small>A pessoa assistida pela máqui…</small>"]:::auto
  N2["2. Pesquisa de preços<br/><small>A pessoa assistida pela máqui…</small>"]:::auto
  N3["3. Acompanhamento<br/><small>A máquina (automação)</small>"]:::auto
  N4["4. SIGADOC e SIAG<br/><small>A pessoa assistida pela máqui…</small>"]:::auto
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
