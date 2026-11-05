# Entrega da Silmara Bueno · 05/11/2026

Arquivos que a Silmara trouxe em `Ncropsia/`, guardados sem alteração:

| Arquivo | O que é |
|---|---|
| `Flowchart.md` | Fluxograma Mermaid com as possibilidades do caso (desfechos da identificação, da família e do sepultamento) |
| `prototipo-sistema-controle-necropsia.html` | Protótipo salvo do navegador (as duas cópias de `Ncropsia/` eram idênticas). Depende de `shell.css` e `shell.js`, que não vieram, e de imagens da internet |
| `PROJETO-2026-11-02.md` | `PROJETO.md` exportado do formulário (igual à cópia em `Aula 8/Entregas/Silmara/`) |

## Revisão do fluxograma

O fluxograma acerta as sete etapas, as três saídas da identificação, a busca de
familiares e o sepultamento pelo Estado como ponto de encontro. Na revisão:

1. As quebras de linha dos nós (`<br>`) se perderam na cópia ("Etapa 1Acionamento").
2. "Não identificado → busca de familiares" foi trocado pelo laço
   necropapiloscopia → DNA, odontologia legal ou antropologia → métodos esgotados.
3. O sepultamento sem familiar passava por caminhos diferentes, um com autorização
   e outro sem. Agora os dois passam pela decisão do Gestor ADM, com justificativa
   e autorização.
4. A funerária vale para os dois destinos (família e Estado), com o Auto de Entrega.
5. Os lacres entraram no fluxo: a ADM confirma o recebimento.
6. O laudo corre em paralelo a partir da necropsia, e o caso só se encerra com
   destino, laudo e lacres confirmados.
7. A exceção "familiar localizado após o sepultamento" virou retificação.

A versão revisada é o TO-BE do app: `docs/diagramas/to-be.manual.mmd`. O que mudou
no código está no Sprint 9 de `sprint.md` e no `README.md`.

## Pendências do `PROJETO.md` para a Silmara

- Seções vazias: 4 (dados), 5 (regras RN), 6 (telas) e os anexos C, D e E.
- Campos trocados: "Campos de data e tempo" traz quem libera o acesso; "Hospedagem"
  traz o período da linha de base; "Plataforma alvo: celular" contradiz o "fora do
  escopo" (sem app móvel).
- "Retenção: indetermidado": definir o prazo (LGPD).
