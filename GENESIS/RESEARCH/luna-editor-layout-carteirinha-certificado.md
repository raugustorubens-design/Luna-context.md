# Editor de Layout do Convergia (Carteirinha/Certificado em Lote) — Especificação (Theory)

Status: Theory — especificação completa fornecida pelo Originador
(2026-07-23), sem execução de campo dentro da LUNA ainda. Especifica em
detalhe o que hoje está registrado de forma vaga no Roadmap como
`CONV-002` ("Editor de layout: posicionamento de campos sobre o
template... com persistência de layout"). Não implementado.

## O fluxo completo (como especificado)

1. Usuário sobe o template visual (imagem de fundo do documento —
   carteirinha, certificado).
2. Usuário sobe o arquivo de dados (ex.: planilha Excel). O Convergia
   lê os cabeçalhos de coluna e gera um "balão" (campo arrastável) para
   cada coluna, já identificado com o nome dela.
   2.1. Cada balão tem um "X" no canto para exclusão — nem toda coluna
        do arquivo de dados precisa virar campo no template atual.
        Isto é necessário porque o mesmo arquivo de dados pode
        alimentar múltiplos templates com conjuntos de campo
        diferentes — caso confirmado com o exemplo real da Carteirinha
        (frente e verso do mesmo cartão, cada lado com campos
        distintos, mesmo arquivo de dados de origem).
3. Usuário posiciona cada balão sobre o template, no local exato onde
   aquele dado deve aparecer.
4. Usuário redimensiona: tamanho da fonte e tamanho do próprio balão.
5. Usuário ajusta opções de escrita (estilo de texto: fonte,
   alinhamento, etc. — mesmo padrão de qualquer editor de texto sobre
   campo posicionado).
6. Usuário confere o preview (visualização fiel ao resultado final,
   antes de gerar de fato).
7. Usuário salva o modelo — o layout (posição, tamanho, tipo de cada
   campo) fica persistido para reuso em lotes futuros.
8. O Convergia processa em lote: aplica o modelo salvo contra todas as
   linhas do arquivo de dados, gerando um documento por linha/
   funcionário (uma carteirinha ou certificado por pessoa).

## Os 4 tipos de campo que o editor precisa suportar

Confirmado por especificação direta, não hipótese:

1. **Texto** — nome, RE, função, setor, validade, etc. Com controle de
   fonte/tamanho/estilo (passos 4-5 acima).
2. **Imagem** — foto do funcionário, posicionada como campo arrastável
   igual ao texto.
3. **Imagem com fundo transparente** — a assinatura do funcionário é um
   caso especial de campo-imagem: precisa de fundo transparente para
   não sobrepor o template com uma caixa branca (assinatura escaneada
   normalmente vem com fundo branco opaco).
4. **Flag/checkbox** — um "quadradinho" booleano que fica preenchido
   (preto) ou vazio conforme o valor da coluna correspondente nos
   dados. Confirmado a partir do exemplo real da Carteirinha (documento
   já analisado nesta conversa): o campo "Veículos/equip. móveis"
   aparece marcado com X quando aplicável, em branco quando não — cada
   categoria de autorização (espaço confinado, instalações elétricas,
   trabalho a quente, etc.) é um flag independente, controlado por uma
   coluna própria no arquivo de dados.

## Faces de template: carteirinha (1 face) vs. certificado (2 faces)

Confirmado por especificação direta — o editor de layout precisa
suportar dois casos distintos de "quantas faces um modelo salvo tem":

- **Carteirinha**: uma única face/template plano. A carteirinha é
  impressa de um lado só e dobrada fisicamente — a aparência de
  "frente e verso" no documento real analisado (2 cartões por página)
  é resultado da dobra física do papel, não de dois templates
  distintos no sistema.
- **Certificado**: duas faces/templates distintos (frente e verso),
  cada uma com seu próprio conjunto de campos posicionados. O verso
  repete a data que já aparece na frente, e inclui o Conteúdo
  Programático do treinamento — a mesma estrutura de módulos/tempo
  sugerido já documentada em `luna-treinamento-adaptativo.md`. Isto é
  outra ligação real entre frentes do Convergia antes tratadas em
  documentos separados: o verso do certificado é, na prática, uma
  renderização do currículo do próprio treinamento concluído pela
  pessoa.

**Achado de campo (lição real, não hipótese):** o Conteúdo Programático
no verso do certificado precisa ser editável pelo usuário, não gerado e
travado. Motivo confirmado pelo Originador: empresas especialistas em
inspeção de documentos frequentemente comparam o que está na lei/norma
com o que foi efetivamente ministrado no treinamento — e já houve caso
real de reprovação em auditoria por ter incluído mais conteúdo do que a
lei exigia (contraintuitivo — mais completo não é necessariamente
melhor do ponto de vista de conformidade documental). Isto significa
que o Conteúdo Programático puxado do módulo de treinamento (ver seção
anterior) deve ser um ponto de partida editável, nunca o texto final
sem revisão humana — o instrutor precisa poder cortar/ajustar antes de
gerar o certificado definitivo.

**Implicação para o editor:** o "modelo salvo" (passo 7) precisa ser
capaz de representar 1 ou 2 templates associados, não sempre 1 fixo —
carteirinha usa 1, certificado usa 2.

## Entidade Funcionário — chaves confirmadas e campos reais completos

Consolidação do que já aparecia de forma consistente em todos os
documentos reais analisados nesta conversa (Planilha de Riscos, PGR,
Carteirinha, OSSM) — agora confirmado explicitamente pelo Originador
como modelo de dado, mais a planilha-mestre real (Manserv Logística)
que alimenta o processamento em lote.

As 3 chaves relacionais:

- **RE (Registro de Empregado)** — chave primária, identificador único
  e estável.
- **Nome** — chave secundária, identificação humana (não é chave
  primária porque nomes podem se repetir; RE não).
- **Função Atual** (nome real da coluna na planilha-mestre —
  equivalente ao "Cargo" mencionado antes) — a chave que relaciona o
  funcionário aos três domínios já mapeados nesta conversa:
  - Risco: a Planilha de Gerenciamento de Riscos já é organizada por
    GHE/Cargo (uma aba por função — Operador Logística, Líder
    Operacional, etc.).
  - Treinamento: qual conteúdo curricular se aplica a qual cargo (ver
    `luna-treinamento-adaptativo.md`).
  - Documentos/Autorizações: a Carteirinha usa Nome/RE/Função/Setor
    como campos fixos; Cargo determina quais categorias de autorização
    (flags do tipo 4 acima) fazem sentido para aquela pessoa.

Campos completos confirmados na planilha-mestre real (Manserv
Logística, exemplo real inspecionado nesta conversa): RE, Nome, Função
Atual, Data de Admissão, PCE, Status, Setor, Turno, Mobilização, Data de
Nascimento, Idade, Sexo, PIS, CPF, RG — e um bloco de contato separado:
Telefone, Endereço, Nº, Bairro, Cidade.

## Decisão do Architect sobre dado sensível (2026-07-23)

O Convergia processa sem armazenar o arquivo de dados do funcionário. O
modelo salvo (passo 7) é só a configuração de layout (posição/tamanho/
tipo de cada campo sobre o template) — não os dados em si (CPF/RG/PIS/
nome/etc.). O arquivo de dados (a planilha-mestre, por exemplo) é
enviado, processado em lote contra o modelo salvo, os documentos de
saída são gerados, e o arquivo de dados não fica retido no sistema
depois disso. Isto resolve a tensão de dado sensível sem exigir uma
decisão de LGPD/armazenamento formal ainda — a maioria dos documentos
do Convergia usa dado essencialmente sensível, e a resposta é não
precisar guardar arquivo de dado nenhum, só a configuração do modelo.

**Esclarecimento adicional sobre o próprio resultado do processamento
(2026-07-23):** os documentos gerados (as carteirinhas/certificados
processados) podem ser baixados pelo cliente no momento do
processamento — a responsabilidade pelo dado sensível contido neles
passa a ser do cliente a partir do download. Se o cliente não baixar
naquele momento, não há como recuperar depois — os documentos gerados
também não são persistidos, mesma lógica do arquivo de dados de
origem. Isto precisa ser comunicado explicitamente ao usuário na
interface (aviso claro antes ou durante o processamento) — não é só
uma decisão técnica silenciosa, é também uma peça de esclarecimento de
proteção de dados para o cliente: ele sabe exatamente onde a
responsabilidade começa (download) e que não há cópia de segurança do
lado da LUNA.

**Onde o aviso precisa aparecer (confirmado):** não basta estar numa
página de apresentação/termos de uso do site — precisa aparecer dentro
do próprio fluxo de edição/geração de documentos, especificamente no
início e no final do processo (antes de o usuário subir o arquivo de
dados, e novamente ao final, junto da oferta de download). Repetir o
aviso nesses dois pontos do fluxo real é o que garante que o cliente
tenha visto a informação no momento em que ela importa, não só como
letra miúda genérica.

**Nota sobre o caráter provisório desta decisão:** o próprio Originador
(no papel de Architect) sinalizou que esta é uma decisão de estágio
atual, não permanente — gerenciar dado sensível do cliente com
persistência real é algo que pode vir a ser considerado no futuro, mas
a organização "ainda não está preparada para isso" (infraestrutura,
processo, e provavelmente decisão de conformidade formal ainda não
amadurecidas). Registrando isto para que uma futura revisão desta
Theory não trate "processa sem armazenar" como um axioma imutável da
arquitetura.

## Telemetria de serviço (KPIs) — não é dado do cliente, é dado sobre o serviço

Distinção importante que o Originador fez explicitamente: o Convergia
não deve gerenciar dado sensível do cliente (ver seção acima), mas deve
gerar um relatório sobre o próprio serviço — tempo de processamento,
dificuldades encontradas, e outros KPIs operacionais. Isto não é sobre
CPF/RG/nome de funcionário — é telemetria sobre o funcionamento do
Convergia em si (quanto tempo um lote levou para processar, que tipo de
erro ocorreu, quantos documentos foram gerados, etc.).

Isto é a instância concreta, aplicada ao Convergia, de dois itens que já
existem de forma abstrata no Roadmap (P5 — Sistema de crescimento e
sustentabilidade): "Definir indicadores econômicos por MVP" e "Definir
telemetria econômica para o Reporter". Até esta conversa, esses itens
não tinham um caso de uso concreto amarrado a eles — agora o Convergia é
o primeiro MVP com um requisito real e específico de telemetria, e o
critério de "cada MVP deve ser rentável" (já mencionado nesta mesma
conversa) depende diretamente de ter esse tipo de dado disponível.

O que ainda não está definido aqui: a lista exata de KPIs (o Originador
citou "tempo, dificuldades e outros" — não uma lista fechada), onde essa
telemetria fica armazenada (isto não tem a mesma restrição de
não-persistência do dado do cliente — é dado operacional da LUNA, não
dado sensível de terceiro), e se isto se conecta ao Reporter existente
(`reporter.analyze_project`, hoje escopado só para análise de
Roadmap/código, não para métricas de uso de capability) ou é um
mecanismo novo e separado.

Esta entidade Funcionário (RE/Nome/Função) é consumida tanto por este
documento (geração em lote de carteirinha/certificado por linha de dado
= por funcionário) quanto pelo documento irmão de relatório fotográfico
(`luna-relatorio-fotografico-auditoria-convergia.md`) e pelo de
treinamento adaptativo (`luna-treinamento-adaptativo.md`) — é a peça de
dado compartilhada entre as três frentes do Convergia especificadas
nesta conversa.

## O que ainda não está definido (não fabricado, sinalizado como aberto)

- Remoção de fundo da assinatura: não especificado se o usuário sobe a
  assinatura já em PNG com transparência pronta, ou se o Convergia
  precisa remover o fundo automaticamente de um scan/foto comum (fundo
  branco opaco). Pergunta feita ao Originador, ainda sem resposta
  registrada.
- Schema formal da entidade Funcionário (que outros campos além de
  RE/Nome/Cargo, tipos de dado, relação com as tabelas de Risco por
  GHE) não foi especificado — só as 3 chaves e o papel de cada uma
  foram confirmados. Nota: com a decisão de processar-sem-armazenar,
  este schema é mais sobre "forma esperada do arquivo de dados de
  entrada" do que sobre uma tabela persistida no banco da LUNA.
- Detalhe técnico de implementação da não-persistência, parcialmente
  esclarecido pela política de download: como o cliente precisa poder
  baixar o documento gerado no momento do processamento, o sistema
  precisa manter o resultado disponível por uma janela de tempo da
  sessão (não é "nunca grava em lugar nenhum") — mas o mecanismo exato
  (link de download temporário, resposta direta do request sem
  intermediário, etc.) e por quanto tempo essa janela dura não foram
  especificados.
- Formato de persistência do "modelo salvo" (passo 7) — não
  especificado se é um objeto JSON de layout, um template de
  renderização específico, ou outra estrutura.

## Próximo passo sugerido

Esta Theory está pronta para virar ADR assim que houver decisão de
caminho técnico para: (a) o motor de renderização de PDF (`CONV-005`,
mesma pendência já registrada em
`luna-relatorio-fotografico-auditoria-convergia.md` — gera a mesma
situação de gargalo aqui, já que carteirinha/certificado também precisa
sair em PDF), e (b) a abordagem de fundo transparente da assinatura
(upload pronto vs. remoção automática).
