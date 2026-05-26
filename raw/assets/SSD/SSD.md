SSD — Spec-Driven Development
Projeto: NOVA-ERP
Versão: 1.0
Data: 02-04-2026
1. Visão do Produto

O NOVA-ERP é um ERP moderno, multi-tenant, orientado para empresas de Cabo Verde, com foco em:

conformidade fiscal local;
faturação eletrónica;
integração com DNRE / e-Fatura / SAF-T CV;
arquitetura SaaS multiempresa;
automação operacional;
inteligência artificial aplicada à gestão;
escalabilidade para pequenas, médias e grandes empresas.

O sistema deve competir em maturidade funcional com soluções como Primavera, PHC, Odoo e SAP Business One, mas com vantagem estratégica em:

adaptação local a Cabo Verde;
experiência moderna;
motor fiscal inteligente;
automação declarativa;
IA operacional e fiscal.
2. Objetivo do SSD

Este documento define a especificação funcional, técnica e operacional para desenvolvimento orientado por especificação (Spec-Driven Development), garantindo que cada módulo seja implementado com:

objetivos claros;
regras de negócio explícitas;
critérios de aceitação;
contratos entre módulos;
prioridades de implementação;
requisitos não funcionais;
eventos e fluxos críticos.

Este SSD deve ser a referência principal antes da escrita de código.

