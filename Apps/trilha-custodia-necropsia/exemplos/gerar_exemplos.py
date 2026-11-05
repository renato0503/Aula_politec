"""Gera os 10 corpos fictícios do Sistema de Controle de Necropsia (espelho do
protótipo "Sistema de Controle de Necropsia — DMML / POLITEC", de 02/11/2026).

O conjunto acompanha o protótipo campo a campo: acionamento, ocorrência, alocação
na base, necropsia, materiais lacrados, identificação, busca de familiares,
liberação ou sepultamento pelo Estado, funerária e entrega do laudo à ADM.

Todos os nomes, protocolos, delegacias e números são fictícios.

Uso: python "Apps/trilha-custodia-necropsia/exemplos/gerar_exemplos.py"
"""
import datetime as dt
import json
import pathlib

AQUI = pathlib.Path(__file__).resolve().parent

MARCOS = ["Saída da base", "Chegada ao local", "Saída do local", "Retorno ao IML"]
MATERIAIS = [("sangue", "Sangue", "Laboratório de DNA"),
             ("bio", "Material biológico", "Laboratório de Toxicologia"),
             ("projetil", "Projétil", "Laboratório de Balística"),
             ("pertences", "Pertences", "Arquivo de bens e pertences")]

PROFIS = {"Técnico Marcos Oliveira": "tecnico", "Médico Legista Dr. Eduardo Prado": "medico",
          "Gestor ADM Paulo Serrano": "gestor", "Central de plantão": "tecnico"}

