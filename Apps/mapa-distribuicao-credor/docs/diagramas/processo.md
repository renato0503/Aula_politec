# Fluxogramas do processo · mapa-distribuicao-credor

Gerados a partir de `projeto.json`. As setas seguem a ordem da tabela.

## AS-IS

```mermaid
%% Fluxograma ASIS · 8 etapas
flowchart TD
  IN(["Início"])
  N1["1. Receber distribuição de itens por órgão"]:::wait
  N2["2. Compor mapa por grupo e item"]:::wait
  N3["3. Preencher valores homologados"]:::wait
  N4["4. Separar homologados, fracassados e desertos"]:::wait
  N5["5. Gerar resultado geral e por órgão"]:::wait
  N6["6. Montar tabela por empresa e órgão"]:::wait
  N7["7. Montar tabela de conferência"]:::wait
  N8["8. Montar distribuição orçamentária por credor e órgão"]:::wait
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
%% Fluxograma TOBE · 6 etapas
flowchart TD
  IN(["Início"])
  N1["1. Receber planilhas das unidades<br/><small>A pessoa assistida pela máqui…</small>"]:::auto
  N2["2. Importar relatório do pregoeiro<br/><small>A máquina (automação)</small>"]:::auto
  N3["3. Gerar mapa por grupo, órgão e empresa<br/><small>A máquina (automação)</small>"]:::auto
  N4["4. Separar homologados, fracassados e desertos<br/><small>A máquina (automação)</small>"]:::auto
  N5["5. Conferir divergências<br/><small>A máquina (automação)</small>"]:::auto
  N6["6. Validar dotação e distribuir<br/><small>A pessoa assistida pela máqui…</small>"]:::auto
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
