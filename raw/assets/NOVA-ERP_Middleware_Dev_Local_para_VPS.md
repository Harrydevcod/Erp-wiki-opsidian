# 🔄 NOVA-ERP — Middleware e-Fatura: Dev Local → VPS Produção

## O middleware é o MESMO software em todo o lado

O `mwcore-efatura` da DNRE é um executável idêntico quer corra no teu portátil, num PC de escritório ou num VPS na cloud. A única diferença é o ficheiro `application.properties` que lhe diz:
- Quem é o transmissor (software house = NOVAERP)
- Quais os emitentes (NIFs das empresas/tenants)
- Modo: produção ou teste

Portanto: **desenvolves e testas localmente, e quando estiver pronto, copias a mesma configuração para o VPS.**

---

## Os 3 ambientes

```
┌─────────────────────────────────────────────────────────────────┐
│                                                                 │
│  1. DEV LOCAL (o teu PC)                                        │
│  ────────────────────────                                       │
│  NOVA-ERP: http://localhost:5173 (Vite dev server)              │
│  Supabase: local (npx supabase start) ou cloud dev project      │
│  Middleware: https://localhost:3443 (mwcore-efatura local)       │
│  Edge Function → chama https://localhost:3443                   │
│                                                                 │
│  application.properties:                                        │
│    transmitter.tax-id = {teu NIF de teste}                      │
│    emitter.groups.tax-id = NIF_TESTE_1:NIF_TESTE_2              │
│    → Pode apontar para ambiente TESTE da DNRE                   │
│                                                                 │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  2. STAGING / TESTES (VPS pequeno ou o teu PC com Docker)       │
│  ─────────────────────────────────────────────────────          │
│  NOVA-ERP: https://staging.novaerp.cv                           │
│  Supabase: projecto staging                                     │
│  Middleware: https://staging-mw.novaerp.cv:3443                 │
│  Edge Function → chama staging-mw.novaerp.cv:3443              │
│                                                                 │
│  application.properties:                                        │
│    → Mesmos NIFs de teste                                       │
│    → Ambiente TESTE da DNRE (saft.tst.efatura.cv)               │
│                                                                 │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  3. PRODUÇÃO (VPS dedicado)                                     │
│  ──────────────────────────                                     │
│  NOVA-ERP: https://app.novaerp.cv                               │
│  Supabase: projecto produção                                    │
│  Middleware: https://mw.novaerp.cv:3443 (rede privada VPC)      │
│  Edge Function → chama mw.novaerp.cv:3443 via VPC              │
│                                                                 │
│  application.properties:                                        │
│    transmitter.tax-id = {NIF real da NOVA-ERP}                  │
│    emitter.groups.tax-id = NIF_TENANT_1:NIF_TENANT_2:...:NIF_N │
│    → Ambiente PRODUÇÃO da DNRE (services.efatura.cv)            │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## Configuração por ambiente (uma variável de ambiente)

O NOVA-ERP só precisa de **1 variável** para saber onde está o middleware:

```env
# .env.local (dev)
MIDDLEWARE_URL=https://localhost:3443

# .env.staging
MIDDLEWARE_URL=https://staging-mw.novaerp.cv:3443

# .env.production
MIDDLEWARE_URL=https://mw.novaerp.cv:3443
```

A Edge Function lê esta variável e faz o POST para lá. O código é idêntico nos 3 ambientes.

---

## Setup dev local (passo a passo)

### 1. Instalar o middleware no teu PC

```bash
# Windows
curl -o mwcore-efatura.zip https://update.efatura.cv/win/mwcore-efatura.zip
# Extrair para C:\mwcore-efatura\

# Linux
curl -o mwcore-efatura.zip https://update.efatura.cv/linux/mwcore-efatura.zip
sudo unzip mwcore-efatura.zip -d /mwcore-efatura/

# macOS
curl -o mwcore-efatura.zip https://update.efatura.cv/mac/mwcore-efatura.zip
unzip mwcore-efatura.zip -d /mwcore-efatura/
```

### 2. Configurar application.properties para dev

```properties
# C:\mwcore-efatura\win\config\application.properties

# --- TRANSMITTER (tu, a software house NOVA-ERP) ---
%prod.transmitter.tax-id=XXXXXXXXX
%prod.transmitter.name=NOVA-ERP DEV
%prod.transmitter.client-id=cv-ef-cli-novaerp-${transmitter.tax-id}
%prod.transmitter.client-secret=SEU_CLIENT_SECRET_AQUI

