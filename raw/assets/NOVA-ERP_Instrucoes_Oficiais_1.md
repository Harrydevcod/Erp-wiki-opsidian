# 🚀 NOVA-ERP — INSTRUÇÕES OFICIAIS DO PROJETO

> Sistema ERP Multi-Tenant SaaS — Nativo de Cabo Verde  
> Nível enterprise: SAP / Odoo / Primavera

---

## 🎯 1. IDENTIDADE DO PROJETO

O **NOVA-ERP** é um sistema ERP moderno, **multi-tenant SaaS**, construído nativamente para Cabo Verde.

**Stack obrigatória:**

| Camada | Tecnologia |
|---|---|
| Frontend | React + Vite + TypeScript + Tailwind CSS |
| Backend | Node.js |
| Base de Dados | Supabase (PostgreSQL) |
| Estilo Visual | Dark Premium — Azul + Laranja |
| Referência Visual | Primavera EVO / Odoo / SAP |

**Objetivo:** Nível enterprise (SAP / Odoo / Primavera), não MVP simples.

---

## 🧠 2. PRINCÍPIOS IMUTÁVEIS

### 2.1 Fiscalidade FIRST (Regra nº 1)

Toda a lógica do sistema respeita obrigatoriamente:

- Código do IVA — Lei nº 21/VI/2003
- Faturação eletrónica DNRE / e-Fatura
- SAF-T CV
- Modelo 106

> ⚠️ **CRÍTICO: Nenhuma funcionalidade pode violar regras fiscais. Sem exceções.**

### 2.2 Multi-Tenant Obrigatório

- Cada empresa = 1 tenant completamente isolado
- Dados nunca se misturam entre tenants
- Suporte a subscrições SaaS, planos e módulos por cliente
- Arquitetura preparada para escala massiva

### 2.3 Modularidade

Cada módulo é independente mas totalmente integrado com os restantes.

---

## 🔌 3. INTEGRAÇÃO COM E-FATURA — MIDDLEWARE (CRÍTICO)

### 3.1 Arquitetura Obrigatória

```
NOVA-ERP  →  Middleware (e-Fatura CV)  →  DNRE / Plataforma Eletrónica
```

> ❗ **Não existe API direta ao e-Fatura. A comunicação é sempre via Middleware oficial da DNRE.**

---

### 3.2 Configuração Dinâmica da URL do Middleware

O sistema deve ter uma **configuração dinâmica e persistente** da URL base do Middleware, por tenant.  
**A URL nunca é hardcoded no código.**

#### Ambientes suportados

| Ambiente | URL Padrão |
|---|---|
| Desenvolvimento (localhost) | `https://localhost:3443` |
| Produção (VPS / Domínio) | Configurável — ex: `https://mw.novaerp.cv:3443` |

#### Requisitos de Implementação

**1. Tabela de configuração no Supabase — campo `middleware_url` por tenant:**

```sql
-- Em tabela settings ou system_config, isolado por tenant_id
middleware_url TEXT DEFAULT 'https://localhost:3443'
```

**2. Painel de configuração no ERP — secção `Configurações > Integração e-Fatura`:**

- Campo editável para a URL do Middleware
- Botão **Testar Ligação** — faz `GET /v1/core/index` e mostra status em tempo real
- Indicador visual: 🟢 Online / 🔴 Offline / 🟡 Não configurado
- Configuração guardada por tenant (isolamento total)

**3. Serviço centralizado no frontend/backend — nunca hardcodar a URL:**

```typescript
// Correto — nunca usar URL fixa
const MIDDLEWARE_URL = await getMiddlewareUrl(tenantId)
// Usa o valor guardado no Supabase para esse tenant
```

**4. Headers obrigatórios em todas as chamadas ao Middleware:**

```http
cv-ef-mw-core-transmitter-key: {transmitter_key}
Content-Type: application/json
```

**5. Suporte a certificado SSL self-signed do Middleware**  
(comportamento esperado pelo Middleware oficial da DNRE — não é erro de configuração)

**6. Modo contingência — quando o Middleware está offline:**

- Bloqueia envio de documentos ao e-Fatura
- Guarda documentos em fila de espera local
- Reenvio automático quando a ligação for restaurada

---

### 3.3 Recursos do Middleware Utilizados

| Recurso | Endpoint | Uso |
|---|---|---|
| Chave do transmissor | `GET /v1/core/transmitter-key` | Autenticação |
| Envio de faturas (LED) | `POST /v1/led/...` | Emissão DFE |
| Validação NIF | `GET /v1/nif/...` | Validar contribuintes |
| Estado da rede | `GET /v1/core/network/status` | Health check |
| Auth OAuth | `GET /v1/core/auth` | Token utilizador |

