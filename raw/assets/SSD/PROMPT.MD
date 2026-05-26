Quero que cries e implementes a base completa do meu ERP SaaS chamado NOVA-ERP, com arquitetura multi-tenant, foco fiscal em Cabo Verde, UX moderna, código limpo, escalável, auditável e pronto para evolução contínua.

TRABALHA COMO ARQUITETO DE SOFTWARE + PRODUCT ENGINEER + TECH LEAD + ERP DOMAIN DESIGNER.

OBJETIVO GERAL
Construir a primeira base real e utilizável do NOVA-ERP, cobrindo:
1. plataforma base multi-tenant
2. autenticação e autorização
3. gestão de tenants/empresas
4. utilizadores, perfis e permissões
5. entidades (clientes, fornecedores, terceiros)
6. artigos/produtos/serviços
7. vendas
8. compras
9. inventário
10. tesouraria / contas correntes / caixa e bancos
11. fiscalidade base Cabo Verde
12. integração preparada para e-Fatura / middleware
13. exportação preparada para SAF-T CV
14. dashboards iniciais
15. base arquitetural para contabilidade, RH, ativos, projetos e IA

META
Quero que entregues um projeto utilizável, coerente, modular e tecnicamente sólido, e não apenas uma demo visual.

STACK E TECNOLOGIA
Assume e implementa com:
- Frontend: React + TypeScript + Vite
- UI: Tailwind CSS
- Backend/server actions/API: TypeScript
- Base de dados: Supabase PostgreSQL
- Auth: Supabase Auth
- ORM/query layer: o que for mais consistente com o stack gerado
- Validação: Zod ou equivalente
- Estado/UI patterns: simples, robustos e fáceis de manter
- Charts/dashboards: biblioteca moderna leve
- Estrutura preparada para crescimento enterprise

INSTRUÇÕES GERAIS DE IMPLEMENTAÇÃO
- Não cries código descartável.
- Não cries mocks falsos quando já for possível criar estrutura real.
- Prioriza modelo de dados sólido.
- Prioriza separação de domínios.
- Prioriza segurança e isolamento multi-tenant.
- Prioriza legibilidade, convenções e escalabilidade.
- Gera a app já com seed inicial mínima.
- Implementa rotas, páginas, componentes, base de dados, políticas de segurança e fluxos principais.
- Usa nomes claros e consistentes.
- Evita overengineering desnecessário, mas não sacrifiques a arquitetura.
- Tudo deve ficar preparado para continuação por fases.

REGRAS ARQUITETURAIS OBRIGATÓRIAS
1. MULTI-TENANT NATIVO
- Todo o sistema deve nascer multi-tenant.
- Cada empresa = 1 tenant lógico.
- Todas as tabelas de domínio devem incluir tenant_id quando aplicável.
- Nenhum dado pode vazar entre tenants.
- Um utilizador pode pertencer a múltiplos tenants.
- Deve existir possibilidade de alternância de tenant no UI.
- Permissões avaliadas por tenant.

2. SEGURANÇA
- Implementar autenticação real.
- Implementar autorização por papéis/perfis/permissões.
- Preparar Row Level Security no Supabase.
- Restringir acesso por tenant_id.
- Proteger ações críticas.
- Guardar logs básicos de auditoria.

3. AUDITORIA
- Criar tabela de auditoria para eventos críticos.
- Registar: tenant_id, actor_user_id, entidade, entity_id, ação, timestamp, before, after.
- Auditar pelo menos:
  - criação de tenant
  - convite de utilizador
  - alterações em entidades
  - criação e alteração de artigos
  - emissão e anulação de documentos
  - mudanças de configuração fiscal
  - liquidações
  - eventos de integração fiscal

4. MODULARIDADE
Separar o sistema por domínios/módulos:
- core
- auth
- tenants
- users
- permissions
- entities
- catalog
- sales
- purchases
- inventory
- treasury
- tax
- integrations
- reporting

