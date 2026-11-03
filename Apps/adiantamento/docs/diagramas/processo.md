# Fluxogramas do processo · adiantamento

Gerados a partir de `projeto.json`. As setas seguem a ordem da tabela.

## AS-IS

```mermaid
%% Fluxograma ASIS · 12 etapas
flowchart TD
  IN(["Início"])
  N1["1. Levantar orçamentos"]:::wait
  N2["2. Encaminhar à DAS"]:::wait
  N3["3. Cadastrar no SICAD"]:::manual
  N4["4. Aprovar (chefia imediata)"]:::wait
  N5["5. Conferir documentos (SESP)"]:::wait
  N6["6. Confirmar dotação (NGER)"]:::wait
  N7["7. Autorizar"]:::wait
  N8["8. Pagar"]:::wait
  N9["9. Aplicar o recurso"]:::wait
  N10["10. Prestar contas"]:::wait
  N11["11. Analisar a prestação"]:::wait
  N12["12. Aprovar e encerrar"]:::wait
  FIM(["Fim"])
  IN --> N1
  N1 --> N2
  N2 --> N3
  N3 --> N4
  N4 --> N5
  N5 --> N6
  N6 --> N7
  N7 --> N8
  N8 --> N9
  N9 --> N10
  N10 --> N11
  N11 --> N12
  N12 --> FIM
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
  N1["1. Registrar o pedido na DAS<br/><small>A pessoa assistida pela máqui…</small>"]:::auto
  N2["2. Acompanhar as etapas<br/><small>A pessoa assistida pela máqui…</small>"]:::auto
  N3["3. Alertar prazos<br/><small>A máquina (automação)</small>"]:::auto
  N4["4. Registrar pendências<br/><small>A pessoa assistida pela máqui…</small>"]:::auto
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
