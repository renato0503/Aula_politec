/**
 * Testa o Code.gs sem a conta Google: simula SpreadsheetApp, Session e LockService
 * com uma planilha em memória carregada da planilha modelo (planilha-modelo/seed.json).
 *
 * Uso: node "Apps/agendamento-cin/testes/testar_code_gs.js"
 */
const fs = require("fs"), path = require("path"), vm = require("vm");
const raiz = path.join(__dirname, "..");
const seed = JSON.parse(fs.readFileSync(path.join(raiz, "planilha-modelo", "seed.json"), "utf8"));
const CABECALHO_LOG = ["id", "data_hora", "usuario", "acao", "protocolo", "detalhe"];

function planilhaFalsa() {
  const abas = {};
  for (const [nome, linhas] of Object.entries(seed)) {
    const cab = linhas.length ? Object.keys(linhas[0]) : CABECALHO_LOG;
    abas[nome] = [cab, ...linhas.map(o => cab.map(c => o[c]))];
  }
  const aba = nome => abas[nome] && {
    getDataRange: () => ({ getValues: () => abas[nome].map(l => l.slice()) }),
    getLastRow: () => abas[nome].length,
    getRange: (r, c, nr = 1, nc = 1) => ({
      setValues: v => v.forEach((l, i) => { abas[nome][r - 1 + i] = abas[nome][r - 1 + i] || []; l.forEach((x, j) => abas[nome][r - 1 + i][c - 1 + j] = x); }),
      setValue: x => { abas[nome][r - 1][c - 1] = x; }
    })
  };
  return { abas, getSheetByName: aba };
}

function carregar(email) {
  const pl = planilhaFalsa();
  const ctx = {
    SpreadsheetApp: { getActive: () => pl, openById: () => pl },
    PropertiesService: { getScriptProperties: () => ({ getProperty: () => null }) },
    Session: { getActiveUser: () => ({ getEmail: () => email }), getScriptTimeZone: () => "America/Cuiaba" },
    Utilities: { formatDate: (d, tz, f) => f === "yyyy-MM-dd" ? "2026-10-29" : "", getUuid: () => Math.random().toString(36).slice(2) },
    LockService: { getScriptLock: () => ({ waitLock: () => {}, releaseLock: () => {} }) },
    HtmlService: {}
  };
  vm.createContext(ctx);
  vm.runInContext(fs.readFileSync(path.join(raiz, "Code.gs"), "utf8"), ctx);
  return { ctx, pl };
}

const resultados = [];
const ok = (nome, cond) => resultados.push([nome, !!cond]);
const falha = (fn) => { try { fn(); return null; } catch (e) { return e.message; } };
const grade = { de: "2026-11-16", ate: "2026-11-27", dias: [1, 2, 3, 4, 5], inicio: "08:00", fim: "16:00", intervalo: 30, vagas: 2 };

// servidor do posto P01
let { ctx, pl } = carregar("servidor.centro@politec.mt.gov.br");
ok("quemSou reconhece o posto P01", ctx.quemSou().posto_id === "P01");
const r1 = ctx.gerarHorarios("P01", grade);
ok("2 semanas úteis = 160 horários (a planilha modelo já tem os de 16/11)", r1.criados + r1.existentes === 160 && r1.existentes === 16);
ok("gerar de novo não duplica", ctx.gerarHorarios("P01", grade).criados === 0);
ok("bloquear o dia 16/11 afeta 16 horários", ctx.bloquear("P01", { data: "2026-11-16" }, true) === 16);
ok("dia bloqueado sai da lista pública", ctx.listarHorarios("P01").filter(h => h.data === "2026-11-16").length === 0);
ok("RN05: P01 não mexe em P02", /RN05/.test(falha(() => ctx.gerarHorarios("P02", grade))));
ok("posto não cadastra posto", /gestão/.test(falha(() => ctx.salvarPosto({ posto_id: "P09", nome: "x", municipio: "y" }))));
ok("cada ação vai para o log", pl.abas.log.length > 1);

// gestão
({ ctx, pl } = carregar("gestao.identificacao@politec.mt.gov.br"));
ctx.salvarPosto({ posto_id: "P03", nome: "Posto Teste", municipio: "Sinop", ativo: true });
ok("gestão cadastra posto novo", ctx.listarTodosPostos().length === 3);
ctx.salvarPosto({ posto_id: "P03", nome: "Posto Teste", municipio: "Sinop", ativo: false });
ok("posto inativo sai da lista pública (RN01)", ctx.listarPostos().length === 2 && ctx.listarTodosPostos().length === 3);

// cidadão (implantação pública: sem e-mail)
({ ctx } = carregar(""));
ok("cidadão vê os postos ativos", ctx.listarPostos().length === 2);
ok("cidadão não gera horários", /RN05/.test(falha(() => ctx.gerarHorarios("P01", grade))));

// Sprint 3: cidadão agenda (hoje simulado = 2026-10-29)
({ ctx, pl } = carregar(""));
const vagas = ctx.listarVagas("P01");
ok("vagas só dentro de 1 a 30 dias e com lugar", vagas.length > 0 && vagas.every(h => h.data >= "2026-10-30" && h.data <= "2026-11-28" && h.ocupadas < h.capacidade));
const r = ctx.reservar({ horario_id: vagas[0].horario_id, nome: "Ana Teste", telefone: "(65) 99999-0000", cpf: "52998224725" });
ok("reserva gera protocolo CIN-XXXXXX", /^CIN-[A-Z2-9]{6}$/.test(r.protocolo));
ok("a reserva aparece na aba agendamentos, com só 4 dígitos do CPF", pl.abas.agendamentos.some(l => l.includes(r.protocolo) && l.includes("4725") && !l.includes("52998224725")));
const comp = ctx.comprovante(r.protocolo);
ok("comprovante sem telefone e com os documentos do posto", comp.primeiro_nome === "Ana" && !JSON.stringify(comp).includes("99999") && !!comp.documentos);
const cheio = vagas.find(h => h.capacidade - h.ocupadas === 1 && h.horario_id !== vagas[0].horario_id) || vagas[0];
ctx.reservar({ horario_id: cheio.horario_id, nome: "B Teste" });
ok("horário lotado não aceita mais reserva", /preenchido|disponível/.test(falha(() => { ctx.reservar({ horario_id: cheio.horario_id, nome: "C Teste" }); ctx.reservar({ horario_id: cheio.horario_id, nome: "D Teste" }); })));

const falhas = resultados.filter(r => !r[1]);
resultados.forEach(([n, c]) => console.log((c ? "ok    " : "FALHA ") + n));
console.log(`${resultados.length - falhas.length}/${resultados.length}`);
process.exit(falhas.length ? 1 : 0);
