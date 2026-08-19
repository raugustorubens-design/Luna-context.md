# GENESIS/pacotes/ — fila de pacotes para o Builder

Pacotes de instrução do Engenheiro/Arquiteto para o Builder, commitados aqui em vez de
anexados por chat. Motivo (registrado em `GENESIS/BUILDER.md`, entrada de 19/08/2026):
cinco vezes um pacote chegou errado, repetido ou desatualizado — não por descuido, mas
porque a ponte era anexo de arquivo, e quando aparecem vários na mesma noite, algum
fica pra trás.

**Uso:** apontar o caminho em vez de reanexar.

> Execute GENESIS/pacotes/2026-08-19-tirar-o-roxo.md

## Fila em 19/08/2026, na ordem de execução

Um por vez. Pare depois de cada um — cada pacote tem seu próprio portão real
(verificação humana, em produção ou em campo) antes do próximo começar.

| # | Pacote | Repositório-alvo | Depende de |
|---|---|---|---|
| — | `2026-08-19-plano-o-resto.md` | `luna-core` (itens 1, 3, 4) · `Luna-context.md` (item 2, já executado) | leia primeiro — contém a ordem e o raciocínio dos demais |
| A | `2026-08-19-tirar-o-roxo.md` | `luna-frontend` | nada — primeiro da fila de código |
| B | `2026-08-19-gate-com-link-ao-campo.md` | `luna-frontend` | o gate urgente de ronda divergente (fora deste pacote) sair do PR #28 para branch própria |
| C | `2026-08-19-safety-walk-cores.md` | `luna-frontend` | **A**, e o mesmo gate urgente mergeado e confirmado em produção antes dele |

O `PLANO_o-resto.md` já traz, por dentro, os itens 1 (vetores faltantes), 3 (gerador de
relatório) e 4 (Constituição no prompt) — não têm arquivo próprio porque já estão
escritos ali. O item 2 (commits documentais) é este próprio commit.

## Regras que valem para todo pacote desta fila

- Nada é removido ou substituído — se uma instrução parecer exigir remoção, pare e
  pergunte.
- Nenhum teste existente pode ser alterado para um novo passar.
- Foto nunca é obrigatória, em nenhum caminho do Safety Walk.
- `git merge-base origin/main HEAD` batendo com a ponta de `origin/main` antes do
  primeiro commit de cada branch.
- Feito = clicado e visto funcionando em produção. Teste verde é estado intermediário.

## Nomenclatura interna desatualizada — não corrigida aqui de propósito

Os pacotes A/B/C e o PLANO citam, no próprio texto, `GENESIS/padroes/PADRAO-CORES.md` e
o pacote `GENESIS_2026-08-17_commit-padrao-cores.md`. Esses nomes foram corrigidos para
`PADRAO-SMX-CORES.md`/`PADRAO-SMX-DESIGN.md` (ver `ADR-023`, `ADR-024`, já mergeados) —
mas os pacotes aqui são cópia literal do que foi recebido, e reescrever o conteúdo para
"atualizar" contrariaria a própria regra de preservação histórica desta pasta. Quem for
executar o Pacote C usa a norma real (`PADRAO-SMX-CORES.md`) mesmo onde o texto do
pacote disser o nome antigo.
