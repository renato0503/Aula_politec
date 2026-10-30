# Formulário, diretorias e linha de base (fictício)

> **Premissa assumida em 30/10/2026.** A leitura do `contexto.md` com a aluna, a
> saída do CPF do formulário, a caixa de e-mail, as diretorias que recebem vagas
> e as métricas ficaram com a premissa abaixo. Ver
> [PREMISSAS.md](../../PREMISSAS.md).

## 1. O CPF sai do formulário

**Decisão: o CPF não é coletado.** O formulário pede:

| Campo | Regra |
|---|---|
| Matrícula | só números, 4 ou mais dígitos (RN01) |
| Nome completo | com pelo menos 2 partes |
| Lotação | texto livre |
| Diretoria | da lista de 4 |
| E-mail | institucional, do domínio `@politec.mt.gov.br` (RN02) |

A matrícula identifica o servidor, e o e-mail institucional garante o
atendimento. Com CPF, a mesma pessoa teria 2 identificadores e a validação
ficaria ambígua.

## 2. A caixa de e-mail

`capacitacao@politec.mt.gov.br` existe e recebe o aviso de divulgação. O envio
do comprovante sai por `mailto:`, com o bloco do e-mail no corpo, para o app
não depender de servidor. O bloco é legível de volta pelo gerador (teste do
Sprint 3).

## 3. As 4 diretorias que recebem vagas

| Sigla | Diretoria |
|---|---|
| DML | Matriz |
| DIN | Interiorização |
| DIT | Tecnologia |
| DCC | Ciência Criminal |

## 4. As 4 métricas

| Métrica | Onde aparece |
|---|---|
| Vagas por diretoria | no curso e no comprovante |
| Prazo de inscrição | no curso e no link |
| Lista de espera | na triagem da inscrição |
| Taxa de aprovação | no painel |

## 5. A linha de base

| Medida | Valor assumido |
|---|---|
| Da divulgação à lista | 12 dias |
| Da lista à convocação | 5 dias |

## 6. Os itens [validar] do contexto

Cada `[validar]` do `contexto.md` foi lido e marcado como **aceito**, com a
decisão anotada no próprio `contexto.md`.

## Como confirmar

1. A leitura do `contexto.md` com a aluna.
2. A decisão da chefia sobre o CPF.
3. A confirmação da TI sobre a caixa de e-mail.
4. A lista real de diretorias que recebem vagas.
5. A medição da linha de base em 2 cursos recentes.
