# O que falta — LUNA Safety Walk, 16/08/2026

Handoff para outro chat. Os 6 commits estão **mergeados e publicados**: `luna-core` PR #43 → `f260caff` (deploy SUCCESS 17:43) e `luna-frontend` PR #27 → `e4a8fc2c` (deploy SUCCESS 17:44). A ordem foi respeitada — core 30s antes do frontend.

O que segue é o que **não** está feito, em ordem de urgência.

---

## 1. BLOQUEADOR — tabela `convergia_ronda_fotos` não existe

**Furo meu.** Criei a coleção no código do `luna-core` (`src/convergia/ronda/foto-store.ts`) e não criei a tabela no Supabase. Todas as outras coleções usadas pelo código têm tabela; essa não.

**Como verifiquei:** `GET /api/convergia/ronda/foto/rfoto_verificacao` em produção responde **400**, não 404. 400 significa que a rota existe e rodou, mas o store lançou — consistente com tabela ausente. Confirmado por SQL: o schema `public` tem `convergia_rondas`, `convergia_ronda_flags`, `convergia_visual_templates` e `convergia_template_positions`. Não tem `convergia_ronda_fotos`.

**Efeito:** todo upload de foto falha. **Não quebra nada** — o cliente cai no caminho antigo em silêncio, por decisão de projeto (nenhuma falha de rede pode impedir alguém de registrar um achado). Mas a Camada 2 fica **inerte**: as fotos continuam viajando dentro do relatório e a original continua no aparelho. Sintoma visível: toda miniatura fica com o **ponto âmbar** e nenhuma vem do servidor.

**Projeto de produção:** `jdbzhrtovpoaafpytgza` — identificado por evidência, é o que contém a ronda de 11/08 que a API devolve. Existe também `qxtntmufvnenfgupwonw` (`luna-safety-walk-piloto`), criado em 10/08, com as mesmas tabelas e **vazio**. Se a intenção é migrar para ele, aplique nos dois.

### Migração

Espelha a convenção de `convergia_visual_templates`: `id` como identity, textos e `created_at timestamptz default now()`, RLS ligado sem policy (acesso pela service key, que a ignora).

```sql
create table public.convergia_ronda_fotos (
  id                   bigint generated always as identity primary key,
  foto_id              text        not null unique,
  achado_id            text,
  campo_mime_type      text        not null,
  campo_data_base64    text        not null,
  campo_size_bytes     bigint      not null,
  original_mime_type   text,
  original_data_base64 text,
  original_size_bytes  bigint,
  created_at           timestamptz not null default now()
);

create index convergia_ronda_fotos_achado_id_idx
  on public.convergia_ronda_fotos (achado_id);

alter table public.convergia_ronda_fotos enable row level security;
```

`achado_id` é nullable **de propósito**: a foto sobe antes de a ronda existir no servidor, então é rastreabilidade, não chave estrangeira.

### Como confirmar que resolveu

```
GET https://uvicorn-main-production-92f8.up.railway.app/api/convergia/ronda/foto/rfoto_qualquer
```

Tem que virar **404 com `{"error":"Foto \"rfoto_qualquer\" não encontrada."}`**. Enquanto responder 400, a tabela ainda não está lá.

---

## 2. A ronda travada de 16/08 ainda não subiu

O servidor continua com **uma ronda só**, a de 11/08. A correção que destrava (`reclaimStaleSyncing`) já está publicada, mas ela roda **no aparelho**, quando o app abre com rede.

**Ação do Rubens:** abrir o LUNA Safety Walk com rede. A ronda presa em "enviando…" deve voltar para a fila e subir sozinha. Confirmar depois que a lista mostra duas rondas.

**Enquanto isso não acontecer: não limpar dados do site nem desinstalar o app** — é onde a ronda está.

Se ela subir duplicada, é o risco assumido e documentado: descarte a cópia extra pelo histórico.

---

## 3. A ronda de 11/08 está no servidor com zero achados

`ronda_8dd1c77d-7adb-4479-bddf-d4908a36c94e` — "Luna Safety Walk - Turno B", UT SYLVAMO - LOGISTICA, `achadosCount: 0`. A tela de edição mostrar só "Observações gerais" é consequência disso, não bug de interface.