# (data, hora de acionamento, número da necropsia, etapa, status do protótipo)
CASOS = [
    dict(proto="000123/2026", data="2026-03-02", hora="07:40", nec="NEC-2026-0123", etapa=2,
         nome="NÃO IDENTIFICADO", agente="Indeterminada",
         chegada="2026-03-02T08:15", delegacia="77ª DP — Vila Nova", autoridade="Dr. Henrique Matos",
         endereco="Rua das Acácias, s/n — margem da rodovia", municipio="Cachoeirinha", uf="PE",
         possivel="", filiacao="", nascimento="", idade="38", sexo="M",
         fonte="Policiamento rodoviário", documento="Não encontrado", telefone="",
         observacoes="Corpo encontrado em valeta, sem documentos.\nCondição de acesso difícil, chuva forte no local.",
         camara="", gaveta="", estado="", lacre_corpo=""),
    dict(proto="000124/2026", data="2026-03-04", hora="21:10", nec="NEC-2026-0124", etapa=2,
         nome="NÃO IDENTIFICADO", agente="Acidente de trânsito",
         chegada="2026-03-04T22:05", delegacia="3ª DP — Centro", autoridade="Dra. Patrícia Leal",
         endereco="Av. Presidente Kennedy, 1.820", municipio="Recife", uf="PE",
         possivel="", filiacao="", nascimento="", idade="45", sexo="M",
         fonte="Bombeiros", documento="Não encontrado", telefone="",
         observacoes="Colisão com veículo de grande porte.\nVítima sem identificação no local.",
         camara="", gaveta="", estado="", lacre_corpo=""),
    dict(proto="000125/2026", data="2026-03-05", hora="10:05", nec="NEC-2026-0125", etapa=3,
         nome="Ricardo Almeida (possível)", agente="Homicídio",
         chegada="2026-03-05T10:50", delegacia="9ª DP — Jardim Ipê", autoridade="Dr. Ronaldo Freire",
         endereco="Rua Sete de Setembro, 455", municipio="Olinda", uf="PE",
         possivel="Ricardo Almeida", filiacao="Maria Almeida / José Almeida", nascimento="1979-06-12",
         idade="46", sexo="M", fonte="Carteira de trabalho no local", documento="Carteira de trabalho (parcial)",
         telefone="(81) 99812-4470",
         observacoes="Vítima com ferimentos por arma de fogo.\nFamiliar informou possível identidade.",
         camara="Câmara 2", gaveta="G-07", estado="Conservado", lacre_corpo="LC-88210"),
    dict(proto="000126/2026", data="2026-03-06", hora="14:20", nec="NEC-2026-0126", etapa=3,
         nome="NÃO IDENTIFICADO", agente="Afogamento",
         chegada="2026-03-06T15:10", delegacia="Capitania dos Portos", autoridade="Cap. Lúcio Barros",
         endereco="Praia de Piedade, orla sul", municipio="Jaboatão dos Guararapes", uf="PE",
         possivel="", filiacao="", nascimento="", idade="30", sexo="M",
         fonte="Salva-vidas", documento="Não encontrado", telefone="",
         observacoes="Corpo recolhido pela maré.\nSem sinais de violência aparente, aguardando exame.",
         camara="Câmara 1", gaveta="G-03", estado="Putrefeito", lacre_corpo="LC-88214"),
    dict(proto="000127/2026", data="2026-03-08", hora="06:45", nec="NEC-2026-0127", etapa=4,
         nome="Desconhecido (possível)", agente="Homicídio",
         chegada="2026-03-08T07:30", delegacia="4ª DP — Boa Viagem", autoridade="Dra. Fernanda Lima",
         endereco="Rua dos Navegantes, 88", municipio="Recife", uf="PE",
         possivel="Desconhecido", filiacao="", nascimento="", idade="34", sexo="M",
         fonte="Vizinhança", documento="Não encontrado", telefone="",
         observacoes="Ferimentos múltiplos por instrumento perfurocortante.\nAguardando laudo preliminar da perícia.",
         camara="Câmara 2", gaveta="G-11", estado="Conservado", lacre_corpo="LC-88230",
         necropsia=dict(medico="Dr. Eduardo Prado", tecnico="Marcos Oliveira", odonto="Dra. Helena Tavares",
                        inicio="14:00", termino=""),
         materiais=dict(sangue=("LA-44101", True), bio=("LA-44102", True),
                         projetil=("LA-44103", False), pertences=("LA-44104", False))),
    dict(proto="000128/2026", data="2026-03-10", hora="18:30", nec="NEC-2026-0128", etapa=5,
         nome="NÃO IDENTIFICADO", agente="Indeterminada",
         chegada="2026-03-10T19:15", delegacia="1ª DP — Santo Antônio", autoridade="Dr. Carlos Ventura",
         endereco="Estrada do Engenho, km 4", municipio="Paulista", uf="PE",
         possivel="", filiacao="", nascimento="", idade="55", sexo="M",
         fonte="Morador local", documento="Não encontrado", telefone="",
         observacoes="Corpo em avançado estado de decomposição.\nSem objetos pessoais no local.",
         camara="Câmara 1", gaveta="G-05", estado="Putrefeito", lacre_corpo="LC-88241",
         necropsia=dict(medico="Dr. Eduardo Prado", tecnico="Marcos Oliveira", odonto="Dra. Helena Tavares",
                        inicio="09:30", termino="12:10"),
         identificacao=dict(resultado="pendente", metodo="Necropapiloscopia", nome_confirmado="",
                             responsavel="", data_confirmacao="",
                             tentativas=[dict(metodo="Necropapiloscopia", resultado="sem resultado",
                                               em="2026-03-12T09:00:00")]),
         materiais=dict(sangue=("LA-44150", True), bio=None, projetil=None, pertences=None)),
    dict(proto="000129/2026", data="2026-03-11", hora="08:00", nec="NEC-2026-0129", etapa=6,
         nome="Juliana Martins", agente="Suicídio",
         chegada="2026-03-11T08:40", delegacia="5ª DP — Casa Amarela", autoridade="Dra. Renata Vieira",
         endereco="Rua Doutor José Maria, 210", municipio="Recife", uf="PE",
         possivel="Juliana Martins", filiacao="Clara Martins", nascimento="1992-02-20",
         idade="34", sexo="F", fonte="Documento no local", documento="RG apresentado",
         telefone="(81) 98877-1203",
         observacoes="Identificação confirmada por documento.\nFamiliar responsável comparecerá para retirada.",
         camara="Câmara 1", gaveta="G-02", estado="Conservado", lacre_corpo="LC-88255",
         necropsia=dict(medico="Dr. Eduardo Prado", tecnico="Marcos Oliveira", odonto="Dra. Helena Tavares",
                        inicio="09:00", termino="12:00"),
         identificacao=dict(resultado="identificado", metodo="Necropapiloscopia", nome_confirmado="Juliana Martins",
                             responsavel="Técnico Marcos Oliveira", data_confirmacao="2026-03-13"),
         familia=dict(tipo="familiar", nome="", parentesco="", documento="", telefone="",
                      data_liberacao="", assinatura="", encontrada=False,
                      busca_iniciada_em="2026-03-13T14:00:00", busca_encerrada_em="",
                      busca_sem_sucesso=False, prazo_busca=30, resultado_busca=""),
         materiais=dict(sangue=("LA-44160", True), bio=None, projetil=None, pertences=("LA-44161", True))),
    dict(proto="000130/2026", data="2026-03-12", hora="11:00", nec="NEC-2026-0130", etapa=6,
         nome="Paulo Ribeiro", agente="Homicídio",
         chegada="2026-03-12T11:45", delegacia="2ª DP — Boa Vista", autoridade="Dr. Marcelo Gomes",
         endereco="Av. Conde da Boa Vista, 900", municipio="Recife", uf="PE",
         possivel="Paulo Ribeiro", filiacao="Antônio Ribeiro", nascimento="1968-09-03",
         idade="57", sexo="M", fonte="Policial militar", documento="Não encontrado", telefone="",
         observacoes="Identidade informada por vizinho, sem confirmação documental.\nFamiliares não localizados.",
         camara="Câmara 2", gaveta="G-09", estado="Conservado", lacre_corpo="LC-88270",
         necropsia=dict(medico="Dr. Eduardo Prado", tecnico="Marcos Oliveira", odonto="Dra. Helena Tavares",
                        inicio="09:00", termino="11:40"),
         identificacao=dict(resultado="identificado", metodo="Necropapiloscopia", nome_confirmado="Paulo Ribeiro",
                             responsavel="Técnico Marcos Oliveira", data_confirmacao="2026-03-14"),
         familia=dict(tipo="semFamiliar", nome="", parentesco="", documento="", telefone="",
                      data_liberacao="", assinatura="", encontrada=False,
                      busca_iniciada_em="2026-03-14T09:00:00", busca_encerrada_em="2026-03-19T10:00:00",
                      busca_sem_sucesso=True, prazo_busca=30,
                      resultado_busca="Sem êxito",
                      autorizacao=dict(numero="SE-5531", data="2026-03-19",
                                       local="Cemitério Municipal Vila Nova Cachoeirinha")),
         funeraria=dict(destino="estado", nome="Funerária Memorial Bandeirantes", auto="AE-20877",
                        data_entrega="2026-03-20", hora_entrega="15:20", autorizacao="SE-5531",
                        data_autorizacao="2026-03-19", local="Cemitério Municipal Vila Nova Cachoeirinha"),
         sepultamento=dict(justificativa="Busca por familiares encerrada sem êxito após 30 dias; "
                                         "identidade confirmada por necropapiloscopia, sem familiar reclamante.",
                           autorizacao="SE-5531", autorizado_em="2026-03-19T10:00:00", perfil="gestor"),
         destino_final="sepultamento",
         materiais=dict(sangue=("LA-44170", True), bio=None, projetil=("LA-44171", True), pertences=None)),
    dict(proto="000131/2026", data="2026-03-14", hora="07:10", nec="NEC-2026-0131", etapa=7,
         nome="Marcelo Duarte", agente="Acidente de trânsito",
         chegada="2026-03-14T07:50", delegacia="6ª DP — Imbiribeira", autoridade="Dr. Jorge Teles",
         endereco="BR-101, km 62", municipio="Cabo de Santo Agostinho", uf="PE",
         possivel="Marcelo Duarte", filiacao="Lúcia Duarte", nascimento="1984-11-05",
         idade="41", sexo="M", fonte="Polícia Rodoviária Federal", documento="CNH",
         telefone="(81) 99650-2281",
         observacoes="Colisão frontal entre veículos.\nIdentificação confirmada pela CNH.",
         camara="Câmara 1", gaveta="G-04", estado="Conservado", lacre_corpo="LC-88290",
         necropsia=dict(medico="Dr. Eduardo Prado", tecnico="Marcos Oliveira", odonto="Dra. Helena Tavares",
                        inicio="09:00", termino="11:30"),
         identificacao=dict(resultado="identificado", metodo="Necropapiloscopia", nome_confirmado="Marcelo Duarte",
                             responsavel="Técnico Marcos Oliveira", data_confirmacao="2026-03-15"),
         familia=dict(tipo="familiar", nome="Lúcia Duarte", parentesco="Mãe", documento="RG 12.998.330-1",
                      telefone="(81) 99650-2281", data_liberacao="2026-03-17", assinatura="", encontrada=True,
                      busca_iniciada_em="2026-03-13T09:00:00", busca_encerrada_em="2026-03-14T11:00:00",
                      busca_sem_sucesso=False, prazo_busca=30, resultado_busca="Familiar localizado"),
         funeraria=dict(destino="familia", nome="Funerária São Judas Tadeu", auto="AE-20901",
                        data_entrega="2026-03-18", hora_entrega="10:30"),
         entrega=dict(responsavel="Lúcia Duarte", documento="AE-20901", data="2026-03-18T10:30:00"),
         situacao="liberado", destino_final="família",
         materiais=dict(sangue=("LA-44180", True), bio=("LA-44181", True), projetil=None, pertences=("LA-44182", True))),
    dict(proto="000132/2026", data="2026-03-15", hora="09:20", nec="NEC-2026-0132", etapa=7,
         nome="Renata Costa", agente="Suicídio",
         chegada="2026-03-15T10:05", delegacia="7ª DP — Afogados", autoridade="Dra. Simone Brito",
         endereco="Rua da Hora, 77", municipio="Recife", uf="PE",
         possivel="Renata Costa", filiacao="Helena Costa", nascimento="1979-04-27",
         idade="46", sexo="F", fonte="Documento no local", documento="RG apresentado",
         telefone="(81) 98112-0764",
         observacoes="Identificação confirmada por documento.\nLaudo entregue à ADM com cadeia de custódia completa.",
         camara="Câmara 1", gaveta="G-01", estado="Conservado", lacre_corpo="LC-88301",
         necropsia=dict(medico="Dr. Eduardo Prado", tecnico="Marcos Oliveira", odonto="Dra. Helena Tavares",
                        inicio="09:30", termino="12:00"),
         identificacao=dict(resultado="identificado", metodo="Necropapiloscopia", nome_confirmado="Renata Costa",
                             responsavel="Técnico Marcos Oliveira", data_confirmacao="2026-03-16"),
         familia=dict(tipo="familiar", nome="Helena Costa", parentesco="Mãe", documento="RG 10.554.201-8",
                      telefone="(81) 98112-0764", data_liberacao="2026-03-18", assinatura="", encontrada=True,
                      busca_iniciada_em="2026-03-15T10:30:00", busca_encerrada_em="2026-03-16T14:00:00",
                      busca_sem_sucesso=False, prazo_busca=30, resultado_busca="Familiar localizado"),
         funeraria=dict(destino="familia", nome="Funerária Serenidade", auto="AE-20855",
                        data_entrega="2026-03-22", hora_entrega="14:00"),
         entrega=dict(responsavel="Helena Costa", documento="AE-20855", data="2026-03-22T14:00:00"),
         laudo=dict(entregue_por="Ana Paula Ribeiro", entregue_em="2026-03-24T10:30:00",
                    recebido_por="Carlos Eduardo Nunes", recebido_em="2026-03-24T11:00:00",
                    assinatura_recebimento="", confirmado_perfil="gestor"),
         situacao="liberado", destino_final="família", custodia_finalizada=True,
         finalizada_em="2026-03-24T11:00:00",
         materiais=dict(sangue=("LA-44190", True), bio=None, projetil=None, pertences=("LA-44191", True))),
]

