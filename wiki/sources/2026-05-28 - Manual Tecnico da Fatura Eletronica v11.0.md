---
type: source
status: active
created: 2026-05-28
updated: 2026-05-28
source_path: https://efatura.cv/assets/files/manual-tecnico-da-fatura-eletronica-v11.0-be67e62c7fb34552fbcc8eeea966e217.pdf
source_type: technical-manual
author: Direcao Nacional de Receitas do Estado / Grupo de Trabalho FE
published: 2025-03-14
ingested: 2026-05-28
tags: [source, efatura, cabo-verde, dfe, dnre, compliance, api, schema]
related: ["[[e-Fatura Cabo Verde]]", "[[Faturacao Eletronica]]", "[[Fiscalidade Cabo Verde]]", "[[DNRE]]", "[[2026-05-28 - Pacote XML XSD e-Fatura 2024-05-27]]", "[[2026-05-28 - Vigencia do Manual de Faturas 2018 apos e-Fatura]]"]
confidence: high
---

# Manual Tecnico da Fatura Eletronica v11.0

## Summary

Manual tecnico oficial da e-Fatura Cabo Verde, versao v11.0, publicado em 2025-03-14 e listado em 2026-05-28 como a versao mais recente na pagina oficial de manuais.

Esta fonte substitui [[2026-05-27 - Manual Tecnico da Fatura Eletronica v10.0]] como autoridade tecnica atual para schema/API. A v10.0 continua util como historico, mas implementacao real deve seguir v11.0 e o pacote XSD oficial em [[2026-05-28 - Pacote XML XSD e-Fatura 2024-05-27]].

Source: https://efatura.cv/docs/manual/

## Version Delta From v10.0

O historico de v11.0 registra:

- atualizacao de `IssueReasonCode`;
- inclusao do composto `RappelPeriod` para notas de credito por rappel;
- inclusao do scope OAuth `cv_ef_dfe_self_billing_authorize`;
- inclusao do scope OAuth `cv_ef_opacc_read_accountant_list`;
- atualizacao dos links de download do middleware.

## Architecture Role

O manual define o contrato tecnico para Documento Fiscal Eletronico (DFE), eventos, validacao, assinatura digital, autorizacao, contingencia, API REST e middleware.

Pontos estruturais:

- o DFE e representado em XML e validado por XSD;
- a comunicacao usa HTTPS/TLS;
- os documentos e eventos exigem assinatura XMLDSig com XAdES-BES;
- a chave de assinatura deve estar associada a certificado da cadeia ICP-CV para validade em producao;
- a Plataforma da e-Fatura (PE) valida e autoriza de forma sincrona apos a submissao;
- o ERP pode ter filas internas, mas cada tentativa PE/middleware e uma tentativa de autorizacao sincrona;
- contingencia nao e apenas retry tecnico: e um modo fiscal oficial com campos e efeitos proprios.

## XML Root Contract

O XML deve seguir W3C XML 1.0 em UTF-8. O namespace raiz e:

```xml
urn:cv:efatura:xsd:v1.0
```

A raiz DFE declara:

- `Version` - obrigatorio; valor `1.0` ate alteracao oficial;
- `Id` - obrigatorio; IUD com exatamente 45 caracteres;
- `DocumentTypeCode` - obrigatorio; valores 1 a 9.

Recomendacoes oficiais de geracao XML:

- validar localmente contra XSD antes de submeter;
- nao incluir comentarios;
- nao incluir zeros insignificantes;
- nao incluir espacos desnecessarios;
- nao formatar com indentacao;
- evitar prefixes de namespace salvo onde o schema exige, como assinatura.

## DFE Type Vocabulary

Tipos oficiais:

- `FTE` - Fatura Eletronica;
- `FRE` - Fatura Recibo Eletronica;
- `TVE` - Talao de Venda Eletronico;
- `RCE` - Recibo Eletronico;
- `NCE` - Nota de Credito Eletronica;
- `NDE` - Nota de Debito Eletronica;
- `DVE` - Nota de Devolucao;
- `DTE` - Documento de Transporte Eletronico;
- `NLE` - Nota de Lancamento.

Implicacao para NOVA-ERP: mesmo que o MVP exponha apenas um subconjunto comercial, a modelagem base deve acomodar todo o vocabulario oficial para evitar migracoes fiscais mal desenhadas.

## Identification, Numbering And Series

Contratos relevantes:

- `Id`/IUD tem exatamente 45 caracteres.
- IUD e composto por elementos como pais, repositorio, data, NIF, LED, tipo de documento, numero, codigo aleatorio e digito de controlo Luhn.
- `LedCode` e obrigatorio, maximo 5 digitos, e representa logica/serie de emissao previamente registrada na PE.
- `Serie` e obrigatoria, maximo 20 caracteres alfanumericos, permitindo letras, numeros, `-` e `_`, sem espacos.
- `DocumentNumber` e obrigatorio, maximo 9 digitos, maior ou igual a 1.
- A numeracao deve ser sequencial, sem falhas, por `(NIF, ano, LED, tipo de documento)`.
- A sequencia reinicia anualmente.
- A unicidade fiscal e por `(NIF, ano, LED, tipo de documento, numero de documento)`.

NOVA-ERP deve tratar atribuicao de numero fiscal como evento atomico e auditavel, separado de draft e separado de tentativa de transmissao.

## Issue Date And Time Rules

Para emissao online:

- `IssueDate`/`IssueTime` nao pode estar mais de 1 hora no futuro em relacao ao SFECV;
- nao pode estar mais de 24 horas no passado.

Para contingencia:

- data/hora de emissao deve estar dentro da janela permitida de 7 dias no passado.

## Document Groups

O manual organiza o DFE em grupos como:

- identificacao do documento;
- emissor;
- recetor;
- transportador/prestador de transporte;
- pagamento;
- linhas/itens;
- totais;
- software;
- contingencia;
- campos personalizados;
- transmissao;
- assinatura.

Regras de obrigatoriedade importantes:

- `EmitterParty` e obrigatorio;
- `ReceiverParty` e obrigatorio exceto nos casos admitidos para TVE;
- `Line` e obrigatorio exceto RCE;
- `Totals` e obrigatorio exceto RCE e DTE;
- `TransportRoute` e obrigatorio em DTE;
- `Reference` aplica FTE/FRE/RCE/NCE/NDE/DVE; e obrigatorio nos documentos corretivos/devolutivos;
- `Payments` aplica FTE/FRE/TVE/RCE/NLE;
- `Delivery` aplica FTE/FRE/TVE;
- `Transmission` e obrigatorio;
- `RepositoryCode` e obrigatorio;
- `Signature` e obrigatorio.

## Emitter And Receiver

Emissor:

- NIF deve ser de Cabo Verde;
- NIF deve existir e estar ativo;
- atividade e enquadramento fiscal devem permitir emissao;
- email e obrigatorio;
- pelo menos telefone ou telemovel e obrigatorio.

Recetor:

- em regra e obrigatorio;
- TVE permite excecoes;
- para TVE, recetor e obrigatorio quando total e igual ou superior a 20.000 ECV;
- desde 2022 a regra de identificacao em TVE aplica-se a todos os contribuintes conforme manual.

Endereco:

- `AddressDetail` e obrigatorio;
- se `CountryCode=CV`, `AddressCode` e obrigatorio, tem exatamente 20 caracteres e deve corresponder a Lista de Lugares em Cabo Verde.

## Tax, Lines And Totals

Codigos de imposto:

- `NA`;
- `IVA`;
- `IS`;
- `IR`.

Regra REMPE relevante: quando contribuinte REMPE emite fatura, `TaxTypeCode` deve ser `NA`, com justificacao fiscal.

