PRD — Product Requirements Document
Projeto: NOVA-ERP
Versão: 1.0
Data: 02-04-2026
Estado: Draft Estratégico de Execução
1. Resumo Executivo

O NOVA-ERP é um ERP SaaS multi-tenant, moderno, fiscalmente orientado, desenhado para empresas de Cabo Verde e preparado para expansão futura para outros países.

O produto tem como objetivo substituir ou competir com soluções como Primavera, PHC, Odoo e SAP Business One no segmento local e regional, oferecendo:

conformidade fiscal nativa para Cabo Verde;
faturação eletrónica;
integração com DNRE / e-Fatura / SAF-T CV;
arquitetura cloud-ready e self-hosting ready;
automação operacional;
dashboards de gestão;
motor fiscal robusto;
inteligência artificial aplicada ao ERP.

O NOVA-ERP deve ser um sistema que permita a uma empresa operar integralmente, desde:

cadastro e master data;
vendas e compras;
inventário;
tesouraria;
contabilidade;
fiscalidade;
recursos humanos;
ativos;
projetos;
reporting;
integração legal e declarativa.
2. Problema que o Produto Resolve

Empresas em Cabo Verde enfrentam vários problemas com os sistemas atuais:

baixa adaptação à legislação local;
processos fiscais dispersos e pouco automatizados;
integração complexa com e-Fatura / DNRE;
pouca flexibilidade para SaaS multiempresa;
UI/UX antiga;
fraca automação;
pouca auditabilidade;
dificuldade de escalar para múltiplas empresas;
baixa preparação para IA e analytics.

O NOVA-ERP resolve isso com uma abordagem moderna:

fiscalidade integrada desde a origem;
motor documental sólido;
multi-tenant nativo;
ERP modular;
automação de regras;
rastreabilidade total;
arquitetura orientada a evolução.
3. Visão do Produto
3.1 Visão

Construir o ERP mais moderno, escalável e fiscalmente preparado para Cabo Verde, com base multi-tenant SaaS e preparado para transformar-se numa plataforma ERP inteligente de referência regional.

3.2 Missão

Permitir que empresas operem, controlem, declarem, analisem e escalem a sua atividade num único sistema confiável, auditável e legalmente alinhado.

3.3 Proposta de valor

O NOVA-ERP oferece:

operação empresarial centralizada;
conformidade fiscal local desde o primeiro dia;
automação dos fluxos de negócio;
rápida adaptação por empresa;
escalabilidade SaaS;
fundação para IA aplicada.
4. Objetivos do Produto
4.1 Objetivos de negócio
lançar um ERP SaaS multi-tenant funcional e vendável;
atender pequenas, médias e grandes empresas;
monetizar por subscrição modular;
reduzir custo de implementação;
permitir onboarding repetível;
criar diferenciação fiscal e tecnológica.
4.2 Objetivos de produto
ter módulos core integrados;
garantir isolamento total entre empresas;
permitir emissão documental e fiscal robusta;
automatizar tesouraria, contabilidade e reporting;
suportar integração com DNRE/e-Fatura/SAF-T CV;
preparar base para IA operacional e fiscal.
4.3 Objetivos técnicos
arquitetura escalável;
modelo de dados multi-tenant consistente;
APIs internas limpas;
auditoria transversal;
segurança por defeito;
performance em operações críticas;
suporte a cloud e self-hosting.
5. Metas de Sucesso
5.1 Métricas de produto
tempo médio de onboarding de empresa
número de empresas ativas
documentos emitidos por mês
taxa de sucesso de emissão fiscal
taxa de sucesso de geração SAF-T
percentagem de automação contabilística
taxa de retenção por tenant
número médio de módulos ativos por empresa
5.2 Métricas operacionais
tempo médio de carregamento dos principais ecrãs
taxa de erros em integração externa
tempo médio de geração de SAF-T
tempo médio de emissão de documento
número de incidentes por tenant
taxa de falhas por job assíncrono
5.3 Metas iniciais
onboarding completo de tenant em menos de 30 minutos
emissão de documento comercial em menos de 3 segundos
geração SAF-T parcial em tempo aceitável para PME
100% de isolamento multi-tenant validado por testes
trilha de auditoria em 100% dos eventos críticos
6. Escopo do Produto
6.1 Incluído no produto
plataforma multi-tenant
gestão de empresas
utilizadores e permissões
clientes e fornecedores
produtos e serviços
vendas
compras
inventário
tesouraria
contabilidade
fiscalidade
RH
ativos
projetos
relatórios
subscrições SaaS
SAF-T CV
integração e-Fatura / middleware
base para IA
6.2 Fora do escopo inicial
manufatura avançada
MRP completo
CRM enterprise completo
BI avançado tipo data warehouse externo
marketplace de apps
multi-país completo já no MVP
payroll multi-país avançado
consolidação multinacional avançada
7. Utilizadores-Alvo
7.1 Perfis principais

