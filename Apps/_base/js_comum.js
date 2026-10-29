/* ---------- comum a todos os apps (Sprint 1) ---------- */
TELAS["#/config"] = async ()=> `<h1>Configuração</h1><p class="sub">Backup, dados de exemplo e perfil desta cópia.</p>` +
  (typeof configExtra === "function" ? await configExtra() : "") + await blocoConfigComum();
TELAS_DEPOIS["#/config"] = async ()=>{ ligarConfigComum(); if (typeof ligarConfigExtra === "function") await ligarConfigExtra(); };
async function resumoBase(stores){
  const linhas = [];
  for (const s of stores) linhas.push(`<div class="card kpi"><div class="v">${(await db.list(s)).length}</div><div class="r">${esc(s)}</div></div>`);
  return `<div class="grade">${linhas.join("")}</div>`;
}
teste("IndexedDB grava e lê", async ()=>{ await db.meta("teste", 42); return (await db.meta("teste")) === 42; });
teste("Todas as rotas têm título e sprint", ()=> APP.rotas.every(r=>r.titulo && r.sprint !== undefined));
teste("lerCSV: ponto e vírgula, aspas e BOM", ()=>{ const r = lerCSV('﻿a;b\n"x;1";2\n'); return r.length === 2 && r[1][0] === "x;1" && r[1][1] === "2"; });
teste("cnpjValido e cpfValido", ()=> cnpjValido("11.222.333/0001-81") && !cnpjValido("11222333000182") && cpfValido("529.982.247-25") && !cpfValido("52998224726"));
teste("dataDeTexto('29/10/2026 09:05:00')", ()=> dataDeTexto("29/10/2026 09:05:00") === "2026-10-29T09:05:00");