Linhas:

- `LineTypeCode` pode ser `N` normal, `C` encargo, `D` deducao, `I` informacao;
- se omitido, assume normal;
- linha de encargo exige `LineReferenceId`;
- quantidade obrigatoria e maior que zero;
- unidade obrigatoria;
- preco, extensao de preco e total liquido obrigatorios exceto onde o documento dispensa, como DTE;
- imposto e obrigatorio exceto DTE/NCE/DVE conforme schema/regras;
- item e descricao sao obrigatorios;
- identificacao interna do emissor e obrigatoria;
- identificacao standard e opcional agora, mas indicada como futura obrigatoriedade quando houver tabela padronizada cabo-verdiana.

Totais:

- `PriceExtensionTotalAmount`;
- `ChargeTotalAmount`;
- `DiscountTotalAmount`;
- `NetTotalAmount`;
- `TaxTotalAmount`;
- `PayableAmount`;
- `WithholdingTaxTotalAmount` opcional;
- `PayableAlternativeAmount` repetivel para moeda alternativa e cambio.

Valores decimais aceitam ate 5 casas decimais; percentagens aceitam ate 3 casas e intervalo 0 a 100.

## IssueReasonCode And RappelPeriod

v11.0 atualiza os motivos de emissao para documentos corretivos/devolutivos.

`IssueReasonCode` e obrigatorio em `NCE`, `NDE` e `DVE`.

Valores atuais capturados do manual:

- `2` - Art. 65 n. 2 CIVA; NCE, NDE, DVE;
- `3` - Art. 65 n. 3 CIVA; NCE, NDE, DVE;
- `4` - Art. 65 n. 4 CIVA; NDE;
- `6` - Art. 65 n. 6 CIVA; NCE, NDE, DVE;
- `7` - Art. 65 n. 7 CIVA; NCE, DVE;
- `8` - Art. 65 n. 8 CIVA; NCE, NDE, DVE;
- `9` - Art. 65 n. 9 CIVA; NCE, NDE, DVE;
- `DD` - Debito de Despesas; NDE;
- `IN` - Indisponivel; NCE, NDE, DVE, regime transitorio;
- `DRP` - Desconto por Rappel; NCE;
- `0` - Outro; DVE.

Para DVE, quando nenhum motivo especifico se aplica, usar `0` e preencher `IssueReasonDescription`.

`RappelPeriod` e um composto novo associado a `NCE` para desconto por rappel. O pacote XSD confirma que e opcional no schema e deve ser usado apenas em NCE.

Implicacao para NOVA-ERP: notas de credito por rappel precisam de campos proprios de periodo (`StartDate`, `EndDate`) e nao devem ser tratadas como nota de credito generica com texto livre.

## References

Referencias aplicam a FTE/FRE/RCE/NCE/NDE/DVE.

Regras centrais:

- em documentos corretivos/devolutivos a referencia e obrigatoria;
- pelo menos um destes deve existir: `FiscalDocument`, `PaymentAmount` ou `Tax`;
- `InnerDocumentNumber` isolado nao basta;
- `FiscalDocument` pode apontar para IUD ou para formato antigo quando `IsOldDocument=true`.

## DTE Transport Route

`DTE` exige rota de transporte:

- pelo menos dois `TransportLocation`;
- primeiro ponto e carga;
- ultimo ponto e descarga;
- pontos intermediarios sao admitidos.

`TransportModeCode`:

- `0` nao especificado;
- `1` maritimo;
- `2` ferroviario;
- `3` rodoviario;
- `4` aereo;
- `5` correio;
- `6` multimodal;
- `7` instalacoes fixas;
- `8` fluvial.

`ReceiverTypeCode` em DTE:

- `1` sujeito passivo;
- `2` nao sujeito passivo;
- `3` guia global.

Quando guia global, campos de recetor nao sao preenchidos.

`TransportDocumentTypeCode`:

- `1` Guia de Remessa;
- `2` Guia de Transporte;
- `3` Guia de Movimentacao de Ativos Proprios;
- `4` Guia de Consignacao;
- `5` Guia/Nota de Devolucao efetuada pelo cliente.

## Contingency And DFA

Modos de emissao:

- `1` online;
- `2` offline;
- `3` off.

`Transmission` requer:

- `TransmitterTaxId`;
- `Software`;
- `RepositoryCode`;
- `Contingency` quando `IssueMode` nao e online.

`RepositoryCode`:

- `1` Principal;
- `2` Homologacao;
- `3` Teste.

Contingencia exige:

- LED;
- data de emissao;
- tipo de motivo;
- IUC quando modo e `OFF`;
- hora de emissao obrigatoria apenas em `OFFLINE`.

`ReasonTypeCode`:

- `1` servico de autorizacao indisponivel; OFFLINE;
- `2` falha de energia; OFF;
- `3` sistema do contribuinte indisponivel; OFF;
- `4` Internet indisponivel; OFFLINE;
- `5` servico de timestamp indisponivel; OFFLINE;
- `0` outro.

Documento Fiscal Auxiliar (DFA):

- e a representacao impressa auxiliar quando o cliente solicita;
- e obrigatorio em contingencia;
- URL publica de QRCode segue o padrao `https://pe.efatura.cv/dfe/view/IUD`;
- acesso publico ocorre apos autorizacao;
- DFA em contingencia deve indicar autorizacao pendente e nao confere direito de deducao ate transmissao/autorizacao.

## API Contract

Base API:

```text
https://services.efatura.cv/{version}/{resource}
```

Lista oficial de endpoints:

```text
https://services.efatura.cv/api-list
```

Autenticacao/autorizacao:

- OAuth/OpenID;
- Authorization Code Flow com PKCE;
- well-known configuration em `https://iam.efatura.cv/auth/realms/taxpayers/.well-known/openid-configuration`.

Scopes relevantes listados no manual:

- LED CRUD/all;
- DFE create/read/list/read-by-IUD/read-stats/delete for homologacao/teste/self-billing authorize/all;
- EVENT create/read/all;
- CERTIFICATE read/all;
- TAXPAYER search/all;
- SOFTWARE read list, transmitter/customer/group scopes/all;
- `cv_ef_dfe_self_billing_authorize`;
- `cv_ef_opacc_read_accountant_list`;
- `offline_access`.

## DFE Submission Contract

Submissao de DFE:

- gerar XML de um ou mais DFEs;
- compactar em ZIP usando Deflate;
- enviar `multipart/form-data`;
- campo do formulario: `file`;
- content type do arquivo: `application/octet-stream`;
- nome de cada XML: `IUD.xml`;
- incluir header `cv-ef-repository-code`.

Consulta:

- lista de DFE aceita filtros como `AuthorizedDateStart`, `AuthorizedDateEnd`, `EmitterTaxId`, `DocumentTypeCodes`, `IssueDirection`;
- XML individual pode ser obtido por endpoint de XML com IUD.

Implicacao para NOVA-ERP: transmissao deve ser modelada como lote/arquivo tecnico separado do documento fiscal, ainda que o fluxo comum envie um unico DFE por vez.

## Events

Eventos usam fluxo semelhante ao DFE:

- gerar XML de evento;
- compactar em ZIP Deflate;
- enviar via recurso `event`;
- nomes de arquivos seguem padrao com pais, repositorio, data/hora e NIF.

Ainda e necessario deep-ingest dos XSDs/event examples antes de fechar cancelamento, anulacao, inutilizacao de numeracao e manifestacao de retificacao no modelo final.

## Self-Billing / Autofaturacao

v11.0 inclui escopo especifico para autorizacao de autofaturacao:

```text
cv_ef_dfe_self_billing_authorize
```

Fluxo:

- comprador solicita autorizacao do vendedor via `POST https://services.efatura.cv/v1/dfe/self-billing/authorize`;
- payload JSON inclui dados do vendedor/comprador e operacao;
- se vendedor tem conta PE, telemovel deve coincidir com o registo PE;
- se vendedor nao tem conta PE, comprador assume responsabilidade e DNRE pode inspecionar;
- resposta pode trazer `succeeded=false` e mensagens;
- codigo de autorizacao resultante entra no XML DFE.

Restricoes materiais capturadas:

- vendedor deve ser microempresa;
- se nao houver enquadramento fiscal, o manual admite regra transitoria apenas ate 2024-12-31 e limite associado ao REMPE isento.

Implementacao NOVA-ERP: autofaturacao nao deve entrar no MVP sem modelagem propria de autorizacao, validade, escopo e auditoria.

## Middleware

Links de download v11.0:

- Windows: `https://update.efatura.cv/win/mw-client/mwcore-efatura.zip`;
- Linux: `https://update.efatura.cv/linux/mw-client/mwcore-efatura.zip`;
- macOS: `https://update.efatura.cv/mac/mw-client/mwcore-efatura.zip`.

Operacao:

- middleware instalado em diretorio raiz;
- exposto como servico HTTP local/privado;
- browser pode alertar sobre certificado self-signed;
- `transmitter-key` de 64 caracteres e gerada/obtida na GUI;
- software contribuinte deve enviar header `cv-ef-mw-core-transmitter-key` em chamadas ao middleware;
- base URL troca `https://services.efatura.cv` por host/porta do middleware, por exemplo `https://localhost:3443`.

Configuracao:

- arquivo principal `MW_HOME/config/application.properties`;
- transmissor cadastrado na PE em Proprietario de Software;
- Redirect URI OAuth deve refletir host/porta do middleware;
- propriedades incluem `transmitter.tax-id`, `transmitter.name`, `transmitter.client-id`, `transmitter.client-secret`;
- emissores podem ser configurados por arquivo ou GUI;
- quando usar GUI para emissores, deixar defaults do bloco de emissores no arquivo.

## NOVA-ERP Implementation Implications

Antes de implementar e-Fatura real, NOVA-ERP deve ter:

- tabela ou estrutura para tipos DFE oficiais, nao apenas tipos comerciais internos;
- controle atomico de LED/serie/numero por tenant, ano e tipo DFE;
- gerador de IUD deterministico/auditavel com digito Luhn;
- snapshot fiscal imutavel antes de assinatura/transmissao;
- validador XSD local e armazenamento do resultado;
- payload XML assinado preservado com politicas de retencao e acesso restrito;
- transmissao em lote ZIP Deflate, mesmo para um documento;
- registro de tentativas com request headers, repositorio, endpoint, response status e mensagens;
- suporte a `IssueReasonCode` como enum governado por tipo de documento;
- suporte especifico a `RappelPeriod` para NCE/DRP;
- modelagem de referencias fiscais com IUD e documento antigo;
- state machine separando estado de negocio, estado fiscal e estado tecnico;
- contingencia oficial separada de retry tecnico;
- middleware configuration boundary por ambiente/transmissor/emissor;
- armazenamento seguro de certificados, secrets, `client_secret`, keystore e `transmitter-key`.

## Uncertainty And Follow-Up

- O manual tecnico nao substitui leitura de legislacao/despachos vigentes para claims juridicos finais.
- Eventos precisam de deep-ingest pelos XSDs e exemplos antes de fechar fluxos de cancelamento/anulacao/inutilizacao.
- O endpoint real, escopos concedidos e respostas de erro devem ser testados em homologacao.
- O modelo de middleware multi-tenant foi resolvido provisoriamente em [[2026-05-28 - Schema Decision - e-Fatura Middleware Topology and Tenant Configuration]], mas ainda requer verificacao operacional com o middleware real antes de producao.