Administrador do sistema
Configura a empresa, utilizadores, permissões, séries, impostos, módulos.

Gestor / Diretor
Consulta dashboards, acompanha vendas, tesouraria, compras, rentabilidade e risco.

Operador comercial / faturação
Emite orçamentos, faturas, recibos, notas de crédito/débito, POS.

Responsável de compras
Gere fornecedores, encomendas, receções, custos e aprovações.

Responsável de armazém
Controla stock, transferências, contagens, lotes, séries e inventários.

Tesouraria / financeiro
Controla pendentes, recebimentos, pagamentos, bancos, reconciliações.

Contabilista
Valida lançamentos, apuramentos, mapas, exercícios e integrações.

Responsável fiscal
Valida documentos, regras fiscais, Modelo 106, SAF-T, e-Fatura.

RH
Gere fichas, processamento salarial, recibos, descontos e mapas.

Técnico / implementador
Configura tenant, parametriza sistema, migra dados, acompanha go-live.

8. Princípios do Produto
8.1 Princípios funcionais
fiscalidade no centro do sistema;
tudo relevante deve ser auditável;
parametrização por empresa;
documentos fiscais imutáveis após certificação;
separação clara entre documentos, stock, tesouraria e contabilidade;
modularidade real.
8.2 Princípios de UX
simples para usar;
rápido nas operações do dia a dia;
estados claros;
erros explicativos;
foco em produtividade;
interface moderna em pt-PT.
8.3 Princípios técnicos
multi-tenant nativo;
segurança por defeito;
event-driven nos fluxos críticos;
jobs assíncronos para tarefas pesadas;
arquitetura preparada para evolução contínua.
9. Arquitetura Funcional
9.1 Blocos principais
Plataforma Base
Master Data
Operação Comercial
Operação Financeira
Fiscalidade
Compliance / Legal
RH / Ativos / Projetos
Reporting / IA
Subscrição SaaS
9.2 Relação entre blocos
Master Data alimenta todos os módulos.
Vendas e compras geram impactos em inventário, tesouraria e contabilidade.
Fiscalidade observa e valida documentos e movimentos.
Contabilidade recebe movimentos integrados ou manuais.
Reporting consome dados operacionais e financeiros.
IA assiste utilizadores com base nos dados autorizados.
10. Requisitos Funcionais Globais
10.1 Multi-tenant
cada empresa é um tenant isolado;
um utilizador pode pertencer a mais de uma empresa;
permissões são avaliadas por tenant;
dados nunca podem cruzar entre tenants.
10.2 Auditoria
criação, edição, anulação, integração e fecho devem gerar eventos auditáveis;
guardar ator, data/hora, tenant, contexto, before/after quando aplicável.
10.3 Configuração por empresa
moeda base;
país;
regime fiscal;
séries;
impostos;
centros;
armazéns;
módulos ativos;
plano de contas.
10.4 Segurança
login seguro;
gestão de sessão;
segregação de acessos;
gestão de segredos;
controlo de permissões por ação;
logs de segurança.
11. Módulo 1 — Plataforma Base
11.1 Objetivo

Fornecer a infraestrutura funcional do ERP: tenants, utilizadores, permissões, auditoria, configuração, notificações e governação do sistema.

