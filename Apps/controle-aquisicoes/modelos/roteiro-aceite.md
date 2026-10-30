# Roteiro de aceite e piloto do Controle de Aquisições (fictício)

> **Premissa assumida em 30/10/2026.** O piloto não foi executado. Base legal:
> Lei nº 14.133/2021, detalhada em [fluxo-e-prazos.md](fluxo-e-prazos.md).

## Roteiro do aceite (com a aquisição)

1. Abrir `#/config` e carregar os dados fictícios.
2. Em `#/processo/novo`, registrar uma aquisição com SIGADOC e SIAG únicos
   (RN01). Repetir o SIGADOC: tem que recusar.
3. Avançar do DFD sem o documento: tem que bloquear (RN02). Anexar e avançar.
4. Abrir uma pendência e tentar avançar: tem que bloquear (RN03). Resolver.
5. Em `#/processo/<id>`, registrar as **três análises** (técnica, orçamentária e
   jurídica) com setor, parecer e decisão. Conferir a trilha de aprovação.
6. Registrar a **modalidade** e o critério de julgamento.
7. Em `#/processo/<id>`, registrar a pesquisa de preços com 3 cotações (RN04) e
   conferir o alerta de inconsistência quando o cotado foge 30% do estimado.
8. Abrir `#/painel`: processos por etapa, tempo médio por etapa, processos
   parados, pendências por unidade e por responsável, prazo médio.
9. Exportar o CSV e imprimir em A4.

**Critério de aceite**: o processo não avança sem documento nem com pendência
aberta; a trilha de aprovação mostra perfil e data; o CSV abre no Excel.

## Piloto com processos simulados

| Medida | Linha de base | Meta |
|---|---|---|
| Ciclo do DFD à modalidade | 43 dias (9 etapas, premissa) | 30 dias |
| Processos parados na etapa | não medido | zero |
| Retrabalho (pendências) | não medido | reduzir 30% |
| Análises registradas fora do sistema | todas | zero |

## Como confirmar

1. Rodar o roteiro com a Coordenadoria de Aquisições.
2. Ajustar os prazos de cada etapa em `src/app.js` (`CA_PRAZO_ETAPA`).
3. Comparar o fluxo novo com o atual em 10 processos simulados.
