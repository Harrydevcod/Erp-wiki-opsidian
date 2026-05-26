Backlog Estruturado — NOVA-ERP
ÉPICO 1 — Plataforma Base Multi-Tenant
Feature 1.1 — Criar tenant/empresa

User Story 1.1.1
Como administrador da plataforma, quero criar uma nova empresa para iniciar a operação no ERP.

Critérios de aceitação

deve permitir criar empresa com nome, NIF, país, moeda base e regime fiscal;
deve gerar tenant_id único;
deve criar utilizador admin inicial;
deve registar auditoria da criação;
a empresa deve ficar em estado setup_pending até concluir configuração mínima.

User Story 1.1.2
Como administrador, quero concluir o onboarding inicial da empresa para a tornar operacional.

Critérios de aceitação

deve validar se existem séries, impostos e pelo menos um utilizador ativo;
deve permitir marcar setup como concluído;
empresa só fica operacional após todas as dependências mínimas estarem satisfeitas.
Feature 1.2 — Gestão de utilizadores

User Story 1.2.1
Como admin da empresa, quero convidar utilizadores para acederem ao meu tenant.

Critérios de aceitação

convite por email;
convite associado a tenant específico;
convite com validade configurável;
utilizador aceita convite e fica ligado ao tenant;
ação auditada.

User Story 1.2.2
Como utilizador com acesso a várias empresas, quero alternar entre tenants sem novo login.

Critérios de aceitação

deve listar apenas empresas às quais o utilizador pertence;
ao trocar de tenant, todos os dados devem ser filtrados pelo novo tenant_id;
não pode haver fuga de contexto entre empresas.
Feature 1.3 — Perfis e permissões

User Story 1.3.1
Como admin, quero criar perfis com permissões por módulo e ação.

Critérios de aceitação

permissões por visualizar, criar, editar, anular, exportar, aprovar;
perfis reutilizáveis;
permissões avaliadas por tenant;
alterações ficam auditadas.

User Story 1.3.2
Como sistema, quero bloquear ações não autorizadas.

Critérios de aceitação

utilizador sem permissão não vê ou não executa ação;
API também deve validar permissão;
tentativa bloqueada pode ser registada em log de segurança.
Feature 1.4 — Auditoria

User Story 1.4.1
Como auditor, quero consultar histórico de alterações relevantes.

Critérios de aceitação

registo com tenant_id, ator, data/hora, entidade, ação;
para alterações críticas, guardar before/after;
pesquisa por período, utilizador e entidade.
ÉPICO 2 — Entidades
Feature 2.1 — Cadastro de clientes e fornecedores

User Story 2.1.1
Como operador, quero criar um cliente com dados comerciais e fiscais.

Critérios de aceitação

campos mínimos: código, nome, NIF, morada, contactos;
validação de unicidade por código e NIF conforme regras;
estado ativo/inativo;
auditoria de criação.

User Story 2.1.2
Como operador, quero criar um fornecedor internacional.

Critérios de aceitação

deve aceitar país estrangeiro;
deve permitir NIF externo ou identificador alternativo;
deve suportar moeda e condições de pagamento próprias.
Feature 2.2 — Cliente indiferenciado

User Story 2.2.1
Como operador POS/vendas, quero emitir para cliente indiferenciado.

Critérios de aceitação

sistema deve suportar entidade especial tipo VD/cliente indiferenciado;
documento pode permitir preenchimento manual de nome/NIF conforme configuração;
fluxo deve respeitar regras fiscais aplicáveis.
Feature 2.3 — Proteção de campos críticos

User Story 2.3.1
Como sistema, quero impedir alteração destrutiva de dados fiscais após documentos certificados.

Critérios de aceitação

bloquear alteração de NIF em entidades com documentos fiscais certificados;
alterações críticas só via fluxo controlado;
mensagem clara ao utilizador.
ÉPICO 3 — Produtos e Serviços
Feature 3.1 — Cadastro de artigos

User Story 3.1.1
Como operador, quero criar um artigo stockável.

Critérios de aceitação

campos mínimos: código, descrição, tipo, unidade, imposto;
pode associar família, subfamília, armazém padrão;
artigo fica disponível para compras, vendas e stock segundo configuração.

User Story 3.1.2
Como operador, quero criar um serviço não stockável.

Critérios de aceitação

tipo serviço;
não gera movimentos de stock;
pode ser usado em compras e vendas.
Feature 3.2 — Unidades e conversões