---

## 📦 4. MÓDULOS DO SISTEMA

### 4.1 Entidades Base

- **Clientes / Fornecedores / Terceiros** — NIF obrigatório, suporte a cliente indiferenciado (VD), segmentação empresa/particular/estado
- **Artigos** — Produtos, Serviços, Ativos; Famílias/Subfamílias, IVA por artigo, stock

### 4.2 Módulos Operacionais

| Módulo | Funcionalidades Principais |
|---|---|
| **Vendas** | Encomenda → Guia → Fatura → Pagamento |
| **Compras** | Encomenda → Receção → Fatura Fornecedor |
| **Inventário** | Stock, movimentos, transferências, lotes/séries |
| **Tesouraria** | Contas correntes, pagamentos, recebimentos, reconciliação bancária |
| **Contabilidade** | Plano de contas SNCRF, diários, apuramento IVA |
| **Fiscalidade** | Modelo 106, SAF-T, e-Fatura |
| **RH** | Funcionários, salários, INPS, férias/faltas |
| **Ativos** | Imobilizado, depreciações, reavaliações |
| **Projetos** | Gestão de projetos ligados a vendas/custos |

---

## 🧾 5. REGRAS FISCAIS CRÍTICAS

### 5.1 Documentos Obrigatórios

| Código | Descrição |
|---|---|
| `FT` | Fatura |
| `FR` | Fatura-Recibo |
| `NC` | Nota de Crédito |
| `ND` | Nota de Débito |
| `GT` | Guia de Transporte |

### 5.2 Elementos Obrigatórios em Cada Documento

- NIF e Nome do cliente
- Data de emissão
- Série e número sequencial
- Descrição detalhada de cada linha
- Taxa e valor de IVA
- QR Code
- IUD (hash fiscal do documento)

### 5.3 Regras Invioláveis

> ⚠️ **NUNCA apagar documentos — usar sempre anulação.**  
> Notas de Crédito referenciam obrigatoriamente a fatura original.  
> Numeração sequencial garantida sem gaps.  
> Prazo de emissão: até 5 dias úteis.

---

## 🧮 6. REGIMES FISCAIS

| Regime | IVA | Declaração | Observações |
|---|---|---|---|
| **Regime Normal** | 15% | Modelo 106 | Declaração mensal/trimestral |
| **REMPE** | Isento | TEU 4% | Lei nº 70/VIII/2014 + Lei nº 5/IX/2016 |

O sistema **adapta automaticamente** os cálculos ao regime fiscal do tenant.  
Mudanças de regime fora do período permitido são bloqueadas.

---

## 📊 7. SAF-T CV

O sistema gera os três tipos obrigatórios:

- SAF-T Faturação
- SAF-T Contabilidade
- SAF-T Inventário

**Requisitos técnicos:**

- Estrutura XML oficial da DNRE
- Dados completos por período fiscal
- Performance preparada para milhões de registos

---

## 🔐 8. SEGURANÇA E AUDITORIA

- Logs de todas as operações (por tenant, por utilizador)
- Histórico completo de alterações
- Hash fiscal dos documentos (IUD)
- Modo "bloqueio fiscal" por período
- Isolamento total de dados entre tenants

---

## 🤖 9. IA NO ERP (IMPLEMENTAÇÃO FASEADA)

| Fase | Funcionalidade |
|---|---|
| **Fase 1** | Validação automática SAF-T + deteção de erros fiscais |
| **Fase 2** | Sugestão automática de lançamentos contabilísticos |
| **Fase 3** | Previsão fiscal + assistente financeiro inteligente |
| **Fase 4** | Automação de processos completos (compras, vendas, reconciliação) |

---

## ⚙️ 10. REGRAS TÉCNICAS IMUTÁVEIS

1. **NUNCA** hardcodar a URL do Middleware — sempre via configuração por tenant
2. **NUNCA** assumir lógica fiscal sem validar a legislação no projeto
3. **NUNCA** permitir inconsistências contabilísticas
4. **TODOS** os módulos integram automaticamente entre si
5. **PERFORMANCE** preparada para milhões de registos desde o início
6. **ARQUITETURA** multi-tenant desde a primeira linha de código

---

## 🎨 11. UX/UI

- Estilo: **dark premium**, azul + laranja
- Referências visuais: Primavera EVO / Odoo / SAP
- Foco em produtividade e velocidade
- Automação máxima de campos e fluxos
- Interface responsiva (web + tablet)

---

## 🧩 FILOSOFIA

> *"O NOVA-ERP não é apenas um ERP — é um sistema fiscal inteligente, nativo de Cabo Verde, construído para escalar."*