3. Princípios de Desenvolvimento
3.1 Princípios do produto
Multi-tenant por defeito.
Fiscalidade como núcleo do sistema.
Tudo auditável.
Tudo parametrizável por empresa.
Modular, extensível e versionável.
API-first sempre que possível.
Preparado para cloud e self-hosting.
Segurança, imutabilidade fiscal e rastreabilidade como requisitos base.
3.2 Princípios técnicos
Frontend: React + Vite + TypeScript + Tailwind.
Backend: Node.js / TypeScript.
Base de dados: PostgreSQL / Supabase.
Autenticação e autorização multi-tenant.
Event-driven nos fluxos críticos.
Logs estruturados e auditoria total.
Feature flags por tenant e por plano.
Filas para tarefas pesadas.
Geração documental desacoplada.
3.3 Princípios funcionais
Nenhum documento fiscal pode ser alterado após certificação/autorização.
Toda ação relevante deve gerar trilha de auditoria.
Toda configuração fiscal deve ser dependente do país e do regime fiscal da empresa.
O ERP deve funcionar por módulos independentes, mas integrados.
4. Escopo Macro do Produto
4.1 Módulos núcleo
Core Platform
Gestão de Empresas / Tenants
Utilizadores, perfis e permissões
Clientes e fornecedores
Produtos e serviços
Vendas
Compras
Inventário / logística
Tesouraria / caixa / bancos
Contabilidade
Fiscalidade
Recursos Humanos
Ativos / equipamentos
Projetos
Relatórios e dashboards
Integrações
Motor SAF-T CV
Motor e-Fatura / middleware
Subscrições e faturação SaaS
IA / assistente operacional
5. Arquitetura Funcional de Alto Nível
5.1 Camadas
Camada 1 — Plataforma base
tenants
utilizadores
permissões
planos/subscrições
auditoria
configurações globais
notificações
ficheiros e anexos
Camada 2 — Master Data
entidades
artigos
serviços
impostos
séries
armazéns
contas contabilísticas
bancos
centros de custo
documentos e tipologias
Camada 3 — Transacional
vendas
compras
stock
tesouraria
RH
ativos
projetos
Camada 4 — Fiscal e legal
IVA
retenções
SAF-T CV
Modelo 106
e-Fatura
autofaturação
documentos fiscais eletrónicos
reconciliação fiscal
Camada 5 — Inteligência e automação
alertas
previsões
IA fiscal
IA comercial
IA operacional
automações e assistentes
6. Personas Principais
Administrador do sistema
Gestor da empresa
Técnico de contabilidade
Responsável fiscal
Operador de vendas/POS
Responsável de compras
Responsável de armazém
RH / processamento salarial
Técnico de suporte / implementador
Auditor interno / externo
7. Multi-Tenant — Regras Base
7.1 Requisitos
Um utilizador pode pertencer a uma ou mais empresas.
Cada empresa é um tenant lógico isolado.
Dados nunca podem misturar-se entre tenants.
Permissões devem ser avaliadas por tenant.
Configurações fiscais, séries, documentos, contas, armazéns e impostos são por tenant.
Um utilizador pode alternar entre empresas sem novo login, se tiver acesso concedido.
7.2 Critérios de aceitação
Todas as queries obrigatoriamente filtradas por tenant_id.
Todas as tabelas core e transacionais com tenant_id.
Logs de auditoria com tenant_id, actor_id, entity_type, entity_id, action, before, after.
Testes automáticos devem impedir acesso cruzado entre tenants.
8. Módulo Core Platform
8.1 Funcionalidades
gestão de tenants
onboarding da empresa
configuração inicial
gestão de utilizadores
gestão de perfis
permissões por módulo/ação
auditoria
notificações
configuração geral do ERP
feature flags
idiomas, moeda, timezone
branding por tenant
8.2 Regras
tenant só pode operar após setup inicial concluído.
empresa deve ter regime fiscal definido.
empresa deve ter moeda base definida.
empresa deve ter série/documentos mínimos ativos antes de faturar.
8.3 Critérios de aceitação
criar empresa
ativar módulos
convidar utilizadores
definir permissões
alternar de tenant
registar auditoria total
9. Módulo de Entidades
9.1 Tipos
cliente
fornecedor
cliente e fornecedor
funcionário
parceiro
entidade pública
cliente indiferenciado / VD
9.2 Campos essenciais
código interno
tipo
nome comercial
nome fiscal
NIF
país
morada
contactos
condição de pagamento
limite de crédito
segmento
mercado
estado fiscal
ativo/inativo
9.3 Regras
NIF deve ser validável conforme país/configuração.
não permitir alterar NIF em entidades com documentos fiscais certificados, salvo fluxo controlado.
cliente indiferenciado deve existir como entidade especial do sistema.
entidades podem ter múltiplos endereços e contactos.
9.4 Critérios de aceitação
criar cliente nacional
criar fornecedor externo
emitir documento para cliente indiferenciado
bloquear edição de campos críticos após movimentos fiscais
10. Módulo de Produtos e Serviços
10.1 Tipos
mercadoria
matéria-prima
produto acabado
serviço
ativo
uso interno
composto / kit
10.2 Campos essenciais
código
descrição
tipo
unidade base
unidade compra
unidade venda
preço de custo
preço de venda
imposto
stock controlado ou não
armazém por defeito
família/subfamília
marca/modelo
lote/série
dimensões
estado
10.3 Regras
serviços não movimentam stock.
serviços podem movimentar receita/custo/centro de custo.
artigo stockável exige configuração de inventário.
artigos com movimentos fiscais certificados não devem permitir alteração destrutiva da descrição base.
10.4 Critérios de aceitação
criar mercadoria
criar serviço não stockável
criar artigo com lote
criar artigo com número de série
vender serviço sem impacto em armazém
11. Módulo Vendas
11.1 Funcionalidades
orçamentos
encomendas
guias
faturas
faturas-recibo
talões
notas de crédito
notas de débito
devoluções
anulações e estornos controlados
POS
documentos em contingência
emissão para cliente indiferenciado
workflows documentais
11.2 Regras fiscais
documentos devem obedecer às tipologias locais.
numeração por série.
hash fiscal / integridade documental.
QR code obrigatório quando aplicável.
ND e NC sempre referenciam documento origem.
documento certificado não é editável.
em contingência, marcar estado e motivo.
submissão posterior dentro da regra legal parametrizada.
11.3 Critérios de aceitação
emitir FT
emitir FR
emitir TV
emitir NC referenciando FT
impedir alteração de FT certificada
gerir série anual ou contínua
comunicar documento ao motor fiscal/e-Fatura
12. Módulo Compras
12.1 Funcionalidades
pedidos de cotação
cotações
encomendas a fornecedor
receções
faturas de compra
notas de fornecedor
devoluções
aprovação interna
integração com stock
integração com tesouraria
integração com contabilidade
12.2 Regras
receção pode atualizar stock antes da fatura, conforme configuração.
compra de serviços não atualiza stock.
documentos devem gerar pendentes em conta corrente conforme parametrização.
permitir compra por linha ou documento.
12.3 Critérios de aceitação
rececionar artigos em stock
lançar compra de serviço
gerar pendente para fornecedor
integrar compra com contabilidade
13. Módulo Inventário / Logística
13.1 Funcionalidades
armazéns
localizações
movimentos internos
transferências
reservas
lotes
séries
contagem
inventário físico
inventário permanente
expedição
receção
rotura de stock
stock mínimo/máximo/reposição
13.2 Regras
stock por tenant, armazém, localização, artigo, lote, série.
ruptura tratada por política do tenant/documento.
transferências podem ter trânsito.
rastreabilidade por lote/série.
inventário gera ajuste com auditoria.
13.3 Critérios de aceitação
entrada de stock
saída de stock
transferência entre armazéns
contagem física
ajuste de inventário
rastreabilidade de lote
14. Módulo Tesouraria / Caixa / Bancos
14.1 Funcionalidades
contas correntes
pendentes
recebimentos
pagamentos
compensações
adiantamentos
caixa
bancos
transferências
emissão de recibos
reconciliação bancária
gestão de cheques
depósitos
movimentos manuais
14.2 Regras
liquidação total ou parcial.
documentos de CC por natureza e tipologia.
reconciliação não altera lançamento original, cria estado/ligação.
pagamentos e recebimentos podem integrar contabilidade automaticamente.
controlo de limite de crédito por cliente.
14.3 Critérios de aceitação
gerar pendente a partir de venda
liquidar parcialmente fatura
reconciliação bancária manual
reconciliação automática por regras
bloquear venda por limite de crédito
15. Módulo Contabilidade
15.1 Funcionalidades
plano de contas
diários
documentos contabilísticos
lançamentos manuais
integrações automáticas
apuramentos
balanços
balancetes
razão
extratos
fechos e aberturas
centros de custo
fluxos de caixa
15.2 Regras
exercício contabilístico por tenant.
bloqueios por período/diário/exercício.
lançamentos automáticos parametrizáveis.
integrações de vendas, compras, bancos, ativos e RH.
reconstrução de acumulados.
trilha de anulação/estorno.
15.3 Critérios de aceitação
criar conta
lançar movimento manual
integrar venda
integrar compra
bloquear período
gerar balancete
16. Módulo Fiscalidade
16.1 Objetivo