5. QUALIDADE DE UX
- Interface moderna, limpa, profissional
- Sidebar com módulos
- Header com seletor de tenant
- Dashboard inicial útil
- Formulários com validação clara
- Tabelas com pesquisa, filtros e paginação
- Estados vazios bem desenhados
- Mensagens de erro compreensíveis
- PT-PT em toda a interface

CONTEXTO LEGAL E FISCAL DE CABO VERDE
Este ERP é orientado a Cabo Verde, por isso deves modelar a base para:
- NIF
- documentos de venda e compra
- FT, FR, TV, NC, ND, devoluções
- séries documentais
- IVA
- REMPE / regime normal como configuração futura
- integração futura com e-Fatura via middleware
- geração futura de SAF-T CV
- campo e estrutura preparados para QR code, IUD, LED e estado de transmissão
- documentos fiscais imutáveis após certificação/autorização

ATENÇÃO:
Nesta fase não precisas concluir toda a integração legal real, mas tens de deixar:
- o domínio desenhado corretamente
- estados previstos
- campos necessários
- arquitetura preparada
- serviços/adapters preparados para futura integração

MÓDULOS A IMPLEMENTAR AGORA

MÓDULO 1 — CORE / TENANTS / AUTH
Implementar:
- ecrã de login
- ecrã de registo ou onboarding inicial
- criação de tenant
- switch de tenant
- membership user ↔ tenant
- perfis e permissões base
- layout principal autenticado
- dashboard base

Estrutura mínima de dados:
- users
- tenants
- tenant_memberships
- roles
- permissions
- role_permissions
- user_role_assignments ou equivalente
- audit_logs

Fluxos:
- criar conta
- criar empresa
- ficar como admin dessa empresa
- convidar utilizador
- aceitar convite
- alternar tenant

MÓDULO 2 — ENTIDADES
Implementar CRUD real de:
- clientes
- fornecedores
- terceiros
- cliente indiferenciado / VD

Campos importantes:
- código
- tipo
- nome comercial
- nome fiscal
- NIF
- país
- morada
- email
- telefone
- limite de crédito
- condição de pagamento
- ativo/inativo
- notas
- created_at / updated_at

Regras:
- não permitir duplicação incoerente
- suportar cliente e fornecedor no mesmo registo se necessário
- preparar bloqueio futuro de alteração de NIF quando houver documentos certificados

MÓDULO 3 — ARTIGOS / PRODUTOS / SERVIÇOS
Implementar CRUD real de:
- mercadorias
- serviços

Campos:
- código
- descrição
- tipo (product/service)
- unidade base
- preço de venda
- preço de custo
- taxa de imposto
- stock_controlado
- ativo
- família/subfamília opcionais
- armazém padrão opcional

Regras:
- serviço não movimenta stock
- produto pode movimentar stock
- preparar extensão futura para lote, série, unidades compostas

MÓDULO 4 — VENDAS
Implementar base funcional de:
- documentos de venda
- linhas de documento
- estados do documento
- emissão de FT, FR, TV, NC, ND
- listagem de documentos
- detalhe do documento
- criação manual de documento
- totalização automática
- impressão/exportação básica em layout simples
- estado de documento: draft, issued, settled, cancelled, credit_note, contingency, fiscal_pending, fiscal_authorized, fiscal_rejected

Tabelas mínimas:
- sale_documents
- sale_document_lines
- document_series
- document_types

Campos importantes:
- tenant_id
- tipo_documento
- série
- número
- entidade
- data
- moeda
- subtotal
- imposto
- total
- estado
- referência ao documento origem para NC/ND
- campos preparados para iud, led, qr_code_payload, fiscal_status, middleware_status

Regras:
- NC e ND referenciam documento origem
- FR gera também liquidação
- TV deve permitir cliente indiferenciado
- documento emitido não deve ser livremente editável depois de fechado
- preparação para hash/assinatura/certificação futura

