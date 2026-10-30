# Roteiro de aceite e piloto do TAP (fictício)

> **Premissa assumida em 30/10/2026.** O piloto de 60 a 90 dias não foi
> executado. Ver [PREMISSAS.md](../../PREMISSAS.md).

## Roteiro do aceite

1. Abrir `#/config` e carregar os dados fictícios.
2. Abrir `#/tap/novo`, preencher um TAP com 2 campos vazios e tentar avançar:
   **tem que bloquear** (RN01, RN02).
3. Completar o TAP, gerar o pacote em `#/minhas` e importar o `.json` em
   `#/triagem`: **o pacote tem que ser aceito** (a verificação do arquivo confere).
4. Registrar uma pendência e devolver: o arquivo de devolução é baixado; importar
   em `#/minhas` e conferir que a proposta volta como "devolvida" (RN05, RN06).
5. Importar de novo o pacote corrigido, aceitar para análise e registrar o
   parecer da equipe.
6. Entrar como autoridade, abrir `#/proposta/<id>` e registrar a decisão de
   aprovação (RN07).
7. Abrir `#/portfolio`: a proposta aprovada aparece; definir prioridade **sem**
   justificativa (tem que recusar, RN08) e depois **com** justificativa.
8. Exportar o portfólio em `.xlsx` e abrir no Excel.
9. Abrir `#/indicadores` e conferir as contagens.

**Critério de aceite**: nenhuma etapa gera erro no console; o pacote alterado é
recusado; a prioridade sem justificativa é recusada; o `.xlsx` abre no Excel.

## Piloto (60 a 90 dias)

| Medida | Linha de base | Meta |
|---|---|---|
| Propostas registradas | 4 semanas de registro manual | todas pelo app |
| Tempo de triagem | não medido | 5 dias úteis |
| Devoluções por documento faltante | alto (checklist manual) | zero sem justificativa |
| Propostas com prioridade justificada | — | 100% das aprovadas |

## Como confirmar

1. Rodar o roteiro com a equipe de projetos e a autoridade.
2. Assinar o aceite e atualizar `PROJETO.md` e `README.md`.
3. Medir 4 semanas com o app e comparar com a linha de base.