11.2 Funcionalidades
criar tenant/empresa
onboarding inicial
ativação de módulos
convites a utilizadores
gestão de perfis
permissões por módulo/ação
branding do tenant
configurações gerais
notificações internas
preferências
auditoria geral
feature flags
11.3 Regras de negócio
empresa só opera após configuração mínima concluída;
cada tenant deve ter admin inicial;
permissões podem ser herdadas por perfil;
ações críticas exigem permissões explícitas;
mudanças estruturais devem ser auditadas.
11.4 Critérios de aceitação
criar empresa com sucesso;
convidar utilizador;
utilizador aceitar convite;
alternar entre empresas;
restringir acesso a módulo;
registar log de configuração.
12. Módulo 2 — Entidades
12.1 Objetivo

Gerir clientes, fornecedores, terceiros, entidades públicas e registos base para operação comercial e financeira.

12.2 Funcionalidades
cadastro de clientes
cadastro de fornecedores
cliente/fornecedor combinado
cliente indiferenciado / VD
múltiplos contactos
múltiplas moradas
dados fiscais
dados comerciais
condições de pagamento
limites de crédito
classificação/segmentação
anexos/documentos
histórico de alterações
12.3 Regras
NIF obrigatório conforme regras locais/configuração;
nome fiscal e nome comercial podem ser distintos;
cliente indiferenciado é entidade especial;
entidades com documentos certificados ficam com restrições em campos críticos;
permitir entidades nacionais e internacionais.
12.4 Critérios de aceitação
criar cliente regular;
criar fornecedor internacional;
emitir documento para cliente indiferenciado;
bloquear alteração de NIF após documento certificado.
13. Módulo 3 — Produtos e Serviços
13.1 Objetivo

Gerir o catálogo de bens, mercadorias, serviços e estruturas transacionáveis.

13.2 Funcionalidades
artigos stockáveis
serviços não stockáveis
kits/compostos
famílias/subfamílias
marcas/modelos
unidades
múltiplas unidades
preços
impostos
custos
armazém sugerido
controlo por lote
controlo por série
atributos
dimensões
estados do artigo
13.3 Regras
serviços não mexem stock;
mercadorias stockáveis exigem dados de inventário;
artigos com histórico fiscal não podem sofrer alterações destrutivas;
unidades devem respeitar fatores de conversão;
impostos devem poder variar por contexto.
13.4 Critérios de aceitação
criar artigo mercadoria;
criar serviço por hora;
configurar múltiplas unidades;
vender serviço sem movimento de stock;
rastrear artigo por série.
14. Módulo 4 — Vendas
14.1 Objetivo

Gerir o ciclo comercial ativo desde orçamento até cobrança e integração fiscal.

14.2 Funcionalidades
orçamento
encomenda de cliente
guia
fatura
fatura-recibo
talão de venda
nota de crédito
nota de débito
devolução
anulação controlada
estorno
working documents
POS
emissão por série
QR code
contingência
comunicação para motor fiscal
impressão/PDF/envio
14.3 Regras
séries documentais obrigatórias;
documentos fiscais devem obedecer ao regime local;
NC e ND referenciam documento origem quando aplicável;
documentos certificados não são editáveis;
numeração sequencial por série;
logs completos de emissão e rejeição;
cliente indiferenciado permitido em fluxos parametrizados.
14.4 Fluxos principais
Orçamento → Encomenda → Fatura
Guia → Fatura
Fatura → Recibo
Fatura → Nota de crédito
Documento em contingência → Reenvio posterior
14.5 Critérios de aceitação
emitir FT com sucesso;
emitir FR com liquidação imediata;
emitir TV;
emitir NC ligada à FT;
impedir edição após certificação;
gerar integração fiscal.
15. Módulo 5 — Compras
15.1 Objetivo

Gerir o ciclo passivo de aquisição de bens e serviços.

15.2 Funcionalidades
pedido de cotação
cotação
encomenda a fornecedor
receção
fatura de compra
devolução a fornecedor
custos adicionais
aprovação de compras
integração stock
integração conta corrente
integração contabilidade
15.3 Regras
compras de mercadoria podem atualizar stock;
compras de serviço não atualizam stock;
faturas de fornecedor podem gerar pendentes;
workflow pode depender de aprovação;
permitir receção antes da fatura.
15.4 Critérios de aceitação
registar compra de artigo;
registar compra de serviço;
criar pendente de fornecedor;
integrar compra na contabilidade;
rececionar artigo em armazém.
16. Módulo 6 — Inventário / Logística
16.1 Objetivo