MÓDULO 5 — COMPRAS
Implementar:
- documentos de compra
- linhas de compra
- fornecedor
- estados
- receção simples
- integração com pendentes

Tipos mínimos:
- fatura fornecedor
- guia/receção
- devolução fornecedor

Tabelas:
- purchase_documents
- purchase_document_lines

Regras:
- compra de mercadoria pode atualizar stock
- compra de serviço não atualiza stock
- compra cria pendente de fornecedor quando aplicável

MÓDULO 6 — INVENTÁRIO
Implementar base funcional:
- armazéns
- movimentos de stock
- stock atual por artigo
- entradas
- saídas
- transferências simples
- ajuste manual

Tabelas:
- warehouses
- stock_movements
- stock_balances ou cálculo equivalente eficiente

Regras:
- movimentos entram por compras, vendas, ajustes ou transferências
- serviços não geram movimentos
- stock por tenant e armazém
- prever tipo do movimento: purchase_in, sale_out, transfer_in, transfer_out, adjustment_in, adjustment_out

MÓDULO 7 — TESOURARIA / CONTAS CORRENTES
Implementar base de:
- pendentes de clientes e fornecedores
- liquidação total
- liquidação parcial
- criação automática de pendentes a partir de vendas e compras
- contas de caixa e banco simplificadas
- movimentos financeiros simples

Tabelas:
- receivables_payables ou separadas
- payments
- payment_allocations
- cash_accounts / bank_accounts
- cash_movements

Regras:
- FR liquida automaticamente
- FT cria pendente de cliente
- compra cria pendente de fornecedor
- liquidação parcial mantém saldo em aberto
- guardar histórico de afetação pagamento ↔ documento

MÓDULO 8 — FISCALIDADE BASE CV
Implementar estrutura de configuração fiscal, sem tentar fechar tudo legalmente já:
- tabela de taxas de imposto
- tabela/configuração de regime fiscal por tenant
- flags para regime normal / REMPE
- base de validação fiscal simples
- estrutura para Modelo 106 futuro
- estrutura para retenções futuras
- estrutura de motivo de isenção

Tabelas mínimas:
- tax_rates
- tenant_tax_profiles
- tax_exemptions ou equivalente
- fiscal_periods

MÓDULO 9 — INTEGRAÇÃO PREPARADA PARA e-FATURA
Não inventes a integração toda agora, mas cria o domínio e os adapters:
- integration_configs
- digital_certificates (apenas metadata e storage reference; nunca expor segredo)
- fiscal_transmissions
- transmission_logs

Criar serviço/interface com métodos tipo:
- generateFiscalPayload(documentId)
- queueTransmission(documentId)
- markAuthorized(documentId, payload)
- markRejected(documentId, reason)
- resendTransmission(documentId)

MÓDULO 10 — SAF-T CV PREPARADO
Criar:
- tabela de export jobs
- estrutura de serviço para gerar XML no futuro
- botão/ação “Gerar SAF-T” com job placeholder real
- histórico de exportações

Sem fake. Quero estrutura técnica real preparada, mesmo que a geração final ainda seja versão inicial.

MÓDULO 11 — DASHBOARD
Implementar dashboard inicial com:
- total vendas do mês
- total compras do mês
- pendentes a receber
- pendentes a pagar
- stock baixo
- documentos recentes
- resumo por tenant atual

MÓDULO 12 — BASE PARA ESCALABILIDADE
Preparar desde já:
- separação de camadas de domínio
- services/use-cases
- repositories ou abstração equivalente se fizer sentido
- validação centralizada
- tipos fortes
- enums consistentes
- componentes reutilizáveis
- seeds iniciais

BASE DE DADOS — ENTREGA O MELHOR MODELO INICIAL POSSÍVEL
Quero um schema inicial robusto.
Inclui:
- chaves primárias
- foreign keys
- índices importantes
- unique constraints
- enums
- campos de auditoria
- status fields
- created_at / updated_at
- soft delete só onde fizer sentido real

