# Padrão SMX de Design

**Caminho:** `GENESIS/padroes/PADRAO-SMX-DESIGN.md`
**Status:** vigente a partir de 17/08/2026
**Autoridade:** norma para toda superfície visual de todo projeto da SMX eXperience teCnollogy
**Adotado por:** ADR-023
**Companheiro:** `PADRAO-SMX-CORES.md` — este governa **como** se desenha; aquele, **com que cor**

> **Nota de nomenclatura (17/08/2026).** Este documento circulou brevemente como
> "Padrão Asimov". O nome estava errado. A Asimov Academy é **fonte do método**, do
> mesmo modo que a FM Global DS 8-21 é fonte dos controles de proteção contra
> incêndio usados na ronda: citada, creditada e seguida — mas a norma é da SMX, e o
> nome dela também.

---

## 1. A regra

> **Nenhuma interface é desenhada do zero. Toda interface parte de uma referência
> escolhida, cujo sistema de design foi extraído antes de qualquer pixel ser escrito.**

Vale para site, aplicativo, PWA, documento gerado, painel interno — qualquer coisa que
alguém vá olhar.

---

## 2. Fontes de referência

Nesta ordem de precedência:

| # | Fonte | O que é |
|---|---|---|
| 1 | **Banco SMX** | Referências já capturadas e extraídas, sob `GENESIS/padroes/referencias/` |
| 2 | **Aura.build** | Origem da maior parte do banco atual |
| 3 | **Mobbin** | Padrões de aplicativo |
| 4 | **Webflow / Dribbble** | Exploração visual |

O banco inicial veio do pacote **"Fundamentos de Vibe Design", da Asimov Academy**:
26 sites capturados e 21 sistemas já extraídos, divididos em temas escuros, temas
claros e componentes. Esse material é ponto de partida, não limite — referência nova
entra pelo **Site Downloader** (`github.com/asimov-academy/Site-Downloader-2.0`), que
captura réplica de site inclusive com JS complexo.

**Baixou, extrai. Extraiu, entra no banco.** Referência não extraída não conta como
referência: vira inspiração vaga, que é exatamente o que esta norma existe para
impedir.

---

## 3. Dois modos. Confundir os dois foi o erro de 17/08

### Modo Extração — existe uma referência

Entrada: um HTML. Saída: arquivos novos ao lado dele, **sem modificar a entrada**.

| Passo | O que faz |
|---|---|
| 1 · Analisar | Ler tudo antes de escrever qualquer coisa: cor, gradiente, sombra, fonte, escala, animação, componente, layout, efeito, asset |
| 2 · Extrair CSS | Cada `<style>` vira `assets/css/[nome-funcional].css`. Nomear por função, não por origem |
| 3 · Extrair JS | Cada `<script>` com código vira `assets/js/[nome-funcional].js`. Não extrair `ld+json` nem handler de uma linha |
| 4 · Classificar SVG | **A** ícone de biblioteca → `<i data-lucide="nome">` · **B** usa `currentColor` → fica inline, minificado numa linha · **C** só cor fixa → vira arquivo `.svg` com `<img>`. **Na dúvida entre B e C, sempre B** |
| 5 · Escrever | `design-system.html` do zero, não cópia editada. Fidelidade pixel a pixel |
| 6 · `STACK.md` | Uma linha por tecnologia encontrada: nome + o que faz ali. Sem categoria, sem enfeite, sem inventar o que não está no fonte |

### Modo Criação — não existe referência ainda

É onde os produtos da SMX estão. Não há site anterior para extrair, então o método de
extração não se aplica direto — mas **a regra continua valendo**.

Ordem obrigatória:

1. Escolher 2 a 4 referências do banco **pelo problema**, não pela aparência — uma IDE
   se parece com uma ferramenta de desenvolvedor, não com um portfólio
2. Extrair o sistema de cada uma, ou ler o `design-system.html` já pronto quando houver
3. **Nomear o que se toma emprestado e o que se recusa, com motivo**
4. Compor. Só aqui se escreve pixel

**Recusar uma referência é permitido. Recusar sem citá-la, não.** Se o banco tem um
exemplo do mesmo gênero e a decisão foi contra ele, o documento diz qual era e por quê.

---

## 4. Estrutura de um `design-system.html`

Nesta ordem, com **navegação horizontal fixa no topo** e âncora por seção:

| # | Seção | Conteúdo |
|---|---|---|
| 0 | **Hero** | Clone exato do hero original. Única mudança permitida: o texto, apresentando o próprio sistema |
| 1 | **Tipografia** | Tabela de especificação. Nome do estilo · amostra viva com o elemento e as classes originais · medida à direita no formato `40px / 48px` |
| 2 | **Cores e superfícies** | Fundos, bordas, divisórias, sobreposições, gradientes como amostra + contexto de uso |
| 3 | **Componentes** | Só os que existem. Estados lado a lado: padrão / hover / ativo / foco / desabilitado |
| 4 | **Layout e espaçamento** | Contêineres, grades, colunas, respiro de seção. Dois ou três padrões reais |
| 5 | **Movimento** | Toda animação presente, com galeria demonstrando cada classe |
| 6 | **Ícones** | Mesmo sistema, variantes de tamanho, herança de cor. **Omitir a seção se não houver ícones** |

Regras duras:

- **Não redesenhar nem inventar estilo.** Reusar nome de classe, animação, tempo e
  curva exatos
- **Se um estilo não é usado na referência, não entra no documento**
- O arquivo se explica pela estrutura — seção *é* documentação
- Todo texto visível em **PT-BR**. Nunca traduzir código, nome de classe, caminho de
  asset ou identificador técnico
- Sem linha em branco desnecessária, atributo vazio ou asset não usado

---

## 5. Encaixe no GENESIS

| Papel | Faz |
|---|---|
| **Arquiteto** | Escolhe as referências. É decisão de produto, não de engenharia |
| **Engenheiro** | Extrai, documenta, produz `design-system.html` + `STACK.md`, nomeia o que foi recusado |
| **Builder** | Porta para o código e commita. Único canal de escrita no GitHub |

Portões:

- Nenhum PR de interface abre sem `design-system.html` correspondente
- Nenhum `design-system.html` é aceito sem `STACK.md` ao lado
- **Feito continua sendo feito:** clicado e visto funcionando em produção. Documento
  de design bonito não é entrega

---

## 6. Onde o trabalho de 17/08 descumpriu esta norma

Registro honesto. O padrão nasceu de um erro concreto e o exemplo é o que o torna útil.

| Exigência | O que aconteceu |
|---|---|
| Consultar o banco antes de desenhar | **Não foi feito** — o material ficou fechado; só os dois prompts de método foram lidos |
| Escolher referências pelo problema | **Não foi feito** — o desenho saiu do código do Safety Walk |
| Nomear referência recusada | Feito só depois de o Arquiteto perguntar |
| Seção Layout e espaçamento | Ausente · corrigido em 17/08 |
| Seção Ícones | Ausente · corrigido em 17/08 |
| Navegação com âncoras | Ausente · corrigido em 17/08 |
| `STACK.md` | Ausente · corrigido em 17/08 |
| Tipografia como tabela de especificação | Corrigido em 17/08 |
| Galeria de movimento | Corrigido em 17/08 |
| Componentes com estados | **Parcial** — falta hover / foco / desabilitado |

**A consequência mais concreta:** a tipografia proposta era Archivo em largura
expandida, peso 800. Nenhuma das 26 referências do banco usa display acima de peso
600, e todas usam entreletra apertada. Era invenção — exatamente o que o item 3 da
seção 4 proíbe. Corrigida para Manrope 500/600.

**Pendência aberta:** refazer a referência dos produtos em modo criação correto —
escolher no banco, extrair, nomear recusas, compor.

---

## 7. Relação com o Padrão SMX de Cores

Este documento **não decide cor**. Ele decide método.

`PADRAO-SMX-CORES.md` decide cor, e as duas normas se cruzam num ponto: quando uma
referência traz uma cor que não passa no portão de matiz do padrão de cores, **a cor
não entra** — o que se toma emprestado da referência é a estrutura, o movimento e o
espaçamento, nunca a paleta.

**Referência dá vocabulário. Não dá identidade.**

Exemplo real, de 17/08: uma referência do banco no mesmo gênero da LUNA — produto de
observabilidade de LLM — usa vidro com desfoque de 50px e três blobs coloridos
animados. Foi recusada, com motivo registrado: a superfície ficaria com a cor do blob
que passou por baixo, cor que ninguém escolheu, e isso quebra a regra de que
superfície é translucidez sobre um fundo definido. A profundidade veio de outra
referência do próprio banco, que usa luz branca a 3,5% em `mix-blend-mode: screen` —
mesmo efeito, sem cor emprestada.

---

## Anexo — fontes creditadas

| Fonte | O que forneceu |
|---|---|
| **Asimov Academy** — curso "Fundamentos de Vibe Design" | O método de extração em seis passos, a estrutura de sete seções do `design-system.html`, o banco inicial de 26 referências e 21 sistemas extraídos, e a ferramenta Site Downloader |
| **Aura.build** | Origem da maior parte das referências do banco |
| **Mobbin** | Padrões de aplicativo |
| **Webflow · Dribbble** | Exploração visual |

Crédito é obrigação, não cortesia: quem for auditar uma decisão de design daqui a um
ano precisa poder chegar na fonte.
