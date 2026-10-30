# Roteiro de aceite da Comissão de Ética (fictício)

> **Premissa assumida em 30/10/2026.** O piloto não foi executado. Base legal:
> LC nº 112/2002-MT (Código de Ética Funcional do Servidor Público Civil do
> Estado), texto em [codigo-etica-lc112-2002.md](codigo-etica-lc112-2002.md).

## Roteiro do aceite

1. Abrir `#/config` e carregar os dados fictícios.
2. Abrir `#/denuncia/nova` e registrar uma denúncia: protocolo, partes, relato
   com 50 caracteres e anexo.
3. Em `#/caso/<protocolo>/classificacao`, conferir as sugestões, abrir o
   **texto do artigo** de cada uma e confirmar a categoria com justificativa
   (RN02).
4. Em `#/caso/<protocolo>/admissibilidade`, decidir por uma das três vias, com
   fundamento e membros presentes. Testar a **prova pendente** (prazo de 5 dias,
   art. 8º, § 1º) e conferir que as oitivas ficam bloqueadas.
5. Em `#/caso/<protocolo>/oitivas`, usar o roteiro sugerido, registrar o termo e
   ver o prazo de nova manifestação (3 dias, art. 8º, § 4º).
6. Em `#/caso/<protocolo>/documentos`, gerar as três minutas e conferir que
   **nenhuma leva o nome das partes** (art. 11).
7. Em `#/caso/<protocolo>/encerramento`, conferir as etapas, aplicar a cominação
   (advertência ou censura ética, art. 9º), marcar o encaminhamento ao PAD
   (art. 10) e encerrar.
8. Em `#/relatorio`, conferir as contagens por etapa e categoria, sem nomes.

**Critério de aceite**: o app nunca mostra o nome das partes no relatório nem
na ementa; a cominação fica registrada com os 5 anos de transcrição na ficha
funcional; o fluxo não pula a admissibilidade.

## Piloto

| Medida | Linha de base | Meta |
|---|---|---|
| Triagem | 3 dias úteis (premissa) | 3 dias úteis |
| Oitiva | 10 dias úteis (premissa) | 10 dias úteis |
| Casos com ementa publicada sem nomes | não medido | 100% |

## Como confirmar

1. Rodar o roteiro com a Comissão e com a assessoria jurídica.
2. Conferir se as 8 categorias cobrem a prática da Comissão (editáveis em `#/config`).
3. Assinar o aceite e atualizar `PROJETO.md` e `README.md`.
