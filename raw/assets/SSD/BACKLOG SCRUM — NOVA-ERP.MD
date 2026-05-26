BACKLOG SCRUM — NOVA-ERP
Estrutura: Épico → Feature → User Story
Convenção:
EP = Épico
FE = Feature
US = User Story
🔵 EP-01 — Plataforma Base Multi-Tenant
🟢 FE-01 — Gestão de Tenants
US-01.01
Criar empresa (tenant)
Critérios:
gera tenant_id
cria admin inicial
estado setup_pending
auditoria criada
US-01.02
Concluir onboarding
Critérios:
valida séries, impostos e utilizador
ativa tenant (active)
🟢 FE-02 — Utilizadores
US-01.03
Convidar utilizador
Critérios:
convite por email
vinculado a tenant
estado pendente → ativo
US-01.04
Alternar entre empresas
Critérios:
troca de contexto sem login
isolamento total de dados
🟢 FE-03 — Permissões
US-01.05
Criar perfil
Critérios:
permissões CRUD + aprovar + exportar
US-01.06
Bloquear acesso não autorizado
Critérios:
UI + API validam permissões
🟢 FE-04 — Auditoria
US-01.07
Registar logs
Critérios:
actor, ação, entidade, timestamp
before/after em alterações críticas
🟠 EP-02 — Entidades
🟢 FE-05 — Clientes e Fornecedores
US-02.01
Criar cliente
US-02.02
Criar fornecedor
US-02.03
Criar cliente/fornecedor combinado
🟢 FE-06 — Cliente Indiferenciado
US-02.04
Emitir para VD
Critérios:
entidade padrão
opcional nome/NIF manual
🟢 FE-07 — Proteção de dados fiscais
US-02.05
Bloquear alteração de NIF
Critérios:
após documento certificado
🟡 EP-03 — Produtos e Serviços
🟢 FE-08 — Cadastro de artigos
US-03.01
Criar artigo stockável
US-03.02
Criar serviço
🟢 FE-09 — Unidades
US-03.03
Definir múltiplas unidades
Critérios:
fator de conversão
🟢 FE-10 — Lotes e Séries
US-03.04
Controlar lote
US-03.05
Controlar série
🔴 EP-04 — Vendas (CRÍTICO)
🟢 FE-11 — Emissão
US-04.01
Emitir FT
US-04.02
Emitir FR
US-04.03
Emitir TV
🟢 FE-12 — Documentos Retificativos
US-04.04
Emitir NC
US-04.05
Emitir ND
🟢 FE-13 — Imutabilidade
US-04.06
Bloquear edição após certificação
🟢 FE-14 — Workflow
US-04.07
Orçamento → Fatura
🟠 EP-05 — Compras
🟢 FE-15 — Documentos
US-05.01
Registar fatura fornecedor
US-05.02
Registar serviço
🟢 FE-16 — Receção
US-05.03
Receber mercadoria
Critérios:
atualiza stock
🟡 EP-06 — Inventário
🟢 FE-17 — Movimentos
US-06.01
Entrada de stock
US-06.02
Saída de stock
🟢 FE-18 — Transferências
US-06.03
Transferir entre armazéns
🟢 FE-19 — Inventário físico
US-06.04
Ajustar inventário
🟣 EP-07 — Tesouraria
🟢 FE-20 — Pendentes
US-07.01
Gerar pendente automático
🟢 FE-21 — Liquidações
US-07.02
Liquidação total
US-07.03
Liquidação parcial
🟢 FE-22 — Crédito
US-07.04
Definir limite de crédito
🟢 FE-23 — Reconciliação
US-07.05
Reconciliação manual
US-07.06
Reconciliação automática
🔵 EP-08 — Contabilidade
🟢 FE-24 — Plano de contas
US-08.01
Criar conta
🟢 FE-25 — Lançamentos
US-08.02
Lançamento manual
🟢 FE-26 — Integração
US-08.03
Integrar vendas
🟢 FE-27 — Bloqueios
US-08.04
Bloquear período
🟠 EP-09 — Fiscalidade (CORE CV)
🟢 FE-28 — Regime fiscal
US-09.01
Configurar regime normal
US-09.02
Configurar REMPE
🟢 FE-29 — Modelo 106
US-09.03
Gerar base Modelo 106
🟢 FE-30 — Validação fiscal
US-09.04
Validar consistência fiscal
🔴 EP-10 — e-Fatura / Middleware (CRÍTICO)
🟢 FE-31 — Configuração
US-10.01
Configurar certificado
🟢 FE-32 — Comunicação
US-10.02
Gerar XML
US-10.03
Enviar documento
🟢 FE-33 — Contingência
US-10.04
Emitir em contingência
🟢 FE-34 — Estados
US-10.05
Marcar autorizado/rejeitado
🟣 EP-11 — SAF-T CV
🟢 FE-35 — Exportação
US-11.01
SAF-T Contabilidade
US-11.02
SAF-T Inventário
🟢 FE-36 — Validação
US-11.03
Validar XML
🟡 EP-12 — RH
🟢 FE-37 — Funcionários
US-12.01
Criar funcionário
🟢 FE-38 — Processamento
US-12.02
Processar salários
🟤 EP-13 — Ativos
🟢 FE-39 — Gestão
US-13.01
Criar ativo
US-13.02
Calcular depreciação
🟢 EP-14 — Projetos
🟢 FE-40 — Gestão de projetos
US-14.01
Criar projeto
US-14.02
Associar custos
🟢 EP-15 — Subscrições SaaS
🟢 FE-41 — Planos
US-15.01
Criar plano
US-15.02
Atribuir plano
🟢 EP-16 — Dashboards
🟢 FE-42 — KPIs
US-16.01
Dashboard vendas
US-16.02
Dashboard financeiro
🧠 EP-17 — IA
🟢 FE-43 — Assistente
US-17.01
Perguntas em linguagem natural
🟢 FE-44 — Sugestões
US-17.02
Sugestões automáticas
🚀 PRIORIZAÇÃO FINAL (EXECUÇÃO REAL)
🔥 Sprint 1–4 (MVP CORE)

EP-01, EP-02, EP-03, EP-04, EP-05, EP-06

🔥 Sprint 5–8 (Financeiro + Fiscal)

EP-07, EP-09, EP-10, EP-11

⚙️ Sprint 9–12 (Completo)

EP-08, EP-16, EP-15

🧠 Pós-MVP

EP-12, EP-13, EP-14, EP-17