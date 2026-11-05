# Bibliotecas embutidas

Baixadas em 29/10/2026. O `Apps/_base/embutir.py` copia cada arquivo para dentro do `index.html`.

| Arquivo | Biblioteca | Versão | Licença | Origem | SHA-256 |
|---|---|---|---|---|---|
| `pdf.min.js` | pdf.js (pdfjs-dist) | 3.11.174 | Apache-2.0 | https://cdn.jsdelivr.net/npm/pdfjs-dist@3.11.174/build/pdf.min.js | `5b5799e6f8c68066…` |
| `pdf.worker.min.js` | pdf.js worker | 3.11.174 | Apache-2.0 | https://cdn.jsdelivr.net/npm/pdfjs-dist@3.11.174/build/pdf.worker.min.js | `feabdf309770ed24…` |
| `pizzip.min.js` | PizZip | 3.1.7 | MIT ou GPLv3 | https://cdn.jsdelivr.net/npm/pizzip@3.1.7/dist/pizzip.min.js | `f1c851bff85c23f2…` |
| `docxtemplater.js` | docxtemplater | 3.47.4 | MIT | https://cdn.jsdelivr.net/npm/docxtemplater@3.47.4/build/docxtemplater.js | `6c227dbbfb979bc9…` |
| `tesseract.min.js` | Tesseract.js | 5.1.1 | Apache-2.0 | https://cdn.jsdelivr.net/npm/tesseract.js@5.1.1/dist/tesseract.min.js | `a8e29918d098b2b0…` |
| `tesseract-worker.min.js` | Tesseract.js worker (`dist/worker.min.js`) | 5.1.1 | Apache-2.0 | https://cdn.jsdelivr.net/npm/tesseract.js@5.1.1/dist/worker.min.js | `aca1229639fc9907…` |
| `tesseract-core-simd-lstm.wasm.js` | tesseract.js-core (WebAssembly embutido) | 5.1.1 | Apache-2.0 | https://cdn.jsdelivr.net/npm/tesseract.js-core@5.1.1/tesseract-core-simd-lstm.wasm.js | `ce20eda9533cbed1…` |
| `por.traineddata.gz` | idioma português (4.0.0_best_int) | 1.0.0 | Apache-2.0 | https://cdn.jsdelivr.net/npm/@tesseract.js-data/por@1.0.0/4.0.0_best_int/por.traineddata.gz | `dacebc1386ddaaf8…` |
O OCR foi copiado de `metas-bi-ocr/vendor` em 05/11/2026. Os três arquivos do Tesseract (worker, núcleo e idioma) entram no `index.html` como blocos que não executam na página (`"blobs"` no `app.json`, marcador `<!-- BLOB: -->` no `construir.py`). O OCR monta um Worker em `blob:` com o núcleo, o worker e um `fetch` local que entrega o idioma: zero requisição de rede. A CSP ganhou `'wasm-unsafe-eval'` para compilar o WebAssembly.