# (protocolo): [(quando, quem, o que aconteceu)]
HISTORICO = {
    "000123/2026": [("02/03/2026 08:20", "Técnico Marcos Oliveira", "Ocorrência registrada e acionamento confirmado."),
                    ("02/03/2026 07:40", "Central de plantão", "Caso acionado pela Polícia Rodoviária.")],
    "000124/2026": [("04/03/2026 22:10", "Técnico Marcos Oliveira", "Acionamento recebido dos Bombeiros."),
                    ("04/03/2026 21:10", "Central de plantão", "Caso registrado para atendimento.")],
    "000125/2026": [("05/03/2026 11:30", "Técnico Marcos Oliveira", "Corpo transferido para câmara fria da base."),
                    ("05/03/2026 10:50", "Técnico Marcos Oliveira", "Ocorrência registrada e possível vítima informada."),
                    ("05/03/2026 10:05", "Central de plantão", "Caso acionado pela Delegacia de Olinda.")],
    "000126/2026": [("06/03/2026 15:30", "Técnico Marcos Oliveira", "Corpo acondicionado para câmara fria."),
                    ("06/03/2026 15:10", "Técnico Marcos Oliveira", "Ocorrência registrada no local."),
                    ("06/03/2026 14:20", "Central de plantão", "Caso acionado pela Capitania dos Portos.")],
    "000127/2026": [("08/03/2026 14:00", "Médico Legista Dr. Eduardo Prado", "Necropsia iniciada na bancada 3."),
                    ("08/03/2026 11:30", "Técnico Marcos Oliveira", "Corpo liberado da câmara fria para necropsia."),
                    ("08/03/2026 07:30", "Técnico Marcos Oliveira", "Ocorrência registrada.")],
    "000128/2026": [("12/03/2026 09:00", "Médico Legista Dr. Eduardo Prado", "Necropsia concluída, laudo preliminar emitido."),
                    ("10/03/2026 19:15", "Técnico Marcos Oliveira", "Ocorrência registrada."),
                    ("10/03/2026 18:30", "Central de plantão", "Caso acionado.")],
    "000129/2026": [("13/03/2026 14:00", "Técnico Marcos Oliveira", "Identificação confirmada por necropapiloscopia."),
                    ("12/03/2026 10:30", "Médico Legista Dr. Eduardo Prado", "Necropsia concluída."),
                    ("11/03/2026 08:40", "Técnico Marcos Oliveira", "Ocorrência registrada.")],
    "000130/2026": [("20/03/2026 16:00", "Técnico Marcos Oliveira", "Sepultamento pelo Estado registrado — funerária Funerária Memorial Bandeirantes, Auto de Entrega AE-20877, autorização SE-5531 de 19/03/2026. Local: Cemitério Municipal Vila Nova Cachoeirinha."),
                    ("19/03/2026 10:00", "Gestor ADM Paulo Serrano", "Busca por familiares encerrada sem êxito. Autorização de sepultamento emitida."),
                    ("13/03/2026 09:00", "Técnico Marcos Oliveira", "Necropsia concluída. Familiar não localizado.")],
    "000131/2026": [("17/03/2026 15:00", "Técnico Marcos Oliveira", "Entrega ao familiar confirmada — funerária ação pendente."),
                    ("16/03/2026 10:00", "Médico Legista Dr. Eduardo Prado", "Necropsia concluída."),
                    ("14/03/2026 07:50", "Técnico Marcos Oliveira", "Ocorrência registrada.")],
    "000132/2026": [("24/03/2026 11:00", "Gestor ADM Paulo Serrano", "Laudo entregue à ADM — entregue por Ana Paula Ribeiro, recebido por Carlos Eduardo Nunes, em 24/03/2026. Assinatura registrada. Caso concluído."),
                    ("22/03/2026 14:00", "Técnico Marcos Oliveira", "Entrega à funerária confirmada — Funerária Serenidade, Auto AE-20855."),
                    ("18/03/2026 09:00", "Técnico Marcos Oliveira", "Liberação ao familiar confirmada."),
                    ("15/03/2026 10:05", "Técnico Marcos Oliveira", "Ocorrência registrada.")],
}


