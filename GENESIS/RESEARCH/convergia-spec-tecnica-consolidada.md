Convergia — Especificação Técnica Consolidada (Arquitetura)
Status: Especificação de arquitetura, consolidando 3 documentos de Theory já aceitos (`luna-treinamento-adaptativo.md`, `luna-relatorio-fotografico-auditoria-convergia.md`, `luna-editor-layout-carteirinha-certificado.md`) mais decisões de sessão não formalizadas em nenhum ADR ainda. Este documento não substitui os três — é a camada que os une num modelo único de arquitetura. Pronto para virar ADR após revisão do Architect.
Decisão de arquitetura confirmada
Convergia permanece rota irmã do Gateway (`/api/convergia/*`, ao lado de `/api/chat`) — nunca vira capability do Gateway. Reafirma ADR-012, não o revoga. A proposta alternativa ("expor via Gateway como novo organ"), que apareceu num relatório de sessão externa, foi avaliada e rejeitada: capability de Gateway significa acoplamento mais forte, contrário ao objetivo de MVP acoplável/desacoplável. Ponto de extração futura recomendado: um ponto de entrada standalone (`src/convergia/standalone-server.ts`), ainda não implementado, que sobe só as rotas do Convergia como processo próprio — mesma base de código, sem duplicação.
Os 6 tipos de trabalho (abstração central)
Todo caso de uso do Convergia é composição de, no máximo, 2 primitivos — não 6 pipelines separados:

1. Extração (primitivo) — não-estruturado → estruturado. PDF nativo ou foto → campos extraídos. Não produz documento final, produz dado.
2. Geração por Template (primitivo) — dado tabular + template visual (campos posicionados) → lote de documentos.
3. Composição de Relatório — Extração (1) + Geração por Template (2)
   * edição/validação humana no meio + conclusão gerada. Não é primitivo novo.
4. Renderização Tabular Genérica — dado estruturado → documento, direto, sem template posicional, sem IA. Já existe e funciona.
5. Reorganização de Arquivo — usa resultado de Extração (1) para agir sobre os próprios arquivos (renomear, indexar em lote).
6. Ingestão de Conhecimento — conteúdo → Guardian/Hipocampo. Não produz nada visível ao cliente; alimenta a memória da LUNA.

Consequência de engenharia: fortalecer os 2 primitivos (Extração, Geração por Template) + Ingestão cobre todos os casos de uso atuais e futuros. Cada caso novo é majoritariamente configuração, não código novo.
Modelo de entidade — Sujeito do Documento (3 chaves)
Não existe uma entidade "Funcionário" fixa. Existe um modelo de 3 chaves, genérico o suficiente para qualquer cliente (indústria, clínica, escola):

* Chave Primária — identificador único e estável (exemplo real: RE).
* Chave Secundária 1 — nome/identidade legível (exemplo: Nome).
* Chave Secundária 2 — função/papel (exemplo: Cargo/GHE).

As 3 chaves juntas são o mecanismo de busca e relacionamento para tudo que depende do Sujeito: exame (ASO), EPIs, treinamentos necessários vs. realizados, documentos pendentes. A UI de configuração mostra "Relação 1 (ex: número de registro, identidade, outro)" e "Relação 2 (ex: cargo, função, atividade)" com exemplos, não uma lista fechada — o cliente mapeia suas próprias colunas.
Campos além das 3 chaves são livres — cada coluna do arquivo de dados enviado vira um campo configurável (balão) no editor de layout, sem schema fixo do lado do Convergia.
Fontes de cruzamento (documentos reais, não inventados pelo Convergia)

* PGR — inventário de risco por GHE, com score Probabilidade+Gravidade=Resultado, Abrangência à parte.
* Matriz de Treinamento — mapeia Cargo/GHE → treinamentos exigidos. Documento padrão do setor (não inventado por este projeto), geralmente derivado do PGR.
* PISSMA (Planejamento Anual de Segurança) — define periodicidade de inspeção (semanal/mensal) e o critério de quando emitir PT (antes da atividade) vs. PÓS TRABALHO (depois, para subcontratada não fixa).
* IPSMA — checklist de inspeção com escala própria (Desprezível/Moderado/Crítico), Conforme/Não Conforme/N/A.

Limitação técnica confirmada (ADR-019): o Signal Engine do Hipocampo hoje calcula relevância só por sobreposição léxica (Jaccard), sem embedding/semântica real. Consultas por chave estruturada (Cargo/GHE exato) funcionam hoje sem depender dessa maturidade. Consultas livres (ex.: "essa foto viola algum risco documentado?") dependem de uma maturidade de busca que ainda não existe — devem ser tratadas como capability limitada até o Signal Engine evoluir, não como pronta.
NRs como fonte de perguntas de inspeção (TST + IA)
Correção de mecanismo (sessão 2026-07-24): as NRs não disparam emissão de PT no Convergia — isso não é papel delas neste sistema. O papel real: cada NR gera um banco de perguntas relacionadas ao ambiente de trabalho, que serve dois consumidores ao mesmo tempo:

1. O TST (Técnico de Segurança do Trabalho), como roteiro de campo ao montar o relatório fotográfico — o que perguntar/observar naquele ambiente, por norma aplicável.
2. A IA, como critério de análise da foto — a mesma pergunta que guia o TST em campo é o que a IA usa para avaliar a imagem.

Isto reforça, não substitui, o princípio já registrado acima: o critério de checagem não é hardcoded no Convergia — é fonte de conhecimento consultável (aqui, banco de perguntas por NR; antes, PGR/IPSMA do GHE/atividade). As duas fontes convivem: PGR/IPSMA trazem o risco já identificado e classificado daquele cliente específico; as NRs trazem o critério normativo geral, aplicável independente do cliente já ter ou não documentado aquele risco.
NRs mapeadas nesta sessão, como ponto de partida do banco de perguntas (não lista fechada): NR-10 (elétrica, atualizada por Portaria MTE 737/2026), NR-11 (transporte/armazenagem), NR-12 (máquinas/equipamentos, inclui LOTO), NR-13 (caldeiras/vasos de pressão), NR-14 (fornos), NR-15 (insalubridade), NR-16 (periculosidade), NR-20 (inflamáveis/ combustíveis), NR-33 (espaços confinados), NR-34 (construção/reparação naval — hidrojateamento, radiação ionizante, montagem de andaime, etc.), NR-35 (altura).
O que ainda não está definido: o formato exato do "banco de perguntas" (uma pergunta por item de cada NR? agrupado por atividade, não por norma?), e se este banco é gerado uma vez e versionado, ou reconstruído a cada consulta a partir do texto da norma. Não fabricado aqui — fica para especificação seguinte.
Casos de uso especificados (instâncias do modelo acima)
1. ASO (Atestado de Saúde Ocupacional) — via `luna-relatorio-fotografico-auditoria-convergia.md` e discussão de sessão

* Entrada: PDFs de ASO com nome de arquivo aleatório, texto nativo (não escaneado, sem necessidade de OCR).
* Extração (tipo 1): nome, RE, data de realização, apto/inapto.
* Parser recomendado: `pdf-parse` (MIT, zero custo) para extração de texto simples; `pdfjs-dist` (MIT, zero custo) como plano B se o layout do PDF embaralhar a ordem do texto.
* Estruturação dos campos: via Claude, Gateway (`reasoningTier: deep`).
* Reorganização de Arquivo (tipo 5): renomear PDFs + gerar planilha-índice.
* Governança de dado sensível: Guardian registra apenas metadado do processamento — nunca o conteúdo de saúde (apto/inapto não persiste como conhecimento da LUNA).
* Direção de produto: template reutilizável, não hardcoded — pensado para oferecer futuramente a clínicas médicas (multi-tenant/isolamento por cliente fora de escopo desta rodada).

2. Relatório Fotográfico de Auditoria

* Ver `luna-relatorio-fotografico-auditoria-convergia.md` para o fluxo completo (contexto → foto → NC gerada e editável → NC manual → template do cliente → conclusão).
* Duas categorias de achado de foto, tecnicamente distintas:
   * Estrutural (empilhamento, centro de carga, distanciamento, altura) — não envolve pessoa identificável na imagem.
   * EPI/comportamental (uso de EPI, cinto de segurança) — envolve pessoa identificável; mesma disciplina de dado sensível do ASO se aplica caso a foto mostre rosto.
* Critério de checagem: não hardcoded no Convergia — consultado dinamicamente do Hipocampo. Duas fontes convivem: PGR + IPSMA do GHE/atividade (risco já identificado pelo cliente) e o banco de perguntas por NR (critério normativo geral — ver seção "NRs como fonte de perguntas de inspeção" acima), respeitando a limitação de busca livre já registrada.
* Modelo de visão recomendado: família Qwen-VL (Qwen2.5-VL/Qwen3-VL), acessível via Groq (`qwen/qwen3.6-27b`, já provider configurado no `luna-core`) — cobre leitura de cena e OCR de rótulo com um único modelo. Groq marca como "preview"; migrar para OpenRouter (também já configurado) quando maturidade de produção for necessária.

3. Carteirinha / Certificado (Editor de Layout)