Controlar entradas, saídas, transferências, reservas e valorização de stock.

16.2 Funcionalidades
armazéns
localizações
entradas
saídas
movimentos internos
transferências
trânsito
reservas
stock mínimo/máximo
reposição
lotes
números de série
inventário físico
inventário permanente
rastreabilidade
valorização
16.3 Regras
stock por tenant + armazém + artigo + lote/série;
transferências entre armazéns devem manter rastreabilidade;
contagem física deve gerar ajuste auditado;
serviços não podem entrar em stock;
política de rutura configurável.
16.4 Critérios de aceitação
entrada de stock;
saída por venda;
transferência de armazém;
inventário físico;
rastrear lote;
bloquear saída por stock insuficiente quando parametrizado.
17. Módulo 7 — Tesouraria / Caixa / Bancos
17.1 Objetivo

Controlar pendentes, cobranças, pagamentos, bancos e reconciliação.

17.2 Funcionalidades
contas correntes
pendentes
adiantamentos
liquidação total
liquidação parcial
compensações
transferências de pendentes
caixa
contas bancárias
movimentos bancários
cheques
depósitos
reconciliação manual
reconciliação automática
mapas de tesouraria
17.3 Regras
pendente nasce de documento ou lançamento manual;
liquidações não apagam histórico;
reconciliação relaciona movimentos sem destruir origem;
pagamentos e recebimentos podem integrar contabilidade;
bloqueio por limite de crédito deve ser suportado.
17.4 Critérios de aceitação
gerar pendente em venda;
liquidar parcialmente;
compensar valores;
criar movimento bancário;
reconciliar extrato com movimento interno.
18. Módulo 8 — Contabilidade
18.1 Objetivo

Manter o registo contabilístico estruturado, legal e integrado com os restantes módulos.

18.2 Funcionalidades
plano de contas
diários
documentos contabilísticos
movimentos manuais
lançamentos automáticos
integração com módulos
extratos
balancetes
razão
acumulados
apuramentos
fecho e abertura
centros de custo
modelos de lançamento
18.3 Regras
conta criada por exercício;
bloqueio de períodos;
integração automática parametrizada;
anulação e estorno com rastreabilidade;
separação entre movimento contabilístico e documento operacional;
prefixos e perfis configuráveis.
18.4 Critérios de aceitação
criar conta;
criar diário;
lançar documento manual;
integrar venda;
integrar compra;
bloquear mês;
gerar balancete.
19. Módulo 9 — Fiscalidade
19.1 Objetivo

Assegurar cálculo, validação, controlo e preparação declarativa fiscal.

19.2 Funcionalidades
regimes fiscais
configuração IVA
REMPE
retenções
documentos fiscais
regras de isenção
livros fiscais
apuramento fiscal
mapas
preparação declarativa
Modelo 106
validação de documentos
controlo de consistência fiscal
19.3 Regras
regime fiscal da empresa condiciona comportamento de cálculo;
REMPE tratado conforme parametrização legal aplicável;
IVA normal conforme taxas configuradas;
retenções conforme regras do país;
notas retificativas obedecem a referência e motivo;
preparação fiscal depende de dados íntegros.
19.4 Critérios de aceitação
configurar empresa em regime normal;
configurar empresa REMPE;
calcular imposto corretamente;
gerar base para Modelo 106;
emitir mapas fiscais por período.
20. Módulo 10 — e-Fatura / Middleware / DNRE
20.1 Objetivo

Permitir comunicação de documentos fiscais eletrónicos conforme o ecossistema da fatura eletrónica de Cabo Verde.

20.2 Fundamentação do produto

A documentação técnica da Fatura Eletrónica de Cabo Verde define que os DFEs são representados em XML, transmitidos por HTTPS/TLS, assinados digitalmente com certificado válido da ICP-CV, e que a plataforma valida estrutura, assinatura, dados e regras antes de autorizar o uso. O manual técnico também inclui capítulo específico para middleware e para emissão/consulta de DFEs e autofaturação.

