# Fluxogramas do processo · trilha-custodia-necropsia

Gerados a partir de `projeto.json`. As setas seguem a ordem da tabela.

## AS-IS

```mermaid
%% Fluxograma ASIS · 8 etapas
flowchart TD
  IN(["Início"])
  N1["1. 1. Acionamento"]:::wait
  N2["2. 2. Deslocamento"]:::wait
  N3["3. 3. Local"]:::wait
  N4["4. 4. Chegada ao IML"]:::wait
  N5["5. 5. Necropsia"]:::wait
  N6["6. 6. Identificação"]:::wait
  N7["7. 7. Guarda"]:::wait
  N8["8. 8. Liberação"]:::wait
  FIM(["Fim"])
  IN --> N1
  N1 --> N2
  N2 --> N3
  N3 --> N4
  N4 --> N5
  N5 --> N6
  N6 --> N7
  N7 --> N8
  N8 --> FIM
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
  N1["1. Acionamento e marcos<br/><small>A pessoa assistida pela máqui…</small>"]:::auto
  N2["2. Registro único<br/><small>A máquina (automação)</small>"]:::auto
  N3["3. Lacres<br/><small>A pessoa assistida pela máqui…</small>"]:::auto
  N4["4. Identificação e busca<br/><small>A máquina (automação)</small>"]:::auto
  N5["5. Painel<br/><small>A máquina (automação)</small>"]:::auto
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
