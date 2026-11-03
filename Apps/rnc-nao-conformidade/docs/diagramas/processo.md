# Fluxogramas do processo · rnc-nao-conformidade

Gerados a partir de `projeto.json`. As setas seguem a ordem da tabela.

## AS-IS

```mermaid
%% Fluxograma ASIS · 6 etapas
flowchart TD
  IN(["Início"])
  N1["1. Identificação da não conformidade"]:::wait
  N2["2. Encaminhamento de validação"]:::wait
  N3["3. Encaminha para o setor notificado"]:::wait
  N4["4. Elaboração e execução"]:::wait
  N5["5. Avaliação"]:::wait
  N6["6. Finalização/encaminhamento"]:::wait
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
%% Fluxograma TOBE · 5 etapas
flowchart TD
  IN(["Início"])
  N1["1. Registrar a RNC<br/><small>A pessoa, sem mudança</small>"]:::humano
  N2["2. Validar a entrada<br/><small>A pessoa assistida pela máqui…</small>"]:::auto
  N3["3. Responder com o plano<br/><small>A pessoa assistida pela máqui…</small>"]:::auto
  N4["4. Avaliar o resultado<br/><small>A pessoa assistida pela máqui…</small>"]:::auto
  N5["5. Indicadores<br/><small>A máquina (automação)</small>"]:::auto
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