20.3 Funcionalidades
configurar certificado digital
configurar credenciais/tokens
gerar XML DFE
assinar XML
enviar por middleware
consultar estado
tratar retorno
reenvio
contingência
logs técnicos
fila de envio
suporte a autofaturação
20.4 Regras
usar middleware quando o fluxo real assim exigir;
armazenar certificado de forma segura;
request e response devem ficar auditáveis;
documentos têm estado técnico;
contingência deve guardar motivo;
reenvio deve ser controlado;
integração assíncrona.
20.5 Critérios de aceitação
gerar XML válido;
assinar documento;
enviar via middleware;
receber autorização;
marcar rejeição;
permitir reprocessar documento rejeitado.
21. Módulo 11 — SAF-T CV
21.1 Objetivo

Gerar ficheiros SAF-T (CV) válidos para contabilidade, inventário e outros tipos previstos.

21.2 Fundamentação

A documentação base de FAQs SAF-T (CV) confirma os tipos de ficheiro previstos — Contabilidade, Inventário, Completo e Outros —, formato XML com UTF-8, exportação por exercício total ou parcial, submissão via SAFTPRO e regras específicas como uso de “0” em SoftwareCertificateNumber enquanto não existir certificação do software.

21.3 Funcionalidades
gerar SAF-T Contabilidade
gerar SAF-T Inventário
gerar SAF-T Completo
gerar SAF-T Outros
exportação por período
exportação por exercício
validação estrutural
histórico de geração
logs de falhas
reprocessamento
21.4 Regras
XML UTF-8;
obedecer à estrutura XSD vigente;
gerar por tenant e período;
dados devem ser consistentes;
exportação deve ser reproduzível;
tarefas pesadas em job assíncrono.
21.5 Critérios de aceitação
gerar ficheiro válido;
validar estrutura;
exportar por exercício parcial;
guardar histórico;
detetar inconsistências impeditivas.
22. Módulo 12 — Recursos Humanos
22.1 Objetivo

Gerir funcionários, processamento salarial e obrigações relacionadas.

22.2 Funcionalidades
ficha do funcionário
regimes e vínculos
remunerações
descontos
faltas
férias
horas extra
subsídios
processamento individual
processamento em lote
recibos
pagamentos
mapas
integração com contabilidade
22.3 Regras
processamento por período;
histórico de alterações;
dados sensíveis protegidos por permissão;
regras laborais parametrizáveis;
possibilidade futura de adaptação por país.
22.4 Critérios de aceitação
criar funcionário;
processar salário mensal;
gerar recibo;
anular processamento quando permitido;
integrar movimento contabilístico.
23. Módulo 13 — Ativos
23.1 Objetivo

Gerir ativos fixos e equipamentos durante todo o seu ciclo de vida.

23.2 Funcionalidades
ficha do bem
aquisição
critérios de depreciação
planos
classes
reavaliação
manutenção
alienação
abate
sinistro
mapas legais
integração contabilidade
23.3 Regras
cálculo de depreciações por critérios definidos;
histórico integral do ativo;
integração com contabilidade;
restrições a alterações após certos estados.
23.4 Critérios de aceitação
criar ativo;
registar aquisição;
calcular depreciação;
gerar integração contabilística.
24. Módulo 14 — Projetos
24.1 Objetivo

Acompanhar projetos, custos, equipas e rentabilidade.

24.2 Funcionalidades
cadastro de projeto
fases
tarefas
orçamento
custos
receitas
timesheets
centro de custo
faturação por projeto
dashboards
24.3 Critérios de aceitação
criar projeto;
associar custo;
associar venda;
calcular margem.
25. Módulo 15 — Subscrições SaaS do próprio ERP
25.1 Objetivo

Permitir comercialização do NOVA-ERP como produto SaaS por planos.

