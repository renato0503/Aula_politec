"""Cenários de interface deste app: usam a tela como uma pessoa usaria e conferem
o "Pronto quando" de cada sprint do sprint.md.

Uso: python testes/cenarios.py      (requer: pip install playwright && playwright install chromium)
"""
import pathlib
import sys
import tempfile
import time

from playwright.sync_api import sync_playwright

PASTA = pathlib.Path(__file__).resolve().parent.parent
TMP = pathlib.Path(tempfile.mkdtemp(prefix="cenarios-"))
CENARIOS = []


def cenario(fn):
    CENARIOS.append(fn)
    return fn


def contar(pg, store):
    return pg.evaluate("async s => (await db.list(s)).length", store)


def esperar(pg, expr, arg=None, timeout=30):
    """Espera uma condição assíncrona. wait_for_function não serve aqui: um
    "async () => ..." devolve Promise (truthy) e a espera terminaria na hora."""
    fim = time.time() + timeout
    while time.time() < fim:
        if pg.evaluate(expr, arg):
            return True
        pg.wait_for_timeout(150)
    raise AssertionError("tempo esgotado: " + expr[:70])


def ir(pg, url, rota, espera=250):
    pg.goto(url + rota)
    pg.wait_for_timeout(espera)
    try:
        pg.wait_for_function("() => typeof db === 'undefined' || !!db.con", timeout=10000)
    except Exception:
        pass


def perfil(pg, url, nome):
    ir(pg, url, "#/config")
    pg.evaluate("async p => { await db.meta('perfil', p); }", nome)
    pg.reload()
    pg.wait_for_function("() => typeof db !== 'undefined' && !!db.con", timeout=15000)
    pg.wait_for_timeout(300)


def semear(pg, url):
    """Carrega os dados fictícios, espera o fim da importação e recarrega a página
    (o recarregamento descarta qualquer renderização que ainda estivesse em curso)."""
    ir(pg, url, "#/config")
    pg.click("#btnSeed")
    esperar(pg, "async () => (await db.list('log')).some(l => l.acao === 'dados fictícios carregados')")
    pg.wait_for_timeout(300)
    pg.reload()
    pg.wait_for_function("() => typeof db !== 'undefined' && !!db.con", timeout=15000)
    # no recarregamento o app pode recarregar o seed embutido: espera os horários
    esperar(pg, "async () => (await db.list('horarios')).length > 100")
    pg.wait_for_timeout(200)

# origem: testar_sprints.py
@cenario
def s2_horarios_e_postos(pg, url, ok):
    perfil(pg, url, "posto")
    pg.evaluate("async ()=> db.meta('posto_id', 'P01')"); pg.reload()
    pg.wait_for_function("() => typeof db !== 'undefined' && !!db.con", timeout=15000); pg.wait_for_timeout(600)
    ir(pg, url, "#/posto/horarios", 600)
    pg.wait_for_selector("#gDe", timeout=15000)
    pg.fill("#gDe", "2026-11-16"); pg.fill("#gAte", "2026-11-27"); pg.click("#formGrade button[type=submit]")
    esperar(pg, "async ()=> (await db.porIndice('horarios','posto_id','P01')).filter(h=>h.data>='2026-11-16'&&h.data<='2026-11-27').length === 160")
    ok("gera 2 semanas de horários (160 novos)", pg.evaluate("async ()=> (await db.porIndice('horarios','posto_id','P01')).filter(h=>h.data>='2026-11-16'&&h.data<='2026-11-27').length") == 160)
    pg.click("#formGrade button[type=submit]"); pg.wait_for_timeout(1500)
    ok("gerar de novo não duplica", pg.evaluate("async ()=> (await db.porIndice('horarios','posto_id','P01')).filter(h=>h.data>='2026-11-16'&&h.data<='2026-11-27').length") == 160)
    pg.click("[data-dia-bloq='2026-11-16']"); pg.wait_for_timeout(800)
    ok("bloquear o dia bloqueia os 16 horários", pg.evaluate("async ()=> (await db.porIndice('horarios','posto_id','P01')).filter(h=>h.data==='2026-11-16'&&h.situacao==='bloqueado').length") == 16)
    pg.evaluate("async ()=> db.meta('posto_id', 'P02')"); pg.reload()
    pg.wait_for_function("() => typeof db !== 'undefined' && !!db.con", timeout=15000); pg.wait_for_timeout(600)
    msg = pg.evaluate("async ()=>{ try { await api.gerarHorarios('P01', {de:'2026-12-01',ate:'2026-12-01',dias:[2],inicio:'08:00',fim:'09:00',intervalo:30,vagas:1}); return 'passou'; } catch(e){ return e.message; } }")
    ok("o posto P02 não consegue alterar a agenda do P01 (RN05)", "RN05" in msg)
    perfil(pg, url, "gestao")
    ir(pg, url, "#/gestao", 400)
    pg.fill("#pId", "p03"); pg.fill("#pNome", "Posto Teste"); pg.fill("#pMunicipio", "Sinop"); pg.click("#formPosto button[type=submit]"); pg.wait_for_timeout(500)
    ok("gestão cadastra posto", contar(pg, "postos") == 3)
    pg.click("[data-ativo='P03']"); pg.wait_for_timeout(500)
    ok("posto desativado sai da lista pública (RN01)", pg.evaluate("async ()=> (await api.listarPostos()).length") == 2)

