
flowchart LR
    A["Etapa 1Acionamento"] --> B["Etapa 2Ocorrência e possível vítima"]
    B --> C["Etapa 3Aguardando necropsia"]
    C --> D["Etapa 4Necropsia em andamento"]
    D --> E["Etapa 5Identificação"]
    E --> E1{"Resultado daidentificação"}
    E1 -- Identificado --> F["Etapa 6Família e liberação"]
    E1 -- Não identificado --> E2["Busca de familiares"]
    E1 -- Decisão ADM --> E3["Encaminhar parasepultamento pelo Estado"]
    E2 --> E4{"Busca comêxito?"}
    E4 -- Sim --> F
    E4 -- Não --> E5["Autorização desepultamento"]
    E5 --> SEP["Sepultado pelo Estado"]
    E3 --> SEP
    F --> F1{"Tipo deliberação"}
    F1 -- A familiar --> F2["Assinatura do familiar"]
    F1 -- Sem familiar --> F3["Busca sem êxito"]
    F3 --> SEP
    F2 --> G["Etapa 7Entrega de laudo para ADM"]
    SEP --> G
    G --> G1["Quem entregaQuem recebeAssinatura"]
    G1 --> H["Custódia finalizadaCaso concluído"]
    SEP -. Corpo liberado .-> FUN["Funerária"]
    FUN -. Desfecho mantido .-> SEP

    style A fill:#1e3a5f,color:#fff
    style B fill:#1e3a5f,color:#fff
    style C fill:#1e3a5f,color:#fff
    style D fill:#1e3a5f,color:#fff
    style E fill:#1e3a5f,color:#fff
    style F fill:#1e3a5f,color:#fff
    style SEP fill:#d97706,color:#fff
    style G fill:#1e3a5f,color:#fff
    style H fill:#16a34a,color:#fff
    style FUN fill:#6b7280,color:#fff