def iso_hora(br):
    """'02/03/2026 08:20' -> '2026-03-02T08:20:00'."""
    d, h = br.split(" ")
    dia, mes, ano = d.split("/")
    return f"{ano}-{mes}-{dia}T{h}:00:00"


def main():
    corpos, marcos, lacres, log = [], [], [], []
    for n, caso in enumerate(CASOS):
        cid = f"C-{n + 1:04d}"
        materiais = caso.get("materiais") or {}
        identificacao = caso.get("identificacao")
        necropsia = caso.get("necropsia")
        nome = caso["nome"]
        identificado = bool(identificacao and identificacao.get("resultado") == "identificado")
        situacao = caso.get("situacao") or ("aguardando identificação" if caso["etapa"] == 5 else "em custódia")
        corpo = {
            "id_corpo": cid,
            "protocolo": caso["proto"],
            "numero_necropsia": caso["nec"],
            "entrada": caso["data"],
            "criado_em": f"{caso['data']}T{caso['hora']}:00",
            "tecnico": "Técnico Marcos Oliveira",
            "origem": caso["delegacia"],
            "natureza": caso["agente"],
            "agente_causal": caso["agente"],
            "municipio": caso["municipio"],
            "local": caso["endereco"],
            "nome": identificacao.get("nome_confirmado", "") if identificado else "",
            "documento": caso["documento"] if identificado else "",
            "desconhecido": not identificado,
            "identificado": identificado,
            "sexo": caso["sexo"],
            "idade": caso["idade"],
            "situacao": situacao,
            "etapa": caso["etapa"],
            "etapa_em": f"{caso['data']}T{caso['hora']}:00",
            "acionamento": {"horario": caso["hora"], "numero": caso["nec"]},
            "ocorrencia": {
                "chegada": caso["chegada"], "delegacia": caso["delegacia"], "autoridade": caso["autoridade"],
                "endereco": caso["endereco"], "municipio": caso["municipio"], "uf": caso["uf"],
                "possivel_nome": caso["possivel"], "filiacao": caso["filiacao"], "nascimento": caso["nascimento"],
                "idade": caso["idade"], "sexo": caso["sexo"], "fonte": caso["fonte"],
                "documento": caso["documento"], "telefone": caso["telefone"], "observacoes": caso["observacoes"],
                "fotos_doc": [], "fotos_cena": [],
            },
            "camara": caso["camara"], "gaveta": caso["gaveta"], "estado_corpo": caso["estado"],
            "lacre_corpo": caso["lacre_corpo"], "confirmado_entrada": bool(caso["camara"]),
            "necropsia": necropsia or {},
            "identificacao": identificacao or {},
            "familia": caso.get("familia") or {},
            "funeraria": caso.get("funeraria") or {},
            "laudo": caso.get("laudo") or {},
            "sepultamento": caso.get("sepultamento"),
            "entrega": caso.get("entrega"),
            "destino_final": caso.get("destino_final", ""),
            "custodia_finalizada": bool(caso.get("custodia_finalizada")),
            "finalizada_em": caso.get("finalizada_em", ""),
            "retificacoes": [],
        }
        corpos.append(corpo)

        # marcos do deslocamento (RN03): os quatro depois que o corpo volta ao IML
        chegada = caso["chegada"]
        datas = {"Saída da base": f"{caso['data']}T{caso['hora']}:00", "Chegada ao local": chegada}
        if caso["etapa"] >= 3:
            base = dt.datetime.fromisoformat(chegada)
            datas["Saída do local"] = (base + dt.timedelta(hours=1)).isoformat()
            datas["Retorno ao IML"] = (base + dt.timedelta(hours=2)).isoformat()
        for k, tipo in enumerate(MARCOS):
            if tipo not in datas:
                continue
            marcos.append({"id_marco": f"{cid}-M{k + 1}", "corpo_id": cid, "tipo": tipo,
                           "data_hora": datas[tipo], "perfil": "tecnico", "observacao": ""})

        # materiais: um registro por tipo, com o lacre e o recebimento pela ADM
        for k, (tipo, nome_material, destino) in enumerate(MATERIAIS):
            item = materiais.get(tipo)
            coletado = bool(item)
            codigo = item[0] if item else ""
            recebido = bool(item and item[1])
            lacres.append({
                "id_lacre": f"{cid}-L{k + 1}", "corpo_id": cid, "tipo": tipo, "nome": nome_material,
                "coletado": coletado, "codigo": codigo, "destino": destino if coletado else "",
                "data_hora": f"{caso['data']}T12:00:00", "perfil": "tecnico",
                **({"recebido_em": f"{caso['data']}T14:00:00", "recebido_por": "Gestor ADM Paulo Serrano",
                    "recebido_perfil": "gestor"} if recebido else {}),
            })

        for k, (quando, quem, texto) in enumerate(HISTORICO[caso["proto"]]):
            log.append({"id": f"L-{cid}-{k + 1}", "corpo_id": cid, "acao": texto,
                        "perfil": PROFIS.get(quem, "tecnico"), "data_hora": iso_hora(quando)})

    seed = {"corpos": corpos, "marcos": marcos, "lacres": lacres, "log": log}
    (AQUI / "seed.json").write_text(json.dumps(seed, ensure_ascii=False, indent=1), encoding="utf-8")
    print({k: len(v) for k, v in seed.items()})


if __name__ == "__main__":
    main()