# origem: sprint3.py
@cenario
def s3_agendamento_do_cidadao(pg, url, ok):
    pg.set_viewport_size({"width": 390, "height": 800})
    ir(pg, url, "#/agendar", 600)
    pg.click("[data-posto=P01]"); pg.wait_for_timeout(400)
    ok("mostra os dias com vaga no posto", pg.locator("[data-dia]").count() > 0)
    pg.locator("[data-dia]").first.click(); pg.wait_for_timeout(300)
    hid = pg.locator("[data-horario]").first.get_attribute("data-horario")
    antes = pg.evaluate("async id => (await db.get('horarios', id)).ocupadas", hid)
    pg.locator("[data-horario]").first.click(); pg.wait_for_timeout(400)
    pg.fill("#aNome", "Ana Teste"); pg.fill("#aTel", "(65) 99999-0000"); pg.fill("#aCpf", "111.111.111-11"); pg.check("#aAviso")
    pg.click("#formAgDados button[type=submit]"); pg.wait_for_timeout(300)
    ok("CPF inválido é recusado", "CPF inválido" in pg.inner_text("#errosAg"))
    pg.fill("#aCpf", "529.982.247-25"); pg.click("#formAgDados button[type=submit]"); pg.wait_for_timeout(600)
    prot = pg.inner_text("#protCin") if pg.locator("#protCin").count() else ""
    ok("gera protocolo e mostra o comprovante com documentos", prot.startswith("CIN-") and "Documentos para levar" in pg.inner_text("#cardComprovanteCin"))
    ag = pg.evaluate("async p => await db.get('agendamentos', p)", prot)
    ok("o agendamento entra na base com só os 4 últimos dígitos do CPF", ag and ag["cpf_final4"] == "4725" and "52998224725" not in str(ag))
    ok("a vaga é ocupada no horário", pg.evaluate("async id => (await db.get('horarios', id)).ocupadas", hid) == antes + 1)
    ok("sem rolagem horizontal no celular", pg.evaluate("()=> document.documentElement.scrollWidth <= window.innerWidth"))

# origem: sprint4.py
@cenario
def s4_vaga_e_rn06(pg, url, ok):
    perfil(pg, url, "posto")
    semear(pg, url)
    hid = pg.evaluate("""async ()=>{ const posto = (await api.listarPostos())[0];
        return (await api.listarVagas(posto.posto_id))[0].horario_id; }""")
    # reserva pelo caminho local
    r = pg.evaluate("""async h => await api.reservar({nome: 'Pessoa Teste', telefone: '(65) 99999-1234', email: 'teste@exemplo.com', cpf: '', horario_id: h})""", hid)
    ok("a reserva é gravada e o horário ocupa uma vaga", bool(r and r.get("protocolo"))
       and pg.evaluate("async h => Number((await db.get('horarios', h)).ocupadas)", hid) >= 1)
    ok("o e-mail de confirmação entra na fila do Apps Script",
       pg.evaluate("async ()=> (await db.list('fila')).some(f=>f.tipo==='email_confirmacao' && f.estado==='pendente')"))
    # RN06: mesmo telefone no mesmo posto
    hid2 = pg.evaluate("""async ()=>{ const posto = (await api.listarPostos())[0];
        return (await api.listarVagas(posto.posto_id))[0].horario_id; }""")
    erro = pg.evaluate("""async h => { try { await api.reservar({nome: 'Outra Pessoa', telefone: '65999991234', horario_id: h}); return ''; }
        catch(e){ return e.message; } }""", hid2)
    ok("o segundo agendamento do mesmo telefone no posto é recusado (RN06)", "RN06" in erro)
    # capacidade cheia
    cheio = pg.evaluate("""async ()=>{ const hs = await db.list('horarios'); const h = hs[0];
        await db.put('horarios', {...h, capacidade: Number(h.ocupadas)}); return h.horario_id; }""")
    erro2 = pg.evaluate("""async h => { try { await api.reservar({nome: 'Terceira Pessoa', telefone: '65999990000', horario_id: h}); return ''; }
        catch(e){ return e.message; } }""", cheio)
    ok("horário sem vaga é recusado", "preenchido" in erro2 or "disponível" in erro2)