25.2 Funcionalidades
planos
módulos por plano
limites
trial
ativação
renovação
upgrade/downgrade
suspensão
reativação
feature flags
billing interno
25.3 Regras
o tenant herda permissões funcionais do plano;
limites devem ser aplicáveis sem perda de dados;
incumprimento pode bloquear operação parcialmente.
25.4 Critérios de aceitação
criar plano;
associar tenant ao plano;
ativar módulos;
aplicar limite funcional.
26. Módulo 16 — Relatórios, Dashboards e Analytics
26.1 Objetivo

Disponibilizar visão operacional, financeira e fiscal em tempo útil.

26.2 Funcionalidades
dashboard executivo
dashboard comercial
dashboard financeiro
dashboard fiscal
dashboard stock
dashboard RH
filtros por período
exportações
relatórios detalhados
KPIs
26.3 Critérios de aceitação
dashboard de vendas;
dashboard tesouraria;
dashboard stock;
dashboard fiscal;
exportar relatório.
27. Módulo 17 — IA / Assistente ERP
27.1 Objetivo

Aumentar produtividade, controlo e capacidade analítica com IA.

27.2 Casos de uso
sugerir classificação contabilística;
detetar inconsistência fiscal;
prever rutura de stock;
sugerir cobrança;
responder perguntas em linguagem natural;
resumir indicadores;
apoiar reconciliações;
gerar alertas de risco.
27.3 Regras
IA não altera dados críticos automaticamente;
sugestões devem ser confirmáveis;
outputs devem ser auditáveis;
acesso respeita permissões do utilizador.
27.4 Critérios de aceitação
pergunta em linguagem natural responde com base autorizada;
sugestão contabilística apresentada com contexto;
alerta de risco fiscal registado.
28. Requisitos Não Funcionais
28.1 Segurança
RBAC por tenant
proteção de segredos
gestão segura de certificados
logs de segurança
prevenção de acesso cruzado
controlo de sessão
políticas de password e MFA futuro
28.2 Performance
páginas principais rápidas
geração assíncrona para relatórios pesados
queries indexadas
paginação
cache seletiva
filas para integrações
28.3 Escalabilidade
suportar crescimento em número de tenants
suportar múltiplas empresas por utilizador
suportar grande volume de documentos
possibilidade futura de particionamento
28.4 Disponibilidade
retries
observabilidade
monitorização
fallback em integrações
contingência documental
backups
28.5 Auditabilidade
before/after
logs técnicos
logs funcionais
histórico por entidade
histórico por documento
histórico por configuração
29. Requisitos de Dados
29.1 Regras gerais
todas as entidades transacionais com tenant_id;
timestamps obrigatórios;
soft delete apenas onde fizer sentido;
versionamento onde necessário;
estados explícitos;
consistência referencial.
29.2 Campos transversais desejáveis
id
tenant_id
created_at
updated_at
created_by
updated_by
status
version
external_reference quando aplicável
30. Requisitos de Integração
30.1 Integrações internas
vendas ↔ stock
compras ↔ stock
vendas ↔ tesouraria
compras ↔ tesouraria
tesouraria ↔ contabilidade
vendas ↔ fiscalidade
contabilidade ↔ SAF-T
RH ↔ contabilidade
ativos ↔ contabilidade
30.2 Integrações externas
middleware e-Fatura
certificação/assinatura
SAF-T / SAFTPRO
pagamentos online
importação/exportação Excel
notificações email/SMS
31. Fluxos Críticos
31.1 Onboarding de empresa
criar tenant
definir país e moeda
definir regime fiscal
ativar módulos
criar admin
configurar séries, impostos, armazéns, contas
sistema apto a operar
31.2 Emissão de fatura
selecionar cliente
selecionar série e documento
inserir linhas
validar fiscalmente
gravar
gerar estados/documento
enviar ao motor fiscal se aplicável
guardar retorno
31.3 Compra com impacto em stock e contabilidade
criar/receber documento
validar fornecedor
lançar linhas
atualizar stock
gerar pendente
integrar contabilidade
31.4 Geração SAF-T
escolher tipo
escolher período
validar dados
gerar XML
armazenar histórico
disponibilizar download
32. Dependências
32.1 Dependências de produto
motor multi-tenant estável;
master data base;
engine documental;
motor fiscal;
auditoria;
permissões.
32.2 Dependências externas
regras legais vigentes;
fluxos DNRE/e-Fatura;
certificados digitais;
XSDs aplicáveis;
meios de pagamento externos quando integrados.
33. Riscos
regras fiscais mudarem;
integração externa ter limitações;
complexidade excessiva cedo demais;
mistura entre lógica fiscal e UI;
falhas em isolamento multi-tenant;
má qualidade do modelo de dados;
permissões mal desenhadas;
crescimento sem observabilidade.
34. Roadmap por Fases
Fase 1 — Core
multi-tenant
auth
permissões
empresas
utilizadores
auditoria
configuração geral
Fase 2 — Master Data
entidades
produtos/serviços
séries
impostos
armazéns
documentos base
Fase 3 — Operação Comercial
vendas
compras
inventário
contas correntes
tesouraria base
Fase 4 — Fiscal Núcleo
regras documentais
IVA/REMPE
Modelo 106 base
e-Fatura base
SAF-T base
Fase 5 — Financeira Completa
contabilidade
reconciliação
fechos
relatórios financeiros
Fase 6 — RH / Ativos / Projetos
módulos complementares
Fase 7 — IA e automação
copiloto ERP
previsões
alertas inteligentes
35. MVP Recomendado
MVP funcional
plataforma base
multi-tenant
utilizadores/permissões
entidades
produtos/serviços
vendas
compras
inventário base
tesouraria base
fiscalidade base
e-Fatura base
SAF-T base
dashboards essenciais
Não incluir no MVP
RH completo
ativos avançados
projetos completos
IA avançada
billing SaaS sofisticado
36. Definition of Done