User Story 3.2.1
Como operador, quero definir unidades de compra e venda diferentes da unidade base.

Critérios de aceitação

unidade base obrigatória;
fatores de conversão configuráveis;
stock expresso sempre na unidade base;
após movimentos, unidade base não pode ser alterada livremente.
Feature 3.3 — Lotes e séries

User Story 3.3.1
Como responsável de armazém, quero controlar artigos por lote.

Critérios de aceitação

entrada e saída por lote;
rastreabilidade;
consulta de validade e stock por lote.

User Story 3.3.2
Como responsável de armazém, quero controlar artigos por número de série.

Critérios de aceitação

entrada com série;
saída com série;
rastreamento histórico por número de série.
ÉPICO 4 — Vendas
Feature 4.1 — Emissão de documentos de venda

User Story 4.1.1
Como operador comercial, quero emitir uma fatura.

Critérios de aceitação

selecionar entidade, série, documento e linhas;
cálculo automático de totais e impostos;
gravação do documento com número sequencial;
geração de PDF/impressão.

User Story 4.1.2
Como operador, quero emitir uma fatura-recibo.

Critérios de aceitação

documento deve gerar faturação e liquidação imediata;
criação do movimento financeiro correspondente;
estados coerentes entre venda e tesouraria.

User Story 4.1.3
Como operador POS, quero emitir talão de venda.

Critérios de aceitação

fluxo rápido;
suporte a cliente indiferenciado;
integração com caixa.
Feature 4.2 — Notas de crédito e débito

User Story 4.2.1
Como operador, quero emitir uma nota de crédito referenciando a fatura original.

Critérios de aceitação

documento origem obrigatório quando aplicável;
linhas e valores consistentes;
impacto fiscal e financeiro refletido corretamente.

User Story 4.2.2
Como operador, quero emitir nota de débito.

Critérios de aceitação

referência ao documento original quando aplicável;
motivo registado;
cálculo fiscal coerente.
Feature 4.3 — Imutabilidade documental

User Story 4.3.1
Como sistema, quero impedir edição de documento fiscal certificado.

Critérios de aceitação

após certificação/autorização, documento fica bloqueado;
apenas ações permitidas: consulta, impressão, emissão de retificativo;
tentativas de edição rejeitadas.
Feature 4.4 — Circuito documental

User Story 4.4.1
Como utilizador, quero converter orçamento em encomenda e fatura.

Critérios de aceitação

possibilidade de reprodução/transformação;
histórico de origem/destino;
quantidades não podem exceder regras configuradas.
ÉPICO 5 — Compras
Feature 5.1 — Registo de documentos de compra

User Story 5.1.1
Como responsável de compras, quero registar fatura de fornecedor.

Critérios de aceitação

seleção de fornecedor, documento, série e linhas;
cálculo de impostos;
geração de pendente em conta corrente conforme configuração;
integração com contabilidade opcional/automática.

User Story 5.1.2
Como responsável de compras, quero registar compra de serviço.

Critérios de aceitação

não gerar stock;
gerar custo e pendente;
integrar contabilisticamente.
Feature 5.2 — Receções

User Story 5.2.1
Como armazém, quero rececionar mercadoria antes da fatura.

Critérios de aceitação

atualizar stock;
manter ligação à encomenda/receção;
posterior fatura deve poder reconciliar-se com a receção.
ÉPICO 6 — Inventário / Logística
Feature 6.1 — Movimentos de stock

User Story 6.1.1
Como armazém, quero registar entrada de stock.

Critérios de aceitação

selecionar armazém e artigo;
atualizar quantidades;
suportar lote/série quando exigido;
ação auditada.

User Story 6.1.2
Como armazém, quero registar saída de stock.

Critérios de aceitação

validar disponibilidade;
respeitar política de rutura;
registar rastreabilidade.
Feature 6.2 — Transferências

User Story 6.2.1
Como armazém, quero transferir stock entre armazéns.

Critérios de aceitação

documento de origem e destino;
suporte a trânsito quando configurado;
manter lote/série.
Feature 6.3 — Inventário físico

User Story 6.3.1
Como responsável de stock, quero fazer contagem física e ajuste.

Critérios de aceitação

criar sessão de inventário;
registar contagens;
calcular diferenças;
gerar ajuste auditado após fecho.
ÉPICO 7 — Tesouraria / Contas Correntes / Bancos
Feature 7.1 — Pendentes

User Story 7.1.1
Como financeiro, quero gerar pendentes automaticamente a partir de vendas e compras.

