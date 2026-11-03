# Fluxogramas do processo · teia-triagem-emails

Gerados a partir de `projeto.json`. As setas seguem a ordem da tabela.

## AS-IS

```mermaid
%% Fluxograma ASIS · 7 etapas
flowchart TD
  IN(["Início"])
  N1["1. Chegada do e-mail de requisição"]:::wait
  N2["2. Triagem inicial e abertura do e-mail"]:::wait
  N3["3. Download e leitura dos anexos"]:::wait
  N4["4. Mapeamento dos 8 campos essenciais"]:::wait
  N5["5. Digitação e consolidação na planilha"]:::wait
  N6["6. Download, renomeação e organização dos PDFs"]:::wait
  N7["7. Validação, aceite e encaminhamento legal"]:::wait
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

## TO-BE

```mermaid
%% Fluxograma TOBE · 7 etapas
flowchart TD
  IN(["Início"])
  N1["1. Monitoramento e varredura da caixa de e-mails<br/><small>A máquina (automação)</small>"]:::auto
  N2["2. Extração de texto e leitura dos anexos (PDF/Imagens)<br/><small>A máquina (automação)</small>"]:::auto
  N3["3. Mapeamento dos 8 campos essenciais<br/><small>A máquina (automação)</small>"]:::auto
  N4["4. Preenchimento da planilha e sinalização de alertas<br/><small>A máquina (automação)</small>"]:::auto
  N5["5. Salvamento, renomeação e organização dos arquivos<br/><small>A máquina (automação)</small>"]:::auto
  N6["6. Validação de fé pública e decisão de aceite<br/><small>A pessoa, sem mudança</small>"]:::humano
  N7["7. Autuação e encaminhamento para a Regional<br/><small>A pessoa, sem mudança</small>"]:::humano
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