Uma feature só está concluída quando:

cumpre o PRD;
tem regras de negócio validadas;
tem controlo multi-tenant;
respeita permissões;
gera auditoria;
tem tratamento de erro;
tem estados claros na UI;
tem testes mínimos;
está integrada com dependências;
não quebra conformidade fiscal.
37. Anexos de Contexto Regulatório do Produto

A documentação técnica de e-Fatura de Cabo Verde descreve que os documentos fiscais eletrónicos são estruturados em XML, transmitidos em canal seguro HTTPS/TLS, assinados digitalmente com certificado válido da ICP-CV, e passam por validações de estrutura, assinatura, tipos de dados, NIFs, códigos, taxas e totais antes de autorização. Também lista os tipos documentais como FTE, FRE, TVE, RCE, NCE, NDE, DVE e DTE, e inclui capítulos para APIs, middleware e autofaturação.

O material de enquadramento da fatura eletrónica indica o ciclo de vida do DFE — criação, validação offline, assinatura, emissão, transmissão, validação online, timestamp, autorização, receção, manifestação e arquivo — e reforça a exigência de certificado digital, contingência e posterior transmissão dos DFEs emitidos em contingência.

O manual orientador de faturação em Cabo Verde consolida regras como obrigação de emissão de fatura por transmissões de bens, prestações de serviços e pagamentos antecipados, prazo geral de emissão até ao 5.º dia útil seguinte ao facto gerador, requisitos mínimos de conteúdo da fatura, numeração sequencial, série e regras sobre talões de venda e dispensa de faturação em casos específicos.

As FAQs de SAF-T (CV) confirmam a obrigatoriedade para sujeitos passivos abrangidos, os tipos de ficheiro previstos, formato XML UTF-8, submissão via SAFTPRO, possibilidade de exportação por período e regras práticas relevantes para implementação, como o uso de “0” no número de certificado do software enquanto não houver certificação atribuída.

38. Conclusão

O NOVA-ERP deve ser construído como uma plataforma ERP moderna, modular, auditável e fiscalmente nativa para Cabo Verde. O produto não deve ser apenas um sistema de faturação ou gestão comercial: deve ser uma base operacional completa, com integração entre módulos, motor fiscal sólido, capacidade SaaS multi-tenant e evolução clara para automação e IA.

Este PRD serve como referência central para:

arquitetura funcional;
planeamento de roadmap;
alinhamento entre produto e desenvolvimento;
criação de prompts para Lovable/Codex/Claude Code;
transformação em backlog épico → feature → user story.