# Fluxogramas do processo · gestao-documentos

Gerados a partir de `projeto.json`. As setas seguem a ordem da tabela.

## AS-IS

```mermaid
%% Fluxograma ASIS · 5 etapas
flowchart TD
  IN(["Início"])
  N1["1. Cadastro"]:::wait
  N2["2. Atribuição"]:::wait
  N3["3. Tramitação e Instrução"]:::wait
  N4["4. Acompanhamento e Prazos"]:::wait
  N5["5. Conclusão"]:::wait
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
%% Fluxograma TOBE · 0 etapas
flowchart TD
  IN(["Início"])
  FIM(["Fim"])
  IN --> FIM
  classDef manual fill:#fff4e5,stroke:#a35f00,color:#3b2a00;
  classDef wait fill:#fff4e5,stroke:#a35f00,stroke-dasharray:5 3,color:#3b2a00;
  classDef auto fill:#eef8f2,stroke:#127a45,color:#0b3b23;
  classDef humano fill:#eef3fa,stroke:#12487f,color:#0a2f5c;
```