# --- EMITTERS (empresas de teste) ---
# Um NIF de teste para começar (o teu NIF pessoal ou de uma empresa de teste)
%prod.emitter.repository=1
%prod.emitter.allowed.scopes=openid+offline_access+cv_ef_led_all+cv_ef_dfe_all+cv_ef_tp_all+cv_ef_event_all
%prod.emitter.groups.tax-id=NIF_TESTE
%prod.emitter.groups.name=EMPRESA TESTE DEV
%prod.emitter.groups.client-secret=CLIENT_SECRET_TESTE

# Para adicionar mais empresas de teste depois:
# %prod.emitter.groups.tax-id=NIF1:NIF2:NIF3
# %prod.emitter.groups.name=Emp1:Emp2:Emp3
# %prod.emitter.groups.client-secret=sec1:sec2:sec3
```

### 3. Iniciar o middleware

```bash
# Windows — instalar como serviço
cd C:\mwcore-efatura\win
install-service.bat
# Ou executar directamente:
start-mwcore.bat

# Linux
cd /mwcore-efatura/linux
sudo ./install-service.sh
# Ou:
./start-mwcore.sh
```

Depois: aceder a `https://localhost:3443` no browser → se vir o painel do middleware, está a funcionar.

### 4. Edge Function aponta para localhost

```typescript
// supabase/functions/submit-dfe/index.ts

const MIDDLEWARE_URL = Deno.env.get('MIDDLEWARE_URL') || 'https://localhost:3443';

// Para dev local, o Edge Function corre via `supabase functions serve`
// e consegue aceder a localhost:3443 porque está no mesmo PC

Deno.serve(async (req) => {
  // ... validar JWT, gerar XML, empacotar ZIP ...
  
  const response = await fetch(`${MIDDLEWARE_URL}/v1/dfes`, {
    method: 'POST',
    body: zipBlob,
    headers: { 'Content-Type': 'application/zip' },
  });
  
  // ... processar resposta ...
});
```

### 5. Testar

```bash
# Terminal 1: middleware DNRE
cd C:\mwcore-efatura\win && start-mwcore.bat

# Terminal 2: Supabase local
npx supabase start
npx supabase functions serve submit-dfe --env-file .env.local

# Terminal 3: NOVA-ERP frontend
npm run dev
```

Agora podes emitir documentos no NOVA-ERP local → Edge Function → middleware local → DNRE (teste ou produção conforme a config).

---

## Migração para VPS (quando estiver pronto)

### O que copias:

```bash
# No VPS (Ubuntu 22.04+ recomendado)
ssh user@vps.novaerp.cv

# 1. Instalar middleware
curl -o mwcore-efatura.zip https://update.efatura.cv/linux/mwcore-efatura.zip
sudo unzip mwcore-efatura.zip -d /mwcore-efatura/

# 2. Copiar application.properties (com NIFs de TODOS os tenants)
sudo nano /mwcore-efatura/linux/config/application.properties
# → Colar a configuração de produção com todos os NIFs

# 3. Importar certificados digitais de cada tenant para o keystore
# (cada tenant faz upload do .pfx durante o onboarding no NOVA-ERP)
keytool -importkeystore \
  -srckeystore tenant_cert.pfx \
  -srcstoretype PKCS12 \
  -destkeystore /mwcore-efatura/linux/config/keystore.jks \
  -deststoretype JKS \
  -alias tenant_NIF_123456789

# 4. Instalar como serviço
cd /mwcore-efatura/linux
sudo ./install-service.sh

# 5. Configurar firewall — middleware acessível APENAS via rede privada
sudo ufw allow from 10.0.0.0/8 to any port 3443  # rede interna VPC
sudo ufw deny 3443                                 # bloquear acesso público
```

### O que mudas no Supabase:

```bash
# Apenas 1 variável de ambiente
supabase secrets set MIDDLEWARE_URL=https://mw.novaerp.cv:3443
```

**Pronto. O código do NOVA-ERP não muda nada. Zero alterações.**

---

## Como adicionar novos tenants em produção

Quando um novo cliente completa o onboarding:

```
1. Cliente preenche wizard no NOVA-ERP (NIF, credenciais, upload certificado)
                    ↓
2. Edge Function "admin-add-tenant-to-middleware":
   a) Lê application.properties actual do VPS (via SSH/API)
   b) Adiciona NIF ao emitter.groups.tax-id (append :NIF_NOVO)
   c) Adiciona nome ao emitter.groups.name (append :NOME_NOVO)
   d) Adiciona secret ao emitter.groups.client-secret (append :SECRET_NOVO)
   e) Importa certificado digital para o keystore
   f) Escreve application.properties actualizado
   g) Reinicia serviço middleware (systemctl restart mwcore-efatura)
                    ↓
3. Middleware reinicia em ~5 segundos com o novo tenant disponível
                    ↓
4. Cliente pode emitir DFEs imediatamente
```

