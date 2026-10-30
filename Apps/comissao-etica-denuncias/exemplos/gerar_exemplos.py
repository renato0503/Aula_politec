"""Gera as categorias iniciais e 10 casos fictícios da Comissão de Ética (Sprint 0).

As categorias estão ancoradas no **Código de Ética Funcional do Servidor Público
Civil do Estado de Mato Grosso** (Lei Complementar nº 112, de 1º/07/2002), cujo
texto foi consultado em 30/10/2026 no acervo do repositório `ctresb/leis`
(fonte oficial: ALMT). Cada categoria traz o artigo aplicável e o trecho do
artigo, para a Comissão conferir a redação.

Os 10 casos são fictícios e trazem a categoria esperada, usada no teste da
classificação assistida (Sprint 3).

Semente fixa = 20261029.
Uso: python "Apps/comissao-etica-denicias/exemplos/gerar_exemplos.py"
"""
import datetime as dt
import json
import pathlib
import random

AQUI = pathlib.Path(__file__).resolve().parent
random.seed(20261029)

FONTE = ("Lei Complementar nº 112, de 01/07/2002 (MT) — Código de Ética Funcional do "
         "Servidor Público Civil do Estado de Mato Grosso. Texto consultado em "
         "30/10/2026 no acervo https://github.com/ctresb/leis, fonte oficial "
         "https://www.al.mt.gov.br/norma-juridica/urn:lex:br;mato.grosso:estadual:lei.complementar:2002-07-01;112")

# (id, nome, artigos, texto do artigo, palavras)
CATEGORIAS = [
    ("assedio_moral", "Assédio moral ou humilhação", "Art. 2º, X; Art. 4º, V e VII",
     "Art. 2º, X: tratar mal uma pessoa que paga seus tributos direta ou indiretamente significa causar-lhe dano moral. "
     "Art. 4º, V: tratar cuidadosamente os usuários dos serviços públicos estaduais. "
     "Art. 4º, VII: ser cortês, ter urbanidade, disponibilidade e atenção, respeitando a capacidade e as limitações "
     "individuais de todos os usuários dos serviços públicos estaduais, sem qualquer espécie de preconceito ou distinção.",
     ["humilh", "assédio", "assedio", "constrang", "grit", "xing", "ameaç", "perseguiç"]),
    ("desrespeito_publico", "Tratamento desrespeitoso ao público", "Art. 4º, V e VII; Art. 5º, VI",
     "Art. 4º, V: tratar cuidadosamente os usuários dos serviços públicos estaduais, aperfeiçoando o processo de comunicação "
     "e contato com o público. "
     "Art. 4º, VII: ser cortês, ter urbanidade e respeito às limitações individuais de todos os usuários. "
     "Art. 5º, VI: permitir que perseguições, simpatias, antipatias, caprichos, paixões ou interesses de ordem pessoal "
     "interfiram no trato com o público.",
     ["cidadão", "atendimento", "grosseir", "mal atendid", "desrespeit", "público", "usuário"]),
    ("uso_cargo", "Uso do cargo em proveito próprio ou de terceiros", "Art. 5º, I; Art. 4º, IX",
     "Art. 5º, I: é vedado ao servidor público o uso do cargo, emprego ou função, bem como facilidades, amizades, tempo, "
     "posição e influências, para obter qualquer favorecimento, para si ou para outrem. "
     "Art. 4º, IX: resistir a todas as pressões de superiores hierárquicos, de contratantes, interessados e outros que visem "
     "obter favores, benesses ou vantagens indevidas.",
     ["favor", "vantagem", "proveito", "parente", "fura fila", "furou a fila", "influência", "propina"]),
    ("sigilo", "Quebra de sigilo funcional", "Art. 5º, XII; Art. 2º, VII",
     "Art. 5º, XII: é vedado ao servidor público fazer uso de informações privilegiadas obtidas no âmbito de seu serviço, "
     "em benefício próprio, de parentes, de amigos ou de terceiros. "
     "Art. 2º, VII: salvo os casos de investigações policiais ou interesse superior do Estado, a publicidade de qualquer "
     "ato administrativo constitui requisito de eficácia e moralidade.",
     ["sigilo", "vazou", "vazamento", "divulgou", "compartilhou", "foto do laudo", "informação sigilosa"]),
    ("redes_sociais", "Conduta inadequada em redes sociais e aplicativos", "Art. 2º, VI; Art. 4º, VI",
     "Art. 2º, VI: a função pública integra-se na vida particular de cada servidor público; os fatos e atos verificados na "
     "conduta do dia a dia em sua vida privada poderão acrescer ou diminuir o seu bom conceito na vida funcional. "
     "Art. 4º, VI: ter consciência de que o seu trabalho é regido por princípios éticos que se materializam na adequada "
     "prestação dos serviços públicos estaduais.",
     ["whatsapp", "instagram", "rede social", "grupo", "postou", "publicação", "print"]),
    ("assiduidade", "Descumprimento de escala, plantão ou horário", "Art. 4º, XI; Art. 2º, XIV",
     "Art. 4º, XI: ser assíduo e frequente ao serviço, na certeza de que a ausência provoca danos ao trabalho ordenado. "
     "Art. 2º, XIV: toda ausência injustificada do servidor público de seu local de trabalho é fator de desmoralização do "
     "serviço público estadual.",
     ["plantão", "escala", "faltou", "atraso", "ausente", "abandon", "horário"]),
    ("conflito_interesses", "Conflito de interesses", "Art. 4º, IX; Art. 5º, VII",
     "Art. 4º, IX: resistir a todas as pressões de contratantes, interessados e outros que visem obter favores ou vantagens "
     "indevidas, e denunciá-las. "
     "Art. 5º, VII: é vedado pleitear, solicitar, provocar, sugerir ou receber qualquer tipo de ajuda financeira, gratificação, "
     "prêmio, comissão, doação ou vantagem de qualquer espécie, para si, familiares ou qualquer pessoa.",
     ["empresa", "contrato", "fornecedor", "sócio", "interesse particular", "consultoria"]),
    ("uso_bens", "Uso indevido de bens e recursos públicos", "Art. 2º, XI; Art. 5º, XI",
     "Art. 2º, XI: causar dano a qualquer bem pertencente ao patrimônio público, deteriorando-o, por descuido ou má vontade, "
     "não constitui apenas uma ofensa ao equipamento e às instalações ou ao Estado, mas a todos os homens de boa vontade. "
     "Art. 5º, XI: é vedado retirar da repartição pública, sem estar legalmente autorizado, qualquer documento, livro ou bem "
     "pertencente ao patrimônio público estadual.",
     ["viatura", "combustível", "equipamento", "material", "uso particular", "computador"]),
]
ROTEIRO_BASE = ["Descreva, com suas palavras, o que aconteceu.", "Quando e onde o fato ocorreu?", "Quem estava presente?",
                "Existe registro (mensagem, documento, escala) do fato?", "O fato já tinha acontecido antes?"]
