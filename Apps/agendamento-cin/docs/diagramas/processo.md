# Fluxogramas do processo · agendamento-cin

Gerados a partir de `projeto.json`. As setas seguem a ordem da tabela.

## AS-IS

```mermaid
%% Fluxograma ASIS · 6 etapas
flowchart TD
  IN(["Início"])
  N1["1. Consulta de vagas"]:::wait
  N2["2. Solicitação de agendamento"]:::wait
  N3["3. Verificação da vaga"]:::wait
  N4["4. Confirmação"]:::wait
  N5["5. Comparecimento"]:::wait
  N6["6. Registro do atendimento"]:::wait
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
%% Fluxograma TOBE · 7 etapas
flowchart TD
  IN(["Início"])
  N1["1. configurar agenda<br/><small>A pessoa assistida pela máqui…</small>"]:::auto
  N2["2. consultar horario<br/><small>A máquina (automação)</small>"]:::auto
  N3["3. agendar atendimento<br/><small>A pessoa assistida pela máqui…</small>"]:::auto
  N4["4. gerar indicadores<br/><small>A pessoa assistida pela máqui…</small>"]:::auto
  N5["5. Confirmar por e-mail<br/><small>A máquina (automação)</small>"]:::auto
  N6["6. Cancelar ou remarcar<br/><small>A pessoa assistida pela máqui…</small>"]:::auto
  N7["7. Registrar comparecimento<br/><small>A pessoa assistida pela máqui…</small>"]:::auto
  FIM(["Fim"])
  IN --> N1
  N1 --> N2
  N2 --> N3
  N3 --> N4
  N4 --> N5
  N5 --> N6
  N6 --> N7
  N7 --> FIM
  classDef manual fill:#fff4e5,stroke:#a35f00,color:#3b2a00;
  classDef wait fill:#fff4e5,stroke:#a35f00,stroke-dasharray:5 3,color:#3b2a00;
  classDef auto fill:#eef8f2,stroke:#127a45,color:#0b3b23;
  classDef humano fill:#eef3fa,stroke:#12487f,color:#0a2f5c;
```