Em dev local: fazes o mesmo manualmente no teu application.properties e reinicias o middleware. Simples.

---

## Gestão do middleware VPS (admin)

### Script de sync automático

```bash
#!/bin/bash
# sync-middleware-config.sh
# Executado pela Edge Function admin ou por cron job

# Buscar todos os tenants activos do Supabase
TENANTS=$(curl -s https://your-project.supabase.co/rest/v1/tenant_efatura_config \
  -H "apikey: SERVICE_KEY" \
  -H "Authorization: Bearer SERVICE_KEY" \
  | jq -r '[.[].nif] | join(":")')

NAMES=$(curl -s https://your-project.supabase.co/rest/v1/tenant_efatura_config \
  -H "apikey: SERVICE_KEY" \
  -H "Authorization: Bearer SERVICE_KEY" \
  | jq -r '[.[].razao_social] | join(":")')

SECRETS=$(curl -s https://your-project.supabase.co/rest/v1/tenant_efatura_config \
  -H "apikey: SERVICE_KEY" \
  -H "Authorization: Bearer SERVICE_KEY" \
  | jq -r '[.[].client_secret_decrypted] | join(":")')

# Actualizar application.properties
sed -i "s|^%prod.emitter.groups.tax-id=.*|%prod.emitter.groups.tax-id=$TENANTS|" \
  /mwcore-efatura/linux/config/application.properties

sed -i "s|^%prod.emitter.groups.name=.*|%prod.emitter.groups.name=$NAMES|" \
  /mwcore-efatura/linux/config/application.properties

sed -i "s|^%prod.emitter.groups.client-secret=.*|%prod.emitter.groups.client-secret=$SECRETS|" \
  /mwcore-efatura/linux/config/application.properties

# Reiniciar
sudo systemctl restart mwcore-efatura

echo "Middleware actualizado com $(echo $TENANTS | tr ':' '\n' | wc -l) tenants"
```

### Monitorização

```bash
# Health check do middleware
curl -k https://localhost:3443/health

# Logs
journalctl -u mwcore-efatura -f

# Ver quantos tenants configurados
grep "emitter.groups.tax-id" /mwcore-efatura/linux/config/application.properties \
  | tr ':' '\n' | wc -l
```

---

## Prompt Lovable — Edge Function com MIDDLEWARE_URL configurável