**Nunca investiguei.** Perguntei ao Rubens se ele registrou achados naquele dia e não tive resposta. Se registrou, existe um **quarto defeito** ainda desconhecido, anterior a tudo que foi corrigido hoje.

---

## 4. Pendências de arquitetura em `luna-core` (nenhuma implementada)

1. **Chave de idempotência** em `POST /convergia/ronda`, usando o `localId` do cliente. Encerra o risco de duplicata em qualquer reenvio — hoje assumido conscientemente em `reclaimStaleSyncing`.
2. **Semântica de remoção** em `PATCH /convergia/ronda/:id`. O PATCH faz upsert por `id` de achado e não sabe dizer "este achado saiu". Por isso remover achado só existe em ronda que ainda não subiu, e a assimetria está documentada em `ronda-editor.tsx`.
3. **Expiração de foto órfã** em `convergia_ronda_fotos`. Dívida criada pelo próprio desenho da Camada 2: a foto sobe antes de a ronda existir, então ronda abandonada deixa foto sem referência. Começa a correr no dia em que a tabela do item 1 existir.

---

## 5. Documentação do Gênese não foi para o GitHub

A instrução do projeto pede que toda conclusão de etapa atualize os documentos do Gênese **no GitHub**. Eu escrevi tudo no **projeto Claude** (visível em qualquer chat do projeto Luna), mas **não commitei em repositório nenhum** — não tinha acesso de escrita.

Documentos que existem só no projeto Claude e deveriam ir para `raugustorubens-design/Luna-context.md`, em `GENESIS/`:

| Documento no projeto | Conteúdo |
|---|---|
| `GENESIS/achados-campo/2026-08-16-safety-walk-viewport-celular.md` | Os três defeitos do relato original, com as medições |
| `GENESIS/achados-campo/2026-08-16-recuperacao-ronda-presa.md` | Estado do servidor, bookmarklet de recuperação, mapa de estados da ronda |
| `GENESIS/achados-campo/2026-08-16-fila-visivel-e-editavel.md` | A correção estrutural da cegueira da fila |
| `GENESIS/decisoes/2026-08-16-armazenamento-e-upload-incremental.md` | A decisão das Camadas 1/2/3, com os números de armazenamento |
| `GENESIS/patches/2026-08-16-luna-core.patch` | O patch aplicado (histórico) |
| `GENESIS/patches/2026-08-16-luna-frontend.patch` | idem |

O `GENESIS/` do repo hoje é plano (`BUILDER.md`, `ENGINEER.md`, `ROADMAP.md`, `STATUS.md`, `RESEARCH/`…). Vale decidir se esses viram subpastas novas ou se o conteúdo entra em `BUILDER.md`/`ENGINEER.md`, que é onde achados de produção têm sido registrados até agora. **Essa decisão não é minha.**

Também não atualizei `STATUS.md` nem `ROADMAP.md` com nada do que foi feito hoje.

---

## 6. Coisas que eu não verifiquei

Para o próximo chat não assumir que estão testadas:

- **Nunca vi a Camada 2 funcionando contra o backend real.** O upload foi verificado contra um servidor HTTP local que eu subi (corpo 5,69 MB, `campo` 0,06 MB, `original` 5,62 MB — a original chega inteira). Contra produção, não — a tabela não existe.
- **Não vi a correção de viewport num celular de verdade.** Só em emulação de Pixel 7 e iPhone 13.
- **`GET /convergia/ronda/foto/:id?versao=original` nunca respondeu 200** em lugar nenhum. O caminho de leitura foi testado só em unidade, com Guardian falso.
- **Não sei se o service worker vai servir a versão nova imediatamente.** A navegação é network-first, então em tese sim, mas não confirmei no aparelho dele.
- **Três issues abertas** em `raugustorubens-design/Luna-context.md` que nunca abri.

---

## Referência rápida

| | |
|---|---|
| Produção frontend | `luna-frontend-production-ffcc.up.railway.app` (Railway `outstanding-learning`) |
| Produção backend | `uvicorn-main-production-92f8.up.railway.app/api` (Railway `honest-joy`, serviço `uvicorn main`) |
| Supabase produção | `jdbzhrtovpoaafpytgza` |
| Supabase piloto (vazio) | `qxtntmufvnenfgupwonw` |
| `luna-core` main | `f260caff` |
| `luna-frontend` main | `e4a8fc2c` |
