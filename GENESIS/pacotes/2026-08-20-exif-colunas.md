# Colunas de EXIF em `convergia_ronda_fotos`

**Caminho:** `GENESIS/pacotes/2026-08-20-exif-colunas.md`
**Estado:** pronto · continuação do `#54`

> ## REPOSITÓRIO-ALVO
>
> **`raugustorubens-design/luna-core`** — exclusivamente.
> Escopo: `supabase/migrations/`.

---

## O que o Builder achou e fez certo em não consertar

No `#54` ele encontrou, além das duas tabelas que faltavam, uma terceira divergência — e
**parou**, porque alterar tabela com dado real batia numa condição de parada do próprio
pacote.

**Confirmei no banco.** A `convergia_ronda_fotos` tem dez colunas:

```
id · foto_id · achado_id
campo_mime_type · campo_data_base64 · campo_size_bytes
original_mime_type · original_data_base64 · original_size_bytes
created_at
```

**Nenhuma coluna de EXIF.** E o `#43` do frontend já está em produção enviando o campo, com
o `#52` do core aberto para recebê-lo.

Parar foi a decisão certa. Registre no `BUILDER.md` como acerto, não só como pendência.

---

## O que fazer

Migração aditiva, em arquivo commitado — nunca aplicada à mão antes de existir no
repositório. É a regra `ENG-036`/`DRIFT-001`.

**Colunas novas, todas anuláveis.** Leia o `foto-store.ts` antes de escrever: a migração
acompanha o que o código já tenta gravar, e não o que eu imagino que ele grave. Pelo
desenho, deve carregar data e hora da captura, coordenada, orientação e identificação do
aparelho.

### As três travas

**Todas anuláveis, sem valor padrão.** As 51 fotos que já existem não têm EXIF, e nunca
terão — foram gravadas antes. **Foto sem metadado continua válida**, exatamente como foto
sem imagem original.

**Nenhuma coluna existente é alterada.** Só acréscimo. Se a migração precisar mexer em
coluna que já tem dado, **pare**.

**Índice só se houver consulta.** Não crie índice por coordenada "para o futuro" — se
ninguém busca por isso hoje, é custo sem uso.

---

## Depois da migração

**Mergeie o `luna-core#52`**, que está aberto em rascunho. Ele é o lado servidor do EXIF, e
sem ele o campo que o frontend manda continua sendo ignorado em silêncio.

**A ordem importa:** migração primeiro, `#52` depois. Invertida, a rota tenta gravar em
coluna que não existe.

---

## Pré-respostas

| Se encontrar | Faça |
|---|---|
| O `#52` já mergeado | Migração mesmo assim, e confirme que a gravação passa |
| `foto-store.ts` gravando campo que não previ | A migração acompanha o código |
| Migração exigindo alterar coluna existente | **Pare** |
| Outra tabela sem arquivo de migração | Reporte. Não crie sem pacote |

## Condições de parada

- Qualquer alteração em coluna que já tem dado
- Necessidade de valor padrão ou de preencher retroativamente
- Aparecer terceira tabela em divergência — vira pacote próprio

## Autorização de merge

Pode mergear após os portões automáticos. Entra no `PENDENTE.md`.

---

## Critério de pronto

1. As colunas aparecem em `information_schema.columns`
2. A migração está **commitada**
3. As 51 fotos existentes continuam legíveis, com EXIF nulo
4. `luna-core#52` mergeado depois

**Portão do Arquiteto:** tirar uma foto pelo `/ronda`, com GPS ligado, e conferir no
Supabase que **data e hora reais da captura** chegaram. Depois, uma foto vinda da galeria —
que costuma vir sem EXIF nenhum — e confirmar que ela anexa normalmente.

---

## O padrão que apareceu três vezes

Três divergências de schema em dois dias: `convergia_relatorio_curadoria`,
`convergia_ronda_relatorios`, e agora as colunas de EXIF.

**Todas passam em todo teste** — o teste usa dobro, e dobro não tem schema. Só falham em
produção.

**Vale um verificador**, e é barato: um passo que compara o que o código espera do banco
com o que existe de fato, e reprova a build quando divergir. É a mesma ideia do
`architecture-check`, aplicada ao schema em vez de à arquitetura.

Isso não entra neste pacote — mas entra na fila, porque é o que impede a quarta.

---

## Memórias geradas

- Três tabelas em divergência em dois dias: código de acesso a schema mergeia verde e falha
  só em produção
- Coluna acrescentada a tabela com dado existente é sempre anulável e sem valor padrão; o
  passado não se reescreve
- Parar por condição de parada e registrar é resultado, não obstáculo