IMPLEMENTAÇÃO DE RLS / SEGURANÇA
Se estiveres a usar Supabase:
- cria policies base para isolamento por tenant
- utilizador só lê/escreve dados do(s) tenant(s) a que pertence
- admin do tenant pode gerir utilizadores desse tenant
- bloquear acesso a documentos de outros tenants

SEED INICIAL
Criar dados de seed mínimos:
- 1 tenant demo
- 1 admin demo
- 1 cliente indiferenciado
- 3 clientes
- 3 fornecedores
- 5 artigos
- 2 serviços
- 1 armazém
- 1 série documental
- alguns documentos exemplo
- alguns movimentos financeiros
- dashboard já com dados visíveis

PÁGINAS / ECRÃS QUE DEVEM EXISTIR
Públicas:
- login
- registo / criar empresa

Privadas:
- dashboard
- tenants/settings
- utilizadores
- perfis/permissões
- clientes
- fornecedores
- artigos
- serviços
- vendas/lista
- vendas/novo
- vendas/detalhe
- compras/lista
- compras/nova
- inventário
- armazéns
- tesouraria
- documentos pendentes
- fiscalidade/configuração
- integrações
- saft/exportações
- auditoria

DESIGN SYSTEM / COMPONENTES
Criar componentes reutilizáveis:
- AppShell
- Sidebar
- Header
- TenantSwitcher
- PageHeader
- DataTable
- FilterBar
- FormField
- MoneyField
- StatusBadge
- EmptyState
- ConfirmDialog
- AuditTimeline
- DocumentTotalsCard

ESTADOS E ENUMS IMPORTANTES
Define enums coerentes para:
- tenant_status
- membership_status
- entity_type
- item_type
- sale_document_type
- purchase_document_type
- document_status
- fiscal_status
- payment_status
- inventory_movement_type
- tax_regime_type

CRITÉRIOS DE QUALIDADE
- código tipado
- sem duplicação desnecessária
- sem componentes gigantes confusos
- sem SQL caótico
- sem nomes genéricos tipo data1, data2, temp
- sem misturar lógica de domínio com UI descontroladamente
- sem hardcodes irresponsáveis
- sem depender de mocks para o essencial

O QUE ESPERO QUE FAÇAS SOZINHO
- tomar boas decisões de arquitetura
- modelar tabelas
- criar rotas
- criar layout
- criar componentes
- criar fluxos CRUD
- criar seeds
- configurar segurança
- deixar comentários apenas onde necessário
- deixar o projeto navegável e coerente

SAÍDA ESPERADA
Quero que implementes diretamente a aplicação com:
1. estrutura do projeto
2. schema/base de dados
3. autenticação
4. páginas
5. componentes
6. CRUDs principais
7. serviços de domínio
8. policies de segurança
9. seeds/demo
10. base preparada para fases seguintes

ORDEM DE EXECUÇÃO
Executa nesta ordem:
1. arquitetura e estrutura do projeto
2. schema e auth
3. multi-tenant e memberships
4. permissões
5. entidades
6. catálogo
7. vendas
8. compras
9. inventário
10. tesouraria
11. fiscalidade base
12. integrações base
13. dashboard
14. refinamento final

IMPORTANTE
- Se tiveres de escolher entre visual bonito e base sólida, escolhe base sólida.
- Se tiveres de escolher entre rapidez e coerência do domínio, escolhe coerência.
- Não me entregues só wireframes.
- Não pares na camada visual.
- Implementa o máximo possível de forma real.
- Mantém tudo preparado para expansão futura para contabilidade, RH, ativos, projetos e IA.
- Trabalha como se isto fosse o foundation release real de um ERP SaaS profissional.

NO FINAL, QUERO:
- app funcional
- navegação funcional
- dados reais de demo
- estrutura séria
- base pronta para continuar evolução

COMEÇA AGORA A IMPLEMENTAÇÃO.