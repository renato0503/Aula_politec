# Roteiro de aceite e posição da TI (fictício)

> **Premissa assumida em 30/10/2026.** O piloto não foi executado e a TI não
> respondeu formalmente. O roteiro abaixo é o que o app espera do aceite. Ver
> [PREMISSAS.md](../../PREMISSAS.md).

## 1. Roteiro com os 30 pedidos fictícios

Cada pedido do exemplo (`exemplos/seed.json`) tem um caso de teste:

| Grupo | Quantidade | O que confere |
|---|---|---|
| Elegíveis, aceitos | 4 | o servidor aceita e o resumo fecha |
| Recusados com motivo | 4 | o motivo aparece no protocolo do cidadão |
| Recebidos, aguardando | 22 | a fila mostra e o cidadão vê "recebido" |

**Passo a passo do aceite**:

1. Abrir `#/config` e carregar os dados fictícios.
2. Abrir `#/pedido` e fazer um pedido novo com as fotos de teste.
3. Anotar o protocolo e abrir `#/protocolo/<protocolo>`: a situação é "Recebido".
4. Entrar como servidor, abrir `#/fila`, selecionar o pedido e aceitar.
5. Voltar ao protocolo: a situação é "Aceito" e o resumo aparece.
6. Abrir o resumo e copiar o texto; conferir os 10 campos.
7. Apagar o pedido pelo botão de retenção (RN06) e conferir que a contagem subiu.
8. Entrar como gestão e abrir `#/indicadores`: os números batem com a base.
9. Repetir para um pedido recusado, conferindo o motivo no protocolo.

**Critério de aceite**: nenhuma etapa gera erro no console, o protocolo do
cidadão sempre mostra a situação atual e o resumo tem o mesmo conteúdo da ficha.

## 2. Acessibilidade

| Item | Como conferir | Situação |
|---|---|---|
| Tela pequena (celular) | abrir em 390 × 844 e navegar pelo pedido | testado no navegador do app |
| Câmera | `capture="user"` no rosto e `capture="environment"` no documento | implementado |
| Leitor de tela | todo campo tem `label for` e a fila usa botões com rótulo | implementado e no teste do Sprint 6 |
| Contraste | paleta institucional validada em `Apps/IDENTIDADE-VISUAL.md` | pendente de validação formal |

## 3. Posição da TI e do encarregado de dados

| Pergunta | Resposta assumida | O que confirmar |
|---|---|---|
| O app pode ficar publicado no GitHub Pages/Firebase? | sim, porque não guarda dado pessoal real | a TI confirmar |
| Há integração com a base de identificação civil? | **não**: o resumo é copiado e lançado à mão | se existe API no médio prazo |
| As fotos são guardadas? | no navegador do cidadão e do servidor, e apagadas na retenção (RN06) | o encarregado de dados confirmar o prazo |
| Quem é o controlador dos dados no piloto? | a POLITEC, com dados fictícios | o encarregado de dados registrar |

## 4. O que muda em produção

1. Trocar as fotos de teste por captura real, com consentimento (LGPD, art. 11).
2. Decidir se o resumo vai por API ou continua copiado.
3. Definir o prazo de retenção (hoje, apaga depois da decisão).
4. Publicar em domínio institucional.

## Como confirmar

1. Rodar o roteiro com a equipe do posto e assinar o aceite.
2. Registrar a posição da TI e do encarregado de dados por e-mail.
3. Atualizar `PROJETO.md` e `README.md` com o resultado.