Ser o cérebro fiscal do ERP para Cabo Verde e, futuramente, multi-país.

16.2 Funcionalidades
regime fiscal da empresa
IVA
REMPE
retenções
documentos fiscais
regras declarativas
modelos legais
validações fiscais
fecho fiscal
livros fiscais
reconciliação fiscal
modelo 106
obrigações periódicas
16.3 Regras específicas
REMPE: IVA 0 e tratamento TEU conforme parametrização do país/regime.
Regime normal: IVA conforme taxa aplicável.
mudança de regime apenas conforme regras legais parametrizadas.
notas de crédito/débito exigem referência ao documento original quando aplicável.
validação de estrutura mínima antes de submissão legal.
16.4 Critérios de aceitação
configurar regime REMPE
configurar regime normal
calcular IVA corretamente
gerar mapa fiscal por período
preparar dados do Modelo 106
validar consistência fiscal antes do fecho
17. Módulo e-Fatura / DNRE / Middleware
17.1 Funcionalidades
configuração da integração
gestão de certificados digitais
gestão de token/código
comunicação via middleware
estados de transmissão
reenvio
contingência
consulta de retorno
logs técnicos
suporte a autofaturação
gestão do LED / IUD / XML
17.2 Regras
não assumir API pública direta se o fluxo exigir middleware.
certificados devem ser armazenados de forma segura.
filas assíncronas para comunicação.
cada DFE deve ter estado:
pendente
em fila
enviado
autorizado
rejeitado
contingência
reenviado
guardar request/response técnico.
17.3 Critérios de aceitação
configurar certificado
emitir XML válido
enviar para middleware
receber resposta
marcar estado
tratar rejeição
permitir reenvio controlado
18. Módulo SAF-T CV
18.1 Funcionalidades
exportação SAF-T Contabilidade
exportação SAF-T Inventário
exportação SAF-T Completo
exportação SAF-T Outros
validação offline
geração por período
geração por exercício
logs de exportação
reprocessamento
auditoria de incoerências
18.2 Regras
XML UTF-8.
obedecer ao XSD vigente configurado.
sem valores negativos quando não permitidos.
separar ficheiros por tipo.
exportação deve ser reproduzível.
performance para grandes volumes.
18.3 Critérios de aceitação
gerar SAF-T contabilidade válido
gerar SAF-T inventário válido
validar estrutura contra XSD
exportar por período parcial
registar histórico de geração
19. Módulo RH
19.1 Funcionalidades
ficha do funcionário
admissões
processamento salarial
faltas
férias
horas extra
descontos
subsídios
pagamentos
mapas
parametrização legal
integração com contabilidade
19.2 Regras
regras laborais parametrizáveis por país.
motor salarial baseado em rubricas.
separar dados sensíveis por permissões.
histórico de alterações remuneratórias.
processamento sequencial por período.
19.3 Critérios de aceitação
criar funcionário
processar salário
lançar desconto legal
gerar recibo
integrar contabilisticamente
20. Módulo Ativos
20.1 Funcionalidades
ficha do ativo
aquisição
depreciação
reavaliação
manutenção
transferência
alienação
abate
sinistro
mapas legais
20.2 Regras
planos de depreciação parametrizáveis.
integração com contabilidade.
histórico completo do ciclo de vida.
20.3 Critérios de aceitação
criar ativo
registar aquisição
calcular depreciação
integrar depreciação na contabilidade
21. Módulo Projetos
21.1 Funcionalidades
criação de projeto
fases
tarefas
custos
receitas
equipas
timesheets
faturação por projeto
rentabilidade
21.2 Critérios de aceitação
criar projeto
alocar custo
associar venda
calcular margem
22. Módulo Subscrições SaaS do próprio ERP
22.1 Funcionalidades
planos
pricing
módulos por plano
limites por plano
trial
upgrade/downgrade
billing cycle
suspensão
reativação
cobrança
gestão do tenant por subscrição
22.2 Regras
módulos ativos dependem do plano.
feature flags controladas por subscrição.
tenant bloqueado parcialmente em incumprimento, sem perda de dados.
22.3 Critérios de aceitação
criar plano
atribuir tenant a plano
ativar/desativar módulos
controlar limites
23. IA no NOVA-ERP
23.1 Objetivos
assistente operacional
assistente fiscal
deteção de anomalias
sugestões automáticas
pesquisa semântica
automação documental
apoio à decisão
23.2 Casos de uso prioritários
sugerir classificação contabilística
detetar incoerência fiscal
prever rutura de stock
prever atraso de clientes
sugerir reposição
responder perguntas sobre dados do ERP
gerar resumos gerenciais
23.3 Regras
IA nunca altera dados críticos sem confirmação humana.
toda sugestão de IA deve ser explicável e auditável.
logs de prompts e outputs sensíveis conforme política de segurança.
24. Eventos de Domínio Principais
tenant.created
tenant.activated
user.invited
user.joined_tenant
entity.created
item.created
sale.document.created
sale.document.certified
sale.document.sent_to_efatura
sale.document.authorized
sale.document.rejected
purchase.document.posted
inventory.movement.created
inventory.adjustment.posted
receivable.created
payable.created
payment.received
payment.made
bank.reconciled
journal.entry.posted
saft.generated
tax.period.closed
payroll.processed
asset.depreciated
subscription.changed
25. Requisitos Não Funcionais
25.1 Segurança
RBAC por tenant
encriptação de segredos
gestão segura de certificados
auditoria completa
proteção contra acesso cruzado entre tenants
logs imutáveis para eventos fiscais críticos
25.2 Performance
listas paginadas
filtros indexados
geração assíncrona de SAF-T e relatórios pesados
suporte a grandes volumes de faturas
filas para integrações externas
25.3 Escalabilidade
arquitetura preparada para múltiplos tenants
background jobs
separação entre transacional e reporting quando necessário
possibilidade futura de particionamento
25.4 Disponibilidade
retries em integrações
contingência para faturação
backups
observabilidade
monitorização técnica
25.5 Auditabilidade
before/after nos eventos críticos
versionamento de configurações fiscais
trilha de quem, quando, onde, o quê
26. Requisitos de UX
interface moderna, limpa e rápida
linguagem pt-PT
foco em produtividade
atalhos e ações em massa
feedback claro de erro fiscal
dashboards por função
documentos com estados visuais claros
pesquisa global
breadcrumbs
ações irreversíveis sempre confirmadas
27. Roadmap de Implementação por Fases
Fase 1 — Plataforma Base
multi-tenant
auth
permissões
empresas
utilizadores
auditoria
configurações
Fase 2 — Master Data
entidades
produtos
serviços
armazéns
impostos
séries
documentos base
Fase 3 — Operação Comercial
vendas
compras
inventário
contas correntes
tesouraria básica
Fase 4 — Fiscal Núcleo
documentos fiscais CV
regras IVA/REMPE
modelo 106 base
motor SAF-T base
integração middleware/e-Fatura
Fase 5 — Financeira Completa
contabilidade
bancos
reconciliação
fechos
mapas
Fase 6 — RH / Ativos / Projetos
módulos complementares
Fase 7 — IA e automação avançada
assistente
deteção de anomalias
previsões
copiloto ERP
28. Definition of Done Global

