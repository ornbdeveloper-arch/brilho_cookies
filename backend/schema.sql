create extension if not exists pgcrypto;

create table if not exists public.cookies (
  id uuid primary key default gen_random_uuid(),
  name text not null,
  flavor text not null default '',
  price numeric(10, 2) not null default 0,
  stock integer not null default 0,
  ingredients jsonb not null default '[]'::jsonb,
  created_at timestamptz not null default now()
);

create table if not exists public.customers (
  id uuid primary key default gen_random_uuid(),
  name text not null,
  cpf text not null unique,
  contact text not null default '',
  created_at timestamptz not null default now()
);

create table if not exists public.sales (
  id uuid primary key default gen_random_uuid(),
  customer_id uuid references public.customers(id) on delete set null,
  customer_name text not null,
  customer_cpf text not null,
  items jsonb not null default '[]'::jsonb,
  total numeric(10, 2) not null default 0,
  payment_method text not null default 'pix',
  payment_status text not null default 'pending',
  pay_later boolean not null default false,
  notes text not null default '',
  created_at timestamptz not null default now(),
  paid_at timestamptz
);

alter table public.cookies enable row level security;
alter table public.customers enable row level security;
alter table public.sales enable row level security;

create policy "Backend can manage cookies"
on public.cookies
for all
using (true)
with check (true);

create policy "Backend can manage customers"
on public.customers
for all
using (true)
with check (true);

create policy "Backend can manage sales"
on public.sales
for all
using (true)
with check (true);