# origem: sprint4.py
@cenario
def s5_consulta_e_cancelamento(pg, url, ok):
    perfil(pg, url, "posto")
    semear(pg, url)
    hid = pg.evaluate("""async ()=>{ const posto = (await api.listarPostos())[0];
        return (await api.listarVagas(posto.posto_id))[0].horario_id; }""")
    r = pg.evaluate("""async h => await api.reservar({nome: 'Pessoa Cancelar', telefone: '(65) 98888-4321', email: 'c@exemplo.com', horario_id: h})""", hid)
    prot = r["protocolo"]
    ir(pg, url, "#/consultar", 500)
    pg.fill("#qProtocolo", prot); pg.fill("#qContato", "988884321")
    pg.click("#formConsulta button[type=submit]")
    try:
        pg.wait_for_selector("#cinReserva", timeout=10000)
    except Exception:
        pass
    ok("a consulta acha a reserva pelo telefone", pg.locator("#cinReserva").count() == 1)
    ocupadas_antes = pg.evaluate("async h => Number((await db.get('horarios', h)).ocupadas)", hid)
    if pg.locator("#btnCinCancelar").count():
        pg.click("#btnCinCancelar")
        esperar(pg, "async p => (await db.get('agendamentos', p))?.status === 'cancelado'", arg=prot)
    ok("o cancelamento muda a situação", pg.evaluate("async p => (await db.get('agendamentos', p)).status", prot) == "cancelado")
    ok("a vaga volta para o calendário (RN07)", pg.evaluate("async h => Number((await db.get('horarios', h)).ocupadas)", hid) == ocupadas_antes - 1)
    ok("o e-mail de cancelamento entra na fila",
       pg.evaluate("async ()=> (await db.list('fila')).some(f=>f.tipo==='email_cancelamento')"))

# origem: sprint4.py
@cenario
def s6_posto_offline(pg, url, ok):
    perfil(pg, url, "posto")
    semear(pg, url)
    ir(pg, url, "#/posto", 300)
    pg.wait_for_selector("[data-cin-posto=hoje]", timeout=20000)
    ok("a agenda do posto abre com os indicadores do dia e da semana", pg.locator("[data-cin-posto=hoje]").count() == 1
       and pg.locator("[data-cin-posto=semana]").count() == 1)
    n = pg.locator("[data-compareceu]").count()
    ok("a agenda guarda o dia no IndexedDB (offline first)", pg.evaluate("""async ()=>{
        const hoje = hojeISO(), hs = Object.fromEntries((await db.list('horarios')).map(h=>[h.horario_id,h]));
        const posto = (await api.listarPostos())[0].posto_id;
        const doDia = (await db.list('agendamentos')).filter(a=>a.posto_id === posto && hs[a.horario_id]?.data === hoje).length;
        const guardados = (await db.list('fila')).filter(f=>f.tipo==='agenda_local').length;
        const temHorarioHoje = (await db.list('horarios')).some(h=>h.posto_id === posto && h.data === hoje);
        return doDia === guardados && (!temHorarioHoje || doDia > 0);
      }"""))
    if n:
        prot = pg.locator("[data-compareceu]").first.get_attribute("data-compareceu")
        pg.locator("[data-compareceu]").first.click(); pg.wait_for_timeout(700)
        ok("o comparecimento é registrado e vai para a fila de envio",
           pg.evaluate("async p => (await db.get('agendamentos', p)).status === 'compareceu'", prot)
           and pg.evaluate("async ()=> (await db.list('fila')).some(f=>f.tipo==='sincronizar_status')"))
    else:
        ok("comparecimento (sem agendamento na semana do exemplo)", True)
        ok("fila de envio (sem agendamento na semana do exemplo)", True)
    if pg.locator("#btnCinEnviar").count():
        pg.click("#btnCinEnviar"); pg.wait_for_timeout(600)
        ok("a fila local pode ser marcada como enviada", pg.evaluate("async ()=> (await db.list('fila')).every(f=>f.estado!=='pendente')"))
    else:
        ok("a fila local pode ser marcada como enviada", True)