Critérios de aceitação

venda gera pendente de cliente;
compra gera pendente de fornecedor;
pendentes visíveis em conta corrente.
Feature 7.2 — Liquidações

User Story 7.2.1
Como financeiro, quero liquidar totalmente uma fatura.

Critérios de aceitação

selecionar documento pendente;
gerar documento de liquidação;
pendente fica fechado;
integração com caixa/banco quando aplicável.

User Story 7.2.2
Como financeiro, quero liquidar parcialmente uma fatura.

Critérios de aceitação

saldo remanescente permanece pendente;
histórico de liquidações parciais visível;
totais sempre coerentes.
Feature 7.3 — Limite de crédito

User Story 7.3.1
Como gestor financeiro, quero definir limite de crédito por cliente.

Critérios de aceitação

configurar valor limite;
no registo de venda o sistema deve bloquear, avisar ou ignorar conforme parametrização;
cálculo considera saldo pendente atual.
Feature 7.4 — Reconciliação bancária

User Story 7.4.1
Como financeiro, quero reconciliar movimentos bancários manualmente.

Critérios de aceitação

listar movimentos internos e extrato;
associar movimentos;
marcar estado reconciliado;
não altera lançamento original.

User Story 7.4.2
Como financeiro, quero reconciliação automática por regras.

Critérios de aceitação

regras por valor, data, referência;
sugestões automáticas;
confirmação humana antes do fecho final.
ÉPICO 8 — Contabilidade
Feature 8.1 — Plano de contas

User Story 8.1.1
Como contabilista, quero criar contas no plano de contas.

Critérios de aceitação

criação por exercício;
validação estrutural do código;
impedir anulação de conta com movimentos.
Feature 8.2 — Lançamentos manuais

User Story 8.2.1
Como contabilista, quero lançar documento manualmente.

Critérios de aceitação

selecionar exercício, diário e documento;
introduzir contas débito/crédito;
validar equilíbrio;
gravar e numerar automaticamente.
Feature 8.3 — Integrações automáticas

User Story 8.3.1
Como contabilista, quero integrar vendas automaticamente na contabilidade.

Critérios de aceitação

documento operacional gera lançamento contabilístico conforme parametrização;
ligação entre documento origem e lançamento;
erros de integração devem ser visíveis e reprocessáveis.
Feature 8.4 — Bloqueios

User Story 8.4.1
Como contabilista, quero bloquear períodos contabilísticos.

Critérios de aceitação

bloqueio por mês, diário ou exercício;
impedir lançamentos em período bloqueado;
ação auditada.
ÉPICO 9 — Fiscalidade
Feature 9.1 — Configuração do regime fiscal

User Story 9.1.1
Como admin/contabilista, quero configurar a empresa em regime normal.

Critérios de aceitação

regime armazenado por tenant;
regras de cálculo fiscal adaptadas;
histórico de alterações de regime.

User Story 9.1.2
Como admin/contabilista, quero configurar a empresa em REMPE.

Critérios de aceitação

deve refletir comportamento fiscal parametrizado para REMPE;
restrições e cálculos aplicáveis devem ser ativados.
Feature 9.2 — Modelo 106

User Story 9.2.1
Como responsável fiscal, quero gerar os dados base para a Modelo 106.

Critérios de aceitação

apurar campos com base nas operações do período;
permitir revisão antes de exportação;
manter rastreabilidade dos valores apurados.
Feature 9.3 — Validação fiscal

User Story 9.3.1
Como sistema, quero validar coerência fiscal antes do fecho.

Critérios de aceitação

verificar documentos, impostos, totais e consistência mínima;
listar erros e avisos;
impedir fecho quando houver erros críticos.
ÉPICO 10 — e-Fatura / Middleware / DNRE
Feature 10.1 — Configuração técnica

User Story 10.1.1
Como admin técnico, quero configurar certificado digital e credenciais.

Critérios de aceitação

armazenamento seguro;
validação básica do ficheiro/certificado;
permissões restritas de acesso.
Feature 10.2 — Geração e envio de DFE

User Story 10.2.1
Como sistema, quero gerar XML do documento fiscal eletrónico.

Critérios de aceitação

estrutura compatível com tipologia documental;
campos obrigatórios preenchidos;
histórico da geração.

User Story 10.2.2
Como sistema, quero enviar DFE via middleware.

Critérios de aceitação

fila assíncrona;
guardar request/response;
atualizar estado técnico do documento.
Feature 10.3 — Contingência

