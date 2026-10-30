-- Esquema do banco de demandas do Hórus (Supabase/PostgreSQL)
--
-- Premissa assumida em 30/10/2026 (ver ../PREMISSAS.md). O DDL real do Hórus
-- não pôde ser copiado pelo grupo; a estrutura abaixo foi inferida do que o
-- app importa e do que a equipe descreveu. Serve para conferir nomes de campo,
-- chaves e tipos antes de ligar a versão offline ao sistema.

-- ---------------------------------------------------------------- organogram
create table if not exists public.orgao (
  id          uuid primary key default gen_random_uuid(),
  nome        text not null,
  criado_em   timestamptz not null default now()
);

create table if not exists public.diretoria (
  id          uuid primary key default gen_random_uuid(),
  orgao_id    uuid not null references public.orgao (id) on delete restrict,
  nome        text not null,
  sigla       text not null,
  criado_em   timestamptz not null default now()
);

create table if not exists public.unidade (
  id            uuid primary key default gen_random_uuid(),
  diretoria_id uuid not null references public.diretoria (id) on delete restrict,
  nome          text not null,
  sigla         text not null,
  criado_em     timestamptz not null default now()
);

create table if not exists public.unidade_medida (
  id          uuid primary key default gen_random_uuid(),
  sigla       text not null unique,
  nome        text not null,
  criado_em   timestamptz not null default now()
);

-- ------------------------------------------------------------------- ciclo
create table if not exists public.ciclo (
  id          uuid primary key default gen_random_uuid(),
  nome        text not null,
  ano         int  not null,
  status      text not null check (status in ('ATIVO', 'ENCERRADO')),
  criado_em   timestamptz not null default now()
);

-- ----------------------------------------------------------------- demandas
create table if not exists public.banco_demanda (
  id                    uuid primary key default gen_random_uuid(),
  ciclo_id              uuid not null references public.ciclo (id) on delete restrict,
  grupo                 text not null check (grupo in ('CUSTEIO', 'INVESTIMENTO')),
  unidade_id            uuid not null references public.unidade (id) on delete restrict,
  especificacao_tecnica text not null,
  quantidade            numeric(14,2) not null,
  unidade_medida_id     uuid not null references public.unidade_medida (id) on delete restrict,
  valor_estimado_c      bigint not null default 0,   -- em centavos
  situacao              text not null,
  criado_em             timestamptz not null default now()
);
create index on public.banco_demanda (ciclo_id);
create index on public.banco_demanda (unidade_id);

-- ----------------------------------------------------------- inclusões e manifestações
create table if not exists public.banco_demanda_inclusao (
  id              uuid primary key default gen_random_uuid(),
  banco_demanda_id uuid not null references public.banco_demanda (id) on delete cascade,
  quadro_id       uuid not null references public.ciclo (id) on delete restrict,
  demanda_id      uuid references public.banco_demanda (id) on delete set null,
  criado_em       timestamptz not null default now()
);
create index on public.banco_demanda_inclusao (banco_demanda_id);

create table if not exists public.banco_demanda_manifestacao (
  id              uuid primary key default gen_random_uuid(),
  banco_demanda_id uuid not null references public.banco_demanda (id) on delete cascade,
  unidade_id      uuid not null references public.unidade (id) on delete restrict,
  quantidade      numeric(14,2) not null,
  justificativa   text not null,
  criado_em       timestamptz not null default now()
);
create index on public.banco_demanda_manifestacao (banco_demanda_id);

-- ------------------------------------------------------- permissões do Hórus
-- A versão offline não reproduz as regras do RLS do Supabase. A decisão de
-- projeto (premissa de 30/10/2026) é servir às unidades que não têm acesso ao
-- Hórus; o registro volta para digitação no sistema oficial.
