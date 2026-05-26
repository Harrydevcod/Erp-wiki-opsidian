# Supabase Deploy

Este projeto ja tem o schema completo em `supabase/migrations`, funcoes em `supabase/functions` e seed em `supabase/seed.sql`.

## 1. Ligar o repositorio ao projeto novo

```powershell
supabase login
supabase link --project-ref <PROJECT_REF>
```

## 2. Subir schema, RLS, policies, triggers e storage

```powershell
supabase db push --include-seed
```

Se preferires nao carregar dados demo, usa:

```powershell
supabase db push
```

## 3. Configurar os webhooks SQL para o projeto novo

Algumas triggers do banco chamam Edge Functions via `pg_net`. A migration mais recente remove a dependencia do projeto antigo, mas precisas gravar a URL do projeto, a legacy `anon` key JWT e um segredo privado dedicado para estes webhooks. A `publishable key` nao funciona aqui porque a compatibilidade legacy das Edge Functions continua dependente das chaves JWT-based do Supabase para chamadas autenticadas normais.

```sql
select public.configure_edge_function_webhooks(
  'https://<PROJECT_REF>.supabase.co',
  '<SUPABASE_LEGACY_ANON_KEY>'
);

select public.configure_edge_function_webhook_secret(
  '<EDGE_FUNCTION_WEBHOOK_SECRET>'
);
```

Podes validar assim:

```sql
select * from public.get_edge_function_webhook_status();
```

## 4. Configurar secrets das Edge Functions

Cria um ficheiro local `.env.functions` a partir de `.env.functions.example` com os secrets necessarios. Exemplo:

```env
SUPABASE_URL=https://<PROJECT_REF>.supabase.co
SUPABASE_ANON_KEY=<SUPABASE_LEGACY_ANON_KEY>
SUPABASE_SERVICE_ROLE_KEY=<SUPABASE_SERVICE_ROLE_KEY>
RESEND_API_KEY=<RESEND_API_KEY>
ADMIN_EMAIL=<ADMIN_EMAIL>
APP_URL=<APP_URL>
CRON_SECRET=<CRON_SECRET>
EDGE_FUNCTION_WEBHOOK_SECRET=<EDGE_FUNCTION_WEBHOOK_SECRET>
AI_API_BASE_URL=https://openrouter.ai/api/v1
AI_API_KEY=<AI_API_KEY>
AI_CHAT_MODEL=google/gemini-2.5-flash
SISP_POS_ID=<SISP_POS_ID>
SISP_POS_AUT_CODE=<SISP_POS_AUT_CODE>
SISP_API_URL=<SISP_API_URL>
```

Depois sobe os secrets:

```powershell
supabase secrets set --env-file .env.functions
```

## 5. Deploy das Edge Functions

```powershell
supabase functions deploy
```

## 6. Variaveis do frontend

No frontend, configura:

```env
VITE_SUPABASE_URL=https://<PROJECT_REF>.supabase.co
VITE_SUPABASE_PUBLISHABLE_KEY=<SUPABASE_PUBLISHABLE_KEY>
VITE_SUPABASE_PROJECT_ID=<PROJECT_REF>
```

## Notas

- O schema remoto e aplicado na ordem dos timestamps das migrations.
- `supabase db push` cria e usa `supabase_migrations.schema_migrations` para controlar o historico remoto.
- As funcoes `notify-service-request`, `order-status-notification` e `notify-new-review` so vao disparar para o projeto certo depois da configuracao do passo 3.
- `EDGE_FUNCTION_WEBHOOK_SECRET` tem de ser o mesmo valor configurado no SQL Editor com `public.configure_edge_function_webhook_secret(...)` e nos secrets das Edge Functions.
- As funcoes `ai-chat`, `moderate-review` e `suggest-review-response` usam um provider OpenAI-compatible configurado por `AI_API_BASE_URL`, `AI_API_KEY` e `AI_CHAT_MODEL`. O exemplo acima assume OpenRouter.
- Para o frontend, prefere `sb_publishable_...`. A `anon` key JWT antiga continua necessaria apenas para compatibilidade com alguns fluxos de Edge Functions e para fallback legacy enquanto o segredo privado dos webhooks nao estiver configurado.
- Se o projeto Supabase novo ja tiver tabelas criadas manualmente fora das migrations deste repo, `supabase db push` nao vai limpar esse lixo. Nesse caso, para isolamento real entre Lovable e Codex, o melhor e recriar um projeto vazio e repetir o processo.
