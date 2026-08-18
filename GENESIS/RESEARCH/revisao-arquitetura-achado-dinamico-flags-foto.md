# Revisão de Arquitetura — Wizard de Ronda: Achado Dinâmico, Flags de Sugestão, Foto em Duas Resoluções

Consolidação de uma sessão de divagação (2026-08-09/10), depois da
Fase 1/extensão de edição (CONV-013) já estarem em produção. Muda
decisão de arquitetura já implementada e testada nesta mesma sessão —
registrado com cuidado antes de qualquer instrução de Builder.

**Contexto importante para decidir o custo da mudança:** nenhuma ronda
real foi enviada em produção ainda (só registros sintéticos de teste,
já removidos). Não há dado real para migrar — a mudança de schema pode
ser feita limpa, sem migração de dado histórico.

## Decisão 1 — Achado vira lista dinâmica, não mais 8 categorias fixas

**Estado atual (produção, hoje):** `RondaSubmission.achados` sempre tem
exatamente uma entrada por categoria de uma lista fixa de 7 (mais
Passivo Trabalhista, 8ª, já decidida — ver "Decisões anteriores"
abaixo), cada uma com estado obrigatório (não avaliado/identificado/
inexistente). O endpoint `PATCH /convergia/ronda/:id` (já em produção)
endereça achado por `categoria`, assumindo esse invariante.

**Decisão nova:** achado vira item de lista livre, sem categoria fixa
como chave. Cada achado carrega: identificador próprio (não mais
"categoria"), origem (de qual flag veio a sugestão, ou "manual" se
adicionado direto), e os mesmos campos de sempre (departamento, foto,
descrição, classificação, gravidade).

**Impacto real no que já existe, para o Builder avaliar com precisão
antes de estimar:**
- `luna-core`: `contracts.ts` (`RondaFinding`/`RondaSubmission`/
  `RondaPatch`), `validation.ts` (`RISK_CATEGORIES`, cobertura das 8
  categorias, `requiredWhenIdentified`), `ronda-store.ts` (`update`
  endereça por `categoria`) — todos precisam de redesenho, não ajuste
  pontual.
- `luna-frontend`: `types.ts`, `ronda-wizard.tsx` (Etapa B inteira),
  `finding-card.tsx` (usa categoria fixa hoje), `ronda-editor.tsx`
  (também endereça por categoria).
- Nenhuma migração de dado — confirmado acima, produção está vazia de
  ronda real.

## Decisão 2 — Sistema de flags/sugestão

Antes da Etapa B (ou como parte dela), a pessoa marca quantos flags
quiser, não mutuamente exclusivos. Catálogo inicial, extensível (tabela,
não enum fixo no código — mesmo princípio já usado em `biblioteca_risco`
etc.):

- As 8 categorias de risco originais + Passivo Trabalhista (9 flags
  individuais).
- Procedimentos (fonte: `biblioteca_protocolo`).
- 5S (checklist fixo próprio, estrutura conhecida — Seiri/Seiton/Seiso/
  Seiketsu/Shitsuke).