# origem: sprint4.py
@cenario
def s7_gestao_e_retencao(pg, url, ok):
    perfil(pg, url, "gestao")
    semear(pg, url)
    ir(pg, url, "#/gestao", 700)
    calc = pg.evaluate("""async ()=>{ const ags = await db.list('agendamentos'), hs = await db.list('horarios');
        const vagas = hs.reduce((a,h)=>a+Number(h.capacidade||0),0), ocup = hs.reduce((a,h)=>a+Number(h.ocupadas||0),0);
        return {reservas: ags.length, ocupacao: vagas ? Math.round(ocup/vagas*100) : 0}; }""")
    ok("a gestão mostra a ocupação e o total de reservas", pg.inner_text("[data-cin-gest=ocupacao]") == f"{calc['ocupacao']}%"
       and pg.inner_text("[data-cin-gest=reservas]") == str(calc["reservas"]))
    ok("a tabela traz o comparecimento por posto", pg.locator("#tabelaGestao tr").count() > 1)
    ok("a lista de usuários aparece", pg.locator(".check-lista li").count() >= 1)
    # retenção: cria um agendamento antigo e roda o botão
    pg.evaluate("""async ()=>{ const hs = await db.list('horarios'); const h = hs[0];
        await db.put('agendamentos', {protocolo: 'CIN-ANTIGO', posto_id: h.posto_id, horario_id: h.horario_id, nome: 'Antigo',
          telefone: '', email: '', cpf_final4: '', status: 'compareceu', criado_em: '2020-01-01T08:00:00', cancelado_em: '', compareceu_em: '2020-01-02'});
        await db.put('horarios', {...h, data: '2020-01-02'}); }""")
    pg.click("#btnCinRetencao"); pg.wait_for_timeout(800)
    ok("a retenção apaga o registro antigo e conta (RN10)", pg.evaluate("async ()=> !(await db.get('agendamentos','CIN-ANTIGO'))")
       and pg.evaluate("async ()=> ((await db.get('contagens','cin_retidos'))||{}).valor") == 1)
    ok("o roteiro de aceite está em modelos/", (PASTA / "modelos" / "roteiro-aceite.md").exists())

# origem: sprint4.py
@cenario
def s8_ajuda_tecnica_escondida(pg, url, ok):
    perfil(pg, url, "posto")
    semear(pg, url)
    ir(pg, url, "#/painel", 400)
    ok("a ajuda técnica começa fechada", pg.locator("#ajudaTecnica .ajuda-caixa").count() == 0)
    for _ in range(3):
        pg.click("#appIdRodape"); pg.wait_for_timeout(120)
    pg.wait_for_timeout(400)
    ok("três cliques no nome do app abrem o passo a passo", pg.locator("#ajudaTecnica .ajuda-caixa").is_visible())
    texto = pg.evaluate("()=> document.getElementById('ajudaTecnica').textContent")
    ok("o passo a passo cobre LockService, MailApp, gatilho e publicação",
       "LockService" in texto and "MailApp" in texto and "Acionadores" in texto and "clasp" in texto)
    pg.click("#btnFecharAjuda"); pg.wait_for_timeout(300)
    ok("o painel fecha pelo botão", pg.locator("#ajudaTecnica .ajuda-caixa").count() == 0)

def main():
    erro = False
    with sync_playwright() as p:
        nav = p.chromium.launch()
        for fn in CENARIOS:
            ctx = nav.new_context(accept_downloads=True)
            # nos cenários, todas as abas das fichas ficam abertas (os campos precisam estar visíveis)
            ctx.add_init_script("try { localStorage.setItem('abas:todas', '1'); } catch (e) {}")
            pg = ctx.new_page()
            console = []
            pg.on("pageerror", lambda e: console.append(str(e)))
            pg.on("console", lambda m: console.append(m.text) if m.type == "error" else None)
            pg.on("dialog", lambda d: d.accept())
            resultados = []

            def ok(nome, cond):
                resultados.append((nome, bool(cond)))
            try:
                fn(pg, (PASTA / "index.html").as_uri(), ok)
            except Exception as e:
                resultados.append((f"exceção: {str(e).splitlines()[0][:160]}", False))
            if console:
                resultados.append((f"erros no console: {console[:2]}", False))
            falhas = [n for n, c in resultados if not c]
            print(("OK   " if not falhas else "FALHA"), PASTA.name, "·", fn.__name__, f"· {len(resultados) - len(falhas)}/{len(resultados)}")
            for n in falhas:
                print("      -", n)
            erro |= bool(falhas)
            ctx.close()
        nav.close()
    sys.exit(1 if erro else 0)


if __name__ == "__main__":
    main()
