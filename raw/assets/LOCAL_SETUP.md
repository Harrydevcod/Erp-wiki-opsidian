# Guia de Configuracao Local

Este projeto foi separado do fluxo do Lovable e passa a correr como uma app React + Supabase normal.

## Pre-requisitos

- Node.js 18+
- npm 9+
- Git

## Opcao 1: setup automatico

### Windows PowerShell

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\scripts\setup.ps1
```

### Windows CMD

```cmd
scripts\setup.bat
```

### Linux / macOS / WSL

```bash
chmod +x scripts/setup.sh
./scripts/setup.sh
```

### Cross-platform

```bash
node scripts/setup.cjs
```

## Opcao 2: setup manual

### Windows PowerShell

```powershell
Copy-Item .env.example .env
npm.cmd install
npm.cmd run dev
```

### Windows CMD

```cmd
copy .env.example .env
npm install
npm run dev
```

### Linux / macOS / WSL

```bash
cp .env.example .env
npm install
npm run dev
```

## Variaveis de ambiente

Para Supabase cloud, preencha no `.env`:

- `VITE_SUPABASE_URL`
- `VITE_SUPABASE_PUBLISHABLE_KEY`
- `VITE_SUPABASE_PROJECT_ID`

Para frontend cloud, prefere a `publishable key` (`sb_publishable_...`). `VITE_SUPABASE_ANON_KEY` continua aceite apenas como fallback de compatibilidade.

Para Supabase local via CLI, prefira `.env.local` a partir de `.env.local.example`:

- `VITE_SUPABASE_URL=http://127.0.0.1:54321`
- `VITE_SUPABASE_ANON_KEY=<anon-key-do-supabase-status>`
- `VITE_SUPABASE_PROJECT_ID=local`

O cliente aceita `VITE_SUPABASE_PUBLISHABLE_KEY` ou `VITE_SUPABASE_ANON_KEY`.

## Supabase local completo

Pre-requisitos adicionais:

- Docker Desktop
- Supabase CLI

### 1. iniciar o stack local

```powershell
supabase start
```

### 2. recriar a base local com migrations e seed

```powershell
supabase db reset
```

### 3. copiar as credenciais locais

```powershell
supabase status
```

Copie a `API URL` e a `anon key` para `.env.local`.

### 4. subir o frontend

```powershell
npm.cmd run dev
```

App local: `http://localhost:8080`

## Rede local

Se quiser abrir o frontend noutro dispositivo da mesma rede:

```powershell
npm.cmd run dev:host
```

## Notas importantes

- O backend continua a ser Supabase.
- As migrations estao em `supabase/migrations`.
- As edge functions estao em `supabase/functions`.
- O login Google agora usa Supabase diretamente, por isso as URLs de redirect devem estar corretas no painel do Supabase.
- Para OAuth local, adicione `http://localhost:8080` nas redirect URLs permitidas do projeto Supabase.
- Para este projeto, use o servidor do Vite. Live Server nao injeta `import.meta.env` nem lida bem com o fallback das rotas SPA.

## Comandos uteis

- `npm run dev`
- `npm run dev:host`
- `npm run build`
- `npm run preview`
- `npm run preview:host`
- `npm run lint`
- `npm run setup`
- `npm run supabase:start`
- `npm run supabase:status`
- `npm run supabase:db:reset`
- `npm run supabase:stop`

## PowerShell no Windows

Se `npm` falhar com erro de execution policy, use `npm.cmd`:

```powershell
npm.cmd install
npm.cmd run dev
npm.cmd run build
```