```
Cria a Edge Function principal de submissão de DFEs do NOVA-ERP que funciona 
tanto com middleware local (dev) como com VPS (produção):

SUPABASE EDGE FUNCTION "submit-dfe":

import { serve } from "https://deno.land/std@0.168.0/http/server.ts"
import { createClient } from "https://esm.sh/@supabase/supabase-js@2"

// A ÚNICA diferença entre dev e produção é esta variável:
// Dev local: MIDDLEWARE_URL=https://localhost:3443
// Produção:  MIDDLEWARE_URL=https://mw.novaerp.cv:3443
const MIDDLEWARE_URL = Deno.env.get('MIDDLEWARE_URL') ?? 'https://localhost:3443'

serve(async (req) => {
  // 1. Autenticar — extrair tenant_id do JWT
  const authHeader = req.headers.get('Authorization')
  const supabase = createClient(
    Deno.env.get('SUPABASE_URL')!,
    Deno.env.get('SUPABASE_ANON_KEY')!,
    { global: { headers: { Authorization: authHeader! } } }
  )
  
  const { data: { user } } = await supabase.auth.getUser()
  if (!user) return new Response('Unauthorized', { status: 401 })
  
  const tenant_id = user.app_metadata.tenant_id
  
  // 2. Receber document_id do body
  const { document_id } = await req.json()
  
  // 3. Buscar documento completo + config do tenant (tudo server-side, seguro)
  const { data: doc } = await supabase
    .from('documents')
    .select('*, document_lines(*), tenant:tenants(*)')
    .eq('id', document_id)
    .eq('tenant_id', tenant_id)
    .single()
  
  if (!doc) return new Response('Document not found', { status: 404 })
  
  // 4. Gerar XML do DFE (função importada)
  const xml = generateDfeXml(doc)
  
  // 5. Gerar IUD
  const iud = generateIUD({
    repositorio: '1',
    data: new Date(doc.data_emissao),
    nif: doc.tenant.nif,
    ledCode: doc.series.led_code,
    documentTypeCode: doc.document_type_code,
    documentNumber: doc.document_number,
  })
  
  // 6. Empacotar em ZIP
  const zip = await packageToZip([{ filename: `${iud}.xml`, content: xml }])
  
  // 7. POST para middleware (mesmo código para dev e produção!)
  try {
    const mwResponse = await fetch(`${MIDDLEWARE_URL}/v1/dfes`, {
      method: 'POST',
      body: zip,
      headers: { 'Content-Type': 'application/zip' },
    })
    
    const mwResult = await mwResponse.json()
    
    // 8. Guardar resultado
    await supabase.from('efatura_submissions').insert({
      tenant_id,
      document_id,
      iud,
      submission_type: 'NORMAL',
      status: mwResponse.ok ? 'AUTORIZADO' : 'REJEITADO',
      request_payload: { iud, xml_hash: sha256(xml) },
      response_payload: mwResult,
      error_message: mwResponse.ok ? null : mwResult.error,
    })
    
    // 9. Actualizar documento
    await supabase.from('documents').update({
      iud,
      status: mwResponse.ok ? 'AUTORIZADO' : 'REJEITADO',
      efatura_status: mwResult,
    }).eq('id', document_id)
    
    return new Response(JSON.stringify({
      success: mwResponse.ok,
      iud,
      status: mwResponse.ok ? 'AUTORIZADO' : 'REJEITADO',
      details: mwResult,
    }), { headers: { 'Content-Type': 'application/json' } })
    
  } catch (error) {
    // Middleware indisponível → contingência
    await supabase.from('documents').update({
      status: 'EMITIDO_CONTINGENCIA',
      contingencia: true,
    }).eq('id', document_id)
    
    await supabase.from('contingency_queue').insert({
      tenant_id,
      document_id,
      xml_content: xml,
      iud,
      status: 'PENDENTE',
    })
    
    return new Response(JSON.stringify({
      success: false,
      contingency: true,
      message: 'Middleware indisponível. Documento emitido em contingência.',
    }), { status: 503, headers: { 'Content-Type': 'application/json' } })
  }
})

VARIÁVEIS DE AMBIENTE SUPABASE:
# Dev (supabase functions serve --env-file .env.local)
MIDDLEWARE_URL=https://localhost:3443

# Produção (supabase secrets set)
MIDDLEWARE_URL=https://mw.novaerp.cv:3443

TESTES:
- Teste 1: Middleware local online → submissão normal → AUTORIZADO
- Teste 2: Middleware local online → DFE com erro → REJEITADO (ex: NIF inválido)
- Teste 3: Middleware desligado → contingência automática
- Teste 4: Middleware volta online → job de contingência reenvia documentos pendentes

SUPABASE CRON JOB "retry-contingency" (a cada 5 minutos):
- SELECT * FROM contingency_queue WHERE status = 'PENDENTE' ORDER BY created_at ASC LIMIT 10
- Para cada: tentar POST para MIDDLEWARE_URL/v1/dfes
- Se sucesso: actualizar queue status → COMUNICADO, document status → AUTORIZADO
- Se falha: incrementar retry_count, actualizar next_retry_at
- Se retry_count > 20: status → FALHA_PERMANENTE, alerta ao tenant
```

---

## Resumo da progressão

```
FASE DEV (agora):
  Teu PC → middleware local (porta 3443) → ambiente teste DNRE
  Custo: 0€
  Tenants: 1-2 de teste

      ↓ quando o MVP estiver funcional

FASE STAGING (beta com clientes reais):
  VPS pequeno (5-10€/mês) → middleware + ambiente teste DNRE
  Custo: ~10€/mês
  Tenants: 5-10 beta testers

      ↓ quando estiver validado com clientes reais

FASE PRODUÇÃO:
  VPS dedicado (20-50€/mês) → middleware + ambiente produção DNRE
  Custo: ~50€/mês
  Tenants: 50-500+
  
      ↓ quando escalar

FASE ESCALA:
  Múltiplos VPS com load balancer (se necessário)
  Ou: um VPS mais potente (o middleware é leve)
  Custo: ~100-200€/mês
  Tenants: 1000+
```

O CÓDIGO DO NOVA-ERP NUNCA MUDA entre estas fases. Só a variável MIDDLEWARE_URL.
