# 🚀 NOVA-ERP — PRD Técnico Faseado (Correção Supabase + Multi-Tenant + Data Layer)

---

## 1. 🧠 DIAGNÓSTICO TÉCNICO

### Problemas identificados
- Queries inválidas no Supabase (comparação entre colunas)
- Sintaxe incorreta de filtros OR
- tenant_id hardcoded (quebra multi-tenant)
- loops de chamadas no frontend

### Impacto
- erros 400 constantes
- dashboard instável
- risco fiscal
- não escalável

---

## 2. 🏗️ ARQUITETURA TARGET

React → Data Layer → Supabase → PostgreSQL

Princípios:
- lógica no DB
- frontend simples
- isolamento por tenant
- performance

---

## 3. ⚙️ PLANO DE EXECUÇÃO

### Fase 1 — Stock
Criar view:
```sql
create view low_stock_products as
select id, name, stock, minimum_stock, tenant_id
from products
where controls_stock = true
  and stock > 0
  and minimum_stock is not null
  and stock <= minimum_stock;
```

### Fase 2 — Documentos
```sql
create view pending_efatura_documents as
select *
from documents
where status = 'issued'
  and (
    efatura_status is null
    or efatura_status in ('pending','error')
  );
```

### Fase 3 — Multi-tenant
- remover tenant fixo
- usar tenant dinâmico do contexto

### Fase 4 — Data Layer
Criar services centralizados

---

## 4. 📦 MIGRAÇÕES SQL

```sql
create index idx_products_tenant on products(tenant_id);
create index idx_documents_tenant on documents(tenant_id);
```

---

## 5. ✅ CHECKLIST

- sem erros 400
- tenant dinâmico
- queries válidas
- dashboard funcional

---

## 6. 🎯 CRITÉRIOS DE ACEITE

### Inventário
- stock correto
- rápido

### Faturação
- documentos corretos
- estados válidos

### Multi-tenant
- isolamento total

---

## 7. 🚀 RESULTADO

- sistema estável
- pronto para escalar
- base sólida ERP
