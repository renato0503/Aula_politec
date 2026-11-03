# Contexto do app · NIHDE

## Arquitetura

Um `index.html` único, offline, com CSS e JS embutidos, IndexedDB e backup
`.json`. O app é autônomo: `nucleo/`, `construir.py`, `src/` e `testes/` são só
dele. O `index.html` é gerado; edite as fontes.

## Dados

- `corpos`: uma linha por corpo. Chave `id` (`C-0001`), protocolo do Atena único.
- `log`: auditoria por corpo (`corpo_id`, ação, detalhe, perfil, data e hora).

## Fluxo do MVP

1. **Entrada** (`#/corpo/novo`): protocolo, unidade, município, local e
   características físicas.
2. **Exames** (`#/corpo/:id`): quatro vias com status, protocolo e data.
3. **Identificação**: via e data; muda a situação. Se o corpo já foi sepultado,
   vira "identificado após sepultamento".
4. **Família**: busca iniciada, família localizada, entrega ou não reclamado.
5. **Sepultamento**: depois de 30 dias, com data, local e certidão.
6. **Relatório**: por unidade, por via e CSV.

## Regras

Ver `PROJETO.md` (RN01 a RN08). As principais: protocolo único, entrega só com
identificação e família, sepultamento só depois de 30 dias, e toda ação na
auditoria.

## LGPD

No MVP, todos os dados são fictícios. A lista mostra iniciais; o nome completo,
o contato da família e o local do sepultamento ficam na ficha. A versão
institucional precisa de autenticação, acesso por papel e retenção definida pela
POLITEC.

## Como construir e testar

```powershell
cd "Apps/gestao_identificados"
python exemplos/gerar_exemplos.py
python construir.py
python testes/testar.py
python testes/cenarios.py
```

## Origem

Envio da Kesia Melo em 03/11/2026 e cinco áudios de 03/11/2026. A transcrição
literal está em `TRANSCRICAO.md`, a versão revisada em `TRANSCRICAO-GEMINI.md` e
a consolidação em `CONTEXTO-AUDIOS.md`.
