"""Gera Apps/LINKS-ALUNOS.md: por app, a equipe, o link do app, o hub, o
formulário de feedback e o repositório. É o texto que o professor manda aos
alunos (lista, e não tabela, para ler bem no WhatsApp e no e-mail).

Uso: python Apps/_base/gerar_links_alunos.py
"""
import json
import pathlib

APPS = pathlib.Path(__file__).resolve().parent.parent
SITE = "https://renato0503.github.io/Aula_politec/"
NOMES = {"agiliza-mais": "Agiliza+ · Gerador de laudos de exame em celular",
         "teia-triagem-emails": "TEIA · Triagem de E-mails com Isolação Automatizada",
         "equipamentos-google-earth": "Mapa de Equipamentos (Google Earth)"}
OBS = {"agendamento-cin": "este link abre a versão de demonstração. A agenda pública definitiva roda no Google Apps Script, que ainda vai ser publicado."}


def main():
    e = json.loads((APPS / "equipes.json").read_text(encoding="utf-8"))["apps"]
    itens = sorted(e.items(), key=lambda kv: (NOMES.get(kv[0]) or kv[1]["projeto"]).lower())
    L = ["# Apps do curso POLITEC/MT · links por equipe", "",
         "Cada app abre direto no navegador (Edge ou Chrome), funciona sem internet e guarda os dados só no seu computador.",
         "O **hub** de cada app mostra o processo de hoje (AS-IS), o processo com o app (TO-BE), os indicadores e como testar.",
         "O **feedback** é o formulário em que você diz o que funciona, o que falta e o que mudar. As respostas guiam a próxima etapa de desenvolvimento do app.", "",
         "## Como fazer o feedback", "",
         "1. Abra o link do app e vá em **Configuração › Carregar dados fictícios**.",
         "2. Use cada tela como se fosse um caso do seu setor.",
         "3. Abra o link de **feedback** do seu app e responda tela por tela. O rascunho fica salvo no navegador até você enviar.",
         "4. Não escreva CPF, nome de pessoa atendida ou dado real de caso.", "",
         f"Todos os apps em uma página: {SITE}Apps/index.html", ""]
    for i, (slug, v) in enumerate(itens, 1):
        L += [f"## {i}. {NOMES.get(slug) or v['projeto']}", "",
              f"- **Equipe:** {', '.join(a['nome'] for a in v['alunos'])}",
              f"- **App:** {SITE}Apps/{slug}/index.html",
              f"- **Hub do app:** {SITE}Apps/{slug}/processo.html",
              f"- **Feedback:** {SITE}Aula%208/feedback/{slug}.html",
              f"- **Código (GitHub):** https://github.com/renato0503/{slug}"]
        if slug == "gestao_identificados":
            L.append(f"- **Painel de desaparecidos (CNPD/MJ):** {SITE}Apps/{slug}/desaparecidos.html")
        if slug in OBS:
            L.append(f"- **Observação:** {OBS[slug]}")
        L.append("")
    L += ["---", "",
          "**Backup:** os dados dos apps ficam só no navegador. Exporte o backup (.json) em **Configuração** toda semana.", ""]
    (APPS / "LINKS-ALUNOS.md").write_text("\n".join(L), encoding="utf-8")
    print(len(itens), "apps em Apps/LINKS-ALUNOS.md")


if __name__ == "__main__":
    main()
