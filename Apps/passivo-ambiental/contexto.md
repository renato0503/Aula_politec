# Passivo Ambiental · contexto e arquitetura

> Equipe: Fábio (Diretoria de Interiorização)
> Fonte: `PROJETO.md` e a arquitetura do curso: **HTML monolítico, offline first**.

---

## 1. O problema

Há cerca de 300 requisições periciais ambientais atrasadas desde 2020 e um perito
disponível. O laudo feito só por sensoriamento remoto leva em média 16 horas,
sendo 12 na confecção dos mapas e 4 na redação.

| Dado informado | Valor |
|---|---|
| Requisições atrasadas | ~300 (desde 2020) |
| Peritos disponíveis | 1 |
| Tempo médio do laudo | 16 h (12 de mapa + 4 de texto) |
| Meta da defesa | 12 h por laudo |
| Prazo da requisição | 10 dias |

## 2. O que o MVP faz e o que não faz

| Faz | Não faz |
|---|---|
| Registra a requisição e controla o prazo | Integra com o Atena |
| Abre o laudo com o cabeçalho preenchido (RN01) | Decide a conclusão técnica |
| Guarda o rascunho e as horas trabalhadas | Assina o laudo |
| Mostra o passivo e os prazos no painel | Edita mapas ou gera PDF (Sprint 3) |
| Lista os mapas do laudo | Armazena dados reais ou sigilosos |

## 3. Regras

- **RN01**: o cabeçalho (processo, órgão, data, tipo, local, coordenadas) vem da
  requisição e pode ser ajustado antes de salvar.
- **RN02**: todo mapa temático precisa de norte, escala e área delimitada (Sprint 3).
- **RN03**: a exportação em PDF só é liberada com cabeçalho completo e pelo menos
  um mapa anexado.

## 4. Telas

| Rota | Perfil | O que faz |
|---|---|---|
| `#/painel` | todos | Abertas, fora do prazo, concluídas e horas registradas |
| `#/requisicoes` | todos | Lista com prazo restante e situação |
| `#/requisicao/nova` | perito | Registro da requisição, que abre o laudo |
| `#/laudo/:id` | perito | Cabeçalho, rascunho, horas e mapas |
| `#/config` | todos | Perfil da cópia, backup e dados fictícios |

## 5. Modelo de dados (IndexedDB `passivo_ambiental_v1`)

| Store | Campos |
|---|---|
| `requisicoes` | id_requisicao, numero_processo, orgao, data_requisicao, tipo_infracao, prazo_dias, local, coordenadas, status |
| `laudos` | id_laudo, requisicao_id, status, local, coordenadas, tipo_infracao, horas_trabalhadas, criado_em, concluido_em |
| `mapas` | id_mapa, laudo_id, modelo, criado_em |

## 6. LGPD

O protótipo usa apenas dados fictícios. A versão institucional deve observar o
sigilo pericial e a LGPD; o laudo e as imagens de satélite podem conter
informação sensível, e o acesso precisa ser restrito ao perito e à chefia.