CASOS = [
    ("assedio_moral", "O chefe do setor gritou com a servidora na frente da equipe e a humilhou repetidas vezes, com ameaças de remoção."),
    ("desrespeito_publico", "O cidadão relata que foi mal atendido no balcão, tratado de forma grosseira e sem resposta sobre o laudo."),
    ("uso_cargo", "Servidor teria furado a fila de exames para atender um parente, usando a influência do cargo."),
    ("sigilo", "Foto do laudo de um caso em andamento foi compartilhada fora da instituição; suspeita de vazamento de informação sigilosa."),
    ("redes_sociais", "Servidor postou no grupo de WhatsApp da unidade print de conversa com comentários ofensivos sobre colegas."),
    ("assiduidade", "Plantonista faltou ao plantão sem aviso e a escala ficou descoberta por seis horas."),
    ("conflito_interesses", "Servidor indicou empresa da qual seria sócio para o contrato de manutenção do laboratório."),
    ("uso_bens", "Viatura da unidade foi usada para uso particular no fim de semana, com gasto de combustível."),
    ("assedio_moral", "Colega relata perseguição constante e constrangimento em reuniões, com xingamentos."),
    ("assiduidade", "Atrasos repetidos no horário de entrada e abandono do posto antes do fim da escala."),
]


def main():
    base = dt.date(2026, 9, 1)
    categorias = [{"id": i, "nome": n, "artigos": art, "texto_artigo": txt, "fonte": FONTE, "palavras": p, "roteiro_base": ROTEIRO_BASE}
                  for i, n, art, txt, p in CATEGORIAS]
    denuncias = []
    for n, (cat, relato) in enumerate(CASOS):
        rec = base + dt.timedelta(days=n * 5)
        denuncias.append({"id": f"CE-2026-{n + 1:03d}", "protocolo": f"CE-2026-{n + 1:03d}", "data_recebimento": rec.isoformat(), "canal": "e-mail",
                          "relato": relato, "denunciante": f"Denunciante Fictício {n + 1}", "denunciado": f"Servidor Fictício {chr(65 + n)}",
                          "etapa": "registro", "situacao": "aberto", "categoria_esperada": cat, "sigilo": True})
    seed = {"categorias": categorias, "denuncias": denuncias}
    (AQUI / "seed.json").write_text(json.dumps(seed, ensure_ascii=False, indent=1), encoding="utf-8")
    print({k: len(v) for k, v in seed.items()})


if __name__ == "__main__":
    main()