* Ver `luna-editor-layout-carteirinha-certificado.md` para o fluxo completo do editor (upload template → balões por coluna → posicionar → redimensionar → preview → salvar modelo → processar em lote).
* 4 tipos de campo: texto, imagem, imagem com fundo transparente (assinatura), flag/checkbox (categoria de autorização).
* Balão tem "X" de exclusão — nem toda coluna do arquivo de dados precisa virar campo no template atual (caso real: frente/verso da carteirinha usam subconjuntos de campo diferentes, mesmo arquivo de dados).
* Carteirinha = 1 face de template (impressão única, dobrada fisicamente — a aparência de frente/verso é da dobra, não de dois templates).
* Certificado = 2 faces de template (frente e verso distintos). O verso repete a data da frente e inclui o Conteúdo Programático do treinamento (puxado do módulo já documentado em `luna-treinamento-adaptativo.md`) — deve ser editável pelo usuário, nunca gerado e travado: achado de campo real (não hipótese) — inspeção de conformidade documental já reprovou um caso por incluir mais conteúdo do que a norma exigia.
* Política de dado sensível: processa sem armazenar. O modelo salvo é só a configuração de layout — nunca os dados em si. O arquivo de dados de origem não fica retido após o processamento em lote.
* Aviso de não-persistência: deve aparecer dentro do fluxo real (início e fim do processo de edição/geração), não só em página de termos de uso. Decisão de estágio atual, não permanente — revisitável quando a organização estiver pronta para gerenciar dado sensível de cliente com persistência real.

4. Documento Tabular Genérico

* Já existe e funciona (`documento-tabular-generico`, csv/json/markdown/html/xlsx/pptx). Apenas expor e testar nesta rodada.

Formatos de saída
Cliente escolhe o formato — aplica-se aos tipos 2, 3 e 4 (os que efetivamente renderizam documento; tipos 1, 5 e 6 não têm "formato de saída" no mesmo sentido).

* xlsx — já existe (`documento-tabular-generico`).
* pptx — já existe, com teste reforçado (abre o zip real, confere XML).
* docx — não existe ainda. Resolver com a lib `docx` (npm, MIT, zero custo) — gera `.docx` real sem depender de Word/Office 365 instalado em lugar nenhum.
* PDF — deixou de ser bloqueador do caminho principal desde que editável (docx/pptx/xlsx) passou a ser prioridade (relatórios/ inspeções frequentemente precisam de complementação que PDF fechado não permite). Vira "bom ter depois", não pré-requisito.

Telemetria de serviço (KPIs)
Distinto de dado do cliente — telemetria sobre o funcionamento do Convergia em si (tempo de processamento, dificuldades, KPIs operacionais). Instância concreta dos itens já abstratos em P5 do Roadmap ("indicadores econômicos por MVP", "telemetria econômica do Reporter"). Não especificado: lista exata de KPIs além de tempo/dificuldades, onde essa telemetria é armazenada (sem a restrição de não-persistência do dado do cliente, por ser dado operacional da LUNA), e se conecta ao Reporter existente ou é mecanismo novo.
Capability nova identificada, ainda sem tipo formal: rotina de treinamento pendente
Cruzamento de Cargo/GHE (via Matriz de Treinamento) contra histórico de treinamentos realizados (extraídos de PDF, com data de realização) → gera lacuna por pessoa: nunca realizado, realizado e vencido (considerar periodicidade de reciclagem por norma — ex. NR-35 costuma ser 2 anos), realizado dentro do prazo. Não é um 7º tipo de trabalho — é Composição de Relatório (3), com entrada vinda do cruzamento interno (chaves + histórico) em vez de arquivo novo enviado.
O que ainda não está definido (não fabricado, sinalizado como aberto)

* Ponto de entrada standalone do Convergia — caminho recomendado, não implementado.
* Mecanismo exato de janela de download temporário (quanto tempo o documento gerado fica disponível antes de não poder mais ser recuperado).
* Lista fechada de KPIs de telemetria e onde persistem.
* Remoção de fundo da assinatura: upload já transparente vs. remoção automática pelo Convergia — não respondido pelo Originador ainda.
* Detalhe de implementação de "processar sem armazenar": em memória pura vs. arquivo temporário com limpeza automática pós-lote.

Próximo passo
Pronto para virar ADR após revisão do Architect. Implementação sugerida em ordem: (1) parser PDF + renderer docx (menor esforço, desbloqueia ASO e formatos de saída de todos os casos), (2) editor de layout com os 4 tipos de campo, (3) integração de leitura de foto com Hipocampo para critério dinâmico (depende de decisão de modelo de visão), (4) rotina de treinamento pendente (depende de 1-3 estarem funcionais).
