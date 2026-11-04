# Roteiro de aceite · TEIA

1. Abrir `index.html` e conferir que a bancada mostra 10 e-mails fictícios.
2. Selecionar um e-mail urgente e conferir os 9 campos.
3. Selecionar um e-mail com campo faltando: o botão de validação fica desabilitado.
4. Preencher o campo, salvar e validar. Conferir a trilha de auditoria.
5. Selecionar o e-mail com divergência: o alerta aparece; tratar o alerta e validar.
6. Selecionar o PDF imagem: o alerta de OCR aparece; preencher o campo, tratar e validar.
7. Em `#/lote`, extrair o lote e conferir a gravação em `extracao`.
8. Em `#/planilha`, conferir as 10 linhas e exportar o CSV com BOM e `;`.
9. Trocar para o perfil Chefia e conferir a configuração.
10. No celular (390 px), conferir a fila em cartões, a ficha e a ausência de rolagem horizontal.
11. Rodar `python testes/testar.py`, `python testes/cenarios.py` e `python testes/jornada.py`.
