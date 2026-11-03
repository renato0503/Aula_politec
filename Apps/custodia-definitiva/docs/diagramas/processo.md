# Fluxogramas do processo · custodia-definitiva

Gerados a partir de `projeto.json`. As setas seguem a ordem da tabela.

## AS-IS

```mermaid
%% Fluxograma ASIS · 12 etapas
flowchart TD
  IN(["Início"])
  N1["1. Coleta do vestígio"]:::wait
  N2["2. Requisição pericial"]:::wait
  N3["3. Recebimento"]:::wait
  N4["4. Registro e distribuição"]:::wait
  N5["5. Processamento pericial"]:::wait
  N6["6. Emissão do laudo"]:::wait
  N7["7. Separação pós-exame"]:::wait
  N8["8. Preparação da devolução"]:::wait
  N9["9. Devolução à autoridade"]:::wait
  N10["10. Preparação da contraprova"]:::wait
  N11["11. Recebimento na custódia"]:::wait
  N12["12. Armazenamento"]:::wait
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
%% Fluxograma TOBE · 12 etapas
flowchart TD
  IN(["Início"])
  N1["1. Coleta e requisição pericial<br/><small>A pessoa, sem mudança</small>"]:::humano
  N2["2. Recebimento e processamento pericial<br/><small>A pessoa, sem mudança</small>"]:::humano
  N3["3. Preparação pós-processamento<br/><small>A pessoa assistida pela máqui…</small>"]:::auto
  N4["4. Cadastro e classificação dos materiais<br/><small>A pessoa assistida pela máqui…</small>"]:::auto
  N5["5. Encaminhamento à Central<br/><small>A pessoa assistida pela máqui…</small>"]:::auto
  N6["6. Recebimento na Central<br/><small>A pessoa assistida pela máqui…</small>"]:::auto
  N7["7. Endereçamento inteligente<br/><small>A máquina (automação)</small>"]:::auto
  N8["8. Armazenamento físico<br/><small>A pessoa assistida pela máqui…</small>"]:::auto
  N9["9. Monitoramento de ocupação<br/><small>A máquina (automação)</small>"]:::auto
  N10["10. Localização e consulta<br/><small>A máquina (automação)</small>"]:::auto
  N11["11. Controle de elegibilidade para descarte<br/><small>A pessoa assistida pela máqui…</small>"]:::auto
  N12["12. Autorização e execução do descarte<br/><small>A pessoa assistida pela máqui…</small>"]:::auto
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