**Ponto ainda não resolvido, marcado aqui para o Architect confirmar
antes de instrução de Builder:** o pedido original agrupava altura/
espaço confinado/elétrico/LOTO sob um único flag "Riscos Críticos"
(porque são as que exigem PT). A última instrução do Architect ("os 8
com flag") pode significar (a) os 8 continuam agrupados, e "Riscos
Críticos" continua existindo como um flag por si, ou (b) cada um dos 8
vira flag individual, e "Riscos Críticos" deixa de existir como
agrupamento — as duas leitura são possíveis, texto ambíguo. **Não
decidido pelo Engineer — precisa de confirmação explícita antes de
especificar o catálogo final.**

**Mecanismo:** cada flag marcado consulta a base de dado real
(`atividade_risco`/`controle_risco` para categorias de risco,
`biblioteca_protocolo` para Procedimentos) e gera **sugestões** — não
achados ainda. Sugestão é só um botão "+ [descrição do item]". Nenhuma
IA conversacional envolvida — é consulta determinística ao banco, não
chat (contorna a limitação já conhecida de `runCognitiveEngine` não ter
tool-calling, ver `ENG-038`).

**Segunda fonte de sugestão, integrada aqui (decisão do Architect,
2026-08-10): Fase 4 do ADR-021 original (leitura de risco na foto,
Decisão 6/9) entra como fonte de sugestão, não como fluxo separado.**
Ao tirar/anexar uma foto, a leitura de imagem (Qwen-VL via Groq, já
especificada) analisa e propõe achado(s) pré-preenchidos — mesmo
formato de sugestão que um flag de banco de dado gera, convergindo no
mesmo "+" da Decisão 3. A IA nunca grava achado sozinha a partir da
leitura da foto; sempre passa pelo "+" e confirmação humana, mesma
disciplina já usada em toda sugestão deste sistema. Duas fontes de
sugestão coexistindo: consulta a dado real (flags) e leitura de imagem
(Fase 4) — o "+" e o formulário de preenchimento são os mesmos,
independente de qual fonte originou a sugestão.

## Decisão 3 — "+" é o mecanismo único de adicionar achado

Não existe formulário diferente por flag/origem. Apertar "+" numa
sugestão (ou o "+" manual, sem sugestão nenhuma por trás) sempre abre o
mesmo formulário completo — mesmo componente reaproveitado
(`FindingCard`, redesenhado para não depender mais de categoria fixa,
ver Decisão 1) — departamento, foto, descrição, classificação,
gravidade. Uma sugestão nunca vira achado sozinha; sempre precisa do
"+" e do preenchimento humano.

**Refinamento do Architect (2026-08-10) — três lugares onde "+"
aparece, não um só:**
1. **"+" na sugestão de um flag** (já descrito acima) — cria achado
   novo do zero, a partir da sugestão.
2. **"+" dentro da mesma categoria/flag, para repetir** — o mesmo risco
   pode aparecer em mais de uma área na mesma ronda (ex. "Trabalho em
   Altura" identificado em 3 pontos diferentes). Cada categoria/flag
   precisa suportar **múltiplos achados**, não um só — reforça que a
   lista dinâmica da Decisão 1 não pode assumir "no máximo um achado
   por categoria", que era o invariante do modelo antigo.
3. **"+" num achado já preenchido, para duplicar** — a partir de um
   achado já completo, cria uma cópia pré-preenchida (mesmos campos),
   deixando a pessoa só trocar o que muda (risco/categoria, área,
   descrição) em vez de preencher tudo de novo do zero. Atalho de
   produtividade real para achados parecidos em áreas diferentes.

**O que substitui "não avaliado" nesta lista dinâmica:** proposta do
Engineer, não confirmada pelo Architect — cada sugestão não convertida
em achado tem uma forma leve de marcar "revisado, não se aplica",
diferente de simplesmente nunca tocar nela (preserva o princípio já
estabelecido: registro explícito, não silêncio). Precisa de
confirmação antes de virar especificação final.

**Correção humana sobre sugestão vira aprendizado (decisão do
Architect, 2026-08-10):** quando a pessoa ajusta/corrige uma sugestão
(de flag ou de leitura de imagem, Fase 4) antes de confirmar o achado,
essa correção — a diferença entre o que a IA propôs e o que o humano
de fato salvou — deve alimentar o Hipocampo (`memoria_luna`, via
Signal Engine, `ADR-019`, já em produção), mesmo princípio já usado na
resposta de P2 (Passivo Trabalhista) e na Decisão 5 do ADR-021
original (sensível/lógica antes de virar memória), agora estendido a
toda sugestão, não só uma categoria.

**Confirmação do Architect (2026-08-10):** quando a IA tem dúvida
(baixa confiança na leitura), o campo aparece marcado/destacado no
mesmo formulário — sem conversa de esclarecimento em tempo real (que
dependeria de tool-calling, ainda não existente, ver nota sobre
`FORGE-WORKSPACE-001`/`ENG-038` acima). **O humano sempre salva a
inferência da IA** — revisa, corrige se precisar (especialista em SSMA,
não leigo — corrige direto, sem precisar de diálogo guiado), confirma.
Mesmo princípio de "+"/confirmação já usado em toda sugestão deste
sistema, sem exceção para o caso de baixa confiança.

**Honestidade sobre o que falta:** o Signal Engine hoje avalia memória
de forma geral (relevância, novidade, recorrência) — não tem o
conceito de "correção humana sobre sugestão de IA" como tipo de sinal
próprio. Capturar esse delta (sugerido vs. confirmado) e persistir pelo
caminho já existente é peça nova, real, ainda que pequena — não cai de
graça do que já está construído.

## Decisão 4 — Foto em duas resoluções (campo vs. apresentação)

**Problema identificado:** a compressão atual do cliente
(`lib/ronda/photo.ts`, `MAX_DIMENSION = 1280`, `JPEG_QUALITY = 0.7`) foi
calibrada para rede de campo ruim e cota de IndexedDB — não para
exibição em TV/painel Power BI do cliente final, onde 1280px fica
visivelmente mole em tela Full HD (1920px) ou 4K (3840px).

**Decisão:** duas versões da mesma foto, geradas em momentos diferentes:
- **Versão de campo** (como hoje, inalterada): 1280px/qualidade 0.7,
  gerada no celular, é o que entra na fila offline e é enviada — otimizada
  pra rede ruim e economia de armazenamento.
- **Versão de apresentação**: maior/melhor qualidade, gerada depois — no
  servidor, na hora de montar o relatório final (Fase 2, `CONV-014`),
  quando já não há mais restrição de rede de campo nem de celular.
  Parâmetros exatos (dimensão/qualidade) ficam para quando a Fase 2 for
  especificada tecnicamente — não decidido aqui.

**Consequência real:** a foto original de maior resolução, capturada
pelo celular, precisa estar disponível no momento de gerar a versão de
apresentação — ou a versão de campo (comprimida) precisa ser a única
fonte, aceitando que a versão de apresentação nunca vai ser melhor do
que 1280px permite. **Não decidido:** guardar a foto original (maior,
mais pesada) em algum lugar até a hora do relatório, ou aceitar o teto
de qualidade que a compressão de campo já impõe. Isso muda se existe
"foto original" para uma segunda versão trabalhar, ou não.

## Decisões anteriores desta sessão, para contexto (já resolvidas, não reabertas aqui)

- P1 (PT): sistema só sinaliza, não gerencia emissão/aprovação.
- P2 (Passivo Trabalhista): 8ª categoria (agora questionável se
  continua "categoria" ou vira "flag individual", ver Decisão 2 acima),
  descrição livre, Luna aprende com o tempo.
- P3 (sequenciamento): esta revisão entra antes de `CONV-012`
  (pipeline assíncrono), que entra antes da validação de campo real.

## Pendências — respostas necessárias antes de instrução de Builder

1. Catálogo de flags: os 8 continuam agrupados sob "Riscos Críticos", ou
   cada um vira flag individual e "Riscos Críticos" deixa de existir
   como conceito? (Decisão 2)
2. Mecanismo de "revisado, não se aplica" para sugestão não convertida —
   confirma a proposta do Engineer ou tem outra ideia? (Decisão 3)
3. Foto original de campo fica guardada em algum lugar para a versão de
   apresentação usar depois, ou a versão de apresentação aceita o teto
   de 1280px como já é hoje? (Decisão 4)

## Escala do trabalho, para gestão de expectativa

Isso não é ajuste — é redesenho real de código que foi escrito, testado
e implantado **hoje**. `luna-core` e `luna-frontend` precisam de
retrabalho real nos módulos de ronda (contratos, validação, store,
wizard, editor). Não estimando prazo aqui — só registrando que é
trabalho de tamanho comparável ao que já foi feito hoje pela Fase 1
inteira, não uma correção pequena.