Uma funcionalidade só é considerada concluída quando:

cumpre a especificação funcional;
cumpre regras de negócio;
respeita isolamento multi-tenant;
tem validações de segurança;
gera auditoria quando aplicável;
tem testes mínimos;
tem estados e erros claros na UI;
está documentada;
está pronta para integração com módulos dependentes;
não quebra conformidade fiscal.
29. User Stories Macro Exemplos
US-001

Como administrador, quero criar uma empresa para iniciar operação no ERP.

US-002

Como gestor, quero alternar entre empresas às quais tenho acesso.

US-003

Como operador comercial, quero emitir uma fatura para um cliente.

US-004

Como operador POS, quero vender a cliente indiferenciado.

US-005

Como responsável fiscal, quero gerar SAF-T CV válido.

US-006

Como contabilista, quero integrar documentos de venda na contabilidade.

US-007

Como tesoureiro, quero reconciliar movimentos bancários.

US-008

Como gestor, quero ver dashboards de vendas, cobrança e stock.

US-009

Como responsável fiscal, quero submeter documentos via middleware.

US-010

Como administrador SaaS, quero controlar os módulos por plano de subscrição.

30. Riscos Principais
complexidade fiscal local;
dependência de fluxos externos DNRE/e-Fatura;
erros de isolamento multi-tenant;
crescimento desordenado do domínio;
mistura entre regras fiscais e UI;
performance em SAF-T e faturação massiva;
ausência de motor de auditoria robusto;
permissões mal desenhadas.
31. Diretrizes Finais para Implementação
começar pelo core multi-tenant;
nunca desenvolver módulo ignorando auditoria;
não implementar faturação antes de séries, impostos, entidades e artigos estarem sólidos;
não implementar SAF-T sem modelo contabilístico e fiscal consistente;
separar claramente:
documentos comerciais,
documentos fiscais,
movimentos de stock,
pendentes de tesouraria,
lançamentos contabilísticos;
tratar fiscalidade como engine e não como lógica espalhada pela UI;
usar configuração orientada por país/regime para futura internacionalização.
32. Resultado Esperado

No fim da execução deste SSD, o NOVA-ERP deverá ter:

base SaaS multi-tenant robusta;
módulos core integrados;
conformidade fiscal Cabo Verde;
motor documental sólido;
contabilidade e tesouraria integradas;
SAF-T e e-Fatura preparados;
fundação pronta para IA empresarial.