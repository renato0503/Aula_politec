# Formatos dos arquivos do caso (SUPOSTOS)

Os formatos abaixo foram **inventados** para os testes. No Sprint 0, o grupo traz amostras anonimizadas dos arquivos reais, e as regras de leitura do app são ajustadas a elas.

| Arquivo | Formato suposto | O app procura |
|---|---|---|
| `DEVICE INFO.txt` | linhas `Rótulo: valor`, CRLF, UTF-8 | `Manufacturer`, `Model`, `Color`, `IMEI 1`, `IMEI 2` |
| `HASHDOHASH.txt` | linhas `Rótulo: valor` | `Arquivo`, `Algoritmo`, `Hash` (64 hexadecimais) |
| `OBJ 01-A/SIM.html` | tabela com linhas campo / valor | `Objeto`, `ICCID`, `Operadora` |
| `Requisicao.pdf` | PDF com texto, rótulos fixos | `Protocolo:`, `Ofício nº`, `Processo nº`, `Autoridade requisitante:`, `Data da solicitação:`, bloco `QUESITOS` |
| `Requisicao-digitalizada.pdf` | o mesmo conteúdo, só imagem (sem camada de texto) | exige OCR ou digitação (Sprint 10) |

Cada pasta traz um `GABARITO.json` com os valores certos, para os testes dos extratores.

| Caso | Situação |
|---|---|
| 001 | completo, 2 cartões SIM (01-A e 01-B) |
| 002 | sem cartão SIM e sem IMEI 2 (RN06) |
| 003 | sem `HASHDOHASH.txt` (RN02) |