User Story 10.3.1
Como operador, quero emitir documento em contingência.

Critérios de aceitação

registar motivo;
marcar documento como contingência;
permitir reenvio posterior;
histórico do reenvio.
Feature 10.4 — Tratamento de resposta

User Story 10.4.1
Como sistema, quero marcar documento como autorizado ou rejeitado.

Critérios de aceitação

estados possíveis: pendente, em fila, enviado, autorizado, rejeitado, contingência;
rejeição deve guardar motivo técnico;
permitir reprocessamento controlado quando aplicável.
ÉPICO 11 — SAF-T CV
Feature 11.1 — Exportação SAF-T

User Story 11.1.1
Como responsável fiscal, quero gerar SAF-T de contabilidade.

Critérios de aceitação

escolha de período/exercício;
geração XML UTF-8;
histórico da exportação.

User Story 11.1.2
Como responsável fiscal, quero gerar SAF-T de inventário.

Critérios de aceitação

exportar dados de inventário válidos;
respeitar estrutura exigida;
permitir download.
Feature 11.2 — Validação

User Story 11.2.1
Como sistema, quero validar ficheiro SAF-T antes de disponibilizar.

Critérios de aceitação

validação estrutural;
deteção de erros impeditivos;
relatório de inconsistências.
ÉPICO 12 — RH
Feature 12.1 — Cadastro de funcionário

User Story 12.1.1
Como RH, quero criar ficha de funcionário.

Critérios de aceitação

dados pessoais, fiscais, contratuais e de pagamento;
estado ativo/inativo;
histórico de alterações relevante.
Feature 12.2 — Processamento salarial

User Story 12.2.1
Como RH, quero processar salários em lote.

Critérios de aceitação

por período;
cálculo de remunerações e descontos;
geração de recibos;
bloqueio de reprocessamento indevido.
ÉPICO 13 — Ativos
Feature 13.1 — Gestão de ativos

User Story 13.1.1
Como financeiro, quero criar ficha de ativo.

Critérios de aceitação

tipo, classificação, conta e critérios de depreciação;
estado do ativo;
histórico de ciclo de vida.

User Story 13.1.2
Como financeiro, quero calcular depreciação.

Critérios de aceitação

cálculo segundo plano configurado;
integração opcional com contabilidade;
registo auditável.
ÉPICO 14 — Projetos
Feature 14.1 — Gestão de projeto

User Story 14.1.1
Como gestor, quero criar um projeto com fases e orçamento.

Critérios de aceitação

código e nome do projeto;
fases;
orçamento base;
estado do projeto.

User Story 14.1.2
Como gestor, quero associar custos e receitas ao projeto.

Critérios de aceitação

custos e receitas visíveis por projeto;
cálculo de margem/rentabilidade.
ÉPICO 15 — Subscrições SaaS
Feature 15.1 — Planos

User Story 15.1.1
Como admin SaaS, quero criar planos de subscrição.

Critérios de aceitação

nome do plano;
preço;
módulos incluídos;
limites configuráveis.

User Story 15.1.2
Como admin SaaS, quero atribuir plano a um tenant.

Critérios de aceitação

ativar/desativar módulos conforme plano;
aplicar limites sem apagar dados;
alterações auditadas.
ÉPICO 16 — Dashboards e Relatórios
Feature 16.1 — Dashboard executivo

User Story 16.1.1
Como gestor, quero ver dashboard com vendas, cobranças, compras e stock.

Critérios de aceitação

filtros por período;
KPIs principais;
navegação para detalhe.
ÉPICO 17 — IA / Assistente ERP
Feature 17.1 — Assistente operacional

User Story 17.1.1
Como utilizador, quero perguntar em linguagem natural sobre dados do ERP.

Critérios de aceitação

resposta respeita permissões do utilizador;
indicar contexto/âmbito da resposta;
não expor dados de outro tenant.

User Story 17.1.2
Como contabilista/fiscal, quero receber sugestões automáticas de classificação ou alerta.

Critérios de aceitação

sugestão não executa sem confirmação;
guardar histórico da sugestão;
permitir aceitar ou rejeitar.
Priorização sugerida
MVP fase 1
Épico 1
Épico 2
Épico 3
Épico 4
Épico 5
Épico 6
Épico 7
Épico 9
Épico 10
Épico 11
fase 2
Épico 8
Épico 16
Épico 15
fase 3
Épico 12
Épico 13
Épico 14
Épico 17